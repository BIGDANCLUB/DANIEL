"""ショート64：日本vs世界 何階まで階段で行く？（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補5番）。59.9秒。

python3 catmeme/short_64_kaidan.py → out/short_64_kaidan.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg54_station_crowd_map"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1階', 'call_customer_service_cat', 'エレベーターを\n呼ぶ', 'walk_white_duck', '階段で\n行く'),
        ('2階', 'sleepy_sleepy_cat', 'エレベーターを\n待つ', 'work_typing_cat', '階段で\n健康に'),
        ('3階', 'glare_disgusted_cat', '階段は\nありえない', 'think_bike_front_seat_cat', 'エレベーターが\n混んでるので\n階段'),
        ('5階', 'drive_monkey_golf_cart', 'エスカレーター', 'sad_looking_away_tabby', '息が\n切れる'),
        ('10階', 'eat_pop_cat', 'エレベーターで\nおやつ', 'despair_dramatic_kitten', '足が\nふるえる'),
        ('20階', 'leave_cat_leaves_home', '引っ越す', 'stare_tabby_wide_eyes_cat', '健康診断の\nため'),
        ('30階', 'surprise_big_pupils_cat', 'ヘリを\n呼ぶ', 'scream_phone_orange_cat', '防災訓練'),
        ('停電', 'sleep_sleeping_cat', '今日は\n帰らない', 'happy_chipi_chapa_cat', '非常階段で\n出社'),
        ('最上階', 'happy_hamster_open_arms', '景色が\n最高', 'blank_black_cat_zoning_out', '景色を見る\n余裕がない'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('日本', '世界'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}何階まで階段で行く？", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_64_kaidan.mp4"), os.path.join(Wd.HERE, "out", "short_64_kaidan_preview"))
