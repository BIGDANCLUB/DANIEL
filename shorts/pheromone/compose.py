"""「もしも男女がフェロモンを出すようになったら？」の合成（よねあぷ型の文字＋効果音＋BGM）。ナレーションなし。
usage: python3 compose.py frames_root out.mp4 [bgm.wav]"""
import importlib.util
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timeline as TL  # noqa: E402

_spec = importlib.util.spec_from_file_location("sugi_compose", os.path.join(HERE, "..", "sugi", "compose.py"))
SC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SC)       # スギ版の色の仕上げと音の部品を使う
FC, CC, Y = SC.FC, SC.CC, SC.Y
O = Y.O
FC.GRADE = dict(FC.GRADE, lo=0.05, hi=0.86, gam=1.45, s=0.6, r=0.98, b=1.01, sat=0.6, vib=0.4)     # 試しの画で計測して決めた値
FPS, SR = TL.FPS, CC.SR
LABEL = "フェロモンが出てから"
WORD, PRE, POST = "フェロモン", "もしも", "が出たら？"
tone, noise, lp, env, band = CC.tone, CC.noise, CC.lp, CC.env, SC.band
HY, HS = FC.HY, FC.HS


def sepia(img):
    """昔の話（実話の場面）は、セピア色の古い写真のように。"""
    a = np.asarray(img.convert("RGB"), np.float32) / 255
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    s = np.clip(lum[..., None] * np.array([1.08, 0.90, 0.66], np.float32), 0, 1)
    out = s * 0.88 + a * 0.12
    return Image.fromarray((out * 255 + 0.5).astype(np.uint8))


def look(base, s):
    return FC.look(sepia(base) if s.get("sepia") else base)


def end_card(im):
    """締め：次は何の「もしも」が見たい？"""
    O.shadow_text(im, (540, 860), "次は何の", Y.f(92, "Black"), anchor="mm", blur=6, alpha=170)
    O.runs_text(im, 540, 1013, [("もしも", Y.KEY), ("が見たい？", Y.WHITE)], Y.f(92, "Black"))
    O.shadow_text(im, (540, 1100), "コメントで聞かせてください", Y.f(40, "Bold"), anchor="mm", blur=4, alpha=150)


def draw(s, i, base):
    g = look(base, s)
    fade = CC.fade
    if s.get("kind") == "open":
        sec = s.get("t0", 0.0) + i / FPS
        if sec < TL.T_VANISH:
            Y.big_title(g, WORD, PRE, "が", "出るようになったら？", "男も女も、異性を引きつける「におい」を出しはじめたら")
            Y.countdown(g, "フェロモンが出るまで", TL.T_VANISH - sec)
            Y.headline(g, "オスのガは[1km先]のメスに気づく", ["においの正体は", "フェロモン"], fade(sec, 0.4, 2.75), y=HY, size=HS)
            Y.headline(g, "人間のフェロモンは[まだない]", ["研究されてきたが", "見つかっていない"], fade(sec, 2.75, TL.T_VANISH + 0.01),
                       y=HY, size=HS)
            Y.note(g, "※研究をもとにした、もしもの話です", fade(sec, 0.2, TL.T_VANISH, k=0.3))
        else:
            Y.title_small(g, WORD, PRE, POST)
            Y.elapsed(g, LABEL, "1", CC.fmt_elapsed(sec - TL.T_VANISH, 1), s.get("loc"))
        return g
    sec = i / FPS
    Y.title_small(g, WORD, PRE, POST)
    e, speed = TL.e_of(s, i)
    Y.elapsed(g, LABEL, CC.fmt_speed(speed), CC.fmt_elapsed(e, speed), s.get("loc"))
    for a, b, head, sub in s.get("captions", []):
        Y.headline(g, head, sub, fade(sec, a, b), y=HY, size=HS)
    if s.get("card"):
        Y.card(g, s["card"], fade(sec, 0.0, 1.3, k=0.12))
    return g


