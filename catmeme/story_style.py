"""「寸劇」シリーズの横動画（1920x1080）。ユーザー提供の参考動画（10/18・10/19 の5本）の作りをまねる。
メモ：docs/sungeki_reference.md ／ ルール：README の「寸劇」シリーズ。見本：story_18_demo.py

作りの要点
- 語り：黒い画面に白い文字だけ（intro・音なし）／黒い画面に写真＋下に字幕（photo・BGM は続ける）
- 寸劇：場面ごとに背景1枚。役の猫を左・（真ん中・）右に並べ、役名は画面の上（白い四角に黒い太字）
  - セリフは話す猫の近くに白い太字＋黒縁。同じ役が続けて話すときは add=True で下に足す
  - セリフごとに話す猫の素材を表情に合わせて差しかえる（cat=）
  - 強調：画面ごと話す猫へズーム＋下に大きな字幕（白＋黒縁／黄色＋黒縁／赤＋白縁）。集中線・吹き出しのイラストも
  - 気持ちが動くところ：顔のアップ＋真ん中に黄色の字幕を1行ずつ足す（zoom(..., pos="mid")）
- 締め：役の猫がみんな同じ踊る猫になって「チャンネル登録、お願いしまーす」
"""
import math
import os
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import parts as P
import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
YELLOW, RED = (255, 225, 0), (230, 20, 20)
CAP = {"white": (WHITE, BLACK), "yellow": (YELLOW, BLACK), "red": (RED, WHITE)}   # 強調字幕の色（文字, 縁）
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("18_story", "18_semicon", "14_japan", "19_inawashiro", "16_tenchim", "15_vambi", "17_imamori", "04_leak", "03_kodomo_nisa", "02_october", "01_todai")]
_FONTS = {}


def font(size):
    """参考に近い太さ（Noto Sans JP の Bold）。"""
    if size not in _FONTS:
        P.font("black", 40)   # フォントを用意させる
        f = ImageFont.truetype(os.path.join(P.FONT_DIR, P.FONTS["black"][0]), size)
        f.set_variation_by_name("Bold")
        _FONTS[size] = f
    return _FONTS[size]


STANDIN = {}   # 背景がまだ届いていない時の仮の背景（名前 → 仮の名前）。届いたら自動でそちらを使う


def bg_path(name):
    if os.path.isabs(name) and os.path.exists(name):
        return name
    for d in BGS:
        for ext in (".png", ".jpg"):
            p = os.path.join(d, name + ext)
            if os.path.exists(p):
                return p
    if name in STANDIN:
        return bg_path(STANDIN[name])
    raise FileNotFoundError(name)


