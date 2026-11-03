"""自堕落シリーズ #8：30代独身男、月曜日にひとりで鳥貴族（11/3 ユーザー指定の流れ・ブロンコビリー/IKEAと同じ作り）。約7〜8分。

python3 catmeme/jidaraku_08_torikizoku.py → out/jidaraku_08_torikizoku.mp4
- 流れ（ユーザー指定）：月曜から飲みたい → 普段は混んでいて行きにくい鳥貴族へ → 安く飲み食いできる・居酒屋ランキングで1位の常連 →
  今日はあえて野獣になる（食べたいものを全部頼んでいい・意訳）→ 金麦（大）が他のドリンクと同じ値段（バグか？）→
  スピードメニューの最推し「ホルモンねぎポン酢」→ むね貴族焼スパイス（むねスパ）→ せせり・ハート塩 → メガハイボール（バグだ）→
  キモのネギごま油・ピーマン肉詰め（このラインナップが好きなオッサン多いはず）→ 山芋の鉄板焼（昔はとろろ焼・紅しょうがとタコ）→
  ZIMA があれば…（ハイボールのジョッキに入れてレモンを絞る）→ それじゃあゆっくり食べていくよー → 満腹 → 会計
- 値段の数字は出さない（全品均一なのは言う）。ランキングの名前は出さない（「居酒屋のランキングで1位の常連」）
- 写真がない料理は字幕だけ（写真が届いたら backgrounds/jidaraku/08_torikizoku に置く）
- 「40代独身の何気ない日常」に鳥貴族の回があるが、11/3 ユーザー指定で作る（流れ・言い回しはユーザーの原稿をもとにした別物）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "08_torikizoku"))
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku", d) for d in ("04_sushiro", "05_gokurakuyu", "06_bronco", "07_ikea")]
OFFICE, STREET, FRONT, IN, COUNTER, ROAD, ROOM_N = ("bg25_office_desk", "bg51_night_street", "t01_front", "t02_inside", "t03_counter",
                                                    "b06_road_night", "j07_room_night")
J.STANDIN.update({FRONT: "bg51_night_street", IN: "bg98_izakaya_night", COUNTER: "bg13_izakaya"})
NIGHT = {OFFICE: 0.85}
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
# 料理の写真（届いた順に backgrounds/jidaraku/08_torikizoku に置く）
BEER, HORMON, MUNE, SESERI, HEART, HIGH, KIMO, PIMAN, YAMAIMO = (
    "f_highball", "f_hormon", "f_mune_spice", "f_seseri", "f_heart", "f_highball", "f_kimo", "f_piman", "f_yamaimo")
ZIMA = "f_zima"


def cuts():
    def s(*a, **k):   # 長さは place() で字幕の文字数から決める
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 月曜日 ----
        s(OFFICE, "work_typing_cat", "月曜日の夜7時", bgm={"file": LOFI, "gain": -12}),
        s(OFFICE, "blank_black_cat_zoning_out", "週のはじめから\nもう疲れている"),
        s(OFFICE, "sleepy_old_memories_cat", "まだ火曜も水曜も\n木曜も金曜もある"),
        s(OFFICE, "despair_dramatic_kitten", "……4日も\nあるのか"),
        s(OFFICE, "sad_looking_away_tabby", "月曜日の朝の\n会議は長い"),
        s(OFFICE, "work_typing_cat", "メールは\n週末のぶんまで\nたまっている"),
        s(OFFICE, "sulk_hungry_cat", "お昼ごはんも\nデスクで食べた"),
        s(OFFICE, "think_chin_paw_orange_cat", "こんな日は\n飲みに行きたい"),
        s(OFFICE, "stare_tabby_wide_eyes_cat", "できれば\nふだんは混んでいて\n行きにくい店に"),
        s(OFFICE, "read_book_orange_kitten", "金曜や土曜は\n行列ができている\nあの店"),
        s(OFFICE, "stare_big_eyes_tabby_kitten", "でも月曜の夜なら……", se="question_hatena_maou"),
        s(OFFICE, "happy_chipi_chapa_cat", "そう\n鳥貴族だ", se="shine_kiraan_maou"),   # 11/3：明るい素材に
        # ---- 来店 ----
        s(FRONT, "leave_cat_leaves_home", "会社を出て\nまっすぐ向かう", se="whoosh_shu", bgm={"file": L.PURPLE, "gain": -12, "fade": 0.8}),
        s(FRONT, "surprise_big_pupils_cat", "鳥貴族", se="gong_dora_jaan"),
        s(FRONT, "read_book_orange_kitten", "安く飲み食いできる店で\n有名だ"),
        s(FRONT, "showoff_gojo_cosplay_cat", "メニューは\n全品同じ値段"),
        s(FRONT, "think_chin_paw_orange_cat", "焼き鳥も\nドリンクも\n釜めしも同じ値段"),
        s(FRONT, "confused_i_dont_know_cat", "どういう計算で\n成り立っているのか\nわからない"),
        s(FRONT, "rizz_cat_rizz", "わからないが\nありがたい"),
        s(FRONT, "stare_interviewer_cat", "店の前を\nのぞいてみる"),
        s(FRONT, "happy_chipi_chapa_cat", "並んでいない！"),
        s(FRONT, "calmdown_dancing_cat", "月曜日の\n奇跡だ"),
        s(FRONT, "stare_interviewer_cat", "なんとかという\n居酒屋ランキングでも\n不動の1位だ"),
        s(FRONT, "think_bike_front_seat_cat", "名前は\n忘れたけど\nとにかく1位だ"),
        s(FRONT, "sad_looking_away_tabby", "だが"),
        s(FRONT, "sleepy_old_memories_cat", "鳥貴族に行ける機会は\nそう無い"),
        s(FRONT, "despair_dramatic_kitten", "週末は満席\n平日も同僚と行くと\n気をつかう"),
        s(FRONT, "angry_aiming_cat", "ならば今日は"),
        s(FRONT, "excited_hodomoe_city_cat", "あえて\n野獣になってみるべき\nかもしれない", se="explosion_dokaan"),
        s(IN, "stare_interviewer_cat", "いらっしゃいませー\nおひとりさまですか？", se="pinpon_notice"),
        s(IN, "happy_hamster_open_arms", "すんなり\nカウンターへ"),
        s(COUNTER, "calmdown_dancing_cat", "月曜日\n最高だ"),
        s(COUNTER, "peek_what_happen_cat", "店内を見わたす"),
        s(COUNTER, "stare_interviewer_cat", "仕事帰りのサラリーマン\n大学生のグループ"),
        s(COUNTER, "sleepy_old_memories_cat", "カウンターには\nひとり客がちらほら"),
        s(COUNTER, "rizz_cat_rizz", "みんな月曜日と\n戦ってきた戦士たちだ"),
        s(COUNTER, "think_chin_paw_orange_cat", "厨房からは\n焼き鳥を焼くにおい"),
        s(COUNTER, "happy_hamster_open_arms", "においだけで\n1杯いける"),
        # ---- 作戦 ----
        s(COUNTER, "read_book_orange_kitten", "タッチパネルを\n開く"),
        s(COUNTER, "think_chin_paw_orange_cat", "鳥貴族は\n何を食べても\nおいしいと評判だ"),
        s(COUNTER, "showoff_gojo_cosplay_cat", "つまり"),
        s(COUNTER, "rizz_cat_rizz", "食べたいものを\n全部頼んでもいい\nということだ"),
        s(COUNTER, "laugh_laughing_dog", "（意訳）"),
        s(COUNTER, "angry_aiming_cat", "迷っている時間は\nもったいない"),
        s(COUNTER, "confused_i_dont_know_cat", "……と言いつつ\nメニューを3周する"),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "焼き鳥\nサイド\n釜めし\nデザート"),
        s(COUNTER, "despair_dramatic_kitten", "全部\nおいしそう"),
        s(COUNTER, "glare_disgusted_cat", "全品同じ値段なので\n値段で選べない"),
        s(COUNTER, "blank_black_cat_zoning_out", "安いのに\n迷うという\nぜいたくな悩み"),
        # ---- 金麦 ----
        s(COUNTER, "cocky_dj_cat", "まず真っ先に\n金麦の大", item=BEER, se="pikon"),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "これが\n他のドリンクと\n同じ値段だというのだ", item=BEER),
        s(COUNTER, "confused_i_dont_know_cat", "大なのに？", item=BEER),
        s(COUNTER, "surprise_big_pupils_cat", "バグか？", item=BEER, se="question_mark_pop_confused_huh"),
        s(COUNTER, "eat_crunchy_cat_luna", "ゴクッ……\nくぅ〜！", item=BEER, se="drink_gulp_gokugoku_thirsty_chug"),
        s(COUNTER, "happy_girlfriend_dance_cat", "月曜日の疲れが\n泡と一緒に\n消えていく"),
        s(COUNTER, "sleepy_old_memories_cat", "会議で言えなかった\nあの一言も"),
        s(COUNTER, "realize_wet_cat_stare", "上司の\n月曜から元気ないねも"),
        s(COUNTER, "happy_hamster_open_arms", "全部\n泡になって消えた"),
        s(COUNTER, "sleepy_old_memories_cat", "そういえば\nかなり前は"),
        s(COUNTER, "think_chin_paw_orange_cat", "金麦ではなく\n淡麗の大ジョッキを\n出していた時期もあった"),
        s(COUNTER, "read_book_orange_kitten", "とり平焼きという\nメニューもあった"),
        s(COUNTER, "sad_banana_cat_cry", "好きだった"),
        s(COUNTER, "realize_wet_cat_stare", "メニューが変わっても\nこの店に来ると\nなぜか落ち着く"),
        # ---- スピードメニュー ----
        s(COUNTER, "work_typing_cat", "そして\nスピードメニューだ"),
        s(COUNTER, "read_book_orange_kitten", "焼き鳥を待つあいだに\nすぐ出てくる\nおつまみ"),
        s(COUNTER, "showoff_gojo_cosplay_cat", "俺の最推し\nスピードメニューは"),
        s(COUNTER, "excited_hodomoe_city_cat", "ホルモン\nねぎポン酢", item=HORMON, se="gong_dora_jaan"),
        s(COUNTER, "eat_pop_cat", "あっさりな味わいに", item=HORMON),
        s(COUNTER, "happy_hamster_open_arms", "ネギとポン酢の\n香ばしさが\nたまらない", item=HORMON),
        s(COUNTER, "think_chin_paw_orange_cat", "しかも\nやわらかい部位と", item=HORMON),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "歯ごたえしっかりの部位が\nまざっている", item=HORMON),
        s(COUNTER, "realize_wet_cat_stare", "やわらかい\nコリコリ\nやわらかい", item=HORMON),
        s(COUNTER, "rizz_cat_rizz", "おつまみとして\nあまりにも\n完成している一皿だ", item=HORMON),
        s(COUNTER, "eat_crunchy_cat_luna", "金麦が\nすすむ", item=BEER),
        s(COUNTER, "peek_what_happen_cat", "厨房を\nのぞいてみる"),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "店員さんが\n1本ずつ串を\n焼いている"),
        s(COUNTER, "think_chin_paw_orange_cat", "店で串を刺している\nと聞いたことがある"),
        s(COUNTER, "happy_girlfriend_dance_cat", "この値段で\nこの手間"),
        s(COUNTER, "sad_banana_cat_cry", "ありがたすぎて\n泣けてくる"),
        # ---- むねスパ ----
        s(COUNTER, "stare_tabby_wide_eyes_cat", "さて\n頼んだ料理が来た", se="pinpon_notice"),
        s(COUNTER, "showoff_gojo_cosplay_cat", "いちばんの\nおすすめは"),
        s(COUNTER, "surprise_big_pupils_cat", "むね貴族焼の\nスパイス", item=MUNE, se="explosion_dokaan"),
        s(COUNTER, "read_book_orange_kitten", "通称\nむねスパ", item=MUNE),
        s(COUNTER, "eat_crunchy_cat_luna", "たんぱくだけど\nやわらかい肉", item=MUNE),
        s(COUNTER, "happy_girlfriend_dance_cat", "ほんのり浮かんだ油に\nまとわりつく\n強めのスパイス", item=MUNE),
        s(COUNTER, "yell_orange_fat_cat", "これが\nたまらない！", item=MUNE),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "なにより\nこの大きさ", item=MUNE),
        s(COUNTER, "happy_hamster_open_arms", "これを1人で\n独占できる", item=MUNE),
        s(COUNTER, "angry_shooting_cat", "肉食動物に\nなった気分だ", item=MUNE),
        s(COUNTER, "sleepy_old_memories_cat", "同僚と来たら\n取り分けて\n1切れずつだった"),
        s(COUNTER, "rizz_cat_rizz", "ひとり飲みの\n特権だ"),
        s(COUNTER, "think_bike_front_seat_cat", "最後の1切れを\n誰が食べるか\n気をつかわなくていい"),
        s(COUNTER, "happy_chipi_chapa_cat", "最後の1切れも\n最初の1切れも\n全部俺のもの"),
        # ---- せせり・ハート ----
        s(COUNTER, "think_bike_front_seat_cat", "ほかにも\n定番の人気焼き鳥といえば"),
        s(COUNTER, "work_typing_cat", "せせりと\nハート塩", item=SESERI, se="pikon"),
        s(COUNTER, "eat_pop_cat", "かかっている\nガーリックパウダーが\nたまらない", item=HEART),
        s(COUNTER, "eat_crunchy_cat_luna", "せせりはやわらかく", item=SESERI),
        s(COUNTER, "surprise_big_pupils_cat", "噛むと\n肉汁があふれる", item=SESERI),
        s(COUNTER, "happy_chipi_chapa_cat", "たまらない", item=SESERI),
        s(COUNTER, "blank_black_cat_zoning_out", "さっきから\nたまらないしか\n言っていない"),
        s(COUNTER, "calm_black_face_sheep", "でも本当に\nたまらないのだから\nしかたない"),
        s(COUNTER, "think_bike_front_seat_cat", "ここで\nひとつの問題が"),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "焼き鳥は\n串から外すか\nそのまま食べるか"),
        s(COUNTER, "glare_disgusted_cat", "外すと\n焼き鳥への\n冒とくだという人もいる"),
        s(COUNTER, "calmdown_dancing_cat", "でも今日は\nひとりだ"),
        s(COUNTER, "rizz_cat_rizz", "誰にも\n何も言われない"),
        s(COUNTER, "eat_crunchy_cat_luna", "串のまま\nかぶりつく"),
        s(COUNTER, "happy_chipi_chapa_cat", "これが\n正解だ"),
        # ---- メガハイボール ----
        s(COUNTER, "stare_tabby_wide_eyes_cat", "おや", se="pi"),
        s(COUNTER, "sad_looking_away_tabby", "金麦が\nもうない", item=BEER),
        s(COUNTER, "cocky_dj_cat", "次は当然\nメガハイボール", item=HIGH, se="gong_dora_jaan"),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "ジョッキが\n顔くらいある", item=HIGH),
        s(COUNTER, "stare_interviewer_cat", "これが\n他のドリンクと\n同じ値段だというのだ", item=HIGH),
        s(COUNTER, "surprise_big_pupils_cat", "バグだ", item=HIGH, se="explosion_chudoon"),
        s(COUNTER, "eat_crunchy_cat_luna", "シュワッ……\nうまい", item=HIGH, se="drink_gulp_gokugoku_thirsty_chug"),
        s(COUNTER, "happy_girlfriend_dance_cat", "焼き鳥の脂を\n炭酸が流していく", item=HIGH),
        s(COUNTER, "peek_what_happen_cat", "となりの大学生たちが\nもりあがっている"),
        s(COUNTER, "stare_interviewer_cat", "かんぱーい！"),
        s(COUNTER, "sleepy_old_memories_cat", "俺にも\nあんな頃があった"),
        s(COUNTER, "despair_dramatic_kitten", "あの頃の友だちは\nもう子どもが2人いる"),
        s(COUNTER, "cocky_dj_cat", "……ひとりで\nかんぱい"),
        s(COUNTER, "happy_hamster_open_arms", "これも\nいいものだ"),
        # ---- キモ・ピーマン ----
        s(COUNTER, "read_book_orange_kitten", "串焼きといえば\nこれも外せない"),
        s(COUNTER, "work_typing_cat", "キモの\nネギごま油", item=KIMO, se="pikon"),
        s(COUNTER, "eat_pop_cat", "ねっとりしたキモに\nごま油の香り", item=KIMO),
        s(COUNTER, "work_typing_cat", "そして\nピーマンの肉詰め", item=PIMAN, se="pikon"),
        s(COUNTER, "eat_crunchy_cat_luna", "シャキッとしたピーマンに\nジューシーな肉", item=PIMAN),
        s(COUNTER, "think_chin_paw_orange_cat", "このラインナップが\n好きなオッサン", item=PIMAN),
        s(COUNTER, "showoff_gojo_cosplay_cat", "絶対\n多いはず", item=PIMAN),
        s(COUNTER, "sleepy_old_memories_cat", "まわりのカウンターを\nそっと見る"),
        s(COUNTER, "laugh_laughing_dog", "となりのオッサンも\nキモを食べていた"),
        s(COUNTER, "happy_hamster_open_arms", "仲間だ"),
        s(COUNTER, "sad_looking_away_tabby", "目が合った"),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "そっとそらした"),
        s(COUNTER, "calm_black_face_sheep", "オッサン同士の\n無言の会話"),
        # ---- 山芋の鉄板焼 ----
        s(COUNTER, "think_bike_front_seat_cat", "一品料理は\nなんといっても"),
        s(COUNTER, "excited_hodomoe_city_cat", "山芋の\n鉄板焼", item=YAMAIMO, se="gong_dora_jaan"),
        s(COUNTER, "eat_pop_cat", "ジュウジュウの鉄板で\nふわふわ", item=YAMAIMO),
        s(COUNTER, "read_book_orange_kitten", "これも人気メニューだが\n昔は\nとろろ焼というメニューだった", item=YAMAIMO),
        s(COUNTER, "sleepy_old_memories_cat", "紅しょうがとか\nタコも\n入っていた気がする", item=YAMAIMO),
        s(COUNTER, "sad_banana_cat_cry", "あれは\n美味かった", item=YAMAIMO),
        s(COUNTER, "realize_wet_cat_stare", "いや\n今のも美味い", item=YAMAIMO),
        s(COUNTER, "think_chin_paw_orange_cat", "思い出の味は\nいつも少しだけ\n美化されている"),
        s(COUNTER, "calm_black_face_sheep", "でも鉄板の上で\nジュウジュウいう音は\n昔と同じだ"),
        # ---- ZIMA ----
        s(COUNTER, "stare_tabby_wide_eyes_cat", "いつの間にか\nハイボールも\nなくなっていた", se="pi", bgm={"file": PASTEL, "gain": -15, "fade": 0.8}),
        s(COUNTER, "think_chin_paw_orange_cat", "たまーに\n復刻しているが"),
        s(COUNTER, "sleepy_old_memories_cat", "ZIMAがあれば\n迷わず頼んでいた", item=ZIMA),
        s(COUNTER, "showoff_gojo_cosplay_cat", "ハイボールの\nジョッキに\nあれを入れて", item=ZIMA),
        s(COUNTER, "work_typing_cat", "カットレモンを\nもらって\n絞るのが", item=ZIMA),
        s(COUNTER, "happy_chipi_chapa_cat", "最高に\n美味いんだ", item=ZIMA),
        s(COUNTER, "despair_dramatic_kitten", "メニューを探す\nやはり今日は\nない"),
        s(COUNTER, "cocky_dj_cat", "かわりに\nもう1杯\nメガハイボール", item=HIGH),
        s(COUNTER, "sleepy_sleepy_cat", "ほろ酔いで\nメニューを見ると"),
        s(COUNTER, "confused_i_dont_know_cat", "全部\nもう1回\n頼みたくなる"),
        s(COUNTER, "angry_aiming_cat", "野獣は\nまだ満たされていない"),
        s(COUNTER, "think_chin_paw_orange_cat", "そういえば\n釜めしもある"),
        s(COUNTER, "read_book_orange_kitten", "炊きあがるまで\n時間がかかるらしい"),
        s(COUNTER, "showoff_gojo_cosplay_cat", "今のうちに\n頼んでおこう"),
        s(COUNTER, "rizz_cat_rizz", "飲み会の\n上級者の動きだ"),
        # ---- ゆっくり食べる ----
        s(COUNTER, "dance_three_kittens", "それじゃあ\nゆっくり\n食べていくよーーー", se="explosion_dokaan",
          bgm={"file": HIRU, "gain": -6, "fade": 0.8}),
        # 11/3 ユーザー指定：だんだんハイボールの回数が増えていく
        s(COUNTER, "eat_crunchy_cat_luna", "むねスパ", item=MUNE),
        s(COUNTER, "eat_pop_cat", "ホルモン", item=HORMON),
        s(COUNTER, "happy_girlfriend_dance_cat", "ハイボール", item=HIGH),
        s(COUNTER, "eat_crunchy_cat_luna", "せせり", item=SESERI),
        s(COUNTER, "happy_girlfriend_dance_cat", "ハイボール", item=HIGH),
        s(COUNTER, "eat_pop_cat", "キモ", item=KIMO),
        s(COUNTER, "happy_girlfriend_dance_cat", "ハイボール", item=HIGH),
        s(COUNTER, "happy_girlfriend_dance_cat", "ハイボール", item=HIGH),
        s(COUNTER, "eat_crunchy_cat_luna", "ピーマン", item=PIMAN),
        s(COUNTER, "happy_girlfriend_dance_cat", "ハイボール", item=HIGH),
        s(COUNTER, "happy_girlfriend_dance_cat", "ハイボール", item=HIGH),
        s(COUNTER, "happy_girlfriend_dance_cat", "ハイボール", item=HIGH),
        s(COUNTER, "eat_pop_cat", "山芋", item=YAMAIMO),
        s(COUNTER, "happy_girlfriend_dance_cat", "ハイボール", item=HIGH),
        s(COUNTER, "happy_girlfriend_dance_cat", "ハイボール", item=HIGH),
        s(COUNTER, "happy_girlfriend_dance_cat", "ハイボール", item=HIGH),
        s(COUNTER, "happy_girlfriend_dance_cat", "ハイボール", item=HIGH),
        s(COUNTER, "dance_maxwell_cat", "無限ループ"),
        s(COUNTER, "work_typing_cat", "スマホで\n料理の写真を撮る"),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "……送る相手が\nいない"),
        s(COUNTER, "sad_banana_cat_cry", "アルバムの中で\n焼き鳥だけが\n増えていく"),
        s(COUNTER, "rizz_cat_rizz", "焼き鳥は\n俺を裏切らない"),
        s(COUNTER, "sleepy_sleepy_cat", "月曜日のことは\nもう\n忘れた"),
        s(COUNTER, "realize_wet_cat_stare", "明日が火曜日なのも\n忘れた"),
        s(COUNTER, "stare_interviewer_cat", "店員さんの\nお待たせしましたー"),
        s(COUNTER, "surprise_big_pupils_cat", "釜めしが\n来た"),
        s(COUNTER, "eat_crunchy_cat_luna", "鶏のだしが\nごはんにしみている"),
        s(COUNTER, "sad_banana_cat_cry", "しめの炭水化物は\n正義"),
        s(COUNTER, "sulk_hungry_cat", "ベルトが\n少しきつい"),
        # ---- 満腹 ----
        s(COUNTER, "sulk_hungry_cat", "満腹だ", se="chiin_01",
          bgm={"file": os.path.join(L.BGM, "手紙のさよなら.mp3"), "gain": -14, "fade": 1.0}),
        s(COUNTER, "blank_black_cat_zoning_out", "野獣は\n眠くなってきた"),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "テーブルの上には\n空のお皿とジョッキ"),
        s(COUNTER, "happy_hamster_open_arms", "野獣は\n満たされた"),
        s(COUNTER, "work_typing_cat", "会計しよう", se="pi"),
        s(IN, "money_counting_orange_cat", "全品同じ値段なので\n計算がラクだ"),
        s(IN, "stare_interviewer_cat", "お会計の画面を見る"),
        s(IN, "surprise_big_pupils_cat", "5000円", se="explosion_dokaan"),
        s(IN, "think_chin_paw_orange_cat", "これだけ\n飲み食いして\n5000円"),
        s(IN, "sad_looking_away_tabby", "正直\nひとりトリキの客単価としては\n高いほうだろう"),
        s(IN, "blank_black_cat_zoning_out", "メガハイボールを\n何杯飲んだかは\n数えないでおく"),
        s(IN, "happy_hamster_open_arms", "でも"),
        s(IN, "sleepy_old_memories_cat", "とても\n幸せな夜だ", se="sparkle_kirakira_01"),
        s(IN, "stare_interviewer_cat", "ありがとうございましたー"),
        # ---- 帰り道 ----
        s(ROAD, "leave_cat_leaves_home", "夜風が気持ちいい", se="whoosh_shu"),
        s(ROAD, "sleepy_old_memories_cat", "月曜日に\n飲みに行くのも\n悪くない"),
        s(ROAD, "think_chin_paw_orange_cat", "週末は混んでいる店も\n月曜なら\n入れる"),
        s(ROAD, "rizz_cat_rizz", "これは\n大人の裏ワザだ"),
        s(ROAD, "happy_chipi_chapa_cat", "体の中に\nむねスパとせせりと\nメガハイボール"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", se="whoosh_shu"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "……明日は火曜日"),
        s(ROOM_N, "think_bike_front_seat_cat", "でも\nさっきまでとは\nちがう"),
        s(ROOM_N, "excited_hodomoe_city_cat", "火曜日からの\n活力が\n得られた", se="shine_kiraan_maou", dur=3.8),
        J.end_card(),
    ]


def place(cs):
    J.auto_tempo(cs)
    for c in cs:
        if c.get("text"):   # 字幕にカギかっこはつけない
            c["text"] = c["text"].replace("「", "").replace("」", "")
        if c.get("bg") in NIGHT:
            c["dark"] = NIGHT[c["bg"]]
    return cs


if __name__ == "__main__":
    cs = place(cuts())
    if os.environ.get("LEN"):
        print(len(cs), round(sum(c["dur"] for c in cs), 1))
    else:
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_08_torikizoku.mp4"), os.path.join(J.HERE, "out", "jidaraku_08_torikizoku_preview"))
