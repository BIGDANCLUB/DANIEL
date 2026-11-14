"""自堕落シリーズ #19：30代独身男、マックの新作チキンをひとりで食べくらべ（11/14 ユーザー指定：ユーザーの感想＋口コミ）。8分すこし。

python3 catmeme/jidaraku_19_mac.py → out/jidaraku_19_mac.mp4
- 流れ（ユーザー指定）：10/21 から新作チキン（ザクザクチキンジューシーマック・スパイシーザクザクジューシーマック・
  てりやきチキンジューシーマック）と単品のザクザクジューシーももチキン → 3つ一気に注文（店員さんには食べくらべに見える）→
  全体の感想 → 3種の感想（てりやきが優勝）→ 後日 夜マックで てりやきの倍 → ももチキン単品とマックフィズ →
  また後日、人気すぎて一時休止で泣き崩れる → 早く再開してくれ
- 公式・ニュースより：11/13 から一時休止（想定を上回る販売でチキンパティの安定供給が難しく）、11月末の再開見込み。夜マックの倍も対象
- 口コミより：レタスのシャキシャキが目立つという声もある／感想は人それぞれ（「個人の感想です」を1回出す）
- 値段は出さない。お店・ほかのお客さんをけなさない
- 写真は backgrounds/jidaraku/19_mac に置く。届くまでは手もちのイラストで仮に（ほかの店の写真は使わない）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "19_mac"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku")]
OFFICE, STREET, STREET_N, ROOM_N = "bg25_office_desk", "bg35_suburb_street", "bg51_night_street", "j07_room_night"
FRONT, SEAT, FRONT_N = "mc01_front", "mc02_seat", "mc03_front_night"
J.STANDIN.update({FRONT: "bg35_suburb_street", SEAT: "bg28_ny_diner", FRONT_N: "bg51_night_street"})
J.HOLD = 4
J.LOOPS = 1
J.SUB_STYLE = "glow"
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
TRAY, ZAKU, SPICY, TERI, BAI, MOMO, FIZZ = "f_tray3", "f_zakuzaku", "f_spicy", "f_teriyaki", "f_teriyaki_bai", "f_momo", "f_fizz"


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 発端 ----
        s(OFFICE, "work_typing_cat", "10月のある日\n昼休み", bgm={"file": LOFI, "gain": -12}),
        s(OFFICE, "scream_phone_orange_cat", "スマホを見る"),
        s(OFFICE, "surprise_big_pupils_cat", "マックから\nチキンの新作が\n出るらしい", se="pi"),
        s(OFFICE, "read_book_orange_kitten", "ザクザクチキン\nジューシーマック"),
        s(OFFICE, "read_book_orange_kitten", "スパイシー\nザクザク\nジューシーマック"),
        s(OFFICE, "read_book_orange_kitten", "てりやきチキン\nジューシーマック"),
        s(OFFICE, "stare_tabby_wide_eyes_cat", "さらに\nサイドメニューに\nももチキン単品"),
        s(OFFICE, "think_chin_paw_orange_cat", "新作が\n3つ同時"),
        s(OFFICE, "angry_aiming_cat", "これは\n食べくらべるしかない"),
        s(OFFICE, "stare_interviewer_cat", "ちょっといいかな", se="pi"),
        s(OFFICE, "surprise_big_pupils_cat", "上司だ"),
        s(OFFICE, "stare_interviewer_cat", "週末\n空いてる？"),
        s(OFFICE, "calmdown_dancing_cat", "週末は\n大事な会議が\nありまして"),
        s(OFFICE, "smug_squint_bicolor_cat", "チキンとの\n会議だ"),
        # ---- 来店 ----
        s(STREET, "drive_driving_cat", "土曜日の昼", se="whoosh_shu", bgm={"file": MORNING, "gain": -12, "fade": 0.8}),
        s(STREET, "happy_hamster_open_arms", "足どりが軽い"),
        s(FRONT, "showoff_gojo_cosplay_cat", "マックに到着", se="gong_dora_jaan"),
        s(FRONT, "peek_what_happen_cat", "店の前に\n新作のポスター"),
        s(FRONT, "stare_big_eyes_tabby_kitten", "ザクザクの文字が\nまぶしい"),
        s(FRONT, "rizz_cat_rizz", "待っていたぞ"),
        s(SEAT, "work_typing_cat", "注文は\nもう決めてある", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(SEAT, "stare_lying_tabby_cat", "……はずだった"),
        s(SEAT, "think_chin_paw_orange_cat", "メニューを見ると\nポテトも\nナゲットも\n呼んでいる"),
        s(SEAT, "despair_dramatic_kitten", "いや\n今日はチキンの日だ"),
        s(SEAT, "angry_aiming_cat", "誘惑を\nふりきる"),
        s(SEAT, "angry_shooting_cat", "新作のバーガー\n3つください", se="pikon"),
        s(SEAT, "stare_interviewer_cat", "3つ\nですね"),
        s(SEAT, "think_chin_paw_orange_cat", "ひとりで\n新作3つ"),
        s(SEAT, "stare_lying_tabby_cat", "店員さんから見れば"),
        s(SEAT, "sad_looking_away_tabby", "あからさまに\n食べくらべに来た人"),
        s(SEAT, "calm_black_face_sheep", "その通りです"),
        s(SEAT, "smug_squint_bicolor_cat", "隠すつもりもない"),
        s(SEAT, "surprise_big_pupils_cat", "トレーが\nやってきた", item=TRAY, se="shine_kiraan_maou"),
        s(SEAT, "happy_girlfriend_dance_cat", "包み紙が\n3つならんでいる", item=TRAY),
        s(SEAT, "joy_happy_happy_happy_cat", "これは\n祭りだ", item=TRAY),
        s(SEAT, "read_book_orange_kitten", "※感想は\n個人のものです", item=TRAY),
        # ---- 全体 ----
        s(SEAT, "think_chin_paw_orange_cat", "まずは\n全体の印象から", item=TRAY),
        s(SEAT, "eat_pop_cat", "ザクッ", item=ZAKU, se="pikon"),
        s(SEAT, "surprise_big_pupils_cat", "ザクザク感が\n前より\n格段に上がっている", item=ZAKU),
        s(SEAT, "eat_crunchy_cat_luna", "なのに\n中のもも肉は\n肉厚で\nやわらかい", item=ZAKU),
        s(SEAT, "happy_hamster_open_arms", "ザクザクと\nやわらかさが\n同時にくる", item=ZAKU),
        s(SEAT, "happy_girlfriend_dance_cat", "うまい", item=ZAKU),
        s(SEAT, "rizz_cat_rizz", "外はザクザク\n中はジューシー", item=ZAKU),
        s(SEAT, "smug_squint_bicolor_cat", "名前に\nうそがない", item=ZAKU),
        # ---- ザクザク ----
        s(SEAT, "angry_aiming_cat", "1つ目\nザクザクチキン\nジューシーマック", item=ZAKU, se="explosion_chudoon"),
        s(SEAT, "eat_pop_cat", "ガブッ", item=ZAKU),
        s(SEAT, "surprise_big_pupils_cat", "マスタードが\n本当に\nいい味を出している", item=ZAKU),
        s(SEAT, "sleepy_sleepy_cat", "重くない\n軽やかな味", item=ZAKU),
        s(SEAT, "eat_crunchy_cat_luna", "玉ねぎと\nチキンの相性が\nとてもいい", item=ZAKU),
        s(SEAT, "happy_hamster_open_arms", "レタスの\nシャキシャキも\nいい仕事をしている", item=ZAKU),
        s(SEAT, "think_chin_paw_orange_cat", "毎日でも\n食べられる\nバランスだ", item=ZAKU),
        s(SEAT, "rizz_cat_rizz", "王道の\n優等生", item=ZAKU),
        s(SEAT, "peek_what_happen_cat", "となりの席の\n学生たちも\n同じ包み紙", item=ZAKU),
        s(SEAT, "happy_hamster_open_arms", "みんな\n新作に夢中だ", item=ZAKU),
        # ---- スパイシー ----
        s(SEAT, "angry_aiming_cat", "2つ目\nスパイシーザクザク\nジューシーマック", item=SPICY, se="explosion_chudoon"),
        s(SEAT, "eat_pop_cat", "ガブッ", item=SPICY),
        s(SEAT, "stare_tabby_wide_eyes_cat", "……", item=SPICY),
        s(SEAT, "scream_standing_marmot", "からい", item=SPICY, se="explosion_dokaan"),
        s(SEAT, "surprise_big_pupils_cat", "ガーリックと\n唐がらしが\nガツンとくる", item=SPICY),
        s(SEAT, "despair_dramatic_kitten", "口の中が\n火事だ", item=SPICY),
        s(SEAT, "eat_crunchy_cat_luna", "冷たいドリンクを\n流しこむ", item=SPICY, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "happy_girlfriend_dance_cat", "うまい", item=SPICY),
        s(SEAT, "think_chin_paw_orange_cat", "単品でもいいが", item=SPICY),
        s(SEAT, "smug_squint_bicolor_cat", "ぜひ\n冷たいドリンクと\nいっしょに", item=SPICY),
        s(SEAT, "rizz_cat_rizz", "これは\nセット推奨\nバーガーだ", item=SPICY),
        # ---- てりやき ----
        s(SEAT, "angry_aiming_cat", "3つ目\nてりやきチキン\nジューシーマック", item=TERI, se="explosion_chudoon", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(SEAT, "eat_pop_cat", "ガブッ", item=TERI),
        s(SEAT, "stare_lying_tabby_cat", "……", item=TERI),
        s(SEAT, "surprise_big_pupils_cat", "これは", item=TERI, se="pi"),
        s(SEAT, "stare_big_eyes_tabby_kitten", "なんと", item=TERI),
        s(SEAT, "showoff_gojo_cosplay_cat", "見つけた", item=TERI, se="gong_dora_jaan"),
        s(SEAT, "joy_happy_happy_happy_cat", "今回の\n優勝わくだ", item=TERI),
        s(SEAT, "read_book_orange_kitten", "てりやきソースと\nスイートレモンソース", item=TERI),
        s(SEAT, "happy_girlfriend_dance_cat", "この2つの\nからみが\nすばらしい", item=TERI),
        s(SEAT, "think_chin_paw_orange_cat", "そもそも", item=TERI),
        s(SEAT, "smug_squint_bicolor_cat", "肉厚やわらか\nもも肉と\nてりやき", item=TERI),
        s(SEAT, "angry_shooting_cat", "相性が\n悪いはずがない", item=TERI, se="explosion_dokaan"),
        s(SEAT, "despair_dramatic_kitten", "正論パンチを\nこれでもかと\nくらわせてくる", item=TERI),
        s(SEAT, "eat_crunchy_cat_luna", "このマリアージュに\n加えて", item=TERI),
        s(SEAT, "happy_hamster_open_arms", "バンズとの\nマリアージュまで\n存在する", item=TERI),
        s(SEAT, "realize_wet_cat_stare", "すばらしすぎる", item=TERI),
        s(SEAT, "think_chin_paw_orange_cat", "タレがあるぶん\nザクザク感は\nひかえめ", item=TERI),
        s(SEAT, "rizz_cat_rizz", "でも\nザクザク衣のおかげで\nべちゃっとしない", item=TERI),
        s(SEAT, "stare_tabby_wide_eyes_cat", "ザクザク衣は\n口の中を切るから\nにがてな人もいそう", item=TERI),
        s(SEAT, "smug_squint_bicolor_cat", "これなら\nその心配もない", item=TERI),
        s(SEAT, "happy_girlfriend_dance_cat", "味も食感も\n食べやすい", item=TERI),
        s(SEAT, "showoff_gojo_cosplay_cat", "これは\n大当たりだ", item=TERI, se="gong_dora_jaan"),
        # ---- 結果 ----
        s(SEAT, "stare_lying_tabby_cat", "3つ食べ終わった", item=TRAY, bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(SEAT, "work_typing_cat", "結果を\nまとめる", item=TRAY),
        s(SEAT, "read_book_orange_kitten", "ザクザクは\n軽やかな王道", item=ZAKU),
        s(SEAT, "read_book_orange_kitten", "スパイシーは\nドリンク必須の\nパンチ力", item=SPICY),
        s(SEAT, "read_book_orange_kitten", "てりやきは\n優勝", item=TERI),
        s(SEAT, "happy_hamster_open_arms", "3つとも\nちゃんとうまい", item=TRAY),
        s(SEAT, "sleepy_sleepy_cat", "おなかは\nパンパンだ", item=TRAY),
        s(SEAT, "stare_interviewer_cat", "ありがとう\nございましたー"),
        s(SEAT, "rizz_cat_rizz", "店員さんの笑顔が\nいつもより\nやさしい気がする"),
        s(SEAT, "calm_black_face_sheep", "たぶん\n気のせいだ"),
        s(FRONT, "leave_cat_leaves_home", "大満足で\n店を出る", se="whoosh_shu"),
        s(STREET, "drive_driving_cat", "帰り道", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(STREET, "think_chin_paw_orange_cat", "頭の中は\nずっと\nてりやき"),
        s(STREET, "sleepy_old_memories_cat", "スイートレモンの\n余韻"),
        s(STREET, "angry_aiming_cat", "決めた"),
        s(STREET, "smug_squint_bicolor_cat", "次は\nてりやきを\nもっと食べる"),
        s(ROOM_N, "scream_phone_orange_cat", "家でSNSを見る", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(ROOM_N, "read_book_orange_kitten", "てりやきが\n一番という声"),
        s(ROOM_N, "read_book_orange_kitten", "スパイシーが\nクセになるという声"),
        s(ROOM_N, "read_book_orange_kitten", "レタスのシャキシャキが\n目立つという声"),
        s(ROOM_N, "think_chin_paw_orange_cat", "感想は\n人それぞれ"),
        s(ROOM_N, "smug_squint_bicolor_cat", "でも\nみんな\n楽しそうだ"),
        s(ROOM_N, "happy_hamster_open_arms", "同じものを食べて\nわいわい語る"),
        s(ROOM_N, "rizz_cat_rizz", "ひとりでも\nこれなら\nさみしくない"),
        # ---- 会社 ----
        s(OFFICE, "work_typing_cat", "月曜日", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(OFFICE, "stare_interviewer_cat", "この資料\n今日中に\n倍の量にして"),
        s(OFFICE, "surprise_big_pupils_cat", "倍……"),
        s(OFFICE, "despair_dramatic_kitten", "いつもなら\n絶望の言葉"),
        s(OFFICE, "think_chin_paw_orange_cat", "でも\n今日の俺には\nちがう意味に聞こえる"),
        s(OFFICE, "read_book_orange_kitten", "夜マックには\n倍バーガーがある"),
        s(OFFICE, "rizz_cat_rizz", "倍の仕事には\n倍のてりやきだ"),
        s(OFFICE, "work_typing_cat", "猛スピードで\n資料を倍にする"),
        s(OFFICE, "leave_cat_leaves_home", "お先に\n失礼します", se="whoosh_shu"),
        s(OFFICE, "stare_interviewer_cat", "先輩\nマックの新作\nどれが一番でした？"),
        s(OFFICE, "smug_squint_bicolor_cat", "てりやき一択だ"),
        s(OFFICE, "stare_interviewer_cat", "わかりました！"),
        s(OFFICE, "peek_what_happen_cat", "翌日"),
        s(OFFICE, "stare_interviewer_cat", "スパイシーの倍に\nしてみました！"),
        s(OFFICE, "surprise_big_pupils_cat", "聞いてなかった"),
        s(OFFICE, "scream_standing_marmot", "からくて\n午後ずっと\n水を飲んでいた", se="explosion_chudoon"),
        s(OFFICE, "blank_black_cat_zoning_out", "でも\nうまかったらしい"),
        # ---- 夜マック ----
        s(FRONT_N, "drive_driving_cat", "夜", se="whoosh_shu", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(FRONT_N, "showoff_gojo_cosplay_cat", "ふたたびマックへ", se="gong_dora_jaan"),
        s(FRONT_N, "angry_shooting_cat", "てりやきチキン\nジューシーマックの\n倍で", se="pikon"),
        s(FRONT_N, "stare_interviewer_cat", "倍ですね"),
        s(FRONT_N, "smug_squint_bicolor_cat", "1日の締めくくりに\nふさわしい注文だ"),
        s(SEAT, "surprise_big_pupils_cat", "きた", item=BAI, se="shine_kiraan_maou"),
        s(SEAT, "stare_big_eyes_tabby_kitten", "チキンが\n2枚", item=BAI),
        s(SEAT, "despair_dramatic_kitten", "高さがおかしい", item=BAI),
        s(SEAT, "eat_pop_cat", "ガブッ", item=BAI, se="pikon"),
        s(SEAT, "scream_standing_marmot", "やわらかチキンの\n暴力", item=BAI, se="explosion_dokaan"),
        s(SEAT, "despair_dramatic_kitten", "口に入りきらない", item=BAI),
        s(SEAT, "work_typing_cat", "上からおさえて\n高さを半分にする", item=BAI),
        s(SEAT, "eat_crunchy_cat_luna", "もう一度\nガブッ", item=BAI),
        s(SEAT, "realize_wet_cat_stare", "もも肉を\nバンズにはさんだ\nつもりが", item=BAI),
        s(SEAT, "sad_banana_cat_cry", "こっちが\nもも肉に\nはさまれていた", item=BAI),
        s(SEAT, "happy_girlfriend_dance_cat", "倍の幸せ", item=BAI),
        s(SEAT, "rizz_cat_rizz", "倍の資料のことは\nもう忘れた", item=BAI),
        # ---- ももチキン ----
        s(SEAT, "think_chin_paw_orange_cat", "さらに\n単品の\nももチキンも\n頼んでおいた", item=MOMO),
        s(SEAT, "stare_tabby_wide_eyes_cat", "ソースは\nかかっていない", item=MOMO),
        s(SEAT, "stare_lying_tabby_cat", "チキンだけが\nどーんと来る", item=MOMO),
        s(SEAT, "eat_pop_cat", "ザクッ", item=MOMO, se="pikon"),
        s(SEAT, "surprise_big_pupils_cat", "衣に\n味がついている", item=MOMO),
        s(SEAT, "happy_hamster_open_arms", "ソースなしでも\nまったく問題なし", item=MOMO),
        s(SEAT, "eat_crunchy_cat_luna", "ザクザク感を\nストレートに\n味わえる", item=MOMO),
        s(SEAT, "smug_squint_bicolor_cat", "食感目当てなら\nこれもいい", item=MOMO),
        s(SEAT, "think_chin_paw_orange_cat", "ただ\n前のチキンも\nザクザクはしていた", item=MOMO),
        s(SEAT, "calm_black_face_sheep", "そこは\n冷静に\nおさえておきたい", item=MOMO),
        # ---- マックフィズ ----
        s(SEAT, "stare_big_eyes_tabby_kitten", "そして\nいっしょに頼んだ\nマックフィズ", item=FIZZ),
        s(SEAT, "eat_crunchy_cat_luna", "ゴクッ", item=FIZZ, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "surprise_big_pupils_cat", "このチキン\nマックフィズとの相性\nバツグンだ", item=FIZZ),
        s(SEAT, "happy_girlfriend_dance_cat", "ザクザク感と\nもも肉の油を", item=FIZZ),
        s(SEAT, "sleepy_sleepy_cat", "フィズの爽快感が\n気持ちよく\n流してくれる", item=FIZZ),
        s(SEAT, "eat_pop_cat", "チキン", item=MOMO),
        s(SEAT, "eat_crunchy_cat_luna", "フィズ", item=FIZZ),
        s(SEAT, "eat_pop_cat", "チキン", item=MOMO),
        s(SEAT, "eat_crunchy_cat_luna", "フィズ", item=FIZZ),
        s(SEAT, "happy_chipi_chapa_cat", "無限ループだ", item=FIZZ),
        s(SEAT, "rizz_cat_rizz", "夜マックは\n大人の遊園地", item=FIZZ),
        s(SEAT, "stare_lying_tabby_cat", "気づけば\nトレーの上は\n空っぽ"),
        s(SEAT, "sleepy_sleepy_cat", "しあわせな\n満腹感"),
        s(SEAT, "calm_black_face_sheep", "あしたの体重は\n見ないことにする"),
        s(FRONT_N, "leave_cat_leaves_home", "満腹で\n店を出る", se="whoosh_shu"),
        s(STREET_N, "sleepy_old_memories_cat", "夜風が\n気持ちいい", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(STREET_N, "think_chin_paw_orange_cat", "次は\nスパイシーの倍を\n試すか"),
        s(STREET_N, "smug_squint_bicolor_cat", "それとも\nもう一度\nてりやきか"),
        s(STREET_N, "happy_hamster_open_arms", "悩む時間すら\n楽しい"),
        # ---- 休止 ----
        s(OFFICE, "work_typing_cat", "そして\n数日後", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(OFFICE, "stare_interviewer_cat", "今週中に\nこの案件\nたのむね"),
        s(OFFICE, "rizz_cat_rizz", "まかせてください"),
        s(OFFICE, "smug_squint_bicolor_cat", "俺には\nてりやきがある"),
        s(OFFICE, "work_typing_cat", "全部\n終わらせた"),
        s(FRONT, "drive_driving_cat", "ごほうびの\nマックへ", se="whoosh_shu"),
        s(FRONT, "angry_shooting_cat", "てりやきチキン\nジューシーマック\nください", se="pikon"),
        s(FRONT, "stare_interviewer_cat", "申し訳ございません"),
        s(FRONT, "stare_interviewer_cat", "こちら\nただいま\n販売を休止しております"),
        s(FRONT, "surprise_big_pupils_cat", "……え", se="pi"),
        s(FRONT, "scream_phone_orange_cat", "あわてて\nスマホで調べる"),
        s(FRONT, "read_book_orange_kitten", "人気すぎて\nチキンが足りず\n一時休止"),
        s(FRONT, "stare_big_eyes_tabby_kitten", "11月13日から\n休止"),
        s(FRONT, "think_chin_paw_orange_cat", "発売から\n1か月もたっていない"),
        s(FRONT, "stare_tabby_wide_eyes_cat", "ザクザクも\nスパイシーも\nももチキンも"),
        s(FRONT, "despair_dramatic_kitten", "夜マックの倍も", se="explosion_chudoon"),
        s(FRONT, "sad_banana_cat_cry", "その場で\n泣きくずれる俺"),
        s(FRONT, "sad_black_dog", "倍の資料を\n倍の速さで\n終わらせたのに"),
        s(FRONT, "calm_black_face_sheep", "人気すぎて\n休止"),
        s(FRONT, "think_chin_paw_orange_cat", "裏を返せば\nそれだけ\nうまいということだ"),
        s(FRONT, "realize_wet_cat_stare", "みんな\nわかっていた"),
        s(FRONT, "smug_squint_bicolor_cat", "俺の舌は\nまちがっていなかった"),
        s(FRONT, "sad_looking_away_tabby", "でも\n今は\nその証明がつらい"),
        s(FRONT, "read_book_orange_kitten", "11月末の\n再開を\n見込んでいるらしい"),
        s(STREET, "sleepy_old_memories_cat", "帰り道", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(STREET, "stare_lying_tabby_cat", "手には\nいつものチーズバーガー"),
        s(STREET, "happy_hamster_open_arms", "これはこれで\nうまい"),
        s(STREET, "think_chin_paw_orange_cat", "でも\n心はてりやき"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", se="whoosh_shu"),
        s(ROOM_N, "scream_phone_orange_cat", "再開の\nお知らせを\n毎日チェックする"),
        s(ROOM_N, "think_chin_paw_orange_cat", "待ちきれない"),
        s(ROOM_N, "angry_aiming_cat", "家で\nてりやきチキンを\n作ってみる"),
        s(ROOM_N, "work_typing_cat", "もも肉に\n衣をつけて\n揚げる"),
        s(ROOM_N, "despair_dramatic_kitten", "衣がはがれる", se="explosion_chudoon"),
        s(ROOM_N, "sad_black_dog", "ザクザクではなく\nボロボロ"),
        s(ROOM_N, "eat_pop_cat", "てりやきソースを\nかける"),
        s(ROOM_N, "calm_black_face_sheep", "うまい\nけど\nちがう"),
        s(ROOM_N, "realize_wet_cat_stare", "スイートレモンが\n足りない"),
        s(ROOM_N, "rizz_cat_rizz", "プロの仕事は\nやっぱりすごい"),
        s(ROOM_N, "sleepy_sleepy_cat", "てりやきの夢を\n見る"),
        s(ROOM_N, "realize_wet_cat_stare", "マックさん"),
        s(ROOM_N, "excited_hodomoe_city_cat", "はやく\n再開してくれ", se="pikon", dur=3.8),
        J.end_card(),
    ]


def place(cs):
    J.diversify(cs)
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_19_mac.mp4"), os.path.join(J.HERE, "out", "jidaraku_19_mac_preview"))
