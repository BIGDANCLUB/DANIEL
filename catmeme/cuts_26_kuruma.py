"""26_kuruma（車ありvs車なし 1年でかかるお金）のカット割り（10/28 ユーザー指定）。3〜4分。作りは 25本目（和牛）と同じ。

python3 catmeme/cuts_26_kuruma.py          → out/26_kuruma_full.mp4
python3 catmeme/cuts_26_kuruma.py --charts → グラフの動く背景だけ作る（out/wide_bars/）
python3 catmeme/cuts_26_kuruma.py --audio  → 音だけ作り直す

10/28 ユーザー指定：
- ローン・保険・ガソリン・駐車場などを比べる。長い内容を濃く圧縮して3〜4分
- 1場面に猫をたくさん。動きの多い素材を多めに。エフェクトは和牛と同じく多め
- ショートのようなグラフでの説明を多く（wide_bars.py：重りが落ちて衝撃波・棒がのびる）
- 車なしの説明は少しでよい。車があるとかかるお金に重点

数字はざっくりの目安（地方都市・コンパクトカー新車250万円・5年ローン金利3%・年8000km・燃費16km/L・ガソリン160円/L・駐車場 月6000円）：
  車のローン 年54万（総額 約270万）／自動車税 30,500円（1.0〜1.5L・2019年10月以降の新車）／重量税 2年16,400円（1t以下）・
  自賠責 2年17,650円 → 年 約1.7万／任意保険 年 約7万／車検 2年 約10万 → 年5万／ガソリン 500L×160円 年8万／駐車場 年7万／
  タイヤ・オイルなど 年3万 → 合計 年 約89万（月 約7.4万）。ローンが終わった6年目からは 年 約35万
  車なし：電車・バス 年9万＋タクシー・カーシェア 年6万 → 年15万
  軽自動車（新車160万・5年ローン）：ローン35万・軽自動車税10,800円・重量税＋自賠責 約1.2万・保険6万・車検4万・ガソリン6.4万
  （燃費20）・駐車場7万・メンテ2.5万 → 年 約63万
  東京23区の月極駐車場は 月3万以上も → 年 約40万
原稿のルール：実在の人・会社は出さない。今日の一言・単語の途中で改行しない・最後はチャンネル登録・過去の動画にはふれない
"""
import os
import sys

import cuts_04_leak as L
import render as R
import wide_bars as B

R.TEMPO = getattr(R, "TEMPO", 1.0) * 0.84   # 掛け合いを2匹にしたら短くなったので、3分すぎになるよう少しゆっくり（10/28）
HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("26_kuruma", "14_japan", "13_yard", "16_tenchim", "04_leak", "02_october",
                                                         "01_todai", "25_wagyu", "18_semicon")]
L.PT = os.path.join(HERE, "parts", "26_kuruma")
pt, cat, chap = L.pt, L.cat, L.chap
PURPLE, COCOA, MIRAI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.NORA

# 背景（ChatGPT で作る背景が届いたら backgrounds/26_kuruma に同じ名前で置けば差しかわる。指示文 scripts/26_kuruma_bg_prompts.md）
STREET, CITY, GARAGE, MONEY, TOKYO, FIELD, BOARD, OFFICE, STATION = (
    "bg48_clean_street", "bg40_hiace_white_city", "bg39_hiace_black_garage", "bg87_refund_money", "bg57_tokyo_skyline",
    "bg63_hokkaido_field", "bg03_blackboard", "bg25_office_desk", "bg54_station_crowd_map")
DEALER, GAS, PARK, SHOP, ROAD, TPARK = ("bg26_car_dealer", "bg26_gas_station", "bg26_parking_lot", "bg26_car_inspection",
                                        "bg26_rural_road", "bg26_tokyo_parking")
STANDIN = {DEALER: CITY, GAS: STREET, PARK: STREET, SHOP: GARAGE, ROAD: FIELD, TPARK: TOKYO}
_bg = L.bg


def bg(n):
    try:
        return _bg(n)
    except FileNotFoundError:
        return _bg(STANDIN[n])


L.bg = bg

# ---- グラフ（ショートと同じ作りの動く背景） ----
CAR = [("車のローン", 54, "red"), ("自動車税", 3, "purple"), ("重量税・自賠責", 2, "navy"), ("任意保険", 7, "orange"),
       ("車検", 5, "coral"), ("ガソリン", 8, "gold"), ("駐車場", 7, "teal"), ("タイヤ・オイル", 3, "pink")]
