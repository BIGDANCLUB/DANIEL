"""43本目（犬と猫 一生でいくらかかる？）のサムネ候補3つ（11/6）。41・42と同じ A・B・C の3パターン。

python3 catmeme/make_thumb_43.py → thumbs/43_petcost_thumb_a/b/c.png
"""
import glob
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

S.BGS += sorted(x for x in glob.glob(os.path.join(T.HERE, "backgrounds", "*")) if os.path.isdir(x))
R, BK, Y, NV = T.RED, T.BLACK, T.YELLOW, T.NAVY


def main():
    T.type_a("43_petcost_thumb_a.png", "bg59_sakura_park", "bg02_room",
             ("dance_cute_dog", 1.0, 300, 410, 320, False),
             [("meow_gray_white_kitten", 1.0, 900, 410, 300, False), ("money_counting_orange_cat", 1.0, 1150, 410, 280, True)],
             "一生でかかるお金",
             [("犬", R), ("vs", BK), ("猫", NV)], [("犬は", BK), ("約610万!?", R)], split=640, size=120)
    T.type_b("43_petcost_thumb_b.png",
             [("bg02_room", [("dance_cute_dog", 1.0, 160, 470, 320, False)]),
              ("bg28_jp_clinic", [("despair_dramatic_kitten", 0.8, 160, 470, 320, False)]),
              ("bg59_sakura_park", [("meow_gray_white_kitten", 1.0, 160, 470, 300, False)]),
              ("bg14_home_night", [("money_counting_orange_cat", 1.0, 160, 470, 320, False)])],
             [("txt", "犬は年41万", 160, 60, 40, Y, -6), ("txt", "猫の病院代1.5倍", 480, 60, 36, Y, 4),
              ("txt", "猫は16歳まで", 800, 60, 40, Y, -4), ("txt", "一生で610万!?", 1120, 60, 40, R, 6)],
             [("犬と猫", R)], [("一生でいくらかかる？", NV)])
    T.type_c("43_petcost_thumb_c.png", "bg02_room",
             [("surprise_big_pupils_cat", 1.0, 1040, 620, 470, False), ("dance_cute_dog", 1.0, 250, 640, 360, False)],
             "犬と猫　一生でかかるお金をくらべると", "犬は猫の約2倍!?", zoom=1.05)


if __name__ == "__main__":
    main()
