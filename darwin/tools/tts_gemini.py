"""① ナレーション生成：Gemini TTS で1文ずつ合成し、【】ごとの音声とタイムラインを作る。

  python tools/tts_gemini.py 01-keiba            # 本番（GEMINI_API_KEY が必要）
  python tools/tts_gemini.py 01-keiba --mock     # APIを使わず無音で尺だけ再現（動作確認用）
  python tools/tts_gemini.py 01-keiba --redo 03_seitai:1   # 特定の文だけ撮り直し
"""
import argparse
import array
import base64
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

from common import load_config, load_episode, out_dir, run_ffmpeg, save_json, wav_duration

RATE = 24000  # Gemini TTS は 24kHz / 16bit / mono の PCM を返す


def write_wav(path, pcm, rate=RATE):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm)


def read_pcm(path):
    with wave.open(str(path), "rb") as w:
        if (w.getnchannels(), w.getsampwidth(), w.getframerate()) != (1, 2, RATE):
            sys.exit(f"想定外のwav形式です（24kHz/16bit/mono以外）: {path}")
        return w.readframes(w.getnframes())


def tighten(pcm, g):
    """前後の無音を削り、文中の長すぎる間を max_pause 秒に詰める（API は呼ばない）。"""
    if not g.get("trim_silence", True):
        return pcm
    samples = array.array("h", pcm)
    win = RATE // 100  # 10ms
    thr = int(32767 * 10 ** (g.get("silence_db", -40) / 20))
    loud = [max(map(abs, samples[i:i + win]), default=0) > thr for i in range(0, len(samples), win)]
    if not any(loud):
        return pcm
    first = loud.index(True)
    last = len(loud) - 1 - loud[::-1].index(True)
    keep_pad = 3                                   # 前後に 30ms だけ残す
    max_gap = int(g.get("max_pause", 0.45) * 100)  # 窓の数
    out = array.array("h")
    run = 0
    for w in range(max(0, first - keep_pad), min(len(loud), last + 1 + keep_pad)):
        chunk = samples[w * win:(w + 1) * win]
        if loud[w]:
            run = 0
            out.extend(chunk)
        else:
            run += 1
            if run <= max_gap:
                out.extend(chunk)
    return out.tobytes()


def process_line(raw_path, proc_path, g):
    """out/tts（API の生音声）→ out/tts_proc（無音カット・速度調整済み）。"""
    pcm = tighten(read_pcm(raw_path), g)
    tempo = float(g.get("tempo", 1.0))
    if abs(tempo - 1.0) < 1e-3:
        write_wav(proc_path, pcm)
        return
    tmp = proc_path.with_suffix(".tmp.wav")
    write_wav(tmp, pcm)
    run_ffmpeg(["-i", tmp, "-af", f"atempo={tempo:.4f}", "-ar", str(RATE), "-ac", "1", "-sample_fmt", "s16", proc_path])
    tmp.unlink()


def silence(sec):
    return b"\x00\x00" * int(round(sec * RATE))


def retry_delay(detail):
    """429 の本文から待つべき秒数を取る（RetryInfo の retryDelay か、本文の "retry in 9.6s"）。"""
    m = re.search(r'"retryDelay":\s*"([\d.]+)s"', detail) or re.search(r"retry in ([\d.]+)s", detail)
    return float(m.group(1)) if m else None


def build_request(text, style, g):
    if g["style_mode"] == "metadata":
        # gemini-3.8 系：話し方の指示を speech_metadata で渡す（読み上げには含まれない）
        part = {"text": text, "speech_metadata": {"style": style}}
        voice = {"voice": g["voice"]}
    else:
        # 旧来の方式：指示文を本文の前に書く
        part = {"text": f"{style}で読み上げてください：\n{text}"}
        voice = {"prebuiltVoiceConfig": {"voiceName": g["voice"]}}
    return {
        "contents": [{"role": "user", "parts": [part]}],
        "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": voice}},
    }


def synthesize(text, style, g, key):
    url = f"{g['api_base']}/models/{g['model']}:generateContent"
    body = json.dumps(build_request(text, style, g)).encode("utf-8")
    for attempt in range(10):
        req = urllib.request.Request(url, data=body, method="POST", headers={
            "Content-Type": "application/json", "x-goog-api-key": key})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                resp = json.load(r)
            break
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            if e.code in (429, 500, 502, 503, 504) and attempt < 9:
                wait = retry_delay(detail) if e.code == 429 else None
                wait = (wait + 2) if wait else min(60, 2 ** (attempt + 1))
                print(f"    {'回数制限' if e.code == 429 else f'エラー {e.code}'}のため {wait:.0f}秒待って再試行（{attempt + 1}/9）")
                time.sleep(wait)
                continue
            if e.code == 429 and "PerDay" in detail:
                sys.exit("Gemini TTS の1日あたりの無料枠を使い切りました。明日再実行するか、AI Studio で課金を有効にしてください。\n"
                         "（生成済みの文はスキップされるので、再実行すれば続きから作ります）")
            sys.exit(f"Gemini TTS エラー {e.code}: {detail[:800]}\n"
                     "※ 400 でリクエスト形式を指摘された場合は config.json の gemini.style_mode を \"prefix\" にしてください。")
    for part in resp.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        inline = part.get("inlineData") or part.get("inline_data")
        if inline:
            data = base64.b64decode(inline["data"])
            mime = inline.get("mimeType") or inline.get("mime_type") or ""
            if data[:4] == b"RIFF":  # wav で返ってきた場合
                with wave.open(io.BytesIO(data), "rb") as w:
                    return w.readframes(w.getnframes()), w.getframerate()
            m = re.search(r"rate=(\d+)", mime)
            return data, int(m.group(1)) if m else RATE
    sys.exit(f"音声が返ってきませんでした: {json.dumps(resp, ensure_ascii=False)[:800]}")


