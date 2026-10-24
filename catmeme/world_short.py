"""「日本vs海外」型・「会社員の1日」型・「左右くらべ（日本／世界）」型の1分ショート（縦 1080x1920）。
10/24 ユーザー提供の参考動画4本（税金格差・有給の反応・定時で帰る予定・地震の反応）の作りをまねる。長さは厳密に 59.9 秒。
土台は income_short.py（猫のステッカー・黒い帯・音）。ここでは足りない部品を足す。

- 帯：行ごとに色を分けられる（「日本」赤・「vs」白・「海外」水色 など）。rich_band()
- 札：赤（国・時刻）／黄（フランス）／オレンジ（アメリカ）／白地オレンジ枠（震度）。小さい国旗も付けられる
- セリフ：*ここ* と書いた所だけ赤くなる
- カット：solo（1匹だけ）／talk（2匹・左右どちらにも役名）／phone（スマホのトーク画面）／split（左右くらべ）
- 下のすきま（SAFE_BOTTOM=1540 より下）と右のはしには、説明の箱を置かない（ショートの決まり）
使い方は short_25a_tax.py など
"""
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw

import income_short as I
import render as R
import story_style as S

W, H = I.W, I.H
WHITE, BLACK, RED, YELLOW = I.WHITE, I.BLACK, I.RED, I.YELLOW
CYAN, GREEN, ORANGE, BLUE = (40, 200, 255), (60, 220, 60), (255, 140, 0), (20, 40, 230)
SAFE_BOTTOM = 1540
HERE = I.HERE
for _d in ("25_world", "19_inawashiro", "18_semicon"):
    _p = os.path.join(HERE, "backgrounds", _d)
    if _p not in I.BGS:
        I.BGS.insert(0, _p) if _d == "25_world" else I.BGS.append(_p)

# ChatGPT で作ってもらう背景（scripts/25_world_bg_prompts.md）。届くまでは手もちの絵で代わりにする
STANDIN = {"bg113_fuji_town": "bg59_sakura_park", "bg114_singapore_bay": "bg44_world_map",
           "bg115_japan_diet": "bg84_courthouse", "bg116_paris_assembly": "bg104_supreme_court",
           "bg117_paris_office": "bg78_agency_office", "bg118_us_capitol": "bg84_courthouse",
           "bg119_us_office": "bg01_us_ai_office"}


def bg_name(n):
    try:
        I.bg_path(n)
        return n
    except FileNotFoundError:
        return STANDIN[n]


def cover(name, blur=0, dark=0.0):
    im = I.cover(bg_name(name))
    if blur:
        im = cv2.GaussianBlur(im, (0, 0), blur)
    if dark:
        im = im * (1 - dark)
    return im


# ---- 文字 ----

def segs_of(t, base, hi=RED):
    """「*ここ*」だけ色を変える → [(文字, 色), ...]。"""
    out, on = [], False
    for i, part in enumerate(t.split("*")):
        if part:
            out.append((part, hi if on else base))
        on = not on
    return out


