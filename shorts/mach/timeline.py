"""「もしも新幹線がマッハ10で走っていたら？」の全体の時間割（59秒、30fps）。
3Dの書き出し（film.py）と、文字の重ね（compose_all.py）の両方がここを読む。
t は「出発からの実際の秒数」。マッハ10＝秒速3400m、出発から1秒で一定の加速でマッハ10に達する（もしもの話）。"""
FPS = 30
V = 3400.0                  # マッハ10（m/秒）
TOTAL_KM = 28.8             # 東京→新横浜（営業キロ）
T_ARRIVE = 1.0 + (TOTAL_KM * 1000 - 1700) / V      # 約8.97秒
T_SHINAGAWA = 1.0 + (6800 - 1700) / V              # 品川（6.8km）約2.50秒
T_TAMA = 3.7                                       # 多摩川の鉄橋（約11km）


def pos(t):
    """出発からの進んだ距離（m）。"""
    if t <= 0:
        return 0.0
    if t <= 1:
        return 1700.0 * t * t
    return 1700.0 + V * (t - 1)


def mach(t):
    return 10.0 * min(max(t, 0), 1.0)


def remain_km(t):
    return max(0.0, TOTAL_KM - pos(min(t, T_ARRIVE)) / 1000)


ORANGE, GREEN = "orange", "green"
REAL = ("実際の速さ", GREEN)


def slow(n):
    return (f"リプレイ　1/{n} スロー", ORANGE)


# 各場面: frames=フレーム数, segs=[(フレーム数, t始め, t終わり, 枠)], widget='mach'|'dist'|'auto'
# captions=[(秒, 秒, [行])]、info=(見出し, [(出す秒, アイコン色, 文字, 色)])、note=(秒, 秒, 文字)
SHOTS = [
    dict(name="s01_open", frames=150, kind="open"),
    dict(name="s02_wheel", frames=45, segs=[(23, 0.0, 0.00004, ("1/500 スロー", ORANGE)), (22, 0.00004, 0.00006, ("1/1000 スロー", ORANGE))],
         widget="mach", note=(0, 1.5, "※東京―新横浜間（28.8km）で計算した、もしもの話です")),
    dict(name="s03a_cab", frames=36, segs=[(36, 0.0, 1.2, REAL)], widget="auto",
         note=(0, 1.2, "※東京―新横浜間（28.8km）で計算した、もしもの話です")),
    dict(name="s03b_shinagawa", frames=48, segs=[(48, 1.2, 2.8, REAL)], widget="dist"),
    dict(name="s03c_tama", frames=48, segs=[(48, 2.8, 4.4, REAL)], widget="dist"),
    dict(name="s03d_town", frames=66, segs=[(66, 4.4, 6.6, REAL)], widget="dist"),
    dict(name="s03e_arrive", frames=117, segs=[(117, 6.6, 10.5, REAL)], widget="dist", freeze=T_ARRIVE),
    dict(name="s05_rewind", frames=21, kind="rewind"),
    dict(name="s06_boom", frames=114, segs=[(114, 0.070, 0.133, slow(60))], widget="mach",
         captions=[(1.3, 3.8, ["音の速さを超えた瞬間、", "白い雲の輪ができた"])]),
    dict(name="s07_heat", frames=120, segs=[(120, 0.660, 0.676, slow(250))], widget="mach",
         captions=[(0.4, 4.0, ["空気の熱で、", "先頭の塗装が燃えた"])]),
    dict(name="s08_streak", frames=120, segs=[(30, 0.688, 0.690, slow(500)), (90, 0.690, 0.990, slow(10))], widget="mach",
         captions=[(0.4, 4.0, ["車体と乗客だけは、", "燃えない設定です"])]),
    dict(name="s09_sound", frames=135, segs=[(135, 1.000, 1.009, slow(500))], widget="mach",
         captions=[(0.3, 4.5, ["音の速さは、のぞみの約4倍。", "マッハ10は、さらにその10倍"])],
         info=("それぞれの速さ", [(0.6, (40, 90, 200), "のぞみ　秒速79m", (255, 255, 255)),
                                  (1.6, (230, 230, 230), "音　　　秒速340m", (255, 255, 255)),
                                  (2.6, None, "×10 → マッハ10", (240, 150, 70))])),
    dict(name="s10_after", frames=105, segs=[(105, 2.480, 2.798, slow(11))], widget="dist",
         captions=[(0.5, 3.5, ["新幹線の音は、", "通りすぎたあとに来る"])]),
    dict(name="s11_bench", frames=120, segs=[(60, 2.495, 2.552, slow(35)), (60, 2.552, 4.552, REAL)], widget="dist",
         captions=[(0.4, 4.0, ["押しのけた空気で、", "ホームのベンチが吹き飛んだ"])]),
    dict(name="s12_osaka", frames=135, segs=[(135, 3.001, 3.010, slow(500))], widget="dist",
         captions=[(0.3, 4.5, ["マッハ10なら、", "東京から新大阪まで2分32秒"])],
         info=("東京→新大阪 515km", [(0.6, (40, 90, 200), "のぞみ　約2時間21分", (255, 255, 255)),
                                     (1.8, (240, 150, 70), "マッハ10　約2分32秒", (240, 150, 70))])),
    dict(name="s13_fisher", frames=120, segs=[(120, 3.72, 4.39, slow(6))], widget="dist",
         captions=[(0.5, 4.0, ["河川敷の釣り人は無事で、", "釣り竿だけが飛んでいった"])]),
    dict(name="s14_river", frames=135, segs=[(135, 3.68, 3.7925, slow(40))], widget="dist",
         captions=[(0.6, 4.5, ["押しのけた空気で、", "多摩川の水面が2つに割れた"])]),
    dict(name="s15_end", frames=135, segs=[(135, 10.5, 15.0, REAL)], widget="dist", freeze=T_ARRIVE,
         captions=[(0.5, 4.5, ["東京から新横浜まで、9秒。", "今の「のぞみ」なら約18分"])]),
]


def shot(name):
    return next(s for s in SHOTS if s["name"] == name)


def t_of(s, i):
    """場面 s の i フレーム目（0始まり）の t と、そのときの枠。"""
    k = 0
    for n, a, b, tag in s["segs"]:
        if i < k + n:
            return a + (b - a) * (i - k) / n, tag
        k += n
    n, a, b, tag = s["segs"][-1]
    return b, tag


def total_frames():
    return sum(s["frames"] for s in SHOTS)
