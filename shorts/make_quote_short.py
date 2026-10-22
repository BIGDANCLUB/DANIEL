#!/usr/bin/env python3
"""動画引用シリーズ（10/22 ユーザー指定）: 参考動画（YouTube「世界から見たスゴイ日本」の新幹線の回）の作りをそのまま真似る。

画面（1080x1920、参考動画を実測）
  - 背景は黒。上の黒帯に2行のタイトル（1行目 白、2行目 黄 #F7FA14）。Noto Sans JP Black 108px、縁取りなし
  - 中央 y=479〜1593 に引用した動画（横幅いっぱい、はみ出しは上下を切る）
  - 下の黒帯に引用元の表示（「@アカウント名」白、y≈1717）
  - 字幕はNoto Sans JP Black 92px、白文字＋黒縁、2行まで、ブロックの中心 y≈1271。出入りはパッと切り替え（動きなし）
    ナレーションは白、動画の中の人のセリフは水色 #50C4EF
声
  - VOICEVOX ずんだもん（ノーマル）、速さ 1.25（参考動画の字幕の表示時間から逆算）。字幕どおりに読む
  - 引用した動画の音は、ナレーション中は下げ、ナレーションのない間は元の大きさで流す
  - 仕上がりの音量は参考動画と同じ -9.6 LUFS 前後

usage: python3 make_quote_short.py story_q001.json out/Q-001.mp4
台本（JSON）
  title: ["1行目（白）", "2行目（黄）"]
  credit: "@account"
  clip: 引用する動画ファイル（台本からの相対パス）
  clip_ss: 動画の開始秒（省略で0）
  lines: [{"say": 読み, "subs": ["1行目\n2行目", ...], "color": "white"|"blue", "kana": 任意,
           "pause": 任意（このあと元の音だけ流す秒数）}]
"""
import json
import os
import subprocess
import sys
import urllib.parse

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import make_doc_short as doc

HERE = os.path.dirname(os.path.abspath(__file__))
FF = doc.FF
W, H, FPS = 1080, 1920, 30
SR = doc.SR
FONT = os.environ.get("QUOTE_FONT", os.path.join(HERE, "fonts", "NotoSansJP[wght].ttf"))   # Noto Sans JP Black（10/22 ユーザー指定）
TITLE_SIZE, TITLE_Y = 108, (272, 403)
VIDEO_TOP, VIDEO_BOTTOM = 479, 1593
CREDIT_SIZE, CREDIT_Y = 70, 1717
SUB_SIZE, SUB_CY, SUB_PITCH, SUB_STROKE = 92, 1271, 106, 8
WHITE, YELLOW, BLUE = "#ffffff", "#f7fa14", "#50c4ef"
VOICE = {"speaker": "ずんだもん", "style": "ノーマル", "speedScale": 1.25}
LEAD, GAP, DUCK_DB, LUFS = 0.2, 0.1, -10, -9.6


def font(size):
    f = ImageFont.truetype(FONT, size)
    if "NotoSans" in FONT:
        f.set_variation_by_name("Black")
    return f


def centered(d, text, y, size, fill, stroke=0):
    f = font(size)
    x = (W - f.getlength(text)) / 2
    d.text((x, y), text, font=f, fill=fill, anchor="lm", stroke_width=stroke, stroke_fill="#000000")


