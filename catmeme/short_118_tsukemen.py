"""ショート118：つけ麺の量で変わる俺の反応（新しい作風・11/18 ユーザー指定）。59.9秒。

python3 catmeme/short_118_tsukemen.py → out/short_118_tsukemen.mp4
- 右：つけ麺のイラスト（量が増えるほど大きく）＋字幕。左：猫ミーム1匹＋猫のひとこと（寸劇）
- 1段：右の写真と字幕が出る → 左の猫とひとことが出る（右の字幕は出したまま）
- 写真はユーザー提供の3枚（ふつう・山盛り・完食）。BGM なし
"""
import os

import world_short as Wd

ST = "bg47_ramen_shop"
PIC, BIG, EMPTY = "pic_tsukemen", "pic_tsukemen_big", "pic_tsukemen_empty"
K = 59.9 / 54.0


def cuts():
    out = []
    # (札, 写真, 大きさ, 右の字幕, 左の猫, 左のひとこと)
    rows = [
        ("200g", PIC, 0.8, "並盛", "happy_hamster_open_arms", "ちょうどいい"),
        ("300g", PIC, 0.85, "中盛", "cocky_dj_cat", "今日はがんばった日\nだから"),
        ("400g", PIC, 0.9, "大盛", "smug_squint_bicolor_cat", "余裕です"),
        ("500g", PIC, 0.95, "特盛", "stare_tabby_wide_eyes_cat", "……思ったより\n多い"),
        ("600g", BIG, 1.0, "増量無料", "think_chin_paw_orange_cat", "無料なら\n頼むしかない"),
        ("700g", BIG, 1.05, "つけ汁が\n足りない", "despair_dramatic_kitten", "汁が先に\n尽きた"),
        ("800g", BIG, 1.1, "割りスープで\n延命", "sleepy_old_memories_cat", "麺と戦う意味を\n考え始める"),
        ("1kg", BIG, 1.2, "店員さん\n「大丈夫ですか？」", "scream_standing_marmot", "大丈夫じゃない"),
        ("完食", EMPTY, 0.9, "完食", "dance_filmed_by_gray_cat", "明日は\n1.2kg"),
    ]
    for k, (lv, pic, sz, rcap, cat, lcap) in enumerate(rows):   # 11/18 ユーザー指定：枠なし・ネイルサロンの参考の配置
        big = k >= len(rows) - 4
        a = Wd.split(ST, lv, dur=2.4 * K, se=["explosion_chudoon"] if big else ["pi"])
        b = Wd.split(ST, lv, left=cat, sound="L", dur=3.6 * K, se="don_hit")
        b["cats"][0].update(x=290, h=760, w=600, bottom=1360)
        for c in (a, b):
            c.update(skit=True, pic=(pic, sz), pic_cap=rcap)
        b.update(pic_cont=True, cat_cap=lcap)
        out += [a, b]
    for c in out:
        c.update(blur=4, band_y=0)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}つけ麺の量で", 96, Wd.BLACK, 95), ("{y}変わる俺の反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_118_tsukemen.mp4"), os.path.join(Wd.HERE, "out", "short_118_tsukemen_preview"))