def text_img(text, size, fill=WHITE, stroke=0, align="center", stroke_col=BLACK, max_w=None):
    """文字（\\n で改行）を RGBA で。max_w をこえるときは小さくする。"""
    while True:
        f = font(size)
        d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        lines = text.split("\n")
        ws = [d0.textlength(ln, font=f) for ln in lines]
        if not max_w or max(ws) + stroke * 2 <= max_w or size <= 30:
            break
        size -= 4
    lh = int(size * 1.32)
    im = Image.new("RGBA", (int(max(ws)) + stroke * 2 + 12, lh * len(lines) + stroke * 2 + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (ln, w) in enumerate(zip(lines, ws)):
        x = {"center": (im.width - w) / 2, "left": stroke + 6, "right": im.width - w - stroke - 6}[align]
        d.text((x, stroke + 6 + i * lh), ln, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_col)
    return im.crop(im.getbbox())


def _star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + math.pi * i / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=fill)


def flag_img(code, h=46):
    """役名の札に付ける小さい国旗（絵で描く）。code = "jp" / "us" / "tw"。"""
    w = int(h * 1.5)
    im = Image.new("RGB", (w * 4, h * 4), WHITE)
    d = ImageDraw.Draw(im)
    W4, H4 = im.size
    if code == "jp":
        r = H4 * 0.3
        d.ellipse((W4 / 2 - r, H4 / 2 - r, W4 / 2 + r, H4 / 2 + r), fill=(188, 0, 45))
    elif code == "us":
        sh = H4 / 13
        for i in range(13):
            d.rectangle((0, i * sh, W4, (i + 1) * sh), fill=(178, 34, 52) if i % 2 == 0 else WHITE)
        cw, ch = W4 * 0.4, sh * 7
        d.rectangle((0, 0, cw, ch), fill=(60, 59, 110))
        for row in range(5):
            for col in range(6):
                x, y = cw * (col + 0.5) / 6, ch * (row + 0.5) / 5
                d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=WHITE)
    elif code == "tw":
        d.rectangle((0, 0, W4, H4), fill=(254, 0, 0))
        cw, ch = W4 / 2, H4 / 2
        d.rectangle((0, 0, cw, ch), fill=(0, 0, 149))
        cx, cy, r = cw / 2, ch / 2, ch * 0.18
        for i in range(12):
            a = 2 * math.pi * i / 12
            p = [(cx + math.cos(a) * ch * 0.38, cy + math.sin(a) * ch * 0.38),
                 (cx + math.cos(a + 0.26) * r, cy + math.sin(a + 0.26) * r), (cx + math.cos(a - 0.26) * r, cy + math.sin(a - 0.26) * r)]
            d.polygon(p, fill=WHITE)
        d.ellipse((cx - r * 1.15, cy - r * 1.15, cx + r * 1.15, cy + r * 1.15), fill=(0, 0, 149))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE)
    elif code == "eu":
        d.rectangle((0, 0, W4, H4), fill=(0, 51, 153))
        for i in range(12):
            a = 2 * math.pi * i / 12
            _star(d, W4 / 2 + math.cos(a) * H4 / 3, H4 / 2 + math.sin(a) * H4 / 3, H4 / 18, (255, 204, 0))
    elif code == "gb":
        d.rectangle((0, 0, W4, H4), fill=(1, 33, 105))
        d.line((0, 0, W4, H4), fill=WHITE, width=int(H4 / 5))
        d.line((0, H4, W4, 0), fill=WHITE, width=int(H4 / 5))
        d.line((0, 0, W4, H4), fill=(200, 16, 46), width=int(H4 / 15))
        d.line((0, H4, W4, 0), fill=(200, 16, 46), width=int(H4 / 15))
        d.rectangle((W4 / 2 - H4 / 6, 0, W4 / 2 + H4 / 6, H4), fill=WHITE)
        d.rectangle((0, H4 / 2 - H4 / 6, W4, H4 / 2 + H4 / 6), fill=WHITE)
        d.rectangle((W4 / 2 - H4 / 10, 0, W4 / 2 + H4 / 10, H4), fill=(200, 16, 46))
        d.rectangle((0, H4 / 2 - H4 / 10, W4, H4 / 2 + H4 / 10), fill=(200, 16, 46))
    elif code == "sg":
        d.rectangle((0, 0, W4, H4 / 2), fill=(238, 36, 49))
        cx, cy, r = W4 * 0.2, H4 * 0.25, H4 * 0.16
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE)
        d.ellipse((cx - r + r * 0.3, cy - r * 0.95, cx + r * 1.25, cy + r * 0.95), fill=(238, 36, 49))
        for i in range(5):
            a = -math.pi / 2 + 2 * math.pi * i / 5
            _star(d, W4 * 0.31 + math.cos(a) * H4 * 0.08, cy + math.sin(a) * H4 * 0.08, H4 * 0.028, WHITE)
    elif code == "kr":
        cx, cy, r = W4 / 2, H4 / 2, H4 * 0.25
        d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=(205, 46, 58))
        d.pieslice((cx - r, cy - r, cx + r, cy + r), 0, 180, fill=(0, 71, 160))
        d.ellipse((cx - r, cy - r / 2, cx, cy + r / 2), fill=(205, 46, 58))
        d.ellipse((cx, cy - r / 2, cx + r, cy + r / 2), fill=(0, 71, 160))
        for k, (bx, by) in enumerate(((0.2, 0.25), (0.8, 0.25), (0.2, 0.75), (0.8, 0.75))):   # 四すみの卦（かんたんに）
            for j in range(3):
                y = H4 * by + (j - 1) * H4 * 0.055
                ang = 1 if (k in (0, 3)) else -1
                x0, x1 = W4 * bx - H4 * 0.11, W4 * bx + H4 * 0.11
                d.line((x0, y - ang * (x0 - W4 * bx) * 0.6, x1, y - ang * (x1 - W4 * bx) * 0.6), fill=BLACK, width=int(H4 * 0.035))
    im = im.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w + 2, h + 2), (150, 150, 150, 255))
    out.paste(im, (1, 1))
    return out


