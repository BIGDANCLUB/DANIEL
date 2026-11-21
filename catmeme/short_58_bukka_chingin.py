"""ショート58：日本vs世界 物価が上がったとき、給料はどうなる？（world_short.py・地震の反応と同じ作り・11/2 ユーザー指定）。59.9秒。

python3 catmeme/short_58_bukka_chingin.py → out/short_58_bukka_chingin.mp4
- 物価の上がり方ごとに「札だけ → 世界の猫（給料も上がる）→ 日本の猫（給料がついてこない）」の3段
- 物価上昇率と賃上げ率のバランスのずれで笑わせる。どの国もけなさない。最後は「みんなも実質賃金をチェックしよう」
- 数字は「よくあるイメージ」としての目安（実在の国の統計の値ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg15_convenience"
K = 59.9 / 58.5


def cuts():
    out = []
    # (物価, 世界の猫, 世界の説明, 日本の猫, 日本の説明)
    rows = [
        ("物価+1%", "slack_nail_filing_cat", "給料も\n自動で+2%", "sleepy_sleepy_cat", "気づかない"),
        ("物価+2%", "talk_orange_white_sitting_cat", "給料+3%で\nむしろ得", "think_chin_paw_orange_cat", "給料は\nそのまま"),
        ("物価+3%", "punch_boxing_white_cat", "賃上げを\n要求する", "stare_big_eyes_tabby_kitten", "給料+1%で\n喜んでしまう"),
        ("物価+4%", "rage_talking_cat", "みんなで\nストライキ", "sad_looking_away_tabby", "ランチを\nおにぎりに"),
        ("物価+5%", "money_counting_orange_cat", "給料+6%で\n決着", "work_typing_cat", "副業を\nさがしはじめる"),
        ("物価+6%", "cocky_dj_cat", "転職して\n給料アップ", "scream_phone_orange_cat", "ポイ活に\n命をかける"),
        ("物価+8%", "fight_cat_fight", "国じゅうで\n大さわぎ", "despair_dramatic_kitten", "実質賃金が\n下がり続ける"),
        ("物価+10%", "dance_three_kittens", "給料も\n10%上がった", "blank_black_cat_zoning_out", "給料+3%で\n「過去最高の賃上げ」"),
        ("結果", "happy_hamster_open_arms", "生活は\nあまり変わらない", "realize_wet_cat_stare", "みんなも\n実質賃金を\nチェックしよう"),
    ]
    for lv, wcat, wcap, jcat, jcap in rows:
        big = lv in ("物価+6%", "物価+8%", "物価+10%", "結果")
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}物価が上がったときの給料", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_58_bukka_chingin.mp4"), os.path.join(Wd.HERE, "out", "short_58_bukka_chingin_preview"))
