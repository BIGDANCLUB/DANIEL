"""ショート98：日本vs世界　終電を逃したときの出費（world_short.py・段階でくらべる型・11/14 ユーザー指定：お金ショート候補3番）。59.9秒。

python3 catmeme/short_98_shuden.py → out/short_98_shuden.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルと被らないことを確認ずみ（11/13 一覧を取り直して確認）
- 目安です（よくあるイメージで、実際の統計ではありません）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg51_night_street'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('23時', 'dance_cute_dog', 'まだ\n飲む', 'stare_tabby_wide_eyes_cat', '終電の時間を\n調べる'),
        ('0時', 'cocky_dj_cat', '深夜バスで\n帰る', 'scream_phone_orange_cat', '終電\n逃した'),
        ('0時10分', 'happy_hamster_open_arms', '友だちの家に\n泊まる', 'think_chin_paw_orange_cat', 'タクシー代\n8000円を\n見る'),
        ('0時30分', 'listen_dancing_dog', 'ライドシェアで\n帰る', 'sad_looking_away_tabby', 'ネットカフェ\n2000円'),
        ('1時', 'rizz_cat_rizz', '24時間\n電車', 'calm_black_face_sheep', 'ファミレスで\nドリンクバー'),
        ('3時', 'smug_squint_bicolor_cat', 'もう家で\n寝ている', 'sleep_sleeping_cat', 'カラオケで\n仮眠'),
        ('5時', 'stare_aloha_gray_cat', 'ぐっすり', 'despair_dramatic_kitten', '始発で帰る'),
        ('翌日', 'dance_filmed_by_gray_cat', '元気に\n出社', 'blank_black_cat_zoning_out', '眠気と\n出費'),
        ('合計', 'showoff_gojo_cosplay_cat', '0円', 'money_counting_orange_cat', '飲み代より\n高い'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}終電を逃したら", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_98_shuden.mp4"), os.path.join(Wd.HERE, "out", "short_98_shuden_preview"))
