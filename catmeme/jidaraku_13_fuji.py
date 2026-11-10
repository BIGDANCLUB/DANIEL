"""自堕落シリーズ #13：30代独身男、ひとりで富士山登頂（11/7 ユーザー指定の流れ・8〜12分）。

python3 catmeme/jidaraku_13_fuji.py → out/jidaraku_13_fuji.mp4
- 流れ（ユーザー指定）：日本の最高峰を見ずに生涯を終えられない → 5合目（ハンター試験の会場・トンパのようなビギナー潰しもいるはず）→
  救助される人とすれちがう・油断しない → 登るほど標高と自販機の値段が上がり、酸素と財布が薄くなる（財布は登山前から薄い）→
  山小屋で1泊（足がくさい・俺もくさいと思われている）→ 起きるとおにぎり（命をもらったに等しい）→ 日の出前に登頂・ご来光 →
  空腹・山頂でカップラーメン（うますぎる・高すぎる・高すぎる（値段が））→ 下山こそ本番 → 筋肉痛で月曜に有給 → 家に何もない・ウーバー →
  富士山は最後の最後まで財布を薄くしてくる場所だ
- 登山の情報（2026年）：吉田ルートは事前予約・通行料1人4000円・7月1日開山／5合目は標高約2300m／山頂は3776m／
  高山病はゆっくり登るのが大事・7合目〜8合目の山小屋に泊まる人が多い／山梨側は7合目より上ならご来光が見える／ご来光は4時半〜5時ごろ
  山の上の値段の数字は出さない（店で変わる）。救助される人をからかわない
- ベンチマーク3チャンネルに富士山の回はない（11/7 確認）
- 写真は backgrounds/jidaraku/13_fuji に置く。届くまでは手もちのイラストで仮に（ほかの店の写真は使わない）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "13_fuji"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku", "01_yakiniku")]
ROOM, ROOM_N, BUS, FIVE, TRAIL, HIGH, HUT, SUMMIT, DOWN, OFFICE = (
    "j01_room", "j07_room_night", "fj00_bus", "fj01_5gome", "fj02_trail", "fj03_trail_high", "fj04_hut", "fj05_summit",
    "fj06_descent", "bg25_office_desk")
NIGHTB = "fj07_night"   # 11/9 夜の登山道の写真
J.STANDIN.update({BUS: "bg26_rural_road", DOWN: "fj03_trail_high"})   # 11/8 写真5枚（5合目・登山道・雲の上の道・山小屋・山頂）。下山は雲の上の砂ぼこりの道の写真で
J.HOLD = 4   # ミスド・ゴンチャと同じ切り替えの数
J.LOOPS = 1   # 11/9 ユーザー指定：素材はくり返さない（終わる前の文で替える）
J.SUB_STYLE = "glow"
J.MAXLEN = {a: 6.0 for a in ("joy_happy_happy_happy_cat", "happy_chipi_chapa_cat", "happy_girlfriend_dance_cat")}   # 11/10 ユーザー指定：1回6秒まで（はじめは9秒）
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
VEND, CURRY, ONIGIRI, SUN, RAMEN, UBER = ("f_vending", "f_hut_curry", "f_onigiri", "f_goraiko", "f_cupramen", "f_uber")


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 決意 ----
        s(ROOM, "sleepy_old_memories_cat", "金曜日の夜\nテレビを見ていた", bgm={"file": LOFI, "gain": -12}),
        dict(s(ROOM, "surprise_big_pupils_cat", "画面いっぱいの\n富士山"), new=True),   # 11/9 ユーザー指定：素材を変える
        s(ROOM, "surprise_big_pupils_cat", "雲の上から\n朝日がのぼる"),
        s(ROOM, "think_chin_paw_orange_cat", "そういえば俺"),
        s(ROOM, "sad_looking_away_tabby", "富士山に\n登ったことがない"),
        s(ROOM, "realize_wet_cat_stare", "新幹線の窓から\n見ただけだ"),
        s(ROOM, "think_bike_front_seat_cat", "このまま\n日本の最高峰を見ずして"),
        s(ROOM, "angry_aiming_cat", "生涯を終えられる\nわけがない", se="explosion_chudoon"),
        s(ROOM, "excited_hodomoe_city_cat", "登るぞ\n富士山", se="shine_kiraan_maou"),
        s(ROOM, "work_typing_cat", "まずは\nスマホで調べる"),
        s(ROOM, "read_book_orange_kitten", "吉田ルートは\n事前の予約が必要"),
        s(ROOM, "money_counting_orange_cat", "通行料は\n1人4000円"),
        s(ROOM, "huh_huh_cat", "登る前から\nお金がかかる"),
        s(ROOM, "read_book_orange_kitten", "山小屋に泊まって\nゆっくり登るのが\nおすすめらしい"),
        s(ROOM, "calm_black_face_sheep", "高山病に\nならないためだ"),
        s(ROOM, "work_typing_cat", "山小屋も予約する"),
        s(ROOM, "stare_lying_tabby_cat", "登山靴\nレインウェア\nヘッドライト"),
        s(ROOM, "money_counting_orange_cat", "道具をそろえたら\n財布が\nすでに薄い", se="pi"),
        s(ROOM, "rizz_cat_rizz", "でも\nもう引き返せない"),
        s(ROOM, "think_chin_paw_orange_cat", "ふと\n不安になる"),
        s(ROOM, "stare_tabby_wide_eyes_cat", "最後に運動したのは\nいつだったか"),
        s(ROOM, "sleepy_old_memories_cat", "たぶん\n学生のころの\n体育祭だ"),
        s(ROOM, "angry_shooting_cat", "前の日に\n近所の坂道を\n3往復する"),
        s(ROOM, "despair_dramatic_kitten", "3往復目で\n息が切れた"),
        s(ROOM, "calm_black_face_sheep", "……まあ\nなんとかなる"),
        # ---- 5合目 ----
        s(BUS, "drive_driving_cat", "土曜日の朝\nバスで5合目へ", se="whoosh_shu", bgm={"file": MORNING, "gain": -12, "fade": 0.8}),
        s(BUS, "sleepy_sleepy_cat", "窓の外が\nどんどん緑になる"),
        s(BUS, "stare_tabby_wide_eyes_cat", "耳が\nキーンとする"),
        s(FIVE, "leave_cat_leaves_home", "富士山5合目", se="gong_dora_jaan", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(FIVE, "read_book_orange_kitten", "標高は\nもう2300m"),
        s(FIVE, "surprise_big_pupils_cat", "ここが\nみんなのスタート地点"),
        s(FIVE, "stare_interviewer_cat", "外国からの登山客\n大学生のグループ\nベテランのおじさん"),
        s(FIVE, "peek_what_happen_cat", "みんな\nここから始まる登山に\n息巻いている"),
        s(FIVE, "think_chin_paw_orange_cat", "この空気\nどこかで見たことがある"),
        s(FIVE, "showoff_gojo_cosplay_cat", "まるで\nハンター試験の\n会場みたいだ", se="explosion_chudoon"),
        s(FIVE, "stare_big_eyes_tabby_kitten", "受験番号のかわりに\n登山の予約画面"),
        s(FIVE, "glare_disgusted_cat", "どこかに\nトンパみたいな\nビギナー潰しもいるに\nちがいない"),
        s(FIVE, "peek_what_happen_cat", "親切そうに\nジュースを\nくれるおじさんには\n気をつけよう"),
        s(FIVE, "calm_black_face_sheep", "だれも\nくれなかった"),
        s(FIVE, "stare_tabby_wide_eyes_cat", "みんなの装備を\nこっそり見る"),
        s(FIVE, "surprise_big_pupils_cat", "ストック2本\nヘルメット\n本格的な人もいる"),
        s(FIVE, "sad_looking_away_tabby", "俺の登山靴は\nまだ値札のあとが\nついている"),
        s(FIVE, "money_counting_orange_cat", "売店で\n金剛杖を買う"),
        s(FIVE, "read_book_orange_kitten", "山小屋ごとに\n焼き印を押して\nもらえるらしい"),
        s(FIVE, "rizz_cat_rizz", "杖が\nスタンプカードになる"),
        s(FIVE, "read_book_orange_kitten", "まずは5合目で\n体を高さに\nならす"),
        s(FIVE, "sleepy_sleepy_cat", "1時間\nベンチで休む"),
        s(FIVE, "stare_lying_tabby_cat", "もう\nちょっと帰りたい"),
        s(FIVE, "yell_orange_fat_cat", "出発", se="gong_match_start"),
        # ---- 6合目〜7合目 ----
        s(TRAIL, "walk_approaching_orange_cat", "歩きはじめは\nなだらかな道", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(TRAIL, "happy_chipi_chapa_cat", "なんだ\nよゆうじゃないか"),
        s(TRAIL, "stare_big_eyes_tabby_kitten", "6合目"),
        s(TRAIL, "surprise_big_pupils_cat", "道が\nいきなり\nジグザグになる"),
        s(TRAIL, "despair_dramatic_kitten", "息が\nもう上がっている"),
        s(TRAIL, "peek_what_happen_cat", "上から\n救助される人が\n下りてきた"),
        s(TRAIL, "sad_looking_away_tabby", "具合が\n悪くなったらしい"),
        s(TRAIL, "think_chin_paw_orange_cat", "富士山は\nなめてはいけない"),
        s(TRAIL, "angry_aiming_cat", "ああいう状況には\nなりたくない"),
        s(TRAIL, "rizz_cat_rizz", "油断せずに行こう"),
        s(TRAIL, "read_book_orange_kitten", "高山病の対策は\nゆっくり歩く\nこまめに水を飲む"),
        s(TRAIL, "calmdown_dancing_cat", "深呼吸しながら\n一歩ずつ"),
        s(TRAIL, "stare_tabby_wide_eyes_cat", "7合目"),
        s(TRAIL, "surprise_big_pupils_cat", "ここから\n岩場になる"),
        s(TRAIL, "punch_tabby_cat_reach", "両手も使って\nよじ登る"),
        s(TRAIL, "despair_dramatic_kitten", "これは\nもう登山じゃない\nクライミングだ"),
        s(TRAIL, "peek_what_happen_cat", "うしろを\nふり返る"),
        s(TRAIL, "joy_happy_happy_happy_cat", "雲が\n足もとにある", se="shine_kiraan_maou"),
        s(TRAIL, "sleepy_old_memories_cat", "下で見ていた雲を\n今は上から見ている"),
        s(TRAIL, "happy_hamster_open_arms", "がんばった分だけ\n景色が\nごほうびをくれる"),
        s(TRAIL, "stare_big_eyes_tabby_kitten", "山小屋で\n杖に焼き印を\n押してもらう"),
        s(TRAIL, "happy_chipi_chapa_cat", "ジュッ\nといい音"),
        s(TRAIL, "money_counting_orange_cat", "焼き印も\n1つずつ\nお金がかかる"),
        s(TRAIL, "think_chin_paw_orange_cat", "でも\n集めたくなる"),
        s(TRAIL, "sad_black_dog", "スタンプカードは\n昔から\nやめられない"),
        # ---- 自販機 ----
        s(TRAIL, "stare_big_eyes_tabby_kitten", "山小屋の前に\n自販機", item=VEND),
        s(TRAIL, "huh_huh_cat", "値段が\n下界とちがう", item=VEND, se="question_mark_pop_confused_huh"),
        s(TRAIL, "read_book_orange_kitten", "荷物は\n人やブルドーザーで\n運び上げているらしい", item=VEND),
        s(TRAIL, "calm_black_face_sheep", "それなら\n高くて当然だ", item=VEND),
        s(TRAIL, "think_chin_paw_orange_cat", "登るにつれて", item=VEND),
        s(TRAIL, "surprise_big_pupils_cat", "標高と\n自販機の値段が\n高くなっていく", item=VEND),
        s(TRAIL, "despair_dramatic_kitten", "そして\n酸素濃度と財布が\n薄くなっていくのだ", item=VEND, se="explosion_chudoon"),
        s(TRAIL, "sad_black_dog", "なお財布は\n登山前から\nすでに薄い", item=VEND),
        s(TRAIL, "money_counting_orange_cat", "スポーツドリンクを\n1本だけ買う", item=VEND),
        s(TRAIL, "eat_crunchy_cat_luna", "ゴクゴク……", item=VEND, se="drink_gulp_gokugoku_thirsty_chug"),
        s(TRAIL, "happy_girlfriend_dance_cat", "体に\nしみわたる", item=VEND),
        s(TRAIL, "realize_wet_cat_stare", "値段のことは\n忘れた", item=VEND),
        # ---- 8合目 ----
        s(HIGH, "walk_approaching_orange_cat", "8合目", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(HIGH, "stare_tabby_wide_eyes_cat", "空気が\nうすい"),
        s(HIGH, "blank_black_cat_zoning_out", "10歩あるいて\n休む"),
        s(HIGH, "sleepy_sleepy_cat", "また10歩あるいて\n休む"),
        s(HIGH, "peek_what_happen_cat", "ベテランのおじさんに\n抜かれる"),
        s(HIGH, "stare_interviewer_cat", "がんばってねー"),
        s(HIGH, "joy_happy_happy_happy_cat", "トンパじゃなかった"),
        s(HIGH, "happy_hamster_open_arms", "山の人は\nみんなやさしい"),
        s(HIGH, "despair_dramatic_kitten", "頭が\n少しぼんやりする"),
        s(HIGH, "read_book_orange_kitten", "今日はここで\n山小屋に泊まる"),
        # ---- 山小屋 ----
        s(HUT, "stare_interviewer_cat", "いらっしゃい\nおつかれさまでしたー", se="pinpon_notice", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(HUT, "happy_chipi_chapa_cat", "やっと\n座れる"),
        s(HUT, "stare_big_eyes_tabby_kitten", "夕ごはんは\nカレー", item=CURRY),
        s(HUT, "eat_crunchy_cat_luna", "もぐもぐ", item=CURRY),
        s(HUT, "surprise_big_pupils_cat", "標高3000mで\n食べるカレーが\nうまい", item=CURRY),
        s(HUT, "sleepy_old_memories_cat", "林間学校を\n思い出す", item=CURRY),
        s(HUT, "read_book_orange_kitten", "夜は\n知らない人と\nならんで寝る"),
        s(HUT, "calm_black_face_sheep", "となりとの間は\n肩がふれるくらい"),
        s(HUT, "peek_what_happen_cat", "外に出ると\n夕日"),
        s(HUT, "surprise_big_pupils_cat", "雲の海が\nオレンジ色に\nそまっている"),
        s(HUT, "sleepy_old_memories_cat", "影富士が\n雲の上にのびる"),
        s(HUT, "happy_hamster_open_arms", "ここまで来た人だけが\n見られる景色だ"),
        s(HUT, "stare_tabby_wide_eyes_cat", "夜は\n星がこわいくらい\n近い"),
        s(HUT, "blank_black_cat_zoning_out", "寒い\n真夏なのに\nダウンを着る"),
        s(HUT, "stare_lying_tabby_cat", "電気が消える"),
        s(HUT, "glare_disgusted_cat", "……くさい"),
        s(HUT, "huh_huh_cat", "ほかの人の足\nくせぇ", se="question_mark_pop_confused_huh"),
        s(HUT, "realize_wet_cat_stare", "いや\nまてよ"),
        s(HUT, "sad_looking_away_tabby", "俺も1日中\n歩いてきた"),
        s(HUT, "despair_dramatic_kitten", "たぶん\nほかの人にも\n俺の足くせぇと\n思われている"),
        s(HUT, "calmdown_dancing_cat", "おたがいさまだ"),
        s(HUT, "snore_snoring_dog", "どこかから\nいびき"),
        s(HUT, "stare_tabby_wide_eyes_cat", "ねむれない"),
        s(HUT, "sleep_sleeping_cat", "……いつの間にか\nねむっていた"),
        # ---- 出発・おにぎり ----
        s(HUT, "stare_big_eyes_tabby_kitten", "夜中の1時\n起きる", se="pi"),
        s(HUT, "stare_interviewer_cat", "これ\n朝ごはんです", item=ONIGIRI),
        s(HUT, "surprise_big_pupils_cat", "おにぎりを\nもらった", item=ONIGIRI),
        s(HUT, "sad_banana_cat_cry", "この高さで\nこのおにぎり", item=ONIGIRI),
        s(HUT, "happy_hamster_open_arms", "命をもらったに\n等しい", item=ONIGIRI, se="shine_kiraan_maou"),
        s(HUT, "work_typing_cat", "ヘッドライトを\nつける"),
        s(NIGHTB, "walk_approaching_orange_cat", "まっくらな中\n頂上をめざす", se="whoosh_shu", bgm={"file": LOFI, "gain": -12, "fade": 0.8}),
        s(NIGHTB, "peek_what_happen_cat", "上を見ると\nヘッドライトの列が\n光の川みたいだ"),
        s(NIGHTB, "stare_tabby_wide_eyes_cat", "下を見ると\n街の明かり"),
        s(NIGHTB, "blank_black_cat_zoning_out", "寒い\n息が白い"),
        s(NIGHTB, "despair_dramatic_kitten", "9合目\n足が重い"),
        s(NIGHTB, "think_bike_front_seat_cat", "でも\nここまで来て\n引き返せない"),
        s(NIGHTB, "angry_shooting_cat", "最後の\n鳥居が見えた", se="explosion_chudoon"),
        # ---- 山頂 ----
        s(SUMMIT, "showoff_gojo_cosplay_cat", "山頂", se="gong_dora_jaan", bgm={"file": MORNING, "gain": -12, "fade": 0.8}),
        s(SUMMIT, "read_book_orange_kitten", "標高3776m\n日本でいちばん\n高い場所"),
        s(SUMMIT, "joy_happy_happy_happy_cat", "日の出前に\nなんとか\n登りきった"),
        s(SUMMIT, "stare_big_eyes_tabby_kitten", "東の空が\nオレンジ色になる", item=SUN),
        s(SUMMIT, "surprise_big_pupils_cat", "ご来光", item=SUN, se="shine_kiraan_maou"),
        s(SUMMIT, "sad_banana_cat_cry", "美しい", item=SUN),
        s(SUMMIT, "realize_wet_cat_stare", "雲の上から\n朝日がのぼる", item=SUN),
        s(SUMMIT, "sleepy_old_memories_cat", "テレビで見た\nあの景色だ", item=SUN),
        s(SUMMIT, "stare_interviewer_cat", "まわりから\n拍手とバンザイ", item=SUN),
        s(SUMMIT, "happy_girlfriend_dance_cat", "知らない人と\nハイタッチ", item=SUN),
        s(SUMMIT, "happy_hamster_open_arms", "登りきった\n達成感", item=SUN),
        s(SUMMIT, "think_chin_paw_orange_cat", "そして\nいっしょに訪れる"),
        s(SUMMIT, "sulk_hungry_cat", "空腹", se="pi"),
        s(SUMMIT, "eat_pop_cat", "おにぎりは\n当然うまい", item=ONIGIRI),
        s(SUMMIT, "think_bike_front_seat_cat", "でも\nここで食べたいものと\n言えば\nひとつ"),
        s(SUMMIT, "rizz_cat_rizz", "そう", item=RAMEN),
        s(SUMMIT, "excited_hodomoe_city_cat", "カップラーメンだ", item=RAMEN, se="explosion_dokaan"),
        s(SUMMIT, "stare_big_eyes_tabby_kitten", "山頂の売店で\nお湯を入れてもらう", item=RAMEN),
        s(SUMMIT, "read_book_orange_kitten", "空気がうすいと\nお湯がぬるめに\nわくらしい", item=RAMEN),
        s(SUMMIT, "think_chin_paw_orange_cat", "3分待つ", item=RAMEN),
        s(SUMMIT, "eat_crunchy_cat_luna", "ズズッ", item=RAMEN, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SUMMIT, "surprise_big_pupils_cat", "うますぎる", item=RAMEN),
        s(SUMMIT, "happy_girlfriend_dance_cat", "塩気が\n体中にしみる", item=RAMEN),
        s(SUMMIT, "stare_tabby_wide_eyes_cat", "高すぎる", item=RAMEN),
        s(SUMMIT, "despair_dramatic_kitten", "高すぎる\n（値段が）", item=RAMEN, se="explosion_chudoon"),
        s(SUMMIT, "calm_black_face_sheep", "でも\nこの高さまで\n運んでくれた人がいる", item=RAMEN),
        s(SUMMIT, "happy_hamster_open_arms", "それを思えば\n安いものだ", item=RAMEN),
        s(SUMMIT, "sad_black_dog", "財布は\nさらに薄くなった", item=RAMEN),
        # ---- 下山 ----
        s(DOWN, "leave_cat_leaves_home", "下山開始", se="whoosh_shu", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(DOWN, "happy_chipi_chapa_cat", "あとは\n下りるだけ"),
        s(DOWN, "think_chin_paw_orange_cat", "……と\n思っていた"),
        s(DOWN, "read_book_orange_kitten", "吉田ルートの下山道は\n砂利のジグザグ道"),
        s(DOWN, "surprise_big_pupils_cat", "ずっと\n同じ景色"),
        s(DOWN, "despair_dramatic_kitten", "足がすべる"),
        s(DOWN, "scream_standing_marmot", "ひざが\n笑っている"),
        s(DOWN, "stare_tabby_wide_eyes_cat", "つま先が\n靴の先にあたって\n痛い"),
        s(DOWN, "angry_aiming_cat", "油断ならない"),
        s(DOWN, "realize_wet_cat_stare", "というか\n足との闘いという\n意味では"),
        s(DOWN, "showoff_gojo_cosplay_cat", "下山こそ本番だ", se="explosion_chudoon"),
        s(DOWN, "blank_black_cat_zoning_out", "砂ぼこりで\n顔が真っ黒"),
        s(DOWN, "peek_what_happen_cat", "ジグザグの\n曲がり角を数える"),
        s(DOWN, "sleepy_sleepy_cat", "途中で\n数えるのをやめた"),
        s(DOWN, "peek_what_happen_cat", "これから登る人と\nすれちがう"),
        s(DOWN, "stare_interviewer_cat", "がんばってくださーい"),
        s(DOWN, "happy_chipi_chapa_cat", "昨日のおじさんと\n同じことを\n言っている"),
        s(DOWN, "rizz_cat_rizz", "俺も\n山の人に\nなったのかもしれない"),
        s(DOWN, "despair_dramatic_kitten", "その直後に\nころぶ"),
        s(DOWN, "sad_looking_away_tabby", "山の人には\nまだ早かった"),
        s(DOWN, "stare_big_eyes_tabby_kitten", "5合目が\n見えてきた"),
        s(FIVE, "joy_happy_happy_happy_cat", "5合目に\n帰ってきた", se="gong_dora_jaan"),
        s(FIVE, "happy_hamster_open_arms", "ハンター試験\n合格だ"),
        s(FIVE, "laugh_laughing_dog", "だれも\n認めてくれない"),
        s(FIVE, "money_counting_orange_cat", "おみやげの\n富士山クッキーを買う"),
        s(FIVE, "sad_black_dog", "財布が\nまた薄くなる"),
        s(BUS, "sleep_sleeping_cat", "帰りのバスで\n気絶するように寝る", se="whoosh_shu"),
        # ---- 筋肉痛・月曜日 ----
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(ROOM, "stare_big_eyes_tabby_kitten", "日曜日の朝"),
        s(ROOM, "scream_standing_marmot", "起き上がれない", se="explosion_chudoon"),
        s(ROOM, "despair_dramatic_kitten", "筋肉痛\n痛すぎる"),
        s(ROOM, "sad_looking_away_tabby", "ふともも\nふくらはぎ\nおしり"),
        s(ROOM, "stare_lying_tabby_cat", "トイレまで\n5分かかる"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "階段を\n後ろ向きに下りる"),
        s(ROOM, "huh_huh_cat", "前向きだと\nひざが言うことを\nきかない"),
        s(ROOM, "work_typing_cat", "スマホで\n筋肉痛\n治し方"),
        s(ROOM, "read_book_orange_kitten", "まずは\nしっかり休むこと"),
        s(ROOM, "sleepy_sleepy_cat", "それなら\n得意だ"),
        s(ROOM, "think_chin_paw_orange_cat", "明日は\n月曜日"),
        s(ROOM, "blank_black_cat_zoning_out", "この足で\n満員電車は\nむりだ"),
        s(ROOM, "call_customer_service_cat", "上司にメール"),
        s(ROOM, "work_typing_cat", "体調不良のため\nお休みを……"),
        s(ROOM, "sad_banana_cat_cry", "結局\n月曜日\n有給とってしまった"),
        s(ROOM_N, "sulk_hungry_cat", "腹が減った"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "冷蔵庫を開ける"),
        s(ROOM_N, "calm_black_face_sheep", "何もない"),
        s(ROOM_N, "despair_dramatic_kitten", "買いに行く足が\nない"),
        s(ROOM_N, "scream_phone_orange_cat", "ウーバー\nたのむしかない", item=UBER, se="pi"),
        s(ROOM_N, "money_counting_orange_cat", "配達料\nサービス料", item=UBER),
        s(ROOM_N, "sad_black_dog", "財布が\nまた薄くなる", item=UBER),
        s(ROOM_N, "realize_wet_cat_stare", "そうか", item=UBER),
        s(ROOM_N, "think_bike_front_seat_cat", "富士山は\n最後の最後まで", item=UBER),
        s(ROOM_N, "showoff_gojo_cosplay_cat", "財布を薄くしてくる\n場所だ", item=UBER, se="gong_dora_jaan"),
        s(ROOM_N, "sleepy_old_memories_cat", "でも\nあのご来光は\nお金では買えない", item=SUN),
        s(ROOM_N, "happy_hamster_open_arms", "スマホの写真を\n何度も見返す", item=SUN),
        s(ROOM_N, "excited_hodomoe_city_cat", "次は\n足をきたえてから\nまた来よう", se="pikon", dur=3.8),
        J.end_card(),
    ]


def place(cs):
    J.diversify(cs)   # 11/9 ユーザー指定：もっと多様な素材を
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_13_fuji.mp4"), os.path.join(J.HERE, "out", "jidaraku_13_fuji_preview"))
