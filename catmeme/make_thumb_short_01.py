"""東大総長選ショートのサムネ（縦 1080x1920）。python3 catmeme/make_thumb_short_01.py → thumbs/short_01_todai.png

ショート一覧では真ん中あたりが大きく見えるので、文字と猫を中央に寄せる。
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import parts as P
from make_thumb_01 import cat_img, outline
from make_thumb_03 import fit_text

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "thumbs", "short_01_todai.png")
W, H = 1080, 1920
YELLOW, RED, WHITE, BLACK, NAVY, ORANGE = (255, 222, 0), (235, 25, 25), (255, 255, 255), (0, 0, 0), (25, 32, 56), (240, 110, 40)


def main():
    bg = Image.open(os.path.join(HERE, "backgrounds", "01_todai", "bg01_campus.png")).convert("RGB")
    bg = bg.resize((int(bg.width * H / bg.height), H)).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(4))
    img = bg.convert("RGBA")
    rays = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rays)
    cx, cy = W / 2, H * 0.47
    for i in range(48):
        a0, a1 = np.deg2rad(i * 7.5), np.deg2rad(i * 7.5 + 3.6)
        rd.polygon([(cx, cy), (cx + 2400 * np.cos(a0), cy + 2400 * np.sin(a0)), (cx + 2400 * np.cos(a1), cy + 2400 * np.sin(a1))],
                   fill=((255, 120, 0, 150) if i % 2 else (255, 230, 0, 130)))
    img.alpha_composite(rays)
    img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 60)))
    d = ImageDraw.Draw(img)
    # 上：タイトル
    fit_text(d, (W / 2, 260), "東大の総長選", 1030, 170, WHITE, BLACK, double=None)
    fit_text(d, (W / 2, 500), "2位が勝った⁉", 1040, 220, YELLOW, BLACK, double=WHITE)
    # 真ん中：VS パネル
    pw = Image.new("RGBA", (W, 330), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pw)
    for k, (head, val, foot, col) in enumerate((("投票1位", "1,107票", "→ 選ばれず", NAVY), ("投票2位", "553票", "→ 総長に！", ORANGE))):
        x0 = 50 + k * 540
        pd.rounded_rectangle((x0, 0, x0 + 440, 320), 30, fill=WHITE, outline=col, width=12)
        pd.rounded_rectangle((x0, 0, x0 + 440, 100), 30, fill=col)
        pd.text((x0 + 220, 52), head, font=P.font("black", 64), fill=WHITE, anchor="mm")
        pd.text((x0 + 220, 175), val, font=P.font("black", 96), fill=col if k else BLACK, anchor="mm")
        pd.text((x0 + 220, 268), foot, font=P.font("black", 56), fill=RED if k else (110, 110, 110), anchor="mm")
    pd.text((W / 2, 175), "＜", font=P.font("black", 110), fill=RED, stroke_width=6, stroke_fill=WHITE, anchor="mm")
    pw = pw.rotate(-3, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(pw, (int(W / 2 - pw.width / 2), 760))
    # 下：猫
    left = outline(cat_img("glare_disgusted_cat", 1.0, 620), 9, (255, 255, 255, 255))
    right = outline(cat_img("surprise_big_pupils_cat", 0.6, 620, True), 9, (255, 255, 255, 255))
    img.alpha_composite(left, (int(270 - left.width / 2), H - left.height - 40))
    img.alpha_composite(right, (int(810 - right.width / 2), H - right.height - 40))
    d = ImageDraw.Draw(img)
    for text, x, y, size, col, rot in (("は？", 230, 1240, 130, WHITE, 10), ("1位の人\nどこいった！？", 790, 1250, 80, RED, -8)):
        f = P.font("black", size)
        lines = text.split("\n")
        tw = int(max(d.textlength(t, font=f) for t in lines)) + 60
        w = Image.new("RGBA", (tw, int(size * 1.25 * len(lines)) + 40), (0, 0, 0, 0))
        wd = ImageDraw.Draw(w)
        for j, t in enumerate(lines):
            yy = 20 + size * 0.6 + j * size * 1.25
            if col == RED:
                wd.text((tw / 2, yy), t, font=f, fill=WHITE, stroke_width=size // 8 + 6, stroke_fill=BLACK, anchor="mm")
            wd.text((tw / 2, yy), t, font=f, fill=col, stroke_width=size // 8, stroke_fill=WHITE if col == RED else BLACK, anchor="mm")
        w = w.rotate(rot, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(w, (int(x - w.width / 2), int(y - w.height / 2)))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.convert("RGB").save(OUT)
    print("->", OUT)


if __name__ == "__main__":
    main()
