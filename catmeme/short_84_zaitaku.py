"""ショート84：在宅勤務の理想と現実（world_short.py・段階でくらべる型・11/7 ユーザー指定：候補17番）。59.9秒。

python3 catmeme/short_84_zaitaku.py → out/short_84_zaitaku.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg14_home_night"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('8時', 'cocky_dj_cat', '朝活で\nコーヒー', 'sleep_sleeping_cat', '8時58分に\n起きる'),
        ('9時', 'work_typing_cat', 'すぐ仕事\nスタート', 'blank_black_cat_zoning_out', 'パジャマで\nログイン'),
        ('10時', 'stare_interviewer_cat', '会議も\nきっちり', 'meow_ragdoll_chubby_cat', 'カメラオフで\nうなずく'),
        ('11時', 'think_chin_paw_orange_cat', '集中して\nはかどる', 'stare_lying_tabby_cat', '洗濯物が\n気になる'),
        ('12時', 'happy_chipi_chapa_cat', '手作りランチ', 'eat_chips_cat', 'お菓子が\nお昼'),
        ('14時', 'read_book_orange_kitten', '資料を\n仕上げる', 'snore_snoring_dog', 'ちょっと\n横になる'),
        ('15時', 'showoff_gojo_cosplay_cat', '進み具合を\n報告', 'scream_phone_orange_cat', 'チャットの\n通知で\nとび起きる'),
        ('18時', 'dance_happy_banana_cat', '定時で\nおしまい', 'sad_looking_away_tabby', '終わりが\nわからず\n21時'),
        ('1か月後', 'happy_hamster_open_arms', '通勤がなくて\n最高', 'despair_dramatic_kitten', '1日\n200歩'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}在宅勤務の", 96, Wd.BLACK, 95), ("{y}理想と現実", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_84_zaitaku.mp4"), os.path.join(Wd.HERE, "out", "short_84_zaitaku_preview"))
