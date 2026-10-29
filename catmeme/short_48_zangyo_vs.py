"""ショート48：日本vs世界 残業への反応の差（world_short.py・short_25d_jishin「地震の反応」と同じ作り・10/29 ユーザー指定）。59.9秒。

python3 catmeme/short_48_zangyo_vs.py → out/short_48_zangyo_vs.mp4
- 1か月の残業時間ごとに「だれもいない（札と線だけ）→ 世界の猫＋説明 → 日本の猫＋説明（世界の猫は残る）」の3段（地震と同じ）
- 世界は少しの残業でも大さわぎ、日本は「ふつう」と言ってしまう、のずれで笑わせる
- 長時間労働をおもしろがらない：80時間からは「体が限界」と正直に書き、最後は「みんなもむりせず休もう」で締める（ショートの締めのルール）
- 45時間＝残業の上限の原則、80時間＝健康に危ないと言われる目安。実在の会社名は出さない。BGM なし
"""
import os

import world_short as Wd

ST = "bg25_office_desk"
K = 59.9 / 58.5


def cuts():
    out = []
    # (残業, 世界の猫, 世界の説明, 日本の猫, 日本の説明)
    rows = [
        ("月1時間", "stare_big_eyes_tabby_kitten", "家族に電話で\nあやまる", "sleepy_sleepy_cat", "定時と\nほぼ同じ"),
        ("月5時間", "meow_ragdoll_chubby_cat", "会社に\n文句を言う", "eat_chips_cat", "今月は\nひまだった"),
        ("月10時間", "glare_disgusted_cat", "転職サイトを\n見はじめる", "talk_orange_white_sitting_cat", "まあまあ\nふつう"),
        ("月20時間", "rage_talking_cat", "弁護士に\n相談する", "work_typing_cat", "ちょっと\nいそがしい月"),
        ("月30時間", "punch_boxing_white_cat", "みんなで\nストライキ", "eat_pop_cat", "コンビニ夕飯が\nふえる"),
        ("月45時間", "scream_phone_orange_cat", "ニュースに\nなる", "think_chin_paw_orange_cat", "残業の上限に\nとどく"),
        ("月60時間", "fight_cat_fight", "会社じゅうが\n大さわぎ", "stare_lying_tabby_cat", "栄養ドリンクが\n手ばなせない"),
        ("月80時間", "stare_tabby_wide_eyes_cat", "言葉を\n失う", "sad_looking_away_tabby", "体が限界\n休むサイン"),
        ("月100時間", "despair_dramatic_kitten", "信じられない", "realize_wet_cat_stare", "みんなも\nむりせず休もう"),
    ]
    for lv, wcat, wcap, jcat, jcap in rows:
        tag_se = {"月45時間": "explosion_chudoon", "月60時間": "explosion_chudoon", "月80時間": "game_mgs_alert", "月100時間": "game_mgs_alert"}
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=[tag_se.get(lv, "pi")]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 120, Wd.BLACK, 95), ("{y}残業への反応", 120, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_48_zangyo_vs.mp4"), os.path.join(Wd.HERE, "out", "short_48_zangyo_vs_preview"))
