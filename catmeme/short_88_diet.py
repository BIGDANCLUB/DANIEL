"""ショート88：ダイエットの理想と現実（world_short.py・段階でくらべる型・11/9 ユーザー指定：候補16番）。59.9秒。

python3 catmeme/short_88_diet.py → out/short_88_diet.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
- 11/10 ユーザー指定：半年の現実は五条猫「ドーナツは穴があるからカロリー0」
"""
import os

import world_short as Wd

ST = "bg02_room"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1日目', 'showoff_gojo_cosplay_cat', 'サラダと\nランニング', 'dance_tabby_standing_cat', 'やる気\nMAX'),
        ('2日目', 'happy_chipi_chapa_cat', '体が軽い', 'despair_dramatic_kitten', '全身\n筋肉痛'),
        ('3日目', 'cocky_dj_cat', 'マイナス1kg', 'eat_chips_cat', 'ごほうびの\nポテチ'),
        ('1週間', 'dance_three_kittens', 'マイナス2kg', 'calm_black_face_sheep', '体重計に\n乗らない'),
        ('2週間', 'smug_squint_bicolor_cat', '腹筋が\nうっすら', 'sulk_hungry_cat', '飲み会で\n全部もどる'),
        ('1か月', 'happy_girlfriend_dance_cat', 'マイナス5kg', 'stare_lying_tabby_cat', '明日から\n本気出す'),
        ('2か月', 'joy_happy_happy_happy_cat', '服が\nゆるくなる', 'eat_pop_cat', '服が\nきつくなる'),
        ('3か月', 'dance_edm_cat', '理想の体', 'sleepy_old_memories_cat', 'ダイエット本が\n3冊ふえた'),
        ('半年', 'happy_hamster_open_arms', 'キープ', 'showoff_gojo_cosplay_cat', 'ドーナツは\n穴があるから\nカロリー0'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}ダイエットの", 96, Wd.BLACK, 95), ("{y}理想と現実", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_88_diet.mp4"), os.path.join(Wd.HERE, "out", "short_88_diet_preview"))
