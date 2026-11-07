"""30本目（大谷翔平 メジャー直行宣言から日本ハム入団まで）のサムネ候補3つ（10/30）。横 1280x720。
焼肉きんぐ（make_thumb_jidaraku.yakiniku_abc）と同じ A・B・C の3パターン。背景はユーザー提供の bg30_*。

python3 catmeme/make_thumb_ohtani.py → thumbs/30_ohtani_thumb_a.png / _b / _c
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "30_ohtani"))
R, BK, Y = T.RED, T.BLACK, T.YELLOW
OHTANI = "talk_orange_white_sitting_cat"


def abc():
    T.type_a("30_ohtani_thumb_a.png", "bg30_press_room", "bg30_draft_hall",
             (OHTANI, 0.6, 260, 410, 330, False),
             [("stare_tabby_wide_eyes_cat", 0.6, 860, 410, 300, False), ("scream_phone_orange_cat", 1.0, 1130, 410, 300, True)],
             "2012年ドラフトの舞台裏",
             [("メジャー直行宣言の", BK), ("大谷翔平", R)], [("まさかの", BK), ("強行指名", R)], split=560, size=118)
    T.type_b("30_ohtani_thumb_b.png",
             [("bg30_summer_stadium", [("punch_boxing_white_cat", 1.0, 160, 470, 320, False)]),
              ("bg30_press_room", [(OHTANI, 0.6, 160, 470, 330, False)]),
              ("bg30_draft_hall", [("surprise_big_pupils_cat", 1.0, 160, 470, 330, False)]),
              ("bg30_negotiation_room", [("think_chin_paw_orange_cat", 1.0, 160, 470, 330, False)])],
             [("txt", "160キロ!?", 160, 60, 44, Y, -6), ("txt", "メジャー行きます", 480, 60, 38, Y, 4),
              ("txt", "1位指名!?", 800, 60, 44, Y, -4), ("txt", "二刀流で!", 1130, 60, 44, R, 6)],
             [("大谷翔平が日本ハムに", R)], [("入るまでの全真相", T.NAVY)])
    T.type_c("30_ohtani_thumb_c.png", "bg30_draft_hall",
             [("surprise_big_pupils_cat", 1.0, 1040, 620, 470, False), (OHTANI, 0.6, 250, 640, 380, False)],
             "大谷翔平　メジャー直行宣言からの…", "強行指名!?", zoom=1.05)


if __name__ == "__main__":
    abc()
