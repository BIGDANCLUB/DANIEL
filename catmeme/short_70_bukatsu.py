"""ショート70：日本vs世界 部活と放課後（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補24番）。59.9秒。

python3 catmeme/short_70_bukatsu.py → out/short_70_bukatsu.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg30_classroom_desk"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('朝6時', 'sleep_sleeping_cat', '寝ている', 'walk_white_duck', '朝練'),
        ('授業の前', 'eat_pop_cat', '朝ごはん', 'stare_tabby_wide_eyes_cat', 'グラウンド\n整備'),
        ('放課後', 'drive_driving_cat', '家に\n帰る', 'work_typing_cat', '部活\nスタート'),
        ('夕方', 'cocky_dj_cat', '習い事', 'despair_dramatic_kitten', '走りこみ'),
        ('夜7時', 'dance_happy_banana_cat', '家族と\n夕食', 'sulk_hungry_cat', 'やっと\n帰る'),
        ('土曜日', 'happy_chipi_chapa_cat', '遊びに\n行く', 'stare_interviewer_cat', '練習試合'),
        ('日曜日', 'calm_black_face_sheep', 'のんびり', 'sad_looking_away_tabby', '大会'),
        ('夏休み', 'dance_three_kittens', '2か月\n休み', 'scream_phone_orange_cat', '合宿'),
        ('引退', 'surprise_big_pupils_cat', '何を？', 'sad_banana_cat_cry', 'あゝ\n青春'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}部活と放課後", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_70_bukatsu.mp4"), os.path.join(Wd.HERE, "out", "short_70_bukatsu_preview"))
