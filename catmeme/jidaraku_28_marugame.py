"""自堕落シリーズ #28：30代独身、給料日前に丸亀製麺の釜揚げうどん半額の日（11/28 ユーザー指定）。約6分（11/28 ユーザー指定：5〜7分）。ドトールと同じ作り。

python3 catmeme/jidaraku_28_marugame.py → out/jidaraku_28_marugame.mp4
- 11/28 ユーザー指定の内容：11月は創業感謝祭で、1日だけでなく11日・21日も釜揚げうどんが半額（この回は11/21）。
  給料日前に助かる。当然「得盛」（丸亀は特盛ではなく「得」という表記）。普段はただの特盛で得ではないのでは…と思うが、
  今日ばかりは名実ともに得盛。天ぷらはお得感たっぷりの野菜かき揚げ。お盆のボリュームがすごい。これで600円未満
- 値段は店や時期で変わるので「600円未満」だけ言う（細かい金額は出さない）
- 11/28 修正：千円札1枚・もやしだけはリアルでないので「ボーナス前かつ給料日前・財布の中身はさびしい・寒くなってきた・財布の中も寒い」に
- 流れ：給料日前の財布 → 今日は21日 → 創業感謝祭で半額 → 店へ・行列 → 「得で」→ 得盛の話 → 天ぷら（野菜かき揚げ）→
  ねぎ・天かす → お会計600円未満 → お盆のボリューム → 実食 → 帰り道 → 給料日まであと少しがんばれる
- 写真：backgrounds/jidaraku/28_marugame（11/28 ユーザー提供5枚：f_poster 創業感謝祭（11/1〜11/30）・mg02_inside 店内（行列と席の両方）・
  mg03_tempura 天ぷらの棚・f_tray お盆・f_kakiage 野菜かき揚げ。f_kamaage はお盆の写真から切り出し。mg01_front 店の外（11/28 ユーザー提供）
- 11/17 からのルール：場面転換ゆっくり・字幕は1行12字・最大2行・2.5〜3秒・職場の回想なし
- 11/26 のルール：素材は多様に（使いすぎの素材を減らす）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "28_marugame"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku")]
ROOM_N, STREET_N = "j07_room_night", "bg51_night_street"
FRONT, LINE, TEMPURA, SEAT = "mg01_front", "mg02_inside", "mg03_tempura", "mg02_inside"
POSTER = "f_poster"
TRAY, KAMA, KAKI = "f_tray", "f_kamaage", "f_kakiage"
J.HOLD = 6
J.LOOPS = 1
J.TEMPO_K = 1.3
J.SUB_SEC = (2.5, 3.0)
J.SUB_STYLE = "glow"
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
COCOA = os.path.join(L.BGM, "星降る夜のホットココア.mp3")


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 給料日前の夜 ----
        s(ROOM_N, "stare_lying_tabby_cat", "仕事帰りの\n夕方6時", bgm={"file": NANDE, "gain": -12}),
        s(ROOM_N, "stare_interviewer_cat", "最近\n急に寒くなってきた"),
        s(ROOM_N, "snore_snoring_dog", "朝、布団から\n出られない"),
        s(ROOM_N, "money_counting_cream_cat", "財布を開く"),
        s(ROOM_N, "despair_dramatic_kitten", "…さびしい"),
        s(ROOM_N, "sulk_hungry_cat", "給料日まで\nあと4日"),
        s(ROOM_N, "blank_black_cat_zoning_out", "ボーナスまでは\nまだ2週間"),
        s(ROOM_N, "sad_black_dog", "ボーナス前で\n給料日前"),
        s(ROOM_N, "sad_banana_cat_cry", "どっちも\nまだ来ない"),
        s(ROOM_N, "stand_real_sheep", "外も寒いが"),
        s(ROOM_N, "realize_wet_cat_stare", "財布の中も\n寒いのだ"),
        s(ROOM_N, "slack_nail_filing_cat", "スマホで\nクーポンを探す"),
        s(ROOM_N, "confused_i_dont_know_cat", "今日使えるものが\nない"),
        s(ROOM_N, "scream_phone_orange_cat", "いや待て", se="pi"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "今日は\n11月21日"),
        s(ROOM_N, "surprise_big_pupils_cat", "あの日だ", se="shine_kiraan_maou"),
        s(ROOM_N, "read_book_orange_kitten", "丸亀製麺は\n毎月1日が\n釜揚げうどん半額", item=POSTER),
        s(ROOM_N, "talk_orange_white_sitting_cat", "でも11月は\n創業感謝祭", item=POSTER),
        s(ROOM_N, "joy_happy_happy_happy_cat", "11日と21日も\n半額になる", item=POSTER),
        s(ROOM_N, "dance_three_kittens", "給料日前に\nこれは助かる"),
        s(ROOM_N, "angry_aiming_cat", "行くしかない"),
        s(ROOM_N, "think_bike_front_seat_cat", "でもこの時間は\n混んでいるはず"),
        s(ROOM_N, "punch_boxing_white_cat", "それでも行く"),
        s(ROOM_N, "dance_edm_cat", "半額の日を\nのがすわけにはいかない"),
        s(ROOM_N, "leave_cat_leaves_home", "上着をはおって\n家を出る"),
        # ---- お店へ ----
        s(STREET_N, "walk_white_duck", "夜の道を歩く", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(STREET_N, "stare_interviewer_cat", "外は\nすっかり冬の空気"),
        s(STREET_N, "peek_what_happen_cat", "途中に\nラーメン屋"),
        s(STREET_N, "meow_gray_white_kitten", "とんこつの匂い"),
        s(STREET_N, "glare_disgusted_cat", "今日は\n浮気しない"),
        s(STREET_N, "peek_what_happen_cat", "コンビニの\nからあげも見える"),
        s(STREET_N, "angry_cat_hits_cat", "見ないふり"),
        s(STREET_N, "ride_kitten_bike", "足が\n少しだけ早くなる"),
        s(STREET_N, "peek_what_happen_cat", "白い看板が\n見えてきた", se="pi"),
        s(FRONT, "showoff_gojo_cosplay_cat", "丸亀製麺", se="gong_dora_jaan"),
        s(FRONT, "stare_standing_marmot", "…並んでいる"),
        s(FRONT, "listen_dancing_dog", "みんな\n考えることは同じ"),
        s(FRONT, "flip_emo_cat_hair", "だが\n回転は速い"),
        s(LINE, "work_typing_cat", "列に並ぶ"),
        s(LINE, "peek_what_happen_cat", "ガラスの向こうで\nうどんを打っている"),
        s(LINE, "stare_interviewer_cat", "湯気が\nもくもく"),
        s(LINE, "meow_gray_white_kitten", "だしの\nいい匂い"),
        s(LINE, "sulk_hungry_cat", "お腹が鳴る"),
        s(LINE, "listen_dancing_dog", "前の人は\n肉うどん"),
        s(LINE, "stare_standing_marmot", "その前の人も\n釜揚げ"),
        s(LINE, "flip_emo_cat_hair", "同志よ"),
        s(LINE, "peek_what_happen_cat", "スーツの人\n学生\n家族連れ"),
        s(LINE, "talk_orange_white_sitting_cat", "みんな\n半額を知っている"),
        s(LINE, "scream_phone_orange_cat", "「得で」\nが聞こえた"),
        s(LINE, "punch_tabby_cat_reach", "わかっている人だ"),
        s(LINE, "read_book_orange_kitten", "メニューを見る\nふりをする"),
        s(LINE, "rizz_cat_rizz", "もう\n決まっている"),
        # ---- 注文 ----
        s(LINE, "call_customer_service_cat", "釜揚げうどん", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(LINE, "yell_orange_fat_cat", "得で", se="pikon"),
        s(LINE, "punch_boxing_white_cat", "当然\n得盛だ"),
        s(LINE, "read_book_orange_kitten", "丸亀では\n特盛ではなく"),
        s(LINE, "stare_big_eyes_tabby_kitten", "得盛と書く"),
        s(LINE, "huh_huh_cat", "普段は\nただの特盛"),
        s(LINE, "confused_i_dont_know_cat", "どこが得なのか\nわからない"),
        s(LINE, "realize_wet_cat_stare", "だが今日は\n半額"),
        s(LINE, "dance_happy_banana_cat", "名実ともに\n得盛である", se="shine_kiraan_maou"),
        s(LINE, "surprise_big_pupils_cat", "桶にたっぷりの\nうどん", item=KAMA),
        s(LINE, "eat_chips_cat", "つけだしも\nあつあつ", item=KAMA),
        # ---- 天ぷら ----
        s(TEMPURA, "walk_approaching_orange_cat", "そして\n天ぷらの棚"),
        s(TEMPURA, "stare_big_eyes_tabby_kitten", "揚げたてが\nずらり"),
        s(TEMPURA, "punch_tabby_cat_reach", "とり天…\nいか天…"),
        s(TEMPURA, "money_counting_orange_cat", "給料日前を\n思い出す"),
        s(TEMPURA, "despair_dramatic_kitten", "とり天を\nトングでつかむ"),
        s(TEMPURA, "sulk_hungry_cat", "…そっと戻す"),
        s(TEMPURA, "think_bike_front_seat_cat", "半額で浮いたお金を\n天ぷらで使ったら"),
        s(TEMPURA, "huh_huh_cat", "意味がない"),
        s(TEMPURA, "confused_i_dont_know_cat", "でも\n1個くらいは"),
        s(TEMPURA, "angry_shooting_cat", "野菜かき揚げ\n一択", item=KAKI, se="pikon"),
        s(TEMPURA, "surprise_big_pupils_cat", "でかい", item=KAKI),
        s(TEMPURA, "happy_girlfriend_dance_cat", "このお得感が\nたまらない", item=KAKI),
        s(TEMPURA, "talk_orange_white_sitting_cat", "野菜も\nとれる", item=KAKI),
        s(TEMPURA, "realize_wet_cat_stare", "つまり\n健康", item=KAKI),
        s(TEMPURA, "mock_swinging_cat", "おにぎりは\n見なかったことにする"),
        s(TEMPURA, "spin_spinning_cat", "ねぎと天かすは\nかけ放題"),
        s(TEMPURA, "mock_swinging_cat", "ちょっと多めに"),
        s(TEMPURA, "itchy_kitten_butt", "しょうがも\nひとつまみ"),
        # ---- お会計 ----
        s(LINE, "money_counting_cream_cat", "お会計"),
        s(LINE, "stare_aloha_gray_cat", "600円未満", se="price_display"),
        s(LINE, "joy_happy_happy_happy_cat", "財布にやさしい"),
        s(SEAT, "work_typing_cat", "お盆を持って\n席へ"),
        s(SEAT, "drive_driving_cat", "お盆が重い", item=TRAY),
        s(SEAT, "surprise_big_pupils_cat", "ボリュームが\nすごい", item=TRAY),
        s(SEAT, "dance_orange_gray_cats", "これで\n600円未満", item=TRAY),
        s(SEAT, "rizz_cat_rizz", "勝ちが\n確定している", item=TRAY),
        # ---- 実食 ----
        s(SEAT, "excited_hodomoe_city_cat", "いただきます", item=KAMA, bgm={"file": COCOA, "gain": -12, "fade": 0.8}),
        s(SEAT, "eat_pop_cat", "うどんを\nつけだしへ", item=KAMA),
        s(SEAT, "eat_crunchy_cat_luna", "すする", item=KAMA, se="eat_paku"),
        s(SEAT, "realize_wet_cat_stare", "…もちもち", item=KAMA),
        s(SEAT, "snore_snoring_dog", "ゆでたての\nやわらかさ", item=KAMA),
        s(SEAT, "dance_tabby_standing_cat", "だしの香りが\nふわっと", item=KAMA),
        s(SEAT, "eat_crunchy_cat_luna", "かき揚げを\nかじる", item=KAKI, se="eat_paku"),
        s(SEAT, "surprise_big_pupils_cat", "サクッ", item=KAKI),
        s(SEAT, "happy_hamster_open_arms", "玉ねぎが甘い", item=KAKI),
        s(SEAT, "talk_orange_white_sitting_cat", "かき揚げを\nつけだしに\nひたす", item=KAKI),
        s(SEAT, "eat_pop_cat", "これがまた\nうまい", item=KAKI),
        s(SEAT, "dance_cute_dog", "うどんと\nかき揚げの往復", item=TRAY),
        s(SEAT, "stare_standing_marmot", "…減らない", item=KAMA),
        s(SEAT, "flip_emo_cat_hair", "さすが得盛", item=KAMA),
        s(SEAT, "eat_chips_cat", "天かすを足して\n味を変える", item=KAMA),
        s(SEAT, "talk_orange_white_sitting_cat", "しょうがを\nつけだしにとかす", item=KAMA),
        s(SEAT, "happy_hamster_open_arms", "体があたたまる", item=KAMA),
        s(SEAT, "stare_big_eyes_tabby_kitten", "となりの席も\n得盛", item=TRAY),
        s(SEAT, "flip_emo_cat_hair", "目が合う"),
        s(SEAT, "punch_tabby_cat_reach", "心の中で\nうなずき合う"),
        s(SEAT, "eat_pop_cat", "残り半分", item=KAMA),
        s(SEAT, "stare_standing_marmot", "少しお腹が\n苦しくなってきた", item=KAMA),
        s(SEAT, "angry_shooting_cat", "だが\n残すわけにはいかない", item=KAMA),
        s(SEAT, "sleepy_old_memories_cat", "子どものころ\n家で食べた\nうどんを思い出す"),
        s(SEAT, "eat_crunchy_cat_luna", "最後のひと玉", item=KAMA),
        s(SEAT, "realize_wet_cat_stare", "…完食", item=TRAY),
        s(SEAT, "happy_hamster_open_arms", "お腹いっぱい"),
        s(SEAT, "slack_nail_filing_cat", "少しだけ\nぼーっとする"),
        s(SEAT, "stare_interviewer_cat", "ごちそうさまでした"),
        # ---- 帰り道と家 ----
        s(FRONT, "walk_white_duck", "お店を出る", bgm={"file": JITAKU, "gain": -10, "fade": 1.0}),
        s(STREET_N, "think_bike_front_seat_cat", "夜風が\nちょうどいい"),
        s(STREET_N, "money_counting_orange_cat", "財布の中は\nまだ少しあたたかい"),
        s(STREET_N, "joy_happy_happy_happy_cat", "給料日まで\nいける"),
        s(STREET_N, "dance_white_dog", "得盛ありがとう"),
        s(STREET_N, "peek_what_happen_cat", "次の半額は\n12月1日"),
        s(STREET_N, "angry_aiming_cat", "もう\n予定に入れた"),
        s(ROOM_N, "dance_tabby_standing_cat", "家に帰る"),
        s(ROOM_N, "money_counting_cream_cat", "レシートを\nながめる"),
        s(ROOM_N, "smug_squint_bicolor_cat", "この数字で\nこの満足感"),
        s(ROOM_N, "work_dog_staring_computer", "12月1日を\nカレンダーに書く"),
        s(ROOM_N, "dance_happy_banana_cat", "ちょっと\n楽しみが増えた"),
        s(ROOM_N, "snore_snoring_dog", "お風呂で\nあったまる"),
        s(ROOM_N, "calmdown_dancing_cat", "今日は\nいい日だった"),
        s(ROOM_N, "stare_lying_tabby_cat", "布団に\nころがる"),
        s(ROOM_N, "sleepy_sleepy_cat", "お腹があたたかい"),
        s(ROOM_N, "sleep_sleeping_cat", "すぐ眠くなる"),
        s(ROOM_N, "realize_wet_cat_stare", "給料日前でも\nちゃんと幸せだった"),
        s(ROOM_N, "excited_hodomoe_city_cat", "次の1日も\n丸亀製麺で", se="pikon", dur=3.8),
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_28_marugame.mp4"), os.path.join(J.HERE, "out", "jidaraku_28_marugame_preview"))
