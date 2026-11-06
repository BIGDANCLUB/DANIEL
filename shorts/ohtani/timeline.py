"""「もしも大谷翔平がホームランを年250本打ったら？」の時間割（約57秒、30fps）。新幹線版と同じ構成。
新幹線の「出発から◯秒／マッハ◯」を「開幕から◯試合／ホームラン◯本」に置き換える。g は開幕からの試合数（小数）。"""
FPS = 30
GAMES = 162
TOTAL_HR = 250
PER_GAME = TOTAL_HR / GAMES          # 約1.54本
BASE_M = 27.43                       # 塁間 90フィート
LAP_M = BASE_M * 4                   # 約110m
HR_M = 120.0                         # 1本の飛距離（仮に120m）


def hr(g):
    return min(TOTAL_HR, int(round(max(g, 0) * PER_GAME)))


ORANGE, GREEN = "orange", "green"
FAST = ("早送り　1秒＝15試合", GREEN)


def slow(n):
    return (f"リプレイ　1/{n} スロー", ORANGE)


SHOTS = [
    dict(name="o01_open", frames=150, kind="open"),
    dict(name="o02_swing", frames=45, segs=[(45, 0.0, 0.0, ("1/500 スロー", ORANGE))],
         note=(0, 1.5, "※2025年の成績とMLBの記録をもとにした、もしもの話です")),
    dict(name="o03a_fly", frames=75, segs=[(75, 0.0, 25.0, FAST)],
         note=(0, 2.5, "※2025年の成績とMLBの記録をもとにした、もしもの話です")),
    dict(name="o03b_stands", frames=90, segs=[(90, 25.0, 70.0, FAST)]),
    dict(name="o03c_board", frames=75, segs=[(75, 70.0, 120.0, FAST)]),
    dict(name="o03d_last", frames=75, segs=[(45, 120.0, 162.0, FAST), (30, 162.0, 162.0, FAST)]),
    dict(name="o05_rewind", frames=21, kind="rewind"),
    dict(name="o06_pergame", frames=132, segs=[(132, 30.0, 30.0, slow(30))],
         captions=[(0.4, 4.4, ["1試合に、", "約1.5本"])]),
    dict(name="o07_bonds", frames=132, segs=[(132, 47.0, 47.0, slow(500))],
         captions=[(0.3, 4.4, ["シーズン最多記録の、", "約3.4倍"])],
         info=("シーズンのホームラン", [(0.6, (230, 230, 230), "ボンズ　73本（2001年）", (255, 255, 255)),
                                     (1.6, (40, 90, 200), "2025年の大谷　55本", (255, 255, 255)),
                                     (2.6, None, "250本 ＝ 73本の 約3.4倍", (240, 150, 70))])),
    dict(name="o08_rain", frames=132, segs=[(132, 60.0, 60.0, slow(10))],
         captions=[(0.4, 4.4, ["外野席には、", "毎試合ボールが降ってくる"])]),
    dict(name="o09_lap", frames=132, segs=[(132, 80.0, 80.0, slow(6))],
         captions=[(0.3, 4.4, ["ダイヤモンドを回る距離は、", "1年で約27km"])],
         info=("ダイヤモンド1周", [(0.6, (240, 240, 240), "1周　約110m", (255, 255, 255)),
                                  (1.6, None, "×250本 ＝ 約27km", (240, 150, 70))])),
    dict(name="o10_distance", frames=132, segs=[(132, 100.0, 100.0, slow(500))],
         captions=[(0.4, 4.4, ["1本120mとすると、飛ばした", "距離は1年で約30km"])]),
    dict(name="o11_walk", frames=132, segs=[(132, 120.0, 120.0, slow(6))],
         captions=[(0.4, 4.4, ["2004年のボンズは、", "1年で120回も敬遠された"])]),
    dict(name="o12_fans", frames=132, segs=[(132, 140.0, 140.0, slow(10))],
         captions=[(0.4, 4.4, ["250個のホームランボールが、", "ファンの手に"])]),
    dict(name="o15_end", frames=132, segs=[(132, 162.0, 162.0, FAST)],
         captions=[(0.5, 4.4, ["数字の上では、ありえない。", "でも、見てみたい"])]),
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
