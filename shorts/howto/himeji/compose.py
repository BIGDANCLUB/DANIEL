"""「姫路城の作り方」の合成：参考元（0秒博士）の型の字幕＋左上の CASTLE KIT ＋右上の見張りの画面＋白い輪＋ナレーション＋BGM＋効果音。
usage: python3 compose.py frames_root out.mp4   → 59.9秒ちょうど"""
import importlib.util
import json
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("hj_timeline", os.path.join(HERE, "timeline.py"))
TL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(TL)

FPS = TL.FPS
W, H = 1080, 1920
RW = 540                       # 3D の書き出しの横幅（印の座標をこの倍率で広げる）
SR = 44100
FONT = os.path.join(HERE, "..", "..", "fonts", "NotoSansJP[wght].ttf")
BGM = os.path.join(HERE, "..", "..", "bgm", "howto_wafu.wav")
TIMING = json.load(open(os.path.join(HERE, "voice", "timing.json")))
LINES = TIMING["lines"]

OW = TL.global_anchors()


def W2(t):
    """v2 の時刻 → v3 の時刻（動きに合わせた効果音・白い輪など）。"""
    return TL.warp(OW, t)


def LT(i):
    """v3 の台本の i 行目のはじまり（秒）。"""
    return LINES[i]["start"]


# 左上のチェックリスト：(秒, 項目)。「これが○○です」などの句の頭
KIT = [(LT(6), "石垣"), (LT(10), "扇の勾配"), (LT(19), "石落とし"), (LT(23), "せまい門"), (LT(32), "狭間"), (LT(35), "白漆喰")]
# 右上の見張りの画面の状態：(はじまりの秒, 状態)。None は出さない
STATUS = [(0.0, "防衛"), (LT(2), "侵入"), (LT(6), "防衛"), (LT(11), "苦戦"), (LT(12), "防衛"), (LT(13), "苦戦"), (LT(19), "防衛"),
          (LT(20), "苦戦"), (LT(24), "防衛"), (LT(26), "侵入"), (LT(30), "防衛"), (LT(33), "苦戦"), (LT(35), "防衛"), (LT(36), None)]
ST_COL = {"侵入": (235, 40, 40), "苦戦": (255, 150, 20), "防衛": (40, 200, 90)}
# 白い輪：(場面, 印の名前, はじまり秒, おわり秒)（秒は全体の時間）
RINGS = [("h01_house", "climb", W2(4.85), LT(4) - 0.05), ("h04_fall", "climber", LT(11) + 0.05, LT(12) - 0.05),
         ("h05_corner", "ishiotoshi", LT(17), LT(18) + 0.4), ("h06_gate", "two", LT(23), LT(24) - 0.05),
         ("h07_sama", "holes", W2(35.75), LT(29) - 0.1)]
# 画面の上に大きく出す文字：(はじまり秒, おわり秒, 文字)
OVER = [(l["start"], (LINES[i + 1]["start"] if i + 1 < len(LINES) else TL.TOTAL), l["over"]) for i, l in enumerate(LINES) if l.get("over")]
OVER = [(a, (b if txt != "2026年" else 58.6), txt) for a, b, txt in OVER] + [(LT(32) + 0.95, LT(33) - 0.1, "997")]


def font(size, weight=800):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


F_CAP = font(56, 700)
F_OVER = font(150, 900)
F_KIT_H = font(30, 900)
F_KIT = font(36, 800)
F_ST = font(34, 900)


def outlined(g, xy, text, f, fill=(255, 255, 255), stroke=7, anchor="mm", shadow=True, alpha=255):
    lay = Image.new("RGBA", g.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    if shadow:
        sh = Image.new("RGBA", g.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0] + 4, xy[1] + 6), text, font=f, fill=(0, 0, 0, int(150 * alpha / 255)), anchor=anchor,
                                stroke_width=stroke, stroke_fill=(0, 0, 0, int(150 * alpha / 255)))
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d.text(xy, text, font=f, fill=(*fill, alpha), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, alpha))
    g.alpha_composite(lay)


