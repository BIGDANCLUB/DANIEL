"""「年収別」型の1分ショート（縦 1080x1920）。10/23 ユーザー提供の参考動画3本（年収別リアルな生活の違い・地震反応の違い・
1番損する夫婦年収）の作りを、そのまままねる。長さは厳密に 59.9 秒（10/23 ユーザー指定）。

参考の作り（576x1024 の参考を 1080x1920 に 1.875 倍）
- 上：背景が少し見えて、その下に黒い帯（y 206〜516）。1行目は赤い極太（白い細縁）、2行目は黄色の極太（黒い細縁）
- 帯の下：区切りの札（赤地・白い枠・白い太字「240万」など）
- 札の下：セリフ（白い太字＋黒い縁、1〜2行）
- 背景：場面（区切り）ごとに1枚の絵を画面いっぱい
- 猫：白いふち取り（ステッカーふう）。区切りの頭は主役の猫1匹を真ん中に大きく＋白い集中線＋「手取り○万！」。
  そのあと会話：左に相手（足元に白い四角の札「友達」など）、右に主役（札なし）。セリフごとに猫を差しかえる
- 音：BGM ＋ しゃべる猫の素材の音。最後にチャンネル登録の画面は入れない（参考どおり）
使い方は short_income_demo.py
"""
import math
import os
import subprocess
import zlib

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import parts as P
import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
TOTAL = 59.9   # 厳密に 59.9 秒
WHITE, BLACK, RED, YELLOW = (255, 255, 255), (0, 0, 0), (225, 10, 10), (255, 222, 0)
BAND = (206, 516)
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("income", "02_october", "14_japan", "17_imamori", "04_leak", "16_tenchim",
                                                       "15_vambi", "01_todai", "03_kodomo_nisa")]
_F = {}


def font(size):
    if size not in _F:
        P.font("black", 40)
        f = ImageFont.truetype(os.path.join(P.FONT_DIR, P.FONTS["black"][0]), size)
        f.set_variation_by_name("Black")
        _F[size] = f
    return _F[size]


def bg_path(n):
    for d in BGS:
        p = os.path.join(d, n + ".png")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(n)


def text(t, size, fill, stroke=0, stroke_col=BLACK, max_w=W - 40):
    while True:
        f = font(size)
        d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        lines = t.split("\n")
        ws = [d0.textlength(ln, font=f) for ln in lines]
        if max(ws) + stroke * 2 <= max_w or size < 30:
            break
        size -= 3
    lh = int(size * 1.18)
    im = Image.new("RGBA", (int(max(ws)) + stroke * 2 + 10, lh * len(lines) + stroke * 2 + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (ln, w) in enumerate(zip(lines, ws)):
        d.text(((im.width - w) / 2, stroke + 4 + i * lh), ln, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_col)
    return im.crop(im.getbbox())


def over(dst, src, alpha, x, y):
    """縦画面用の重ね合わせ（render.over は横画面の大きさで切るため）。"""
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, dst.shape[1]), min(y + h, dst.shape[0])
    if x1 <= x0 or y1 <= y0:
        return
    a = alpha[y0 - y:y1 - y, x0 - x:x1 - x]
    if a.ndim == 2:
        a = a[..., None]
    d = dst[y0:y1, x0:x1]
    d *= 1 - a
    d += src[y0 - y:y1 - y, x0 - x:x1 - x] * a


def put(out, pil, cx, cy):
    img, a = R.to_np(pil)
    over(out, img, a, int(cx - pil.width / 2), int(cy - pil.height / 2))


def cover(name):
    im = Image.open(bg_path(name)).convert("RGB")
    k = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * k + 0.5), int(im.height * k + 0.5)), Image.LANCZOS)
    x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    return np.asarray(im.crop((x0, y0, x0 + W, y0 + H)))[:, :, ::-1].astype(np.float32) / 255


