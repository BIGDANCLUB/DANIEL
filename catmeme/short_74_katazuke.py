"""ショート74：休日の部屋の片づけ（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補38番）。59.9秒。

python3 catmeme/short_74_katazuke.py → out/short_74_katazuke.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg02_room"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('5分', 'work_typing_cat', '机の上を\n片づける', 'slack_nail_filing_cat', '順調'),
        ('10分', 'calm_black_face_sheep', '引き出しも', 'think_chin_paw_orange_cat', '引き出しを\n開ける'),
        ('15分', 'happy_chipi_chapa_cat', 'いらない物を\n捨てる', 'read_book_orange_kitten', '昔の手紙を\n見つける'),
        ('30分', 'money_counting_orange_cat', '本棚を\n整理', 'sleepy_old_memories_cat', '卒業アルバムを\n見つける'),
        ('1時間', 'cocky_dj_cat', 'クローゼットへ', 'sad_banana_cat_cry', 'アルバムを\n読んで泣く'),
        ('2時間', 'happy_hamster_open_arms', '部屋が\nピカピカ', 'eat_pop_cat', '昔の友だちに\nLINE'),
        ('3時間', 'dance_three_kittens', 'ゴミ出し\n完了', 'despair_dramatic_kitten', '床が物で\nいっぱい'),
        ('夜', 'sleep_sleeping_cat', 'スッキリ\n寝る', 'blank_black_cat_zoning_out', '出した物の\n上で寝る'),
        ('次の日', 'showoff_gojo_cosplay_cat', 'きれいな\n部屋', 'stare_tabby_wide_eyes_cat', 'もっと\n散らかっている'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('予定', '実際'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}休日の", 96, Wd.BLACK, 95), ("{y}部屋の片づけ", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_74_katazuke.mp4"), os.path.join(Wd.HERE, "out", "short_74_katazuke_preview"))
