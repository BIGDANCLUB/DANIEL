"""自堕落シリーズ #11 ゴンチャのサムネ（11/8）。いつものAパターンで文言3案。

python3 catmeme/make_thumb_gongcha.py → thumbs/jidaraku_11_gongcha_thumb_a1/a2/a3.png
左：赤い外観・右：グラスのミルクティー（タピオカ）
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in (os.path.join("jidaraku", "11_gongcha"), "jidaraku"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK = T.RED, T.BLACK


def main():
    L = ("scream_phone_orange_cat", 1.0, 150, 410, 260, False)
    RC = [("huh_huh_cat", 1.0, 1150, 410, 300, False)]
    for name, tag, l1, l2 in [
        ("a1", "30代独身　タピオカデビュー", [("氷……", BK), ("あります！", R)], [("ゴンチャ", T.BLUE), ("で大パニック", BK)]),
        ("a2", "30代独身　初めてのゴンチャ", [("注文が", BK), ("むずかしすぎる", R)], [("甘さを", BK), ("全部で!?", R)]),
        ("a3", "30代独身　ひとりゴンチャ", [("タピオカを", BK), ("ひとつ！", R)], [("それ", BK), ("トッピングです", R)]),
    ]:
        T.type_a("jidaraku_11_gongcha_thumb_%s.png" % name, "g01_front", "f_milktea", L, RC, tag, l1, l2, split=640, size=108)


if __name__ == "__main__":
    main()


def final():
    """11/8 ユーザー指定：a3 をもとに文字を会話の形に・猫を少し大きくして両はしへ。"""
    L = ("scream_phone_orange_cat", 1.0, 125, 410, 300, False)
    RC = [("huh_huh_cat", 1.0, 1185, 410, 340, False)]
    T.type_a("jidaraku_11_gongcha_thumb_final.png", "g01_front", "f_milktea", L, RC, "30代独身　ゴンチャデビュー",
             [("ワイ「", BK), ("タピオカを1つ！", R), ("」", BK)], [("店員「", BK), ("それトッピングだよ", R), ("」", BK)],
             split=640, size=104)
