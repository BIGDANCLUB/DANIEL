"""物語（再現ドラマ）形式の横動画。10/18 ユーザー提供の参考動画のフォーマットをまねる。

参考の作り（1920x1080）：
  1. 冒頭：黒い画面に白い太字だけ（縁なし・真ん中）。1〜2行ずつ切り替える。音なし
  2. 導入：黒い画面の真ん中に写真（横 6割ほど）＋下に白い太字の字幕（細い黒縁）。音なし
  3. 寸劇：写真の背景を全面に、猫ミームを左右に大きく。猫の頭の上に役名（白い四角に黒い太字）。
     セリフは白い太字＋黒縁。左の猫は左寄せ、右の猫は右寄せで、前のセリフを残したまま下に足していく。
     BGM は寸劇から始まる
使い方は story_18_demo.py を見る。
"""
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
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("18_story",)]
_FONTS = {}


def font(size):
    """参考に近い太さ（Noto Sans JP の Bold）。"""
    if size not in _FONTS:
        P.font("black", 40)   # フォントを用意させる
        f = ImageFont.truetype(os.path.join(P.FONT_DIR, P.FONTS["black"][0]), size)
        f.set_variation_by_name("Bold")
        _FONTS[size] = f
    return _FONTS[size]


def bg_path(name):
    if os.path.isabs(name) and os.path.exists(name):
        return name
    for d in BGS:
        for ext in (".png", ".jpg"):
            p = os.path.join(d, name + ext)
            if os.path.exists(p):
                return p
    raise FileNotFoundError(name)


def text_img(text, size, fill=WHITE, stroke=0, align="center"):
    """1行または複数行の文字（\\n で改行）を RGBA で。"""
    f = font(size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    lines = text.split("\n")
    ws = [d0.textlength(ln, font=f) for ln in lines]
    lh = int(size * 1.32)
    im = Image.new("RGBA", (int(max(ws)) + stroke * 2 + 12, lh * len(lines) + stroke * 2 + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (ln, w) in enumerate(zip(lines, ws)):
        x = {"center": (im.width - w) / 2, "left": stroke + 6, "right": im.width - w - stroke - 6}[align]
        d.text((x, stroke + 6 + i * lh), ln, font=f, fill=fill, stroke_width=stroke, stroke_fill=BLACK)
    return im.crop(im.getbbox())


def label_img(text, size=84):
    """役名：白い四角に黒い太字。"""
    t = text_img(text, size, fill=BLACK)
    im = Image.new("RGBA", (t.width + 30, t.height + 24), (255, 255, 255, 255))
    im.alpha_composite(t, (15, 12))
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


# ---- カット（render.build_audio に渡せる形） ----

def intro(text, dur=3.6):
    """冒頭：黒い画面に白い文字だけ。"""
    return dict(kind="intro", text=text, dur=dur, fixed=True, no_pop=True)


def photo(name, text, dur=4.0):
    """導入：黒い画面の真ん中に写真、下に字幕。"""
    return dict(kind="photo", photo=name, text=text, dur=dur, fixed=True, no_pop=True)


def skit(bg, cats, lines, dur, bgm=None, se=None):
    """寸劇。cats=[(素材, 役名, "L"/"R", 高さ)]、lines=[(セリフ, "L"/"R", 出る秒)]。
    猫の音は消す（参考は BGM だけ）。"""
    ks = [dict(a=a, label=lab, side=sd, h=h, mute=True) for a, lab, sd, h in cats]
    c = dict(kind="skit", bg=bg, cats=ks, lines=lines, dur=dur, fixed=True, no_pop=True)
    if bgm:
        c["bgm"] = bgm
    if se:
        c["se"] = se
    return c


class Renderer:
    def __init__(self, c):
        self.c = c
        k = c["kind"]
        if k == "intro":
            self.base = np.zeros((H, W, 3), np.float32)
            t = text_img(c["text"], 88)
            put(self.base, t, (W - t.width) / 2, (H - t.height) / 2)
        elif k == "photo":
            self.base = np.zeros((H, W, 3), np.float32)
            im = Image.open(bg_path(c["photo"])).convert("RGB")
            s = min(1180 / im.width, 760 / im.height)
            im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS).convert("RGBA")
            put(self.base, im, (W - im.width) / 2, 60)
            t = text_img(c["text"], 84, stroke=5)
            put(self.base, t, (W - t.width) / 2, 60 + im.height + (H - 60 - im.height - t.height) / 2)
        else:
            self.base = cover(c["bg"])
            self.clips = [R.Clip(k_["a"], flip=(k_["side"] == "R")) for k_ in c["cats"]]
            self.labels = [label_img(k_["label"]) for k_ in c["cats"]]
            self.lines = [(text_img(t, 84, stroke=8), sd, at) for t, sd, at in c["lines"]]

    def frame(self, t):
        if self.c["kind"] != "skit":
            return self.base
        out = self.base.copy()
        for k, clip, lab in zip(self.c["cats"], self.clips, self.labels):
            fr, a = clip.frame(t)
            s = k["h"] / fr.shape[0]
            w, h = max(1, int(fr.shape[1] * s)), max(1, int(fr.shape[0] * s))
            img = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
            al = cv2.resize(a.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA)
            cx = k.get("x", 270 if k["side"] == "L" else W - 270)
            x0, y0 = int(cx - w / 2), H + k.get("drop", 60) - h
            R.over(out, img, al, x0, y0)
            put(out, lab, min(max(cx - lab.width / 2, 40), W - 40 - lab.width), max(40, y0 + k.get("label_dy", 60)))
        rows = {"L": 0, "R": 0}
        n = 0
        for im, sd, at in self.lines:
            if t < at:
                continue
            y = 640 + n * 108   # 参考どおり、画面の下寄りに1行ずつ足す
            put(out, im, 40 if sd == "L" else W - 40 - im.width, y)
            rows[sd] += 1
            n += 1
        return out

    def close(self):
        for c in getattr(self, "clips", []):
            if getattr(c, "cap", None) is not None:
                c.cap.release()


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
