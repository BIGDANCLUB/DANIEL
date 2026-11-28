"""自堕落シリーズ #26：30代独身、給料日に1人で焼肉ライク（11/22 ユーザー指定）。約5分でよい。ドンキ回（#25）と同じ作り。

python3 catmeme/jidaraku_26_yakinikulike.py → out/jidaraku_26_yakinikulike.mp4
- 11/21 ベンチマーク比較に合わせた作り：身近な店・短いタイトルに「きっかけ」・ささやかな幸せで終わる・自虐少なめ・うんちくなし
- 流れ：給料日の帰り道「自分にごほうび」→ 店に着く → 1人1台のロースター席 → タッチパネルで注文 → 最初の1枚・ご飯にワンバウンド →
  タレを試す → 牛タンを追加 → ご飯おかわり → スープで一息 → 帰り道「来月もがんばろう」→ 家で満腹のまま寝る
- 写真はユーザー提供（11/22）backgrounds/jidaraku/26_yakinikulike。焼いている写真は右下の透かし文字を切り落とした
- ご飯の写真：吉野家の丼（f_rice）は店のマークが入っているので使わず、焼肉ライクのセット写真（ご飯入り）で代用
- おかわり無料かどうか・値段は言い切らない（看板に見える「580円〜」だけ）
- 11/17 からのルール：場面転換ゆっくり・字幕は1行12字・最大2行・2.5〜3秒・職場の回想なし
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "26_yakinikulike"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku")]
ROOM_N, STREET_N = "j07_room_night", "bg51_night_street"
FRONT, SEAT = "yl01_front", "yl02_seat"
SET, GRILL, TAN = "f_set", "f_grill", "f_tan"
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
        # ---- 給料日の帰り道 ----
        s(STREET_N, "stare_lying_tabby_cat", "金曜の夜", bgm={"file": LOFI, "gain": -12}),
        s(STREET_N, "money_counting_orange_cat", "今日は給料日"),
        s(STREET_N, "think_chin_paw_orange_cat", "1か月\nよくがんばった"),
        s(STREET_N, "smug_squint_bicolor_cat", "がんばった自分に\nごほうびをあげたい"),
        s(STREET_N, "think_chin_paw_orange_cat", "ごほうびといえば"),
        s(STREET_N, "angry_aiming_cat", "肉だ"),
        s(STREET_N, "calm_black_face_sheep", "でも\n焼肉は\nひとりだと入りにくい"),
        s(STREET_N, "stare_tabby_wide_eyes_cat", "そこに見えてきた\n明るい看板", se="pi"),
        s(FRONT, "showoff_gojo_cosplay_cat", "焼肉ライク", se="gong_dora_jaan"),
        s(FRONT, "surprise_big_pupils_cat", "ひとり焼肉の\nお店だ"),
        s(FRONT, "read_book_orange_kitten", "焼肉セット\n580円から"),
        s(FRONT, "happy_hamster_open_arms", "財布にもやさしい"),
        s(FRONT, "rizz_cat_rizz", "今日は\nここにしよう"),
        # ---- 席へ ----
        s(SEAT, "work_typing_cat", "カウンター席に\n案内される", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(SEAT, "stare_big_eyes_tabby_kitten", "目の前に\nひとり用の\nロースター"),
        s(SEAT, "happy_hamster_open_arms", "1人1台"),
        s(SEAT, "peek_what_happen_cat", "まわりを見ると\nひとり客ばかり"),
        s(SEAT, "rizz_cat_rizz", "ここなら\n誰にも\n気をつかわない"),
        s(SEAT, "read_book_orange_kitten", "タレや調味料も\n手の届くところに\n並んでいる"),
        s(SEAT, "smug_squint_bicolor_cat", "にんにくもある"),
        s(SEAT, "joy_happy_happy_happy_cat", "ここは\n自分だけの城だ"),
        s(SEAT, "peek_what_happen_cat", "となりの人も\n黙々と焼いている"),
        s(SEAT, "rizz_cat_rizz", "話さなくていい\n気楽さ"),
        s(SEAT, "think_chin_paw_orange_cat", "前は\n焼肉といえば\n大勢で行くものだった"),
        s(SEAT, "calm_black_face_sheep", "取り分けたり\n焼く係になったり"),
        s(SEAT, "happy_hamster_open_arms", "今日は\n全部\n自分のためだけ"),
        # ---- 注文 ----
        s(SEAT, "work_typing_cat", "注文は\nタッチパネル", se="pikon", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(SEAT, "think_chin_paw_orange_cat", "カルビ\nハラミ\n牛タン"),
        s(SEAT, "confused_i_dont_know_cat", "セットの量も\n選べるらしい"),
        s(SEAT, "money_counting_orange_cat", "いつもなら\n少なめにする"),
        s(SEAT, "angry_shooting_cat", "でも今日は\n給料日"),
        s(SEAT, "showoff_gojo_cosplay_cat", "多めで", se="pikon"),
        s(SEAT, "happy_hamster_open_arms", "ご飯は\n大盛り"),
        s(SEAT, "smug_squint_bicolor_cat", "迷いはない"),
        s(SEAT, "stare_tabby_wide_eyes_cat", "注文して\nすぐに"),
        s(SEAT, "surprise_big_pupils_cat", "もう来た", item=SET, se="shine_kiraan_maou"),
        s(SEAT, "happy_girlfriend_dance_cat", "カルビ\n牛タン\nご飯にスープ", item=SET),
        s(SEAT, "rizz_cat_rizz", "この景色だけで\n1週間がんばれる", item=SET),
        # ---- 焼いて食べる ----
        s(SEAT, "work_typing_cat", "まずは\nカルビから", item=GRILL, bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(SEAT, "stare_big_eyes_tabby_kitten", "ジュッ", item=GRILL, se="meat_grilling_sizzle"),
        s(SEAT, "happy_hamster_open_arms", "この音が\nたまらない", item=GRILL),
        s(SEAT, "think_chin_paw_orange_cat", "焼き加減は\n自分の好みだけで\n決めていい", item=GRILL),
        s(SEAT, "smug_squint_bicolor_cat", "ちょっと\n焼きすぎるくらいが\n好き", item=GRILL),
        s(SEAT, "eat_pop_cat", "タレにつけて", item=GRILL),
        s(SEAT, "work_typing_cat", "ご飯に\nワンバウンド", item=SET),
        s(SEAT, "eat_crunchy_cat_luna", "ひと口", item=SET, se="eat_paku"),
        s(SEAT, "realize_wet_cat_stare", "…うまい", item=SET),
        s(SEAT, "joy_happy_happy_happy_cat", "これのために\n働いた", item=SET),
        s(SEAT, "eat_pop_cat", "タレが\nしみたご飯も\nまたうまい", item=SET),
        s(SEAT, "read_book_orange_kitten", "次は\n甘口のタレ", item=GRILL),
        s(SEAT, "eat_crunchy_cat_luna", "甘いのも\nいい", item=GRILL),
        s(SEAT, "think_chin_paw_orange_cat", "辛口も\n試してみる", item=GRILL),
        s(SEAT, "surprise_big_pupils_cat", "ご飯が\n止まらない", item=SET),
        s(SEAT, "rizz_cat_rizz", "誰にも\n取られない", item=GRILL),
        s(SEAT, "work_typing_cat", "次の肉を\nすぐ網にのせる", item=GRILL, se="meat_grilling_sizzle"),
        s(SEAT, "stare_tabby_wide_eyes_cat", "焼ける間に\nご飯をひと口", item=SET),
        s(SEAT, "smug_squint_bicolor_cat", "このリズムが\n完成された", item=GRILL),
        s(SEAT, "happy_girlfriend_dance_cat", "焼く\n食べる\nご飯", item=GRILL),
        s(SEAT, "eat_pop_cat", "にんにくも\n少しだけ", item=GRILL),
        s(SEAT, "realize_wet_cat_stare", "明日は休みだから\n気にしない", item=GRILL),
        s(SEAT, "happy_hamster_open_arms", "最後の1枚も\n自分のもの", item=GRILL),
        # ---- 牛タン ----
        s(SEAT, "think_chin_paw_orange_cat", "ここで\nもうひとつ", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(SEAT, "work_typing_cat", "タッチパネルで\n牛タンを追加", se="pikon"),
        s(SEAT, "surprise_big_pupils_cat", "来た", item=TAN, se="shine_kiraan_maou"),
        s(SEAT, "stare_big_eyes_tabby_kitten", "うすくて\nきれいな色", item=TAN),
        s(SEAT, "work_typing_cat", "さっとあぶって", item=TAN, se="meat_grilling_sizzle"),
        s(SEAT, "smug_squint_bicolor_cat", "レモンで\nさっぱり", item=TAN),
        s(SEAT, "eat_crunchy_cat_luna", "コリコリ", item=TAN, se="eat_paku"),
        s(SEAT, "happy_girlfriend_dance_cat", "カルビのあとの\n牛タンは\n反則だ", item=TAN),
        s(SEAT, "think_chin_paw_orange_cat", "牛タンは\n焼きすぎ注意", item=TAN),
        s(SEAT, "work_typing_cat", "2枚目は\n慎重に", item=TAN),
        s(SEAT, "smug_squint_bicolor_cat", "片面だけ\nさっと", item=TAN, se="meat_grilling_sizzle"),
        s(SEAT, "joy_happy_happy_happy_cat", "完璧な焼き加減", item=TAN),
        s(SEAT, "rizz_cat_rizz", "ひとり焼肉は\n焼き加減の\n修行の場でもある", item=TAN),
        # ---- 締め ----
        s(SEAT, "stare_lying_tabby_cat", "気づけば\nご飯が\nなくなっていた", item=SET, bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(SEAT, "think_chin_paw_orange_cat", "おかわり\nするか", item=SET),
        s(SEAT, "angry_aiming_cat", "する", se="pikon"),
        s(SEAT, "rizz_cat_rizz", "誰にも\n止められない"),
        s(SEAT, "eat_pop_cat", "残りの肉と\nご飯を\nしっかり食べる", item=SET),
        s(SEAT, "calm_black_face_sheep", "スープで\nひと息", item=SET),
        s(SEAT, "realize_wet_cat_stare", "…満腹", item=SET),
        s(SEAT, "money_counting_orange_cat", "お会計も\n思ったより\nやさしい", se="price_display"),
        s(SEAT, "happy_hamster_open_arms", "ごちそうさまでした"),
        # ---- 帰り道と家 ----
        s(FRONT, "walk_approaching_orange_cat", "お店を出る", bgm={"file": JITAKU, "gain": -10, "fade": 1.0}),
        s(STREET_N, "smug_squint_bicolor_cat", "夜風が\n気持ちいい"),
        s(STREET_N, "sad_looking_away_tabby", "服から\n焼肉のにおい"),
        s(STREET_N, "happy_hamster_open_arms", "でもいい\nこのあと\n誰にも会わない"),
        s(STREET_N, "rizz_cat_rizz", "来月も\nがんばろう"),
        s(STREET_N, "think_chin_paw_orange_cat", "コンビニに\n寄りそうになる"),
        s(STREET_N, "smug_squint_bicolor_cat", "今日はもう\n満たされている"),
        s(ROOM_N, "dance_tabby_standing_cat", "家に着いて\nお風呂"),
        s(ROOM_N, "realize_wet_cat_stare", "満腹で\nあったかい"),
        s(ROOM_N, "sleepy_sleepy_cat", "布団に入る"),
        s(ROOM_N, "stare_lying_tabby_cat", "ひとりの給料日"),
        s(ROOM_N, "happy_hamster_open_arms", "でも\nちゃんと\n幸せだった"),
        s(ROOM_N, "think_chin_paw_orange_cat", "次の給料日は"),
        s(ROOM_N, "excited_hodomoe_city_cat", "ハラミを\n多めにしよう", se="pikon", dur=3.8),
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_26_yakinikulike.mp4"), os.path.join(J.HERE, "out", "jidaraku_26_yakinikulike_preview"))
