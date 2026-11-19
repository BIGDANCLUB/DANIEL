"""「もしも日本から富士山が消えたら？」の時間割（30fps、約92秒）。台本は SCRIPT.md（v2）。
e は「富士山が消えてから」の経過秒。segs = [(コマ数, e0, e1)]。"""

FPS = 30
DAY = 86400
YEAR = 365 * DAY
T_VANISH = 5.4


def segs(*parts):
    return list(parts)


def at(e0, frames, dur):
    """e0 から dur 秒ぶんを frames コマで。"""
    return segs((frames, e0, e0 + dur))


H = 3600
SHOTS = [
    dict(name="f01_open", frames=240, kind="open", loc="静岡・富士市の家（朝6時）"),
    dict(name="f02_train", frames=120, segs=at(0.0, 120, 4.0), loc="同じ瞬間 ― 東海道新幹線",
         captions=[(0.3, 4.0, "その朝、日本から[富士山]が消えた", ["高さ3776m、日本一の山が", "一瞬でなくなった"])]),
    dict(name="f03_shadow", frames=150, segs=at(4.0, 150, 5.0), loc="同じころ ― 静岡・朝霧高原",
         captions=[(0.6, 5.0, "朝日の[影]が消えた", ["日の出に長く伸びていた", "山の影（影富士）が、スッと消える"])]),
    dict(name="f04_sento", frames=105, segs=at(1 * DAY + 10 * H, 105, 3000), card="次の日", loc="東京・お風呂屋さん",
         captions=[(1.0, 3.5, "壁の[富士山]だけが残った", ["銭湯の壁の絵が", "本物より先に、なつかしい景色に"])]),
    dict(name="f05_kitadake", frames=105, segs=at(3 * DAY + 9 * H, 105, 9000), card="3日後", loc="山梨・南アルプス 北岳",
         captions=[(1.0, 3.5, "日本一は[北岳]へ", ["高さ3193m", "日本一が、583m低くなった"])]),
    dict(name="f06_cloud", frames=180, segs=at(7 * DAY + 8 * H, 180, 20000), card="1週間後", loc="富士山があった場所の上空",
         captions=[(1.0, 3.4, "山にぶつかった[風]が上って", ["冷えると、山の上に", "笠雲やつるし雲ができていた"]),
                   (3.4, 6.0, "[笠雲]も[つるし雲]もできない", ["風は、そのまま通りすぎる"])]),
    dict(name="f07_spring", frames=180, segs=at(30 * DAY + 9 * H, 180, 40 * DAY), card="1か月後", loc="静岡・清水町の柿田川",
         captions=[(1.0, 6.0, "わき水は[まだ止まらない]", ["富士山にふった雨や雪は", "何十年もかけて地下を流れてくる"])]),
    dict(name="f08_snow", frames=135, segs=at(182 * DAY + 11 * H, 135, 30000), card="半年後", loc="静岡・富士宮",
         captions=[(1.0, 4.5, "夏まで残る[雪]がない", ["雪どけ水が少しずつ地下へ", "しみこむ流れが止まった"])]),
    dict(name="f09_hazard", frames=135, segs=at(YEAR + 10 * H, 135, 6000), card="1年後", loc="静岡・富士宮",
         captions=[(1.0, 4.5, "[噴火]の心配はなくなった", ["最後の噴火は1707年（宝永噴火）", "「いいこと」もあった"])]),
    dict(name="f10_plumb", frames=135, segs=at(2 * YEAR + 11 * H, 135, 1500), card="2年後", loc="静岡・中学校の理科室",
         captions=[(1.0, 4.5, "おもりの糸が[ほんの少し]まっすぐに", ["大きな山は、まわりのものを", "ほんのわずかに引っぱっていた"])]),
    dict(name="f11_diamond", frames=135, segs=at(3 * YEAR + 16 * H, 135, 1800), card="3年後", loc="山梨・山中湖（夕方）",
         captions=[(1.0, 4.5, "[ダイヤモンド富士]はもう来ない", ["山頂に太陽が重なる景色を", "待つ人もいなくなった"])]),
    dict(name="f12_kid", frames=180, segs=at(5 * YEAR + 10 * H, 180, 600), card="5年後", loc="静岡・富士市のおじいさんの家",
         captions=[(1.2, 6.0, "おじいちゃん、[一富士]ってなに？", ["「一富士 二鷹 三なすび」", "孫は、富士山を見たことがない"])]),
    dict(name="f13_lowwater", frames=150, segs=at(8 * YEAR + 10 * H, 150, 200 * DAY), card="8年後", loc="静岡・清水町の柿田川",
         captions=[(1.0, 5.0, "わき水が[減ってきた]", ["地下にたまっていた水にも", "終わりが見えてきた"])]),
    dict(name="f14_trout", frames=90, segs=at(9 * YEAR + 9 * H, 90, 3000), card="9年後", loc="静岡・富士宮のニジマス養殖場",
         captions=[(0.5, 3.0, "ニジマスの[池]が浅く", ["冷たいわき水で育てていた"])]),
    dict(name="f15_paper", frames=90, segs=at(9 * YEAR + 11 * H, 90, 3000), loc="静岡・富士市の製紙工場",
         captions=[(0.2, 3.0, "紙をつくる[水]が足りない", ["富士市は、地下水で栄えた紙の町"])]),
    dict(name="f16_tap", frames=90, segs=at(9 * YEAR + 18 * H, 90, 300), loc="静岡・三島の家",
         captions=[(0.2, 3.0, "蛇口の水が[細くなった]", ["わき水は、まわりの町の水道にも"])]),
    dict(name="f17_return", frames=210, segs=segs((60, 10 * YEAR - 2.0, 10 * YEAR), (150, 10 * YEAR, 10 * YEAR + 5.0)),
         loc="静岡・富士市（10年後の同じ日、朝6時）",
         captions=[(2.4, 7.0, "雲の向こうに[白い頂]が", ["消えたのと", "同じ日の、同じ時刻"])]),
    dict(name="j1_home", frames=60, segs=at(10 * YEAR + 5.0, 60, 2.0), loc="静岡・富士市",
         captions=[(0.0, 9.0, "やっぱり、[あってよかった]", ["10年ぶりの、いつもの景色"])], cap_from="j1_home"),
    dict(name="j2_trout", frames=45, segs=at(10 * YEAR + 7.0, 45, 1.5), loc="静岡・富士宮", cap_cont=True),
    dict(name="j3_paper", frames=45, segs=at(10 * YEAR + 8.5, 45, 1.5), loc="静岡・富士市", cap_cont=True),
    dict(name="j4_tap", frames=45, segs=at(10 * YEAR + 10.0, 45, 1.5), loc="静岡・三島", cap_cont=True),
    dict(name="j5_wide", frames=75, segs=at(10 * YEAR + 11.5, 75, 2.5), loc="静岡・富士市", cap_cont=True),
    dict(name="f19_end", frames=90, kind="end"),
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
