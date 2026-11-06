"""自堕落シリーズ #10 新時代のサムネ（11/6 ユーザー指定：いつものAパターン）。

python3 catmeme/make_thumb_shinjidai.py → thumbs/jidaraku_10_shinjidai_thumb_a.png
左：夜の外観・右：伝串と生ビール。札：30代独身 水曜の夜。字幕（11/6 ユーザー指定）：新時代は一人飲みもオススメ／パリモチとカニの遊園地!?
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in (os.path.join("jidaraku", "10_shinjidai"), "jidaraku"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK = T.RED, T.BLACK


def main():
    T.type_a("jidaraku_10_shinjidai_thumb_a.png", "n01_front", "f_denkushi",
             ("happy_hamster_open_arms", 1.0, 110, 410, 250, False),
             [("excited_hodomoe_city_cat", 1.0, 1150, 410, 320, False)],
             "30代独身　水曜の夜",
             [("新時代", T.BLUE), ("は", BK), ("一人飲み", R), ("もオススメ", BK)],
             [("パリモチ", R), ("と", BK), ("カニ", R), ("の遊園地!?", BK)], split=640, size=104)


if __name__ == "__main__":
    main()
