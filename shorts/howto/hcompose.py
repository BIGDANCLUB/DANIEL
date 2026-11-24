"""作り方シリーズ共通の合成（忍者屋敷・核シェルター〜）。姫路城（himeji/compose.py）と同じ見た目：
参考元（0秒博士）の型の字幕＋左上の KIT のチェックリスト＋右上の小さな画面（敵のレーダー／放射線の計器）＋白い輪＋大きな文字＋ナレーション＋BGM＋効果音。
動画ごとの中身（KIT の項目・状態・効果音など）は各フォルダの compose.py に書いて、run(cfg, folder) を呼ぶ。"""
import json
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from htimeline import Timeline

W, H = 1080, 1920
RW = 540                       # 3D の書き出しの横幅（印の座標をこの倍率で広げる）
SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "NotoSansJP[wght].ttf")
MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-ExtraBold.ttf"


def font(size, weight=800):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def mono(size):
    try:
        return ImageFont.truetype(MONO, size)
    except Exception:
        return font(size, 900)


F_CAP = font(56, 700)
F_ST = font(34, 900)
F_HEAD = mono(30)
F_ITEM = font(34, 700)
F_RAD = mono(22)


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


class Composer:
    def __init__(self, cfg, folder):
        self.cfg = cfg
        self.TL = Timeline(folder)
        self.LINES = self.TL.lines
        self.markers = {}
        self.root = None

    # ---------- 画面の上にのせるもの ----------
    def caption(self, g, t):
        """字幕：白・黒い縁と影。画面の上から約67%の高さに1行。句から次の句まで出しっぱなし。"""
        cur = None
        L = self.LINES
        for i, l in enumerate(L):
            nxt = L[i + 1]["start"] if i + 1 < len(L) else self.TL.TOTAL
            if l["start"] - 0.03 <= t < nxt - 0.03:
                cur = l
        if cur is None:
            return
        txt = cur["text"].replace(" ", "　")
        f = F_CAP
        while f.getlength(txt) > W - 90 and f.size > 40:
            f = font(f.size - 2, 700)
        outlined(g, (W // 2, int(H * 0.67)), txt, f, stroke=4)

    def kit(self, g, t):
        """左上：作ったものが ✓ で増えていくチェックリスト（黄色い見出し＋項目ごとの黒い札、新しい項目は一瞬光る）。"""
        items = [(ts, name) for ts, name in self.cfg.KIT if t >= ts]
        x0, y0 = 30, 120
        lay = Image.new("RGBA", g.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.text((x0, y0), self.cfg.KIT_TITLE, font=F_HEAD, fill=(255, 196, 40, 255), stroke_width=3, stroke_fill=(40, 25, 0, 200))
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

    def status_at(self, t):
        s = None
        for ts, st in self.cfg.STATUS:
            if t >= ts:
                s = st
        return s

    def _badge(self, d, cx, top, st):
        col = self.cfg.ST_COL[st]
        tw = F_ST.getlength(st)
        bx0 = cx - tw / 2 - 22
        d.rounded_rectangle((bx0, top, bx0 + tw + 44, top + 54), 6, fill=(25, 22, 20, 220), outline=(*col, 255), width=4)
        d.text((cx, top + 27), st, font=F_ST, fill=(*col, 255), anchor="mm")

    def scope(self, g, t):
        st = self.status_at(t)
        if st is None:
            return
        if getattr(self.cfg, "SCOPE", "radar") == "gauge":
            return self.gauge(g, t, st)
        cx, cy, R = W - 168, 268, 110
        lay = Image.new("RGBA", g.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.text((cx, cy - R - 22), self.cfg.SCOPE_TITLE, font=F_RAD, fill=(150, 230, 170, 230), anchor="mm")
        d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(4, 34, 18, 225), outline=(90, 200, 120, 200), width=3)
        for rr in (R * 0.33, R * 0.66):
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(70, 170, 100, 110), width=2)
        d.line((cx - R, cy, cx + R, cy), fill=(70, 170, 100, 110), width=2)
        d.line((cx, cy - R, cx, cy + R), fill=(70, 170, 100, 110), width=2)
        ang = math.degrees(t * 2.4) % 360
        d.pieslice((cx - R, cy - R, cx + R, cy + R), ang - 50, ang, fill=(110, 255, 150, 70))
        d.line((cx, cy, cx + R * math.cos(math.radians(ang)), cy + R * math.sin(math.radians(ang))), fill=(150, 255, 180, 220), width=3)
        d.rectangle((cx - 12, cy - 10, cx + 12, cy + 10), outline=(255, 255, 255, 220), width=3)
        lv = self.cfg.ST_LEVEL[st]                      # 0（安全）〜 2（危ない）
        n = (1, 3, 4)[lv]
        rng = np.random.default_rng(3)
        blobs = Image.new("RGBA", g.size, (0, 0, 0, 0))
        db = ImageDraw.Draw(blobs)
        for k in range(n):
            base = rng.uniform(0, 2 * math.pi)
            r0 = rng.uniform(0.5, 0.9)
            if lv == 2:
                r0 = max(0.15, r0 - 0.3 * ((t * 0.5 + k * 0.2) % 1.0))
            elif lv == 0:
                r0 = min(0.95, r0 + 0.25 * ((t * 0.3) % 1.0))
            a = base + 0.1 * math.sin(t * 1.3 + k)
            x, y = cx + R * r0 * math.cos(a), cy + R * r0 * math.sin(a)
            db.ellipse((x - 13, y - 13, x + 13, y + 13), fill=(255, 140, 30, 150))
            db.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(255, 200, 80, 255))
        lay.alpha_composite(blobs.filter(ImageFilter.GaussianBlur(3)))
        self._badge(d, cx, cy + R + 22, st)
        g.alpha_composite(lay)

    def gauge(self, g, t, st):
        """右上：放射線の計器（半円の目盛り・ふるえる針・状態の札）。レーダーと同じ大きさと色づかい。"""
        cx, cy, R = W - 168, 300, 112
        lay = Image.new("RGBA", g.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.text((cx, cy - R - 50), self.cfg.SCOPE_TITLE, font=F_RAD, fill=(150, 230, 170, 230), anchor="mm")
        d.rounded_rectangle((cx - R - 12, cy - R - 28, cx + R + 12, cy + 30), 14, fill=(4, 34, 18, 225), outline=(90, 200, 120, 200), width=3)
        segs = [((40, 200, 90), 180, 240), ((255, 190, 30), 240, 300), ((235, 40, 40), 300, 360)]
        for col, a0, a1 in segs:
            d.arc((cx - R, cy - R, cx + R, cy + R), a0, a1, fill=(*col, 230), width=16)
        for k in range(13):
            a = math.radians(180 + 15 * k)
            r0, r1 = R - 26, R - (36 if k % 3 == 0 else 31)
            d.line((cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a)), fill=(200, 255, 210, 180), width=3)
        lv = self.cfg.ST_LEVEL[st]
        target = (0.12, 0.5, 0.88)[lv]
        jit = (0.01, 0.03, 0.06)[lv] * math.sin(t * 23) + (0.0, 0.015, 0.04)[lv] * math.sin(t * 37 + 1)
        u = min(0.98, max(0.02, target + jit))
        a = math.radians(180 + 180 * u)
        d.line((cx, cy, cx + (R - 20) * math.cos(a), cy + (R - 20) * math.sin(a)), fill=(255, 255, 255, 240), width=6)
        d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=(255, 255, 255, 240))
        self._badge(d, cx, cy + 46, st)
        g.alpha_composite(lay)

    def over_text(self, g, t):
        for a, b, txt in self.cfg.OVER:
            if a <= t < b:
                age = t - a
                s = 1.0 + 0.25 * max(0.0, 1 - age / 0.18)
                f = font(int(150 * s), 900)
                while f.getlength(txt) > W - 80 and f.size > 60:
                    f = font(f.size - 6, 900)
                outlined(g, (W // 2, 560), txt, f, fill=(255, 255, 255), stroke=9)

    def ring(self, g, name, scene, f_local, age, dur):
        mk = self.markers.get(scene)
        if mk is None:
            p = os.path.join(self.root, scene, "markers.json")
            mk = self.markers[scene] = json.load(open(p)) if os.path.exists(p) else {}
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

    # ---------- 色 ----------
    def grade(self, img):
        g = getattr(self.cfg, "GRADE", GRADE)
        a = np.asarray(img, np.float32) / 255
        a = np.clip((a - g["lo"]) / (g["hi"] - g["lo"]), 0, 1) ** g["gam"]
        lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
        a = lum[..., None] + (a - lum[..., None]) * g["sat"]
        a = a * np.array([g["r"], 1.0, g["b"]], np.float32)
        if getattr(self.cfg, "SKY_LIFT", True):
            a = sky_lift(a)
        return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))

    def frame_source(self, scene, i):
        """3D は 2コマおきに書き出している。間のコマは前後の平均（大きく変わるときは前のコマ）。"""
        d = os.path.join(self.root, scene)

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
    def build_audio(self):
        total = self.TL.TOTAL
        n = int(total * SR)
        voice = np.zeros(n + SR)
        sfx = np.zeros(n + SR)

        def put(x, at, g=1.0, buf=None):
            buf = sfx if buf is None else buf
            i = int(at * SR)
            j = min(len(buf), i + len(x))
            if j > i and i >= 0:
                buf[i:j] += g * x[: j - i]
        for l in self.LINES:
            put(read_wav(l["wav"]), l["start"], 1.0, voice)
        self.cfg.sfx(put, self.TL)
        bgm = read_wav(self.cfg.BGM)[:n + SR]
        bgm = np.pad(bgm, (0, max(0, n + SR - len(bgm))))
        t = np.arange(len(bgm)) / SR
        bgm *= np.clip((total - t) / 1.5, 0, 1)
        v = voice / max(1e-6, np.abs(voice).max()) * 0.9
        s = sfx / max(1e-6, np.abs(sfx).max()) * 0.45
        b = bgm / max(1e-6, np.abs(bgm).max()) * 0.16
        mix = v + s + b
        mix = mix[:n] / max(1e-6, np.abs(mix).max()) * 0.78
        return loudness_to(mix, -13.0)

    def run(self, root, out):
        self.root = root
        TL, cfg = self.TL, self.cfg
        total = TL.TOTAL
        fr_tab = TL.frames()
        enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r",
                                str(TL.FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                                out + ".video.mp4"], stdin=subprocess.PIPE)
        for name, _ in TL.CUTS:
            f0, nf = fr_tab[name]
            for i in range(nf):
                t = (f0 + i) / TL.FPS
                src = self.frame_source(name, i)
                g = self.grade(src).resize((W, H), Image.LANCZOS).convert("RGBA")
                for sc, mk, a, b in cfg.RINGS:
                    if sc == name and a <= t < b:
                        self.ring(g, mk, sc, i + 1, t - a, b - a)
                self.over_text(g, t)
                self.kit(g, t)
                self.scope(g, t)
                self.caption(g, t)
                enc.stdin.write(g.convert("RGB").tobytes())
            print("composed", name, flush=True)
        enc.stdin.close()
        enc.wait()
        audio = self.build_audio()
        wav = out + ".mix.wav"
        with wave.open(wav, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((audio * 32767).astype(np.int16).tobytes())
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", out + ".video.mp4", "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", f"{total:.3f}", "-movflags", "+faststart", out], check=True)
        os.remove(out + ".video.mp4")
        os.remove(wav)
        print("done", out, f"{total:.2f}s")


GRADE = dict(lo=0.04, hi=0.97, gam=1.0, sat=1.12, r=1.0, b=1.0)
# 空の青だけを明るく（姫路城と同じ）：3D の空 (20,45,92) → 参考元の空 (67,93,140) くらいに
SKY = dict(k=0.8, add=(0.20, 0.22, 0.25), br=(0.155, 0.255), bg=(0.08, 0.16))


def sky_lift(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    w = np.clip((b - r - SKY["br"][0]) / (SKY["br"][1] - SKY["br"][0]), 0, 1) * \
        np.clip((b - g - SKY["bg"][0]) / (SKY["bg"][1] - SKY["bg"][0]), 0, 1)
    out = a * SKY["k"] + np.array(SKY["add"], np.float32)
    return a + (out - a) * w[..., None]


# ---------- 効果音の素（合成） ----------
def noise(dur, seed=0):
    return np.random.default_rng(seed).standard_normal(int(dur * SR))


def lp_fast(x, cut):
    X = np.fft.rfft(x)
    fq = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (fq / cut) ** 4)
    return np.fft.irfft(X, len(x))


def hp_fast(x, cut):
    X = np.fft.rfft(x)
    fq = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (cut / np.maximum(fq, 1)) ** 4)
    return np.fft.irfft(X, len(x))


