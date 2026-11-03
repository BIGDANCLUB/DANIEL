"""ショート66：日本vs世界 ランチ代の感覚（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補8番）。59.9秒。

python3 catmeme/short_66_lunch.py → out/short_66_lunch.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg15_convenience"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('300円', 'surprise_big_pupils_cat', '安すぎて\n不安', 'happy_chipi_chapa_cat', 'おにぎり\n2個'),
        ('500円', 'stare_interviewer_cat', 'コーヒー\n1杯', 'eat_pop_cat', 'ワンコイン\n弁当'),
        ('800円', 'sad_looking_away_tabby', 'サンドイッチ\nだけ', 'eat_crunchy_cat_luna', '日替わり\n定食'),
        ('1000円', 'think_chin_paw_orange_cat', 'ふつうの\nランチ', 'glare_disgusted_cat', 'ちょっと\n高い'),
        ('1500円', 'calm_black_face_sheep', 'まだ\nふつう', 'despair_dramatic_kitten', 'ぜいたく\nすぎる'),
        ('2000円', 'money_counting_orange_cat', 'ハンバーガー\nセット', 'scream_phone_orange_cat', 'ボーナスの\n日だけ'),
        ('3000円', 'cocky_dj_cat', 'ちょっと\nいいランチ', 'blank_black_cat_zoning_out', '会社の\n経費'),
        ('5000円', 'dance_three_kittens', '記念日', 'sad_banana_cat_cry', '月の食費が\n消える'),
        ('次の日', 'happy_hamster_open_arms', 'また\nランチ', 'sulk_hungry_cat', 'もやし\n生活'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('日本', '世界'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}ランチ代の感覚", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_66_lunch.mp4"), os.path.join(Wd.HERE, "out", "short_66_lunch_preview"))
