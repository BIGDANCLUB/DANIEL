"""ショート154：日本vs世界　昼寝の時間への反応（world_short.py・段階でくらべる型・11/28 ユーザー指定）。59.9秒。

python3 catmeme/short_154_hirune_sekai.py → out/short_154_hirune_sekai.mp4
- 11/28 自分のチャンネル分析：伸びるのは「全員に自分の数字がある」×「札が時間・気温などの段階」
- 11/28 作り直し：伸びた動画（睡眠時間・お風呂・遅刻・プレゼント・ランチ）の字幕に合わせる＝短い言い切り（ふつう・ありえない）と具体的な行動の対比、段階が進むほど極端、最後は札をひねって（失神）とスマホ猫と踊る猫
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
        ('10分', 'stare_interviewer_cat', 'ふつう', 'peek_what_happen_cat', 'トイレの\n個室で'),
        ('20分', 'eat_chips_cat', 'ちょうどいい', 'work_typing_cat', 'よだれで\n資料がぬれる'),
        ('30分', 'flip_emo_cat_hair', 'まだ\n足りない', 'scream_phone_orange_cat', '起きたら\n上司が横に'),
        ('1時間', 'dance_edm_cat', 'シエスタ', 'sad_banana_cat_cry', '始末書'),
        ('2時間', 'dance_orange_gray_cats', 'お店も\n閉める', 'despair_dramatic_kitten', '休日なのに\n罪悪感'),
        ('3時間', 'rizz_cat_rizz', 'よく寝た', 'stare_lying_tabby_cat', '夜\n眠れない'),
        ('5時間', 'surprise_big_pupils_cat', '大丈夫？', 'confused_i_dont_know_cat', '起きたら\n夕方5時の\nチャイム'),
        ('8時間', 'scream_standing_marmot', '救急車を\n呼ぶ', 'stand_real_sheep', '土曜日が\n消滅'),
        ('0分', 'blank_black_cat_zoning_out', '（失神）', 'dance_filmed_by_gray_cat', '昼休みも\n電話番'),
    ]
    return Wd.vs_rows(ST, rows, heads=('日本', '世界'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}昼寝の時間への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_154_hirune_sekai.mp4"), os.path.join(Wd.HERE, "out", "short_154_hirune_sekai_preview"))
