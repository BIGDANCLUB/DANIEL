"""自堕落シリーズ #28 丸亀製麺のサムネ（11/28）。ドトール・吉野家の決定版と同じ作り：
夜の外観を全面・ユーザー提供の猫（t_cat_udon：うどんをすする猫）を真ん中・白い札・黄色い角丸の帯にネタの一言（赤＋一部青）。

python3 catmeme/make_thumb_marugame.py → thumbs/jidaraku_28_marugame_thumb_c1〜c3.png
"""
import os

from PIL import Image, ImageDraw

import make_thumb_long_ref as T
import make_thumb_short_ref as S

D = os.path.join(T.HERE, "backgrounds", "jidaraku", "28_marugame")
S.BGS.insert(0, D)
CAT = os.path.join(D, "t_cat_udon.png")


def one(name, big_runs, sub_runs=None, tag="30代独身　給料日前"):
    img = T.fill_photo("mg01_front", T.W, T.H, cy=0.35)
    big = T.runs(big_runs, 210, 12, 1200)
    line = big
    if sub_runs:
        sub = T.runs(sub_runs, 130, 10, 700)
        line = Image.new("RGBA", (big.width + sub.width, big.height), (0, 0, 0, 0))
        line.alpha_composite(big, (0, 0))
        line.alpha_composite(sub, (big.width, big.height - sub.height - 8))
    if line.width > T.W - 100:
        k2 = (T.W - 100) / line.width
        line = line.resize((int(line.width * k2), int(line.height * k2)), Image.LANCZOS)
    bh = line.height + 36
    by = T.H - bh - 14
    if os.path.exists(CAT):
        cat = Image.open(CAT).convert("RGBA")
        cat = cat.crop((0, 0, cat.width, int(cat.height * 0.66)))   # 顔・うどん・どんぶりまで
        k = 600 / cat.width
        cat = cat.resize((600, int(cat.height * k)), Image.LANCZOS)
        img.alpha_composite(cat, ((T.W - cat.width) // 2, max(0, by - cat.height + 40)))
    ImageDraw.Draw(img).rounded_rectangle((30, by, T.W - 30, by + bh), 40, fill=(255, 245, 60, 255))
    img.alpha_composite(line, ((T.W - line.width) // 2, by + 18))
    t = T.runs([(tag, (T.RED, T.WHITE))], 64, 2, 900)
    box = Image.new("RGBA", (t.width + 56, t.height + 34), T.WHITE + (255,))
    box.alpha_composite(t, (28, 17))
    img.alpha_composite(box, ((T.W - box.width) // 2, by - box.height + 12))
    T.save(img, name)


def main():
    one("jidaraku_28_marugame_thumb_c1.png", [("名実ともに", T.RED), ("得盛", T.BLUE)])
    one("jidaraku_28_marugame_thumb_c2.png", [("財布も寒い日の", T.RED), ("得盛", T.BLUE)], tag="30代独身　ボーナス前")
    one("jidaraku_28_marugame_thumb_c3.png", [("今日だけは", T.RED), ("得", T.BLUE)], [("（半額）", T.RED)])


if __name__ == "__main__":
    main()
