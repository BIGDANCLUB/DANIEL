"""「もしも日本からスズメが消えたら？」の合成（よねあぷ型の文字＋効果音＋BGM）。ナレーションなし。
usage: python3 compose.py frames_root out.mp4 [bgm.wav]"""
import importlib.util
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timeline as TL  # noqa: E402

_spec = importlib.util.spec_from_file_location("sugi_compose", os.path.join(HERE, "..", "sugi", "compose.py"))
SC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SC)       # スギ版の色の仕上げ（少し暗め・オレンジ弱め）と音の部品を使う
FC, CC, Y = SC.FC, SC.CC, SC.Y
# 夕方の場面が多く、明るくオレンジに寄りすぎた（明るさ 122・暖かさ 24）ので、中間を下げて黄色みを弱める（計測で決めた値）
FC.GRADE = dict(FC.GRADE, gam=1.8, lo=0.18, hi=0.80, s=1.0, r=0.96, b=1.02, sat=0.85, vib=1.0)
FPS, SR = TL.FPS, CC.SR
LABEL = "スズメが消えてから"
WORD, PRE, POST = "スズメ", "もしも", "が消えたら？"
tone, noise, lp, env, band = CC.tone, CC.noise, CC.lp, CC.env, SC.band
HY, HS = FC.HY, FC.HS


def sepia(img):
    """昔の話（実話の場面）は、セピア色の古い写真のように。"""
    a = np.asarray(img.convert("RGB"), np.float32) / 255
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    s = np.clip(lum[..., None] * np.array([1.08, 0.90, 0.66], np.float32), 0, 1)
    out = s * 0.88 + a * 0.12
    return Image.fromarray((out * 255 + 0.5).astype(np.uint8))


def look(base, s):
    return FC.look(sepia(base) if s.get("sepia") else base)


def draw(s, i, base):
    g = look(base, s)
    sec = i / FPS
    fade = CC.fade
    if s.get("kind") == "open":
        if sec < TL.T_VANISH:
            Y.big_title(g, WORD, PRE, "が", "消えたら？", "新潟・米どころの村。10月、稲刈りの夕方")
            Y.countdown(g, "スズメが消えるまで", TL.T_VANISH - sec)
            Y.headline(g, "田んぼに[スズメの大群]", ["秋の日本には", "約4,500万羽いるとされる"], fade(sec, 0.4, 2.8), y=HY, size=HS)
            Y.headline(g, "毎年、[米]をねらうやつら", ["農家とスズメの", "長いたたかい"], fade(sec, 2.8, TL.T_VANISH + 0.01),
                       y=HY, size=HS)
            Y.note(g, "※統計や研究をもとにした、もしもの話です", fade(sec, 0.2, TL.T_VANISH, k=0.3))
        else:
            Y.title_small(g, WORD, PRE, POST)
            Y.elapsed(g, LABEL, "1", CC.fmt_elapsed(sec - TL.T_VANISH, 1), s.get("loc"))
        return g
    Y.title_small(g, WORD, PRE, POST)
    e, speed = TL.e_of(s, i)
    Y.elapsed(g, LABEL, CC.fmt_speed(speed), CC.fmt_elapsed(e, speed), s.get("loc"))
    for a, b, head, sub in s.get("captions", []):
        Y.headline(g, head, sub, fade(sec, a, b), y=HY, size=HS)
    if s.get("cap_cont"):
        Y.headline(g, TL.JOY[0], TL.JOY[1], 1.0, y=HY, size=HS)
    if s.get("card"):
        Y.card(g, s["card"], fade(sec, 0.0, 1.3, k=0.12))
    return g


# ---------- 音 ----------
def tweet(seed=0, double=None):
    """スズメの「チュン」（速く下がる高い声）。double で「チュンチュン」。"""
    r = np.random.default_rng(seed)
    out = []
    for k in range(2 if (double if double is not None else r.random() < 0.5) else 1):
        d = r.uniform(0.05, 0.08)
        n = int(d * SR)
        f0 = r.uniform(4600, 5600)
        x = tone(d, f0, f0 * 0.72) + 0.35 * tone(d, f0 * 2, f0 * 1.44)
        out.append(x * env(n, 0.003, 0.02) * r.uniform(0.18, 0.3))
        out.append(np.zeros(int(r.uniform(0.04, 0.09) * SR)))
    return np.concatenate(out)


def flock_snd(dur, seed=1, density=1.0):
    """群れ：たくさんの羽音（ザワザワ）と、チュンチュンの声。"""
    tt = np.arange(int(dur * SR)) / SR
    x = band(noise(dur, seed), 300, 3500) * (0.5 + 0.5 * np.sin(2 * np.pi * 16 * tt) ** 2) * 0.35 * density
    r = np.random.default_rng(seed)
    for t0 in r.uniform(0, dur - 0.3, int(dur * 12 * density)):
        tw = tweet(int(t0 * 1000) + seed)
        i = int(t0 * SR)
        j = min(len(x), i + len(tw))
        x[i:j] += tw[: j - i]
    return x


