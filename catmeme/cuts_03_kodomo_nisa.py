"""03_kodomo_nisa（こどもNISA）のカット割り。原稿 scripts/03_kodomo_nisa.md。

python3 catmeme/cuts_03_kodomo_nisa.py          → out/03_kodomo_nisa_full.mp4
python3 catmeme/cuts_03_kodomo_nisa.py --audio  → 音だけ作り直す
python3 catmeme/cuts_03_kodomo_nisa.py 0:10     → 先頭10カットだけ
"""
import os
import sys

import render as R


HERE = os.path.dirname(os.path.abspath(__file__))
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("03_kodomo_nisa", "02_october", "01_todai")]   # 前の動画の背景も使い回す
PT = os.path.join(HERE, "parts", "03_kodomo_nisa")
BGM = os.path.join(HERE, "bgm")

PURPLE = os.path.join(BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
COCOA = os.path.join(BGM, "星降る夜のホットココア.mp3")
MIRAI = os.path.join(BGM, "未来を創る君たちへ.mp3")
KAMI = os.path.join(BGM, "神の怒り.mp3")


def bg(n):
    for d in BGS:
        p = os.path.join(d, n + ".png")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(n)


def pt(n):
    return os.path.join(PT, n + ".png")


def news(a, say, b="bg02_room", **kw):
    """ニュース猫（左）のセリフ。"""
    cat = {"a": a, "x": kw.pop("x", 500), "h": kw.pop("h", 760), "bottom": 1010, "flip": kw.pop("flip", False),
           "ss": kw.pop("ss", 0.0), "anchor": kw.pop("anchor", False), "sound": kw.pop("sound", False)}
    return dict(bg=bg(b), cats=[cat], say=say, say_name="ニュース猫", **kw)


def sage(a, say, b="bg02_room", **kw):
    """博識な猫（右）のセリフ。"""
    cat = {"a": a, "x": kw.pop("x", 1420), "h": kw.pop("h", 740), "bottom": 1010, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False), "anchor": kw.pop("anchor", False)}
    return dict(bg=bg(b), cats=[cat], say=say, say_name="博識な猫", plate_xy=(1080, 900), **kw)


def papa(a, say, b="bg14_home_night", **kw):
    """パパ猫（右・子育て中の親）。"""
    cat = {"a": a, "x": kw.pop("x", 1420), "h": kw.pop("h", 740), "bottom": 1010, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg(b), cats=[cat], say=say, say_name="パパ猫", plate_xy=(1080, 900), **kw)


def narr(b, sub, a, **kw):
    """ナレーション（左に猫、右に大きな文字）。"""
    cat = {"a": a, "x": kw.pop("x", 470), "h": kw.pop("h", 640), "bottom": 990, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg(b), cats=[cat], sub=sub, **kw)


def card(c, sub, cat=None, b="bg03_blackboard", **kw):
    """解説カード＋右下の小さい猫＋字幕。"""
    cats = [{"a": cat, "x": 1752, "h": 330, "bottom": 830, "float": True, "small": True,
             "sound": kw.pop("sound", False)}] if cat else []
    return dict(bg=bg(b), card=pt(c), cats=cats, sub=sub, **kw)


