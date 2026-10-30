"""33_ha（歯をみがかない・歯医者にずっと行かないとどうなる…？）のカット割り（10/30 ユーザー指定）。約3分。

python3 catmeme/cuts_33_ha.py → out/33_ha_full.mp4

10/30 ユーザー指定：二郎系の動画と同じルール。8分ぶんの原稿量を3分に圧縮・SE・エフェクト多め。
ニュース猫・博識な猫は出さない。ナレーション（下の大きな字）と、架空の「ズボラ猫」「歯医者猫」だけで進める。
内容は一般的な目安（日本歯科医師会・厚生労働省などの一般向けの説明より）：
- みがかないと食べかすと細菌で歯垢（プラーク）がたまる。歯垢は数日〜2週間ほどで歯石になり、歯ブラシでは取れない
- 口のにおい、歯ぐきが赤くはれて血が出る（歯肉炎）。むし歯は C1→C2（しみる）→C3（神経・激痛）→C4（根だけ）。自然には治らない
- 歯周病：歯を支える骨がとけて歯がぐらぐら。歯を失う原因のいちばんは歯周病。大人の多くが歯周病か、その手前と言われる
- 歯周病は糖尿病や心臓の病気などとの関係も指摘されている（一般的な話）
- 早く行くほど治療は短く安い。進むと根の治療で何度も通う。歯を失うとブリッジ・入れ歯・インプラント（保険がきかず1本数十万円ほど）
- 定期健診は3〜6か月に1回がすすめられる。「80歳で20本」の8020運動
原稿のルール：今日の一言・単語の途中で改行しない・最後はチャンネル登録・過去の動画にはふれない・こわがらせすぎない
"""
import glob
import os
import sys

import cuts_04_leak as L
import cuts_26_kuruma as K
import render as R

R.TEMPO = 1.32
HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", "33_ha")] + sorted(
    d for d in glob.glob(os.path.join(HERE, "backgrounds", "*")) if os.path.isdir(d))
L.PT = os.path.join(HERE, "parts", "33_ha")
pt, cat, chap, fx, CONAN, POON = L.pt, L.cat, L.chap, K.fx, K.CONAN, K.POON
PURPLE, COCOA, MIRAI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.NORA

HERO, DOC = "ズボラ猫", "歯医者猫"   # どちらも架空
L.ROLE[HERO] = (200, 90, 0)
L.ROLE[DOC] = (0, 130, 150)
LOOK = {"ねむい": "sleepy_sleepy_cat", "ぼー": "blank_black_cat_zoning_out", "食べる": "eat_pop_cat", "ポリポリ": "eat_chips_cat",
        "知らんぷり": "slack_nail_filing_cat", "ごろごろ": "stare_lying_tabby_cat", "おどろく": "stare_tabby_wide_eyes_cat",
        "いたい": "despair_dramatic_kitten", "なく": "sad_banana_cat_cry", "さけぶ": "scream_phone_orange_cat",
        "しょんぼり": "sad_looking_away_tabby", "考える": "think_chin_paw_orange_cat", "気づく": "realize_wet_cat_stare",
        "よろこぶ": "happy_chipi_chapa_cat", "いじける": "sulk_hungry_cat", "いや": "glare_disgusted_cat", "にげる": "dance_white_dog"}
DOC_LOOK = {"話す": "stare_interviewer_cat", "説明": "read_book_orange_kitten", "おこる": "rage_talking_cat", "笑顔": "happy_hamster_open_arms",
            "見る": "peek_what_happen_cat"}

# 背景（ChatGPT で作る背景が届いたら backgrounds/33_ha に同じ名前で置けば差しかわる。指示文 scripts/33_ha_bg_prompts.md）
SINK, ROOM, MOUTH, CLINIC, CHAIR, BOARD, MONEY = ("bg33_washroom", "bg33_room_night", "bg33_teeth_closeup", "bg33_dental_clinic",
                                                  "bg33_dental_chair", "bg03_blackboard", "bg87_refund_money")
K.STANDIN.update({SINK: "st02_home_kitchen", ROOM: "bg14_home_night", MOUTH: "bg102_quiet_room", CLINIC: "bg28_jp_clinic",
                  CHAIR: "bg28_jp_clinic"})
bg = K.bg
NAR = (60, 830, 1860, 1070)
BACK = ["ごろごろ", "知らんぷり", "ねむい", "ぼー", "ポリポリ", "考える"]
_k = {"b": 0}

# 派手な音（どれも配布サイトの音）
BOOM, GONG, SLASH, DRUM, CYM, DASH, KIRA, HEROSE, UP = ("explosion_dokaan", "gong_dora_jaan", "sword_shakiin", "taiko_dodon_01",
                                                        "cymbal_maou", "dash_super_fast", "shine_kiraan_maou", "hero_pose", "power_up")


