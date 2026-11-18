"""「もしもカラスが消えたら？」の時間割（30fps、59.9秒＝1797コマに固定）。よねあぷ型：
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
    dict(name="c02_wire", frames=90, segs=segs((90, 0.0, 3.0)), loc="同じ瞬間 ― 東京・新宿の電線",
         captions=[(0.3, 3.0, "日本中のカラスが、消えた", ["ハシブトガラスもハシボソガラスも", "ぜんぶ消えた"])]),
    dict(name="c03_quiet", frames=90, segs=segs((90, 3.0, 6.6)), loc="東京・新宿の公園（朝6時）",
         captions=[(0.2, 3.0, "カーカーが聞こえない", ["朝の鳴き声が、街から消えた"])]),
    dict(name="c04_garbage", frames=120, segs=segs((120, 1 * DAY + 60, 1 * DAY + 300)), card="次の朝",
         loc="東京・新宿のゴミ置き場（朝7時）",
         captions=[(0.9, 4.0, "ゴミが散らからない", ["ゴミ袋を破るカラスが", "いなくなった"])]),
    dict(name="c05_orchard", frames=120, segs=segs((120, 3 * DAY + 4 * 3600, 3 * DAY + 4 * 3600 + 12000)), card="3日後",
         loc="長野・りんご畑",
         captions=[(0.9, 4.0, "畑の被害が消えた", ["カラスによる農作物の被害は", "全国で年 約13億円（2022年度）"])]),
    dict(name="c06_road", frames=165, segs=segs((165, 7 * DAY + 8 * 3600, 7 * DAY + 8 * 3600 + 16500)), card="1週間後",
         loc="国道沿い（8月）",
         captions=[(0.9, 3.0, "死がいが片付かない", ["道で死んだ動物を", "カラスが食べて片付けていた"]),
                   (3.0, 5.5, "くさる時のガスが出る", ["アンモニアや硫化水素", "そのにおいが、ハエを呼ぶ"])]),
    dict(name="c07_flies", frames=135, segs=segs((135, 30 * DAY + 9 * 3600, 30 * DAY + 9 * 3600 + 45000)), card="1か月後",
         loc="東京・住宅街",
         captions=[(0.9, 4.5, "ハエが大発生", ["卵から約2週間で成虫に", "1匹が数百個の卵を産む"])]),
    dict(name="c08_rats", frames=120, segs=segs((120, 90 * DAY + 16 * 3600, 90 * DAY + 16 * 3600 + 2400)), card="3か月後",
         loc="東京・新宿のゴミ置き場（夜10時）",
         captions=[(0.9, 4.0, "ネズミが増えた", ["カラスと取り合っていた生ゴミを", "ネズミがひとり占め"])]),
    dict(name="c09_birds", frames=120, segs=segs((120, 182 * DAY + 3 * 3600, 182 * DAY + 3 * 3600 + 120000)), card="半年後",
         loc="静岡・キャベツ畑",
         captions=[(0.9, 4.0, "今度は小鳥が畑を荒らす", ["カラスに食べられていた卵やヒナが育ち", "ヒヨドリが増えた"])]),
    dict(name="c10_book", frames=135, segs=segs((135, 5 * YEAR + 10 * 3600, 5 * YEAR + 10 * 3600 + 450)), card="5年後",
         loc="東京・おじいさんの家",
         captions=[(1.0, 4.5, "これ、なあに？", ["♪からすといっしょに かえりましょう", "その鳥を、見たことがない"])]),
    dict(name="c11_bench", frames=180,
         segs=segs((45, 6 * YEAR, 6 * YEAR + 3 * DAY), (45, 7 * YEAR, 7 * YEAR + 3 * DAY),
                   (45, 8 * YEAR, 8 * YEAR + 3 * DAY), (45, 9 * YEAR, 9 * YEAR + 3 * DAY)),
         loc="同じ公園（毎朝6時）",
         captions=[(0.3, 6.0, "毎朝、同じベンチで", ["おじいさんはパンくずをまいた", "クロは、あの日から来ていない"])]),
    dict(name="c12_return", frames=270, segs=segs((60, 10 * YEAR - 2.0, 10 * YEAR), (210, 10 * YEAR, 10 * YEAR + 7.0)),
         loc="同じ公園（10年後の同じ日、朝6時）",
         captions=[(2.4, 5.2, "カラスがもどってきた！", ["カラスたちにとっては", "1秒もたっていない"]),
                   (5.2, 9.0, "おかえり", ["10年、待っていた"])]),
    dict(name="c13_end", frames=72, kind="end"),
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


TOTAL = 1797      # 59.9秒に固定（ユーザー指定）


def total_frames():
    return sum(s["frames"] for s in SHOTS)
