#!/usr/bin/env python3
"""元動画のフレームから焼き込み文字（タイトル・字幕）を消して背景画像を作る。

usage: python3 extract_plates.py source.mp4 outdir
"""
import os
import subprocess
import sys

import cv2
import numpy as np

from make_short import FF

# (名前, 取り出す秒, 字幕が短い行を選ぶと消し跡が小さい)
PLATES = [("room", 15.2), ("hall", 101.8), ("veranda", 117.6)]
# 文字が載っている領域 (y0, y1, x0, x1)
TEXT_BOXES = [(90, 460, 190, 890), (855, 1065, 0, 1080)]


def grab(src, t):
    raw = subprocess.run([FF, "-loglevel", "error", "-ss", str(t), "-i", src, "-frames:v", "1",
                          "-vf", "scale=1080:1920", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3).copy()


def clean(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    white = (v > 215) & (s < 60)
    yellow = (h > 18) & (h < 35) & (s > 120) & (v > 200)
    green = (h > 40) & (h < 80) & (s > 90) & (v > 180)
    fill = (white | yellow | green).astype(np.uint8)
    dark = (v < 45).astype(np.uint8)
    mask = np.zeros(frame.shape[:2], np.uint8)
    for y0, y1, x0, x1 in TEXT_BOXES:
        # 黒縁に接している明るい画素＝文字
        core = fill[y0:y1, x0:x1] & cv2.dilate(dark[y0:y1, x0:x1], np.ones((9, 9), np.uint8))
        mask[y0:y1, x0:x1] = cv2.dilate(core, np.ones((19, 19), np.uint8)) * 255
    return cv2.inpaint(frame, mask, 9, cv2.INPAINT_TELEA)


def main(src, outdir):
    os.makedirs(outdir, exist_ok=True)
    for name, t in PLATES:
        path = os.path.join(outdir, name + ".png")
        cv2.imwrite(path, clean(grab(src, t)))
        print(path)


if __name__ == "__main__":
    main(*sys.argv[1:3])
