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
        t = rich([segs], size, stroke=4, stroke_col=sc, max_w=W - 170)   # スマホで左右が少し切れるので余白をとる（10/26）
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


def solo(bg, tag, say, cat, label=None, lines=False, dur=2.5, se=None, scale=1.0, tag_style="red", flag=None, big_say=False, **extra):
    """1匹だけ（真ん中に大きく）。lines=True で白い集中線。"""
    c = dict(kind="solo", bg=bg, tag=tag, say=say, tag_style=tag_style, flag=flag, lines=lines, big_say=big_say, dur=dur,
             fixed=True, no_pop=True, cats=[_cat(cat, 540, 860 * scale, 900 * scale, 1600, label, mute=False)], **extra)
    if se:
        c["se"] = se
    return c


def talk(bg, tag, say, left, right, who="R", llabel=None, rlabel=None, dur=2.5, se=None, lscale=1.0, rscale=1.0,
         tag_style="red", flag=None, **extra):
    """2匹の会話。しゃべる側（who）の猫だけ音を出す。役名は左右どちらにも付けられる。"""
    cats = [_cat(left, 300, 860 * lscale, 640 * lscale, 1580, llabel, mute=who != "L"),
            _cat(right, 780, 860 * rscale, 640 * rscale, 1580, rlabel, mute=who != "R")]
    c = dict(kind="talk", bg=bg, tag=tag, say=say, tag_style=tag_style, flag=flag, cats=cats, dur=dur, fixed=True, no_pop=True, **extra)
    if se:
        c["se"] = se
    return c


def phone(bg, tag, msgs, cat=None, say=None, dur=3.0, se="pikon", friend_icon="meow_gray_white_kitten", me_icon="huh_huh_cat"):
    """スマホのトーク画面（水色の画面・緑の枠のふきだし）。msgs = [(\"friend\"|\"me\", 文, 時刻), ...]。手前に猫。"""
    return dict(kind="phone", bg=bg, tag=tag, msgs=msgs, say=say, tag_style="red", flag=None, dur=dur, fixed=True, no_pop=True,
                se=se, icons=dict(friend=friend_icon, me=me_icon), say_y=1010,
                cats=[_cat(cat, 360, 640, 620, 1590, None, mute=False)] if cat else [],
                props=[("phone", 610, 1220, 190)] if cat else [])


def split(bg, tag, left=None, right=None, cap=None, cap_side="R", sound="R", dur=3.2, se=None, cap_full=False):
    """左右くらべ：左「日本」右「世界」。cap は下の緑の枠の説明（cap_side の側に出す）。sound の側の猫だけ鳴く。"""
    cats = []
    if left:
        cats.append(_cat(left, 275, 600, 500, 1290, None, mute=sound != "L"))
    if right:
        cats.append(_cat(right, 805, 600, 500, 1290, None, mute=sound != "R"))
    c = dict(kind="split", bg=bg, tag=tag, cap=cap, cap_side=cap_side, cap_full=cap_full, tag_style="shindo", flag=None, cats=cats, dur=dur,
             fixed=True, no_pop=True, say=None)
    if se:
        c["se"] = se
    return c


# ---- 描画 ----

def cap_box(t, full=False):
    """下の説明：白地・緑の太い枠・青い太字。full=True は横いっぱい（まとめ用・10/26）。"""
    tx = rich([[(ln, BLUE)] for ln in t.split("\n")], 96 if full else 76, stroke=3, stroke_col=WHITE, max_w=960 if full else 450,
              lh=1.12)
    im = Image.new("RGBA", (W - 60 if full else max(tx.width + 50, 300), tx.height + 44), GREEN + (255,))
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


