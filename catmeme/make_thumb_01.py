"""1本目（東大総長）のサムネイル 1280x720。python3 catmeme/make_thumb_01.py → catmeme/thumbs/01_todai.png"""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import parts as P
import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "thumbs", "01_todai.png")
W, H = 1280, 720


def cat_img(name, t, h, flip=False):
    c = R.Clip(name, flip=flip)
    bgr, a = c.frame(t)
    c.close()
    rgba = np.dstack([bgr[..., ::-1], (a * 255).astype(np.uint8)])
    rgba[:, :3, 3] = 0   # 端の1〜2列に残る縦線を消す
    rgba[:, -3:, 3] = 0
    rgba[:3, :, 3] = 0
    im = Image.fromarray(rgba, "RGBA")
    im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    arr = np.array(im)
    arr[:, -8:, 3] = 0   # 右端に残る白い縦線を消す
    return Image.fromarray(arr, "RGBA")


def outline(im, px, color):
    """透過画像のまわりに縁取りをつける。"""
    a = im.split()[-1].filter(ImageFilter.MaxFilter(px * 2 + 1))
    base = Image.new("RGBA", im.size, color)
    base.putalpha(a)
    base.alpha_composite(im)
    # 画像の端（体が枠で切れているところ）には縁取りを付けない
    arr = np.array(base)
    src = np.array(im)[..., 3]
    edge = np.zeros(src.shape, bool)
    m = px * 2 + 6
    edge[:, :m] = edge[:, -m:] = True
    edge[:m, :] = True
    arr[..., 3][edge & (src == 0)] = 0
    return Image.fromarray(arr, "RGBA")


def text(d, xy, s, size, fill, stroke, stroke_fill, anchor="la"):
    d.text(xy, s, font=P.font("black", size), fill=fill, stroke_width=stroke, stroke_fill=stroke_fill, anchor=anchor)


RED = (230, 20, 20)


def main(badge_parts=(("553", 1), (" ＞ ", 0), ("1107", 0)), out=OUT, cat=("surprise_big_pupils_cat", 0.6, False),
         band="東大の新総長", line1="投票2位が", line2="総長に!?", ray_cols=((255, 40, 40), (255, 210, 0)),
         line2_color=(255, 40, 40), band_color=(255, 220, 0), cat_left=False):
    bg = Image.open(os.path.join(HERE, "backgrounds", "01_todai", "bg06_spotlight.png")).convert("RGB").resize((W, H))
    img = bg.convert("RGBA")
    # 集中線（赤と黄色の放射）
    rays = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rays)
    cx, cy = 330, 400
    for i in range(36):
        a0 = np.deg2rad(i * 10)
        a1 = np.deg2rad(i * 10 + 5)
        r = 1600
        col = (*ray_cols[0], 150) if i % 2 else (*ray_cols[1], 120)
        rd.polygon([(cx, cy), (cx + r * np.cos(a0), cy + r * np.sin(a0)), (cx + r * np.cos(a1), cy + r * np.sin(a1))], fill=col)
    img.alpha_composite(rays)
    # 右側を暗くして文字を読みやすく
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for x in range(W):
        sd.line([(x, 0), (x, H)], fill=(0, 0, 0, int(max(0, (x - 420) / (W - 420)) * 150)))
    img.alpha_composite(shade)

    # 猫（驚く猫を大きく）
    cat = outline(cat_img(cat[0], cat[1], 640, cat[2]), 8, (255, 255, 255, 255))
    img.alpha_composite(cat, (0 if cat_left else max(0, 330 - cat.width // 2), H - cat.height + (0 if cat_left else 20)))

    d = ImageDraw.Draw(img)
    # 上の黄色い帯
    d.polygon([(470, 30), (1250, 30), (1230, 130), (450, 130)], fill=band_color)
    text(d, (850, 80), band, 76 if len(band) <= 9 else int(76 * 9 / len(band)), (20, 20, 20), 0, None, anchor="mm")
    # メインの文字
    text(d, (870, 222), line1, 128 if len(line1) <= 5 else int(128 * 5 / len(line1)), (255, 255, 255), 12, (0, 0, 0), anchor="mm")
    text(d, (870, 380), line2, min(172, int(172 * 740 / d.textlength(line2, font=P.font("black", 172)))), line2_color, 14, (255, 255, 255), anchor="mm")
    # 下の札（赤い部分と黒い部分を並べる。"\n" で2行）
    lines = [[]]
    for t, col in badge_parts:
        if t == "\n":
            lines.append([])
        else:
            lines[-1].append((t, col))
    size = 84 if len(lines) == 1 else 62
    f = P.font("black", size)
    tws = [sum(d.textlength(t, font=f) for t, _ in ln) for ln in lines]
    if max(tws) > 620:
        f = P.font("black", int(size * 620 / max(tws)))
        tws = [sum(d.textlength(t, font=f) for t, _ in ln) for ln in lines]
    lh = f.size * 1.15
    bw, bh = int(max(tws) + 70), int(lh * len(lines) + 46)
    badge = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    bd.rounded_rectangle((0, 0, bw - 1, bh - 1), 24, fill=(255, 255, 255), outline=(0, 0, 0), width=8)
    for i, (ln, tw) in enumerate(zip(lines, tws)):
        x, y = bw / 2 - tw / 2, 23 + lh * (i + 0.5)
        for t, col in ln:
            bd.text((x, y), t, font=f, fill=RED if col else (20, 20, 20), anchor="lm")
            x += bd.textlength(t, font=f)
    badge = badge.rotate(-4, expand=True, resample=Image.BICUBIC)
    bx = min(int(870 - badge.width / 2), W - badge.width - 8)
    img.alpha_composite(badge, (bx, H - badge.height - 6))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out)
    print("->", out)


# 札は 553 ＞ 1107 のまま、ほかを変えた案
VARIANTS = {
    "f": dict(cat=("huh_huh_cat", 1.0, False), band="東大の総長選", line1="1位なのに", line2="落選!?"),
    "g": dict(cat=("confused_i_dont_know_cat", 1.5, True), cat_left=True, band="意向投票の結果", line1="東大が選んだ", line2="まさかの2位",
              ray_cols=((40, 120, 255), (255, 210, 0)), line2_color=(255, 220, 0)),
    "h": dict(cat=("despair_dramatic_kitten", 1.0, False), band="過半数1107票", line1="投票の", line2="意味とは",
              ray_cols=((120, 40, 200), (255, 60, 120))),
    "i": dict(cat=("peek_what_happen_cat", 1.0, False), band="東大150年で初の女性総長", line1="でも投票は", line2="2位!?",
              ray_cols=((255, 120, 0), (255, 230, 0))),
    "j": dict(cat=("angry_shooting_cat", 1.0, False), band="東大の新総長", line1="ダブルスコア", line2="逆転!?",
              ray_cols=((255, 0, 0), (20, 20, 20)), band_color=(255, 255, 255)),
}

if __name__ == "__main__":
    main()
    for k, v in VARIANTS.items():
        main(out=OUT.replace(".png", f"_{k}.png"), **v)
