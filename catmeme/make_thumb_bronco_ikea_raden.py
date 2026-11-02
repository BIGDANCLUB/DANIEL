"""今日（11/2）作った長尺のサムネ候補3つずつ：自堕落 #6 ブロンコビリー・#7 IKEA・39本目（VTuberの音声ガイド）。焼肉きんぐと同じ A・B・C の3パターン。

python3 catmeme/make_thumb_bronco_ikea_raden.py → thumbs/<名前>_thumb_a/b/c.png
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in ("39_raden", os.path.join("jidaraku", "06_bronco"), os.path.join("jidaraku", "07_ikea"),
          os.path.join("jidaraku", "05_gokurakuyu"), os.path.join("jidaraku", "01_yakiniku"), "jidaraku"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK, Y, NV = T.RED, T.BLACK, T.YELLOW, T.NAVY


def bronco():
    T.type_a("jidaraku_06_bronco_thumb_a.png", "b05_salad_bar", "b04_table",
             ("happy_hamster_open_arms", 1.0, 300, 410, 330, False),
             [("eat_crunchy_cat_luna", 1.0, 1100, 410, 320, True)],
             "30代独身　1週間カップ麺",
             [("ステーキハウスに", BK), ("野菜を食べに", R)], [("行った結果", BK), ("肉が美味かった", R)], split=620, size=104)
    T.type_b("jidaraku_06_bronco_thumb_b.png",
             [("bg25_office_desk", [("despair_dramatic_kitten", 0.8, 160, 470, 320, False)]),
              ("b05_salad_bar", [("happy_hamster_open_arms", 1.0, 160, 470, 300, False)]),
              ("b04_table", [("eat_crunchy_cat_luna", 1.0, 160, 470, 300, False)]),
              ("b07_room_night", [("sad_looking_away_tabby", 1.0, 160, 470, 300, False)])],
             [("txt", "緑を1週間見てない", 160, 60, 34, Y, -6), ("txt", "緑黄色の森!", 480, 60, 42, Y, 4),
              ("txt", "ごはん3杯", 800, 60, 44, Y, -4), ("txt", "冷蔵庫が砂漠", 1130, 60, 40, R, 6)],
             [("30代独身　1人ブロンコビリーで", R)], [("野菜を食べまくった結果", NV)])
    T.type_c("jidaraku_06_bronco_thumb_c.png", "b02_front",
             [("excited_hodomoe_city_cat", 1.0, 1060, 620, 460, False)],
             "野菜を食べにステーキハウスへ", "肉が美味かった", zoom=1.05)


def ikea():
    T.type_a("jidaraku_07_ikea_thumb_a.png", "i01_front", "i02_living",
             ("stare_big_eyes_tabby_kitten", 0.6, 300, 410, 330, False),
             [("sad_banana_cat_cry", 1.0, 1100, 410, 320, True)],
             "30代独身　丁寧な暮らしがしたい",
             [("休日に", BK), ("1人IKEA", R)], [("3時間歩いて", BK), ("買えたのは1つ", R)], split=620, size=112)
    T.type_b("jidaraku_07_ikea_thumb_b.png",
             [("i09_arrow", [("think_bike_front_seat_cat", 1.0, 160, 470, 300, False)]),
              ("i06_restaurant", [("eat_pop_cat", 1.0, 160, 470, 300, False)]),
              ("i05_market", [("despair_dramatic_kitten", 0.8, 160, 470, 320, False)]),
              ("i06_restaurant", [("sad_banana_cat_cry", 1.0, 160, 470, 330, False)])],
             [("txt", "人生にも矢印を", 160, 60, 38, Y, -6), ("txt", "肉にジャム!?", 480, 60, 42, Y, 4),
              ("txt", "何も買えない", 800, 60, 40, Y, -4), ("txt", "50円で泣く", 1130, 60, 42, R, 6)],
             [("30代独身　休日に1人IKEAで", R)], [("丁寧な暮らしを目指した結果", NV)])
    T.type_c("jidaraku_07_ikea_thumb_c.png", "i06_restaurant",
             [("sad_banana_cat_cry", 1.0, 1060, 620, 460, False)],
             "独り身でも受け入れてくれる場所", "IKEAはいい所", zoom=1.05)


def raden():
    T.type_a("39_raden_thumb_a.png", "bg39_museum", "bg39_rodin",
             ("money_counting_orange_cat", 1.0, 300, 410, 320, False),
             [("surprise_big_pupils_cat", 1.0, 1100, 410, 320, True)],
             "VTuberの美術館ガイド",
             [("費用154万円", BK), ("→", BK)], [("地域で3600万円", R), ("約23倍!?", R)], split=620, size=108)
    T.type_b("39_raden_thumb_b.png",
             [("bg97_tabloid_desk", [("stare_tabby_wide_eyes_cat", 0.6, 160, 470, 330, False)]),
              ("bg39_rodin", [("read_book_orange_kitten", 1.0, 160, 470, 300, False)]),
              ("bg39_lobby", [("dance_three_kittens", 1.0, 160, 470, 300, False)]),
              ("bg87_refund_money", [("money_counting_orange_cat", 1.0, 160, 470, 300, False)])],
             [("txt", "県の資料に154万円", 160, 60, 34, Y, -6), ("txt", "推しの声で鑑賞", 480, 60, 38, Y, 4),
              ("txt", "3人に1人が推しで来館", 800, 60, 30, Y, -4), ("txt", "3600万円!?", 1130, 60, 42, R, 6)],
             [("VTuberに県のお仕事を頼んだら", R)], [("費用と効果がすごかった", NV)])
    T.type_c("39_raden_thumb_c.png", "bg39_museum",
             [("surprise_big_pupils_cat", 1.0, 1040, 620, 470, False), ("money_counting_orange_cat", 1.0, 250, 640, 360, False)],
             "154万円の音声ガイドが生んだお金", "約23倍!?", zoom=1.05)


if __name__ == "__main__":
    bronco()
    ikea()
    raden()
