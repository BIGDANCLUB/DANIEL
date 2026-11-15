"""自堕落シリーズ #20 サンマルクのパン食べ放題のサムネ（11/15）。マック回 c2 と同じ形：
左に外観・右に料理・左上の帯・猫1匹を真ん中に大きく・黄色い枠に2行。

python3 catmeme/make_thumb_stmarc.py → thumbs/jidaraku_20_stmarc_thumb_c1〜c3.png
"""
import os

import make_thumb_long_ref as T
import make_thumb_mac as M
import make_thumb_short_ref as S

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "jidaraku", "20_stmarc"))
R, BK = T.RED, T.BLACK
TAG = "30代独身　ひとりパン食べ放題"


def main():
    M.center_cat("jidaraku_20_stmarc_thumb_c1.png", "surprise_big_pupils_cat",
                 [("焼きたてパン", R), ("食べ放題", BK)], [("パン10個", R), ("食べた結果…", BK)],
                 left="sm01_front", right="f_basket", tag=TAG)
    M.center_cat("jidaraku_20_stmarc_thumb_c2.png", "stare_big_eyes_tabby_kitten",
                 [("パンの", BK), ("回転ずし", R)], [("断れずに", BK), ("わんこそば状態", R)],
                 left="sm02_seat", right="f_basket", tag=TAG)
    M.center_cat("jidaraku_20_stmarc_thumb_c3.png", "showoff_gojo_cosplay_cat",
                 [("ガーリックパン", R), ("は", BK)], [("暴力の香り", R), ("だった", BK)],
                 left="sm01_front", right="f_basket", tag=TAG)


if __name__ == "__main__":
    main()


def line2_set():
    """11/15 ユーザー指定：c1 をもとに2行目だけ3案（d1〜d3）。"""
    l1 = [("焼きたてパン", R), ("食べ放題", BK)]
    for name, l2 in [("d1", [("元を取る", BK), ("つもりが…", R)]),
                     ("d2", [("店員さんに", BK), ("常連扱い", R), ("された", BK)]),
                     ("d3", [("パンの重み", R), ("で立てない", BK)])]:
        M.center_cat("jidaraku_20_stmarc_thumb_%s.png" % name, "surprise_big_pupils_cat", l1, l2,
                     left="sm01_front", right="f_basket", tag=TAG)