def whoosh(dur=0.6, seed=1):
    n = int(dur * SR)
    x = hp_fast(noise(dur, seed), 300)
    t = np.linspace(0, 1, n)
    return lp_fast(x, 2500) * np.sin(np.pi * t) ** 1.5 * 0.6


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


def creak(seed=0, dur=0.5):
    """木がきしむ音（回る壁、床板）。"""
    t = np.arange(int(dur * SR)) / SR
    f = 180 + 60 * np.sin(t * 9 + seed)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.5 + 0.5 * np.sin(t * 40))
    return lp_fast(x, 1800) * np.sin(np.pi * t / dur) * 0.35


def bang(seed=0):
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    x = noise(0.6, seed) * np.exp(-t / 0.06)
    x = lp_fast(x, 3000) + 0.6 * np.sin(2 * np.pi * 60 * t) * np.exp(-t / 0.08)
    return x * 0.8


def boom(seed=0, dur=3.0):
    """遠くの大きな爆発：低いドーンと長い地鳴り。"""
    t = np.arange(int(dur * SR)) / SR
    x = lp_fast(noise(dur, seed), 160) * np.exp(-t / 0.9) * 2.0
    x += np.sin(2 * np.pi * 38 * t) * np.exp(-t / 0.6)
    return x * np.minimum(1, t / 0.02)


