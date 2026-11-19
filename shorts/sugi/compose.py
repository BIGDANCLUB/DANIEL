"""「もしも日本からスギが消えたら？」の合成（よねあぷ型の文字＋効果音＋BGM）。ナレーションなし。
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

_spec = importlib.util.spec_from_file_location("fuji_compose", os.path.join(HERE, "..", "fuji", "compose.py"))
FC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(FC)
CC, Y = FC.CC, FC.Y
FPS, SR = TL.FPS, CC.SR
LABEL = "スギが消えてから"
WORD, PRE, POST = "スギ", "もしも", "が消えたら？"
tone, noise, lp, env = CC.tone, CC.noise, CC.lp, CC.env
HY, HS = FC.HY, FC.HS
look = FC.look


def draw(s, i, base):
    g = look(base)
    sec = i / FPS
    fade = CC.fade
    if s.get("kind") == "open":
        if sec < TL.T_VANISH:
            Y.big_title(g, WORD, PRE, "が", "消えたら？", "秋田・山あいの町。3月、花粉がいちばん飛ぶ朝")
            Y.countdown(g, "スギが消えるまで", TL.T_VANISH - sec)
            Y.headline(g, "山から[黄色いけむり]", ["スギ花粉。風がふくと", "山ごと舞い上がる"], fade(sec, 0.4, 2.8), y=HY, size=HS)
            Y.headline(g, "毎年3月は、[地獄]だった", ["ある調査では", "約4割がスギ花粉症"], fade(sec, 2.8, TL.T_VANISH + 0.01),
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
def band(x, lo, hi):
    return lp(x, hi) - lp(x, lo)


def sneeze(seed=1):
    """「はっ……くしょん！」：息をすう音 → 一瞬止まる → はじける息と声。"""
    a = int(0.55 * SR)
    tt = np.arange(a) / SR
    inh = band(noise(0.55, seed), 700, 3200) * (tt / 0.55) ** 2 * 0.35
    inh += np.sin(2 * np.pi * np.cumsum(420 + 260 * tt / 0.55) / SR) * (tt / 0.55) ** 3 * 0.08
    gap = np.zeros(int(0.12 * SR))
    n = int(0.6 * SR)
    t2 = np.arange(n) / SR
    burst = band(noise(0.6, seed + 1), 400, 6000) * env(n, 0.003, 0.09) * 1.1
    f = 330 - 120 * t2 / 0.6
    voice = sum(np.sin(2 * np.pi * k * np.cumsum(f) / SR) / k for k in range(1, 6)) * env(n, 0.01, 0.16) * 0.35
    sh = band(noise(0.6, seed + 2), 2500, 7000) * np.clip((t2 - 0.08) / 0.05, 0, 1) * np.exp(-np.maximum(t2 - 0.08, 0) / 0.12) * 0.5
    return np.concatenate([inh, gap, burst + voice + sh])


def rain_snd(dur, seed=21, level=1.0):
    tt = np.arange(int(dur * SR)) / SR
    x = band(noise(dur, seed), 800, 7000) * 0.22
    r = np.random.default_rng(seed)
    for t0 in r.uniform(0, dur - 0.05, int(dur * 40)):
        i = int(t0 * SR)
        m = int(0.02 * SR)
        x[i:i + m] += band(noise(0.02, int(t0 * 997)), 1500, 8000)[:m] * env(m, 0.0005, 0.004) * 0.6
    return x * np.minimum(1, tt / 0.3) * level


def rumble(dur, seed=22, grow=1.0):
    tt = np.arange(int(dur * SR)) / SR
    x = lp(noise(dur, seed), 120) * 3.0 + band(noise(dur, seed + 1), 200, 900) * 0.35
    return x * np.minimum(1, (tt / max(0.1, dur * 0.4)) ** grow) * np.clip((dur - tt) / 0.6, 0, 1)


def murmur(dur, seed=23):
    tt = np.arange(int(dur * SR)) / SR
    x = band(noise(dur, seed), 250, 1600) * (0.8 + 0.2 * np.sin(2 * np.pi * 2.3 * tt))
    return x * np.minimum(1, tt / 0.4) * np.clip((dur - tt) / 0.4, 0, 1) * 0.45


def chime():
    """駅の発車メロディ（短い6音）。"""
    notes = [784, 988, 1175, 988, 1319, 1175]
    out = []
    for k, f in enumerate(notes):
        n = int(0.22 * SR)
        x = sum(np.sin(2 * np.pi * f * h * np.arange(n) / SR) / (h * h) for h in (1, 2, 3))
        out.append(x * env(n, 0.004, 0.12))
    return np.concatenate(out) * 0.18


def winddown(dur=2.6, f0=180.0):
    """丸のこのモーターが止まっていく音（音がだんだん低く）。"""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = f0 * np.maximum(0, 1 - tt / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(k * ph) / k for k in range(1, 9)) * (1 - tt / dur) * 0.25
    return x + band(noise(dur, 24), 2000, 6000) * (1 - tt / dur) ** 2 * 0.15


def creak(seed=0):
    n = int(0.18 * SR)
    r = np.random.default_rng(seed)
    f = r.uniform(380, 520)
    tt = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * (f + 60 * np.sin(2 * np.pi * 9 * tt)) * tt)) * 0.15
    return lp(x, 2500) * env(n, 0.01, 0.06)


def step(seed=0, hard=True):
    n = int(0.09 * SR)
    x = band(noise(0.09, seed), 300 if hard else 150, 3500 if hard else 1200) * env(n, 0.001, 0.02)
    return x * (0.6 if hard else 0.8)


def brake():
    n = int(1.2 * SR)
    tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * np.cumsum(2400 - 300 * tt) / SR) * np.exp(-tt / 0.5) * np.minimum(1, tt / 0.05) * 0.12
    return x + band(noise(1.2, 25), 300, 2500) * np.exp(-tt / 0.6) * 0.3


def build_audio(total):
    st = {s["name"]: TL.start_of(s["name"]) for s in TL.SHOTS}
    a = np.zeros(int(total * SR) + SR)

    def put(x, at, gain=1.0):
        i = int(at * SR)
        j = min(len(a), i + len(x))
        if j > i:
            a[i:j] += gain * x[: j - i]

    put(CC.ambience(total), 0, 1.0)
    # 冒頭：風が山をゆらし、花粉が舞う／鳥／お父さんのくしゃみ／カウントダウン → 消える
    put(FC.wind(5.6, 31), 0.0, 1.0)
    for k in range(4):
        put(CC.whoosh(1.0, 40 + k), 0.2 + k * 1.3, 0.45)
    for k in range(5):
        put(CC.chirp(k), 0.4 + k * 1.0, 0.5)
    put(sneeze(1), 95 / FPS - 0.67, 1.2)
    for k in range(1, 6):
        put(CC.tick(), TL.T_VANISH - k, 0.6)
    put(CC.sparkle(1, 2.0), TL.T_VANISH, 1.0)
    put(CC.flutter(2.0), TL.T_VANISH + 0.1, 0.8)
    put(FC.wind(2.5, 32), TL.T_VANISH + 0.3, 0.5)
    for s in TL.SHOTS:
        if s.get("card"):
            put(CC.whoosh(0.9, hash(s["name"]) % 50), st[s["name"]] - 0.2, 0.7)
        for a0, b0, head, sub in s.get("captions", []):
            put(CC.pop(), st[s["name"]] + a0, 0.6)
    t = st["s02_shrine"]
    put(CC.sparkle(2, 1.4), t + 12 / FPS, 0.8)
    put(FC.thud(), t + (12 + 16) / FPS, 1.0)
    put(CC.chirp(7), t + 2.2, 0.4)
    t = st["s03_station"]
    put(murmur(5.0), t, 1.0)
    put(chime(), t + 0.3, 1.0)
    for k in range(10):
        put(step(k), t + 0.4 + k * 0.45, 0.4)
    t = st["s04_bare"]
    put(FC.wind(4.5, 33), t, 1.0)
    for k in range(3):
        put(CC.caw(k), t + 1.2 + k * 1.1, 0.25)
    t = st["s05_lumber"]
    put(winddown(2.8), t, 0.9)
    put(CC.caw(5), t + 2.8, 0.2)
    t = st["s06_rain"]
    put(rain_snd(6.0 + 3.5), t, 1.0)
    put(rumble(4.4, 22, 1.5), t + 52 / FPS, 1.4)
    for k in range(6):
        put(FC.thud(), t + 52 / FPS + 1.2 + k * 0.5, 0.25)
    t = st["s07_river"]
    put(FC.water(3.5, 1.6, 26), t, 1.0)
    t = st["s08_snow"]
    put(FC.wind(5.0, 34), t, 0.6)
    put(rumble(3.6, 27, 1.2), t + 40 / FPS, 1.3)
    put(CC.whoosh(2.0, 28), t + 40 / FPS + 0.6, 0.8)
    put(brake(), t + 1.4, 0.8)
    t = st["s09_sake"]
    put(FC.wind(4.0, 35), t, 0.5)
    for k in range(5):
        put(creak(k), t + 0.4 + k * 0.8, 0.6)
    t = st["s10_nikko"]
    for k in range(9):
        put(step(10 + k, hard=False), t + 0.3 + k * 0.48, 0.6)
    for k in range(3):
        put(CC.chirp(20 + k), t + 0.8 + k * 1.2, 0.4)
    t = st["s11_jomon"]
    put(FC.water(4.5, 0.3, 36), t, 0.6)
    for k in range(4):
        put(FC.drip(), t + 0.5 + k * 1.0, 0.5)
        put(CC.chirp(30 + k), t + 0.9 + k * 1.0, 0.35)
    t = st["s12_hanami"]
    put(murmur(5.0, 37), t, 0.6)
    put(FC.cheer(1.5, 38), t + 2.0, 0.3)
    for k in range(4):
        put(CC.chirp(40 + k), t + 0.5 + k * 1.1, 0.4)
    t = st["s13_hinoki"]
    put(FC.wind(3.5, 39), t, 0.5)
    put(sneeze(3), t + 62 / FPS - 0.67, 1.2)
    t = st["s14_plant"]
    for k in range(6):
        put(FC.thud(), t + 0.6 + k * 0.65, 0.18)
        put(CC.chirp(50 + k), t + 0.9 + k * 0.65, 0.3)
    t = st["s15_return"]
    for k in range(1, 3):
        put(CC.tick(), t + 2.0 - k, 0.5)
    put(CC.sparkle(3, 2.2), t + 1.3, 1.0)
    for k in range(4):
        put(CC.chirp(60 + k), t + 3.0 + k * 0.8, 0.5)
    put(FC.wind(3.0, 40), t + 4.6, 0.9)
    put(CC.whoosh(1.2, 41), t + 4.7, 0.5)
    t = st["j1_sneeze"]
    put(sneeze(5), t + 34 / FPS - 0.67, 1.3)
    put(FC.cheer(st["s99_end"] - t - 0.6, 42), t + 1.6, 0.8)
    put(winddown(1.0, 120) * 0, st["j2_lumber"], 0.0)
    put(FC.fanfare(), st["j2_lumber"] + 0.1, 0.5)
    put(creak(9), st["j3_sake"] + 0.3, 0.6)
    for k in range(3):
        put(step(70 + k, hard=False), st["j4_nikko"] + 0.2 + k * 0.4, 0.5)
    put(sneeze(7), st["j5_wide"] + 1.0, 0.6)
    a = a / max(1e-6, np.abs(a).max()) * 0.8
    return a


def main():
    root, out = sys.argv[1], sys.argv[2]
    bgm = sys.argv[3] if len(sys.argv) > 3 else None
    total = TL.total_frames() / FPS
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Y.W}x{Y.H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                            out + ".video.mp4"], stdin=subprocess.PIPE)
    last_img = None
    for s in TL.SHOTS:
        if s.get("kind") == "end":
            base = look(last_img)
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
            last_img = prev
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
