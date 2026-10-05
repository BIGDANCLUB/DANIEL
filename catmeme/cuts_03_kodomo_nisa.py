"""03_kodomo_nisa（こどもNISA）のカット割り。原稿 scripts/03_kodomo_nisa.md。

v2: 参考動画（ニャースインフォ）ふうの作り
  - 猫は2匹ずつ並べて掛け合い。足元に色つきの役名札（ニュース猫=赤、博識な猫=青、パパ猫=緑、ネットの声=紫）
  - セリフは画面上に白い縁取り文字。強調は赤い文字＋集中線＋画面の揺れ
  - 図は画面の真ん中に差し込み、両側に猫。下に説明の字幕
  - 事実の説明は「説明モード」（画面を灰色の小窓に縮めて、黒地に説明文）
  - 場面の区切りは黒い画面に小さな文字（「本題に入るその前に…」など）
  - 場面転換は白飛びなしのパッと切り替え＋シュッという音。BGMは前より大きめ

python3 catmeme/cuts_03_kodomo_nisa.py          → out/03_kodomo_nisa_full.mp4
python3 catmeme/cuts_03_kodomo_nisa.py --audio  → 音だけ作り直す
python3 catmeme/cuts_03_kodomo_nisa.py 0:10     → 先頭10カットだけ
"""
import os
import sys

import render as R

R.NYAS_STYLE = True     # 文字がポンと飛び出す
R.WHITE_DIP = 0.0       # 白飛びの転換はしない（パッと切り替え）
R.FG_DUCK = -9          # 猫の音・SEが鳴っている間のBGMの下げ幅（前は -20。参考動画はBGMが大きめ）

HERE = os.path.dirname(os.path.abspath(__file__))
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("03_kodomo_nisa", "02_october", "01_todai")]   # 前の動画の背景も使い回す
PT = os.path.join(HERE, "parts", "03_kodomo_nisa")
BGM = os.path.join(HERE, "bgm")

