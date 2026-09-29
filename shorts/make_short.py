#!/usr/bin/env python3
"""縦型ショート（1080x1920）を台本JSONから組み立てる。

参考フォーマット:
  - 画像は全面（帯なし）。1行ごとにカットを切り替え、ゆっくりズーム／パン
  - 字幕は画面中央。白文字＋太い黒縁、キーワードは {黄} <赤>
  - 字幕はフレーズごとにポップイン（拡大＋フェード）
  - 冒頭1行はフック：大きめの黄色文字

音声は元動画のナレーションを行ごとに切り出して並べ直す（BGMは後付け前提なので入れない）。

usage: python3 make_short.py story.json source.mp4 out.mp4
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
FONTS = {
    "sans": ("NotoSansJP[wght].ttf", "ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf"),
}
COLORS = {"{": "#ffe600", "<": "#ff2020"}

SUB_CY = 975          # 字幕の中心Y（参考動画はほぼ画面中央）
SUB_SIZE = 96
HOOK_SIZE = 136
SUB_MAX_W = 1040
POP = 0.22            # ポップイン秒


def ffmpeg_bin():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


FF = ffmpeg_bin()


def font(kind, size):
    name, path = FONTS[kind]
    local = os.path.join(FONT_DIR, name)
    if not os.path.exists(local):
        os.makedirs(FONT_DIR, exist_ok=True)
        urllib.request.urlretrieve("https://raw.githubusercontent.com/google/fonts/main/" + path, local)
    f = ImageFont.truetype(local, size)
    f.set_variation_by_name("Black")
    return f


def parse_runs(text, base):
    """'月に{11万円}だけ' -> [('月に', base), ('11万円', yellow), ('だけ', base)]"""
    runs, i = [], 0
    for m in re.finditer(r"\{[^}]*\}|<[^>]*>", text):
        if m.start() > i:
            runs.append((text[i:m.start()], base))
        runs.append((m.group()[1:-1], COLORS[m.group()[0]]))
        i = m.end()
    if i < len(text):
        runs.append((text[i:], base))
    return runs


def plain(text):
    return re.sub(r"[{}<>]", "", text)


def rich_text(text, size, max_w, base="#ffffff", stroke_ratio=0.14, line_gap=0.02):
    """複数行・色分け・黒縁のテキストをRGBA画像で返す。幅に収まるよう自動縮小。"""
    lines = text.split("\n")
    while True:
        f = font("sans", size)
        sw = max(2, int(size * stroke_ratio))
        widths = [f.getlength(plain(l)) for l in lines]
        if max(widths) + 2 * sw <= max_w or size <= 30:
            break
        size -= 2
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * (1 + line_gap))
    iw = int(max(widths)) + 2 * sw + 4
    ih = lh * len(lines) + 2 * sw
    img = Image.new("RGBA", (iw, ih), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for li, l in enumerate(lines):
        x = (iw - widths[li]) / 2
        y = sw + li * lh
        for seg, col in parse_runs(l, base):
            d.text((x, y), seg, font=f, fill=col, stroke_width=sw, stroke_fill="#000000")
            x += f.getlength(seg)
    return img


def load_audio(src):
    raw = subprocess.run(
        [FF, "-loglevel", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def build_audio(cfg, src_audio):
    """行ごとの音声を並べ、各行の開始・終了（出力時間軸）を返す。"""
    tempo = cfg["tempo"]
    parts = [np.zeros(int(cfg["lead_in"] * tempo * SR), np.float32)]
    t = cfg["lead_in"] * tempo
    timings = []
    fade = int(0.012 * SR)
    ramp = np.linspace(0, 1, fade, dtype=np.float32)
    for i, line in enumerate(cfg["lines"]):
        if i:
            parts.append(np.zeros(int(cfg["gap"] * SR), np.float32))
            t += cfg["gap"]
        a, b = max(0.0, line["audio"][0]), line["audio"][1]
        seg = src_audio[int(a * SR):int(b * SR)].copy()
        seg[:fade] *= ramp
        seg[-fade:] *= ramp[::-1]
        parts.append(seg)
        timings.append((t / tempo, (t + len(seg) / SR) / tempo))
        t += len(seg) / SR
    parts.append(np.zeros(int(cfg["tail"] * tempo * SR), np.float32))
    return np.concatenate(parts), timings


def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def ease_back(x, k=1.9):
    x = min(max(x, 0.0), 1.0) - 1
    return 1 + (k + 1) * x ** 3 + k * x ** 2


class Shot:
    """画像の一部（9:16の枠）を、start→end の枠へ補間しながら全面に映す。"""

    def __init__(self, img, spec):
        self.img = img
        self.a = self._box(spec["box"])
        motion = spec.get("move", "in")
        x, y, w, h = self.a
        if motion == "in":
            k = 0.88
            self.b = (x + w * (1 - k) / 2, y + h * (1 - k) / 2, w * k, h * k)
        elif motion == "out":
            self.b, k = self.a, 0.88
            self.a = (x + w * (1 - k) / 2, y + h * (1 - k) / 2, w * k, h * k)
        elif motion in ("left", "right", "up", "down"):
            k = 0.9
            w2, h2 = w * k, h * k
            dx = {"left": (w - w2, 0), "right": (0, w - w2)}.get(motion, ((w - w2) / 2,) * 2)
            dy = {"up": (h - h2, 0), "down": (0, h - h2)}.get(motion, ((h - h2) / 2,) * 2)
            self.a = (x + dx[0], y + dy[0], w2, h2)
            self.b = (x + dx[1], y + dy[1], w2, h2)
        else:
            self.b = self.a

    def _box(self, box):
        x, y, w = box[:3]
        h = w * H / W
        iw, ih = self.img.size
        x = min(max(0, x), iw - w)
        y = min(max(0, y), ih - h)
        return (x, y, w, h)

    def render(self, p):
        p = p * p * (3 - 2 * p) * 0.5 + p * 0.5      # 少しだけイーズ
        x, y, w, h = (a + (b - a) * p for a, b in zip(self.a, self.b))
        return self.img.transform((W, H), Image.EXTENT, (x, y, x + w, y + h), Image.BICUBIC)


def main(story_path, src, out):
    cfg = json.load(open(story_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(story_path))
    work = os.path.splitext(out)[0] + "_work"
    os.makedirs(work, exist_ok=True)

    # --- 音声 ---
    audio, timings = build_audio(cfg, load_audio(src))
    raw_wav = os.path.join(work, "narration_raw.f32")
    audio.astype(np.float32).tofile(raw_wav)
    wav = os.path.splitext(out)[0] + "_narration.wav"
    subprocess.run([FF, "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw_wav,
                    "-af", f"atempo={cfg['tempo']},loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), wav], check=True)
    total = len(audio) / SR / cfg["tempo"]
    nframes = int(total * FPS)

    # --- カット ---
    images = {k: Image.open(os.path.join(base, v)).convert("RGB") for k, v in cfg["images"].items()}
    shots = [Shot(images[l["shot"]["image"]], l["shot"]) for l in cfg["lines"]]
    cut_at = [0.0] + [st for st, _ in timings[1:]] + [total]

    # --- 字幕 ---
    subs = []
    for i, l in enumerate(cfg["lines"]):
        if l.get("hook"):
            subs.append(rich_text(l["text"], HOOK_SIZE, SUB_MAX_W, base="#ffe600", line_gap=0.0))
        else:
            subs.append(rich_text(l["text"], SUB_SIZE, SUB_MAX_W))
    note = None
    if cfg.get("disclaimer"):
        note = rich_text(cfg["disclaimer"], 28, 600, stroke_ratio=0.12)
        note.putalpha(note.getchannel("A").point(lambda v: int(v * 0.75)))

    enc = subprocess.Popen(
        [FF, "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
        stdin=subprocess.PIPE)

    for n in range(nframes):
        t = n / FPS
        li = max(i for i in range(len(shots)) if cut_at[i] <= t)
        p = (t - cut_at[li]) / (cut_at[li + 1] - cut_at[li])
        frame = shots[li].render(min(1.0, p)).convert("RGBA")

        st = timings[li][0] if li else 0.0
        a = (t - st) / POP
        sub = subs[li]
        if a < 1:
            sc = 0.55 + 0.45 * ease_back(a)
            sub = sub.resize((max(1, int(sub.width * sc)), max(1, int(sub.height * sc))), Image.BILINEAR)
            alpha = ease_out(a * 1.6)
            sub.putalpha(sub.getchannel("A").point(lambda v: int(v * alpha)))
        frame.alpha_composite(sub, ((W - sub.width) // 2, SUB_CY - sub.height // 2))
        if note:
            frame.alpha_composite(note, (24, 150))

        enc.stdin.write(frame.convert("RGB").tobytes())
        if n % 300 == 0:
            print(f"frame {n}/{nframes}", flush=True)
    enc.stdin.close()
    enc.wait()

    # 字幕ファイル（編集ソフト用）
    def ts(x):
        return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x * 1000 % 1000):03d}"
    with open(os.path.splitext(out)[0] + ".srt", "w", encoding="utf-8") as fp:
        for i, ((st, en), l) in enumerate(zip(timings, cfg["lines"])):
            fp.write(f"{i + 1}\n{ts(st)} --> {ts(en)}\n{plain(l['text'])}\n\n")
    print(f"done: {out} ({total:.2f}s)")


if __name__ == "__main__":
    main(*sys.argv[1:4])
