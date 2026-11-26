"""心臓の拍の時刻（3D の輪と、合成の「ドクン」の音で同じものを使う）。
bpm_fn(t) → その時刻の1分あたりの拍。beats(t0, t1, bpm_fn, phase) → 拍の時刻のリスト（秒）。"""


def beats(t0, t1, bpm_fn, phase=0.0):
    out = []
    t = t0 + phase
    while t < t1:
        out.append(t)
        t += 60.0 / max(20.0, bpm_fn(t))
    return out


def ramp(a, b, t_a, t_b):
    """t_a〜t_b で a → b に変わる bpm。"""
    def f(t):
        if t <= t_a:
            return a
        if t >= t_b:
            return b
        return a + (b - a) * (t - t_a) / (t_b - t_a)
    return f


# 場面ごとの主役の心拍（場面の中の秒）。音（合成）と輪（3D）の両方で使う。
MAIN = {
    "d00_open": (5.6, 7.0, ramp(80, 95, 5.6, 7.0)),
    "d01_burst": (0.0, 4.0, ramp(95, 85, 0.0, 4.0)),
    "d02_train": (0.0, 5.0, ramp(72, 125, 1.4, 2.6)),
    "d03_distance": (0.0, 4.5, ramp(120, 110, 0.0, 4.5)),
    "d04_meeting": (0.0, 5.0, ramp(80, 130, 1.0, 3.5)),
    "d05_bridge": (0.0, 5.0, ramp(95, 125, 0.0, 2.5)),
    "d06_coaster": (0.0, 5.0, ramp(100, 150, 1.0, 2.2)),
    "d07_library": (0.0, 4.0, ramp(75, 75, 0, 1)),
    "d08_home": (0.0, 8.0, ramp(66, 62, 0.0, 8.0)),
}


def main_beats(scene):
    if scene not in MAIN:
        return []
    t0, t1, f = MAIN[scene]
    return beats(t0, t1, f)
