"""01_todai_president（東大総長）のカット割り。原稿 scripts/01_todai_president.md の 1〜5 章。

python3 catmeme/cuts_01_todai.py            → out/01_todai_trial.mp4（試作：冒頭〜「選ばれたのは」）
"""
import os
import sys

import parts as P
import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.join(HERE, "backgrounds", "01_todai")
PT = os.path.join(HERE, "parts", "01_todai")
BGM = os.path.join(HERE, "bgm")


def bg(n):
    return os.path.join(BG, n + ".png")


def pt(n):
    return os.path.join(PT, n + ".png")


def news(a, say, **kw):
    """ニュース猫（リビング・中央）のセリフ。"""
    cat = {"a": a, "x": kw.pop("x", 500), "h": kw.pop("h", 760), "bottom": 1010, "flip": kw.pop("flip", False),
           "ss": kw.pop("ss", 0.0), "anchor": kw.pop("anchor", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg("bg02_room"), cats=[cat], say=say, say_name="ニュース猫", **kw)


def card(c, sub, cat=None, b="bg03_blackboard", **kw):
    """解説カード＋右下の小さい猫＋字幕。"""
    cats = [{"a": cat, "x": 1752, "h": 330, "bottom": 830, "float": True, "small": True}] if cat else []
    return dict(bg=bg(b), card=pt(c), cats=cats, sub=sub, **kw)


CANDS = [("大越慎一さん", "call_customer_service_cat"), ("菅野暁さん", "dance_wop_cat"),
         ("染谷隆夫さん", "spit_not_my_taste_cat"), ("藤垣裕子さん", "sleepy_old_memories_cat"),
         ("山本隆司さん", "sleepy_sleepy_cat")]
CAND_X = [250, 605, 960, 1315, 1670]


def candidates():
    cats, tags = [], []
    for (name, a), x in zip(CANDS, CAND_X):
        cats.append({"a": a, "x": x, "h": 360, "bottom": 690, "still": True, "float": True})
        tags.append(P.name_plate(name, int(x - (len(name) * 40 + 26) / 2), 705, size=40))
    return cats, tags


TEACHERS = [{"a": "sleepy_old_memories_cat", "x": 560, "h": 420, "bottom": 840, "float": True},
            {"a": "work_typing_cat", "x": 960, "h": 470, "bottom": 850, "float": True},
            {"a": "blank_black_cat_zoning_out", "x": 1380, "h": 430, "bottom": 850, "flip": True}]
MEETING = [{"a": "scold_talking_cats", "x": 700, "h": 520, "bottom": 900},
           {"a": "tense_two_cats_face_off", "x": 1300, "h": 500, "bottom": 900, "flip": True}]


def narr(b, sub, a, **kw):
    """ナレーション（出来事の説明）。左に猫、右に大きな文字。"""
    cat = {"a": a, "x": kw.pop("x", 470), "h": kw.pop("h", 640), "bottom": 990, "flip": kw.pop("flip", False),
           "sound": kw.pop("sound", False)}
    return dict(bg=bg(b), cats=[cat], sub=sub, **kw)


PURPLE = os.path.join(BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")


def cuts_trial():
    cand_cats, cand_tags = candidates()
    return [
        # ---- 1. つかみ ----
        dict(card=None, layers=[pt("e00_notice")], dur=1.8, bgm={"file": PURPLE, "gain": -7}),
        dict(bg=bg("bg01_campus"), card=pt("e01_title"), dur=2.4, se="chime",
             cats=[{"a": "wave_waving_cat", "x": 300, "h": 420, "bottom": 1040, "float": True}]),
        narr("bg01_campus", "2026年9月28日\n東大の次の「総長」が\n決まった", "work_typing_cat"),
        news("slack_nail_filing_cat", "ほーん、\n東大のボス\n決まったんだ"),
        narr("bg01_campus", "選ばれたのは\n投票で2位だった人", "peek_what_happen_cat", se="don"),
        news("blank_black_cat_zoning_out", "……は？", dur=1.3),
        news("huh_huh_cat", "いやいやいや\n待って待って"),
        news("confused_i_dont_know_cat", "2位？\n1位じゃなくて？\nなんで？？"),
        narr("bg01_campus", "しかも\n東大150年の歴史で\n初めての女性の総長", "call_customer_service_cat", se="don"),
        news("despair_dramatic_kitten", "ちょ、\n情報量\nバグってんだけど"),
        # ---- 2. 総長ってだれ？ ----
        news("weird_meowing_cat", "てか総長って\nなに？\n暴走族のアタマ？"),
        card("e02_soucho", "総長＝大学のいちばん上の人（ふつうは「学長」）", "work_typing_cat", dur=2.4),
        news("glare_disgusted_cat", "呼び方つっよ", dur=1.4, anchor=True),
        card("e02_soucho", "次の総長の任期は　2027年4月から6年間", "sulk_hungry_cat", dur=2.2),
        news("surprise_big_pupils_cat", "6年！？\nなっが", dur=1.5),
        # ---- 3. 候補者は5人 ----
        dict(bg=bg("bg01_campus"), sub="候補者は5人", cats=cand_cats, layers=cand_tags, dur=2.2, se="pop"),
        news("showoff_gojo_cosplay_cat", "うわ、\n全員つよそう", dur=1.6),
        # ---- 4. 先生たちの投票 ----
        dict(bg=bg("bg04_voting"), sub="学内の先生たちが投票\n「意向投票」", cats=TEACHERS, dur=2.2),
        dict(bg=bg("bg04_voting"), cats=TEACHERS, say="どれにしよ〜\nまあこの人っしょ", say_name="先生たち",
             plate_xy=(60, 900), dur=2.0),
        narr("bg06_spotlight", "2回目の投票の\n結果は……", "dance_koto_nai_cat", se="drum", dur=2.2),
        card("e05_votes", "染谷さんが過半数でダントツ1位", "angry_aiming_cat", dur=2.6, se="don"),
        news("realize_wet_cat_stare", "え、1位の人、\n半分以上\n取ってんじゃん"),
        news("joy_happy_happy_happy_cat", "2位の倍よ倍！\nはい優勝！\n解散！", sound=True),
        # ---- 5. 最後に決めるのは会議 ----
        narr("bg05_meeting", "ところが\n最後に決めるのは\n投票じゃない", "sleepy_sleepy_cat", se="don",
             bgm={"file": None, "fade": 1.0}),
        card("e04_flow", "最後は「総長選考・監察会議」（16人）が決める", "call_customer_service_cat",
             b="bg05_meeting", dur=2.6),
        news("blank_black_cat_zoning_out", "……ん？", dur=1.2, flip=True),
        dict(bg=bg("bg05_meeting"), cats=MEETING, say="はーい、\nじゃ会議はじめまーす", say_name="会議の猫たち",
             plate_xy=(60, 900), bgm={"file": os.path.join(BGM, "2_23_AM.mp3"), "gain": -5, "fade": 0.8}),
        card("e04_flow", "投票は「参考にする材料の一つ」　書類や面接も合わせて決める", "slack_nail_filing_cat",
             b="bg05_meeting", dur=2.8),
        news("huh_goat_talks_to_huh_cat", "え、投票って\nただのアンケート\n的なやつ？"),
        dict(bg=bg("bg05_meeting"), cats=MEETING, say="うーん……", say_name="会議の猫たち", plate_xy=(60, 900),
             dur=1.6, bgm={"file": None, "fade": 0.8}),
        news("sleep_sleeping_cat", "なげーよ", dur=1.3),
        dict(bg=bg("bg06_spotlight"), sub="そして選ばれたのは——", dur=2.0, se="drum"),
        dict(bg=bg("bg06_spotlight"), card=pt("e05c_reveal"), dur=2.8, se="don",
             cats=[{"a": "sleepy_old_memories_cat", "x": 960, "h": 300, "bottom": 1000, "float": True, "still": True}],
             sting={"file": os.path.join(BGM, "神の怒り.mp3"), "len": 6.0, "gain": -18}),
        news("weird_meowing_cat", "えええええ！？", dur=1.3, flip=True),
        news("laugh_laughing_dog", "2位の人\nきたーーー！？", dur=1.6),
        news("tense_two_cats_face_off", "マジかよ\n逆転じゃん", dur=1.8),
    ]


if __name__ == "__main__":
    out = os.path.join(HERE, "out", "01_todai_trial.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cuts = cuts_trial()
    if sys.argv[1:] == ["--audio"]:   # 音だけ作り直す
        R.remux_audio(cuts, out, out.replace(".mp4", "_a.mp4"))
        os.replace(out.replace(".mp4", "_a.mp4"), out)
        sys.exit()
    if len(sys.argv) > 1:   # 例: python3 cuts_01_todai.py 0:5 → 先頭5カットだけ
        a, b = (int(x) if x else None for x in sys.argv[1].split(":"))
        cuts = cuts[a:b]
    R.render(cuts, out, preview_dir=os.path.join(HERE, "out", "01_todai_trial_preview"))
