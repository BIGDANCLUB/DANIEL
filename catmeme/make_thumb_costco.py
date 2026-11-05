"""自堕落シリーズ #9 コストコのサムネ（11/5 ユーザー指定：いつものAパターン）。

python3 catmeme/make_thumb_costco.py → thumbs/jidaraku_09_costco_thumb_a.png
左：コストコ外観（届くまで店内 c03_entrance）・右：焼いた牛タン（余白に傾け字幕「これもう牛とのキスだろ」）
札：30代独身 ひとり買い物。字幕：休日の1人コストコは危険／牛タンの塊をどう食い尽くす？
"""
import os

from PIL import Image

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in (os.path.join("jidaraku", "09_costco"), "jidaraku"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK = T.RED, T.BLACK
NAME = "jidaraku_09_costco_thumb_a.png"


def left_photo():
    for n in ("c02_front", "c03_entrance"):   # 外観の写真が届いたら c02_front を優先
        try:
            S.bg_path(n) if hasattr(S, "bg_path") else None
            T.fill_photo(n, 10, 10)
            return n
        except Exception:
            continue


def main():
    T.type_a(NAME, left_photo(), "f_gyutan_yaki",
             ("surprise_big_pupils_cat", 1.0, 330, 410, 300, False),
             [("excited_hodomoe_city_cat", 1.0, 1150, 410, 300, False)],
             "30代独身　ひとり買い物",
             [("休日の", BK), ("1人コストコ", T.BLUE), ("は危険", BK)],
             [("牛タンの塊", R), ("をどう食い尽くす？", BK)], split=640, size=104)
    p = os.path.join(T.HERE, "thumbs", NAME)
    img = Image.open(p).convert("RGBA")
    T.scribble(img, "これもう牛とのキスだろ", 930, 78, 50, T.YELLOW, angle=6)
    T.save(img, NAME)


if __name__ == "__main__":
    main()
