"""ショート78：ジム通いの理想と現実（world_short.py・段階でくらべる型・11/6 ユーザー指定：候補15番）。59.9秒。

python3 catmeme/short_78_gym.py → out/short_78_gym.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg02_room"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('入会日', 'showoff_gojo_cosplay_cat', 'ウェアを\n全部そろえる', 'money_counting_orange_cat', '年会費を\n一括払い'),
        ('1日目', 'punch_boxing_white_cat', 'マシンを\n全部制覇', 'happy_hamster_open_arms', 'やる気\nMAX'),
        ('2日目', 'dance_tabby_standing_cat', '筋肉痛でも\n行く', 'despair_dramatic_kitten', '全身\n筋肉痛'),
        ('3日目', 'cocky_dj_cat', 'プロテインを\n買う', 'sleepy_sleepy_cat', '今日は\n休養日'),
        ('1週間', 'dance_edm_cat', '体が\n軽い', 'calm_black_face_sheep', '雨なので\n休み'),
        ('2週間', 'smug_squint_bicolor_cat', '腹筋が\nうっすら', 'eat_chips_cat', 'ジムの帰りに\nラーメン'),
        ('1か月', 'happy_girlfriend_dance_cat', '体重\nマイナス3kg', 'stare_lying_tabby_cat', '体重\nプラス1kg'),
        ('3か月', 'dance_three_kittens', 'トレーナーと\n友だちに', 'blank_black_cat_zoning_out', '会員カードが\n行方不明'),
        ('半年', 'joy_happy_happy_happy_cat', '大会に\n出る', 'sad_banana_cat_cry', '会費だけ\n払っている'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}ジム通いの", 96, Wd.BLACK, 95), ("{y}理想と現実", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_78_gym.mp4"), os.path.join(Wd.HERE, "out", "short_78_gym_preview"))
