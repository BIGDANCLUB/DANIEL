"""ショート62：日本vs世界 有給休暇の使い方（world_short.py・地震の反応と同じ作り・11/2 ユーザー指定：段階的にくらべられる題材）。59.9秒。

python3 catmeme/short_62_yukyu.py → out/short_62_yukyu.mp4
- 有給の日数ごとに「札だけ → 世界の猫 → 日本の猫」の3段。数字が大きくなるほど差が広がるずれで笑わせる。どの国もけなさない
- 数字・反応は「よくあるイメージ」としての目安（実在の国の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg25_office_desk"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 世界の猫, 世界の説明, 日本の猫, 日本の説明)
    rows = [
        ('1日', 'glare_disgusted_cat', '足りない', 'stare_big_eyes_tabby_kitten', '理由を\n聞かれる'),
        ('3日', 'walk_white_duck', '週末とつなげて\n旅行', 'money_counting_orange_cat', 'お土産を\n全員に配る'),
        ('5日', 'slack_nail_filing_cat', 'まだまだ\nこれから', 'work_typing_cat', '会社に言われて\nやっと取る'),
        ('10日', 'ride_kitten_bike', '1回目の\n夏休み', 'think_chin_paw_orange_cat', '1年で\n使いきれない'),
        ('15日', 'dance_three_kittens', '2週間の\n家族旅行', 'despair_dramatic_kitten', '休み明けの机が\n書類の山'),
        ('20日', 'cocky_dj_cat', 'ぜんぶ使うのが\nあたりまえ', 'sad_looking_away_tabby', '半分以上\n残る'),
        ('25日', 'happy_chipi_chapa_cat', 'まとめて\n南の島へ', 'scream_phone_orange_cat', '休んでも\n仕事のメールを見る'),
        ('30日', 'joy_happy_happy_happy_cat', '1か月の\nバカンス', 'blank_black_cat_zoning_out', '辞めるときに\nまとめて使う'),
        ('結果', 'happy_hamster_open_arms', '休んだぶん\nしっかり働く', 'realize_wet_cat_stare', 'みんなも\n有給を\n使おう'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}有給休暇の使い方", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_62_yukyu.mp4"), os.path.join(Wd.HERE, "out", "short_62_yukyu_preview"))
