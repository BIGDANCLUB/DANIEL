"""ショート106：年代別　お酒の飲み方（world_short.py・段階でくらべる型・11/15 ユーザー指定：候補13番）。59.9秒。

python3 catmeme/short_106_osake.py → out/short_106_osake.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/15 一覧で確認）
- 概要欄の注意：※よくあるイメージです　※お酒は20歳になってから。BGM なし
"""
import os

import world_short as Wd

ST = 'bg13_izakaya'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('20代', 'dance_cute_dog', 'とりあえず\n生', 'cocky_dj_cat', '朝まで\nオール'),
        ('25歳', 'happy_hamster_open_arms', 'ハイボール', 'listen_dancing_dog', '飲み放題で\nもとをとる'),
        ('30代', 'work_typing_cat', '缶ビール\n1本', 'rizz_cat_rizz', '昼から\nクラフトビール'),
        ('35歳', 'think_chin_paw_orange_cat', 'ノンアル', 'smug_squint_bicolor_cat', '日本酒を\n少しずつ'),
        ('40代', 'stare_lying_tabby_cat', '糖質ゼロ', 'stare_aloha_gray_cat', 'ワインを\n1本'),
        ('50代', 'calm_black_face_sheep', '休肝日', 'read_book_orange_kitten', 'いい焼酎を\nお湯割りで'),
        ('60代', 'sleepy_old_memories_cat', '晩酌\n1杯', 'sleepy_sleepy_cat', '夕方4時から\n晩酌'),
        ('70代', 'sad_looking_away_tabby', '医者に\n止められる', 'huh_huh_cat', 'こっそり\n1杯'),
        ('100歳', 'showoff_gojo_cosplay_cat', 'とりあえず\n生', 'dance_filmed_by_gray_cat', 'とりあえず\n生'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('休日', '平日'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}年代別", 96, Wd.BLACK, 95), ("{y}お酒の飲み方", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_106_osake.mp4"), os.path.join(Wd.HERE, "out", "short_106_osake_preview"))
