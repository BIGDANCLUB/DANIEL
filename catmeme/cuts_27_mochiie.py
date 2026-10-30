"""27_mochiie（持ち家vs賃貸 一生でかかるお金）のカット割り（10/29 ユーザー指定）。3〜4分。作りは 26本目（車）と同じ。

python3 catmeme/cuts_27_mochiie.py          → out/27_mochiie_full.mp4
python3 catmeme/cuts_27_mochiie.py --charts → グラフの動く背景だけ作る（out/wide_bars/）

10/29 ユーザー指定：画面を半分に分けて比べる形（左＝持ち家・右＝賃貸。左右で別の背景・それぞれの猫）
車の動画で決めたルールも使う：
- ショートのようなグラフを多く。積み上がる途中の音はゲーム・アニメの音
- 「!?」の場面はコナン、「え…」の場面はポーン。どちらも1回目はふつう、連打は1本で2回まで
- コナン・ポーンの場面は猫の声とほかの音を入れない。集中線は控えめ。ヒビ・白黒・お札・スロット・ぐるぐるは多用しない

数字はざっくりの目安（30歳の夫婦・郊外の3LDK・2026年）：
  持ち家：4500万円の戸建て。頭金450万＋諸費用300万。ローン4050万・35年・金利1%（変動）→ 月約11.4万・総返済 約4800万
    固定資産税・都市計画税 年約12万 ×35年＝420万／修繕（屋根・外壁・給湯器・水回り）35年で約600万／火災・地震保険 35年で約150万
    → 35年の合計 約6720万。ローン完済後は税金＋修繕で 年約30万
  賃貸：家賃 月13万 ×12×35年＝5460万／更新料（2年ごとに1か月分）約220万／初期費用・引っ越し 約100万 → 35年の合計 約5780万
    65歳以降も家賃と更新料で 年約160万
  90歳まで（60年）：持ち家 6720＋25年×30万＝約7470万／賃貸 5780＋25年×約162万＝約9840万
  金利2%なら月約13.4万
原稿のルール：実在の人・会社は出さない。今日の一言・単語の途中で改行しない・最後はチャンネル登録・過去の動画にはふれない
"""
import os
import sys

import cuts_04_leak as L
import render as R
import wide_bars as B

R.TEMPO = getattr(R, "TEMPO", 1.0) * 1.05   # 左右の字幕と金額を読める速さ（3分すぎ）
HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", d) for d in ("27_mochiie", "26_kuruma", "14_japan", "13_yard", "16_tenchim", "04_leak", "03_kodomo_nisa", "15_vambi",
                                                         "02_october", "01_todai", "25_wagyu")]
L.PT = os.path.join(HERE, "parts", "27_mochiie")
pt, cat, chap = L.pt, L.cat, L.chap
PURPLE, COCOA, MIRAI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.NORA
L.ROLE["持ち家派"] = (220, 110, 20)
L.ROLE["賃貸派"] = (0, 110, 210)

# 背景（ChatGPT で作る背景が届いたら backgrounds/27_mochiie に同じ名前で置けば差しかわる。指示文 scripts/27_mochiie_bg_prompts.md）
HOUSE, APT, LIVING, ROOM, AGENT, ROOF, BOARD, MONEY = (
    "bg27_house_exterior", "bg27_apartment_exterior", "bg27_house_living", "bg27_apartment_room", "bg27_real_estate",
    "bg27_roof_repair", "bg03_blackboard", "bg87_refund_money")
STANDIN = {HOUSE: "bg48_clean_street", APT: "bg57_tokyo_skyline", LIVING: "bg19_kids_room", ROOM: "bg02_room",
           AGENT: "bg78_agency_office", ROOF: "bg26_car_inspection"}
_bg = L.bg


def bg(n):
    try:
        return _bg(n)
    except FileNotFoundError:
        return _bg(STANDIN[n])


L.bg = bg

_bbg = B._bg


def _chart_bg(n):
    """グラフの背景：まだ届いていない背景は仮の背景で。"""
    try:
        return _bbg(n)
    except FileNotFoundError:
        return _bbg(STANDIN[n])


B._bg = _chart_bg


# ---- グラフ（ショートと同じ作りの動く背景）。左＝持ち家（オレンジ）・右＝賃貸（青） ----
VS = [("持ち家", "orange"), ("賃貸", "blue")]
HOUSE_35 = [("頭金・諸費用", 750, "gold"), ("ローン返済", 4800, "orange"), ("固定資産税", 420, "purple"), ("修繕", 600, "coral"),
            ("保険", 150, "pink")]
