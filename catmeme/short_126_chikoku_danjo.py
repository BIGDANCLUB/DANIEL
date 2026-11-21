"""ショート126：彼氏vs彼女　相手が遅れた時（world_short.py・段階でくらべる型・11/20 ユーザー指定：候補15番（11/21））。59.9秒。

python3 catmeme/short_126_chikoku_danjo.py → out/short_126_chikoku_danjo.mp4
- ベンチマークで伸びている「男女の比べっこ」型（11/20 調査）。ほのぼのにある題材とは被らないものを選んだ
- 札は相手の遅れ。右＝彼氏が遅れた時の彼女、左＝彼女が遅れた時の彼氏
- 段階ごとに「札だけ → 右の猫（彼女）→ 左の猫（彼氏）」の3段。どちらもけなさない、よくあるイメージ。BGM なし
"""
import os

import world_short as Wd

ST = 'bg54_station_crowd_map'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫＝彼女, 右の説明, 左の猫＝彼氏, 左の説明)
    rows = [
        ('1分', 'glare_disgusted_cat', '遅い', 'calm_black_face_sheep', '全然\n大丈夫'),
        ('5分', 'think_chin_paw_orange_cat', '連絡は？', 'work_typing_cat', 'スマホ\nいじる'),
        ('10分', 'stare_tabby_wide_eyes_cat', '既読\nつかない', 'smug_squint_bicolor_cat', 'コンビニで\n立ち読み'),
        ('15分', 'sad_looking_away_tabby', 'もう\n帰ろうかな', 'listen_dancing_dog', 'ゲーム\n1周'),
        ('30分', 'rage_talking_cat', '怒りを\nためる', 'happy_hamster_open_arms', 'まだ\n余裕'),
        ('1時間', 'scream_phone_orange_cat', '友達に\n実況する', 'cocky_dj_cat', '1人で\nカフェに入る'),
        ('1時間半', 'despair_dramatic_kitten', '本当に\n帰る', 'dance_cute_dog', '店員と\n仲良くなる'),
        ('2時間', 'rizz_cat_rizz', '1人で\n焼肉', 'confused_i_dont_know_cat', 'ちょっと\n心配'),
        ('到着', 'stare_lying_tabby_cat', '（無言）', 'stare_interviewer_cat', '全然\n待ってないよ'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}彼氏vs彼女", 96, Wd.BLACK, 95), ("{y}相手が遅れた時", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_126_chikoku_danjo.mp4"), os.path.join(Wd.HERE, "out", "short_126_chikoku_danjo_preview"))
