"""自堕落シリーズ #9 コストコのサムネ（11/5 ユーザー指定：いつものAパターン）。

python3 catmeme/make_thumb_costco.py → thumbs/jidaraku_09_costco_thumb_a.png
左にカート・右に牛タンの塊。札：30代独身 ひとり買い物。字幕：休日の1人コストコは危険／牛タンの塊をカートに入れる
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in (os.path.join("jidaraku", "09_costco"), "jidaraku"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK = T.RED, T.BLACK


def main():
    T.type_a("jidaraku_09_costco_thumb_a.png", "f_cart", "f_gyutan",
             ("surprise_big_pupils_cat", 1.0, 330, 410, 300, False),
             [("excited_hodomoe_city_cat", 1.0, 1080, 410, 330, False)],
             "30代独身　ひとり買い物",
             [("休日の", BK), ("1人コストコ", T.BLUE), ("は危険", BK)],
             [("牛タンの塊", R), ("をカートに入れる", BK)], split=640, size=104)


if __name__ == "__main__":
    main()
