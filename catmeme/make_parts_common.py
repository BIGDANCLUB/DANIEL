"""全動画共通の画面部品を書き出す。

python3 catmeme/make_parts_common.py → catmeme/parts/common/*.png
- subscribe.png … 動画の最後の「チャンネル登録よろしく！」の画面（10/12 ユーザー指定。「→ ○本目もどうぞ」の画面の代わり）
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "common")
RED = (230, 30, 30)


def subscribe():
    img = Image.new("RGBA", (P.W, P.H), (24, 24, 30, 255))
    d = ImageDraw.Draw(img)
    # 斜めのしま（にぎやかし）
    for x in range(-P.H, P.W, 120):
        d.polygon([(x, P.H), (x + 60, P.H), (x + 60 + P.H, 0), (x + P.H, 0)], fill=(32, 32, 40, 255))
    cx = 760
    big = P.big_text("チャンネル登録", (90, 150, 1430, 420), max_size=190, max_lines=1, fill=P.WHITE)
    img.alpha_composite(big)
    # 赤いボタン
    bx0, by0, bx1, by1 = cx - 430, 470, cx + 430, 690
    d.rounded_rectangle((bx0 + 10, by0 + 14, bx1 + 10, by1 + 14), 40, fill=(90, 0, 0, 255))
    d.rounded_rectangle((bx0, by0, bx1, by1), 40, fill=RED + (255,))
    f = P.font("black", 130)
    d.text((cx, (by0 + by1) / 2 - 8), "登録する", font=f, fill=P.WHITE, anchor="mm")
    yoro = P.big_text("よろしく！", (90, 740, 1430, 1000), max_size=170, max_lines=1, fill=(255, 225, 0))
    img.alpha_composite(yoro)
    return img


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    subscribe().save(os.path.join(OUT, "subscribe.png"))
    print("->", OUT)
