"""30_ohtani（大谷翔平 メジャー直行宣言から日本ハム入団まで）のカット割り（10/30 ユーザー指定）。約3分。

python3 catmeme/cuts_30_ohtani.py → out/30_ohtani_full.mp4

10/30 ユーザー指定：
- いつもの2匹（ニュース猫・博識な猫）は使わない。登場人物とナレーションだけで進める
- 実在の人の扱い：今回だけ例外で、名前を出し、名札つきの猫で演じる（ユーザーが選んだ）。からかう表現はしない
- 演出・音のルールは車の動画と同じ（コナン＝「!?」・ポーン＝「え…」、連打は2回まで。集中線は控えめ）

事実（報道・球団の発表より・2012年）：
- 花巻東高校3年。2012年7月、夏の岩手大会準決勝で高校生史上初の160km/h
- 10月21日 記者会見で「日本のプロ野球を経ずにメジャーリーグに挑戦したい」と表明
- 多くの球団が指名を見送る中、10月25日のドラフト会議で日本ハムが単独で1位指名
- 本人は「アメリカでやりたい気持ちは変わらない」
- 日本ハムは資料「大谷翔平君 夢への道しるべ ～日本スポーツにおける若年期海外進出の考察～」を用意し、
  高校から直接海外に行った選手の例やデータを示した。さらに投手と打者の「二刀流」で育てるプランを提案
- 交渉は栗山英樹監督・山田正雄GMらが担当。12月9日に入団を表明、12月25日に入団会見。背番号は11
- その後 2018年にメジャーへ。二刀流で活躍し、MVPを何度も受賞
原稿のルール：今日の一言・単語の途中で改行しない・最後はチャンネル登録・過去の動画にはふれない
"""
import glob
import os
import sys

import cuts_04_leak as L
import cuts_26_kuruma as K
import render as R

R.TEMPO = 0.98   # 10/30 ユーザー指定：内容をふやしてテンポを上げる（6分を3分に濃縮するイメージ）
HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", "30_ohtani")] + sorted(
    d for d in glob.glob(os.path.join(HERE, "backgrounds", "*")) if os.path.isdir(d))
L.PT = os.path.join(HERE, "parts", "30_ohtani")
pt, chap = L.pt, L.chap
PURPLE, COCOA, MIRAI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.NORA
CONAN, POON = K.CONAN, K.POON

# 登場人物（名札つきの猫）。10/30 ユーザー指定「単一の素材ではなく色々な素材で」：名札は同じで、場面ごとに素材を変える
# 呼び方："大谷翔平" はいつもの素材、"大谷翔平@打つ" のように @ のあとで素材を選ぶ
CAST = {
    "大谷翔平": ("talk_orange_white_sitting_cat", (200, 30, 30)),
    "栗山監督": ("think_chin_paw_orange_cat", (20, 60, 140)),
    "山田GM": ("read_book_orange_kitten", (20, 60, 140)),
    "佐々木監督": ("stare_interviewer_cat", (0, 120, 60)),
    "メジャー球団": ("cocky_dj_cat", (90, 60, 150)),
    "ほかの球団": ("sleepy_sleepy_cat", (100, 100, 100)),
    "記者たち": ("scream_phone_orange_cat", (60, 60, 60)),
}
LOOK = {   # 同じ人の別の素材（気持ち・動きに合わせる）
    "大谷翔平": {"話す": "talk_orange_white_sitting_cat", "おさない": "stare_big_eyes_tabby_kitten", "やる気": "excited_hodomoe_city_cat",
               "打つ": "mock_swinging_cat", "投げる": "punch_boxing_white_cat", "考える": "realize_wet_cat_stare",
               "おどろく": "surprise_big_pupils_cat", "書く": "work_typing_cat", "くやしい": "sad_looking_away_tabby",
               "よろこぶ": "happy_hamster_open_arms", "走る": "dance_white_dog", "決意": "stare_tabby_wide_eyes_cat",
               "ひろう": "ignore_orange_cat_sniffed"},
    "栗山監督": {"考える": "think_chin_paw_orange_cat", "話す": "talk_orange_white_sitting_cat", "熱い": "rage_talking_cat",
               "こまる": "despair_dramatic_kitten", "よろこぶ": "happy_chipi_chapa_cat"},
    "山田GM": {"読む": "read_book_orange_kitten", "宣言": "yell_orange_fat_cat", "計算": "money_counting_orange_cat",
              "見せる": "work_typing_cat"},
    "佐々木監督": {"見る": "stare_interviewer_cat", "おどろく": "stare_tabby_wide_eyes_cat"},
    "メジャー球団": {"余裕": "cocky_dj_cat", "ほれる": "rizz_cat_rizz", "見せびらかす": "showoff_gojo_cosplay_cat",
                "おどろく": "surprise_big_pupils_cat"},
    "ほかの球団": {"ねむい": "sleepy_sleepy_cat", "知らんぷり": "slack_nail_filing_cat", "目をそらす": "ignore_orange_cat_sniffed",
              "むり": "glare_disgusted_cat"},
    "記者たち": {"さけぶ": "scream_phone_orange_cat", "かたまる": "stare_tabby_wide_eyes_cat", "おどろく": "surprise_big_pupils_cat",
             "メモ": "work_typing_cat"},
}
for _n, (_a, _c) in CAST.items():
    L.ROLE[_n] = _c