def caption(g, t):
    """字幕：白・黒い縁と影。画面の上から約67%の高さに1行（参考元と同じ）。句から次の句まで出しっぱなし。"""
    cur = None
    for i, l in enumerate(LINES):
        nxt = LINES[i + 1]["start"] if i + 1 < len(LINES) else TL.TOTAL
        if l["start"] - 0.03 <= t < nxt - 0.03:
            cur = l
    if cur is None:
        return
    txt = cur["text"].replace(" ", "　")
    f = F_CAP
    while f.getlength(txt) > W - 90 and f.size > 40:
        f = font(f.size - 2, 700)
    outlined(g, (W // 2, int(H * 0.67)), txt, f, stroke=4)


MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-ExtraBold.ttf"


def mono(size):
    try:
        return ImageFont.truetype(MONO, size)
    except Exception:
        return font(size, 900)


F_HEAD = mono(30)
F_ITEM = font(34, 700)
F_RAD = mono(22)


def kit(g, t):
    """左上：作ったものが ✓ で増えていくチェックリスト（参考元2と同じ形：黄色い見出し＋項目ごとの黒い札）。"""
    items = [(ts, name) for ts, name in KIT if t >= ts]
    x0, y0 = 30, 120
    lay = Image.new("RGBA", g.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((x0, y0), "CASTLE KIT", font=F_HEAD, fill=(255, 196, 40, 255), stroke_width=3, stroke_fill=(40, 25, 0, 200))
    for k, (ts, name) in enumerate(items):
        y = y0 + 46 + 62 * k
        age = t - ts
        a = min(1.0, age / 0.15)
        tw = F_ITEM.getlength(name)
        x1 = x0 + 62 + tw + 20
        slide = int((1 - a) * -40)
        d.rounded_rectangle((x0 + slide, y, x1 + slide, y + 54), 7, fill=(38, 42, 48, int(205 * a)), outline=(255, 255, 255, int(40 * a)),
                            width=2)
        d.text((x0 + 18 + slide, y + 27), "✓", font=F_ITEM, fill=(150, 235, 140, int(255 * a)), anchor="lm")
        d.text((x0 + 58 + slide, y + 27), name, font=F_ITEM, fill=(255, 255, 255, int(255 * a)), anchor="lm")
        if age < 0.7:
            k2 = 1 - age / 0.7
            d.rounded_rectangle((x0 - 4, y - 4, x1 + 4, y + 58), 9, outline=(255, 210, 60, int(255 * k2)), width=4)
    g.alpha_composite(lay)


def status_at(t):
    s = None
    for ts, st in STATUS:
        if t >= ts:
            s = st
    return s


def scope(g, t):
    """右上：見張りの丸い画面（参考元2の ENEMY RADAR と同じ形）と状態の札（侵入 赤／苦戦 橙／防衛 緑）。"""
    st = status_at(t)
    if st is None:
        return
    cx, cy, R = W - 168, 268, 110
    lay = Image.new("RGBA", g.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((cx, cy - R - 22), "ENEMY RADAR", font=F_RAD, fill=(150, 230, 170, 230), anchor="mm")
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(4, 34, 18, 225), outline=(90, 200, 120, 200), width=3)
    for rr in (R * 0.33, R * 0.66):
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(70, 170, 100, 110), width=2)
    d.line((cx - R, cy, cx + R, cy), fill=(70, 170, 100, 110), width=2)
    d.line((cx, cy - R, cx, cy + R), fill=(70, 170, 100, 110), width=2)
    ang = math.degrees(t * 2.4) % 360
    d.pieslice((cx - R, cy - R, cx + R, cy + R), ang - 50, ang, fill=(110, 255, 150, 70))
    d.line((cx, cy, cx + R * math.cos(math.radians(ang)), cy + R * math.sin(math.radians(ang))), fill=(150, 255, 180, 220), width=3)
    d.rectangle((cx - 12, cy - 10, cx + 12, cy + 10), outline=(255, 255, 255, 220), width=3)       # 城
    n = {"侵入": 4, "苦戦": 3, "防衛": 1}[st]
    rng = np.random.default_rng(3)
    blobs = Image.new("RGBA", g.size, (0, 0, 0, 0))
    db = ImageDraw.Draw(blobs)
    for k in range(n):
        base = rng.uniform(0, 2 * math.pi)
        r0 = rng.uniform(0.5, 0.9)
        if st == "侵入":
            r0 = max(0.15, r0 - 0.3 * ((t * 0.5 + k * 0.2) % 1.0))
        elif st == "防衛":
            r0 = min(0.95, r0 + 0.25 * ((t * 0.3) % 1.0))
        a = base + 0.1 * math.sin(t * 1.3 + k)
        x, y = cx + R * r0 * math.cos(a), cy + R * r0 * math.sin(a)
        db.ellipse((x - 13, y - 13, x + 13, y + 13), fill=(255, 140, 30, 150))
        db.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(255, 200, 80, 255))
    lay.alpha_composite(blobs.filter(ImageFilter.GaussianBlur(3)))
    col = ST_COL[st]
    tw = F_ST.getlength(st)
    bx0, by0 = cx - tw / 2 - 22, cy + R + 22
    d.rounded_rectangle((bx0, by0, bx0 + tw + 44, by0 + 54), 6, fill=(25, 22, 20, 220), outline=(*col, 255), width=4)
    d.text((cx, by0 + 27), st, font=F_ST, fill=(*col, 255), anchor="mm")
    g.alpha_composite(lay)


def over_text(g, t):
    for a, b, txt in OVER:
        if a <= t < b:
            age = t - a
            s = 1.0 + 0.25 * max(0.0, 1 - age / 0.18)
            f = font(int(150 * s), 900)
            outlined(g, (W // 2, 560), txt, f, fill=(255, 255, 255), stroke=9)


MARKERS = {}


def ring(g, name, scene, f_local, age, dur):
    mk = MARKERS.get(scene)
    if mk is None:
        p = os.path.join(ROOT, scene, "markers.json")
        mk = MARKERS[scene] = json.load(open(p)) if os.path.exists(p) else {}
    keys = sorted(int(k) for k in mk)
    if not keys:
        return
    k = min(keys, key=lambda q: abs(q - f_local))
    v = mk[str(k)].get(name)
    if not v or v[2] <= 0:
        return
    sc = W / RW
    x, y = v[0] * sc, v[1] * sc
    pop = min(1.0, age / 0.15)
    out = 1.0 - max(0.0, (age - (dur - 0.15)) / 0.15)
    r = 110 * (0.6 + 0.4 * pop) + 6 * math.sin(age * 6)
    lay = Image.new("RGBA", g.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    a = int(255 * min(pop, out))
    d.ellipse((x - r - 3, y - r - 3, x + r + 3, y + r + 3), outline=(0, 0, 0, a // 3), width=14)
    d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 255, a), width=9)
    g.alpha_composite(lay)


GRADE = dict(lo=0.04, hi=0.97, gam=1.0, sat=1.12, r=1.0, b=1.0)


def grade(img, g=None):
    """参考元に合わせた色：黒をしめて（影 lo 約30）、色を濃く（彩度 約38）、少し暖かく（計測で決めた値）。"""
    g = g or GRADE
    a = np.asarray(img, np.float32) / 255
    a = np.clip((a - g["lo"]) / (g["hi"] - g["lo"]), 0, 1) ** g["gam"]
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = lum[..., None] + (a - lum[..., None]) * g["sat"]
    a = a * np.array([g["r"], 1.0, g["b"]], np.float32)
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


ROOT = None


def frame_source(scene, i):
    """3D は 2コマおきに書き出している。間のコマは前後の平均（カットをまたぐときは前のコマ）。"""
    d = os.path.join(ROOT, scene)

    def load(k):
        p = os.path.join(d, f"f_{k:04d}.png")
        return Image.open(p).convert("RGB") if os.path.exists(p) else None
    cur = load(i + 1)
    if cur is not None:
        return cur
    a, b = None, None
    for k in range(i, 0, -1):
        a = load(k)
        if a is not None:
            break
    for k in range(i + 2, i + 5):
        b = load(k)
        if b is not None:
            break
    if a is None:
        return b
    if b is None:
        return a
    A, B = np.asarray(a, np.float32), np.asarray(b, np.float32)
    if np.abs(A - B).mean() > 28:
        return a
    return Image.fromarray(((A + B) / 2 + 0.5).astype(np.uint8))


# ---------- 音 ----------
def env(n, att, dec):
    t = np.arange(n) / SR
    return np.minimum(t / max(att, 1e-4), 1) * np.exp(-t / dec)


def noise(dur, seed=0):
    return np.random.default_rng(seed).standard_normal(int(dur * SR))


def lp(x, cut):
    a = math.exp(-2 * math.pi * cut / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def lp_fast(x, cut):
    """周波数の領域で低い音だけ残す（速い）。"""
    X = np.fft.rfft(x)
    fq = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (fq / cut) ** 4)
    return np.fft.irfft(X, len(x))


def hp_fast(x, cut):
    X = np.fft.rfft(x)
    fq = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (cut / np.maximum(fq, 1)) ** 4)
    return np.fft.irfft(X, len(x))


def whoosh(dur=0.6, seed=1, up=True):
    n = int(dur * SR)
    x = hp_fast(noise(dur, seed), 300)
    t = np.linspace(0, 1, n)
    e = np.sin(np.pi * t) ** 1.5
    return lp_fast(x, 2500) * e * 0.6


def thud(seed=0, f=70, dur=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t / 0.03))) / SR) * np.exp(-t / 0.12)
    hit = lp_fast(noise(dur, seed), 900) * np.exp(-t / 0.02)
    return (body + 0.6 * hit) * 0.9