# ---------- 音 ----------
def wingbeat(seed=0):
    """ガの羽音「パタッ」（やわらかく短い、粉っぽい音）。"""
    r = np.random.default_rng(seed)
    n = int(0.06 * SR)
    x = band(noise(0.06, seed), 250, 2200) * env(n, 0.002, 0.018)
    return x * r.uniform(0.5, 0.9)


def heartbeat():
    """「ドキッ・ドキッ」（低い音を2回）。"""
    out = np.zeros(int(0.7 * SR))
    for k, (t0, a) in enumerate(((0.0, 1.0), (0.22, 0.7))):
        n = int(0.18 * SR)
        tt = np.arange(n) / SR
        x = np.sin(2 * np.pi * np.cumsum(65 - 25 * tt / 0.18) / SR) * np.exp(-tt / 0.06) * a
        i = int(t0 * SR)
        out[i:i + n] += x
    return out * 0.9


def poof(seed=0):
    """けむりが「ぽわん」と出る音（やわらかいノイズ＋上がる音）。"""
    n = int(0.6 * SR)
    tt = np.arange(n) / SR
    x = band(noise(0.6, seed), 300, 3000) * np.exp(-tt / 0.15) * 0.5
    x += tone(0.6, 500, 1100) * np.exp(-tt / 0.2) * 0.25
    return x * np.minimum(1, tt / 0.01)


def hiss(dur=1.2, seed=31):
    """電車のドアが開く「プシュー」。"""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    return band(noise(dur, seed), 1500, 7000) * np.minimum(1, tt / 0.02) * np.exp(-tt / 0.45) * 0.7


def door_chime():
    """発車メロディのような短い「ピンポン」。"""
    out = []
    for f0 in (988, 784):
        n = int(0.35 * SR)
        tt = np.arange(n) / SR
        out.append((np.sin(2 * np.pi * f0 * tt) + 0.3 * np.sin(4 * np.pi * f0 * tt)) * np.exp(-tt / 0.25) * 0.25)
    return np.concatenate(out)


def clink(seed=0):
    """ガラスびんの「カチャ」。"""
    r = np.random.default_rng(seed)
    n = int(0.25 * SR)
    tt = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * r.uniform(0.97, 1.03) * tt) * np.exp(-tt / d) * a
            for f, d, a in ((2300, 0.08, 1.0), (3900, 0.05, 0.6), (5600, 0.03, 0.4)))
    return x * 0.22


def deflate(dur=1.1):
    """がっかりの「ひゅるるる」（下がっていく音）。"""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = 700 * np.exp(-tt * 1.6) + 120
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.04 * np.sin(2 * np.pi * 9 * tt))) / SR
    return np.sin(ph) * np.minimum(1, tt / 0.03) * np.clip((dur - tt) / 0.3, 0, 1) * 0.22


def piano(notes, dt=0.42, decay=0.7, amp=0.16):
    out = np.zeros(int((len(notes) * dt + 2.0) * SR))
    for k, ch in enumerate(notes):
        for f in (ch if isinstance(ch, tuple) else (ch,)):
            n = int(2.0 * SR)
            tt = np.arange(n) / SR
            x = sum(np.sin(2 * np.pi * f * h * tt) / (h * h) for h in (1, 2, 3, 4)) * np.exp(-tt / decay) * amp
            i = int(k * dt * SR)
            out[i:i + n] += x
    return out


def impact():
    n = int(0.9 * SR)
    tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * np.cumsum(70 - 30 * tt) / SR) * np.exp(-tt / 0.25) * 0.9
    return x + band(noise(0.9, 71), 300, 5000) * np.exp(-tt / 0.06) * 0.6


def pass_by(dur=1.3, seed=72):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    x = noise(dur, seed)
    y = np.zeros(n)
    for i in range(0, n, 1024):
        u = tt[i] / dur
        y[i:i + 1024] = lp(x[i:i + 1024], 600 + 4500 * (1 - abs(2 * u - 1)))
    return y * np.sin(np.pi * tt / dur) ** 1.5 * 1.0


