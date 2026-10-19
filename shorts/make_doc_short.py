#!/usr/bin/env python3
"""ドキュメンタリー風ショート（参考動画の作りに合わせた形式）を台本JSONから作る。

参考動画の作り:
  - 上部の帯なし。1文ごとに全面の写真を出し、ゆっくりズームイン（切り替えはカット）
  - 字幕は画面中央に短いフレーズ（1〜2行）を、読み上げに合わせて次々に表示。白字＋黒縁＋影、
    強調は {黄} <赤>。表示の瞬間に小さくポップ
  - 冒頭は数行のフック文をまとめて表示
  - 男性ナレーション（〜のである調）、重めのBGM

このチャンネルのルール:
  - 尺はぴったり 60.00 秒（59.99〜60.00）。原稿の量と、読み終わり後の空白で合わせる
    （読み上げが入りきらないときはエラーで止まり、削る秒数を表示する）
  - 参考動画の最後のエンディング（ご視聴ありがとうございます等）は使わない
  - 冒頭に se/チリン.mp3
  - 渡された画像・動画（scenes の "file"）は1本で2回まで。足りない分は Gemini で生成

台本（story_docXXX.json）:
  lines[]: {"say": 読み上げ, "tone": 気持ち, "subs": [フレーズ, ...], "scene": 場面名}
           1行目の subs はフック文（"\\n" で改行した1つのブロック）
  scenes:  {"名前": {"prompt": "..."}}（Gemini 生成）または {"名前": {"file": "渡された画像のパス"}}
  tts:     声の設定（tts_gemini と同じ。後で VOICEVOX に差し替えられるよう分けてある）
  bgm:     bgm/ からの相対パス

usage: python3 make_doc_short.py story_doc001.json out/DOC-001.mp4
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import gen_images_gemini
import tts_gemini
from make_short import FF, SR, load_audio, shorten_pauses, trim_silence

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
SANS = os.path.join(HERE, "fonts", "NotoSansJP[wght].ttf")
SERIF = os.path.join(HERE, "fonts", "NotoSerifJP[wght].ttf")
YELLOW, RED = "#ffff00", "#ff0000"   # チャンネルのルールで固定
SUB_SIZE = 102         # 参考動画の文字枠（576px幅で7文字382×64px）に合わせて実測で校正
SUB_CY = 0.50          # 字幕の中心（画面の高さに対する割合）
SUB_MAX_W = 1050
ZOOM = 0.14            # 1カットの間にズームインする量
# 字幕の出方（参考動画を30fpsで実測）: 小さく半透明で出て 0.13 秒で 104% まで拡大、
# 0.27 秒まで保ってから 0.37 秒で 100% に戻る
POP_CURVE = [(0.0, 0.48), (0.033, 0.78), (0.067, 0.93), (0.13, 1.045), (0.27, 1.045), (0.37, 1.0)]


def pop_scale(dt):
    pts = POP_CURVE
    if dt >= pts[-1][0]:
        return 1.0
    for (t0, s0), (t1, s1) in zip(pts, pts[1:]):
        if t0 <= dt < t1:
            return s0 + (s1 - s0) * (dt - t0) / (t1 - t0)
    return 1.0


def pop_alpha(dt):
    return min(1.0, 0.5 + dt / 0.07 * 0.5)
DURATION = 60.0        # 尺（秒）
INTRO_SE = os.path.join(HERE, "se", "チリン.mp3")
MAX_FILE_USES = 2      # 渡された素材は1本で2回まで


FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/"


def font(path, size, weight):
    if not os.path.exists(path):   # fonts/ は git 管理外なので、無ければ Google Fonts から取る
        os.makedirs(os.path.dirname(path), exist_ok=True)
        name = os.path.basename(path)
        folder = "notoserifjp" if "Serif" in name else "notosansjp"
        urllib.request.urlretrieve(FONT_URL + folder + "/" + name.replace("[", "%5B").replace("]", "%5D"), path)
    f = ImageFont.truetype(path, size)
    f.set_variation_by_name(weight)
    return f


def runs(text):
    out, i = [], 0
    for m in re.finditer(r"\{[^}]*\}|<[^>]*>", text):
        if m.start() > i:
            out.append((text[i:m.start()], "#ffffff"))
        out.append((m.group()[1:-1], YELLOW if m.group()[0] == "{" else RED))
        i = m.end()
    if i < len(text):
        out.append((text[i:], "#ffffff"))
    return out


def plain(t):
    return re.sub(r"[{}<>]", "", t)


def caption(text, size=SUB_SIZE):
    """白字・黒縁・うっすら影のテロップ（複数行、{黄}<赤>）。"""
    lines = text.split("\n")
    while True:
        f = font(SANS, size, "Black")
        sw = max(3, int(size * 0.11))      # 黒縁は参考動画と同じ太さ（1080px幅で約11px）
        widths = [f.getlength(plain(l)) for l in lines]
        if max(widths) + 2 * sw <= SUB_MAX_W or size < 36:
            break
        size -= 2
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * 1.0)
    pad = sw + 10
    iw, ih = int(max(widths)) + 2 * pad, lh * len(lines) + 2 * pad
    txt = Image.new("RGBA", (iw, ih), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    for li, l in enumerate(lines):
        x = (iw - widths[li]) / 2
        y = pad + li * lh
        for seg, col in runs(l):
            d.text((x, y), seg, font=f, fill=col, stroke_width=sw, stroke_fill="#000000")
            x += f.getlength(seg)
    shadow = Image.new("RGBA", (iw, ih), (0, 0, 0, 0))
    shadow.putalpha(txt.getchannel("A").filter(ImageFilter.GaussianBlur(6)).point(lambda v: v * 0.55))
    out = Image.new("RGBA", (iw + 6, ih + 6), (0, 0, 0, 0))
    out.alpha_composite(shadow, (6, 6))
    out.alpha_composite(txt, (0, 0))
    return out


def mora(text):
    """読み上げの長さの目安（かな1字=1、漢字≈1.8、数字は読みの長さ）。字幕の切り替えに使う。"""
    t = plain(text).replace("\n", "")
    n = 0.0
    for m in re.finditer(r"\d+|.", t):
        g = m.group()
        if g.isdigit():
            n += 2.2 * len(g) + (1 if len(g) >= 4 else 0)   # 2016 → にせんじゅうろく
        elif re.match(r"[\u4e00-\u9fff々]", g):
            n += 1.8
        elif re.match(r"[ぁ-んァ-ンー]", g):
            n += 0.0 if g in "ゃゅょャュョァィゥェォ" else 1.0
        elif g in "、。，．！？「」『』（）・ 　":
            n += 0.0
        else:
            n += 1.0
    return max(n, 0.5)


def pauses(a, min_len=0.08, db_th=-38):
    """音声の中の間（秒）を [(中心, 長さ)] で返す。"""
    win = int(0.01 * SR)
    n = len(a) // win
    if n == 0:
        return []
    db = 20 * np.log10(np.sqrt((a[:n * win].reshape(n, win) ** 2).mean(1)) + 1e-9)
    q, out, i = db < db_th, [], 0
    while i < n:
        if q[i]:
            j = i
            while j < n and q[j]:
                j += 1
            if j - i >= min_len * 100 and i > 0 and j < n:
                out.append(((i + j) / 200, (j - i) / 100))
            i = j
        else:
            i += 1
    return out


def phrase_bounds(clip, phrases):
    """文の中のフレーズの切り替え時刻（文頭からの秒）。読みの長さで見積もり、近くの間に合わせる。"""
    total = len(clip) / SR
    w = np.array([mora(p) for p in phrases])
    est = np.cumsum(w)[:-1] / w.sum() * total
    gaps = pauses(clip)
    out, last = [], 0.0
    for e in est:
        cand = [g for g, L in gaps if last + 0.25 < g < total - 0.2 and abs(g - e) < 0.8]
        b = min(cand, key=lambda g: abs(g - e)) if cand else max(e, last + 0.3)
        out.append(b)
        last = b
    return out


VIDEO_EXT = (".mp4", ".mov", ".webm", ".m4v")


class VideoBG:
    """動く背景。縦画面いっぱいに切り抜き、30fps で順に読む（短ければくり返す）。"""
    def __init__(self, path, ss=0.0):
        self.path, self.ss, self.proc = path, ss, None

    def start(self):
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}"
        self.proc = subprocess.Popen([FF, "-loglevel", "error", "-stream_loop", "-1", "-ss", f"{self.ss}",
                                      "-i", self.path, "-vf", vf, "-an", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                     stdout=subprocess.PIPE)

    def frame(self):
        if self.proc is None:
            self.start()
        buf = self.proc.stdout.read(W * H * 3)
        return Image.frombytes("RGB", (W, H), buf)

    def stop(self):
        if self.proc:
            self.proc.kill()
            self.proc = None


def cover(img):
    """画像を 9:16 に切り抜いて、ズーム用に少し大きめ（1.0倍=画面ぴったり）で返す。"""
    iw, ih = img.size
    if iw / ih > W / H:
        nw = int(ih * W / H)
        img = img.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
    else:
        nh = int(iw * H / W)
        img = img.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
    return img.convert("RGB").resize((int(W * (1 + ZOOM)), int(H * (1 + ZOOM))), Image.LANCZOS)


def zoom_frame(big, p):
    """p=0..1 でゆっくりズームイン（中央基準）。"""
    s = 1 + ZOOM - ZOOM * (1 - p)          # 表示する範囲の倍率（1+ZOOM の画像から切り出す）
    w, h = big.width / s, big.height / s
    x, y = (big.width - w) / 2, (big.height - h) / 2
    return big.transform((W, H), Image.EXTENT, (x, y, x + w, y + h), Image.BILINEAR)


# --- 声 ---
def voice_clips(story_path, cfg, key, lines, work):
    """tts_gemini で声を作り（足りない分だけ）、行ごとの音声を返す。"""
    tts = dict(cfg[key])
    base = os.path.dirname(os.path.abspath(story_path))
    if tts.get("engine") == "voicevox_files":
        # VOICEVOX アプリの「音声を全て書き出し」で出したファイル（001_…wav, 002_…wav …）を行の順に使う
        d = os.path.join(base, tts["dir"])
        files = sorted(f for f in os.listdir(d) if f.lower().endswith(".wav"))
        if len(files) != len(lines):
            sys.exit(f"{d} の wav が {len(files)} 個です（台本は {len(lines)} 行）。VOICEVOX で1行ずつ書き出してください")
        return [shorten_pauses(trim_silence(load_audio(os.path.join(d, f)).copy()), cfg.get("max_pause", 0.25))
                for f in files]
    tts["voice_dir"] = os.path.join(base, tts["voice_dir"])
    sub = {"tts": tts, "lines": [{"text": l["say"], "say": l["say"], "tone": l.get("tone")} for l in lines]}
    p = os.path.join(work, f"_{key}.json")
    json.dump(sub, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    tts_gemini.ensure_voice(p)
    clips = []
    for i in range(len(lines)):
        a = trim_silence(load_audio(tts_gemini.wav_path(sub, work, i)).copy())
        clips.append(shorten_pauses(a, cfg.get("max_pause", 0.25)))
    return clips


def atempo(a, tempo, work, name):
    if abs(tempo - 1) < 1e-3:
        return a
    raw = os.path.join(work, name + ".f32")
    a.astype(np.float32).tofile(raw)
    out = subprocess.run([FF, "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw,
                          "-af", f"atempo={tempo}", "-f", "f32le", "-"], check=True, capture_output=True).stdout
    return np.frombuffer(out, np.float32).copy()


def bgm_track(path, n, volume_db):
    b = load_audio(path)
    reps = int(np.ceil(n / len(b)))
    b = np.tile(b, reps)[:n]
    rms = np.sqrt((b ** 2).mean() + 1e-12)
    return b / rms * 10 ** ((-16 + volume_db) / 20) * 0.9


def main(story_path, out):
    cfg = json.load(open(story_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(story_path))
    work = os.path.splitext(out)[0] + "_work"
    os.makedirs(work, exist_ok=True)
    lines = cfg["lines"]
    duration = cfg.get("duration", DURATION)

    # 素材（画像）: 渡された素材は2回まで、それ以外は Gemini で生成
    scenes = cfg["scenes"]
    for name, sc in scenes.items():
        if "file" in sc:
            uses = sum(1 for l in lines if l["scene"] == name)
            if uses > MAX_FILE_USES:
                sys.exit(f"渡された素材 {name} を {uses} 回使っています（1本で{MAX_FILE_USES}回まで）")
    gen_images_gemini.ensure_images(story_path)

    def img(name):
        sc = scenes[name]
        if "file" in sc:
            return Image.open(os.path.join(base, sc["file"]))
        return Image.open(gen_images_gemini.scene_path(cfg, base, name))

    # 声
    tempo = cfg.get("tempo", 1.0)
    clips = [atempo(c, tempo, work, f"m{i}") for i, c in enumerate(voice_clips(story_path, cfg, "tts", lines, work))]
    gap = int(cfg.get("gap", 0.12) * SR)
    lead = int(cfg.get("lead_in", 0.45) * SR)          # チリンの後に読み始める
    parts, timings, t = [np.zeros(lead, np.float32)], [], lead
    for i, c in enumerate(clips):
        timings.append((t / SR, (t + len(c)) / SR))
        parts.append(c)
        t += len(c)
        if i + 1 < len(clips):
            parts.append(np.zeros(gap, np.float32))
            t += gap
    n = int(round(duration * SR))
    end_voice = t / SR
    if t > n - int(0.3 * SR):
        sys.exit(f"読み上げが {end_voice:.2f} 秒で {duration} 秒に収まりません。"
                 f"原稿を約 {end_voice - duration + 0.3:.1f} 秒分削るか tempo を上げてください")
    parts.append(np.zeros(n - t, np.float32))          # 読み終わり後の空白で尺を合わせる
    voice = np.concatenate(parts)[:n]
    voice = voice / (np.abs(voice).max() + 1e-9) * 0.89
    print(f"  読み終わり {end_voice:.2f}s → 空白 {duration - end_voice:.2f}s")

    # 冒頭のチリン
    se = load_audio(INTRO_SE) * 10 ** (cfg.get("intro_se_volume", -3) / 20)
    voice[:len(se)] += se[:n]

    # BGM（声の間は下げる簡易ダッキング）。最後はフェードアウト
    env = np.convolve(np.abs(voice), np.ones(int(0.3 * SR)) / (0.3 * SR), "same")
    duck = np.where(env > 0.02, 10 ** (-4 / 20), 1.0)
    duck = np.convolve(duck, np.ones(int(0.2 * SR)) / (0.2 * SR), "same")
    b = bgm_track(os.path.join(HERE, "bgm", cfg["bgm"]), n, cfg.get("bgm_volume", -11))
    b[:int(0.6 * SR)] *= np.linspace(0, 1, int(0.6 * SR))
    fo = int(min(2.5, duration - end_voice + 1.0) * SR)
    b[-fo:] *= np.linspace(1, 0, fo)
    mix = np.clip(voice + b * duck, -0.98, 0.98).astype(np.float32)
    wav = os.path.splitext(out)[0] + "_audio.wav"
    mix.tofile(wav + ".f32")
    subprocess.run([FF, "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", wav + ".f32",
                    "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", str(SR), "-t", f"{duration:.3f}", wav], check=True)
    os.remove(wav + ".f32")

    # 字幕: 各文の中でフレーズを文字数の比で割り当てる。最後のフレーズは動画の終わりまで残す
    subs = []
    for li, (l, (s, e)) in enumerate(zip(lines, timings)):
        phrases = l["subs"]
        nxt = timings[li + 1][0] if li + 1 < len(timings) else duration
        if li == 0:   # フックはまとめて1ブロック
            subs.append((0.0, nxt, caption(phrases[0])))
            continue
        cuts = [s] + [s + x for x in phrase_bounds(clips[li], phrases)] + [nxt]
        for k, p in enumerate(phrases):
            subs.append((cuts[k], cuts[k + 1], caption(p)))

    # カット: 文ごとに場面。同じ場面が続く文は1カットにまとめる
    shots = []
    for li, (l, (s, e)) in enumerate(zip(lines, timings)):
        st = 0.0 if li == 0 else s
        if not (shots and shots[-1][2] == l["scene"]):
            shots.append([st, None, l["scene"]])
    for i in range(len(shots)):
        shots[i][1] = shots[i + 1][0] if i + 1 < len(shots) else duration
    def is_video(sc):
        return scenes[sc].get("file", "").lower().endswith(VIDEO_EXT)
    bigs = {sc: (VideoBG(os.path.join(base, scenes[sc]["file"]), scenes[sc].get("ss", 0)) if is_video(sc)
                 else cover(img(sc))) for _, _, sc in shots}
    current = None

    # --- 書き出し（ちょうど duration 秒） ---
    nframes = int(round(duration * FPS))
    proc = subprocess.Popen([FF, "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
                             "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                             "-c:a", "aac", "-b:a", "192k", "-t", f"{duration:.3f}", "-movflags", "+faststart", out],
                            stdin=subprocess.PIPE)
    for fi in range(nframes):
        tt = fi / FPS
        sh = next(x for x in shots if x[0] <= tt < x[1] or x is shots[-1])
        p = (tt - sh[0]) / max(0.1, sh[1] - sh[0])
        bg = bigs[sh[2]]
        if current is not sh:
            for other in bigs.values():
                if isinstance(other, VideoBG) and other is not bg:
                    other.stop()
            current = sh
        if isinstance(bg, VideoBG):
            frame = bg.frame().convert("RGBA")       # 動画はそのまま流す（ズームなし）
        else:
            frame = zoom_frame(bg, min(1, p)).convert("RGBA")
        cur = [x for x in subs if x[0] <= tt < x[1]]
        if cur:
            a, _, cap = cur[-1]
            dt = tt - a
            sc, al = pop_scale(dt), pop_alpha(dt)
            c = cap if sc == 1.0 else cap.resize((max(1, int(cap.width * sc)), max(1, int(cap.height * sc))), Image.BICUBIC)
            if al < 1:
                c = c.copy()
                c.putalpha(c.getchannel("A").point(lambda v: int(v * al)))
            frame.alpha_composite(c, ((W - c.width) // 2, int(H * SUB_CY) - c.height // 2))
        proc.stdin.write(frame.convert("RGB").tobytes())
        if fi % 300 == 0:
            print(f"frame {fi}/{nframes}", flush=True)
    proc.stdin.close()
    proc.wait()

    def ts(x):
        return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x * 1000 % 1000):03d}"
    with open(os.path.splitext(out)[0] + ".srt", "w", encoding="utf-8") as fh:
        for i, (l, (s, e)) in enumerate(zip(lines, timings)):
            fh.write(f"{i + 1}\n{ts(s)} --> {ts(e)}\n{l['say']}\n\n")
    print(f"done: {out} ({duration:.2f}s)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
