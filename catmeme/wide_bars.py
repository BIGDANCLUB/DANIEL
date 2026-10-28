"""長尺（横 1920x1080）用の、ショートのような棒グラフの動く背景を作る（10/28 ユーザー指定：ショートのようなグラフでの説明を多く）。

作った mp4 をカットの bg にして、その上に猫と字幕をのせる（render.py の動く背景）。
- 見た目はショートの棒グラフ（bars_short.py の bright）と同じ：白〜水色のすりガラスのパネル、グラデーションの棒、白い字
- 重り（項目）が上から落ちてくる → 着地で白い光と衝撃波（うすい黄色＋黒ふちの輪が2重）と放射線、パネルが少し揺れる
- 棒の上には合計の金額（数字がカウントアップ）。棒の下には列の名前の札
- 画面の上（y<230）は字幕、左右のはし（x<300, x>1620）は猫が入るので空けておく
"""
import math
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import parts as P
import render as R

W, H = 1920, 1080
FPS = R.FPS
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "wide_bars")
PX0, PY0, PX1, PY1 = 300, 236, 1620, 1000   # パネル
BASE_Y = 900   # 棒の下の端
TOP_Y = 440    # いちばん高い棒の上の端（上に見出しと合計の数字が入る）

COL = {
    "red": (235, 80, 90), "blue": (60, 130, 235), "purple": (150, 95, 225), "orange": (250, 150, 50),
    "coral": (250, 110, 120), "teal": (30, 175, 170), "green": (60, 190, 120), "pink": (240, 110, 180),
    "navy": (70, 90, 200), "gold": (235, 175, 30), "gray": (140, 150, 165),
}


def font(size):
    return P.font("black", size)