NOCAR = [("電車・バス", 9, "blue"), ("タクシー・カーシェア", 6, "green")]
VS = [("車あり", "red"), ("車なし", "blue")]
HEAD = "1年でかかるお金（地方・コンパクトカーの目安）"


def _have(names):
    return [(-1, 0, n, v, c) for n, v, c in CAR if n in names]


def _drop(names, t0=0.5, gap=1.1):
    return [(t0 + gap * k, 0, n, v, c) for k, (n, v, c) in enumerate(x for x in CAR if x[0] in names)]


CHARTS = {
    # つかみ：全部まとめてドドドッと落ちる
    # 10/29 ユーザー指定：最初のローンだけドーン、あとは速く積む（いろいろな音・最後は1UP）
    "k0_preview": B.Chart(VS, [(0.3, 0, *CAR[0])] + [(1.0 + 0.22 * k, 0, n, v, c) for k, (n, v, c) in enumerate(CAR[1:])]
                          + [(3.0 + 0.4 * k, 1, n, v, c) for k, (n, v, c) in enumerate(NOCAR)], 95, bg=STREET, head=HEAD,
                          highlight=0),
    "k1_loan": B.Chart(VS, _drop(["車のローン"]), 95, bg=DEALER, head=HEAD),
    "k2_tax": B.Chart(VS, _have(["車のローン"]) + _drop(["自動車税", "重量税・自賠責"]), 95, bg=PARK, head=HEAD),
    "k3_ins": B.Chart(VS, _have(["車のローン", "自動車税", "重量税・自賠責"]) + _drop(["任意保険", "車検"]), 95, bg=SHOP, head=HEAD),
    "k4_run": B.Chart(VS, _have(["車のローン", "自動車税", "重量税・自賠責", "任意保険", "車検"])
                      + _drop(["ガソリン", "駐車場", "タイヤ・オイル"]), 95, bg=STREET, head=HEAD, highlight=0),
    "k5_vs": B.Chart(VS, _have([n for n, _, _ in CAR]) + [(0.5 + 1.0 * k, 1, n, v, c) for k, (n, v, c) in enumerate(NOCAR)],
                     95, bg=STATION, head=HEAD, result_at=2.8, highlight=0),
    "d1_tax3": B.Chart([("自動車税", "purple"), ("重量税", "navy"), ("自賠責保険", "teal")],
                       [(0.4, 0, "毎年", 30500, "purple"), (1.3, 1, "2年で16,400円", 8200, "navy"), (2.2, 2, "2年で17,650円", 8825, "teal")],
                       34000, bg=BOARD, head="乗らなくても取られるお金（1年あたり）", total_fmt="{v}円"),
    "d2_gas": B.Chart([("年5000km", "gold"), ("年8000km", "orange"), ("年12000km", "red")],
                      [(0.4, 0, "", 5, "gold"), (1.2, 1, "", 8, "orange"), (2.0, 2, "", 12, "red")], 13, bg=GAS,
                      head="1年のガソリン代（燃費16km/L・160円/L）", total_fmt="年{v}万"),
    "d3_park": B.Chart([("地方", "teal"), ("東京23区", "red")], [(0.4, 0, "月6000円", 7, "teal"), (1.4, 1, "月3万〜", 40, "red")],
                       45, bg=TPARK, head="1年の駐車場代（月極の目安）", total_fmt="年{v}万", highlight=1),
    "d4_10y": B.Chart(VS, [(0.4, 0, "1〜5年目\n（ローンあり）", 445, "red"), (1.5, 0, "6〜10年目", 175, "coral"),
                           (2.6, 1, "10年分", 150, "blue")], 650, bg=MONEY, head="10年でかかるお金の合計", total_fmt="{v}万",
                      result_at=3.6, highlight=0),
    "d5_kei": B.Chart([("コンパクトカー", "red"), ("軽自動車", "orange"), ("車なし", "blue")],
                      [(-1, 0, "", 89, "red"), (0.5, 1, "", 63, "orange"), (-1, 2, "", 15, "blue")], 95, bg=ROAD,
                      head="1年でかかるお金（新車・5年ローンの目安）"),
}


