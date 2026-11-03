"""ショート69：日本vs世界 春の過ごし方（world_short.py・段階でくらべる型・11/3 ユーザー指定：候補21番）。59.9秒。

python3 catmeme/short_69_haru.py → out/short_69_haru.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- 「ほのぼの猫ミーム」と強く被るテーマは使わない（research/honobono_overlap_20261103.md）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg59_sakura_park"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('3月', 'calm_black_face_sheep', 'まだ\n寒いね', 'stare_interviewer_cat', '卒業式'),
        ('4月1日', 'laugh_laughing_dog', 'エイプリル\nフール', 'work_typing_cat', '入社式'),
        ('桜が咲いた', 'walk_white_duck', 'きれいだね', 'happy_chipi_chapa_cat', 'お花見の\n場所取り'),
        ('場所取り', 'confused_i_dont_know_cat', 'なぜ\n朝から？', 'sleep_sleeping_cat', '新入社員が\nシートで待つ'),
        ('お花見', 'eat_crunchy_cat_luna', 'ピクニック', 'dance_three_kittens', '宴会'),
        ('花粉', 'slack_nail_filing_cat', '気にしない', 'despair_dramatic_kitten', '目と鼻が\n大変'),
        ('新学期', 'read_book_orange_kitten', '学校は\n9月から', 'stare_big_eyes_tabby_kitten', 'クラス替えに\nドキドキ'),
        ('桜が散った', 'sleepy_sleepy_cat', 'ふつうの\n日', 'sad_looking_away_tabby', '葉桜で\n飲む'),
        ('春の終わり', 'happy_hamster_open_arms', '夏休みの\n計画', 'blank_black_cat_zoning_out', 'なんだか\nやる気が出ない'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}春の過ごし方", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_69_haru.mp4"), os.path.join(Wd.HERE, "out", "short_69_haru_preview"))
