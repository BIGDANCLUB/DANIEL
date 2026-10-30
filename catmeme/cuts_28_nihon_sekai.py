"""28_nihon_sekai（日本で高い物・安い物 世界とくらべてみた）のカット割り（10/29 ユーザー指定）。3分ほど。
人気の「日本vs世界」ショートとつなげる長い動画。持ち家vs賃貸と同じく、画面を左右半分に分けてくらべる（左＝日本・右＝世界）。

python3 catmeme/cuts_28_nihon_sekai.py          → out/28_nihon_sekai_full.mp4
python3 catmeme/cuts_28_nihon_sekai.py --charts → グラフの動く背景だけ作る

ルールは車・持ち家の動画と同じ（コナン＝「!?」・ポーン＝「え…」、1回目はふつう・連打は2回まで・集中線は控えめ）。
値段はざっくりの目安（1ドル＝155円・1ポンド＝195円）：
  ビッグマック 日本 約480円／アメリカ 約900円（5.8ドル）／スイス 約1300円
  ランチ 日本 約1000円／ニューヨーク 約3500円（チップ込み）。ラーメン ニューヨークで 約3000円以上
  電車の初乗り 東京 約180円／ニューヨーク 約450円（2.9ドル）／ロンドン 約540円（2.8ポンド・ICカード）
  病院（かぜで受診） 日本 約2000円（3割負担）／アメリカ 保険によっては 数万円
  ガソリン1L 日本 約170円／アメリカ 約145円。高速道路 東京→大阪 約1万3000円／アメリカは無料の道が多い
  家賃（ワンルーム）東京 約10万円／ニューヨーク 50万円以上（3500ドル前後）。コンビニのおにぎり 日本 約200円／ニューヨーク 500円〜
  円：10年ほど前は1ドル110円前後 → 155円前後。日本の給料は30年ほどあまり変わっていない
原稿のルール：実在の人・会社・お店の名前は出さない（ビッグマックは物価くらべの目安として名前だけ）。どの国もけなさない
"""
import glob
import os
import sys

import cuts_04_leak as L
import cuts_26_kuruma as K
import render as R
import wide_bars as B

R.TEMPO = 1.15   # 字幕と金額を読める速さ
HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", "28_nihon_sekai")] + sorted(
    d for d in glob.glob(os.path.join(HERE, "backgrounds", "*")) if os.path.isdir(d))
L.PT = os.path.join(HERE, "parts", "28_nihon_sekai")
pt, cat, chap, fx, CONAN, POON = L.pt, L.cat, L.chap, K.fx, K.CONAN, K.POON
PURPLE, COCOA, MIRAI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.NORA
L.ROLE["日本の猫"] = (200, 30, 30)
L.ROLE["世界の猫"] = (0, 110, 210)

# 背景（ChatGPT で作る背景が届いたら backgrounds/28_nihon_sekai に同じ名前で置けば差しかわる。指示文 scripts/28_nihon_sekai_bg_prompts.md）
JP_ST, NY_ST, JP_FOOD, NY_FOOD, JP_TRAIN, NY_TRAIN, JP_HOSP, NY_HOSP, JP_ROAD, US_ROAD, WORLD, MONEY, BOARD = (
    "bg48_clean_street", "bg28_ny_street", "bg47_ramen_shop", "bg28_ny_diner", "bg54_station_crowd_map", "bg28_ny_subway",
    "bg28_jp_clinic", "bg28_us_hospital", "bg28_jp_highway", "bg28_us_highway", "bg44_world_map", "bg87_refund_money",
    "bg03_blackboard")
K.STANDIN.update({NY_ST: "bg114_singapore_bay", NY_FOOD: "bg13_izakaya", NY_TRAIN: "bg45_airport_arrival",
                  JP_HOSP: "bg25_office_desk", NY_HOSP: "bg24_server_room", JP_ROAD: "bg63_hokkaido_field",
                  US_ROAD: "bg63_hokkaido_field"})
