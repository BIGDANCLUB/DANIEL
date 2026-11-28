"""ショート153：20代vs50代　年収別ボーナスの使い道（world_short.py・段階でくらべる型・11/28 ユーザー指定）。59.9秒。

python3 catmeme/short_153_bonus_nenshu_5060.py → out/short_153_bonus_nenshu_5060.mp4
- 11/28 ユーザー指定：「段階別に比べられる題材がいい」。札は年収（300万〜1500万）。右＝50代、左＝20代。右の字幕は赤
- 11/24 の決まり：題材は「生々しさ」「コメントが増えそう」・字幕は生々しく人間味あふれる本音・固定コメント案を付ける
- Wd.vs_rows（少し前の形：猫は大きくしない・字幕はそれぞれの側・左に移っても右の字幕は残す）
- 素材は 142/150/151 とできるだけ重ならないもの。どちらもけなさない
- 概要欄の注意：※よくあるイメージです（人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg02_room'


def cuts():
    # (札, 右の猫＝50代, 右の字幕, 左の猫＝20代, 左の字幕)
    rows = [
        ('年収300万', 'stand_real_sheep', '出るだけ\nありがたい', 'eat_chips_cat', '寸志3万円\n焼肉で消える'),
        ('年収400万', 'despair_dramatic_kitten', '車検で\n全部消える', 'dance_edm_cat', '推しの\n遠征費'),
        ('年収500万', 'work_typing_cat', '子どもの\n塾代', 'rizz_cat_rizz', 'ちょっといい\n財布を買う'),
        ('年収600万', 'scream_standing_marmot', '大学の\n入学金', 'punch_boxing_white_cat', '新NISAに\n全力'),
        ('年収700万', 'angry_aiming_cat', '住宅ローンの\n繰り上げ返済', 'dance_orange_gray_cats', '海外旅行\n行っちゃう'),
        ('年収800万', 'stare_lying_tabby_cat', '親の介護に\nまわす', 'mock_swinging_cat', 'タワマンを\n見に行くだけ'),
        ('年収1000万', 'surprise_big_pupils_cat', '老後資金に\n青ざめる', 'happy_hamster_open_arms', '腕時計を\n即予約'),
        ('年収1500万', 'dance_tabby_standing_cat', 'やっと自分に\nごほうび', 'scream_phone_orange_cat', '住民税の額に\n叫ぶ'),
        ('本音', 'sleep_sleeping_cat', '使い道を\n考える前に\nもう無い', 'angry_shooting_cat', '来年こそ\n転職して上げる'),
    ]
    return Wd.vs_rows(ST, rows, heads=('20代', '50代'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}20代vs50代", 96, Wd.BLACK, 95), ("{y}年収別ボーナスの使い道", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_153_bonus_nenshu_5060.mp4"), os.path.join(Wd.HERE, "out", "short_153_bonus_nenshu_5060_preview"))
