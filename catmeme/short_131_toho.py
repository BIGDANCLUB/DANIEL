"""ショート131：日本vs世界　「徒歩○分」への反応（world_short.py・段階でくらべる型・11/22 ユーザー指定：候補3番）。59.9秒。

python3 catmeme/short_131_toho.py → out/short_131_toho.mp4
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルの全タイトル（ほのぼの248・40代独身229・おひとりさま7）と被らないことを確認ずみ（11/22）
- 11/22 修正：徒歩1分 世界「普通」・徒歩1時間 日本「終電逃して／冒険の旅」
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg48_clean_street'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('徒歩1分', 'cocky_dj_cat', '普通', 'money_counting_orange_cat', '駅前！\n家賃高い'),
        ('徒歩3分', 'rizz_cat_rizz', 'タクシーを\n呼ぶ', 'happy_hamster_open_arms', 'サンダルで\nコンビニ'),
        ('徒歩5分', 'despair_dramatic_kitten', '遠い', 'smug_squint_bicolor_cat', '駅近物件'),
        ('徒歩10分', 'sad_looking_away_tabby', '車がないと\n無理', 'calm_black_face_sheep', 'ふつう'),
        ('徒歩15分', 'stare_tabby_wide_eyes_cat', '引っ越しを\n考える', 'think_chin_paw_orange_cat', '自転車を\n買うか迷う'),
        ('徒歩20分', 'glare_disgusted_cat', 'ありえない', 'work_typing_cat', 'バスもある'),
        ('徒歩30分', 'scream_standing_marmot', '遭難', 'dance_cute_dog', '健康のために\n歩く'),
        ('徒歩45分', 'call_customer_service_cat', '救助を呼ぶ', 'walk_approaching_orange_cat', '1駅くらい\n歩いちゃう'),
        ('徒歩1時間', 'showoff_gojo_cosplay_cat', '冒険の旅', 'walk_white_duck', '終電逃して\n冒険の旅'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}「徒歩○分」への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_131_toho.mp4"), os.path.join(Wd.HERE, "out", "short_131_toho_preview"))
