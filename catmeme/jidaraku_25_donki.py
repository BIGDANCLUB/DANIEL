"""自堕落シリーズ #25：30代独身、休日の夜に予定がないので1人でドンキへ（11/21 ユーザー指定）。約5分でよい（11/21：8分こえなくてよい）。

python3 catmeme/jidaraku_25_donki.py → out/jidaraku_25_donki.mp4
- 11/21 ベンチマーク比較（research/bench_jidaraku_20261121.md）に合わせた作り：
  身近な店・短いタイトルに「きっかけ」・ささやかな幸せで終わる・自虐少なめ・うんちくなし・商品をひとつずつ楽しむ
- 流れ：休日の夜、予定なし・歯ブラシが切れた → 入店（ダンジョン） → お菓子 → 冬の着る毛布 → 便利グッズ（冬にハンディファン）
  → 冷凍からあげとお酒 → かごいっぱい・レジ → 家で着る毛布で宅飲み → オチ：歯ブラシを買い忘れ
- 写真はユーザー提供（11/21）backgrounds/jidaraku/25_donki。f_* はかごの写真から切り出し。入口の曲は流さない（文字で触れるだけ）
- 11/17 からのルール：場面転換ゆっくり・字幕は1行12字・最大2行・2.5〜3秒・職場の回想なし
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "25_donki"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku")]
ROOM_N, STREET_N = "j07_room_night", "bg51_night_street"
FRONT, AISLE, SNACK, FROZEN, GADGET, BASKET = "dk01_front", "dk02_aisle", "dk03_snack", "dk04_frozen_sake", "dk05_gadget", "dk06_basket"
BLANKET, KARAAGE, FAN, CHUHAI, CHIPS = "f_blanket", "f_karaage", "f_gadget", "f_chuhai", "f_snack"
J.HOLD = 6
J.LOOPS = 1
J.TEMPO_K = 1.3
J.SUB_SEC = (2.5, 3.0)
J.SUB_STYLE = "glow"
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 休日の夜 ----
        s(ROOM_N, "stare_lying_tabby_cat", "休日の夜", bgm={"file": LOFI, "gain": -12}),
        s(ROOM_N, "blank_black_cat_zoning_out", "予定は\nとくにない"),
        s(ROOM_N, "calm_black_face_sheep", "昼まで寝て\n動画を見ていたら\nもう夜"),
        s(ROOM_N, "think_chin_paw_orange_cat", "そういえば"),
        s(ROOM_N, "surprise_big_pupils_cat", "歯ブラシが\nボロボロだった", se="pi"),
        s(ROOM_N, "think_chin_paw_orange_cat", "この時間でも\nあいている店"),
        s(ROOM_N, "angry_aiming_cat", "ドンキ\n行くか"),
        s(STREET_N, "walk_approaching_orange_cat", "上着をはおって\n夜の道を歩く"),
        s(STREET_N, "sad_looking_away_tabby", "風が冷たい"),
        s(STREET_N, "stare_tabby_wide_eyes_cat", "遠くに\n黄色い光が見えてきた"),
        s(FRONT, "showoff_gojo_cosplay_cat", "ドン・キホーテ", se="gong_dora_jaan"),
        s(FRONT, "surprise_big_pupils_cat", "夜なのに\nまぶしい"),
        s(FRONT, "smug_squint_bicolor_cat", "ペンギンも\nサンタの帽子"),
        s(FRONT, "rizz_cat_rizz", "もう\nクリスマスの準備か"),
        s(FRONT, "angry_shooting_cat", "目的は\n歯ブラシだけ"),
        s(FRONT, "work_typing_cat", "5分で帰る"),
        # ---- 入店 ----
        s(AISLE, "excited_hodomoe_city_cat", "入口に入ると\nあの曲が流れている", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(AISLE, "dance_tabby_standing_cat", "なぜか\nワクワクしてくる"),
        s(AISLE, "stare_tabby_wide_eyes_cat", "天井まで\nぎっしりの商品"),
        s(AISLE, "peek_what_happen_cat", "通路は\n迷路みたい"),
        s(AISLE, "think_chin_paw_orange_cat", "これは\nダンジョンだ"),
        s(AISLE, "confused_i_dont_know_cat", "歯ブラシは\nどこだろう"),
        s(AISLE, "walk_white_duck", "とりあえず\n奥へ進む"),
        # ---- お菓子 ----
        s(SNACK, "surprise_big_pupils_cat", "お菓子の\nコーナーに出た", se="pikon", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(SNACK, "stare_big_eyes_tabby_kitten", "見たことない\nお菓子ばかり"),
        s(SNACK, "happy_hamster_open_arms", "外国のお菓子が\nずらり"),
        s(SNACK, "read_book_orange_kitten", "手書きのポップが\nいちいち面白い"),
        s(SNACK, "think_chin_paw_orange_cat", "これは\n今しか\n買えないかも", item=CHIPS),
        s(SNACK, "smug_squint_bicolor_cat", "ポテチと\nスナックを\nかごへ", item=CHIPS, se="eat_paku"),
        s(SNACK, "rizz_cat_rizz", "グミも\nついでに", item=CHIPS),
        s(SNACK, "calm_black_face_sheep", "歯ブラシの前に\n歯に悪いものを\n買っている"),
        # ---- 冬のコーナー ----
        s(AISLE, "stare_tabby_wide_eyes_cat", "さらに奥へ", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(AISLE, "surprise_big_pupils_cat", "冬のコーナーだ", item=BLANKET, se="shine_kiraan_maou"),
        s(AISLE, "peek_what_happen_cat", "ふわふわの\n着る毛布", item=BLANKET),
        s(AISLE, "think_chin_paw_orange_cat", "前から\n気になっていた", item=BLANKET),
        s(AISLE, "work_typing_cat", "ちょっと\nさわってみる", item=BLANKET),
        s(AISLE, "realize_wet_cat_stare", "…やわらかい", item=BLANKET),
        s(AISLE, "happy_girlfriend_dance_cat", "これを着て\nこたつに入ったら", item=BLANKET),
        s(AISLE, "joy_happy_happy_happy_cat", "最強では？", item=BLANKET),
        s(AISLE, "sad_looking_away_tabby", "うちに\nこたつはない", item=BLANKET),
        s(AISLE, "smug_squint_bicolor_cat", "でも\n毛布はある", item=BLANKET),
        s(AISLE, "rizz_cat_rizz", "冬の夜が\n変わる気がする", item=BLANKET),
        s(AISLE, "angry_aiming_cat", "かごへ", item=BLANKET, se="pikon"),
        # ---- 便利グッズ ----
        s(GADGET, "stare_tabby_wide_eyes_cat", "便利グッズの\nコーナー"),
        s(GADGET, "read_book_orange_kitten", "ゆでたまごが\nかんたんに\nむける道具"),
        s(GADGET, "think_chin_paw_orange_cat", "ゆでたまごは\nめったに作らない"),
        s(GADGET, "peek_what_happen_cat", "スマホホルダー\nマッサージ機"),
        s(GADGET, "money_counting_orange_cat", "ぜんぶ\n安く見えてくる"),
        s(GADGET, "surprise_big_pupils_cat", "あ\nハンディファン", item=FAN, se="pi"),
        s(GADGET, "think_chin_paw_orange_cat", "いまは\n11月", item=FAN),
        s(GADGET, "smug_squint_bicolor_cat", "でも\n暖房のききすぎた\n部屋で使える", item=FAN),
        s(GADGET, "rizz_cat_rizz", "たぶん", item=FAN),
        s(GADGET, "happy_hamster_open_arms", "かごへ", item=FAN, se="pikon"),
        # ---- 冷凍食品とお酒 ----
        s(FROZEN, "stare_tabby_wide_eyes_cat", "冷凍食品と\nお酒のコーナー", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(FROZEN, "think_chin_paw_orange_cat", "ここまで来たら"),
        s(FROZEN, "angry_aiming_cat", "今夜は\n宅飲みにしよう"),
        s(FROZEN, "surprise_big_pupils_cat", "大容量の\nからあげ", item=KARAAGE),
        s(FROZEN, "eat_pop_cat", "レンジで\nすぐ食べられる", item=KARAAGE),
        s(FROZEN, "smug_squint_bicolor_cat", "これは\n明日の分にもなる", item=KARAAGE),
        s(FROZEN, "happy_hamster_open_arms", "チューハイは\nレモンとピーチ", item=CHUHAI),
        s(FROZEN, "rizz_cat_rizz", "1本100円ちょっと", item=CHUHAI),
        s(FROZEN, "money_counting_orange_cat", "スーパーより\n安いかもしれない", item=CHUHAI),
        s(FROZEN, "work_typing_cat", "2本\nかごへ", item=CHUHAI, se="pikon"),
        # ---- かごいっぱい・レジ ----
        s(BASKET, "stare_tabby_wide_eyes_cat", "ふと\nかごを見る", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(BASKET, "surprise_big_pupils_cat", "いっぱい", se="explosion_chudoon"),
        s(BASKET, "read_book_orange_kitten", "お菓子\n着る毛布\nハンディファン"),
        s(BASKET, "read_book_orange_kitten", "からあげと\nチューハイ"),
        s(BASKET, "confused_i_dont_know_cat", "5分で帰る\nはずだった"),
        s(BASKET, "think_chin_paw_orange_cat", "時計を見ると\n1時間たっていた"),
        s(AISLE, "work_typing_cat", "レジにならぶ"),
        s(AISLE, "stare_interviewer_cat", "お会計は\nこちらになります", se="price_display"),
        s(AISLE, "scream_standing_marmot", "…え\nこんなに？", se="explosion_chudoon"),
        s(AISLE, "calm_black_face_sheep", "でも\nひとつひとつは\n安かった"),
        s(AISLE, "happy_hamster_open_arms", "まあいっか"),
        s(AISLE, "rizz_cat_rizz", "楽しかったし"),
        # ---- 家で ----
        s(STREET_N, "walk_approaching_orange_cat", "大きな袋を下げて\n夜の道を帰る", bgm={"file": JITAKU, "gain": -10, "fade": 1.0}),
        s(STREET_N, "smug_squint_bicolor_cat", "行きより\n足取りが軽い"),
        s(ROOM_N, "dance_tabby_standing_cat", "帰ってすぐ\n着る毛布を着る", item=BLANKET),
        s(ROOM_N, "realize_wet_cat_stare", "…あったかい", item=BLANKET),
        s(ROOM_N, "happy_girlfriend_dance_cat", "全身が\nふわふわに\nつつまれる", item=BLANKET),
        s(ROOM_N, "eat_pop_cat", "からあげを\nレンジでチン", item=KARAAGE, se="pinpon_notice"),
        s(ROOM_N, "happy_hamster_open_arms", "チューハイを\nあける", item=CHUHAI, se="drink_gulp_gokugoku_thirsty_chug"),
        s(ROOM_N, "eat_crunchy_cat_luna", "からあげ\nうまい", item=KARAAGE),
        s(ROOM_N, "eat_chips_cat", "知らない味の\nポテチも\n意外とうまい", item=CHIPS),
        s(ROOM_N, "smug_squint_bicolor_cat", "暖房がききすぎてきた"),
        s(ROOM_N, "rizz_cat_rizz", "ハンディファンの\n出番だ", item=FAN, se="pikon"),
        s(ROOM_N, "joy_happy_happy_happy_cat", "買ってよかった", item=FAN),
        s(ROOM_N, "stare_lying_tabby_cat", "予定のない\n休日の夜"),
        s(ROOM_N, "happy_hamster_open_arms", "でも\nなんだか\n満たされている"),
        s(ROOM_N, "rizz_cat_rizz", "ドンキは\n大人の遊園地だ"),
        # ---- オチ ----
        s(ROOM_N, "sleepy_sleepy_cat", "そろそろ寝よう"),
        s(ROOM_N, "work_typing_cat", "歯をみがこう"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "…"),
        s(ROOM_N, "surprise_big_pupils_cat", "歯ブラシ\n買ってない", se="explosion_chudoon"),
        s(ROOM_N, "despair_dramatic_kitten", "いちばんの\n目的だった"),
        s(ROOM_N, "think_chin_paw_orange_cat", "でも"),
        s(ROOM_N, "smug_squint_bicolor_cat", "また\nドンキに行く\n理由ができた"),
        s(ROOM_N, "excited_hodomoe_city_cat", "来週の休日も\n予定は決まった", se="pikon", dur=3.8),
        J.end_card(),
    ]


def place(cs):
    J.diversify(cs)
    J.prefer_long(cs)
    J.reflow(cs)
    J.auto_tempo(cs)
    for c in cs:
        if c.get("text"):
            c["text"] = c["text"].replace("「", "").replace("」", "")
    return cs


if __name__ == "__main__":
    cs = place(cuts())
    if os.environ.get("LEN"):
        print(len(cs), round(sum(c["dur"] for c in cs), 1))
    else:
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_25_donki.mp4"), os.path.join(J.HERE, "out", "jidaraku_25_donki_preview"))
