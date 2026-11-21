"""作り方シリーズ用の和風BGM（オリジナル）。参考元の BGM を計測した特徴に合わせる：
テンポ 117 BPM、レ・ファ・ソ・ラ・ドの5音（和風の音階）、低い太鼓の拍、シャカシャカした高い音、明るく軽快。
usage: python3 make_bgm_wafu.py out.wav [秒数=62] [seed=1]"""
import sys
import wave

import numpy as np

SR = 44100
BPM = 117.0
BEAT = 60.0 / BPM
SCALE = [62, 65, 67, 69, 72, 74, 77, 79, 81, 84]          # レ ファ ソ ラ ド（2オクターブ）


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)


def pluck(freq, dur, bright=1.0, seed=0):
    """琴・三味線のようなはじく音（倍音が多く、すぐ減る）。"""
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for k in range(1, 9):
        x += np.sin(2 * np.pi * freq * k * t * (1 + 0.0008 * k)) * (bright ** (k - 1)) / k ** 1.2 * np.exp(-t * (2.5 + 1.8 * k))
    x += np.random.default_rng(seed).standard_normal(n) * np.exp(-t / 0.004) * 0.15
    return x * 0.5


def taiko(dur=0.6, f=62.0, seed=0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * np.cumsum(f * (1 + 0.6 * np.exp(-t / 0.03))) / SR) * np.exp(-t / 0.18)
    hit = np.random.default_rng(seed).standard_normal(n) * np.exp(-t / 0.008) * 0.3
    return (body + hit) * 0.9


def shaker(dur=0.06, seed=0):
    n = int(dur * SR)
    x = np.random.default_rng(seed).standard_normal(n)
    x = np.diff(np.concatenate([[0], x]))            # 高い音だけ
    return x * env(n, 0.004, 0.018) * 0.12


def wood(seed=0):
    n = int(0.08 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1250 * t) * np.exp(-t / 0.015) * 0.25


def bass(freq, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)
    return x * env(n, 0.01, dur * 0.6) * 0.35


def make(total=62.0, seed=1):
    rng = np.random.default_rng(seed)
    n = int(total * SR)
    out = np.zeros(n + SR)

    def put(x, t, g=1.0):
        i = int(t * SR)
        j = min(len(out), i + len(x))
        if j > i:
            out[i:j] += g * x[: j - i]
    beats = int(total / BEAT)
    # 4小節ずつのメロディ（5音から作る、オリジナル）
    phrases = []
    for p in range(4):
        r = np.random.default_rng(seed * 10 + p)
        line, idx = [], 4
        for k in range(16):
            idx = int(np.clip(idx + r.choice([-2, -1, -1, 0, 1, 1, 2]), 0, len(SCALE) - 1))
            line.append(None if (k % 4 == 3 and r.random() < 0.35) else SCALE[idx])
        line[-1] = 62 + 12 * (p % 2)
        phrases.append(line)
    roots = [50, 50, 53, 55, 50, 57, 55, 50]          # レ・ファ・ソ・ラ の低音
    for b in range(beats):
        t = b * BEAT
        bar, pos = divmod(b, 4)
        # 太鼓：1・3拍目、小節の最後に「ドドン」
        put(taiko(seed=b), t, (0.4, 0.32, 0.36, 0.32)[pos])      # 毎拍（参考元の低い拍は 117 BPM）
        if pos == 3 and bar % 2 == 1:
            put(taiko(f=70, seed=b + 500), t + BEAT / 2, 0.5)
        # シャカシャカ（16分）
        for s in range(4):
            put(shaker(seed=b * 4 + s), t + s * BEAT / 4, 1.0 if s % 2 == 0 else 0.6)
        # 拍子木のような「カッ」（2・4拍目）
        if pos in (1, 3):
            put(wood(), t, 0.5)
        # 低音（8分で刻む）
        root = roots[(bar // 2) % len(roots)]
        for s in range(2):
            put(bass(hz(root), BEAT / 2), t + s * BEAT / 2, 0.45)
        # メロディ（8分音符、琴のような音）。最初の2小節はリズムだけで入る
        if bar >= 2:
            line = phrases[(bar // 4) % 4]
            for s in range(2):
                m = line[((bar % 4) * 4 + pos) % 16]
                if m and (s == 0 or rng.random() < 0.45):
                    put(pluck(hz(m), 0.5, 0.7, seed=b * 2 + s), t + s * BEAT / 2, 0.55)
        # 和音（4小節ごとに長い音）
        if pos == 0 and bar % 4 == 0 and bar >= 2:
            for m in (root + 12, root + 19, root + 24):
                put(pluck(hz(m), 2.0, 0.5, seed=b + 900) * 0.6, t, 0.4)
    out = out[:n]
    fade = int(1.5 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    out /= max(1e-6, np.abs(out).max())
    return out * 0.85


if __name__ == "__main__":
    path = sys.argv[1]
    total = float(sys.argv[2]) if len(sys.argv) > 2 else 62.0
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    x = make(total, seed)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    print("wrote", path, f"{total:.1f}s")
