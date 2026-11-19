"""「もしも日本からスギが消えたら？」の時間割（30fps、約86秒）。台本は SCRIPT.md。
e は「スギが消えてから」の経過秒。segs = [(コマ数, e0, e1)]。"""

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


JOY = ("おかえり、[スギ]", ["鼻はムズムズするけれど", "やっぱり、あってよかった"])

SHOTS = [
    dict(name="s01_open", frames=240, kind="open", loc="秋田・山あいの町（3月の朝7時）"),
    dict(name="s02_shrine", frames=120, segs=at(0.0, 120, 4.0), loc="同じ瞬間 ― 長野・山あいの神社",
         captions=[(0.5, 4.0, "その朝、日本から[スギ]が消えた", ["人工林の約4割、441万ha", "東京都の約20倍の広さ"])]),
    dict(name="s03_station", frames=150, segs=at(600.0, 150, 5.0), loc="10分後 ― 東京・朝の駅のホーム",
         captions=[(0.6, 5.0, "鼻が、[とおった]", ["1964年に見つかってから約60年", "花粉のない春がきた"])]),
    dict(name="s04_bare", frames=135, segs=at(7 * DAY + 9 * H, 135, 20000), card="1週間後", loc="秋田・山あいの町",
         captions=[(1.0, 4.5, "山が[まだら]になった", ["スギのあった斜面は", "土がむき出しに"])]),
    dict(name="s05_lumber", frames=120, segs=at(30 * DAY + 10 * H, 120, 3000), card="1か月後", loc="宮崎・製材所",
         captions=[(1.0, 4.0, "国産の木の[6割]が消えた", ["日本でとれる木材の", "約6割はスギだった"])]),
    dict(name="s06_rain", frames=180, segs=at(95 * DAY + 15 * H, 180, 1500), card="3か月後", loc="梅雨 ― 山あいの集落",
         captions=[(1.2, 6.0, "山が[くずれはじめた]", ["スギの根が", "斜面の土をつかまえていた"])]),
    dict(name="s07_river", frames=105, segs=at(95 * DAY + 16 * H, 105, 1200), loc="同じ日 ― 山あいの川",
         captions=[(0.3, 3.5, "川が[茶色]に", ["山の土が", "雨といっしょに流れてくる"])]),
    dict(name="s08_snow", frames=150, segs=at(300 * DAY + 9 * H, 150, 600), card="10か月後", loc="新潟・雪国の山道",
         captions=[(1.2, 5.0, "[雪崩]が止まらない", ["スギの林が", "斜面の雪をささえていた"])]),
    dict(name="s09_sake", frames=120, segs=at(YEAR + 17 * H, 120, 1800), card="1年後", loc="兵庫・灘の酒蔵",
         captions=[(1.0, 4.0, "新酒の[しるし]が作れない", ["酒蔵の杉玉は", "新しいお酒ができた合図"])]),
    dict(name="s10_nikko", frames=135, segs=at(2 * YEAR + 10 * H, 135, 3000), card="2年後", loc="栃木・日光の杉並木",
         captions=[(1.0, 4.5, "世界一の[並木道]が、ただの道に", ["日光杉並木：約37kmに", "約1万2千本のスギ"])]),
    dict(name="s11_jomon", frames=135, segs=at(3 * YEAR + 11 * H, 135, 3000), card="3年後", loc="鹿児島・屋久島",
         captions=[(1.0, 4.5, "[縄文杉]に、もう会えない", ["何千年も生きてきたと", "言われる木"])]),
    dict(name="s12_hanami", frames=150, segs=at(5 * YEAR + 13 * H, 150, 1200), card="5年後", loc="東京・公園（3月）",
         captions=[(1.0, 5.0, "春が、[いちばん好き]になった", ["花粉症の人も", "マスクなしでお花見"])]),
    dict(name="s13_hinoki", frames=105, segs=at(5 * YEAR + 35 * DAY + 13 * H, 105, 900), loc="5年後の4月 ― 同じ公園",
         captions=[(0.3, 3.5, "でも、[ヒノキ]は残っていた", ["スギ花粉症の人は", "ヒノキにも反応しやすい"])]),
    dict(name="s14_plant", frames=135, segs=at(7 * YEAR + 60 * DAY + 10 * H, 135, 40 * DAY), card="7年後", loc="秋田・山の斜面",
         captions=[(1.0, 4.5, "山に、[木を植えなおす]", ["根が育って土を守るまで", "何十年もかかる"])]),
    dict(name="s15_return", frames=210, segs=segs((60, 10 * YEAR - 2.0, 10 * YEAR), (150, 10 * YEAR, 10 * YEAR + 5.0)),
         loc="秋田・山あいの町（10年後の同じ日、朝7時）",
         captions=[(2.4, 7.0, "山に、[スギ]がもどってきた", ["消えたのと", "同じ日の、同じ時刻"])]),
    dict(name="j1_sneeze", frames=75, segs=at(10 * YEAR + 5.0, 75, 2.5), loc="秋田・山あいの町",
         captions=[(0.0, 9.0, *JOY)]),
    dict(name="j2_lumber", frames=45, segs=at(10 * YEAR + 7.5, 45, 1.5), loc="宮崎・製材所", cap_cont=True),
    dict(name="j3_sake", frames=45, segs=at(10 * YEAR + 9.0, 45, 1.5), loc="兵庫・灘の酒蔵", cap_cont=True),
    dict(name="j4_nikko", frames=45, segs=at(10 * YEAR + 10.5, 45, 1.5), loc="栃木・日光の杉並木", cap_cont=True),
    dict(name="j5_wide", frames=75, segs=at(10 * YEAR + 12.0, 75, 2.5), loc="秋田・山あいの町", cap_cont=True),
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
