"""自堕落シリーズ #23 吉野家の牛すき鍋膳のサムネ（11/18）。競馬回の決定版（final5）と同じ形：
写真を全面・左に猫・黄色い角丸の帯に赤い太字・帯の上に白地の札（黒い枠なし）。

python3 catmeme/make_thumb_yoshinoya.py → thumbs/jidaraku_23_yoshinoya_thumb_c1〜c3.png
"""
import os

from PIL import Image, ImageDraw

import make_thumb_long_ref as T
import make_thumb_short_ref as S

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "jidaraku", "23_yoshinoya"))


def one(name, bg, cat, big_text, tag="30代独身", cat_x=300, item=None):
    img = T.fill_photo(bg, T.W, T.H, cy=0.5)
    if item:
        it = T.fill_photo(item, 620, 470)
        fr = Image.new("RGBA", (it.width + 24, it.height + 24), (255, 255, 255, 255))
        fr.alpha_composite(it, (12, 12))
        fr = fr.rotate(-3, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(fr, (T.W - fr.width - 30, 20))
    T.put_cat(img, cat, 0.6, cat_x, 560, 520, False)
    big = T.runs([(big_text, T.RED)], 180, 10, T.W - 260)
    bh = big.height + 40
    by = T.H - bh - 18
    ImageDraw.Draw(img).rounded_rectangle((80, by, T.W - 80, by + bh), 36, fill=(255, 245, 60, 255))
    img.alpha_composite(big, ((T.W - big.width) // 2, by + 20))
    t = T.runs([(tag, (T.RED, T.WHITE))], 60, 2, 900)
    box = Image.new("RGBA", (t.width + 56, t.height + 34), T.WHITE + (255,))
    box.alpha_composite(t, (28, 17))
    img.alpha_composite(box, ((T.W - box.width) // 2, by - box.height + 12))
    T.save(img, name)


def main():
    one("jidaraku_23_yoshinoya_thumb_c1.png", "yo02_seat", "stare_big_eyes_tabby_kitten", "牛すき鍋膳", item="f_nabe")
    one("jidaraku_23_yoshinoya_thumb_c2.png", "yo02_seat", "huh_huh_cat", "おかわりできる？", tag="毎年まぎらわしい", item="f_rice")
    one("jidaraku_23_yoshinoya_thumb_c3.png", "yo01_front", "realize_wet_cat_stare", "今年も来た冬の鍋", tag="30代独身　吉野家", item="f_nabe")


if __name__ == "__main__":
    main()


def final():
    """11/18 ユーザー指定：夜の店構え（yo03_front_wide）を全面・踊る猫のイラスト（t_cat_dance）・
    白い札「今年も来た」・黄色い帯「吉野家 牛すき鍋膳」。右に牛すき鍋膳の写真。"""
    img = T.fill_photo("yo03_front_wide", T.W, T.H, cy=0.45)
    it = T.fill_photo("f_nabe", 560, 400)
    fr = Image.new("RGBA", (it.width + 24, it.height + 24), (255, 255, 255, 255))
    fr.alpha_composite(it, (12, 12))
    fr = fr.rotate(-3, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(fr, (T.W - fr.width - 30, 150))
    cat = Image.open(os.path.join(T.HERE, "backgrounds", "jidaraku", "23_yoshinoya", "t_cat_dance.png")).convert("RGBA")
    k = 560 / cat.height
    cat = cat.resize((int(cat.width * k), 560), Image.LANCZOS)
    img.alpha_composite(cat, (60, 40))
    big = T.runs([("吉野家 牛すき鍋膳", T.RED)], 170, 10, T.W - 220)
    bh = big.height + 40
    by = T.H - bh - 18
    ImageDraw.Draw(img).rounded_rectangle((60, by, T.W - 60, by + bh), 36, fill=(255, 245, 60, 255))
    img.alpha_composite(big, ((T.W - big.width) // 2, by + 20))
    t = T.runs([("今年も来た", (T.RED, T.WHITE))], 72, 2, 900)
    box = Image.new("RGBA", (t.width + 60, t.height + 36), T.WHITE + (255,))
    box.alpha_composite(t, (30, 18))
    img.alpha_composite(box, ((T.W - box.width) // 2, by - box.height + 12))
    T.save(img, "jidaraku_23_yoshinoya_thumb_final.png")


def final2():
    """11/18 ユーザー指定：「20代ぼっち女 1人焼肉に行く」と同じ構図。店構えを全面・猫を真ん中に大きく・
    白い札「今年も来た」・極太明朝の大きな文字「吉野家（黄）牛すき鍋膳（赤）」（黒い太いふち＋影）。帯なし。"""
    from PIL import ImageFilter, ImageFont
    img = T.fill_photo("yo03_front_wide", T.W, T.H, cy=0.4)
    cat = Image.open(os.path.join(T.HERE, "backgrounds", "jidaraku", "23_yoshinoya", "t_cat_dance.png")).convert("RGBA")
    k = 700 / cat.height
    cat = cat.resize((int(cat.width * k), 700), Image.LANCZOS)
    img.alpha_composite(cat, ((T.W - cat.width) // 2, 10))
    f = ImageFont.truetype(os.path.join(T.HERE, "fonts", "ZenOldMincho-Black.ttf"), 200)
    parts = [("吉野家", (255, 232, 0)), ("牛すき鍋膳", (232, 28, 28))]
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    ws = [d0.textlength(t, font=f) + (40 if i == 0 else 0) for i, (t, _) in enumerate(parts)]
    layer = Image.new("RGBA", (int(sum(ws)) + 80, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = 40
    for (t, col), w in zip(parts, ws):
        d.text((x, 20), t, font=f, fill=(15, 15, 15), stroke_width=20, stroke_fill=(15, 15, 15))
        d.text((x, 20), t, font=f, fill=col, stroke_width=6, stroke_fill=col)
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
    t = T.runs([("今年も来た", (T.RED, T.WHITE))], 66, 2, 900)
    box = Image.new("RGBA", (t.width + 60, t.height + 36), T.WHITE + (255,))
    box.alpha_composite(t, (30, 18))
    img.alpha_composite(box, ((T.W - box.width) // 2, by - box.height + 4))
    img.alpha_composite(out, ((T.W - out.width) // 2, by))
    T.save(img, "jidaraku_23_yoshinoya_thumb_final.png")


def final3():
    """11/18 ユーザー指定：帯と文字は c1（白い札＋黄色い角丸の帯に赤いゴシック）。猫は「1人焼肉」のように上半身をアップで真ん中に。"""
    img = T.fill_photo("yo03_front_wide", T.W, T.H, cy=0.4)
    cat = Image.open(os.path.join(T.HERE, "backgrounds", "jidaraku", "23_yoshinoya", "t_cat_dance.png")).convert("RGBA")
    cat = cat.crop((0, 0, cat.width, int(cat.height * 0.55)))   # 上半身だけ
    k = 760 / cat.width
    cat = cat.resize((760, int(cat.height * k)), Image.LANCZOS)
    img.alpha_composite(cat, ((T.W - cat.width) // 2, T.H - cat.height))
    big = T.runs([("吉野家 牛すき鍋膳", T.RED)], 170, 10, T.W - 220)
    bh = big.height + 40
    by = T.H - bh - 18
    ImageDraw.Draw(img).rounded_rectangle((60, by, T.W - 60, by + bh), 36, fill=(255, 245, 60, 255))
    img.alpha_composite(big, ((T.W - big.width) // 2, by + 20))
    t = T.runs([("今年も来た", (T.RED, T.WHITE))], 60, 2, 900)
    box = Image.new("RGBA", (t.width + 56, t.height + 34), T.WHITE + (255,))
    box.alpha_composite(t, (28, 17))
    img.alpha_composite(box, ((T.W - box.width) // 2, by - box.height + 12))
    T.save(img, "jidaraku_23_yoshinoya_thumb_final.png")
