"""「もしもカラスが消えたら？」の合成（よねあぷ型の文字＋効果音＋BGM）。ナレーションなし。
usage: python3 compose.py frames_root out.mp4 [bgm.mp3]"""
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timeline as TL  # noqa: E402
import overlay_y as Y  # noqa: E402

sys.argv += [] if len(sys.argv) > 2 else []
FPS, SR = TL.FPS, 44100
LABEL = "カラスが消えてから"


def fmt_elapsed(e, speed):
    if e < 3600:
        return f"{int(e // 60):02d}:{e % 60:05.2f}"
    if e < TL.DAY:
        h, r = divmod(int(e), 3600)
        return f"{h:02d}:{r // 60:02d}:{r % 60:02d}"
    y, r = divmod(int(e), TL.YEAR)
    d, r = divmod(r, TL.DAY)
    h, r = divmod(r, 3600)
    if y == 0:
        return f"{d}日 {h:02d}:{r // 60:02d}"
    if speed < 10:      # ×1 の時は秒まで動かす
        return f"{y}年 {d}日 {h:02d}:{r // 60:02d}:{r % 60:02d}"
    return f"{y}年 {d}日 {h:02d}時"


def fmt_speed(s):
    if s < 9.95:
        v = f"{s:.1f}"
        return v[:-2] if v.endswith(".0") else v
    return f"{round(s):,}"


def look(img):
    g = img.convert("RGB")
    g = ImageEnhance.Color(g).enhance(1.12)
    g = ImageEnhance.Contrast(g).enhance(1.04)
    return g.resize((Y.W, Y.H), Image.LANCZOS).convert("RGBA")


def fade(sec, a, b, k=0.15):
    if sec < a or sec >= b:
        return 0.0
    return min(1.0, (sec - a) / k, (b - sec) / k)


def draw(s, i, base):
    g = look(base)
    sec = i / FPS
    if s.get("kind") == "open":
        if sec < TL.T_VANISH:
            Y.big_title(g, "カラス", "もしも", "が", "消えたら？", "毎朝6時。おじいさんとクロの朝ごはん")
            Y.countdown(g, "カラスが消えるまで", TL.T_VANISH - sec)
            Y.headline(g, "この子の名前は、クロ", ["毎朝、おじいさんに", "パンくずをもらいにくる"], fade(sec, 0.4, 2.8))
            left = math.ceil(TL.T_VANISH - sec)
            Y.headline(g, f"あと{left}秒で、クロは消える", ["日本中のカラスといっしょに"], fade(sec, 2.8, TL.T_VANISH + 0.01))
        else:
            e = sec - TL.T_VANISH
            Y.title_small(g, "カラス", "もしも", "が消えたら？")
            Y.elapsed(g, LABEL, "1", fmt_elapsed(e, 1), s.get("loc"))
        return g
    Y.title_small(g, "カラス", "もしも", "が消えたら？")
    e, speed = TL.e_of(s, i)
    Y.elapsed(g, LABEL, fmt_speed(speed), fmt_elapsed(e, speed), s.get("loc"))
    for a, b, head, sub in s.get("captions", []):
        Y.headline(g, head, sub, fade(sec, a, b))
    if s.get("card"):
        Y.card(g, s["card"], fade(sec, 0.0, 1.3, k=0.12))
    return g


# ---------- 音 ----------
def tone(dur, f0, f1=None):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = f0 if f1 is None else f0 + (f1 - f0) * tt / dur
    return np.sin(2 * np.pi * np.cumsum(np.full(n, 1.0) * f) / SR)


def noise(dur, seed=0):
    return np.random.default_rng(seed).standard_normal(int(dur * SR))


def lp(x, cutoff):
    from scipy.signal import lfilter
    a = 1 - math.exp(-2 * math.pi * cutoff / SR)
    return lfilter([a], [1, a - 1], x)


def env(n, attack, decay):
    tt = np.arange(n) / SR
    return np.minimum(tt / max(attack, 1e-3), 1.0) * np.exp(-tt / decay)


