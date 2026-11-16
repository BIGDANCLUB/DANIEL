"""ショート112：日本vs世界　1日のごはんにかける時間（world_short.py・段階でくらべる型・11/16 ユーザー指定：候補2番）。59.9秒。

python3 catmeme/short_112_gohan.py → out/short_112_gohan.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・地域・人もけなさない
- 自分のチャンネルで伸びた「日本vs世界・地域どうしの比べ合い」の傾向に合わせた（11/16）
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/16 一覧で確認）
- 概要欄の注意：※目安です（よくあるイメージで、実際の統計ではありません）。BGM なし
"""
import os

import world_short as Wd

ST = 'st02_home_kitchen'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('朝ごはん', 'happy_hamster_open_arms', '家族で\n30分', 'work_typing_cat', '立ったまま\n3分'),
        ('通勤中', 'listen_dancing_dog', 'カフェで\nコーヒー', 'stare_tabby_wide_eyes_cat', 'ゼリー飲料\n10秒'),
        ('昼ごはん', 'cocky_dj_cat', 'ゆっくり\n1時間半', 'eat_crunchy_cat_luna', 'デスクで\n7分'),
        ('おやつ', 'dance_cute_dog', 'ケーキと\nお茶会', 'think_chin_paw_orange_cat', 'お客さんの\nおみやげ1個'),
        ('夕方', 'rizz_cat_rizz', 'ワインで\n乾杯', 'sad_looking_away_tabby', '残業中に\nチョコ1粒'),
        ('晩ごはん', 'smug_squint_bicolor_cat', '家族で\n2時間', 'stare_lying_tabby_cat', '23時に\nコンビニ弁当'),
        ('夜食', 'stare_aloha_gray_cat', '食べない', 'scream_phone_orange_cat', 'カップ麺\n3分待てない'),
        ('休日', 'happy_chipi_chapa_cat', 'ブランチ\n3時間', 'calm_black_face_sheep', '1日1食で\nすむ'),
        ('合計', 'dance_filmed_by_gray_cat', '1日5時間', 'blank_black_cat_zoning_out', '1日30分'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}ごはんにかける時間", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_112_gohan.mp4"), os.path.join(Wd.HERE, "out", "short_112_gohan_preview"))