PURPLE = os.path.join(BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
COCOA = os.path.join(BGM, "星降る夜のホットココア.mp3")
MIRAI = os.path.join(BGM, "未来を創る君たちへ.mp3")
KAMI = os.path.join(BGM, "神の怒り.mp3")

NORA = os.path.join(BGM, "野良猫は宇宙を目指した.mp3")
NEWS, SAGE, PAPA, NET = (215, 35, 35), (40, 90, 200), (35, 140, 65), (120, 50, 170)
ROLE = {"ニュース猫": NEWS, "博識な猫": SAGE, "パパ猫": PAPA, "ネットの声": NET}


def bg(n):
    for d in BGS:
        p = os.path.join(d, n + ".png")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(n)


def pt(n):
    return os.path.join(PT, n + ".png")


def cat(a, role, x, h=640, bottom=1010, **kw):
    return dict(a=a, x=x, h=h, bottom=bottom, label=role, label_color=ROLE[role], label_size=kw.pop("label_size", 66), **kw)


# 右の猫（博識な猫など）がしゃべるセリフ。それ以外は左の猫がしゃべる
RIGHT_LINES = ["実際に動かすのは", "タダになる箱", "毎月5万なら", "個別の株は", "お小遣いアップ", "そういう家は",
               "うまくいけば", "早く始めるほど", "親のNISAなら", "追加の箱", "家庭しだい"]


def duo(b, left, right, say, **kw):
    """2匹並べての掛け合い。left/right = (素材, 役名)。セリフは画面の上。しゃべっていない方の猫の音は消す。"""
    right_talks = any(k in say for k in RIGHT_LINES)
    cats = [cat(left[0], left[1], 500, h=760, bottom=1040, flip=kw.pop("lflip", False), mute=right_talks),
            cat(right[0], right[1], 1430, h=760, bottom=1040, flip=kw.pop("rflip", False), mute=not right_talks)]
    return dict(bg=bg(b), cats=cats, say=say, text_top=True, **kw)


def solo(b, a, role, say, side="L", **kw):
    """1匹だけ。セリフは猫の反対側。"""
    x = 500 if side == "L" else 1420
    return dict(bg=bg(b), cats=[cat(a, role, x, h=kw.pop("h", 720), flip=kw.pop("flip", False))], say=say, **kw)


def close(b, a, role, say, red=True, **kw):
    """驚きのアップ。赤い文字＋集中線＋揺れ。"""
    c = cat(a, role, kw.pop("x", 960), h=kw.pop("h", 760), bottom=1060, float=True, flip=kw.pop("flip", False))
    return dict(bg=bg(b), cats=[c], say=say, text_top=True, say_style="red" if red else None,
                fx=["lines", "shake"], **kw)


def dia(c, sub, b="bg03_blackboard", left=None, right=None, **kw):
    """図を大きく差し込み、右下に小さめの猫1匹、下に説明の字幕。"""
    who = right or left
    cats = [cat(who[0], who[1], 1790, h=400, bottom=1060, float=True, label_size=54)] if who else []
    return dict(bg=bg(b), inset={"card": pt(c), "box": (40, 15, 1660, 815)}, cats=cats, sub=sub,
                sub_box=(60, 820, 1600, 1070), sub_size=70, **kw)


def expl(b, cats, say, text, **kw):
    """説明モード：直前の場面を灰色の小窓にして、黒地に説明文。"""
    return dict(bg=bg(b), cats=cats, say=say, text_top=True, explain=text, no_pop=True, **kw)


def chap(text, **kw):
    return dict(bg=None, chapter=text, chapter_size=140, dur=kw.pop("dur", 1.8), se=kw.pop("se", "whoosh_shu"), **kw)


def place(b, text, **kw):
    return dict(bg=bg(b), place=text, dur=kw.pop("dur", 1.4), fx=["zoom"], **kw)


def net(a, say, tag="ネットの声", **kw):
    c = cat(a, "ネットの声", 500, h=700)
    c["label"] = tag
    return dict(bg=bg("bg09_sns"), cats=[c], say=say, **kw)


def pops(*items):
    """時間差で出る文字。items = (秒, 文字, (x0,y0,x1,y1)[, "red"])。それぞれポンの音つき。"""
    out = []
    for it in items:
        out.append({"t": it[0], "text": it[1], "box": it[2], "dur": 9, "size": 100, "style": it[3] if len(it) > 3 else None})
    return out


def pop_se(*ts, f="pop"):
    return [{"f": f, "at": t, "gain": -6} for t in ts]


# 掛け合いの組み合わせ（同じ素材が続けて出すぎないよう、場面ごとに猫を変える）
def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(card=None, layers=[pt("e00_notice")], dur=3.4, se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- 1. つかみ ----
        dict(bg=bg("bg19_kids_room"), card=pt("e01_title"), dur=2.4, bgm={"file": PURPLE, "gain": -2}, se="jan",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        chap("話は2026年10月1日…"),
        dict(bg=bg("bg20_counter"), sub="「こどもNISA」の\n口座の受付が\nスタート", say_style="red", fx=["lines"],
             cats=[cat("work_typing_cat", "博識な猫", 470, h=640)], se="doon_movie"),
        duo("bg20_counter", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "こどもNISA？\n子どもが投資すんの？", se="question_hatena_maou"),
        duo("bg20_counter", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "いや、実際に動かすのは親な", se="tsukkomi_bishi"),
        close("bg20_counter", "confused_i_dont_know_cat", "ニュース猫",
              "え、じゃあ\n親のNISAと何が違うのよ", red=False, flip=True, se="boing_fail"),
        duo("bg20_counter", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "てか、NISAって\nそもそもなんだっけ", se="pikon"),
        duo("bg20_counter", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "投資で増えた分の税金が\nタダになる箱な", se="anime_doraemon_gadget"),
        dict(bg=bg("bg06_spotlight"), say="今日のテーマ", text_top=True, dur=3.4, se=["jan"] + pop_se(0.7, 1.4, 2.1),
             cats=[cat("showoff_gojo_cosplay_cat", "博識な猫", 1640, h=560, float=True)],
             pops=pops((0.7, "① ふつうのNISAとの違い", (80, 330, 1300, 470)),
                       (1.4, "② お得なところ", (80, 520, 1300, 660)),
                       (2.1, "③ イマイチなところ", (80, 710, 1300, 850), "red"))),
        # ---- 2. こどもNISAってなに？ ----
        chap("まずは　きほんから", dur=1.4, bgm={"file": NORA, "gain": -2}),
        dia("e02_basic", "0〜17歳の子どもの名前で作る　NISAの口座", "bg19_kids_room",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="page_turn_01"),
        dia("e02_basic", "1年に60万円まで　合計600万円まで", "bg19_kids_room",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="card_flip"),
        dia("e02_basic", "増えた分に　税金がかからない（ふつうは約20％）", "bg19_kids_room",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="shine_kira_01"),
        duo("bg19_kids_room", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "60万って、月5万か", se="pikon"),
        duo("bg19_kids_room", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "そう。毎月5万なら\n10年で600万に届く", se="idea_newtype_01"),
        close("bg16_food_aisle", "despair_dramatic_kitten", "ニュース猫", "いや月5万は\nムリだって！！",
              se=["doon_heavy", "tsukkomi_bashi"]),
        dia("e02_basic", "買えるのは　国が選んだ「積立向けの投資信託」だけ", "bg19_kids_room",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="page_turn_02"),
        dia("e02_basic", "お金を出して運用するのは　親など（親権者）", "bg19_kids_room",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="card_place"),
        duo("bg19_kids_room", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "・・・", se="silly", dur=1.4),
        duo("bg19_kids_room", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "子どもの名前で\n親が運用……ややこしいな", se="cursor_move_01"),
        # ---- 3. ふつうのNISAとの違い ----
        chap("ふつうのNISAと　なにが違う？", se="quiz_question_01"),
        dia("e03_compare", "ふつうのNISAと　比べてみると", "bg20_counter",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="xylophone_transition"),
        dia("e03_compare", "枠は　大人の6分の1くらい", "bg20_counter",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="game_dq_miss"),
        duo("bg20_counter", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "しかも個別の株は\n買えないからな", se="buzzer_wrong"),
        duo("bg20_counter", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "引き出し\n12歳までNGって……", se="kon",
            pops=pops((1.2, "？？？", (60, 380, 600, 520))), ),
        close("bg20_counter", "realize_wet_cat_stare", "ニュース猫", "引き出せないの\nキツくね！？",
              se=["doon_heavy"]),
        dia("e03b_withdraw", "12歳未満は　原則引き出せない（大きな災害などだけ例外）", "bg21_school_gate",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="doon_heavy"),
        dia("e03b_withdraw", "12歳からは　子どものための出費なら引き出せる", "bg21_school_gate",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="pinpoon_note"),
        dia("e03b_withdraw", "ただし　子どもの同意と　使い道の書類が必要", "bg21_school_gate",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="pc_warning"),
        close("bg21_school_gate", "angry_cat_hits_cat", "ニュース猫", "子どもの同意！？\n反抗期だったら詰むじゃん",
              se=["game_mgs_alert"]),
        duo("bg21_school_gate", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "お小遣いアップで\n交渉するしかない", se="taiko_kaka"),
        dia("e03b_withdraw", "18歳になると　自動で「ふつうのNISA」に引っ越し", "bg20_counter",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="whoosh_shu"),
        expl("bg20_counter", [cat("@react", "ニュース猫", 520), cat("@calm", "博識な猫", 1420)],
             "え、600万使ってたら……", "実は　こどもNISAで使った枠は\n大人になってからの1,800万円に含まれます", dur=3.6,
             se="doon_movie"),
        dia("e03c_1800", "18歳からの残りは　1,200万円", "bg20_counter",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="card_flip"),
        close("bg20_counter", "glare_disgusted_cat", "ニュース猫", "将来の枠を\n前借りしてるだけじゃん！",
              se=["game_aceattorney_desk_slam"]),
        # ---- 4. お得なところ ----
        chap("じゃあ　お得なところは？", se="quiz_question_02"),
        dia("e04_merit", "① 家族の非課税の枠が増える", "bg14_home_night",
            left=("@papa", "パパ猫"), right=("@calm", "博識な猫"), se="pinpoon_correct"),
        duo("bg14_home_night", ("@papa", "パパ猫"), ("@calm", "博識な猫"),
            "うち、自分のNISA枠\nもう埋まりそうでさ", se="cursor_move_01"),
        duo("bg14_home_night", ("@papa", "パパ猫"), ("@calm", "博識な猫"),
            "そういう家は\n子どもの分600万が上乗せ", se="game_mario_1up"),
        solo("bg14_home_night", "joy_happy_happy_happy_cat", "パパ猫", "よっしゃ\n枠増えた", side="L", sound=True),
        dia("e04_merit", "② 0歳から始めると　18年も運用できる", "bg19_kids_room",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="button_13"),
        dia("e04b_sim", "月1万円を0歳から18年　入れたお金は216万円", "bg19_kids_room",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="card_place"),
        dia("e04b_sim", "年3％で増えたら　約286万円（※仮の計算。減ることもある）", "bg19_kids_room",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="game_dq_level_up"),
        close("bg19_kids_room", "weird_meowing_cat", "ニュース猫", "70万も\n増えてんの！？", se=["game_zelda_item_get"]),
        duo("bg19_kids_room", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "あくまで\n“うまくいけば”な", se="game_smash_zannen"),
        duo("bg19_kids_room", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "じゃあ0歳から\n始めないと損？", se="question_hatena_maou"),
        duo("bg19_kids_room", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "早く始めるほど\n時間を味方にできるってだけな", se="shine_kira_01"),
        dia("e04c_junior", "③ 前の制度「ジュニアNISA」の反省で　使いやすくなった", "bg03_blackboard",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="page_turn_02"),
        dia("e04c_junior", "前は　18歳まで原則引き出せず　非課税も5年だけ", "bg03_blackboard",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="game_dq_attack_enemy"),
        dia("e04c_junior", "こどもNISAは　12歳から教育費に使える・非課税は無期限", "bg03_blackboard",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="game_airride_checker"),
        solo("bg21_school_gate", "mock_swinging_cat", "ニュース猫", "中学・高校の\n入学金に使えるのはデカい",
             side="L", se="jan"),
        dia("e04_merit", "④ おじいちゃん・おばあちゃんからの援助の受け皿にもなる", "bg14_home_night",
            left=("@papa", "パパ猫"), right=("@calm", "博識な猫"), se="pinpon_notice"),
        duo("bg14_home_night", ("@papa", "パパ猫"), ("@calm", "博識な猫"),
            "じいじが孫のために\n何かしたいって言っててさ", se="cursor_move_02"),
        expl("bg14_home_night", [cat("@papa", "パパ猫", 520), cat("@calm", "博識な猫", 1420)],
             "", "ただし　もらったお金が1年で合計110万円を超えると\n贈与税がかかることがあるので注意", dur=3.4, se="pc_warning"),
        close("bg14_home_night", "spin_spinning_cat", "ニュース猫", "税金の話\n多すぎて目が回る", red=False,
              se=["spring_byoin"]),
        # ---- 5. イマイチなところ ----
        chap("でも　イマイチという声も多い…", se="doon_heavy",
             bgm={"file": COCOA, "gain": -2}),
        dia("e05_demerit", "① 「まず親のNISAを埋めるのが先」", "bg03_blackboard",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="pi"),
        duo("bg03_blackboard", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "親のNISAなら\nいつでも引き出せるし\n枠もデカいからな", se="pikon"),
        net("sleep_sleeping_cat", "親の枠すら\n埋まってないのに\n子どもの分とか\n無理ゲー", "親の声", se="kon"),
        dia("e05_demerit", "② 「お金に余裕のある家しか使えない」", "bg03_blackboard",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="pi"),
        net("rage_talking_cat", "結局\n金持ちの子が\nさらに有利に\nなるだけ", "格差を心配する声", se="boon"),
        close("bg09_sns", "laugh_laughing_dog", "ネットの声", "親ガチャを\n国が強化してて草", se=["tv_gakitsuka_dedeen"]),
        dia("e05_demerit", "③ 引き出しのルールがめんどう", "bg03_blackboard",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="pi"),
        net("confused_i_dont_know_cat", "12歳まで使えない\nその後も書類\nハードル高い", "親の声", se="tear_drop"),
        dia("e05_demerit", "④ 18歳で子どものお金になる", "bg03_blackboard",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="pi"),
        close("bg14_home_night", "tense_two_cats_face_off", "パパ猫", "18歳でいきなり数百万……\n全部溶かされたら！？",
              se=["game_undertale_encounter"]),
        solo("bg14_home_night", "dance_wild_dog", "パパ猫", "うちの子に限って……\nいや、ありうる", side="R",
             se="anime_shinchan_taraan"),
        dia("e05_demerit", "⑤ 投資だから　減ることもある（アンケートでも不安の1位）", "bg03_blackboard",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="pi"),
        solo("bg02_room", "sad_banana_cat_cry", "ニュース猫", "教育費が減ったら\nシャレにならん", side="L", se="shock_piano"),
        dia("e05_demerit", "⑥ 「どうせまた制度が変わる」", "bg03_blackboard",
            left=("@react", "ニュース猫"), right=("@calm", "博識な猫"), se="pi"),
        expl("bg03_blackboard", [cat("@react", "ニュース猫", 520), cat("@calm", "博識な猫", 1420)],
             "", "前の制度「ジュニアNISA」は　使う人が少なく\n2023年で廃止されました", dur=3.4, se="fall_hyuu"),
        close("bg06_spotlight", "angry_shooting_cat", "ニュース猫", "前作、\n打ち切りだったの！？",
              se=["explosion_dokaan"], sting={"file": KAMI, "len": 4.0, "gain": -16}),
        net("mock_swinging_cat", "国のNISA\n毎回パッチ\n当てすぎ", "制度への不信", se="game_minecraft_anvil"),
        net("huh_goat_talks_to_huh_cat", "子どもが\n18歳になる前に\nまた変わりそう", "制度への不信", se="silly"),
        chap("一方で…", dur=1.2),
        net("happy_chipi_chapa_cat", "出産祝いを\n預ける先が\nできてありがたい", "歓迎する声", sound=True),
        net("wave_waving_cat", "子どもと一緒に\nお金の勉強が\nできる", "歓迎する声", se="pinpoon_correct"),
        # ---- 6. どんな家に向いてる？ ----
        chap("結局　どんな家に向いてる？", se="quiz_question_01"),
        dia("e06_fit", "向いているのは　親のNISAが埋まりそう・祖父母の援助がある家", "bg14_home_night",
            left=("@papa", "パパ猫"), right=("@calm", "博識な猫"), se="pinpoon_note"),
        dia("e06_fit", "向いていないのは　親のNISAがまだ空いている・すぐ使うかもしれないお金", "bg14_home_night",
            left=("@papa", "パパ猫"), right=("@calm", "博識な猫"), se="buzzer_wrong"),
        duo("bg14_home_night", ("@papa", "パパ猫"), ("@calm", "博識な猫"),
            "余裕がある家の\n“追加の箱”って考えると\nわかりやすい", se="idea_newtype_01"),
        close("bg14_home_night", "calmdown_dancing_cat", "パパ猫", "……うち、\n親の枠もスカスカだわ", red=False,
              se=["tv_dokkiri_tettere"]),
        # ---- 7. まとめ ----
        dict(bg=bg("bg03_blackboard"), inset={"card": pt("e07_matome"), "box": (200, 60, 1720, 860)}, dur=4.4,
             cats=[cat("excited_hodomoe_city_cat", "ニュース猫", 1750, h=380, bottom=1060, float=True)],
             bgm={"file": MIRAI, "gain": -2, "fade": 0.8}, se="chiin_01"),
        duo("bg02_room", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "お得かどうかは\n家庭しだいってわけ", se="tv_professional_poon"),
        duo("bg02_room", ("@react", "ニュース猫"), ("@calm", "博識な猫"),
            "結局、余裕ある家の\n選択肢が増えたってことね", se="taiko_kaka"),
        solo("bg02_room", "drive_driving_cat", "ニュース猫", "とりあえず\n自分のNISAから\nちゃんとやるわ", side="L",
             se="pikoon_retro"),
        dict(bg=bg("bg03_blackboard"), card=pt("e08_ending"), dur=3.0, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
    ]


# 猫ミーム素材を途中で切らずに最後まで流すカット（切る秒は assets/play.json）
FULL = ["よっしゃ", "出産祝い"]


def apply_fx(cuts):
    for c in cuts:
        k = " ".join(str(c.get(x) or "") for x in ("say", "sub"))
        if any(f in k for f in FULL) and c.get("cats"):
            c["cats"][0]["full"] = True
            cfg = R.ASSET_PLAY.get(c["cats"][0]["a"], {})
            if cfg.get("until"):
                c["cats"][0]["until"] = cfg["until"]
    # 場所（背景）が変わるカットの頭にシュッという音（すでに付いている音とは重ねる）
    prev = None
    for c in cuts:
        if c.get("bg") != prev and prev is not None:
            se = c.get("se")
            lst = [] if not se else ([se] if isinstance(se, (str, dict)) else list(se))
            if not any((s if isinstance(s, str) else s.get("f")) == "whoosh_shu" for s in lst):
                lst = [{"f": "whoosh_shu", "gain": -10}] + lst
            c["se"] = lst
        prev = c.get("bg")
    return cuts


# 猫ミームの自動の割り当て（"@react" などの所）。役名はそのままで、セリフごとに素材を入れ替える。
# 同じ素材は1本で3回まで、前後2場面には同じ素材を出さない。曲つき・長さ指定の素材は自動では選ばない
POOLS = {
    "react": ["surprise_big_pupils_cat", "huh_huh_cat", "realize_wet_cat_stare", "peek_what_happen_cat", "weird_meowing_cat",
              "blank_black_cat_zoning_out", "glare_disgusted_cat", "spit_not_my_taste_cat", "sulk_hungry_cat",
              "angry_cat_hits_cat", "fight_cat_fight", "rage_talking_cat", "leave_cat_leaves_home", "sad_banana_cat_cry",
              "spin_spinning_cat", "mock_swinging_cat", "sleepy_sleepy_cat", "sleep_sleeping_cat", "angry_aiming_cat",
              "tense_two_cats_face_off"],
    "calm": ["itchy_kitten_butt", "calm_black_face_sheep", "work_typing_cat", "think_bike_front_seat_cat",
             "call_customer_service_cat", "cocky_dj_cat", "showoff_gojo_cosplay_cat", "drive_driving_cat",
             "drive_monkey_golf_cart", "ride_kitten_bike", "slack_nail_filing_cat", "eat_crunchy_cat_luna", "eat_pop_cat",
             "taunt_cat_and_scared_dog", "wakeup_dog_hits_bowl", "sleepy_old_memories_cat", "listen_dancing_dog",
             "excited_hodomoe_city_cat"],
    "papa": ["shady_dancing_man", "dance_wild_dog", "dance_edm_cat", "calmdown_dancing_cat", "dance_trending_cat",
             "dance_wop_cat", "happy_girlfriend_dance_cat", "laugh_laughing_dog", "dance_koto_nai_cat"],
}
FALLBACK = {"react": ["papa", "calm"], "calm": ["papa", "react"], "papa": ["calm", "react"]}


def allocate(cuts, max_use=3, gap=2):
    count, last = {}, {}
    for i, c in enumerate(cuts):   # 指定ずみの素材を先に数える
        for k in c.get("cats", []):
            if not k["a"].startswith("@"):
                count[k["a"]] = count.get(k["a"], 0) + 1
    fixed_at = {}
    for i, c in enumerate(cuts):
        for k in c.get("cats", []):
            if not k["a"].startswith("@"):
                fixed_at.setdefault(k["a"], []).append(i)
    for i, c in enumerate(cuts):
        here = {k["a"] for k in c.get("cats", [])}
        for k in c.get("cats", []):
            if not k["a"].startswith("@"):
                last[k["a"]] = i
                continue
            pool = k["a"][1:]
            def ok(a):
                near_fixed = any(abs(j - i) <= gap for j in fixed_at.get(a, []))
                return (count.get(a, 0) < max_use and a not in here and i - last.get(a, -99) > gap and not near_fixed)
            for name in [pool] + FALLBACK[pool]:
                cands = [a for a in POOLS[name] if ok(a)]
                if cands:
                    break
            else:
                raise RuntimeError(f"cut {i}: 猫ミームが足りない")
            a = min(cands, key=lambda a: (count.get(a, 0), last.get(a, -99)))
            k["a"] = a
            count[a] = count.get(a, 0) + 1
            last[a] = i
            here.add(a)
    return cuts


def cuts_full():
    return apply_fx(allocate(cuts_all()))


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
