"""32_jiro（毎日 二郎系ラーメンを食べ続けるとどうなる…？）のカット割り（10/30 ユーザー指定）。約3分。

python3 catmeme/cuts_32_jiro.py          → out/32_jiro_full.mp4
python3 catmeme/cuts_32_jiro.py --charts → グラフの動く背景だけ作る

10/30 ユーザー指定：8分ぶんの原稿量を3分に圧縮。SE・エフェクト多め（エスコンの動画と同じ作り）。
- 10/30 ユーザー指定：ニュース猫・博識な猫は出さない。ナレーションで解説。食べ続けるのは架空の「チャレンジ猫」、つっこみは架空の「友だち猫」（場面ごとに素材を変える・名札は同じ）
- お店の名前は出さない（「二郎系ラーメン」というジャンルの呼び方だけ）。お店や食べる人をけなさない。最後は「ほどほどに」
数字はざっくりの目安（お店・量・トッピングで大きく変わる）：
- 二郎系ラーメン1杯 約1500〜2000kcal（グラフは1800）。塩分はスープまで飲むと10g以上も（グラフは12g）
- 大人の男性が1日に必要なカロリー 約2700kcal（ふつうに動く30〜40代）。食塩の1日の目標 男性7.5g未満・女性6.5g未満（国の基準）
- 体脂肪1kg＝約7200kcal。ふつうの1食（約700kcal）を二郎系に置きかえると1日 約800kcal（以上）多い
  → 計算上 1週間 約0.8kg・1か月 約3kg・半年 約20kg・1年 約40kg。実際は体が慣れたり食べる量が変わるので、ここまで単純ではない
- 塩分が多い→むくみ・のどがかわく。続くと血圧が上がりやすい。脂が多い→中性脂肪がふえやすい（一般的な話）
- よい所：もやし・キャベツ（野菜）と豚（たんぱく質）がたっぷり
原稿のルール：今日の一言・単語の途中で改行しない・最後はチャンネル登録・過去の動画にはふれない
"""
import glob
import os
import sys

import cuts_04_leak as L
import cuts_26_kuruma as K
import render as R
import wide_bars as B

R.TEMPO = 1.22
HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", "32_jiro")] + sorted(
    d for d in glob.glob(os.path.join(HERE, "backgrounds", "*")) if os.path.isdir(d))
L.PT = os.path.join(HERE, "parts", "32_jiro")
pt, cat, chap, fx, CONAN, POON = L.pt, L.cat, L.chap, K.fx, K.CONAN, K.POON
PURPLE, COCOA, MIRAI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.NORA

HERO_NAME = "チャレンジ猫"
L.ROLE[HERO_NAME] = (220, 120, 0)
L.ROLE["友だち猫"] = (0, 110, 210)
LOOK = {"食べる": "eat_pop_cat", "がっつく": "eat_crunchy_cat_luna", "ポリポリ": "eat_chips_cat", "よろこぶ": "happy_chipi_chapa_cat",
        "ワクワク": "excited_hodomoe_city_cat", "のむ": "eat_crunchy_cat_luna", "ねむい": "sleepy_sleepy_cat",
        "ぼー": "blank_black_cat_zoning_out", "おどろく": "stare_tabby_wide_eyes_cat", "ぜつぼう": "despair_dramatic_kitten",
        "なく": "sad_banana_cat_cry", "いじける": "sulk_hungry_cat", "考える": "think_chin_paw_orange_cat", "さけぶ": "scream_phone_orange_cat",
        "ならぶ": "walk_white_duck", "走る": "dance_white_dog", "気づく": "realize_wet_cat_stare", "おどる": "dance_happy_banana_cat"}

# 背景（ChatGPT で作る背景が届いたら backgrounds/32_jiro に同じ名前で置けば差しかわる。指示文 scripts/32_jiro_bg_prompts.md）
LINE, COUNTER, BOWL, ROOM, SCALE, CLINIC, PARK, BOARD = (
    "bg32_shop_line", "bg32_counter", "bg32_bowl_mountain", "bg32_room_night", "bg32_bathroom_scale", "bg32_clinic",
    "bg32_jog_park", "bg03_blackboard")
K.STANDIN.update({LINE: "bg47_ramen_shop", COUNTER: "bg47_ramen_shop", BOWL: "bg67_food_sample", ROOM: "bg14_home_night",
                  SCALE: "bg02_room", CLINIC: "bg28_jp_clinic", PARK: "bg59_sakura_park"})
bg = K.bg
_bbg = B._bg


def _chart_bg(n):
    try:
        return _bbg(n)
    except FileNotFoundError:
        return _bbg(K.STANDIN[n])


