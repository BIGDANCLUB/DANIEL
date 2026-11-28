"""テンポ系ショート用：壁かけ時計の絵（自作・透過）→ backgrounds/shorts_pic/pic_clock_HHMM.png"""
import math
import os
import sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make(hh, mm, night=False):
    S = 600
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = S / 2
    d.ellipse((6, 6, S - 6, S - 6), fill=(40, 40, 46, 255))
    face = (35, 45, 80, 255) if night else (250, 250, 248, 255)
    ink = (240, 240, 250) if night else (30, 30, 36)
    d.ellipse((34, 34, S - 34, S - 34), fill=face)
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = 238 if i % 5 else 222
        d.line((c + r1 * math.cos(a), c + r1 * math.sin(a), c + 250 * math.cos(a), c + 250 * math.sin(a)),
               fill=ink, width=10 if i % 5 == 0 else 3)
    ah = math.radians((hh % 12 + mm / 60) * 30 - 90)
    am = math.radians(mm * 6 - 90)
    d.line((c, c, c + 135 * math.cos(ah), c + 135 * math.sin(ah)), fill=ink, width=22)
    d.line((c, c, c + 205 * math.cos(am), c + 205 * math.sin(am)), fill=ink, width=12)
    d.ellipse((c - 18, c - 18, c + 18, c + 18), fill=(220, 40, 40))
    out = os.path.join(HERE, "backgrounds", "shorts_pic", "pic_clock_%02d%02d%s.png" % (hh, mm, "n" if night else ""))
    im.save(out)
    return out


if __name__ == "__main__":
    for t in sys.argv[1:]:   # 例 1755 2300n
        n = t.endswith("n")
        t = t.rstrip("n")
        print(make(int(t[:-2]), int(t[-2:]), n))
