"""ショート93：日本vs世界 プレゼントの金額（world_short.py・段階でくらべる型・11/12 ユーザー指定：候補8番）。59.9秒。

python3 catmeme/short_93_present.py → out/short_93_present.mp4
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
        ('500円', 'happy_hamster_open_arms', 'ありがとう!', 'sad_looking_away_tabby', '気をつかわせて\nすみません'),
        ('1000円', 'dance_cute_dog', 'うれしい!', 'think_chin_paw_orange_cat', 'お返しを\n考えはじめる'),
        ('3000円', 'wave_waving_cat', 'ハグ', 'money_counting_orange_cat', '半額のお返しを\n調べる'),
        ('5000円', 'cocky_dj_cat', '最高!', 'stare_lying_tabby_cat', 'お返しの\nお返しが\n来る'),
        ('1万円', 'rizz_cat_rizz', 'パーティー', 'surprise_big_pupils_cat', '逆に\nこわい'),
        ('3万円', 'smug_squint_bicolor_cat', '愛してる', 'despair_dramatic_kitten', '何か\n裏がある？'),
        ('手作り', 'happy_girlfriend_dance_cat', '涙', 'calm_black_face_sheep', '置き場所に\n困る'),
        ('現金', 'stare_aloha_gray_cat', '便利!', 'peek_what_happen_cat', 'のし袋に\n入れなおす'),
        ('お返し', 'dance_filmed_by_gray_cat', 'いらない\n飲み行こうぜ', 'scream_phone_orange_cat', 'お返しの\nお返しの\nお返し'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}プレゼントの金額", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_93_present.mp4"), os.path.join(Wd.HERE, "out", "short_93_present_preview"))
