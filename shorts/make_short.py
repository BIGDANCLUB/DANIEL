#!/usr/bin/env python3
"""縦型ショート（1080x1920）を台本JSONから組み立てる。

参考フォーマット:
  - 画像は全面（帯なし）。1行ごとにカットを切り替え、ゆっくりズーム／パン
  - 字幕は画面中央。白文字＋太い黒縁、キーワードは {黄} <赤>
  - 字幕はフレーズごとにポップイン（拡大＋フェード）
  - 冒頭1行はフック：大きめの黄色文字
  - "banner" があれば画面上部に動画概要の帯を出し続ける
  - 赤字（<…>）は表示直後にもう一度ポンと弾ませる
  - 行に "se": "don" / "coin" があれば、その行の頭に効果音を重ねる
  - BGM は bgm/ の曲からランダムに1曲（台本の "bgm" で指定も可）。声の間は自動で下げる

素材（BGMは後付け前提なので入れない）:
  音声 … 行に "audio":[開始,終了] があれば元動画から切り出し、無ければ Gemini TTS（tts_gemini.py）
  画像 … 行に "shot":{"image":...} があれば共有画像を切り出し、"prompt" があれば Gemini 画像生成
         （gen_images_gemini.py）。足りない音声・画像はレンダリング前に自動で生成する。

usage:
  python3 make_short.py story.json out.mp4                     # TTS＋生成画像の台本
  python3 make_short.py story.json out.mp4 --source src.mp4    # 元動画の声を使う台本
"""
import argparse
import json
import os
import random
import re
import subprocess
import sys
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import gen_images_gemini
import tts_gemini

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
PUNCH = (0.28, 0.30, 0.15)   # 赤字の弾み：開始秒・長さ・最大拡大率
BANNER_H = 330
BANNER_SIZE = 112


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
    # 弾ませる演出用：赤字を除いた下地と、赤字だけのレイヤー（周りの文字や縁を含まない）
    rest = Image.new("RGBA", (iw, ih), (0, 0, 0, 0))
    dr = ImageDraw.Draw(rest)
    reds = []
    for li, l in enumerate(lines):
        x = (iw - widths[li]) / 2
        y = sw + li * lh
        for seg, col in parse_runs(l, base):
            d.text((x, y), seg, font=f, fill=col, stroke_width=sw, stroke_fill="#000000")
            if col == COLORS["<"]:
                layer = Image.new("RGBA", (iw, ih), (0, 0, 0, 0))
                ImageDraw.Draw(layer).text((x, y), seg, font=f, fill=col, stroke_width=sw, stroke_fill="#000000")
                box = layer.getbbox()
                reds.append((layer.crop(box), box))
            else:
                dr.text((x, y), seg, font=f, fill=col, stroke_width=sw, stroke_fill="#000000")
            x += f.getlength(seg)
    img.info["red"] = reds
    img.info["rest"] = rest
    return img


def punch(sub, dt):
    """表示から dt 秒の字幕に、赤字だけ一瞬拡大したものを重ねる。"""
    start, dur, amp = PUNCH
    x = (dt - start) / dur
    if not 0 < x < 1 or not sub.info.get("red"):
        return sub
    sc = 1 + amp * np.sin(np.pi * x)
    pad = int(max(p.height for p, _ in sub.info["red"]) * amp) + 4
    canvas = Image.new("RGBA", (sub.width + 2 * pad, sub.height + 2 * pad), (0, 0, 0, 0))
    # 赤字を先に置き、残りの文字を上に重ねる（拡大した赤字が隣の字を隠さないように）
    for part, (x0, y0, x1, y1) in sub.info["red"]:
        part = part.resize((int(part.width * sc), int(part.height * sc)), Image.BICUBIC)
        cx, cy = (x0 + x1) / 2 + pad, (y0 + y1) / 2 + pad
        canvas.alpha_composite(part, (int(cx - part.width / 2), int(cy - part.height / 2)))
    canvas.alpha_composite(sub.info["rest"], (pad, pad))
    return canvas


