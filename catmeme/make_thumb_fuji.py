"""自堕落シリーズ #13 富士山のサムネ（11/10）。いつものAパターンで文言3案。a1 を採用（11/10 ユーザー指定）。

python3 catmeme/make_thumb_fuji.py → thumbs/jidaraku_13_fuji_thumb_a1/a2/a3.png
左：ご来光・右：山頂のカップラーメン（写真は右上にのせる代わりに背景に）
"""
import os

from PIL import Image

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in (os.path.join("jidaraku", "13_fuji"), "jidaraku"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK = T.RED, T.BLACK


def main():
    L = ("happy_hamster_open_arms", 1.0, 130, 410, 280, False)
    RC = [("despair_dramatic_kitten", 0.8, 1160, 410, 300, False)]
    for name, left, right, tag, l1, l2 in [
        ("a1", "fj05_summit", "f_vending", "30代独身　ひとり富士山",
         [("標高", BK), ("と", BK), ("自販機の値段", R), ("が上がる", BK)], [("酸素", T.BLUE), ("と", BK), ("財布", R), ("が薄くなる", BK)]),
        ("a2", "f_goraiko", "f_cupramen", "30代独身　ひとり富士山",
         [("山頂のカップ麺", BK)], [("うますぎる", T.BLUE), ("高すぎる", R), ("（値段が）", BK)]),
        ("a3", "fj01_5gome", "fj07_night", "30代独身　ひとり富士山",
         [("5合目は", BK), ("ハンター試験", R), ("の会場", BK)], [("日本の最高峰に", BK), ("ひとりで挑む", R)]),
    ]:
        T.type_a("jidaraku_13_fuji_thumb_%s.png" % name, left, right, L, RC, tag, l1, l2, split=640, size=104)


if __name__ == "__main__":
    main()