def fwip(seed=0):
    n = int(0.25 * SR)
    t = np.linspace(0, 1, n)
    return hp_fast(noise(0.25, seed), 1500) * np.sin(np.pi * t) ** 2 * 0.35


def swish(dur=0.9, seed=0):
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    return lp_fast(hp_fast(noise(dur, seed), 500), 4000) * (np.sin(np.pi * t) ** 0.8) * 0.4


def ding():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1976 * t)) * np.exp(-t / 0.25) * 0.35


def hum(dur, f=120, seed=0):
    """機械（ファン）のうなり。"""
    t = np.arange(int(dur * SR)) / SR
    x = sum(np.sin(2 * np.pi * f * k * t) / k for k in (1, 2, 3)) * 0.3 + lp_fast(noise(dur, seed), 800) * 0.3
    return x * np.minimum(1, t / 0.3) * np.minimum(1, (dur - t) / 0.3)


def ticks(dur, rate=12, seed=0):
    """ガイガーカウンターのカリカリ（rate＝1秒あたりの数）。"""
    n = int(dur * SR)
    x = np.zeros(n)
    rng = np.random.default_rng(seed)
    for k in rng.uniform(0, dur, max(1, int(dur * rate))):
        i = int(k * SR)
        m = min(n - i, 200)
        x[i:i + m] += rng.uniform(0.6, 1.0) * np.exp(-np.arange(m) / 15.0) * np.sign(rng.uniform(-1, 1))
    return x * 0.6