def caw(seed=0, dur=0.34, f0=560, f1=430):
    """カラスの「カァ」：倍音の多いざらついた声。"""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = f0 + (f1 - f0) * tt / dur
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(k * ph) / k for k in range(1, 14))
    x = x * (1 + 0.5 * np.sin(2 * np.pi * 70 * tt)) + 0.4 * noise(dur, seed)
    x = lp(x - lp(x, 650), 3800)
    shape = np.minimum(tt / 0.025, 1) * np.clip((dur - tt) / 0.12, 0, 1)
    return x * shape * 0.5


def sparkle(seed=1, dur=1.6, up=True):
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    y = np.zeros(n)
    notes = [1568, 2093, 2637, 3136, 4186]
    for k in range(9):
        fq = notes[k % 5] * (1 if up else 0.75)
        at = int((k * 0.09 if up else (8 - k) * 0.09) * SR)
        m = n - at
        y[at:] += tone(m / SR, fq) * env(m, 0.002, 0.35) * r.uniform(0.15, 0.3)
    return y


def whoosh(dur=0.8, seed=2):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    x = noise(dur, seed)
    y = np.zeros(n)
    for i in range(0, n, 1024):
        y[i:i + 1024] = lp(x[i:i + 1024], 300 + 2500 * (tt[i] / dur))
    return y * np.sin(np.pi * tt / dur) ** 2 * 0.7


def tick():
    n = int(0.1 * SR)
    return tone(0.1, 1300) * env(n, 0.001, 0.025) * 0.5


def pop():
    n = int(0.12 * SR)
    return tone(0.12, 900, 1400) * env(n, 0.003, 0.04) * 0.35


def buzz(dur, density=1.0, seed=5):
    """ハエの羽音（何匹も重ねる）。"""
    tt = np.arange(int(dur * SR)) / SR
    r = np.random.default_rng(seed)
    y = np.zeros_like(tt)
    for k in range(int(3 + 9 * density)):
        f = r.uniform(170, 260) * (1 + 0.04 * np.sin(2 * np.pi * r.uniform(2, 6) * tt + r.uniform(0, 6)))
        ph = 2 * np.pi * np.cumsum(f) / SR
        saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
        y += saw * (0.5 + 0.5 * np.sin(2 * np.pi * r.uniform(0.3, 1.2) * tt + r.uniform(0, 6))) ** 2
    return lp(y, 2500) * 0.12


def squeak(seed=0):
    r = np.random.default_rng(seed)
    d = r.uniform(0.06, 0.12)
    n = int(d * SR)
    return tone(d, r.uniform(3200, 4200), r.uniform(3600, 4800)) * env(n, 0.004, 0.03) * 0.3


def chirp(seed=0):
    """ヒヨドリっぽい「ピーヨ」。"""
    r = np.random.default_rng(seed)
    a = tone(0.18, 2600, 3300) * env(int(0.18 * SR), 0.01, 0.08)
    b = tone(0.22, 3000, 2300) * env(int(0.22 * SR), 0.01, 0.1)
    return np.concatenate([a, np.zeros(int(0.04 * SR)), b]) * r.uniform(0.15, 0.3)


def flutter(dur, seed=7):
    tt = np.arange(int(dur * SR)) / SR
    return lp(noise(dur, seed), 1800) * (0.5 + 0.5 * np.sin(2 * np.pi * 14 * tt)) ** 3 * 0.35


def ambience(dur, seed=9):
    return lp(noise(dur, seed), 400) * 0.05