def who_(w):
    """"大谷翔平@打つ" → (素材, "大谷翔平")"""
    name, _, look = w.partition("@")
    return (LOOK[name][look] if look else CAST[name][0]), name


# 背景（ChatGPT で作る背景が届いたら backgrounds/30_ohtani に同じ名前で置けば差しかわる）
HS, KOSHIEN, PRESS, DRAFT, NEGO, DOME, US = ("bg30_hs_ground", "bg30_summer_stadium", "bg30_press_room", "bg30_draft_hall",
                                            "bg30_negotiation_room", "bg30_hokkaido_ballpark", "bg30_us_ballpark")
K.STANDIN.update({HS: "bg21_school_gate", KOSHIEN: "bg43_award_stage", PRESS: "bg07_press", DRAFT: "bg43_award_stage",
                  NEGO: "bg05_meeting", DOME: "bg63_hokkaido_field", US: "bg28_ny_street"})
bg, fx = K.bg, K.fx
NAR = (60, 800, 1860, 1065)


def p(who, say, b, red=False, **kw):
    """登場人物がしゃべる（まん中に大きく1匹・名札・上に字幕）。"""
    a, name = who_(who)
    c = dict(bg=bg(b), cats=[L.cat(a, name, 960, h=760, bottom=1075, label_size=60)], say=say, text_top=True, keep_overlap=True, **kw)
    if red:
        c.update(say_style="red", fx=["shake"] + list(kw.get("fx", [])))
    return c


def two(left, right, say, b, who="L", **kw):
    """2人の場面（左右に大きく・しゃべる方だけ鳴らす）。"""
    (la, ln), (ra, rn) = who_(left), who_(right)
    cats = [L.cat(la, ln, 470, h=740, bottom=1075, label_size=56, mute=who != "L"),
            L.cat(ra, rn, 1450, h=740, bottom=1075, label_size=56, mute=who != "R")]
    return dict(bg=bg(b), cats=cats, say=say, text_top=True, keep_overlap=True, **kw)


def crowd(who, say, b, looks, red=False, **kw):
    """同じ役の猫を3匹ならべる（記者たち・ほかの球団など）。まん中だけ鳴らす。"""
    cats = [L.cat(LOOK[who][lk], who, x, h=600, bottom=1075, label_size=48, mute=k != 1)
            for k, (lk, x) in enumerate(zip(looks, (380, 960, 1540)))]
    c = dict(bg=bg(b), cats=cats, say=say, text_top=True, keep_overlap=True, **kw)
    if red:
        c.update(say_style="red", fx=["shake"])
    return c


def n(text, b, who=None, **kw):
    """ナレーション：画面の下に白い大きな字。登場人物は小さめに後ろで（声は出さない）。"""
    who = who or []
    xs = {1: (960,), 2: (560, 1360), 3: (420, 960, 1500)}.get(len(who), ())
    cats = [L.cat(*who_(w), x, h=560, bottom=790, label_size=50, mute=True, float=True) for w, x in zip(who, xs)]
    return dict(bg=bg(b), cats=cats, sub=text, sub_box=NAR, sub_size=84, keep_overlap=True, se=kw.pop("se", "page_turn_01"), **kw)


