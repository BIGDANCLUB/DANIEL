"""自堕落シリーズ #22 はじめての競馬場のサムネ（11/17）。マック回 c2 の形をもとに、
11/17 ユーザー指定：黄色い帯を少し横にせまく・「初めての競馬」を赤い大きな文字1行で。

python3 catmeme/make_thumb_keiba.py → thumbs/jidaraku_22_keiba_thumb_c1〜c3.png
"""
import os

from PIL import Image, ImageDraw

import make_thumb_long_ref as T
import make_thumb_short_ref as S

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "jidaraku", "22_keiba"))
TAG = "30代独身　ひとり競馬場"


def one(name, cat, left="kb02_stand", right="f_horse", text="初めての競馬", inset=90):
    W, H, top_h, split = T.W, T.H, 410, 640
    img = Image.new("RGBA", (W, H), T.WHITE)
    img.alpha_composite(T.fill_photo(left, split, top_h, cx=0.5), (0, 0))
    img.alpha_composite(T.fill_photo(right, W - split - 4, top_h), (split + 4, 0))
    ImageDraw.Draw(img).rectangle((inset, top_h + 18, W - inset, H - 14), fill=(255, 245, 60, 255), outline=T.BLACK, width=6)
    T.put_cat(img, cat, 1.0, 640, top_h + 18, 420, False)
    t = T.runs([(text, (T.RED, T.WHITE))], 52, 2, 640)
    box = Image.new("RGBA", (t.width + 50, t.height + 34), T.WHITE + (255,))
    ImageDraw.Draw(box).rectangle((0, 0, box.width - 1, box.height - 1), outline=T.BLACK, width=5)
    tg = T.runs([(TAG, (T.RED, T.WHITE))], 52, 2, 640)
    box = Image.new("RGBA", (tg.width + 50, tg.height + 34), T.WHITE + (255,))
    ImageDraw.Draw(box).rectangle((0, 0, box.width - 1, box.height - 1), outline=T.BLACK, width=5)
    box.alpha_composite(tg, (25, 17))
    box = box.rotate(2, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(box, (14, top_h - box.height + 40))
    big = T.runs([(text, T.RED)], 200, 10, W - inset * 2 - 60)
    y0 = top_h + 18 + (H - 14 - top_h - 18 - big.height) // 2
    img.alpha_composite(big, ((W - big.width) // 2, y0))
    T.save(img, name)


def main():
    one("jidaraku_22_keiba_thumb_c1.png", "surprise_big_pupils_cat")
    one("jidaraku_22_keiba_thumb_c2.png", "stare_big_eyes_tabby_kitten", left="kb01_gate")
    one("jidaraku_22_keiba_thumb_c3.png", "sad_banana_cat_cry")


if __name__ == "__main__":
    main()


def full(name, cat, col, cy=0.3, cat_x=300, small_text="30代独身", fill=(255, 255, 255, 245)):
    """11/17 ユーザー指定：「40代独身 給料日 焼肉」のサムネをまねる。走る馬の写真を全面に・左上の帯はなし・
    小さい明朝「30代独身」・白い角丸の帯（黒い枠なし）に明朝の大きな文字。"""
    import make_thumb_jidaraku as JT
    img = T.fill_photo("f_horse", T.W, T.H, cy=cy, zoom=1.06)   # 写真の白いふちを切る
    T.put_cat(img, cat, 0.6, cat_x, 560, 520, False)
    small = JT.serif_text(small_text, 54, T.WHITE, 7, T.BLACK, 600)
    big = JT.serif_text("初めての競馬", 170, col, 0, T.WHITE, T.W - 200)
    box = Image.new("RGBA", (T.W - 160, big.height + 40), (0, 0, 0, 0))
    ImageDraw.Draw(box).rounded_rectangle((0, 0, box.width - 1, box.height - 1), 36, fill=fill)
    box.alpha_composite(big, ((box.width - big.width) // 2, 20))
    by = T.H - box.height - 18
    img.alpha_composite(small, ((T.W - small.width) // 2, by - small.height - 8))
    img.alpha_composite(box, (80, by))
    T.save(img, name)


def full_set():
    full("jidaraku_22_keiba_thumb_d1.png", "stare_big_eyes_tabby_kitten", (210, 40, 30))
    full("jidaraku_22_keiba_thumb_d2.png", "stare_big_eyes_tabby_kitten", (20, 20, 20))


def final():
    """11/17 ユーザー指定：d1 をもとに小さい文字を「30代にして」に（帯は白・黄色はやめた）。"""
    full("jidaraku_22_keiba_thumb_final.png", "stare_big_eyes_tabby_kitten", (210, 40, 30), small_text="30代にして")


def final2():
    """11/17 ユーザー指定：帯を c1 の黄色い帯＋赤いゴシックの大きな文字にもどす（黒い枠なし）。背景は走る馬の全面のまま。"""
    import make_thumb_jidaraku as JT
    img = T.fill_photo("f_horse", T.W, T.H, cy=0.3, zoom=1.06)
    T.put_cat(img, "stare_big_eyes_tabby_kitten", 0.6, 300, 560, 520, False)
    big = T.runs([("初めての競馬", T.RED)], 200, 10, T.W - 260)
    bh = big.height + 40
    by = T.H - bh - 18
    ImageDraw.Draw(img).rounded_rectangle((80, by, T.W - 80, by + bh), 36, fill=(255, 245, 60, 255))   # 11/17 角丸（白い帯の形をまねる）
    img.alpha_composite(big, ((T.W - big.width) // 2, by + 20))
    small = JT.serif_text("30代にして", 54, T.WHITE, 7, T.BLACK, 600)
    img.alpha_composite(small, ((T.W - small.width) // 2, by - small.height - 8))
    T.save(img, "jidaraku_22_keiba_thumb_final.png")


def final3():
    """11/17 ユーザー指定：「20代ぼっち女 1人焼肉に行く」のサムネをまねる。帯なし・ピンクの角丸札に白い明朝「30代独身」・
    下に極太明朝の大きな文字「初めての（黄色）競馬（赤）」（白いふち＋黒いふち）。背景は走る馬の全面。"""
    from PIL import ImageFont
    import jidaraku as J
    img = T.fill_photo("f_horse", T.W, T.H, cy=0.3, zoom=1.06)
    T.put_cat(img, "stare_big_eyes_tabby_kitten", 0.6, 300, 520, 480, False)
    f = ImageFont.truetype(J.SERIF, 200)
    try:
        f.set_variation_by_axes([900])
    except Exception:
        pass
    parts = [("初めての", (255, 230, 0)), ("競馬", (230, 30, 30))]
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    ws = [d0.textlength(t, font=f) for t, _ in parts]
    tw = int(sum(ws)) + 60
    th = 260
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = 30
    for (t, col), w in zip(parts, ws):
        d.text((x, 10), t, font=f, fill=(20, 20, 20), stroke_width=22, stroke_fill=(20, 20, 20))
        d.text((x, 10), t, font=f, fill=col, stroke_width=9, stroke_fill=(255, 255, 255))
        x += w
    layer = layer.crop(layer.getbbox())
    if layer.width > T.W - 40:
        k = (T.W - 40) / layer.width
        layer = layer.resize((int(layer.width * k), int(layer.height * k)), Image.LANCZOS)
    by = T.H - layer.height - 24
    sf = ImageFont.truetype(J.SERIF, 64)
    try:
        sf.set_variation_by_axes([800])
    except Exception:
        pass
    sw = int(d0.textlength("30代独身", font=sf))
    tag = Image.new("RGBA", (sw + 60, 96), (0, 0, 0, 0))
    ImageDraw.Draw(tag).rounded_rectangle((0, 0, tag.width - 1, tag.height - 1), 18, fill=(232, 70, 140, 255))
    ImageDraw.Draw(tag).text((30, 8), "30代独身", font=sf, fill=(255, 255, 255))
    img.alpha_composite(tag, ((T.W - tag.width) // 2, by - tag.height - 6))
    img.alpha_composite(layer, ((T.W - layer.width) // 2, by))
    T.save(img, "jidaraku_22_keiba_thumb_final.png")


def final4():
    """11/17 ユーザー指定：
    - 「30代独身」は c1 の札（白地・黒い枠・赤いゴシック・少しかたむける）
    - 大きな文字は参考（1人焼肉に行く）に忠実に：極太の明朝（Zen Old Mincho Black・OFL）・黒い太いふち＋黒い影、白いふちなし"""
    from PIL import ImageFilter, ImageFont
    img = T.fill_photo("f_horse", T.W, T.H, cy=0.3, zoom=1.06)
    T.put_cat(img, "stare_big_eyes_tabby_kitten", 0.6, 300, 520, 480, False)
    f = ImageFont.truetype(os.path.join(T.HERE, "fonts", "ZenOldMincho-Black.ttf"), 230)
    parts = [("初めての", (255, 232, 0)), ("競馬", (232, 28, 28))]
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    ws = [d0.textlength(t, font=f) for t, _ in parts]
    layer = Image.new("RGBA", (int(sum(ws)) + 80, 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = 40
    for (t, col), w in zip(parts, ws):
        d.text((x, 20), t, font=f, fill=(15, 15, 15), stroke_width=20, stroke_fill=(15, 15, 15))
        d.text((x, 20), t, font=f, fill=col, stroke_width=6, stroke_fill=col)   # 文字そのものを太らせる（参考の極太に近づける）
        x += w
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 170), (0, 0), layer.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    out = Image.new("RGBA", (layer.width + 10, layer.height + 10), (0, 0, 0, 0))
    out.alpha_composite(sh, (10, 10))
    out.alpha_composite(layer, (0, 0))
    out = out.crop(out.getbbox())
    if out.width > T.W - 30:
        k = (T.W - 30) / out.width
        out = out.resize((int(out.width * k), int(out.height * k)), Image.LANCZOS)
    by = T.H - out.height - 14
    t = T.runs([("30代独身", (T.RED, T.WHITE))], 60, 2, 640)
    box = Image.new("RGBA", (t.width + 56, t.height + 34), T.WHITE + (255,))
    ImageDraw.Draw(box).rectangle((0, 0, box.width - 1, box.height - 1), outline=T.BLACK, width=5)
    box.alpha_composite(t, (28, 17))
    box = box.rotate(2, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(box, ((T.W - box.width) // 2, by - box.height + 10))
    img.alpha_composite(out, ((T.W - out.width) // 2, by))
    T.save(img, "jidaraku_22_keiba_thumb_final.png")
