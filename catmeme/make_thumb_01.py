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


def main():
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
        col = (255, 40, 40, 150) if i % 2 else (255, 210, 0, 120)
        rd.polygon([(cx, cy), (cx + r * np.cos(a0), cy + r * np.sin(a0)), (cx + r * np.cos(a1), cy + r * np.sin(a1))], fill=col)
    img.alpha_composite(rays)
    # 右側を暗くして文字を読みやすく
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for x in range(W):
        sd.line([(x, 0), (x, H)], fill=(0, 0, 0, int(max(0, (x - 420) / (W - 420)) * 150)))
    img.alpha_composite(shade)

    # 猫（驚く猫を大きく）
    cat = outline(cat_img("surprise_big_pupils_cat", 0.6, 640), 8, (255, 255, 255, 255))
    img.alpha_composite(cat, (max(0, 330 - cat.width // 2), H - cat.height + 20))

    d = ImageDraw.Draw(img)
    # 上の黄色い帯
    d.polygon([(470, 30), (1250, 30), (1230, 130), (450, 130)], fill=(255, 220, 0))
    text(d, (850, 80), "東大の新総長", 76, (20, 20, 20), 0, None, anchor="mm")
    # メインの文字
    text(d, (870, 245), "投票2位が", 132, (255, 255, 255), 12, (0, 0, 0), anchor="mm")
    text(d, (870, 420), "総長に!?", 190, (255, 40, 40), 14, (255, 255, 255), anchor="mm")
    # 下の札（553＞1107）
    badge = Image.new("RGBA", (600, 140), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    bd.rounded_rectangle((0, 0, 599, 139), 24, fill=(255, 255, 255), outline=(0, 0, 0), width=8)
    f = P.font("black", 86)
    parts = [("553", (230, 20, 20)), (" ＞ ", (20, 20, 20)), ("1107", (20, 20, 20))]
    x = 300 - sum(bd.textlength(t, font=f) for t, _ in parts) / 2
    for t, col in parts:
        bd.text((x, 72), t, font=f, fill=col, anchor="lm")
        x += bd.textlength(t, font=f)
    badge = badge.rotate(-4, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(badge, (590, 552))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.convert("RGB").save(OUT)
    print("->", OUT)


if __name__ == "__main__":
    main()