def clack(seed=0):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    x = hp_fast(noise(0.12, seed), 800) * np.exp(-t / 0.012)
    x += np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.02) * 0.4
    return x * 0.6


def bang(seed=0):
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    x = noise(0.6, seed) * np.exp(-t / 0.06)
    x = lp_fast(x, 3000) + 0.6 * np.sin(2 * np.pi * 60 * t) * np.exp(-t / 0.08)
    return x * 0.8


def fwip(seed=0):
    n = int(0.25 * SR)
    t = np.linspace(0, 1, n)
    x = hp_fast(noise(0.25, seed), 1500) * np.sin(np.pi * t) ** 2
    return x * 0.35


def crackle(dur, seed=0, density=60):
    n = int(dur * SR)
    x = lp_fast(noise(dur, seed), 600) * 0.25
    rng = np.random.default_rng(seed)
    for k in rng.uniform(0, dur, int(dur * density)):
        i = int(k * SR)
        m = min(n - i, 300)
        x[i:i + m] += rng.uniform(-1, 1) * np.exp(-np.arange(m) / 40.0)
    return x * 0.5


def swish(dur=0.9, seed=0):
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    x = lp_fast(hp_fast(noise(dur, seed), 500), 4000) * (np.sin(np.pi * t) ** 0.8)
    return x * 0.4


