"""29_kome（お米が消えた夏 お米の値段はなぜ上がった？）のカット割り（10/29 ユーザー指定）。3分ほど。作りは 26本目（車）と同じ。

python3 catmeme/cuts_29_kome.py          → out/29_kome_full.mp4
python3 catmeme/cuts_29_kome.py --charts → グラフの動く背景だけ作る

車の動画で決めたルールを使う（部品は cuts_26_kuruma から借りる）：
- 掛け合いはニュース猫（左）と博識な猫（右）の2匹だけ大きく。グラフを多く・積み上がる途中はゲーム・アニメの音
- 「!?」はコナン、「え…」はポーン（1回目はふつう、連打は2回まで）。その場面は猫の声とほかの音を入れない
- 集中線は控えめ。ヒビ・白黒・お札・スロット・ぐるぐる・「？」の飾りは1回ずつくらい

事実とざっくりの目安（報道・農林水産省の発表より）：
- 2024年8月ごろ、スーパーの棚からお米が消えた（「令和の米騒動」と呼ばれた）。1人1袋までの店も
  2024年8月に南海トラフ地震の臨時情報が出て、買いだめが重なった
- 原因と言われること：2023年の猛暑で品質のよい米が減り、精米すると取れる量も減った／観光客・外食で使う量がふえた／
  長く作る量をおさえてきた（生産調整）／業者どうしで先に買い集める動き
- スーパーの5kgの平均（目安）：2023年 約2000円 → 2024年8月 約2600円 → 2025年1月 約3700円 → 2025年5月 約4300円
- 2025年3月に国の備蓄米を入札で放出、5月からは随意契約で放出し、5kg 2000円台の備蓄米が店頭に
- 3人家族で月10kg食べると：2023年 月約4000円（年約4.8万）→ 2025年5月 月約8600円（年約10.3万）
原稿のルール：実在の人は出さない（役所は名札つきの猫）。農家・お店をせめない。今日の一言・最後はチャンネル登録
"""
import glob
import os
import sys

import cuts_04_leak as L
import cuts_26_kuruma as K
import render as R
import wide_bars as B

R.TEMPO = 1.15   # 文字を読める速さ（3分ほど）
HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", "29_kome")] + sorted(
    d for d in glob.glob(os.path.join(HERE, "backgrounds", "*")) if os.path.isdir(d))
L.PT = os.path.join(HERE, "parts", "29_kome")
pt, cat, chap = L.pt, L.cat, L.chap
nn, ss, boom, fx, qq, CONAN, POON = K.nn, K.ss, K.boom, K.fx, K.qq, K.CONAN, K.POON
PURPLE, COCOA, MIRAI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.NORA
L.ROLE["農林水産省"] = (90, 60, 150)

# 背景（ChatGPT で作る背景が届いたら backgrounds/29_kome に同じ名前で置けば差しかわる。指示文 scripts/29_kome_bg_prompts.md）
SHELF, FIELD, STORE, KITCHEN, WARE, BOARD, MONEY = (
    "bg29_empty_rice_shelf", "bg29_rice_field", "bg29_rice_store", "bg29_kitchen_rice", "bg29_rice_warehouse", "bg03_blackboard",
    "bg87_refund_money")
K.STANDIN.update({SHELF: "bg15_convenience", FIELD: "ph06_kumamoto_fields", STORE: "bg15_convenience", KITCHEN: "st02_home_kitchen",
                  WARE: "bg03_jp_material_plant"})
bg = K.bg
_bbg = B._bg


def _chart_bg(n):
    try:
        return _bbg(n)
    except FileNotFoundError:
        return _bbg(K.STANDIN[n])


B._bg = _chart_bg

# ---- グラフ ----
YEARS = [("2023年", "green"), ("2024年8月", "gold"), ("2025年1月", "orange"), ("2025年5月", "red")]
K.CHARTS.update({
    "m1_price": B.Chart(YEARS, [(0.4, 0, "", 2000, "green"), (1.2, 1, "", 2600, "gold"), (2.0, 2, "", 3700, "orange"),
                                (2.8, 3, "", 4300, "red")], 4600, bg=STORE, head="スーパーのお米 5kgの値段（目安）",
                        total_fmt="{v}円", highlight=3),
    "m2_bichiku": B.Chart([("ふつうのお米", "red"), ("備蓄米", "teal")], [(-1, 0, "", 4300, "red"), (0.5, 1, "", 2100, "teal")], 4600,
                          bg=STORE, head="5kgの値段（2025年夏ごろの目安）", total_fmt="{v}円"),
    "m3_kakei": B.Chart([("2023年", "green"), ("2025年5月", "red")], [(0.4, 0, "", 4.8, "green"), (1.4, 1, "", 10.3, "red")], 11.5,
                        bg=KITCHEN, head="3人家族のお米代（1年・月10kgの目安）", total_fmt="年{v}万", highlight=1),
})
K.STEP_SE.update({"m1_price": ["game_coin_get_money_gain_happy"]})
K.DROP_SE.update({"m1_price": {1: "anime_dbz_punch", 2: "game_dq_attack_enemy", 3: "explosion_chudoon"},
                  "m2_bichiku": {1: "game_zelda_item_get"}, "m3_kakei": {1: "explosion_chudoon"}})
