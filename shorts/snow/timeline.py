"""「もしも日本中の雪が毎日2倍に積もったら？」の時間割（約58秒、30fps）。新幹線版と同じ構成。
t は降り始めからの日数。積雪 h(t) = 1cm × 2^t（降り始めに1cm、毎日2倍になる、もしもの話）。"""
FPS = 30


def h(t):
    """積雪（m）。"""
    return 0.01 * 2 ** max(t, 0.0)


ORANGE, GREEN = "orange", "green"
SLOW_DAYS = 4.0 * 20000 / 86400          # 4秒のスロー（1/20000）で進む日数


def fast(n):
    return (f"早送り　1秒＝{n}日", GREEN)


SLOW = ("リプレイ　1/20000 スロー", ORANGE)


def slow_seg(t0, frames=120):
    return [(frames, t0, t0 + SLOW_DAYS * frames / 120, SLOW)]


SPACE = {"n03e_space", "n12_space100", "n13_space30", "n14_moon", "n15_end"}

SHOTS = [
    dict(name="n01_open", frames=150, kind="open"),
    dict(name="n02_flake", frames=45, segs=[(45, 0.0, 0.0104, ("1/20000 スロー", ORANGE))],
         note=(0, 1.5, "※日本中の積雪が毎日2倍になる、もしもの話です")),
    dict(name="n03a_village", frames=75, segs=[(75, 0.0, 9.0, fast(4))],
         note=(0, 2.5, "※日本中の積雪が毎日2倍になる、もしもの話です")),
    dict(name="n03b_town", frames=60, segs=[(60, 9.0, 13.0, fast(2))]),
    dict(name="n03c_tokyo", frames=60, segs=[(60, 13.0, 17.0, fast(2))]),
    dict(name="n03d_fuji", frames=60, segs=[(60, 17.0, 20.0, fast(2))]),
    dict(name="n03e_space", frames=75, segs=[(75, 20.0, 36.0, fast(6))]),
    dict(name="n05_rewind", frames=21, kind="rewind"),
    dict(name="n06_winter", frames=120, segs=slow_seg(6.0),
         captions=[(0.3, 4.0, ["6日で64cm。", "ここまでは、雪国のふつうの冬"])]),
    dict(name="n07_house", frames=120, segs=slow_seg(7.9),
         captions=[(0.3, 4.0, ["8日で2.5m。", "家の1階が雪に埋まった"])]),
    dict(name="n08_record", frames=120, segs=slow_seg(10.2),
         captions=[(0.3, 4.0, ["10日半で11.8m。", "伊吹山の世界記録を超えた"])],
         info=("積雪の世界記録", [(0.5, (235, 235, 240), "伊吹山　11.82m", (255, 255, 255)),
                                (1.4, None, "1927年2月14日", (240, 150, 70))])),
    dict(name="n09_town", frames=120, segs=slow_seg(11.6),
         captions=[(0.3, 4.0, ["12日で41m。", "電柱も信号機も、雪の下"])]),
    dict(name="n10_tokyo", frames=120, segs=slow_seg(15.5),
         captions=[(0.3, 4.0, ["16日で655m。", "スカイツリー（634m）が見えなくなった"])]),
    dict(name="n11_fuji", frames=120, segs=slow_seg(18.1),
         captions=[(0.3, 4.0, ["18日半で3776m。", "富士山が雪に沈んだ"])]),
    dict(name="n12_space100", frames=120, segs=slow_seg(22.8),
         captions=[(0.3, 4.0, ["23日で100km。", "雪の表面が、宇宙に届いた"])]),
    dict(name="n13_space30", frames=120, segs=slow_seg(28.6),
         captions=[(0.3, 4.0, ["29日で5000km超。", "地球の半径に迫る高さに"])],
         info=("毎日2倍の積雪", [(0.4, None, "0日　　1cm", (255, 255, 255)),
                                (1.0, None, "10日　 10m", (255, 255, 255)),
                                (1.6, None, "20日　 10km", (255, 255, 255)),
                                (2.2, None, "30日　 1万km", (240, 150, 70))])),
    dict(name="n14_moon", frames=120, segs=slow_seg(34.8),
         captions=[(0.3, 4.0, ["35日で38万km。", "雪の山が、月まで届いた"])]),
    dict(name="n15_end", frames=120, segs=[(120, 36.0, 36.0, fast(6))],
         captions=[(0.4, 4.0, ["最初はたった1cm。", "毎日2倍は、それほど恐ろしい"])]),
]


def shot(name):
    return next(s for s in SHOTS if s["name"] == name)


def t_of(s, i):
    k = 0
    for n, a, b, tag in s["segs"]:
        if i < k + n:
            return a + (b - a) * (i - k) / n, tag
        k += n
    n, a, b, tag = s["segs"][-1]
    return b, tag


def total_frames():
    return sum(s["frames"] for s in SHOTS)
