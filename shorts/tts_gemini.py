#!/usr/bin/env python3
"""Gemini TTS で台本の各行を読み上げ、行ごとの WAV を作る。

- APIキーは環境変数 GEMINI_API_KEY から読む
- 生成した音声は voice_dir/NN.wav に保存し、文・声・指示が同じなら再生成しない
- キーが無くても、AI Studio などで作った音声を voice_dir/NN.wav に置けばそれを使う

- 複数行をまとめて1回で読ませ、文の間の無音で行ごとに切り分ける（API 回数を節約。tts.batch 行ずつ、既定5）。
  切り分けが文字数の比率と合わなければ、そのまとまりだけ1行ずつ作り直す

usage:
  python3 tts_gemini.py story.json            # 足りない行だけ生成
  python3 tts_gemini.py story.json --force    # 全行作り直し
  python3 tts_gemini.py --list-models         # 使える TTS モデル名を確認
"""
import base64
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import wave

import numpy as np

API = "https://generativelanguage.googleapis.com/v1beta"
DEFAULTS = {
    "model": "gemini-3.8-flash-tts",
    "voice": "Sulafat",
    # 人物像・場面・演技指示。行ごとの "tone"（その一文の気持ち）が後ろに付く
    "style": ("# AUDIO PROFILE\n72歳の日本人女性。穏やかで温かい声。\n"
              "## THE SCENE\n自分の身に起きた出来事を、目の前の人に打ち明けるように語っている。\n"
              "### DIRECTOR'S NOTES\n棒読みにせず、感情をこめて抑揚をはっきりつける。数字は少し強調する。"),
    "voice_dir": "voice",
}


def spoken(line):
    """読み上げる文。say があればそれ、無ければ字幕から強調記号と改行を除いたもの。"""
    if line.get("say"):
        return line["say"]
    return re.sub(r"[{}<>\[\]\n]", "", line["text"])


def tts_config(cfg):
    return {**DEFAULTS, **cfg.get("tts", {})}


def wav_path(cfg, base, i):
    return os.path.join(base, tts_config(cfg)["voice_dir"], f"{i + 1:02d}.wav")


def _key(tc, text, tone=None):
    return hashlib.sha1(json.dumps([tc["model"], tc["voice"], tc["style"], text, tone]).encode()).hexdigest()


def build_prompt(tc, text, tone=None):
    """指示（人物像・気持ち）と読み上げ文を分けて渡す。区切らないと指示まで読み上げてしまう。"""
    if not tc["style"]:
        return text
    head = tc["style"] + (f"この一文の気持ち：{tone}" if tone else "")
    return f"{head}\n指示文は読まず、TRANSCRIPT の日本語だけを読み上げること。\n#### TRANSCRIPT\n{text}"


def _request(path, body=None):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY が設定されていません（環境変数に登録してください）")
    req = urllib.request.Request(f"{API}/{path}", data=json.dumps(body).encode() if body else None,
                                 headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code == 429 and "per_day" in msg:
                # 1日の上限はしばらく空かないので、やり直さずに止める（失敗も回数に数えられるため）
                sys.exit("Gemini API の1日の上限に達しました（" + (re.search(r"model: ([\w.-]+)", msg) or [None, "?"])[1]
                         + "）。上限が空いてから再実行してください")
            if e.code in (429, 500, 503) and attempt < 5:
                wait = 2 ** attempt * 5
                print(f"  {e.code} → {wait}s 待って再試行", flush=True)
                time.sleep(wait)
                continue
            sys.exit(f"Gemini API エラー {e.code}: {msg[:500]}")


def _tts(tc, prompt):
    """プロンプトを読ませて (PCM16 bytes, rate) を返す。"""
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": tc["voice"]}}},
        },
    }
    res = _request(f"models/{tc['model']}:generateContent", body)
    part = res["candidates"][0]["content"]["parts"][0]["inlineData"]
    pcm, ch, width, rate = decode_audio(base64.b64decode(part["data"]), part.get("mimeType", ""))
    assert ch == 1 and width == 2, (ch, width)
    return pcm, rate