# 10/30 ユーザー指定「SEも派手なのを」：場面の頭の音（どれも配布サイトの音）
BOOM, GONG, SLASH, DRUM, CYM, DASH, KIRA = "explosion_dokaan", "gong_dora_jaan", "sword_shakiin", "taiko_dodon_01", "cymbal_maou", \
    "dash_super_fast", "shine_kiraan_maou"


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(bg=bg(DOME), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in (
                ("dance_tabby_standing_cat", 260, 600), ("dance_three_kittens", 700, 520), ("happy_hamster_open_arms", 1180, 560),
                ("dance_happy_banana_cat", 1640, 600))],
             fx=["dim"], layers_top=[pt("e00_notice")], dur=5.0, no_pop=True, notice=True,
             se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- つかみ ----
        n("2012年10月\n18歳の高校生の言葉に\n日本中がおどろいた", PRESS, ["大谷翔平@決意"], se=BOOM, bgm={"file": PURPLE, "gain": -4}),
        p("大谷翔平", "日本のプロ野球には行かず\nメジャーリーグに\n挑戦したいです", PRESS, se="pinpon_notice"),
        crowd("記者たち", "高校から\nいきなりメジャー!?", PRESS, ("かたまる", "さけぶ", "おどろく"), red=True, se=CONAN),
        n("ところが4日後\nある球団が\nとんでもない行動に出る", DRAFT, ["栗山監督@熱い"], se="doon_heavy"),
        dict(bg=bg(DOME), card=pt("e01_title"), dur=3.4, se=GONG,
             cats=[{"a": LOOK["大谷翔平"]["打つ"], "x": 300, "h": 440, "bottom": 1050, "float": True, "mute": True}]),
        # ---- ① 岩手の少年 ----
        chap("① 岩手の野球少年", se=SLASH, bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        n("1994年\n岩手県の奥州市に生まれる", HS, ["大谷翔平@おさない"], se=KIRA),
        n("父は社会人野球の選手\n母はバドミントンの選手\nスポーツ一家だった", HS, ["大谷翔平@おさない"]),
        n("高校は花巻東へ\n先輩には\nあの菊池雄星", HS, ["大谷翔平@やる気"], se=DASH),
        n("1年生のとき\n81マスの「目標シート」を書いた\nまん中の目標は……", HS, ["大谷翔平@書く"], se="card_place"),
        fx(p("大谷翔平@やる気", None, HS, se=["drumroll", {"f": "explosion_bokaan", "at": 0.9}], dur=2.2),
           slot=("ドラ1 ", 8, "球団")),   # 8球団から1位指名されたい（スロットで回って止まる）
        n("「運」のマスには\nゴミ拾い・あいさつ\n部屋のそうじ", HS, ["大谷翔平@ひろう"], se="sparkle_kirakira_01"),
        # ---- ② 160キロ ----
        chap("② 160キロの高校生", se=SLASH),
        n("2012年の春\nセンバツで甲子園へ", KOSHIEN, ["大谷翔平@やる気"], se=DRUM),
        n("相手は大阪桐蔭\nエースは藤浪晋太郎", KOSHIEN, ["大谷翔平@決意"], se="gong_match_start"),
        fx(p("大谷翔平@打つ", "藤浪から\nホームラン!!", KOSHIEN, red=True, se=["kaan", BOOM]), "lines"),
        n("でも試合は\n2対9で負けてしまった", KOSHIEN, ["大谷翔平@くやしい"], se="deflate_hyororo"),
        n("2012年7月\n夏の岩手大会\n準決勝", KOSHIEN, ["大谷翔平@投げる"], se=DRUM),
        fx(p("佐々木監督@おどろく", "160キロ!?\n高校生で初めてだ", KOSHIEN, red=True, se=["explosion_dokaan", "glass_break_01"]), "crack"),
        n("ところが決勝で負けて\n最後の夏の甲子園には\n行けなかった", KOSHIEN, ["大谷翔平@くやしい"], se="shock_piano"),
        n("9月には\n18歳以下の世界大会に\n日本代表で出場", US, ["大谷翔平@投げる"], se=DASH),
        crowd("メジャー球団", "すごい高校生がいる\nぜひうちに来てほしい", US, ("余裕", "ほれる", "見せびらかす"), se="hero_pose"),
        n("アメリカの球団の\nスカウトたちが\n何度も見に来ていた", US, ["メジャー球団@ほれる"]),
        # ---- ③ メジャー直行宣言 ----
        chap("③ メジャー直行宣言", se=SLASH, bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        n("10月21日\n大谷は記者会見を開く", PRESS, ["大谷翔平@決意"], se="doon_movie"),
        p("大谷翔平@決意", "若いうちから\n世界のいちばん上で\n勝負したい", PRESS, se="power_up"),
        n("高校から直接メジャーへ\n当時の日本では\nほとんど例がなかった", PRESS, ["大谷翔平"]),
        crowd("ほかの球団", "本人がそう言うなら\n指名はやめておこう……", DRAFT, ("ねむい", "知らんぷり", "目をそらす"), se="deflate_hyororo"),
        n("多くの球団が\n指名を見送る流れに", DRAFT, ["ほかの球団@目をそらす"]),
        # ---- ④ 強行指名 ----
        chap("④ まさかの強行指名", se=SLASH),
        n("10月25日\nドラフト会議", DRAFT, ["栗山監督", "山田GM"], se=DRUM),
        fx(p("山田GM@宣言", "北海道日本ハム\n1位指名\n大谷翔平", DRAFT, se=["hyoshigi_01", GONG]), "mono"),
        dict(qmarks=6, **crowd("記者たち", None, DRAFT, ("かたまる", "さけぶ", "おどろく"), se=["anime_conan_hirameki_remix_a"],
                               fx=["flash", "ring"], dur=2.0, no_pop=True)),   # コナン連打＋特大の「？」
        crowd("記者たち", "メジャーに行くって\n言ってるのに\n指名した……", DRAFT, ("メモ", "さけぶ", "かたまる"), red=True,
              se=["explosion_chudoon"]),
        n("1位指名は日本ハムだけ\nまさかの単独指名", DRAFT, ["山田GM@計算"], se=CYM),
        p("栗山監督@熱い", "その年いちばんの選手を\n指名するのが\nうちのやり方だ", DRAFT, se="air_horn"),
        p("大谷翔平@決意", "アメリカでやりたい\n気持ちは\n変わりません", PRESS, se="kon"),
        p("栗山監督@こまる", "え……\nこのままじゃ\n入ってもらえない", NEGO, se=POON),
        # ---- ⑤ 夢への道しるべ ----
        chap("⑤ 夢への道しるべ", se=SLASH, bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        n("日本ハムは\n1冊の資料を用意した", NEGO, ["山田GM@見せる"], se="page_turn_02"),
        p("山田GM@読む", "「大谷翔平君\n夢への道しるべ」", NEGO, se=["card_flip", KIRA]),
        n("高校から直接\n海外に行った選手たちが\nどうなったかをデータで示した", NEGO, ["山田GM@見せる", "大谷翔平@考える"]),
        n("メジャーで活躍できた選手は\nほんのひとにぎり\nきびしい現実だった", NEGO, ["大谷翔平@考える"], se="shock_piano"),
        two("山田GM@読む", "大谷翔平@考える", "まず日本で力をつけてから\nメジャーに行くほうが\n夢に近づけるかもしれない", NEGO,
            who="L", se="kon"),
        p("大谷翔平@考える", "え……\nそんな考え方も\nあるのか", NEGO, se="tv_professional_poon_remix_a"),
        # ---- ⑥ 二刀流 ----
        chap("⑥ 二刀流という提案", se=SLASH),
        two("栗山監督@熱い", "大谷翔平", "ピッチャーもバッターも\n両方やってみないか", NEGO, who="L", se="power_up"),
        p("大谷翔平@おどろく", "両方!?\nプロで!?", NEGO, red=True, se=["anime_conan_hirameki_remix_b"]),
        n("プロで投げて打つ選手は\nほとんどいなかった\n前代未聞の提案", NEGO, ["栗山監督@熱い"], se=BOOM),
        crowd("ほかの球団", "え……\nプロで二刀流なんて\n無理でしょ", DRAFT, ("むり", "ねむい", "知らんぷり"), se="tv_professional_poon_remix_b"),
        p("栗山監督@熱い", "誰もやったことがないなら\nやってみればいい", NEGO, se=["hero_pose"]),
        # ---- ⑦ 決断 ----
        chap("⑦ 決断", se=SLASH, bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        n("何度も話し合いを重ねて\n12月9日", PRESS, ["大谷翔平@考える", "栗山監督"], se=DRUM),
        fx(p("大谷翔平@よろこぶ", "日本ハムに\nお世話になります", PRESS, se=["fanfare_pararappara", "cheer_applause"]), "money"),
        n("12月25日 入団会見\n背番号は11", DOME, ["大谷翔平@よろこぶ", "栗山監督@よろこぶ"], se=GONG),
        n("11はダルビッシュ有が\nつけていた番号", DOME, ["大谷翔平@決意"], se=KIRA),
        two("栗山監督@よろこぶ", "大谷翔平@やる気", "二刀流で\n日本一の選手になろう", DOME, who="L", se="power_up"),
        # ---- ⑧ その後 ----
        chap("⑧ その後", se=SLASH),
        n("2014年\n11勝と10本塁打\n日本のプロ野球で初めて", DOME, ["大谷翔平@投げる", "大谷翔平@打つ"], se=BOOM),
        fx(p("大谷翔平@投げる", None, DOME, se=["drumroll", {"f": "explosion_dokaan", "at": 0.9}], dur=2.2), slot=("2016年 ", 165, "キロ")),
        n("日本最速の165キロ\nチームは日本一\n大谷はリーグMVP", DOME, ["大谷翔平@よろこぶ"], se=["fanfare_pararappara"]),
        n("2018年\n約束どおりメジャーへ", US, ["大谷翔平@走る"], se=DASH),
        crowd("メジャー球団", "投げて打つ!?\nこんな選手は\n見たことがない", US, ("おどろく", "余裕", "ほれる"), red=True, se=[CONAN]),
        n("1年目で新人王\n2021年にはMVP", US, ["大谷翔平@打つ"], se=CYM),
        n("2023年\nWBCで世界一\n大会MVPにも", US, ["大谷翔平@よろこぶ"], se=["cheer_applause", BOOM]),
        fx(n("2024年 ドジャースで\n50本塁打・50盗塁\nチームは世界一", US, ["大谷翔平@打つ", "大谷翔平@走る"], se=["explosion_dokaan", "bravo_applause"]),
           "money"),
        n("二刀流でMVPを何度も受賞\n世界一の野球選手と\n呼ばれるように", US, ["大谷翔平@決意"], se=KIRA),
        # ---- まとめ ----
        chap("まとめ", se=SLASH),
        n("夢をあきらめたのではなく\n夢への道を\nいっしょに考えた", NEGO, ["栗山監督", "大谷翔平@考える"], se="sparkle_kirakira_01"),
        n("あの強行指名がなければ\n今の二刀流は\nなかったかもしれない", DOME, ["大谷翔平@決意"], se=GONG),
        dict(bg=bg(DOME), card=pt("e10_ending"), dur=3.0, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    cs = K.hype(L.apply_fx(cuts_all()))
    for c in cs:   # 10/30 ユーザー指定「テンポを上げて」：猫の音に合わせて場面をのばさない・素材を最後まで流さない
        if not c.get("notice") and not c.get("card"):
            c["fixed"] = True
        for k in c.get("cats", []):
            k.setdefault("full", False)
    return cs


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "30_ohtani_full.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cuts = cuts_full()
    if sys.argv[1:] == ["--len"]:
        print(len(cuts), round(sum(R.cut_dur(c) for c in cuts), 1))
        sys.exit()
    if len(sys.argv) > 1:
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=out.replace(".mp4", "_preview"))
