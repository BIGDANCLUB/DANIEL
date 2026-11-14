"""ショート63：日本vs世界 行列にどこまで並ぶ？（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補1番）。59.9秒。

python3 catmeme/short_63_gyouretsu.py → out/short_63_gyouretsu.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
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
        ('5分', 'slack_nail_filing_cat', 'ふつうに\n並ぶ', 'stare_interviewer_cat', 'ふつうに\n並ぶ'),
        ('15分', 'glare_disgusted_cat', 'ちょっと\n長い', 'calm_black_face_sheep', 'まだまだ\nこれから'),
        ('30分', 'leave_cat_leaves_home', '帰る', 'read_book_orange_kitten', 'スマホで\n時間をつぶす'),
        ('1時間', 'rage_talking_cat', 'お店に\n文句を言う', 'think_chin_paw_orange_cat', '並んだぶん\nおいしいはず'),
        ('2時間', 'drive_driving_cat', '別のお店へ\n行く', 'sleepy_sleepy_cat', '立ったまま\n寝る'),
        ('3時間', 'surprise_big_pupils_cat', '意味が\nわからない', 'happy_hamster_open_arms', '達成感が\nすごい'),
        ('5時間', 'fight_cat_fight', '大さわぎ', 'work_typing_cat', '整理券が\n配られる'),
        ('徹夜', 'scream_standing_marmot', '警察を\n呼ぶ', 'dance_three_kittens', 'テントを\n張る'),
        ('先頭に着いた', 'confused_i_dont_know_cat', 'なんの\nお店だっけ', 'blank_black_cat_zoning_out', '何の行列か\n知らずに\n並んでいた'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}行列の待ち時間", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_63_gyouretsu.mp4"), os.path.join(Wd.HERE, "out", "short_63_gyouretsu_preview"))
