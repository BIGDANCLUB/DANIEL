#!/usr/bin/env python3
"""ドキュメンタリー風ショート（参考動画の作りに合わせた形式）を台本JSONから作る。

参考動画の作り:
  - 上部の帯なし。1文ごとに全面の写真を出し、ゆっくりズームイン（切り替えはカット）
  - 字幕は画面中央に短いフレーズ（1〜2行）を、読み上げに合わせて次々に表示。白字＋黒縁＋影、
    強調は {黄} <赤>。表示の瞬間に小さくポップ
  - 冒頭は数行のフック文をまとめて表示
  - 男性ナレーション（〜のである調）、重めのBGM。効果音なし
  - 最後にエンドカード: 丸いアイコン画像、「ご視聴／ありがとうございます」（明朝）、
    紫の「いいね・コメントも／なんとかお願いします！」が1文字ずつ出る。女性の声、明るいBGM

台本（story_docXXX.json）:
  lines[]: {"say": 読み上げ, "tone": 気持ち, "subs": [フレーズ, ...], "scene": 場面名}
           1行目の subs はフック文（"\\n" で改行した1つのブロック）
  outro:   {"say": 締めの挨拶, "icon": 場面名, "bg": 場面名}
  tts / outro_tts: 声の設定（tts_gemini と同じ。後で VOICEVOX に差し替えられるよう分けてある）
  bgm / outro_bgm: bgm/ からの相対パス

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
YELLOW, RED = "#fff21a", "#ff2626"
SUB_SIZE = 96          # 参考動画（576px幅で1文字約51px）を1080px幅に換算
SUB_CY = 0.50          # 字幕の中心（画面の高さに対する割合）
SUB_MAX_W = 1040
ZOOM = 0.14            # 1カットの間にズームインする量
POP = 0.10             # 字幕のポップ時間
ICON = 560             # エンドカードの丸アイコンの直径（参考動画は画面幅の約半分）


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
        sw = max(3, int(size * 0.075))
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
    tts["voice_dir"] = os.path.join(os.path.dirname(os.path.abspath(story_path)), tts["voice_dir"])
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
    lines, outro = cfg["lines"], cfg["outro"]

    # 素材（画像）
    gen_images_gemini.ensure_images(story_path)
    img = lambda name: Image.open(gen_images_gemini.scene_path(cfg, base, name))

    # 声
    tempo = cfg.get("tempo", 1.0)
    clips = [atempo(c, tempo, work, f"m{i}") for i, c in enumerate(voice_clips(story_path, cfg, "tts", lines, work))]
    oclip = atempo(voice_clips(story_path, cfg, "outro_tts", [outro], work)[0], cfg.get("outro_tempo", 1.0), work, "o")
    gap = int(cfg.get("gap", 0.12) * SR)
    t, parts, timings = 0, [np.zeros(int(0.15 * SR), np.float32)], []
    t = len(parts[0])
    for c in clips:
        timings.append((t / SR, (t + len(c)) / SR))
        parts += [c, np.zeros(gap, np.float32)]
        t += len(c) + gap
    t_main = t / SR + 0.35
    parts.append(np.zeros(int(t_main * SR) - t, np.float32))
    o_start = t_main + 0.5
    parts += [np.zeros(int(0.5 * SR), np.float32), oclip, np.zeros(int(cfg.get("outro_tail", 2.2) * SR), np.float32)]
    voice = np.concatenate(parts)
    total = len(voice) / SR
    voice = voice / (np.abs(voice).max() + 1e-9) * 0.89

    # BGM: 本編は重い曲、エンドカードは明るい曲。声の間は下げる（簡易ダッキング）
    n = len(voice)
    env = np.convolve(np.abs(voice), np.ones(int(0.3 * SR)) / (0.3 * SR), "same")
    duck = np.where(env > 0.02, 10 ** (-4 / 20), 1.0)
    duck = np.convolve(duck, np.ones(int(0.2 * SR)) / (0.2 * SR), "same")
    m_end = int(t_main * SR)
    b1 = bgm_track(os.path.join(HERE, "bgm", cfg["bgm"]), m_end, cfg.get("bgm_volume", -11))
    b1[:int(0.6 * SR)] *= np.linspace(0, 1, int(0.6 * SR))
    b1[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))
    b2 = bgm_track(os.path.join(HERE, "bgm", cfg["outro_bgm"]), n - m_end, cfg.get("bgm_volume", -11))
    b2[:int(0.4 * SR)] *= np.linspace(0, 1, int(0.4 * SR))
    b2[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))
    mix = voice + np.concatenate([b1, b2]) * duck
    mix = np.clip(mix, -0.98, 0.98).astype(np.float32)
    wav = os.path.splitext(out)[0] + "_audio.wav"
    mix.tofile(wav + ".f32")
    subprocess.run([FF, "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", wav + ".f32",
                    "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", str(SR), wav], check=True)
    os.remove(wav + ".f32")

    # 字幕: 各文の中でフレーズを文字数の比で割り当てる
    subs = []          # (開始, 終了, 画像)
    for li, (l, (s, e)) in enumerate(zip(lines, timings)):
        phrases = l["subs"]
        if li == 0:   # フックはまとめて1ブロック
            subs.append((0.0, e + 0.06, caption(phrases[0])))
            continue
        lens = [max(1, len(plain(p).replace("\n", ""))) for p in phrases]
        cum = np.cumsum([0] + lens) / sum(lens)
        nxt = timings[li + 1][0] if li + 1 < len(timings) else t_main
        for k, p in enumerate(phrases):
            a = s + (e - s) * cum[k]
            b = s + (e - s) * cum[k + 1] if k + 1 < len(phrases) else nxt
            subs.append((a, b, caption(p)))
    # カット: 文ごとに場面。同じ場面が続く文は1カットにまとめる
    shots = []
    for li, (l, (s, e)) in enumerate(zip(lines, timings)):
        st = 0.0 if li == 0 else s
        if shots and shots[-1][2] == l["scene"]:
            shots[-1][1] = None
        else:
            if shots:
                shots[-1][1] = st
            shots.append([st, None, l["scene"]])
    shots[-1][1] = t_main
    for i in range(len(shots) - 1):
        shots[i][1] = shots[i + 1][0]
    bigs = {sc: cover(img(sc)) for _, _, sc in shots}

    # エンドカード素材
    ob = cover(img(outro["bg"]))
    icon = img(outro["icon"]).convert("RGB")
    side = min(icon.size)
    icon = icon.crop(((icon.width - side) // 2, (icon.height - side) // 2,
                      (icon.width + side) // 2, (icon.height + side) // 2)).resize((ICON, ICON), Image.LANCZOS)
    mask = Image.new("L", (ICON * 4, ICON * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, ICON * 4 - 1, ICON * 4 - 1), fill=255)
    icon.putalpha(mask.resize((ICON, ICON), Image.LANCZOS))

    def serif_line(text, size, color="#f4f1ea", spacing=0.12):
        f = font(SERIF, size, "Regular")
        ws = [f.getlength(c) for c in text]
        tw = int(sum(ws) + size * spacing * (len(text) - 1))
        im = Image.new("RGBA", (tw + 30, size * 2), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        x = 15
        for c, w in zip(text, ws):
            d.text((x, size * 0.3), c, font=f, fill=color)
            x += w + size * spacing
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        sh.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(5)).point(lambda v: v * 0.8))
        o = Image.new("RGBA", im.size, (0, 0, 0, 0))
        o.alpha_composite(sh, (3, 3))
        o.alpha_composite(im)
        return o

    thanks1 = serif_line("ご視聴", 96, spacing=0.14)
    thanks2 = serif_line("ありがとうございます", 88, spacing=0.12)
    ask = outro.get("ask", "いいね・コメントも\nなんとかお願いします！")

    def purple(text):
        f = font(SANS, 62, "Bold")
        lines_ = text.split("\n")
        ws = [f.getlength(x) for x in lines_]
        im = Image.new("RGBA", (int(max(ws + [1])) + 20, 86 * len(lines_) + 10), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for i, x in enumerate(lines_):
            d.text(((im.width - ws[i]) / 2, 5 + i * 86), x, font=f, fill="#8a55ff",
                   stroke_width=3, stroke_fill="#f3eeff")
        return im

    ask_plain = ask.replace("\n", "")
    ask_imgs = {}

    # --- 書き出し ---
    nframes = int(total * FPS)
    proc = subprocess.Popen([FF, "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
                             "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                             "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                            stdin=subprocess.PIPE)
    for fi in range(nframes):
        tt = fi / FPS
        if tt < t_main:
            sh = next(s for s in shots if s[0] <= tt < s[1] or s is shots[-1])
            p = (tt - sh[0]) / max(0.1, sh[1] - sh[0])
            frame = zoom_frame(bigs[sh[2]], min(1, p)).convert("RGBA")
            cur = [x for x in subs if x[0] <= tt < x[1]]
            if cur:
                a, b, cap = cur[-1]
                dt = tt - a
                sc = 0.88 + 0.12 * min(1, dt / POP)
                c = cap if sc >= 1 else cap.resize((int(cap.width * sc), int(cap.height * sc)), Image.BILINEAR)
                cy = int(H * SUB_CY)
                frame.alpha_composite(c, ((W - c.width) // 2, cy - c.height // 2))
        else:
            dt = tt - t_main
            frame = zoom_frame(ob, min(1, dt / (total - t_main)) * 0.6).convert("RGBA")
            frame.alpha_composite(icon, ((W - ICON) // 2, 40))
            frame.alpha_composite(thanks1, ((W - thanks1.width) // 2, 610))
            frame.alpha_composite(thanks2, ((W - thanks2.width) // 2, 790))
            # 紫の文字を1文字ずつ
            k = int(max(0, dt - 0.8) / 0.09)
            shown = ask_plain[:k]
            if shown:
                cut = ask.split("\n")[0]
                txt = shown if len(shown) <= len(cut) else shown[:len(cut)] + "\n" + shown[len(cut):]
                if txt not in ask_imgs:
                    ask_imgs[txt] = purple(txt)
                pi = ask_imgs[txt]
                frame.alpha_composite(pi, ((W - pi.width) // 2, 960))
        proc.stdin.write(frame.convert("RGB").tobytes())
        if fi % 300 == 0:
            print(f"frame {fi}/{nframes}", flush=True)
    proc.stdin.close()
    proc.wait()

    # 字幕ファイル
    def ts(x):
        return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x * 1000 % 1000):03d}"
    with open(os.path.splitext(out)[0] + ".srt", "w", encoding="utf-8") as fh:
        for i, (l, (s, e)) in enumerate(zip(lines, timings)):
            fh.write(f"{i + 1}\n{ts(s)} --> {ts(e)}\n{l['say']}\n\n")
    print(f"done: {out} ({total:.2f}s)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