bg = K.bg
_bbg = B._bg


def _chart_bg(n):
    try:
        return _bbg(n)
    except FileNotFoundError:
        return _bbg(K.STANDIN[n])


B._bg = _chart_bg

# ---- グラフ（左＝日本・右＝世界） ----
K.CHARTS.update({
    "w1_bigmac": B.Chart([("日本", "red"), ("アメリカ", "blue"), ("スイス", "purple")],
                         [(0.4, 0, "", 480, "red"), (1.2, 1, "", 900, "blue"), (2.0, 2, "", 1300, "purple")], 1400,
                         bg=JP_FOOD, head="ビッグマック1個の値段（目安）", total_fmt="{v}円", highlight=0),
    "w2_lunch": B.Chart([("東京", "red"), ("ニューヨーク", "blue")], [(0.4, 0, "", 1000, "red"), (1.4, 1, "チップ込み", 3500, "blue")],
                        3800, bg=NY_FOOD, head="お昼ごはん1回（目安）", total_fmt="{v}円"),
    "w3_train": B.Chart([("東京", "red"), ("ニューヨーク", "blue"), ("ロンドン", "purple")],
                        [(0.4, 0, "", 180, "red"), (1.2, 1, "", 450, "blue"), (2.0, 2, "", 540, "purple")], 600,
                        bg=JP_TRAIN, head="電車・地下鉄の初乗り（目安）", total_fmt="{v}円", highlight=0),
    "w4_hosp": B.Chart([("日本", "red"), ("アメリカ", "blue")], [(0.4, 0, "3割負担", 2000, "red"), (1.4, 1, "保険しだい", 30000, "blue")],
                       32000, bg=JP_HOSP, head="かぜで病院に行ったとき（目安）", total_fmt="{v}円〜"),
    "w5_gas": B.Chart([("日本", "red"), ("アメリカ", "blue")], [(0.4, 0, "", 170, "red"), (1.4, 1, "", 145, "blue")], 190,
                      bg=JP_ROAD, head="ガソリン1リットル（目安）", total_fmt="{v}円", highlight=0),
    "w6_yen": B.Chart([("10年前", "green"), ("今", "red")], [(0.4, 0, "", 110, "green"), (1.4, 1, "", 155, "red")], 170,
                      bg=MONEY, head="1ドルを買うのに必要な円（目安）", total_fmt="{v}円", highlight=1),
})
K.DROP_SE.update({"w1_bigmac": {1: "anime_dbz_punch", 2: "explosion_chudoon"}, "w2_lunch": {1: "explosion_chudoon"},
                  "w3_train": {1: "game_mario_jump", 2: "game_dq_attack_enemy"}, "w4_hosp": {1: "explosion_chudoon"},
                  "w5_gas": {1: "pafu"}, "w6_yen": {1: "explosion_chudoon"}})
K.STEP_SE.update({k: ["game_coin_get_money_gain_happy"] for k in ("w1_bigmac", "w2_lunch", "w3_train", "w4_hosp", "w6_yen")})
K.STEP_SE["w5_gas"] = ["explosion_chudoon"]


def g(name, say, who="S", **kw):
    """グラフの場面（車の動画と同じ）。左はしの猫を「日本の猫」、右はしの猫を「世界の猫」にする。"""
    c = K.g(name, say, who=who, **kw)
    for q, role in zip(c["cats"], ("日本の猫", "世界の猫")):
        q.update(label=role, label_color=L.ROLE[role])
    return c


