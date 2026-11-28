"""ショート119：平日のコンビニ夜ごはん 大体こうなる（テンポ系・11/19 ユーザー指定）。約25秒。

python3 catmeme/short_119_conbini_yoru.py → out/short_119_conbini_yoru.mp4
- テンポ系（118 つけ麺と同じ作り）：枠なし・右に透過の絵・左に大きな猫・白い太字・59.9秒でなくてよい
- 月曜は同じ猫「今週こそ健康www」を出したまま、右の絵だけテンポよく替える（同じ素材も毎回最初から）
- 絵は backgrounds/shorts_pic/ に置く（ユーザーが生成して送る）
"""
import os

import world_short as Wd

ST = "bg14_home_night"


def cuts():
    out = []
    # 前半：月曜は意識が高い（同じ猫のまま絵だけ替わる）
    for lv, pic, cap in [("月曜", "pic_cv_salad", "サラダ"), ("月曜", "pic_cv_chicken", "サラダ\nチキン"),
                         ("月曜", "pic_cv_veggie", "野菜\nジュース")]:
        c = Wd.split(ST, lv, left="smug_squint_bicolor_cat", sound="L", dur=1.6, se="pi")
        c["cats"][0].update(x=270, h=640, w=520, bottom=1400)
        c.update(skit=True, pic=(pic, 0.66), pic_cap=cap, cat_cap="今週こそ\n健康www")
        out.append(c)
    # 後半：日がたつほどくずれていく
    rows = [
        ("火曜", "pic_cv_onigiri", 0.68, "おにぎり\n2個", "think_chin_paw_orange_cat", "まあ\nお米も大事"),
        ("水曜", "pic_cv_bento", 0.70, "からあげ\n弁当", "work_typing_cat", "残業したから\nセーフ"),
        ("木曜", "pic_cv_cupmen", 0.72, "カップ麺", "sleepy_sleepy_cat", "もう何も\n考えたくない"),
        ("金曜", "pic_cv_beer", 0.74, "ビールと\nからあげ", "happy_girlfriend_dance_cat", "1週間の\nごほうび"),
        ("金曜23時", "pic_cv_ice", 0.75, "アイスも", "eat_crunchy_cat_luna", "ついでに\nもう1個"),
        ("土曜", "pic_cv_chicken", 0.76, "冷蔵庫に\nサラダチキン", "dance_filmed_by_gray_cat", "来週こそ\n健康www"),
    ]
    for k, (lv, pic, sz, rcap, cat, lcap) in enumerate(rows):
        big = k >= len(rows) - 3
        a = Wd.split(ST, lv, dur=0.7, se=["explosion_chudoon"] if big else ["pi"])
        b = Wd.split(ST, lv, left=cat, sound="L", dur=2.2, se="don_hit")
        b["cats"][0].update(x=270, h=640, w=520, bottom=1400)
        for c in (a, b):
            c.update(skit=True, pic=(pic, sz), pic_cap=rcap)
        b.update(pic_cont=True, cat_cap=lcap)
        out += [a, b]
    for c in out:
        c.update(blur=4, band_y=0, skit_bottom=1200, cat_cap_y=560, free_len=True, pic_right=True)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{r}コンビニ{y}夜ごはん", 132, Wd.BLACK, 100), ("{y}平日は大体こうなる", 120, Wd.BLACK, 250)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_119_conbini_yoru.mp4"), os.path.join(Wd.HERE, "out", "short_119_conbini_yoru_preview"))
