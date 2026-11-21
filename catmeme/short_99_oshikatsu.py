"""ショート99：年代別　推し活の出費（world_short.py・段階でくらべる型・11/14 ユーザー指定：お金ショート候補12番）。59.9秒。

python3 catmeme/short_99_oshikatsu.py → out/short_99_oshikatsu.mp4
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
        ('10代', 'dance_cute_dog', 'グッズ\n1個', 'work_typing_cat', 'おこづかいを\n全部'),
        ('20代', 'cocky_dj_cat', '遠征\n全通', 'eat_chips_cat', 'もやし生活'),
        ('30代', 'rizz_cat_rizz', '祭壇を\n作る', 'stare_lying_tabby_cat', '服は\n5年前のまま'),
        ('40代', 'smug_squint_bicolor_cat', 'アクスタ\n全種類', 'think_chin_paw_orange_cat', '健康診断は\nけちる'),
        ('50代', 'stare_aloha_gray_cat', '応援広告を\n出す', 'sad_looking_away_tabby', '老眼鏡は\n100円'),
        ('60代', 'happy_chipi_chapa_cat', '年金で\n全国ツアー', 'calm_black_face_sheep', 'ごはんは\nおかゆ'),
        ('70代', 'listen_dancing_dog', '孫と\nいっしょに参戦', 'huh_huh_cat', 'チケットの\n取り方が\nわからない'),
        ('80代', 'happy_hamster_open_arms', '推しが\n生きがい', 'sleepy_old_memories_cat', '推しが\n生きがい'),
        ('100歳', 'showoff_gojo_cosplay_cat', '推しの\n孫を推す', 'dance_filmed_by_gray_cat', '生涯\n現役オタク'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('自分用', '推し用'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}年代別", 96, Wd.BLACK, 95), ("{y}推し活の出費", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_99_oshikatsu.mp4"), os.path.join(Wd.HERE, "out", "short_99_oshikatsu_preview"))
