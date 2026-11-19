"""ショート120：夏休みの宿題 大体こうなる（テンポ系・11/19 ユーザー指定）。

python3 catmeme/short_120_shukudai.py → out/short_120_shukudai.mp4
- テンポ系：枠なし・右に日めくりカレンダー（自作の絵）＋宿題の進みぐあい・左に大きな猫・白い太字・59.9秒でなくてよい
- 8/25〜8/27 はハッピーハッピーハッピー猫を連打（同じ素材も毎回最初から・合計6秒以内）。
  8/28 とまどい・8/29 焦り・8/30 全力・8/31 諦め・9/1 怒られて泣く・9/2 全力・9/3 スマホ猫と踊る猫（11/19 ユーザー指定）
"""
import os

import world_short as Wd

ST = "bg19_kids_room"


def cuts():
    out = []
    for d in (25, 26, 27):   # 前半：同じ猫のまま日付だけ進む（ハッピー猫は合計6秒以内）
        c = Wd.split(ST, "8/%d" % d, left="joy_happy_happy_happy_cat", sound="L", dur=1.6, se="pi")
        c["cats"][0].update(x=270, h=640, w=520, bottom=1400)
        c.update(skit=True, pic=("pic_cal_8_%d" % d, 0.72), pic_cap="宿題\n0%", cat_cap="まだ\n余裕www")
        out.append(c)
    rows = [
        ("8/28", "pic_cal_8_28", "宿題\n0%", "confused_i_dont_know_cat", "あれ…？\nあと何日？"),
        ("8/29", "pic_cal_8_29", "宿題\nまだ0%", "scream_standing_marmot", "やばい\nやばい"),
        ("8/30", "pic_cal_8_30", "宿題\n30%", "work_typing_cat", "全力で\nやる"),
        ("8/31", "pic_cal_8_31", "宿題\n40%", "blank_black_cat_zoning_out", "もう\nむり"),
        ("9/1", "pic_cal_9_1", "提出日", "sad_banana_cat_cry", "先生に\n怒られた"),
        ("9/2", "pic_cal_9_2", "宿題\n60%", "work_typing_cat", "全力で\nやる"),
        ("9/3", "pic_cal_9_3", "宿題\n60%", "dance_filmed_by_gray_cat", "うおｗ"),
    ]
    for k, (lv, pic, rcap, cat, lcap) in enumerate(rows):
        big = k >= len(rows) - 3
        a = Wd.split(ST, lv, dur=0.7, se=["explosion_chudoon"] if big else ["pi"])
        b = Wd.split(ST, lv, left=cat, sound="L", dur=2.2, se="don_hit")
        b["cats"][0].update(x=270, h=640, w=520, bottom=1400)
        for c in (a, b):
            c.update(skit=True, pic=(pic, 0.72), pic_cap=rcap)
        b.update(pic_cont=True, cat_cap=lcap)
        out += [a, b]
    for c in out:
        c.update(blur=4, band_y=0, skit_bottom=1200, cat_cap_y=560, free_len=True, pic_right=True, pic_cap_below=True)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{r}夏休みの宿題", 132, Wd.BLACK, 100), ("{y}大体こうなる", 132, Wd.BLACK, 250)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_120_shukudai.mp4"), os.path.join(Wd.HERE, "out", "short_120_shukudai_preview"))