def ding():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1976 * t)) * np.exp(-t / 0.25)
    return x * 0.35


def drone(dur, seed=0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t + p) for f, p in ((38, 0), (41, 1), (76, 2), (82, 3))) * 0.25
    x += lp_fast(noise(dur, seed), 200) * 0.6
    return x * np.minimum(1, t / 0.5) * 0.5


def roar(dur, seed=0):
    t = np.arange(int(dur * SR)) / SR
    return lp_fast(noise(dur, seed), 400) * (0.6 + 0.4 * np.sin(t * 3)) * 0.7


def cheer(dur, seed=0):
    t = np.arange(int(dur * SR)) / SR
    x = lp_fast(hp_fast(noise(dur, seed), 400), 3000)
    return x * np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.8) * 0.5


def rumble(dur, seed=0):
    t = np.arange(int(dur * SR)) / SR
    return lp_fast(noise(dur, seed), 120) * np.sin(np.pi * t / dur) * 1.2


def read_wav(p):
    with wave.open(p) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        if w.getnchannels() == 2:
            x = x.reshape(-1, 2).mean(1)
    if sr != SR:
        n = int(len(x) * SR / sr)
        x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
    return x


def limiter(x, ceil=0.78, look=0.003, rel=0.12):
    """先読みのピーク制限（声と効果音の山だけ下げて、全体を大きくできるように）。"""
    n = len(x)
    L = max(1, int(look * SR))
    need = np.minimum(1.0, ceil / np.maximum(np.abs(x), 1e-9))
    pad = np.concatenate([need, np.ones(L)])
    win = np.lib.stride_tricks.sliding_window_view(pad, L + 1)[:n].min(1)
    try:
        from scipy.signal import lfilter
        a = math.exp(-1 / (rel * SR))
        # 下げるのはすぐ、戻すのはゆっくり：1-g を「最大値を保ちながら減衰」させる
        r = 1 - win
        out = np.empty(n)
        acc = 0.0
        for i in range(0, n, 4096):
            seg = r[i:i + 4096]
            y = np.empty(len(seg))
            for j, v in enumerate(seg):
                acc = v if v > acc else acc * a
                y[j] = acc
            out[i:i + 4096] = y
        g = 1 - out
        _ = lfilter
    except Exception:
        g = win
    return x * g


