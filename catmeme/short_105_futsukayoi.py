"""ショート105：日本vs世界　二日酔いの朝（world_short.py・段階でくらべる型・11/15 ユーザー指定：候補9番）。59.9秒。

python3 catmeme/short_105_futsukayoi.py → out/short_105_futsukayoi.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/15 一覧で確認）
- 概要欄の注意：※目安です（よくあるイメージで、実際の統計ではありません）※お酒は20歳になってから。BGM なし
"""
import os

import world_short as Wd

ST = 'bg02_room'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('6時', 'sleep_sleeping_cat', '寝ている', 'scream_phone_orange_cat', '目覚ましで\n頭がガンガン'),
        ('6時半', 'sleepy_sleepy_cat', 'まだ\n寝ている', 'stare_tabby_wide_eyes_cat', '昨日の記憶を\nさがす'),
        ('7時', 'happy_hamster_open_arms', '休むと\n連絡', 'think_chin_paw_orange_cat', 'しじみの\nみそ汁'),
        ('8時', 'listen_dancing_dog', '二度寝', 'work_typing_cat', '満員電車で\nたえる'),
        ('9時', 'cocky_dj_cat', '迎え酒', 'sad_looking_away_tabby', '朝礼で\n真っ青'),
        ('10時', 'rizz_cat_rizz', 'ブランチ', 'stare_lying_tabby_cat', 'トイレに\n3回目'),
        ('12時', 'dance_cute_dog', '元気', 'calm_black_face_sheep', 'ランチは\nおかゆ'),
        ('夕方', 'happy_chipi_chapa_cat', 'また\n飲みに行く', 'despair_dramatic_kitten', 'もう二度と\n飲まないと\n誓う'),
        ('夜', 'dance_filmed_by_gray_cat', '乾杯！', 'blank_black_cat_zoning_out', '誓いを破って\n乾杯'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}二日酔いの朝", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_105_futsukayoi.mp4"), os.path.join(Wd.HERE, "out", "short_105_futsukayoi_preview"))
