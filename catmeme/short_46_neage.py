"""ショート46：日本vs世界 値上げされたときの反応の差（world_short.py・short_25d_jishin「地震の反応」と同じ作り・10/29 ユーザー指定）。59.9秒。

python3 catmeme/short_46_neage.py → out/short_46_neage.mp4
- 値上げの大きさごとに「だれもいない（札と線だけ）→ 世界の猫＋説明 → 日本の猫＋説明（世界の猫は残る）」の3段（地震と同じ）
- 世界は値上げが大きくなるほど大さわぎ、日本は「ちょっと高いね」のまま落ち着いている、のずれで笑わせる。最後のまとめは入れない
- 実在の会社・お店・商品・政治家の名前は出さない。BGM なし
"""
import os

import world_short as Wd

ST = "bg15_convenience"
K = 59.9 / 58.5


def cuts():
    out = []
    # (値上げ, 世界の猫, 世界の説明, 日本の猫, 日本の説明)
    rows = [
        ("10円", "stare_big_eyes_tabby_kitten", "すぐに\n気づく", "sleepy_sleepy_cat", "気づかない"),
        ("30円", "meow_ragdoll_chubby_cat", "SNSで\n文句の嵐", "think_chin_paw_orange_cat", "まあ\nしかたないか"),
        ("50円", "glare_disgusted_cat", "買うのを\nやめる", "talk_orange_white_sitting_cat", "「ちょっと高いね」\nと言って買う"),
        ("100円", "rage_talking_cat", "お店の前で\n抗議する", "money_counting_orange_cat", "ポイントで\n取り返す"),
        ("1割", "dance_filmed_by_gray_cat", "街で\nデモ行進", "ignore_orange_cat_sniffed", "量が減っても\n気づかない"),
        ("2割", "punch_boxing_white_cat", "給料を上げろと\nストライキ", "ride_kitten_bike", "安いお店を\nはしごする"),
        ("3割", "slap_cat_slaps_kitten", "国に\n文句が殺到", "read_book_orange_kitten", "お弁当を\n作りはじめる"),
        ("5割", "fight_cat_fight", "国じゅうが\n大さわぎ", "work_typing_cat", "節約レシピが\n大人気"),
        ("2倍", "dance_three_kittens", "踊る", "scream_phone_orange_cat", "SNSで\nスーパー玉手を\n褒め称える"),   # 10/29 ユーザー指定
    ]
    for lv, wcat, wcap, jcat, jcap in rows:
        # 札が出た瞬間の音（10/29 ユーザー指定）：3割・5割はチュドーン、2倍はパワーアップ、2割は金額表示（10/30：版権の心配がない音に差し替え）
        tag_se = {"2割": "price_display", "3割": "explosion_chudoon", "5割": "explosion_chudoon", "2倍": "power_up"}
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=[tag_se.get(lv, "pi")]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}値上げへの反応", 96, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_46_neage.mp4"), os.path.join(Wd.HERE, "out", "short_46_neage_preview"))
