"""12（赤い羽根募金、2.5億円が消えた）のサムネ（横 1280x720）。作りは make_thumb_11.py と同じ（猫の顔に文字を被せない）。

python3 catmeme/make_thumb_12.py → thumbs/12_akaihane.png
注意：元事務局長は「着服の疑い」。猫で演じない・名前や顔を出さない。猫は募金した人（被害者側）とニュース猫。
"""
import os

from make_thumb_03 import make

HERE = os.path.dirname(os.path.abspath(__file__))
NEWS, DON = (215, 35, 35), (35, 140, 65)
WHITE, YELLOW, RED, NAVY, BLACK = (255, 255, 255), (255, 222, 0), (235, 25, 25), (25, 32, 56), (0, 0, 0)

THUMB = dict(
    bg_dir="02_october", bg="bg15_convenience", ray_cols=((255, 40, 40), (255, 255, 255)),
    left=("surprise_big_pupils_cat", 0.6, False, "ニュース猫", NEWS), right=("sad_banana_cat_cry", 1.0, True, "募金した猫", DON),
    top="", big="", sub="", badge="", cat_h=360, tags=True,
    lines=(("赤い羽根募金", 70, 96, WHITE, BLACK, RED),
           ("2.5億円が消えた", 200, 150, YELLOW, BLACK, WHITE),
           ("善意はどこへ!?", 326, 96, RED, WHITE, BLACK)),
    stickers=(("1人で通帳も印鑑も管理", 640, 470, 44, NAVY, YELLOW, -2),
              ("今年は大臣も羽根をつけない", 640, 580, 38, WHITE, RED, 2)),
    words=())

if __name__ == "__main__":
    make(os.path.join(HERE, "thumbs", "12_akaihane.png"), **THUMB)
