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
