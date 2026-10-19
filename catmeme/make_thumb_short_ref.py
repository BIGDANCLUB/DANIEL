"""ショートのサムネ：参考フォーマット（ユーザー指定 10/13）をマネして作る。縦 1080x1920。

参考3枚（「外国人が思わず撮影！日本の子供に衝撃！」「整備工場にトヨタが来た時の海外の反応」「帰国直後に衝撃 日本との違い」）の作り
- 上：黒い帯に2行の極太ゴシック。1行目と2行目で色を変える（赤×黄／黄×オレンジ／黄×ピンク）。行いっぱいの大きさ
- 真ん中〜下：写真を全面に（帯のすぐ下から一番下まで）。猫ミームは写真の中に入れ込む
- 写真の中ほど〜下に、ひとことテロップを1つ（3種類）
    a) 青い文字＋白い縁を、半透明の白いぼかし帯にのせる（「日本の日常の光景。」）
    b) 赤い文字＋黒い太縁、少し傾ける（「40年ぶりだぞ!!」）
    c) 白い文字＋青い縁を2行、暗い半透明の帯にのせる（「こんなこと日本では…」）
- 写真を借りたときは、左下に小さく灰色で「引用元：○○」
- いちばん下の白いタイトルはYouTubeの画面の表示なので、サムネには入れない
- YouTube の一覧では上下が少し切れる（約9:14）ので、大事な物は y=140〜1780 の中に置く

python3 catmeme/make_thumb_short_ref.py → thumbs/short_12_akaihane_ref_a.png / _b / _c
"""
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import parts as P
import render as R
import short_hooks as H

HERE = os.path.dirname(os.path.abspath(__file__))
SW, SH = 1080, 1920
BAND_H = 560            # 黒い帯の下端（2行とも横いっぱいの大きな文字。一覧では上が約140切れる）
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, YELLOW, ORANGE, PINK, BLUE = (232, 28, 36), (255, 228, 0), (255, 108, 24), (240, 56, 120), (24, 84, 200)
DEEP_YELLOW = (255, 190, 0)   # 白い縁の明るい黄色は見にくい（10/14 ユーザー指定）→ 濃い黄色＋黒い縁
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("added", "13_yard", "14_japan", "15_vambi", "16_tenchim", "17_imamori", "17_imamori/photos", "18_semicon", "18_story", "19_inawashiro", "02_october", "01_todai", "04_leak", "03_kodomo_nisa", "02_october", "01_todai")]


def bg_path(n):
    for d in BGS:
        p = os.path.join(d, n + ".png")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(n)


def photo(name, zoom=1.0, cx=0.5):
    """背景を帯の下の全面に敷く（縦に合わせて拡大し、cx の位置で切り出す）。"""
    im = Image.open(bg_path(name)).convert("RGB")
    h = SH - BAND_H
    k = h / im.height * zoom
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    x0 = int((im.width - SW) * cx)
    y0 = (im.height - h) // 2
    return im.crop((x0, y0, x0 + SW, y0 + h))


