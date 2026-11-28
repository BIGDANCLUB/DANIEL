"""40本目（新築マンションvs中古＋リノベ）のサムネ候補3つ（11/3）。タワマン回と同じ A・B・C の3パターン。

python3 catmeme/make_thumb_40.py → thumbs/40_mansion_thumb_a/b/c.png
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in ("35_tower", "01_todai", "02_october", "04_leak", "78_agency", "48_clean"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
import glob
S.BGS += sorted(x for x in glob.glob(os.path.join(T.HERE, "backgrounds", "*")) if os.path.isdir(x))
R, BK, Y, NV = T.RED, T.BLACK, T.YELLOW, T.NAVY


def main():
    T.type_a("40_mansion_thumb_a.png", "bg35_tower", "bg02_room",
             ("showoff_gojo_cosplay_cat", 1.0, 300, 410, 320, False),
             [("surprise_big_pupils_cat", 1.0, 900, 410, 320, False), ("money_counting_orange_cat", 1.0, 1150, 410, 280, True)],
             "1700万円も安いのに",
             [("新築", R), ("vs", BK), ("中古＋リノベ", NV)], [("30年で差は", BK), ("たった190万!?", R)], split=600, size=108)
    T.type_b("40_mansion_thumb_b.png",
             [("bg35_tower", [("showoff_gojo_cosplay_cat", 1.0, 160, 470, 320, False)]),
              ("bg02_room", [("happy_hamster_open_arms", 1.0, 160, 470, 320, False)]),
              ("bg35_tower_lobby", [("despair_dramatic_kitten", 0.8, 160, 470, 330, False)]),
              ("bg35_suburb_street", [("surprise_big_pupils_cat", 1.0, 160, 470, 330, False)])],
             [("txt", "新築6500万", 160, 60, 42, Y, -6), ("txt", "中古＋リノベ4800万", 480, 60, 34, Y, 4),
              ("txt", "修繕積立金が…", 800, 60, 38, Y, -4), ("txt", "売る時に逆転!?", 1130, 60, 38, R, 6)],
             [("新築マンションと中古＋リノベ", R)], [("30年でいくら違う？", NV)])
    T.type_c("40_mansion_thumb_c.png", "bg35_tower",
             [("surprise_big_pupils_cat", 1.0, 1040, 620, 470, False), ("money_counting_orange_cat", 1.0, 250, 640, 360, False)],
             "1700万安い中古　30年でくらべると", "差は190万!?", zoom=1.05)


if __name__ == "__main__":
    main()
