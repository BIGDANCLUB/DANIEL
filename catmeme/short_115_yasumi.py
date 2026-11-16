"""ショート115：日本vs世界　1年の休みの日数（world_short.py・段階でくらべる型・11/16 ユーザー指定：候補19番）。59.9秒。

python3 catmeme/short_115_yasumi.py → out/short_115_yasumi.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・地域・人もけなさない
- 自分のチャンネルで伸びた「日本vs世界・地域どうしの比べ合い」の傾向に合わせた（11/16）
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/16 一覧で確認）
- 概要欄の注意：※目安です（よくあるイメージで、実際の統計ではありません）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg109_calendar'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('土日', 'dance_cute_dog', 'しっかり\n休む', 'work_typing_cat', '土曜は\n出勤'),
        ('祝日', 'happy_hamster_open_arms', '休む', 'think_chin_paw_orange_cat', '会社のカレンダーは\n平日'),
        ('有給', 'cocky_dj_cat', '全部\n使う', 'stare_lying_tabby_cat', '5日だけ\nなんとか'),
        ('夏休み', 'listen_dancing_dog', '3週間', 'sad_looking_away_tabby', '3日'),
        ('年末年始', 'rizz_cat_rizz', '2週間', 'stare_tabby_wide_eyes_cat', '5日\n(実家で疲れる)'),
        ('病気', 'smug_squint_bicolor_cat', 'すぐ休む', 'scream_phone_orange_cat', '熱があっても\nリモートで参加'),
        ('連休', 'stare_aloha_gray_cat', '海外旅行', 'calm_black_face_sheep', 'どこも混んでて\n家にいる'),
        ('合計', 'happy_chipi_chapa_cat', '年150日', 'despair_dramatic_kitten', '年120日'),
        ('結局', 'dance_filmed_by_gray_cat', '人生を\n楽しむ', 'blank_black_cat_zoning_out', '休みの日も\n仕事のことを\n考える'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}1年の休みの日数", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_115_yasumi.mp4"), os.path.join(Wd.HERE, "out", "short_115_yasumi_preview"))
