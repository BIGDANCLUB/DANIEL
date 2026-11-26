"""「もしも人間がタマゴで生まれたら？」の合成。フェロモン版（PH-001）の合成をもとに、文字・音を差しかえる。
usage: python3 compose.py frames_root out.mp4 [bgm.wav]"""
import importlib.util
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timeline as TL  # noqa: E402  （フェロモン版より先に読み込む）

_spec = importlib.util.spec_from_file_location("ph_compose", os.path.join(HERE, "..", "pheromone", "compose.py"))
PC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PC)
FC, CC, Y, SC = PC.FC, PC.CC, PC.Y, PC.SC
FPS, SR = TL.FPS, CC.SR
HY, HS = PC.HY, PC.HS
PC.LABEL = "タマゴになってから"
PC.WORD, PC.PRE, PC.POST = "タマゴ", "もしも人間が", "で生まれたら？"
PC.EXPO = {"e00_open": 0.85, "e01_burst": 0.85, "e02_size": 0.8, "e03_warm": 0.9, "e04_office": 0.82, "e05_penguin": 0.75,
           "e06_strong": 0.9, "e07_hatch": 0.9, "e08_home": 0.9}


def draw(s, i, base):
    g = PC.look(base, s)
    fade = CC.fade
    W_, P_, Q_ = PC.WORD, PC.PRE, PC.POST
    if s.get("kind") == "open":
        sec = s.get("t0", 0.0) + i / FPS
        if sec < TL.T_VANISH:
            Y.big_title(g, W_, "もしも人間が", "で", "生まれたら？", "赤ちゃんが、おなかの中ではなく、タマゴで生まれてきたら")
            Y.countdown(g, "タマゴになるまで", TL.T_VANISH - sec)
            Y.headline(g, "赤ちゃんは[約3kg]で生まれる", ["お母さんのおなかで", "約9か月育つ"], fade(sec, 0.4, 2.75), y=HY, size=HS)
            Y.headline(g, "タマゴを産む哺乳類も[いる]", ["カモノハシは", "タマゴで子どもを産む"], fade(sec, 2.75, TL.T_VANISH + 0.01), y=HY, size=HS)
            Y.note(g, "※研究をもとにした、もしもの話です", fade(sec, 0.2, TL.T_VANISH, k=0.3))
        else:
            Y.title_small(g, W_, P_, Q_)
            Y.elapsed(g, PC.LABEL, "1", CC.fmt_elapsed(sec - TL.T_VANISH, 1), s.get("loc"))
        return g
    sec = i / FPS
    Y.title_small(g, W_, P_, Q_)
    e, speed = TL.e_of(s, i)
    Y.elapsed(g, PC.LABEL, CC.fmt_speed(speed), CC.fmt_elapsed(e, speed), s.get("loc"))
    for a, b, head, sub in s.get("captions", []):
        Y.headline(g, head, sub, fade(sec, a, b), y=HY, size=HS)
    if s.get("card"):
        Y.card(g, s["card"], fade(sec, 0.0, 1.3, k=0.12))
    return g


def crack(seed=0):
    """殻の「ピシッ」。"""
    r = np.random.default_rng(seed)
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    x = SC.band(CC.noise(0.12, seed), 2000, 8000) * np.exp(-t / 0.015)
    x += np.sin(2 * np.pi * r.uniform(2500, 4000) * t) * np.exp(-t / 0.01) * 0.3
    return x * 0.8


def cry(dur=1.4, seed=0):
    """赤ちゃんの「おぎゃあ」（やさしく、短く）。"""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f0 = 420 + 60 * np.sin(2 * np.pi * 1.6 * t) + 40 * np.sin(2 * np.pi * 5.5 * t)
    ph = 2 * np.pi * np.cumsum(f0) / SR
    x = sum(np.sin(k * ph) * a for k, a in ((1, 1.0), (2, 0.5), (3, 0.35), (4, 0.15)))
    env = np.minimum(1, t / 0.08) * np.clip((dur - t) / 0.3, 0, 1) * (0.6 + 0.4 * np.sin(np.pi * t / dur))
    return x * env * 0.12


