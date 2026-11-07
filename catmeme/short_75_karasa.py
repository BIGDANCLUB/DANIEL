"""ショート75：日本vs世界 辛さレベル（world_short.py・段階でくらべる型・11/6 ユーザー指定：候補12番）。59.9秒。

python3 catmeme/short_75_karasa.py → out/short_75_karasa.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg47_ramen_shop"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1辛', 'calm_black_face_sheep', '甘い', 'sad_looking_away_tabby', 'ちょっと\n辛い'),
        ('2辛', 'stare_interviewer_cat', 'ふつう', 'eat_crunchy_cat_luna', '水を\n1杯'),
        ('3辛', 'eat_chips_cat', 'もう少し\n辛くして', 'peek_what_happen_cat', '汗が\n止まらない'),
        ('5辛', 'smug_squint_bicolor_cat', 'やっと\n辛くなってきた', 'realize_wet_cat_stare', 'ハンカチが\nびしょびしょ'),
        ('7辛', 'cocky_dj_cat', 'ちょうどいい', 'scream_phone_orange_cat', '店員さんに\n水を3杯'),
        ('10辛', 'happy_hamster_open_arms', 'おいしい', 'despair_dramatic_kitten', 'くちびるが\nたらこ'),
        ('20辛', 'dance_edm_cat', 'おかわり', 'blank_black_cat_zoning_out', '味が\nしない'),
        ('30辛', 'showoff_gojo_cosplay_cat', '激辛チャレンジ\n優勝', 'sleepy_old_memories_cat', '走馬灯が\n見える'),
        ('完食', 'joy_happy_happy_happy_cat', 'ふつうに\n完食', 'dance_filmed_by_gray_cat', '翌朝が\n本番'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}辛さレベル", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_75_karasa.mp4"), os.path.join(Wd.HERE, "out", "short_75_karasa_preview"))