FLAG_OF = {"日本": "jp", "アメリカ": "us", "台湾": "tw", "ヨーロッパ": "eu", "イギリスの旅行者": "gb", "江戸の子ども": "jp",
           "寺子屋の師匠": "jp", "八百屋のおかみ": "jp", "シンガポール": "sg", "韓国": "kr", "日本の会社員": "jp"}
FLAGS = False   # 国どうしの寸劇で True（役名の札に国旗）


def label_img(text, size=72, flag=None):
    """役名：白い四角に黒い太字。flag があれば文字の左に小さい国旗。"""
    t = text_img(text, size, fill=BLACK)
    fl = flag_img(flag, int(size * 0.62)) if flag else None
    fw = fl.width + 14 if fl else 0
    im = Image.new("RGBA", (t.width + 28 + fw, t.height + 22), (255, 255, 255, 255))
    if fl:
        im.alpha_composite(fl, (14, (im.height - fl.height) // 2))
    im.alpha_composite(t, (14 + fw, 11))
    return im


def put(out, pil, x, y):
    """左上 (x, y) に PIL の RGBA を重ねる。"""
    img, a = R.to_np(pil)
    R.over(out, img, a, int(x), int(y))


def cover(path):
    im = Image.open(bg_path(path)).convert("RGB")
    k = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * k + 0.5), int(im.height * k + 0.5)), Image.LANCZOS)
    x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    return np.asarray(im.crop((x0, y0, x0 + W, y0 + H)))[:, :, ::-1].astype(np.float32) / 255


def rays(out, cx, cy, n=150, col=(0, 215, 255), seed=7):
    """マンガふうの集中線（10/21 ユーザー指定「もっとかっこよく」）。色は BGR。
    外側が太く中心に向かって細くなる三角の線を細かく並べ、中心はぽっかり空ける。線のふちに濃い色、外側ほど少し暗く。"""
    rng = np.random.default_rng(seed)
    hh, ww = out.shape[:2]
    R_ = math.hypot(ww, hh)
    ov = np.zeros((hh, ww), np.float32)       # 線の濃さ
    edge = np.zeros((hh, ww), np.float32)     # 線のふち
    for i in range(n):
        a = 2 * math.pi * (i + rng.uniform(-0.35, 0.35)) / n
        r0 = rng.uniform(300, 520) * (1.0 if i % 3 else 1.35)   # 内側のはじまり（ばらつかせる）
        half = rng.uniform(0.004, 0.013) * (2.2 if i % 7 == 0 else 1.0)   # 外側の太さ（ときどき太い線）
        tip = (cx + math.cos(a) * r0, cy + math.sin(a) * r0)
        p1 = (cx + math.cos(a - half) * R_, cy + math.sin(a - half) * R_)
        p2 = (cx + math.cos(a + half) * R_, cy + math.sin(a + half) * R_)
        pts = np.array([tip, p1, p2], np.int32)
        cv2.fillConvexPoly(ov, pts, 1.0, cv2.LINE_AA)
        cv2.polylines(edge, [pts], True, 1.0, 3, cv2.LINE_AA)
    # 中心は空け、外側ほどくっきり
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    d = np.hypot(xx - cx, yy - cy)
    fade = np.clip((d - 260) / 260, 0, 1)
    ov *= fade
    edge *= fade
    dark = np.clip(1 - 0.35 * np.clip((d - 400) / 900, 0, 1), 0.6, 1)[..., None]   # まわりを少し暗く（周辺減光）
    out *= dark
    c = np.array(col, np.float32) / 255
    ec = c * 0.45                              # ふちは濃い色
    out[:] = out * (1 - edge[..., None]) + ec * edge[..., None]
    out[:] = out * (1 - ov[..., None]) + c * ov[..., None]


