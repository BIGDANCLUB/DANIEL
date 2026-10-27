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
SEG_COL = {"red": ((230, 20, 20), WHITE), "gray": ((205, 205, 205), BLACK), "dark": ((140, 140, 140), BLACK),
           "green": ((40, 210, 60), BLACK), "purple": ((170, 40, 200), WHITE), "orange": ((255, 140, 0), BLACK)}


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
        if c.get("shout"):
            self.shout_im = I.text("＼" + c["shout"][0] + "／", 76, YELLOW, stroke=9, stroke_col=BLACK, max_w=520).rotate(
                8, expand=True, resample=Image.BICUBIC)
        if c.get("result"):
            tx = I.text(c["result"], 170, WHITE, stroke=12, stroke_col=(150, 0, 60), max_w=W - 200)
            rb = Image.new("RGBA", (tx.width + 160, tx.height + 70), BASE + (255,))
            ImageDraw.Draw(rb).rectangle((0, 0, rb.width - 1, rb.height - 1), outline=YELLOW, width=12)
            rb.alpha_composite(tx, (80, 35))
            self.res = rb.rotate(-4, expand=True, resample=Image.BICUBIC)
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
            cv2.rectangle(out, (x0 - 6, int(top) - 6), (x1 + 6, BAR_BOT + 6), (0, 0, 0), -1)
            out[int(top):BAR_BOT, x0:x1] = np.array(BASE[::-1], np.float32) / 255
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
                out[int(y):int(y + hpx), x0:x1] = np.array(col[::-1], np.float32) / 255
                cv2.rectangle(out, (x0, int(y)), (x1, int(y + hpx)), (0, 0, 0), 4)
                if grow > 0.6:
                    lab = st["seglab"][(name, j)]
                    if lab.height > hpx - 6:   # 細い段は札を小さくして段の中におさめる（10/27）
                        k_ = max(hpx - 6, 20) / lab.height
                        lab = lab.resize((max(1, int(lab.width * k_)), max(1, int(lab.height * k_))), Image.LANCZOS)
                    I.put(out, lab, (x0 + x1) / 2 if CATX else x0 + lab.width / 2 + 14, y + min(hpx, 120) / 2 + 4)
                y += hpx
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
                img, al = self._cat(clip, name, t, 460 if big else 380, 250)
                hh, ww = al.shape
                x0 = int(min(max(CATX[j] - ww / 2, 10), W - ww - 10))
                I.over(out, img, al, x0, int(1300 - hh))
                continue
            img, al = self._cat(clip, name, t, 330 if big else 290, 330 if big else 300)
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
        if c.get("shout"):   # 「＼もっと入れろや／」のような掛け声（猫の上・10/27）
            text_, j = c["shout"]
            sh = self.shout_im
            x = (CATX[j] if CATX else COLX[j])
            x = min(max(x, sh.width / 2 + 10), W - sh.width / 2 - 10)
            I.put(out, sh, x + 6 * math.sin(t * 30), 860)
        if c.get("result"):   # 結果発表：ピンクの帯がズームで出て、キラキラ（10/27 ユーザー指定：重りではない表現）
            u = min(1.0, t / 0.22)
            ov = np.zeros((H, W), np.float32)
            for i in range(36):
                a = 2 * math.pi * i / 36 + t * 1.2
                pts = np.array([(W / 2, 820), (W / 2 + 2400 * math.cos(a - 0.04), 820 + 2400 * math.sin(a - 0.04)),
                                (W / 2 + 2400 * math.cos(a + 0.04), 820 + 2400 * math.sin(a + 0.04))], np.int32)
                cv2.fillConvexPoly(ov, pts, 1.0)
            out = out * (1 - 0.35 * u) + ov[..., None] * 0.5 * u * np.array([0.6, 0.95, 1.0], np.float32)
            sc = 0.3 + 0.7 * (1 - (1 - u) ** 3) + (0.03 * math.sin(t * 16) if t > 0.3 else 0)
            im = self.res.resize((max(1, int(self.res.width * sc)), max(1, int(self.res.height * sc))))
            I.put(out, im, W / 2, 820)
            for i in range(10):   # キラキラ
                ph = (t * 3 + i * 0.37) % 1.0
                x = W / 2 + math.cos(i * 2.3) * (300 + 180 * ph)
                y = 820 + math.sin(i * 2.3) * (200 + 120 * ph)
                r_ = int(26 * (1 - ph)) + 4
                cv2.line(out, (int(x - r_), int(y)), (int(x + r_), int(y)), (1, 1, 1), 5, cv2.LINE_AA)
                cv2.line(out, (int(x), int(y - r_)), (int(x), int(y + r_)), (1, 1, 1), 5, cv2.LINE_AA)
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
                if t - land < 0.5:
                    for side in (-1, 1):
                        for k in range(3):
                            x0 = W / 2 + side * (420 + k * 30)
                            y0 = y_land + self.ban.height - 20 - k * 40
                            cv2.line(out, (int(x0), int(y0)), (int(x0 + side * 90), int(y0 - 50)), (1, 1, 1), 9, cv2.LINE_AA)
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


