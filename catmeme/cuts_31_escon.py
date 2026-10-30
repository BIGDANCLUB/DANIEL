"""31_escon（札幌ドームの家賃が高すぎて、日本ハムがエスコンフィールドを建てて引っ越した話）のカット割り（10/30 ユーザー指定）。約3分。

python3 catmeme/cuts_31_escon.py → out/31_escon_full.mp4

10/30 ユーザー指定：8分ぶんの原稿量を、テンポよく3分ほどに凝縮。SE・演出は大盛り。
- 10/30 ユーザー指定：ニュース猫・博識な猫は出さない。ナレーションと登場する猫（道民ファンは架空）だけで進める。球団・ドーム・市は名札つきの猫（実在の人は出さない・名前も出さない）
- 演出・音のルールは車の動画と同じ（コナン＝「!?」・ポーン＝「え…」、連打は2回まで）

事実（報道・球団や市の発表より。金額はざっくりの目安）：
- 札幌ドームは札幌市が建てたドーム（2001年開業）。運営は市が出資する会社。日本ハムは2004年に東京から札幌へ移り、ここを本拠地に
- 球団が払う使用料・警備・清掃などは、年に20億円以上とも言われた。球場の看板広告や飲食の売上は、おもにドーム側の収入
- サッカーと共用。野球のときは人工芝。球団の思いどおりに球場を作りかえることはむずかしかった
- 球団は運営のしかたの見直しを求めたが、大きくは変わらなかった。2016年ごろ、自前の新球場をめざす構想が表に出る
- 候補地は札幌市内と北広島市。2018年に北広島市に決定。2020年に着工、総工費は約600億円
- 2023年3月「エスコンフィールドHOKKAIDO」開業。開け閉めできる屋根・天然芝・約3万5000席。温泉とサウナつきの観客席、
  ホテル、ビール工房つきのレストラン、子どもの遊び場。まわりを「ボールパーク」として町づくり
- 完成前、ホームからバックネットまでの距離が規則より短いと指摘されて話題に
- 札幌ドームは大きなお客さんを失い、赤字に（報道）。2024年から命名権で「大和ハウス プレミストドーム」に
- 北広島駅から歩いて約20分。球場の近くに新しい駅をつくる計画もある
原稿のルール：今日の一言・単語の途中で改行しない・最後はチャンネル登録・過去の動画にはふれない・どちらもけなさない
"""
import glob
import os
import sys

import cuts_04_leak as L
import cuts_26_kuruma as K
import render as R

R.TEMPO = 1.07
HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", "31_escon")] + sorted(
    d for d in glob.glob(os.path.join(HERE, "backgrounds", "*")) if os.path.isdir(d))
L.PT = os.path.join(HERE, "parts", "31_escon")
pt, cat, chap, fx, CONAN, POON = L.pt, L.cat, L.chap, K.fx, K.CONAN, K.POON
PURPLE, COCOA, MIRAI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.NORA

# 球団・ドーム・市は名札つきの猫（気持ちに合わせて素材を変える）
ORG = {
    "日本ハム": ((0, 60, 140), {"話す": "talk_orange_white_sitting_cat", "こまる": "despair_dramatic_kitten",
                             "決意": "stare_tabby_wide_eyes_cat", "計算": "money_counting_orange_cat", "よろこぶ": "happy_hamster_open_arms",
                             "おこる": "rage_talking_cat", "考える": "think_chin_paw_orange_cat"}),
    "札幌ドーム": ((100, 100, 110), {"余裕": "cocky_dj_cat", "知らんぷり": "slack_nail_filing_cat", "さみしい": "sad_banana_cat_cry",
                               "あせる": "scream_phone_orange_cat", "計算": "money_counting_orange_cat"}),
    "札幌市": ((0, 120, 60), {"話す": "stare_interviewer_cat", "考える": "think_bike_front_seat_cat", "こまる": "sad_looking_away_tabby",
                           "見送る": "wave_waving_cat"}),
    "北広島市": ((200, 90, 0), {"よろこぶ": "happy_chipi_chapa_cat", "やる気": "excited_hodomoe_city_cat",
                             "おどる": "dance_three_kittens", "手をあげる": "happy_hamster_open_arms"}),
}
for _n, (_c, _) in ORG.items():
    L.ROLE[_n] = _c