B._bg = _chart_bg
# 10/30 ユーザー指定：ニュース猫・博識な猫は出さない。ナレーション（下の大きな字）とチャレンジ猫・友だち猫だけで進める
NAR = (60, 830, 1860, 1070)
FRIEND = "友だち猫"   # 架空
FRIEND_LOOK = ["stare_big_eyes_tabby_kitten", "surprise_big_pupils_cat", "huh_huh_cat", "glare_disgusted_cat", "stare_tabby_wide_eyes_cat"]
BACK = ["考える", "食べる", "ポリポリ", "ぼー", "気づく", "ねむい", "がっつく"]
_k = {"f": 0, "b": 0}


def two_lines(text):
    """10/30 ユーザー指定「字幕を大きく」：ナレーションは2行まで。3行以上は、長さがそろう所で2行にまとめる。"""
    ls = text.split("\n")
    if len(ls) <= 2:
        return text
    k = min(range(1, len(ls)), key=lambda i: abs(len("".join(ls[:i])) - len("".join(ls[i:]))))
    return "　".join(ls[:k]) + "\n" + "　".join(ls[k:])


def n(text, b, who=None, **kw):
    """ナレーション：画面の下に白い大きな字。後ろにチャレンジ猫を小さめに（声は出さない）。"""
    lk = who or BACK[_k["b"] % len(BACK)]
    _k["b"] += 1
    cats = [cat(LOOK[lk], HERO_NAME, 960, h=560, bottom=790, label_size=50, mute=True, float=True)]
    return dict(bg=bg(b), cats=cats, sub=two_lines(text), sub_box=NAR, sub_size=110, keep_overlap=True, se=kw.pop("se", "page_turn_01"), **kw)


def ss(say, b, **kw):
    return n(say, b, **kw)


def nn(say, b, red=False, **kw):
    """友だち猫がおどろく・つっこむ（まん中に大きく1匹）。"""
    a = FRIEND_LOOK[_k["f"] % len(FRIEND_LOOK)]
    _k["f"] += 1
    c = dict(bg=bg(b), cats=[cat(a, FRIEND, 960, h=780, bottom=1075, label_size=60)], say=say, text_top=True, keep_overlap=True, **kw)
    if red:
        c.update(say_style="red", fx=["shake", "lines"])
    return c

# ---- グラフ ----
K.CHARTS.update({
    "j1_kcal": B.Chart([("ふつうの1食", "green"), ("二郎系1杯", "red"), ("大人の1日分", "blue")],
                       [(0.4, 0, "", 700, "green"), (1.2, 1, "目安", 1800, "red"), (2.0, 2, "", 2700, "blue")], 3000,
                       bg=COUNTER, unit="", head="カロリーくらべ（目安）", total_fmt="{v}kcal", highlight=1),
    "j2_salt": B.Chart([("1日の目標", "green"), ("二郎系1杯", "red")],
                       [(0.4, 0, "男性", 7.5, "green"), (1.4, 1, "スープまで", 12, "red")], 13,
                       bg=BOWL, unit="", head="塩分くらべ（目安）", total_fmt="{v}g", highlight=1),
})
K.DROP_SE.update({"j1_kcal": {1: "explosion_dokaan", 2: "taiko_dodon_01"}, "j2_salt": {1: "explosion_dokaan"}})
K.STEP_SE.update({"j1_kcal": ["pikon"], "j2_salt": ["pikon"]})

# 派手な音（どれも配布サイトの音）
BOOM, GONG, SLASH, DRUM, CYM, DASH, KIRA, HERO, UP = ("explosion_dokaan", "gong_dora_jaan", "sword_shakiin", "taiko_dodon_01",
                                                      "cymbal_maou", "dash_super_fast", "shine_kiraan_maou", "hero_pose", "power_up")


def h(look, say, b, red=False, **kw):
    """チャレンジ猫（まん中に大きく1匹・名札・上に字幕）。"""
    c = dict(bg=bg(b), cats=[cat(LOOK[look], HERO_NAME, 960, h=780, bottom=1075, label_size=60)], say=say, text_top=True,
             keep_overlap=True, **kw)
    if red:
        c.update(say_style="red", fx=["shake", "lines"])
    return c


def g(name, say, who="S", **kw):
    """グラフの場面（猫は出さない・字幕だけ）。"""
    c = K.g(name, say, who=who, **kw)
    c["cats"] = []
    return c


def day(text, b, look, se=None):
    """日数の札：スロットのように回って止まる（1日目 → 1年 など）。"""
    pre, v, post = text
    return fx(h(look, None, b, se=["drumroll", {"f": se or "explosion_bokaan", "at": 0.9}], dur=2.0), slot=(pre, v, post))