def base_frame(title, credit):
    """黒地にタイトルと引用元を描いた下敷き（動画の部分は透明）。"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(im)
    for text, y, col in zip(title, TITLE_Y, (WHITE, YELLOW)):
        size = TITLE_SIZE
        while font(size).getlength(text) > W - 40:
            size -= 2
        centered(d, text, y, size, col)
    centered(d, credit, CREDIT_Y, CREDIT_SIZE, WHITE)
    im.paste((0, 0, 0, 0), (0, VIDEO_TOP, W, VIDEO_BOTTOM))
    return im


def subtitle(text, color):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = text.split("\n")
    y0 = SUB_CY - SUB_PITCH * (len(rows) - 1) / 2
    for i, r in enumerate(rows):
        size = SUB_SIZE
        while font(size).getlength(r) > W - 60:
            size -= 2
        centered(d, r, y0 + i * SUB_PITCH, size, color, SUB_STROKE)
    return im


def voice(lines, vdir):
    """ずんだもんで1行ずつ作り、各行の音声と字幕ページの切り替え時刻を返す。"""
    import hashlib
    try:
        doc.urllib.request.urlopen(doc.VOICEVOX_URL + "/version", timeout=3)
    except Exception:
        subprocess.run(["bash", os.path.join(HERE, "tools", "voicevox_setup.sh")], check=True)
    sid = doc.voicevox_speaker(VOICE["speaker"], VOICE["style"])
    os.makedirs(vdir, exist_ok=True)
    out = []
    for i, l in enumerate(lines):
        q = doc.vv_query(l["say"], sid)
        if l.get("kana"):
            q["accent_phrases"] = json.loads(doc.vv_post("/accent_phrases?" + urllib.parse.urlencode(
                {"text": l["kana"], "speaker": sid, "is_kana": "true"})))
        q.update(speedScale=VOICE["speedScale"], prePhonemeLength=0.0, postPhonemeLength=0.05)
        key = hashlib.sha1(json.dumps([sid, l["say"], l.get("kana"), VOICE], ensure_ascii=False).encode()).hexdigest()[:12]
        wav = os.path.join(vdir, f"{i + 1:02d}_{key}.wav")
        if not os.path.exists(wav):
            open(wav, "wb").write(doc.vv_post(f"/synthesis?speaker={sid}", q))
        a = doc.load_audio(wav)
        pages = l["subs"]
        bounds = []
        if len(pages) > 1:      # ページの切り替え: モーラ数の比で文中の時刻に当てる
            starts = doc.mora_starts(q)
            counts = [doc.n_moras(doc.vv_query(doc.page_reading(p), sid)) for p in pages]
            scale = doc.n_moras(q) / max(1, sum(counts))
            cum = 0.0
            for c in counts[:-1]:
                cum += c * scale
                bounds.append(starts[min(len(starts) - 1, int(round(cum)))])
        out.append((a, bounds))
    return out


def main(story_path, out):
    cfg = json.load(open(story_path))
    base = os.path.dirname(os.path.abspath(story_path))
    work = os.path.splitext(out)[0] + "_work"
    os.makedirs(work, exist_ok=True)
    lines = cfg["lines"]
    clips = voice(lines, os.path.join(base, cfg.get("voice_dir", work + "/voice")))

    # タイムライン: 行ごとに読み、"pause" があれば元の音だけ流す
    t, subs, narr = LEAD, [], []
    for l, (a, bounds) in zip(lines, clips):
        st, dur = t, len(a) / SR
        edges = [st] + [st + b for b in bounds] + [st + dur]
        for p, (s0, s1) in zip(l["subs"], zip(edges, edges[1:])):
            subs.append([s0, s1, p, BLUE if l.get("color") == "blue" else WHITE])
        narr.append((st, a))
        t = st + dur + GAP + l.get("pause", 0)
    total = cfg.get("duration") or t + cfg.get("tail", 0.3)
    for i in range(len(subs) - 1):       # 次の字幕までは前の字幕を出しておく（参考動画と同じ）
        subs[i][1] = subs[i + 1][0]
    subs[-1][1] = min(total, subs[-1][1] + 0.3)
    n = int(round(total * SR))

    # 音: 引用した動画の音（ナレーション中は下げる）＋ずんだもん
    clip = os.path.join(base, cfg["clip"])
    ss = cfg.get("clip_ss", 0)
    orig = np.frombuffer(subprocess.run([FF, "-v", "error", "-ss", str(ss), "-i", clip, "-t", f"{total:.3f}",
                                         "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                        capture_output=True).stdout, np.float32).copy()
    orig = np.pad(orig, (0, max(0, n - len(orig))))[:n] * 10 ** (cfg.get("clip_volume", 0) / 20)
    vo = np.zeros(n, np.float32)
    gain = np.ones(n, np.float32)
    for st, a in narr:
        i = int(st * SR)
        seg = a[:max(0, n - i)]
        vo[i:i + len(seg)] += seg
        gain[max(0, i - int(0.1 * SR)):i + len(seg) + int(0.1 * SR)] = 10 ** (DUCK_DB / 20)
    gain = np.convolve(gain, np.ones(int(0.1 * SR)) / (0.1 * SR), "same").astype(np.float32)
    mix = np.clip(vo + orig * gain, -0.99, 0.99).astype(np.float32)
    raw = os.path.join(work, "mix.f32")
    mix.tofile(raw)
    wav = os.path.join(work, "mix.wav")
    # 参考動画と同じ大きさ（-9.6 LUFS）に: 測ってから音量を足し、リミッターで頭を抑える
    r = subprocess.run([FF, "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw,
                        "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    now = float([x for x in r.splitlines() if x.strip().startswith("I:")][-1].split()[1])
    gain_db = LUFS - now
    for _ in range(3):
        subprocess.run([FF, "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw,
                        "-af", f"volume={gain_db:.2f}dB,alimiter=limit=0.97:attack=5:release=50:level=false",
                        "-ar", str(SR), "-t", f"{total:.3f}", wav], check=True)
        r = subprocess.run([FF, "-hide_banner", "-i", wav, "-af", "ebur128", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        got = float([x for x in r.splitlines() if x.strip().startswith("I:")][-1].split()[1])
        if abs(got - LUFS) < 0.3:
            break
        gain_db += LUFS - got

    # 映像
    over = base_frame(cfg["title"], cfg["credit"])
    vh = VIDEO_BOTTOM - VIDEO_TOP
    reader = subprocess.Popen([FF, "-v", "error", "-ss", str(ss), "-stream_loop", "-1", "-i", clip,
                               "-vf", f"scale={W}:{vh}:force_original_aspect_ratio=increase,crop={W}:{vh},fps={FPS}",
                               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen([FF, "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}",
                            "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    cache = {}
    for fi in range(int(round(total * FPS))):
        tt = fi / FPS
        buf = reader.stdout.read(W * vh * 3)
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        if len(buf) == W * vh * 3:
            frame.paste(Image.frombytes("RGB", (W, vh), buf), (0, VIDEO_TOP))
        frame.alpha_composite(over)
        cur = [s for s in subs if s[0] <= tt < s[1]]
        if cur:
            k = (cur[-1][2], cur[-1][3])
            if k not in cache:
                cache[k] = subtitle(k[0].replace("{", "").replace("}", "").replace("<", "").replace(">", ""), k[1])
            frame.alpha_composite(cache[k])
        enc.stdin.write(frame.convert("RGB").tobytes())
    reader.kill()
    enc.stdin.close()
    enc.wait()
    with open(os.path.splitext(out)[0] + ".srt", "w") as f:
        for i, (s0, s1, p, _) in enumerate(subs):
            ts = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{x % 60:06.3f}".replace(".", ",")
            f.write(f"{i + 1}\n{ts(s0)} --> {ts(s1)}\n{p}\n\n")
    print(f"done: {out} ({total:.2f}s)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
