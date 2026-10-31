"""31本目（エスコン）と自堕落シリーズ #4（スシロー）のサムネ候補3つずつ（10/31）。焼肉きんぐと同じ A・B・C の3パターン。

python3 catmeme/make_thumb_escon_sushiro.py → thumbs/31_escon_thumb_a/b/c.png・jidaraku_04_sushiro_thumb_a/b/c.png
"""
import os

import make_thumb_jidaraku as JT
import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in ("31_escon_photos", "31_escon", os.path.join("jidaraku", "04_sushiro"), os.path.join("jidaraku", "01_yakiniku")):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK, Y, NV = T.RED, T.BLACK, T.YELLOW, T.NAVY

# 背景が透明な料理の写真は白で埋めた版を使う（そのままだと黒くなる）
import tempfile
from PIL import Image
_W = tempfile.mkdtemp()
for n in ("f_ebi_mala", "f_kanimiso"):
    src = Image.open(S.bg_path(n)).convert("RGBA")
    im = Image.new("RGB", src.size, (255, 255, 255))
    im.paste(src, (0, 0), src)
    im.save(os.path.join(_W, n + ".png"))
S.BGS.insert(0, _W)


def escon():
    T.type_a("31_escon_thumb_a.png", "bg31_dome_inside", "bg31_escon_outside",
             ("despair_dramatic_kitten", 0.8, 280, 410, 330, False),
             [("happy_hamster_open_arms", 1.0, 900, 410, 330, False), ("money_counting_orange_cat", 1.0, 1150, 410, 280, True)],
             "札幌ドーム→エスコン",
             [("家賃", BK), ("年20億", R), ("が高すぎて", BK)], [("球場ごと", BK), ("建てた球団", R)], split=600, size=110)
    T.type_b("31_escon_thumb_b.png",
             [("bg31_dome_inside", [("money_counting_orange_cat", 1.0, 160, 470, 320, False)]),
              ("bg31_city_meeting", [("rage_talking_cat", 1.0, 160, 470, 330, False)]),
              ("bg31_construction", [("stare_tabby_wide_eyes_cat", 0.6, 160, 470, 330, False)]),
              ("bg31_escon_inside", [("excited_hodomoe_city_cat", 1.0, 160, 470, 330, False)])],
             [("txt", "家賃20億!?", 160, 60, 42, Y, -6), ("txt", "何度頼んでも…", 480, 60, 38, Y, 4),
              ("txt", "600億で建設", 800, 60, 40, Y, -4), ("txt", "温泉つき!", 1130, 60, 44, R, 6)],
             [("年20億の家賃収入最高！", R)], [("⇒交渉にも応じなかった結果…", NV)])   # 10/31 ユーザー指定
    T.type_c("31_escon_thumb_c.png", "bg31_escon_inside",
             [("surprise_big_pupils_cat", 1.0, 1040, 620, 470, False), ("money_counting_orange_cat", 1.0, 250, 640, 360, False)],
             "家賃が高すぎて球場を建てた球団", "600億!?", zoom=1.05)


def sushiro():
    T.type_a("jidaraku_04_sushiro_thumb_a.png", "s01_store_front", "f_ebi_mala",
             ("stare_big_eyes_tabby_kitten", 0.6, 300, 410, 330, False),
             [("surprise_big_pupils_cat", 1.0, 1100, 410, 300, True)],
             "30代独身の休日",
             [("休日に", BK), ("1人スシロー", R)], [("寿司と", BK), ("異種格闘技", R), ("した結果", BK)], split=620, size=118)   # 10/31 ユーザー指定
    T.type_b("jidaraku_04_sushiro_thumb_b.png",
             [("j01_room", [("angry_aiming_cat", 1.0, 160, 470, 300, False)]),
              ("f_kanimiso", [("happy_hamster_open_arms", 1.0, 160, 470, 300, False)]),
              ("f_ebi_mala", [("confused_i_dont_know_cat", 1.0, 160, 470, 300, False)]),
              ("s02_inside", [("despair_dramatic_kitten", 0.8, 160, 470, 330, False)])],
             [("txt", "朝メシ抜き", 160, 60, 42, Y, -6), ("txt", "かにみそ最強", 480, 60, 40, Y, 4),
              ("txt", "これ寿司…？", 800, 60, 42, Y, -4), ("txt", "8000円…", 1130, 60, 44, R, 6)],
             [("30代独身　1人スシローで", R)], [("寿司と戦争した結果", NV)])
    T.type_c("jidaraku_04_sushiro_thumb_c.png", "s02_inside",
             [("stare_big_eyes_tabby_kitten", 0.6, 1060, 600, 460, False)],
             "30代独身　休日に1人スシロー", "8000円…だと…", zoom=1.05)


if __name__ == "__main__":
    escon()
    sushiro()