def rich(lines, size, stroke=0, stroke_col=BLACK, max_w=W - 50, lh=1.18):
    """lines = [[(文字, 色), ...], ...]。行ごとに真ん中そろえ。はみ出すときは小さくする。"""
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    while True:
        f = I.font(size)
        ws = [sum(d0.textlength(s, font=f) for s, _ in ln) for ln in lines]
        if max(ws) + stroke * 2 <= max_w or size < 30:
            break
        size -= 3
    h = int(size * lh)
    im = Image.new("RGBA", (int(max(ws)) + stroke * 2 + 10, h * len(lines) + stroke * 2 + 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (ln, w) in enumerate(zip(lines, ws)):
        x = (im.width - w) / 2
        for s, col in ln:
            d.text((x, stroke + 4 + i * h), s, font=f, fill=col, stroke_width=stroke, stroke_fill=stroke_col)
            x += d0.textlength(s, font=f)
    return im.crop(im.getbbox())


def say_img(t, size=80, base=WHITE, stroke=7):
    return rich([segs_of(ln, base) for ln in t.split("\n")], size, stroke=stroke, max_w=W - 60)


def rich_band(rows, y0, y1):
    """上の黒い帯。rows = [(行のマークアップ, 文字の大きさ, 縁の色, 中心のy), ...]。
    行のマークアップは「{r}日本{w}vs{c}海外」のように {色} で色を切りかえる。"""
    cols = dict(r=RED, w=WHITE, c=CYAN, y=YELLOW, g=GREEN, k=BLACK)
    im = Image.new("RGBA", (W, y1 - y0), (0, 0, 0, 255))
    for mk, size, sc, cy in rows:
        segs, col = [], WHITE
        for part in mk.split("{")[0:]:
            if not part:
                continue
            if "}" in part:
                key, txt = part.split("}", 1)
                col = cols[key]
            else:
                txt = part
            if txt:
                segs.append((txt, col))
        t = rich([segs], size, stroke=4, stroke_col=sc, max_w=W - 30)
        im.alpha_composite(t, ((W - t.width) // 2, int(cy - y0 - t.height / 2)))
    return im


def tag_img(t, style="red", flag=None, size=104):
    """区切りの札。"""
    fill, fg, border, sc = dict(red=(RED, WHITE, WHITE, (150, 0, 0)), yellow=(YELLOW, BLACK, None, None),
                                orange=(ORANGE, BLACK, None, None), time=(RED, WHITE, WHITE, (150, 0, 0)),
                                shindo=(WHITE, RED, ORANGE, None))[style]
    tx = rich([[(t, fg)]], size, stroke=3 if sc else 0, stroke_col=sc or BLACK)
    fl = S.flag_img(flag, h=int(size * 0.72)) if flag else None
    inner = tx.width + (fl.width + 22 if fl else 0)
    bw = 12 if style == "shindo" else 6
    im = Image.new("RGBA", (max(inner + 80, 320), int(size * 1.36)), (border or fill) + (255,))
    ImageDraw.Draw(im).rectangle((bw, bw, im.width - bw - 1, im.height - bw - 1), fill=fill)
    x = (im.width - inner) // 2
    if fl:
        im.alpha_composite(fl.convert("RGBA"), (x, (im.height - fl.height) // 2))
        x += fl.width + 22
    im.alpha_composite(tx, (x, (im.height - tx.height) // 2))
    return im


# ---- カット ----

def _cat(a, x, h, w, bottom, label=None, mute=True):
    return dict(a=a, x=x, h=h, w=w, bottom=bottom, label=label, mute=mute)


def solo(bg, tag, say, cat, label=None, lines=False, dur=2.5, se=None, scale=1.0, tag_style="red", flag=None, big_say=False):
    """1匹だけ（真ん中に大きく）。lines=True で白い集中線。"""
    c = dict(kind="solo", bg=bg, tag=tag, say=say, tag_style=tag_style, flag=flag, lines=lines, big_say=big_say, dur=dur,
             fixed=True, no_pop=True, cats=[_cat(cat, 540, 860 * scale, 900 * scale, 1600, label, mute=False)])
    if se:
        c["se"] = se
    return c


def talk(bg, tag, say, left, right, who="R", llabel=None, rlabel=None, dur=2.5, se=None, lscale=1.0, rscale=1.0,
         tag_style="red", flag=None):
    """2匹の会話。しゃべる側（who）の猫だけ音を出す。役名は左右どちらにも付けられる。"""
    cats = [_cat(left, 300, 860 * lscale, 640 * lscale, 1580, llabel, mute=who != "L"),
            _cat(right, 780, 860 * rscale, 640 * rscale, 1580, rlabel, mute=who != "R")]
    c = dict(kind="talk", bg=bg, tag=tag, say=say, tag_style=tag_style, flag=flag, cats=cats, dur=dur, fixed=True, no_pop=True)
    if se:
        c["se"] = se
    return c


def phone(bg, tag, msgs, cat, say=None, dur=3.0, se="pikon", friend_icon="meow_gray_white_kitten", me_icon="huh_huh_cat"):
    """スマホのトーク画面（水色の画面・緑の枠のふきだし）。msgs = [(\"friend\"|\"me\", 文, 時刻), ...]。手前に猫。"""
    return dict(kind="phone", bg=bg, tag=tag, msgs=msgs, say=say, tag_style="red", flag=None, dur=dur, fixed=True, no_pop=True,
                se=se, icons=dict(friend=friend_icon, me=me_icon), cats=[_cat(cat, 300, 560, 520, 1590, None, mute=False)])


def split(bg, tag, left=None, right=None, cap=None, cap_side="R", sound="R", dur=3.2, se=None):
    """左右くらべ：左「日本」右「世界」。cap は下の緑の枠の説明（cap_side の側に出す）。sound の側の猫だけ鳴く。"""
    cats = []
    if left:
        cats.append(_cat(left, 275, 600, 500, 1290, None, mute=sound != "L"))
    if right:
        cats.append(_cat(right, 805, 600, 500, 1290, None, mute=sound != "R"))
    c = dict(kind="split", bg=bg, tag=tag, cap=cap, cap_side=cap_side, tag_style="shindo", flag=None, cats=cats, dur=dur,
             fixed=True, no_pop=True, say=None)
    if se:
        c["se"] = se
    return c


# ---- 描画 ----

def cap_box(t):
    """下の説明：白地・緑の太い枠・青い太字。"""
    tx = rich([[(ln, BLUE)] for ln in t.split("\n")], 76, stroke=3, stroke_col=WHITE, max_w=450, lh=1.12)
    im = Image.new("RGBA", (max(tx.width + 50, 300), tx.height + 44), GREEN + (255,))
    ImageDraw.Draw(im).rectangle((9, 9, im.width - 10, im.height - 10), fill=WHITE)
    im.alpha_composite(tx, ((im.width - tx.width) // 2, (im.height - tx.height) // 2))
    return im


def rounded(w, h, r, fill):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill)
    return im


def icon_img(name, d=120):
    """猫の顔の丸いアイコン（素材の1枚目から）。"""
    cl = R.Clip(name)
    fr, a = cl.frame(0.5)
    if getattr(cl, "cap", None) is not None:
        cl.cap.release()
    y0, y1, x0, x1 = I.clip_bbox(name)
    al = a[y0:y1, x0:x1].astype(np.float32)[..., None]
    fr = (fr[y0:y1, x0:x1].astype(np.float32) * al + 255 * (1 - al)).astype(np.uint8)   # 抜いた所は白に
    s = min(fr.shape[:2])
    cy, cx = fr.shape[0] // 3, fr.shape[1] // 2
    y = max(0, min(cy - s // 2, fr.shape[0] - s))
    x = max(0, min(cx - s // 2, fr.shape[1] - s))
    sq = cv2.resize(fr[y:y + s, x:x + s], (d, d))
    pil = Image.fromarray(sq[:, :, ::-1]).convert("RGBA")
    m = Image.new("L", (d, d), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
    out = Image.new("RGBA", (d + 12, d + 12), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse((0, 0, d + 11, d + 11), fill=GREEN + (255,))
    out.paste(pil, (6, 6), m)
    return out


def phone_img(c):
    """スマホ（黒い角丸）＋水色の画面＋ふきだし。"""
    pw, ph = 800, 1000
    im = rounded(pw, ph, 70, (40, 40, 44, 255))
    im.alpha_composite(rounded(pw - 44, ph - 44, 52, (40, 225, 200, 255)), (22, 22))
    y = 190
    for who, t, tm in c["msgs"]:
        tx = rich([[(ln, BLACK)] for ln in t.split("\n")], 60, max_w=420, lh=1.12)
        b = Image.new("RGBA", (tx.width + 48, tx.height + 40), GREEN + (255,))
        ImageDraw.Draw(b).rectangle((8, 8, b.width - 9, b.height - 9), fill=WHITE)
        b.alpha_composite(tx, (24, 20))
        ic = icon_img(c["icons"][who], 120)
        if who == "friend":   # 相手は左、自分は右によせる
            bx, ix = 60, 60 + b.width + 16
        else:
            bx = pw - 60 - b.width
            ix = bx - 16 - ic.width
        im.alpha_composite(b, (bx, y))
        im.alpha_composite(ic, (ix, y - 20))
        tt = rich([[(tm, BLACK)]], 40)
        im.alpha_composite(tt, (bx + 10, y + b.height + 8))
        y += b.height + 90
    return im


class Renderer(I.Renderer):
    def __init__(self, c, band):
        self.c, self.band = c, band
        k = c["kind"]
        self.base = cover(c["bg"], blur=c.get("blur", 0), dark=c.get("dark", 0.0))
        if c.get("lines"):
            I.speed_lines(self.base, W / 2, 1150)
        self.tag = tag_img(c["tag"], c.get("tag_style", "red"), c.get("flag"))
        self.tag_y = c.get("tag_y", 600)
        self.say = None
        if c.get("say"):
            self.say = say_img(c["say"], 104 if c.get("big_say") else 80, stroke=8 if c.get("big_say") else 7)
        self.say_y = c.get("say_y", 690)
        self.clips = [R.Clip(q["a"]) for q in c["cats"]]
        self.labels = [I.name_tag(q["label"]) if q.get("label") else None for q in c["cats"]]
        self.bbox = {}
        self.phone = phone_img(c) if k == "phone" else None
        if k == "split":
            self.heads = (rich([[("日本", BLUE)]], 140, stroke=6, stroke_col=WHITE), rich([[("世界", RED)]], 140, stroke=6, stroke_col=WHITE))
            self.cap = cap_box(c["cap"]) if c.get("cap") else None

    def frame(self, t):
        out = self.base.copy()
        c = self.c
        if self.phone is not None:
            I.put(out, self.phone, W / 2 + 20, 1010)
        if c["kind"] == "split":
            cv2.rectangle(out, (W // 2 - 8, 680), (W // 2 + 8, 1290), (0, 0, 0), -1)
        for i, q in enumerate(c["cats"]):
            s = 1.0 if t > 0.12 else 0.85 + 0.15 * (t / 0.12)   # ポンと出る
            img, al = self.cat_img(i, q, t)
            if s < 1:
                img = cv2.resize(img, None, fx=s, fy=s)
                al = cv2.resize(al, None, fx=s, fy=s)
            h, w = al.shape
            lo, hi = (20, W - 20) if c["kind"] != "split" else ((20, W // 2 - 14) if q["x"] < W / 2 else (W // 2 + 14, W - 40))
            x0 = min(max(int(q["x"] - w / 2), lo), hi - w)   # 画面（左右くらべでは自分の側）からはみ出さない
            over_cat(out, img, al, x0, int(q["bottom"] - h), c["kind"] == "split")
            if self.labels[i] is not None:
                lx = q["x"] - 60 if q["x"] < W / 2 else q["x"] + 40
                lw = self.labels[i].width / 2
                I.put(out, self.labels[i], min(max(lx, lw + 40), W - lw - 60), q["bottom"])
        if c["kind"] == "split":   # 「日本」「世界」は猫より手前
            I.put(out, self.heads[0], 275, 600)
            I.put(out, self.heads[1], 805, 600)
        if c["kind"] == "split" and self.cap is not None:
            cx = 275 if c["cap_side"] == "L" else 805
            cx = min(max(cx, self.cap.width / 2 + 20), W - self.cap.width / 2 - 40)
            cy = min(1310 + self.cap.height / 2, SAFE_BOTTOM - self.cap.height / 2)
            I.put(out, self.cap, cx, cy)
        b = R.to_np(self.band)
        I.over(out, b[0], b[1], 0, c.get("band_y", I.BAND[0]))
        I.put(out, self.tag, W / 2, self.tag_y)
        if self.say is not None:
            I.put(out, self.say, W / 2, self.say_y + self.say.height / 2)
        return out


def over_cat(out, img, al, x, y, split_mode):
    I.over(out, img, al, x, y)


def run(cs, band, out_path, prev=None):
    I.run(cs, None, None, out_path, prev, band=band, renderer=Renderer)


# 帯のひな形（参考どおりの位置・色。文字は台本ごとに変える）
def band_vs(line1, line2):
    """「日本vs海外」型：1行目 {r}日本{w}vs{c}海外、2行目 黄色（一部の色を変えてもよい）。"""
    return rich_band([(line1, 150, WHITE, 300), (line2, 104, BLACK, 440)], *I.BAND)
