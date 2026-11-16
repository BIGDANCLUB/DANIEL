"""ショート116：東京vs地方　1日の車の運転時間（world_short.py・段階でくらべる型・11/16 ユーザー指定：候補21番）。59.9秒。

python3 catmeme/short_116_kuruma_chiho.py → out/short_116_kuruma_chiho.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・地域・人もけなさない
- 自分のチャンネルで伸びた「日本vs世界・地域どうしの比べ合い」の傾向に合わせた（11/16）
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/16 一覧で確認）
- 概要欄の注意：※目安です（よくあるイメージで、地域や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg26_rural_road'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('0分', 'work_typing_cat', '免許はあるけど\nペーパー', 'happy_hamster_open_arms', '車がないと\n生きていけない'),
        ('5分', 'stare_tabby_wide_eyes_cat', '乗らない', 'cocky_dj_cat', 'コンビニへ\n車で'),
        ('10分', 'think_chin_paw_orange_cat', '乗らない', 'dance_cute_dog', 'ゴミ出しも\n車で'),
        ('30分', 'sad_looking_away_tabby', '駐車場が\n見つからない', 'listen_dancing_dog', '通勤'),
        ('1時間', 'scream_phone_orange_cat', '渋滞で\n1キロ', 'rizz_cat_rizz', 'イオンへ\nドライブ'),
        ('2時間', 'stare_lying_tabby_cat', '首都高で\n迷う', 'smug_squint_bicolor_cat', 'となり町の\nラーメン屋'),
        ('3時間', 'despair_dramatic_kitten', '駐車代\n3000円', 'stare_aloha_gray_cat', '日帰り温泉'),
        ('飲み会', 'calm_black_face_sheep', '電車で\n帰れる', 'sad_banana_cat_cry', '運転代行を\nよぶ'),
        ('休日', 'blank_black_cat_zoning_out', '家で寝る', 'dance_filmed_by_gray_cat', 'とりあえず\nドライブ'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('東京', '地方'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}東京vs地方", 96, Wd.BLACK, 95), ("{y}1日の車の運転時間", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_116_kuruma_chiho.mp4"), os.path.join(Wd.HERE, "out", "short_116_kuruma_chiho_preview"))
