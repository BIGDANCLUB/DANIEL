"""読み上げ型ショート（画面も参考どおり：線がゆれる・猫大きめで重なってよい・字幕は下まん中で日本青/世界赤・背景が横に流れる）
（11/22 ユーザー指定：ベンチマーク「真面目過ぎる人の末路」の読み上げ形式だけまねる）。

ずんだもん（VOICEVOX）が「札＋先に出る側」→ その字幕 →「後に出る側」→ その字幕 を間をあけずに読む。
場面の長さは読み上げの長さに合わせる（59.9秒にしない）。猫の鳴き声は消して、効果音と読み上げだけ。
- 台本：scripts/short_<名前>_yomiage_zundamon.txt（00＝頭のひと言（なくてよい・11/22 132は「おい！」なし）、そのあと1段につき4行）
- 声：tools/zunda_tts.py（/home/user/vv の VOICEVOX 公式一式）
- 概要欄に「VOICEVOX:ずんだもん」を必ず書く
"""
import os
import subprocess
import wave

import numpy as np

import world_short as Wd

SR = 24000
GAP = 0.06   # 読み上げどうしのすき間（ほぼ間をあけない）


def wav(path):
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768, w.getframerate()


def build(name, st, rows, heads, band, script, speed=1.25, target=None):
    vdir = os.path.join(Wd.HERE, "out", "voice_" + name)
    subprocess.run(["python3", os.path.join(Wd.HERE, "tools", "zunda_tts.py"), script, vdir, str(speed)], check=True)
    v = {f[:-4]: wav(os.path.join(vdir, f))[0] for f in os.listdir(vdir) if f.endswith(".wav")}
    L = {k: len(a) / SR for k, a in v.items()}
    cs, plan = [], []   # plan: (カット番号, 声の番号, カット内の開始秒)
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        n = [("%02d" % (k * 4 + i + 1)) for i in range(4)]
        big = k >= len(rows) - 3
        head = ["00"] if k == 0 and "00" in v else []   # 00＝頭のひと言（台本にあるときだけ）
        da = sum(L[h] + GAP for h in head) + L[n[0]] + GAP
        a = Wd.split(st, lv, dur=da, se=["explosion_chudoon"] if big else ["pi"])
        b = Wd.split(st, lv, right=wcat, cap=wcap, cap_side="R", sound=None, dur=L[n[1]] + 0.25, se="don_hit")
        c = Wd.split(st, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound=None, dur=L[n[2]] + GAP + L[n[3]] + 0.35)
        t = 0.0
        for h in head + [n[0]]:
            plan.append((len(cs), h, t))
            t += L[h] + GAP
        plan.append((len(cs) + 1, n[1], 0.05))
        plan.append((len(cs) + 2, n[2], 0.0))
        plan.append((len(cs) + 2, n[3], L[n[2]] + GAP))
        cs += [a, b, c]
    if target:   # 足りない分は、字幕が出ているカット（右・左）の読み終わりのあとの間として均等に足す
        caps = [c for i, c in enumerate(cs) if i % 3]
        extra = (target - sum(c["dur"] for c in cs)) / len(caps)
        for c in caps:
            c["dur"] += extra
    t0 = 0.0
    for c in cs:
        c.update(blur=9, band_y=0, tag_y=460, free_len=True, heads=heads, ref=True, t0=t0)   # ref：参考どおりの画面（11/22）
        t0 += c["dur"]
        for q in c["cats"]:   # 猫は大きめ・少し重なってよい
            q.update(h=860, w=660, bottom=1500, x=330 if q["x"] < 540 else 750)
        c["cats"].sort(key=lambda q: q["x"] < 540)   # 後から出る左（日本）を右の猫の上に重ねる（11/22 ユーザー指定）
    Wd.hai_extend = lambda x: x   # 猫は鳴かないので、鳴くまで場面をのばす処理はしない（読み上げとずれるため）
    out = os.path.join(Wd.HERE, "out", "short_%s.mp4" % name)
    raw = out.replace(".mp4", "_noVoice.mp4")
    Wd.run(cs, band, raw, out.replace(".mp4", "_preview"))
    starts = np.cumsum([0] + [c["dur"] for c in cs])
    total = starts[-1]
    track = np.zeros(int((total + 1) * SR), np.float32)
    for ci, key, off in plan:
        s = int((starts[ci] + off) * SR)
        track[s:s + len(v[key])] += v[key][: len(track) - s]
    vw = out.replace(".mp4", "_voice.wav")
    with wave.open(vw, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(track * 1.0, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", raw, "-i", vw, "-filter_complex",
                    "[0:a]volume=0.55[a0];[1:a]volume=1.6[a1];[a0][a1]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out], check=True)
    print("->", out, round(total, 1))