def make_banner(text):
    """画面上部の概要帯（黒地に白・黄の2行）。"""
    band = Image.new("RGBA", (W, BANNER_H), (8, 8, 8, 255))
    t = rich_text(text, BANNER_SIZE, W - 60, stroke_ratio=0.06, line_gap=0.0)
    band.alpha_composite(t, ((W - t.width) // 2, BANNER_H - t.height - 18))
    return band


def sound_effect(kind):
    """効果音を合成して返す（素材ファイル不要）。don: 重い一打 / coin: チャリン。"""
    if kind == "don":
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        f = 48 + 60 * np.exp(-t * 18)                     # 下がっていく低音
        body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
        click = np.random.default_rng(0).standard_normal(n) * np.exp(-t * 90) * 0.35
        se = body + click
        return (se / np.abs(se).max() * 0.6).astype(np.float32)
    if kind == "coin":
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        out = np.zeros(n, np.float32)
        for delay in (0.0, 0.09):
            tt = np.clip(t - delay, 0, None)
            on = (t >= delay)
            for fr, g in ((2637, 0.5), (3951, 0.35), (5274, 0.2)):
                out += on * g * np.sin(2 * np.pi * fr * tt) * np.exp(-tt * 7)
        return (out / np.abs(out).max() * 0.4).astype(np.float32)
    sys.exit(f"未知の効果音: {kind}（don / coin）")


BGM_DIR = os.path.join(HERE, "bgm")
BGM_EXT = (".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac")


def pick_bgm(cfg, work):
    """使う BGM のパスを返す。
    "bgm" 省略 or "random" … bgm/ 直下とサブフォルダ全部からランダム
    "random:スカッと"      … bgm/スカッと/ の中からランダム
    "曲名.mp3"             … bgm/ からの相対パスで指定
    "none"                 … BGM なし
    ランダムで選んだ曲は work に記録し、作り直しても同じ曲を使う。"""
    spec = cfg.get("bgm", "random")
    if not spec or spec == "none":
        return None
    if not spec.startswith("random"):
        path = os.path.join(BGM_DIR, spec)
        if not os.path.exists(path):
            sys.exit(f"BGM が見つかりません: {path}")
        return path
    memo = os.path.join(work, "bgm_choice.txt")
    if os.path.exists(memo):
        prev = open(memo, encoding="utf-8").read().strip()
        if os.path.exists(os.path.join(BGM_DIR, prev)) and prev.startswith(spec[7:]):
            return os.path.join(BGM_DIR, prev)
    root = os.path.join(BGM_DIR, spec[7:]) if spec.startswith("random:") else BGM_DIR
    songs = sorted(os.path.relpath(os.path.join(d, f), BGM_DIR)
                   for d, _, fs in os.walk(root) for f in fs if f.lower().endswith(BGM_EXT))
    if not songs:
        print(f"  ※ {root} に BGM が無いので BGM なしで書き出します")
        return None
    choice = random.choice(songs)
    open(memo, "w", encoding="utf-8").write(choice)
    return os.path.join(BGM_DIR, choice)


def mix_bgm(wav, bgm, total, volume_db):
    """ナレーション（効果音込み）に BGM を重ねて上書きする。
    曲は音量をそろえてから volume_db 下げ、声が出ている間はさらに自動で下げる（ダッキング）。
    曲が短ければ繰り返し、最後はフェードアウト。"""
    tmp = wav + ".bgm.wav"
    fade = min(2.0, total / 4)
    graph = (f"[1:a]aformat=sample_rates={SR}:channel_layouts=mono,loudnorm=I=-16:TP=-2,"
             f"volume={volume_db}dB,atrim=0:{total:.3f},afade=t=in:d=0.8,"
             f"afade=t=out:st={total - fade:.3f}:d={fade:.3f}[b];"
             "[0:a]asplit[v][key];"
             "[b][key]sidechaincompress=threshold=0.03:ratio=2.5:attack=30:release=500[bd];"
             "[v][bd]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.9[out]")
    subprocess.run([FF, "-loglevel", "error", "-y", "-i", wav, "-stream_loop", "-1", "-i", bgm,
                    "-filter_complex", graph, "-map", "[out]", "-ar", str(SR), "-ac", "1", tmp], check=True)
    os.replace(tmp, wav)


def mix_effects(wav, cfg, timings):
    """ナレーションWAVに行ごとの効果音を重ねて上書きする。"""
    marks = [(timings[i][0] if i else 0.0, l["se"]) for i, l in enumerate(cfg["lines"]) if l.get("se")]
    if not marks:
        return
    a = load_audio(wav).copy()
    for at, kind in marks:
        se = sound_effect(kind)
        s = int(at * SR)
        e = min(len(a), s + len(se))
        a[s:e] += se[:e - s]
    np.clip(a, -1, 1).astype(np.float32).tofile(wav + ".f32")
    subprocess.run([FF, "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1",
                    "-i", wav + ".f32", wav], check=True)
    os.remove(wav + ".f32")


def load_audio(src):
    raw = subprocess.run(
        [FF, "-loglevel", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def trim_silence(a, db=-45, pad=0.04):
    win = int(0.01 * SR)
    n = len(a) // win
    if n == 0:
        return a
    rms = np.sqrt((a[:n * win].reshape(n, win) ** 2).mean(1) + 1e-12)
    loud = np.where(20 * np.log10(rms) > db)[0]
    if len(loud) == 0:
        return a
    s = max(0, loud[0] * win - int(pad * SR))
    e = min(len(a), (loud[-1] + 1) * win + int(pad * SR))
    return a[s:e]


def shorten_pauses(a, max_pause, db=-35):
    """行の途中の間が max_pause 秒より長ければ、その長さまで詰める（抑揚は残して間延びだけ削る）。"""
    win = int(0.01 * SR)
    n = len(a) // win
    if n == 0 or not max_pause:
        return a
    quiet = 20 * np.log10(np.sqrt((a[:n * win].reshape(n, win) ** 2).mean(1)) + 1e-9) < db
    keep = np.ones(len(a), bool)
    fade = int(0.01 * SR)
    i = 0
    while i < n:
        if not quiet[i]:
            i += 1
            continue
        j = i
        while j < n and quiet[j]:
            j += 1
        if (j - i) * 0.01 > max_pause and i > 0 and j < n:
            half = int(max_pause * SR / 2)
            keep[i * win + half:j * win - half] = False
        i = j
    out = a[keep]
    # 詰めた継ぎ目は無音部分なのでクリックは出ないが、念のため最初と最後を軽くフェード
    out[:fade] *= np.linspace(0, 1, min(fade, len(out)), dtype=np.float32)
    return out


def line_clips(cfg, base, source):
    """各行の音声（元動画の切り出し、または TTS の WAV）を返す。"""
    src_audio = None
    clips = []
    for i, line in enumerate(cfg["lines"]):
        if "audio" in line:
            if src_audio is None:
                if not source:
                    sys.exit("audio 区間を使う行があるので --source で元動画を指定してください")
                src_audio = load_audio(source)
            a, b = max(0.0, line["audio"][0]), line["audio"][1]
            clips.append(src_audio[int(a * SR):int(b * SR)].copy())
        else:
            clip = trim_silence(load_audio(tts_gemini.wav_path(cfg, base, i)).copy())
            clips.append(shorten_pauses(clip, cfg.get("max_pause", 0.3)))
    return clips


def build_audio(cfg, clips):
    """行ごとの音声を並べ、各行の開始・終了（出力時間軸）を返す。"""
    tempo = cfg.get("tempo", 1.0)
    parts = [np.zeros(int(cfg.get("lead_in", 0.05) * tempo * SR), np.float32)]
    t = cfg.get("lead_in", 0.05) * tempo
    timings = []
    fade = int(0.012 * SR)
    ramp = np.linspace(0, 1, fade, dtype=np.float32)
    for i, seg in enumerate(clips):
        if i:
            parts.append(np.zeros(int(cfg.get("gap", 0.15) * SR), np.float32))
            t += cfg.get("gap", 0.15)
        seg[:fade] *= ramp
        seg[-fade:] *= ramp[::-1]
        parts.append(seg)
        timings.append((t / tempo, (t + len(seg) / SR) / tempo))
        t += len(seg) / SR
    parts.append(np.zeros(int(cfg.get("tail", 1.3) * tempo * SR), np.float32))
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


AUTO_MOVES = ["in", "left", "out", "right", "in", "up", "out", "down"]


def make_shots(cfg, base):
    """行ごとのカット。shot 指定があれば共有画像の切り出し、prompt 行は生成画像を全面で。"""
    cache = {}

    def load(path):
        if path not in cache:
            cache[path] = Image.open(path).convert("RGB")
        return cache[path]

    shots = []
    for i, l in enumerate(cfg["lines"]):
        spec = dict(l.get("shot", {}))
        if "image" in spec:
            img = load(os.path.join(base, cfg["images"][spec["image"]]))
        elif "scene" in l:
            # 場面画像の一部を切り出す。crop = [中心x, 中心y, 拡大率]（x,y は 0〜1、拡大率1で全体）
            img = load(gen_images_gemini.scene_path(cfg, base, l["scene"]))
            cx, cy, zoom = l.get("crop", [0.5, 0.5, 1.0])
            w = img.width / zoom
            h = w * H / W
            spec.setdefault("box", [cx * img.width - w / 2, cy * img.height - h / 2, w])
        else:
            img = load(gen_images_gemini.image_path(cfg, base, i))
        spec.setdefault("box", [0, 0, img.width])
        spec.setdefault("move", l.get("move", AUTO_MOVES[i % len(AUTO_MOVES)]))
        shots.append(Shot(img, spec))
    return shots


def main(story_path, out, source=None):
    cfg = json.load(open(story_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(story_path))
    work = os.path.splitext(out)[0] + "_work"
    os.makedirs(work, exist_ok=True)

    # --- 素材の自動生成（足りないものだけ） ---
    tts_gemini.ensure_voice(story_path)
    gen_images_gemini.ensure_images(story_path)

    # --- 音声 ---
    tempo = cfg.get("tempo", 1.0)
    audio, timings = build_audio(cfg, line_clips(cfg, base, source))
    raw_wav = os.path.join(work, "narration_raw.f32")
    audio.astype(np.float32).tofile(raw_wav)
    wav = os.path.splitext(out)[0] + "_narration.wav"
    subprocess.run([FF, "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw_wav,
                    "-af", f"atempo={tempo},loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), wav], check=True)
    mix_effects(wav, cfg, timings)
    total = len(audio) / SR / tempo
    bgm = pick_bgm(cfg, work)
    if bgm:
        print(f"  BGM: {os.path.relpath(bgm, BGM_DIR)}")
        mix_bgm(wav, bgm, total, cfg.get("bgm_volume", -10))
    nframes = int(total * FPS)

    # --- カット ---
    shots = make_shots(cfg, base)
    cut_at = [0.0] + [st for st, _ in timings[1:]] + [total]

    # --- 字幕 ---
    subs = []
    for i, l in enumerate(cfg["lines"]):
        if l.get("hook"):
            subs.append(rich_text(l["text"], HOOK_SIZE, SUB_MAX_W, base="#ffe600", line_gap=0.0))
        else:
            subs.append(rich_text(l["text"], SUB_SIZE, SUB_MAX_W))
    banner = make_banner(cfg["banner"]) if cfg.get("banner") else None
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
            # 1行目はフィードで最初に目に入るので、0フレーム目から文字を見せる（拡大だけで弾ませる）
            sc = (0.8 + 0.2 * ease_back(a)) if li == 0 else (0.55 + 0.45 * ease_back(a))
            sub = sub.resize((max(1, int(sub.width * sc)), max(1, int(sub.height * sc))), Image.BILINEAR)
            alpha = 1.0 if li == 0 else ease_out(a * 1.6)
            sub.putalpha(sub.getchannel("A").point(lambda v: int(v * alpha)))
        else:
            sub = punch(sub, t - st)
        frame.alpha_composite(sub, ((W - sub.width) // 2, SUB_CY - sub.height // 2))
        if banner:
            frame.alpha_composite(banner, (0, 0))
        if note:
            frame.alpha_composite(note, (24, BANNER_H + 20 if banner else 150))

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
    if not 45 <= total <= 55:
        print(f"  ※ 45〜55秒から外れています。台本の tempo を {tempo * total / 52:.2f} 付近にすると約52秒になります")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("story")
    ap.add_argument("out")
    ap.add_argument("--source", help="audio 区間を使う行がある場合の元動画")
    args = ap.parse_args()
    main(args.story, args.out, args.source)