def build_audio(total):
    st = {s["name"]: TL.start_of(s["name"]) for s in TL.SHOTS}
    a = np.zeros(int(total * SR) + SR)

    def put(x, at, gain=1.0):
        i = int(at * SR)
        j = min(len(a), i + len(x))
        if j > i:
            a[i:j] += gain * x[: j - i]

    put(CC.ambience(total), 0, 1.0)
    rng = np.random.default_rng(7)
    # 冒頭（最初の5秒は派手に）：ドン → ガの羽音が0.1〜0.16秒おき → 切りかえのシュッ → 人波の足音 → すれちがうゴーッ
    put(impact(), 0.0, 1.0)
    put(CC.flutter(2.6, 3), 0.0, 0.5)
    t0 = 0.04
    while t0 < 2.6:
        put(wingbeat(int(t0 * 1000)), t0, rng.uniform(0.7, 1.0))
        t0 += rng.uniform(0.10, 0.16)
    put(pass_by(1.0, 72), 0.9, 0.8)
    put(CC.whoosh(0.9, 50), 2.45, 0.9)
    put(SC.murmur(3.4, 54), 2.6, 0.9)
    t0 = 2.62
    while t0 < TL.T_VANISH:
        put(SC.step(int(t0 * 997)), t0, rng.uniform(0.6, 1.0))
        t0 += rng.uniform(0.08, 0.13)
    put(pass_by(1.1, 73), 3.6, 0.7)
    for k in range(1, 6):
        put(CC.tick(), TL.T_VANISH - k, 0.6)
    # 出はじめる瞬間：ぽわん＋キラキラ＋ドキッ
    put(poof(1), TL.T_VANISH, 1.0)
    put(CC.sparkle(1, 2.0), TL.T_VANISH, 0.9)
    put(heartbeat(), TL.T_VANISH + 0.25, 1.0)
    put(SC.murmur(2.4, 55), TL.T_VANISH + 0.4, 0.6)
    for s in TL.SHOTS:
        if s.get("segs"):
            e0, sp = TL.e_of(s, 0)
            if sp > 50:      # 早送りの場面は、時計のカチカチ
                for k, tt in enumerate(np.arange(0.25, s["frames"] / FPS - 0.1, 0.4)):
                    put(SC.clock(k), st[s["name"]] + tt, 0.7)
        if s.get("card"):
            put(CC.whoosh(0.9, hash(s["name"]) % 50), st[s["name"]] - 0.2, 0.7)
        for a0, b0, head, sub in s.get("captions", []):
            put(CC.pop(), st[s["name"]] + a0, 0.6)
    t = st["p02_burst"]
    put(SC.murmur(4.0, 56), t, 0.9)
    for k in range(6):
        put(poof(10 + k), t + 0.2 + k * 0.55, 0.45)
    t = st["p03_plume"]
    put(FC.wind(4.5, 57), t, 0.25)
    put(heartbeat(), t + 0.6, 0.7)
    put(heartbeat(), t + 2.6, 0.6)
    t = st["p04_train"]
    put(SC.rumble(3.0, 58, 0.5), t, 0.5)
    put(hiss(), t + 92 / FPS, 1.0)
    put(door_chime(), t + 100 / FPS, 0.8)
    put(CC.whoosh(1.2, 59), t + 95 / FPS, 0.6)
    t = st["p05_office"]
    for k in range(14):
        put(SC.step(120 + k), t + 0.9 + k * 0.22, 0.4)
    put(FC.cheer(3.0, 60), t + 1.8, 0.35)
    put(heartbeat(), t + 2.2, 0.6)
    t = st["p06_wind"]
    put(FC.wind(5.0, 61), t, 0.9)
    for k in range(5):
        put(CC.chirp(70 + k), t + 0.6 + k * 0.9, 0.35)
    for k in range(12):
        put(SC.step(130 + k, hard=False), t + 0.5 + k * 0.38, 0.4)
    t = st["p07_perfume"]
    for k in range(7):
        put(clink(k), t + (22 + k * 13 + 10) / FPS, 0.8)
    t = st["p08_silk"]
    put(CC.flutter(4.8, 62), t + 0.1, 0.5)
    for k in range(8):
        put(SC.clock(k), t + 0.4 + k * 0.6, 0.3)
    t = st["p09_orchard"]
    put(FC.wind(5.0, 63), t, 0.4)
    put(CC.flutter(5.0, 64), t, 0.35)
    for k in range(4):
        put(CC.chirp(80 + k), t + 0.8 + k * 1.1, 0.3)
    t = st["p10_confuse"]
    put(SC.murmur(5.5, 65), t, 1.0)
    for k in range(20):
        put(SC.step(150 + k), t + 0.3 + k * 0.26, 0.4)
    put(deflate(1.0), t + 3.2, 0.6)
    t = st["p11_used"]
    for k in range(10):
        put(SC.step(180 + k), t + 0.4 + k * 0.45, 0.35)
    put(deflate(1.3), t + 1.6, 1.0)
    t = st["p12_home"]
    put(FC.thud(), t + 0.3, 0.3)
    put(piano([(262, 330, 392), 392, 440, 392, (349, 440, 523), 523, 494, 440, (330, 392, 523), 392, 440, 523, (349, 440, 587),
               (392, 494, 587), (330, 392, 523)], dt=0.55, decay=1.0, amp=0.12), t + 0.9, 1.0)
    put(heartbeat() * 0.5, t + 2.4, 0.6)
    a = a / max(1e-6, np.abs(a).max()) * 0.8
    return a


