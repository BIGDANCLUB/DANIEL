"""ショート85：早起きの理想と現実（world_short.py・段階でくらべる型・11/7 ユーザー指定：候補19番）。59.9秒。

python3 catmeme/short_85_hayaoki.py → out/short_85_hayaoki.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg48_clean_street"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('前の夜', 'read_book_orange_kitten', '22時に\n寝る', 'scream_phone_orange_cat', '気づいたら\n2時'),
        ('5時', 'showoff_gojo_cosplay_cat', '目覚ましより\n先に起きる', 'sleep_sleeping_cat', '目覚ましを\n止める'),
        ('5時半', 'dance_tabby_standing_cat', 'ランニング', 'sleepy_sleepy_cat', 'スヌーズ\n1回目'),
        ('6時', 'cocky_dj_cat', 'シャワーと\nコーヒー', 'snore_snoring_dog', 'スヌーズ\n5回目'),
        ('6時半', 'work_typing_cat', '読書と\n勉強', 'stare_lying_tabby_cat', '布団の中で\nスマホ'),
        ('7時', 'happy_chipi_chapa_cat', 'ゆっくり\n朝ごはん', 'surprise_big_pupils_cat', 'いつもの\n時間に\n起きる'),
        ('7時半', 'joy_happy_happy_happy_cat', 'よゆうで\n出発', 'despair_dramatic_kitten', '走る'),
        ('3日後', 'happy_girlfriend_dance_cat', 'すっかり\n習慣に', 'calm_black_face_sheep', '早起きは\n休日だけに'),
        ('1週間後', 'dance_three_kittens', '朝が\n好きになる', 'dance_filmed_by_gray_cat', '早起き\nなにそれ'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}早起きの", 96, Wd.BLACK, 95), ("{y}理想と現実", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_85_hayaoki.mp4"), os.path.join(Wd.HERE, "out", "short_85_hayaoki_preview"))