def build_audio(total, st):
    a = np.zeros(int(total * SR) + SR)

    def put(x, at, gain=1.0):
        i = int(at * SR)
        j = min(len(a), i + len(x))
        if j > i:
            a[i:j] += gain * x[: j - i]

    end_out = st["c13_end"]
    put(ambience(end_out), 0, 1.0)
    # 冒頭：クロの声とカウントダウン
    for t, sd in ((0.6, 1), (2.0, 2), (3.6, 3)):
        put(caw(sd), t, 0.8)
    for t, sd in ((1.2, 4), (3.0, 5)):
        put(caw(sd, f0=600, f1=470) * 0.6, t, 0.45)    # 電線のカラス
    for k in range(1, 6):
        put(tick(), TL.T_VANISH - k, 0.6)
    put(sparkle(1), TL.T_VANISH, 0.9)
    put(sparkle(2), st["c02_wire"] + 0.1, 0.8)
    # 章カード
    for s in TL.SHOTS:
        if s.get("card"):
            put(whoosh(0.9, hash(s["name"]) % 50), st[s["name"]] - 0.2, 0.7)
        for a0, b0, head, sub in s.get("captions", []):
            put(pop(), st[s["name"]] + a0, 0.6)
    # ハエ・ネズミ・小鳥
    s6, s7 = st["c06_road"], st["c07_flies"]
    b6 = buzz(6.0, 0.6, 5) * np.linspace(0.1, 1.0, int(6.0 * SR))
    put(b6, s6, 0.7)
    put(buzz(6.0, 1.6, 6), s7, 1.1)
    for k in range(10):
        put(squeak(k), st["c08_rats"] + 0.6 + k * 0.42, 0.8)
    put(flutter(4.5), st["c09_birds"] + 0.3, 0.8)
    for k in range(6):
        put(chirp(k), st["c09_birds"] + 0.8 + k * 0.7, 0.7)
    # 毎朝（季節が変わるたび）
    for k in range(1, 4):
        put(whoosh(0.5, 30 + k) * 0.6, st["c11_bench"] + k * 1.5 - 0.15, 0.5)
    # 再会
    r0 = st["c12_return"]
    for k in range(1, 3):
        put(tick(), r0 + 2.0 - k, 0.5)
    put(sparkle(3, 2.0), r0 + 1.4, 1.0)
    for t, sd in ((2.9, 11), (4.6, 12), (6.2, 13), (7.9, 14)):
        put(caw(sd), r0 + t, 0.9)
    a = a / max(1e-6, np.abs(a).max()) * 0.8
    return a


def main():
    root, out = sys.argv[1], sys.argv[2]
    bgm = sys.argv[3] if len(sys.argv) > 3 else None
    total_frames = TL.total_frames()
    assert total_frames == TL.TOTAL, f"{total_frames} != {TL.TOTAL}"
    total = total_frames / FPS
    st, k = {}, 0
    for s in TL.SHOTS:
        st[s["name"]] = k / FPS
        k += s["frames"]
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Y.W}x{Y.H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                            out + ".video.mp4"], stdin=subprocess.PIPE)
    last_img = None
    for s in TL.SHOTS:
        if s.get("kind") == "end":
            base = look(last_img)
            dark = Image.new("RGBA", base.size, (0, 0, 0, 0))
            for i in range(s["frames"]):
                g = base.copy()
                k = min(1.0, i / 12)
                dark = Image.new("RGBA", base.size, (8, 8, 10, int(150 * k)))
                g.alpha_composite(dark)
                if i >= 6:
                    Y.end_card(g)
                enc.stdin.write(g.convert("RGB").tobytes())
            continue
        d = os.path.join(root, s["name"])
        prev = None
        for i in range(s["frames"]):
            p = os.path.join(d, f"f_{i + 1:04d}.png")
            if os.path.exists(p):
                prev = Image.open(p).convert("RGB")
            last_img = prev
            enc.stdin.write(draw(s, i, prev).convert("RGB").tobytes())
        print("composed", s["name"], flush=True)
    enc.stdin.close()
    enc.wait()
    audio = build_audio(total, st)
    wav = out + ".sfx.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    inputs = ["-i", out + ".video.mp4", "-i", wav]
    fc = "[1:a]volume=1.0[s]"
    if bgm:
        inputs += ["-stream_loop", "-1", "-i", bgm]
        fc += (f";[2:a]volume=0.25,atrim=0:{total:.2f},afade=t=out:st={total - 2.5:.2f}:d=2.5[b];"
               "[s][b]amix=inputs=2:normalize=0[m];[m]loudnorm=I=-14:TP=-1.5[a]")
    else:
        fc += ";[s]loudnorm=I=-14:TP=-1.5[a]"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", out], check=True)
    os.remove(out + ".video.mp4")
    os.remove(wav)
    print("done", out, f"{total:.2f}s")


if __name__ == "__main__":
    main()
