"""ショート124：彼氏vs彼女　旅行の荷物（world_short.py・段階でくらべる型・11/20 ユーザー指定：候補3番）。59.9秒。

python3 catmeme/short_124_ryoko_nimotsu.py → out/short_124_ryoko_nimotsu.mp4
- ベンチマークで伸びている「男女の比べっこ」型（11/20 調査）。ほのぼのにある題材とは被らないものを選んだ
- 段階ごとに「札だけ → 右の猫（彼女）→ 左の猫（彼氏）」の3段。どちらもけなさない、よくあるイメージ。BGM なし
"""
import os

import world_short as Wd

ST = 'bg45_airport_arrival'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫＝彼女, 右の説明, 左の猫＝彼氏, 左の説明)
    rows = [
        ('1週間前', 'listen_dancing_dog', '荷造り\nスタート', 'work_typing_cat', 'まだ\n1週間ある'),
        ('前日', 'scream_standing_marmot', 'スーツケース\n2個目', 'blank_black_cat_zoning_out', 'まだ\n何もしてない'),
        ('前日の夜', 'rizz_cat_rizz', 'もしもの服\n5着', 'smug_squint_bicolor_cat', 'リュックに\n5分'),
        ('当日の朝', 'think_chin_paw_orange_cat', 'ヘアアイロン\n入れた？', 'scream_phone_orange_cat', '充電器\n忘れた'),
        ('空港', 'despair_dramatic_kitten', '重量\nオーバー', 'cocky_dj_cat', 'ほぼ\n手ぶら'),
        ('1日目', 'confused_i_dont_know_cat', 'どの服に\nしよう', 'stare_lying_tabby_cat', '昨日と\n同じ服'),
        ('2日目', 'sad_looking_away_tabby', 'もしもの服\n出番なし', 'money_counting_orange_cat', 'コンビニで\n下着を買う'),
        ('帰り', 'happy_hamster_open_arms', 'お土産で\nパンパン', 'sad_banana_cat_cry', '荷物持ち\n係'),
        ('家に着いて', 'dance_edm_cat', 'すぐ洗濯', 'stare_tabby_wide_eyes_cat', 'リュック\n1週間放置'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('彼氏', '彼女'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}彼氏vs彼女", 96, Wd.BLACK, 95), ("{y}旅行の荷物", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_124_ryoko_nimotsu.mp4"), os.path.join(Wd.HERE, "out", "short_124_ryoko_nimotsu_preview"))
