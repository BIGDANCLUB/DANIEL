"""姫路城の作り方：場面ごとの時間（59.9秒）。ナレーションの時刻（voice/timing.json）から作る。"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
TOTAL = 59.9
# 場面名と頭の秒（ナレーションの区切りに合わせる）
CUTS = [("h01_house", 0.00), ("h02_stone", 6.20), ("h03_curve", 9.45), ("h04_fall", 15.38), ("h05_corner", 18.68),
        ("h06_gate", 25.07), ("h07_sama", 31.89), ("h08_cone", 37.66), ("h09_fire", 44.32), ("h10a_1609", 49.71),
        ("h10b_1945", 52.33), ("h10c_final", 55.00)]


def frames():
    """場面ごとの (頭のコマ（全体で0から）, コマ数)。合計 = 59.9秒 × 30 = 1797。"""
    total = int(round(TOTAL * FPS))
    starts = [int(round(t * FPS)) for _, t in CUTS] + [total]
    return {n: (starts[i], starts[i + 1] - starts[i]) for i, (n, _) in enumerate(CUTS)}


def scene(name):
    f0, nf = frames()[name]
    t0 = f0 / FPS
    tj = os.path.join(HERE, "voice", "timing.json")
    lines = []
    if os.path.exists(tj):
        for L in json.load(open(tj))["lines"]:
            lines.append(dict(L, t=L["start"] - t0, t_end=L["start"] - t0 + L["dur"]))
    return dict(name=name, f0=f0, nf=nf, t0=t0, dur=nf / FPS, lines=lines)
