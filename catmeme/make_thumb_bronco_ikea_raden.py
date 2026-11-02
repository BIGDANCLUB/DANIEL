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
             "30代独身　一人メシ",   # 11/2 ユーザー指定
             [("ブロンコビリー", R), ("とは", BK)], [("⇒", BK), ("野菜", R), ("を食べに行く場所", BK)], split=620, size=112)
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


def raden_a2():
    """11/2 ユーザー指定：Aをもとに「Vtuberに154万円で依頼／⇒23倍の費用対効果!?」＋らでんさんの画像（前にもらった画像）。"""
    from PIL import Image
    T.type_a("39_raden_thumb_a.png", "bg39_museum", "bg39_rodin",
             ("money_counting_orange_cat", 1.0, 230, 410, 300, False),
             [("surprise_big_pupils_cat", 1.0, 1090, 410, 300, True)],
             "VTuberの美術館ガイド",
             [("県がVtuberに", BK), ("154万円", R), ("で依頼", BK)], [("⇒", BK), ("23倍", R), ("の費用対効果!?", BK)], split=640, size=104)
    p = os.path.join(T.HERE, "thumbs", "39_raden_thumb_a.png")
    img = Image.open(p).convert("RGBA")
    r = Image.open(os.path.join(T.HERE, "parts", "39_raden", "p_raden.png")).convert("RGBA")
    k = 400 / r.height
    r = r.resize((int(r.width * k), 400), Image.LANCZOS)
    img.alpha_composite(r, ((T.W - r.width) // 2, 6))
    # 「VTuberの美術館ガイド」の札が画像に隠れないよう、札をもう一度いちばん上に重ねる（11/2 ユーザー指摘）
    from PIL import ImageDraw
    t = T.runs([("VTuberの美術館ガイド", (R, T.WHITE))], 52, 2, 640)
    box = Image.new("RGBA", (t.width + 50, t.height + 34), T.WHITE + (255,))
    ImageDraw.Draw(box).rectangle((0, 0, box.width - 1, box.height - 1), outline=T.BLACK, width=5)
    box.alpha_composite(t, (25, 17))
    box = box.rotate(2, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(box, (14, 410 - box.height + 40))
    img.convert("RGB").save(p)
    print("->", p)


if __name__ == "__main__":
    bronco()
    ikea()
    raden()
    raden_a2()