def n(text, b, who=None, **kw):
    """ナレーション：画面の下に白い大きな字。後ろにズボラ猫を小さめに（声は出さない）。"""
    lk = who or BACK[_k["b"] % len(BACK)]
    _k["b"] += 1
    cats = [cat(LOOK[lk], HERO, 960, h=560, bottom=790, label_size=50, mute=True, float=True)]
    return dict(bg=bg(b), cats=cats, sub=text, sub_box=NAR, sub_size=110, keep_overlap=True, se=kw.pop("se", "page_turn_01"), **kw)


def h(look, say, b, red=False, **kw):
    """ズボラ猫（まん中に大きく1匹・名札・上に字幕）。"""
    c = dict(bg=bg(b), cats=[cat(LOOK[look], HERO, 960, h=780, bottom=1075, label_size=60)], say=say, text_top=True,
             keep_overlap=True, **kw)
    if red:
        c.update(say_style="red", fx=["shake", "lines"])
    return c


def d(look, say, b=CLINIC, red=False, **kw):
    """歯医者猫（まん中に大きく1匹・名札・上に字幕）。"""
    c = dict(bg=bg(b), cats=[cat(DOC_LOOK[look], DOC, 960, h=780, bottom=1075, label_size=60)], say=say, text_top=True,
             keep_overlap=True, **kw)
    if red:
        c.update(say_style="red", fx=["shake", "lines"])
    return c


def two(hl, dl, say, b=CHAIR, who="R", **kw):
    """ズボラ猫（左）と歯医者猫（右）。しゃべる方だけ鳴らす。"""
    cats = [cat(LOOK[hl], HERO, 470, h=740, bottom=1075, label_size=56, mute=who != "L"),
            cat(DOC_LOOK[dl], DOC, 1450, h=740, bottom=1075, label_size=56, mute=who != "R")]
    return dict(bg=bg(b), cats=cats, say=say, text_top=True, keep_overlap=True, **kw)


def day(pre, v, post, b, look, se=None):
    """日数の札：スロットのように回って止まる。"""
    return fx(h(look, None, b, se=["drumroll", {"f": se or "explosion_bokaan", "at": 0.9}], dur=2.0), slot=(pre, v, post))


