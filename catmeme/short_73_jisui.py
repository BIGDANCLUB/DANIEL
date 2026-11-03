"""ショート73：ひとり暮らし 自炊の理想と現実（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補36番）。59.9秒。

python3 catmeme/short_73_jisui.py → out/short_73_jisui.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "st02_home_kitchen"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1日目', 'showoff_gojo_cosplay_cat', 'スパイスから\nカレー', 'happy_chipi_chapa_cat', '本当に\n作った'),
        ('2日目', 'cocky_dj_cat', 'パスタを\n手作り', 'eat_crunchy_cat_luna', 'カレーの\n残り'),
        ('3日目', 'happy_hamster_open_arms', '作り置き\n5品', 'eat_pop_cat', 'カレー\nうどん'),
        ('1週間', 'read_book_orange_kitten', '栄養バランス\n完ぺき', 'think_chin_paw_orange_cat', '野菜炒め'),
        ('2週間', 'calm_black_face_sheep', '週末に\nまとめて料理', 'sleepy_sleepy_cat', 'もやし\n炒め'),
        ('3週間', 'money_counting_orange_cat', '食費が\n半分に', 'sad_looking_away_tabby', '卵かけ\nごはん'),
        ('1か月', 'dance_three_kittens', '料理が\n趣味に', 'despair_dramatic_kitten', '冷蔵庫に\nソースだけ'),
        ('2か月', 'happy_girlfriend_dance_cat', '友だちを\n呼ぶ', 'scream_phone_orange_cat', '出前アプリ'),
        ('半年', 'surprise_big_pupils_cat', '料理教室へ', 'blank_black_cat_zoning_out', 'スパイスが\n賞味期限切れ'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}ひとり暮らし", 96, Wd.BLACK, 95), ("{y}自炊の理想と現実", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_73_jisui.mp4"), os.path.join(Wd.HERE, "out", "short_73_jisui_preview"))
