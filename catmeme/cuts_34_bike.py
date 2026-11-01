"""34_bike（車vs125ccバイク 1年でかかるお金）のカット割り（10/31 ユーザー指定「車の有無の動画の要領で、自動車vs小型二輪」）。3分ほど。

python3 catmeme/cuts_34_bike.py          → out/34_bike_full.mp4
python3 catmeme/cuts_34_bike.py --charts → グラフの動く背景だけ作る

作りは 26本目（車ありvs車なし）と同じ：いつもの2匹の掛け合い＋グラフ（重りが落ちて棒がのびる）＋スロット・ヒビ・お札などの演出。
小型二輪＝125cc以下のバイク（原付二種・小型限定普通二輪免許）として計算。
数字はざっくりの目安（2026年・地方・年8000km・ガソリン170円/L）：
  車（26本目と同じ）：ローン54万・自動車税3万・重量税と自賠責2万・任意保険7万・車検5万・ガソリン8万・駐車場7万・メンテ3万 → 年 約89万
  125cc：車体35万を5年で割って7万／軽自動車税（90cc超125cc以下）年2,400円／重量税なし（250cc以下）／自賠責 1年 約7,000円／
    任意保険 年 約3万（ファミリーバイク特約なら年1〜2万）／車検なし（250cc以下）／ガソリン 160L×170円 約2.7万（燃費50km/L）／
    バイク駐輪場 月2,000円 年2.4万／オイル・タイヤ 年1.5万 → 年 約17.6万（グラフは18万）
  10年：車 445＋175＝620万／バイク 約176万（2台目を買っても約210万）
  125ccの注意：高速道路・自動車専用道路は走れない、2段階右折はいらない（原付一種とちがう）、2人乗りは免許1年以上で可。
  免許：小型限定普通二輪（AT）で教習所 約10万円前後。2025年4月から、出力をおさえた125cc（新基準原付）は原付免許でも乗れる
原稿のルール：実在の人・会社は出さない。今日の一言・単語の途中で改行しない・最後はチャンネル登録・過去の動画にはふれない
"""
import os
import sys

import cuts_04_leak as L
import cuts_26_kuruma as K
import render as R
import wide_bars as B

R.TEMPO = getattr(R, "TEMPO", 1.0) * 0.98
HERE = L.HERE
L.PT = os.path.join(HERE, "parts", "34_bike")
pt, cat, chap, fx, CONAN, POON = L.pt, L.cat, L.chap, K.fx, K.CONAN, K.POON
PURPLE, COCOA, MIRAI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.NORA
bg, nn, ss, boom, qq, g = K.bg, K.nn, K.ss, K.boom, K.qq, K.g
STREET, MONEY, GAS, PARK, SHOP, ROAD, CITY, STATION, BOARD = (K.STREET, K.MONEY, K.GAS, K.PARK, K.SHOP, K.ROAD, K.CITY,
                                                              K.STATION, K.BOARD)
# 背景：バイクの背景が届いたら backgrounds/34_bike に同じ名前で置けば差しかわる（届くまでは車の動画の背景）
L.BGS.insert(0, os.path.join(HERE, "backgrounds", "34_bike"))
BSHOP, BPARK, RAIN = "bg34_bike_shop", "bg34_bike_parking", "bg34_rainy_road"
K.STANDIN.update({BSHOP: K.DEALER, BPARK: K.PARK, RAIN: K.ROAD})
_bbg = B._bg


def _chart_bg(n):   # グラフの背景も、届くまでは代わりの背景
    try:
        return _bbg(n)
    except FileNotFoundError:
        return _chart_bg(K.STANDIN[n])


B._bg = _chart_bg

# ---- グラフ ----
CAR = K.CAR
BIKE = [("車体代（5年で割る）", 7, "blue"), ("軽自動車税", 0.24, "purple"), ("自賠責", 0.7, "navy"), ("任意保険", 3, "orange"),
        ("ガソリン", 2.7, "gold"), ("駐輪場", 2.4, "teal"), ("オイル・タイヤ", 1.5, "pink")]
