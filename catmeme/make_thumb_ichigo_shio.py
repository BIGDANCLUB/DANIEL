"""自堕落シリーズ #14 いちご狩り・#15 潮干狩りのサムネ（11/10）。いつものAパターンで文言3案ずつ。

python3 catmeme/make_thumb_ichigo_shio.py → thumbs/jidaraku_14_ichigo_thumb_a1〜a3.png・jidaraku_15_shiohigari_thumb_a1〜a3.png
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in (os.path.join("jidaraku", "14_ichigo"), os.path.join("jidaraku", "15_shiohigari"), "jidaraku"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK = T.RED, T.BLACK


def main():
    L = ("happy_hamster_open_arms", 1.0, 125, 410, 280, False)
    for name, left, right, rc, tag, l1, l2 in [
        ("jidaraku_14_ichigo_thumb_a1", "ic03_house", "f_strawberry", "sad_banana_cat_cry", "30代独身　ひとりいちご狩り",
         [("食べ放題", R), ("より", BK)], [("タダのいちご", R), ("がうまかった", BK)]),
        ("jidaraku_14_ichigo_thumb_a2", "ic01_farm", "f_rennyu", "huh_huh_cat", "30代独身　ひとりいちご狩り",
         [("……1名様", BK), ("ですねー", BK)], [("不審者扱いゲージ", R), ("爆上がり", BK)]),
        ("jidaraku_14_ichigo_thumb_a3", "ic03_house", "f_strawberry", "despair_dramatic_kitten", "30代独身　ひとりいちご狩り",
         [("目標", BK), ("50個", R), ("で挑んだ結果", BK)], [("小学生", R), ("に負けた", BK)]),
        ("jidaraku_15_shiohigari_thumb_a1", "sh02_flat", "f_sakamushi", "sad_banana_cat_cry", "30代独身　ひとり潮干狩り",
         [("独り身の", BK), ("むなしさ", T.BLUE)], [("酒蒸し", R), ("が洗い流す", BK)]),
        ("jidaraku_15_shiohigari_thumb_a2", "sh02_flat", "f_net", "showoff_gojo_cosplay_cat", "30代独身　ひとり潮干狩り",
         [("プロ級", R), ("の腕前で", BK)], [("袋が", BK), ("パンパン!?", R)]),
        ("jidaraku_15_shiohigari_thumb_a3", "sh01_beach", "f_asari", "rizz_cat_rizz", "30代独身　ひとり潮干狩り",
         [("あさりを", BK), ("おなかいっぱい", R)], [("取りすぎた", R), ("結果…", BK)]),
    ]:
        T.type_a(name + ".png", left, right, L, [(rc, 1.0, 1170, 410, 300, False)], tag, l1, l2, split=640, size=108)


if __name__ == "__main__":
    main()
