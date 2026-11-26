"""「もしも恋のドキドキが周りに聞こえるようになったら？」の合成。フェロモン版（PH-001）の合成をもとに、文字・音を差しかえる。
心臓の「ドクン」は beats.py の拍の時刻（3D の輪と同じ）で鳴らす。
usage: python3 compose.py frames_root out.mp4 [bgm.wav]"""
import importlib.util
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timeline as TL  # noqa: E402  （フェロモン版より先に読み込む）
import beats as BT  # noqa: E402

_spec = importlib.util.spec_from_file_location("ph_compose", os.path.join(HERE, "..", "pheromone", "compose.py"))
PC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PC)
FC, CC, Y, SC = PC.FC, PC.CC, PC.Y, PC.SC
FPS, SR = TL.FPS, CC.SR
HY, HS = PC.HY, PC.HS
PC.LABEL = "聞こえだしてから"
PC.WORD, PC.PRE, PC.POST = "ドキドキ", "もしも", "が聞こえたら？"
PC.EXPO = {"d00_open": 1.6, "d01_burst": 1.3, "d02_train": 0.87, "d04_meeting": 0.82, "d07_library": 0.9, "d08_home": 0.85}


def draw(s, i, base):
    g = PC.look(base, s)
    fade = CC.fade
    W_, P_, Q_ = PC.WORD, PC.PRE, PC.POST
    if s.get("kind") == "open":
        sec = s.get("t0", 0.0) + i / FPS
        if sec < TL.T_VANISH:
            Y.big_title(g, W_, P_, "が", "聞こえるようになったら？", "恋をしたときの心臓の音が、まわりの人に聞こえはじめたら")
            Y.countdown(g, "聞こえるまで", TL.T_VANISH - sec)
            Y.headline(g, "心臓は1日に[約10万回]打つ", ["ふだんは", "聞こえない"], fade(sec, 0.4, 2.75), y=HY, size=HS)
            Y.headline(g, "好きな人の前では[速くなる]", ["1分に70回が", "100回をこえることも"], fade(sec, 2.75, TL.T_VANISH + 0.01), y=HY, size=HS)
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


def thump(gain=1.0):
    """心臓の「ドクン」（低い2回の音）。フェロモン版の heartbeat を少し低く・太く。"""
    return PC.heartbeat() * gain


def shush(dur=0.9, seed=0):
    """図書館の「シーッ」。"""
    n = int(dur * SR)
    t = np.arange(n) / SR
    return SC.band(CC.noise(dur, seed), 2500, 7000) * np.minimum(1, t / 0.08) * np.clip((dur - t) / 0.2, 0, 1) * 0.5


def build_audio(total):
    st = {s["name"]: TL.start_of(s["name"]) for s in TL.SHOTS}
    a = np.zeros(int(total * SR) + SR)

    def put(x, at, gain=1.0):
        i = int(at * SR)
        j = min(len(a), i + len(x))
        if j > i and i >= 0:
            a[i:j] += gain * x[: j - i]

    put(CC.ambience(total), 0, 1.0)
    rng = np.random.default_rng(7)
    # 冒頭：人波（足音・すれちがい）＋時計のカチカチ → 5.6秒でドン＋ドクン
    put(SC.murmur(TL.T_VANISH + 1.0, 54), 0.0, 0.9)
    t0 = 0.05
    while t0 < TL.T_VANISH:
        put(SC.step(int(t0 * 997)), t0, rng.uniform(0.6, 1.0))
        t0 += rng.uniform(0.08, 0.13)
    for k, tt in enumerate((0.6, 1.9, 3.2, 4.4)):
        put(PC.pass_by(1.0, 72 + k), tt, 0.7)
    for k in range(1, 6):
        put(CC.tick(), TL.T_VANISH - k, 0.6)
    put(PC.impact(), TL.T_VANISH, 1.0)
    put(CC.sparkle(1, 1.6), TL.T_VANISH, 0.6)
    # 場面ごとの主役の心拍（輪と同じ時刻）
    for s in TL.SHOTS:
        name = s["name"]
        for t in BT.main_beats(name):
            put(thump(1.0), st[name] + t, 1.0 if name != "d08_home" else 0.55)
        if s.get("segs"):
            e0, sp = TL.e_of(s, 0)
            if sp > 50:
                for k, tt in enumerate(np.arange(0.25, s["frames"] / FPS - 0.1, 0.4)):
                    put(SC.clock(k), st[name] + tt, 0.5)
        if s.get("card"):
            put(CC.whoosh(0.9, hash(name) % 50), st[name] - 0.2, 0.7)
        for a0, b0, head, sub in s.get("captions", []):
            put(CC.pop(), st[name] + a0, 0.6)
    # まわりの人の心拍（小さく、ばらばらに）
    for name, n, g in (("d00_open", 25, 0.25), ("d01_burst", 40, 0.3), ("d02_train", 6, 0.25), ("d07_library", 20, 0.35)):
        s = TL.shot(name)
        t_from = TL.T_VANISH if name == "d00_open" else 0.0
        for k in range(n):
            b = rng.uniform(68, 92)
            for t in BT.beats(t_from, s["frames"] / FPS, lambda t, b=b: b, rng.uniform(0, 60 / b)):
                put(thump(1.0), st[name] + t, g * rng.uniform(0.5, 1.0))
    t = st["d01_burst"]
    put(SC.murmur(4.0, 56), t, 0.8)
    t = st["d02_train"]
    put(SC.rumble(5.0, 58, 0.5), t, 0.5)
    put(CC.sparkle(2, 1.4), t + 2.6, 0.5)
    t = st["d03_distance"]
    put(SC.rumble(4.5, 60, 0.3), t, 0.3)
    t = st["d04_meeting"]
    put(SC.murmur(1.5, 61), t + 2.4, 0.5)
    t = st["d05_bridge"]
    put(FC.wind(5.0, 62), t, 0.6)
    put(PC.deflate(0.8) * 0.0, t, 0.0)
    put(CC.sparkle(3, 1.2), t + 2.3, 0.5)
    t = st["d06_coaster"]
    for k in range(10):
        put(SC.clock(100 + k), t + 0.1 + 0.1 * k, 0.6)
    put(SC.rumble(4.0, 63, 0.8), t + 1.0, 1.0)
    put(FC.cheer(2.5, 64), t + 1.1, 0.7)
    put(CC.sparkle(4, 1.6), t + 3.2, 0.6)
    t = st["d07_library"]
    put(shush(1.0, 65), t + 1.8, 0.9)
    t = st["d08_home"]
    put(PC.piano([(262, 330, 392), 392, 440, 392, (349, 440, 523), 523, 494, 440, (330, 392, 523), 392, 440, 523, (349, 440, 587),
                  (392, 494, 587), (330, 392, 523)], dt=0.55, decay=1.0, amp=0.12), t + 0.6, 1.0)
    a = a / max(1e-6, np.abs(a).max()) * 0.8
    return a


PC.draw = draw
PC.build_audio = build_audio

if __name__ == "__main__":
    PC.main()
