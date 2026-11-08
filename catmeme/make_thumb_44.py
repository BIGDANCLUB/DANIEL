"""44本目（たばこを吸う人と吸わない人の生涯コスト）のサムネ候補3つ（11/8）。41〜43と同じ A・B・C の3パターン。

python3 catmeme/make_thumb_44.py → thumbs/44_tabako_thumb_a/b/c.png
"""
import glob
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

S.BGS += sorted(x for x in glob.glob(os.path.join(T.HERE, "backgrounds", "*")) if os.path.isdir(x))
R, BK, Y, NV = T.RED, T.BLACK, T.YELLOW, T.NAVY


def main():
    T.type_a("44_tabako_thumb_a.png", "bg15_convenience", "bg51_night_street",
             ("think_chin_paw_orange_cat", 1.0, 300, 410, 320, False),
             [("surprise_big_pupils_cat", 1.0, 900, 410, 320, False), ("money_counting_orange_cat", 1.0, 1150, 410, 280, True)],
             "1日1箱 580円",
             [("たばこ代", BK), ("30年で", BK)], [("約635万!?", R)], split=640, size=118)
    T.type_b("44_tabako_thumb_b.png",
             [("bg15_convenience", [("think_chin_paw_orange_cat", 1.0, 160, 470, 320, False)]),
              ("bg25_office_desk", [("money_counting_orange_cat", 1.0, 160, 470, 320, False)]),
              ("bg98_izakaya_night", [("despair_dramatic_kitten", 0.8, 160, 470, 320, False)]),
              ("bg14_home_night", [("surprise_big_pupils_cat", 1.0, 160, 470, 330, False)])],
             [("txt", "1箱580円", 160, 60, 42, Y, -6), ("txt", "1年で21万", 480, 60, 42, Y, 4),
              ("txt", "半箱でも318万", 800, 60, 38, Y, -4), ("txt", "30年で635万!?", 1120, 60, 38, R, 6)],
             [("たばこを吸う人と吸わない人", R)], [("一生でいくら違う？", NV)])
    T.type_c("44_tabako_thumb_c.png", "bg51_night_street",
             [("surprise_big_pupils_cat", 1.0, 1040, 620, 470, False), ("think_chin_paw_orange_cat", 1.0, 250, 640, 360, False)],
             "1日580円のたばこ代を30年積み上げると", "新車2台分!?", zoom=1.05)


if __name__ == "__main__":
    main()
