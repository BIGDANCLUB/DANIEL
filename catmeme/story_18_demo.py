"""「寸劇」シリーズ（story_style.py）の見本。参考動画5本の作りを一通り入れる。

python3 catmeme/story_18_demo.py → out/story_18_demo.mp4
お話は「留学生がコンビニに驚いた」という再構成の作り話（実在の人物は出さない）。背景・写真・イラストは AI で作った。
"""
import os

import story_style as T

BGM = os.path.join(T.HERE, "bgm", "nc102462_Cat_life.mp3")


def cuts():
    cs = [
        T.intro("これは、日本に来た留学生たちが語った", 3.2),
        T.intro("コンビニでの驚きをもとに再構成したお話です。", 3.4),
        T.photo("st01_phone_hands", "SNSで日本のコンビニを知った海外の10代にとって", 3.6),
        T.photo("st01_phone_hands", "私たちの「いつものお店」が、\n特別に見えることがあります。", 3.6),
    ]
    a = T.Scene("st02_home_kitchen", [("留学生", "L", "dance_tabby_standing_cat"), ("ママ", "R", "punch_tabby_cat_reach")],
                bgm={"file": BGM, "gain": -8})
    a.say("L", "日本のコンビニ、早く行ってみたい！！", h=920)
    a.say("R", "夜中でも開いてるんだってね", cat="talk_orange_white_sitting_cat")
    a.zoom("L", "おにぎりもお弁当もあるんだよ！！", color="red", bubble="il_onigiri", cat="stare_big_eyes_tabby_kitten")
    cs += a.cuts
    cs.append(T.intro("そして、日本に来て1週間——", 3.0))
    b = T.Scene("st03_konbini", [("留学生", "L", "meow_gray_white_kitten"), ("日本人JK", "C", "stare_interviewer_cat"),
                                 ("店員", "R", "talk_orange_white_sitting_cat")], bgm={"file": BGM, "gain": -8, "from": 30})
    b.say("R", "お弁当、温めますか？")
    b.zoom("L", "え、温めてくれるの！？", color="yellow", cat="surprise_big_pupils_cat")
    b.say("C", "普通だよw", cat="laugh_laughing_dog")
    b.say("L", "おにぎりも！！", cat="dance_tabby_standing_cat", h=920)
    b.say("L", "からあげも！！", add=True)
    b.say("L", "肉まんも！！", add=True)
    b.zoom("L", ["な、なにこれ…", "この便利さ…"], pos="mid", cat="stare_big_eyes_tabby_kitten")
    b.zoom("C", "ようこそ日本へ", color="red", rays=True, cat="stare_interviewer_cat")
    cs += b.cuts
    cs += [
        T.photo("st04_konbini_friends", "日本人には当たり前のコンビニも", 3.4),
        T.photo("st04_konbini_friends", "海外の10代には、忘れられない\n「日本の思い出」になるのかもしれません。", 4.2),
    ]
    c = T.Scene("st05_rainbow_meadow", [("留学生", "L", "dance_tabby_standing_cat"), ("日本人JK", "C", "stare_interviewer_cat"),
                                        ("店員", "R", "talk_orange_white_sitting_cat")])
    c.say("C", "明日もコンビニ寄ってく？")
    c.say("L", "行く！！", h=920)
    c.ending("happy_girlfriend_dance_cat")
    cs += c.cuts
    return cs


if __name__ == "__main__":
    T.run(cuts(), os.path.join(T.HERE, "out", "story_18_demo.mp4"), os.path.join(T.HERE, "out", "story_18_demo_preview"))
