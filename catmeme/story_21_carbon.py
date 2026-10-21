"""21_carbon（飛行機の半分は“日本の糸”？　ボーイング787を支える炭素繊維）。原稿 scripts/sungeki_carbon.md（v1）。
「寸劇」シリーズ（README・story_style.py）。日本の素材シリーズその2（18本目の続き）。役名の札に小さい国旗。

python3 catmeme/story_21_carbon.py          → out/21_carbon_full.mp4
python3 catmeme/story_21_carbon.py --audio  → 音だけ作り直す

原稿のルール（必ず守る）：
- 冒頭で「再構成したお話」。会話は作り話。実在の会社の人を猫で演じない（役はアメリカ・ヨーロッパ・日本の“架空の素材メーカーの社員”）
- 会社名（ボーイング・東レ・三菱重工・帝人・三菱ケミカル）は語り（photo）の事実の説明の中だけ
- 他の国をバカにしない。「約半分」「35％超」「約7割」は「と言われている」「とされる」で出す
- 背景は ChatGPT で作ってもらう（scripts/21_carbon_bg_prompts.md）。届くまでは STANDIN の仮の背景
"""
import os
import sys

import story_style as T

T.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "21_carbon"))
T.FLAGS = True
T.STANDIN.update({"ph01_airplane_sky": "bg45_airport_arrival", "ph02_carbon_fiber": "ph05_cleanroom_workers",
                  "ph03_787_assembly": "bg45_airport_arrival", "ph04_factory_furnace": "ph03_chemical_plant",
                  "ph05_sunset_runway": "ph07_sunset_factory", "bg01_us_hangar": "bg01_us_ai_office",
                  "bg02_jp_fiber_plant": "bg03_jp_material_plant", "bg03_airport_gate": "bg45_airport_arrival",
                  "bg04_rainbow_meadow": "st05_rainbow_meadow"})
BGM_DIR = os.path.join(T.HERE, "bgm")
LIGHT = {"file": os.path.join(BGM_DIR, "nc102462_Cat_life.mp3"), "gain": -1}
BRIGHT = {"file": os.path.join(BGM_DIR, "未来を創る君たちへ.mp3"), "gain": -2}
US, EU, JP = "アメリカ", "ヨーロッパ", "日本"
OUT = os.path.join(T.HERE, "out", "21_carbon_full.mp4")
NOTE = "※飛行機と“ある素材”をめぐる国と企業の関係をもとに再構成したお話です"


def ph(name, text, **kw):
    n = len(text.replace("\n", ""))
    return T.photo(name, text, dur=kw.pop("dur", max(3.4, 1.4 + 0.11 * n)), **kw)


