"""自堕落シリーズ #26 焼肉ライクのサムネ（11/22）。ドンキ・吉野家の決定版と同じ作り：
夜の外観を全面・ユーザー提供の猫（t_cat_yakiniku）を上半身アップで真ん中・白い札・黄色い角丸の帯にネタの一言（赤＋一部青）。

python3 catmeme/make_thumb_yakinikulike.py → thumbs/jidaraku_26_yakinikulike_thumb_c1〜c3.png
"""
import os

from PIL import Image, ImageDraw

import make_thumb_long_ref as T
import make_thumb_short_ref as S

D = os.path.join(T.HERE, "backgrounds", "jidaraku", "26_yakinikulike")
S.BGS.insert(0, D)


def one(name, runs, tag="30代独身　給料日の夜"):
    img = T.fill_photo("yl01_front", T.W, T.H, cy=0.45)
    cat = Image.open(os.path.join(D, "t_cat_yakiniku.png")).convert("RGBA")
    cat = cat.crop((0, 0, cat.width, int(cat.height * 0.52)))   # 上半身（顔・ご飯・肉）
    k = 700 / cat.width
    cat = cat.resize((700, int(cat.height * k)), Image.LANCZOS)
    img.alpha_composite(cat, (T.W - cat.width - 10, T.H - cat.height - 150))   # 右寄せ：左の光る看板（焼肉ライク 580円）を見せる
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
    one("jidaraku_26_yakinikulike_thumb_c1.png", [("これのために", T.RED), ("働いた", T.BLUE)])
    one("jidaraku_26_yakinikulike_thumb_c2.png", [("1人1台は", T.RED), ("自分だけの城", T.BLUE)])
    one("jidaraku_26_yakinikulike_thumb_c3.png", [("給料日は", T.RED), ("カルビに溶ける", T.BLUE)])


if __name__ == "__main__":
    main()


def final():
    """11/22 ユーザー指定：猫は真ん中・帯「焼肉ライクで城主になる」（焼肉ライクを青）。"""
    img = T.fill_photo("yl01_front", T.W, T.H, cy=0.45)
    cat = Image.open(os.path.join(D, "t_cat_yakiniku.png")).convert("RGBA")
    cat = cat.crop((0, 0, cat.width, int(cat.height * 0.52)))
    k = 700 / cat.width
    cat = cat.resize((700, int(cat.height * k)), Image.LANCZOS)
    img.alpha_composite(cat, ((T.W - cat.width) // 2, T.H - cat.height - 150))
    big = T.runs([("焼肉ライク", T.BLUE), ("で城主になる", T.RED)], 170, 10, T.W - 220)
    bh = big.height + 40
    by = T.H - bh - 18
    ImageDraw.Draw(img).rounded_rectangle((60, by, T.W - 60, by + bh), 36, fill=(255, 245, 60, 255))
    img.alpha_composite(big, ((T.W - big.width) // 2, by + 20))
    t = T.runs([("30代独身　給料日の夜", (T.RED, T.WHITE))], 60, 2, 900)
    box = Image.new("RGBA", (t.width + 56, t.height + 34), T.WHITE + (255,))
    box.alpha_composite(t, (28, 17))
    img.alpha_composite(box, ((T.W - box.width) // 2, by - box.height + 12))
    T.save(img, "jidaraku_26_yakinikulike_thumb_final.png")
