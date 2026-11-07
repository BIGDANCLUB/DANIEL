"""11（2,000万円の車を盗んだ疑いでも不起訴）のサムネ（横 1280x720）。作りは make_thumb_10.py と同じ。

python3 catmeme/make_thumb_11.py → thumbs/11_fukiso.png
注意：不起訴の人は罪に問われていない（猫で演じない・「犯人」と呼ばない）。国籍で煽らない。怒りは「理由を説明しない仕組み」と「被害者」に向ける。
"""
import os

from make_thumb_03 import make

HERE = os.path.dirname(os.path.abspath(__file__))
NEWS, VIC = (215, 35, 35), (35, 140, 65)
WHITE, YELLOW, RED, NAVY = (255, 255, 255), (255, 222, 0), (235, 25, 25), (25, 32, 56)

THUMB = dict(
    bg_dir="01_todai", bg="bg07_press", ray_cols=((255, 40, 40), (40, 0, 0)),
    left=("rage_talking_cat", 1.0, False, "ニュース猫", NEWS), right=("sad_banana_cat_cry", 1.0, True, "被害者", VIC),
    top="", big="", sub="", badge="",
    cat_h=360, tags=True,   # 猫の顔に文字が被らないよう、猫を小さめにして文字を上に寄せる
    lines=(("2,000万円の車を盗んだ疑いでも", 62, 76, WHITE, (0, 0, 0), RED),
           ("まさかの不起訴", 190, 150, YELLOW, (0, 0, 0), WHITE),
           ("日本はナメられてる!?", 318, 92, RED, WHITE, (0, 0, 0))),
    stickers=(("理由の説明なし", 640, 470, 46, NAVY, YELLOW, -2),
              ("仙台・横浜で不起訴が続く", 640, 580, 38, WHITE, RED, 2)),
    words=())

if __name__ == "__main__":
    make(os.path.join(HERE, "thumbs", "11_fukiso.png"), **THUMB)
