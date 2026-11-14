"""ショート102：コンビニコーヒーを毎日買うと（world_short.py・段階でくらべる型・11/14 ユーザー指定：お金ショート候補24番）。59.9秒。

python3 catmeme/short_102_coffee.py → out/short_102_coffee.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/13 一覧を取り直して確認）
- 目安です（平日だけ1日1杯、コンビニ250円・水筒30円で計算）。BGM なし
"""
import os

import world_short as Wd

ST = 'st03_konbini'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1杯', 'happy_hamster_open_arms', '1杯\n約30円', 'eat_crunchy_cat_luna', '1杯\n約250円'),
        ('1週間', 'work_typing_cat', '150円', 'stare_tabby_wide_eyes_cat', '1250円'),
        ('1か月', 'smug_squint_bicolor_cat', '600円', 'think_chin_paw_orange_cat', '5000円'),
        ('半年', 'cocky_dj_cat', '3600円', 'stare_lying_tabby_cat', '3万円'),
        ('1年', 'rizz_cat_rizz', '7200円', 'surprise_big_pupils_cat', '6万円'),
        ('5年', 'stare_aloha_gray_cat', '3万6000円', 'money_counting_orange_cat', '30万円'),
        ('10年', 'dance_cute_dog', '7万2000円', 'scream_standing_marmot', '60万円'),
        ('30年', 'showoff_gojo_cosplay_cat', '21万6000円', 'despair_dramatic_kitten', '180万円'),
        ('でも', 'happy_chipi_chapa_cat', '水筒\nなくした', 'dance_filmed_by_gray_cat', '朝の1杯は\nプライスレス'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('毎日買う', '水筒'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}コンビニコーヒーを", 96, Wd.BLACK, 95), ("{y}毎日買うと", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_102_coffee.mp4"), os.path.join(Wd.HERE, "out", "short_102_coffee_preview"))
