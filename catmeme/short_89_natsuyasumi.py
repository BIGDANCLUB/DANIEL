"""ショート89：夏休みの理想と現実（world_short.py・段階でくらべる型・11/9 ユーザー指定：候補18番）。59.9秒。

python3 catmeme/short_89_natsuyasumi.py → out/short_89_natsuyasumi.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
- 11/10 ユーザー指定：2日目の理想はスマホで撮る猫と踊る猫・出社日の現実は電話の猫「退職代行」
"""
import os

import world_short as Wd

ST = "bg62_okinawa_beach"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1日目', 'showoff_gojo_cosplay_cat', '海へ\n出発', 'sleep_sleeping_cat', '昼まで\n寝る'),
        ('2日目', 'dance_filmed_by_gray_cat', 'バーベキュー', 'scream_phone_orange_cat', '1日中\nスマホ'),
        ('3日目', 'cocky_dj_cat', '花火大会', 'eat_chips_cat', 'エアコンの部屋で\nお菓子'),
        ('4日目', 'happy_chipi_chapa_cat', '温泉旅行', 'stare_lying_tabby_cat', '動画を\n20本見る'),
        ('5日目', 'read_book_orange_kitten', '読書と\n勉強', 'snore_snoring_dog', '昼寝'),
        ('6日目', 'dance_three_kittens', '友だちと\n遊ぶ', 'calm_black_face_sheep', 'コンビニに\n行っただけ'),
        ('7日目', 'joy_happy_happy_happy_cat', '日焼けして\n元気', 'sad_looking_away_tabby', '肌が\n真っ白'),
        ('最終日', 'happy_girlfriend_dance_cat', 'いい夏だった', 'despair_dramatic_kitten', '何もして\nないのに\n終わった'),
        ('出社日', 'dance_happy_banana_cat', 'やる気\nいっぱい', 'call_customer_service_cat', '退職\n代行'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}夏休みの", 96, Wd.BLACK, 95), ("{y}理想と現実", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_89_natsuyasumi.mp4"), os.path.join(Wd.HERE, "out", "short_89_natsuyasumi_preview"))
