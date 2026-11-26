"""「いかだの作り方」の合成（共通の hcompose を使う）。左上の RAFT KIT、右上の航海の計器（危険／注意／安全）、白い輪、効果音。
usage: python3 compose.py frames_root out.mp4   → 59.9秒ちょうど"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import hcompose as HC  # noqa: E402
from htimeline import Timeline  # noqa: E402

T = Timeline(HERE)
LT, LE = T.LT, T.LE
SR = HC.SR

BGM = os.path.join(HERE, "..", "..", "bgm", "howto_raft.wav")
KIT_TITLE = "RAFT KIT"
KIT = [(LT(1) + 0.8, "縄"), (LT(5) + 1.0, "バルサ"), (LT(10), "アウトリガー"), (LT(15) + 0.6, "木の棒"), (LT(19), "舵"), (LT(21) + 0.6, "帆"),
       (LT(27), "センターボード"), (LT(33) - 0.2, "帆柱")]
SCOPE = "gauge"
SCOPE_TITLE = "VOYAGE"
ST_COL = {"危険": (235, 40, 40), "注意": (255, 170, 20), "安全": (40, 200, 90)}
ST_LEVEL = {"危険": 2, "注意": 1, "安全": 0}
STATUS = [(0.0, "安全"), (LT(3), "注意"), (LT(4), "危険"), (LT(5) + 1.0, "安全"), (LT(7), "注意"), (LT(8), "危険"), (LT(10), "安全"),
          (LT(12), "注意"), (LT(13), "危険"), (LT(15) + 0.6, "安全"), (LT(16), "注意"), (LT(19), "安全"), (LT(20), "注意"), (LT(22), "安全"),
          (LT(23), "注意"), (LT(26) + 0.5, "安全"), (LT(28), None), (LT(32), "安全")]
RINGS = [("s01_drill", "hero", LT(4), LE(4) + 0.2), ("s03_outrigger", "hero", LT(8) + 0.3, LE(8) + 0.4)]
OVER = [(l["start"], (T.lines[i + 1]["start"] if i + 1 < len(T.lines) else T.TOTAL), l["over"]) for i, l in enumerate(T.lines) if l.get("over")]


def drill_whine(dur, f=180.0, seed=0):
    """電動ドリルの「ウィィーン」（木をけずる音つき）。"""
    n = int(dur * SR)
    t = np.arange(n) / SR
    ff = f * (1 + 0.25 * np.minimum(1, t / 0.15)) * (1 + 0.01 * np.sin(2 * np.pi * 7 * t))
    ph = 2 * np.pi * np.cumsum(ff) / SR
    x = sum(np.sin(k * ph) / k for k in range(1, 9)) * 0.35
    x += HC.lp_fast(HC.hp_fast(HC.noise(dur, seed), 600), 4000) * 0.3
    return x * np.minimum(1, t / 0.04) * np.clip((dur - t) / 0.12, 0, 1)


def splash(dur=0.8, seed=0):
    """水しぶき「バシャッ」。"""
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = HC.lp_fast(HC.noise(dur, seed), 3500) * np.exp(-t / 0.18) * np.minimum(1, t / 0.01)
    return x * 0.9


def bubbles(dur=1.2, seed=0):
    """ブクブク（沈む）。"""
    r = np.random.default_rng(seed)
    out = np.zeros(int(dur * SR))
    for _ in range(int(dur * 14)):
        t0 = r.uniform(0, dur - 0.08)
        n = int(0.06 * SR)
        tt = np.arange(n) / SR
        f = r.uniform(300, 700) * (1 + 3 * tt / 0.06)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.02) * 0.3
        i = int(t0 * SR)
        out[i:i + n] += x
    return out


def buzzer(dur=0.5):
    t = np.arange(int(dur * SR)) / SR
    x = np.sign(np.sin(2 * np.pi * 130 * t)) * 0.3
    return HC.lp_fast(x, 1500) * np.minimum(1, t / 0.01) * np.clip((dur - t) / 0.05, 0, 1)


def sfx(put, TL):
    st = {n: t for n, t in TL.CUTS}
    # 1) ドリルで丸太に穴（最初の 1.7秒）→ 縄でしばる → 海へ → ブクブク
    put(HC.thud(1, 70, 0.4), 0.05, 0.7)
    put(drill_whine(LT(1) - 0.15, 180, 1), 0.08, 1.0)
    put(HC.ticks(LT(1) - 0.2, 22, 2), 0.1, 0.4)
    for k in range(7):
        put(HC.clack(10 + k) * 0.6, LT(1) + 0.05 + 0.07 * k, 0.5)
    for k in range(6):
        put(HC.fwip(20 + k), LT(1) + 0.7 + 0.06 * k, 0.4)
    put(HC.whoosh(0.8, 3), LT(2) - 0.1, 0.6)
    put(splash(0.9, 4), LT(2) + 0.7, 1.0)
    put(HC.ding(), LT(2) + 0.9, 0.7)
    put(bubbles(1.6, 5), LT(3) + 0.3, 0.8)
    put(splash(0.5, 6), LT(3) + 0.4, 0.5)
    put(buzzer(0.45), LT(4) + 0.1, 0.5)
    # 2) バルサに替わる（ポン）→ 浮く
    put(HC.thud(7, 120, 0.3), LT(5) + 0.85, 0.6)
    put(HC.swish(0.6, 8), LT(5) + 0.9, 0.5)
    put(HC.ding(), LT(6) + 0.2, 0.8)
    # 3) 大波 → ザバーン → アウトリガー → また波（ゆれて戻る）→ 南の島
    put(HC.roar(1.8, 9), LT(7) + 0.1, 0.7)
    put(splash(1.2, 10), LT(8) + 0.5, 1.0)
    put(HC.thud(11, 120, 0.3), LT(9) + 0.05, 0.6)
    put(HC.roar(1.4, 12), LT(10) - 0.4, 0.5)
    put(HC.ding(), LT(10), 0.8)
    put(HC.swish(1.2, 13), LT(11), 0.4)
    # 4) 縄がギシギシ → ブチッ → 横からドリル → 棒がスッ・コン
    put(HC.creak(14, 0.8), LT(12) + 0.2, 0.6)
    put(splash(0.5, 15), LT(12) + 0.3, 0.4)
    for k in range(3):
        put(HC.bang(16 + k) * 0.6, LT(13) + 0.05 * k, 0.7)
    put(drill_whine(LT(15) - 0.1 - LT(14), 180, 17), LT(14), 0.9)
    put(HC.swish(0.5, 18), LT(15) + 0.1, 0.5)
    put(HC.clack(19), LT(15) + 0.8, 0.8)
    put(HC.clack(20), LT(15) + 0.9, 0.7)
    put(HC.ding(), LT(15) + 0.9, 0.7)
    # 5) 流される（ザー）→ 舵（ポン）→ ギィッと曲がる
    put(HC.swish(2.0, 21), LT(16), 0.5)
    put(HC.thud(22, 120, 0.3), LT(17) + 0.3, 0.6)
    put(HC.creak(23, 0.6), LT(18) + 0.1, 0.6)
    put(HC.ding(), LT(19), 0.8)
    # 6) パシャパシャこぐ → 帆がバサッ → 風でビューッ
    for k in range(int((LT(21) - LT(20)) / 0.4)):
        put(splash(0.25, 30 + k) * 0.5, LT(20) - 0.1 + 0.4 * k, 0.4)
    put(HC.fwip(40), LT(21) + 0.3, 0.8)
    put(HC.whoosh(0.8, 41), LT(21) + 0.5, 0.6)
    put(HC.roar(2.0, 42) * 0.5, LT(22), 0.5)
    # 7) 横風 → 板を差しこむ（スッ×3、ポチャン）→ 止まる
    put(HC.roar(1.8, 43) * 0.5, LT(23), 0.6)
    for k in range(3):
        put(HC.fwip(44 + k), LT(25) + 0.2 * k, 0.6)
        put(splash(0.3, 47 + k) * 0.6, LT(25) + 0.2 * k + 0.4, 0.5)
    put(HC.swish(1.2, 50), LT(26), 0.5)
    put(HC.ding(), LT(27), 0.8)
    # 8) 実話：ドン（1947年）→ 線がのびる（カチカチ）→ 到着
    put(HC.thud(51, 60, 0.6), LT(28), 0.8)
    put(HC.roar(1.4, 52) * 0.4, LT(29), 0.4)
    put(HC.ticks(LT(31) + 0.4 - LT(30), 10, 53), LT(30), 0.4)
    put(HC.ding(), LT(31) + 0.4, 0.8)
    put(HC.cheer(1.4, 54), LT(31) + 0.5, 0.3)
    # 9) 最後のドリル → 完成の歓声
    put(drill_whine(LT(33) - 0.1 - LT(32), 180, 55), LT(32) + 0.05, 1.0)
    put(HC.ticks(LT(33) - 0.2 - LT(32), 20, 56), LT(32) + 0.05, 0.4)
    put(HC.cheer(2.4, 57), LT(33) - 0.05, 0.6)
    put(HC.ding(), LT(33) - 0.05, 0.9)
    _ = st


if __name__ == "__main__":
    HC.main(sys.modules[__name__], HERE)
