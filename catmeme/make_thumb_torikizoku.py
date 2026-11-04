"""自堕落シリーズ #8 鳥貴族のサムネ（11/4 ユーザー指定：いつものAパターン・左に看板・右にむねスパ）。

python3 catmeme/make_thumb_torikizoku.py → thumbs/jidaraku_08_torikizoku_thumb_a.png
字幕：月曜の1人トリキは最高🦆／むねスパを金麦で流し込む（絵文字は Noto Color Emoji で描いて重ねる）
"""
import os

from PIL import Image, ImageDraw, ImageFont

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in (os.path.join("jidaraku", "08_torikizoku"), "jidaraku"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK, NV = T.RED, T.BLACK, T.NAVY
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
SIZE, TOP_H, SW = 104, 410, 8


def emoji(ch, h):
    f = ImageFont.truetype(EMOJI_FONT, 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def main():
    line1 = [("月曜の", BK), ("1人トリキ", R), ("は最高", BK), ("　 ", BK)]
    line2 = [("むねスパ", R), ("を", BK), ("金麦", R), ("で流し込む", BK)]
    name = "jidaraku_08_torikizoku_thumb_a.png"
    T.type_a(name, "t01_front", "f_mune_spice",
             ("happy_hamster_open_arms", 1.0, 330, 410, 300, False),
             [("eat_crunchy_cat_luna", 1.0, 1100, 410, 300, True)],
             "30代独身　一人飲み", line1, line2, split=640, size=SIZE)
    p = os.path.join(T.HERE, "thumbs", name)
    img = Image.open(p).convert("RGBA")
    # runs() と同じやり方で、実際の文字の大きさを求める（はみ出すと小さくなる）
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    size = SIZE
    while sum(d0.textlength(t, font=T.P.font("black", size)) for t, _ in line1) > T.W - 40 - SW * 2 and size > 30:
        size -= 3
    f = T.P.font("black", size)
    total = sum(d0.textlength(t, font=f) for t, _ in line1)
    text = sum(d0.textlength(t, font=f) for t, _ in line1[:-1])
    tw = int(total) + SW * 2 + 20
    x0 = (T.W - tw) // 2 + SW + 10
    em = emoji("🦆", int(size * 0.95))
    img.alpha_composite(em, (int(x0 + text + SW + 26), TOP_H + 40 + SW + int(size * 0.18)))
    img.convert("RGB").save(p)
    print("->", p)


if __name__ == "__main__":
    main()
