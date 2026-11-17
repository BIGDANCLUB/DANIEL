"""「もしも電車の乗客が1駅ごとに2倍になったら？」の時間割（約51秒、30fps）。巻き戻しなしで、だんだん増えていく。
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
FAST = ("早送り", GREEN)
STOP = ("一時停止", ORANGE)

# 床板（屋根の上の乗り場）：11両で長さ約225m。乗客は 1㎡に4人。
TRAIN_L = 225.0
DECK_START = 13.0     # 13駅目で車内がいっぱい → 屋根に床板


def deck_area(x):
    """床板の上に乗る人の広さ（㎡）。車内に乗りきれない分。"""
    return max(0.0, n(x) - 8192) / DENSITY


def deck_size(x):
    """床板の (幅, 長さ) m。最初は電車の長さのまま幅だけ広がり、幅が長さを超えたら正方形。"""
    a = deck_area(x)
    w = max(4.2, a / TRAIN_L)
    if w <= TRAIN_L:
        return w, TRAIN_L
    s = math.sqrt(a)
    return s, s


def segs(*parts):
    """(frames, x0, x1) を並べる。x0 == x1 は一時停止（数字が止まる）。"""
    return [(f, a, b, STOP if a == b else FAST) for f, a, b in parts]


# 名前に AERIAL が入った場面は、空から見下ろす（太陽のにじみを弱く）
AERIAL = {"f05_wide", "f06_tokyo", "f07_japan", "f08_loop", "f09_world", "f10_area", "f11_end"}
NOTE = "※乗客が1駅ごとに2倍になる、もしもの話です"

SHOTS = [
    dict(name="e01_open", frames=150, kind="open"),
    dict(name="f02_car", frames=180, segs=segs((45, 0, 0), (45, 0, 5), (60, 5, 5), (30, 5, 7)),
         note=(0, 2.8, NOTE),
         captions=[(0.2, 1.5, ["最初の乗客は、", "たった1人"]), (3.0, 5.0, ["5駅目で32人。", "ここまでは、いつもの車内"])]),
    dict(name="f03_full", frames=180, segs=segs((30, 7, 10), (60, 10, 10), (30, 10, 13), (60, 13, 13)),
         captions=[(1.0, 3.0, ["10駅目で1024人。", "1両に約93人のすし詰め"]),
                   (4.0, 6.0, ["13駅目で8192人。", "1両に約740人。もう乗れない"])]),
    dict(name="f04_deck", frames=195, segs=segs((90, 13, 13), (45, 13, 16), (60, 16, 16)),
         captions=[(0.3, 2.9, ["そこで電車の屋根に", "床板を取り付けた"]),
                   (4.6, 6.5, ["16駅目で6万5536人。", "東京ドームの満員より多い"])]),
    dict(name="f05_wide", frames=135, segs=segs((45, 16, 20), (90, 20, 20)),
         captions=[(1.5, 4.5, ["20駅目で104万人。", "床板は東京ドーム5個分"])]),
    dict(name="f06_tokyo", frames=120, segs=segs((45, 20, 24), (75, 24, 24)),
         captions=[(1.5, 4.0, ["24駅目で1677万人。", "東京都の人口を超えた"])],
         info=("人口", [(0.3, (235, 235, 240), "東京都　約1429万人", (255, 255, 255)),
                       (1.5, None, "24駅目　約1677万人", (240, 150, 70))])),
    dict(name="f07_japan", frames=120, segs=segs((45, 24, 27), (75, 27, 27)),
         captions=[(1.5, 4.0, ["27駅目で1億3421万人。", "日本の人口を超えた"])],
         info=("人口", [(0.3, (235, 235, 240), "日本　約1億2268万人", (255, 255, 255)),
                       (1.5, None, "27駅目　約1億3421万人", (240, 150, 70))])),
    dict(name="f08_loop", frames=120, segs=segs((45, 27, 30), (75, 30, 30)),
         captions=[(1.5, 4.0, ["山手線を1周（30駅）で、", "10億7374万人"])],
         info=("1駅ごとに2倍の乗客", [(0.3, None, "0駅　　1人", (255, 255, 255)),
                                     (0.7, None, "10駅　 1024人", (255, 255, 255)),
                                     (1.1, None, "20駅　 約105万人", (255, 255, 255)),
                                     (1.5, None, "30駅　 約10.7億人", (240, 150, 70))])),
    dict(name="f09_world", frames=120, segs=segs((45, 30, 33), (75, 33, 33)),
         captions=[(1.5, 4.0, ["33駅目で約86億人。", "世界の人口を超えた"])]),
    dict(name="f10_area", frames=120, segs=segs((120, 33, 33)),
         captions=[(0.3, 4.0, ["床板の広さは約2150㎢。", "東京都とほぼ同じ"])],
         info=("1㎡に4人で立つと", [(0.5, None, "約86億人　約2150㎢", (255, 255, 255)),
                                    (1.4, (235, 235, 240), "東京都　約2194㎢", (240, 150, 70))])),
    dict(name="f11_end", frames=120, segs=segs((120, 33, 33)),
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