def main():
    root, out = sys.argv[1], sys.argv[2]
    bgm = sys.argv[3] if len(sys.argv) > 3 else None
    total = TL.total_frames() / FPS
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Y.W}x{Y.H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                            out + ".video.mp4"], stdin=subprocess.PIPE)
    last_img, last_s = None, None
    for s in TL.SHOTS:
        if s.get("kind") == "end":
            base = look(last_img, last_s)
            for i in range(s["frames"]):
                g = base.copy()
                g.alpha_composite(Image.new("RGBA", base.size, (8, 8, 10, int(150 * min(1.0, i / 12)))))
                if i >= 6:
                    end_card(g)
                enc.stdin.write(g.convert("RGB").tobytes())
            continue
        d = os.path.join(root, s["name"])
        prev = None
        for i in range(s["frames"]):
            p = os.path.join(d, f"f_{i + 1:04d}.png")
            if os.path.exists(p):
                cur = Image.open(p).convert("RGB")
                nxt = os.path.join(d, f"f_{i + 2:04d}.png")
                prev = cur
            elif prev is not None:
                nxt = os.path.join(d, f"f_{i + 2:04d}.png")
                if os.path.exists(nxt):         # 1コマおきに書き出したときは、前後をまぜて間をうめる
                    cur = Image.blend(prev, Image.open(nxt).convert("RGB"), 0.5)
                else:
                    cur = prev
            else:
                cur = Image.new("RGB", (540, 960), (0, 0, 0))
            last_img, last_s = cur, s
            enc.stdin.write(draw(s, i, cur).convert("RGB").tobytes())
        print("composed", s["name"], flush=True)
    enc.stdin.close()
    enc.wait()
    audio = build_audio(total)
    wav = out + ".sfx.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    inputs = ["-i", out + ".video.mp4", "-i", wav]
    fc = "[1:a]volume=1.0[s]"
    if bgm:
        inputs += ["-stream_loop", "-1", "-i", bgm]
        fc += (f";[2:a]volume={os.environ.get('BGM_VOL', '0.3')},atrim=0:{total:.2f},afade=t=out:st={total - 2.5:.2f}:d=2.5[b];"
               "[s][b]amix=inputs=2:normalize=0[m];[m]loudnorm=I=-14:TP=-1.5[a]")
    else:
        fc += ";[s]loudnorm=I=-14:TP=-1.5[a]"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", out], check=True)
    os.remove(out + ".video.mp4")
    os.remove(wav)
    print("done", out, f"{total:.2f}s")


if __name__ == "__main__":
    main()
