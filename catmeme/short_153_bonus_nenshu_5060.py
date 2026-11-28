"""ショート153：20代vs50代　年収別ボーナスの使い道（world_short.py・段階でくらべる型・11/28 ユーザー指定）。59.9秒。

python3 catmeme/short_153_bonus_nenshu_5060.py → out/short_153_bonus_nenshu_5060.mp4
- 11/28 ユーザー指定：「段階別に比べられる題材がいい」。札は年収（300万〜1500万）。右＝50代、左＝20代。右の字幕は赤
- 11/24 の決まり：題材は「生々しさ」「コメントが増えそう」・字幕は生々しく人間味あふれる本音・固定コメント案を付ける
- Wd.vs_rows（少し前の形：猫は大きくしない・字幕はそれぞれの側・左に移っても右の字幕は残す）
- 11/28 修正：300万 50代みかん・20代鳥貴族／400万 車検(軽自動車)／500万 ポールスミスの財布／600万 子どもの学費／700万 20代 車の頭金（運転する猫）／海外旅行は800万へ／1000万 老後資金に足りますか？・接待ゴルフの道具（泣く猫）／1500万 子どもの新居費用（しょんぼり犬）／本音を差しかえ
- 素材は 142/150/151 とできるだけ重ならないもの。どちらもけなさない
- 概要欄の注意：※よくあるイメージです（人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg02_room'


def cuts():
    # (札, 右の猫＝50代, 右の字幕, 左の猫＝20代, 左の字幕)
    rows = [
        ('年収300万', 'stand_real_sheep', 'みかん', 'eat_chips_cat', '鳥貴族'),
        ('年収400万', 'despair_dramatic_kitten', '車検\n(軽自動車)', 'dance_edm_cat', '推しの\n遠征費'),
        ('年収500万', 'work_typing_cat', '子どもの\n塾代', 'rizz_cat_rizz', 'ポールスミスの\n財布'),
        ('年収600万', 'scream_standing_marmot', '子どもの\n学費', 'punch_boxing_white_cat', '新NISAに\n全力'),
        ('年収700万', 'angry_aiming_cat', '住宅ローンの\n繰り上げ返済', 'drive_driving_cat', '車の頭金に\nあてる'),
        ('年収800万', 'stare_lying_tabby_cat', '親の介護に\nまわす', 'dance_orange_gray_cats', '海外旅行\n行っちゃう'),
        ('年収1000万', 'surprise_big_pupils_cat', '老後資金に\n足りますか？', 'sad_banana_cat_cry', '接待ゴルフの\n道具を揃える'),
        ('年収1500万', 'sad_black_dog', '子どもの\n新居費用に\n消える', 'scream_phone_orange_cat', '住民税の額に\n叫ぶ'),
        ('本音', 'sleep_sleeping_cat', 'この年齢だと\n買いたいものが\nそんなに無い', 'angry_shooting_cat', '来年こそ\n転職する\n(中々しない)'),
    ]
    return Wd.vs_rows(ST, rows, heads=('20代', '50代'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}20代vs50代", 96, Wd.BLACK, 95), ("{y}年収別ボーナスの使い道", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_153_bonus_nenshu_5060.mp4"), os.path.join(Wd.HERE, "out", "short_153_bonus_nenshu_5060_preview"))
