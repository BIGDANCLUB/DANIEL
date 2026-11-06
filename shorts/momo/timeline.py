"""「もしも桃太郎が光の速さで鬼ヶ島に向かったら？」の時間割（約59秒、30fps）。新幹線版と同じ構成。
t は出発からの実際の秒数。光の速さ c で、出発した瞬間から一定の速さ（もしもの話）。"""
FPS = 30
C = 299_792_458.0            # 光の速さ（m/秒）
TOTAL_KM = 37.0              # 吉備津 → 女木島（直線）
T_ARRIVE = TOTAL_KM * 1000 / C          # 約0.000123秒
SOUND = 340.0


def pos(t):
    return min(max(t, 0.0) * C, TOTAL_KM * 1000)


def remain_km(t):
    return max(0.0, TOTAL_KM - pos(t) / 1000)


ORANGE, GREEN = "orange", "green"
REAL = ("実際の速さ", GREEN)


def slow(label):
    return (f"リプレイ　{label} スロー", ORANGE)


OKU = 1e-8         # 1億分の1
# 場面の位置（出発からの距離 m）→ そこを通る t
def t_at(m):
    return m / C


SHOTS = [
    dict(name="m01_open", frames=150, kind="open"),
    dict(name="m02_foot", frames=45, segs=[(45, 0.0, 1.5 * OKU, ("1/1億 スロー", ORANGE))],
         note=(0, 1.5, "※鬼ヶ島は女木島（香川県高松市）とする説で計算した、もしもの話です")),
    dict(name="m03a_vanish", frames=75, segs=[(75, 0.0, 2.5, REAL)], freeze=T_ARRIVE,
         note=(0, 2.5, "※鬼ヶ島は女木島（香川県高松市）とする説で計算した、もしもの話です")),
    dict(name="m03b_island", frames=90, segs=[(90, 2.5, 5.5, REAL)], freeze=T_ARRIVE),
    dict(name="m03c_animals", frames=60, segs=[(60, 5.5, 7.5, REAL)], freeze=T_ARRIVE,
         captions=[(0.3, 2.0, ["出発から到着まで、", "0.00012秒"])]),
    dict(name="m05_rewind", frames=21, kind="rewind"),
    dict(name="m06_run", frames=132, segs=[(132, t_at(200), t_at(200) + 4.4 * OKU, slow("1/1億"))],
         captions=[(0.4, 4.4, ["1億分の1秒で、", "3m進む"])]),
    dict(name="m07_fire", frames=132, segs=[(132, t_at(800), t_at(800) + 4.4 * OKU, slow("1/1億"))],
         captions=[(0.4, 4.4, ["空気とぶつかる熱で、", "着物が燃えた"])]),
    dict(name="m08_safe", frames=132, segs=[(132, t_at(3000), t_at(3000) + 4.4 * OKU, slow("1/1億"))],
         captions=[(0.4, 4.4, ["桃太郎ときびだんごだけは、", "燃えない設定です"])]),
    dict(name="m09_light", frames=132, segs=[(132, t_at(10000), t_at(10000) + 4.4 * OKU, slow("1/1億"))],
         captions=[(0.3, 4.4, ["光の速さは、", "音の約88万倍"])],
         info=("それぞれの速さ", [(0.6, (250, 230, 120), "光　1秒で地球7周半", (255, 255, 255)),
                                  (1.6, (230, 230, 230), "音　秒速340m", (255, 255, 255)),
                                  (2.6, None, "光は音の 約88万倍", (240, 150, 70))])),
    dict(name="m10_sound", frames=132, segs=[(132, 0.0003, 0.0003 + 4.4, REAL)], freeze=T_ARRIVE,
         captions=[(0.4, 4.4, ["出発の足音が鬼ヶ島に", "届くのは、109秒後"])]),
    dict(name="m11_sea", frames=132, segs=[(132, t_at(20000), t_at(20000) + 4.4, REAL)], freeze=T_ARRIVE,
         captions=[(0.5, 4.4, ["押しのけた空気で、", "瀬戸内海が2つに割れた"])]),
    dict(name="m12_clock", frames=132, segs=[(132, t_at(30000), t_at(30000) + 4.4 * OKU, slow("1/1億"))],
         captions=[(0.3, 4.4, ["光の速さでは、桃太郎の時計は", "止まる。出発と到着が同じ瞬間"])],
         info=("桃太郎の時計", [(0.6, (240, 150, 70), "出発 0秒", (255, 255, 255)),
                                (1.6, (240, 150, 70), "到着 0秒", (255, 255, 255))])),
    dict(name="m13_oni", frames=132, segs=[(132, T_ARRIVE - 1.5 * OKU, T_ARRIVE + 2.9 * OKU, slow("1/1億"))],
         captions=[(0.5, 4.4, ["鬼が気づいたときには、", "もう着いていた"])]),
    dict(name="m14_club", frames=132, segs=[(132, T_ARRIVE, T_ARRIVE + 4.4 / 30, slow("1/30"))], freeze=T_ARRIVE,
         captions=[(0.4, 4.4, ["鬼は無事で、", "金棒だけが飛んでいった"])]),
    dict(name="m15_end", frames=132, segs=[(132, 10.0, 14.4, REAL)], freeze=T_ARRIVE,
         captions=[(0.5, 4.4, ["そのころ犬・猿・キジは、", "まだ村にいた"])]),
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
