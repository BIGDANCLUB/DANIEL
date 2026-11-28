"""ショート154：日本vs世界　昼寝の時間への反応（world_short.py・段階でくらべる型・11/28 ユーザー指定）。59.9秒。

python3 catmeme/short_154_hirune_sekai.py → out/short_154_hirune_sekai.mp4
- 11/28 自分のチャンネル分析：伸びるのは「全員に自分の数字がある」×「札が時間・気温などの段階」
- 11/28 ユーザー指定：コメントを増やすため、字幕は極端かつ具体的でウケ狙い（iPhone18ProMAX のように）
- 右＝世界、左＝日本。※よくあるイメージです（国や人によって違います）
- Wd.vs_rows（少し前の形・左に移っても右の字幕は残す・右の字幕は赤）。どの地域・国・人もけなさない
"""
import os

import world_short as Wd

ST = 'bg14_home_night'


def cuts():
    # (札, 右の猫, 右の字幕, 左の猫, 左の字幕)
    rows = [
        ('5分', 'huh_goat_talks_to_huh_cat', '昼寝？\nまばたきでしょ', 'joy_happy_happy_happy_cat', '午後も\n戦える！'),
        ('15分', 'flip_emo_cat_hair', 'パワーナップ\n効率最高', 'work_typing_cat', 'よだれで\n資料がふやける'),
        ('30分', 'eat_chips_cat', 'エスプレッソで\n仕上げ', 'stare_interviewer_cat', '起きたら\n上司と目が合う'),
        ('1時間', 'dance_edm_cat', 'シエスタは\nまだこれから', 'scream_phone_orange_cat', '起きたら\n通知99+'),
        ('2時間', 'dance_orange_gray_cats', '店を閉めて\n家族で寝る', 'despair_dramatic_kitten', '休日なのに\n罪悪感'),
        ('3時間', 'rizz_cat_rizz', '人生を\n楽しんでる', 'blank_black_cat_zoning_out', '夜眠れず\n朝4時にYouTube'),
        ('5時間', 'surprise_big_pupils_cat', 'さすがに\n寝すぎ', 'sad_banana_cat_cry', '起きたら\n日曜の夜9時'),
        ('8時間', 'huh_huh_cat', 'それは\nもう夜', 'stand_real_sheep', '土曜日が\n消滅した'),
        ('本音', 'snore_snoring_dog', '眠いときに\n寝る', 'dance_filmed_by_gray_cat', '昼寝したいから\n会社やめたい'),
    ]
    return Wd.vs_rows(ST, rows, heads=('日本', '世界'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}昼寝の時間への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_154_hirune_sekai.mp4"), os.path.join(Wd.HERE, "out", "short_154_hirune_sekai_preview"))
