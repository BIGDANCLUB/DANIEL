"""「棒グラフで比べる」型の1分ショート（縦 1080x1920）。10/23 ユーザー提供の参考動画（1番損する夫婦年収）の作りをまねる。
台本・帯の文字は参考と変える。長さは厳密に 59.9 秒。BGM なし（猫の音と効果音だけ）。

参考の作り（576x1024 → 1080x1920 に 1.875 倍）
- 背景（オフィスの絵）の上に、水色の大きなパネル。上に赤い太字の2行（白い縁）
- 黄色い棒が3本（=それぞれの年収の全体）。下に白い札（「年収／夫○万／妻○万」・色つきの太字）
- 「○○ 参戦!!」の割り込み：黒いもやの帯＋ミーム猫＋赤い文字＋大きな白緑の文字。そのあと棒の上から差し引く分が
  赤・灰色で積もっていく（「△126万」）。最後に残った黄色に「手取り○万」
- 棒の手前（下のほう）に猫が3匹。セリフは白い太字＋黒縁を棒の上に（ときどき緑の枠の白い吹き出し）
- 最後に大きな文字（参考は GAME SET）
"""
import math
import os
import subprocess
import zlib

import cv2
import numpy as np
from PIL import Image, ImageDraw

import income_short as I
import render as R

HERE = I.HERE
W, H = 1080, 1920
TOTAL = 59.9
WHITE, BLACK, RED, YELLOW = (255, 255, 255), (0, 0, 0), (225, 20, 20), (255, 245, 0)
BASE = (255, 60, 170)   # 棒のもとの色（10/27 ユーザー指定：他チャンネルと被らないよう黄色をやめて目立つピンクに）
TEAL = (130, 235, 215)
PANEL = (30, 60, 1050, 1620)
COLX = (205, 540, 875)
COLW = 250
BAR_TOP, BAR_BOT = 300, 1250
# 10/27 ユーザー指定：黄色をやめて、きれいで見やすい配色に（もとの色はエメラルドのグラデーション＋うすい斜めじま）
SEG_COL_OLD = {"red": ((230, 20, 20), WHITE), "gray": ((205, 205, 205), BLACK), "dark": ((140, 140, 140), BLACK),
           "green": ((40, 210, 60), BLACK), "purple": ((170, 40, 200), WHITE), "orange": ((255, 140, 0), BLACK)}


SEG_COL = {"red": ((236, 84, 84), WHITE), "green": ((66, 145, 235), WHITE), "purple": ((150, 90, 210), WHITE),
           "orange": ((247, 140, 60), WHITE), "dark": ((96, 112, 132), WHITE), "gray": ((150, 162, 178), WHITE)}
BASE_TOP, BASE_BOT = (40, 205, 150), (10, 140, 120)   # 残りのお金（エメラルド）
NAVY_PANEL = (22, 30, 58)


