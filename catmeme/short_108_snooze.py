"""ショート108：スヌーズを押した回数別（world_short.py・段階でくらべる型・11/15 ユーザー指定：候補29番）。59.9秒。

python3 catmeme/short_108_snooze.py → out/short_108_snooze.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/15 一覧で確認）
- 概要欄の注意：※よくあるイメージです。BGM なし
"""
import os

import world_short as Wd

ST = 'bg02_room'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('0回', 'happy_hamster_open_arms', '1回で\n起きる', 'scream_phone_orange_cat', 'アラーム\n鳴る'),
        ('1回', 'work_typing_cat', '朝活', 'sleepy_sleepy_cat', 'あと5分'),
        ('2回', 'read_book_orange_kitten', '読書', 'sleep_sleeping_cat', 'あと5分'),
        ('3回', 'smug_squint_bicolor_cat', '朝ごはん', 'sleepy_old_memories_cat', '夢の続きを\n見る'),
        ('4回', 'cocky_dj_cat', 'ストレッチ', 'stare_tabby_wide_eyes_cat', '時計を見て\n二度見'),
        ('5回', 'rizz_cat_rizz', 'コーヒー', 'surprise_big_pupils_cat', '家を出る\n10分前'),
        ('6回', 'stare_aloha_gray_cat', '余裕の出発', 'scream_standing_marmot', '顔だけ\n洗って\nダッシュ'),
        ('7回', 'dance_cute_dog', '駅で\nのんびり', 'despair_dramatic_kitten', '電車が\n目の前で\n出発'),
        ('10回', 'dance_filmed_by_gray_cat', '優雅な朝', 'blank_black_cat_zoning_out', '起きたら\n昼'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('現実', '理想'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}スヌーズを", 96, Wd.BLACK, 95), ("{y}押した回数別", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_108_snooze.mp4"), os.path.join(Wd.HERE, "out", "short_108_snooze_preview"))
