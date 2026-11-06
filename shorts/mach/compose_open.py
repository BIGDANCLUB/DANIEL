"""オープニング（0〜5秒）の試作：レンダ→色味→文字を重ねて mp4 にする。
usage: python3 compose_open.py frames_dir out.mp4"""
import glob
import os
import subprocess
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import overlay as O  # noqa: E402
from grade import grade, find_sun  # noqa: E402

src, out = sys.argv[1], sys.argv[2]
frames = sorted(glob.glob(os.path.join(src, "f_*.png")))
FPS = 30
WHITE, OR = (255, 255, 255), O.ORANGE
title1 = [("もしも", WHITE), ("新幹線", OR), ("が", WHITE)]
title2 = [("マッハ10", OR), ("で走っていたら？", WHITE)]
quote = ["東京駅から新横浜駅まで28.8km。", "今の「のぞみ」なら約18分"]
src_line = "東海道新幹線の時刻表より"

enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{O.W}x{O.H}",
                        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", out],
                       stdin=subprocess.PIPE)
sun = None
for i, p in enumerate(frames):
    base = Image.open(p).convert("RGB")
    if sun is None:
        sun = find_sun(base)
    g = grade(base, sun=sun).resize((O.W, O.H), Image.LANCZOS).convert("RGBA")
    t = i / FPS
    count = 5 - int(t)          # 出発まで 5→1
    O.watermark(g)
    O.opening(g, title1, title2, count if count >= 1 else None, quote, src_line)
    enc.stdin.write(g.convert("RGB").tobytes())
enc.stdin.close()
enc.wait()
print("done", out, len(frames))
