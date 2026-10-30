"""30_ohtani（大谷翔平 メジャー直行宣言から日本ハム入団まで）のカット割り（10/30 ユーザー指定）。3分半ほど。

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

R.TEMPO = 1.15
HERE = L.HERE
L.BGS = [os.path.join(HERE, "backgrounds", "30_ohtani")] + sorted(
    d for d in glob.glob(os.path.join(HERE, "backgrounds", "*")) if os.path.isdir(d))
L.PT = os.path.join(HERE, "parts", "30_ohtani")
pt, chap = L.pt, L.chap
PURPLE, COCOA, MIRAI, NORA = L.PURPLE, L.COCOA, L.MIRAI, L.NORA
CONAN, POON = K.CONAN, K.POON

# 登場人物（名札つきの猫・いつも同じ素材）
CAST = {
    "大谷翔平": ("talk_orange_white_sitting_cat", (200, 30, 30)),
    "栗山監督": ("think_chin_paw_orange_cat", (20, 60, 140)),
    "山田GM": ("read_book_orange_kitten", (20, 60, 140)),
    "佐々木監督": ("stare_interviewer_cat", (0, 120, 60)),
    "メジャー球団": ("cocky_dj_cat", (90, 60, 150)),
    "ほかの球団": ("sleepy_sleepy_cat", (100, 100, 100)),
    "記者たち": ("scream_phone_orange_cat", (60, 60, 60)),
}
for _n, (_a, _c) in CAST.items():
    L.ROLE[_n] = _c

# 背景（ChatGPT で作る背景が届いたら backgrounds/30_ohtani に同じ名前で置けば差しかわる）
HS, KOSHIEN, PRESS, DRAFT, NEGO, DOME, US = ("bg30_hs_ground", "bg30_summer_stadium", "bg30_press_room", "bg30_draft_hall",
                                            "bg30_negotiation_room", "bg30_hokkaido_ballpark", "bg30_us_ballpark")
K.STANDIN.update({HS: "bg21_school_gate", KOSHIEN: "bg43_award_stage", PRESS: "bg07_press", DRAFT: "bg43_award_stage",
                  NEGO: "bg05_meeting", DOME: "bg63_hokkaido_field", US: "bg28_ny_street"})
bg, fx = K.bg, K.fx
NAR = (60, 800, 1860, 1065)


def p(who, say, b, red=False, **kw):
    """登場人物がしゃべる（まん中に大きく1匹・名札・上に字幕）。"""
    a, _ = CAST[who]
    c = dict(bg=bg(b), cats=[L.cat(a, who, 960, h=760, bottom=1075, label_size=60)], say=say, text_top=True, keep_overlap=True, **kw)
    if red:
        c.update(say_style="red", fx=["shake"])
    return c


def two(left, right, say, b, who="L", **kw):
    """2人の場面（左右に大きく・しゃべる方だけ鳴らす）。"""
    cats = [L.cat(CAST[left][0], left, 470, h=740, bottom=1075, label_size=56, mute=who != "L"),
            L.cat(CAST[right][0], right, 1450, h=740, bottom=1075, label_size=56, mute=who != "R")]
    return dict(bg=bg(b), cats=cats, say=say, text_top=True, keep_overlap=True, **kw)


def n(text, b, who=None, **kw):
    """ナレーション：画面の下に白い大きな字。登場人物は小さめに後ろで（声は出さない）。"""
    cats = [L.cat(CAST[w][0], w, x, h=560, bottom=790, label_size=50, mute=True, float=True)
            for w, x in zip(who or [], (960,) if len(who or []) == 1 else (560, 1360))]
    return dict(bg=bg(b), cats=cats, sub=text, sub_box=NAR, sub_size=84, keep_overlap=True, se=kw.pop("se", "page_turn_01"), **kw)


def cuts_all():
    return [
        # ---- 0. 注意書き ----
        dict(bg=bg(DOME), cats=[{"a": a_, "x": x_, "h": h_, "bottom": 1070, "mute": True} for a_, x_, h_ in (
                ("dance_tabby_standing_cat", 260, 600), ("dance_three_kittens", 700, 520), ("happy_hamster_open_arms", 1180, 560),
                ("dance_happy_banana_cat", 1640, 600))],
             fx=["dim"], layers_top=[pt("e00_notice")], dur=6.0, no_pop=True, notice=True,
             se={"f": "chime_announce", "len": 3.0, "gain": -2}),
        # ---- ① つかみ ----
        n("2012年10月\nひとりの高校生の言葉に\n日本中がおどろいた", PRESS, ["大谷翔平"], bgm={"file": PURPLE, "gain": -4}),
        p("大谷翔平", "日本のプロ野球には行かず\nメジャーリーグに\n挑戦したいです", PRESS, se="pinpon_notice"),
        p("記者たち", "高校から\nいきなりメジャー!?", PRESS, red=True, se=CONAN),
        n("ところが4日後\nある球団がとんでもない行動に出る", DRAFT, ["栗山監督"], se="doon_heavy"),
        dict(bg=bg(DOME), card=pt("e01_title"), dur=4.2, se="jan",
             cats=[{"a": CAST["大谷翔平"][0], "x": 300, "h": 440, "bottom": 1050, "float": True, "mute": True}]),
        # ---- ② 160キロの高校生 ----
        chap("① 160キロの高校生", se="quiz_question_01", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        n("岩手県の花巻東高校\n身長193cmのピッチャー", HS, ["大谷翔平"]),
        n("2012年7月\n夏の岩手大会の準決勝", KOSHIEN, ["大谷翔平"]),
        fx(p("佐々木監督", "160キロ……\n高校生で初めてだ", KOSHIEN, red=True, se=["explosion_dokaan"]), "crack"),
        n("投げるだけじゃない\nバッターとしても\n大きなホームランを打った", KOSHIEN, ["大谷翔平"]),
        p("メジャー球団", "すごい高校生がいる\nぜひうちに来てほしい", US, se="pi"),
        n("アメリカの球団の\nスカウトたちも\n何度も見に来ていた", US, ["メジャー球団"]),
        # ---- ③ メジャー直行宣言 ----
        chap("② メジャー直行宣言", se="doon_heavy"),
        p("大谷翔平", "若いうちから\n世界のいちばん上で\n勝負したい", PRESS, se="kon"),
        n("日本のプロ野球を通らずに\n高校から直接メジャーへ\n当時はほとんど例がなかった", PRESS, ["大谷翔平"]),
        p("ほかの球団", "本人がそう言うなら\n指名はやめておこう……", DRAFT, se="deflate_hyororo"),
        n("多くの球団が\n指名を見送る流れになった", DRAFT, ["ほかの球団"]),
        # ---- ④ 強行指名 ----
        chap("③ まさかの強行指名", se="doon_heavy", bgm={"file": COCOA, "gain": -4, "fade": 0.6}),
        n("10月25日\nドラフト会議", DRAFT, ["栗山監督", "山田GM"]),
        p("山田GM", "北海道日本ハム\n1位指名\n大谷翔平", DRAFT, se="hyoshigi_01"),
        dict(qmarks=6, **p("記者たち", None, DRAFT, se=["anime_conan_hirameki_remix_a"], fx=["flash", "ring"], dur=2.0, no_pop=True)),   # コナン連打＋特大の「？」
        p("記者たち", "メジャーに行くって\n言ってるのに\n指名した……", DRAFT, red=True, se=["explosion_chudoon"]),
        n("日本ハムは\n「その年にいちばんいい選手を指名する」\nという考えをつらぬいた", DRAFT, ["山田GM"]),
        p("大谷翔平", "アメリカでやりたい\n気持ちは\n変わりません", PRESS, se="kon"),
        p("栗山監督", "え……\nこのままじゃ\n入ってもらえない", NEGO, se=POON),
        # ---- ⑤ 夢への道しるべ ----
        chap("④ 夢への道しるべ", se="whoosh_shu", bgm={"file": MIRAI, "gain": -4, "fade": 0.6}),
        n("日本ハムは\n1冊の資料を用意した", NEGO, ["山田GM"]),
        p("山田GM", "「大谷翔平君\n夢への道しるべ」", NEGO, se="card_flip"),
        n("高校から直接\n海外に行った選手たちが\nどうなったかをデータで示した", NEGO, ["山田GM", "大谷翔平"]),
        two("山田GM", "大谷翔平", "まず日本で力をつけてから\nメジャーに行くほうが\n夢に近づけるかもしれない", NEGO, who="L", se="kon"),
        p("大谷翔平", "え……\nそんな考え方も\nあるのか", NEGO, se="tv_professional_poon_remix_a"),
        # ---- ⑥ 二刀流 ----
        chap("⑤ 二刀流という提案", se="doon_heavy"),
        two("栗山監督", "大谷翔平", "ピッチャーもバッターも\n両方やってみないか", NEGO, who="L", se="pikon"),
        p("大谷翔平", "両方!?\nプロで!?", NEGO, red=True, se=["anime_conan_hirameki_remix_b"]),
        n("プロで投げて打つ選手は\nほとんどいなかった\n「二刀流」という提案", NEGO, ["栗山監督"]),
        p("ほかの球団", "え……\nプロで二刀流なんて\n無理でしょ", DRAFT, se="tv_professional_poon_remix_b"),
        p("栗山監督", "誰もやったことがないなら\nやってみればいい", NEGO, se="kon"),
        # ---- ⑦ 入団 ----
        chap("⑥ 決断", se="doon_heavy", bgm={"file": NORA, "gain": -4, "fade": 0.6}),
        n("話し合いを重ねて\n12月9日", PRESS, ["大谷翔平"]),
        fx(p("大谷翔平", "日本ハムに\nお世話になります", PRESS, se=["game_mario_1up"]), "money"),
        n("12月25日 入団会見\n背番号は11", DOME, ["大谷翔平", "栗山監督"], se="fanfare_pararappara"),
        two("栗山監督", "大谷翔平", "二刀流で\n日本一の選手になろう", DOME, who="L", se="pikon"),
        # ---- ⑧ その後 ----
        chap("⑦ その後", se="whoosh_shu"),
        n("日本ハムで\n投げて打って\n日本一にも", DOME, ["大谷翔平"]),
        n("2018年\n約束どおりメジャーへ", US, ["大谷翔平"], se="whoosh_shu"),
        p("メジャー球団", "投げて打つ!?\nこんな選手は\n見たことがない", US, red=True, se=[CONAN]),
        n("二刀流でMVPを何度も受賞\n世界一の野球選手と\n呼ばれるように", US, ["大谷翔平"], se="sparkle_kirakira_01"),
        # ---- まとめ ----
        chap("まとめ", se="doon_heavy"),
        n("夢を変えたのではなく\n夢への道を\nいっしょに考えた", NEGO, ["栗山監督", "大谷翔平"]),
        n("あの強行指名がなければ\n今の二刀流は\nなかったかもしれない", DOME, ["大谷翔平"]),
        dict(bg=bg(DOME), card=pt("e10_ending"), dur=3.6, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        dict(bg=None, card=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=3.4, se="chirin",
             cats=[{"a": "wave_waving_cat", "x": 1560, "h": 520, "bottom": 1040, "float": True}]),
    ]


def cuts_full():
    return K.hype(L.apply_fx(cuts_all()))


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