def build_audio(total):
    st = {s["name"]: TL.start_of(s["name"]) for s in TL.SHOTS}
    a = np.zeros(int(total * SR) + SR)

    def put(x, at, gain=1.0):
        i = int(at * SR)
        j = min(len(a), i + len(x))
        if j > i and i >= 0:
            a[i:j] += gain * x[: j - i]

    put(CC.ambience(total), 0, 1.0)
    rng = np.random.default_rng(9)
    # 冒頭：新生児室（足音・カートの音・赤ちゃんの声）＋時計 → 5.6秒でポンポンポン
    put(SC.murmur(TL.T_VANISH, 70), 0.0, 0.5)
    for k, tt in enumerate((0.3, 1.5, 2.9, 4.1)):
        put(cry(1.0, k), tt, 0.6)
        put(PC.pass_by(0.9, 80 + k), tt + 0.4, 0.6)
    t0 = 0.05
    while t0 < TL.T_VANISH:
        put(SC.step(int(t0 * 991)), t0, rng.uniform(0.5, 0.8))
        t0 += rng.uniform(0.11, 0.16)
    for k in range(1, 6):
        put(CC.tick(), TL.T_VANISH - k, 0.6)
    put(PC.impact(), TL.T_VANISH, 0.8)
    for k in range(18):
        put(PC.poof(k), TL.T_VANISH + 0.03 * k * 2, 0.5)
    put(CC.sparkle(1, 1.8), TL.T_VANISH, 0.7)
    for s in TL.SHOTS:
        name = s["name"]
        if s.get("segs"):
            e0, sp = TL.e_of(s, 0)
            if sp > 50:
                for k, tt in enumerate(np.arange(0.25, s["frames"] / FPS - 0.1, 0.4)):
                    put(SC.clock(k), st[name] + tt, 0.5)
        if s.get("card"):
            put(CC.whoosh(0.9, hash(name) % 50), st[name] - 0.2, 0.7)
        for a0, b0, head, sub in s.get("captions", []):
            put(CC.pop(), st[name] + a0, 0.6)
    t = st["e01_burst"]
    put(SC.murmur(4.0, 71), t, 0.8)
    put(PC.heartbeat(), t + 0.5, 0.6)
    t = st["e02_size"]
    for k in range(3):
        put(PC.poof(20 + k), t + (10 + 18 * k) / FPS, 0.6)
    t = st["e03_warm"]
    put(PC.heartbeat() * 0.5, t + 1.2, 0.5)
    put(CC.sparkle(2, 1.2), t + 1.2, 0.4)
    put(SC.step(300, hard=False), t + 2.3, 0.5)
    t = st["e04_office"]
    for k in range(10):
        put(SC.step(310 + k), t + 0.9 + 0.22 * k, 0.4)
    put(PC.heartbeat(), t + 2.0, 0.5)
    t = st["e05_penguin"]
    put(FC.wind(5.0, 72), t, 1.0)
    t = st["e06_strong"]
    put(FC.thud(), t + 1.5, 0.8)
    put(PC.deflate(0.6) * 0.0, t, 0.0)
    put(CC.sparkle(3, 1.0), t + 2.0, 0.5)
    t = st["e07_hatch"]
    for k in range(9):
        put(crack(k), t + 1.4 + 0.27 * k, 0.8)
    put(crack(20), t + 4.0, 1.0)
    put(cry(1.6, 21), t + 4.3, 1.0)
    put(FC.cheer(1.6, 73) * 0.6, t + 4.5, 0.5)
    t = st["e08_home"]
    put(PC.piano([(262, 330, 392), 392, 440, 392, (349, 440, 523), 523, 494, 440, (330, 392, 523), 392, 440, 523, (349, 440, 587),
                  (392, 494, 587), (330, 392, 523)], dt=0.55, decay=1.0, amp=0.12), t + 0.6, 1.0)
    a = a / max(1e-6, np.abs(a).max()) * 0.8
    return a


PC.draw = draw
PC.build_audio = build_audio

if __name__ == "__main__":
    PC.main()
