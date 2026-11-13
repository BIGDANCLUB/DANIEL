"""自堕落シリーズ #16 ソロキャンプのサムネ（11/13）。いつものAパターンで文言3案。

python3 catmeme/make_thumb_camp.py → thumbs/jidaraku_16_camp_thumb_a1〜a3.png
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in (os.path.join("jidaraku", "16_camp"), "jidaraku"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK = T.RED, T.BLACK


def main():
    L = ("happy_hamster_open_arms", 1.0, 125, 410, 280, False)
    for name, left, right, rc, l1, l2 in [
        ("a1", "cp02_site_night", "cp03_fire", "sad_banana_cat_cry",
         [("上司の理不尽", R), ("も", BK)], [("たき火", R), ("にくべてきた", BK)]),
        ("a2", "cp01_site", "f_tent", "despair_dramatic_kitten",
         [("ペグを打つたび", BK)], [("会社の理不尽", R), ("がよみがえる", BK)]),
        ("a3", "cp02_site_night", "cp03_fire", "rizz_cat_rizz",
         [("たき火は", BK)], [("大人のストレス焼却炉", R)]),
    ]:
        T.type_a("jidaraku_16_camp_thumb_%s.png" % name, left, right, L, [(rc, 1.0, 1170, 410, 300, False)],
                 "30代独身　ひとりソロキャンプ", l1, l2, split=640, size=108)


if __name__ == "__main__":
    main()


def final():
    """11/13 ユーザー指定：a1 をもとに文字を「会社の理不尽はたき火で／全て燃やす燃やす燃やす燃やす」に。"""
    L = ("happy_hamster_open_arms", 1.0, 125, 410, 280, False)
    T.type_a("jidaraku_16_camp_thumb_final.png", "cp02_site_night", "cp03_fire", L, [("sad_banana_cat_cry", 1.0, 1170, 410, 300, False)],
             "30代独身　ひとりソロキャンプ", [("会社の理不尽", R), ("はたき火で", BK)],
             [("全て", BK), ("燃やす燃やす燃やす燃やす", R)], split=640, size=108)