def sp(say, who="L", lb=JP_ST, rb=NY_ST, red=False, side=None, **kw):
    """画面半分（持ち家vs賃貸と同じ）：左＝日本（日本の猫）・右＝世界（世界の猫）。しゃべる側の上に字幕。side は左右の金額など。"""
    big, small = (700, 600) if not side else (600, 520)
    cats = [cat("@react", "日本の猫", 480, h=big if who == "L" else small, bottom=1075, label_size=54, mute=who != "L"),
            cat("@calm", "世界の猫", 1440, h=big if who == "R" else small, bottom=1075, label_size=54, mute=who != "R")]
    out = dict(bg=bg(lb), bg2=bg(rb), split=("日本", "世界"), split_cols=((200, 30, 30), (0, 110, 210)), split_y=232,
               split_tint=0.1, split_size=58, cats=cats, say=say,
               text_box=(30, 10, 930, 225) if who == "L" else (990, 10, 1890, 225), say_size=100, keep_overlap=True,
               side_text=side, **kw)
    if red:
        out.update(say_style="red", fx=["shake"])
    return out


def qq2(lb, rb, remix):
    """コナンの連打＋色とりどりの「？？？？？？」（画面半分のまま）。"""
    c = sp(None, "L", lb, rb)
    c.update(qmarks=6, qmark_y=420, se=[remix], dur=2.0, no_pop=True, fx=["flash", "ring"])
    return c


