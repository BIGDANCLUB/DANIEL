"""ショート103：日本vs世界　出張の過ごし方（world_short.py・段階でくらべる型・11/15 ユーザー指定：候補3番）。59.9秒。

python3 catmeme/short_103_shucchou.py → out/short_103_shucchou.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/15 一覧で確認）
- 概要欄の注意：※目安です（よくあるイメージで、実際の統計ではありません）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg53_shinkansen'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('前日', 'cocky_dj_cat', '観光地を\n調べる', 'work_typing_cat', '資料を\n3回見直す'),
        ('移動', 'dance_cute_dog', '映画を\n見る', 'stare_tabby_wide_eyes_cat', '新幹線で\nパソコン'),
        ('到着', 'happy_hamster_open_arms', 'まず\nランチ', 'think_chin_paw_orange_cat', '手土産を\n買う'),
        ('商談', 'rizz_cat_rizz', '30分で\n終わる', 'stare_lying_tabby_cat', '名刺交換で\n15分'),
        ('夕方', 'listen_dancing_dog', 'ホテルの\nプールへ', 'read_book_orange_kitten', '経費の\n領収書を整理'),
        ('夜', 'smug_squint_bicolor_cat', '現地の\nバーへ', 'sad_looking_away_tabby', '接待の\n2次会'),
        ('ホテル', 'stare_aloha_gray_cat', 'ぐっすり', 'scream_phone_orange_cat', '明日の\n資料を直す'),
        ('帰り', 'happy_chipi_chapa_cat', '観光して\n帰る', 'sleep_sleeping_cat', '新幹線で\n爆睡'),
        ('翌日', 'dance_filmed_by_gray_cat', '休み', 'blank_black_cat_zoning_out', '朝から\n報告書'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}出張の過ごし方", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_103_shucchou.mp4"), os.path.join(Wd.HERE, "out", "short_103_shucchou_preview"))