RENT_35 = [("初期費用・引っ越し", 100, "teal"), ("家賃", 5460, "blue"), ("更新料", 220, "navy")]
HEAD35 = "35年でかかるお金（30歳の夫婦・郊外の3LDKの目安）"
CHARTS = {
    # つかみ：左右とも一気に積む
    "c0_preview": B.Chart(VS, [(0.3 + 0.3 * k, 0, n, v, c) for k, (n, v, c) in enumerate(HOUSE_35)]
                          + [(2.0 + 0.35 * k, 1, n, v, c) for k, (n, v, c) in enumerate(RENT_35)], 7500, bg=HOUSE, head=HEAD35,
                          total_fmt="{v}万"),
    "c1_first": B.Chart(VS, [(0.4, 0, "頭金・諸費用", 750, "gold"), (1.4, 1, "敷金・礼金など", 50, "teal")], 800, bg=AGENT,
                        head="最初にかかるお金", total_fmt="{v}万", highlight=0),
    "c2_month": B.Chart(VS, [(0.4, 0, "ローン", 11.4, "orange"), (1.4, 1, "家賃", 13, "blue")], 15, bg=LIVING,
                        head="毎月はらうお金（金利1%の場合）", total_fmt="月{v}万"),
    "c3_house": B.Chart([("固定資産税", "purple"), ("修繕", "coral"), ("保険", "pink")],
                        [(0.4, 0, "年12万×35年", 420, "purple"), (1.3, 1, "屋根・外壁\n水回り", 600, "coral"), (2.2, 2, "火災・地震", 150, "pink")],
                        650, bg=ROOF, head="持ち家だけにかかるお金（35年）", total_fmt="{v}万"),
    "c4_rent": B.Chart([("更新料", "navy"), ("引っ越し", "teal")],
                       [(0.4, 0, "2年ごとに\n1か月分", 220, "navy"), (1.3, 1, "初期費用", 100, "teal")],
                       650, bg=ROOM, head="賃貸だけにかかるお金（35年）", total_fmt="{v}万"),
    "c5_35y": B.Chart(VS, [(0.3 + 0.5 * k, 0, n, v, c) for k, (n, v, c) in enumerate(HOUSE_35)]
                      + [(3.0 + 0.5 * k, 1, n, v, c) for k, (n, v, c) in enumerate(RENT_35)], 7500, bg=MONEY, head=HEAD35,
                      total_fmt="{v}万", result_at=4.8, highlight=1),
    "c6_90y": B.Chart(VS, [(-1, 0, "35年まで", 6720, "orange"), (-1, 1, "35年まで", 5780, "blue"),
                           (0.5, 0, "老後25年", 750, "gold"), (1.6, 1, "老後25年\nの家賃", 4060, "red")], 10500, bg=MONEY,
                      head="90歳までにかかるお金（60年）", total_fmt="{v}万", result_at=2.9, highlight=0),
}

# 積み上がる途中の音（ゲーム・アニメの音を優先・10/29 ルール）。列ごと
GAME = ["game_coin_get_money_gain_happy", "anime_dbz_punch", "game_mario_jump", "game_dq_attack_enemy", "game_aceattorney_ping",
        "anime_shinchan_genkotsu", "game_smash_homerun_bat", "game_ff_cursor", "anime_dbz_teleport", "game_dq_miss"]
STEP_SE = {"c0_preview": {0: ["explosion_chudoon"] + GAME[:4], 1: GAME[5:7] + ["game_mario_1up"]},
           "c1_first": {0: ["explosion_chudoon"], 1: ["pafu"]},
           "c2_month": {0: [GAME[2]], 1: [GAME[1]]},
           "c3_house": {0: [GAME[3]], 1: [GAME[6]], 2: [GAME[4]]},
           "c4_rent": {0: [GAME[0]], 1: ["pafu"]},
           "c5_35y": {0: GAME[:5], 1: GAME[5:8]},
           "c6_90y": {0: ["pafu"], 1: ["explosion_chudoon"]}}


def chart_path(name):
    return B.make(name, CHARTS[name])


