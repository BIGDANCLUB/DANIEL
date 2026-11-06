"""全場面をつないで、色味・文字・効果音を付けて1本の mp4 にする。
usage: python3 compose_all.py frames_root out.mp4 [bgm.mp3]
frames_root/<場面名>/f_####.png（step で飛ばした所は前のコマを使う）と sun.json を読む。"""
import glob
import json
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw
from scipy.signal import lfilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import overlay as O  # noqa: E402
import timeline as TL  # noqa: E402
from grade import grade  # noqa: E402

root, out = sys.argv[1], sys.argv[2]
bgm = sys.argv[3] if len(sys.argv) > 3 else None
FPS, SR = TL.FPS, 44100
WHITE, OR = (255, 255, 255), O.ORANGE


def load_frames(name, n):
    d = os.path.join(root, name)
    sun = json.load(open(os.path.join(d, "sun.json"))) if os.path.exists(os.path.join(d, "sun.json")) else {}
    paths, last, suns, last_sun = [], None, [], None
    for f in range(1, n + 1):
        p = os.path.join(d, f"f_{f:04d}.png")
        if os.path.exists(p):
            last = p
            last_sun = sun.get(str(f), last_sun if str(f) not in sun else None)
        paths.append(last)
        suns.append(last_sun)
    return paths, suns


def fmt_t(t, tag):
    slow = "/" in tag[0] and int(tag[0].split("/")[1].split()[0]) >= 30
    return f"{t:.3f}" if slow else f"{t:.2f}"


def fmt_mach(m):
    if m >= 9.95:
        return "10"
    if m < 0.05:
        return "0"
    return f"{m:.1f}"


def fmt_km(k):
    if k >= 3:
        return f"{k:.0f}"
    if k > 0.05:
        return f"{k:.1f}"
    return "0"


