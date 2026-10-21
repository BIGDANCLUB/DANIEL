"""22本目（寺子屋と江戸の識字率・寸劇シリーズ）のショート。作りは short_18_semicon.py と同じ。60秒ちょうど。

python3 catmeme/short_22_terakoya.py → out/short_22_terakoya.mp4
- 登場人物はすべて架空（実在の外国人・歴史上の人物は出さない）。役名の左に小さい国旗
- 識字率は「推計・幅あり」。「世界一」と言わない。他の国との比較の数字は出さない。外国をバカにしない
- 「寸劇」とは書かない。画面の下と右端には猫・役名・写真を置かない
- 背景は仮（ChatGPT の画像が届いたら差しかえ：scripts/22_terakoya_bg_prompts.md）
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M
from short_18_semicon import photo_img

HERE = M.HERE
NAME = "short_22_terakoya"
TITLE = ("実は江戸の子どもは", "字が読めた", M.WHITE, M.YELLOW, M.RED)
C = M.C
NORA = os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3")
M.BGS[:0] = [os.path.join(HERE, "backgrounds", d) for d in ("22_terakoya", "14_japan", "18_story")]
# 仮の背景（22_terakoya の画像が届いたら同じ名前でそちらを使う）
STANDIN = {"bg01_edo_shop_street": "bg56_kyoto_temple", "bg02_terakoya_room": "bg55_ryokan", "ph02_terakoya": "bg55_ryokan",
           "ph05_old_books": "bg08_study", "ph06_meiji_school": "bg21_school_gate"}
WHO = {"GB": ("イギリスの旅行者", "gb"), "KID": ("江戸の子ども", "jp"), "SEN": ("寺子屋の師匠", "jp"), "OKA": ("八百屋のおかみ", "jp")}
MEADOW = "st05_rainbow_meadow"


def bgn(n):
    try:
        M.bg_path(n)
        return n
    except FileNotFoundError:
        return STANDIN[n]


def say(bg, who, text, a, dur, size=96, se="pi", **kw):
    c = M.cut(bgn(bg), text, [(a, C, 1100, False)], dur, label=WHO[who][0], label_x=540, size=size, se=se, **kw)
    c["label_flag"] = WHO[who][1]
    c["label_size"] = 90
    return c


def tell(name, text, dur, **kw):
    c = M.cut(MEADOW, text, [], dur, size=kw.pop("size", 86), se=kw.pop("se", "kon"), **kw)
    img = photo_img(bgn(name))
    c["img"], c["img_y"] = img, M.SAFE_BOTTOM - 10 - img.height / 2
    return c


ST, ROOM = "bg01_edo_shop_street", "bg02_terakoya_room"


def cuts():
    return [
        say(ST, "KID", "“本日、*大安売り*”\nだって！", "excited_hodomoe_city_cat", 2.6, bgm={"file": NORA, "gain": -2}),
        say(ST, "GB", "……今\n*読んだ？*", "surprise_big_pupils_cat", 2.2, size=110),
        say(ST, "KID", "みんな読めるよ\n*寺子屋*で習ったもん", "dance_trending_cat", 2.8),
        say(ST, "GB", "*テラコヤ……？*", "huh_huh_cat", 2.0, size=110),
        tell("ph02_terakoya", "寺子屋は\n町や村の人がひらいた\n*子どもの手習い塾*", 3.2),
        say(ROOM, "SEN", "わしはただの隠居じゃよ\n*町内の子*に教えとるだけ", "sleepy_old_memories_cat", 3.2, size=90),
        say(ROOM, "GB", "ふつうの町の人が\n*先生！？*", "stare_big_eyes_tabby_kitten", 2.6),
        tell("ph02_terakoya", "幕末には全国で\n*1万を超え*\n1万5千以上とも", 3.2),
        say(ROOM, "OKA", "先生、今月のお礼\n*大根*でいいかい？", "slack_nail_filing_cat", 2.8),
        say(ROOM, "GB", "授業料が\n*大根！？*", "huh_goat_talks_to_huh_cat", 2.2, size=110),
        tell("ph02_terakoya", "お礼は野菜や品物でも\n*よかった*と言われる", 3.0),
        say(ST, "OKA", "読めなきゃ\n*商売にならない*\nからね", "slack_nail_filing_cat", 2.6),
        tell("ph05_old_books", "識字率に*正確な統計はない*\n推計で 庶民の男子5割前後\n女子2割前後とも", 3.6, size=80),
        tell("ph05_old_books", "江戸の町では\n*7割を超えていた*\nとも言われる", 3.0),
        say(ROOM, "GB", "国のお金じゃなく\n*町の人たちが*……", "realize_wet_cat_stare", 2.8),
        say(ROOM, "SEN", "自分の子に\n*“読める大人”*に\nなってほしいだけじゃよ", "talk_orange_white_sitting_cat", 3.2, size=90),
        tell("ph06_meiji_school", "明治5年の“学制”\n学校が広がった土台に\n*寺子屋*があった、とも", 3.2),
        say(MEADOW, "KID", "“い・ろ・は”\n*書けた？*", "excited_hodomoe_city_cat", 2.2),
        say(MEADOW, "GB", "……い……ろ……", "meow_gray_white_kitten", 2.0),
        say(MEADOW, "SEN", "※登場人物はすべて架空です\n※識字率は推計で、資料によって幅があります\n※背景はAIで作っています",
            "sleepy_old_memories_cat", 3.0, size=44, se="pinpon_notice"),
    ]


def main():
    cs = M.keep_going(cuts())
    title = M.title_band(*TITLE)
    for c in cs:
        c["draw"] = M.make_draw(c, title)
    print(f"{len(cs)} カット・{sum(R.cut_dur(c) for c in cs):.1f}秒")
    S.run(cs, title, os.path.join(HERE, "out", NAME + ".mp4"), os.path.join(HERE, "out", NAME + "_preview"))


if __name__ == "__main__":
    main()
