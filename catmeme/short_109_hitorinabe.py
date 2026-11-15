"""ショート109：ひとり鍋の理想と現実（world_short.py・段階でくらべる型・11/15 ユーザー指定：候補21番）。59.9秒。

python3 catmeme/short_109_hitorinabe.py → out/short_109_hitorinabe.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/15 一覧で確認）
- 概要欄の注意：※よくあるイメージです。BGM なし
"""
import os

import world_short as Wd

ST = 'bg14_home_night'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('買い物', 'read_book_orange_kitten', '1人分の\n野菜だけ', 'money_counting_orange_cat', '白菜\n丸ごと'),
        ('準備', 'work_typing_cat', '土鍋を\n出す', 'think_chin_paw_orange_cat', '鍋つゆが\n4人前'),
        ('1日目', 'happy_hamster_open_arms', '具だくさん\n寄せ鍋', 'eat_pop_cat', 'うまい'),
        ('2日目', 'cocky_dj_cat', 'しめの\n雑炊', 'stare_lying_tabby_cat', 'まだ白菜が\n半分'),
        ('3日目', 'smug_squint_bicolor_cat', 'キムチ鍋', 'sad_looking_away_tabby', '同じ鍋'),
        ('4日目', 'rizz_cat_rizz', '豆乳鍋', 'calm_black_face_sheep', 'カレーに\n変える'),
        ('5日目', 'dance_cute_dog', 'トマト鍋', 'stare_tabby_wide_eyes_cat', 'まだ\n白菜がある'),
        ('1週間', 'stare_aloha_gray_cat', '鍋パーティー', 'despair_dramatic_kitten', '白菜の夢を\n見る'),
        ('結局', 'dance_filmed_by_gray_cat', 'ひとり鍋\n最高', 'happy_chipi_chapa_cat', '白菜に\n勝てない'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}ひとり鍋の", 96, Wd.BLACK, 95), ("{y}理想と現実", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_109_hitorinabe.mp4"), os.path.join(Wd.HERE, "out", "short_109_hitorinabe_preview"))
