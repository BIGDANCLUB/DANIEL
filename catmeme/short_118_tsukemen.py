"""ショート118：つけ麺食べる時 大体こうなる（旧：つけ麺の量で変わる俺の反応）（新しい作風・11/18 ユーザー指定）。59.9秒。

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
    """11/18 ユーザー指定「テンポ系」：参考動画のように、同じ猫のまま右の絵だけテンポよく切りかえる。
    200〜400g はハムスター「余裕www」を出しっぱなし（素材も続けて再生）。500g からは段ごとに猫と字幕が替わる。59.9秒でなくてよい。"""
    out = []
    # 前半：同じ猫のまま絵だけ替わる
    ham, t0 = "happy_hamster_open_arms", 0.0
    for lv, sz, cap in [("200g", 0.85, "並盛"), ("300g", 0.95, "中盛"), ("400g", 1.05, "大盛")]:
        c = Wd.split(ST, lv, left=ham, sound="L", dur=1.6, se="pi")
        c["cats"][0].update(x=290, h=760, w=600, bottom=1250, ss=t0)
        c.update(skit=True, pic=(PIC, sz), pic_cap=cap, cat_cap="余裕www")
        out.append(c)
        t0 += 1.6
    # 後半：絵 → 猫とひとこと（少し早め）
    rows = [
        ("500g", PIC, 1.15, "特盛", "stare_tabby_wide_eyes_cat", "……思ったより\n多い"),
        ("600g", BIG, 1.15, "増量無料", "think_chin_paw_orange_cat", "無料なら\n頼むしかない"),
        ("700g", BIG, 1.25, "つけ汁が\n足りない", "despair_dramatic_kitten", "汁が先に\n尽きた"),
        ("800g", BIG, 1.35, "割りスープで\n延命", "sleepy_old_memories_cat", "麺と戦う意味を\n考え始める"),
        ("1kg", BIG, 1.5, "店員さん\n「大丈夫ですか？」", "scream_standing_marmot", "大丈夫じゃない"),
        ("完食", EMPTY, 1.15, "完食", "dance_filmed_by_gray_cat", "明日は\n1.2kg"),
    ]
    for k, (lv, pic, sz, rcap, cat, lcap) in enumerate(rows):
        big = k >= len(rows) - 3
        a = Wd.split(ST, lv, dur=0.7, se=["explosion_chudoon"] if big else ["pi"])
        b = Wd.split(ST, lv, left=cat, sound="L", dur=2.2, se="don_hit")
        b["cats"][0].update(x=290, h=760, w=600, bottom=1250)
        for c in (a, b):
            c.update(skit=True, pic=(pic, sz), pic_cap=rcap)
        b.update(pic_cont=True, cat_cap=lcap)
        out += [a, b]
    for c in out:
        c.update(blur=4, band_y=0, skit_bottom=1250, cat_cap_y=540, free_len=True)   # テンポ系：59.9秒でなくてよい
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{w}つけ麺{y}食べる時", 132, Wd.BLACK, 100), ("{y}大体こうなる", 132, Wd.BLACK, 250)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_118_tsukemen.mp4"), os.path.join(Wd.HERE, "out", "short_118_tsukemen_preview"))
