"""「もしも電車の乗客が1駅ごとに2倍になったら？」の時間割（約56秒、30fps）。新幹線版と同じ構成。
x は発車してからの駅の数（小数）。乗客 N(x) = 2^x 人（最初は1人、1駅ごとに2倍。もしもの話）。
舞台は山手線（1周30駅）。人がぎゅうぎゅうに立つと 1㎡に4人として、人の広がりを円の半径で表す。"""
import math

FPS = 30
DENSITY = 4.0          # 1㎡に4人


def n(x):
    return 2 ** max(x, 0.0)


def radius(x):
    """乗客がぎゅうぎゅうに立ったときの円の半径（m）。"""
    return math.sqrt(n(x) / DENSITY / math.pi)


ORANGE, GREEN = "orange", "green"


def fast(t):
    return (f"早送り　1秒＝{t}駅", GREEN)


SLOW = ("リプレイ　1/10 スロー", ORANGE)


def slow_seg(x0, frames=120):
    return [(frames, x0, x0 + 0.5, SLOW)]


AERIAL = {"e03c_city", "e03d_wide", "e09_dome", "e10_tokyo", "e11_japan", "e12_loop", "e13_world", "e14_area", "e15_end"}

SHOTS = [
    dict(name="e01_open", frames=150, kind="open"),
    dict(name="e02_one", frames=45, segs=[(45, 0.0, 0.0, ("1/500 スロー", ORANGE))],
         note=(0, 1.5, "※乗客が1駅ごとに2倍になる、もしもの話です")),
    dict(name="e03a_car", frames=75, segs=[(75, 0.0, 10.0, fast(4))],
         note=(0, 2.5, "※乗客が1駅ごとに2倍になる、もしもの話です")),
    dict(name="e03b_platform", frames=60, segs=[(60, 10.0, 15.0, fast(5))]),
    dict(name="e03c_city", frames=60, segs=[(60, 15.0, 25.0, fast(10))]),
    dict(name="e03d_wide", frames=60, segs=[(60, 25.0, 33.0, fast(8))]),
    dict(name="e05_rewind", frames=21, kind="rewind"),
    dict(name="e06_five", frames=120, segs=slow_seg(4.5),
         captions=[(0.3, 4.0, ["5駅目で32人。", "ここまでは、いつもの車内"])]),
    dict(name="e07_ten", frames=120, segs=slow_seg(9.5),
         captions=[(0.3, 4.0, ["10駅目で1024人。", "1両に約93人のすし詰め"])]),
    dict(name="e08_full", frames=120, segs=slow_seg(12.5),
         captions=[(0.3, 4.0, ["13駅目で8192人。", "1両に約740人。もう乗れない"])]),
    dict(name="e09_dome", frames=120, segs=slow_seg(15.5),
         captions=[(0.3, 4.0, ["16駅目で6万5536人。", "東京ドームの満員より多い"])]),
    dict(name="e10_tokyo", frames=120, segs=slow_seg(23.5),
         captions=[(0.3, 4.0, ["24駅目で1677万人。", "東京都の人口を超えた"])],
         info=("人口", [(0.5, (235, 235, 240), "東京都　約1429万人", (255, 255, 255)),
                       (1.4, None, "24駅目　約1677万人", (240, 150, 70))])),
    dict(name="e11_japan", frames=120, segs=slow_seg(26.5),
         captions=[(0.3, 4.0, ["27駅目で1億3421万人。", "日本の人口を超えた"])],
         info=("人口", [(0.5, (235, 235, 240), "日本　約1億2268万人", (255, 255, 255)),
                       (1.4, None, "27駅目　約1億3421万人", (240, 150, 70))])),
    dict(name="e12_loop", frames=120, segs=slow_seg(29.5),
         captions=[(0.3, 4.0, ["山手線を1周（30駅）で、", "10億7374万人"])],
         info=("1駅ごとに2倍の乗客", [(0.4, None, "0駅　　1人", (255, 255, 255)),
                                     (1.0, None, "10駅　 1024人", (255, 255, 255)),
                                     (1.6, None, "20駅　 約105万人", (255, 255, 255)),
                                     (2.2, None, "30駅　 約10.7億人", (240, 150, 70))])),
    dict(name="e13_world", frames=120, segs=slow_seg(32.5),
         captions=[(0.3, 4.0, ["33駅目で約86億人。", "世界の人口を超えた"])]),
    dict(name="e14_area", frames=120, segs=[(120, 33.0, 33.0, SLOW)],
         captions=[(0.3, 4.0, ["ぎゅうぎゅうに立つと、", "東京都とほぼ同じ広さ"])],
         info=("1㎡に4人で立つと", [(0.5, None, "約86億人　約2150㎢", (255, 255, 255)),
                                    (1.4, (235, 235, 240), "東京都　約2194㎢", (240, 150, 70))])),
    dict(name="e15_end", frames=120, segs=[(120, 33.0, 33.0, fast(8))],
         captions=[(0.4, 4.0, ["最初はたった1人。", "山手線1周と3駅で、世界中の人が乗った"])]),
]


def shot(name):
    return next(s for s in SHOTS if s["name"] == name)


def t_of(s, i):
    k = 0
    for nn, a, b, tag in s["segs"]:
        if i < k + nn:
            return a + (b - a) * (i - k) / nn, tag
        k += nn
    nn, a, b, tag = s["segs"][-1]
    return b, tag


def total_frames():
    return sum(s["frames"] for s in SHOTS)