def roar(dur, seed=0):
    t = np.arange(int(dur * SR)) / SR
    return lp_fast(noise(dur, seed), 400) * (0.6 + 0.4 * np.sin(t * 3)) * 0.7


def rumble(dur, seed=0):
    t = np.arange(int(dur * SR)) / SR
    return lp_fast(noise(dur, seed), 120) * np.sin(np.pi * t / dur) * 1.2


def cheer(dur, seed=0):
    t = np.arange(int(dur * SR)) / SR
    x = lp_fast(hp_fast(noise(dur, seed), 400), 3000)
    return x * np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.8) * 0.5


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
    """先読みのピーク制限（山だけ下げて、全体を大きくできるように）。"""
    n = len(x)
    L = max(1, int(look * SR))
    need = np.minimum(1.0, ceil / np.maximum(np.abs(x), 1e-9))
    pad = np.concatenate([need, np.ones(L)])
    win = np.lib.stride_tricks.sliding_window_view(pad, L + 1)[:n].min(1)
    a = math.exp(-1 / (rel * SR))
    r = 1 - win
    out = np.empty(n)
    acc = 0.0
    for i, v in enumerate(r):
        acc = v if v > acc else acc * a
        out[i] = acc
    return x * (1 - out)


def lufs(x):
    p = os.path.join(os.environ.get("TMPDIR", "/tmp"), f"_howto_lufs_{os.getpid()}.wav")
    with wave.open(p, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    r = subprocess.run(["ffmpeg", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    os.remove(p)
    return float([l for l in r.splitlines() if l.strip().startswith("I:")][-1].split()[1])


def loudness_to(x, target=-13.0):
    """参考元（約 -12〜-13 LUFS）に合わせる：大きさを上げて、山は先読みで抑える。"""
    for _ in range(8):
        I = lufs(x)
        if abs(I - target) < 0.25:
            break
        x = limiter(x * 10 ** ((target - I) / 20 * 1.3))
    return x


def main(cfg, folder):
    Composer(cfg, folder).run(sys.argv[1], sys.argv[2])