# 背景（ChatGPT で作る背景が届いたら backgrounds/31_escon に同じ名前で置けば差しかわる。指示文 scripts/31_escon_bg_prompts.md）
DOME, DOME_IN, CITY, LAND, BUILD, ESCON, PARK, ONSEN, MONEY, BOARD = (
    "bg31_sapporo_dome", "bg31_dome_inside", "bg31_city_meeting", "bg31_empty_land", "bg31_construction", "bg31_escon_outside",
    "bg31_escon_inside", "bg31_onsen_seats", "bg87_refund_money", "bg03_blackboard")
K.STANDIN.update({DOME: "bg63_hokkaido_field", DOME_IN: "bg43_award_stage", CITY: "bg05_meeting", LAND: "bg63_hokkaido_field",
                  BUILD: "bg26_rural_road", ESCON: "ph06_kumamoto_fields", PARK: "bg63_hokkaido_field", ONSEN: "bg100_lounge_night"})
bg = K.bg
# 10/30 ユーザー指定：ニュース猫・博識な猫は出さない。ナレーション（下の大きな字）と登場する猫だけで進める（大谷の動画と同じ）
NAR = (60, 830, 1860, 1070)
FAN = "道民ファン"   # 架空の北海道のファン（実在の人ではない）
L.ROLE[FAN] = (200, 30, 30)
FAN_LOOK = ["stare_big_eyes_tabby_kitten", "surprise_big_pupils_cat", "huh_huh_cat", "excited_hodomoe_city_cat", "glare_disgusted_cat",
            "stare_tabby_wide_eyes_cat"]
BACK = [("日本ハム", "考える"), ("札幌ドーム", "余裕"), ("日本ハム", "計算"), ("北広島市", "やる気"), ("札幌市", "考える"), ("日本ハム", "決意")]
_k = {"fan": 0, "back": 0}


def n(text, b, who=None, **kw):
    """ナレーション：画面の下に白い大きな字。後ろに登場する猫を小さめに（声は出さない）。"""
    if who is None:
        who = [BACK[_k["back"] % len(BACK)]]
        _k["back"] += 1
    xs = {1: (960,), 2: (560, 1360)}.get(len(who), ())
    cats = [cat(ORG[w][1][lk], w, x, h=560, bottom=790, label_size=50, mute=True, float=True) for (w, lk), x in zip(who, xs)]
    return dict(bg=bg(b), cats=cats, sub=text, sub_box=NAR, sub_size=110, keep_overlap=True, se=kw.pop("se", "page_turn_01"), **kw)


def fan(say, b, red=False, **kw):
    """道民ファンの猫がおどろく・つっこむ（まん中に大きく1匹）。"""
    a = FAN_LOOK[_k["fan"] % len(FAN_LOOK)]
    _k["fan"] += 1
    c = dict(bg=bg(b), cats=[cat(a, FAN, 960, h=780, bottom=1075, label_size=60)], say=say, text_top=True, keep_overlap=True, **kw)
    if red:
        c.update(say_style="red", fx=["shake", "lines"])
    return c


def ss(say, b, **kw):
    return n(say, b, **kw)


def nn(say, b, red=False, **kw):
    return fan(say, b, red=red, **kw)


def boom(say, b, se=None, **kw):
    return fan(say, b, red=True, se=se or ["explosion_chudoon"], **kw)

# 10/30 ユーザー指定「SE・演出は大盛り」：場面の頭の派手な音（どれも配布サイトの音）
BOOM, GONG, SLASH, DRUM, CYM, DASH, KIRA, HERO, UP = ("explosion_dokaan", "gong_dora_jaan", "sword_shakiin", "taiko_dodon_01",
                                                      "cymbal_maou", "dash_super_fast", "shine_kiraan_maou", "hero_pose", "power_up")


def o(who, look, say, b, red=False, **kw):
    """球団・ドーム・市の猫がしゃべる（まん中に大きく1匹・名札・上に字幕）。"""
    c = dict(bg=bg(b), cats=[cat(ORG[who][1][look], who, 960, h=780, bottom=1075, label_size=60)], say=say, text_top=True,
             keep_overlap=True, **kw)
    if red:
        c.update(say_style="red", fx=["shake", "lines"])
    return c


