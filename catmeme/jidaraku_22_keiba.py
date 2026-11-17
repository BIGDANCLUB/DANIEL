"""自堕落シリーズ #22：30代独身男、はじめてひとりで競馬場へ（11/17 ユーザー指定）。8〜9分。

python3 catmeme/jidaraku_22_keiba.py → out/jidaraku_22_keiba.mp4
- 流れ（ユーザー指定）：めちゃくちゃ混んでいる → フードが意外とうまい → 馬が目の前を全速力で走る姿が見られて楽しい →
  メインレースまでに当たって少しだけ増えたお金を、メインレースに全部つぎこんでハズレ →
  払い戻し機に馬券を入れて帰るものだと勘ちがいし、ハズレ券を入れてしまう（そして何も起こらない）恥ずかしさ
- 11/17 ユーザー指定：場面転換が早すぎる → 字幕1つを長め（TEMPO_K 1.3）・1つの素材で文を多めにつなぐ（HOLD 6）。
  指定がないかぎり職場の回想は入れない
- 競馬場の名前・実在の馬や騎手の名前は出さない。お金の額は「数千円」くらいでぼかす。
  「馬券は20歳から」「無理のない範囲で」を1回出す。ほかのお客さんをけなさない
- 写真は backgrounds/jidaraku/22_keiba に置く。届くまでは手もちのイラストで仮に（ほかの店の写真は使わない）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "22_keiba"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku")]
ROOM, ROOM_N, STREET = "j01_room", "j07_room_night", "bg35_suburb_street"
GATE, STAND, PADDOCK, TRACK, FOOD = "kb01_gate", "kb02_stand", "kb03_paddock", "kb04_track", "kb05_food"
J.STANDIN.update({GATE: "bg54_station_crowd_map", STAND: "bg30_summer_stadium", PADDOCK: "bg63_hokkaido_field",
                  TRACK: "bg30_summer_stadium", FOOD: "bg54_station_crowd_map"})
J.HOLD = 6
J.LOOPS = 1
J.TEMPO_K = 1.3
J.SUB_STYLE = "glow"
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
NEWSPAPER, MARK, TICKET, GOURMET, BEER, HORSE, MACHINE = ("f_newspaper", "f_marksheet", "f_ticket", "f_food", "f_beer",
                                                           "f_horse", "f_machine")


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 前日 ----
        s(ROOM_N, "stare_lying_tabby_cat", "土曜日の夜", bgm={"file": LOFI, "gain": -12}),
        s(ROOM_N, "scream_phone_orange_cat", "スマホで\n動画を見ていた"),
        s(ROOM_N, "surprise_big_pupils_cat", "競馬場の動画"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "大歓声の中\n馬が\nゴールに飛びこむ"),
        s(ROOM_N, "realize_wet_cat_stare", "なんだか\nかっこいい"),
        s(ROOM_N, "think_chin_paw_orange_cat", "競馬は\nやったことがない"),
        s(ROOM_N, "think_chin_paw_orange_cat", "でも\n競馬場は\n入場料が\nほんの少しらしい"),
        s(ROOM_N, "smug_squint_bicolor_cat", "見るだけでも\n楽しめるらしい"),
        s(ROOM_N, "excited_hodomoe_city_cat", "明日は\n競馬場だ", se="shine_kiraan_maou"),
        s(ROOM_N, "read_book_orange_kitten", "夜ふかしして\n競馬の\n基本を調べる"),
        s(ROOM_N, "read_book_orange_kitten", "単勝は\n1着の馬を当てる"),
        s(ROOM_N, "read_book_orange_kitten", "複勝は\n3着までに入れば\n当たり"),
        s(ROOM_N, "calm_black_face_sheep", "馬券は\n20歳から\n無理のない\n範囲で"),
        s(ROOM_N, "sleep_sleeping_cat", "予算は\n決めて\n寝る"),
        # ---- 当日・到着 ----
        s(STREET, "drive_driving_cat", "日曜日の朝", se="whoosh_shu", bgm={"file": MORNING, "gain": -12, "fade": 0.8}),
        s(STREET, "stare_tabby_wide_eyes_cat", "駅をおりると\n人の流れが\nひとつの方向へ"),
        s(STREET, "peek_what_happen_cat", "みんな\n新聞を\n手にしている", item=NEWSPAPER),
        s(STREET, "think_chin_paw_orange_cat", "これが\n競馬新聞か", item=NEWSPAPER),
        s(STREET, "money_counting_orange_cat", "俺も\n1部\n買ってみる", item=NEWSPAPER),
        s(STREET, "huh_huh_cat", "記号と数字が\nびっしり", item=NEWSPAPER, se="question_mark_pop_confused_huh"),
        s(STREET, "confused_i_dont_know_cat", "何ひとつ\nわからない", item=NEWSPAPER),
        s(GATE, "showoff_gojo_cosplay_cat", "競馬場に\n到着", se="gong_dora_jaan", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(GATE, "surprise_big_pupils_cat", "人が\nめちゃくちゃ\n多い", se="pi"),
        s(GATE, "stare_big_eyes_tabby_kitten", "おじさん\nカップル\n家族づれ\n若者のグループ"),
        s(GATE, "despair_dramatic_kitten", "ゲートの前から\nもう行列"),
        s(GATE, "think_chin_paw_orange_cat", "競馬って\nこんなに\n人気だったのか"),
        s(STAND, "stare_lying_tabby_cat", "スタンドに入る"),
        s(STAND, "sad_looking_away_tabby", "座る場所が\nない"),
        s(STAND, "calm_black_face_sheep", "階段の\nはしっこに\n立つことにする"),
        s(STAND, "happy_hamster_open_arms", "でも\n目の前には\n広い芝生のコース"),
        s(STAND, "realize_wet_cat_stare", "空が広い"),
        s(STAND, "sleepy_old_memories_cat", "都会の真ん中に\nこんな場所が\nあったのか"),
        s(STAND, "stare_big_eyes_tabby_kitten", "正面には\n巨大な画面"),
        s(STAND, "surprise_big_pupils_cat", "家のテレビの\n何百倍だ"),
        s(STAND, "peek_what_happen_cat", "芝生の広場では\n子どもが\n走りまわっている"),
        s(STAND, "happy_hamster_open_arms", "レジャーシートで\nお弁当を広げる家族"),
        s(STAND, "think_chin_paw_orange_cat", "競馬場って\nピクニックの場所\nでもあるのか"),
        s(STAND, "smug_squint_bicolor_cat", "ひとりで来ているのは\n俺と\n新聞のおじさんたち"),
        s(STAND, "rizz_cat_rizz", "おじさんたちと\n静かな連帯感"),
        # ---- 馬券を買う ----
        s(STAND, "work_typing_cat", "まずは\n馬券を買ってみる", item=MARK, bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(STAND, "read_book_orange_kitten", "マークシートに\nぬりつぶす", item=MARK),
        s(STAND, "huh_huh_cat", "どこを\nぬればいいんだ", item=MARK, se="question_mark_pop_confused_huh"),
        s(STAND, "peek_what_happen_cat", "となりのおじさんが\nちらっと見て", item=MARK),
        s(STAND, "stare_interviewer_cat", "兄ちゃん\nはじめてか？\nここに馬の番号だよ", item=MARK),
        s(STAND, "happy_hamster_open_arms", "競馬場の人は\nやさしい", item=MARK),
        s(STAND, "think_chin_paw_orange_cat", "最初のレースは\n名前が\nかっこいい馬の\n複勝で", item=TICKET),
        s(STAND, "smug_squint_bicolor_cat", "根拠は\nない", item=TICKET),
        # ---- 馬が目の前を走る ----
        s(TRACK, "stare_tabby_wide_eyes_cat", "レースが\nはじまる", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(TRACK, "surprise_big_pupils_cat", "ファンファーレ", se="gong_dora_jaan"),
        s(TRACK, "joy_happy_happy_happy_cat", "スタンドが\nどっとわく"),
        s(TRACK, "stare_big_eyes_tabby_kitten", "ゲートが開く", se="pi"),
        s(TRACK, "stare_lying_tabby_cat", "遠くで\n馬が\n走っている"),
        s(TRACK, "think_chin_paw_orange_cat", "小さくて\nよく見えない"),
        s(TRACK, "stare_tabby_wide_eyes_cat", "と思ったら"),
        s(TRACK, "scream_standing_marmot", "目の前を\n全速力で\n駆けぬけていく", item=HORSE, se="explosion_dokaan"),
        s(TRACK, "surprise_big_pupils_cat", "ドドドドドド", item=HORSE),
        s(TRACK, "realize_wet_cat_stare", "地面が\nゆれている", item=HORSE),
        s(TRACK, "happy_girlfriend_dance_cat", "動画とは\nぜんぜんちがう", item=HORSE),
        s(TRACK, "showoff_gojo_cosplay_cat", "馬って\nこんなに\nでかくて\n速いのか", item=HORSE),
        s(TRACK, "sleepy_old_memories_cat", "あっという間に\nゴール", item=HORSE),
        s(TRACK, "stare_lying_tabby_cat", "俺の馬は", item=TICKET),
        s(TRACK, "calm_black_face_sheep", "どこを\n走っていたのか\nわからない", item=TICKET),
        s(TRACK, "sad_looking_away_tabby", "ハズレ", item=TICKET),
        s(TRACK, "rizz_cat_rizz", "でも\nいいものを見た", item=HORSE),
        s(TRACK, "think_chin_paw_orange_cat", "2レース目も\n3レース目も\nハズレ", item=TICKET),
        s(TRACK, "calm_black_face_sheep", "でも\n毎回\n馬が目の前を\n走りぬけていく", item=HORSE),
        s(TRACK, "happy_girlfriend_dance_cat", "それだけで\n楽しい", item=HORSE),
        s(TRACK, "smug_squint_bicolor_cat", "これは\n入場料で見られる\nスポーツ観戦だ", item=HORSE),
        # ---- 競馬場グルメ ----
        s(FOOD, "sulk_hungry_cat", "腹が減った", se="pi", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(FOOD, "stare_big_eyes_tabby_kitten", "フードコートへ", item=GOURMET),
        s(FOOD, "surprise_big_pupils_cat", "思ったより\n店が多い", item=GOURMET),
        s(FOOD, "think_chin_paw_orange_cat", "カレー\nもつ煮\n焼きそば\nステーキ丼", item=GOURMET),
        s(FOOD, "despair_dramatic_kitten", "どこも\n行列", item=GOURMET),
        s(FOOD, "money_counting_orange_cat", "名物っぽい\nもつ煮込みを\n買う", item=GOURMET),
        s(FOOD, "eat_pop_cat", "ズズッ", item=GOURMET, se="pikon"),
        s(FOOD, "happy_girlfriend_dance_cat", "うまい", item=GOURMET),
        s(FOOD, "eat_crunchy_cat_luna", "競馬場の\nごはんが\n意外とうまい", item=GOURMET),
        s(FOOD, "happy_hamster_open_arms", "ビールも\nたのんでしまう", item=BEER, se="drink_gulp_gokugoku_thirsty_chug"),
        s(FOOD, "sleepy_sleepy_cat", "昼の青空の下\nもつ煮とビール", item=BEER),
        s(FOOD, "rizz_cat_rizz", "これだけで\n来たかいがあった", item=BEER),
        s(FOOD, "peek_what_happen_cat", "となりのテーブルでは\nおじさんが\nステーキ丼", item=GOURMET),
        s(FOOD, "stare_interviewer_cat", "ここのは\n勝った日に食うんだよ", item=GOURMET),
        s(FOOD, "think_chin_paw_orange_cat", "勝った日の\nステーキ丼", item=GOURMET),
        s(FOOD, "angry_aiming_cat", "それを\n今日の目標にする", item=GOURMET),
        s(FOOD, "work_typing_cat", "食べ終わって\nトイレへ", item=BEER),
        s(FOOD, "despair_dramatic_kitten", "トイレも\n行列", item=BEER),
        s(FOOD, "calm_black_face_sheep", "競馬場は\nどこへ行っても\n行列", item=BEER),
        # ---- パドック ----
        s(PADDOCK, "stare_tabby_wide_eyes_cat", "パドックという\n場所があるらしい", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(PADDOCK, "read_book_orange_kitten", "レース前の馬が\nぐるぐる歩いて\n見せてくれる場所", item=HORSE),
        s(PADDOCK, "surprise_big_pupils_cat", "近い", item=HORSE),
        s(PADDOCK, "stare_big_eyes_tabby_kitten", "毛が\nつやつやしている", item=HORSE),
        s(PADDOCK, "peek_what_happen_cat", "まわりの人は\n真剣な顔で\nメモをとっている", item=HORSE),
        s(PADDOCK, "think_chin_paw_orange_cat", "俺も\nそれっぽく\nうなずく", item=HORSE),
        s(PADDOCK, "smug_squint_bicolor_cat", "あの馬\nいい顔してる", item=HORSE),
        s(PADDOCK, "calm_black_face_sheep", "根拠は\nやっぱりない", item=HORSE),
        s(PADDOCK, "stare_interviewer_cat", "兄ちゃん\nあの馬は\n首の使い方がいいよ", item=HORSE),
        s(PADDOCK, "surprise_big_pupils_cat", "首の使い方", item=HORSE),
        s(PADDOCK, "think_chin_paw_orange_cat", "わからないけど\n信じてみる", item=HORSE),
        s(PADDOCK, "smug_squint_bicolor_cat", "競馬場の先生だ", item=HORSE),
        # ---- 当たる ----
        s(STAND, "work_typing_cat", "パドックで\n気に入った馬の\n複勝を買う", item=TICKET, bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(TRACK, "stare_lying_tabby_cat", "レースがはじまる"),
        s(TRACK, "angry_aiming_cat", "いけ", se="pi"),
        s(TRACK, "scream_standing_marmot", "そのまま", se="explosion_chudoon"),
        s(TRACK, "surprise_big_pupils_cat", "3着", se="shine_kiraan_maou"),
        s(TRACK, "joy_happy_happy_happy_cat", "当たった", item=TICKET),
        s(TRACK, "happy_girlfriend_dance_cat", "はじめての的中", item=TICKET),
        s(TRACK, "stare_interviewer_cat", "兄ちゃん\nやったな", item=TICKET),
        s(TRACK, "happy_hamster_open_arms", "となりのおじさんと\nハイタッチ", item=TICKET),
        s(TRACK, "money_counting_orange_cat", "その後も\n少しずつ当たって\n予算が\n少しだけ増えた", item=TICKET),
        s(TRACK, "showoff_gojo_cosplay_cat", "俺には\n才能があるのかもしれない", item=TICKET, se="gong_dora_jaan"),
        s(TRACK, "rizz_cat_rizz", "いや\nたぶんない", item=TICKET),
        # ---- メインレース ----
        s(STAND, "stare_tabby_wide_eyes_cat", "そして\nいよいよ\nメインレース", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(STAND, "surprise_big_pupils_cat", "スタンドの人が\nさらにふえる"),
        s(STAND, "think_chin_paw_orange_cat", "手元には\n少しだけ増えたお金"),
        s(STAND, "sleepy_old_memories_cat", "ここで\n悪魔がささやく"),
        s(STAND, "smug_squint_bicolor_cat", "増えたぶんは\nもともと\nなかったお金だ"),
        s(STAND, "angry_aiming_cat", "全部\nいこう", se="explosion_chudoon"),
        s(STAND, "work_typing_cat", "今度は\n単勝", item=TICKET),
        s(STAND, "money_counting_orange_cat", "増えたぶん\nすべて\nぶっこむ", item=TICKET),
        s(STAND, "realize_wet_cat_stare", "馬券を\nにぎる手に\n汗", item=TICKET),
        s(TRACK, "surprise_big_pupils_cat", "ファンファーレ", se="gong_dora_jaan"),
        s(TRACK, "joy_happy_happy_happy_cat", "大歓声"),
        s(TRACK, "stare_big_eyes_tabby_kitten", "スタート", se="pi"),
        s(TRACK, "stare_lying_tabby_cat", "俺の馬は\n先頭あたり"),
        s(TRACK, "angry_aiming_cat", "そのまま"),
        s(TRACK, "angry_shooting_cat", "そのまま\nいけ", se="explosion_dokaan"),
        s(TRACK, "scream_standing_marmot", "最後の直線", item=HORSE),
        s(TRACK, "despair_dramatic_kitten", "うしろから\nすごい勢いで\n何頭もくる", item=HORSE),
        s(TRACK, "sad_banana_cat_cry", "かわされた", item=HORSE, se="explosion_chudoon"),
        s(TRACK, "blank_black_cat_zoning_out", "4着", item=TICKET),
        s(TRACK, "calm_black_face_sheep", "増えたお金は\n全部\n馬のもとへ", item=TICKET),
        s(TRACK, "sad_looking_away_tabby", "もとどおり", item=TICKET),
        s(TRACK, "stare_interviewer_cat", "兄ちゃん\nそれが競馬だ", item=TICKET),
        s(TRACK, "realize_wet_cat_stare", "おじさんの言葉が\nしみる", item=TICKET),
        s(FOOD, "stare_lying_tabby_cat", "帰りに\nフードコートの前を通る", item=GOURMET),
        s(FOOD, "stare_big_eyes_tabby_kitten", "勝った日の\nステーキ丼", item=GOURMET),
        s(FOOD, "sad_looking_away_tabby", "今日は\n見るだけ", item=GOURMET),
        s(FOOD, "calm_black_face_sheep", "目標は\n来月に\nもちこし", item=GOURMET),
        # ---- 払い戻し機 ----
        s(GATE, "stare_lying_tabby_cat", "帰ろう", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(GATE, "peek_what_happen_cat", "出口の近くに\n機械がならんでいる", item=MACHINE),
        s(GATE, "peek_what_happen_cat", "みんな\n馬券を入れてから\n帰っていく", item=MACHINE),
        s(GATE, "think_chin_paw_orange_cat", "なるほど", item=MACHINE),
        s(GATE, "smug_squint_bicolor_cat", "帰るときは\n馬券を\nここに入れるのが\nマナーなんだな", item=MACHINE),
        s(GATE, "work_typing_cat", "ハズレ券を\nそっと入れる", item=MACHINE),
        s(GATE, "stare_tabby_wide_eyes_cat", "……", item=MACHINE),
        s(GATE, "stare_big_eyes_tabby_kitten", "…………", item=MACHINE),
        s(GATE, "blank_black_cat_zoning_out", "何も起こらない", item=MACHINE),
        s(GATE, "read_book_orange_kitten", "よく見ると\n払い戻し機と\n書いてある", item=MACHINE),
        s(GATE, "surprise_big_pupils_cat", "当たった馬券を\nお金にかえる\n機械だった", item=MACHINE, se="pi"),
        s(GATE, "despair_dramatic_kitten", "うしろに\n人が\nならんでいる", item=MACHINE),
        s(GATE, "sad_banana_cat_cry", "顔が\nあつい", item=MACHINE),
        s(GATE, "leave_cat_leaves_home", "足早に\nその場を去る", se="whoosh_shu"),
        # ---- 帰り道 ----
        s(STREET, "sleepy_old_memories_cat", "帰り道", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(STREET, "think_chin_paw_orange_cat", "お金は\n入場前と\nほぼ同じ"),
        s(STREET, "stare_lying_tabby_cat", "でも\n頭の中では\nまだ馬が\n走っている"),
        s(STREET, "happy_hamster_open_arms", "目の前を\n駆けぬけた\nあの音"),
        s(STREET, "eat_crunchy_cat_luna", "青空の下の\nもつ煮とビール"),
        s(STREET, "smug_squint_bicolor_cat", "となりのおじさんとの\nハイタッチ"),
        s(STREET, "rizz_cat_rizz", "入場料以上に\n楽しかった"),
        s(STREET, "peek_what_happen_cat", "駅まで\n人の大行列"),
        s(STREET, "stare_tabby_wide_eyes_cat", "みんな\n今日の\n勝ち負けの話をしている"),
        s(STREET, "happy_hamster_open_arms", "知らない人どうしなのに\nなんだか仲間みたいだ"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", se="whoosh_shu", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(ROOM_N, "scream_phone_orange_cat", "スマホで\n今日のレースを\n見返す"),
        s(ROOM_N, "despair_dramatic_kitten", "メインレースの\n最後の直線"),
        s(ROOM_N, "sad_looking_away_tabby", "何回見ても\nかわされる"),
        s(ROOM_N, "think_chin_paw_orange_cat", "そして\nあの機械の前の\n俺"),
        s(ROOM_N, "blank_black_cat_zoning_out", "思い出すたびに\n顔があつくなる"),
        s(ROOM_N, "read_book_orange_kitten", "次の予定を\n調べる"),
        s(ROOM_N, "excited_hodomoe_city_cat", "来月も\n行こう\n今度は\n払い戻し機に\n当たり券を\n入れるために", se="pikon", dur=4.2),
        J.end_card(),
    ]


def place(cs):
    J.diversify(cs)
    J.prefer_long(cs)   # 11/17 ユーザー指定：場面転換をゆっくりに
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_22_keiba.mp4"), os.path.join(J.HERE, "out", "jidaraku_22_keiba_preview"))