def cuts():
    # ---- 0. 出だし（クイズ型・10/21：黒い画面で始めない） ----
    cs = [
        T.hook("ph01_airplane_sky", "ある旅客機の半分近くは\n何でできている？", sub="Q.", color="yellow", dur=3.4,
               bgm=LIGHT, cat=("think_bike_front_seat_cat", "R")),
        T.full("ph01_airplane_sky", "空を飛ぶ旅客機。\nその体は、ずっと“金属”で作られてきました。", dur=4.0),
        T.full("ph01_airplane_sky", "ところが今、その半分近くが\n“糸”から作られている飛行機があります。", dur=4.2),
    ]
    # ---- 1. アメリカ、燃料代に泣く ----
    a = T.Scene("bg01_us_hangar", [(US, "L", "despair_dramatic_kitten"), (EU, "R", "slack_nail_filing_cat")])
    a.say("L", "燃料代、高すぎる……")
    a.say("L", "機体がもっと軽ければ……", add=True)
    a.say("R", "アルミより軽くて、鉄より強いもの？\nそんな都合のいいもの、\nあるわけないでしょ", dur=3.6)
    a.zoom("L", "……あるらしいんだよ", color="white", cat="realize_wet_cat_stare")
    a.say("R", "は？", cat="huh_huh_cat", dur=1.6)
    cs += a.cuts
    # ---- 2. 日本の“黒い糸” ----
    b = T.Scene("bg02_jp_fiber_plant", [(US, "L", "realize_wet_cat_stare"), (JP, "R", "talk_orange_white_sitting_cat")])
    b.say("R", "いらっしゃいませ。\nこちら、うちの“糸”です", dur=2.8)
    b.zoom("L", "糸！？　飛行機を糸で作れって！？", color="yellow", cat="surprise_big_pupils_cat")
    cs += b.cuts
    cs += [
        ph("ph02_carbon_fiber", "炭素繊維。\n髪の毛の10分の1ほどの細さの、黒い糸です。"),
        ph("ph02_carbon_fiber", "樹脂で固めると、軽いのに、\n鉄より強くなると言われています。"),
    ]
    c = T.Scene("bg02_jp_fiber_plant", [(US, "L", "surprise_big_pupils_cat"), (JP, "R", "sleepy_old_memories_cat")])
    c.say("R", "釣りざおや、\nテニスのラケットにも使われてまして", dur=3.0)
    c.zoom("L", ["軽い…", "強い…", "しかもサビない…"], pos="mid", cat="stare_big_eyes_tabby_kitten")
    c.zoom("L", "それで飛行機、作って！！", color="red", rays=True, cat="angry_aiming_cat")
    c.say("R", "……がんばります", cat="meow_gray_white_kitten", dur=2.0)
    cs += c.cuts
    # ---- 3. 787、誕生 ----
    cs += [
        T.intro("そして——", 2.4),
        ph("ph03_787_assembly", "ボーイング787。機体の重さのおよそ半分に、\n炭素繊維の複合材料が使われていると言われています。",
           bgm=dict(LIGHT, **{"from": 40})),
        ph("ph03_787_assembly", "その炭素繊維は、日本の東レが長期契約で供給。"),
        ph("ph03_787_assembly", "主翼は三菱重工が作り、\n2007年に最初の主翼を出荷しました。"),
        ph("ph03_787_assembly", "日本の会社の受け持ちは35％を超えるとも言われ、\n“準国産機”と呼ばれることもあります。"),
    ]
    d = T.Scene("bg03_airport_gate", [(US, "L", "cocky_dj_cat"), (EU, "C", "glare_disgusted_cat"),
                                      (JP, "R", "talk_orange_white_sitting_cat")])
    d.say("L", "どう？　うちの787")
    d.say("C", "……ほぼ日本製じゃない？")
    d.zoom("L", "言うな！！", color="red", cat="rage_talking_cat", dur=1.8)
    d.say("R", "いえいえ、\nアメリカさんの飛行機です", dur=2.8)
    d.say("C", "……で、うちにも糸、\n売ってくれる？", cat="slack_nail_filing_cat", dur=2.8)
    d.zoom("L", "ずるい！！", color="yellow", cat="sad_banana_cat_cry", dur=1.8)
    cs += d.cuts
    # ---- 4. なぜ日本が強い？ ----
    cs += [
        ph("ph04_factory_furnace", "炭素繊維は、糸を何千度という高温で焼いて作ります。"),
        ph("ph04_factory_furnace", "東レ・帝人・三菱ケミカルなど日本の会社で、\n世界の過半から約7割を占めるとされています。"),
        ph("ph04_factory_furnace", "何十年も前、まだ使い道がはっきりしない頃から、\n作り続けてきたことが強みになった、と言われています。",
           dur=5.4),
    ]
    e = T.Scene("bg02_jp_fiber_plant", [(US, "L", "think_bike_front_seat_cat"), (JP, "R", "sleepy_old_memories_cat")])
    e.say("L", "なんでそんなに\n長く続けられたの？", dur=2.6)
    e.say("R", "最初は、釣りざおくらいしか\n売れなかったんですけどね", dur=3.0)
    e.say("R", "“いつか飛行機に”って、\n言い続けてたら……", add=True, dur=3.0)
    e.zoom("L", ["……ほんとに", "飛んだ…"], pos="mid", cat="realize_wet_cat_stare")
    cs += e.cuts
    # ---- 5. 締め ----
    cs += [
        ph("ph05_sunset_runway", "派手な飛行機の陰で、\n黒い糸を作り続けてきた日本の会社。", bgm=BRIGHT),
        ph("ph05_sunset_runway", "空の上の“軽さ”は、地上の長い我慢から\n生まれたのかもしれません。", dur=4.4),
    ]
    f = T.Scene("bg04_rainbow_meadow", [(US, "L", "excited_hodomoe_city_cat"), (EU, "C", "dance_trending_cat"),
                                        (JP, "R", "meow_gray_white_kitten")])
    f.say("L", "次は車も糸で作って！")
    f.say("C", "うちは自転車！")
    f.say("R", "……順番にお作りします", dur=2.6)
    f.ending("happy_girlfriend_dance_cat")
    cs += f.cuts
    return cs


if __name__ == "__main__":
    if sys.argv[1:] == ["--audio"]:
        T.remux(cuts(), OUT)
        sys.exit()
    T.run(cuts(), OUT, OUT.replace("_full.mp4", "_preview"))
