"""25本目（和牛を狙った男たち）のサムネ・ドパガキ向け版（10/28 ユーザー指定）。横 1280x720。
こい色・集中線・爆発の吹き出し・特大の文字・赤丸と矢印・驚く猫を大きく。人は描かない。

python3 catmeme/make_thumb_wagyu_dopa.py → thumbs/25_wagyu_dopa_a.png / _b / _c
"""
import math
import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

import make_thumb_long_ref as T
import make_thumb_short_ref as S

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "25_wagyu"))
W, H = T.W, T.H
RED, YEL, WHITE, BLACK = (235, 20, 30), (255, 235, 0), (255, 255, 255), (0, 0, 0)


def punchy(name, zoom=1.0, cx=0.5, cy=0.5):
    """写真を色こく・くっきり。"""
    im = T.fill_photo(name, W, H, cx=cx, zoom=zoom, cy=cy).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.6)
    im = ImageEnhance.Contrast(im).enhance(1.25)
    return im.convert("RGBA")


def burst_lines(img, cx, cy, col=(255, 255, 255, 150), n=48):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i in range(n):
        a = 2 * math.pi * i / n
        d.polygon([(cx, cy), (cx + 2000 * math.cos(a - 0.03), cy + 2000 * math.sin(a - 0.03)),
                   (cx + 2000 * math.cos(a + 0.03), cy + 2000 * math.sin(a + 0.03))], fill=col)
    img.alpha_composite(ov)


def explosion(text, w, h, fill=YEL, tcol=RED, size=80, angle=-8):
    """ギザギザの爆発の吹き出し。"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    for i in range(28):
        a = 2 * math.pi * i / 28
        r = (0.5 if i % 2 == 0 else 0.42)
        pts.append((w / 2 + w * r * math.cos(a), h / 2 + h * r * math.sin(a)))
    d.polygon(pts, fill=BLACK)
    pts2 = [(w / 2 + (x - w / 2) * 0.93, h / 2 + (y - h / 2) * 0.93) for x, y in pts]
    d.polygon(pts2, fill=fill)
    t = T.runs([(text, (tcol, WHITE))], size, 10, int(w * 0.8))
    im.alpha_composite(t, ((w - t.width) // 2, (h - t.height) // 2))
    return im.rotate(angle, expand=True, resample=Image.BICUBIC)


def big_text(parts, size, max_w, angle=0, shadow=True):
    """特大の文字。どの色も黒い太いふち（白い字が背景に埋もれないように）。"""
    parts = [(t_, (c_, BLACK)) for t_, c_ in parts]
    t = T.runs(parts, size, 16, max_w, shadow=shadow)
    return t.rotate(angle, expand=True, resample=Image.BICUBIC)


def red_circle(img, box, w=14):
    d = ImageDraw.Draw(img)
    d.ellipse(box, outline=WHITE, width=w + 10)
    d.ellipse(box, outline=RED, width=w)


def put(img, im, x, y):
    img.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))


def a():
    """ストロー1本＋特大「ストロー1本で国の宝が…」"""
    img = punchy("bg25_frozen_straws", zoom=1.15, cx=0.55)
    burst_lines(img, 700, 470)
    red_circle(img, (560, 360, 960, 560))
    T.arrow(img, 1010, 230, 860, 380, col=RED, w=26)
    T.put_cat(img, "stare_tabby_wide_eyes_cat", 0.6, 1100, 730, 520, True)
    T.put_cat(img, "huh_huh_cat", 1.0, 170, 730, 400, False)
    put(img, big_text([("ストロー", WHITE), ("1本", YEL)], 150, 900, -4), 470, 120)
    put(img, big_text([("で", WHITE), ("国の宝", RED), ("が…", WHITE)], 150, 900, -4), 500, 270)
    put(img, explosion("365本!?", 420, 300, size=110), 960, 560)
    T.save(img, "25_wagyu_dopa_a.png")


def b():
    """サシのアップ＋「見つけたのは中国!?」"""
    img = punchy("bg25_wagyu_sashi", zoom=1.1)
    burst_lines(img, 640, 400, col=(255, 230, 120, 110))
    band = Image.new("RGBA", (W, 190), (200, 0, 20, 235))
    img.alpha_composite(band, (0, H - 190))
    T.put_cat(img, "surprise_big_pupils_cat", 0.6, 1080, 560, 560, True)
    T.put_cat(img, "despair_dramatic_kitten", 0.8, 200, 560, 440, False)
    put(img, explosion("和牛が海外へ!?", 600, 340, size=110, angle=6), 600, 230)
    put(img, big_text([("見つけたのは", WHITE), ("中国", YEL), ("!?", WHITE)], 140, W - 60, 0), 640, H - 95)
    T.save(img, "25_wagyu_dopa_b.png")


def c():
    """和牛のお皿＋「法律なかった!?」＋懲役10年"""
    img = punchy("bg25_wagyu_steak", zoom=1.05)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 90))
    img.alpha_composite(shade)
    burst_lines(img, 640, 360, col=(255, 255, 255, 120))
    T.put_cat(img, "huh_huh_cat", 1.0, 1110, 730, 560, True)
    T.put_cat(img, "stare_tabby_wide_eyes_cat", 0.6, 160, 730, 420, False)
    put(img, big_text([("和牛 持ち出し", WHITE)], 120, 1000, -3), 600, 110)
    put(img, big_text([("法律", YEL), ("なかった!?", RED)], 190, 1150, -3), 610, 300)
    put(img, explosion("今は懲役10年", 620, 320, fill=YEL, tcol=RED, size=100, angle=-6), 640, 560)
    T.save(img, "25_wagyu_dopa_c.png")


if __name__ == "__main__":
    a()
    b()
    c()