VS = [("車", "red"), ("125ccバイク", "blue")]
HEAD = "1年でかかるお金（地方・年8000kmの目安）"


def both(names_car, names_bike, t0=0.5, gap=0.9, have_car=(), have_bike=()):
    st = [(-1, 0, n, v, c) for n, v, c in CAR if n in have_car] + [(-1, 1, n, v, c) for n, v, c in BIKE if n in have_bike]
    k = 0
    for n, v, c in CAR:
        if n in names_car:
            st.append((t0 + gap * k, 0, n, v, c))
            k += 1
    for n, v, c in BIKE:
        if n in names_bike:
            st.append((t0 + gap * k, 1, n, v, c))
            k += 1
    return st


ALLC, ALLB = [n for n, _, _ in CAR], [n for n, _, _ in BIKE]
K.CHARTS.update({
    "b0_preview": B.Chart(VS, [(0.3, 0, *CAR[0])] + [(0.9 + 0.2 * k, 0, n, v, c) for k, (n, v, c) in enumerate(CAR[1:])]
                          + [(2.8 + 0.3 * k, 1, n, v, c) for k, (n, v, c) in enumerate(BIKE)], 95, bg=STREET, head=HEAD, highlight=1),
    "b1_body": B.Chart(VS, both(["車のローン"], ["車体代（5年で割る）"]), 95, bg=BSHOP, head=HEAD),
    "b2_tax": B.Chart(VS, both(["自動車税", "重量税・自賠責", "車検"], ["軽自動車税", "自賠責"], have_car=["車のローン"],
                              have_bike=["車体代（5年で割る）"]), 95, bg=PARK, head=HEAD),
    "b3_ins": B.Chart(VS, both(["任意保険"], ["任意保険"], have_car=["車のローン", "自動車税", "重量税・自賠責", "車検"],
                              have_bike=["車体代（5年で割る）", "軽自動車税", "自賠責"]), 95, bg=SHOP, head=HEAD),
    "b4_run": B.Chart(VS, both(["ガソリン", "駐車場", "タイヤ・オイル"], ["ガソリン", "駐輪場", "オイル・タイヤ"],
                              have_car=["車のローン", "自動車税", "重量税・自賠責", "車検", "任意保険"],
                              have_bike=["車体代（5年で割る）", "軽自動車税", "自賠責", "任意保険"]), 95, bg=GAS, head=HEAD,
                      result_at=6.0, highlight=1),
    "b5_gas": B.Chart([("車（16km/L）", "red"), ("125cc（50km/L）", "blue")], [(0.4, 0, "", 8.5, "red"), (1.4, 1, "", 2.7, "blue")], 10,
                      bg=GAS, head="1年のガソリン代（年8000km・170円/L）", total_fmt="年{v}万", highlight=1),
    "b6_tax": B.Chart([("車", "red"), ("125cc", "blue")], [(0.4, 0, "自動車税", 30500, "purple"), (1.4, 1, "軽自動車税", 2400, "blue")],
                      34000, bg=BOARD, head="毎年の税金", total_fmt="{v}円", highlight=1),
    "b7_10y": B.Chart(VS, [(0.4, 0, "1〜5年目\n（ローンあり）", 445, "red"), (1.5, 0, "6〜10年目", 175, "coral"),
                           (2.6, 1, "10年分", 176, "blue")], 650, bg=MONEY, head="10年でかかるお金の合計", total_fmt="{v}万",
                      result_at=3.6, highlight=1),
})
K.DROP_SE.update({"b0_preview": {1: "pafu"}, "b1_body": {1: "pafu"}, "b2_tax": {1: "pafu"}, "b3_ins": {1: "pafu"}, "b4_run": {1: "pafu"},
                  "b5_gas": {1: "pafu"}, "b6_tax": {1: "pafu"}, "b7_10y": {1: "pafu"}})   # バイクの列は気の抜けた軽い音
