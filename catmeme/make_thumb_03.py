"""3本目（こどもNISA）のサムネイル 1280x720。python3 catmeme/make_thumb_03.py → catmeme/thumbs/03_kodomo_nisa*.png

参考（ニャースインフォのサムネ）: 猫を左右に大きく・極太の縁取り文字・赤と黄色の強調・上に小さな帯
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import parts as P
from make_thumb_01 import cat_img, outline

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "thumbs", "03_kodomo_nisa.png")
W, H = 1280, 720
YELLOW, RED, WHITE, BLACK = (255, 222, 0), (235, 25, 25), (255, 255, 255), (0, 0, 0)


def fit_text(d, xy, s, max_w, size, fill, stroke_fill, sw_ratio=0.13, anchor="mm", double=None):
    f = P.font("black", size)
    while d.textlength(s, font=f) > max_w and size > 30:
        size -= 4
        f = P.font("black", size)
    sw = max(6, int(size * sw_ratio))
    if double:   # 2重の縁取り（外側 double、内側 stroke_fill）
        d.text(xy, s, font=f, fill=double, stroke_width=sw + 8, stroke_fill=double, anchor=anchor)
    d.text(xy, s, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke_fill, anchor=anchor)


def tag(img, text, color, cx, y, size=40):
    t = P.label_tag(text, color, size=size)
    img.alpha_composite(t, (int(cx - t.width / 2), int(y)))


def make(out, left, right, top, big, sub, badge="年60万円・最大600万円", ray_cols=((255, 60, 60), (255, 220, 0)), bg="bg19_kids_room",
         cat_h=470, extras=(), words=(), tags=True, bg_dir="03_kodomo_nisa"):
    path = os.path.join(HERE, "backgrounds", bg_dir, bg + ".png")
    img = Image.open(path).convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(3)).convert("RGBA")
    # 集中線
    rays = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rays)
    cx, cy = W / 2, H * 0.48
    for i in range(48):
        a0, a1 = np.deg2rad(i * 7.5), np.deg2rad(i * 7.5 + 3.6)
        col = (*ray_cols[i % 2], 140)
        rd.polygon([(cx, cy), (cx + 1600 * np.cos(a0), cy + 1600 * np.sin(a0)), (cx + 1600 * np.cos(a1), cy + 1600 * np.sin(a1))], fill=col)
    img.alpha_composite(rays)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 70))
    img.alpha_composite(shade)
    # 猫（左右に大きく）
    for name, t, flip, x, h, bottom in extras:   # 脇役の小さい猫ミーム（大きい猫より奥）
        c = outline(cat_img(name, t, h, flip), 6, (255, 255, 255, 255))
        img.alpha_composite(c, (int(x - c.width / 2), int(bottom - c.height)))
    for (name, t, flip, role, color), x in ((left, 230), (right, 1050)):
        c = outline(cat_img(name, t, cat_h, flip), 8, (255, 255, 255, 255))
        img.alpha_composite(c, (int(x - c.width / 2), H - c.height + 10))
        if tags:
            tag(img, role, color, x, H - 78, size=42)
    d = ImageDraw.Draw(img)
    # 上の帯
    d.polygon([(250, 18), (1030, 18), (1010, 98), (270, 98)], fill=RED)
    fit_text(d, (640, 58), top, 720, 56, WHITE, RED, sw_ratio=0.0)
    # メインの大きな文字
    fit_text(d, (640, 225), big, 1180, 190, YELLOW, BLACK, double=WHITE)
    fit_text(d, (640, 400), sub, 760, 120, RED, WHITE, double=BLACK)
    # 下の真ん中の札（数字）
    if not badge:
        badge = None
    f = P.font("black", 56)
    tw = d.textlength(badge or "", font=f)
    bx0, by0 = 640 - tw / 2 - 30, 520
    b = Image.new("RGBA", (int(tw + 60), 100), (0, 0, 0, 0))
    bd = ImageDraw.Draw(b)
    bd.rounded_rectangle((0, 0, b.width - 1, 99), 20, fill=WHITE, outline=BLACK, width=7)
    bd.text((b.width / 2, 52), badge or "", font=f, fill=BLACK, anchor="mm")
    b = b.rotate(3, expand=True, resample=Image.BICUBIC)
    if badge:
        img.alpha_composite(b, (int(640 - b.width / 2), 515))
    # 猫のまわりの手書き風のひとこと（傾けて置く）
    for text, x, y, size, col, rot in words:
        f = P.font("black", size)
        tw = int(d.textlength(text, font=f)) + 40
        w = Image.new("RGBA", (tw, size + 40), (0, 0, 0, 0))
        ImageDraw.Draw(w).text((tw / 2, (size + 40) / 2), text, font=f, fill=col, stroke_width=max(5, size // 9),
                               stroke_fill=BLACK if col != BLACK else WHITE, anchor="mm")
        w = w.rotate(rot, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(w, (int(x - w.width / 2), int(y - w.height / 2)))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out)
    print("->", out)


NEWS, SAGE, PAPA = (215, 35, 35), (40, 90, 200), (35, 140, 65)
VARIANTS = {
    "": dict(left=("surprise_big_pupils_cat", 0.6, False, "ニュース猫", NEWS), right=("huh_huh_cat", 1.0, False, "パパ猫", PAPA),
             top="2027年スタート　受付はもう始まった", big="こどもNISA", sub="結局お得なの!?"),
    "_b": dict(left=("despair_dramatic_kitten", 1.0, False, "パパ猫", PAPA), right=("glare_disgusted_cat", 1.0, False, "ニュース猫", NEWS),
               top="親のNISAと何が違う？", big="こどもNISA", sub="損する家もある!?", badge="18歳で子どものお金に",
               ray_cols=((120, 40, 200), (255, 60, 120))),
    "_c": dict(left=("weird_meowing_cat", 1.0, False, "ニュース猫", NEWS), right=("calm_black_face_sheep", 1.0, False, "博識な猫", SAGE),
               top="0歳から非課税で投資できる", big="こどもNISA", sub="親ガチャ強化!?", badge="余裕のある家ほど有利？",
               ray_cols=((255, 120, 0), (255, 230, 0))),
    # 猫ミーム感を強めた版（Cベース）：おなじみの猫を増やし、猫のひとことを散らす
    "_d": dict(left=("huh_huh_cat", 1.0, False, "ニュース猫", NEWS), right=("sad_banana_cat_cry", 1.0, False, "ニュース猫", NEWS),
               top="0歳から非課税で投資できる", big="こどもNISA", sub="親ガチャ強化!?", badge="",
               ray_cols=((255, 120, 0), (255, 230, 0)), cat_h=480, tags=False,
               extras=(("excited_hodomoe_city_cat", 0.8, False, 450, 270, 735), ("laugh_laughing_dog", 0.8, False, 700, 270, 735)),
               words=(("はぁ？", 150, 505, 92, WHITE, 12), ("ずるい…", 1150, 345, 64, (120, 200, 255), -10),
                      ("ﾙﾝﾙﾝ♪", 450, 480, 54, YELLOW, 8), ("勝ち組www", 710, 480, 54, YELLOW, -8))),
}

if __name__ == "__main__":
    for k, v in VARIANTS.items():
        make(OUT.replace(".png", k + ".png"), **v)
