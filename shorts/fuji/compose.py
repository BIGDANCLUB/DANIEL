"""「もしも日本から富士山が消えたら？」の合成（よねあぷ型の文字＋効果音＋BGM）。ナレーションなし。
usage: python3 compose.py frames_root out.mp4 [bgm.mp3]"""
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

_spec = importlib.util.spec_from_file_location("crow_compose", os.path.join(HERE, "..", "crow", "compose.py"))
CC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CC)
Y = CC.Y
FPS, SR = TL.FPS, CC.SR
LABEL = "富士山が消えてから"
WORD, PRE, POST = "富士山", "もしも", "が消えたら？"
tone, noise, lp, env = CC.tone, CC.noise, CC.lp, CC.env


HY, HS = 1170, 86      # 見出しは画面の中ほどに大きく（参考元に合わせる）


# 色の調整（参考元に合わせて計測で決めた値）：黒を締める・S字で明暗をはっきり・暖かく・あざやかに
GRADE = dict(lo=0.14, hi=0.82, gam=1.3, s=0.8, r=1.02, b=0.95, sat=1.0, vib=1.2)


def grade(a, g=None):
    """黒を締める → S字カーブ → 少し暖かく → くすんだ色ほど強く色をのせる（肌がオレンジにならないように）。"""
    g = g or GRADE
    a = np.clip((a - g["lo"]) / (g["hi"] - g["lo"]), 0, 1) ** g.get("gam", 1.0)
    a = a * (1 - g["s"]) + a * a * (3 - 2 * a) * g["s"]
    a[..., 0] *= g["r"]
    a[..., 2] *= g["b"]
    lum = (a @ np.array([0.299, 0.587, 0.114], np.float32))[..., None]
    chroma = (a.max(-1) - a.min(-1))[..., None]
    k = g["sat"] + g["vib"] * np.clip(1 - chroma / 0.35, 0, 1)
    return np.clip(lum + (a - lum) * k, 0, 1)


def look(img):
    a = np.asarray(img.convert("RGB"), np.float32) / 255
    g = Image.fromarray((grade(a) * 255 + 0.5).astype(np.uint8))
    return g.resize((Y.W, Y.H), Image.LANCZOS).convert("RGBA")


def draw(s, i, base, t_joy=None):
    g = look(base)
    sec = i / FPS
    fade = CC.fade
    if s.get("kind") == "open":
        if sec < TL.T_VANISH:
            Y.big_title(g, WORD, PRE, "が", "消えたら？", "静岡・富士市。縁側から富士山が見える家")
            Y.countdown(g, "富士山が消えるまで", TL.T_VANISH - sec)
            Y.headline(g, "毎朝あいさつする[あの山]", ["おじいさんの、70年の日課"], fade(sec, 0.4, 2.8), y=HY, size=HS)
            Y.headline(g, "いつもの朝は、[これが最後]", ["日本一の山が、ある朝とつぜん"], fade(sec, 2.8, TL.T_VANISH + 0.01), y=HY, size=HS)
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
    if s.get("cap_cont") and t_joy is not None:
        Y.headline(g, "やっぱり、[あってよかった]", ["10年ぶりの、いつもの景色"], 1.0, y=HY, size=HS)
    if s.get("card"):
        Y.card(g, s["card"], fade(sec, 0.0, 1.3, k=0.12))
    return g


# ---------- 音 ----------
def water(dur, level=1.0, seed=3):
    tt = np.arange(int(dur * SR)) / SR
    x = lp(noise(dur, seed), 1500) - lp(noise(dur, seed), 200)
    return x * (0.7 + 0.3 * np.sin(2 * np.pi * 0.7 * tt)) * 0.25 * level


def wind(dur, seed=4):
    tt = np.arange(int(dur * SR)) / SR
    return lp(noise(dur, seed), 500) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.25 * tt - 1.5)) * 0.6


def rumble(dur, seed=5):
    tt = np.arange(int(dur * SR)) / SR
    x = lp(noise(dur, seed), 160) * 1.2
    for t0 in np.arange(0.3, dur, 0.9):     # レールのつなぎ目
        i = int(t0 * SR)
        n = int(0.08 * SR)
        if i + n < len(x):
            x[i:i + n] += lp(noise(0.08, int(t0 * 10)), 600)[:n] * env(n, 0.002, 0.02) * 2
    return x * np.minimum(1, tt / 0.3) * 0.5


def fanfare():
    notes = [523, 659, 784, 1047]
    out = []
    for k, f in enumerate(notes):
        d = 0.16 if k < 3 else 0.6
        n = int(d * SR)
        x = sum(np.sin(2 * np.pi * f * h * np.arange(n) / SR) / h for h in (1, 2, 3))
        out.append(x * env(n, 0.005, 0.12 if k < 3 else 0.35))
    return np.concatenate(out) * 0.25


