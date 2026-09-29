#!/usr/bin/env python3
"""縦型ショート（1080x1920）を台本JSONから組み立てる。

レイアウト:
  上段  … フック用タイトル（3行・強調色つき）
  中段  … シーン画像（ゆっくりズーム＋クロスフェード）、章チップ、残高バッジ
  字幕  … 画像下部に大きな縁取り字幕。{黄} <赤> [緑] で強調
  背景  … シーン画像のぼかし

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
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
FONTS = {
    "heavy": ("DelaGothicOne-Regular.ttf", "ofl/delagothicone/DelaGothicOne-Regular.ttf"),
    "sans": ("NotoSansJP[wght].ttf", "ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf"),
}
COLORS = {"{": "#ffe14d", "<": "#ff5a5a", "[": "#5fe08a"}
CLOSE = {"{": "}", "<": ">", "[": "]"}

IMG_Y, IMG_H = 600, 860          # シーン画像の表示位置
SUB_CY = 1300                    # 字幕の中心Y
FADE = 0.4                       # シーン切り替えのクロスフェード秒


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
    if kind == "sans":
        f.set_variation_by_name("Black")
    return f


def parse_runs(text):
    """'月に{11万円}だけ' -> [('月に', white), ('11万円', yellow), ('だけ', white)]"""
    runs, i = [], 0
    for m in re.finditer(r"\{[^}]*\}|<[^>]*>|\[[^\]]*\]", text):
        if m.start() > i:
            runs.append((text[i:m.start()], "#ffffff"))
        runs.append((m.group()[1:-1], COLORS[m.group()[0]]))
        i = m.end()
    if i < len(text):
        runs.append((text[i:], "#ffffff"))
    return runs


def plain(text):
    return re.sub(r"[{}<>\[\]]", "", text)


def rich_text(text, kind, size, max_w, stroke_ratio=0.13, line_gap=0.18):
    """複数行・色分け・縁取りのテキストをRGBA画像で返す。幅に収まるよう自動縮小。"""
    lines = text.split("\n")
    while True:
        f = font(kind, size)
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
        for seg, col in parse_runs(l):
            d.text((x, y), seg, font=f, fill=col, stroke_width=sw, stroke_fill="#000000")
            x += f.getlength(seg)
    return img


def chip(text, bg, size=40, pad=(22, 10), radius=14, fg="#ffffff"):
    f = font("sans", size)
    tw = f.getlength(text)
    asc, desc = f.getmetrics()
    img = Image.new("RGBA", (int(tw + 2 * pad[0]), asc + desc + 2 * pad[1]), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius, fill=bg)
    d.text((pad[0], pad[1]), text, font=f, fill=fg)
    return img


def grab_frame(src, t):
    raw = subprocess.run(
        [FF, "-loglevel", "error", "-ss", str(t), "-i", src, "-frames:v", "1",
         "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        check=True, capture_output=True).stdout
    return Image.frombytes("RGB", (W, H), raw)


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
            g = cfg["scene_gap"] if line["scene"] != cfg["lines"][i - 1]["scene"] else cfg["gap"]
            parts.append(np.zeros(int(g * SR), np.float32))
            t += g
        a, b = max(0.0, line["audio"][0]), line["audio"][1]
        seg = src_audio[int(a * SR):int(b * SR)].copy()
        seg[:fade] *= ramp
        seg[-fade:] *= ramp[::-1]
        parts.append(seg)
        timings.append((t / tempo, (t + len(seg) / SR) / tempo))
        t += len(seg) / SR
    parts.append(np.zeros(int(cfg["tail"] * tempo * SR), np.float32))
    return np.concatenate(parts), timings


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def main(story_path, src, out):
    cfg = json.load(open(story_path, encoding="utf-8"))
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

    # --- シーン素材 ---
    scenes = []
    for s in cfg["scenes"]:
        fr = grab_frame(src, s["frame_t"])
        x, y, w, h = s["crop"]
        img = fr.crop((x, y, x + w, y + h))
        bg = img.resize((int(H * w / h), H), Image.LANCZOS)
        bg = bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, H))
        bg = bg.filter(ImageFilter.GaussianBlur(28))
        bg = Image.blend(bg, Image.new("RGB", (W, H), "#000000"), 0.62)
        scenes.append({"img": img.resize((int(W * 1.12), int(IMG_H * 1.12)), Image.LANCZOS), "bg": bg,
                       "chapter": chip(s["chapter"], (0, 0, 0, 190), size=38)})
    scene_start = {}
    for (st, _), line in zip(timings, cfg["lines"]):
        scene_start.setdefault(line["scene"], st)
    scene_start[0] = 0.0
    scene_end = {}
    ids = sorted(scene_start)
    for i, sid in enumerate(ids):
        scene_end[sid] = scene_start[ids[i + 1]] if i + 1 < len(ids) else total

    # --- 固定レイヤー（タイトル） ---
    title = Image.new("RGBA", (W, IMG_Y), (0, 0, 0, 0))
    y = 150
    for t in cfg["title"]:
        if t.get("band"):
            txt = rich_text(t["text"], "heavy", t["size"], W - 120, stroke_ratio=0.0)
            band = Image.new("RGBA", (txt.width + 50, txt.height + 18), t["band"])
            band.alpha_composite(txt, (25, 9))
            title.alpha_composite(band, ((W - band.width) // 2, y + 6))
            y += band.height + 14
        else:
            txt = rich_text(t["text"], "heavy", t["size"], W - 80)
            title.alpha_composite(txt, ((W - txt.width) // 2, y))
            y += txt.height - 6
    if cfg.get("disclaimer"):
        f = font("sans", 26)
        ImageDraw.Draw(title).text((W - 30, IMG_Y - 12), cfg["disclaimer"], font=f,
                                   fill=(255, 255, 255, 170), anchor="rb")

    # 画像下部のグラデ（字幕を読みやすく）
    grad = Image.new("RGBA", (W, IMG_H), (0, 0, 0, 0))
    ga = np.zeros((IMG_H, W), np.uint8)
    ramp = np.clip((np.arange(IMG_H) - IMG_H * 0.45) / (IMG_H * 0.55), 0, 1) ** 1.4 * 200
    ga[:] = ramp[:, None].astype(np.uint8)
    grad.putalpha(Image.fromarray(ga))

    subs = [rich_text(l["text"], "heavy", 78, 960) for l in cfg["lines"]]
    badges = []
    cur = None
    for (st, _), l in zip(timings, cfg["lines"]):
        if "badge" in l:
            cur = (st, chip(l["badge"]["text"], l["badge"]["color"], size=40))
        badges.append(cur)
    ctas = [(st, chip(l["cta"], "#ffffff", size=44, fg="#111111")) if l.get("cta") else None
            for (st, _), l in zip(timings, cfg["lines"])]

    def scene_layer(sid, t):
        sc = scenes[sid]
        p = (t - scene_start[sid]) / max(0.1, scene_end[sid] - scene_start[sid])
        z = 1.0 + 0.10 * p                     # ゆっくりズームイン
        big = sc["img"]
        cw, ch = int(W * 1.12 / z), int(IMG_H * 1.12 / z)
        dx = (big.width - cw) * (0.5 + (0.12 if sid % 2 else -0.12) * (p - 0.5))
        dy = (big.height - ch) * 0.5
        crop = big.crop((int(dx), int(dy), int(dx) + cw, int(dy) + ch)).resize((W, IMG_H), Image.BILINEAR)
        frame = sc["bg"].copy()
        frame.paste(crop, (0, IMG_Y))
        return frame

    enc = subprocess.Popen(
        [FF, "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
        stdin=subprocess.PIPE)

    for n in range(nframes):
        t = n / FPS
        sid = max(s for s in ids if scene_start[s] <= t)
        frame = scene_layer(sid, t)
        # 次シーンへのクロスフェード
        nxt = [s for s in ids if 0 <= scene_start[s] - t < FADE and s != sid]
        if nxt:
            k = 1 - (scene_start[nxt[0]] - t) / FADE
            frame = Image.blend(frame, scene_layer(nxt[0], scene_start[nxt[0]]), k)
        frame = frame.convert("RGBA")
        frame.alpha_composite(grad, (0, IMG_Y))
        frame.alpha_composite(title)
        # 章チップ
        frame.alpha_composite(scenes[sid]["chapter"], (28, IMG_Y + 24))

        # 現在の字幕行（次の行が始まるまで表示し続ける）
        li = None
        for i, (st, _) in enumerate(timings):
            if t >= st - 0.05:
                li = i
        if li is not None:
            st = timings[li][0]
            a = ease((t - st + 0.05) / 0.14)
            sub = subs[li]
            sc = 0.86 + 0.14 * a
            s_img = sub.resize((max(1, int(sub.width * sc)), max(1, int(sub.height * sc))), Image.BILINEAR)
            if a < 1:
                s_img.putalpha(s_img.getchannel("A").point(lambda v: int(v * a)))
            frame.alpha_composite(s_img, ((W - s_img.width) // 2, SUB_CY - s_img.height // 2))

            b = badges[li]
            if b:
                ba = ease((t - b[0]) / 0.18)
                bi = b[1]
                bs = 0.7 + 0.3 * ba if ba < 1 else 1 + 0.06 * max(0, 1 - (t - b[0] - 0.18) / 0.25)
                bimg = bi.resize((int(bi.width * bs), int(bi.height * bs)), Image.BILINEAR)
                frame.alpha_composite(bimg, (W - 28 - bimg.width, IMG_Y + 24))
            c = ctas[li]
            if c and t >= c[0] + 0.6:
                ca = ease((t - c[0] - 0.6) / 0.25)
                cimg = c[1].copy()
                cimg.putalpha(cimg.getchannel("A").point(lambda v: int(v * ca)))
                frame.alpha_composite(cimg, ((W - cimg.width) // 2, IMG_Y + IMG_H + 40 - int(20 * (1 - ca))))

        enc.stdin.write(frame.convert("RGB").tobytes())
        if n % 150 == 0:
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