def _write(out, pcm, rate):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm)


def synthesize(tc, text, out, tone=None):
    pcm, rate = _tts(tc, build_prompt(tc, text, tone))
    _write(out, pcm, rate)


def build_batch_prompt(tc, items):
    """複数の文をまとめて読ませるプロンプト。文ごとの気持ちは指示側に並べ、読み上げ部分は文だけにする。"""
    notes = "\n".join(f"・「{t}」…{tone or '自然に'}" for t, tone in items)
    head = (tc["style"] + "\n各文の気持ち（この順に読む）:\n" + notes +
            "\n文と文の間は、はっきり1秒ほど間をあけること。文の途中では長い間をあけないこと。"
            "\n指示文は読まず、TRANSCRIPT の日本語だけを、1行ずつ順番に読み上げること。")
    return head + "\n#### TRANSCRIPT\n" + "\n".join(t for t, _ in items)


def split_by_pauses(pcm, rate, texts):
    """まとめて読んだ音声を、文の数に合わせて無音部分で切り分ける。
    候補の無音から、文字数の比率で予想される切れ目に最も近く・長い無音を選ぶ（動的計画法）。
    うまく切れなければ None。"""
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    n = len(texts)
    if n == 1:
        return [pcm]
    win = int(0.01 * rate)
    frames = len(a) // win
    db = 20 * np.log10(np.sqrt((a[:frames * win].reshape(frames, win) ** 2).mean(1)) + 1e-9)
    loud = np.where(db > -35)[0]
    if len(loud) == 0:
        return None
    s0, s1 = loud[0], loud[-1] + 1                     # 声のある範囲（10ms単位）
    quiet = db < -35
    gaps = []                                           # (中心, 長さ) 10ms単位
    i = s0
    while i < s1:
        if quiet[i]:
            j = i
            while j < s1 and quiet[j]:
                j += 1
            if j - i >= 15:                             # 0.15秒以上の無音だけ候補
                gaps.append(((i + j) // 2, j - i))
            i = j
        else:
            i += 1
    if len(gaps) < n - 1:
        return None
    w = np.array([len(re.sub(r"[、。！？!?「」\s]", "", t)) + 1 for t in texts], float)
    expect = s0 + (s1 - s0) * np.cumsum(w)[:-1] / w.sum()   # 予想される切れ目
    span = s1 - s0
    # dp[k][g]: k番目の切れ目に候補 g を使ったときの最小コスト
    INF = 1e18
    G = len(gaps)
    cost = [[INF] * G for _ in range(n - 1)]
    prev = [[-1] * G for _ in range(n - 1)]
    for g, (c, L) in enumerate(gaps):
        cost[0][g] = abs(c - expect[0]) / span * 10 - min(L, 120) / 100
    for k in range(1, n - 1):
        for g, (c, L) in enumerate(gaps):
            local = abs(c - expect[k]) / span * 10 - min(L, 120) / 100
            for h in range(g):
                if cost[k - 1][h] + local < cost[k][g]:
                    cost[k][g] = cost[k - 1][h] + local
                    prev[k][g] = h
    g = int(np.argmin(cost[n - 2]))
    if cost[n - 2][g] >= INF / 2:
        return None
    cuts = []
    for k in range(n - 2, -1, -1):
        cuts.append(gaps[g][0])
        g = prev[k][g]
    cuts = sorted(cuts)
    bounds = [0] + [c * win for c in cuts] + [len(a)]
    parts = [pcm[bounds[i] * 2:bounds[i + 1] * 2] for i in range(n)]
    # 検証: 各文の長さが文字数の比率から大きく外れていないか
    dur = np.array([len(p) / 2 / rate for p in parts])
    exp = (s1 - s0) * 0.01 * w / w.sum()
    ratio = dur / np.maximum(exp, 0.3)
    if (ratio < 0.45).any() or (ratio > 2.2).any():
        return None
    return parts


def plausible(pcm, rate, text):
    """文字数に対して長すぎる音声（指示文や別の文まで読んだもの）を弾く。普通の読みは1文字0.2秒前後。"""
    chars = len(re.sub(r"[、。！？!?「」<>{}\s]", "", text))
    return len(pcm) / 2 / rate <= chars * 0.4 + 2.0


def decode_audio(data, mime=""):
    """API の音声を (PCM, ch, 幅, rate) に。2.5 系は生PCM（audio/L16）、3.x 系は WAV ファイル丸ごと。
    WAV を生PCMとして扱うと、ヘッダが頭の「プチッ」、末尾のメタデータが「ザッ」というノイズになる。"""
    if data[:4] == b"RIFF":
        with wave.open(io.BytesIO(data)) as src:
            return src.readframes(src.getnframes()), src.getnchannels(), src.getsampwidth(), src.getframerate()
    m = re.search(r"rate=(\d+)", mime)
    return data, 1, 2, int(m.group(1)) if m else 24000


def ensure_voice(story_path, force=False):
    cfg = json.load(open(story_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(story_path))
    tc = tts_config(cfg)
    manifest_path = os.path.join(base, tc["voice_dir"], "manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}
    todo = []                                           # 作る必要のある行
    for i, line in enumerate(cfg["lines"]):
        if "audio" in line:
            continue
        out = wav_path(cfg, base, i)
        k = _key(tc, spoken(line), line.get("tone"))
        # 手で置いたファイル（manifest に無い）はそのまま使う
        if os.path.exists(out) and not force and manifest.get(os.path.basename(out), k) == k:
            continue
        todo.append((i, line, out, k))

    def save(i, out, k, pcm, rate):
        _write(out, pcm, rate)
        manifest[os.path.basename(out)] = k
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        json.dump(manifest, open(manifest_path, "w"), ensure_ascii=False, indent=1)

    batch = int(tc.get("batch", 5))
    # 連続した行ごとに分け、それぞれを batch 行以下の均等なまとまりにする（例: 16行→4行×4）
    runs, cur = [], []
    for item in todo:
        if cur and item[0] != cur[-1][0] + 1:
            runs.append(cur)
            cur = []
        cur.append(item)
    if cur:
        runs.append(cur)
    groups = []
    for run in runs:
        n = -(-len(run) // batch)
        size = -(-len(run) // n)
        groups += [run[j:j + size] for j in range(0, len(run), size)]
    for grp in groups:
        texts = [spoken(l) for _, l, _, _ in grp]
        if len(grp) > 1:
            print(f"[{grp[0][0] + 1:02d}-{grp[-1][0] + 1:02d}] まとめて生成（{len(grp)}行）", flush=True)
            pcm, rate = _tts(tc, build_batch_prompt(tc, [(t, l.get("tone")) for t, (_, l, _, _) in zip(texts, grp)]))
            parts = split_by_pauses(pcm, rate, texts)
            if parts and not all(plausible(p, rate, t) for p, t in zip(parts, texts)):
                print("  文字数に対して長すぎる行あり", flush=True)
                parts = None
            if parts:
                for (i, l, out, k), p in zip(grp, parts):
                    save(i, out, k, p, rate)
                continue
            print("  切り分けに失敗 → 1行ずつ作り直します", flush=True)
        for (i, l, out, k), t in zip(grp, texts):
            print(f"[{i + 1:02d}] {t}", flush=True)
            for _ in range(3):
                pcm, rate = _tts(tc, build_prompt(tc, t, l.get("tone")))
                if plausible(pcm, rate, t):
                    break
                print("  長すぎるので作り直します", flush=True)
            save(i, out, k, pcm, rate)


def list_models():
    res = _request("models?pageSize=1000")
    for m in res.get("models", []):
        if "tts" in m["name"].lower():
            print(m["name"].split("/", 1)[1], "-", m.get("displayName", ""))


if __name__ == "__main__":
    if "--list-models" in sys.argv:
        list_models()
    else:
        ensure_voice(sys.argv[1], force="--force" in sys.argv)
