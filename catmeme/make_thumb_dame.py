"""ダメ人間の猫ミームのサムネ（縦 1080x1920）。動画と同じ帯・猫ミームに、極太フォント・集中線・爆発バッジで派手にする。

python3 catmeme/make_thumb_dame.py → thumbs/short_dame_rent.png
"""
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import parts as P
import short_hooks as H
import short_refstyle as M

HERE = M.HERE
SW, SH = M.SW, M.SH
WHITE, BLACK, RED, YELLOW, LIME = M.WHITE, M.BLACK, M.RED, M.YELLOW, M.LIME
ORANGE = (255, 120, 0)


def fancy(text, size, top=(255, 245, 120), bottom=(255, 150, 0), rims=((0, 0, 0, 9), (235, 25, 25, 26), (0, 0, 0, 38)),
          shadow=18, max_w=None):
    """極太フォントの文字：上下のグラデーション＋何重もの縁（内側から順に rims=(色, 太さ)）＋影。max_w に収まるまで小さくする。"""
    d0 = ImageDraw.Draw(Image.new("L", (8, 8)))
    pad = max(w for *_, w in rims) + shadow + 10
    while True:
        f = P.font("dela", size)
        l, t_, r, b = d0.textbbox((0, 0), text, font=f)
        if not max_w or r - l + pad * 2 <= max_w or size < 40:
            break
        size -= 6
    W_, H_ = int(r - l + pad * 2), int(b - t_ + pad * 2)
    xy = (pad - l, pad - t_)
    out = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    base = Image.new("L", (W_, H_), 0)
    ImageDraw.Draw(base).text(xy, text, font=f, fill=255)
    base = np.asarray(base)

    def mask(w):   # 縁は文字の形をふくらませて作る（フォントの縁取り機能だとゴミが出るため）
        if w == 0:
            return Image.fromarray(base)
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * w + 1, 2 * w + 1))
        return Image.fromarray(cv2.dilate(base, k))

    outer = rims[-1][3]
    sh = mask(outer).filter(ImageFilter.GaussianBlur(6))
    out.paste((0, 0, 0, 200), (shadow, shadow), Image.eval(sh, lambda v: v * 200 // 255).crop((0, 0, W_ - shadow, H_ - shadow)))
    for *col, w in reversed(rims):
        out.paste(tuple(col) + (255,), (0, 0), mask(w))
    g = np.linspace(0, 1, H_)[:, None, None]
    grad = (np.array(top) * (1 - g) + np.array(bottom) * g).repeat(W_, 1).astype(np.uint8)
    out.paste(Image.fromarray(grad, "RGB"), (0, 0), mask(0))
    return out


def burst(text, r=235, n=16, fill=RED, col=YELLOW, size=62):
    """ギザギザの爆発バッジ。"""
    S_ = int(r * 2 + 40)
    im = Image.new("RGBA", (S_, S_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = S_ / 2
    pts = [(c + (r if i % 2 == 0 else r * 0.74) * math.cos(math.pi * i / n), c + (r if i % 2 == 0 else r * 0.74) * math.sin(math.pi * i / n))
           for i in range(n * 2)]
    d.polygon([(x + 10, y + 12) for x, y in pts], fill=(0, 0, 0, 160))
    d.polygon(pts, fill=fill + (255,), outline=WHITE, width=12)
    f = P.font("dela", size)
    d.multiline_text((c, c), text, font=f, fill=col, anchor="mm", align="center", spacing=6, stroke_width=8, stroke_fill=BLACK)
    return im


def envelope(top, money, w=390, h=275):
    """飛んでいく茶封筒（家賃袋など）。左に流れる線つき。"""
    m = 90    # 流れる線の分
    im = Image.new("RGBA", (w + m + 30, h + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, y in enumerate((0.25, 0.5, 0.75)):
        d.line([(10 + 25 * (i % 2), h * y), (m - 10, h * y)], fill=WHITE + (230,), width=12)
    x0 = m
    d.rounded_rectangle((x0 + 14, 16, x0 + w + 14, h + 16), 14, fill=(0, 0, 0, 150))
    d.rounded_rectangle((x0, 0, x0 + w, h), 14, fill=(214, 168, 104, 255), outline=BLACK, width=8)
    d.polygon([(x0 + 6, 6), (x0 + w - 6, 6), (x0 + w / 2, h * 0.38)], fill=(190, 142, 80, 255), outline=BLACK, width=6)
    d.text((x0 + w / 2, h * 0.52), top, font=P.font("dela", 76), fill=BLACK, anchor="mm")
    d.text((x0 + w / 2, h * 0.80), money, font=P.font("dela", 66), fill=RED, anchor="mm", stroke_width=6, stroke_fill=WHITE)
    return im


def _canvas(w, h):
    im = Image.new("RGBA", (w + 30, h + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    return im, d


def wallet(money, w=400, h=270):
    """開いた空っぽの財布。"""
    im, d = _canvas(w, h)
    d.rounded_rectangle((14, 16, w + 14, h + 16), 30, fill=(0, 0, 0, 150))
    d.rounded_rectangle((0, 0, w, h), 30, fill=(150, 40, 40, 255), outline=BLACK, width=8)
    d.rounded_rectangle((26, 26, w - 26, h * 0.42), 16, fill=(60, 15, 15, 255), outline=BLACK, width=6)   # 札入れ（空っぽ）
    d.text((w / 2, h * 0.24), "スッカラカン", font=P.font("dela", 48), fill=(200, 200, 200), anchor="mm")
    d.text((w / 2, h * 0.72), money, font=P.font("dela", 96), fill=YELLOW, anchor="mm", stroke_width=8, stroke_fill=BLACK)
    return im


def scale(value, w=380, h=320):
    """体重計（数字の画面つき）。"""
    im, d = _canvas(w, h)
    d.rounded_rectangle((14, 16, w + 14, h + 16), 40, fill=(0, 0, 0, 150))
    d.rounded_rectangle((0, 0, w, h), 40, fill=(245, 245, 245, 255), outline=BLACK, width=8)
    d.rounded_rectangle((40, 36, w - 40, h * 0.55), 14, fill=(30, 40, 30, 255), outline=BLACK, width=6)
    d.text((w / 2, h * 0.32), value, font=P.font("dela", 92), fill=(255, 70, 70), anchor="mm")
    d.text((w / 2, h * 0.78), "体重計", font=P.font("dela", 56), fill=BLACK, anchor="mm")
    return im


def clock(hhmm, r=180):
    """目覚まし時計（針と数字）。"""
    w = h = r * 2 + 40
    im, d = _canvas(w, h)
    c = w / 2
    for sx in (-1, 1):   # ベル
        d.ellipse((c + sx * r * 0.62 - 55, 0, c + sx * r * 0.62 + 55, 90), fill=(230, 40, 40, 255), outline=BLACK, width=7)
    d.ellipse((c - r + 14, 40 + 16, c + r + 14, 40 + 2 * r + 16), fill=(0, 0, 0, 150))
    d.ellipse((c - r, 40, c + r, 40 + 2 * r), fill=(230, 40, 40, 255), outline=BLACK, width=8)
    d.ellipse((c - r + 28, 68, c + r - 28, 40 + 2 * r - 28), fill=WHITE + (255,), outline=BLACK, width=6)
    cy = 40 + r
    h_, m_ = (int(v) for v in hhmm.split(":"))
    for ang, ln, wd in (((h_ % 12 + m_ / 60) * 30, r * 0.42, 16), (m_ * 6, r * 0.66, 10)):
        a = math.radians(ang - 90)
        d.line([(c, cy), (c + ln * math.cos(a), cy + ln * math.sin(a))], fill=BLACK, width=wd)
    d.text((c, cy - r * 0.40), hhmm, font=P.font("dela", 70), fill=RED, anchor="mm", stroke_width=6, stroke_fill=WHITE)
    return im


def phone(top, value, w=300, h=460):
    """スマホの画面（残高など）。"""
    im, d = _canvas(w, h)
    d.rounded_rectangle((14, 16, w + 14, h + 16), 40, fill=(0, 0, 0, 150))
    d.rounded_rectangle((0, 0, w, h), 40, fill=(25, 25, 30, 255), outline=WHITE, width=8)
    d.rounded_rectangle((22, 50, w - 22, h - 50), 18, fill=(240, 240, 245, 255))
    d.text((w / 2, h * 0.36), top, font=P.font("dela", 62), fill=BLACK, anchor="mm")
    d.text((w / 2, h * 0.58), value, font=P.font("dela", 74), fill=RED, anchor="mm")
    return im


def rays(out, cy, cols=((255, 40, 40), (255, 200, 0)), alpha=0.55, n=48):
    """止まった集中線（放射状）。"""
    im = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, L_ = SW / 2, 3000
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 0.5) / n
        d.polygon([(cx, cy), (cx + L_ * math.cos(a0), cy + L_ * math.sin(a0)), (cx + L_ * math.cos(a1), cy + L_ * math.sin(a1))],
                  fill=cols[i % 2] + (int(255 * alpha),))
    H.put(out, im, SW / 2, SH / 2)


def vignette(out, k=0.75):
    yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
    r = np.sqrt(((xx - SW / 2) / (SW / 2)) ** 2 + ((yy - SH * 0.55) / (SH / 2)) ** 2)
    out *= (1 - k * np.clip(r - 0.55, 0, 1))[..., None]


def make(out_path, top, lines, cats, items=(), bg="bg06_spotlight"):
    """lines=[(文字, 大きさ, 中心y, 角度, 上の色, 下の色)]、cats=[(素材, x, 高さ, 反転, 役名)]、
    items=[(画像, 中心x, 中心y, 角度)]（爆発バッジ・封筒など。猫ミームに重ならない所に置く）。"""
    out = M.vbg(bg).copy() * 0.55
    rays(out, SH * 0.42)
    vignette(out)
    for a, x, h, fl, tag in cats:
        H.cat(out, a, 1.0, x, SH + 40, h, flip=fl)
        if tag:
            H.put(out, fancy(tag, 120, top=(200, 255, 120), bottom=(90, 210, 20), rims=((0, 0, 0, 22),), shadow=10), x, SH - 200)
    for s, size, y, ang, c1, c2 in lines:
        H.put(out, fancy(s, size, top=c1, bottom=c2, max_w=SW + 40), SW / 2, y, angle=ang)
    for im, x, y, ang in items:
        H.put(out, im, x, y, angle=ang)
    band = Image.new("RGBA", (SW, 300), (0, 0, 0, 235))
    H.put(out, band, SW / 2, 170)
    H.put(out, fancy(top, 170, top=(255, 90, 90), bottom=(200, 0, 0), rims=((255, 255, 255, 9), (0, 0, 0, 22)), shadow=10,
                     max_w=SW - 30), SW / 2, 170)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cv2.imwrite(out_path, (np.clip(out, 0, 1) * 255).astype(np.uint8))
    print("->", out_path)


def dame_rent():
    """#1 家賃で馬券買っちゃった。"""
    make(os.path.join(HERE, "thumbs", "short_dame_rent.png"), "とあるダメ人間",
         [("家賃で", 200, 520, -5, (255, 255, 255), (255, 255, 255)),
          ("馬券", 340, 790, -5, (255, 240, 0), (255, 170, 0)),
          ("買っちゃった", 145, 1030, -5, (255, 255, 255), (255, 255, 255))],
         [("sad_banana_cat_cry", 290, 800, False, None)],
         items=[(envelope("家賃", "7万2千円"), 840, 1330, 12)])


WHITE2 = ((255, 255, 255), (255, 255, 255))
GOLD = ((255, 240, 0), (255, 170, 0))
TOP = "とあるダメ人間"


def thumb(name, lines, cat, item, item_y=1330):
    """#2 以降の共通の並び：3行の文字・左下に猫ミーム・右下に小物（猫に重ねない）。lines=[(文字, 大きさ, 金色か)]。"""
    ys = (520, 790, 1030)
    make(os.path.join(HERE, "thumbs", name + ".png"), TOP,
         [(s, size, y, -5, *(GOLD if gold else WHITE2)) for (s, size, gold), y in zip(lines, ys)],
         [(cat, 290, 800, False, None)], items=[(item, 840, item_y, 12)])


def dame_payday():
    thumb("short_dame_payday", [("給料日から", 190, False), ("3日で", 230, False), ("残高82円", 260, True)],
          "despair_dramatic_kitten", wallet("82円"))


def dame_diet():
    thumb("short_dame_diet", [("ダイエット", 200, False), ("3日目で", 190, False), ("ラーメン大盛り", 220, True)],
          "eat_crunchy_cat_luna", scale("+5kg"))


def dame_late():
    thumb("short_dame_late", [("電車のせいに", 180, False), ("したら", 160, False), ("自転車通勤", 230, True)],
          "confused_i_dont_know_cat", clock("9:25"), item_y=1470)


def dame_gacha():
    thumb("short_dame_gacha", [("生活費で", 210, False), ("ガチャ", 340, True), ("回した", 190, False)],
          "blank_black_cat_zoning_out", phone("残高", "512円"), item_y=1480)


if __name__ == "__main__":
    import sys
    for n in sys.argv[1:] or ["rent"]:
        globals()["dame_" + n]()
