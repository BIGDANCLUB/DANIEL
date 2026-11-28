"""41本目（中学から私立vs大学まで国公立）のサムネ候補3つ（11/3）。タワマン回と同じ A・B・C の3パターン。

python3 catmeme/make_thumb_40.py → thumbs/41_gakuhi_thumb_a/b/c.png
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
    T.type_a("41_gakuhi_thumb_a.png", "bg21_school_gate", "bg01_campus",
             ("read_book_orange_kitten", 1.0, 300, 410, 320, False),
             [("surprise_big_pupils_cat", 1.0, 900, 410, 320, False), ("money_counting_orange_cat", 1.0, 1150, 410, 280, True)],
             "子ども1人あたり",
             [("中学から私立", R), ("vs", BK), ("大学まで国公立", NV)], [("学費の差は", BK), ("約700万!?", R)], split=600, size=100)
    T.type_b("41_gakuhi_thumb_b.png",
             [("bg19_kids_room", [("despair_dramatic_kitten", 0.8, 160, 470, 320, False)]),
              ("bg30_classroom_desk", [("money_counting_orange_cat", 1.0, 160, 470, 320, False)]),
              ("bg21_school_gate", [("happy_hamster_open_arms", 1.0, 160, 470, 320, False)]),
              ("bg01_campus", [("surprise_big_pupils_cat", 1.0, 160, 470, 330, False)])],
             [("txt", "小学生で塾250万", 160, 60, 36, Y, -6), ("txt", "私立中は年156万", 480, 60, 36, Y, 4),
              ("txt", "高校は支援あり", 800, 60, 38, Y, -4), ("txt", "合計700万差!?", 1130, 60, 40, R, 6)],
             [("中学から私立と大学まで国公立", R)], [("学費はいくら違う？", NV)])
    T.type_c("41_gakuhi_thumb_c.png", "bg21_school_gate",
             [("surprise_big_pupils_cat", 1.0, 1040, 620, 470, False), ("read_book_orange_kitten", 1.0, 250, 640, 360, False)],
             "中学から私立　大学まで国公立とくらべると", "差は700万!?", zoom=1.05)


if __name__ == "__main__":
    main()