g = K.g


def org(b, say, **kw):
    """役所は名札つきの猫（実在の人は出さない）。"""
    return dict(bg=bg(b), cats=[cat("stare_interviewer_cat", "農林水産省", 960, h=760, bottom=1075)], say=say, text_top=True,
                keep_overlap=True, **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(bg=bg(FIELD), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in (
                ("dance_happy_banana_cat", 220, 600), ("walk_white_duck", 640, 520), ("eat_pop_cat", 1000, 520),
                ("happy_hamster_open_arms", 1360, 560), ("dance_three_kittens", 1720, 560))],
             fx=["dim"], layers_top=[pt("e00_notice")], dur=6.0, no_pop=True, notice=True,
             se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- ① つかみ ----
        nn("スーパーの棚から\nお米が消えた!?", SHELF, red=True, se=CONAN, bgm={"file": PURPLE, "gain": -4}),
        ss("2024年の夏\n本当にあったこと", SHELF, se="pi"),
        boom("そして値段は\n2倍以上に", STORE, who="S", se=["explosion_dokaan"]),
        dict(bg=bg(FIELD), card=pt("e01_title"), dur=4.0, se="jan",
             cats=[{"a": "eat_pop_cat", "x": 300, "h": 440, "bottom": 1050, "float": True, "mute": True},
                   {"a": "sad_banana_cat_cry", "x": 1640, "h": 420, "bottom": 1050, "float": True, "mute": True}]),
        # ---- ② 何が起きた？ ----
        chap("① 何が起きた？", se="quiz_question_01", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        ss("2024年8月\nスーパーのお米の棚が\n空っぽに", SHELF, se="pi"),
        ss("「1人1袋まで」\nというお店も", SHELF, se="pinpon_notice"),
        nn("え……\nお米って売り切れるの？", SHELF, se=POON),
        ss("ちょうどそのころ\n大きな地震への\n注意の呼びかけが出た", SHELF, se="kon"),
        ss("みんなが少し多めに\n買ったことも重なった", SHELF, se="pi"),
        nn("秋に新米が出れば\n元にもどるでしょ？", FIELD, se="pikon"),
        ss("ところが……", FIELD, se="pi"),
        # ---- ③ 値段が2倍に ----
        chap("② 値段が2倍に", se="doon_heavy"),
        g("m1_price", "5kgの値段を\nならべると……", dur=4.0),
        fx(boom("5kg\n4000円超え!?", STORE, se=[CONAN]), "money"),
        qq(STORE, "anime_conan_hirameki_remix_b"),   # コナン連打（1回目）＋色とりどりの「？？？？？？」
        nn("お米って\nこんなに高かった？", STORE, se="deflate_hyororo"),
        # ---- ④ なぜ上がった？ ----
        chap("③ なぜ上がった？", se="whoosh_shu", bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        ss("理由はひとつじゃない\nいくつも重なった", BOARD, se="pi"),
        ss("2023年の猛暑で\n品質のいいお米が減った", FIELD, se="kon"),
        nn("暑いと\nお米ってダメになるの？", FIELD, se="question_hatena_maou"),
        ss("白くにごったお米がふえて\n見た目の等級が下がる", FIELD, se="kon"),
        ss("精米すると\nとれる量も減った", WARE, se="kon"),
        ss("観光客や外食で\nお米を使う量がふえた", STORE, se="pi"),
        ss("2024年の観光客は\n過去最多の\n3600万人以上", STORE, se="pi"),
        nn("みんな日本の\nおにぎり好きだもんね", STORE, se="pikon"),
        ss("長いあいだ\n作る量をおさえてきた", FIELD, se="pi"),
        ss("お米を食べる人が\n減ってきたから\n作りすぎないように", FIELD, se="kon"),
        ss("業者どうしで\n先に買い集める動きも", WARE, se="kon"),
        fx(nn("え……\nお米はあるのに\nお店にない？", WARE, se="tv_professional_poon_remix_a"), "swirl"),   # ポーン連打（1回目）
        # ---- ⑤ 国が動いた ----
        chap("④ 国が動いた", se="doon_heavy", bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        org(WARE, "いざという時のための\n備蓄米を出します", se="pinpon_notice"),
        ss("2025年3月に\n入札で放出", WARE, se="pi"),
        ss("5月からは\n値段を決めて\n直接お店へ", WARE, se="pi"),
        g("m2_bichiku", "備蓄米は\n5kg 2000円台", dur=3.4),
        fx(boom("お店に\n長い行列!?", STORE, se=["anime_conan_hirameki_remix_c"]), "crack"),   # コナン連打（2回目）
        ss("外国のお米を\n買う人もふえた", STORE, se="pi"),
        nn("でも新米が出ても\nなかなか安くならない", STORE, se="kon"),
        ss("新しいお米も\n前より高い値段で\n取り引きされている", WARE, se="kon"),
        # ---- ⑥ 家計への影響 ----
        chap("⑤ 家計への影響", se="whoosh_shu"),
        ss("3人家族で\n月10kg食べると……", KITCHEN, se="pi"),
        g("m3_kakei", "1年のお米代が\n2倍以上に", dur=3.4),
        fx(nn("え……\n年に5万円も\nふえてる", KITCHEN, se="tv_professional_poon_remix_b"), "mono"),   # ポーン連打（2回目）
        ss("でも農家さんからは\n「やっと続けられる値段」\nという声もある", FIELD, se="kon"),
        nn("作る人がいなくなったら\nもっと困るもんね", FIELD, se="pikon"),
        # ---- ⑦ できること ----
        chap("⑥ 今できること", se="whoosh_shu", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        ss("あわてて\n買いだめしない", KITCHEN, se="pi"),
        ss("いろいろなお店や\n銘柄をくらべる", STORE, se="pi"),
        ss("ふるさと納税で\nお米をもらう手も", KITCHEN, se="pikon"),
        ss("炊いたごはんは\n小分けにして冷凍", KITCHEN, se="pi"),
        nn("むだにしないのが\nいちばんの節約か", KITCHEN, se="pikon"),
        nn("ごはんの\nありがたみが\nわかった……", KITCHEN, se="kon"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy"),
        K.card("e07_points", "お米の値段は　天気・需要・作る量・流通が重なって決まる", dur=5.6),
        ss("お米の値段は\nいくつもの理由が\n重なって動く", FIELD, se="kon"),
        nn("毎日のごはん\n大事に食べよう", FIELD, se="pikon"),
        dict(bg=bg(FIELD), card=pt("e10_ending"), dur=3.6, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


# ---- 10/30 ユーザー指定「エフェクト多く・1場面のSEをもっと増やして、SE洪水くらいに」 ----
FLOOD = ["game_coin_get_money_gain_happy", "anime_dbz_punch", "game_mario_jump", "game_dq_attack_enemy", "game_aceattorney_ping",
         "anime_shinchan_genkotsu", "game_ff_cursor", "anime_dbz_teleport", "kaan", "tsukkomi_bashi", "boing_02", "puni",
         "game_smash_homerun_bat", "game_mario_jump_bao", "pa", "pikon", "spo", "frying_pan_kaan", "game_dq_miss", "eat_paku"]
EXTRA_FX = {7: "crack", 20: "crack", 25: "money", 29: "money", 38: "crack", 49: "money"}   # 1人1袋・猛暑・観光客・買い集め・新米も高い・ふるさと納税


def flood(cuts):
    """どの場面も：頭・字幕が出るところ・なかほど・終わりぎわに、ゲーム・アニメの音を4〜6個。エフェクトも1場面に3〜4個。
    コナン・ポーンの場面はルールどおりその音だけ。説明画面（表・まとめ）は読みやすさ優先。"""
    n = 0
    for i, c in enumerate(cuts):
        if c.get("notice") or c.get("chapter") or c.get("card") or c.get("inset"):
            continue
        names = [x if isinstance(x, str) else x.get("f", "") for x in (c.get("se") or [])]
        if any("conan" in n_ or "poon" in n_ for n_ in names):
            continue
        d = R.cut_dur(c)
        lst = list(c.get("se") or [])
        ats = [0.12, 0.3] + [round(d * r, 2) for r in (0.45, 0.65, 0.85) if d * r > 0.5]
        if c.get("chart"):
            ats = [round(d * r, 2) for r in (0.75, 0.9)]   # グラフは落ちる音のあと、結果のところに重ねる
        for at in ats:
            lst.append({"f": FLOOD[n % len(FLOOD)], "gain": -7 if at > 0.3 else -5, "at": at})
            n += 1
        # 10/30 ユーザー指摘「動きのないところにSEをつけない」：SEを鳴らすところには必ず動きを足す
        # （猫がぴょんと跳ねて、画面が小さくグッと寄る）。場面の頭（0.3秒まで）は登場の動きがあるので足さない
        c["beats"] = [at for at in ats if at > 0.25]
        if c.get("say_style") == "red":
            lst += [{"f": "explosion_dokaan", "gain": -5, "at": 0.05}, {"f": "kaan", "gain": -5, "at": 0.4}]
        c["se"] = lst
        fx_ = list(c.get("fx", [])) + ["punch", "border"]
        if i % 2 == 0:
            fx_.append("ring")
        if i % 3 == 1 and not c.get("chart"):
            fx_ += ["flash", "zoom"]
        if i % 4 == 3 and not c.get("chart"):
            fx_ += ["lines", "shake"]
        if i in EXTRA_FX and not c.get("chart") and not set(fx_) & {"mono", "swirl", "money", "crack"}:
            fx_.append(EXTRA_FX[i])
        c["fx"] = list(dict.fromkeys(fx_))
    return cuts


def cuts_full():
    return flood(K.hype(L.apply_fx(L.allocate(cuts_all(), max_use=7, gap=1))))


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "29_kome_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if sys.argv[1:] == ["--charts"]:
        for k in ("m1_price", "m2_bichiku", "m3_kakei"):
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
