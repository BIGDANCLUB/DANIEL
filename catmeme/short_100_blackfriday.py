"""ショート100：ブラックフライデーの理想と現実（world_short.py・段階でくらべる型・11/14 ユーザー指定：お金ショート候補19番）。59.9秒。

python3 catmeme/short_100_blackfriday.py → out/short_100_blackfriday.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/13 一覧を取り直して確認）
- よくあるイメージです。BGM なし
"""
import os

import world_short as Wd

ST = 'bg14_home_night'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1週間前', 'read_book_orange_kitten', '欲しいものを\nリストにする', 'scream_phone_orange_cat', 'なんとなく\nアプリを見る'),
        ('前日', 'work_typing_cat', '値段を\nメモしておく', 'think_chin_paw_orange_cat', 'カートに\n30個'),
        ('0時', 'angry_aiming_cat', 'リストの物だけ\n買う', 'surprise_big_pupils_cat', 'セール開始\n全部ほしい'),
        ('0時5分', 'smug_squint_bicolor_cat', '半額で\nゲット', 'money_counting_orange_cat', '送料無料まで\nあと1000円'),
        ('1時', 'happy_hamster_open_arms', '寝る', 'stare_lying_tabby_cat', 'いらない物で\n1000円うめる'),
        ('翌日', 'dance_cute_dog', 'いい買い物\nだった', 'sad_looking_away_tabby', 'セール前と\n同じ値段だった'),
        ('1週間後', 'cocky_dj_cat', 'さっそく\n使う', 'despair_dramatic_kitten', '段ボールが\n10箱'),
        ('1か月後', 'happy_chipi_chapa_cat', '大満足', 'calm_black_face_sheep', 'まだ\n開けてない'),
        ('請求日', 'stare_aloha_gray_cat', '予算どおり', 'dance_filmed_by_gray_cat', 'カードの\n請求を見て\n気絶'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}ブラックフライデーの", 96, Wd.BLACK, 95), ("{y}理想と現実", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_100_blackfriday.mp4"), os.path.join(Wd.HERE, "out", "short_100_blackfriday_preview"))
