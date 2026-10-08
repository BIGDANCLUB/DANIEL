"""05（ペスト研究所）・06（絶望ライン工）のサムネ（横 1280x720）。

python3 catmeme/make_thumb_05_06.py → thumbs/05_plague.png, thumbs/06_zetsubou.png
作りは make_thumb_04.py と同じ（上の赤帯／大きな黄色い文字／赤い副題／札／猫）。
注意：05 は亡くなった方がいるので、ふざけた猫・ひとことは使わない。「当局はペストを否定」を札で必ず出す。
06 は本人・家族をバカにしない。
"""
import os

from make_thumb_03 import make

HERE = os.path.dirname(os.path.abspath(__file__))
NEWS, SAGE = (215, 35, 35), (40, 90, 200)
WHITE, YELLOW, RED, NAVY = (255, 255, 255), (255, 222, 0), (235, 25, 25), (25, 32, 56)

THUMBS = {
    "05_plague": dict(
        bg_dir="01_todai", bg="bg11_tsukuba", ray_cols=((120, 40, 40), (60, 60, 90)),
        left=("surprise_big_pupils_cat", 0.6, False, "ニュース猫", NEWS), right=("think_bike_front_seat_cat", 1.0, False, "博識な猫", SAGE),
        top="シベリアの研究所で職員が死亡・約200人を隔離", big="令和のペスト", sub="結局どうなった？", badge="",
        cat_h=470, tags=True,
        stickers=(("ロシア当局「ペストは検出されず」⇒本当か？", 640, 560, 42, WHITE, RED, -2),),
        words=()),
    "06_zetsubou": dict(
        bg_dir="02_october", bg="bg14_home_night", ray_cols=((255, 60, 60), (255, 210, 0)),
        left=("surprise_big_pupils_cat", 0.6, False, "ニュース猫", NEWS), right=("huh_huh_cat", 1.0, True, "ネットの声", (120, 50, 170)),
        top="「年収240万・43歳独身」の人気YouTuber", big="実は既婚", sub="で大炎上!?", badge="",
        cat_h=480, tags=False,
        stickers=(("“独身の休日”の4日後に結婚報告", 640, 530, 40, RED, WHITE, -2),
                  ("「絶望ライン工」謝罪・活動休止", 640, 625, 40, NAVY, YELLOW, 2)),
        words=(("4日後!?", 190, 470, 72, WHITE, 10), ("おめでたいのに…", 1110, 455, 44, YELLOW, -8))),
}

if __name__ == "__main__":
    for name, v in THUMBS.items():
        make(os.path.join(HERE, "thumbs", name + ".png"), **v)
