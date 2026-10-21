"""22_terakoya（江戸の子どもは字が読めた　寺子屋が“世界トップクラスの識字率”を生んだと言われる理由）。
原稿 scripts/sungeki_terakoya.md（v1）。「寸劇」シリーズ（README・story_style.py）。役名の札に小さい国旗。

python3 catmeme/story_22_terakoya.py          → out/22_terakoya_full.mp4
python3 catmeme/story_22_terakoya.py --audio  → 音だけ作り直す

原稿のルール（必ず守る）：
- 冒頭で「再構成したお話」。登場人物はすべて架空（実在の外国人・歴史上の人物は猫で演じない・名前も出さない）
- 識字率の数字は推計で幅がある：「推計」「〜とも」「と言われている」を付ける。「世界一」と言い切らない
- 外国をバカにしない（他国との比較の数字は出さない）。外国人の役は“素直に驚いて感心する旅行者”
- 背景は ChatGPT で作ってもらう（scripts/22_terakoya_bg_prompts.md）。届くまでは STANDIN の仮の背景
"""
import os
import sys

import story_style as T

T.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "22_terakoya"))
T.FLAGS = True
T.STANDIN.update({"ph01_edo_street": "bg60_autumn_leaves", "ph02_terakoya": "bg55_ryokan", "ph03_daikon": "bg16_food_aisle",
                  "ph04_kashihonya": "bg56_kyoto_temple", "ph05_old_books": "bg08_study", "ph06_meiji_school": "bg21_school_gate",
                  "ph07_sunset_edo": "bg60_autumn_leaves", "il_terakoya": "bg55_ryokan", "bg01_edo_shop_street": "bg56_kyoto_temple",
                  "bg02_terakoya_room": "bg55_ryokan", "bg03_rainbow_meadow": "st05_rainbow_meadow"})
BGM_DIR = os.path.join(T.HERE, "bgm")
NORA = {"file": os.path.join(BGM_DIR, "野良猫は宇宙を目指した.mp3"), "gain": -2}
BRIGHT = {"file": os.path.join(BGM_DIR, "未来を創る君たちへ.mp3"), "gain": -2}
GB, KID, SEN, OKA = "イギリスの旅行者", "江戸の子ども", "寺子屋の師匠", "八百屋のおかみ"
OUT = os.path.join(T.HERE, "out", "22_terakoya_full.mp4")
NOTE = "※幕末の日本を訪れた外国人の驚きをもとに再構成したお話です（登場人物は架空）"


def ph(name, text, **kw):
    n = len(text.replace("\n", ""))
    return T.photo(name, text, dur=kw.pop("dur", max(3.4, 1.4 + 0.11 * n)), **kw)


