"""自堕落シリーズ #4：30代独身男、ひとりでスシローに行く（10/31 ユーザー指定・焼肉きんぐと同じ作り）。約8分。

python3 catmeme/jidaraku_04_sushiro.py → out/jidaraku_04_sushiro.mp4
- 流れ：朝ごはんを抜いて11時に来店「今日は寿司との戦争だ」→ カウンター → お酒 → 海鮮漬け軍艦・カニサラダ軍艦 →
  かぼちゃ天ぷら・茶碗蒸し（はま寿司の大葉とマグロのはさみ揚げの独白）→ かにみそ軍艦（いちばんうまいというYouTuberもいる）→
  まぐろ・中とろ・サーモン・デカえびなど → ラーメンに10分悩む → マーラー風エビ揚げネギ添え（回転寿司は異種格闘技の魔境）→
  デザート → 満腹「もう晩ごはんもいらない…」→ 会計「8000円…だと…」
- 口コミ・ランキングの声（2026年ごろ）：本鮪のまぐろの評価が高い／茶碗蒸しはサイド人気1位（とろとろで出汁がきいている・具がごろっと）／
  かぼちゃ天ぷらも上位／鯛だし塩ラーメン／かにみそをポテトにつける食べ方。値段はオチの8000円以外は書かない（焼肉きんぐと同じ）
- 実在の人（YouTuber など）の名前は出さない。字幕に句読点なし。「にゃ」なし。単語の途中で改行しない
- 料理の写真は右上に白いふちで出す（item）。写真が届いていない料理は字幕だけ
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "04_sushiro"))
ROOM, FRONT, IN, COUNTER, ROOM_N = "j01_room", "s01_store_front", "s02_inside", "s03_counter", "s09_room_night"
J.STANDIN.update({COUNTER: IN, ROOM_N: ROOM})
NIGHT = {ROOM_N: 0.72}
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
# 料理の写真（届いた順に backgrounds/jidaraku/04_sushiro に置く）
EBI, KANIMISO, HASAMI = "f_ebi_mala", "f_kanimiso", "f_hasamiage"
ZUKE, KANISARA, KABOCHA, CHAWAN, MAGURO, TORO, SALMON, DEKAEBI, RAMEN, PARFAIT, BEER = (
    "f_zuke_gunkan", "f_kanisalad", "f_kabocha", "f_chawanmushi", "f_maguro", "f_chutoro", "f_salmon", "f_dekaebi", "f_ramen",
    "f_parfait", "f_beer")


def cuts():
    def s(*a, **k):   # 1つの字幕は3.4秒（8分前後にする）
        k.setdefault("dur", 3.4)
        return J.line(*a, **k)
    return [
        # ---- 朝（戦いの前） ----
        s(ROOM, "sleep_sleeping_cat", "土曜の朝9時\n珍しく目が覚めた", bgm={"file": L.NORA, "gain": -12}),
        s(ROOM, "blank_black_cat_zoning_out", "部屋着は\n今日も高校のジャージ"),
        s(ROOM, "eat_pop_cat", "冷蔵庫を開ける\n食パンが1枚"),
        s(ROOM, "angry_aiming_cat", "……いや\n今日は食べない"),
        s(ROOM, "realize_wet_cat_stare", "朝ごはんは抜く\n胃袋は空にしておく"),
        s(ROOM, "slack_nail_filing_cat", "スマホで\nスシローのメニューを開く"),
        s(ROOM, "read_book_orange_kitten", "期間限定のフェアも\nしっかり予習する"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "口コミには\n「まぐろがうまい」\n「茶碗蒸しがとろとろ」"),
        s(ROOM, "think_bike_front_seat_cat", "ネットの人気ランキングも\n上から順に読む"),
        s(ROOM, "excited_hodomoe_city_cat", "仕事の資料より\nよっぽど真剣だ"),
        s(ROOM, "showoff_gojo_cosplay_cat", "アプリで受付\n11時に予約した", se="pikon"),
        s(ROOM, "blank_black_cat_zoning_out", "ジャージの上に\nパーカーを羽織る"),
        s(ROOM, "dance_three_kittens", "今日は\n寿司との戦争だ", se="gong_match_start"),
        # ---- 店へ ----
        s(FRONT, "ride_kitten_bike", "11時\nスシローに到着", se="whoosh_shu"),
        s(FRONT, "peek_what_happen_cat", "開店直後なのに\n駐車場はもう半分うまっている"),
        s(FRONT, "stare_interviewer_cat", "家族連れが\n楽しそうに入っていく"),
        s(FRONT, "rizz_cat_rizz", "俺はひとり\nでも今日は戦士だ"),
        s(IN, "work_typing_cat", "受付の機械で\nアプリの番号を読みこむ"),
        s(IN, "stare_tabby_wide_eyes_cat", "人数は「1」"),
        s(IN, "stare_interviewer_cat", "「カウンター席へ\nどうぞ〜」", se="pinpon_notice"),
        s(COUNTER, "calmdown_dancing_cat", "カウンターは\nひとり客の聖地"),
        s(COUNTER, "sleepy_old_memories_cat", "となりも\nその向こうもひとり"),
        s(COUNTER, "realize_wet_cat_stare", "誰も\nこっちを見ていない"),
        s(COUNTER, "happy_chipi_chapa_cat", "最高の\n環境だ"),
        s(COUNTER, "read_book_orange_kitten", "目の前には\n注文用のタッチパネル"),
        s(COUNTER, "think_chin_paw_orange_cat", "お茶の粉を入れて\nお湯を注ぐ"),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "ガリを小皿に\n山盛りにする"),
        s(COUNTER, "showoff_gojo_cosplay_cat", "これで\n準備は整った"),
        # ---- 開戦 ----
        s(COUNTER, "cocky_dj_cat", "まずは\nアルコールを頼む", bgm={"file": L.PURPLE, "gain": -12, "fade": 0.8}),
        s(COUNTER, "yell_orange_fat_cat", "昼の11時に\nビール", item=BEER),
        s(COUNTER, "happy_hamster_open_arms", "休日の特権だ"),
        s(COUNTER, "eat_crunchy_cat_luna", "ゴクッ……\n「くぅ〜！」", se="drink_gulp_gokugoku_thirsty_chug"),
        s(COUNTER, "work_typing_cat", "1皿目は\n本日の海鮮漬け軍艦", item=ZUKE),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "タレにつかった\n切り落としの海鮮が\nこれでもかと乗っている", item=ZUKE),
        s(COUNTER, "eat_pop_cat", "ひと口\n……甘じょっぱい", item=ZUKE),
        s(COUNTER, "happy_girlfriend_dance_cat", "「これ\nビールに合いすぎる」"),
        s(COUNTER, "work_typing_cat", "続いて\nカニサラダ軍艦", item=KANISARA),
        s(COUNTER, "laugh_laughing_dog", "マヨネーズの\nやさしい味", item=KANISARA),
        s(COUNTER, "realize_wet_cat_stare", "高い寿司屋には\nたぶん置いてない", item=KANISARA),
        s(COUNTER, "rizz_cat_rizz", "でもこれが\nいいんだよ"),
        s(COUNTER, "sleepy_old_memories_cat", "子どものころ\n親にねだったのも\nこの軍艦だった"),
        # ---- サイドメニュー ----
        s(COUNTER, "think_bike_front_seat_cat", "寿司の合間には\nサイドメニュー"),
        s(COUNTER, "work_typing_cat", "かぼちゃの天ぷらと\n茶碗蒸し", se="pikon"),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "かぼちゃ天は\n口コミでも上位の常連", item=KABOCHA),
        s(COUNTER, "eat_crunchy_cat_luna", "サクッ……\n中はほくほく", item=KABOCHA),
        s(COUNTER, "happy_hamster_open_arms", "茶碗蒸しは\nサイド人気1位", item=CHAWAN),
        s(COUNTER, "eat_pop_cat", "とろとろで\n出汁がきいている", item=CHAWAN),
        s(COUNTER, "surprise_big_pupils_cat", "スプーンを入れると\n具がごろっと出てくる", item=CHAWAN),
        s(COUNTER, "sleepy_old_memories_cat", "サイドメニューと言えば……", se="question_hatena_maou"),
        s(COUNTER, "think_chin_paw_orange_cat", "前に行った\nはま寿司の", item=HASAMI),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "大葉とマグロの\nはさみ揚げ", item=HASAMI),
        s(COUNTER, "happy_chipi_chapa_cat", "あれは\n絶品だった", item=HASAMI),
        s(COUNTER, "realize_wet_cat_stare", "大葉の香りと\nふわふわのマグロ", item=HASAMI),
        s(COUNTER, "glare_disgusted_cat", "……いや\n今はスシローに集中しろ"),
        s(COUNTER, "angry_aiming_cat", "浮気は\n戦場では命取りだ"),
        # ---- 寿司ラッシュ ----
        s(COUNTER, "work_typing_cat", "ここからは\n寿司ラッシュだ", se="explosion_dokaan"),
        s(COUNTER, "cocky_dj_cat", "まずは\nまぐろ", item=MAGURO),
        s(COUNTER, "happy_hamster_open_arms", "口コミでも\nいちばん評価が高い", item=MAGURO),
        s(COUNTER, "eat_pop_cat", "「回転寿司で\nこのまぐろは反則だろ」", item=MAGURO),
        s(COUNTER, "dance_wop_cat", "続けて中とろ", item=TORO),
        s(COUNTER, "surprise_big_pupils_cat", "口の中で\nとけた", item=TORO),
        s(COUNTER, "dance_three_kittens", "サーモンは\n大きく切られた\nジャンボとろサーモン", item=SALMON),
        s(COUNTER, "laugh_laughing_dog", "皿からはみ出している", item=SALMON),
        s(COUNTER, "yell_orange_fat_cat", "デカえびも\n頼んでしまう", item=DEKAEBI),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "「えびデカっ！」", item=DEKAEBI, se="question_mark_pop_confused_huh"),
        s(COUNTER, "happy_girlfriend_dance_cat", "ビールを\nおかわり"),
        s(COUNTER, "read_book_orange_kitten", "レーンを流れてくる\nおすすめの皿にも\nつい手がのびる"),
        s(COUNTER, "dance_koto_nai_cat", "皿がどんどん\n積み上がっていく"),
        # ---- かにみそ ----
        s(COUNTER, "think_bike_front_seat_cat", "そして俺が\n今日いちばん\n楽しみにしていた皿"),
        s(COUNTER, "work_typing_cat", "かにみそ軍艦", item=KANIMISO, se="gong_dora_jaan"),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "地味な見た目だ", item=KANIMISO),
        s(COUNTER, "peek_what_happen_cat", "スシローでいちばんうまいのは\nかにみそ軍艦だという\nYouTuberもいる", item=KANIMISO),
        s(COUNTER, "eat_crunchy_cat_luna", "ひと口……", item=KANIMISO),
        s(COUNTER, "realize_wet_cat_stare", "濃厚なかにみそと\nのりの香り", item=KANIMISO),
        s(COUNTER, "happy_hamster_open_arms", "……わかる\n実際 同意できる", item=KANIMISO, se="pinpoon_correct"),
        s(COUNTER, "sleepy_old_memories_cat", "これは\n日本酒が欲しくなる味だ"),
        s(COUNTER, "rizz_cat_rizz", "かにみそを\nフライドポテトに\nつける裏ワザもあるらしい"),
        s(COUNTER, "showoff_gojo_cosplay_cat", "次に来たときの\n宿題にしておく"),
        # ---- ラーメンに悩む ----
        s(COUNTER, "stare_tabby_wide_eyes_cat", "1時間がたった", se="pi", bgm={"file": LOFI, "gain": -14, "fade": 1.0}),
        s(COUNTER, "read_book_orange_kitten", "タッチパネルの\nラーメンのページで\n指が止まる", item=RAMEN),
        s(COUNTER, "think_chin_paw_orange_cat", "鯛だし塩ラーメン\nやさしい味らしい", item=RAMEN),
        s(COUNTER, "think_bike_front_seat_cat", "でも\nこってり系も気になる"),
        s(COUNTER, "confused_i_dont_know_cat", "寿司屋でラーメン\n食べていいのか？"),
        s(COUNTER, "sleepy_old_memories_cat", "お腹はもう\n7割くらい"),
        s(COUNTER, "despair_dramatic_kitten", "ラーメン1杯で\n寿司が何皿食べられる？"),
        s(COUNTER, "think_chin_paw_orange_cat", "頼む\nいや……やめる"),
        s(COUNTER, "stare_big_eyes_tabby_kitten", "でもやっぱり……"),
        s(COUNTER, "blank_black_cat_zoning_out", "気づけば\n10分悩んでいた", se="cuckoo_pappo"),
        s(COUNTER, "realize_wet_cat_stare", "その間に\nビールは空になった"),
        s(COUNTER, "angry_aiming_cat", "……ラーメンは\nまた今度にする"),
        s(COUNTER, "cocky_dj_cat", "かわりに\nハイボールを頼む"),
        # ---- マーラー風エビ ----
        s(COUNTER, "stare_tabby_wide_eyes_cat", "ふと目に入った\n期間限定の皿", se="pikon"),
        s(COUNTER, "surprise_big_pupils_cat", "マーラー風エビ揚げ\nネギ添え", item=EBI, se="explosion_bokaan"),
        s(COUNTER, "confused_i_dont_know_cat", "……寿司なのか\nこれは", item=EBI),
        s(COUNTER, "work_typing_cat", "迷わず押した", item=EBI),
        s(COUNTER, "eat_crunchy_cat_luna", "ピリッとしびれる辛さに\nサクサクのネギ", item=EBI),
        s(COUNTER, "happy_chipi_chapa_cat", "「うまっ！」\nハイボールが進む", item=EBI),
        s(COUNTER, "think_bike_front_seat_cat", "絶対に\nこういう回転寿司でしか\n出てこない寿司だよなぁ", item=EBI),
        s(COUNTER, "sleepy_old_memories_cat", "中華とも寿司とも言えない\n異種格闘技"),
        s(COUNTER, "realize_wet_cat_stare", "そんな異種格闘技に\n気軽にチャレンジできる"),
        s(COUNTER, "showoff_gojo_cosplay_cat", "それが\nスシローに代表される\n回転寿司チェーンの魅力"),
        s(COUNTER, "rizz_cat_rizz", "ここは\n魔境だ"),
        # ---- 限界 ----
        s(COUNTER, "dance_maxwell_cat", "調子に乗って\n炙りの皿も追加"),
        s(COUNTER, "dance_edm_cat", "いくらもうにも\n少しずつ"),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "皿のタワーが\n目の高さをこえた"),
        s(COUNTER, "confused_i_dont_know_cat", "あれ……\nお腹が重い"),
        s(COUNTER, "sulk_hungry_cat", "シャリが\n胃の中でふくらんでいる"),
        s(COUNTER, "despair_dramatic_kitten", "寿司はご飯だと\n今さら思い出す"),
        s(COUNTER, "sleepy_sleepy_cat", "ガリで\n口をリセットする"),
        s(COUNTER, "think_chin_paw_orange_cat", "温かいお茶で\nひと休み"),
        s(COUNTER, "stare_interviewer_cat", "となりのひとり客は\n5皿で帰っていった"),
        s(COUNTER, "realize_wet_cat_stare", "大人の\n食べ方だ"),
        # ---- デザート ----
        s(COUNTER, "stare_big_eyes_tabby_kitten", "でも\nデザートのページが\n目に入る"),
        s(COUNTER, "glare_disgusted_cat", "「デザートは\n別腹って言うしな」"),
        s(COUNTER, "happy_chipi_chapa_cat", "パフェを\n頼んでしまった", item=PARFAIT, se="pikon"),
        s(COUNTER, "eat_pop_cat", "冷たくて甘い\n口の中がさっぱりする", item=PARFAIT),
        s(COUNTER, "sleepy_old_memories_cat", "胃袋は\nさっぱりしない"),
        # ---- 満腹 ----
        s(COUNTER, "sulk_hungry_cat", "う〜\n満腹", se="chiin_01", bgm={"file": os.path.join(L.BGM, "手紙のさよなら.mp3"), "gain": -14, "fade": 1.0}),
        s(COUNTER, "blank_black_cat_zoning_out", "もう晩ごはんも\nいらない……"),
        s(COUNTER, "sleep_sleeping_cat", "背もたれのない\nカウンターがつらい"),
        s(COUNTER, "stare_tabby_wide_eyes_cat", "積み上がった皿を\n数えてみる"),
        s(COUNTER, "despair_dramatic_kitten", "……数えるのを\nやめた"),
        s(COUNTER, "work_typing_cat", "タッチパネルの\n「お会計」を押す", se="pi"),
        s(IN, "money_counting_orange_cat", "セルフレジへ向かう"),
        s(IN, "stare_interviewer_cat", "お会計の画面を見る"),
        s(IN, "surprise_big_pupils_cat", "8000円……", se="explosion_dokaan"),
        s(IN, "despair_dramatic_kitten", "……だと……", se="chin_bell_failure_sad_ending"),
        s(IN, "sad_banana_cat_cry", "回転寿司で\n8000円……"),
        s(IN, "blank_black_cat_zoning_out", "ビールとハイボールと\nかにみそと異種格闘技の\nせいだ"),
        s(IN, "realize_wet_cat_stare", "寿司との戦争\n財布の完敗だった"),
        # ---- 帰り道〜夜 ----
        s(FRONT, "leave_cat_leaves_home", "外に出る\nまだ昼の1時半", se="whoosh_shu"),
        s(FRONT, "sleepy_sleepy_cat", "自転車をこぐ足が重い"),
        s(ROOM_N, "sleep_sleeping_cat", "夜 晩ごはんは\n本当にいらなかった"),
        s(ROOM_N, "slack_nail_filing_cat", "スマホに\nスシローのアプリの通知"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "「来週から\nかにフェア開催！」"),
        s(ROOM_N, "realize_wet_cat_stare", "……"),
        s(ROOM_N, "excited_hodomoe_city_cat", "次こそ\nポテトにかにみそだ", se="pikon", dur=3.4),
        J.end_card(),
    ]


def place(cs):
    for c in cs:
        if c.get("bg") in NIGHT:
            c["dark"] = NIGHT[c["bg"]]
    return cs


if __name__ == "__main__":
    cs = place(cuts())
    if os.environ.get("LEN"):
        print(len(cs), round(sum(c["dur"] for c in cs), 1))
    else:
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_04_sushiro.mp4"), os.path.join(J.HERE, "out", "jidaraku_04_sushiro_preview"))