def vs(lw, ll, rw, rl, say, b, who="L", **kw):
    """2つの組織が向かい合う（しゃべる方だけ鳴らす）。"""
    cats = [cat(ORG[lw][1][ll], lw, 470, h=740, bottom=1075, label_size=56, mute=who != "L"),
            cat(ORG[rw][1][rl], rw, 1450, h=740, bottom=1075, label_size=56, mute=who != "R")]
    return dict(bg=bg(b), cats=cats, say=say, text_top=True, keep_overlap=True, **kw)


def sp(say, who="L", side=None, red=False, **kw):
    """画面半分：左＝札幌ドーム・右＝エスコン。しゃべる側の上に字幕。side は左右の短い言葉。"""
    big, small = (700, 600) if not side else (600, 520)
    cats = [cat(ORG["札幌ドーム"][1]["余裕"], "札幌ドーム", 480, h=big if who == "L" else small, bottom=1075, label_size=54, mute=who != "L"),
            cat(ORG["日本ハム"][1]["よろこぶ"], "日本ハム", 1440, h=big if who == "R" else small, bottom=1075, label_size=54, mute=who != "R")]
    out = dict(bg=bg(DOME_IN), bg2=bg(PARK), split=("札幌ドーム", "エスコン"), split_cols=((90, 90, 100), (0, 60, 140)), split_y=232,
               split_tint=0.1, split_size=58, cats=cats, say=say,
               text_box=(30, 10, 930, 225) if who == "L" else (990, 10, 1890, 225), say_size=100, keep_overlap=True,
               side_text=side, **kw)
    if red:
        out.update(say_style="red", fx=["shake"])
    return out