def speed_lines(im, k, seed):
    """運転席目線の集中線（参考の加速の場面）。k=0〜1。"""
    if k <= 0:
        return
    r = np.random.default_rng(seed)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx, cy = O.W / 2, O.H * 0.5
    for _ in range(int(60 * k)):
        a = r.uniform(0, 2 * math.pi)
        r0 = r.uniform(300, 600)
        r1 = r0 + r.uniform(300, 900) * k
        d.line((cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
               fill=(255, 245, 230, int(90 * k)), width=int(r.uniform(2, 5)))
    im.alpha_composite(lay)


def draw_shot(s, i, base, sun):
    if sun:
        g = grade(base, sun=tuple(sun))
    else:
        g = grade(base, sun=(base.width / 2, -base.height * 0.4), glow=0.4, haze=0.15)
    g = g.resize((O.W, O.H), Image.LANCZOS).convert("RGBA")
    sec = i / FPS
    O.watermark(g)
    if s.get("kind") == "open":
        count = 5 - int(sec)
        O.opening(g, [("もしも", WHITE), ("新幹線", OR), ("が", WHITE)], [("マッハ10", OR), ("で走っていたら？", WHITE)],
                  count if count >= 1 else None, ["東京駅から新横浜駅まで28.8km。", "今の「のぞみ」なら約18分"],
                  "東海道新幹線の時刻表より")
        return g
    t, tag = TL.t_of(s, i)
    td = min(t, s["freeze"]) if s.get("freeze") else t
    if s["name"] == "s03a_cab":
        speed_lines(g, min(1.0, TL.mach(t) / 10), i)
    O.timer(g, "出発から", (fmt_t(td, tag), "秒"), tag[0], O.TAG_GREEN if tag[1] == "green" else O.TAG_ORANGE)
    w = s.get("widget")
    if w == "auto":
        w = "mach" if t < 1.0 else "dist"
    if w == "mach":
        O.speed(g, "新幹線の速さ", "マッハ", fmt_mach(TL.mach(t)))
    else:
        O.speed(g, "新横浜まで", "", fmt_km(TL.remain_km(td)), "km")
    if s.get("note") and s["note"][0] <= sec < s["note"][1]:
        O.note(g, s["note"][2])
    for a, b, lines in s.get("captions", []):
        if a <= sec < b:
            O.caption(g, lines)
    if s.get("info"):
        title, rows = s["info"]
        shown = [(ic, tx, col) for (at, ic, tx, col) in rows if sec >= at]
        O.info_box(g, title, shown)
    return g


def rewind_frames(cache, n):
    """「◀◀ リプレイ」：直前の場面を速く逆に流す。"""
    src = cache[::-1]
    out = []
    for k in range(n):
        im = src[int(k * (len(src) - 1) / max(1, n - 1))].copy()
        a = np.asarray(im.convert("RGB")).astype(np.int16)
        a = np.roll(a, 6, axis=1) * np.array([1.0, 0.9, 0.9])
        a[::4] = a[::4] * 0.7                       # 走査線
        g = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
        O.watermark(g)
        t = TL.T_ARRIVE * (1 - k / (n - 1)) + 0.083 * (k / (n - 1))
        O.timer(g, "出発から", (f"{t:.2f}", "秒"))
        O.rewind(g, k)
        out.append(g)
    return out


# ---------- 音（ナレーションなし、効果音と BGM） ----------
def tone(dur, f0, f1=None, kind="sine"):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = f0 if f1 is None else f0 + (f1 - f0) * tt / dur
    ph = 2 * np.pi * np.cumsum(np.full(n, 1.0) * f) / SR
    return np.sin(ph)


def noise(dur, seed=0):
    return np.random.default_rng(seed).standard_normal(int(dur * SR))


def lp(x, cutoff):
    a = 1 - math.exp(-2 * math.pi * cutoff / SR)
    return lfilter([a], [1, a - 1], x)


def env(n, attack, decay):
    tt = np.arange(n) / SR
    return np.minimum(tt / max(attack, 1e-3), 1.0) * np.exp(-tt / decay)


def sfx_boom(dur=2.5, seed=1):
    n = int(dur * SR)
    b = tone(dur, 55, 32) * env(n, 0.005, 0.6) + 0.6 * lp(noise(dur, seed), 300) * env(n, 0.002, 0.35)
    return b * 0.9


def sfx_whoosh(dur=1.2, up=True, seed=2):
    n = int(dur * SR)
    x = noise(dur, seed)
    tt = np.arange(n) / SR
    shape = np.sin(np.pi * tt / dur) ** 2
    cut = 400 + 3000 * (tt / dur if up else 1 - tt / dur)
    y = np.zeros(n)
    blk = 2048
    for i in range(0, n, blk):
        y[i:i + blk] = lp(x[i:i + blk], cut[i])
    return y * shape * 1.2


def sfx_tick():
    n = int(0.12 * SR)
    return tone(0.12, 1200) * env(n, 0.001, 0.03) * 0.5


def sfx_crackle(dur, seed=3):
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    y = lp(noise(dur, seed), 900) * 0.25
    for _ in range(int(dur * 40)):
        p = r.integers(0, n - 2000)
        y[p:p + 2000] += r.uniform(0.2, 0.6) * np.exp(-np.arange(2000) / 200) * r.choice((-1, 1))
    return y


def sfx_splash(dur=2.0, seed=4):
    n = int(dur * SR)
    x = noise(dur, seed)
    return (x - lp(x, 1500)) * env(n, 0.01, 0.5) * 0.7


def sfx_screech(dur=1.5):
    n = int(dur * SR)
    return (tone(dur, 2400, 2600) * 0.3 + 0.2 * (noise(dur, 9) - lp(noise(dur, 9), 3000))) * env(n, 0.05, 0.8)


def build_audio(total, starts):
    a = np.zeros(int(total * SR) + SR)

    def put(x, at, gain=1.0):
        i = int(at * SR)
        j = min(len(a), i + len(x))
        a[i:j] += gain * x[: j - i]

    for k in range(5):
        put(sfx_tick(), k + 0.05, 0.6)
    st = starts
    put(sfx_screech(1.5), st["s02_wheel"], 0.5)
    put(sfx_boom(2.5), st["s02_wheel"] + 1.45, 0.8)
    put(sfx_whoosh(1.4, True, 5), st["s03a_cab"], 1.0)
    put(sfx_boom(2.0, 6), st["s03b_shinagawa"] + (TL.T_SHINAGAWA - 1.2), 0.9)
    put(sfx_boom(2.0, 7), st["s03c_tama"] + (TL.T_TAMA - 2.8), 0.8)
    put(sfx_splash(2.0, 8), st["s03c_tama"] + (TL.T_TAMA - 2.8) + 0.1, 0.6)
    put(sfx_boom(2.0, 9), st["s03d_town"] + 0.2, 0.8)
    put(sfx_boom(3.0, 10), st["s03e_arrive"] + (TL.T_ARRIVE - 6.6), 1.0)
    put(sfx_whoosh(0.7, False, 11), st["s05_rewind"], 0.8)
    s6 = TL.shot("s06_boom")
    t1 = st["s06_boom"] + (0.1 - 0.07) / (0.133 - 0.07) * s6["frames"] / FPS
    put(sfx_boom(3.5, 12) * 1.2, t1, 1.0)
    put(sfx_crackle(4.0), st["s07_heat"], 0.6)
    put(sfx_whoosh(3.0, False, 13), st["s08_streak"] + 1.0, 0.8)
    put(sfx_crackle(4.5, 14), st["s09_sound"], 0.35)
    put(sfx_whoosh(1.0, True, 15), st["s10_after"] + 0.2, 0.6)
    put(sfx_boom(2.5, 16), st["s10_after"] + 1.0, 0.9)
    put(sfx_boom(2.5, 17), st["s11_bench"] + 0.6, 0.9)
    put(sfx_whoosh(2.0, False, 18), st["s11_bench"] + 2.0, 0.7)
    put(sfx_boom(2.5, 19), st["s13_fisher"] + 0.3, 0.6)
    put(sfx_splash(3.0, 20), st["s14_river"] + 0.8, 0.8)
    put(sfx_boom(2.5, 21), st["s14_river"] + 0.6, 0.7)
    a = a / max(1e-6, np.abs(a).max()) * 0.8
    return a


def main():
    total_frames = TL.total_frames()
    total = total_frames / FPS
    starts, k = {}, 0
    for s in TL.SHOTS:
        starts[s["name"]] = k / FPS
        k += s["frames"]
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{O.W}x{O.H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                            out + ".video.mp4"], stdin=subprocess.PIPE)
    cache = []
    for s in TL.SHOTS:
        if s.get("kind") == "rewind":
            for g in rewind_frames(cache, s["frames"]):
                enc.stdin.write(g.convert("RGB").tobytes())
            cache = []
            continue
        name = "s01_open" if s.get("kind") == "open" else s["name"]
        paths, suns = load_frames(name, s["frames"])
        prev_p, prev_img = None, None
        for i, (p, sun) in enumerate(zip(paths, suns)):
            if p != prev_p:
                prev_img, prev_p = Image.open(p).convert("RGB"), p
            g = draw_shot(s, i, prev_img, sun)
            if s["name"].startswith("s03"):
                cache.append(g.convert("RGB").resize((540, 960)).resize((O.W, O.H)))
            enc.stdin.write(g.convert("RGB").tobytes())
        print("composed", s["name"], flush=True)
    enc.stdin.close()
    enc.wait()
    audio = build_audio(total, starts)
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
        fc += f";[2:a]volume=0.22,atrim=0:{total:.2f},afade=t=out:st={total - 2:.2f}:d=2[b];[s][b]amix=inputs=2:normalize=0[m];[m]loudnorm=I=-14:TP=-1.5[a]"
    else:
        fc += ";[s]loudnorm=I=-14:TP=-1.5[a]"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", out], check=True)
    os.remove(out + ".video.mp4")
    print("done", out, f"{total:.2f}s")


if __name__ == "__main__":
    main()
