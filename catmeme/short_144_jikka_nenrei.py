"""ショート144：日本vs世界　実家暮らしの年齢への反応（world_short.py・段階でくらべる型・11/24 ユーザー指定：候補3番）。59.9秒。

python3 catmeme/short_144_jikka_nenrei.py → out/short_144_jikka_nenrei.mp4
- 11/24 の決まり：題材は「生々しさ」「コメントが増えそう」・字幕は生々しく人間味あふれる本音・固定コメント案を付ける
- Wd.vs_rows（少し前の形：猫は大きくしない・字幕はそれぞれの側・左に移っても右の字幕は残す）
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どちらもけなさない
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg02_room'


def cuts():
    # (札, 右の猫＝世界, 右の字幕, 左の猫＝日本, 左の字幕)
    rows = [
        ('18歳', 'dance_cute_dog', '家を出る\nパーティー', 'happy_hamster_open_arms', '母の唐揚げが\n毎日出る'),
        ('22歳', 'listen_dancing_dog', 'ルームシェアで\n家賃を割る', 'smug_squint_bicolor_cat', '給料は\nほぼ全部\nおこづかい'),
        ('25歳', 'cocky_dj_cat', '親を\n家に招く側', 'think_chin_paw_orange_cat', '「家に3万\n入れてる」が\n口ぐせ'),
        ('28歳', 'rizz_cat_rizz', 'パートナーと\n同棲', 'sad_looking_away_tabby', '彼女を\n家に呼べない'),
        ('30歳', 'calm_black_face_sheep', 'ふつう\n家賃高いし', 'stare_tabby_wide_eyes_cat', '合コンで\n実家と言えない'),
        ('33歳', 'glare_disgusted_cat', '親と\n二世帯で\n仲良く', 'confused_i_dont_know_cat', '洗濯物を\n母にたたまれる'),
        ('35歳', 'stare_interviewer_cat', '家を買う\n頭金に', 'despair_dramatic_kitten', '「いつ出ていくの」\nが冗談じゃない'),
        ('38歳', 'dance_edm_cat', '親の介護も\n家族で', 'money_counting_orange_cat', '貯金だけは\n800万ある'),
        ('40歳', 'dance_filmed_by_gray_cat', '家族だから\n当たり前', 'blank_black_cat_zoning_out', '親より先に\n起きたことがない'),
    ]
    return Wd.vs_rows(ST, rows, heads=('日本', '世界'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}実家暮らしの年齢への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_144_jikka_nenrei.mp4"), os.path.join(Wd.HERE, "out", "short_144_jikka_nenrei_preview"))
