"""TikTokのロゴ（青緑と赤の音符マーク）と、その横の白い文字が猫の上に重なって残ったときに、周りの色で埋める。
clean_tiktok_greenscreen.py のあとに使う（緑の上のロゴはあちらで消える。猫に重なった分だけこちらで消す）。
usage: python3 wipe_tiktok_logo.py in.mp4 out.mp4 [最後に落とすフレーム数]
"""
import subprocess
import sys

import cv2
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
drop = int(sys.argv[3]) if len(sys.argv) > 3 else 0
cap = cv2.VideoCapture(src)
fps, W, H, N = cap.get(5), int(cap.get(3)), int(cap.get(4)), int(cap.get(7))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy",
                      "-shortest", dst], stdin=subprocess.PIPE)
i = 0
while True:
    ok, f = cap.read()
    if not ok or i >= N - drop:
        break
    b, g, r = [f[..., k].astype(int) for k in range(3)]
    green = (g > 120) & (g > r + 50) & (g > b + 50)
    logo = ((b > 170) & (g > 170) & (r < 130)) | ((r > 170) & (g < 90) & (b > 50))
    if logo.sum() > 15:
        near = cv2.dilate(logo.astype(np.uint8), np.ones((25, 60), np.uint8)) > 0   # 文字（TikTok・ユーザー名）はロゴのすぐ近く
        white = (f.min(2) > 200) & near
        m = cv2.dilate(((logo | white) & ~green).astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
        f = cv2.inpaint(f, m, 5, cv2.INPAINT_TELEA)
    p.stdin.write(f.tobytes())
    i += 1
p.stdin.close()
p.wait()