def chart_path(name):
    return B.make(name, CHARTS[name])


# 項目が落ちるときの音（列ごと）。車なしは気の抜ける軽い音、駐車場の東京は1UP（10/28 ユーザー指定）
STEP_SE = {"k0_preview": ["explosion_chudoon", "pikon", "kon", "pa", "tsukkomi_bashi", "boing_02", "puni", "game_mario_1up"]}   # 車ありの列：1つ目から順に
DROP_SE = {"k0_preview": {1: "pafu"}, "k5_vs": {1: "pafu"}, "d4_10y": {1: "pafu"}, "d3_park": {1: "game_mario_1up"},
           "d5_kei": {1: "game_zelda_item_get"}}   # 軽自動車はゴマダレー


def g(name, say, who="S", still=False, dur=None, red=False, se=None, **kw):
    """グラフの場面：グラフの動く背景＋左はしにニュース猫・右はしに博識な猫（しゃべる方だけ鳴らす）。字幕は上。
    still=True はグラフが出来上がった絵のまま（同じグラフの2つ目以降の場面）。
    「車なし」の列が0のあいだは、その列の上で小さな猫が踊る（10/28 ユーザー指定）。"""
    ch = CHARTS[name]
    ss = ch.still_from() + 0.5 if still else 0.0
    cats = [cat("@react", "ニュース猫", 150, h=560, bottom=1080, label_size=50, mute=who != "N"),
            cat("@calm", "博識な猫", 1775, h=560, bottom=1080, label_size=50, mute=who != "S")]
    if ch.cols == VS and not any(st[1] == 1 for st in ch.steps):
        cats.append({"a": "@papa", "x": ch.cx[1], "h": 190, "bottom": B.BASE_Y - 4, "mute": True, "full": False, "float": True})
    lst = [] if not se else ([se] if isinstance(se, (str, dict)) else list(se))
    if not still:
        car = 0
        for t0, col, _n, _v, _c in ch.steps:
            if t0 >= 0:
                f = DROP_SE.get(name, {}).get(col, "explosion_chudoon")
                if name in STEP_SE and col == 0:   # 項目ごとに音を変える
                    f = STEP_SE[name][min(car, len(STEP_SE[name]) - 1)]
                    car += 1
                lst.append({"f": f, "at": t0 + 0.3, "gain": -6 if f == "explosion_chudoon" else -3})
        if ch.result_at is not None:
            lst.append({"f": "game_mario_1up", "at": ch.result_at, "gain": -4})
        need = ch.still_from() - 0.6
        dur = max(dur or 0, need / R.TEMPO)
    return dict(bg=chart_path(name), bg_ss=ss, cats=cats, say=say, text_box=(60, 6, 1860, 226), say_size=104,
                say_style="red" if red else None, keep_overlap=True, chart=True, dur=dur, se=lst, fixed=not still, **kw)


# ---- 掛け合い：ニュース猫（左）と博識な猫（右）の2匹だけ、大きく（10/28 ユーザー指定：2匹の会話なので素材は2つ・その代わり大きめ） ----
def m(say, b, who="S", red=False, **kw):
    """who="N"：ニュース猫（左）がしゃべる。who="S"：博識な猫（右）がしゃべる。しゃべる方だけ鳴らす。"""
    cats = [cat("@react", "ニュース猫", 470, h=780, bottom=1075, label_size=56, mute=who != "N"),
            cat("@calm", "博識な猫", 1450, h=780, bottom=1075, label_size=56, mute=who != "S")]
    out = dict(bg=bg(b), cats=cats, say=say, text_top=True, keep_overlap=True, **kw)
    if red:
        out.update(say_style="red", fx=["lines", "shake"])
    return out


def nn(say, b=STREET, **kw):
    return m(say, b, who="N", **kw)


def ss(say, b=STREET, **kw):
    return m(say, b, who="S", **kw)


def boom(say, b=STREET, who="N", **kw):
    """驚きのアップ：まん中に大きく1匹。赤い文字・集中線・揺れ。"""
    role = ("@react", "ニュース猫") if who == "N" else ("@calm", "博識な猫")
    se = kw.pop("se", ["explosion_chudoon"])
    return dict(bg=bg(b), cats=[cat(role[0], role[1], 960, h=800, bottom=1075, float=True)], say=say, text_top=True,
                say_style="red", fx=["shake"], keep_overlap=True, se=se, **kw)


