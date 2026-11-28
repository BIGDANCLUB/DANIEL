"""11本目ショートのサムネ・派手版（ドーパミン多め）2案。縦 1080x1920。

python3 catmeme/make_thumb_short_11_dopa.py → thumbs/short_11_fukiso_dopa_a.png / _b.png
ルールは本編と同じ：不起訴の人は描かない・「犯人」と言わない・国籍で煽らない（サムネに国籍は入れない）。
"""
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw

import parts as P
import short_hooks as H
import short_refstyle as M

HERE = M.HERE
SW, SH = M.SW, M.SH
WHITE, BLACK, RED, YELLOW = (255, 255, 255), (0, 0, 0), (235, 25, 25), (255, 225, 0)
LIME = (120, 235, 40)


def outline(text, size, fill, stroke=BLACK, sw=None, w=SW - 20, angle=0.0):
    """極太の縁取り文字（2重縁）。"""
    f = P.font("black", size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    lines = text.split("\n")
    while max(d0.textlength(ln, font=f) for ln in lines) > w - 60 and size > 40:
        size -= 6
        f = P.font("black", size)
    sw = sw or max(10, size // 7)
    lh = int(size * 1.12)
    tw = int(max(d0.textlength(ln, font=f) for ln in lines)) + sw * 4 + 20
    im = Image.new("RGBA", (tw, lh * len(lines) + sw * 4 + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        x = (tw - d.textlength(ln, font=f)) / 2
        y = sw * 2 + i * lh
        d.text((x, y), ln, font=f, fill=WHITE if stroke == BLACK else BLACK, stroke_width=sw + 10,
               stroke_fill=WHITE if stroke == BLACK else BLACK)
        d.text((x, y), ln, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
    return im.rotate(angle, expand=True, resample=Image.BICUBIC) if angle else im


def stamp(text, size=170, col=RED, angle=-12):
    """ハンコふうの札（赤い枠＋赤い文字、白地）。"""
    f = P.font("black", size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = int(d0.textlength(text, font=f)) + 110
    th = int(size * 1.3) + 70
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, tw - 1, th - 1), 26, fill=WHITE, outline=col, width=22)
    d.rounded_rectangle((26, 26, tw - 27, th - 27), 16, outline=col, width=6)
    d.text((tw / 2, th / 2), text, font=f, fill=col, anchor="mm")
    return im.rotate(angle, expand=True, resample=Image.BICUBIC)


def band(text, col, fg=WHITE, size=78, angle=0.0):
    f = P.font("black", size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = int(d0.textlength(text, font=f)) + 80
    im = Image.new("RGBA", (tw, int(size * 1.5)), col + (255,))
    ImageDraw.Draw(im).text((tw / 2, im.height / 2), text, font=f, fill=fg, anchor="mm")
    return im.rotate(angle, expand=True, resample=Image.BICUBIC)


def save(out, name):
    p = os.path.join(HERE, "thumbs", name)
    cv2.imwrite(p, (np.clip(out, 0, 1) * 255).astype(np.uint8))
    print("->", p)


def thumb_a():
    """A：赤×黄の回る集中線に、巨大な「不起訴」のハンコ。怒る猫と泣く猫を大きく。"""
    out = H.blank((200, 10, 10))
    H.rays(out, 0.0, cols=((255, 40, 40), (255, 215, 0)), cy=0.52, alpha=0.95)
    H.cat(out, "rage_talking_cat", 1.0, 270, SH + 260, 900)
    H.cat(out, "sad_banana_cat_cry", 1.0, 820, SH + 60, 820, flip=True)
    H.put(out, outline("2,000万円の車\n盗んだ疑いで逮捕", 112, YELLOW), SW / 2, 260)
    H.put(out, outline("→ 結果", 110, WHITE), SW / 2, 540)
    H.put(out, stamp("不起訴", 210), SW / 2, 850)
    H.put(out, outline("はああああ！？", 116, RED, WHITE, angle=6), SW / 2, 1110)
    H.put(out, band("理由は説明なし", BLACK, YELLOW, 70, angle=-4), SW / 2, 1270)
    H.put(out, outline("車の持ち主", 76, LIME), 830, SH - 110)
    save(out, "short_11_fukiso_dopa_a.png")


def thumb_b():
    """B：黒地に黄色の巨大「2,000万円」→ 赤い「パー」。泣くバナナ猫をど真ん中にアップ。"""
    out = H.blank((15, 15, 15))
    H.rays(out, 0.0, cols=((60, 60, 60), (25, 25, 25)), cy=0.62, alpha=1.0)
    H.cat(out, "sad_banana_cat_cry", 1.0, SW / 2, SH + 60, 1250)
    H.put(out, outline("2,000万円", 230, YELLOW), SW / 2, 260)
    H.put(out, outline("盗まれて", 120, WHITE), SW / 2, 440)
    H.put(out, stamp("不起訴", 180, angle=8), SW / 2, 730)
    H.put(out, outline("殴られても\n不起訴", 100, RED, WHITE, angle=-8), 250, 930)
    H.put(out, outline("理由は\nナシ！？", 100, YELLOW, angle=8), 840, 940)
    H.put(out, band("被害者 泣き寝入り", RED, WHITE, 86), SW / 2, SH - 110)
    save(out, "short_11_fukiso_dopa_b.png")


if __name__ == "__main__":
    thumb_a()
    thumb_b()
