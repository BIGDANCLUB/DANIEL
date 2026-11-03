"""ショート67：日本vs世界 ゴミの分別（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補12番）。59.9秒。

python3 catmeme/short_67_gomi.py → out/short_67_gomi.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg48_clean_street"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1種類', 'slack_nail_filing_cat', 'ぜんぶ\nいっしょ', 'stare_big_eyes_tabby_kitten', 'ありえない'),
        ('2種類', 'calm_black_face_sheep', 'ゴミと\nリサイクル', 'think_chin_paw_orange_cat', '燃える・\n燃えない'),
        ('3種類', 'glare_disgusted_cat', '多すぎる', 'work_typing_cat', 'ペットボトルは\n別'),
        ('5種類', 'confused_i_dont_know_cat', '意味が\nわからない', 'read_book_orange_kitten', 'ラベルと\nキャップも\nはがす'),
        ('10種類', 'leave_cat_leaves_home', '引っ越す', 'happy_chipi_chapa_cat', 'ふつう'),
        ('20種類', 'surprise_big_pupils_cat', '研究所\nみたい', 'money_counting_orange_cat', '分別表を\n冷蔵庫に貼る'),
        ('40種類以上', 'scream_standing_marmot', 'ゴミの\n大学', 'dance_three_kittens', '町が\n有名になる'),
        ('日をまちがえた', 'sleep_sleeping_cat', '誰も\n気にしない', 'despair_dramatic_kitten', '黄色い紙が\n貼られる'),
        ('収集日の朝', 'drive_driving_cat', 'いつでも\n出せる', 'stare_tabby_wide_eyes_cat', 'カラスとの\n戦い'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}ゴミの分別", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_67_gomi.mp4"), os.path.join(Wd.HERE, "out", "short_67_gomi_preview"))
