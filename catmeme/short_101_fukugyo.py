"""ショート101：副業の理想と現実（world_short.py・段階でくらべる型・11/14 ユーザー指定：お金ショート候補23番）。59.9秒。

python3 catmeme/short_101_fukugyo.py → out/short_101_fukugyo.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/13 一覧を取り直して確認）
- よくあるイメージです。BGM なし
"""
import os

import world_short as Wd

ST = 'bg14_home_night'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1日目', 'work_typing_cat', '副業を\nはじめる', 'read_book_orange_kitten', '副業の本を\n買う'),
        ('1週間', 'cocky_dj_cat', '月5万円\n達成', 'think_chin_paw_orange_cat', '何をやるか\nまだ考えてる'),
        ('1か月', 'rizz_cat_rizz', '月10万円', 'stare_lying_tabby_cat', '初収入\n120円'),
        ('3か月', 'smug_squint_bicolor_cat', '本業より\n楽しい', 'sleepy_old_memories_cat', '本業で\nねむい'),
        ('半年', 'dance_cute_dog', '月30万円', 'money_counting_orange_cat', '道具代で\n赤字'),
        ('1年', 'showoff_gojo_cosplay_cat', '会社を\nやめる', 'sad_looking_away_tabby', '確定申告が\nわからない'),
        ('1年半', 'stare_aloha_gray_cat', '自由な\n生活', 'despair_dramatic_kitten', '副業の副業を\n探す'),
        ('2年', 'happy_chipi_chapa_cat', '大成功', 'calm_black_face_sheep', '合計の利益\n3000円'),
        ('結局', 'listen_dancing_dog', '人生最高', 'dance_filmed_by_gray_cat', '本業が\nいちばん\nえらい'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}副業の", 96, Wd.BLACK, 95), ("{y}理想と現実", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_101_fukugyo.mp4"), os.path.join(Wd.HERE, "out", "short_101_fukugyo_preview"))