def heavy(text, size, fill, stroke, sw, w=SW - 30):
    """極太ゴシックを1行。横幅に収まるまで小さくする。"""
    f = P.font("black", size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    while d0.textlength(text, font=f) > w - sw * 2 and size > 40:
        size -= 4
        f = P.font("black", size)
    tw = int(d0.textlength(text, font=f)) + sw * 2 + 10
    im = Image.new("RGBA", (tw, int(size * 1.3) + sw * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((sw + 5, sw), text, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
    return im.crop(im.getbbox())


def caption(text, style, col=RED):
    lines = text.split("\n")
    if style == "a":     # 青い文字＋白い縁、半透明の白いぼかし帯
        t = heavy(text, 92, BLUE, WHITE, 9, w=SW - 160)
        pad = Image.new("RGBA", (t.width + 120, t.height + 60), (255, 255, 255, 120)).filter(ImageFilter.GaussianBlur(6))
        pad.alpha_composite(t, (60, 30))
        return pad, 0
    if style == "b":     # 赤い文字＋黒い太縁、少し傾ける
        t = heavy(text, 120, col, BLACK, 12, w=SW - 120)
        return t.rotate(4, expand=True, resample=Image.BICUBIC), 0
    # c: 白い文字＋青い縁を2行、暗い半透明の帯
    ts = [heavy(ln, 76, WHITE, BLUE, 8, w=SW - 140) for ln in lines]
    w, h = max(t.width for t in ts) + 80, sum(t.height + 16 for t in ts) + 40
    pad = Image.new("RGBA", (w, h), (20, 30, 60, 150))
    y = 20
    for t in ts:
        pad.alpha_composite(t, ((w - t.width) // 2, y))
        y += t.height + 16
    return pad, 0


def make(out_name, line1, col1, line2, col2, bg, cats, cap, cap_style, cap_y=1220, credit="", zoom=1.0, cx=0.5,
         stroke1=BLACK, cap_col=RED):
    img = Image.new("RGB", (SW, SH), BLACK)
    img.paste(photo(bg, zoom, cx), (0, BAND_H))
    out = np.asarray(img)[:, :, ::-1].astype(np.float32) / 255
    for name, t, x, bottom, h, flip in cats:   # 猫ミームを写真の中に入れ込む
        H.cat(out, name, t, x, bottom, h, flip=flip)
    pil = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)[:, :, ::-1]).convert("RGBA")
    # 上の黒い帯（2行）
    t1 = heavy(line1, 190, col1, stroke1, 6)   # 参考どおり1行8〜10文字で、横いっぱいの大きさ
    t2 = heavy(line2, 190, col2, BLACK, 6)
    gap = 30
    top = 150 + (BAND_H - 150 - t1.height - t2.height - gap) // 2
    pil.alpha_composite(t1, ((SW - t1.width) // 2, top))
    pil.alpha_composite(t2, ((SW - t2.width) // 2, top + t1.height + gap))
    # ひとことテロップ
    c, _ = caption(cap, cap_style, cap_col)
    pil.alpha_composite(c, ((SW - c.width) // 2, int(cap_y - c.height / 2)))
    if credit:
        ImageDraw.Draw(pil).text((40, 1700), "引用元：" + credit, font=P.font("round_b", 34), fill=(190, 190, 190, 255))
    p = os.path.join(HERE, "thumbs", out_name)
    pil.convert("RGB").save(p)
    print("->", p)


def akaihane():
    """12本目（赤い羽根）で3案。1行8〜10文字。"""
    make("short_12_akaihane_ref_a.png", "国税が来て発覚！", RED, "赤い羽根2.5億円", YELLOW,
         "bg35_akaihane_box", [("sad_banana_cat_cry", 1.0, 820, 1880, 640, True), ("surprise_big_pupils_cat", 0.6, 230, 1900, 560, False)],
         "2.5億円が消えた!!", "b", cap_y=880, stroke1=WHITE)
    make("short_12_akaihane_ref_b.png", "大臣が赤い羽根を", YELLOW, "つけなかった理由", ORANGE,
         "bg36_akaihane_bow", [("huh_huh_cat", 1.0, 540, 1940, 820, False)], "2.5億円が消えた!!", "b", cap_y=1180)
    make("short_12_akaihane_ref_c.png", "通帳も印鑑も1人", YELLOW, "赤い羽根の闇", PINK,
         "bg34_akaihane_full", [("glare_disgusted_cat", 1.0, 540, 1960, 760, False)],
         "こんなこと普通の会社では\n絶対ありえないんだけど…", "c", cap_y=1600)


def yard():
    """13本目（盗難ハイエース）のショート2本ぶん。1行8〜10文字。逮捕された人は描かない。"""
    make("short_13_yard_ref.png", "盗難ハイエース", DEEP_YELLOW, "容疑はたった1台", RED,
         "bg41_yard_scrap", [("surprise_big_pupils_cat", 0.6, 250, 1900, 620, False), ("sad_banana_cat_cry", 1.0, 830, 1880, 600, True)],
         "300台なのに!?", "b", cap_y=900)
    make("short_13b_yard_ref.png", "盗難が減った理由", DEEP_YELLOW, "まさかの“海峡”", RED,
         "bg42_yard_raid_ai", [("huh_huh_cat", 1.0, 560, 1960, 900, False)],
         "対策じゃなかった!?", "b", cap_y=1000)


def tenchim():
    """16本目（てんちむ）のショート2本ぶん。背景はユーザー提供の本人の写真。猫は顔にも字幕にもかけない（字幕より上・左右の端）。
    10/15 ユーザー指定：「賠償」だと分かる文言、結果ではなく「どうやって!?」と中身を気にさせるひとこと。"""
    make("short_16_tenchim_ref.png", "てんちむ3.8億円賠償", DEEP_YELLOW, "まさかの0円に", RED,
         "bg81_tenchim_neon", [("surprise_big_pupils_cat", 0.6, 120, 1440, 400, False), ("excited_hodomoe_city_cat", 1.0, 960, 1440, 420, True)],
         "どうやって覆した!?", "b", cap_y=1640)
    make("short_16b_tenchim_ref.png", "この元子役が", DEEP_YELLOW, "返金負担4億円超", RED,
         "bg92_tenchim_child", [("stare_big_eyes_tabby_kitten", 1.0, 120, 1440, 400, False), ("huh_huh_cat", 1.0, 900, 1560, 400, True)],
         "なぜ自腹で!?", "b", cap_y=1640)


def imamori():
    """17本目（今森茉耶）のショート2本ぶん。背景はユーザー提供の写真。猫は顔にも字幕にもかけない（字幕より上・右の端）。
    ひとことは濃い黄色で、画面の下（隠れるところ）より上に（10/16 ユーザー指定）。"""
    make("short_17_imamori_ref.png", "元戦隊ヒロイン", DEEP_YELLOW, "再出発から6日", RED,
         "p6_event_portrait", [("stare_big_eyes_tabby_kitten", 1.0, 840, 1240, 360, True)],
         "何があった!?", "b", cap_y=1420, cx=0.2, cap_col=DEEP_YELLOW)
    make("short_17b_imamori_ref.png", "放送中に", DEEP_YELLOW, "ヒロイン交代", RED,
         "p7_cast_announcement", [("surprise_big_pupils_cat", 0.6, 150, 1250, 300, False)],
         "番組はどうした!?", "b", cap_y=1420, cx=0.18, cap_col=DEEP_YELLOW)


def inawashiro():
    """19本目（猪苗代湖ボート事故）のショート。人が亡くなった事故なので落ち着いた猫だけ。事故の様子は描かない。"""
    make("short_19_inawashiro_ref.png", "猪苗代湖ボート事故", DEEP_YELLOW, "最高裁で逆転有罪", RED,
         "bg104_supreme_court", [("realize_wet_cat_stare", 1.0, 870, 1240, 340, True)],
         "なぜ覆った？", "b", cap_y=1420, cap_col=DEEP_YELLOW)


if __name__ == "__main__":
    import sys
    {"12": akaihane, "13": yard, "16": tenchim, "17": imamori, "19": inawashiro}[sys.argv[1] if len(sys.argv) > 1 else "13"]()
