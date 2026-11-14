"""自堕落シリーズ #12 ミスド（ドーナツビュッフェ）のサムネ（11/7）。いつものAパターンで文言3案。

python3 catmeme/make_thumb_misdo.py → thumbs/jidaraku_12_misdo_thumb_a1/a2/a3.png
左：外観・右：ショーケースの棚（11/7 ユーザー指定・a1 を採用）
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in (os.path.join("jidaraku", "12_misdo"), "jidaraku"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK = T.RED, T.BLACK


def main():
    L = ("happy_hamster_open_arms", 1.0, 120, 410, 250, False)
    RC = [("excited_hodomoe_city_cat", 1.0, 1160, 410, 300, False)]
    for name, tag, l1, l2 in [
        ("a1", "30代独身　日曜の朝", [("ミスド", T.BLUE), ("の", BK), ("食べ放題", R), ("に1人で挑戦", BK)], [("60分で", BK), ("何個いける!?", R)]),
        ("a2", "30代独身　日曜の朝", [("1個まで", R), ("だった俺が", BK)], [("ミスド", T.BLUE), ("60分", R), ("食べ放題!?", BK)]),
        ("a3", "30代独身　ひとりミスド", [("ドーナツ", BK), ("ビュッフェ60分", R)], [("10個とった", R), ("結果…", BK)]),
    ]:
        T.type_a("jidaraku_12_misdo_thumb_%s.png" % name, "m01_front", "m02_showcase", L, RC, tag, l1, l2, split=640, size=104)


if __name__ == "__main__":
    main()