def lufs(x):
    p = "/tmp/_hj_lufs.wav"
    with wave.open(p, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    r = subprocess.run(["ffmpeg", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in r.splitlines() if l.strip().startswith("I:")][-1].split()[1])


def loudness_to(x, target=-13.0):
    """参考元（約 -12〜-13 LUFS）に合わせる：大きさを上げて、山は先読みで抑える。"""
    for _ in range(8):
        I = lufs(x)
        if abs(I - target) < 0.25:
            break
        x = limiter(x * 10 ** ((target - I) / 20 * 1.3))
    return x


def build_audio(total):
    n = int(total * SR)
    voice = np.zeros(n + SR)
    sfx = np.zeros(n + SR)

    def putn(buf, x, at, g=1.0):
        """at は v3 の時刻。"""
        i = int(at * SR)
        j = min(len(buf), i + len(x))
        if j > i and i >= 0:
            buf[i:j] += g * x[: j - i]

    def put(buf, x, at, g=1.0):
        """at は v2 の時刻（場面の動きに合わせた効果音）。v3 へ写して置く。"""
        putn(buf, x, W2(at), g)
    for l in LINES:
        putn(voice, read_wav(l["wav"]), l["start"], 1.0)
    st = {name: t for name, t in TL.OLD_CUTS}          # v2 の場面の頭（put で v3 へ写る）
    # 1) 冒頭：塀がドドドッと飛び出す、カメラがシュッと引く、梯子がガシャッ、登る音
    put(sfx, whoosh(0.9, 1), 0.15, 0.9)
    for k, ts in enumerate([0.10, 0.30, 0.30, 0.95, 1.07]):
        put(sfx, thud(k, 60 + 8 * k), ts + 0.15, 0.8)
    put(sfx, thud(9, 55, 0.8), 1.25, 0.6)
    for k in range(8):
        put(sfx, clack(10 + k), 3.5 + 0.08 * k, 0.5)
        for j in range(4):
            put(sfx, clack(30 + k * 4 + j), 4.4 + 0.08 * k + j * 0.22, 0.25)
    put(sfx, whoosh(0.7, 3), 3.0, 0.6)
    # 2) 石垣：段ごとにゴトッ、着地でドン
    for k in range(16):
        put(sfx, thud(40 + k, 90 + 4 * k, 0.3), st["h02_stone"] + 0.45 + k * 0.12, 0.45)
    put(sfx, thud(60, 45, 1.0), st["h02_stone"] + 2.30, 1.0)
    put(sfx, rumble(1.2, 61), st["h02_stone"] + 2.25, 0.6)
    putn(sfx, ding(), LT(6), 0.8)
    # 3) 扇の勾配：線が伸びるシュー
    for k, ts in enumerate([9.55, 10.75, 12.25]):
        put(sfx, swish(0.9, 70 + k), ts, 0.5)
    putn(sfx, ding(), LT(10), 0.8)
    put(sfx, whoosh(0.8, 71), 13.95, 0.6)
    # 4) 落ちる
    for k in range(4):
        put(sfx, whoosh(0.5, 80 + k), 17.3 + 0.12 * k, 0.5)
        put(sfx, thud(85 + k, 70, 0.5), 18.15 + 0.12 * k, 0.6)
    # 5) 角：走る足音、櫓がドンドン組み上がる、蓋がバタン、石がゴロゴロ
    for k in range(10):
        put(sfx, clack(100 + k), st["h05_corner"] + 0.2 + 0.13 * k, 0.2)
    for k in range(5):
        put(sfx, thud(110 + k, 80, 0.4), 20.75 + 0.3 * k, 0.6)
    put(sfx, clack(120), 22.6, 0.9)
    put(sfx, thud(121, 120, 0.3), 22.62, 0.5)
    put(sfx, rumble(1.4, 122), 23.75, 0.9)
    for k in range(5):
        put(sfx, thud(125 + k, 65, 0.5), 24.1 + 0.18 * k, 0.7)
    putn(sfx, ding(), LT(19), 0.8)
    # 6) 門：群れの足音、石垣がゴゴゴと寄る、矢の雨
    put(sfx, roar(2.0, 130), st["h06_gate"] + 0.1, 0.3)
    put(sfx, rumble(1.0, 131), 27.2, 1.0)
    putn(sfx, ding(), LT(23), 0.8)
    for k in range(26):
        put(sfx, fwip(140 + k), 29.9 + 0.06 * k, 0.5)
    for k in range(10):
        put(sfx, thud(170 + k, 75, 0.3), 30.3 + 0.12 * k, 0.4)
    # 7) 鉄砲：パーン、木づちでコーン
    for k in range(10):
        put(sfx, bang(180 + k), 33.7 + 0.2 * k, 0.6)
    for k, ts in enumerate([35.75, 36.25, 36.75]):
        put(sfx, thud(190 + k, 140, 0.35), ts, 0.9)
        put(sfx, clack(195 + k), ts, 0.8)
    put(sfx, whoosh(0.9, 199), st["h07_sama"] + 0.4, 0.7)
    # 8) 狭間：「穴は内側が広く外側が狭い」で台形のふちが光る（v3 で足した句）、弾がカキン、数える音
    putn(sfx, swish(0.8, 205), LT(29) + 0.2, 0.6)
    putn(sfx, ding(), LT(29) + 0.45, 0.35)
    for k in range(6):
        put(sfx, bang(200 + k), 37.85 + 0.22 * k, 0.35)
        put(sfx, clack(210 + k), 38.15 + 0.22 * k, 0.4)
    putn(sfx, ding(), LT(32), 0.8)
    for k in range(30):
        put(sfx, clack(220 + k) * 0.5, 41.6 + 0.05 * k, 0.35)
    # 9) 火矢：ヒュン、ボッ、パチパチ → こてのシャーッ → ジュッ
    for k in range(7):
        put(sfx, fwip(260 + k), st["h09_fire"] + 0.1 + 0.2 * k, 0.6)
        put(sfx, thud(270 + k, 150, 0.25), st["h09_fire"] + 0.65 + 0.2 * k, 0.4)
    put(sfx, crackle(3.0, 280), st["h09_fire"] + 0.7, 0.6)
    put(sfx, swish(1.1, 281), 46.45, 0.8)
    put(sfx, swish(1.0, 282), 47.6, 0.8)
    putn(sfx, ding(), LT(35), 0.8)
    # 10) 完成：ドドン、時が流れるシュー、1945年の爆撃機と火、2026年の歓声
    for k in range(5):
        put(sfx, thud(300 + k, 70, 0.5), st["h10a_1609"] + 0.15 + 0.27 * k, 0.6)
    put(sfx, whoosh(1.2, 305), st["h10a_1609"] + 1.5, 0.5)
    put(sfx, drone(2.7, 310), st["h10b_1945"], 0.6)
    put(sfx, crackle(2.7, 311, 90), st["h10b_1945"], 0.5)
    put(sfx, whoosh(0.8, 312), st["h10c_final"] - 0.3, 0.6)
    putn(sfx, cheer(3.6, 320), LT(39) - 0.1, 0.6)
    putn(sfx, ding(), LT(40) - 0.09, 0.9)
    bgm = read_wav(BGM)[:n + SR]
    bgm = np.pad(bgm, (0, max(0, n + SR - len(bgm))))
    t = np.arange(len(bgm)) / SR
    bgm *= np.clip((total - t) / 1.5, 0, 1)
    v = voice / max(1e-6, np.abs(voice).max()) * 0.9
    s = sfx / max(1e-6, np.abs(sfx).max()) * 0.45
    b = bgm / max(1e-6, np.abs(bgm).max()) * 0.16
    mix = v + s + b
    mix = mix[:n] / max(1e-6, np.abs(mix).max()) * 0.78
    return loudness_to(mix, -13.0)


def main():
    global ROOT
    ROOT, out = sys.argv[1], sys.argv[2]
    total = TL.TOTAL
    fr_tab = TL.frames()
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", out + ".video.mp4"],
                           stdin=subprocess.PIPE)
    for name, _ in TL.CUTS:
        f0, nf = fr_tab[name]
        for i in range(nf):
            t = (f0 + i) / FPS
            src = frame_source(name, i)
            g = grade(src).resize((W, H), Image.LANCZOS).convert("RGBA")
            for sc, mk, a, b in RINGS:
                if sc == name and a <= t < b:
                    ring(g, mk, sc, i + 1, t - a, b - a)
            over_text(g, t)
            kit(g, t)
            scope(g, t)
            caption(g, t)
            enc.stdin.write(g.convert("RGB").tobytes())
        print("composed", name, flush=True)
    enc.stdin.close()
    enc.wait()
    audio = build_audio(total)
    wav = out + ".mix.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", out + ".video.mp4", "-i", wav, "-filter_complex",
                    "[1:a]anull[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "44100", "-t", f"{total:.3f}", "-movflags", "+faststart", out], check=True)
    os.remove(out + ".video.mp4")
    os.remove(wav)
    print("done", out, f"{total:.2f}s")


if __name__ == "__main__":
    main()
