"""35本目（タワマンvs一戸建て）と自堕落シリーズ #5（極楽湯）のサムネ候補3つずつ（11/1）。焼肉きんぐと同じ A・B・C の3パターン。

python3 catmeme/make_thumb_tower_goku.py → thumbs/35_tower_thumb_a/b/c.png・jidaraku_05_gokurakuyu_thumb_a/b/c.png
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in ("35_tower", os.path.join("jidaraku", "05_gokurakuyu"), os.path.join("jidaraku", "01_yakiniku")):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK, Y, NV = T.RED, T.BLACK, T.YELLOW, T.NAVY


def tower():
    T.type_a("35_tower_thumb_a.png", "bg35_tower", "bg35_house",
             ("cocky_dj_cat", 1.0, 300, 410, 330, False),
             [("happy_hamster_open_arms", 1.0, 900, 410, 320, False), ("money_counting_orange_cat", 1.0, 1150, 410, 280, True)],
             "同じ6500万円なのに",
             [("タワマン", R), ("vs", BK), ("一戸建て", NV)], [("住むだけで", BK), ("30年2000万差", R)], split=600, size=108)
    T.type_b("35_tower_thumb_b.png",
             [("bg35_tower_lobby", [("cocky_dj_cat", 1.0, 160, 470, 320, False)]),
              ("bg35_tower_parking", [("stare_tabby_wide_eyes_cat", 0.6, 160, 470, 330, False)]),
              ("bg35_house", [("happy_hamster_open_arms", 1.0, 160, 470, 330, False)]),
              ("bg35_suburb_street", [("despair_dramatic_kitten", 0.8, 160, 470, 330, False)])],
             [("txt", "管理費 月2.5万", 160, 60, 38, Y, -6), ("txt", "駐車場 月3万!?", 480, 60, 38, Y, 4),
              ("txt", "管理費0円!", 800, 60, 42, Y, -4), ("txt", "でも売るなら…", 1130, 60, 38, R, 6)],
             [("タワマンと一戸建て", R)], [("住むだけでいくら違う？", NV)])
    T.type_c("35_tower_thumb_c.png", "bg35_tower",
             [("surprise_big_pupils_cat", 1.0, 1040, 620, 470, False), ("money_counting_orange_cat", 1.0, 250, 640, 360, False)],
             "タワマン　住むだけでかかるお金", "年117万!?", zoom=1.05)


def goku():
    T.type_a("jidaraku_05_gokurakuyu_thumb_a.png", "g01_front", "g08_rest",
             ("stare_big_eyes_tabby_kitten", 0.6, 300, 410, 330, False),
             [("sad_looking_away_tabby", 1.0, 1100, 410, 300, True)],
             "30代独身の急な休み",
             [("平日に", BK), ("1人スーパー銭湯", R)], [("体はポカポカ", BK), ("心は寒い", R)], split=620, size=112)
    T.type_b("jidaraku_05_gokurakuyu_thumb_b.png",
             [("j01_room", [("think_chin_paw_orange_cat", 1.0, 160, 470, 300, False)]),
              ("g04_roten", [("happy_hamster_open_arms", 1.0, 160, 470, 300, False)]),
              ("g07_manga", [("sleepy_sleepy_cat", 1.0, 160, 470, 300, False)]),
              ("g08_rest", [("sad_banana_cat_cry", 1.0, 160, 470, 330, False)])],
             [("txt", "急に休み", 160, 60, 44, Y, -6), ("txt", "露天最高!", 480, 60, 44, Y, 4),
              ("txt", "漫画5巻", 800, 60, 44, Y, -4), ("txt", "カップルだらけ", 1130, 60, 38, R, 6)],
             [("30代独身　1人スーパー銭湯で", R)], [("情緒がこわれた結果", NV)])
    T.type_c("jidaraku_05_gokurakuyu_thumb_c.png", "g09_road",
             [("sad_banana_cat_cry", 1.0, 1060, 620, 460, False)],
             "30代独身　平日に1人スーパー銭湯", "心は寒い…", zoom=1.05)


if __name__ == "__main__":
    tower()
    goku()
