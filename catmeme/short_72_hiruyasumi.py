"""ショート72：昼休みのコンビニ争奪戦（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補31番）。59.9秒。

python3 catmeme/short_72_hiruyasumi.py → out/short_72_hiruyasumi.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg15_convenience"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [   # 11/3 ユーザー指定：12時以降の現実側を後ろへずらす
        ('11:55', 'slack_nail_filing_cat', 'ゆっくり\n選ぼう', 'work_typing_cat', '会議が\n長引く'),
        ('12:00', 'happy_chipi_chapa_cat', 'チャイムと\n同時にダッシュ', 'work_typing_cat', 'まだ\n会議中'),
        ('12:03', 'eat_pop_cat', 'からあげ\n弁当', 'work_typing_cat', 'やっと結論を\nまとめる'),
        ('12:05', 'cocky_dj_cat', 'スイーツも\n買う', 'stare_tabby_wide_eyes_cat', 'エレベーター\n待ち'),
        ('12:10', 'happy_hamster_open_arms', '温めて\nもらう', 'sad_looking_away_tabby', 'おにぎりの\n棚がからっぽ'),
        ('12:15', 'calm_black_face_sheep', '公園で\n食べる', 'sad_banana_cat_cry', 'サンドイッチを\n買って出る'),
        ('12:30', 'sleepy_old_memories_cat', '食後の\nコーヒー', 'scream_phone_orange_cat', '食事中に\n電話が鳴る'),
        ('12:55', 'sleep_sleeping_cat', '昼寝', 'scold_talking_cats_close', '上司から\n説教をくらう'),
        ('13:00', 'dance_three_kittens', '午後も\nがんばる', 'scold_talking_cats_close', '上司の説教が\nサビを迎える'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('現実', '理想'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}昼休みの", 96, Wd.BLACK, 95), ("{y}コンビニ争奪戦", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_72_hiruyasumi.mp4"), os.path.join(Wd.HERE, "out", "short_72_hiruyasumi_preview"))