def cheer(dur, seed=6):
    """みんなの歓声（帯域をしぼったざわめき）＋拍手。"""
    tt = np.arange(int(dur * SR)) / SR
    x = lp(noise(dur, seed), 1800) - lp(noise(dur, seed), 350)
    x *= np.minimum(1, tt / 0.4) * (0.8 + 0.2 * np.sin(2 * np.pi * 3 * tt)) * 0.9
    r = np.random.default_rng(seed)
    for t0 in r.uniform(0.2, dur - 0.1, int(dur * 25)):
        i = int(t0 * SR)
        n = int(0.03 * SR)
        x[i:i + n] += noise(0.03, int(t0 * 1000))[:n] * env(n, 0.001, 0.008) * 0.5
    return x * 0.5


def thud():
    """遠くで重いものが落ちた、低い「ドスン」と、ザーッと広がる音。"""
    n = int(1.6 * SR)
    x = lp(noise(1.6, 31), 90) * 3.0 * env(n, 0.005, 0.35)
    x += (lp(noise(1.6, 32), 2500) - lp(noise(1.6, 32), 400)) * env(n, 0.02, 0.6) * 0.5
    return x


def hum(dur):
    tt = np.arange(int(dur * SR)) / SR
    return sum(np.sin(2 * np.pi * 60 * h * tt) / h for h in (1, 2, 3, 5)) * 0.06


def drip():
    n = int(0.15 * SR)
    return tone(0.15, 1800, 900) * env(n, 0.002, 0.04) * 0.35


def build_audio(total, st):
    a = np.zeros(int(total * SR) + SR)

    def put(x, at, gain=1.0):
        i = int(at * SR)
        j = min(len(a), i + len(x))
        if j > i:
            a[i:j] += gain * x[: j - i]

    put(CC.ambience(total), 0, 1.0)
    for k in range(5):
        put(CC.chirp(k), 0.5 + k * 0.9, 0.6)
    for k in range(1, 6):
        put(CC.tick(), TL.T_VANISH - k, 0.6)
    put(CC.sparkle(1, 2.0), TL.T_VANISH, 1.0)
    t_fall = TL.T_VANISH + 8 / FPS
    put(CC.whoosh(1.2, 21), t_fall, 0.7)                          # 残った雪が落ちていく
    put(thud(), t_fall + 36 / FPS, 1.0)                           # 地面に落ちて、粉が広がる
    for s in TL.SHOTS:
        if s.get("card"):
            put(CC.whoosh(0.9, hash(s["name"]) % 50), st[s["name"]] - 0.2, 0.7)
        for a0, b0, head, sub in s.get("captions", []):
            put(CC.pop(), st[s["name"]] + a0, 0.6)
    put(rumble(4.0), st["f02_train"], 0.8)
    put(CC.sparkle(2, 1.4), st["f02_train"] + 0.3, 0.7)
    put(CC.whoosh(1.2, 9), st["f03_shadow"] + 1.3, 0.6)
    put(water(3.5, 0.6), st["f04_sento"], 0.7)
    for k in range(4):
        put(drip(), st["f04_sento"] + 0.8 + k * 0.7, 0.6)
    put(wind(3.5), st["f05_kitadake"], 0.5)
    put(fanfare(), st["f05_kitadake"] + 1.1, 0.7)
    put(wind(6.0, 7), st["f06_cloud"], 0.9)
    put(CC.sparkle(4, 1.2), st["f06_cloud"] + 3.4, 0.5)
    put(water(6.0, 1.0, 8), st["f07_spring"], 0.8)
    put(CC.flutter(3.0), st["f09_hazard"] + 1.0, 0.8)
    put(wind(4.5, 11), st["f09_hazard"], 0.5)
    put(water(5.0, 0.35, 12), st["f13_lowwater"], 0.8)
    put(water(3.0, 0.3, 13), st["f14_trout"], 0.7)
    put(hum(1.4) * np.linspace(1, 0, int(1.4 * SR)), st["f15_paper"], 0.8)
    for k in range(4):
        put(drip(), st["f16_tap"] + 0.4 + k * 0.6, 0.7)
    r0 = st["f17_return"]
    for k in range(1, 3):
        put(CC.tick(), r0 + 2.0 - k, 0.5)
    put(CC.sparkle(3, 2.2), r0 + 1.3, 1.0)
    for k in range(4):
        put(CC.chirp(10 + k), r0 + 3.2 + k * 0.8, 0.6)
    j0 = st["j1_home"]
    put(cheer(st["f19_end"] - j0 + 0.5), j0, 0.9)
    put(water(1.5, 1.0, 14), st["j2_trout"], 0.6)
    put(hum(1.5), st["j3_paper"], 0.6)
    put(water(1.5, 1.2, 15), st["j4_tap"], 0.8)
    a = a / max(1e-6, np.abs(a).max()) * 0.8
    return a


def main():
    root, out = sys.argv[1], sys.argv[2]
    bgm = sys.argv[3] if len(sys.argv) > 3 else None
    total = TL.total_frames() / FPS
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
            enc.stdin.write(draw(s, i, prev, t_joy=0).convert("RGB").tobytes())
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
        fc += (f";[2:a]volume={os.environ.get('BGM_VOL', '0.25')},atrim=0:{total:.2f},afade=t=out:st={total - 2.5:.2f}:d=2.5[b];"
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