CONAN = "anime_conan_hirameki_idea_realize_truth"
POON = "tv_professional_poon"


def qq(b, remix, who="N"):
    """コナンの連打の場面：字幕のかわりに、いろいろな色とエフェクトの「？？？？？？」。猫はまん中に大きく（声は消す）。"""
    role = ("@react", "ニュース猫") if who == "N" else ("@calm", "博識な猫")
    return dict(bg=bg(b), cats=[cat(role[0], role[1], 960, h=760, bottom=1075, float=True, mute=True)], qmarks=6,
                text_top=True, fx=["lines", "flash", "ring"], keep_overlap=True, no_pop=True, dur=2.0, se=[remix])


def fx(c, *names, **extra):
    """場面にエフェクトを足す（10/29 採用：crack ヒビ・mono 一瞬白黒・money お札・swirl ぐるぐる。どれも多用しない）。"""
    c["fx"] = list(c.get("fx", [])) + list(names)
    c.update(extra)
    return c


def card(c, sub, b=BOARD, **kw):
    return L.dia(c, sub, b, right=("@calm", "博識な猫"), dur=kw.pop("dur", 4.4), se=kw.pop("se", "card_flip"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き（動く猫の上を半分暗くして・ピンポンパンポーン） ----
        dict(bg=bg(STREET), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in (
                ("drive_driving_cat", 220, 600), ("dance_three_kittens", 640, 520), ("ride_kitten_bike", 1000, 560),
                ("drive_monkey_golf_cart", 1360, 560), ("dance_tabby_standing_cat", 1720, 600))],
             fx=["dim"], layers_top=[pt("e00_notice")], dur=6.0, no_pop=True, notice=True,
             se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- ① つかみ ----
        nn("車って\n1年でいくら\nかかると思う？", STREET, se="question_hatena_maou", bgm={"file": PURPLE, "gain": -4}),
        ss("ガソリン代くらい\nでしょ？\n月1万とか", STREET, se="pikon"),
        fx(boom(None, STREET, who="S", se=["explosion_dokaan", {"f": "kaan", "at": 0.9}]), slot=("年 約", 89, "万円")),   # 金額のスロット（10/29）
        boom("年89万!?\nガソリン代だけじゃ\nないの!?", STREET, se=[CONAN]),   # 早めにコナン（10/28 ユーザー指定）
        g("k0_preview", "ローン・税金・保険・ガソリン……\n積み上げるとこうなる", dur=5.6),
        boom("月になおすと\n7万4000円！？", MONEY, se=["shock_piano"]),
        qq(MONEY, "anime_conan_hirameki_remix_b"),   # コナンの連打＋色とりどりの「？？？？？？」（10/28 ユーザー指定）
        fx(nn("え……\n家賃もう1個\n払ってるじゃん", MONEY, se=POON), "mono"),   # 「え…」の場面はポーン（1回目はふつう・10/28）
        dict(bg=bg(STREET), card=pt("e01_title"), dur=4.0, se="jan",
             cats=[{"a": "drive_driving_cat", "x": 300, "h": 440, "bottom": 1050, "float": True},
                   {"a": "dance_three_kittens", "x": 1640, "h": 400, "bottom": 1050, "float": True, "mute": True}]),
        card("e02_premise", "地方に住む会社員・コンパクトカー新車250万円の場合", dur=5.2),
        # ---- ② 車のローン ----
        chap("① 車のローン", se="quiz_question_01", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        ss("250万の車を\n5年ローンで買う", DEALER, se="pi"),
        nn("頭金なしで\n月4万5000円か\nいけるいける", DEALER, se="pikon"),
        ss("金利3%だと\n払う合計は\n約270万", DEALER, se="kon"),
        boom("利息だけで\n20万！？", DEALER, se=["explosion_chudoon"]),
        g("k1_loan", "1年あたり\n54万円", dur=3.4),
        g("k1_loan", "いちばん大きいのが\nこのローン", who="N", still=True),
        nn("でもローンが\n終われば\nタダでしょ？", DEALER, se="question_mark_pop_confused_huh"),
        ss("ここからが\n本番!?", DEALER, se="anime_conan_hirameki_remix_c", red=True),   # !? とコナン（2回目からは連打・10/28）
        # ---- ③ 税金 ----
        chap("② 乗らなくても\n取られるお金", se="doon_heavy", bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        ss("車は持ってる\nだけで\n税金がかかる", PARK, se="pi"),
        g("d1_tax3", "自動車税・重量税・自賠責\nこの3つは必ず払う", dur=4.4),
        nn("自動車税だけで\n3万円！？", PARK, red=True, se=["explosion_dokaan"]),
        ss("毎年5月に\n通知が来る", PARK, se="pinpon_notice"),
        nn("え……\n5月って連休で\nお金ないのに", PARK, se="tv_professional_poon_remix_a"),   # 2回目からはポーン連打
        g("k2_tax", "税金と自賠責で\n年 約5万", dur=3.6),
        # ---- ④ 保険と車検 ----
        chap("③ 保険と車検", se="whoosh_shu"),
        ss("自賠責だけじゃ\n足りないから\n任意保険にも入る", SHOP, se="pi"),
        nn("任意なら\n入らなくていい？", SHOP, se="question_hatena_maou"),
        boom("事故で\n何千万も払う\nことになるよ", SHOP, who="S", se=["shock_piano"]),
        nn("入ります\n入らせてください", SHOP, se="pikon"),
        ss("保険は\n年 約7万\n若いともっと高い", SHOP, se="kon"),
        ss("そして2年ごとに\n車検", SHOP, se="pi"),
        nn("車検って\nいくらするの？", SHOP, se="question_hatena_maou"),
        ss("整備も入れて\n約10万\n1年あたり5万", SHOP, se="kon"),
        g("k3_ins", "保険と車検で\nさらに12万", dur=3.8),
        fx(boom("まだ1メートルも\n走ってないのに！？", GARAGE, se=["explosion_chudoon", {"f": "glass_break_01", "gain": -4}]), "crack"),
        # ---- ⑤ 走るお金（ガソリン・駐車場・メンテ） ----
        chap("④ 走るお金", se="whoosh_shu", bgm={"file": PURPLE, "gain": -4, "fade": 0.6}),
        ss("年8000km走ると\nガソリンは\n約500リットル", GAS, se="pi"),
        nn("1リットル160円で\n……8万円！", GAS, red=True, se=["explosion_dokaan"]),
        g("d2_gas", "走るほど\nガソリン代はふえる", dur=3.8),
        nn("遠くに通勤してたら\nもっとかかるのか", GAS, se="kon"),
        ss("家の駐車場がないと\n月極を借りる", PARK, se="pi"),
        nn("地方なら\n月6000円くらい？", PARK, se="pikon"),
        g("d3_park", "東京だと\n月3万以上も", dur=3.4),
        boom("駐車場だけで\n年40万！？", TPARK, se=["explosion_chudoon"]),
        ss("タイヤ交換\nオイル交換も\n年3万くらい", GARAGE, se="kon"),
        g("k4_run", "ぜんぶ積むと……", dur=4.6),
        fx(boom("1年で\n89万円！！", MONEY, se=["explosion_dokaan"]), "money"),
        nn("毎月7万4000円が\n車に消えてる……", MONEY, se="deflate_hyororo"),
        # ---- ⑥ 車なしとくらべる ----
        chap("⑤ 車なしだと？", se="quiz_question_01", bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        dict(bg=bg(STATION), split=("車あり", "車なし"), say="車なしは 電車・バス\nときどきタクシーやカーシェア", text_box=(140, 30, 1780, 400),
             cats=[{"a": "drive_driving_cat", "x": 480, "h": 560, "bottom": 1075, "mute": True, "float": True},
                   cat("@calm", "博識な猫", 1440, h=560, bottom=1075, label_size=52)], keep_overlap=True, se="pi"),   # 画面分割（10/29）
        g("k5_vs", "車なしは\n年 約15万", dur=4.6),
        fx(boom("差は\n年74万円！？", STATION, se=["shock_piano", {"f": "glass_break_01", "gain": -4}]), "crack"),
        g("d4_10y", "10年で\nくらべると……", dur=5.4),
        fx(nn("え……ローンが終わっても\n年35万は\nかかり続けるの？", MONEY, se="tv_professional_poon_remix_b"), "swirl"),
        fx(boom("10年で\n470万の差！？", MONEY, se=["explosion_chudoon"]), "money"),
        fx(nn("え……\n新車もう1台\n買えるじゃん", MONEY, se=POON), "mono"),   # 連打は1本で2回まで（10/29）なのでふつうのポーン
        # ---- ⑦ 安くするなら ----
        chap("⑥ 安くするなら", se="whoosh_shu"),
        nn("でも地方は\n車がないと\n生活できない", ROAD, se="kon"),
        ss("それなら\n軽自動車という手も", ROAD, se="pikon"),
        g("d5_kei", "軽なら\n年 約63万", dur=3.4),
        ss("軽自動車税は\n年1万800円\n燃費もいい", ROAD, se="pi"),
        ss("保険の見直し\n中古車を選ぶ\nこれも効く", ROAD, se="pi"),
        nn("たまにしか\n乗らない人は？", CITY, se="question_hatena_maou"),
        ss("カーシェアや\nレンタカーのほうが\n安いことも", CITY, se="pinpon_notice"),   # ポーンは「え…」の場面だけ（10/28 ルール）
        # ---- ⑧ まとめ ----
        chap("まとめ", se="doon_heavy", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        card("e07_points", "持っているだけでかかるお金を知っておこう", dur=5.6),
        nn("車は便利だけど\nお金も\nしっかりかかる", STREET, se="kon"),
        ss("必要かどうか\n1年の合計で\n考えてみよう", STREET, se="kon"),
        dict(bg=bg(STREET), card=pt("e10_ending"), dur=3.6, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


FLASHY = ("explosion", "shock", "dokaan", "desk_slam", "siren", "jan", "power_up", "doon_heavy", "glass_break")
POP_SE = ("pikon", "spo", "puni", "kote", "pa", "papa", "peta", "suupo", "button_13", "cursor_move_01")   # 頭の小さな音
BIG_SE = ("voice_uuwaa", "boing_02", "tsukkomi_bashi", "punch", "frying_pan_kaan", "kaan", "hit_dogo_maou", "shock_piano")


def hype(cuts):
    """和牛と同じ：派手な演出と効果音を多めに（キラキラ・紙吹雪はなし）。グラフの場面は見やすさ優先で集中線・寄りはしない。"""
    for i, c in enumerate(cuts):
        if c.get("notice"):
            continue
        fx = list(c.get("fx", []))
        se = c.get("se")
        ses = " ".join((x if isinstance(x, str) else x.get("f", "")) for x in ([se] if isinstance(se, (str, dict)) else (se or [])))
        big = c.get("say_style") == "red" or any(k in ses for k in FLASHY) or c.get("chapter")
        if c.get("chart"):
            fx += ["border"] + (["flash", "ring"] if big else [])
        else:
            fx += ["punch"]   # 10/29 ユーザー指摘「集中線多用しすぎ」：集中線は驚きの場面の3回に1回だけ
            if i % 4 == 1:
                fx.append("border")
            if big:
                fx += ["flash", "shake", "ring", "border"] + (["lines"] if i % 3 == 0 else [])
            else:
                fx.append("zoom")
        c["fx"] = list(dict.fromkeys(f for f in fx if f not in ("spark", "confetti")))
        lst = [] if not se else ([se] if isinstance(se, (str, dict)) else list(se))
        lst.append({"f": POP_SE[i % len(POP_SE)], "gain": -7})
        if big:
            lst.append({"f": BIG_SE[i % len(BIG_SE)], "gain": -4, "at": 0.25})
        if big and i % 3 == 0:
            lst.append({"f": "armor_damage_hit", "gain": -5})
        c["se"] = lst
    return cuts


def cuts_full():
    return hype(L.apply_fx(L.allocate(cuts_all(), max_use=7, gap=1)))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "26_kuruma_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if sys.argv[1:] == ["--charts"]:
        for k in CHARTS:
            print(B.make(k, CHARTS[k], force=True))
        sys.exit()
    cuts = cuts_full()
    if sys.argv[1:] == ["--audio"]:
        R.remux_audio(cuts, out, out.replace(".mp4", "_a.mp4"))
        os.replace(out.replace(".mp4", "_a.mp4"), out)
        sys.exit()
    if sys.argv[1:] == ["--len"]:
        print(len(cuts), round(sum(R.cut_dur(c) for c in cuts), 1))
        sys.exit()
    if len(sys.argv) > 1:
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=out.replace(".mp4", "_preview"))
