"""自堕落シリーズ #21 ケンタッキー食べ放題のサムネ（11/16）。マック回 c2・サンマルク回と同じ形：
左に入口・右にチキン・左上の帯・猫1匹を真ん中に大きく・黄色い枠に2行。

python3 catmeme/make_thumb_kfc.py → thumbs/jidaraku_21_kfc_thumb_c1〜c3.png
"""
import os

import make_thumb_long_ref as T
import make_thumb_mac as M
import make_thumb_short_ref as S

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "jidaraku", "21_kfc"))
R, BK = T.RED, T.BLACK
TAG = "30代独身　ひとりチキン食べ放題"


def main():
    M.center_cat("jidaraku_21_kfc_thumb_c1.png", "surprise_big_pupils_cat",
                 [("チキン食べ放題", R), ("80分", BK)], [("元を取るまで", BK), ("食べた結果…", R)],
                 left="kf01_front", right="f_plate", tag=TAG)
    M.center_cat("jidaraku_21_kfc_thumb_c2.png", "stare_big_eyes_tabby_kitten",
                 [("チキン食べ放題", R), ("で", BK)], [("衣だけ", R), ("食べたくなった", BK)],
                 left="kf02_seat", right="f_plate", tag=TAG)
    M.center_cat("jidaraku_21_kfc_thumb_c3.png", "sad_banana_cat_cry",
                 [("元は取れた", BK)], [("胃袋の元", R), ("は取れていない", BK)],
                 left="kf01_front", right="f_plate", tag=TAG)


if __name__ == "__main__":
    main()


def final():
    """11/16 ユーザー指定：c2 をもとに文字を「ケンタッキー食べ放題／衣だけのメニューが欲しい！」に。"""
    M.center_cat("jidaraku_21_kfc_thumb_final.png", "stare_big_eyes_tabby_kitten",
                 [("ケンタッキー", R), ("食べ放題", BK)], [("衣だけ", R), ("のメニューが欲しい！", BK)],
                 left="kf02_seat", right="f_plate", tag=TAG)


def final2():
    """11/16 ユーザー指定：c3 をもとに右の写真をチキン単品（f_chicken）に。"""
    M.center_cat("jidaraku_21_kfc_thumb_final2.png", "sad_banana_cat_cry",
                 [("元は取れた", BK)], [("胃袋の元", R), ("は取れていない", BK)],
                 left="kf01_front", right="f_chicken", tag=TAG)