def speed_lines(out, cx, cy, seed=3):
    """白い集中線（参考どおり、明るい背景に白い細い三角の線）。"""
    rng = np.random.default_rng(seed)
    ov = np.zeros(out.shape[:2], np.float32)
    Rr = math.hypot(W, H)
    for i in range(110):
        a = 2 * math.pi * (i + rng.uniform(-0.4, 0.4)) / 110
        r0 = rng.uniform(380, 620)
        half = rng.uniform(0.003, 0.010)
        pts = np.array([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a - half) * Rr, cy + math.sin(a - half) * Rr),
                        (cx + math.cos(a + half) * Rr, cy + math.sin(a + half) * Rr)], np.int32)
        cv2.fillConvexPoly(ov, pts, 1.0, cv2.LINE_AA)
    out[:] = out * (1 - ov[..., None] * 0.92) + ov[..., None] * 0.92


def title_band(top, sub):
    """上の黒い帯（2行）。"""
    im = Image.new("RGBA", (W, BAND[1] - BAND[0]), (0, 0, 0, 255))
    t1 = text(top, 176, RED, stroke=4, stroke_col=WHITE)
    t2 = text(sub, 110, YELLOW, stroke=4, stroke_col=BLACK)
    im.alpha_composite(t1, ((W - t1.width) // 2, 290 - BAND[0] - t1.height // 2))
    im.alpha_composite(t2, ((W - t2.width) // 2, 448 - BAND[0] - t2.height // 2))
    return im


def tag_box(t):
    """区切りの札：赤地・白い枠・白い太字。"""
    tx = text(t, 112, WHITE, stroke=3, stroke_col=(150, 0, 0))
    im = Image.new("RGBA", (max(tx.width + 80, 380), 142), (255, 255, 255, 255))
    ImageDraw.Draw(im).rectangle((6, 6, im.width - 7, im.height - 7), fill=RED)
    im.alpha_composite(tx, ((im.width - tx.width) // 2, (im.height - tx.height) // 2))
    return im


def name_tag(t):
    tx = text(t, 92, BLACK)
    im = Image.new("RGBA", (tx.width + 48, tx.height + 34), (255, 255, 255, 255))
    im.alpha_composite(tx, (24, 17))
    return im


# ---- カット ----

def intro(bg, tag, say, cat, dur=2.4, bgm=None, se="don_hit", quake=0):
    """区切りの頭：主役の猫1匹を真ん中に大きく＋白い集中線＋大きなセリフ。"""
    c = dict(kind="intro", bg=bg, tag=tag, say=say, cats=[dict(a=cat, mute=False, x=540, h=820, w=920, bottom=1680)], dur=dur, fixed=True,
             no_pop=True, se=se, quake=quake)
    if bgm:
        c["bgm"] = bgm
    return c


def talk(bg, tag, say, left, right, who="R", dur=2.5, label="友達", se=None, lscale=1.0, rscale=1.0, quake=0):
    """会話：左に相手（札つき）、右に主役。しゃべる側の猫だけ音を出す。left/right は素材名。"""
    # 左右とも幅600まで（中心は480ずつ離す → 重なっても120くらいまで。大きく重ならない・10/23）
    cats = [dict(a=left, mute=who != "L", x=300, h=860, w=640, bottom=1580, label=label),
            dict(a=right, mute=who != "R", x=780, h=860, w=640, bottom=1580)]
    for k, sc in zip(cats, (lscale, rscale)):   # この場面だけ猫を大きく（多少の重なりはOK・10/23）
        k["h"], k["w"] = k["h"] * sc, k["w"] * sc
    c = dict(kind="talk", bg=bg, tag=tag, say=say, cats=cats, quake=quake, dur=dur, fixed=True, no_pop=True)
    if se:
        c["se"] = se
    return c


_BBOX = {}


def clip_bbox(name):
    """素材の中で猫が見えている範囲（数枚のフレームの中央値）。最初の1枚だけで決めると、ノイズや動きで猫が小さくなるため。"""
    if name not in _BBOX:
        cl = R.Clip(name)
        n = max(1, int(cl.n / cl.fps))
        boxes = []
        for t in np.linspace(0.2, max(0.3, n - 0.3), 8):
            fr, a = cl.frame(float(t))
            ys, xs = np.nonzero(a > 0.5)
            if len(ys) < 200:
                continue
            ya, yb = np.percentile(ys, [1, 99.5])
            xa, xb = np.percentile(xs, [1, 99])
            boxes.append((ya, yb, xa, xb))
        if getattr(cl, "cap", None) is not None:
            cl.cap.release()
        if boxes:
            b = np.median(np.array(boxes), 0).astype(int)
            _BBOX[name] = (b[0], b[1] + 1, b[2], b[3] + 1)
        else:
            _BBOX[name] = (0, fr.shape[0], 0, fr.shape[1])
    return _BBOX[name]


class Renderer:
    _sticker = {}

    def __init__(self, c, band):
        self.c, self.band = c, band
        self.base = cover(c["bg"])
        if c["kind"] == "intro":
            speed_lines(self.base, W / 2, 1150)
        self.tag = tag_box(c["tag"])
        big = c["kind"] == "intro"
        self.say = text(c["say"], 112 if big else 80, WHITE, stroke=8 if big else 7, max_w=W - 60)
        self.say_y = 800 if big else 790
        self.clips = [R.Clip(k["a"]) for k in c["cats"]]
        self.labels = [name_tag(k["label"]) if k.get("label") else None for k in c["cats"]]
        self.bbox = {}
        if c.get("quake", 0) >= 2:
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
            self.vignette = np.clip((d - 0.75) / 0.5, 0, 1).astype(np.float32)
            g = text("ゴゴゴゴ", 120, (120, 30, 160), stroke=8, stroke_col=WHITE)
            self.gogo = [g.rotate(a_, expand=True, resample=Image.BICUBIC) for a_ in (-18, 14, -10, 20)]

    def cat_img(self, i, k, t):
        fr, a = self.clips[i].frame(t + 0.25)   # 素材の最初の1枚が真っ黒なものがある（huh_huh_cat など）ので少し先から
        if i not in self.bbox:   # 余白を落として、見えている猫の大きさで決める（素材全体から1回だけ計算・どの場面でも同じ大きさ）
            self.bbox[i] = clip_bbox(k["a"])
        y0, y1, x0, x1 = self.bbox[i]
        fr, a = fr[y0:y1, x0:x1], a[y0:y1, x0:x1]
        s = min(k["h"] / fr.shape[0], k.get("w", 10 ** 6) / fr.shape[1])   # 高さと幅の両方に収める（重なり・はみ出しを防ぐ・10/23）
        w, h = max(1, int(fr.shape[1] * s)), max(1, int(fr.shape[0] * s))
        img = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
        al = cv2.resize(a.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA)
        # 白いふち取り（ステッカーふう・参考どおり）
        pad = 14
        img = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
        al = cv2.copyMakeBorder(al, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
        edge = cv2.dilate((al > 0.4).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))).astype(np.float32)
        edge = cv2.GaussianBlur(edge, (3, 3), 0)
        img = img * al[..., None] + (1 - al[..., None]) * 1.0
        return img, np.maximum(al, edge)

    def frame(self, t):
        out = self.base.copy()
        c = self.c
        for i, k in enumerate(c["cats"]):
            s = 1.0 if t > 0.12 else 0.85 + 0.15 * (t / 0.12)   # ポンと出る
            img, al = self.cat_img(i, k, t)
            if s < 1:
                img = cv2.resize(img, None, fx=s, fy=s)
                al = cv2.resize(al, None, fx=s, fy=s)
            h, w = al.shape
            x0 = int(k["x"] - w / 2)
            x0 = min(max(x0, 20), W - w - 20)   # 画面からはみ出さない
            over(out, img, al, x0, int(k["bottom"] - h))
            if self.labels[i] is not None:
                put(out, self.labels[i], max(self.labels[i].width / 2 + 40, k["x"] - 60), k["bottom"])
        q = c.get("quake", 0)
        if q:   # 揺れの演出（10/24 ユーザー指定：震度が大きいほど派手に）
            amp = (8, 22, 46, 70)[min(q, 3)]
            dx = amp * (math.sin(t * 47) + 0.5 * math.sin(t * 113))
            dy = amp * 0.6 * (math.cos(t * 59) + 0.5 * math.sin(t * 97))
            rot = (0, 0.6, 1.6, 2.8)[min(q, 3)] * math.sin(t * 31)
            M_ = cv2.getRotationMatrix2D((W / 2, H / 2), rot, 1.04 if q >= 2 else 1.0)
            M_[0, 2] += dx
            M_[1, 2] += dy
            out = cv2.warpAffine(out, M_, (W, H), borderMode=cv2.BORDER_REFLECT)
            if q >= 2:   # 赤く点滅するふち
                pulse = 0.5 + 0.5 * math.sin(t * 14)
                vig = self.vignette * (0.35 + 0.45 * pulse) * (1.0 if q >= 3 else 0.6)
                out = out * (1 - vig[..., None]) + vig[..., None] * np.array([0.05, 0.05, 0.95], np.float32)
            if q >= 2:   # 「ゴゴゴゴ」の文字が画面のはしでふるえる
                for (gx, gy), im in zip(((150, 980), (930, 1150), (160, 1420), (920, 1700)), self.gogo):
                    put(out, im, gx + 10 * math.sin(t * 40 + gx), gy + 8 * math.cos(t * 37 + gy))
            if q >= 3 and int(t * 6) % 2 == 0:   # 白いフラッシュ（強い揺れ）
                out = out * 0.82 + 0.18
        b = R.to_np(self.band)
        over(out, b[0], b[1], 0, BAND[0])
        put(out, self.tag, W / 2, 600)
        put(out, self.say, W / 2, self.say_y + self.say.height / 2 - 40)
        return out

    def close(self):
        for cl in self.clips:
            if getattr(cl, "cap", None) is not None:
                cl.cap.release()


def run(cs, top, sub, out_path, prev=None, band=None, renderer=None):
    durs = [c["dur"] for c in cs]
    total = sum(durs)
    if abs(total - TOTAL) > 1e-6:   # 厳密に 59.9 秒（最後のカットで合わせる・最大±3秒）
        diff = TOTAL - total
        if abs(diff) > 3 or durs[-1] + diff < 1.5:
            raise SystemExit(f"長さ {total:.2f}秒。59.9秒に合わせるには {diff:+.2f}秒 の調整が必要です。カットを足すか削ってください")
        durs[-1] += diff
        cs[-1]["dur"] = durs[-1]
    starts = list(np.cumsum([0] + durs[:-1]))
    R.conan_confusion(cs, zlib.crc32(os.path.basename(out_path).encode()))   # 戸惑いの場面はコナンのひらめき（10/28）
    band = band or title_band(top, sub)
    renderer = renderer or Renderer
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wav = out_path + ".audio.f32"
    R.build_audio(cs, starts, durs, TOTAL).tofile(wav)
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(R.FPS), "-i", "-",
         "-f", "f32le", "-ar", str(R.SR), "-ac", "2", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", out_path],
        stdin=subprocess.PIPE)
    if prev:
        os.makedirs(prev, exist_ok=True)
    nframes = int(round(TOTAL * R.FPS))
    fno = 0
    for i, c in enumerate(cs):
        rd = renderer(c, band)
        end = min(nframes, int(round((starts[i] + durs[i]) * R.FPS)))
        shot = False
        while fno < end:
            tt = fno / R.FPS - starts[i]
            u8 = (np.clip(rd.frame(tt), 0, 1) * 255).astype(np.uint8)
            proc.stdin.write(u8.tobytes())
            if prev and not shot and tt > 1.0:
                cv2.imwrite(os.path.join(prev, f"{i:02d}.jpg"), u8, [cv2.IMWRITE_JPEG_QUALITY, 80])
                shot = True
            fno += 1
        rd.close()
        print(f"\r{i + 1}/{len(cs)}  {fno / R.FPS:5.1f}s / {TOTAL}s", end="", flush=True)
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    print(f"\n-> {out_path} ({TOTAL}s)")