def audition(ep, ep_dir, g, key, voices, sample):
    sid, _, idx = sample.partition(":")
    sec = next((x for x in ep["sections"] if x["id"] == sid), None)
    if sec is None or not idx.isdigit() or not 1 <= int(idx) <= len(sec["lines"]):
        sys.exit(f"--sample-line の指定が不正です: {sample}（例: 01_basho:1）")
    line = sec["lines"][int(idx) - 1]
    style = f"{g['base_style']} 今回の文は「{line['emotion']}」：{g['emotions'].get(line['emotion'], line['emotion'])}。"
    dest = out_dir(ep_dir, "voice_samples")
    print(f"聞き比べ：「{line['text']}」")
    for v in voices:
        raw = dest / f"{v}_raw.wav"
        print(f"  {v} …")
        data, rate = synthesize(line.get("tts_text", line["text"]), style, {**g, "voice": v}, key)
        write_wav(raw, data, rate)
        process_line(raw, dest / f"{v}.wav", g)
        raw.unlink()
    print(f"\n保存先: {dest}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--mock", action="store_true", help="API を呼ばず est 秒の無音を作る")
    ap.add_argument("--redo", nargs="*", default=[], help="撮り直す文（例: 03_seitai:1）。all で全文")
    ap.add_argument("--lines", action="store_true", help="文ごとの長さも表示する")
    ap.add_argument("--audition", nargs="+", metavar="VOICE",
                    help="声の聞き比べ。指定した声で同じ1文を作り out/voice_samples/ に保存（本番の音声は変えない）")
    ap.add_argument("--sample-line", default="01_basho:1", help="聞き比べに使う文（既定 01_basho:1）")
    args = ap.parse_args()

    cfg = load_config()
    g = cfg["gemini"]
    ep_dir, ep = load_episode(args.episode)
    key = os.environ.get("GEMINI_API_KEY")
    if not args.mock and not key:
        sys.exit("環境変数 GEMINI_API_KEY が未設定です（動作確認だけなら --mock）。")

    if args.audition:
        audition(ep, ep_dir, g, key, args.audition, args.sample_line)
        return

    line_dir = out_dir(ep_dir, "tts")
    proc_dir = out_dir(ep_dir, "tts_proc")
    sec_dir = out_dir(ep_dir, "narration")
    timeline = {"sections": [], "total": 0.0}
    t = 0.0
    for sec in ep["sections"]:
        pcm = silence(g["section_head"])
        cursor = g["section_head"]
        lines_tl = []
        for i, line in enumerate(sec["lines"], 1):
            wav_path = line_dir / f"{sec['id']}_{i:02d}.wav"
            redo = "all" in args.redo or f"{sec['id']}:{i}" in args.redo
            if redo or not wav_path.exists():
                if args.mock:
                    write_wav(wav_path, silence(line["est"]))
                else:
                    style = f"{g['base_style']} 今回の文は「{line['emotion']}」：{g['emotions'].get(line['emotion'], line['emotion'])}。"
                    print(f"  TTS {sec['id']}:{i} ({line['emotion']}) {line['text']}")
                    data, rate = synthesize(line.get("tts_text", line["text"]), style, g, key)
                    if rate != RATE:
                        sys.exit(f"想定外のサンプルレート {rate}Hz です")
                    write_wav(wav_path, data)
            proc_path = proc_dir / wav_path.name
            process_line(wav_path, proc_path, g)
            raw_dur = wav_duration(wav_path)
            dur = wav_duration(proc_path)
            if i > 1:
                pcm += silence(g["line_gap"])
                cursor += g["line_gap"]
            pcm += read_pcm(proc_path)
            lines_tl.append({"index": i, "text": line["text"], "emotion": line["emotion"],
                             "start": round(t + cursor, 3), "duration": round(dur, 3), "raw": round(raw_dur, 3), "est": line["est"],
                             "cues": line.get("cues", [])})
            cursor += dur
        pcm += silence(g["section_tail"])
        sec_wav = sec_dir / f"{sec['id']}.wav"
        write_wav(sec_wav, pcm)
        dur = wav_duration(sec_wav)
        timeline["sections"].append({"id": sec["id"], "label": sec["label"], "start": round(t, 3),
                                     "duration": round(dur, 3), "lines": lines_tl})
        t += dur
    timeline["total"] = round(t, 3)
    save_json(Path(ep_dir, "out", "timeline.json"), timeline)

    if args.lines:
        print("\n文ごとの長さ（生音声 → 調整後 / 見積）")
        for s in timeline["sections"]:
            for l in s["lines"]:
                print(f"  {s['id']}:{l['index']}  {l['raw']:5.2f} → {l['duration']:5.2f}秒 / {l['est']:.1f}  {l['text'][:24]}")
    print(f"\n【】ごとの尺（無音カット {'あり' if g.get('trim_silence', True) else 'なし'}"
          f"・文中の間は最大 {g.get('max_pause', 0.45)}秒・速度 {g.get('tempo', 1.0)}倍）")
    for s in timeline["sections"]:
        est = sum(l["est"] for l in s["lines"])
        print(f"  {s['id']:<12} {s['label']:<8} {s['duration']:6.2f}秒  (見積 {est:.1f}秒)")
    print(f"  合計 {timeline['total']:.2f}秒")


if __name__ == "__main__":
    main()
