"""「自堕落シリーズ」の長尺横動画（1920x1080）。10/24 ユーザー提供の参考動画3本（30代独身が快活CLUBで過ごす1日）の作りをまねる。

参考の作り
- 場所ごとに背景の絵（写真ふう）を画面いっぱい。場所が変わるまで同じ背景
- 猫は1匹だけ（主人公の「俺」）。セリフ1つごとに別の猫ミームに差しかえる。真ん中に大きく、ふち取りなし
- 下に字幕：明朝体の太字・白・黒い縁。1〜2行。ひとりごとの語り（「〜だ。」「〜する。」）、声に出すセリフは「」
- 1つの字幕は2.5〜3秒くらい。ナレーションの声はない（猫ミームの音と小さめのBGM）
- 最後にチャンネル登録の画面は入れない（参考どおり）。長尺のルールで最後に subscribe.png を付ける
使い方は jidaraku_01_yakiniku.py
"""
import os
import subprocess
import urllib.request

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import income_short as I
import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
SERIF = os.path.join(HERE, "fonts", "NotoSerifJP.ttf")
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("jidaraku", "jidaraku/01_yakiniku", "02_october", "04_leak", "14_japan",
                                                       "01_todai", "16_tenchim", "15_vambi", "17_imamori")]
STANDIN = {}   # 背景が届くまでの仮（名前 → 手もちの背景）
_F = {}


def font(size):
    if size not in _F:
        if not os.path.exists(SERIF):
            os.makedirs(os.path.dirname(SERIF), exist_ok=True)
            urllib.request.urlretrieve("https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifjp/NotoSerifJP%5Bwght%5D.ttf",
                                       SERIF)
        f = ImageFont.truetype(SERIF, size)
        f.set_variation_by_name("Black")
        _F[size] = f
    return _F[size]


def bg_path(n):
    for d in BGS:
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            p = os.path.join(d, n + ext)
            if os.path.exists(p):
                return p
    if n in STANDIN:
        return bg_path(STANDIN[n])
    raise FileNotFoundError(n)


def cover(name):
    im = Image.open(bg_path(name)).convert("RGB")
    k = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * k + 0.5), int(im.height * k + 0.5)), Image.LANCZOS)
    x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    return np.asarray(im.crop((x0, y0, x0 + W, y0 + H)))[:, :, ::-1].astype(np.float32) / 255


def sub_img(t, size=84):
    """字幕：明朝体の太字・白・黒い縁（参考どおり）。"""
    f = font(size)
    t = t.replace("。", "").replace("、", " ")   # 自堕落シリーズの字幕は句読点なし（10/26 ユーザー指定）
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    lines = t.split("\n")
    ws = [d0.textlength(ln, font=f) for ln in lines]
    st = 8
    lh = int(size * 1.22)
    im = Image.new("RGBA", (int(max(ws)) + st * 2 + 10, lh * len(lines) + st * 2 + 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (ln, w) in enumerate(zip(lines, ws)):
        d.text(((im.width - w) / 2, st + 4 + i * lh), ln, font=f, fill=(255, 255, 255), stroke_width=st, stroke_fill=(0, 0, 0))
    return im.crop(im.getbbox())


def line(bg, cat, text, dur=3.0, h=760, x=960, bottom=1010, se=None, bgm=None, mute=False, flip=False):
    """字幕1つ＝1カット。猫は1匹。"""
    c = dict(bg=bg, text=text, dur=dur, fixed=True, no_pop=True, cats=[dict(a=cat, h=h, x=x, bottom=bottom, mute=mute, flip=flip)])
    if se:
        c["se"] = se
    if bgm:
        c["bgm"] = bgm
    return c


def end_card(dur=4.0, bgm=None):
    """長尺の決まり：最後は subscribe.png。"""
    c = dict(bg=None, end=True, text=None, dur=dur, fixed=True, no_pop=True, cats=[])
    if bgm:
        c["bgm"] = bgm
    return c


class Renderer:
    def __init__(self, c):
        self.c = c
        if c.get("end"):
            im = Image.open(os.path.join(HERE, "parts", "common", "subscribe.png")).convert("RGB").resize((W, H), Image.LANCZOS)
            self.base = np.asarray(im)[:, :, ::-1].astype(np.float32) / 255
        else:
            self.base = cover(c["bg"])
            if c.get("dark"):   # 同じ絵を夜っぽく暗くして使いまわす
                self.base = self.base * (1 - c["dark"]) + np.array([0.25, 0.08, 0.05], np.float32) * c["dark"] * 0.4
        self.sub = sub_img(c["text"]) if c.get("text") else None
        self.clips = [R.Clip(k["a"]) for k in c["cats"]]

    def frame(self, t):
        out = self.base.copy()
        for cl, k in zip(self.clips, self.c["cats"]):
            fr, a = cl.frame(t + 0.25)
            y0, y1, x0, x1 = I.clip_bbox(k["a"])
            fr, a = fr[y0:y1, x0:x1], a[y0:y1, x0:x1]
            if k.get("flip"):
                fr, a = fr[:, ::-1], a[:, ::-1]
            s = min(k["h"] / fr.shape[0], 1100 / fr.shape[1])
            w, h = max(1, int(fr.shape[1] * s)), max(1, int(fr.shape[0] * s))
            img = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
            al = cv2.resize(a.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA)
            xx = min(max(int(k["x"] - w / 2), 0), W - w)
            I.over(out, img, al, xx, int(k["bottom"] - h))
        if self.sub is not None:
            img, a = R.to_np(self.sub)
            I.over(out, img, a, int(W / 2 - self.sub.width / 2), int(1040 - self.sub.height))
        return out

    def close(self):
        for cl in self.clips:
            if getattr(cl, "cap", None) is not None:
                cl.cap.release()


def run(cs, out_path, prev=None, only=None):
    durs = [c["dur"] for c in cs]
    total = float(sum(durs))
    starts = list(np.cumsum([0] + durs[:-1]))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wav = out_path + ".audio.f32"
    R.build_audio(cs, starts, durs, total).tofile(wav)
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(R.FPS), "-i", "-",
         "-f", "f32le", "-ar", str(R.SR), "-ac", "2", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", out_path],
        stdin=subprocess.PIPE)
    if prev:
        os.makedirs(prev, exist_ok=True)
    nframes = int(round(total * R.FPS))
    fno = 0
    for i, c in enumerate(cs):
        rd = Renderer(c)
        end = min(nframes, int(round((starts[i] + durs[i]) * R.FPS)))
        shot = False
        while fno < end:
            tt = fno / R.FPS - starts[i]
            u8 = (np.clip(rd.frame(tt), 0, 1) * 255).astype(np.uint8)
            proc.stdin.write(u8.tobytes())
            if prev and not shot and tt > 1.0:
                cv2.imwrite(os.path.join(prev, f"{i:03d}.jpg"), cv2.resize(u8, (640, 360)), [cv2.IMWRITE_JPEG_QUALITY, 80])
                shot = True
            fno += 1
        rd.close()
        print(f"\r{i + 1}/{len(cs)}  {fno / R.FPS:6.1f}s / {total:.1f}s", end="", flush=True)
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    print(f"\n-> {out_path} ({total:.1f}s)")
