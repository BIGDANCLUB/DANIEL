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


def type_a_set():
    """11/14 ユーザー指定：いつものA案の形（左に外観・右に料理・左上の帯・黄色い枠に2行）で3案。"""
    R, BK = T.RED, T.BLACK
    L = ("happy_hamster_open_arms", 1.0, 125, 410, 280, False)
    for name, left, right, rc, l1, l2 in [
        ("b1", "mc01_front", "f_teriyaki", "showoff_gojo_cosplay_cat",
         [("マック新作チキン", R), ("3種", BK)], [("優勝", R), ("はまさかの…", BK)]),
        ("b2", "mc01_front", "f_lineup", "surprise_big_pupils_cat",
         [("新作3つ", R), ("一気に頼んだら", BK)], [("店員さん", BK), ("に全部バレた", R)]),
        ("b3", "mc03_front_night", "f_teriyaki_bai", "sad_banana_cat_cry",
         [("うますぎて", BK), ("販売休止", R)], [("てりやきの倍", R), ("を食べ納め", BK)]),
    ]:
        T.type_a("jidaraku_19_mac_thumb_%s.png" % name, left, right, L, [(rc, 1.0, 1170, 410, 300, False)],
                 "30代独身　ひとりマック新作チキン", l1, l2, split=640, size=108)


def center_cat(name, cat, l1, l2, left="mc01_front", right="f_teriyaki", tag="30代独身　ひとりマック新作チキン"):
    """11/14 ユーザー指定：b1 をもとに、猫を1匹だけ真ん中に大きく置く形（左右の写真・左上の帯・黄色い枠の2行はそのまま）。"""
    from PIL import ImageDraw as D
    W, H, top_h, split = T.W, T.H, 410, 640
    img = Image.new("RGBA", (W, H), T.WHITE)
    img.alpha_composite(T.fill_photo(left, split, top_h, cx=0.5), (0, 0))
    img.alpha_composite(T.fill_photo(right, W - split - 4, top_h), (split + 4, 0))
    t = T.runs([(tag, (T.RED, T.WHITE))], 52, 2, 640)
    box = Image.new("RGBA", (t.width + 50, t.height + 34), T.WHITE + (255,))
    D.Draw(box).rectangle((0, 0, box.width - 1, box.height - 1), outline=T.BLACK, width=5)
    box.alpha_composite(t, (25, 17))
    box = box.rotate(2, expand=True, resample=Image.BICUBIC)
    D.Draw(img).rectangle((0, top_h + 18, W, H), fill=(255, 245, 60, 255), outline=T.BLACK, width=6)
    T.put_cat(img, cat, 1.0, 640, top_h + 18, 420, False)   # 黄色い枠の上にのる大きな猫
    img.alpha_composite(box, (14, top_h - box.height + 40))   # 帯は猫より手前
    a = T.runs(l1, 108, 8, W - 40)
    b = T.runs(l2, 108, 8, W - 40)
    img.alpha_composite(a, ((W - a.width) // 2, top_h + 40))
    img.alpha_composite(b, ((W - b.width) // 2, top_h + 50 + a.height))
    T.save(img, name)


def center_set():
    R, BK = T.RED, T.BLACK
    l1, l2 = [("マック新作チキン", R), ("3種", BK)], [("食べ比べした結果…", BK)]
    center_cat("jidaraku_19_mac_thumb_c1.png", "stare_big_eyes_tabby_kitten", l1, l2)
    center_cat("jidaraku_19_mac_thumb_c2.png", "surprise_big_pupils_cat", l1, l2)
    center_cat("jidaraku_19_mac_thumb_c3.png", "showoff_gojo_cosplay_cat", l1, l2)
