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


# ---- 10/28 ユーザー指定：B をもとに、虹色・金色に光らせて、猫ミームをもっと使う ----
def rainbow_rays(img, cx, cy, n=36, alpha=150, rot=0.0):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    cols = [(255, 60, 60), (255, 160, 0), (255, 240, 0), (60, 220, 90), (40, 170, 255), (150, 90, 255), (255, 80, 200)]
    for i in range(n):
        a = 2 * math.pi * i / n + rot
        c = cols[i % len(cols)]
        d.polygon([(cx, cy), (cx + 2200 * math.cos(a - 0.05), cy + 2200 * math.sin(a - 0.05)),
                   (cx + 2200 * math.cos(a + 0.05), cy + 2200 * math.sin(a + 0.05))], fill=c + (alpha,))
    img.alpha_composite(ov)


def glow(im, col=(255, 220, 80), r=18, k=2):
    """文字や吹き出しのまわりを光らせる。"""
    a = im.split()[-1].filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(r))
    g = Image.new("RGBA", im.size, col + (0,))
    g.putalpha(a.point(lambda v: min(255, v * k)))
    pad = Image.new("RGBA", im.size, (0, 0, 0, 0))
    pad.alpha_composite(g)
    pad.alpha_composite(im)
    return pad


def gold_text(text, size, max_w, angle=0):
    """金色のグラデーションの特大文字（黒い太いふち）。"""
    t = T.runs([(text, ((255, 215, 0), BLACK))], size, 16, max_w, shadow=True, grad=((255, 250, 190), (230, 150, 0)))
    return t.rotate(angle, expand=True, resample=Image.BICUBIC)


def rainbow_text(text, size, max_w, angle=0):
    t = T.runs([(text, (WHITE, BLACK))], size, 16, max_w, shadow=True)
    w, h = t.size
    grad = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(grad)
    cols = [(255, 70, 70), (255, 170, 0), (255, 240, 0), (70, 230, 100), (50, 180, 255), (170, 100, 255)]
    for x in range(w):
        u = x / max(1, w - 1) * (len(cols) - 1)
        i = min(int(u), len(cols) - 2)
        f = u - i
        c = tuple(int(cols[i][k] * (1 - f) + cols[i + 1][k] * f) for k in range(3))
        gd.line((x, 0, x, h), fill=c + (255,))
    # 白い文字の部分だけ虹色に（ふちの黒は残す）
    px = t.load()
    gp = grad.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0 and r > 200 and g > 200 and b > 200:
                px[x, y] = gp[x, y][:3] + (a,)
    return t.rotate(angle, expand=True, resample=Image.BICUBIC)


def sparkles(img, pts):
    d = ImageDraw.Draw(img)
    for x, y, r in pts:
        for w_, col in ((r // 3 + 6, BLACK), (r // 3, (255, 250, 200))):
            d.polygon([(x, y - r), (x + w_ / 3, y - w_ / 3), (x + r, y), (x + w_ / 3, y + w_ / 3), (x, y + r),
                       (x - w_ / 3, y + w_ / 3), (x - r, y), (x - w_ / 3, y - w_ / 3)], fill=col)


def rainbow_band(img, y0, h):
    band = Image.new("RGBA", (W, h))
    d = ImageDraw.Draw(band)
    cols = [(230, 0, 40), (255, 110, 0), (230, 0, 120), (120, 0, 200), (230, 0, 40)]
    for x in range(W):
        u = x / (W - 1) * (len(cols) - 1)
        i = min(int(u), len(cols) - 2)
        f = u - i
        d.line((x, 0, x, h), fill=tuple(int(cols[i][k] * (1 - f) + cols[i + 1][k] * f) for k in range(3)) + (240,))
    d.rectangle((0, 0, W - 1, 8), fill=(255, 215, 0, 255))
    d.rectangle((0, h - 9, W - 1, h - 1), fill=(255, 215, 0, 255))
    img.alpha_composite(band, (0, y0))


def b_plus(name, variant):
    img = punchy("bg25_wagyu_sashi", zoom=1.1)
    rainbow_rays(img, 640, 330, alpha=140, rot=0.04 * variant)
    rainbow_band(img, H - 200, 200)
    cats = {
        1: [("surprise_big_pupils_cat", 0.6, 1090, 540, 560, True), ("despair_dramatic_kitten", 0.8, 170, 560, 420, False),
            ("huh_huh_cat", 1.0, 400, 545, 300, False), ("stare_tabby_wide_eyes_cat", 0.6, 830, 545, 280, True)],
        2: [("stare_tabby_wide_eyes_cat", 0.6, 1110, 545, 560, True), ("sad_banana_cat_cry", 1.0, 160, 560, 400, False),
            ("surprise_big_pupils_cat", 0.6, 420, 545, 290, False), ("rage_talking_cat", 1.0, 840, 545, 280, True)],
        3: [("huh_huh_cat", 1.0, 1100, 550, 560, True), ("despair_dramatic_kitten", 0.8, 180, 560, 420, False),
            ("surprise_big_pupils_cat", 0.6, 420, 545, 290, False), ("money_counting_orange_cat", 1.0, 850, 545, 280, True)],
    }[variant]
    for c_ in cats:
        T.put_cat(img, *c_)
    ex = explosion("和牛が海外へ密輸!?", 700, 380, fill=(255, 230, 0), size=120, angle=6)
    put(img, glow(ex, (255, 255, 255), r=22), 620, 225)
    l1 = T.runs([("見つけたのは", (WHITE, BLACK))], 128, 16, 700, shadow=True)
    l2 = gold_text("中国!?", 150, 520) if variant != 2 else rainbow_text("中国!?", 150, 520)
    x0 = (W - (l1.width + l2.width)) // 2
    img.alpha_composite(l1, (x0, H - 100 - l1.height // 2))
    img.alpha_composite(l2, (x0 + l1.width - 10, H - 100 - l2.height // 2))
    T.save(img, name)


if __name__ == "__main__":
    for v in (1, 2, 3):
        b_plus(f"25_wagyu_dopa_b{v}.png", v)
