"""「もしも人間がタマゴで生まれたら？」の時間割（30fps、約52秒）。台本は SCRIPT.md。e は「タマゴになってから」の経過秒。"""

FPS = 30
DAY = 86400
YEAR = 365 * DAY
T_VANISH = 5.6          # タマゴになる瞬間
H = 3600


def segs(*parts):
    return list(parts)


def at(e0, frames, dur):
    return segs((frames, e0, e0 + dur))


SHOTS = [
    dict(name="e00_open", frames=210, kind="open", t0=0.0, loc="東京・病院の新生児室"),
    dict(name="e01_burst", frames=120, segs=at(0.0, 120, 4.0), loc="同じ瞬間 ― 東京・病院",
         captions=[(0.4, 4.0, "その日から、赤ちゃんは[タマゴ]で生まれる", ["世界中で、いっせいに", "※体のしくみは考えない、もしもの話です"])]),
    dict(name="e02_size", frames=135, segs=at(DAY, 135, 300), card="1日後", loc="東京・病院",
         captions=[(1.0, 4.5, "重さは[約4.5kg]", ["ダチョウの卵の約3倍", "（3kgの赤ちゃんが入る大きさを計算）"])]),
    dict(name="e03_warm", frames=150, segs=at(7 * DAY, 150, 3000), card="1週間後", loc="東京・あの2人の家",
         captions=[(1.0, 5.0, "37℃で[温め続ける]", ["人の体温と同じ", "1日に何度も向きを変える"])]),
    dict(name="e04_office", frames=150, segs=at(30 * DAY + 2 * H, 150, 1200), card="1か月後", loc="東京・会社",
         captions=[(1.0, 5.0, "お父さんも[タマゴ]をかかえて出勤", ["交代で温めるので", "会社にタマゴ置き場"])]),
    dict(name="e05_penguin", frames=150, segs=at(30 * DAY + 3 * H, 150, 300), loc="【実話】南極 ― コウテイペンギンの冬",
         captions=[(0.4, 5.0, "ペンギンの父は[約2か月]温める", ["南極の冬、足の上で", "何も食べずに"])]),
    dict(name="e06_strong", frames=135, segs=at(91 * DAY + 20 * H, 135, 30), card="3か月後", loc="東京・あの2人の家",
         captions=[(1.0, 4.5, "タマゴは[上から]の力に強い", ["丸い殻が力を分ける", "ダチョウの卵は大人が乗ってもわれにくい"])]),
    dict(name="e07_hatch", frames=180, segs=at(274 * DAY + 10 * H, 180, 60), card="9か月後", loc="東京・あの2人の家",
         captions=[(1.0, 6.0, "赤ちゃんが[自分で]殻をわる", ["鳥のひなは くちばしの先の", "「卵歯」で殻をわる"])]),
    dict(name="e08_home", frames=240, segs=at(274 * DAY + 21 * H, 240, 8.0), card="その夜", loc="東京・あの2人の家（夜9時）",
         captions=[(1.0, 4.4, "かえるまで[9か月]", ["ふたりで交代で", "温めつづけた"]),
                   (4.4, 8.0, "おなかでもタマゴでも[待つ時間]は同じ", ["生まれてきてくれて", "ありがとう"])]),
    dict(name="s99_end", frames=90, kind="end"),
]


def shot(name):
    return next(s for s in SHOTS if s["name"] == name)


def e_of(s, i):
    k = 0
    for n, a, b in s["segs"]:
        if i < k + n:
            return a + (b - a) * (i - k) / n, (b - a) / (n / FPS)
        k += n
    n, a, b = s["segs"][-1]
    return b, (b - a) / (n / FPS)


def total_frames():
    return sum(s["frames"] for s in SHOTS)


def start_of(name):
    k = 0
    for s in SHOTS:
        if s["name"] == name:
            return k / FPS
        k += s["frames"]
    raise KeyError(name)
