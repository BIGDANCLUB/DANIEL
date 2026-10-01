"""猫ミーム長尺動画の画面部品（字幕枠・吹き出し・名前テロップ・解説カード）を作る。

すべて 1920x1080 の透過PNG（RGBA）で返すので、背景 → 猫 → 部品 の順に重ねて使う。
動画の書き出し時もこのモジュールの関数でその場で描く想定。
"""
import os
import urllib.request

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
FONTS = {
    "round": ("MPLUSRounded1c-ExtraBold.ttf", "ofl/mplusrounded1c/MPLUSRounded1c-ExtraBold.ttf"),
    "round_b": ("MPLUSRounded1c-Bold.ttf", "ofl/mplusrounded1c/MPLUSRounded1c-Bold.ttf"),
}

# 色
NAVY = (31, 42, 68)
INK = (34, 34, 34)
MUTED = (95, 100, 112)
CREAM = (255, 253, 247)
WHITE = (255, 255, 255)
YELLOW = (255, 212, 59)
ACCENT = (232, 116, 59)       # 強調（選ばれた人など）
BAR = (76, 111, 179)          # ふつうの棒
NEUTRAL = (154, 160, 172)     # 目立たせない棒
LINE = (226, 228, 234)

# レイアウト
SUB_BOX = (90, 850, W - 90, 1040)      # ナレーション字幕の枠
CARD_BOX = (110, 60, 1590, 800)        # 解説カード（右下は小さい猫用に空ける）
CAT_SLOT = (1600, 470, 1900, 830)      # 解説カード中に猫を置く場所


def font(kind, size):
    name, path = FONTS[kind]
    local = os.path.join(FONT_DIR, name)
    if not os.path.exists(local):
        os.makedirs(FONT_DIR, exist_ok=True)
        urllib.request.urlretrieve("https://raw.githubusercontent.com/google/fonts/main/" + path, local)
    return ImageFont.truetype(local, size)


def canvas():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def text_w(d, s, f):
    return d.textlength(s, font=f)


NO_HEAD = "、。，．・：；？！ー〜…」』）】!?)ぁぃぅぇぉっゃゅょァィゥェォッャュョ"


def wrap(d, text, f, max_w):
    """日本語を1文字ずつ折り返す（行頭に句読点などが来ないようにする）。"""
    lines = []
    for para in text.split("\n"):
        cur = ""
        for ch in para:
            if cur and text_w(d, cur + ch, f) > max_w and ch not in NO_HEAD:
                lines.append(cur)
                cur = ch
            else:
                cur += ch
        lines.append(cur)
    return lines


def fit(d, text, kind, size, max_w, max_lines, min_size=28):
    """max_lines 行に収まるまで文字を小さくする。"""
    while True:
        f = font(kind, size)
        lines = wrap(d, text, f, max_w)
        if len(lines) <= max_lines or size <= min_size:
            return f, lines
        size -= 4


def draw_lines(d, lines, f, cx, cy, fill, gap=1.25, stroke=0, stroke_fill=None, align="center", x0=None):
    lh = f.size * gap
    y = cy - lh * len(lines) / 2
    for ln in lines:
        if align == "center":
            x = cx - text_w(d, ln, f) / 2
        else:
            x = x0
        d.text((x, y + (lh - f.size) / 2 - f.size * 0.08), ln, font=f, fill=fill,
               stroke_width=stroke, stroke_fill=stroke_fill)
        y += lh


def shadow(img, box, radius, offset=8, alpha=70):
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle((x0 + offset, y0 + offset, x1 + offset, y1 + offset),
                                         radius, fill=(0, 0, 0, alpha))
    img.alpha_composite(sh)


# ---------- 字幕・吹き出し・名前 ----------

def subtitle(text=""):
    """ナレーション字幕（画面下の紺の帯＋白文字）。text 空なら枠だけ。"""
    img = canvas()
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = SUB_BOX
    d.rounded_rectangle(SUB_BOX, 28, fill=NAVY + (232,))
    d.rounded_rectangle((x0, y0, x0 + 18, y1), 9, fill=YELLOW + (255,))
    if text:
        f, lines = fit(d, text, "round", 64, x1 - x0 - 120, 2)
        draw_lines(d, lines, f, (x0 + x1) / 2 + 9, (y0 + y1) / 2, WHITE)
    return img


