"""① ナレーション生成：Gemini TTS で1文ずつ合成し、【】ごとの音声とタイムラインを作る。

  python tools/tts_gemini.py 01-keiba            # 本番（GEMINI_API_KEY が必要）
  python tools/tts_gemini.py 01-keiba --mock     # APIを使わず無音で尺だけ再現（動作確認用）
  python tools/tts_gemini.py 01-keiba --redo 03_seitai:1   # 特定の文だけ撮り直し
"""
import argparse
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

from common import load_config, load_episode, out_dir, save_json, wav_duration

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


def silence(sec):
    return b"\x00\x00" * int(round(sec * RATE))


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
    for attempt in range(5):
        req = urllib.request.Request(url, data=body, method="POST", headers={
            "Content-Type": "application/json", "x-goog-api-key": key})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                resp = json.load(r)
            break
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(2 ** (attempt + 1))
                continue
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--mock", action="store_true", help="API を呼ばず est 秒の無音を作る")
    ap.add_argument("--redo", nargs="*", default=[], help="撮り直す文（例: 03_seitai:1）。all で全文")
    args = ap.parse_args()

    cfg = load_config()
    g = cfg["gemini"]
    ep_dir, ep = load_episode(args.episode)
    key = os.environ.get("GEMINI_API_KEY")
    if not args.mock and not key:
        sys.exit("環境変数 GEMINI_API_KEY が未設定です（動作確認だけなら --mock）。")

    line_dir = out_dir(ep_dir, "tts")
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
            dur = wav_duration(wav_path)
            if i > 1:
                pcm += silence(g["line_gap"])
                cursor += g["line_gap"]
            pcm += read_pcm(wav_path)
            lines_tl.append({"index": i, "text": line["text"], "emotion": line["emotion"],
                             "start": round(t + cursor, 3), "duration": round(dur, 3), "est": line["est"],
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

    print("\n【】ごとの尺（実測）")
    for s in timeline["sections"]:
        est = sum(l["est"] for l in s["lines"])
        print(f"  {s['id']:<12} {s['label']:<8} {s['duration']:6.2f}秒  (見積 {est:.1f}秒)")
    print(f"  合計 {timeline['total']:.2f}秒")


if __name__ == "__main__":
    main()