def cuts():
    # ---- 0〜1. 出だし（いきなり寸劇・10/21：黒い画面で始めない。「再構成」は左下の札） ----
    cs = []
    a = T.Scene("bg01_edo_shop_street", [(GB, "L", "surprise_big_pupils_cat"), (KID, "R", "excited_hodomoe_city_cat")], bgm=NORA)
    a.say("R", "“本日、大安売り”だって！\nおっかあに言ってこよ！", dur=3.0)
    a.zoom("L", "……今、読んだ？", color="white", cat="surprise_big_pupils_cat")
    a.say("R", "え？　読めるよ？", cat="huh_huh_cat")
    a.zoom("L", "この子、字が読めるの！？", color="yellow", cat="stare_big_eyes_tabby_kitten")
    cs += a.cuts
    cs += [
        T.full("ph01_edo_street", "今から160年ほど前、江戸。", dur=3.2),
        T.full("ph01_edo_street", "海の向こうから来た人たちが、\nある“当たり前の光景”に驚いたと言われています。", dur=4.6),
    ]
    a2 = T.Scene("bg01_edo_shop_street", [(GB, "L", "stare_big_eyes_tabby_kitten"), (KID, "R", "dance_trending_cat")])
    a2.say("R", "みんな読めるよ。\n寺子屋で習ったもん", dur=2.8)
    a2.zoom("L", "テラコヤ……？", color="white", bubble="il_terakoya", cat="think_bike_front_seat_cat")
    cs += a2.cuts
    # ---- 2. 寺子屋へ ----
    b = T.Scene("bg02_terakoya_room", [(GB, "L", "think_bike_front_seat_cat"), (SEN, "C", "sleepy_old_memories_cat"),
                                       (KID, "R", "itchy_kitten_butt")])
    b.say("C", "ようこそ。今日は手習い\n（字の練習）の日でしてな", dur=3.0)
    b.say("R", "“いろはにほへと”〜！")
    b.say("R", "そろばんも得意！", add=True)
    b.say("L", "先生は、お坊さん？　武士？", dur=2.6)
    b.say("C", "わしはただの隠居じゃよ。\n町内の子に教えとるだけ", cat="talk_orange_white_sitting_cat", dur=3.0)
    b.zoom("L", "ふつうの町の人が、先生！？", color="yellow", cat="surprise_big_pupils_cat")
    cs += b.cuts
    b2 = T.Scene("bg02_terakoya_room", [(GB, "L", "think_bike_front_seat_cat"), (SEN, "C", "sleepy_old_memories_cat"),
                                        (KID, "R", "dance_trending_cat")])
    b2.say("L", "何人くらい、通ってるの？")
    b2.say("C", "今日は二十人ほどかのう", dur=2.4)
    b2.say("R", "となりの寺子屋にも、\n友だちがいっぱい！", dur=2.6)
    b2.zoom("L", "町に、いくつもあるの！？", color="yellow", cat="surprise_big_pupils_cat")
    b2.say("C", "町内ごとに、ひとつふたつは\nあるもんじゃよ", cat="talk_orange_white_sitting_cat", dur=2.8)
    cs += b2.cuts
    cs += [
        ph("ph02_terakoya", "寺子屋は、町や村の人がひらいた、\n子どものための手習い塾。"),
        ph("ph02_terakoya", "幕末には全国で1万を超え、\n1万5千以上とも言われます。\n江戸の町だけでも1,200以上あったとされています。", dur=5.4),
    ]
    # ---- 3. 月謝は野菜でもいい？ ----
    c = T.Scene("bg02_terakoya_room", [(GB, "L", "surprise_big_pupils_cat"), (SEN, "C", "sleepy_old_memories_cat"),
                                       (OKA, "R", "slack_nail_filing_cat")])
    c.say("R", "先生、今月のお礼、\n大根でいいかい？", dur=2.6)
    c.say("C", "おお、助かる助かる")
    c.zoom("L", "授業料が大根！？", color="red", rays=True, cat="huh_goat_talks_to_huh_cat")
    c.say("R", "お金のない家は、\nそれで十分さ", cat="laugh_laughing_dog", dur=2.6)
    cs += c.cuts
    c2 = T.Scene("bg02_terakoya_room", [(GB, "L", "realize_wet_cat_stare"), (SEN, "C", "sleepy_old_memories_cat"),
                                        (OKA, "R", "slack_nail_filing_cat")])
    c2.say("L", "お金のない家の子も、\n来ていいの？", dur=2.6)
    c2.say("C", "もちろん。読めて困る子は\nおらんからの", dur=2.8)
    c2.say("R", "うちの子なんか、\n今じゃわたしより字がうまいよ", cat="laugh_laughing_dog", dur=3.0)
    c2.zoom("L", ["親より…", "うまい…"], pos="mid", cat="stare_big_eyes_tabby_kitten")
    cs += c2.cuts
    cs.append(ph("ph03_daikon", "お礼は、お金でも、季節の野菜や品物でも\nよかったと言われています。身分に関係なく\n"
                                "通えたことも、広がった理由のひとつとされます。", dur=5.8))
    # ---- 4. なぜ、みんな字を習った？ ----
    d = T.Scene("bg01_edo_shop_street", [(GB, "L", "think_bike_front_seat_cat"), (KID, "C", "dance_koto_nai_cat"),
                                         (OKA, "R", "slack_nail_filing_cat")])
    d.say("L", "どうして、そんなに\n字を習わせるの？", dur=2.6)
    d.say("R", "読めなきゃ、\n商売にならないからね", dur=2.6)
    d.say("R", "証文（契約書）も、帳簿も、\nお触れ（お知らせ）も、全部、字", add=True, dur=3.6)
    d.say("C", "それに、\n貸本屋の本が読みたい！", dur=2.6)
    cs += d.cuts
    d2 = T.Scene("bg01_edo_shop_street", [(GB, "L", "surprise_big_pupils_cat"), (KID, "C", "dance_koto_nai_cat"),
                                          (OKA, "R", "slack_nail_filing_cat")])
    d2.say("C", "読めないと、\nお使いもできないし！", dur=2.6)
    d2.say("R", "値段の札も、\n全部字だからね", dur=2.4)
    d2.say("L", "町じゅうが、\n字であふれてる……", cat="realize_wet_cat_stare", dur=2.6)
    d2.zoom("L", "まるで町全体が学校だ！！", color="yellow", cat="excited_hodomoe_city_cat")
    cs += d2.cuts
    cs += [
        ph("ph04_kashihonya", "江戸には本を貸して回る“貸本屋”がいて、\n町の人たちは物語や瓦版を楽しんでいました。"),
        ph("ph04_kashihonya", "読み・書き・そろばんは、\n暮らしと商売に欠かせない力だったのです。"),
    ]
    # ---- 5. 数字で見ると ----
    cs += [
        ph("ph05_old_books", "幕末の識字率には、正確な統計はありません。"),
        ph("ph05_old_books", "推計では、庶民の男子で5割前後、\n女子で2割前後とも、\n江戸の町では7割を超えていたとも言われます。", dur=5.4),
        ph("ph05_old_books", "当時としては、世界でもトップクラスだったと\n言われることがあります。\n（数字は資料によって幅があります）", dur=5.4),
    ]
    e = T.Scene("bg02_terakoya_room", [(GB, "L", "realize_wet_cat_stare"), (SEN, "C", "talk_orange_white_sitting_cat"),
                                       (KID, "R", "dance_trending_cat")])
    e.zoom("L", ["国のお金じゃなく…", "町の人たちが…", "こんなに…"], pos="mid", cat="realize_wet_cat_stare")
    e.say("C", "みんな、自分の子に\n“読める大人”になってほしいだけじゃよ", dur=3.4)
    e.zoom("L", "国に帰ったら、絶対に書き残す！！", color="red", rays=True, cat="angry_aiming_cat")
    e.say("R", "じゃあ、わたしが字、\n教えてあげる！", dur=2.6)
    cs += e.cuts
    e2 = T.Scene("bg02_terakoya_room", [(GB, "L", "meow_gray_white_kitten"), (SEN, "C", "sleepy_old_memories_cat"),
                                        (KID, "R", "excited_hodomoe_city_cat")])
    e2.say("R", "まずは“い”から！\nこうやって筆を持って……", dur=2.8)
    e2.say("L", "……むずかしい", cat="sulk_hungry_cat", dur=2.0)
    e2.say("C", "みんな最初はそうじゃ。\nゆっくりでええ", dur=2.6)
    e2.say("R", "毎日ちょっとずつ！", add=True)
    cs += e2.cuts
    # ---- 6. その後 ----
    cs += [
        T.intro("そして——", 2.4),
        ph("ph06_meiji_school", "明治5年（1872年）、\n全国に学校をつくる“学制”が始まります。", bgm=dict(NORA, **{"from": 50})),
        ph("ph06_meiji_school", "学校がすばやく広がった土台には、\n寺子屋の積み重ねがあったと言われています。"),
    ]
    # ---- 7. 締め ----
    cs += [
        ph("ph07_sunset_edo", "看板を読む子ども。大根で払う授業料。\n町のおじいさんの先生。", bgm=BRIGHT),
        ph("ph07_sunset_edo", "日本人には当たり前だった光景が、\n海の向こうの人には“奇跡”に見えたのかもしれません。", dur=4.8),
    ]
    f = T.Scene("bg03_rainbow_meadow", [(GB, "L", "meow_gray_white_kitten"), (SEN, "C", "sleepy_old_memories_cat"),
                                        (KID, "R", "excited_hodomoe_city_cat")])
    f.say("R", "“い・ろ・は”、書けた？")
    f.say("L", "……い……ろ……")
    f.say("C", "上出来、上出来")
    f.ending("happy_girlfriend_dance_cat")
    cs += f.cuts
    return cs


if __name__ == "__main__":
    if sys.argv[1:] == ["--audio"]:
        T.remux(cuts(), OUT)
        sys.exit()
    T.run(cuts(), OUT, OUT.replace("_full.mp4", "_preview"))
