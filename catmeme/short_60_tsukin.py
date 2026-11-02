"""ショート60：日本vs世界 通勤時間（片道）（world_short.py・地震の反応と同じ作り・11/2 ユーザー指定：段階的にくらべられる題材）。59.9秒。

python3 catmeme/short_60_tsukin.py → out/short_60_tsukin.mp4
- 通勤時間ごとに「札だけ → 世界の猫 → 日本の猫」の3段。数字が大きくなるほど差が広がるずれで笑わせる。どの国もけなさない
- 数字・反応は「よくあるイメージ」としての目安（実在の国の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg54_station_crowd_map"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 世界の猫, 世界の説明, 日本の猫, 日本の説明)
    rows = [
        ('10分', 'ride_kitten_bike', '自転車で\nのんびり', 'sulk_hungry_cat', '会社の近くは\n家賃が高い'),
        ('20分', 'calm_black_face_sheep', '近いね', 'stare_tabby_wide_eyes_cat', '満員電車で\nぎゅうぎゅう'),
        ('30分', 'leave_cat_leaves_home', '遠いから\n引っ越す', 'slack_nail_filing_cat', 'ふつう'),
        ('45分', 'think_chin_paw_orange_cat', '転職を\n考える', 'sleepy_sleepy_cat', '立ったまま\n寝られる'),
        ('1時間', 'glare_disgusted_cat', 'ありえない', 'read_book_orange_kitten', 'ソシャゲの\nスタミナ消費に\nピッタリ'),
        ('1時間半', 'work_typing_cat', '在宅勤務に\nする', 'stare_lying_tabby_cat', '座るために\n始発に並ぶ'),
        ('2時間', 'drive_driving_cat', 'もう別の国に\n行ける', 'blank_black_cat_zoning_out', '睡眠時間に\nカウントする'),
        ('2時間半', 'scream_standing_marmot', 'それは\n旅行', 'dance_filmed_by_gray_cat', '逆に家で\n寝なくなる'),
        ('3時間', 'happy_chipi_chapa_cat', '旅行中に\n仕事が終わる', 'despair_dramatic_kitten', '職場が\n家になる'),   # 11/2 ユーザー指定：結果はなし
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}電車通勤時間", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_60_tsukin.mp4"), os.path.join(Wd.HERE, "out", "short_60_tsukin_preview"))