def prop_img(kind, w):
    """小道具（絵で描く）：desk 机／tv テレビ／phone スマホ（手に持つ）。"""
    if kind == "desk":
        h = int(w * 0.62)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for x in (int(w * 0.08), int(w * 0.86)):
            d.rectangle((x, int(h * 0.2), x + int(w * 0.06), h), fill=(150, 150, 160, 255), outline=BLACK + (255,), width=4)
        d.rectangle((0, 0, w - 1, int(h * 0.24)), fill=(230, 180, 60, 255), outline=BLACK + (255,), width=5)
        return im
    if kind == "tv":
        h = int(w * 0.8)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, int(h * 0.86)), 18, fill=(70, 70, 76, 255), outline=BLACK + (255,), width=5)
        d.rectangle((int(w * 0.08), int(h * 0.08), int(w * 0.92), int(h * 0.74)), fill=(120, 200, 255, 255))
        d.rectangle((int(w * 0.35), int(h * 0.86), int(w * 0.65), h - 1), fill=(60, 60, 60, 255))
        return im
    if kind == "phone":
        h = int(w * 1.9)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, h - 1), int(w * 0.16), fill=(235, 215, 190, 255), outline=(120, 100, 80, 255), width=4)
        for i, (cx, cy) in enumerate(((0.3, 0.12), (0.3, 0.27), (0.6, 0.2))):
            r = w * 0.11
            d.ellipse((w * cx - r, h * cy - r, w * cx + r, h * cy + r), fill=(40, 40, 50, 255))
        return im
    if kind.startswith("phone:"):   # スマホの画面に赤い文字（「給料明細」「残高」など）
        im = prop_img("phone", w)
        tx = rich([[(ln, RED)] for ln in kind[6:].split("\n")], int(w * 0.42), stroke=5, stroke_col=WHITE, max_w=int(w * 2.2), lh=1.1)
        out = Image.new("RGBA", (max(im.width, tx.width) + 20, im.height), (0, 0, 0, 0))
        out.alpha_composite(im, ((out.width - im.width) // 2, 0))
        out.alpha_composite(tx, ((out.width - tx.width) // 2, int(im.height * 0.55 - tx.height / 2)))
        return out
    if kind.startswith("cloud:"):   # 考えごとの雲（白い楕円＋黒い字）
        tx = rich([[(ln, BLACK)] for ln in kind[6:].replace("@R", "").split("\n")], 64, max_w=int(w * 0.8), lh=1.15)
        h = max(int(w * 0.55), tx.height + 90)
        im = Image.new("RGBA", (w, h + 70), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.ellipse((0, 0, w - 1, h - 1), fill=WHITE + (255,), outline=(60, 60, 60, 255), width=5)
        tail = ((w * 0.7, h + 18, 22), (w * 0.78, h + 52, 13)) if kind.startswith("cloud:") and "@R" in kind else \
            ((w * 0.3, h + 18, 22), (w * 0.22, h + 52, 13))
        for cx, cy, r in tail:
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE + (255,), outline=(60, 60, 60, 255), width=4)
        im.alpha_composite(tx, ((w - tx.width) // 2, (h - tx.height) // 2))
        return im
    raise ValueError(kind)


def bubble_img(t, size=60):
    """緑の枠の白いふきだし（黒い字）。"""
    tx = rich([[(ln, BLACK)] for ln in t.split("\n")], size, max_w=720, lh=1.12)
    b = Image.new("RGBA", (tx.width + 48, tx.height + 40), GREEN + (255,))
    ImageDraw.Draw(b).rectangle((8, 8, b.width - 9, b.height - 9), fill=WHITE)
    b.alpha_composite(tx, (24, 20))
    return b


def subscribe_img(done):
    """チャンネル登録ボタン（参考の最後と同じ。赤→「登録済み」の灰色）。"""
    tx = rich([[("登録済み" if done else "チャンネル登録", WHITE)]], 84)
    im = rounded(tx.width + 90, tx.height + 50, 22, ((140, 140, 140, 255) if done else (220, 0, 20, 255)))
    im.alpha_composite(tx, ((im.width - tx.width) // 2, (im.height - tx.height) // 2))
    return im


class Renderer(I.Renderer):
    def __init__(self, c, band):
        self.c, self.band = c, band
        k = c["kind"]
        self.base = cover(c["bg"], blur=c.get("blur", 0), dark=c.get("dark", 0.0))
        if c.get("letterbox") is not None:   # 横長の絵を黒い画面のまん中に（参考「社会人1年目と2年目」の作り）
            y0 = c["letterbox"]
            im = Image.open(I.bg_path(bg_name(c["bg"]))).convert("RGB")
            k = max(W / im.width, 608 / im.height)
            im = im.resize((int(im.width * k + 0.5), int(im.height * k + 0.5)), Image.LANCZOS)
            x_, y_ = (im.width - W) // 2, (im.height - 608) // 2
            self.base = np.zeros((H, W, 3), np.float32)
            self.base[y0:y0 + 608] = np.asarray(im.crop((x_, y_, x_ + W, y_ + 608)))[:, :, ::-1].astype(np.float32) / 255
        self.foot = None
        if c.get("foot"):   # 下の白い四角の文字（「これが現実」など）
            tx = rich([[(c["foot"], BLACK)]], 84)
            self.foot = Image.new("RGBA", (tx.width + 60, tx.height + 40), (255, 255, 255, 255))
            self.foot.alpha_composite(tx, (30, 20))
        if c.get("lines"):
            I.speed_lines(self.base, W / 2, 1150)
        self.tag = tag_img(c["tag"], c.get("tag_style", "red"), c.get("flag"))
        self.tag_y = c.get("tag_y", 600)
        self.say = None
        if c.get("say"):
            big = c.get("big_say")
            longest = max(len(ln.replace("*", "")) for ln in c["say"].split("\n"))
            size = c.get("say_size") or (120 if big else (128 if longest <= 5 else (110 if longest <= 8 else 96)))   # 字幕は大きめ。短い字幕はもっと大きく（10/28 ユーザー指定）
            if c["kind"] == "solo" and not c.get("say_size") and len(c["cats"]) == 1 and not c.get("props"):
                # 1匹の場面は「40分たってた!?」と同じ：時刻の下にまん中で大きく（画面からはみ出さない大きさまで・10/28 ユーザー指定）
                wid = max(sum(1 if ord(ch) > 255 else 0.55 for ch in ln.replace("*", "")) for ln in c["say"].split("\n"))
                size = int(min(135 if "\n" not in c["say"] else 118, 960 / wid))
            self.say = say_img(c["say"], size, stroke=12 if size >= 150 else 8)
        self.say_y = c.get("say_y", 690)
        self.huh = None
        if c.get("say_fx") == "huh":   # 「!?!?!?」：1つずつポンと出る・赤と黄色・少し傾けて震える（10/28 ユーザー指定）
            n = c["say"].count("!?")
            size = c.get("say_size", 150)
            self.huh = [rich([[("!?", (RED, YELLOW)[j % 2])]], size, stroke=10, stroke_col=BLACK).rotate(
                (-12, 9, -6, 12, -9)[j % 5], expand=True, resample=Image.BICUBIC) for j in range(n)]
            self.say = None
        self.clips = [R.Clip(q["a"]) for q in c["cats"]]
        self.labels = [I.name_tag(q["label"]) if q.get("label") else None for q in c["cats"]]
        self.bbox = {}
        self.phone = phone_img(c) if k == "phone" else None
        self.props = [(prop_img(kd, int(w)), x, y) for kd, x, y, w in c.get("props", [])]
        self.bubbles = [(bubble_img(t_), x, y, at) for t_, x, y, at in c.get("bubbles", [])]
        self.subs = (subscribe_img(False), subscribe_img(True)) if c.get("subscribe") else None
        if k == "split":
            hl, hr = c.get("heads", ("日本", "世界"))
            self.heads = (rich([[(hl, BLUE)]], 140, stroke=6, stroke_col=WHITE), rich([[(hr, RED)]], 140, stroke=6, stroke_col=WHITE))
            self.cap = cap_box(c["cap"], c.get("cap_full", False)) if c.get("cap") else None

    def side_layout(self):
        """字幕が猫とかさなるときは、猫を左によせて字幕を猫の右どなりに出す（10/26 ユーザー指定）。1匹だけの場面で使う。"""
        c = self.c
        self.say_xy = None
        if c["kind"] != "solo" or self.say is None or len(c["cats"]) != 1 or c.get("big_say"):
            return
        q = c["cats"][0]
        y0, y1, x0, x1 = I.clip_bbox(q["a"])
        sc = min(q["h"] / (y1 - y0), q.get("w", 10 ** 6) / (x1 - x0))
        w, h = int((x1 - x0) * sc) + 28, int((y1 - y0) * sc) + 28
        top = q["bottom"] - h
        say_top, say_bot = self.say_y, self.say_y + self.say.height
        if say_bot < top + 10 and not UNDER:   # かさならない
            return
        if self.props:   # 小道具（スマホ・雲）がある場面は、猫を字幕の下まで小さくする
            k = (q["bottom"] - say_bot - 20) / h
            q["h"], q["w"] = q["h"] * k, q.get("w", 10 ** 6) * k
            return
        if UNDER:   # 字幕は時刻の下にまん中、猫はその下にまん中で大きく（字幕に少しかかってよい・10/28 ユーザー指定）
            q["bottom"] = max(q["bottom"], 1680)
            avail = q["bottom"] - (say_bot - 25)
            q["h"], q["w"], q["x"] = avail - 28, W - 160, W / 2
            return
        need = min(max(self.say.width * 0.5, 300), W - 90 - 0.6 * W)   # 字幕は小さくしない。猫と少しかさなってよい（10/28 ユーザー指定）。猫は画面の幅の6割より小さくしない
        if W - w - 90 < need:
            k = (W - 90 - need) / w
            if k < (0.8 if c.get("under") else 0.45):   # 横に置くと猫が小さくなりすぎる → 字幕を上、猫をその下に大きく（10/26 ユーザー指定）
                if not c.get("under"):
                    return
                k2 = (q["bottom"] - say_bot - 20) / h
                q["h"], q["w"] = q["h"] * k2, q.get("w", 10 ** 6) * k2 * 1.3
                return
            q["h"], q["w"] = q["h"] * k, q.get("w", 10 ** 6) * k
            w, h = int(w * k), int(h * k)
            top = q["bottom"] - h
        q["x"] = 20 + w / 2
        cx = min(20 + w + (W - 20 - w) / 2, W - 25 - self.say.width / 2)   # 入りきらない分は猫にかぶせる
        cy = max(top + h * 0.3, self.tag_y + 120 + self.say.height / 2)
        self.say_xy = (cx, cy)

    def frame(self, t):
        out = self.base.copy()
        c = self.c
        if not hasattr(self, "say_xy"):
            self.side_layout()
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
        for im, x, y in self.props:   # 小道具は猫の手前
            I.put(out, im, x, y)
        for im, x, y, at in self.bubbles:
            if t >= at:
                I.put(out, im, x, y)
        if c["kind"] == "split":   # 「日本」「世界」は猫より手前
            I.put(out, self.heads[0], 275, 600)
            I.put(out, self.heads[1], 805, 600)
        if c["kind"] == "split" and self.cap is not None:
            cx = W / 2 if c.get("cap_full") else (275 if c["cap_side"] == "L" else 805)
            cx = min(max(cx, self.cap.width / 2 + 20), W - self.cap.width / 2 - 20)
            cy = min(1310 + self.cap.height / 2, SAFE_BOTTOM - self.cap.height / 2)
            I.put(out, self.cap, cx, cy)
        b = R.to_np(self.band)
        I.over(out, b[0], b[1], 0, c.get("band_y", I.BAND[0]))
        I.put(out, self.tag, W / 2, self.tag_y)
        if self.huh:
            n = len(self.huh)
            rng = np.random.default_rng(int(t * R.FPS))
            for j, im in enumerate(self.huh):
                t0 = 0.08 * j
                if t < t0:
                    break
                k = 1.0 + 0.5 * max(0.0, 1 - (t - t0) / 0.1)   # 大きく出て縮む
                if k != 1.0:
                    im = im.resize((int(im.width * k), int(im.height * k)), Image.BILINEAR)
                cx = 30 + (W - 60) * (j + 0.5) / n + rng.integers(-6, 7)   # 少し画面からはみ出てもよい（10/28 ユーザー指定）
                cy = self.say_y + 90 + (-18 if j % 2 else 12) + rng.integers(-6, 7)
                I.put(out, im, cx, cy)
        if self.say is not None:
            if self.say_xy:
                I.put(out, self.say, *self.say_xy)
            else:
                I.put(out, self.say, W / 2, self.say_y + self.say.height / 2)
        if self.foot is not None:
            I.put(out, self.foot, W / 2, c.get("foot_y", 1330))
        if self.subs is not None:   # 参考の最後：ボタンが出て、少しあとに「登録済み」
            I.put(out, self.subs[1 if t > 1.3 else 0], W / 2, 1180)
        if c.get("hype"):
            out = hype_fx(out, t)
        return out


_VIG = None


def hype_fx(out, t):
    """エフェクト全力（10/28 ユーザー指定：前日深夜の暴飲暴食＆ゲームの場面）。
    ドンと寄る＋リズムで脈打つ・まわりがパーティーの光（ピンク→水色→黄色）で点滅・頭に白い光。"""
    global _VIG
    if _VIG is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        _VIG = np.clip((d - 0.55) / 0.6, 0, 1)[..., None] ** 1.5
    z = 1.0 + 0.14 * max(0.0, 1 - t / 0.18) + 0.03 * abs(math.sin(t * 9))
    big = cv2.resize(out, None, fx=z, fy=z, interpolation=cv2.INTER_LINEAR)
    y0, x0 = (big.shape[0] - H) // 2, (big.shape[1] - W) // 2   # 画面は揺らさない（10/28 ユーザー指定）
    out = big[y0:y0 + H, x0:x0 + W]
    col = np.array([(0.85, 0.25, 1.0), (1.0, 0.9, 0.2), (0.2, 0.95, 1.0)][int(t / 0.12) % 3], np.float32)   # BGR：ピンク・水色・黄色
    out = out * (1 - _VIG * 0.55) + col * _VIG * 0.55
    if t < 0.1:
        out = out * 0.35 + 0.65 * (1 - t / 0.1) + out * 0.65 * (t / 0.1)
    return out


def over_cat(out, img, al, x, y, split_mode):
    I.over(out, img, al, x, y)


def run(cs, band, out_path, prev=None):
    dedupe(cs)
    I.run(cs, None, None, out_path, prev, band=band, renderer=Renderer)


# 帯のひな形（参考どおりの位置・色。文字は台本ごとに変える）
def band_vs(line1, line2):
    """「日本vs海外」型：1行目 {r}日本{w}vs{c}海外、2行目 黄色（一部の色を変えてもよい）。"""
    return rich_band([(line1, 150, WHITE, 300), (line2, 104, BLACK, 440)], *I.BAND)


# ---- 同じ素材が続かないようにする（10/26 ユーザー指定：同じ素材が連続で使われがち） ----
MOODS = [
    ["stare_tabby_wide_eyes_cat", "surprise_big_pupils_cat", "stare_big_eyes_tabby_kitten", "peek_what_happen_cat", "huh_huh_cat"],
    ["dance_tabby_standing_cat", "happy_hamster_open_arms", "happy_girlfriend_dance_cat", "happy_chipi_chapa_cat", "dance_wop_cat",
     "dance_three_kittens", "dance_orange_gray_cats", "laugh_laughing_dog", "yell_orange_fat_cat", "excited_hodomoe_city_cat"],
    ["sad_banana_cat_cry", "despair_dramatic_kitten", "sad_black_dog", "sulk_hungry_cat", "sleepy_old_memories_cat",
     "blank_black_cat_zoning_out"],
    ["talk_orange_white_sitting_cat", "stare_interviewer_cat", "realize_wet_cat_stare", "read_book_orange_kitten", "rizz_cat_rizz",
     "cocky_dj_cat", "showoff_gojo_cosplay_cat", "money_counting_orange_cat", "think_bike_front_seat_cat", "calmdown_dancing_cat"],
    ["rage_talking_cat", "glare_disgusted_cat", "angry_aiming_cat", "meow_ragdoll_chubby_cat", "punch_boxing_white_cat"],
]


UNDER = True   # 1匹の場面の並べ方（10/28 ユーザー指定：「40分たってた!?」の場面を参考に、字幕は上まん中・猫はその下にまん中で大きく）
KEEP = {"scream_standing_marmot"}   # 続けて使ってよい素材（マーモットのくり返しは演出・10/26 ユーザー指定）


def dedupe(cs, key="cats"):
    """前のカットと同じ素材があれば、同じ気持ちのグループの別の素材にかえる。"""
    def names(c):
        return {q["a"] for q in c.get(key, []) if q.get("a")}
    for i in range(1, len(cs)):
        if cs[i].get("kind") == "split":   # 左右くらべは同じ猫が残るのが演出
            continue
        prev = names(cs[i - 1])
        nxt = names(cs[i + 1]) if i + 1 < len(cs) else set()
        for q in cs[i].get(key, []):
            a = q.get("a")
            if not a or a not in prev or a in KEEP:
                continue
            group = next((g for g in MOODS if a in g), MOODS[3])
            used = prev | nxt | names(cs[i])
            alt = [x for x in group if x not in used] or [x for x in MOODS[3] if x not in used]
            q["a"] = alt[(i * 7 + len(a)) % len(alt)]
    return cs