def twang():
    """電線がはね上がる「ビヨン」（低い音がふるえながら消える）。"""
    n = int(1.4 * SR)
    tt = np.arange(n) / SR
    f = 95 * (1 + 0.05 * np.sin(2 * np.pi * 7 * tt))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + 0.5 * np.sin(2.01 * ph) + 0.25 * np.sin(3.03 * ph)) * np.exp(-tt / 0.45)
    return x * np.minimum(1, tt / 0.005) * 0.35


def clank(seed=0):
    """鍋をたたく「カーン」（金属の、整数倍でない響き）。"""
    r = np.random.default_rng(seed)
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * r.uniform(0.95, 1.05) * tt) * np.exp(-tt / d) * a
            for f, d, a in ((520, 0.25, 1.0), (1290, 0.15, 0.6), (2170, 0.1, 0.4), (3420, 0.06, 0.3)))
    return (x + band(noise(0.35, seed), 2000, 8000) * np.exp(-tt / 0.01)) * 0.25


def drone_snd(dur):
    tt = np.arange(int(dur * SR)) / SR
    f = 170 * (1 + 0.01 * np.sin(2 * np.pi * 0.5 * tt))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(k * ph) / k for k in range(1, 10)) * 0.12 + band(noise(dur, 61), 500, 4000) * 0.12
    return x * np.minimum(1, tt / 0.4) * np.clip((dur - tt) / 0.4, 0, 1)


def piano(notes, dt=0.32):
    out = []
    for f in notes:
        n = int(dt * SR)
        tt = np.arange(n) / SR
        out.append(sum(np.sin(2 * np.pi * f * h * tt) / (h * h) for h in (1, 2, 3, 4)) * np.exp(-tt / 0.35) * 0.16)
    return np.concatenate(out)


def grains_snd(seed=0):
    """米つぶが地面に落ちる「パラパラ」。"""
    r = np.random.default_rng(seed)
    x = np.zeros(int(0.6 * SR))
    for t0 in r.uniform(0.0, 0.5, 18):
        i = int(t0 * SR)
        m = int(0.01 * SR)
        x[i:i + m] += band(noise(0.01, int(t0 * 1e4)), 3000, 9000)[:m] * env(m, 0.0005, 0.002) * 0.6
    return x


def flap(seed=0):
    """羽ばたきの「バサッ」（短いざらついた音が2〜3回）。"""
    r = np.random.default_rng(seed)
    out = np.zeros(int(0.12 * SR))
    for k in range(r.integers(2, 4)):
        i = int(k * r.uniform(0.025, 0.04) * SR)
        n = int(0.03 * SR)
        out[i:i + n] += band(noise(0.03, seed * 7 + k), 400, 4500)[:n] * env(n, 0.001, 0.008) * r.uniform(0.6, 1.0)
    return out


def impact():
    """始まりの「ドン」（低い音＋ザッ）。"""
    n = int(0.9 * SR)
    tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * np.cumsum(70 - 30 * tt) / SR) * np.exp(-tt / 0.25) * 0.9
    return x + band(noise(0.9, 71), 300, 5000) * np.exp(-tt / 0.06) * 0.6


def pass_by(dur=1.3, seed=72):
    """群れが頭の上をすれ違う「ゴーッ」（近づいて高く → 遠ざかって低く）。"""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    x = noise(dur, seed)
    y = np.zeros(n)
    for i in range(0, n, 1024):
        u = tt[i] / dur
        y[i:i + 1024] = lp(x[i:i + 1024], 600 + 4500 * (1 - abs(2 * u - 1)))
    return y * np.sin(np.pi * tt / dur) ** 1.5 * 1.2


