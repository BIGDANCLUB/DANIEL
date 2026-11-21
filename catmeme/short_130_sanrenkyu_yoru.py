"""ショート130：3連休の最終日の夜ww（テンポ系の短い型・11/21 ユーザー指定：短い型候補13番）。

python3 catmeme/short_130_sanrenkyu_yoru.py → out/short_130_sanrenkyu_yoru.mp4
- ベンチマークで出てきた16〜20秒の短い型（11/20 調査）。右に時計（自作の絵 tools/make_pic_clock.py）、左に大きな猫と白い太字
- 1段1カット（札＝時刻）で次々に進む。同じ素材も毎回最初から。BGM なし
"""
import os

import world_short as Wd

ST = "bg14_home_night"


def cuts():
    rows = [
        ("18:00", "pic_clock_1800n", "happy_hamster_open_arms", "まだ\n6時間ある"),
        ("20:00", "pic_clock_2000n", "calm_black_face_sheep", "準備は\nあとで"),
        ("21:00", "pic_clock_2100n", "confused_i_dont_know_cat", "何もしてない\nことに気づく"),
        ("22:00", "pic_clock_2200n", "despair_dramatic_kitten", "休みを\n返して"),
        ("23:00", "pic_clock_2300n", "stare_lying_tabby_cat", "スマホが\nやめられない"),
        ("23:59", "pic_clock_2359n", "blank_black_cat_zoning_out", "寝たら\n明日が来る"),
        ("0:00", "pic_clock_0000n", "sad_banana_cat_cry", "火曜日…"),
    ]
    out = []
    for k, (tm, pic, cat, cap) in enumerate(rows):
        c = Wd.split(ST, tm, left=cat, sound="L", dur=2.4, se=["explosion_chudoon"] if k == len(rows) - 1 else "pi")
        c["cats"][0].update(x=270, h=640, w=520, bottom=1400)
        c.update(skit=True, pic=(pic, 0.72), cat_cap=cap)
        out.append(c)
    for c in out:
        c.update(blur=4, band_y=0, skit_bottom=1200, cat_cap_y=560, free_len=True, pic_right=True)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{r}3連休{y}最終日の夜", 110, Wd.BLACK, 100), ("{y}大体こうなるww", 120, Wd.BLACK, 250)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_130_sanrenkyu_yoru.mp4"), os.path.join(Wd.HERE, "out", "short_130_sanrenkyu_yoru_preview"))
