"""ショート123：彼氏vs彼女　買い物に行った時（world_short.py・段階でくらべる型・11/20 ユーザー指定：候補1番）。59.9秒。

python3 catmeme/short_123_kaimono_danjo.py → out/short_123_kaimono_danjo.mp4
- ベンチマークで伸びている「男女の比べっこ」型（11/20 調査）。ほのぼのにある題材とは被らないものを選んだ
- 段階ごとに「札だけ → 右の猫（彼女）→ 左の猫（彼氏）」の3段。どちらもけなさない、よくあるイメージ。BGM なし
"""
import os

import world_short as Wd

ST = 'bg86_product_shelf'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫＝彼女, 右の説明, 左の猫＝彼氏, 左の説明)
    rows = [
        ('出発前', 'dance_cute_dog', '見るだけ\nだからね', 'calm_black_face_sheep', '靴下だけ\n買う'),
        ('10分', 'happy_hamster_open_arms', 'かわいい〜', 'smug_squint_bicolor_cat', '靴下\n買った'),
        ('30分', 'think_chin_paw_orange_cat', 'これと\nこれどっち？', 'stare_tabby_wide_eyes_cat', 'どっちも\n似合う'),
        ('1時間', 'cocky_dj_cat', 'やっぱり\n最初の店', 'confused_i_dont_know_cat', '最初の店…？'),
        ('1時間半', 'rizz_cat_rizz', '試着\nしてくる', 'blank_black_cat_zoning_out', 'ベンチと\n一体化'),
        ('2時間', 'listen_dancing_dog', 'ちょっと\n休憩しよ', 'sad_looking_away_tabby', 'やっと\n座れる'),
        ('2時間半', 'dance_edm_cat', 'まだ見てない\n店ある', 'despair_dramatic_kitten', '足が\n棒'),
        ('3時間', 'stare_interviewer_cat', '今日は\nいいや', 'scream_phone_orange_cat', 'えっ'),
        ('帰り道', 'happy_girlfriend_dance_cat', '楽しかった！', 'stare_lying_tabby_cat', '財布は\n無事'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}彼氏vs彼女", 96, Wd.BLACK, 95), ("{y}買い物に行った時", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_123_kaimono_danjo.mp4"), os.path.join(Wd.HERE, "out", "short_123_kaimono_danjo_preview"))