def card(c, sub, **kw):
    return L.dia(c, sub, BOARD, right=("@calm", "世界の猫"), dur=kw.pop("dur", 4.4), se=kw.pop("se", "card_flip"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(bg=bg(WORLD), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in (
                ("dance_tabby_standing_cat", 220, 600), ("walk_white_duck", 640, 520), ("dance_happy_banana_cat", 1000, 560),
                ("dance_three_kittens", 1360, 520), ("happy_hamster_open_arms", 1720, 560))],
             fx=["dim"], layers_top=[pt("e00_notice")], dur=6.0, no_pop=True, notice=True,
             se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- ① つかみ ----
        sp("最近 日本って\nなんでも高くない？", "L", se="pikon", bgm={"file": PURPLE, "gain": -4}),
        sp("世界から見ると\n日本は「安い国」だよ", "R", se="pi"),
        sp("日本が安い!?\nそんなわけ……", "L", red=True, se=CONAN),   # !? はコナン（1回目はふつう）
        dict(bg=bg(WORLD), card=pt("e01_title"), dur=4.0, se="jan",
             cats=[{"a": "dance_tabby_standing_cat", "x": 300, "h": 440, "bottom": 1050, "float": True, "mute": True},
                   {"a": "walk_white_duck", "x": 1640, "h": 420, "bottom": 1050, "float": True, "mute": True}]),
        card("e02_premise", "1ドル155円・おもにアメリカとくらべた目安", dur=5.0),
        # ---- ② 外食 ----
        chap("① 外食", se="quiz_question_01", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        sp("まずは\nハンバーガー", "R", JP_FOOD, NY_FOOD, se="pi"),
        g("w1_bigmac", "同じハンバーガーが\n国によってこんなにちがう", who="S", dur=3.8),
        sp("スイスだと\n日本の約3倍", "R", JP_FOOD, NY_FOOD, side=("約480円", "約1300円"), se="kon"),
        sp("ランチは\nどうかな？", "L", JP_FOOD, NY_FOOD, se="question_hatena_maou"),
        g("w2_lunch", "ニューヨークのランチは\n日本の3倍以上", who="S", dur=3.4),
        sp("ラーメン1杯\n3000円以上も", "R", JP_FOOD, NY_FOOD, side=("約1000円", "3000円〜"), se="pi"),
        fx(sp("え……\nさらにチップで\n2割上乗せ？", "L", JP_FOOD, NY_FOOD, se=POON), "mono"),   # え…はポーン（1回目はふつう）
        # ---- ③ 電車 ----
        chap("② 電車", se="whoosh_shu"),
        g("w3_train", "電車の初乗りも\n日本がいちばん安い", who="S", dur=3.8),
        sp("しかも日本の電車は\n時間どおりに来る", "R", JP_TRAIN, NY_TRAIN, se="pikon"),
        sp("それ世界だと\nすごいことなの？", "L", JP_TRAIN, NY_TRAIN, se="question_hatena_maou"),
        sp("数分おくれただけで\nおわびの放送が\n流れるのは日本くらい", "R", JP_TRAIN, NY_TRAIN, se="kon"),
        # ---- 家賃・コンビニ ----
        sp("家賃もちがう\nワンルームで", "R", JP_ST, NY_ST, side=("東京 約10万", "NY 50万以上"), se="pi"),
        sp("ニューヨークは\nルームシェアが\nふつうなんだって", "R", JP_ST, NY_ST, se="kon"),
        sp("コンビニのおにぎりも\n日本は200円くらい", "L", JP_ST, NY_ST, side=("約200円", "500円〜"), se="pikon"),
        sp("100円ショップも\n世界の人には大人気", "R", JP_ST, NY_ST, se="pi"),
        # ---- ④ 病院 ----
        chap("③ 病院", se="doon_heavy", bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        sp("日本は保険で\n3割だけはらう", "R", JP_HOSP, NY_HOSP, side=("約2000円", None), se="pi"),
        sp("アメリカは\n入っている保険しだい", "R", JP_HOSP, NY_HOSP, side=(None, "数万円も"), se="kon"),
        g("w4_hosp", "かぜでも\n数万円かかることも", who="S", dur=3.4),
        qq2(JP_HOSP, NY_HOSP, "anime_conan_hirameki_remix_a"),   # コナン連打（1回目）＋「？？？？？？」
        sp("かぜで\n数万円は\nこわすぎる……", "L", JP_HOSP, NY_HOSP, se="deflate_hyororo"),
        # ---- ⑤ 日本で高い物 ----
        chap("④ 日本で高い物", se="whoosh_shu", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        sp("でも日本のほうが\n高い物もある", "R", JP_ROAD, US_ROAD, se="pi"),
        g("w5_gas", "ガソリンは\n日本のほうが高い", who="S", dur=3.4),
        sp("高速道路も\n東京から大阪で\n約1万3000円", "R", JP_ROAD, US_ROAD, side=("約1万3000円", "無料の道が多い"), se="kon"),
        fx(sp("え……\nアメリカは\n無料なの？", "L", JP_ROAD, US_ROAD, se="tv_professional_poon_remix_a"), "swirl"),   # ポーン連打（1回目）
        sp("果物も高い\nメロン1玉\n1万円のものも", "R", JP_FOOD, NY_FOOD, se="pi"),
        sp("家の電気代も\n高めと言われる", "R", JP_ST, NY_ST, se="kon"),
        # ---- ⑥ なぜ日本は安い？ ----
        chap("⑤ なぜ日本は\n安いの？", se="doon_heavy", bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        sp("ひとつは\n円安", "R", MONEY, MONEY, se="pi"),
        g("w6_yen", "1ドルを買うのに\n前より45円も多く必要", who="S", dur=3.4),
        sp("世界からは\n日本の物が安く見える", "R", JP_ST, NY_ST, se="kon"),
        sp("もうひとつは\n給料があまり\n上がっていないこと", "R", MONEY, MONEY, se="kon"),
        sp("世界は物の値段も\n給料も上がってきた", "R", JP_ST, NY_ST, se="pi"),
        fx(sp("え……\n日本だけ\n止まってたの？", "L", MONEY, MONEY, se="tv_professional_poon_remix_b"), "mono"),   # ポーン連打（2回目）
        # ---- ⑦ 観光客から見ると ----
        chap("⑥ 観光客から見ると", se="whoosh_shu"),
        sp("観光客にとって日本は\n安くておいしい国", "R", JP_FOOD, NY_ST, se="pikon"),
        sp("だから観光客が\nどんどんふえている", "R", JP_ST, NY_ST, se="pi"),
        fx(sp("逆に日本から\n海外旅行に行くと\n全部高い!?", "L", JP_ST, NY_ST, red=True, se="anime_conan_hirameki_remix_b"), "money"),   # コナン連打（2回目）
        sp("ランチ1回で\n3500円は\nきびしい……", "L", JP_FOOD, NY_FOOD, se="deflate_hyororo"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        card("e07_points", "安い日本　高い日本　両方を知っておこう", dur=5.6),
        sp("外食・電車・病院は\n日本がとても安い", "R", JP_FOOD, NY_FOOD, se="kon"),
        sp("安いのはうれしいけど\n給料も上がってほしい", "L", JP_ST, NY_ST, se="kon"),
        dict(bg=bg(WORLD), card=pt("e10_ending"), dur=3.6, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


# ---- 10/30 ユーザー指定「エフェクトを増やし、SEの入るタイミング・数を増やす」 ----
MID_SE = ["game_coin_get_money_gain_happy", "anime_dbz_punch", "game_mario_jump", "game_dq_attack_enemy", "game_aceattorney_ping",
          "anime_shinchan_genkotsu", "game_ff_cursor", "anime_dbz_teleport", "kaan", "tsukkomi_bashi", "boing_02", "puni"]
NUM_SE = ["game_coin_get_money_gain_happy", "kaan", "game_aceattorney_ping", "frying_pan_kaan"]
EXTRA_FX = {9: "crack", 14: "money", 22: "money", 31: "money", 40: "crack", 46: "money"}   # ヒビ・お札をところどころに足す


def more(cuts):
    """どの場面も：頭の音に加えて、字幕・金額が出るところと場面のなかほどにも音。エフェクトも1場面に2〜3個。"""
    for i, c in enumerate(cuts):
        if c.get("notice") or c.get("chapter") or c.get("card") or c.get("inset"):   # 説明の画面は読みやすさ優先
            continue
        names = [x if isinstance(x, str) else x.get("f", "") for x in (c.get("se") or [])]
        if any("conan" in n_ or "poon" in n_ for n_ in names):   # コナン・ポーンの場面はその音だけ（ルールどおり）
            continue
        d = R.cut_dur(c)
        lst = list(c.get("se") or [])
        if c.get("side_text"):   # 左右の金額が出るところで、チャリン・カーンなど
            lst.append({"f": NUM_SE[i % len(NUM_SE)], "gain": -3, "at": 0.25})
        if d > 1.6:   # 場面のなかほどにもう1つ（ゲーム・アニメの音）
            lst.append({"f": MID_SE[i % len(MID_SE)], "gain": -6, "at": round(d * 0.55, 2)})
        if c.get("say_style") == "red":   # 赤字の驚きはドンと重ねる
            lst.append({"f": "explosion_dokaan", "gain": -6, "at": 0.05})
        c["se"] = lst
        fx_ = list(c.get("fx", []))
        fx_ += ["punch", "border"]
        if i % 3 == 0:
            fx_.append("ring")
        if i % 4 == 2 and not c.get("chart"):
            fx_ += ["flash", "zoom"]
        if i % 5 == 1 and not c.get("chart"):
            fx_.append("lines")
        if i in EXTRA_FX and not c.get("chart") and "mono" not in fx_ and "swirl" not in fx_:
            fx_.append(EXTRA_FX[i])
        c["fx"] = list(dict.fromkeys(fx_))
    return cuts


def cuts_full():
    return more(K.hype(L.apply_fx(L.allocate(cuts_all(), max_use=7, gap=1))))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "28_nihon_sekai_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if sys.argv[1:] == ["--charts"]:
        for k in ("w1_bigmac", "w2_lunch", "w3_train", "w4_hosp", "w5_gas", "w6_yen"):
            print(B.make(k, K.CHARTS[k], force=True))
        sys.exit()
    cuts = cuts_full()
    if sys.argv[1:] == ["--len"]:
        print(len(cuts), round(sum(R.cut_dur(c) for c in cuts), 1))
        sys.exit()
    if len(sys.argv) > 1:
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=out.replace(".mp4", "_preview"))