def grad_fill(h, w, top, bot, stripes=False):
    """上から下へのグラデーション（BGR 0〜1）。stripes=True でうすい斜めじま。"""
    h, w = max(1, int(h)), max(1, int(w))
    u = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    a = np.array(top[::-1], np.float32) / 255
    b = np.array(bot[::-1], np.float32) / 255
    g = np.repeat(a * (1 - u) + b * u, w, axis=1)
    if stripes:
        yy, xx = np.mgrid[0:h, 0:w]
        m = (((xx + yy) // 18) % 2 == 0).astype(np.float32)[..., None]
        g = g * (1 - 0.08 * m) + 0.08 * m
    # 左に光（立体感）
    sh = np.linspace(1.12, 0.92, w, dtype=np.float32)[None, :, None]
    return np.clip(g * sh, 0, 1)


def label_card(lines, col):
    """下の札：白地に色つきの太字（3行）。"""
    im = Image.new("RGBA", (COLW + 40, 230), (255, 255, 255, 255))
    y = 10
    for i, ln in enumerate(lines):
        t = I.text(ln, 64, col if i else (230, 60, 0), stroke=3, stroke_col=WHITE, max_w=COLW + 20)
        im.alpha_composite(t, ((im.width - t.width) // 2, y))
        y += t.height + 6
    return im


def banner(name, word, big, cat):
    """割り込みの帯：黒いもや＋猫＋赤い文字＋大きな白緑の文字。"""
    im = Image.new("RGBA", (W, 760), (0, 0, 0, 0))
    m = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(m)
    rng = np.random.default_rng(5)
    for _ in range(70):   # もやもやした黒い帯
        x = rng.uniform(-100, W + 100)
        y = rng.uniform(150, 610)
        r = rng.uniform(80, 200)
        d.ellipse((x - r * 1.6, y - r * 0.6, x + r * 1.6, y + r * 0.6), fill=255)
    m = m.resize((W // 4, 190)).resize(im.size)
    from PIL import ImageFilter
    m = m.filter(ImageFilter.GaussianBlur(6))
    black = Image.new("RGBA", im.size, (5, 10, 30, 255))
    black.putalpha(m)
    glow = Image.new("RGBA", im.size, (60, 110, 255, 0))
    glow.putalpha(m.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.55)))
    im.alpha_composite(glow)
    im.alpha_composite(black)
    t1 = I.text(word, 150, RED, stroke=6, stroke_col=BLACK, max_w=560)
    t2 = I.text(big, 250, (235, 255, 235), stroke=12, stroke_col=(30, 120, 60), max_w=620)
    im.alpha_composite(t1, (750 - t1.width // 2, 300 - t1.height // 2))   # 猫（左）にかけない
    im.alpha_composite(t2, (740 - t2.width // 2, 500 - t2.height // 2))
    return im


def weight_img(name):
    """上から落ちてくる「重り」（黒い鉄のかたまり・上に持ち手の輪）に項目名。10/24 ユーザー指定：のしかかる演出。"""
    w, h = 820, 430
    im = Image.new("RGBA", (w, h + 130), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((w / 2 - 110, 0, w / 2 + 110, 190), outline=(25, 25, 30), width=44)          # 持ち手
    d.polygon([(110, 130), (w - 110, 130), (w - 10, h + 120), (10, h + 120)], fill=(30, 30, 36))   # 台形の重り
    d.polygon([(130, 150), (w - 130, 150), (w - 100, 200), (100, 200)], fill=(80, 80, 92))        # てかり
    d.line([(10, h + 120), (w - 10, h + 120)], fill=(0, 0, 0), width=10)
    t = I.text(name, 150, WHITE, stroke=8, stroke_col=(150, 0, 0), max_w=w - 120)
    im.alpha_composite(t, ((w - t.width) // 2, 130 + (h - 10 - t.height) // 2))
    return im


def thud_text(t):
    im = I.text(t, 210, (255, 40, 40), stroke=12, stroke_col=WHITE)
    return im.rotate(-8, expand=True, resample=Image.BICUBIC)


def crown_img(w=300):
    """金色の王冠。"""
    h = int(w * 0.72)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(10, h - 50), (10, 60), (w * 0.27, h * 0.45), (w / 2, 10), (w * 0.73, h * 0.45), (w - 10, 60), (w - 10, h - 50)]
    d.polygon(pts, fill=(255, 205, 30), outline=(150, 90, 0))
    d.line(pts + [pts[0]], fill=(150, 90, 0), width=10)
    d.rectangle((10, h - 60, w - 10, h - 10), fill=(240, 175, 20), outline=(150, 90, 0), width=8)
    for x, y in ((10, 60), (w / 2, 10), (w - 10, 60)):
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(230, 30, 60), outline=(120, 0, 20), width=5)
    return im


def stamp_img(text):
    """赤いはんこ（丸の中に文字）。"""
    r = 200
    im = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((8, 8, r * 2 - 8, r * 2 - 8), outline=(220, 20, 20), width=22)
    d.ellipse((40, 40, r * 2 - 40, r * 2 - 40), outline=(220, 20, 20), width=8)
    t = I.text(text, 170, (220, 20, 20), max_w=r * 2 - 120)
    im.alpha_composite(t, (r - t.width // 2, r - t.height // 2))
    return im.rotate(-14, expand=True, resample=Image.BICUBIC)


def finish_text(t):
    im = I.text(t, 260, (220, 255, 120), stroke=14, stroke_col=(20, 90, 30))
    return im.rotate(6, expand=True, resample=Image.BICUBIC)


class Renderer:
    def __init__(self, c, static):
        self.c, self.st = c, static
        self.clips = [R.Clip(a) if a else None for a in c["cats3"]]
        self.say = I.text(c["say"], 78, WHITE, stroke=8, max_w=W - 120) if c.get("say") else None
        self.box = c.get("box", False)
        self.ban = weight_img(c["banner"][1]) if c.get("banner") else None
        self.thud = thud_text(c["banner"][2]) if c.get("banner") else None
        self.ban_cat = R.Clip(c["banner"][3]) if c.get("banner") else None
        self.fin = c.get("finish")   # 1位の列（0〜2）。10/24：「勝負あり!!」の文字はやめて、王冠とはんこの演出
        if self.fin is not None:
            self.crown, self.stamp = crown_img(), stamp_img(c.get("finish_word", "1位"))
        self.bbox = {}
        if c.get("callout"):
            lines = c["callout"]
            rows = [I.text(lines[0], 110, WHITE, stroke=10, stroke_col=(20, 30, 80), max_w=W - 160),
                    I.text(lines[1], 150, (255, 225, 60), stroke=14, stroke_col=(170, 20, 40), max_w=W - 140)]
            bw = max(r.width for r in rows) + 90
            bh = sum(r.height for r in rows) + 90
            box = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
            ImageDraw.Draw(box).rounded_rectangle((0, 0, bw - 1, bh - 1), 40, fill=(230, 40, 70, 240), outline=WHITE, width=10)
            y = 35
            for r in rows:
                box.alpha_composite(r, ((bw - r.width) // 2, y))
                y += r.height + 20
            self.call_im = box.rotate(-3, expand=True, resample=Image.BICUBIC)
        if c.get("shout"):
            self.shout_im = I.text("＼" + c["shout"][0] + "／", 76, YELLOW, stroke=9, stroke_col=BLACK, max_w=520).rotate(
                8, expand=True, resample=Image.BICUBIC)
        if c.get("result"):
            tx = I.text(c["result"], 180, (255, 220, 110), stroke=10, stroke_col=(80, 50, 0), max_w=W - 200)
            rb = Image.new("RGBA", (W - 60, tx.height + 90), (0, 0, 0, 0))
            d_ = ImageDraw.Draw(rb)
            d_.rectangle((0, 0, rb.width - 1, rb.height - 1), fill=(12, 14, 30, 235))
            for k_, y_ in enumerate((10, rb.height - 22)):
                d_.rectangle((0, y_, rb.width - 1, y_ + 12), fill=(220, 180, 80, 255))
            rb.alpha_composite(tx, ((rb.width - tx.width) // 2, 45))
            self.res = rb
        if c.get("minus"):
            good = c.get("good")   # True なら「プラス（貯金できる）」の色（10/27）
            sc_ = (0, 110, 40) if good else (180, 0, 0)
            big = I.text(c["minus"][0], 210, YELLOW, stroke=16, stroke_col=sc_, max_w=W - 150)
            band_ = Image.new("RGBA", (W + 200, big.height + 80), ((0, 70, 30, 235) if good else (0, 0, 0, 235)))
            band_.alpha_composite(big, ((band_.width - big.width) // 2, 40))
            self.minus = (band_.rotate(-6, expand=True, resample=Image.BICUBIC),
                          I.text(c["minus"][1], 96, WHITE, stroke=10, stroke_col=sc_, max_w=W - 170))
            self.bill = bill_img()

    def _cat(self, clip, name, t, h, w):
        fr, a = clip.frame(t + 0.25)
        y0, y1, x0, x1 = I.clip_bbox(name)
        fr, a = fr[y0:y1, x0:x1], a[y0:y1, x0:x1]
        s = min(h / fr.shape[0], w / fr.shape[1])
        ww, hh = max(1, int(fr.shape[1] * s)), max(1, int(fr.shape[0] * s))
        img = cv2.resize(fr, (ww, hh), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
        al = cv2.resize(a.astype(np.float32), (ww, hh), interpolation=cv2.INTER_AREA)
        pad = 12
        img = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
        al = cv2.copyMakeBorder(al, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
        edge = cv2.dilate((al > 0.4).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))).astype(np.float32)
        img = img * al[..., None] + (1 - al[..., None])
        return img, np.maximum(al, edge)

    def frame(self, t):
        c, st = self.c, self.st
        out = st["base"].copy()
        # 棒：黄色の全体 → 上から差し引く分を積む
        for j, cx in enumerate(COLX):
            x0, x1 = int(cx - COLW / 2), int(cx + COLW / 2)
            total = st["incomes"][j]
            scale = (BAR_BOT - BAR_TOP) / st["max_income"]
            top = BAR_BOT - total * scale
            sh = out[int(top) + 10:BAR_BOT + 10, x0 + 10:x1 + 10]   # 影
            sh *= 0.55
            out[int(top):BAR_BOT, x0:x1] = grad_fill(BAR_BOT - int(top), x1 - x0, BASE_TOP, BASE_BOT, stripes=True)
            y = top
            for k, (name, kind) in enumerate(st["items"]):
                if k >= c["shown"]:
                    break
                v = st["values"][name][j]
                if not v:   # 0 の項目は描かない
                    continue
                grow = 1.0 if (k < c["shown"] - 1 or not c.get("grow")) else min(1.0, t / 0.5)
                hpx = v * scale * grow   # 2列のときは金額どおりの長さ（10/26）
                col, tc = SEG_COL[kind]
                if int(y + hpx) > int(y):
                    lt = tuple(min(255, int(v_ * 1.15)) for v_ in col)
                    dk = tuple(int(v_ * 0.82) for v_ in col)
                    out[int(y):int(y + hpx), x0:x1] = grad_fill(int(y + hpx) - int(y), x1 - x0, lt, dk)
                cv2.line(out, (x0, int(y + hpx)), (x1, int(y + hpx)), (1, 1, 1), 3, cv2.LINE_AA)
                if grow > 0.6:
                    lab = st["seglab"][(name, j)]
                    if lab.height > hpx - 6:   # 細い段は札を小さくして段の中におさめる（10/27）
                        k_ = max(hpx - 6, 20) / lab.height
                        lab = lab.resize((max(1, int(lab.width * k_)), max(1, int(lab.height * k_))), Image.LANCZOS)
                    I.put(out, lab, (x0 + x1) / 2 if CATX else x0 + lab.width / 2 + 14, y + min(hpx, 120) / 2 + 4)
                y += hpx
            cv2.rectangle(out, (x0, int(top)), (x1, BAR_BOT), (1, 1, 1), 3, cv2.LINE_AA)   # 白い細いふち
            if c.get("take"):
                I.put(out, st["takelab"][j], cx, y + 90)
        for j, cx in enumerate(COLX):   # 下の札
            lab = st["cards"][j]
            I.put(out, lab, cx, 1420)
        # 猫（棒の手前・下のほう）
        for j, (clip, name) in enumerate(zip(self.clips, c["cats3"])):
            if clip is None:
                continue
            big = c.get("big") == j
            if CATX:   # 棒の外側（左の列は左、右の列は右）
                allv = isinstance(c.get("voice"), tuple) and len(c["voice"]) >= 2   # 冒頭（全員）は大きく
                if c.get("take"):   # 結果のあとは今までどおり（棒にかかりすぎないように）
                    img, al = self._cat(clip, name, t, 460 if big else 380, 250)
                    cx_ = CATX[j]
                else:   # それ以外は大きく、棒に少しかかってよい（10/27 ユーザー指定）
                    img, al = self._cat(clip, name, t, 640 if (allv or big) else 560, 400 if (allv or big) else 360)
                    cx_ = CATX[j] + (60 if j == 0 else -60)
                hh, ww = al.shape
                x0 = int(min(max(cx_ - ww / 2, 10), W - ww - 10))
                I.over(out, img, al, x0, int(1300 - hh))
                continue
            if isinstance(c.get("big"), int) and isinstance(c.get("voice"), tuple):   # 3匹とも大きく（冒頭のマーモット）
                big = True
            img, al = self._cat(clip, name, t, 520 if big else 460, 350 if big else 340)   # もう少し棒にかかってもよい（10/27）
            hh, ww = al.shape
            x0 = int(min(max(COLX[j] - ww / 2, 10), W - ww - 10))
            I.over(out, img, al, x0, int(1310 - hh))
        # タイトル
        I.put(out, st["title"], W / 2, 175)
        if self.say is not None:
            if self.box:
                bx = Image.new("RGBA", (self.say.width + 60, self.say.height + 44), (255, 255, 255, 255))
                ImageDraw.Draw(bx).rectangle((0, 0, bx.width - 1, bx.height - 1), outline=(40, 210, 40), width=10)
                inner = I.text(c["say"], 70, BLACK, max_w=W - 160)
                bx = Image.new("RGBA", (inner.width + 60, inner.height + 44), (255, 255, 255, 255))
                ImageDraw.Draw(bx).rectangle((0, 0, bx.width - 1, bx.height - 1), outline=(40, 210, 40), width=10)
                bx.alpha_composite(inner, (30, 22))
                I.put(out, bx, W / 2, c.get("say_y", 640))
            else:
                I.put(out, self.say, W / 2, c.get("say_y", 640))
        if c.get("callout"):   # 冒頭のタイトルコール（画面の上半分・10/27 ユーザー指定）
            u = min(1.0, t / 0.2)
            im = self.call_im
            sc = 1.6 - 0.6 * (1 - (1 - u) ** 3)
            im2 = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))))
            I.put(out, im2, W / 2 + 8 * math.sin(t * 40) * max(0.0, 1 - t / 0.5), 560)
        if c.get("shout"):   # 「＼もっと入れろや／」のような掛け声（猫の上・10/27）
            text_, j = c["shout"]
            sh = self.shout_im
            x = (CATX[j] if CATX else COLX[j])
            x = min(max(x, sh.width / 2 + 10), W - sh.width / 2 - 10)
            I.put(out, sh, x + 6 * math.sin(t * 30), 470)   # 字幕より上・猫にかからない高さ（10/27）
        if c.get("result"):   # 結果発表：暗転→上からスポットライト2本が交差→金色の文字が光って出る→紙吹雪（10/27 作り直し）
            u = min(1.0, t / 0.25)
            out = out * (1 - 0.6 * u)
            cone = np.zeros((H, W), np.float32)
            for side in (-1, 1):
                ang = side * (0.35 - 0.25 * math.sin(min(1.0, t / 0.6) * math.pi / 2))
                tx_ = W / 2 + side * 520
                pts = np.array([(tx_ - 40, -50), (tx_ + 40, -50),
                                (W / 2 + 300 + math.tan(ang) * 300, 1000), (W / 2 - 300 + math.tan(ang) * 300, 1000)], np.int32)
                cv2.fillConvexPoly(cone, pts, 0.35 * u)
            cone = cv2.GaussianBlur(cone, (81, 81), 0)
            out = out + cone[..., None] * np.array([0.75, 0.92, 1.0], np.float32)
            if t > 0.3:
                v_ = min(1.0, (t - 0.3) / 0.2)
                sc = 1.25 - 0.25 * v_
                im = self.res.resize((max(1, int(self.res.width * sc)), max(1, int(self.res.height * sc))))
                I.put(out, im, W / 2, 820)
                if t < 0.55:   # 出た瞬間のきらめき
                    out = out + (0.55 - t) * 1.2
            for i in range(40):   # 紙吹雪
                ph = (t * 0.7 + i * 0.137) % 1.0
                x = (i * 97 + 40 * math.sin(t * 3 + i)) % W
                y = -40 + ph * (H + 80)
                col = ((0.3, 0.8, 1.0), (1.0, 0.6, 0.3), (0.5, 1.0, 0.6), (1.0, 1.0, 1.0), (0.9, 0.5, 1.0))[i % 5]
                ww = 8 + 18 * abs(math.sin(t * 8 + i))   # くるくる回って見える
                cv2.rectangle(out, (int(x), int(y)), (int(x + ww), int(y + 28)), col, -1)
        if self.ban is not None:   # 重りが上から落ちてきて、棒にのしかかる（ドスン→画面がゆれる）
            land = 0.38
            u = min(1.0, t / land)
            y_land = 480
            y = -self.ban.height + (y_land + self.ban.height) * u * u          # だんだん速く落ちる
            if t > land:                                                     # 着地のあと少し沈んで戻る
                y = y_land + 26 * math.exp(-(t - land) * 9) * math.sin((t - land) * 30)
            img, al = self._cat(self.ban_cat, self.c["banner"][3], t, 330, 330)   # 重りの上（右の肩）に猫が乗っている
            I.over(out, img, al, int(W / 2 + 230 - al.shape[1] / 2), int(y + 170 - al.shape[0]))
            I.put(out, self.ban, W / 2, y + self.ban.height / 2)
            if t > land:
                # 着地の土ぼこり（白い線）と、効果のひとこと
                dt = t - land
                if dt < 0.6:   # 衝撃波：着地点から広がる輪（2重）＋放射状の線（10/27 ユーザー指定）
                    gy = int(y_land + self.ban.height - 40)
                    for delay, base_r in ((0.0, 1.0), (0.12, 0.8)):
                        u_ = (dt - delay) / 0.45
                        if 0 < u_ < 1:
                            rx, ry = int((400 + 700 * u_) * base_r), int((60 + 170 * u_) * base_r)
                            th_ = max(2, int(26 * (1 - u_)))
                            cv2.ellipse(out, (W // 2, gy), (rx, ry), 0, 0, 360, (0.05, 0.05, 0.1), th_ + 8, cv2.LINE_AA)
                            cv2.ellipse(out, (W // 2, gy), (rx, ry), 0, 0, 360, (0.6, 0.95, 1.0), th_, cv2.LINE_AA)
                    if dt < 0.35:
                        u_ = dt / 0.35
                        for i in range(14):   # 放射状に飛ぶ線
                            a_ = math.pi + math.pi * i / 13
                            r0, r1 = 440 + 300 * u_, 520 + 500 * u_
                            p0 = (int(W / 2 + r0 * math.cos(a_)), int(gy + r0 * 0.45 * math.sin(a_)))
                            p1 = (int(W / 2 + r1 * math.cos(a_)), int(gy + r1 * 0.45 * math.sin(a_)))
                            cv2.line(out, p0, p1, (0.05, 0.05, 0.1), 15, cv2.LINE_AA)
                            cv2.line(out, p0, p1, (0.6, 0.95, 1.0), 7, cv2.LINE_AA)
                    if dt < 0.08:   # 一瞬白く光る
                        out = out * 0.6 + 0.4
                kk = min(1.0, (t - land) / 0.15)
                th = self.thud.resize((max(1, int(self.thud.width * (0.5 + 0.5 * kk))), max(1, int(self.thud.height * (0.5 + 0.5 * kk)))))
                I.put(out, th, W / 2, y_land + self.ban.height + 120)
                if t - land < 0.35:   # 画面がゆれる
                    a_ = 22 * (1 - (t - land) / 0.35)
                    M_ = np.float32([[1, 0, a_ * math.sin(t * 90)], [0, 1, a_ * math.cos(t * 70)]])
                    out = cv2.warpAffine(out, M_, (W, H), borderMode=cv2.BORDER_REPLICATE)
        if c.get("minus"):   # 最後：「マイナス○○円」を画面いっぱいに強く出す（10/26 ユーザー指定：もっと派手に）
            k = min(1.0, t / 0.2)
            out = out * (1 - 0.6 * k)
            # 赤い集中線（回る）と、赤く点滅する画面
            ov = np.zeros((H, W), np.float32)
            cx, cy = W / 2, 820
            for i in range(48):
                a = 2 * math.pi * i / 48 + t * 0.6
                d = 0.035
                pts = np.array([(cx, cy), (cx + 2400 * math.cos(a - d), cy + 2400 * math.sin(a - d)),
                                (cx + 2400 * math.cos(a + d), cy + 2400 * math.sin(a + d))], np.int32)
                cv2.fillConvexPoly(ov, pts, 1.0)
            flash = 0.45 + 0.35 * (int(t * 8) % 2)
            rc = np.array([0.1, 0.8, 1.0] if c.get("good") else [0.05, 0.05, 0.85], np.float32)   # 金色／赤
            out = out * (1 - ov[..., None] * flash * k) + ov[..., None] * flash * k * rc
            # お札が上から降って、下へ落ちていく（お金が出ていく）
            for i in range(14):
                x = (i * 157 + 60) % W
                y = -200 + ((t * 900 + i * 230) % (H + 400))
                bill = self.bill.rotate((i * 37 + t * 200) % 360, expand=True)
                I.put(out, bill, x, y)
            # 大きな文字：ドン！と縮みながら出て、着地で画面がゆれる
            big, sub = self.minus
            u = min(1.0, t / 0.18)
            sc = 3.0 - 2.0 * u
            im = big.resize((max(1, int(big.width * sc)), max(1, int(big.height * sc))))
            pul = 1.0 + 0.04 * math.sin(t * 18) if t > 0.3 else 1.0
            if pul != 1.0:
                im = im.resize((int(im.width * pul), int(im.height * pul)))
            I.put(out, im, W / 2, cy)
            if t > 0.55:
                v = min(1.0, (t - 0.55) / 0.15)
                sb = sub.resize((max(1, int(sub.width * (1.6 - 0.6 * v))), max(1, int(sub.height * (1.6 - 0.6 * v)))))
                I.put(out, sb, W / 2, 1110)
            if 0.18 < t < 0.75:   # 着地のゆれ
                a_ = 34 * (1 - (t - 0.18) / 0.57)
                M_ = np.float32([[1, 0, a_ * math.sin(t * 95)], [0, 1, a_ * math.cos(t * 77)]])
                out = cv2.warpAffine(out, M_, (W, H), borderMode=cv2.BORDER_REPLICATE)
            if t < 0.12:   # 出た瞬間に白く光る
                out = out * 0.4 + 0.6
        if self.fin is not None:   # 1位以外の列を暗くして、1位にスポットライト＋王冠が落ちてきて、はんこがポン
            j = self.fin
            dim = np.ones((H, W, 1), np.float32) * 0.45
            x0, x1 = int(COLX[j] - COLW / 2 - 40), int(COLX[j] + COLW / 2 + 40)
            dim[:, x0:x1] = 1.0
            dim[:310] = 1.0
            k = min(1.0, t / 0.3)
            out = out * (1 - (1 - dim) * k)
            cone = np.zeros((H, W), np.float32)   # スポットライト（上から広がる光）
            pts = np.array([(COLX[j] - 60, 300), (COLX[j] + 60, 300), (x1 + 60, 1500), (x0 - 60, 1500)], np.int32)
            cv2.fillConvexPoly(cone, pts, 0.22 * k)
            cone = cv2.GaussianBlur(cone, (61, 61), 0)
            out = out + cone[..., None] * np.array([0.6, 0.95, 1.0], np.float32)
            u = min(1.0, max(0.0, (t - 0.25) / 0.35))
            cy = -200 + (390 + 200) * (1 - (1 - u) ** 3)
            I.put(out, self.crown, COLX[j], cy)
            if t > 0.7:
                s_ = min(1.0, (t - 0.7) / 0.12)
                sc = 1.8 - 0.8 * s_
                st_ = self.stamp.resize((int(self.stamp.width * sc), int(self.stamp.height * sc)))
                I.put(out, st_, COLX[j], 880)
        return out

    def close(self):
        for cl in self.clips + [self.ban_cat]:
            if cl is not None and getattr(cl, "cap", None) is not None:
                cl.cap.release()


CATX = None   # 猫の位置（None なら棒の下のほう）。2列のときは棒の外側に置いて、残りのお金を隠さない（10/26）


def bill_img(w=240):
    """お札（10/27 作り直し：地紋のロゼット・ホログラムの帯・すかし・記番号で本物らしく。実在の紙幣の図柄はまねない）。"""
    h = int(w * 0.5)
    S_ = 3
    W_, H_ = w * S_, h * S_
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for y in range(H_):   # 紙の色（あわい茶〜クリーム）
        u = y / H_
        d.line((0, y, W_, y), fill=(int(222 - 14 * u), int(208 - 16 * u), int(170 - 18 * u), 255))
    for cx, cy, rr in ((W_ * 0.3, H_ * 0.5, H_ * 0.42), (W_ * 0.62, H_ * 0.55, H_ * 0.3)):   # ロゼット（細い線のうず模様）
        for k in range(36):
            a0 = 2 * math.pi * k / 36
            pts = []
            for q in range(0, 361, 6):
                th = math.radians(q)
                r_ = rr * (0.55 + 0.45 * math.cos(5 * th + a0))
                pts.append((cx + r_ * math.cos(th + a0), cy + r_ * math.sin(th + a0)))
            d.line(pts, fill=(170, 140, 95, 70), width=2)
    for i in range(0, W_, 7):   # 細い地紋
        d.line([(i + 10 * math.sin(yy / 15), yy) for yy in range(0, H_, 5)], fill=(185, 155, 110, 55), width=1)
    hx = int(W_ * 0.47)   # ホログラムの帯（虹色）
    for x in range(hx, hx + int(W_ * 0.07)):
        u = (x - hx) / (W_ * 0.07)
        col = (int(200 + 55 * math.sin(u * 6)), int(200 + 55 * math.sin(u * 6 + 2)), int(200 + 55 * math.sin(u * 6 + 4)), 200)
        d.line((x, 0, x, H_), fill=col)
    cx, cy, r = W_ * 0.8, H_ * 0.5, H_ * 0.3   # すかし
    d.ellipse((cx - r * 0.75, cy - r, cx + r * 0.75, cy + r), fill=(238, 228, 200, 255), outline=(150, 115, 70, 255), width=3)
    d.rectangle((14, 14, W_ - 15, H_ - 15), outline=(105, 75, 40, 255), width=7)
    d.rectangle((30, 30, W_ - 31, H_ - 31), outline=(150, 115, 70, 255), width=2)
    f = I.font(int(H_ * 0.24))
    d.text((W_ * 0.06, H_ * 0.08), "10000", font=f, fill=(95, 62, 28, 255))
    d.text((W_ * 0.06, H_ * 0.62), "壱万円", font=f, fill=(95, 62, 28, 255))
    f3 = I.font(int(H_ * 0.1))
    d.text((W_ * 0.55, H_ * 0.08), "ZZ 000000 Z", font=f3, fill=(140, 60, 40, 255))   # ありえない記番号（作りもの）
    im = im.resize((w, h), Image.LANCZOS)
    sh = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((7, 7, w + 7, h + 7), fill=(0, 0, 0, 90))
    sh.alpha_composite(im, (0, 0))
    return sh


def set_cols(n):
    """列の数（2 か 3）に合わせて、棒の位置と太さを決める。"""
    global COLX, COLW, CATX, BAR_BOT
    if n == 2:
        COLX, COLW, CATX, BAR_BOT = (395, 685), 210, (150, 930), 1250
    else:   # 3列：棒を短くして、猫は棒の下に置く（残りのお金を隠さない・10/27）
        COLX, COLW, CATX, BAR_BOT = (205, 540, 875), 250, None, 990


BRIGHT = dict(   # 明るい版（10/27 ユーザー指定：もっと明るい色で）
    seg={"red": ((255, 104, 104), WHITE), "green": ((70, 172, 255), WHITE), "purple": ((178, 120, 255), WHITE),
         "orange": ((255, 158, 64), WHITE), "dark": ((118, 140, 170), WHITE), "gray": ((160, 175, 195), WHITE)},
    base=((110, 240, 190), (40, 205, 175)), panel=((250, 252, 255), (225, 238, 252)), frame=(0.95, 0.65, 0.35))   # frame は BGR
DARK = dict(seg=dict(SEG_COL), base=(BASE_TOP, BASE_BOT), panel=((30, 40, 78), (14, 18, 38)), frame=(0.85, 0.75, 0.45))


def make_static(spec):
    global SEG_COL, BASE_TOP, BASE_BOT
    sty = BRIGHT if spec.get("style") == "bright" else DARK
    SEG_COL = sty["seg"]
    BASE_TOP, BASE_BOT = sty["base"]
    set_cols(len(spec["incomes"]))
    base = I.cover(spec["bg"])
    x0, y0, x1, y1 = PANEL
    pn = grad_fill(y1 - y0, x1 - x0, *sty["panel"])   # 紺（明るい版は白〜水色）のすりガラス
    base[y0:y1, x0:x1] = base[y0:y1, x0:x1] * 0.18 + pn * 0.82
    cv2.rectangle(base, (x0, y0), (x1 - 1, y1 - 1), sty["frame"], 4, cv2.LINE_AA)
    title = Image.new("RGBA", (W, 230), (0, 0, 0, 0))
    if spec.get("style") == "bright":
        t1 = I.text(spec["title"][0], 92, (230, 40, 70), stroke=6, stroke_col=WHITE)
        t2 = I.text(spec["title"][1], 92, (25, 70, 170), stroke=6, stroke_col=WHITE)
    else:
        t1 = I.text(spec["title"][0], 92, WHITE, stroke=6, stroke_col=(200, 40, 60))
        t2 = I.text(spec["title"][1], 92, (255, 215, 100), stroke=6, stroke_col=(60, 40, 10))
    title.alpha_composite(t1, ((W - t1.width) // 2, 8))
    title.alpha_composite(t2, ((W - t2.width) // 2, 118))
    st = dict(base=base, title=title, incomes=spec["incomes"], max_income=max(spec["incomes"]), items=spec["items"],
              values=spec["values"])
    st["cards"] = [label_card(lines, col) for lines, col in zip(spec["cards"], spec["card_cols"])]
    unit = spec.get("unit", "万")
    st["seglab"] = {(name, j): I.text(f"△{spec['values'][name][j]:,}{unit}" if unit == "円" else f"△{spec['values'][name][j]}{unit}",
                                      50, SEG_COL[kind][1], stroke=0)
                    for name, kind in spec["items"] for j in range(len(spec["incomes"]))}
    take = [spec["incomes"][j] - sum(spec["values"][n][j] for n, _ in spec["items"]) for j in range(len(spec["incomes"]))]
    word = spec.get("take_word", "手取り")
    st["takelab"] = [I.text(f"{word}\n{round(v):,}{unit}" if unit == "円" else f"{word}\n約{round(v, 1):g}{unit}", 70, WHITE, stroke=7,
                              stroke_col=(0, 90, 70)) for v in take]
    return st


def run(spec, cs, out_path, prev=None):
    durs = [c["dur"] for c in cs]
    total = sum(durs)
    diff = TOTAL - total
    if abs(diff) > 3 or durs[-1] + diff < 1.2:
        raise SystemExit(f"長さ {total:.2f}秒。59.9秒にするには {diff:+.2f}秒 の調整が必要です")
    durs[-1] += diff
    cs[-1]["dur"] = durs[-1]
    for c in cs:   # 音（BGMなし）：しゃべる猫だけ鳴らす
        v_ = c.get("voice")
        voices = v_ if isinstance(v_, (list, tuple)) else [v_]   # 両方の猫を鳴らすときはリストで（10/27）
        c["cats"] = [dict(a=a, mute=(j not in voices)) for j, a in enumerate(c["cats3"]) if a]
        c.update(fixed=True, no_pop=True)
    R.conan_confusion(cs, zlib.crc32(os.path.basename(out_path).encode()))   # 戸惑いの場面はコナンのひらめき（10/28）
    starts = list(np.cumsum([0] + durs[:-1]))
    st = make_static(spec)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wav = out_path + ".audio.f32"
    R.build_audio(cs, starts, durs, TOTAL).tofile(wav)
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(R.FPS), "-i", "-",
         "-f", "f32le", "-ar", str(R.SR), "-ac", "2", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", out_path],
        stdin=subprocess.PIPE)
    if prev:
        os.makedirs(prev, exist_ok=True)
    nframes = int(round(TOTAL * R.FPS))
    fno = 0
    for i, c in enumerate(cs):
        rd = Renderer(c, st)
        end = min(nframes, int(round((starts[i] + durs[i]) * R.FPS)))
        shot = False
        while fno < end:
            tt = fno / R.FPS - starts[i]
            u8 = (np.clip(rd.frame(tt), 0, 1) * 255).astype(np.uint8)
            proc.stdin.write(u8.tobytes())
            if prev and not shot and tt > 0.8:
                cv2.imwrite(os.path.join(prev, f"{i:02d}.jpg"), u8, [cv2.IMWRITE_JPEG_QUALITY, 80])
                shot = True
            fno += 1
        rd.close()
        print(f"\r{i + 1}/{len(cs)}  {fno / R.FPS:5.1f}s / {TOTAL}s", end="", flush=True)
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    print(f"\n-> {out_path} ({TOTAL}s)")
