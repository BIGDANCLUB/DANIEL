"""ショート71：日本vs世界 1日に謝る回数（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補28番）。59.9秒。

python3 catmeme/short_71_ayamaru.py → out/short_71_ayamaru.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg78_agency_office"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1回', 'calm_black_face_sheep', 'Sorry', 'stare_interviewer_cat', 'すみません'),
        ('3回', 'glare_disgusted_cat', '謝り\nすぎ', 'work_typing_cat', '朝の\nあいさつ代わり'),
        ('5回', 'confused_i_dont_know_cat', '何か\nしたの？', 'think_chin_paw_orange_cat', '道を\nゆずるたびに'),
        ('10回', 'surprise_big_pupils_cat', '大事件？', 'read_book_orange_kitten', 'メールの\n最初と最後に'),
        ('20回', 'rage_talking_cat', '弁護士を\n呼ぶ', 'sleepy_old_memories_cat', '電話で\nおじぎ'),
        ('30回', 'leave_cat_leaves_home', '心配に\nなる', 'happy_hamster_open_arms', 'ありがとうの\n意味でも使う'),
        ('50回', 'scream_standing_marmot', 'ニュースに\nなる', 'blank_black_cat_zoning_out', 'ぶつかって\nきた人に謝る'),
        ('100回', 'fight_cat_fight', '国際問題', 'despair_dramatic_kitten', 'すみませんが\n口ぐせ'),
        ('寝言', 'sleep_sleeping_cat', 'すやすや', 'sleepy_sleepy_cat', '寝言でも\nすみません'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('日本', '世界'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}1日に謝る回数", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_71_ayamaru.mp4"), os.path.join(Wd.HERE, "out", "short_71_ayamaru_preview"))
