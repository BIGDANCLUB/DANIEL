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
