"""個人情報流出ショート2本のサムネ（縦 1080x1920）。

python3 catmeme/make_thumb_short_04.py → thumbs/short_04a_license.png, thumbs/short_04b_coupon.png
作りは make_thumb_short_01.py と同じ（上：大きなタイトル／真ん中：パネル／下：猫2匹とひとこと）。
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import parts as P
from make_thumb_01 import cat_img, outline
from make_thumb_03 import fit_text

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
YELLOW, RED, WHITE, BLACK, NAVY, ORANGE = (255, 222, 0), (235, 25, 25), (255, 255, 255), (0, 0, 0), (25, 32, 56), (240, 110, 40)


def base(bg_name, ray_cols):
    bg = Image.open(os.path.join(HERE, "backgrounds", "04_leak", bg_name + ".png")).convert("RGB")
    bg = bg.resize((int(bg.width * H / bg.height), H))
    x0 = (bg.width - W) // 2
    img = bg.crop((x0, 0, x0 + W, H)).filter(ImageFilter.GaussianBlur(4)).convert("RGBA")
    rays = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rays)
    cx, cy = W / 2, H * 0.47
    for i in range(48):
        a0, a1 = np.deg2rad(i * 7.5), np.deg2rad(i * 7.5 + 3.6)
        rd.polygon([(cx, cy), (cx + 2400 * np.cos(a0), cy + 2400 * np.sin(a0)), (cx + 2400 * np.cos(a1), cy + 2400 * np.sin(a1))],
                   fill=ray_cols[i % 2])
    img.alpha_composite(rays)
    img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
    return img


def words(img, items):
    """猫のひとこと（斜めの縁取り文字）。items=[(文字, x, y, 大きさ, 色, 角度)]。"""
    d = ImageDraw.Draw(img)
    for text, x, y, size, col, rot in items:
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


def cats(img, left, right):
    """left/right=(素材, 時間の割合, 左右反転)。"""
    a = outline(cat_img(left[0], left[1], 620, left[2]), 9, (255, 255, 255, 255))
    b = outline(cat_img(right[0], right[1], 620, right[2]), 9, (255, 255, 255, 255))
    img.alpha_composite(a, (int(270 - a.width / 2), H - a.height - 40))
    img.alpha_composite(b, (int(810 - b.width / 2), H - b.height - 40))


def topic_band(img, text="個人情報流出"):
    """いちばん上の帯（何の話か一目でわかるように）。"""
    d = ImageDraw.Draw(img)
    d.polygon([(40, 70), (W - 40, 50), (W - 60, 200), (60, 215)], fill=RED)
    d.polygon([(40, 70), (W - 40, 50), (W - 60, 200), (60, 215)], outline=WHITE, width=8)
    fit_text(d, (W / 2, 135), text, 940, 120, WHITE, RED, sw_ratio=0.0)


def save(img, name):
    out = os.path.join(HERE, "thumbs", name + ".png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out)
    print("->", out)


def license_thumb():
    img = base("bg23_hacker_room", ((255, 40, 40, 150), (255, 210, 0, 120)))
    d = ImageDraw.Draw(img)
    topic_band(img, "個人情報流出")
    fit_text(d, (W / 2, 330), "免許証が", 1030, 150, WHITE, BLACK, double=None)
    fit_text(d, (W / 2, 520), "流出すると…？", 1040, 180, YELLOW, BLACK, double=WHITE)
    # 真ん中：「ローンが組めない」を大きく
    for k, (text, fill, fg, y, rot, size) in enumerate((("家や車のローンが\n組めない⁉", RED, WHITE, 680, -3, 118),)):
        f = P.font("black", size)
        lines = text.split("\n")
        bw, bh = 1020, int(size * 1.25 * len(lines)) + 50
        b = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        bd = ImageDraw.Draw(b)
        bd.rounded_rectangle((0, 0, bw - 1, bh - 1), 28, fill=fill, outline=BLACK if fill == WHITE else WHITE, width=9)
        for n, t in enumerate(lines):
            bd.text((bw / 2, 25 + size * 0.62 + n * size * 1.25), t, font=f, fill=fg, anchor="mm")
        b = b.rotate(rot, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(b, (int(W / 2 - b.width / 2), y))
    cats(img, ("huh_huh_cat", 1.0, False), ("surprise_big_pupils_cat", 0.6, True))
    words(img, [("は？", 230, 1250, 130, WHITE, 10), ("家も車も\nムリ！？", 800, 1260, 90, RED, -8)])
    save(img, "short_04a_license")


def coupon_thumb():
    img = base("bg26_phone_alert", ((255, 40, 40, 150), (255, 210, 0, 120)))
    d = ImageDraw.Draw(img)
    topic_band(img, "個人情報流出のあとに…")
    fit_text(d, (W / 2, 330), "その「お詫びクーポン」", 1030, 120, WHITE, BLACK, double=None)
    fit_text(d, (W / 2, 530), "押しちゃダメ⁉", 1040, 180, YELLOW, BLACK, double=WHITE)
    # 真ん中：スマホの通知ふう（実在の会社名は出さない）
    pw = Image.new("RGBA", (900, 330), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pw)
    pd.rounded_rectangle((0, 0, 900, 320), 40, fill=WHITE, outline=(200, 200, 200), width=4)
    pd.rounded_rectangle((30, 30, 120, 120), 20, fill=ORANGE)
    pd.text((75, 75), "!", font=P.font("black", 70), fill=WHITE, anchor="mm")
    pd.text((150, 75), "【お詫び】クーポンのお知らせ", font=P.font("black", 50), fill=BLACK, anchor="lm")
    pd.text((40, 175), "ご迷惑をおかけしました。", font=P.font("black", 42), fill=(80, 80, 80), anchor="lm")
    pd.text((40, 245), "こちらから受け取り → http://…", font=P.font("black", 42), fill=(30, 90, 220), anchor="lm")
    pw = pw.rotate(3, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(pw, (int(W / 2 - pw.width / 2), 680))
    stamp = Image.new("RGBA", (420, 150), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle((0, 0, 420, 150), 20, fill=RED, outline=WHITE, width=8)
    sd.text((210, 75), "偽物かも", font=P.font("black", 96), fill=WHITE, anchor="mm")
    stamp = stamp.rotate(-10, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(stamp, (int(W / 2 - stamp.width / 2 + 200), 930))
    cats(img, ("happy_girlfriend_dance_cat", 0.5, False), ("glare_disgusted_cat", 1.0, True))
    words(img, [("ラッキー♪", 250, 1240, 100, WHITE, 10), ("押すな！", 800, 1250, 120, RED, -8)])
    save(img, "short_04b_coupon")


if __name__ == "__main__":
    license_thumb()
    coupon_thumb()