def build_audio(total):
    st = {s["name"]: TL.start_of(s["name"]) for s in TL.SHOTS}
    a = np.zeros(int(total * SR) + SR)

    def put(x, at, gain=1.0):
        i = int(at * SR)
        j = min(len(a), i + len(x))
        if j > i:
            a[i:j] += gain * x[: j - i]

    put(CC.ambience(total), 0, 1.0)
    # 冒頭（最初の5秒は派手に）：ドン → バサッとチュンが1秒に20回以上 → カットのたびにシュッ → 頭の上をすれ違うゴーッ
    put(impact(), 0.0, 1.0)
    put(flock_snd(TL.T_VANISH, 1, 1.0), 0.0, 0.35)       # ザワザワは小さく、粒の立った音を目立たせる
    rng = np.random.default_rng(7)
    t0 = 0.05
    while t0 < TL.T_VANISH:                                 # バサッ：0.1〜0.16秒おきに、はっきり区切って
        put(flap(int(t0 * 1000)), t0, rng.uniform(0.7, 1.0))
        t0 += rng.uniform(0.10, 0.16)
    for t0 in rng.uniform(0.1, TL.T_VANISH, 30):
        put(tweet(int(t0 * 997)), t0, 1.0)
    put(CC.whoosh(1.0, 50), 1.25, 0.8)
    put(CC.whoosh(1.0, 51), 3.1, 0.8)
    put(pass_by(), 4.7, 1.0)
    for k in range(1, 6):
        put(CC.tick(), TL.T_VANISH - k, 0.6)
    put(CC.sparkle(1, 2.0), TL.T_VANISH, 1.0)
    put(FC.wind(2.4, 52), TL.T_VANISH + 0.2, 0.4)
    for s in TL.SHOTS:
        if s.get("segs"):
            e0, sp = TL.e_of(s, 0)
            if sp > 50:      # 早送りの場面は、時計のカチカチ
                for k, tt in enumerate(np.arange(0.25, s["frames"] / FPS - 0.1, 0.4)):
                    put(SC.clock(k), st[s["name"]] + tt, 0.7)
        if s.get("card"):
            put(CC.whoosh(0.9, hash(s["name"]) % 50), st[s["name"]] - 0.2, 0.7)
        for a0, b0, head, sub in s.get("captions", []):
            put(CC.pop(), st[s["name"]] + a0, 0.6)
    t = st["s02_wire"]
    for k in range(6):
        put(tweet(100 + k), t + 0.02 + k * 0.05, 0.8)
    put(CC.sparkle(2, 1.4), t + 10 / FPS, 0.8)
    put(twang(), t + 13 / FPS, 1.0)
    t = st["s03_feed"]
    for k, f0 in enumerate((14, 54, 94)):
        put(grains_snd(k), t + f0 / FPS + 0.35, 0.8)
    put(FC.wind(4.5, 53), t, 0.3)
    t = st["s04_scare"]
    put(CC.caw(3), t + 1.4, 0.2)
    put(FC.thud(), t + 40 / FPS, 0.3)
    t = st["s05_issa"]
    put(SC.murmur(4.5, 54), t, 0.5)
    for k in range(4):
        put(SC.step(80 + k), t + 0.6 + k * 0.25, 0.3)
    t = st["s06_fukura"]
    put(FC.wind(4.5, 55), t, 0.7)
    t = st["s07_spring"]
    put(CC.buzz(5.0, 0.4, 56), t, 0.5)
    t = st["s08_paddy"]
    put(CC.buzz(5.5, 1.0, 57), t, 0.8)
    for k in range(10):
        put(SC.step(90 + k, hard=False), t + 0.3 + k * 0.5, 0.5)
    t = st["s09_china"]
    for k in range(14):
        put(clank(k), t + 0.2 + k * 0.32, 0.7)
    put(CC.buzz(3.0, 2.0, 58), t + 2.0, 1.0)
    put(SC.rumble(3.0, 59, 1.0), t + 2.0, 0.6)
    t = st["s10_drone"]
    put(drone_snd(4.5), t, 1.0)
    t = st["s11_song"]
    put(piano([523, 523, 587, 659, 587, 523, 440, 523, 587, 523, 440, 392, 440, 523]), t + 0.3, 1.0)
    put(SC.murmur(4.0, 60), t + 0.4, 0.35)
    t = st["s12_return"]
    for k in range(1, 3):
        put(CC.tick(), t + 2.0 - k, 0.5)
    put(CC.sparkle(3, 2.2), t + 1.3, 1.0)
    put(flock_snd(4.8, 62, 1.2), t + 2.2, 1.0)
    t = st["j1_chase"]
    put(flock_snd(2.5, 63, 1.0), t, 0.9)
    put(FC.cheer(st["s99_end"] - t - 0.6, 64), t + 1.0, 0.7)
    t = st["j2_garden"]
    for k in range(6):
        put(tweet(200 + k), t + 0.1 + k * 0.22, 0.8)
    t = st["j3_wire"]
    put(twang(), t + 18 / FPS, 0.9)
    for k in range(5):
        put(tweet(300 + k), t + 0.6 + k * 0.15, 0.7)
    put(SC.murmur(1.5, 65), st["j4_school"], 0.5)
    put(flock_snd(2.5, 66, 0.8), st["j5_wide"], 0.6)
    a = a / max(1e-6, np.abs(a).max()) * 0.8
    return a


def main():
    root, out = sys.argv[1], sys.argv[2]
    bgm = sys.argv[3] if len(sys.argv) > 3 else None
    total = TL.total_frames() / FPS
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Y.W}x{Y.H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                            out + ".video.mp4"], stdin=subprocess.PIPE)
    last_img, last_s = None, None
    for s in TL.SHOTS:
        if s.get("kind") == "end":
            base = look(last_img, last_s)
            for i in range(s["frames"]):
                g = base.copy()
                g.alpha_composite(Image.new("RGBA", base.size, (8, 8, 10, int(150 * min(1.0, i / 12)))))
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
            last_img, last_s = prev, s
            enc.stdin.write(draw(s, i, prev).convert("RGB").tobytes())
        print("composed", s["name"], flush=True)
    enc.stdin.close()
    enc.wait()
    audio = build_audio(total)
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
        fc += (f";[2:a]volume={os.environ.get('BGM_VOL', '0.3')},atrim=0:{total:.2f},afade=t=out:st={total - 2.5:.2f}:d=2.5[b];"
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
