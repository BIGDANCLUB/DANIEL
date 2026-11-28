"""ショート122：東京vs地方　家賃でどこまで住める？（world_short.py・段階でくらべる型・11/20 ユーザー指定：候補9番）。59.9秒。

python3 catmeme/short_122_yachin_chiho.py → out/short_122_yachin_chiho.mp4
- 段階ごとに「札だけ → 右の猫（地方）→ 左の猫（東京）」の3段。どの地域・人もけなさない
- 11/20 修正：地方側の説明を変更・最後は「0円」で両方ネタに全振り（ユーザー指定）
- 金額はざっくりのイメージ（地域や駅によって違う）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg35_suburb_street'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫＝地方, 右の説明, 左の猫＝東京, 左の説明)
    rows = [
        ('家賃3万', 'happy_hamster_open_arms', '1K\n築浅', 'angry_cat_hits_cat', '不動産屋\n「帰れ」'),
        ('家賃4万', 'dance_cute_dog', '1DK', 'sad_looking_away_tabby', '風呂なし\nアパート'),
        ('家賃5万', 'cocky_dj_cat', '1LDK', 'think_chin_paw_orange_cat', '駅から\n徒歩20分'),
        ('家賃6万', 'rizz_cat_rizz', '駅近\n1LDK', 'despair_dramatic_kitten', 'ワンルーム\n15平米'),
        ('家賃7万', 'listen_dancing_dog', '2LDK\n駐車場つき', 'stare_lying_tabby_cat', 'ロフトつき\n1K'),
        ('家賃8万', 'smug_squint_bicolor_cat', '一軒家も', 'money_counting_orange_cat', 'やっと\n1DK'),
        ('家賃10万', 'surprise_big_pupils_cat', 'そんなに\n払うの？', 'work_typing_cat', '駅近の\n1LDK'),
        ('家賃15万', 'scream_phone_orange_cat', '駅前マンション\nでも行ける', 'blank_black_cat_zoning_out', '2LDK\n（都心は無理）'),
        ('0円', 'drive_driving_cat', '山', 'happy_girlfriend_dance_cat', '実家暮らし\n（最強）'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}東京vs地方", 96, Wd.BLACK, 95), ("{y}家賃でどこまで住める？", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_122_yachin_chiho.mp4"), os.path.join(Wd.HERE, "out", "short_122_yachin_chiho_preview"))
