"""ショート61：日本vs世界 睡眠時間（world_short.py・地震の反応と同じ作り・11/2 ユーザー指定：段階的にくらべられる題材）。59.9秒。

python3 catmeme/short_61_suimin.py → out/short_61_suimin.mp4
- 睡眠時間ごとに「札だけ → 世界の猫 → 日本の猫」の3段。数字が大きくなるほど差が広がるずれで笑わせる。どの国もけなさない
- 数字・反応は「よくあるイメージ」としての目安（実在の国の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg14_home_night"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 世界の猫, 世界の説明, 日本の猫, 日本の説明)
    rows = [
        ('9時間', 'sleep_sleeping_cat', 'ふつう', 'sad_looking_away_tabby', '寝すぎて\n罪悪感'),
        ('8時間', 'stare_interviewer_cat', '理想的', 'sleepy_old_memories_cat', '休みの日\nだけ'),
        ('7時間', 'think_chin_paw_orange_cat', 'ちょっと\n足りない', 'joy_happy_happy_happy_cat', 'よく寝た\nほう'),
        ('6時間', 'call_customer_service_cat', '仕事を\n休む', 'slack_nail_filing_cat', 'ふつう'),
        ('5時間', 'peek_what_happen_cat', '病院へ\n行く', 'eat_chips_cat', 'コーヒー3杯で\nのりきる'),
        ('4時間', 'glare_disgusted_cat', 'ありえない', 'showoff_gojo_cosplay_cat', '寝てない\nアピール'),
        ('3時間', 'fight_cat_fight', '大さわぎ', 'snore_snoring_dog', '電車で座ったら\n一瞬で寝る'),
        ('2時間', 'surprise_big_pupils_cat', '医者に\n止められる', 'blank_black_cat_zoning_out', '会議の記憶が\nない'),
        ('徹夜', 'blank_black_cat_zoning_out', '（失神）', 'dance_filmed_by_gray_cat', 'うおｗ'),   # 11/2 ユーザー指定：結果はなし
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}睡眠時間", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_61_suimin.mp4"), os.path.join(Wd.HERE, "out", "short_61_suimin_preview"))