def card(c, sub, **kw):
    return L.dia(c, sub, BOARD, dur=kw.pop("dur", 4.4), se=kw.pop("se", "card_flip"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(bg=bg(LINE), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in (
                ("eat_pop_cat", 260, 560), ("eat_crunchy_cat_luna", 700, 520), ("eat_chips_cat", 1180, 540),
                ("dance_happy_banana_cat", 1640, 600))],
             fx=["dim"], layers_top=[pt("e00_notice")], dur=5.0, no_pop=True, notice=True,
             se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- つかみ ----
        h("ワクワク", "決めた！\n毎日 二郎系ラーメンを\n食べ続ける！", BOWL, red=True, se=[BOOM], bgm={"file": PURPLE, "gain": -4}),
        nn("毎日!?\nあの山盛りを!?", BOWL, red=True, se=[CONAN]),
        ss("体はどう変わるのか\n計算してみよう", BOWL, se=DRUM),
        dict(bg=bg(BOWL), card=pt("e01_title"), dur=3.4, se=GONG,
             cats=[{"a": "eat_pop_cat", "x": 300, "h": 440, "bottom": 1050, "float": True, "mute": True}]),
        card("e02_premise", "計算の前提（ざっくりの目安）", dur=4.6),
        # ---- ① 二郎系ってどんなラーメン？ ----
        chap("① 二郎系ってどんなラーメン？", se=SLASH, bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        ss("極太の麺に\nもやしとキャベツの山", BOWL, se=KIRA),
        ss("分厚い豚\n背脂とにんにく", BOWL, se=["meat_grilling_sizzle"]),
        nn("「ニンニク入れますか？」\nって聞かれるやつ！", COUNTER, se="pikon"),
        h("ワクワク", "ヤサイ\nマシマシで！", COUNTER, red=True, se=["air_horn", BOOM]),
        ss("トッピングを増やす\n「コール」の文化", COUNTER, se=HERO),
        ss("麺だけで\nふつうのラーメンの\n2倍以上あることも", BOWL, se=UP),
        # ---- ② 1杯のカロリー ----
        chap("② 1杯でどれくらい？", se=SLASH),
        g("j1_kcal", "1杯で\n大人の1日分の\n半分以上!?", who="N", red=True, dur=4.0),
        fx(nn("え……\n1杯で\n1日の半分？", COUNTER, se=POON), "mono"),
        g("j2_salt", "スープまで飲むと\n塩分は1日の目標を\n大きくこえる", who="S", dur=3.8),
        ss("いつもの1食より\n1日 約800kcal\n多くなる計算", MONEY := "bg87_refund_money", se=DRUM),
        # ---- ③ 1日目 ----
        day(("", 1, "日目"), COUNTER, "食べる"),
        fx(h("がっつく", "うまーい!!\n最高!!", BOWL, red=True, se=[CYM, "cheer_applause"]), "lines"),
        h("のむ", "スープも\n全部いっちゃう！", BOWL, se="drink_gulp_gokugoku_thirsty_chug"),
        ss("食べたあとは\nのどがかわいて\n眠くなりやすい", ROOM, se="pi"),
        h("ねむい", "おなかいっぱいで\n動けない……", ROOM, se="deflate_hyororo"),
        # ---- ④ 1週間 ----
        day(("", 1, "週間"), LINE, "ならぶ", se=GONG),
        h("ならぶ", "今日も\n行列にならぶ", LINE, se=DASH),
        fx(ss("計算上は\n体重 約+0.8kg", SCALE, se=["drumroll", {"f": "explosion_bokaan", "at": 0.9}], dur=2.2),
           slot=("体重 +", 0.8, "kg")),
        ss("塩分が多いと\n体が水をためこんで\nむくみやすい", SCALE, se="kon"),
        h("おどろく", "朝 顔が\nパンパン!?", ROOM, red=True, se=["anime_conan_hirameki_remix_a"]),
        # ---- ⑤ 1か月 ----
        day(("", 1, "か月"), COUNTER, "ポリポリ", se=GONG),
        fx(ss("計算上は\n体重 約+3kg", SCALE, se=["drumroll", {"f": BOOM, "at": 0.9}], dur=2.2), slot=("体重 +", 3, "kg")),
        h("いじける", "ズボンが\nきつい……", ROOM, se="gugi"),
        nn("でも野菜は\nたっぷり食べてるよね？", BOWL, se="question_hatena_maou"),
        ss("もやしとキャベツと\n豚のたんぱく質は\nたしかにいい所", BOWL, se=KIRA),
        ss("ただ脂と塩分と\n麺の量が\nそれ以上に多い", BOWL, se="shock_piano"),
        # ---- ⑥ 半年 ----
        chap("③ 半年後", se=SLASH, bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        fx(ss("計算上は\n体重 約+20kg", SCALE, se=["drumroll", {"f": "explosion_dokaan", "at": 0.9}], dur=2.2),
           slot=("体重 +", 20, "kg")),
        fx(h("さけぶ", "体重計が\nこわれた!?", SCALE, red=True, se=["glass_break_01", BOOM]), "crack"),
        ss("階段で息が切れる\nひざや腰に\n負担がかかる", PARK, se="pi"),
        h("ぼー", "体が\n重い……", PARK, se="deflate_hyororo"),
        # ---- ⑦ 健康診断 ----
        chap("④ 健康診断の日", se=SLASH),
        ss("塩分が多い日が続くと\n血圧が上がりやすい", CLINIC, se="pc_warning"),
        ss("脂が多いと\n血の中の脂\n中性脂肪もふえやすい", CLINIC, se="kon"),
        fx(h("ぜつぼう", "判定\n「要再検査」……", CLINIC, red=True, se=["chin_bell_failure_sad_ending"]), "mono"),
        fx(nn("え……\nまだ半年なのに？", CLINIC, se="tv_professional_poon_remix_a"), "swirl"),
        # ---- ⑧ 1年 ----
        day(("", 1, "年"), CLINIC, "なく", se=BOOM),
        fx(ss("計算上は\n体重 約+40kg", SCALE, se=["drumroll", {"f": "explosion_dokaan", "at": 0.9}], dur=2.2),
           slot=("体重 +", 40, "kg")),
        nn("+40kg!?\nもう別の猫じゃん!?", SCALE, red=True, se=["anime_conan_hirameki_remix_b"]),
        ss("ただし実際は\n体が慣れたり\n食べる量が変わるので\nここまで単純ではない", SCALE, se="pi"),
        ss("それでも毎日は\n体への負担が\nじわじわ積もる", CLINIC, se="shock_piano"),
        # ---- ⑨ 楽しむコツ ----
        chap("⑤ 楽しむコツ", se=SLASH, bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        ss("スープは\n飲み干さない", BOWL, se=KIRA),
        ss("麺は「少なめ」で\nたのむこともできる", COUNTER, se="pikon"),
        ss("次の食事は\n軽めにして\n野菜と水分を", ROOM, se="pi"),
        fx(h("走る", "食べたぶん\n歩く！走る！", PARK, se=[DASH, UP]), "lines"),
        h("気づく", "毎日じゃなくて\nごほうびの日に\nしよう", COUNTER, se=HERO),
        # ---- まとめ ----
        chap("まとめ", se=SLASH),
        card("e07_points", "今回のポイント", dur=4.4),
        nn("おいしいからこそ\nたまにが\nいちばんだね", BOWL, se="pikon"),
        h("おどる", "週末の\nごほうびに\nいってきます！", LINE, se=["cheer_applause", "fanfare_pararappara"]),
        dict(bg=bg(BOWL), card=pt("e10_ending"), dur=3.0, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def more(cuts):
    """多め：赤字の驚きにはドンを重ねる。エフェクトも1場面に2〜3個（エスコンの動画と同じ）。"""
    for i, c in enumerate(cuts):
        if c.get("notice") or c.get("chapter") or c.get("card") or c.get("inset"):
            continue
        names = [x if isinstance(x, str) else x.get("f", "") for x in (c.get("se") or [])]
        if any("conan" in n_ or "poon" in n_ for n_ in names):
            continue
        lst = list(c.get("se") or [])
        if c.get("say_style") == "red":
            lst.append({"f": "explosion_dokaan", "gain": -6, "at": 0.05})
        c["se"] = lst
        fx_ = list(c.get("fx", [])) + ["punch", "border"]
        if i % 3 == 0:
            fx_.append("ring")
        if i % 4 == 2 and not c.get("chart"):
            fx_ += ["flash", "zoom"]
        if i % 5 == 1 and not c.get("chart"):
            fx_.append("lines")
        c["fx"] = list(dict.fromkeys(fx_))
    return cuts


def cuts_full():
    cs = more(K.hype(L.apply_fx(L.allocate(cuts_all(), max_use=7, gap=1))))
    for c in cs:   # テンポ優先：猫の音に合わせて場面をのばさない・素材を最後まで流さない
        if not c.get("notice") and not c.get("card") and not c.get("chart"):
            c["fixed"] = True
        for k in c.get("cats", []):
            k.setdefault("full", False)
    return cs


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "32_jiro_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if sys.argv[1:] == ["--charts"]:
        for k in ("j1_kcal", "j2_salt"):
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
