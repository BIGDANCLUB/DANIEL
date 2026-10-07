"""04 個人情報流出のサムネ（横 1280x720）。python3 catmeme/make_thumb_04.py → thumbs/04_leak.png ほか

作りは make_thumb_03.py と同じ（上の赤帯／大きな黄色い文字／赤い副題／札／左右の猫）。
"""
import os

from make_thumb_03 import make

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "thumbs", "04_leak.png")
NEWS, SAGE, HACK = (215, 35, 35), (40, 90, 200), (30, 30, 30)
WHITE, YELLOW = (255, 255, 255), (255, 222, 0)
COMMON = dict(bg_dir="04_leak", bg="bg24_server_room", ray_cols=((255, 40, 40), (255, 210, 0)))
VARIANTS = {
    # 正式版：猫ミーム感を強めた版（脇役の猫とひとことを散らす）
    "": dict(left=("surprise_big_pupils_cat", 0.6, False, "ニュース猫", NEWS), right=("angry_aiming_cat", 1.0, False, "ハッカー猫", HACK),
             top="9月末から　漏えいの発表がほぼ毎日", big="個人情報", sub="盗まれすぎ問題!?", badge="", cat_h=480, tags=False,
             extras=(("sad_banana_cat_cry", 1.0, False, 450, 270, 735), ("glare_disgusted_cat", 1.0, True, 830, 270, 735)),
             words=(("1,000万件!?", 200, 640, 58, WHITE, 10), ("ﾌｯﾌｯﾌ…", 1130, 345, 64, (190, 190, 190), -10),
                    ("ﾋｴｯ", 450, 480, 56, YELLOW, 8), ("お詫びクーポン?", 830, 480, 44, YELLOW, -8))),
    # 別案：件数を札にしたシンプル版
    "_b": dict(left=("weird_meowing_cat", 1.0, False, "ニュース猫", NEWS), right=("eat_pop_cat", 1.0, False, "博識な猫", SAGE),
               top="焼肉きんぐ・タイムズカー・デジタル庁…", big="個人情報", sub="盗まれすぎ問題!?",
               badge="あなたの情報も漏れてるかも？"),
}

if __name__ == "__main__":
    for k, v in VARIANTS.items():
        make(OUT.replace(".png", k + ".png"), **{**COMMON, **v})
