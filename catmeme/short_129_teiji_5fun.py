"""ショート129：定時5分前の気持ちww（テンポ系の短い型・11/21 ユーザー指定：短い型候補12番）。

python3 catmeme/short_129_teiji_5fun.py → out/short_129_teiji_5fun.mp4
- ベンチマークで出てきた16〜20秒の短い型（11/20 調査）。右に時計（自作の絵 tools/make_pic_clock.py）、左に大きな猫と白い太字
- 11/21 修正：上司のカットはとまどう猫・その後 19〜22時に叫ぶマーモット4カット（字幕ははみ出す「あああ…」）
- 1段1カット（札＝時刻）で次々に進む。同じ素材も毎回最初から。BGM なし
"""
import os

import world_short as Wd

ST = "bg25_office_desk"


def cuts():
    rows = [
        ("17:55", "pic_clock_1755", "work_typing_cat", "片付け\n開始"),
        ("17:56", "pic_clock_1756", "think_chin_paw_orange_cat", "PCの電源に\n手をかける"),
        ("17:57", "pic_clock_1757", "smug_squint_bicolor_cat", "上着を\n着る"),
        ("17:58", "pic_clock_1758", "stare_tabby_wide_eyes_cat", "カバンを\n持つ"),
        ("17:59", "pic_clock_1759", "stare_interviewer_cat", "出口を\n見つめる"),
        ("18:00", "pic_clock_1800", "happy_hamster_open_arms", "お先に\n失礼します！"),
        ("18:00", "pic_clock_1800", "confused_i_dont_know_cat", "上司\n「ちょっと\nいい？」"),
    ]
    out = []
    for k, (tm, pic, cat, cap) in enumerate(rows):
        c = Wd.split(ST, tm, left=cat, sound="L", dur=2.4, se=["explosion_chudoon"] if k == len(rows) - 1 else "pi")
        c["cats"][0].update(x=270, h=640, w=520, bottom=1400)
        c.update(skit=True, pic=(pic, 0.72), cat_cap=cap)
        out.append(c)
    for hh in (19, 20, 21, 22):   # 11/21 ユーザー指定：叫ぶマーモットが1回叫んだらすぐ次へ。字幕は画面に収まりきらない「あああ…」
        c = Wd.split(ST, "%d:00" % hh, left="scream_standing_marmot", sound="L", dur=1.2, se=None)
        c["cats"][0].update(x=270, h=640, w=520, bottom=1400)
        c.update(skit=True, pic=("pic_clock_%d00" % hh, 0.72), cat_cap="あ" * 20, cat_cap_over=True)
        out.append(c)
    for c in out:
        c.update(blur=4, band_y=0, skit_bottom=1200, cat_cap_y=560, free_len=True, pic_right=True)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{r}定時5分前{y}の", 132, Wd.BLACK, 100), ("{y}気持ちww", 132, Wd.BLACK, 250)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_129_teiji_5fun.mp4"), os.path.join(Wd.HERE, "out", "short_129_teiji_5fun_preview"))