def bubble(text="", name="", cat_x=960, top=90, color=ACCENT):
    """猫のセリフの吹き出し。cat_x は猫の中心X（しっぽをそちらへ向ける）。"""
    img = canvas()
    d = ImageDraw.Draw(img)
    f, lines = fit(d, text or "　", "round", 70, 1300, 2)
    tw = max(text_w(d, ln, f) for ln in lines) if text else 600
    bw = int(min(max(tw + 120, 420), 1400))
    bh = int(f.size * 1.3 * len(lines) + 90)
    bx0 = int(min(max(cat_x - bw / 2, 60), W - 60 - bw))
    box = (bx0, top, bx0 + bw, top + bh)
    shadow(img, box, 44)
    tail_x = min(max(cat_x, bx0 + 80), bx0 + bw - 80)
    tail = [(tail_x - 34, top + bh - 6), (tail_x + 34, top + bh - 6), (tail_x + (cat_x - tail_x) * 0.3, top + bh + 70)]
    d.polygon(tail, fill=WHITE, outline=INK)
    d.rounded_rectangle(box, 44, fill=WHITE, outline=INK, width=6)
    d.line(tail[:2], fill=WHITE, width=10)
    d.line([tail[0], tail[2]], fill=INK, width=6)
    d.line([tail[1], tail[2]], fill=INK, width=6)
    if text:
        draw_lines(d, lines, f, bx0 + bw / 2, top + bh / 2, INK, gap=1.3)
    if name:
        nf = font("round", 36)
        nw = text_w(d, name, nf) + 48
        nb = (bx0 + 36, top - 30, bx0 + 36 + nw, top + 26)
        d.rounded_rectangle(nb, 28, fill=color, outline=WHITE, width=4)
        d.text((nb[0] + 24, nb[1] + 6), name, font=nf, fill=WHITE)
    return img


def name_tag(name, sub="", x=None, y=700, color=NAVY):
    """人物の名前テロップ（猫の足元あたりに出す）。x は中心X。"""
    img = canvas()
    d = ImageDraw.Draw(img)
    nf, sf = font("round", 54), font("round_b", 34)
    w = max(text_w(d, name, nf), text_w(d, sub, sf) if sub else 0) + 80
    h = 92 + (50 if sub else 0)
    cx = W / 2 if x is None else x
    box = (int(cx - w / 2), y, int(cx + w / 2), y + h)
    shadow(img, box, 20, offset=6)
    d.rounded_rectangle(box, 20, fill=WHITE, outline=color, width=6)
    d.rounded_rectangle((box[0], box[1], box[2], box[1] + 14), 6, fill=color)
    d.text((cx - text_w(d, name, nf) / 2, y + 22), name, font=nf, fill=INK)
    if sub:
        d.text((cx - text_w(d, sub, sf) / 2, y + 96), sub, font=sf, fill=MUTED)
    return img


# ---------- 解説カード ----------

def card(title, tag=""):
    """白いカード＋紺の見出し帯。(img, draw, 本文領域) を返す。"""
    img = canvas()
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = CARD_BOX
    shadow(img, CARD_BOX, 36, offset=12, alpha=80)
    d.rounded_rectangle(CARD_BOX, 36, fill=CREAM + (250,))
    d.rounded_rectangle((x0, y0, x1, y0 + 130), 36, fill=NAVY)
    d.rectangle((x0, y0 + 90, x1, y0 + 130), fill=NAVY)
    d.rectangle((x0, y0 + 130, x1, y0 + 138), fill=YELLOW)
    tf, tl = fit(d, title, "round", 64, x1 - x0 - 140 - (260 if tag else 0), 1)
    d.text((x0 + 60, y0 + 65 - tf.size * 0.62), tl[0], font=tf, fill=WHITE)
    if tag:
        gf = font("round", 34)
        gw = text_w(d, tag, gf) + 44
        gb = (x1 - 50 - gw, y0 + 38, x1 - 50, y0 + 94)
        d.rounded_rectangle(gb, 28, fill=YELLOW)
        d.text((gb[0] + 22, gb[1] + 7), tag, font=gf, fill=NAVY)
    return img, d, (x0 + 70, y0 + 180, x1 - 70, y1 - 50)


def bullets(title, items, tag="", size=58):
    img, d, (bx0, by0, bx1, by1) = card(title, tag)
    f = font("round", size)
    step = min((by1 - by0) / max(len(items), 1), size * 2.0)
    y = by0 + ((by1 - by0) - step * len(items)) / 2
    for it in items:
        cy = y + step / 2
        d.ellipse((bx0, cy - 14, bx0 + 28, cy + 14), fill=ACCENT)
        lines = wrap(d, it, f, bx1 - bx0 - 70)
        draw_lines(d, lines[:1], f, 0, cy, INK, align="left", x0=bx0 + 56)
        y += step
    return img


