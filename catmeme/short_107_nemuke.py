"""ショート107：午後の眠気　時間別（world_short.py・段階でくらべる型・11/15 ユーザー指定：候補26番）。59.9秒。

python3 catmeme/short_107_nemuke.py → out/short_107_nemuke.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/15 一覧で確認）
- 概要欄の注意：※よくあるイメージです。BGM なし
"""
import os

import world_short as Wd

ST = 'bg25_office_desk'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('13時', 'work_typing_cat', '午後も\nがんばるぞ', 'eat_crunchy_cat_luna', 'ランチで\n満腹'),
        ('13時半', 'read_book_orange_kitten', '資料を読む', 'sleepy_sleepy_cat', '同じ行を\n5回読む'),
        ('14時', 'rizz_cat_rizz', '会議で発言', 'sleepy_old_memories_cat', '会議で\nうなずくだけ'),
        ('14時半', 'smug_squint_bicolor_cat', '集中', 'sleep_sleeping_cat', '一瞬\n意識が飛ぶ'),
        ('15時', 'happy_hamster_open_arms', 'おやつで\nひと休み', 'eat_pop_cat', 'コーヒー\n3杯目'),
        ('15時半', 'cocky_dj_cat', 'バリバリ', 'stare_tabby_wide_eyes_cat', '目を開けて\n寝ている'),
        ('16時', 'dance_cute_dog', '仕上げ', 'scream_standing_marmot', '上司に\n名前を呼ばれる'),
        ('17時', 'stare_aloha_gray_cat', '定時', 'angry_aiming_cat', '急に\n目が覚める'),
        ('18時', 'dance_filmed_by_gray_cat', '帰る', 'happy_chipi_chapa_cat', '眠気が\n完全に消える'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}午後の眠気", 96, Wd.BLACK, 95), ("{y}時間別", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_107_nemuke.mp4"), os.path.join(Wd.HERE, "out", "short_107_nemuke_preview"))
