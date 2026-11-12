"""ショート97：冷凍庫の中身の理想と現実（ひとり暮らし年数別）（world_short.py・段階でくらべる型・11/12 ユーザー指定：候補29番）。59.9秒。

python3 catmeme/short_97_reitouko.py → out/short_97_reitouko.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg14_home_night"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1年目', 'showoff_gojo_cosplay_cat', '作り置き\nぎっしり', 'happy_hamster_open_arms', '冷凍食品\nぎっしり'),
        ('2年目', 'work_typing_cat', '肉と魚を\n小分け', 'eat_chips_cat', '冷凍\nチャーハン'),
        ('3年目', 'read_book_orange_kitten', '季節の\n野菜', 'stare_lying_tabby_cat', 'アイスだけ'),
        ('4年目', 'cocky_dj_cat', '手作り\nギョーザ', 'think_chin_paw_orange_cat', 'いつのか\nわからない肉'),
        ('5年目', 'smug_squint_bicolor_cat', '冷凍ごはん', 'sad_looking_away_tabby', '霜で\n中が見えない'),
        ('6年目', 'dance_cute_dog', 'フルーツ', 'calm_black_face_sheep', 'もらった\n保冷剤'),
        ('7年目', 'listen_dancing_dog', 'パンを\n冷凍', 'despair_dramatic_kitten', '保冷剤が\n増殖'),
        ('8年目', 'happy_chipi_chapa_cat', '整理整頓', 'blank_black_cat_zoning_out', '保冷剤\n30個'),
        ('10年目', 'stare_aloha_gray_cat', '理想の\n冷凍庫', 'dance_filmed_by_gray_cat', '保冷剤しか\nない'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}冷凍庫の中身の", 96, Wd.BLACK, 95), ("{y}理想と現実", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_97_reitouko.mp4"), os.path.join(Wd.HERE, "out", "short_97_reitouko_preview"))