K.STEP_SE.update({"b0_preview": ["explosion_chudoon"] + K.GAME_STEP[:6] + ["game_mario_1up"],
                  "b2_tax": K.GAME_STEP[6:9], "b4_run": [K.GAME_STEP[3], K.GAME_STEP[9], K.GAME_STEP[0]]})


# 11/1 ユーザー指定：つかみのグラフの右（バイク）は、気の抜けたゲームの音を1つずつちがう音で積み、いちばん上（最後）だけパフ
K.DROP_SE["b0_preview"] = {1: ["game_dq_miss", "game_smash_zannen", "game_yoshi_detteiu_so_what_bored", "game_touhou_pichuun_miss_defeat",
                               "game_rockman_death_tiun_fail_game_over", "boing_fail", "pafu"]}


def card(c, sub, **kw):
    return L.dia(c, sub, BOARD, right=("@calm", "博識な猫"), dur=kw.pop("dur", 4.4), se=kw.pop("se", "card_flip"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(bg=bg(STREET), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in (
                ("drive_driving_cat", 220, 600), ("ride_kitten_bike", 640, 560), ("dance_three_kittens", 1000, 520),
                ("drive_monkey_golf_cart", 1360, 560), ("dance_happy_banana_cat", 1720, 600))],
             fx=["dim"], layers_top=[pt("e00_notice")], dur=6.0, no_pop=True, notice=True,
             se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- ① つかみ ----
        nn("通勤の足\n車とバイク\nどっちが安い？", STREET, se="question_hatena_maou", bgm={"file": PURPLE, "gain": -4}),
        ss("車は1年で\n約89万円", STREET, se="pi"),
        fx(boom(None, STREET, who="S", se=["explosion_dokaan", {"f": "kaan", "at": 0.9}]), slot=("125ccなら 年 約", 18, "万円")),
        boom("18万!?\n車の5分の1!?", STREET, se=[CONAN]),
        g("b0_preview", "ぜんぶ積み上げると\nこうなる", dur=5.6),
        fx(nn("え……\nこんなにちがうの？", MONEY, se=POON), "mono"),
        dict(bg=bg(STREET), card=pt("e01_title"), dur=4.0, se="jan",
             cats=[{"a": "drive_driving_cat", "x": 300, "h": 440, "bottom": 1050, "float": True},
                   {"a": "ride_kitten_bike", "x": 1640, "h": 400, "bottom": 1050, "float": True, "mute": True}]),
        card("e02_premise", "地方に住む会社員・年8000km走る場合", dur=5.2),
        # ---- ② 買うお金 ----
        chap("① 買うお金", se="quiz_question_01", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        ss("車は新車250万\n5年ローンで\n年54万", K.DEALER, se="pi"),
        nn("バイクは？", BSHOP, se="question_hatena_maou"),
        ss("125ccの新車は\n30万〜40万くらい", BSHOP, se="pikon"),
        g("b1_body", "5年で割ると\n年7万", dur=3.6),
        boom("スタートから\n47万の差!?", BSHOP, se=["explosion_chudoon"]),
        # ---- ③ 税金・車検 ----
        chap("② 税金と車検", se="doon_heavy", bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        ss("125ccの税金は\n軽自動車税\n年2400円", PARK, se="pi"),
        g("b6_tax", "車の自動車税は\n約3万円", dur=3.8),
        nn("12分の1!?", PARK, red=True, se=["explosion_dokaan"]),
        ss("しかも250cc以下は\n車検がない", PARK, se="pikon"),
        ss("重量税もかからない\n自賠責は年7000円くらい", PARK, se="kon"),
        g("b2_tax", "税金と車検だけで\nこの差", dur=4.6),
        fx(boom("車検代10万が\nゼロ!?", SHOP, se=["explosion_chudoon", {"f": "glass_break_01", "gain": -4}]), "crack"),
        # ---- ④ 保険 ----
        chap("③ 保険", se="whoosh_shu"),
        ss("任意保険は\n年3万くらい", SHOP, se="pi"),
        ss("車を持っているなら\nファミリーバイク特約で\nもっと安くなる", SHOP, se="pinpon_notice"),
        nn("車の保険に\nおまけで\nつけられるの？", SHOP, se="question_hatena_maou"),
        ss("年1万〜2万くらいで\nつけられることが多い", SHOP, se="kon"),
        g("b3_ins", "保険も\n車の半分以下", dur=3.6),
        # ---- ⑤ 走るお金 ----
        chap("④ 走るお金", se="whoosh_shu", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        ss("125ccの燃費は\n1リットルで\n50km前後", GAS, se="pi"),
        g("b5_gas", "ガソリン代は\n3分の1以下", dur=3.6),
        nn("満タンにしても\n1000円ちょっと!?", GAS, red=True, se=["explosion_dokaan"]),
        ss("駐輪場も\n月2000円くらい", BPARK, se="kon"),
        ss("オイルもタイヤも\n安くて小さい", BPARK, se="pi"),
        g("b4_run", "ぜんぶ積むと……", dur=6.4),
        fx(boom("車89万\nバイク18万!!", MONEY, se=["explosion_dokaan"]), "money"),
        qq(MONEY, "tv_professional_poon_remix_b"),   # 11/1 ユーザー指定：ここはポーン連打
        fx(nn("え……\n年71万も\nちがうの？", MONEY, se="tv_professional_poon_remix_a"), "swirl"),
        g("b7_10y", "10年で\nくらべると……", dur=5.4),
        fx(boom("10年で\n440万の差!?", MONEY, se=["explosion_chudoon"]), "money"),
        # ---- ⑥ でも弱点も ----
        chap("⑤ バイクの弱点", se="doon_heavy", bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        ss("雨の日は\nカッパを着る", RAIN, se="pi"),
        nn("ずぶぬれで\n会社に着く……", RAIN, se="deflate_hyororo"),
        ss("冬はとにかく寒い\n手袋とネックウォーマーは必須", RAIN, se="freeze_kochiin"),
        ss("125ccは\n高速道路を\n走れない", ROAD, se="pc_warning"),
        boom("高速に\n乗れない!?", ROAD, se=["explosion_dokaan"]),
        ss("荷物も\nたくさんは積めない", ROAD, se="kon"),
        ss("2人乗りは\n免許を取って\n1年たってから", ROAD, se="pinpon_notice"),
        ss("事故のときは\n体を守るものがない\n安全運転がいちばん", ROAD, se="kon"),
        # ---- ⑦ 免許 ----
        chap("⑥ 免許は？", se="whoosh_shu"),
        ss("125ccは\n小型限定の\n二輪免許", CITY, se="pi"),
        ss("AT限定なら\n教習所で\n10万円前後", CITY, se="kon"),
        ss("2025年からは\n出力をおさえた125ccなら\n原付免許でも乗れる", CITY, se="pinpon_notice"),
        nn("意外と\nハードル低い!?", CITY, red=True, se=["explosion_dokaan"]),
        # ---- ⑧ どっちがいい？ ----
        chap("⑦ どっちがいい？", se="quiz_question_01", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        ss("ひとりで\n近くに通勤するなら\nバイクが強い", STREET, se="pi"),
        ss("家族で出かける\n雨の日も遠出も\nなら車", STREET, se="pi"),
        nn("両方持つのは？", STREET, se="question_hatena_maou"),
        ss("ふだんはバイク\n家族の日は\nカーシェアという手も", STATION, se="pikon"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy"),
        card("e07_points", "1年の合計で考えてみよう", dur=5.6),
        nn("安さなら\nバイクの圧勝", STREET, se="kon"),
        ss("でも雨と寒さと\n荷物も考えて\nえらぼう", STREET, se="kon"),
        dict(bg=bg(STREET), card=pt("e10_ending"), dur=3.6, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    return K.hype(L.apply_fx(L.allocate(cuts_all(), max_use=7, gap=1)))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "34_bike_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if sys.argv[1:] == ["--charts"]:
        for k in ("b0_preview", "b1_body", "b2_tax", "b3_ins", "b4_run", "b5_gas", "b6_tax", "b7_10y"):
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