def g(name, say, who="R", still=False, dur=None, red=False, se=None, **kw):
    """グラフの場面：左はしに持ち家派・右はしに賃貸派（しゃべる方だけ鳴らす）。字幕は上。"""
    ch = CHARTS[name]
    ss = ch.still_from() + 0.5 if still else 0.0
    cats = [cat("@react", "持ち家派", 150, h=560, bottom=1080, label_size=48, mute=who != "L"),
            cat("@calm", "賃貸派", 1775, h=560, bottom=1080, label_size=48, mute=who != "R")]
    lst = [] if not se else ([se] if isinstance(se, (str, dict)) else list(se))
    if not still:
        cnt = {}
        for t0, col, _n, _v, _c in ch.steps:
            if t0 < 0:
                continue
            seq = STEP_SE.get(name, {}).get(col, ["explosion_chudoon"])
            f = seq[min(cnt.get(col, 0), len(seq) - 1)]
            cnt[col] = cnt.get(col, 0) + 1
            lst.append({"f": f, "at": t0 + 0.3, "gain": -6 if f == "explosion_chudoon" else -3})
        if ch.result_at is not None:
            lst.append({"f": "game_mario_1up", "at": ch.result_at, "gain": -4})
        dur = max(dur or 0, (ch.still_from() - 0.6) / R.TEMPO)
    return dict(bg=chart_path(name), bg_ss=ss, cats=cats, say=say, text_box=(60, 6, 1860, 226), say_size=104,
                say_style="red" if red else None, keep_overlap=True, chart=True, dur=dur, se=lst, fixed=not still, **kw)


def sp(say, who="L", lb=HOUSE, rb=APT, red=False, side=None, **kw):
    """画面半分の比べる場面（10/29 ユーザー指定）：左＝持ち家（持ち家派の猫）・右＝賃貸（賃貸派の猫）。
    who はしゃべる側（L/R）。しゃべる猫は大きく、聞く猫は少し小さく。side=(左の文字, 右の文字) は金額などをそれぞれの側に大きく。"""
    big, small = (700, 600) if not side else (600, 520)
    cats = [cat("@react", "持ち家派", 480, h=big if who == "L" else small, bottom=1075, label_size=54, mute=who != "L"),
            cat("@calm", "賃貸派", 1440, h=big if who == "R" else small, bottom=1075, label_size=54, mute=who != "R")]
    out = dict(bg=bg(lb), bg2=bg(rb), split=("持ち家", "賃貸"), split_cols=((220, 110, 20), (0, 110, 210)), split_y=232,
               split_tint=0.1, split_size=58, cats=cats, say=say, text_box=(30, 10, 930, 225) if who == "L" else (990, 10, 1890, 225), say_size=100, keep_overlap=True,
               side_text=side, **kw)
    if red:
        out.update(say_style="red", fx=["shake"])
    return out


def fx(c, *names, **extra):
    """場面にエフェクトを足す（crack ヒビ・mono 一瞬白黒・money お札・swirl ぐるぐる。多用しない）。"""
    c["fx"] = list(c.get("fx", [])) + list(names)
    c.update(extra)
    return c


CONAN = "anime_conan_hirameki_idea_realize_truth"
CONAN_R = ["anime_conan_hirameki_remix_a", "anime_conan_hirameki_remix_b", "anime_conan_hirameki_remix_c"]
POON = "tv_professional_poon"
POON_R = ["tv_professional_poon_remix_a", "tv_professional_poon_remix_b"]   # c はボツ（10/29）


def qq(who="L", lb=HOUSE, rb=APT, remix=CONAN_R[1]):
    """コナンの連打の場面：字幕のかわりに、いろいろな色とエフェクトの「？？？？？？」。画面半分のまま。"""
    c = sp(None, who, lb, rb)
    c.update(qmarks=8, qmark_size=660, qmark_y=430, se=[remix], dur=2.0, no_pop=True, fx=["flash", "ring"])
    return c


