"""27本目（持ち家vs賃貸 一生でかかるお金）のサムネ候補3つ（10/30）。横 1280x720。焼肉きんぐと同じ A・B・C の3パターン。

python3 catmeme/make_thumb_mochiie.py → thumbs/27_mochiie_thumb_a.png / _b / _c
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "26_kuruma"))   # 修繕の場面の整備工場（動画でも同じ背景）

R, BK, Y, NV = T.RED, T.BLACK, T.YELLOW, T.NAVY
HOUSE, APT = "bg48_clean_street", "bg57_tokyo_skyline"


def abc():
    T.type_a("27_mochiie_thumb_a.png", HOUSE, APT,
             ("despair_dramatic_kitten", 0.8, 300, 410, 330, False),
             [("talk_orange_white_sitting_cat", 1.0, 900, 410, 330, False), ("money_counting_orange_cat", 1.0, 1150, 410, 280, True)],
             "一生でかかるお金",
             [("持ち家", R), ("vs", BK), ("賃貸", NV)], [("90歳までで", BK), ("2370万差", R)], split=600, size=108)
    T.type_b("27_mochiie_thumb_b.png",
             [(HOUSE, [("stare_tabby_wide_eyes_cat", 0.6, 160, 470, 320, False)]),
              (APT, [("talk_orange_white_sitting_cat", 1.0, 160, 470, 330, False)]),
              ("bg26_car_inspection", [("despair_dramatic_kitten", 0.8, 160, 470, 330, False)]),
              ("bg02_room", [("sad_banana_cat_cry", 1.0, 160, 470, 330, False)])],
             [("txt", "頭金750万!?", 160, 60, 42, Y, -6), ("txt", "家賃 月13万", 480, 60, 42, Y, 4),
              ("txt", "修繕600万", 800, 60, 44, Y, -4), ("txt", "老後も家賃…", 1130, 60, 42, R, 6)],
             [("持ち家と賃貸", R)], [("一生でいくら違う？", NV)])
    T.type_c("27_mochiie_thumb_c.png", APT,
             [("surprise_big_pupils_cat", 1.0, 1040, 620, 470, False), ("money_counting_orange_cat", 1.0, 250, 640, 360, False)],
             "持ち家vs賃貸　90歳まで住むと…", "2370万差!?", zoom=1.05)


if __name__ == "__main__":
    abc()