def card(c, sub, **kw):
    return L.dia(c, sub, BOARD, dur=kw.pop("dur", 4.4), se=kw.pop("se", "card_flip"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(bg=bg(SINK), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in (
                ("sleepy_sleepy_cat", 260, 560), ("stare_lying_tabby_cat", 700, 520), ("happy_hamster_open_arms", 1180, 560),
                ("dance_happy_banana_cat", 1640, 600))],
             fx=["dim"], layers_top=[pt("e00_notice")], dur=5.0, no_pop=True, notice=True,
             se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- つかみ ----
        h("ごろごろ", "歯みがき\nめんどくさい……\n今日もいいや", ROOM, se=["deflate_hyororo"], bgm={"file": PURPLE, "gain": -4}),
        h("知らんぷり", "歯医者も\nもう何年も\n行ってない", ROOM, se="pi"),
        d("おこる", "そのままだと\nとんでもないことに!!", CLINIC, red=True, se=[BOOM, "pc_warning"]),
        n("歯をみがかない・歯医者に行かない\nと口の中はどうなるのか", MOUTH, se=DRUM),
        dict(bg=bg(MOUTH), card=pt("e01_title"), dur=3.4, se=GONG,
             cats=[{"a": "sleepy_sleepy_cat", "x": 300, "h": 440, "bottom": 1050, "float": True, "mute": True}]),
        # ---- ① 1日目 ----
        chap("① みがかなかった次の日", se=SLASH, bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        day("", 1, "日目", ROOM, "ねむい"),
        n("食べかすと細菌で\n歯の表面に歯垢がたまる", MOUTH, se="kon"),
        h("いや", "なんか歯が\nネバネバする……", SINK, se="puni"),
        d("説明", "歯垢は\nただの汚れではなく\n細菌のかたまり", CLINIC, se=KIRA),
        # ---- ② 3日〜1週間 ----
        day("", 3, "日目", ROOM, "ぼー", se=GONG),
        n("細菌がふえて\n口のにおいが強くなる", MOUTH, se="pi"),
        h("おどろく", "えっ……\n口がくさい!?", SINK, red=True, se=[CONAN]),
        day("", 1, "週間", SINK, "しょんぼり", se=BOOM),
        n("歯ぐきが赤くはれて\nみがくと血が出る", MOUTH, se="shock_piano"),
        d("話す", "それが歯肉炎\n歯周病の入り口", CLINIC, se=DRUM),
        # ---- ③ 2週間〜1か月 ----
        chap("② 歯石ができる", se=SLASH),
        n("歯垢は数日〜2週間ほどで\nかたい歯石に", MOUTH, se=["rock_split"]),
        fx(h("いたい", "歯ブラシで\nこすっても\n取れない!?", SINK, red=True, se=["glass_break_01", BOOM]), "crack"),
        d("説明", "歯石は\n歯医者さんで\nしか取れない", CLINIC, se="kon"),
        # ---- ④ むし歯 ----
        chap("③ むし歯が進む", se=SLASH, bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        card("e03_mushiba", "むし歯の進み方（目安）", dur=4.6),
        n("最初は痛くないから\n気づきにくい", MOUTH, se="pi"),
        day("", 6, "か月", ROOM, "ポリポリ", se=GONG),
        fx(h("さけぶ", "アイスが\nしみる!!", SINK, red=True, se=["freeze_kochiin", BOOM]), "mono"),
        fx(h("いたい", "夜中に\nズキズキ激痛!!", ROOM, red=True, se=["explosion_dokaan", "hit_dogo_maou"]), "lines"),
        d("話す", "神経まで\n進んでいます", CHAIR, se="pc_warning"),
        h("おどろく", "え……\n歯って自然に\n治らないの？", CHAIR, se=POON),
        d("説明", "むし歯は\n自然には治りません", CHAIR, red=True, se=[GONG]),
        # ---- ⑤ 歯周病 ----
        chap("④ 歯周病", se=SLASH),
        day("", 5, "年", ROOM, "しょんぼり", se=BOOM),
        n("歯を支える骨が\n少しずつとけていく", MOUTH, se="shock_piano"),
        fx(h("いたい", "歯が\nぐらぐらする!?", SINK, red=True, se=["anime_conan_hirameki_remix_a"]), "swirl"),
        n("歯を失う原因のいちばんは\nむし歯ではなく歯周病", MOUTH, se=[CYM]),
        n("大人の多くが\n歯周病かその手前と言われる", CLINIC, se="pi"),
        d("説明", "糖尿病や心臓の病気との\n関係も指摘されて\nいるんです", CLINIC, se="kon"),
        # ---- ⑥ 10年 ----
        day("", 10, "年", ROOM, "なく", se=BOOM),
        fx(h("なく", "ついに\n歯が抜けた……", SINK, red=True, se=["chin_bell_failure_sad_ending"]), "mono"),
        h("考える", "抜けたら\nまた生えてくる？", CHAIR, se="question_hatena_maou"),
        fx(d("おこる", "大人の歯は\n二度と生えてきません!!", CHAIR, red=True, se=["explosion_dokaan", "glass_break_01"]), "crack"),
        n("ブリッジ・入れ歯\nインプラント", CHAIR, se=DRUM),
        fx(n("インプラントは保険がきかず\n1本 数十万円ほど", MONEY, who="おどろく",
             se=["drumroll", {"f": "explosion_bokaan", "at": 0.9}], dur=2.6), "money"),
        h("さけぶ", "数十万!?\n1本で!?", MONEY, red=True, se=["anime_conan_hirameki_remix_b"]),
        # ---- ⑦ 歯医者に行かないと ----
        chap("⑤ 歯医者に行かないと", se=SLASH, bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        n("早く行くほど\n治療は短く安くすむ", CLINIC, se=KIRA),
        n("進んでからだと\n根の治療で何度も通う", CLINIC, se="kon"),
        fx(h("しょんぼり", "え……\n通う回数がふえるの？", CHAIR, se="tv_professional_poon_remix_a"), "swirl"),
        d("笑顔", "痛くなる前の\n定期健診が\nいちばんラク", CLINIC, se=HEROSE),
        n("健診は\n3〜6か月に1回が目安", CLINIC, se=UP),
        # ---- ⑧ 今日からできること ----
        chap("⑥ 今日からできること", se=SLASH),
        n("寝る前の歯みがきは\nとくにていねいに", SINK, who="気づく", se=KIRA),
        n("歯と歯のすき間は\nフロスや歯間ブラシで", SINK, who="考える", se="pikon"),
        fx(h("よろこぶ", "今日から\nちゃんとみがく！", SINK, se=[UP, "cheer_applause"]), "lines"),
        n("「80歳で20本」\n自分の歯を残そう", SINK, who="よろこぶ", se=GONG),
        # ---- まとめ ----
        chap("まとめ", se=SLASH),
        card("e07_points", "今回のポイント", dur=4.4),
        two("よろこぶ", "笑顔", "痛くなる前に\nまた来てくださいね", CHAIR, who="R", se=["fanfare_pararappara"]),
        dict(bg=bg(SINK), card=pt("e10_ending"), dur=3.0, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def more(cuts):
    """多め：赤字の驚きにはドンを重ねる。エフェクトも1場面に2〜3個（エスコン・二郎系の動画と同じ）。"""
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
        if i % 4 == 2:
            fx_ += ["flash", "zoom"]
        if i % 5 == 1:
            fx_.append("lines")
        c["fx"] = list(dict.fromkeys(fx_))
    return cuts


def cuts_full():
    cs = more(K.hype(L.apply_fx(cuts_all())))
    for c in cs:   # テンポ優先：猫の音に合わせて場面をのばさない・素材を最後まで流さない
        if not c.get("notice") and not c.get("card"):
            c["fixed"] = True
        for k in c.get("cats", []):
            k.setdefault("full", False)
    return cs


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "33_ha_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cuts = cuts_full()
    if sys.argv[1:] == ["--len"]:
        print(len(cuts), round(sum(R.cut_dur(c) for c in cuts), 1))
        sys.exit()
    if len(sys.argv) > 1:
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=out.replace(".mp4", "_preview"))