def bars(title, rows, tag="", note="", unit="票"):
    """横棒グラフ。rows = [(ラベル, 値, 強調するか, 右に付ける札)]。
    1系列なので凡例なし。値は棒の先に直接書く。強調は色＋札の2重で示す。"""
    img, d, (bx0, by0, bx1, by1) = card(title, tag)
    if note:
        by1 -= 60
        nf = font("round_b", 34)
        d.text((bx0, by1 + 14), note, font=nf, fill=MUTED)
    lf, vf, bf = font("round", 50), font("round", 54), font("round", 34)
    label_w = max(text_w(d, r[0], lf) for r in rows) + 40
    vmax = max(r[1] for r in rows)
    track = bx1 - bx0 - label_w - 380
    row_h = (by1 - by0) / len(rows)
    bar_h = min(84, row_h * 0.62)
    any_hi = any(r[2] for r in rows)
    ax = bx0 + label_w
    for i, (label, val, hi, badge) in enumerate(rows):
        cy = by0 + row_h * (i + 0.5)
        d.text((bx0, cy - lf.size * 0.62), label, font=lf, fill=INK)
        bw = max(track * val / vmax, 12)
        col = ACCENT if hi else (NEUTRAL if any_hi else BAR)
        d.rounded_rectangle((ax, cy - bar_h / 2, ax + bw, cy + bar_h / 2), 4, fill=col)
        d.rectangle((ax, cy - bar_h / 2, ax + 6, cy + bar_h / 2), fill=col)  # 根元は角を丸めない
        vs = f"{val:,}{unit}"
        vx = ax + bw + 20
        d.text((vx, cy - vf.size * 0.62), vs, font=vf, fill=INK)
        if badge:
            gx = vx + text_w(d, vs, vf) + 24
            gw = text_w(d, badge, bf) + 36
            d.rounded_rectangle((gx, cy - 30, gx + gw, cy + 30), 30, fill=ACCENT if hi else NAVY)
            d.text((gx + 18, cy - bf.size * 0.62), badge, font=bf, fill=WHITE)
    d.line((ax, by0, ax, by1), fill=LINE, width=4)
    return img


def flow(title, steps, tag=""):
    """①→②→③ の流れ図。steps = [(見出し, 説明)]。"""
    img, d, (bx0, by0, bx1, by1) = card(title, tag)
    n = len(steps)
    gap = 70
    bw = (bx1 - bx0 - gap * (n - 1)) / n
    hf, sf, nf = font("round", 46), font("round_b", 38), font("round", 40)
    for i, (head, sub) in enumerate(steps):
        x0 = bx0 + i * (bw + gap)
        last = i == n - 1
        box = (x0, by0 + 20, x0 + bw, by1 - 20)
        d.rounded_rectangle(box, 28, fill=WHITE, outline=ACCENT if last else BAR, width=6)
        cx = x0 + bw / 2
        d.ellipse((cx - 38, box[1] + 36, cx + 38, box[1] + 112), fill=ACCENT if last else BAR)
        d.text((cx - text_w(d, str(i + 1), nf) / 2, box[1] + 74 - nf.size * 0.62), str(i + 1), font=nf, fill=WHITE)
        hl = wrap(d, head, hf, bw - 50)
        draw_lines(d, hl, hf, cx, box[1] + 200, INK)
        sl = wrap(d, sub, sf, bw - 50)
        draw_lines(d, sl, sf, cx, box[1] + 330, MUTED, gap=1.35)
        if not last:
            ax = x0 + bw + 12
            ay = (box[1] + box[3]) / 2
            d.polygon([(ax, ay - 26), (ax + gap - 24, ay), (ax, ay + 26)], fill=NAVY)
    return img


def message(lines, sub="", opaque=False, size=86):
    """大きな1〜2行の文字（タイトル・まとめ・締め・注意書き）。"""
    img = Image.new("RGBA", (W, H), NAVY + (255,)) if opaque else canvas()
    d = ImageDraw.Draw(img)
    f = font("round", size)
    if not opaque:
        tw = max(text_w(d, ln, f) for ln in lines)
        hh = f.size * 1.35 * len(lines) + (90 if sub else 0) + 120
        box = (int(W / 2 - tw / 2 - 90), int(450 - hh / 2), int(W / 2 + tw / 2 + 90), int(450 + hh / 2))
        shadow(img, box, 40, offset=12, alpha=80)
        d.rounded_rectangle(box, 40, fill=CREAM + (250,), outline=NAVY, width=8)
        cy = 450 - (45 if sub else 0)
        draw_lines(d, lines, f, W / 2, cy, INK, gap=1.35)
        if sub:
            sf = font("round_b", 40)
            d.text((W / 2 - text_w(d, sub, sf) / 2, box[3] - 100), sub, font=sf, fill=MUTED)
    else:
        draw_lines(d, lines, f, W / 2, H / 2 - (40 if sub else 0), WHITE, gap=1.6)
        if sub:
            sf = font("round_b", 40)
            d.text((W / 2 - text_w(d, sub, sf) / 2, H / 2 + f.size * len(lines) * 0.8), sub, font=sf, fill=YELLOW)
    return img


def placeholder_bg(label="背景"):
    """確認用の仮背景（グラデーション＋仮の猫の位置）。"""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line((0, y, W, y), fill=(int(170 + 50 * t), int(200 + 30 * t), int(225 - 10 * t), 255))
    f = font("round_b", 40)
    d.text((40, 30), f"［仮の背景：{label}］", font=f, fill=(255, 255, 255, 200))
    return img


def placeholder_cat(img, box, label="猫"):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, 30, fill=(120, 120, 120, 170), outline=WHITE, width=4)
    f = font("round", 44)
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    d.text((cx - text_w(d, label, f) / 2, cy - 30), label, font=f, fill=WHITE)