def card(c, sub, **kw):
    return L.dia(c, sub, BOARD, dur=kw.pop("dur", 4.4), se=kw.pop("se", "card_flip"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(bg=bg(ESCON), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in (
                ("dance_filmed_by_gray_cat", 300, 560), ("dance_three_kittens", 800, 520), ("happy_hamster_open_arms", 1240, 560),
                ("dance_happy_banana_cat", 1660, 600))],
             fx=["dim"], layers_top=[pt("e00_notice")], dur=5.0, no_pop=True, notice=True,
             se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- つかみ ----
        nn("プロ野球の球団が\n球場ごと引っ越した!?", ESCON, red=True, se=[CONAN], bgm={"file": PURPLE, "gain": -4}),
        ss("北海道の日本ハム\n札幌ドームを出て\n自分で球場を建てたんだ", ESCON, se=BOOM),
        nn("なんでわざわざ\n出ていったの？", DOME, se="question_hatena_maou"),
        fx(ss("いちばんの理由は\nお金", MONEY, se=["drumroll", {"f": "explosion_bokaan", "at": 0.9}], dur=2.2),
           slot=("年 ", 20, "億円以上")),
        boom("使うだけで\n年20億円以上!?", MONEY, se=["explosion_dokaan", "glass_break_01"]),
        dict(bg=bg(ESCON), card=pt("e01_title"), dur=3.4, se=GONG,
             cats=[{"a": "happy_chipi_chapa_cat", "x": 300, "h": 440, "bottom": 1050, "float": True, "mute": True}]),
        # ---- ① 札幌ドームへ ----
        chap("① 北海道にやってきた", se=SLASH, bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        ss("日本ハムは\nもともと東京の球団", DOME, se=DASH),
        ss("2004年に\n北海道の札幌へ\n引っ越してきた", DOME, se=UP),
        o("日本ハム", "決意", "北海道の球団として\nがんばります！", DOME, se=HERO),
        ss("本拠地は\n札幌ドーム", DOME, se=KIRA),
        o("札幌ドーム", "余裕", "札幌市が建てた\n大きなドームです", DOME_IN, se=CYM),
        nn("じゃあ日本ハムは\n借りて使ってたの？", DOME_IN, se="question_hatena_maou"),
        ss("いわば家賃をはらう\n「借りぐらし」", DOME_IN, se="kon"),
        ss("人気も出て\n2006年と2016年には\n日本一にも", DOME_IN, se=["cheer_applause", BOOM]),
        # ---- ② 高すぎる家賃 ----
        chap("② 高すぎる家賃", se=SLASH, bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        o("日本ハム", "計算", "使用料に\n警備に清掃……", MONEY, se="price_display"),
        fx(o("日本ハム", "こまる", "ぜんぶで\n年20億円以上!?", MONEY, red=True, se=["explosion_dokaan"]), "money"),
        nn("家賃20億って\nどういう世界!?", MONEY, red=True, se=["anime_conan_hirameki_remix_a"]),
        ss("しかも球場の看板や\n飲食の売上は\nおもにドーム側の収入", DOME_IN, se=DRUM),
        o("札幌ドーム", "計算", "看板とお弁当の\nお金は\nこちらに", DOME_IN, se="price_display"),
        fx(nn("え……\nお客さんを呼んでも\n球団はもうからない？", DOME_IN, se=POON), "mono"),
        ss("サッカーと共用だから\n野球のときは人工芝", DOME_IN, se="pi"),
        ss("球団の思いどおりに\n作りかえるのも\nむずかしかった", DOME_IN, se="kon"),
        # ---- ③ 交渉 ----
        chap("③ 話し合いは平行線", se=SLASH),
        vs("日本ハム", "話す", "札幌市", "考える", "運営を\n球団にまかせて\nもらえませんか", CITY, who="L", se="pikon"),
        vs("日本ハム", "考える", "札幌市", "こまる", "うーん……\n大きくは\n変えられない", CITY, who="R", se="deflate_hyororo"),
        fx(sp("球団が使うのに\n自由がきかない", "L", side=("借りもの", "自分の物"), se="pi"), "swirl"),
        o("日本ハム", "おこる", "それなら\n自分たちで\n球場を建てる！", CITY, red=True, se=["explosion_bokaan", "rock_split"]),
        boom("球場を\n自分で建てる!?", CITY, se=["explosion_dokaan", "air_horn"]),
        ss("2016年ごろ\n新しい球場の計画が\n表に出た", CITY, se=GONG),
        # ---- ④ 引っ越し先 ----
        chap("④ 引っ越し先はどこ？", se=SLASH, bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        ss("候補は\n札幌市の中と\nとなりの北広島市", LAND, se=DRUM),
        o("北広島市", "手をあげる", "ぜひうちに\n来てください！", LAND, se=UP),
        nn("北広島市って\nどんな所？", LAND, se="question_hatena_maou"),
        ss("札幌のとなりの\n人口5万人ほどの町\n空港にも近い", LAND, se="pi"),
        fx(ss("2018年\n北広島市に決定", LAND, se=["drumroll", {"f": GONG, "at": 0.9}], dur=2.4), "mono"),
        o("北広島市", "おどる", "やったー！", LAND, se=["cheer_applause", "fanfare_pararappara"]),
        o("札幌市", "見送る", "……\n行ってしまうのか", CITY, se="chin_bell_failure_sad_ending"),
        # ---- ⑤ 600億円の球場 ----
        chap("⑤ 600億円の球場", se=SLASH),
        ss("2020年に\n工事がスタート", BUILD, se="hit_dogo_maou"),
        fx(ss("かかったお金は", BUILD, se=["drumroll", {"f": "explosion_bokaan", "at": 0.9}], dur=2.2), slot=("約", 600, "億円")),
        nn("600億!?\n球団が自分で!?", BUILD, red=True, se=["anime_conan_hirameki_remix_b"]),
        ss("球団の会社が建てて\n自分たちで持つ", BUILD, se="kon"),
        ss("家賃をはらうのではなく\nもうけは自分たちに", MONEY, se="price_display"),
        fx(o("日本ハム", "計算", "看板も飲食も\nこれからは\nうちの収入", MONEY, se=["price_display", KIRA]), "money"),
        # ---- ⑥ エスコン誕生 ----
        chap("⑥ エスコン誕生", se=SLASH, bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        ss("2023年3月\nエスコンフィールド\nHOKKAIDO 開業", ESCON, se=["fanfare_pararappara", BOOM]),
        card("e02_compare", "ドームとエスコンのちがい", dur=4.2),
        fx(sp("屋根は\n開け閉めできる", "R", side=("閉じたまま", "開け閉め"), se=["sword_shakiin"]), "lines"),
        sp("芝は\n本物の天然芝", "R", side=("人工芝", "天然芝"), se=KIRA),
        o("日本ハム", "よろこぶ", "外野の向こうには\n温泉とサウナ!!", ONSEN, red=True, se=["explosion_bokaan", "shine_kira_01"]),
        boom("球場で\n温泉!?", ONSEN, se=["explosion_dokaan", "cymbal_maou"]),
        ss("ホテルに\nビール工房のレストラン\n子どもの遊び場まで", PARK, se=HERO),
        ss("野球がない日も\n人が集まる\n「ボールパーク」", PARK, se=UP),
        # ---- ⑦ ハプニング ----
        chap("⑦ ハプニングも", se=SLASH),
        ss("完成前\nホームからネットまでの\n距離が規則より短いと\n指摘された", PARK, se="pc_warning"),
        fx(nn("え……\n600億の球場で\nサイズちがい？", PARK, se="tv_professional_poon_remix_a"), "crack"),
        ss("話し合いのうえ\nそのまま開業して\n話題になった", PARK, se="kon"),
        ss("駅から歩いて\n約20分と少し遠い", ESCON, se="pi"),
        ss("近くに新しい駅を\nつくる計画もある", ESCON, se=DASH),
        # ---- ⑧ 残された札幌ドーム ----
        chap("⑧ 残された札幌ドーム", se=SLASH, bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        o("札幌ドーム", "あせる", "いちばんの\nお客さんが\nいなくなった……", DOME, red=True, se=["explosion_dokaan", "glass_break_01"]),
        ss("イベントがへって\n赤字になったと\n報道された", DOME, se="shock_piano"),
        fx(ss("2024年からは\n名前を売る\n命名権も", DOME, se=GONG), "swirl"),
        o("札幌ドーム", "さみしい", "コンサートや\nサッカーで\nがんばります", DOME_IN, se="deflate_hyororo"),
        # ---- まとめ ----
        chap("まとめ", se=SLASH, bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        card("e07_points", "今回のポイント", dur=4.4),
        nn("借りるより\n自分で建てたほうが\nいいこともあるんだね", ESCON, se="pikon"),
        ss("ただし600億円の\n大きな勝負", ESCON, se=DRUM),
        o("日本ハム", "決意", "北海道で\nずっと愛される\n球場に！", PARK, se=["cheer_applause", HERO]),
        dict(bg=bg(ESCON), card=pt("e10_ending"), dur=3.0, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


EXTRA_FX = {}   # 場面ごとの追加演出（cuts_all の fx で指定）


def more(cuts):
    """大盛り：どの場面も頭の音に加えて、赤字の驚きにはドン・字幕が出た所にポン。エフェクトも1場面に2〜3個。"""
    for i, c in enumerate(cuts):
        if c.get("notice") or c.get("chapter") or c.get("card") or c.get("inset"):
            continue
        names = [x if isinstance(x, str) else x.get("f", "") for x in (c.get("se") or [])]
        if any("conan" in n_ or "poon" in n_ for n_ in names):
            continue
        lst = list(c.get("se") or [])
        if c.get("side_text"):
            lst.append({"f": "kaan", "gain": -3, "at": 0.03})
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
    cs = more(K.hype(L.apply_fx(L.allocate(cuts_all(), max_use=7, gap=1))))
    for c in cs:   # テンポ優先：猫の音に合わせて場面をのばさない・素材を最後まで流さない（大谷の動画と同じ）
        if not c.get("notice") and not c.get("card"):
            c["fixed"] = True
        for k in c.get("cats", []):
            k.setdefault("full", False)
    return cs


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "31_escon_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cuts = cuts_full()
    if sys.argv[1:] == ["--len"]:
        print(len(cuts), round(sum(R.cut_dur(c) for c in cuts), 1))
        sys.exit()
    if len(sys.argv) > 1:
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=out.replace(".mp4", "_preview"))
