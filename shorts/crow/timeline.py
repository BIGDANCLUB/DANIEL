"""「もしもカラスが消えたら？」の時間割（30fps、約90秒）。よねあぷ型：
冒頭で「クロ」に感情移入 → 消える → 身近な変化 → 逆転（死がい・ハエ・ネズミ・小鳥）→ 懐かしさ → 10年後に再会。
e は「カラスが消えてから」の経過秒。segs = [(コマ数, e0, e1)]。"""

FPS = 30
DAY = 86400
YEAR = 365 * DAY
T_VANISH = 5.4          # 冒頭の何秒目に消えるか


def segs(*parts):
    return list(parts)


SHOTS = [
    dict(name="c01_open", frames=180, kind="open", loc="東京・新宿の公園（朝6時）"),
    dict(name="c02_wire", frames=120, segs=segs((120, 0.0, 4.0)), loc="同じ瞬間 ― 東京・新宿の電線",
         captions=[(0.4, 4.0, "その朝、日本から[カラス]が消えた", ["ハシブトガラスも、ハシボソガラスも", "電線から、空から、いなくなった"])]),
    dict(name="c03_quiet", frames=120, segs=segs((120, 4.0, 8.8)), loc="東京・新宿の公園（朝6時）",
         captions=[(0.2, 4.0, "「カァ」の[声]がしない", ["いつもの朝の合図が、なくなった"])]),
    dict(name="c04_garbage", frames=150, segs=segs((150, 1 * DAY + 60, 1 * DAY + 360)), card="次の朝",
         loc="東京・新宿のゴミ置き場（朝7時）",
         captions=[(1.0, 5.0, "ゴミ袋が[破られない]", ["朝のゴミ置き場が", "きれいなまま"])]),
    dict(name="c05_orchard", frames=150, segs=segs((150, 3 * DAY + 4 * 3600, 3 * DAY + 4 * 3600 + 15000)), card="3日後",
         loc="長野・りんご畑",
         captions=[(1.0, 5.0, "りんごが[つつかれない]", ["カラスによる農作物の被害は", "全国で年 約13億円（2022年度）"])]),
    dict(name="c05b_walnut", frames=180, segs=segs((180, 5 * DAY + 15 * 3600, 5 * DAY + 15 * 3600 + 18000)), card="5日後",
         loc="宮城・仙台の道路",
         captions=[(1.0, 5.8, "クルミが[割れないまま]", ["車にクルミをひかせて割る", "かしこいカラスがいた"])]),
    dict(name="c06_road", frames=180, segs=segs((180, 7 * DAY + 8 * 3600, 7 * DAY + 8 * 3600 + 18000)), card="1週間後",
         loc="国道沿い（8月）",
         captions=[(1.0, 3.2, "道ばたの[死がい]が残る", ["カラスは死がいも食べる", "街のそうじ屋の一員だった"]),
                   (3.2, 6.0, "くさるにおいが[ハエ]を呼ぶ", ["アンモニアや硫化水素が出る"])]),
    dict(name="c06b_kite", frames=180, segs=segs((180, 14 * DAY + 10 * 3600, 14 * DAY + 10 * 3600 + 18000)), card="2週間後",
         loc="同じ国道沿い",
         captions=[(1.0, 3.4, "代わりに[トビ]がやってきた", ["死がいを食べる鳥は", "カラスだけではない"]),
                   (3.4, 6.0, "でも、[街なか]には少ない", ["トビがいるのは", "おもに海や川の近く"])]),
    dict(name="c07_flies", frames=180, segs=segs((180, 30 * DAY + 9 * 3600, 30 * DAY + 9 * 3600 + 60000)), card="1か月後",
         loc="東京・住宅街",
         captions=[(1.0, 6.0, "[ハエ]が増えはじめた", ["卵から約2週間で成虫に", "残った死がいが、ハエのゆりかごに"])]),
    dict(name="c08_rats", frames=150, segs=segs((150, 90 * DAY + 16 * 3600, 90 * DAY + 16 * 3600 + 3000)), card="3か月後",
         loc="東京・新宿のゴミ置き場（夜10時）",
         captions=[(1.0, 5.0, "生ゴミは[ネズミ]のもの", ["カラスと取り合っていたエサを", "ネズミがひとり占め"])]),
    dict(name="c09_birds", frames=150, segs=segs((150, 182 * DAY + 3 * 3600, 182 * DAY + 3 * 3600 + 150000)), card="半年後",
         loc="静岡・キャベツ畑",
         captions=[(1.0, 5.0, "[小鳥]のヒナが育ちやすく", ["カラスは卵やヒナも食べていた", "ただ、ヘビなどが代わりに食べることも"])]),
    dict(name="c10_book", frames=180, segs=segs((180, 5 * YEAR + 10 * 3600, 5 * YEAR + 10 * 3600 + 600)), card="5年後",
         loc="東京・おじいさんの家",
         captions=[(1.2, 6.0, "おじいちゃん、[この鳥]なに？", ["♪からすといっしょに かえりましょう", "孫は、カラスを見たことがない"])]),
    dict(name="c10b_shrine", frames=180, segs=segs((180, 5 * YEAR + 10 * 3600 + 600, 5 * YEAR + 10 * 3600 + 1200)),
         loc="同じころ ― 和歌山・熊野の神社",
         captions=[(0.4, 6.0, "神話の[八咫烏]は残っていた", ["道案内をした、三本足のカラス", "サッカー日本代表のマークにも"])]),
    dict(name="c11_bench", frames=240,
         segs=segs((60, 6 * YEAR, 6 * YEAR + 3 * DAY), (60, 7 * YEAR, 7 * YEAR + 3 * DAY),
                   (60, 8 * YEAR, 8 * YEAR + 3 * DAY), (60, 9 * YEAR, 9 * YEAR + 3 * DAY)),
         loc="同じ公園（毎朝6時）",
         captions=[(0.3, 8.0, "雨の日も、[雪の日]も", ["おじいさんは同じベンチで", "パンくずをまき続けた"])]),
    dict(name="c12_return", frames=270, segs=segs((60, 10 * YEAR - 2.0, 10 * YEAR), (210, 10 * YEAR, 10 * YEAR + 7.0)),
         loc="同じ公園（10年後の同じ日、朝6時）",
         captions=[(2.4, 5.2, "朝6時、[黒い羽]が帰ってきた", ["消えたのと", "同じ日の、同じ時刻"]),
                   (5.2, 9.0, "クロ、[遅かったな]", ["10年ぶりの、いつもの朝ごはん"])]),
    dict(name="c13_end", frames=90, kind="end"),
]


def shot(name):
    return next(s for s in SHOTS if s["name"] == name)


def e_of(s, i):
    """i コマ目の経過秒と、その区間の倍速。"""
    k = 0
    for n, a, b in s["segs"]:
        if i < k + n:
            return a + (b - a) * (i - k) / n, (b - a) / (n / FPS)
        k += n
    n, a, b = s["segs"][-1]
    return b, (b - a) / (n / FPS)


def total_frames():
    return sum(s["frames"] for s in SHOTS)
