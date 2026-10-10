"""参考マネのショート（免許証が漏れるとヤバすぎる）のサムネ（縦 1080x1920）。動画と同じ見た目で、いちばん強い場面を1枚に。

python3 catmeme/make_thumb_refstyle.py → thumbs/short_refstyle_license.png
"""
import os

import cv2
import numpy as np

import short_refstyle as M

HERE = M.HERE
OUT = os.path.join(HERE, "thumbs", "short_refstyle_license.png")


def main():
    title = M.title_band("閲覧注意", "免許証が漏れるとヤバすぎる")
    c = M.cut(M.HOME, "免許証が漏れたら\n*ブラック入り*！？", [("sad_banana_cat_cry", M.L, 1050, False), ("angry_aiming_cat", M.Rr, 1050, True)],
              label=M.HAN, size=130)
    for k in c["cats"]:
        k["pop"] = False
    f = M.make_draw(c, title)(1.0)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv2.imwrite(OUT, (np.clip(f, 0, 1) * 255).astype(np.uint8))
    print("->", OUT)


if __name__ == "__main__":
    main()
