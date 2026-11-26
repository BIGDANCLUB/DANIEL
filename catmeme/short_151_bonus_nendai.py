"""ショート151：20代vs40代　冬のボーナスの使い道（world_short.py・段階でくらべる型・11/26 ユーザー指定：146 が伸びたので20代vs40代の続き・候補3番）。59.9秒。

python3 catmeme/short_151_bonus_nendai.py → out/short_151_bonus_nendai.mp4
- 11/24 の決まり：題材は「生々しさ」「コメントが増えそう」・字幕は生々しく人間味あふれる本音・固定コメント案を付ける
- 11/26 修正：3日目40代「洗濯機が壊れる」・1週間後20代「ソシャゲガチャへ課金」・1月20代「口座には何も残っていない」・本音20代「夏のボーナスはよ！！」・素材を全部見直し（初期の素材も含めて最近使っていないもの中心・150 とも重ならない。最後のスマホ猫と踊る猫はそのまま）
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
        ('入金の朝', 'ignore_orange_cat_sniffed', '明細を\nそっと閉じる', 'huh_huh_cat', '金額を\n二度見'),
        ('1日目', 'money_counting_orange_cat', '住宅ローンの\nボーナス払い', 'showoff_gojo_cosplay_cat', '新しい\nスマホを予約'),
        ('2日目', 'sulk_hungry_cat', '子どもの\n冬休み費用', 'dance_wild_dog', '友達と\n旅行の計画'),
        ('3日目', 'spit_not_my_taste_cat', '洗濯機が\n壊れる', 'flip_emo_cat_hair', 'ちょっといい\n時計'),
        ('1週間後', 'talk_orange_white_sitting_cat', '親にも\nちょっと渡す', 'spin_spinning_cat', 'ソシャゲ\nガチャへ課金'),
        ('2週間後', 'think_bike_front_seat_cat', '新NISAに\n少しだけ', 'dance_white_dog', '年末の\n飲み会ラッシュ'),
        ('年末', 'meow_ragdoll_chubby_cat', 'お年玉で\n消える', 'peek_what_happen_cat', 'あれ…\n残りいくら？'),
        ('1月', 'stand_real_sheep', '自分には\n何も残ってない', 'weird_meowing_cat', '口座には\n何も\n残っていない'),
        ('本音', 'leave_cat_leaves_home', 'ボーナスは\n通り過ぎる\nもの', 'dance_filmed_by_gray_cat', '夏のボーナス\nはよ！！'),
    ]
    return Wd.vs_rows(ST, rows, heads=('20代', '40代'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}20代vs40代", 96, Wd.BLACK, 95), ("{y}冬のボーナスの使い道", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_151_bonus_nendai.mp4"), os.path.join(Wd.HERE, "out", "short_151_bonus_nendai_preview"))
