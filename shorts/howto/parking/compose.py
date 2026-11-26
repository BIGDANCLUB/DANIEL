"""「立体駐車場の作り方」の合成（共通の hcompose を使う）。左上の PARKING KIT、右上の駐車場の満空表示（満車／混雑／空車）、白い輪、効果音。
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

BGM = os.path.join(HERE, "..", "..", "bgm", "howto_parking.wav")
KIT_TITLE = "PARKING KIT"
KIT = [(LT(1) + 0.4, "白い線"), (LT(6) + 0.6, "鉄骨の床"), (LT(12) + 0.6, "坂道17%"), (LT(17) + 1.0, "エレベーター"), (LT(22), "ターンテーブル"),
       (LT(25) + 0.8, "三角の鉄骨"), (LT(29) + 1.2, "光のセンサー"), (LT(31) + 1.0, "料金所と看板")]
SCOPE = "gauge"
SCOPE_TITLE = "PARKING"
ST_COL = {"満車": (235, 40, 40), "混雑": (255, 170, 20), "空車": (40, 200, 90)}
ST_LEVEL = {"満車": 2, "混雑": 1, "空車": 0}
STATUS = [(0.0, "空車"), (LT(2) + 0.6, "混雑"), (LT(4), "満車"), (LT(6) + 0.5, "空車"), (LT(8), "満車"), (LT(9) + 0.3, "空車"),
          (LT(10), "混雑"), (LT(12) + 0.5, "空車"), (LT(15), "満車"), (LT(17) + 0.8, "空車"), (LT(20), "混雑"), (LT(21) + 1.0, "空車"),
          (LT(24), "満車"), (LT(25) + 1.0, "空車"), (LT(27) + 0.5, "混雑"), (LT(29) + 1.2, "空車"), (LT(33), None)]
RINGS = [("s01_drill", "full", LT(4), LE(4) + 0.2), ("s03_ramp", "car", LT(8) + 0.4, LE(8) + 0.3), ("s05_turn", "car", LT(20), LE(20) + 0.2),
         ("s07_sensor", "hero", LT(28) - 0.2, LE(28) + 0.4)]
OVER = [(l["start"], (T.lines[i + 1]["start"] if i + 1 < len(T.lines) else T.TOTAL), l["over"]) for i, l in enumerate(T.lines) if l.get("over")]


def drill_whine(dur, f=210.0, seed=0):
    """電動ドリルの「ウィィーン」：モーターのうなり（倍音の多い音）＋けずる音。"""
    n = int(dur * SR)
    t = np.arange(n) / SR
    ff = f * (1 + 0.25 * np.minimum(1, t / 0.15)) * (1 + 0.01 * np.sin(2 * np.pi * 7 * t))
    ph = 2 * np.pi * np.cumsum(ff) / SR
    x = sum(np.sin(k * ph) / k for k in range(1, 9)) * 0.35
    x += HC.hp_fast(HC.noise(dur, seed), 2500) * 0.25
    env = np.minimum(1, t / 0.04) * np.clip((dur - t) / 0.12, 0, 1)
    return x * env


def horn(seed=0):
    """車のクラクション「プーッ」。"""
    dur = 0.55
    t = np.arange(int(dur * SR)) / SR
    x = sum(np.sign(np.sin(2 * np.pi * f * t)) * 0.3 for f in (415, 523))
    x = HC.lp_fast(x, 2500)
    return x * np.minimum(1, t / 0.02) * np.clip((dur - t) / 0.05, 0, 1) * 0.6


def beeps(n=4, f=1000.0, on=0.12, off=0.12):
    """バックの「ピーッ ピーッ」・警告音。"""
    out = []
    for _ in range(n):
        t = np.arange(int(on * SR)) / SR
        out.append(np.sin(2 * np.pi * f * t) * np.minimum(1, t / 0.005) * np.clip((on - t) / 0.01, 0, 1) * 0.4)
        out.append(np.zeros(int(off * SR)))
    return np.concatenate(out)


def buzzer(dur=0.5):
    """だめの「ブーッ」。"""
    t = np.arange(int(dur * SR)) / SR
    x = np.sign(np.sin(2 * np.pi * 130 * t)) * 0.3
    return HC.lp_fast(x, 1500) * np.minimum(1, t / 0.01) * np.clip((dur - t) / 0.05, 0, 1)


def sfx(put, TL):
    st = {n: t for n, t in TL.CUTS}
    # 1) ドリル（最初の 1.7秒）、線がシュッ、車が入る、満車でクラクション
    put(HC.thud(1, 60, 0.4), 0.05, 0.8)
    put(drill_whine(LT(1) - 0.15, 210, 1), 0.08, 1.0)
    put(HC.ticks(LT(1) - 0.2, 26, 2), 0.1, 0.5)
    for k in range(10):
        put(HC.fwip(10 + k), LT(1) + 0.04 * k * 2, 0.35)
    put(HC.roar(1.8, 3) * 0.5, LT(2) - 0.2, 0.5)
    for k in range(10):
        put(HC.clack(20 + k) * 0.4, LT(2) + 0.6 + 0.1 * k, 0.3)
    put(HC.ding(), LT(2) + 0.9, 0.7)
    put(HC.rumble(2.0, 4) * 0.4, LT(3), 0.4)
    put(horn(1), LT(4) + 0.2, 0.8)
    put(horn(2), LT(4) + 0.9, 0.6)
    put(buzzer(0.45), LT(4) + 0.05, 0.5)
    # 2) 柱がのびる、床がドン×3
    put(HC.rumble(1.2, 5), st["s02_floors"] + 0.15, 0.8)
    put(HC.creak(6, 0.6), st["s02_floors"] + 0.4, 0.5)
    for k in range(3):
        put(HC.thud(7 + k, 55, 0.6), LT(6) + 0.05 + 0.35 * k + 0.2, 1.0)
        put(HC.clack(30 + k), LT(6) + 0.05 + 0.35 * k + 0.2, 0.6)
    for k in range(12):
        put(HC.clack(40 + k) * 0.5, LT(6) + 0.6 + 0.08 * k, 0.3)
    put(HC.ding(), LT(7), 0.8)
    # 3) 坂道：のぼれない → 急な坂でガリガリ → 17% → 18m → 上がる
    put(HC.roar(1.2, 8) * 0.5, LT(8), 0.5)
    put(horn(3), LT(8) + 1.2, 0.6)
    put(HC.whoosh(0.5, 9), LT(9) + 0.05, 0.6)
    put(HC.thud(10, 70, 0.5), LT(9) + 0.55, 0.8)
    put(HC.roar(1.4, 11) * 0.6, LT(10) + 0.2, 0.6)
    put(HC.hp_fast(HC.noise(1.8, 12), 1800) * np.linspace(1, 0.3, int(1.8 * SR)) * 0.5, LT(10) + 1.05, 0.9)   # ガリガリ
    put(buzzer(0.4), LT(11) + 0.4, 0.4)
    put(HC.whoosh(0.7, 13), LT(12) - 0.1, 0.6)
    put(HC.ding(), LT(12) + 0.6, 0.8)
    put(HC.swish(1.0, 14), LT(13) + 0.2, 0.5)
    put(HC.roar(2.0, 15) * 0.5, LT(14) - 0.6, 0.5)
    put(HC.ding(), LT(14), 0.8)
    # 4) 半分も使う（ブーッ）→ 片づく → タワーが立ち上がる、エレベーター
    put(buzzer(0.5), LT(15) + 0.4, 0.6)
    put(HC.whoosh(0.6, 16), LT(16), 0.7)
    put(HC.thud(17, 50, 0.7), LT(16) + 0.6, 0.8)
    put(HC.rumble(1.4, 18), LT(17) - 0.4, 1.0)
    put(HC.hum(LE(18) - LT(17), 90, 19), LT(17) + 0.5, 0.4)
    put(HC.ding(), LT(18), 0.8)
    put(HC.cheer(1.6, 20), LT(18) + 0.2, 0.3)
    # 5) 奥まで入る → バックのピーッ・道路を車がビュン → 床が回る
    put(HC.roar(1.2, 21) * 0.5, LT(19), 0.5)
    put(beeps(5, 1000), LT(20) + 0.2, 0.6)
    put(HC.whoosh(1.0, 22), LT(20) + 0.6, 0.7)
    put(HC.hum(1.5, 70, 23), LT(21) + 0.2, 0.5)
    put(HC.clack(24), LT(21) + 1.6, 0.6)
    put(HC.ding(), LT(22), 0.8)
    # 6) ドスン（1.5トン）→ 車がどんどん → ギシギシ → 鉄骨カンカン → 押す
    put(HC.thud(25, 45, 0.8), LT(23) + 0.6, 1.0)
    for k in range(24):
        put(HC.clack(50 + k) * 0.35, LT(24) - 0.2 + 0.05 * k, 0.3)
    put(HC.creak(26, 0.8), LT(24) + 0.6, 0.7)
    put(HC.creak(27, 0.8), LT(24) + 1.3, 0.6)
    for k in range(10):
        put(HC.bang(60 + k) * 0.4, LT(25) + 0.1 + 0.07 * k, 0.4)
    put(HC.ding(), LT(25) + 1.1, 0.8)
    put(HC.swish(0.8, 28), LT(26) + 0.2, 0.5)
    put(HC.creak(29, 0.6), LT(26) + 0.5, 0.6)
    # 7) 回転灯ピーポー → はさまれる → 光のセンサーで止まる
    put(beeps(6, 880, 0.15, 0.15), LT(27) + 0.6, 0.5)
    put(HC.hum(2.4, 70, 30), LT(27) + 0.6, 0.4)
    put(HC.roar(0.6, 31) * 0.4, LT(28), 0.5)
    put(HC.swish(0.6, 32), LT(29) + 0.2, 0.4)
    put(beeps(2, 1500, 0.08, 0.06), LT(29) + 1.1, 0.7)
    put(HC.thud(33, 80, 0.4), LT(29) + 1.1, 0.7)
    put(HC.ding(), LT(30), 0.8)
    # 8) ポンポン（料金所・バー・看板）→ 最後のドリル → 完成の歓声
    for k, dt in enumerate((0.3, 0.4, 0.8)):
        put(HC.thud(40 + k, 110, 0.3), LT(31) + dt, 0.6)
    put(drill_whine(LT(33) - 0.15 - LT(32), 210, 41), LT(32), 1.0)
    put(HC.ticks(LT(33) - 0.2 - LT(32), 24, 42), LT(32), 0.4)
    put(HC.cheer(2.6, 43), LT(33) - 0.05, 0.6)
    put(HC.ding(), LT(33) - 0.05, 0.9)


if __name__ == "__main__":
    HC.main(sys.modules[__name__], HERE)