def bill_img(w=230):
    """お札（リアルに見えるよう、地紋・すかし・数字・枠を描く。本物の紙幣のまねはしない・10/27）。"""
    h = int(w * 0.5)
    S_ = 3
    im = Image.new("RGBA", (w * S_, h * S_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W_, H_ = im.size
    for y in range(H_):   # うすい茶色のグラデーション
        u = y / H_
        d.line((0, y, W_, y), fill=(int(214 - 20 * u), int(196 - 22 * u), int(150 - 20 * u), 255))
    for i in range(0, W_, 9):   # 細かい地紋（波線）
        pts = [(i + 18 * math.sin(yy / 22), yy) for yy in range(0, H_, 6)]
        d.line(pts, fill=(190, 160, 110, 120), width=2)
    d.rectangle((10, 10, W_ - 11, H_ - 11), outline=(110, 80, 40, 255), width=8)
    d.rectangle((26, 26, W_ - 27, H_ - 27), outline=(140, 105, 60, 255), width=3)
    cx, cy, r = W_ * 0.72, H_ * 0.5, H_ * 0.32   # 右のすかし（だ円）
    d.ellipse((cx - r * 0.8, cy - r, cx + r * 0.8, cy + r), fill=(235, 222, 190, 255), outline=(130, 95, 50, 255), width=4)
    d.ellipse((cx - r * 0.45, cy - r * 0.55, cx + r * 0.45, cy + r * 0.35), fill=(205, 185, 140, 255))
    f = I.font(int(H_ * 0.26))
    d.text((W_ * 0.08, H_ * 0.12), "10000", font=f, fill=(90, 60, 25, 255))
    f2 = I.font(int(H_ * 0.34))
    d.text((W_ * 0.12, H_ * 0.45), "壱万", font=f2, fill=(110, 75, 35, 255))
    im = im.resize((w, h), Image.LANCZOS)
    sh = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((6, 6, w + 6, h + 6), fill=(0, 0, 0, 90))
    sh.alpha_composite(im, (0, 0))
    return sh


def set_cols(n):
    """列の数（2 か 3）に合わせて、棒の位置と太さを決める。"""
    global COLX, COLW, CATX, BAR_BOT
    if n == 2:
        COLX, COLW, CATX, BAR_BOT = (395, 685), 210, (150, 930), 1250
    else:   # 3列：棒を短くして、猫は棒の下に置く（残りのお金を隠さない・10/27）
        COLX, COLW, CATX, BAR_BOT = (205, 540, 875), 250, None, 990


def make_static(spec):
    set_cols(len(spec["incomes"]))
    base = I.cover(spec["bg"])
    x0, y0, x1, y1 = PANEL
    base[y0:y1, x0:x1] = base[y0:y1, x0:x1] * 0.25 + np.array(TEAL[::-1], np.float32) / 255 * 0.75
    title = Image.new("RGBA", (W, 230), (0, 0, 0, 0))
    t1 = I.text(spec["title"][0], 92, RED, stroke=5, stroke_col=WHITE)
    t2 = I.text(spec["title"][1], 92, RED, stroke=5, stroke_col=WHITE)
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
                              stroke_col=(120, 0, 50)) for v in take]
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