def bubble_img(path, w=760, h=560):
    """白い丸い吹き出し（黒い線・左下に向かうしっぽ）の中にイラスト。"""
    im = Image.new("RGBA", (w, h + 90), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(w * 0.22, h * 0.80), (w * 0.10, h + 80), (w * 0.38, h * 0.88)], fill=WHITE, outline=BLACK, width=8)
    d.ellipse((6, 6, w - 6, h - 6), fill=WHITE, outline=BLACK, width=8)
    d.polygon([(w * 0.23, h * 0.78), (w * 0.13, h + 62), (w * 0.37, h * 0.86)], fill=WHITE)
    ill = Image.open(bg_path(path)).convert("RGB")
    box = Image.eval(ill.convert("L"), lambda v: 255 if v < 235 else 0).getbbox()   # 白い余白を落とす
    ill = (ill.crop(box) if box else ill).convert("RGBA")
    k = min(w * 0.58 / ill.width, h * 0.70 / ill.height)
    ill = ill.resize((int(ill.width * k), int(ill.height * k)), Image.LANCZOS)
    im.alpha_composite(ill, ((w - ill.width) // 2, (h - ill.height) // 2))
    return im


# ---- 語り・締め（render.build_audio に渡せるカット） ----

def intro(text, dur=3.6):
    """黒い画面に白い文字だけ（冒頭・時間を飛ばすところ）。音なし。"""
    return dict(kind="intro", text=text, dur=dur, fixed=True, no_pop=True, bgm={"file": None, "fade": 0.4})


def photo(name, text, dur=4.0, bgm=None):
    """黒い画面の真ん中に写真＋下に字幕。冒頭（最初の語り）は音なし、話の途中は BGM を続ける（bgm で曲を変えられる）。"""
    c = dict(kind="photo", photo=name, text=text, dur=dur, fixed=True, no_pop=True)
    if bgm is not None:
        c["bgm"] = bgm
    return c


# ---- 出だし（10/21 ユーザー指定：毎回「黒い画面＋白い文字」で始めない。下の型を回して使う） ----
# 「再構成したお話」は note=（左下の小さい札）で出だしの数カットに出す（ルールは守ったまま、黒い画面にしない）

def hook(bg, big, sub=None, color="yellow", dur=3.0, rays=False, cat=None, note=None, se="jan", bgm=None):
    """つかみ：背景を画面いっぱいに、真ん中に大きな文字（クイズ・数字ドン・ひとこと）。sub は上の小さい文字。
    cat=(素材, "L"/"R") で猫を1匹そえる。"""
    c = dict(kind="hook", bg=bg, big=big, sub=sub, color=color, dur=dur, rays=rays, fixed=True, no_pop=True, se=se,
             cats=[dict(a=cat[0], side=cat[1], mute=True)] if cat else [])
    if note:
        c["note"] = note
    if bgm:
        c["bgm"] = bgm
    return c


def full(bg, text, dur=4.0, note=None, bgm=None, se=None):
    """語り：写真を画面いっぱいに（黒い画面にしない）、下に字幕。"""
    c = dict(kind="full", bg=bg, text=text, dur=dur, fixed=True, no_pop=True)
    if note:
        c["note"] = note
    if bgm:
        c["bgm"] = bgm
    if se:
        c["se"] = se
    return c


def note_img(text):
    t = text_img(text, 40, fill=WHITE)
    im = Image.new("RGBA", (t.width + 36, t.height + 22), (0, 0, 0, 170))
    im.alpha_composite(t, (18, 11))
    return im


def subscribe_card(dur=3.4):
    """チャンネル共通の「チャンネル登録よろしく！」の画面（寸劇では Scene.ending を使う）。"""
    return dict(kind="still", img=os.path.join(HERE, "parts", "common", "subscribe.png"), dur=dur, fixed=True, no_pop=True,
                se="chirin")


# ---- 寸劇の場面 ----

# 素材の声をそのまま使う猫（10/21 ユーザー指定）。しゃべる役がこの猫のときだけ元の音を鳴らす（ほかの猫は音を消す）
VOICE = {"huh_huh_cat",               # 「はぁ？」
         "despair_dramatic_kitten"}   # 泣く・絶望する


def _voice(cats, side):
    for k in cats:
        if k["side"] == side and k["a"] in VOICE:
            k["mute"] = False


PACE = 0.3   # セリフ1つごとの「間」を少し長めに（10/21：動画は3〜4分。速すぎると内容が追えない）
SLOTS = {2: {"L": 330, "R": W - 330}, 3: {"L": 270, "C": 930, "R": W - 260}}


class Scene:
    """1つの場面（背景1枚）。役ごとに今の猫・今のセリフを覚えて、1セリフ＝1カットを作る。

    sc = Scene("st04_arcade", [("海外留学生", "L", "dance_tabby_standing_cat"), ("日本人JK", "R", "punch_tabby_cat_reach")])
    sc.say("L", "日本人、写真に本気すぎる！！", cat="laugh_...")      # 話す猫を差しかえてセリフ
    sc.say("L", "りんご飴！！", add=True)                             # 同じ役のセリフを下に足す
    sc.zoom("L", "自然なのに盛る！？", color="yellow")                 # 画面ごとズーム＋大きな字幕
    sc.zoom("L", "浴衣だあああ！！", color="red", bubble="il_yukata")  # 吹き出しのイラストつき
    sc.zoom("R", "ずっと憧れてたんだよね", color="red", rays=True)     # 集中線
    sc.zoom("L", ["な、なにこれ…", "この胸の高鳴り…"], pos="mid")      # 顔のアップ＋真ん中に黄色を1行ずつ
    cuts += sc.cuts
    """

    def __init__(self, bg, roles, bgm=None, h=720):
        self.bg = bg
        self.order = [sd for _, sd, _ in roles]
        self.role = {sd: dict(label=lab, cat=cat, h=h, since=0.0, flip=False) for lab, sd, cat in roles}
        self.lines = {sd: [] for sd in self.order}
        self.age = {sd: 99 for sd in self.order}
        self.t = 0.0
        self.cuts = []
        self.bgm = bgm

    def enter(self, label, side, cat, h=None):
        """あとから役が増える（参考：教室に日本人JKが入ってくる）。"""
        if side not in self.role:
            self.order.append(side)
            self.lines[side], self.age[side] = [], 99
        self.role[side] = dict(label=label, cat=cat, h=h or 720, since=self.t, flip=False)

    def _set_cat(self, side, cat, h, flip):
        r = self.role[side]
        if cat and cat != r["cat"]:
            r.update(cat=cat, since=self.t)
        if h:
            r["h"] = h
        if flip is not None:
            r["flip"] = flip

    def _snapshot(self):
        cats = [dict(a=self.role[sd]["cat"], side=sd, label=self.role[sd]["label"], h=self.role[sd]["h"],
                     flip=self.role[sd]["flip"], ss=self.t - self.role[sd]["since"], mute=True) for sd in self.order]
        lines = {sd: list(self.lines[sd]) for sd in self.order if self.age[sd] <= 1 and self.lines[sd]}
        return cats, lines

    def _push(self, c, dur):
        c.update(dur=dur, fixed=True, no_pop=True)
        if self.bgm and not self.cuts:
            c["bgm"] = self.bgm
        self.cuts.append(c)
        self.t += dur

    @staticmethod
    def _dur(text):
        return min(3.6, max(1.6, 1.0 + 0.1 * len(text))) + PACE

    def say(self, side, text, cat=None, dur=None, add=False, h=None, flip=None, se=None, clear_others=False):
        """セリフ。cat で話す猫を差しかえる。add=True で同じ役の前のセリフを残して下に足す。"""
        self._set_cat(side, cat, h, flip)
        for sd in self.order:
            self.age[sd] += 1
        self.lines[side] = (self.lines[side] + [text]) if add else [text]
        self.age[side] = 0
        if clear_others:
            for sd in self.order:
                if sd != side:
                    self.age[sd] = 99
        cats, lines = self._snapshot()
        _voice(cats, side)
        c = dict(kind="beat", bg=self.bg, cats=cats, lines=lines, n=len(self.order), speaker=side)
        if se:
            c["se"] = se
        self._push(c, dur or self._dur(text))

    def zoom(self, side, text, color="white", cat=None, dur=None, pos="bottom", rays=False, bubble=None, z=None,
             h=None, se=None):
        """強調：画面ごと side の猫へズーム＋大きな字幕。text をリストにすると1行ずつ足す（pos="mid" は顔のアップ）。"""
        self._set_cat(side, cat, h, None)
        texts = text if isinstance(text, list) else [text]
        step = [self._dur(t) for t in texts]
        cats, _ = self._snapshot()
        _voice(cats, side)
        c = dict(kind="beat", bg=self.bg, cats=cats, lines={}, n=len(self.order),
                 zoom=dict(side=side, z=z or (2.0 if pos == "mid" else 1.5), pos=pos, color="yellow" if pos == "mid" else color,
                           texts=texts, at=list(np.cumsum([0] + step[:-1])), rays=rays, bubble=bubble))
        if se:
            c["se"] = se
        for sd in self.order:   # ズームのあとは前のセリフを消す
            self.age[sd] = 99
        self._push(c, dur or sum(step))

    def ending(self, cat, text="チャンネル登録、お願いしまーす", dur=3.4, h=None):
        """締め：役の猫をみんな同じ踊る猫にして、下に大きな白い字幕。"""
        for sd in self.order:
            self.role[sd].update(cat=cat, since=self.t, flip=False, h=h or self.role[sd]["h"])
        cats, _ = self._snapshot()
        self._push(dict(kind="beat", bg=self.bg, cats=cats, lines={}, n=len(self.order), caption=text), dur)


class Renderer:
    def __init__(self, c):
        self.c = c
        k = c["kind"]
        self.clips = []
        if k == "intro":
            self.base = np.zeros((H, W, 3), np.float32)
            t = text_img(c["text"], 80, max_w=W - 120)
            put(self.base, t, (W - t.width) / 2, (H - t.height) / 2)
        elif k == "photo":
            self.base = np.zeros((H, W, 3), np.float32)
            t = text_img(c["text"], 80, stroke=4, max_w=W - 80)
            im = Image.open(bg_path(c["photo"])).convert("RGB")
            s = min(1220 / im.width, min(800, H - 50 - t.height - 70) / im.height)   # 字幕が3行でも入るように写真を縮める
            im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS).convert("RGBA")
            put(self.base, im, (W - im.width) / 2, 50)
            put(self.base, t, (W - t.width) / 2, 50 + im.height + (H - 50 - im.height - t.height) / 2)
        elif k == "still":
            self.base = cover(c["img"])
        elif k == "hook":
            self.base = cover(c["bg"]) * 0.72
            if c.get("rays"):
                rays(self.base, W / 2, H / 2)
            fill, st = CAP[c["color"]]
            self.big = text_img(c["big"], 170, fill=fill, stroke=12, stroke_col=st, max_w=W - 120)
            self.sub = text_img(c["sub"], 70, stroke=7, max_w=W - 120) if c.get("sub") else None
            self.clips = [R.Clip(k_["a"]) for k_ in c["cats"]]
        elif k == "full":
            self.base = cover(c["bg"])
            g = np.linspace(0, 1, 360, dtype=np.float32)[:, None, None] ** 1.5 * 0.75   # 下を暗くして字幕を読みやすく
            self.base[H - 360:] *= 1 - g
            t = text_img(c["text"], 76, stroke=6, max_w=W - 100)
            put(self.base, t, (W - t.width) / 2, H - t.height - (110 if c.get("note") else 60))   # 左下の札と重ねない
        else:
            self._init_beat(c)
        self.note = note_img(c["note"]) if c.get("note") else None

    def _init_beat(self, c):
        self.base = cover(c["bg"])
        slots = SLOTS[3 if c["n"] >= 3 else 2]
        zm = c.get("zoom")
        self.cx = {k_["side"]: slots[k_["side"]] for k_ in c["cats"]}
        if zm and zm["rays"]:
            k_ = next(k_ for k_ in c["cats"] if k_["side"] == zm["side"])
            rays(self.base, self.cx[zm["side"]], H - k_["h"] * 0.55)
        self.clips = [R.Clip(k_["a"], flip=k_["flip"]) for k_ in c["cats"]]
        self.bbox = {}
        # 役名：左の役は左上、右の役は右上、真ん中の役は真ん中の上（参考どおり画面の上に固定）
        self.labels = []
        for k_ in c["cats"]:
            lab = label_img(k_["label"], flag=k_.get("flag") or FLAG_OF.get(k_["label"]) if FLAGS else None)
            x = {"L": 40, "R": W - 40 - lab.width}.get(k_["side"], self.cx[k_["side"]] - lab.width / 2)
            self.labels.append([lab, x, 40 if k_["side"] != "C" else 70, k_["side"]])
        # 真ん中の役名が左右の役名と重なるときは、下の段にずらす（長い役名のとき）
        side = {sd: (x, x + lab.width) for lab, x, y, sd in self.labels}
        for it in self.labels:
            if it[3] == "C":
                x0, x1 = it[1], it[1] + it[0].width
                if ("L" in side and x0 < side["L"][1] + 16) or ("R" in side and x1 > side["R"][0] - 16):
                    it[2] = 40 + it[0].height + 14
        self.labels = [tuple(it[:3]) for it in self.labels]
        # セリフ：左の役は左寄せ、右の役は右寄せ、真ん中は猫の下あたり。同じ役の行は下に足す
        self.lines = []
        spk = c.get("speaker")
        order = sorted(c["lines"], key=lambda sd: sd != spk)   # 今しゃべっている役から置く
        placed = []
        for sd in order:
            ims = [text_img(t, 72, stroke=7, max_w=W * 0.62) for t in c["lines"][sd]]
            hh = sum(im.height for im in ims) + 14 * (len(ims) - 1)
            xs = [{"L": 50, "R": W - 50 - im.width}.get(sd, self.cx[sd] - im.width / 2) for im in ims]
            x0, x1 = min(xs), max(x + im.width for x, im in zip(xs, ims))
            y = 760 - hh / 2
            # 前のセリフが今のセリフと横に重なるときは、上にずらす
            for px0, px1, py0, py1 in placed:
                if x0 < px1 and px0 < x1 and y < py1 and py0 < y + hh:
                    y = py0 - hh - 24
            placed.append((x0, x1, y, y + hh))
            for x, im in zip(xs, ims):
                self.lines.append((im, x, y))
                y += im.height + 14
        self.caps = []
        if zm:
            fill, st = CAP[zm["color"]]
            for t, at in zip(zm["texts"], zm["at"]):
                big = 120 if zm["pos"] == "mid" else 160
                self.caps.append((text_img(t, big, fill=fill, stroke=10, stroke_col=st, max_w=W - 80), at))
            self.bub = bubble_img(zm["bubble"]) if zm.get("bubble") else None
        if c.get("caption"):
            self.caps.append((text_img(c["caption"], 130, stroke=10, max_w=W - 80), 0.0))

    def frame(self, t):
        out = self._frame(t)
        if self.note is not None:
            out = out.copy() if out is self.base else out
            put(out, self.note, 30, H - self.note.height - 26)
        return out

    def _frame(self, t):
        c = self.c
        if c["kind"] == "hook":
            out = self.base.copy()
            for k_, clip in zip(c["cats"], self.clips):
                fr, a = clip.frame(t)
                s = 500 / fr.shape[0]
                w, h = int(fr.shape[1] * s), int(fr.shape[0] * s)
                img = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
                al = cv2.resize(a.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA)
                R.over(out, img, al, int((200 if k_["side"] == "L" else W - 200) - w / 2), H + 30 - h)
            k = 1.0 if t > 0.18 else 1.6 - 0.6 * (t / 0.18)   # ドンと出る
            big = self.big if k == 1.0 else self.big.resize((int(self.big.width * k), int(self.big.height * k)))
            y = H / 2 - big.height / 2 + (40 if self.sub else 0)
            put(out, big, (W - big.width) / 2, y)
            if self.sub is not None and t > 0.1:
                put(out, self.sub, (W - self.sub.width) / 2, H / 2 - self.big.height / 2 - self.sub.height - 10)
            return out
        if c["kind"] != "beat":
            return self.base
        out = self.base.copy()
        tops, acx = {}, {}
        for i, (k_, clip) in enumerate(zip(c["cats"], self.clips)):
            fr, a = clip.frame(t + k_["ss"])
            if i not in self.bbox:   # 素材の余白を落とし、h は見えている猫の高さにする
                ys, xs = np.nonzero(a > 0.5)
                if len(ys):
                    m = int(0.04 * fr.shape[0])
                    ya, yb = np.percentile(ys, [0.5, 99.9]).astype(int)   # 端のごみの点は数えない
                    xa, xb = np.percentile(xs, [0.5, 99.5]).astype(int)
                    self.bbox[i] = (max(ya - m, 0), min(yb + 1, fr.shape[0]), max(xa - m, 0), min(xb + m, fr.shape[1]))
                else:
                    self.bbox[i] = (0, fr.shape[0], 0, fr.shape[1])
            y0_, y1_, x0_, x1_ = self.bbox[i]
            fr, a = fr[y0_:y1_, x0_:x1_], a[y0_:y1_, x0_:x1_]
            s = k_["h"] / fr.shape[0]
            w, h = max(1, int(fr.shape[1] * s)), max(1, int(fr.shape[0] * s))
            img = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
            al = cv2.resize(a.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA)
            cx = min(max(self.cx[k_["side"]], w * 0.4), W - w * 0.4)   # 横に広い素材も画面から大きくはみ出さないように
            R.over(out, img, al, int(cx - w / 2), H + 30 - h)
            tops[k_["side"]] = H + 30 - h
            acx[k_["side"]] = cx
        for lab, x, y in self.labels:
            put(out, lab, x, y)
        zm = c.get("zoom")
        if zm:   # 画面ごと話す猫へズーム（役名もいっしょに大きくなって上が切れる）
            z = zm["z"]
            cx = acx[zm["side"]]
            cy = tops[zm["side"]] + (H - tops[zm["side"]]) * (0.30 if zm["pos"] == "mid" else 0.42)
            ww, hh = W / z, H / z
            x0 = min(max(cx - ww / 2, 0), W - ww)
            y0 = min(max(cy - hh / 2, 0), H - hh)
            out = cv2.resize(out[int(y0):int(y0 + hh), int(x0):int(x0 + ww)], (W, H), interpolation=cv2.INTER_LINEAR)
            if self.bub is not None:
                put(out, self.bub, W - self.bub.width - 60, 30)
            shown = [im for im, at in self.caps if t >= at]
            if zm["pos"] == "mid":
                y = H * 0.50
                for im in shown:
                    put(out, im, (W - im.width) / 2, y)
                    y += im.height + 30
            elif shown:
                im = shown[-1]
                put(out, im, (W - im.width) / 2, H - im.height - 70)
        else:
            for im, x, y in self.lines:
                put(out, im, x, y)
            for im, _ in self.caps:
                put(out, im, (W - im.width) / 2, H - im.height - 80)
        return out

    def close(self):
        for cl in self.clips:
            if getattr(cl, "cap", None) is not None:
                cl.cap.release()


def remux(cs, out_path):
    """音だけ作り直す（映像はそのまま）。"""
    durs = [c["dur"] for c in cs]
    starts = list(np.cumsum([0] + durs[:-1]))
    total = float(sum(durs))
    wav = out_path + ".audio.f32"
    R.build_audio(cs, starts, durs, total).tofile(wav)
    tmp = out_path.replace(".mp4", "_a.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out_path, "-f", "f32le", "-ar", str(R.SR), "-ac", "2", "-i", wav, "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", tmp],
                   check=True)
    os.replace(tmp, out_path)
    os.remove(wav)


def run(cs, out_path, prev=None):
    durs = [c["dur"] for c in cs]
    starts = list(np.cumsum([0] + durs[:-1]))
    total = float(sum(durs))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wav = out_path + ".audio.f32"
    R.build_audio(cs, starts, durs, total).tofile(wav)
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(R.FPS), "-i", "-",
         "-f", "f32le", "-ar", str(R.SR), "-ac", "2", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", out_path],
        stdin=subprocess.PIPE)
    if prev:
        os.makedirs(prev, exist_ok=True)
    fno = 0
    for i, c in enumerate(cs):
        rd = Renderer(c)
        end = int(round((starts[i] + durs[i]) * R.FPS))
        shot = False
        while fno < end:
            tt = fno / R.FPS - starts[i]
            u8 = (np.clip(rd.frame(tt), 0, 1) * 255).astype(np.uint8)
            proc.stdin.write(u8.tobytes())
            if prev and not shot and tt > durs[i] - 0.2:
                cv2.imwrite(os.path.join(prev, f"{i:02d}.jpg"), u8, [cv2.IMWRITE_JPEG_QUALITY, 80])
                shot = True
            fno += 1
        rd.close()
        print(f"\r{i + 1}/{len(cs)}  {fno / R.FPS:5.1f}s / {total:.1f}s", end="", flush=True)
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    print(f"\n-> {out_path} ({total:.1f}s)")
