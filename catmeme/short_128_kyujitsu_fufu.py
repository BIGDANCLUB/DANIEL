"""ショート128：夫vs妻　休日の朝（world_short.py・段階でくらべる型・11/21 ユーザー指定：男女型候補12番）。59.9秒。

python3 catmeme/short_128_kyujitsu_fufu.py → out/short_128_kyujitsu_fufu.mp4
- ベンチマークで伸びている「男女の比べっこ」型（11/20 調査）。ほのぼのにある題材とは被らないものを選んだ
- 11/21 修正：もっと夫vs妻に（妻が夫に言う→夫の返し、の掛け合いにした・ユーザー指定）
- 札は時刻。右＝妻、左＝夫
- 段階ごとに「札だけ → 右の猫（妻）→ 左の猫（夫）」の3段。どちらもけなさない、よくあるイメージ。BGM なし
"""
import os

import world_short as Wd

ST = 'bg02_room'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫＝妻, 右の説明, 左の猫＝夫, 左の説明)
    rows = [
        ('6:00', 'work_typing_cat', '起きて\n洗濯スタート', 'sleep_sleeping_cat', '爆睡'),
        ('7:00', 'dance_cute_dog', '朝ごはん\nできたよ', 'sleepy_sleepy_cat', 'あと5分…'),
        ('8:00', 'listen_dancing_dog', '掃除機で\n夫のまわりも\n吸う', 'snore_snoring_dog', 'まだ\n起きない'),
        ('9:00', 'glare_disgusted_cat', 'いつまで\n寝てるの？', 'sad_looking_away_tabby', '休みの日\nくらい\n寝かせて'),
        ('10:00', 'cocky_dj_cat', '洗濯物\n干し終わった', 'happy_hamster_open_arms', '起床\n（いい朝だ）'),
        ('10:30', 'stare_interviewer_cat', '……', 'smug_squint_bicolor_cat', '朝ごはん\nある？'),
        ('11:00', 'rage_talking_cat', '冷めてる\nけどね', 'confused_i_dont_know_cat', '何か\n手伝おうか？'),
        ('11:30', 'angry_cat_hits_cat', 'もう全部\n終わった', 'stare_tabby_wide_eyes_cat', '言ってくれたら\nやったのに'),
        ('12:00', 'angry_aiming_cat', 'お昼は\nあなたが作って', 'money_counting_orange_cat', '出前\nとろうか'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('夫', '妻'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}夫vs妻", 96, Wd.BLACK, 95), ("{y}休日の朝", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_128_kyujitsu_fufu.mp4"), os.path.join(Wd.HERE, "out", "short_128_kyujitsu_fufu_preview"))
