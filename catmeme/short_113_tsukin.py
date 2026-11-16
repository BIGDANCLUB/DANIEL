"""ショート113：日本vs世界　通勤中の過ごし方（world_short.py・段階でくらべる型・11/16 ユーザー指定：候補3番）。59.9秒。

python3 catmeme/short_113_tsukin.py → out/short_113_tsukin.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・地域・人もけなさない
- 自分のチャンネルで伸びた「日本vs世界・地域どうしの比べ合い」の傾向に合わせた（11/16）
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/16 一覧で確認）
- 概要欄の注意：※目安です（よくあるイメージで、実際の統計ではありません）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg54_station_crowd_map'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1駅', 'dance_cute_dog', '音楽で\nノリノリ', 'work_typing_cat', 'メールを\nチェック'),
        ('2駅', 'happy_hamster_open_arms', 'となりの人と\nおしゃべり', 'stare_tabby_wide_eyes_cat', '目を合わせない'),
        ('3駅', 'cocky_dj_cat', '朝ごはん', 'think_chin_paw_orange_cat', '今日の会議を\nシミュレーション'),
        ('5駅', 'listen_dancing_dog', '電話で\n大声トーク', 'sad_looking_away_tabby', '音を出さないよう\n息をひそめる'),
        ('7駅', 'rizz_cat_rizz', 'メイク', 'sleepy_sleepy_cat', '立ったまま\n寝る'),
        ('10駅', 'smug_squint_bicolor_cat', '読書', 'read_book_orange_kitten', '資格の\n勉強'),
        ('15駅', 'stare_aloha_gray_cat', '到着', 'scream_phone_orange_cat', 'まだ半分'),
        ('20駅', 'happy_chipi_chapa_cat', 'もう\n働いている', 'despair_dramatic_kitten', '乗りかえで\nダッシュ'),
        ('到着', 'dance_filmed_by_gray_cat', '元気いっぱい', 'blank_black_cat_zoning_out', 'もう\n1日分\n疲れた'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}通勤中の過ごし方", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_113_tsukin.mp4"), os.path.join(Wd.HERE, "out", "short_113_tsukin_preview"))
