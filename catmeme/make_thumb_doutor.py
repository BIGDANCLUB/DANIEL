"""自堕落シリーズ #27 ドトールのモーニングのサムネ（11/22）。ドンキ・吉野家の決定版と同じ作り：
夜の外観を全面・ユーザー提供の猫（t_cat_coffee）を上半身アップで真ん中・白い札・黄色い角丸の帯にネタの一言（赤＋一部青）。

python3 catmeme/make_thumb_yakinikulike.py → thumbs/jidaraku_27_doutor_thumb_c1〜c3.png
"""
import os

from PIL import Image, ImageDraw

import make_thumb_long_ref as T
import make_thumb_short_ref as S

D = os.path.join(T.HERE, "backgrounds", "jidaraku", "27_doutor")
S.BGS.insert(0, D)


def one(name, runs, tag="30代独身　給料日の夜"):
    img = T.fill_photo("dt01_front", T.W, T.H, cy=0.3)
    cat = Image.open(os.path.join(D, "t_cat_coffee.png")).convert("RGBA")
    cat = cat.crop((0, 0, cat.width, int(cat.height * 0.6)))   # 上半身（顔・ドトールのカップまで）
    k = 640 / cat.width
    cat = cat.resize((640, int(cat.height * k)), Image.LANCZOS)
    img.alpha_composite(cat, ((T.W - cat.width) // 2, T.H - cat.height - 170))   # 11/23 ユーザー指定：猫は真ん中
    big = T.runs(runs, 170, 10, T.W - 220)
    bh = big.height + 40
    by = T.H - bh - 18
    ImageDraw.Draw(img).rounded_rectangle((60, by, T.W - 60, by + bh), 36, fill=(255, 245, 60, 255))
    img.alpha_composite(big, ((T.W - big.width) // 2, by + 20))
    t = T.runs([(tag, (T.RED, T.WHITE))], 60, 2, 900)
    box = Image.new("RGBA", (t.width + 56, t.height + 34), T.WHITE + (255,))
    box.alpha_composite(t, (28, 17))
    img.alpha_composite(box, ((T.W - box.width) // 2, by - box.height + 12))
    T.save(img, name)


def main():
    one("jidaraku_27_doutor_thumb_c1.png", [("休日の朝を", T.RED), ("ワンコイン", T.BLUE), ("で買う", T.RED)], tag="30代独身　平日休み")
    one("jidaraku_27_doutor_thumb_c2.png", [("給料日前でも", T.RED), ("優雅な朝", T.BLUE)], tag="30代独身　平日休み")
    one("jidaraku_27_doutor_thumb_c3.png", [("みんな出勤", T.RED), ("俺はモーニング", T.BLUE)], tag="30代独身　平日休み")


if __name__ == "__main__":
    main()

