"""ショート134：彼氏vs彼女　LINEの返事が来ない時（world_short.py・段階でくらべる型・11/22 ユーザー指定：候補15番）。59.9秒。

python3 catmeme/short_134_line_danjo.py → out/short_134_line_danjo.mp4
- ベンチマークで伸びている「男女の比べっこ」型（11/20 調査）。ほのぼのにある題材とは被らないものを選んだ（11/22 全タイトルで確認）
- 札は送ってからの時間。右＝彼女、左＝彼氏（相手の返事を待つときの反応）
- 段階ごとに「札だけ → 右の猫（彼女）→ 左の猫（彼氏）」の3段。どちらもけなさない、よくあるイメージ。BGM なし
"""
import os

import world_short as Wd

ST = 'bg14_home_night'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫＝彼女, 右の説明, 左の猫＝彼氏, 左の説明)
    rows = [
        ('1分後', 'think_chin_paw_orange_cat', '返事\nまだかな', 'calm_black_face_sheep', '送ったことを\n忘れてる'),
        ('5分後', 'stare_tabby_wide_eyes_cat', '既読\nつかない', 'work_typing_cat', 'ゲーム中'),
        ('15分後', 'peek_what_happen_cat', 'トーク画面を\n何度も開く', 'smug_squint_bicolor_cat', '動画を\n見てる'),
        ('30分後', 'scream_phone_orange_cat', '追いLINE', 'happy_hamster_open_arms', '気にしない'),
        ('1時間後', 'glare_disgusted_cat', 'SNSは\n更新してる…', 'dance_cute_dog', 'お風呂'),
        ('2時間後', 'confused_i_dont_know_cat', '友達に相談', 'sleepy_sleepy_cat', '寝る準備'),
        ('3時間後', 'rage_talking_cat', 'スタンプ\n連打', 'sleep_sleeping_cat', '爆睡'),
        ('次の朝', 'despair_dramatic_kitten', '既読無視って\nこと？', 'dance_tabby_standing_cat', 'おはよう！'),
        ('返事', 'angry_cat_hits_cat', '怒ってない', 'stare_interviewer_cat', 'なんで\n怒ってるの？'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=('彼氏', '彼女'))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}彼氏vs彼女", 96, Wd.BLACK, 95), ("{y}LINEの返事が来ない時", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_134_line_danjo.mp4"), os.path.join(Wd.HERE, "out", "short_134_line_danjo_preview"))