def net(a, say, tag, **kw):
    """ネットの声（スマホ背景・左に猫）。"""
    cat = {"a": a, "x": kw.pop("x", 500), "h": kw.pop("h", 720), "bottom": 1010, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg("bg09_sns"), cats=[cat], say=say, say_name=tag, **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=3.4),
        # ---- 1. つかみ ----
        dict(bg=bg("bg19_kids_room"), card=pt("e01_title"), dur=2.4, bgm={"file": PURPLE, "gain": -7},
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        narr("bg20_counter", "2026年10月1日\n「こどもNISA」の\n口座の受付が\nスタート", "work_typing_cat"),
        narr("bg20_counter", "始まるのは\n2027年1月から", "call_customer_service_cat", dur=1.8),
        news("peek_what_happen_cat", "こどもNISA？\n子どもが\n投資すんの？"),
        sage("itchy_kitten_butt", "いや、実際に\n動かすのは\n親な", dur=1.8),
        news("confused_i_dont_know_cat", "え、じゃあ\n親のNISAと\nなにが違うのよ", flip=True),
        sage("showoff_gojo_cosplay_cat", "そこが\n今日の本題", dur=1.6),
        news("leave_cat_leaves_home", "てか、NISAって\nそもそも\nなんだっけ"),
        sage("think_bike_front_seat_cat", "投資で増えた分の\n税金が\nタダになる箱な", b="bg20_counter"),
        dict(bg=bg("bg06_spotlight"), card=pt("e01b_theme"), dur=3.0,
             cats=[{"a": "dance_koto_nai_cat", "x": 1752, "h": 330, "bottom": 830, "float": True, "small": True}]),
        # ---- 2. こどもNISAってなに？ ----
        card("e02_basic", "0〜17歳の子どもの名前で作る　NISAの口座", "eat_crunchy_cat_luna", b="bg19_kids_room", dur=2.6),
        card("e02_basic", "1年に60万円まで　合計600万円まで　投資できる", "eat_crunchy_cat_luna", b="bg19_kids_room",
             dur=2.6),
        card("e02_basic", "増えた分に　税金がかからない（ふつうは約20％かかる）", "eat_crunchy_cat_luna",
             b="bg19_kids_room", dur=2.8),
        news("think_bike_front_seat_cat", "60万って\n月5万か", dur=1.6),
        sage("drive_driving_cat", "そう。\n毎月5万なら\n10年で600万に\n届く"),
        news("sulk_hungry_cat", "いや\n月5万は\nムリだって", b="bg16_food_aisle"),
        card("e02_basic", "買えるのは　国が選んだ「積立向けの投資信託」だけ", "ride_kitten_bike", b="bg19_kids_room",
             dur=2.6),
        card("e02_basic", "お金を出して運用するのは　親など（親権者）", "ride_kitten_bike", b="bg19_kids_room", dur=2.4),
        news("blank_black_cat_zoning_out", "子どもの名前で\n親が運用……\nややこしいな", dur=1.9),
        # ---- 3. ふつうのNISAとの違い ----
        card("e03_compare", "ふつうのNISAと　比べてみると", "excited_hodomoe_city_cat", b="bg20_counter", dur=3.2),
        card("e03_compare", "枠は　大人の6分の1くらい", "excited_hodomoe_city_cat", b="bg20_counter", dur=2.4),
        sage("call_customer_service_cat", "しかも\n個別の株は\n買えないからな", b="bg20_counter"),
        news("dance_maxwell_cat", "選べるのは\n投資信託だけね\n了解", b="bg20_counter", dur=1.8),
        news("realize_wet_cat_stare", "引き出し\n12歳まで\nNGって……"),
        news("huh_huh_cat", "引き出せないの\nキツくね？"),
        card("e03b_withdraw", "12歳未満は　原則引き出せない（大きな災害など　やむを得ない時だけ例外）", "slack_nail_filing_cat",
             b="bg21_school_gate", dur=3.2),
        card("e03b_withdraw", "12歳からは　「子どものための出費」なら引き出せる", "slack_nail_filing_cat",
             b="bg21_school_gate", dur=2.6),
        card("e03b_withdraw", "ただし　子どもの同意と　使い道の書類が必要", "slack_nail_filing_cat", b="bg21_school_gate",
             dur=2.4),
        news("angry_cat_hits_cat", "子どもの同意!?\n反抗期だったら\n詰むじゃん", b="bg21_school_gate"),
        sage("cocky_dj_cat", "お小遣いアップで\n交渉するしか\nない", b="bg21_school_gate"),
        card("e03b_withdraw", "18歳になると　自動で「ふつうのNISA」に引っ越し", "taunt_cat_and_scared_dog", dur=2.4),
        card("e03c_1800", "ただし　こどもNISAで使った枠は　大人の1,800万円に含まれる", "taunt_cat_and_scared_dog",
             dur=3.0),
        news("surprise_big_pupils_cat", "え、\n600万\n使ってたら……", se="don"),
        sage("work_typing_cat", "大人になってからの\n残りは\n1,200万ってこと"),
        news("glare_disgusted_cat", "将来の枠を\n前借りしてる\nだけじゃん", anchor=True),
        # ---- 4. お得なところ ----
        card("e04_merit", "お得なところ　① 家族の非課税の枠が増える", "happy_girlfriend_dance_cat", dur=2.6),
        papa("calm_black_face_sheep", "うち、\n自分のNISA枠\nもう埋まりそう\nでさ"),
        sage("itchy_kitten_butt", "そういう家は\n子どもの分\n600万が\n上乗せになる", b="bg14_home_night"),
        papa("joy_happy_happy_happy_cat", "よっしゃ\n枠増えた", sound=True),
        card("e04_merit", "② 0歳から始めると　18年も運用できる", "dance_wop_cat", b="bg19_kids_room", dur=2.4),
        card("e04b_sim", "月1万円を0歳から18年　入れたお金は216万円", "dance_wop_cat", b="bg19_kids_room", dur=2.6),
        card("e04b_sim", "年3％で増えたら　約286万円（※仮の計算。減ることもある）", "dance_wop_cat",
             b="bg19_kids_room", dur=3.0),
        news("weird_meowing_cat", "70万も\n増えてんの!?"),
        sage("listen_dancing_dog", "あくまで\n“うまくいけば”\nな", dur=1.8),
        news("peek_what_happen_cat", "じゃあ\n0歳から\n始めないと損？", b="bg19_kids_room"),
        sage("blank_black_cat_zoning_out", "早く始めるほど\n時間を\n味方にできる\nってだけな", b="bg19_kids_room"),
        card("e04c_junior", "③ 前の制度「ジュニアNISA」の反省で　使いやすくなった", "spit_not_my_taste_cat", dur=2.8),
        card("e04c_junior", "前は　18歳まで原則引き出せず　非課税も5年だけ", "spit_not_my_taste_cat", dur=2.6),
        card("e04c_junior", "こどもNISAは　12歳から教育費に使える・非課税は無期限", "spit_not_my_taste_cat", dur=2.8),
        news("mock_swinging_cat", "中学・高校の\n入学金に\n使えるのは\nデカい", b="bg21_school_gate"),
        card("e04_merit", "④ おじいちゃん・おばあちゃんからの援助の受け皿にもなる", "sleepy_old_memories_cat",
             b="bg14_home_night", dur=2.8),
        papa("shady_dancing_man", "じいじが\n孫のために\n何かしたい\nって言っててさ"),
        card("e04_merit", "ただし　もらったお金は1年で合計110万円を超えると　贈与税に注意", "slack_nail_filing_cat",
             b="bg14_home_night", dur=3.0),
        news("spin_spinning_cat", "税金の話\n多すぎて\n目が回る", dur=1.8),
        # ---- 5. イマイチなところ ----
        card("e05_demerit", "でも　イマイチという声も多い", "sleepy_sleepy_cat", dur=2.4, bgm={"file": COCOA, "gain": -7}),
        card("e05_demerit", "① 「まず親のNISAを埋めるのが先」", "sleepy_sleepy_cat", dur=2.2),
        sage("drive_monkey_golf_cart", "親のNISAなら\nいつでも\n引き出せるし\n枠もデカいからな"),
        net("sleep_sleeping_cat", "親の枠すら\n埋まってないのに\n子どもの分とか\n無理ゲー", "親の声"),
        news("huh_huh_cat", "で、結局\n親と子\nどっちが先なの？"),
        sage("angry_aiming_cat", "引き出しやすさで\n言えば\n親が先って\n意見が多いな"),
        card("e05_demerit", "② 「お金に余裕のある家しか使えない」", "fight_cat_fight", dur=2.2),
        net("rage_talking_cat", "結局\n金持ちの子が\nさらに有利に\nなるだけ", "格差を心配する声"),
        net("laugh_laughing_dog", "親ガチャを\n国が強化してて\n草", "格差を心配する声"),
        card("e05_demerit", "③ 引き出しのルールがめんどう", "fight_cat_fight", dur=2.0),
        net("confused_i_dont_know_cat", "12歳まで\n使えない\nその後も書類\nハードル高い", "親の声"),
        card("e05_demerit", "④ 18歳で子どものお金になる", "wakeup_dog_hits_bowl", dur=2.0),
        net("despair_dramatic_kitten", "18歳で\nいきなり数百万\n全部溶かされたら\nどうすんの", "親の声"),
        papa("tense_two_cats_face_off", "うちの子に\n限って……\nいや、ありうる"),
        card("e05_demerit", "⑤ 投資だから　減ることもある（アンケートでも不安の1位）", "wakeup_dog_hits_bowl", dur=2.8),
        news("sad_banana_cat_cry", "教育費が\n減ったら\nシャレにならん"),
        card("e05_demerit", "⑥ 「どうせまた制度が変わる」　前のジュニアNISAは使われずに2023年で廃止",
             "dance_trending_cat", dur=3.2),
        news("angry_shooting_cat", "前作、\n打ち切り\nだったの!?", sting={"file": KAMI, "len": 4.0, "gain": -18}),
        sage("sulk_hungry_cat", "ジュニアNISAは\n使う人が\n少なかったからな"),
        net("mock_swinging_cat", "国のNISA\n毎回パッチ\n当てすぎ", "制度への不信"),
        net("huh_goat_talks_to_huh_cat", "子どもが\n18歳になる前に\nまた変わりそう", "制度への不信"),
        narr("bg09_sns", "一方で", "showoff_gojo_cosplay_cat", dur=1.4),
        net("happy_chipi_chapa_cat", "出産祝いを\n預ける先が\nできてありがたい", "歓迎する声", sound=True),
        net("wave_waving_cat", "子どもと一緒に\nお金の勉強が\nできる", "歓迎する声"),
        # ---- 6. どんな家に向いてる？ ----
        card("e06_fit", "向いているのは　親のNISAが埋まりそう・祖父母の援助がある家", "dance_edm_cat",
             b="bg14_home_night", dur=3.0),
        card("e06_fit", "向いていないのは　親のNISAがまだ空いている・すぐ使うかもしれないお金", "dance_edm_cat",
             b="bg14_home_night", dur=3.2),
        news("calmdown_dancing_cat", "なるほど、\nまず親の枠から\nってことね", b="bg14_home_night"),
        news("dance_wild_dog", "……うち、\n親の枠も\nスカスカだわ", b="bg14_home_night", dur=1.9),
        sage("eat_pop_cat", "余裕がある家の\n“追加の箱”って\n考えると\nわかりやすい", b="bg14_home_night"),
        papa("cocky_dj_cat", "よし、\nまず自分のを\nちゃんとやるわ", flip=True),
        # ---- 7. まとめ ----
        dict(bg=bg("bg03_blackboard"), card=pt("e07_matome"), dur=4.4,
             cats=[{"a": "excited_hodomoe_city_cat", "x": 1752, "h": 330, "bottom": 830, "float": True, "small": True}],
             bgm={"file": MIRAI, "gain": -7, "fade": 0.8}),
        sage("realize_wet_cat_stare", "お得かどうかは\n家庭しだい\nってわけ"),
        news("glare_disgusted_cat", "結局\n余裕ある家の\n選択肢が\n増えたってことね"),
        news("drive_driving_cat", "とりあえず\n自分のNISAから\nちゃんとやるわ"),
        dict(bg=bg("bg03_blackboard"), card=pt("e08_ending"), dur=3.0,
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
    ]


# 効果音（catmeme/se/）。セリフ・字幕・カード画像の一部が一致したカットに付ける（上から順に最初の一致）
SE_MAP = [
    # ゲーム・テレビ番組の音（⚠ 権利は各社。収益化で申し立てを受けることがある）
    ("今日の本題", "game_monhun_quest_start"), ("e01b_theme", "game_smash_ready_go"), ("タダになる箱", "anime_doraemon_gadget"),
    ("6分の1", "game_dq_miss"), ("反抗期", "game_mgs_alert"), ("前借り", "game_aceattorney_desk_slam"),
    ("上乗せ", "game_mario_1up"), ("約286万円", "game_dq_level_up"), ("70万も", "game_zelda_item_get"),
    ("うまくいけば", "game_smash_zannen"), ("前は　18歳まで", "game_dq_attack_enemy"), ("無期限", "game_airride_checker"),
    ("じいじが", "game_dq_inn"), ("親ガチャ", "tv_gakitsuka_dedeen"), ("溶かされたら", "game_undertale_encounter"),
    ("限って", "anime_shinchan_taraan"), ("打ち切り", "game_smash_gameset"), ("パッチ", "game_minecraft_anvil"),
    ("スカスカ", "tv_dokkiri_tettere"), ("家庭しだい", "tv_professional_poon"),
    ("そもそも\nなんだっけ", "pikon"), ("タダになる箱", "idea_newtype_01"), ("個別の株", "buzzer_wrong"),
    ("投資信託だけね", "tsukkomi_bishi"), ("始めないと損", "question_hatena_maou"), ("時間を\n味方", "shine_kira_01"),
    ("じいじが", "pinpon_notice"), ("どっちが先", "pi"), ("親が先って", "hyoshigi_01"), ("使う人が\n少なかった", "fall_hyuu"),
    ("スカスカ", "deflate_hyororo"), ("選択肢が\n増えた", "taiko_kaka"),
    ("e00_notice", {"f": "chime_announce", "len": 3.0, "gain": -2}), ("e01_title", "chirin"), ("e01b_theme", "jan"),
    ("口座の受付", "quiz_question_01"), ("2027年1月から", "card_place"), ("子どもが\n投資", "question_hatena_maou"),
    ("動かすのは", "tsukkomi_bishi"), ("なにが違う", "pi"), ("今日の本題", "shine_kiraan_maou"),
    ("名前で作る", "page_turn_01"), ("合計600万円まで", "card_flip"), ("税金がかからない", "shine_kira_01"),
    ("月5万か", "pikon"), ("10年で600万", "idea_newtype_01"), ("月5万は\nムリ", "tsukkomi_bashi"),
    ("積立向けの投資信託", "page_turn_02"), ("親権者", "card_place"), ("ややこしいな", "silly"),
    ("比べてみると", "xylophone_transition"), ("6分の1", "fall_hyuu"), ("12歳まで\nNG", "kon"),
    ("引き出せないの", "boing_fail"), ("12歳未満は", "doon_heavy"), ("子どものための出費", "pinpoon_note"),
    ("使い道の書類", "pc_warning"), ("反抗期", "explosion_chudoon"), ("交渉する", "taiko_kaka"),
    ("自動で「ふつう", "whoosh_shu"), ("1,800万円に含まれる", "doon_movie"), ("1,200万", "card_flip"),
    ("前借り", "punch"),
    ("家族の非課税", "pinpoon_correct"), ("もう埋まりそう", "cursor_move_01"), ("上乗せ", "shine_kira_01"),
    ("18年も運用", "button_13"), ("入れたお金は216", "card_place"), ("約286万円", "fanfare_pararappara"),
    ("70万も", "voice_uuwaa"), ("うまくいけば", "deflate_hyororo"), ("ジュニアNISA」の反省", "page_turn_02"),
    ("前は　18歳まで", "buzzer_wrong"), ("無期限", "pinpoon_correct"), ("入学金", "jan"),
    ("援助の受け皿", "button_26"), ("110万円を超える", "pc_warning"), ("目が回る", "spring_byoin"),
    ("イマイチという声", "quiz_question_02"), ("親のNISAを埋める", "pi"), ("いつでも\n引き出せる", "pikon"),
    ("無理ゲー", "kon"), ("余裕のある家", "pi"), ("金持ちの子", "boon"), ("親ガチャ", "boing_01"),
    ("ルールがめんどう", "pi"), ("ハードル高い", "tear_drop"), ("18歳で子ども", "pi"), ("溶かされたら", "glass_break_01"),
    ("限って", "car_brake"), ("減ることもある（", "pi"), ("シャレにならん", "shock_piano"),
    ("どうせまた制度", "pi"), ("打ち切り", "explosion_dokaan"), ("パッチ", "kote"), ("また変わりそう", "silly"),
    ("一方で", "whoosh_shu"), ("ビール党", None), ("出産祝い", None), ("お金の勉強", "pinpoon_correct"),
    ("向いているのは", "pinpoon_note"), ("向いていないのは", "buzzer_wrong"), ("まず親の枠", "taiko_kaka"),
    ("追加の箱", "idea_newtype_01"), ("まず自分の", "hyoshigi_01"),
    ("e07_matome", "chiin_01"), ("家庭しだい", "hyoshigi_02"), ("自分のNISAから", "pikoon_retro"),
    ("e08_ending", "chirin"),
]

# 猫ミーム素材を途中で切らずに最後まで流すカット（切る秒は assets/play.json）
FULL = ["よっしゃ", "出産祝い"]


def apply_se(cuts):
    for c in cuts:
        k = " ".join(str(c.get(x) or "") for x in ("say", "sub"))
        if any(f in k for f in FULL) and c.get("cats"):
            c["cats"][0]["full"] = True
            cfg = R.ASSET_PLAY.get(c["cats"][0]["a"], {})
            if cfg.get("until"):
                c["cats"][0]["until"] = cfg["until"]
    for c in cuts:
        key = " ".join(str(c.get(k) or "") for k in ("say", "sub", "card", "layers"))
        for snip, se in SE_MAP:
            if snip in key:
                if se is not None:
                    c["se"] = se
                break
    return cuts


def cuts_full():
    return apply_se(cuts_all())


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "03_kodomo_nisa_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cuts = cuts_full()
    if sys.argv[1:] == ["--audio"]:
        R.remux_audio(cuts, out, out.replace(".mp4", "_a.mp4"))
        os.replace(out.replace(".mp4", "_a.mp4"), out)
        sys.exit()
    if len(sys.argv) > 1:
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=out.replace(".mp4", "_preview"))
