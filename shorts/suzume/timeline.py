"""「もしも日本からスズメが消えたら？」の時間割（30fps、約74秒）。台本は SCRIPT.md。
e は「スズメが消えてから」の経過秒。segs = [(コマ数, e0, e1)]。"""

FPS = 30
DAY = 86400
YEAR = 365 * DAY
T_VANISH = 5.6
H = 3600


def segs(*parts):
    return list(parts)


def at(e0, frames, dur):
    """e0 から dur 秒ぶんを frames コマで。"""
    return segs((frames, e0, e0 + dur))


JOY = ("おかえり、[スズメ]", ["米はねらわれるけれど", "やっぱり、いてよかった"])

SHOTS = [
    dict(name="s01_open", frames=240, kind="open", loc="新潟・米どころの村（10月の夕方5時）"),
    dict(name="s02_wire", frames=120, segs=at(0.0, 120, 4.0), loc="同じ瞬間 ― 新潟・村の電線",
         captions=[(0.5, 4.0, "その夕方、日本から[スズメ]が消えた", ["いちばん身近な鳥が", "一羽残らず"])]),
    dict(name="s03_feed", frames=135, segs=at(14 * H, 135, 300), card="次の朝", loc="東京・おばあちゃんの家",
         captions=[(1.0, 4.5, "[チュンチュン]が聞こえない", ["毎朝あたりまえだった声が", "どこにもない"])]),
    dict(name="s04_scare", frames=135, segs=at(7 * DAY + 10 * H, 135, 9000), card="1週間後", loc="新潟・田んぼ",
         captions=[(1.0, 4.5, "[案山子]の出番がなくなった", ["米をねらう鳥が", "もう来ない"])]),
    dict(name="s05_issa", frames=135, segs=at(30 * DAY + 16 * H, 135, 1800), card="1か月後", loc="長野・小学校の教室",
         captions=[(1.0, 4.5, "[一茶]の句の主役が消えた", ["「雀の子 そこのけそこのけ", "御馬が通る」（小林一茶）"])]),
    dict(name="s06_fukura", frames=135, segs=at(92 * DAY + 15 * H, 135, 6000), card="3か月後", loc="新潟・雪の村",
         captions=[(1.0, 4.5, "冬の[ふくら雀]がいない", ["羽に空気をためて", "寒さをしのぐ姿"])]),
    dict(name="s07_spring", frames=150, segs=at(182 * DAY + 16 * H, 150, 20000), card="半年後", loc="東京・家庭菜園（4月）",
         captions=[(1.0, 5.0, "スズメは[害鳥]だけじゃなかった", ["春から夏は、ヒナに", "たくさんの虫を運んでいた"])]),
    dict(name="s08_paddy", frames=165, segs=at(300 * DAY + 17 * H, 165, 3000), card="10か月後", loc="新潟・田んぼ（8月）",
         captions=[(1.0, 5.5, "田んぼに[虫]が増えた", ["稲の葉を食べる虫を", "食べる鳥がいない"])]),
    dict(name="s09_china", frames=150, segs=at(300 * DAY + 18 * H, 150, 300), loc="【実話】1958年 ― 中国の農村", sepia=True,
         captions=[(0.4, 5.0, "中国では[本当に起きた]", ["1958年、スズメを追い払ったあと", "害虫が大発生したとされる"])]),
    dict(name="s10_drone", frames=135, segs=at(YEAR + 300 * DAY + 10 * H, 135, 3000), card="2年目の夏", loc="新潟・田んぼ",
         captions=[(1.0, 4.5, "[農薬]をまく回数がふえた", ["スズメのかわりに", "虫を減らすため"])]),
    dict(name="s11_song", frames=135, segs=at(5 * YEAR + 10 * H, 135, 1500), card="5年後", loc="東京・幼稚園",
         captions=[(1.0, 4.5, "[すずめの学校]を知らない子", ["1921年の童謡", "「チイチイパッパ」"])]),
    dict(name="s12_return", frames=210, segs=segs((60, 10 * YEAR - 2.0, 10 * YEAR), (150, 10 * YEAR, 10 * YEAR + 5.0)),
         loc="新潟・米どころの村（10年後の同じ日、夕方5時）",
         captions=[(2.4, 7.0, "空に[スズメ]がもどってきた", ["消えたのと", "同じ日の、同じ時刻"])]),
    dict(name="j1_chase", frames=75, segs=at(10 * YEAR + 5.0, 75, 2.5), loc="新潟・米どころの村",
         captions=[(0.0, 9.0, *JOY)]),
    dict(name="j2_garden", frames=45, segs=at(10 * YEAR + 7.5, 45, 1.5), loc="東京・おばあちゃんの家", cap_cont=True),
    dict(name="j3_wire", frames=45, segs=at(10 * YEAR + 9.0, 45, 1.5), loc="新潟・村の電線", cap_cont=True),
    dict(name="j4_school", frames=45, segs=at(10 * YEAR + 10.5, 45, 1.5), loc="長野・小学校の教室", cap_cont=True),
    dict(name="j5_wide", frames=75, segs=at(10 * YEAR + 12.0, 75, 2.5), loc="新潟・米どころの村", cap_cont=True),
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
