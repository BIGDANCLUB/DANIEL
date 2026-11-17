"""ショート114：日本vs世界　家に帰ってからの過ごし方（world_short.py・段階でくらべる型・11/16 ユーザー指定：候補11番）。59.9秒。

python3 catmeme/short_114_kitaku.py → out/short_114_kitaku.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・地域・人もけなさない
- 自分のチャンネルで伸びた「日本vs世界・地域どうしの比べ合い」の傾向に合わせた（11/16）
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/16 一覧で確認）
- 概要欄の注意：※目安です（よくあるイメージで、実際の統計ではありません）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg02_room'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('17時', 'dance_cute_dog', '帰宅', 'work_typing_cat', 'まだ会社'),
        ('18時', 'happy_hamster_open_arms', '家族と\n晩ごはん', 'stare_tabby_wide_eyes_cat', 'まだ会社'),
        ('19時', 'cocky_dj_cat', 'ジムへ', 'think_chin_paw_orange_cat', 'やっと\n退社'),
        ('20時', 'listen_dancing_dog', '友だちと\nパーティー', 'sad_looking_away_tabby', '満員電車'),
        ('21時', 'rizz_cat_rizz', '映画を見る', 'eat_pop_cat', '帰宅して\nごはん'),
        ('22時', 'smug_squint_bicolor_cat', '読書', 'stare_lying_tabby_cat', 'お風呂に入る\n元気がない'),
        ('23時', 'stare_aloha_gray_cat', 'ぐっすり', 'scream_phone_orange_cat', 'スマホを\nだらだら'),
        ('0時', 'happy_chipi_chapa_cat', '夢の中', 'despair_dramatic_kitten', '自分の時間が\nほしくて\n夜ふかし'),
        ('1時', 'dance_filmed_by_gray_cat', '熟睡', 'blank_black_cat_zoning_out', '寝たくないまま\n寝落ちする'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}帰宅後の過ごし方", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_114_kitaku.mp4"), os.path.join(Wd.HERE, "out", "short_114_kitaku_preview"))
