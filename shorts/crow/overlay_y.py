"""よねあぷ（@yoneapp-games）型の文字の見せ方（1080x1920）。
冒頭：大きな2行タイトル＋状況の一文＋「〇〇が消えるまで ○秒」。
本編：上に小さなタイトル1行、左上に「〇〇が消えてから ▶▶×倍速」と経過時間（色つき下線）、場所、下に大きな見出し＋説明2行。"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mach"))
import overlay as O  # noqa: E402

W, H = 1080, 1920
KEY = (130, 205, 95)        # キーワードの色（よねあぷの「蚊」の緑）
LINE = (130, 205, 95)       # 経過時間の下線
WHITE = (255, 255, 255)
SANS = O.SANS


def f(size, weight="Bold"):
    return O.font(SANS, size, weight)


def runs(im, cx, y, parts, fnt, anchor="ls"):
    O.runs_text(im, cx, y, parts, fnt, anchor_y=anchor)


def title_small(im, word, rest_before, rest_after):
    runs(im, 540, 215, [(rest_before, WHITE), (word, KEY), (rest_after, WHITE)], f(46, "Black"))


def headline(im, text, sub=(), alpha=1.0, y=1330):
    """下の大きな見出し（箱なし、影つき）＋小さな説明。"""
    if alpha <= 0:
        return
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    hf = f(76, "Black")
    size = 76
    while hf.getlength(text) > 980:
        size -= 4
        hf = f(size, "Black")
    O.shadow_text(lay, (540, y), text, hf, anchor="mm", blur=6, alpha=170)
    for i, s in enumerate(sub):
        O.shadow_text(lay, (540, y + 92 + i * 54), s, f(38, "Bold"), anchor="mm", blur=4, alpha=170)
    if alpha < 1:
        a = lay.split()[3].point(lambda v: int(v * alpha))
        lay.putalpha(a)
    im.alpha_composite(lay)


def elapsed(im, label, speed, value, loc=None):
    """左上：「カラスが消えてから ▶▶×60」＋「1日 06:00」＋下線＋場所。"""
    x = 108
    lab = f"{label}　▶▶ ×{speed}" if speed else label
    O.shadow_text(im, (x, 300), lab, f(30, "Bold"), anchor="lm", blur=3, alpha=140)
    vf = f(86, "Bold")
    O.shadow_text(im, (x - 4, 408), value, vf, anchor="ls", blur=5, alpha=150)
    w = vf.getlength(value)
    O.rounded_box(im, (x, 424, x + w, 432), LINE + (255,), radius=4)
    if loc:
        d = ImageDraw.Draw(im)
        d.ellipse((x, 466, x + 22, 488), fill=(230, 60, 60, 255))
        O.shadow_text(im, (x + 34, 477), loc, f(30, "Bold"), anchor="lm", blur=3, alpha=140)


def countdown(im, label, sec_left):
    O.shadow_text(im, (108, 650), label, f(32, "Bold"), anchor="lm", blur=3, alpha=140)
    num = f"{sec_left:.2f}"
    nf = f(110, "Bold")
    O.shadow_text(im, (104, 790), num, nf, anchor="ls", blur=5, alpha=150)
    O.shadow_text(im, (110 + nf.getlength(num), 790), "秒", f(52, "Bold"), anchor="ls", blur=4, alpha=150)


def big_title(im, word, before, after_line1, line2, situation):
    tf = f(98, "Black")
    runs(im, 540, 330, [(before, WHITE), (word, KEY), (after_line1, WHITE)], tf)
    runs(im, 540, 460, [(line2, WHITE)], tf)
    O.shadow_text(im, (540, 548), situation, f(36, "Bold"), anchor="mm", blur=4, alpha=160)


def card(im, text, alpha):
    """章カード（「次の朝」「1週間後」）：画面のまん中に大きな白文字。"""
    if alpha <= 0:
        return
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    O.shadow_text(lay, (540, 900), text, f(140, "Black"), anchor="mm", blur=8, alpha=190)
    a = lay.split()[3].point(lambda v: int(v * alpha))
    lay.putalpha(a)
    im.alpha_composite(lay)


def end_card(im):
    O.shadow_text(im, (540, 860), "次は何が", f(92, "Black"), anchor="mm", blur=6, alpha=170)
    O.shadow_text(im, (540, 980), "消えたら見たい？", f(92, "Black"), anchor="mm", blur=6, alpha=170)
    O.shadow_text(im, (540, 1095), "コメントで教えてね", f(40, "Bold"), anchor="mm", blur=4, alpha=150)
    O.rounded_box(im, (370, 1150, 710, 1210), (255, 255, 255, 40), radius=30, outline=(255, 255, 255, 200), width=2)
    O.shadow_text(im, (540, 1180), "リクエストまってるよ！", f(28, "Bold"), anchor="mm", blur=2, alpha=100)
