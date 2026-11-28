"""ショート150：20代vs40代　給料日の過ごし方（world_short.py・段階でくらべる型・11/26 ユーザー指定：146 が伸びたので20代vs40代の続き・候補2番）。59.9秒。

python3 catmeme/short_150_kyuryobi_nendai.py → out/short_150_kyuryobi_nendai.mp4
- 11/24 の決まり：題材は「生々しさ」「コメントが増えそう」・字幕は生々しく人間味あふれる本音・固定コメント案を付ける
- 11/26 修正：朝7時の20代「今日の夜どこ行くか考える」・素材を全部見直し（初期に使っていた素材も含めて、最近使っていないものを中心に。最後のスマホ猫と踊る猫はそのまま）
- 札は給料日の時刻（最後は3日後と本音）。右＝40代、左＝20代。右の字幕は赤
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
        ('給料日 0時', 'sleepy_old_memories_cat', '明細を見て\nため息', 'dance_three_kittens', '残高を\nスクショ'),
        ('朝7時', 'work_dog_staring_computer', '住宅ローン\n引き落とし', 'excited_hodomoe_city_cat', '今日の夜\nどこ行くか\n考える'),
        ('昼12時', 'eat_crunchy_cat_luna', 'いつもの\n500円弁当', 'yell_orange_fat_cat', '1500円の\nランチ'),
        ('夕方5時', 'read_book_orange_kitten', '子どもの\n塾代を振込', 'dance_wop_cat', '欲しかった\n服をポチる'),
        ('夜7時', 'realize_wet_cat_stare', '家で\n発泡酒', 'dance_maxwell_cat', '焼肉で\n乾杯'),
        ('夜9時', 'money_counting_cream_cat', '家計簿アプリを\n開く', 'dance_koto_nai_cat', '2軒目へ'),
        ('夜11時', 'sleepy_sleepy_cat', 'もう寝る', 'ride_kitten_bike', 'タクシーで\n帰宅'),
        ('3日後', 'stare_aloha_gray_cat', '計画どおり', 'scream_standing_marmot_fast', '残高を見て\n叫ぶ'),
        ('本音', 'sad_black_dog', '自分のための\nお金がない', 'dance_filmed_by_gray_cat', '来月も\n同じことする'),
    ]
    return Wd.vs_rows(ST, rows, heads=('20代', '40代'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}20代vs40代", 96, Wd.BLACK, 95), ("{y}給料日の過ごし方", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_150_kyuryobi_nendai.mp4"), os.path.join(Wd.HERE, "out", "short_150_kyuryobi_nendai_preview"))
