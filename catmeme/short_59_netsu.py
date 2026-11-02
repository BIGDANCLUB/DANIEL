"""ショート59：日本vs世界 熱が出たときの反応（world_short.py・地震の反応と同じ作り・11/2 ユーザー指定：段階的にくらべられる題材）。59.9秒。

python3 catmeme/short_59_netsu.py → out/short_59_netsu.mp4
- 体温ごとに「札だけ → 世界の猫 → 日本の猫」の3段。数字が大きくなるほど差が広がるずれで笑わせる。どの国もけなさない
- 数字・反応は「よくあるイメージ」としての目安（実在の国の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg28_us_hospital"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 世界の猫, 世界の説明, 日本の猫, 日本の説明)
    rows = [
        ('37.0℃', 'slack_nail_filing_cat', '念のため\n休む', 'work_typing_cat', 'ふつうに\n出社'),
        ('37.5℃', 'call_customer_service_cat', '病院へ\n行く', 'stare_big_eyes_tabby_kitten', 'マスクして\n出社'),
        ('38.0℃', 'sleep_sleeping_cat', '1週間\n休む', 'think_chin_paw_orange_cat', '午後から\n出社'),
        ('38.5℃', 'talk_orange_white_sitting_cat', '上司が\n「帰って」', 'scream_phone_orange_cat', '上司に\n電話であやまる'),
        ('39.0℃', 'sleepy_old_memories_cat', '家族が\n看病', 'work_dog_staring_computer', 'リモートで\n会議に出る'),
        ('39.5℃', 'eat_crunchy_cat_luna', 'スープを飲んで\n寝る', 'despair_dramatic_kitten', '仕事のメールを\n返す'),
        ('40.0℃', 'fight_cat_fight', 'すぐに\n病院へ', 'sad_looking_away_tabby', '熱が下がったら\n休日出勤'),
        ('41.0℃', 'surprise_big_pupils_cat', '大さわぎ', 'huh_huh_cat', '体温計を\n疑う'),
        ('結果', 'happy_hamster_open_arms', '早く\n治る', 'realize_wet_cat_stare', 'みんなも\n熱の日は\nしっかり休もう'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}熱が出たときの反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_59_netsu.mp4"), os.path.join(Wd.HERE, "out", "short_59_netsu_preview"))
