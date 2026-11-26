"""ショート150：20代vs40代　給料日の過ごし方（world_short.py・段階でくらべる型・11/26 ユーザー指定：146 が伸びたので20代vs40代の続き・候補2番）。59.9秒。

python3 catmeme/short_150_kyuryobi_nendai.py → out/short_150_kyuryobi_nendai.mp4
- 11/24 の決まり：題材は「生々しさ」「コメントが増えそう」・字幕は生々しく人間味あふれる本音・固定コメント案を付ける
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
        ('給料日 0時', 'calm_black_face_sheep', '明細を見て\nため息', 'dance_cute_dog', '残高を\nスクショ'),
        ('朝7時', 'work_typing_cat', '住宅ローン\n引き落とし', 'happy_hamster_open_arms', '今日は\nタクシー出勤'),
        ('昼12時', 'think_chin_paw_orange_cat', 'いつもの\n500円弁当', 'cocky_dj_cat', '1500円の\nランチ'),
        ('夕方5時', 'stare_tabby_wide_eyes_cat', '子どもの\n塾代を振込', 'rizz_cat_rizz', '欲しかった\n服をポチる'),
        ('夜7時', 'sad_looking_away_tabby', '家で\n発泡酒', 'dance_edm_cat', '焼肉で\n乾杯'),
        ('夜9時', 'money_counting_orange_cat', '家計簿アプリを\n開く', 'listen_dancing_dog', '2軒目へ'),
        ('夜11時', 'blank_black_cat_zoning_out', 'もう寝る', 'surprise_big_pupils_cat', 'タクシーで\n帰宅'),
        ('3日後', 'smug_squint_bicolor_cat', '計画どおり', 'scream_standing_marmot', '残高を見て\n叫ぶ'),
        ('本音', 'sad_banana_cat_cry', '自分のための\nお金がない', 'dance_filmed_by_gray_cat', '来月も\n同じことする'),
    ]
    return Wd.vs_rows(ST, rows, heads=('20代', '40代'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}20代vs40代", 96, Wd.BLACK, 95), ("{y}給料日の過ごし方", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_150_kyuryobi_nendai.mp4"), os.path.join(Wd.HERE, "out", "short_150_kyuryobi_nendai_preview"))
