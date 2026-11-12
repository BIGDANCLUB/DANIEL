"""ショート96：年代別 好きな食べもの（昼と夜）（world_short.py・段階でくらべる型・11/12 ユーザー指定：候補28番）。59.9秒。

python3 catmeme/short_96_sukinatabemono.py → out/short_96_sukinatabemono.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg13_izakaya"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('10代', 'eat_pop_cat', '給食の\nあげパン', 'happy_hamster_open_arms', 'ハンバーグ'),
        ('20代', 'dance_cute_dog', 'ラーメン\n大盛り', 'cocky_dj_cat', '焼肉\n食べ放題'),
        ('30代', 'work_typing_cat', 'コンビニ\n弁当', 'eat_chips_cat', 'ビールと\n唐揚げ'),
        ('40代', 'sleepy_old_memories_cat', 'そば', 'stare_lying_tabby_cat', '焼き鳥と\nハイボール'),
        ('50代', 'calm_black_face_sheep', 'うどん', 'sad_looking_away_tabby', '漬物と\nお茶づけ'),
        ('60代', 'read_book_orange_kitten', '煮物', 'stare_aloha_gray_cat', '湯豆腐'),
        ('70代', 'talk_orange_white_sitting_cat', 'おかゆ', 'sleep_sleeping_cat', '早く寝る'),
        ('80代', 'surprise_big_pupils_cat', 'ステーキ', 'showoff_gojo_cosplay_cat', '焼肉\n食べ放題'),
        ('100歳', 'dance_white_dog', 'ハンバーグ', 'happy_chipi_chapa_cat', '結局\n子どもの\nころの味'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('夜', '昼'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}年代別", 96, Wd.BLACK, 95), ("{y}好きな食べもの", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_96_sukinatabemono.mp4"), os.path.join(Wd.HERE, "out", "short_96_sukinatabemono_preview"))
