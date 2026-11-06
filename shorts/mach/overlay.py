"""参考動画（@basuragnews）の文字の見せ方を、計測した位置・大きさで再現する（1080x1920）。"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
SERIF = os.path.join(HERE, "..", "fonts", "NotoSerifJP[wght].ttf")
SANS = os.path.join(HERE, "..", "fonts", "NotoSansJP[wght].ttf")
ORANGE = (240, 150, 70)          # タイトルのキーワード（参考の淡いオレンジ）
TAG_ORANGE = (232, 112, 40)      # 「リプレイ 1/500 スロー」の枠
TAG_GREEN = (40, 170, 110)       # 「実際の速さ」の枠
WATERMARK = os.environ.get("MACH_WATERMARK", "@nihon_de_ikiru")


def font(path, size, weight):
    f = ImageFont.truetype(path, size)
    f.set_variation_by_name(weight)
    return f


def shadow_text(im, xy, text, f, fill=(255, 255, 255), anchor="la", blur=6, alpha=150, spacing=0):
    """柔らかい影つきの文字（参考は白文字＋ぼかした黒い影）。"""
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0] + 2, xy[1] + 3), text, font=f, fill=(0, 0, 0, alpha), anchor=anchor)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    im.alpha_composite(sh)
    ImageDraw.Draw(im).text(xy, text, font=f, fill=fill, anchor=anchor)


def runs_text(im, cx, y, runs, f, anchor_y="ls"):
    """色違いの文字列を中央ぞろえで1行に（runs = [(文字, 色), ...]）。"""
    total = sum(f.getlength(t) for t, _ in runs)
    x = cx - total / 2
    for t, col in runs:
        shadow_text(im, (x, y), t, f, fill=col, anchor="l" + anchor_y[1])
        x += f.getlength(t)


def rounded_box(im, box, fill, radius=24, outline=None, width=0):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)
    im.alpha_composite(lay)


def watermark(im):
    shadow_text(im, (968, 105), WATERMARK, font(SANS, 30, "Bold"), fill=(255, 255, 255, 185), anchor="rm", blur=3, alpha=90)


# ---------- オープニング ----------
def opening(im, title1, title2, count, quote_lines, quote_src):
    """title1/title2 は [(文字, 色)] の列。count は「出発まで」の数字（None なら出さない）。"""
    tf = font(SERIF, 70, "Black")
    runs_text(im, 540, 335, title1, tf)
    runs_text(im, 540, 468, title2, tf)
    if count is not None:
        shadow_text(im, (118, 730), "出発まで", font(SANS, 34, "Bold"), anchor="lm")
        shadow_text(im, (114, 880), str(count), font(SERIF, 104, "Regular"), anchor="ls")
    rounded_box(im, (88, 1215, 1000, 1472), (30, 22, 18, 125), radius=26)
    qf = font(SERIF, 52, "SemiBold")
    for i, line in enumerate(quote_lines):
        shadow_text(im, (530, 1282 + i * 78), line, qf, anchor="mm", blur=4, alpha=110)
    shadow_text(im, (540, 1436), quote_src, font(SANS, 27, "Bold"), fill=(255, 255, 255, 220), anchor="mm", blur=3, alpha=90)


# ---------- 本編の数字 ----------
def timer(im, label, value, tag=None, tag_color=TAG_ORANGE):
    """左上：「出発から」＋「1.002秒」＋オレンジ（または緑）の枠。"""
    shadow_text(im, (118, 327), label, font(SANS, 32, "Bold"), fill=(255, 255, 255, 235), anchor="lm")
    f = font(SERIF, 112, "Regular")
    num, unit = value
    shadow_text(im, (114, 468), num, f, anchor="ls")
    shadow_text(im, (114 + f.getlength(num), 468), unit, font(SERIF, 96, "Regular"), anchor="ls")
    if tag:
        tf = font(SANS, 33, "Bold")
        tw = tf.getlength(tag)
        x0, y0 = 113, 497
        rounded_box(im, (x0, y0, x0 + tw + 64, y0 + 58), tag_color + (255,), radius=29, outline=(255, 245, 235, 255), width=3)
        ImageDraw.Draw(im).text((x0 + 32, y0 + 29), tag, font=tf, fill=(255, 255, 255), anchor="lm")


def speed(im, label, prefix, num, unit="", y_label=680, y_base=835):
    """中央：「新幹線の速さ」＋「マッハ 6.7」。距離のときは prefix='' unit='km'。"""
    shadow_text(im, (540, y_label), label, font(SANS, 32, "Bold"), fill=(255, 255, 255, 235), anchor="mm")
    pf, nf, uf = font(SERIF, 58, "Regular"), font(SERIF, 122, "Regular"), font(SERIF, 54, "Regular")
    total = pf.getlength(prefix) + nf.getlength(num) + uf.getlength(unit)
    x = 540 - total / 2
    if prefix:
        shadow_text(im, (x, y_base), prefix, pf, anchor="ls")
        x += pf.getlength(prefix)
    shadow_text(im, (x, y_base), num, nf, anchor="ls")
    x += nf.getlength(num)
    if unit:
        shadow_text(im, (x, y_base), unit, uf, anchor="ls")


def caption(im, lines, y_first=1297, step=78, box=True):
    """下の説明：ゴシック極太の白2行、半透明の黒い角丸の箱。"""
    f = font(SANS, 48, "Black")
    if box:
        wmax = max(f.getlength(l) for l in lines)
        x0, x1 = 540 - wmax / 2 - 44, 540 + wmax / 2 + 44
        rounded_box(im, (x0, y_first - 52, x1, y_first + step * (len(lines) - 1) + 48), (20, 16, 14, 120), radius=24)
    for i, l in enumerate(lines):
        shadow_text(im, (540, y_first + i * step), l, f, anchor="mm", blur=4, alpha=120)


def note(im, text, y=1497):
    """下の小さな注意書き（「※〜計算した、もしもの話です」）。"""
    shadow_text(im, (540, y), text, font(SANS, 24, "Bold"), fill=(255, 255, 255, 220), anchor="mm", blur=3, alpha=110)


def info_box(im, title, rows):
    """右上の黒い箱。rows = [(アイコン色 or None, 文字, 色), ...]。"""
    x0, y0, x1 = 580, 168, 963
    h = 72 + 66 * len(rows)
    rounded_box(im, (x0, y0, x1, y0 + max(h, 257)), (24, 26, 34, 232), radius=18, outline=(235, 235, 240, 255), width=3)
    d = ImageDraw.Draw(im)
    d.text((x0 + 24, y0 + 34), title, font=font(SANS, 28, "Bold"), fill=(255, 255, 255), anchor="lm")
    for i, (icon, text, col) in enumerate(rows):
        y = y0 + 106 + i * 66
        x = x0 + 24
        if icon:
            d.ellipse((x, y - 30, x + 60, y + 30), fill=icon, outline=(240, 240, 240), width=3)
            x += 92
        d.text((x, y), text, font=font(SANS, 38, "Bold"), fill=col, anchor="lm")


def rewind(im, t):
    """「◀◀ リプレイ」の巻き戻し表示（オレンジの帯）。"""
    f = font(SANS, 40, "Black")
    rounded_box(im, (300, 1140, 780, 1215), TAG_ORANGE + (255,), radius=12)
    ImageDraw.Draw(im).text((540, 1178), "◀◀ リプレイ", font=f, fill=(255, 255, 255), anchor="mm")
