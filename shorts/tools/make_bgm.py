"""参考元（よねあぷ）風のBGMを合成する。曲の流用ではなく、同じ「作り」の音を自前で作る。
- 純音（サイン波）の和音パッド：少しずらした2本で、ゆっくりうなる。ハ長調、約3秒ごとに和音が変わる。
- 低いサイン波のベース（和音の根音）。
- ときどき鳴る、高いベルの音（すぐ減衰）。
usage: python3 tools/make_bgm.py out.wav 秒数 [明るくする秒] [seed]"""
import sys
import wave

import numpy as np

SR = 44100
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
CHORDS = {"C": ("C", "E", "G"), "Am": ("A", "C", "E"), "G": ("G", "B", "D"), "F": ("F", "A", "C"),
          "Em": ("E", "G", "B"), "Dm": ("D", "F", "A")}
PROG = ["C", "Am", "G", "F", "C", "Am", "Em", "F", "Dm", "G", "C", "Am", "F", "G", "Em", "Am"]


def hz(name, octave):
    return 440.0 * 2 ** ((NOTE[name] + 12 * (octave + 1) - 69) / 12)


def make(total, bright_at=None, seed=1, chord_sec=3.0):
    r = np.random.default_rng(seed)
    n = int(total * SR) + SR
    t = np.arange(n) / SR
    out = np.zeros(n)
    k = 0
    t0 = 0.0
    while t0 < total + chord_sec:
        ch = CHORDS[PROG[k % len(PROG)]]
        root = ch[0]
        a, b = int(max(0, t0 - 0.15) * SR), min(n, int((t0 + chord_sec + 0.2) * SR))
        if a >= b:
            break
        tt = t[a:b] - t0
        # なめらかに入って抜ける（前後の和音と重ねる）
        envp = np.clip((tt + 0.15) / 0.3, 0, 1) * np.clip((chord_sec + 0.2 - tt) / 0.35, 0, 1)
        envp = envp * envp * (3 - 2 * envp)
        bright = bright_at is not None and t0 >= bright_at
        pad = np.zeros(b - a)
        for i, nm in enumerate(ch):
            for octv, g in ((4, 0.22), (5, 0.10 if not bright else 0.16)):
                f = hz(nm, octv)
                pad += g * (np.sin(2 * np.pi * f * tt) + np.sin(2 * np.pi * f * 1.0012 * tt + i))
        out[a:b] += pad * envp * 0.5
        # ベース（2オクターブ目の根音、和音の頭で少し強く）
        fb = hz(root, 2)
        envb = envp * (0.75 + 0.25 * np.exp(-np.maximum(tt, 0) * 1.5))
        out[a:b] += 0.42 * np.sin(2 * np.pi * fb * tt) * envb
        # ベル（和音の音を高い音域でぽつぽつ）
        hits = []
        if r.random() < (0.8 if bright else 0.5):      # 和音の頭で上がっていくアルペジオ
            seq = [(nm, 5) for nm in ch] + [(ch[0], 6), (ch[1], 6)]
            for j, (nm, o) in enumerate(seq[: int(r.integers(3, 6))]):
                hits.append((0.1 + j * 0.16, hz(nm, o)))
        for bt in np.arange(1.0, chord_sec, 0.375):
            if r.random() < (0.35 if bright else 0.18):
                hits.append((bt, hz(ch[r.integers(0, 3)], int(r.choice([5, 6])))))
        for bt, f in hits:
            if True:
                s = int((t0 + bt) * SR)
                L = int(1.2 * SR)
                if s + L >= n:
                    continue
                u = np.arange(L) / SR
                bell = (np.sin(2 * np.pi * f * u) + 0.25 * np.sin(2 * np.pi * f * 2.0 * u)) * np.exp(-u * 6.0)
                bell *= np.minimum(1, u / 0.004)
                out[s:s + L] += bell * r.uniform(0.10, 0.18)
        t0 += chord_sec
        k += 1
    out = out[: int(total * SR)]
    # 全体のフェードと音量
    fade = int(1.5 * SR)
    out[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    out[-fade:] *= np.linspace(1, 0, fade)
    return out / np.abs(out).max() * 0.8


def main():
    path, total = sys.argv[1], float(sys.argv[2])
    bright = float(sys.argv[3]) if len(sys.argv) > 3 else None
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    y = make(total, bright, seed)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((y * 32767).astype(np.int16).tobytes())
    print("wrote", path)


if __name__ == "__main__":
    main()
