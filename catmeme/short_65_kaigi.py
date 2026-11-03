"""ショート65：日本vs世界 会議の長さ（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補7番）。59.9秒。

python3 catmeme/short_65_kaigi.py → out/short_65_kaigi.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg25_office_desk"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('5分', 'slack_nail_filing_cat', 'もう\n終わり', 'stare_interviewer_cat', 'まだ\nあいさつ中'),
        ('15分', 'money_counting_orange_cat', '決めて\n解散', 'read_book_orange_kitten', '資料の\n読み合わせ'),
        ('30分', 'glare_disgusted_cat', '長すぎる', 'sleepy_old_memories_cat', '前回の\nおさらい'),
        ('1時間', 'leave_cat_leaves_home', '途中で\n帰る', 'think_chin_paw_orange_cat', '結論は\n次回へ'),
        ('2時間', 'rage_talking_cat', '抗議する', 'sleepy_sleepy_cat', '目を開けたまま\n寝る'),
        ('3時間', 'surprise_big_pupils_cat', '残業代を\n請求', 'work_dog_staring_computer', '内職を\nはじめる'),
        ('半日', 'fight_cat_fight', 'ストライキ', 'despair_dramatic_kitten', '会議のための\n会議'),
        ('1日', 'scream_standing_marmot', '会社が\nつぶれる', 'stare_tabby_wide_eyes_cat', '議事録が\n10ページ'),
        ('終わったら', 'happy_hamster_open_arms', 'すぐ\n実行', 'blank_black_cat_zoning_out', '何が決まったか\n誰も知らない'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}会議の長さ", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_65_kaigi.mp4"), os.path.join(Wd.HERE, "out", "short_65_kaigi_preview"))
