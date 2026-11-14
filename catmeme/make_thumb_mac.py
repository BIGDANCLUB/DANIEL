"""自堕落シリーズ #19 マック新作チキンのサムネ（11/14）。焼肉きんぐ回と同じ形：背景いっぱい＋猫1匹を大きく真ん中、
小さい明朝「30代独身」、下の白い角丸の帯に赤い明朝のデカ字幕。

python3 catmeme/make_thumb_mac.py → thumbs/jidaraku_19_mac_thumb_a1〜a3.png
"""
import os

from PIL import Image, ImageDraw

import make_thumb_jidaraku as JT
import make_thumb_long_ref as T
import make_thumb_short_ref as S

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "jidaraku", "19_mac"))


def one(name, bg, cat, big_text, small_text="30代独身", zoom=1.0):
    img = T.fill_photo(bg, T.W, T.H, zoom=zoom)
    T.put_cat(img, cat, 0.6, 640, 560, 540, False)
    small = JT.serif_text(small_text, 54, T.WHITE, 7, T.BLACK, 600)
    img.alpha_composite(small, ((T.W - small.width) // 2, 455))
    big = JT.serif_text(big_text, 140, (210, 40, 30), 0, T.WHITE, T.W - 90)
    box = Image.new("RGBA", (T.W - 30, big.height + 40), (0, 0, 0, 0))
    ImageDraw.Draw(box).rounded_rectangle((0, 0, box.width - 1, box.height - 1), 36, fill=(255, 255, 255, 245))
    box.alpha_composite(big, ((box.width - big.width) // 2, 20))
    img.alpha_composite(box, (15, T.H - box.height - 12))
    T.save(img, name)


def main():
    one("jidaraku_19_mac_thumb_a1.png", "mc01_front", "stare_big_eyes_tabby_kitten", "マック新作チキン食べくらべ")
    one("jidaraku_19_mac_thumb_a2.png", "mc03_front_night", "surprise_big_pupils_cat", "新作3つ一気に頼んだ結果")
    one("jidaraku_19_mac_thumb_a3.png", "mc02_seat", "sad_banana_cat_cry", "人気すぎて販売休止")


if __name__ == "__main__":
    main()
