"""姫路城の作り方：場面ごとの時間（59.9秒）。ナレーションの時刻（voice/timing.json）から作る。

v3（2026-11-22）：声を参考元と同じ速さ（1秒に約8.8モーラ）にして、参考元の言い回しを足した（41行）。
場面の中の動き（film.py）と効果音（compose.py）は v2 の時刻で書いてあるので、WARP で v2 の時刻 → v3 の時刻に伸び縮みさせる。"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
TOTAL = 59.9
# 場面名と頭の秒（ナレーションの区切りに合わせる。各場面の最初の句の 約0.05秒前）
CUTS = [("h01_house", 0.00), ("h02_stone", 5.25), ("h03_curve", 8.06), ("h04_fall", 13.10), ("h05_corner", 15.92),
        ("h06_gate", 26.18), ("h07_sama", 33.22), ("h08_cone", 38.47), ("h09_fire", 46.49), ("h10a_1609", 51.10),
        ("h10b_1945", 53.30), ("h10c_final", 55.50)]

# ---------- v2（前の版）の時刻 ----------
OLD_CUTS = [("h01_house", 0.00), ("h02_stone", 6.20), ("h03_curve", 9.45), ("h04_fall", 15.38), ("h05_corner", 18.68),
            ("h06_gate", 25.07), ("h07_sama", 31.89), ("h08_cone", 37.66), ("h09_fire", 44.32), ("h10a_1609", 49.71),
            ("h10b_1945", 52.33), ("h10c_final", 55.00)]
# v2 の35行の (はじまり, 長さ)
OLD_LINES = [(0.25, 1.666), (1.976, 1.188), (3.223, 1.556), (4.839, 1.348), (6.247, 0.453), (6.761, 1.741), (8.562, 0.884),
             (9.506, 1.102), (10.668, 1.446), (12.174, 1.473), (13.707, 1.639), (15.406, 1.825), (17.291, 1.388), (18.738, 1.924),
             (20.722, 1.67), (22.452, 1.328), (23.84, 1.282), (25.182, 1.965), (27.208, 1.193), (28.461, 1.395), (29.916, 2.041),
             (32.017, 1.513), (33.59, 1.892), (35.541, 2.163), (37.764, 1.716), (39.54, 1.71), (41.31, 3.05), (44.42, 1.978),
             (46.459, 2.232), (48.751, 1.017), (49.828, 2.538), (52.426, 2.581), (55.067, 1.026), (56.153, 0.726), (56.939, 1.568)]
# v2 の行 → v3 の行（同じ内容の句）
OLD2NEW = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17, 19, 20, 22, 23, 24, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38,
           39, 40]
# 場面の中で、v2 の時刻を v3 のどこへ合わせるかを足す（行の頭どうしの対応のほかに）。値は (v2 の場面内の秒, v3 の行, その行の頭からの秒)
EXTRA = {
    # 角：走って集まる → 「必死に登り始めます」で登る
    "h05_corner": [(1.3, 14, -0.5)],
}
# 行の対応を場面ごとに変える：{場面: {v2 の行: (v3 の行, その行の頭からの秒)}}
LINE_OVERRIDE = {
    # 櫓は「だから角の真上に」の終わりごろから組み上がる。石は「真下へ石を落とせます」で落ちる
    "h05_corner": {14: (15, 0.45), 16: (18, 0.0)},
}
# 場面の中の動きを v2 の終わりより先まで続ける（v3 で場面が長くなったところ）。値は v2 の時刻で考えた場面の長さ
OLD_DUR_EXT = {"h05_corner": 7.6}


def frames(cuts=None):
    """場面ごとの (頭のコマ（全体で0から）, コマ数)。合計 = 59.9秒 × 30 = 1797。"""
    cuts = cuts or CUTS
    total = int(round(TOTAL * FPS))
    starts = [int(round(t * FPS)) for _, t in cuts] + [total]
    return {n: (starts[i], starts[i + 1] - starts[i]) for i, (n, _) in enumerate(cuts)}


def new_lines():
    tj = os.path.join(HERE, "voice", "timing.json")
    return json.load(open(tj))["lines"]


def _span(cuts, name):
    names = [n for n, _ in cuts]
    i = names.index(name)
    t0 = cuts[i][1]
    t1 = cuts[i + 1][1] if i + 1 < len(cuts) else TOTAL
    return t0, t1


def scene_anchors(name, extend=True):
    """場面の中の (v2 の秒, v3 の秒) の対応（場面の頭からの秒）。"""
    NL = new_lines()
    o0, o1 = _span(OLD_CUTS, name)
    n0, n1 = _span(CUTS, name)
    od = OLD_DUR_EXT.get(name, o1 - o0) if extend else o1 - o0
    an = [(0.0, 0.0)]
    ov = LINE_OVERRIDE.get(name, {})
    for i, (s, _) in enumerate(OLD_LINES):
        if o0 <= s < o1:
            j, dt = ov.get(i, (OLD2NEW[i], 0.0))
            an.append((s - o0, NL[j]["start"] + dt - n0))
    for (ot, li, dt) in EXTRA.get(name, []):
        an.append((ot, NL[li]["start"] + dt - n0))
    if name == "h05_corner":
        # 石が落ちてから 1.2秒（v2）→ 「真下へ石を落とせます」の頭から 1.25秒（v3）
        d = OLD_LINES[16][0] - o0
        an.append((d + 1.2, NL[18]["start"] + 1.25 - n0))
    if name == "h08_cone":
        # 「穴は内側が広く外側が狭い」（v3 で足した句）のあいだは、v2 の最初の一瞬をゆっくり見せる（film.py で新しい動きを足す）
        an.append((0.06, NL[29]["start"] - n0))
    an.append((od, n1 - n0))
    an = sorted(an)
    for (a, b), (c, d) in zip(an, an[1:]):
        assert c > a and d > b, (name, an)
    return an


def warp(an, t):
    """v2 の秒 → v3 の秒（区分ごとの直線。外は傾き1）。"""
    if t <= an[0][0]:
        return an[0][1] + (t - an[0][0])
    for (a, b), (c, d) in zip(an, an[1:]):
        if t <= c:
            return b + (t - a) * (d - b) / (c - a)
    return an[-1][1] + (t - an[-1][0])


def unwarp(an, t):
    return warp([(b, a) for a, b in an], t)


def global_anchors():
    """全体の (v2 の秒, v3 の秒)。効果音・左上のリストなどを v2 の時刻のまま v3 へ写す。"""
    an = []
    for (name, o0), (_, n0) in zip(OLD_CUTS, CUTS):
        for a, b in scene_anchors(name, extend=False):
            an.append((o0 + a, n0 + b))
    an.append((TOTAL, TOTAL))
    out = []
    for a, b in sorted(an):
        if not out or (a > out[-1][0] + 1e-6 and b > out[-1][1] + 1e-6):
            out.append((a, b))
    return out


def scene(name):
    f0, nf = frames()[name]
    t0 = f0 / FPS
    lines = []
    tj = os.path.join(HERE, "voice", "timing.json")
    if os.path.exists(tj):
        for L in json.load(open(tj))["lines"]:
            lines.append(dict(L, t=L["start"] - t0, t_end=L["start"] - t0 + L["dur"]))
    o0, o1 = _span(OLD_CUTS, name)
    return dict(name=name, f0=f0, nf=nf, t0=t0, dur=nf / FPS, lines=lines, old_t0=o0, old_dur=OLD_DUR_EXT.get(name, o1 - o0),
                anchors=scene_anchors(name))
