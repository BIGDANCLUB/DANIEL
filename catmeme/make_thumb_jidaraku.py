"""自堕落シリーズのサムネ（横 1280x720）。make_thumb_long_ref.py の部品を使う。

python3 catmeme/make_thumb_jidaraku.py → thumbs/jidaraku_01_yakiniku_thumb.png
"""
import os

from PIL import Image, ImageDraw

import make_thumb_long_ref as T
import make_thumb_short_ref as S

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "jidaraku", "01_yakiniku"))


def yakiniku():
    """網の上のきんぐカルビの写真いっぱい＋驚く猫。上に黒い帯、下に黄色い大きな文字（参考 C 型）。"""
    img = T.fill_photo("j05_grill", T.W, T.H, zoom=1.05)
    T.put_cat(img, "stare_tabby_wide_eyes_cat", 0.6, 1010, 600, 520, True)
    T.put_cat(img, "despair_dramatic_kitten", 0.8, 230, 640, 380, False)
    shade = Image.new("RGBA", (T.W, T.H))
    sd = ImageDraw.Draw(shade)
    for y in range(T.H):
        sd.line((0, y, T.W, y), fill=(0, 0, 0, int(170 * max(0, (y - 380) / 340))))
    img.alpha_composite(shade)
    t = T.runs([("30代独身　ひとり焼肉きんぐで調子に乗った結果", (T.YELLOW, T.BLACK))], 58, 6, T.W - 30)
    ImageDraw.Draw(img).rectangle((0, 0, T.W, t.height + 22), fill=T.BLACK + (255,))
    img.alpha_composite(t, ((T.W - t.width) // 2, 11))
    T.scribble(img, "きんぐカルビ", 600, 200, 80, T.YELLOW, -6)
    T.scribble(img, "デカすぎ!!", 640, 300, 96, T.RED, -6)
    b = T.runs([("食べすぎた…", (T.YELLOW, T.BLACK))], 210, 12, 1040, grad=((255, 250, 210), (245, 200, 30)))
    img.alpha_composite(b, ((T.W - b.width) // 2 - 60, T.H - b.height - 30))
    T.save(img, "jidaraku_01_yakiniku_thumb.png")


def serif_text(t, size, fill, stroke, stroke_col, max_w):
    import jidaraku as J
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    while d0.textlength(t, font=J.font(size)) + stroke * 2 > max_w and size > 30:
        size -= 4
    f = J.font(size)
    w = int(d0.textlength(t, font=f)) + stroke * 2 + 20
    im = Image.new("RGBA", (w, int(size * 1.4) + stroke * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((stroke + 10, stroke), t, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_col)
    return im.crop(im.getbbox())


def yakiniku_b():
    """10/26 ユーザー指定の参考（「休日に1人快活クラブ」）どおり：お店の外観いっぱい＋猫1匹を大きく真ん中に、
    小さい明朝「30代独身」、下の白い角丸の帯に赤い明朝のデカ字幕。"""
    img = T.fill_photo("j02_store_front", T.W, T.H, zoom=1.0)
    T.put_cat(img, "stare_big_eyes_tabby_kitten", 0.6, 640, 560, 540, False)
    small = serif_text("30代独身", 54, T.WHITE, 7, T.BLACK, 600)
    img.alpha_composite(small, ((T.W - small.width) // 2, 455))
    big = serif_text("休日に1人焼肉きんぐ", 140, (210, 40, 30), 0, T.WHITE, T.W - 90)
    box = Image.new("RGBA", (T.W - 30, big.height + 40), (0, 0, 0, 0))
    ImageDraw.Draw(box).rounded_rectangle((0, 0, box.width - 1, box.height - 1), 36, fill=(255, 255, 255, 245))
    box.alpha_composite(big, ((box.width - big.width) // 2, 20))
    img.alpha_composite(box, (15, T.H - box.height - 12))
    T.save(img, "jidaraku_01_yakiniku_thumb.png")


if __name__ == "__main__":
    yakiniku_b()
