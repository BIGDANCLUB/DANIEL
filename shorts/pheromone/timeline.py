"""「もしも男女がフェロモンを出すようになったら？」の時間割（30fps、約68秒）。台本は SCRIPT.md。
e は「フェロモンが出てから」の経過秒。segs = [(コマ数, e0, e1)]。"""

FPS = 30
DAY = 86400
YEAR = 365 * DAY
T_VANISH = 5.6          # 出はじめる瞬間（ほかの作品と同じ名前で使う）
H = 3600


def segs(*parts):
    return list(parts)


def at(e0, frames, dur):
    """e0 から dur 秒ぶんを frames コマで。"""
    return segs((frames, e0, e0 + dur))


SHOTS = [
    dict(name="p00_moth", frames=78, kind="open", t0=0.0, loc="夕暮れの林"),            # 冒頭は2つの場面（林 → 交差点）
    dict(name="p01_open", frames=162, kind="open", t0=2.6, loc="東京・駅前の交差点（朝8時）"),
    dict(name="p02_burst", frames=120, segs=at(0.0, 120, 4.0), loc="同じ瞬間 ― 東京・駅前の交差点",
         captions=[(0.4, 4.0, "その朝、男女から[フェロモン]が出た", ["世界中で、いっせいに", "※見えるように色をつけています"])]),
    dict(name="p03_plume", frames=135, segs=at(10.0, 135, 4.5), loc="東京・駅前の交差点",
         captions=[(0.4, 4.5, "においは[頭の上]へのぼる", ["体温であたためられた空気が", "上へ流れる（秒速約20cm）"])]),
    dict(name="p04_train", frames=150, segs=at(30 * 60, 150, 600), card="30分後", loc="東京・通勤電車",
         captions=[(1.0, 5.0, "電車に においが[たまる]", ["閉めきった車内は逃げ場がない", "ドアが開くと、外へ流れ出す"])]),
    dict(name="p05_office", frames=150, segs=at(H + 15 * 60, 150, 1200), card="1時間後", loc="東京・会社",
         captions=[(1.0, 5.0, "52歳の課長に[モテ期]がきた", ["生まれてはじめて", "まわりに人が集まる"])]),
    dict(name="p06_wind", frames=150, segs=at(3 * H + 50 * 60, 150, 900), card="3時間後", loc="東京・公園（風の強い日）",
         captions=[(1.0, 5.0, "においは[風下]へ流れる", ["においのもとへは、風上へ", "ジグザグに進む（ガと同じ）"])]),
    dict(name="p07_perfume", frames=135, segs=at(DAY + 3 * H, 135, 3000), card="次の日", loc="東京・デパートの香水売り場",
         captions=[(1.0, 4.5, "フェロモン香水は[効かない]", ["効くという", "確かな研究はなかった"])]),
    dict(name="p08_silk", frames=150, segs=at(DAY + 4 * H, 150, 300), loc="【実話】1959年 ― ドイツの研究所", sepia=True,
         captions=[(0.4, 5.0, "最初のフェロモンは[カイコ]から", ["日本から取りよせた約50万匹から", "6.4mgを取り出した"])]),
    dict(name="p09_orchard", frames=150, segs=at(7 * DAY + 6 * H, 150, 6000), card="1週間後", loc="青森・リンゴ畑",
         captions=[(1.0, 5.0, "畑では[わざと]においを満たす", ["オスがメスを見つけられず", "虫が増えない（交信かく乱）"])]),
    dict(name="p10_confuse", frames=165, segs=at(30 * DAY + 8 * H, 165, 3000), card="1か月後", loc="東京・駅前の交差点",
         captions=[(1.0, 5.5, "でも、[だれ]のにおいか わからない", ["街じゅうがにおいでいっぱいになり", "リンゴ畑と同じことが起きた"])]),
    dict(name="p11_used", frames=150, segs=at(91 * DAY + 10 * H, 150, 3000), card="3か月後", loc="東京・会社",
         captions=[(1.0, 5.0, "課長の[モテ期]が終わった", ["同じにおいには鼻が慣れて", "感じなくなる"])]),
    dict(name="p12_home", frames=240, segs=at(YEAR + 19 * H, 240, 8.0), card="1年後", loc="東京・課長の家（夜7時）",
         captions=[(1.0, 4.4, "妻は[30年前]から気づいていた", ["においで相性がわかる、という", "研究がある（1995年 スイス）"]),
                   (4.4, 8.0, "においより[長いつきあい]", ["フェロモンが出る前から", "30年、となりにいる人"])]),
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
