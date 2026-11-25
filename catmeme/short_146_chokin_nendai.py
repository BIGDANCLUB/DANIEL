"""ショート146：20代vs40代　貯金額ごとの心の声（world_short.py・段階でくらべる型・11/24 ユーザー指定：候補14番）。59.9秒。

python3 catmeme/short_146_chokin_nendai.py → out/short_146_chokin_nendai.mp4
- 11/24 の決まり：題材は「生々しさ」「コメントが増えそう」・字幕は生々しく人間味あふれる本音・固定コメント案を付ける
- 11/25 修正：本音の段 40代「正直めっちゃ不安」（泣く猫）・20代「40代のオレがなんとかする」（スマホ猫と踊る猫）。右の字幕は赤
- Wd.vs_rows（少し前の形：猫は大きくしない・字幕はそれぞれの側・左に移っても右の字幕は残す）
- 段階ごとに「札だけ → 右の猫（40代）→ 左の猫（20代）」の3段。どちらもけなさない
- 概要欄の注意：※よくあるイメージです（人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg14_home_night'


def cuts():
    # (札, 右の猫＝40代, 右の字幕, 左の猫＝20代, 左の字幕)
    rows = [
        ('0円', 'sad_banana_cat_cry', '老後が\n本気でこわい', 'happy_hamster_open_arms', 'まだ若いし\nなんとかなる'),
        ('10万円', 'despair_dramatic_kitten', '冠婚葬祭\n1回で消える', 'dance_cute_dog', '旅行1回分！'),
        ('50万円', 'sad_looking_away_tabby', '車検と\n歯医者で溶ける', 'smug_squint_bicolor_cat', 'ちょっと\n大人になった'),
        ('100万円', 'think_chin_paw_orange_cat', '同期は\n家を買った', 'cocky_dj_cat', 'SNSで\n報告したい'),
        ('300万円', 'stare_tabby_wide_eyes_cat', '親の介護費を\n調べてしまう', 'rizz_cat_rizz', '転職しても\n半年は生きられる'),
        ('500万円', 'calm_black_face_sheep', 'やっと\n平均くらい？', 'surprise_big_pupils_cat', '誰にも\n言えない額'),
        ('1000万円', 'money_counting_orange_cat', 'でも\n住宅ローンが\n残っている', 'scream_standing_marmot', 'FIREの\n計算を始める'),
        ('通帳を見る', 'blank_black_cat_zoning_out', '見なかった\nことにする', 'work_typing_cat', '毎日アプリで\n確認する'),
        ('本音', 'sad_banana_cat_cry', '正直\nめっちゃ\n不安', 'dance_filmed_by_gray_cat', '40代のオレが\nなんとかする'),
    ]
    return Wd.vs_rows(ST, rows, heads=('20代', '40代'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}20代vs40代", 96, Wd.BLACK, 95), ("{y}貯金額ごとの心の声", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_146_chokin_nendai.mp4"), os.path.join(Wd.HERE, "out", "short_146_chokin_nendai_preview"))