def text_img(t, size, fill=(255, 255, 255), stroke=6, stroke_col=(20, 20, 30)):
    f = font(size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lines = t.split("\n")
    ws = [d0.textlength(ln, font=f) for ln in lines]
    lh = int(size * 1.15)
    im = Image.new("RGBA", (int(max(ws)) + stroke * 2 + 8, lh * len(lines) + stroke * 2 + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (ln, w) in enumerate(zip(lines, ws)):
        d.text(((im.width - w) / 2, stroke + 2 + i * lh), ln, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_col)
    return im.crop(im.getbbox())


def fit_text(t, max_w, max_h, size, **kw):
    while size > 20:
        im = text_img(t, size, **kw)
        if im.width <= max_w and im.height <= max_h:
            return im
        size -= 4
    return text_img(t, size, **kw)


def grad_block(w, h, col):
    """上が明るく下がこい、うすい斜めじまの角丸の棒。"""
    w, h = max(int(w), 2), max(int(h), 2)
    top = np.array([min(255, c + 70) for c in col], np.float32)
    bot = np.array([max(0, c - 25) for c in col], np.float32)
    k = np.linspace(0, 1, h)[:, None, None]
    arr = (top * (1 - k) + bot * k) * np.ones((h, w, 1), np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    arr += ((xx + yy) // 18 % 2 == 0)[..., None] * 10
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=min(18, w // 4, h // 2), fill=255)
    im.putalpha(mask)
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=min(18, w // 4, h // 2), outline=(255, 255, 255, 230), width=3)
    return im


def ease_in(x):
    return x * x


def ease_out(x):
    return 1 - (1 - x) ** 3


class Chart:
    """cols=[(名前, 色)]。steps=[(秒, 列, 項目, 金額, 色)]（秒<0 は最初から積んである）。vmax=いちばん上の金額。"""

    def __init__(self, cols, steps, vmax, bg="bg48_clean_street", unit="万", head="", hold=12.0, total_fmt="年{v}万",
                 result_at=None, highlight=None):
        self.cols, self.steps, self.vmax, self.unit = cols, sorted(steps, key=lambda s: s[0]), vmax, unit
        self.total_fmt, self.result_at, self.highlight = total_fmt, result_at, highlight
        self.dur = max([0] + [s[0] for s in steps]) + 1.4 + hold
        n = len(cols)
        span = PX1 - PX0 - 120
        self.cw = min(380, span / n * 0.66)
        self.cx = [PX0 + 60 + span * (i + 0.5) / n for i in range(n)]
        self.static = self._static(bg, head)
        self.blocks = {}

    def _static(self, bg, head):
        b = Image.open(_bg(bg)).convert("RGB")
        k = max(W / b.width, H / b.height)
        b = b.resize((int(b.width * k + 1), int(b.height * k + 1))).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(5))
        b = Image.blend(b, Image.new("RGB", (W, H), (255, 255, 255)), 0.25).convert("RGBA")
        pn = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(pn)
        d.rounded_rectangle((PX0, PY0, PX1, PY1), radius=36, fill=(235, 248, 255, 205), outline=(120, 215, 245, 255), width=6)
        for v in range(1, 5):   # うすい目盛り
            y = BASE_Y - (BASE_Y - TOP_Y) * v / 4
            d.line((PX0 + 40, y, PX1 - 40, y), fill=(150, 200, 230, 120), width=2)
        d.line((PX0 + 30, BASE_Y, PX1 - 30, BASE_Y), fill=(60, 90, 120, 255), width=5)
        b.alpha_composite(pn)
        for (name, col), cx in zip(self.cols, self.cx):   # 列の名前の札
            c = COL.get(col, col)
            t = fit_text(name, int(self.cw + 120), 90, 72, stroke=6, stroke_col=tuple(max(0, x - 90) for x in c))
            card = Image.new("RGBA", (t.width + 50, t.height + 26), (0, 0, 0, 0))
            ImageDraw.Draw(card).rounded_rectangle((0, 0, card.width - 1, card.height - 1), radius=18, fill=c + (255,),
                                                   outline=(255, 255, 255, 255), width=4)
            card.alpha_composite(t, (25, 13))
            b.alpha_composite(card, (int(cx - card.width / 2), BASE_Y + 16))
        if head:
            t = fit_text(head, PX1 - PX0 - 80, 76, 62, fill=(30, 60, 110), stroke=6, stroke_col=(255, 255, 255))
            b.alpha_composite(t, (int((PX0 + PX1 - t.width) / 2), PY0 + 18))
        return b

    def still_from(self):
        return max([0] + [s[0] for s in self.steps] + [(self.result_at or -9) + 1.7]) + 1.4

    def ypx(self, v):
        return (BASE_Y - TOP_Y) * v / self.vmax

    def block(self, i, label, h, col):
        key = (i, label, int(h))
        if key not in self.blocks:
            im = grad_block(self.cw, h, COL.get(col, col))
            if h >= 70:
                t = fit_text(label, int(self.cw - 16), int(h - 8), 62, stroke=6, stroke_col=tuple(max(0, x - 110) for x in COL.get(col, col)))
                im.alpha_composite(t, (int((im.width - t.width) / 2), int((im.height - t.height) / 2)))
            self.blocks[key] = im
        return self.blocks[key]

    def frame(self, t):
        im = self.static.copy()
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        stack = [0.0] * len(self.cols)
        side_y = [10 ** 6] * len(self.cols)   # 細い項目の名前が重ならないように（下から順に積む）
        shake = 0.0
        rings = []
        for t0, i, label, v, col in self.steps:
            h = self.ypx(v)
            y_land = BASE_Y - self.ypx(stack[i]) - h
            if t0 < 0 or t >= t0 + 0.32:
                y = y_land
                if t0 >= 0 and t < t0 + 0.9:
                    rings.append((self.cx[i], BASE_Y - self.ypx(stack[i]), (t - t0 - 0.32) / 0.58))
                    shake = max(shake, 1 - (t - t0 - 0.32) / 0.4)
            elif t >= t0:   # 上から落ちてくる
                y = -h - 20 + (y_land + h + 20) * ease_in((t - t0) / 0.32)
            else:
                continue
            blk = self.block(i, label, h, col)
            layer.alpha_composite(blk, (int(self.cx[i] - self.cw / 2), int(y)))
            if t0 < 0 or t >= t0 + 0.32:
                stack[i] += v
            if label and h < 70 and (t0 < 0 or t >= t0 + 0.32):   # 細い項目は名前を横に
                tl = fit_text(label, 300, 60, 38, fill=COL.get(col, col), stroke=5, stroke_col=(255, 255, 255))
                ly = min(y + h / 2 - tl.height / 2, side_y[i] - tl.height - 2)
                side_y[i] = ly
                layer.alpha_composite(tl, (int(self.cx[i] + self.cw / 2 + 10), int(ly)))
        for i, cx in enumerate(self.cx):   # 合計（カウントアップ）
            if stack[i] <= 0:
                continue
            tot = stack[i]
            last = max([s[0] for s in self.steps if s[1] == i and s[0] >= 0 and s[0] + 0.32 <= t] or [-9])
            if 0 <= t - last - 0.32 < 0.5:
                prev = tot - next(s[3] for s in self.steps if s[1] == i and s[0] == last)
                tot = prev + (tot - prev) * ease_out((t - last - 0.32) / 0.5)
            hl = self.highlight == i
            txt = self.total_fmt.format(v=_num(tot))
            col = (230, 30, 40) if hl or i == 0 else (30, 90, 200)
            tm = text_img(txt, 104 if hl else 88, fill=col, stroke=9, stroke_col=(255, 255, 255))
            ty = BASE_Y - self.ypx(stack[i]) - tm.height - 14
            layer.alpha_composite(tm, (int(cx - tm.width / 2), int(max(PY0 + 8, ty))))
        d = ImageDraw.Draw(layer)
        for x, y, p in rings:   # 衝撃波
            if p < 0:
                continue
            for j, k in enumerate((1.0, 0.65)):
                r = (40 + 260 * ease_out(min(1, p))) * k
                a = int(255 * max(0, 1 - p))
                d.ellipse((x - r * 1.6, y - r * 0.5, x + r * 1.6, y + r * 0.5), outline=(20, 20, 20, a), width=10 - j * 3)
                d.ellipse((x - r * 1.6, y - r * 0.5, x + r * 1.6, y + r * 0.5), outline=(255, 245, 160, a), width=6 - j * 2)
            if p < 0.35:
                for a_ in range(0, 360, 20):
                    ca, sa = math.cos(math.radians(a_)), math.sin(math.radians(a_))
                    r0, r1 = 60 + 200 * p, 140 + 360 * p
                    d.line((x + ca * r0, y + sa * r0 * 0.6, x + ca * r1, y + sa * r1 * 0.6), fill=(255, 250, 200, int(230 * (1 - p / 0.35))), width=6)
            if p < 0.12:
                fl = Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - p / 0.12))))
                layer.alpha_composite(fl)
        if shake > 0:
            dx = int(14 * shake * math.sin(t * 90))
            dy = int(9 * shake * math.cos(t * 70))
            moved = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            moved.alpha_composite(layer, (max(0, dx), max(0, dy)), (max(0, -dx), max(0, -dy)))
            layer = moved
        im.alpha_composite(layer)
        if self.result_at is not None and t >= self.result_at:
            im = self._result(im, t - self.result_at)
        return im.convert("RGB")

    def _result(self, im, u):
        """結果発表：少し暗く → 黒い帯に金色の「結果発表」→ 帯が消えて結果が残る。"""
        if u > 1.6:
            return im
        a = min(1, u / 0.15) * (1 if u < 1.3 else max(0, 1 - (u - 1.3) / 0.3))
        dark = Image.new("RGBA", (W, H), (0, 0, 0, int(140 * a)))
        im.alpha_composite(dark)
        band = Image.new("RGBA", (W, 220), (10, 10, 10, int(235 * a)))
        t = text_img("結果発表", int(150 * (1.25 - 0.25 * min(1, u / 0.2))), fill=(255, 215, 60), stroke=10, stroke_col=(90, 50, 0))
        band.alpha_composite(t, (int((W - t.width) / 2), int((220 - t.height) / 2)))
        if a < 1:
            band.putalpha(band.getchannel("A").point(lambda v: int(v * a)))
        im.alpha_composite(band, (0, 430))
        return im


def _num(v):
    return f"{v:.1f}".rstrip("0").rstrip(".") if v < 10 and abs(v - round(v)) > 0.05 else f"{round(v):,}"


def _bg(name):
    for d in os.listdir(os.path.join(HERE, "backgrounds")):
        p = os.path.join(HERE, "backgrounds", d, name + ".png")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(name)


def make(name, chart, force=False):
    """out/wide_bars/<name>.mp4 を作る（あれば作り直さない）。返り値はパス。"""
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".mp4")
    if os.path.exists(path) and not force:
        return path
    n = int(chart.dur * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", path],
                         stdin=subprocess.PIPE)
    last = None
    for k in range(n):
        t = k / FPS
        if last is not None and t > chart.still_from():   # 動きが止まったあとは同じ絵
            p.stdin.write(last)
            continue
        last = np.asarray(chart.frame(t)).tobytes()
        p.stdin.write(last)
    p.stdin.close()
    p.wait()
    return path

