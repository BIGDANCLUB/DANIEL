"""作り方シリーズのナレーション（VOICEVOX）。台本の行ごとに声を作り、59.9秒に収まる読みの速さを探して、行ごとの開始時刻を返す。
usage: python3 voice.py himeji   →  himeji/voice/line_XX.wav と himeji/voice/timing.json"""
import importlib
import io
import json
import os
import sys
import urllib.parse
import urllib.request
import wave

import numpy as np

URL = os.environ.get("VOICEVOX_URL", "http://127.0.0.1:50021")
SR = 24000


def post(path, data=None, params=None):
    q = urllib.parse.urlencode(params or {})
    req = urllib.request.Request(f"{URL}{path}?{q}", data=json.dumps(data).encode() if data is not None else b"",
                                 method="POST", headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=120).read()


def synth(text, speaker, speed, kana=None, pitch=0.0, intonation=1.15):
    if kana:
        q = json.loads(post("/accent_phrases", None, {"text": kana, "speaker": speaker, "is_kana": "true"}))
        aq = json.loads(post("/audio_query", None, {"text": text, "speaker": speaker}))
        aq["accent_phrases"] = q
    else:
        aq = json.loads(post("/audio_query", None, {"text": text, "speaker": speaker}))
    aq.update(speedScale=speed, pitchScale=pitch, intonationScale=intonation, prePhonemeLength=0.02, postPhonemeLength=0.04,
              outputSamplingRate=SR, outputStereo=False)
    wav = post("/synthesis", aq, {"speaker": speaker})
    with wave.open(io.BytesIO(wav)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    nz = np.where(np.abs(x) > 0.01)[0]          # 前後の無音を切る
    if len(nz):
        x = x[max(0, nz[0] - 200): nz[-1] + 400]
    morae = sum(len(p["moras"]) for p in aq["accent_phrases"])
    return x, morae


def build(name):
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, name))
    S = importlib.import_module("script")
    out = os.path.join(here, name, "voice")
    os.makedirs(out, exist_ok=True)
    budget = S.TOTAL - S.LEAD - S.TAIL
    speed = 1.15
    for _ in range(8):
        clips = [synth(L["text"], S.SPEAKER, speed, L.get("kana"), getattr(S, "PITCH", 0.0), getattr(S, "INTONATION", 1.15))
                 for L in S.LINES]
        total = sum(len(c[0]) for c in clips) / SR + S.GAP * (len(clips) - 1)
        print(f"speed {speed:.3f} → {total:.2f}s (budget {budget:.2f}s)", flush=True)
        if abs(total - budget) < 0.15:
            break
        speed *= total / budget
    morae = sum(c[1] for c in clips)
    t = S.LEAD
    timing = []
    for k, (L, (x, m)) in enumerate(zip(S.LINES, clips)):
        p = os.path.join(out, f"line_{k:02d}.wav")
        with wave.open(p, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
        d = len(x) / SR
        timing.append(dict(L, start=round(t, 3), dur=round(d, 3), wav=p))
        t += d + S.GAP
    # 余りは最後の間（TAIL）に足す。足りなければ GAP を詰める
    json.dump(dict(speed=speed, morae=morae, voice_end=round(t - S.GAP, 3), lines=timing), open(os.path.join(out, "timing.json"), "w"),
              ensure_ascii=False, indent=1)
    print(f"done: speed {speed:.3f}, {morae} morae, {morae / (t - S.LEAD):.1f} morae/s, voice ends {t - S.GAP:.2f}s")


def refit(name):
    """声だけ替える：今の timing.json の行ごとの頭と長さはそのままにして、新しい声を行ごとに同じ長さで読ませる（映像の作り直しがいらない）。
    VOICEVOX の速さ（speedScale）を行ごとに合わせ、残りのわずかな差は前後の無音で埋めるか、ごく少し縮める。"""
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, name))
    S = importlib.import_module("script")
    out = os.path.join(here, name, "voice")
    tj = os.path.join(out, "timing.json")
    T = json.load(open(tj))
    pitch, inton = getattr(S, "PITCH", 0.0), getattr(S, "INTONATION", 1.15)
    morae = 0
    for k, (L, old) in enumerate(zip(S.LINES, T["lines"])):
        target = old["dur"]
        sp = T["speed"]
        for _ in range(8):                                 # 目標の長さより 0〜0.04秒 短くなる速さを探す（足りない分はうしろを無音で埋める）
            x, m = synth(L["text"], S.SPEAKER, sp, L.get("kana"), pitch, inton)
            d = len(x) / SR
            if target - 0.04 <= d <= target:
                break
            sp *= d / (target - 0.02)
        n = int(round(target * SR))
        x = x[:n] if len(x) > n else np.concatenate([x, np.zeros(n - len(x), np.float32)])
        f = int(0.012 * SR)                                # 終わりを少しだけ弱めて、切れた音のプツッを防ぐ
        x[-f:] *= np.linspace(1, 0, f, dtype=np.float32)
        morae += m
        with wave.open(os.path.join(out, f"line_{k:02d}.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
        print(f"{k:02d} speed {sp:.3f} {d:.2f}s → {target:.2f}s  {L['text']}", flush=True)
    T.update(speaker=S.SPEAKER, morae=morae)
    json.dump(T, open(tj, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    if "--keep-timing" in sys.argv:
        refit(sys.argv[1])
    else:
        build(sys.argv[1])
