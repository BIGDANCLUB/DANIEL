"""ショート151：20代vs40代　冬のボーナスの使い道（world_short.py・段階でくらべる型・11/26 ユーザー指定：146 が伸びたので20代vs40代の続き・候補3番）。59.9秒。

python3 catmeme/short_151_bonus_nendai.py → out/short_151_bonus_nendai.mp4
- 11/24 の決まり：題材は「生々しさ」「コメントが増えそう」・字幕は生々しく人間味あふれる本音・固定コメント案を付ける
- 札はボーナスが入ってからの日数（12月向き）。右＝40代、左＝20代。右の字幕は赤
- Wd.vs_rows（少し前の形：猫は大きくしない・字幕はそれぞれの側・左に移っても右の字幕は残す）
- 段階ごとに「札だけ → 右の猫（40代）→ 左の猫（20代）」の3段。どちらもけなさない
- 概要欄の注意：※よくあるイメージです（人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg02_room'


def cuts():
    # (札, 右の猫＝40代, 右の字幕, 左の猫＝20代, 左の字幕)
    rows = [
        ('入金の朝', 'stare_interviewer_cat', '明細を\nそっと閉じる', 'happy_hamster_open_arms', '金額を\n二度見'),
        ('1日目', 'money_counting_orange_cat', '住宅ローンの\nボーナス払い', 'cocky_dj_cat', '新しい\nスマホを予約'),
        ('2日目', 'think_chin_paw_orange_cat', '子どもの\n冬休み費用', 'dance_cute_dog', '友達と\n旅行の計画'),
        ('3日目', 'calm_black_face_sheep', '冷蔵庫が\n壊れる', 'rizz_cat_rizz', 'ちょっといい\n時計'),
        ('1週間後', 'sad_looking_away_tabby', '親にも\nちょっと渡す', 'dance_edm_cat', '欲しかったもの\n全部買った'),
        ('2週間後', 'stare_tabby_wide_eyes_cat', '新NISAに\n少しだけ', 'listen_dancing_dog', '年末の\n飲み会ラッシュ'),
        ('年末', 'despair_dramatic_kitten', 'お年玉で\n消える', 'confused_i_dont_know_cat', 'あれ…\n残りいくら？'),
        ('1月', 'blank_black_cat_zoning_out', '自分には\n何も残ってない', 'scream_standing_marmot', 'カードの\n請求が来る'),
        ('本音', 'sad_banana_cat_cry', 'ボーナスは\n通り過ぎる\nもの', 'dance_filmed_by_gray_cat', '夏のボーナスで\nなんとかする'),
    ]
    return Wd.vs_rows(ST, rows, heads=('20代', '40代'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}20代vs40代", 96, Wd.BLACK, 95), ("{y}冬のボーナスの使い道", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_151_bonus_nendai.mp4"), os.path.join(Wd.HERE, "out", "short_151_bonus_nendai_preview"))