def card(c, sub, b=BOARD, **kw):
    return L.dia(c, sub, b, right=("@calm", "賃貸派"), dur=kw.pop("dur", 4.4), se=kw.pop("se", "card_flip"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き（動く猫の上を半分暗くして・ピンポンパンポーン） ----
        dict(bg=bg(HOUSE), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in (
                ("dance_happy_banana_cat", 220, 600), ("dance_three_kittens", 640, 520), ("walk_white_duck", 1000, 520),
                ("happy_hamster_open_arms", 1360, 560), ("dance_tabby_standing_cat", 1720, 600))],
             fx=["dim"], layers_top=[pt("e00_notice")], dur=6.0, no_pop=True, notice=True,
             se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- ① つかみ ----
        sp("家賃なんて捨て金\n買ったほうが得でしょ！", "L", se="pikon", bgm={"file": PURPLE, "gain": -4}),
        sp("35年ローンとか無理\n身軽が一番！", "R", se="pikon"),
        g("c0_preview", "35年でかかるお金を\nぜんぶ積むと……", dur=6.0),
        fx(sp("え……\n賃貸のほうが\n940万も安い？", "L", LIVING, ROOM, se=POON), "mono"),   # え…の場面はポーン（1回目はふつう）
        sp("でも話は\nここで終わらない!?", "R", red=True, se=CONAN),   # !? の場面はコナン（1回目はふつう）
        dict(bg=bg(HOUSE), card=pt("e01_title"), dur=4.0, se="jan",
             cats=[{"a": "dance_happy_banana_cat", "x": 300, "h": 440, "bottom": 1050, "float": True, "mute": True},
                   {"a": "walk_white_duck", "x": 1640, "h": 420, "bottom": 1050, "float": True, "mute": True}]),
        card("e02_premise", "郊外の3LDK・30歳の夫婦の場合", dur=5.4),
        # ---- ② 最初にかかるお金 ----
        chap("① 最初にかかるお金", se="quiz_question_01", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        sp("家を買うと\nまず頭金と諸費用", "L", AGENT, AGENT, side=("頭金450万\n諸費用300万", None), se="pi"),
        sp("賃貸は\n敷金・礼金・仲介料", "R", AGENT, AGENT, side=(None, "約50万"), se="pi"),
        g("c1_first", "最初の一歩は\n持ち家がずっと重い", dur=3.6),
        sp("750万!?\n貯金がぜんぶ消える", "L", AGENT, AGENT, red=True, se=CONAN_R[0]),   # コナン連打（1回目）
        # ---- ③ 毎月のお金 ----
        chap("② 毎月はらうお金", se="whoosh_shu"),
        sp("4050万を35年ローン\n金利1%なら", "L", LIVING, ROOM, side=("月11.4万", None), se="pi"),
        sp("同じ広さの3LDKを\n借りると", "R", LIVING, ROOM, side=(None, "月13万"), se="pi"),
        g("c2_month", "毎月だけなら\n持ち家のほうが安い！", who="L", dur=3.4),
        sp("ほら！\nやっぱり買ったほうが得！", "L", LIVING, ROOM, red=True, se="explosion_dokaan"),
        sp("ところが……", "R", LIVING, ROOM, se="pi"),
        # ---- ④ 持ち家だけにかかるお金 ----
        chap("③ 持ち家だけに\nかかるお金", se="doon_heavy", bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        sp("家は持ってるだけで\n毎年 固定資産税", "R", HOUSE, APT, side=("年12万", None), se="pi"),
        sp("10〜15年ごとに\n屋根と外壁の塗り直し", "R", ROOF, APT, side=("1回100万〜", None), se="pi"),
        sp("給湯器・お風呂・キッチンも\nいつかは壊れる", "R", ROOF, APT, se="kon"),
        g("c3_house", "35年で\n約1170万", dur=3.8),
        qq("L", ROOF, APT),   # コナン連打（2回目）＋色とりどりの「？？？？？？」
        sp("ローンのほかに\n1000万以上……", "L", ROOF, APT, se="deflate_hyororo"),
        # ---- ⑤ 賃貸だけにかかるお金 ----
        chap("④ 賃貸だけに\nかかるお金", se="whoosh_shu"),
        sp("賃貸は2年ごとに\n更新料", "L", HOUSE, APT, side=(None, "家賃1か月分"), se="pi"),
        sp("引っ越すたびに\n初期費用もかかる", "L", HOUSE, ROOM, se="pi"),
        g("c4_rent", "35年で\n約320万", who="R", dur=3.2),
        sp("え……\n賃貸はそれだけ？", "L", HOUSE, ROOM, se=POON_R[0]),   # ポーン連打（1回目）
        sp("修繕は大家さんが\nやってくれるからね", "R", HOUSE, ROOM, se="kon"),
        # ---- ⑥ 35年の合計 ----
        chap("⑤ 35年の合計", se="quiz_question_01", bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        g("c5_35y", "35年で\nくらべると……", dur=6.4),
        fx(sp("賃貸のほうが\n約940万 安い", "R", MONEY, MONEY, red=True, se="explosion_dokaan"), "money"),
        sp("え……\n車が何台も買える額……", "L", MONEY, MONEY, se=POON_R[1]),   # ポーン連打（2回目）
        # ---- ⑦ でも35年後は？ ----
        chap("⑥ でも35年後は？", se="doon_heavy"),
        sp("ローンが終わったら\n持ち家は税金と修繕だけ", "L", HOUSE, APT, side=("年 約30万", None), se="pi"),
        sp("賃貸は90歳になっても\n家賃をはらい続ける", "R", HOUSE, APT, side=(None, "年 約160万"), se="pi"),
        fx(sp("え……\nずっとはらうの？", "R", LIVING, ROOM, se=POON), "swirl"),   # 連打は2回まで → ふつうのポーン
        g("c6_90y", "90歳まで\nくらべると……", dur=4.6),
        fx(sp("逆転!?\n持ち家が約2370万 安い", "L", MONEY, MONEY, red=True, se=CONAN), "crack"),
        sp("しかも持ち家は\n家と土地が残る", "L", HOUSE, APT, se="pikon"),
        # ---- ⑧ 気をつけたいこと ----
        chap("⑦ 気をつけたいこと", se="whoosh_shu", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        sp("金利が上がると\nローンの返済もふえる", "R", LIVING, ROOM, side=("金利2%なら\n月13.4万", None), se="pi"),
        sp("地震や水害で\n家が傷むことも", "R", HOUSE, APT, se="kon"),
        sp("転勤や家族が変わっても\n住みかえにくい", "R", HOUSE, APT, se="kon"),
        sp("でも賃貸は\n年をとると借りにくい", "L", HOUSE, APT, se="kon"),
        sp("老後の家賃を\nはらい続けられるか", "L", LIVING, ROOM, se="kon"),
        # ---- ⑨ まとめ ----
        chap("まとめ", se="doon_heavy"),
        card("e07_points", "どっちが得かは　住む年数と暮らし方しだい", dur=5.6),
        sp("同じ場所に長く住むなら\n持ち家", "L", HOUSE, APT, se="pikon"),
        sp("身軽に住みかえたいなら\n賃貸", "R", HOUSE, APT, se="pikon"),
        sp("自分の暮らし方で\n選んでみよう", "R", LIVING, ROOM, se="kon"),
        dict(bg=bg(HOUSE), card=pt("e10_ending"), dur=3.6, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


FLASHY = ("explosion", "shock", "dokaan", "desk_slam", "siren", "jan", "power_up", "doon_heavy", "glass_break")
POP_SE = ("pikon", "spo", "puni", "kote", "pa", "papa", "peta", "suupo", "button_13", "cursor_move_01")   # 頭の小さな音
BIG_SE = ("voice_uuwaa", "boing_02", "tsukkomi_bashi", "punch", "frying_pan_kaan", "kaan", "hit_dogo_maou", "shock_piano")


def hype(cuts):
    """車の動画と同じ：派手な演出と効果音を多めに。集中線は驚きの場面の3回に1回だけ。コナン・ポーンの場面はその音だけ。"""
    for i, c in enumerate(cuts):
        if c.get("notice"):
            continue
        fx_ = list(c.get("fx", []))
        se = c.get("se")
        ses = " ".join((x if isinstance(x, str) else x.get("f", "")) for x in ([se] if isinstance(se, (str, dict)) else (se or [])))
        big = c.get("say_style") == "red" or any(k in ses for k in FLASHY) or c.get("chapter")
        if c.get("chart"):
            fx_ += ["border"] + (["flash", "ring"] if big else [])
        else:
            fx_ += ["punch"]
            if i % 4 == 1:
                fx_.append("border")
            if big:
                fx_ += ["flash", "shake", "ring", "border"] + (["lines"] if i % 3 == 0 else [])
            elif not c.get("split"):
                fx_.append("zoom")
        c["fx"] = list(dict.fromkeys(f for f in fx_ if f not in ("spark", "confetti")))
        lst = [] if not se else ([se] if isinstance(se, (str, dict)) else list(se))
        names_ = [x if isinstance(x, str) else x.get("f", "") for x in lst]
        if any("conan" in n_ or "poon" in n_ for n_ in names_):
            for q in c.get("cats", []):
                q["mute"] = True
            c["no_pop"] = True
            c["se"] = [{"f": n_, "gain": 0} if ("conan" in n_ or "poon" in n_) else x for n_, x in zip(names_, lst)]
            continue
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
    out = os.path.join(HERE, "out", "27_mochiie_full.mp4")
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
