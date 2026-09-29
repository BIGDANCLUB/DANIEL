#!/usr/bin/env python3
"""Gemini TTS で台本の各行を読み上げ、行ごとの WAV を作る。

- APIキーは環境変数 GEMINI_API_KEY から読む
- 生成した音声は voice_dir/NN.wav に保存し、文・声・指示が同じなら再生成しない
- キーが無くても、AI Studio などで作った音声を voice_dir/NN.wav に置けばそれを使う

usage:
  python3 tts_gemini.py story.json            # 足りない行だけ生成
  python3 tts_gemini.py story.json --force    # 全行作り直し
  python3 tts_gemini.py --list-models         # 使える TTS モデル名を確認
"""
import base64
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import wave

API = "https://generativelanguage.googleapis.com/v1beta"
DEFAULTS = {
    "model": "gemini-2.5-flash-preview-tts",
    "voice": "Sulafat",
    "style": "次の日本語を、70代の女性が静かに身の上を語るように、落ち着いた温かい声で、ややゆっくり読み上げてください。",
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


def _key(tc, text):
    return hashlib.sha1(json.dumps([tc["model"], tc["voice"], tc["style"], text]).encode()).hexdigest()


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
            if e.code in (429, 500, 503) and attempt < 5:
                wait = 2 ** attempt * 5
                print(f"  {e.code} → {wait}s 待って再試行", flush=True)
                time.sleep(wait)
                continue
            sys.exit(f"Gemini API エラー {e.code}: {msg[:500]}")


def synthesize(tc, text, out):
    body = {
        "contents": [{"parts": [{"text": f"{tc['style']}\n{text}" if tc["style"] else text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": tc["voice"]}}},
        },
    }
    res = _request(f"models/{tc['model']}:generateContent", body)
    part = res["candidates"][0]["content"]["parts"][0]["inlineData"]
    pcm = base64.b64decode(part["data"])
    rate = int(re.search(r"rate=(\d+)", part.get("mimeType", "")).group(1)) if "rate=" in part.get("mimeType", "") else 24000
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm)


def ensure_voice(story_path, force=False):
    cfg = json.load(open(story_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(story_path))
    tc = tts_config(cfg)
    manifest_path = os.path.join(base, tc["voice_dir"], "manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}
    for i, line in enumerate(cfg["lines"]):
        if "audio" in line:
            continue
        out = wav_path(cfg, base, i)
        text = spoken(line)
        k = _key(tc, text)
        name = os.path.basename(out)
        # 手で置いたファイル（manifest に無い）はそのまま使う
        if os.path.exists(out) and not force and manifest.get(name, k) == k:
            continue
        print(f"[{i + 1:02d}] {text}", flush=True)
        synthesize(tc, text, out)
        manifest[name] = k
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        json.dump(manifest, open(manifest_path, "w"), ensure_ascii=False, indent=1)


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
