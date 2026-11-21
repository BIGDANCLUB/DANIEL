"""ショート128：夫vs妻　休日の朝（world_short.py・段階でくらべる型・11/21 ユーザー指定：男女型候補12番）。59.9秒。

python3 catmeme/short_128_kyujitsu_fufu.py → out/short_128_kyujitsu_fufu.mp4
- ベンチマークで伸びている「男女の比べっこ」型（11/20 調査）。ほのぼのにある題材とは被らないものを選んだ
- 札は時刻。右＝妻、左＝夫
- 段階ごとに「札だけ → 右の猫（妻）→ 左の猫（夫）」の3段。どちらもけなさない、よくあるイメージ。BGM なし
"""
import os

import world_short as Wd

ST = 'bg02_room'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫＝妻, 右の説明, 左の猫＝夫, 左の説明)
    rows = [
        ('6:00', 'work_typing_cat', '洗濯機\nまわす', 'stare_lying_tabby_cat', '爆睡'),
        ('7:00', 'dance_cute_dog', '朝ごはん\n作る', 'calm_black_face_sheep', '寝返り'),
        ('8:00', 'listen_dancing_dog', '掃除機\nかける', 'stare_tabby_wide_eyes_cat', 'うるさくて\n起きかける'),
        ('9:00', 'think_chin_paw_orange_cat', '買い出しの\nリスト作り', 'blank_black_cat_zoning_out', '二度寝'),
        ('10:00', 'cocky_dj_cat', '洗濯物\n干し終わる', 'happy_hamster_open_arms', '起床'),
        ('10:30', 'stare_interviewer_cat', 'お茶で\nひと息', 'smug_squint_bicolor_cat', '朝ごはん\nある？'),
        ('11:00', 'glare_disgusted_cat', '笑顔が\n消える', 'confused_i_dont_know_cat', '何か\n手伝おうか？'),
        ('11:30', 'rizz_cat_rizz', 'もう\n終わった', 'scream_phone_orange_cat', 'えっ'),
        ('12:00', 'money_counting_orange_cat', 'お昼\nどうする？', 'dance_edm_cat', '今日は\n何しよう？'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('夫', '妻'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}夫vs妻", 96, Wd.BLACK, 95), ("{y}休日の朝", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_128_kyujitsu_fufu.mp4"), os.path.join(Wd.HERE, "out", "short_128_kyujitsu_fufu_preview"))
