"""物語形式（story_style.py）の見本。参考動画の冒頭と同じ流れ：黒い画面の文字 → 写真＋字幕 → 猫の寸劇。

python3 catmeme/story_18_demo.py → out/story_18_demo.mp4
お話は「留学生がコンビニに驚いた」という再構成の作り話（実在の人物は出さない）。背景は AI で作った写真ふう。
"""
import os

import story_style as T

BGM = os.path.join(T.HERE, "bgm", "nc102462_Cat_life.mp3")


def cuts():
    return [
        T.intro("これは、日本に来た留学生たちが語った", 3.6),
        T.intro("コンビニでの驚きをもとに\n再構成したお話です。", 3.6),
        T.photo("st01_phone_hands", "SNSで日本のコンビニを知った海外の10代にとって", 4.0),
        T.photo("st01_phone_hands", "私たちの「いつものお店」が、\n特別に見えることがあります。", 4.0),
        T.skit("st02_home_kitchen",
               [("dance_tabby_standing_cat", "留学生", "L", 1000), ("punch_tabby_cat_reach", "ママ", "R", 820)],
               [("日本のコンビニ、早く行ってみたい！！", "L", 0.3), ("夜中でも開いてるんだってね", "R", 2.6)],
               5.6, bgm={"file": BGM, "gain": -8}),
        T.skit("st03_konbini",
               [("surprise_big_pupils_cat", "留学生", "L", 760), ("talk_orange_white_sitting_cat", "店員", "R", 940)],
               [("お弁当、温めますか？", "R", 0.3), ("え、お店で温めてくれるの！？", "L", 2.2)],
               5.0),
        T.ending(),
    ]


if __name__ == "__main__":
    T.run(cuts(), os.path.join(T.HERE, "out", "story_18_demo.mp4"), os.path.join(T.HERE, "out", "story_18_demo_preview"))
