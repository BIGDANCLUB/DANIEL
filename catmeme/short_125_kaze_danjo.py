"""ショート125：彼氏vs彼女　風邪をひいた時（world_short.py・段階でくらべる型・11/20 ユーザー指定：候補13番（11/21））。59.9秒。

python3 catmeme/short_125_kaze_danjo.py → out/short_125_kaze_danjo.mp4
- ベンチマークで伸びている「男女の比べっこ」型（11/20 調査）。ほのぼのにある題材とは被らないものを選んだ
- 札は体温。右＝彼女、左＝彼氏（同じ体温のときの反応）
- 段階ごとに「札だけ → 右の猫（彼女）→ 左の猫（彼氏）」の3段。どちらもけなさない、よくあるイメージ。BGM なし
"""
import os

import world_short as Wd

ST = 'bg02_room'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫＝彼女, 右の説明, 左の猫＝彼氏, 左の説明)
    rows = [
        ('36.8℃', 'calm_black_face_sheep', 'ちょっと\nだるいかも', 'stare_tabby_wide_eyes_cat', 'なんか\n熱っぽい'),
        ('37.0℃', 'work_typing_cat', '普通に\n出勤', 'sad_looking_away_tabby', '会社に\n休みの連絡'),
        ('37.2℃', 'dance_cute_dog', '家事も\nいつも通り', 'despair_dramatic_kitten', 'もうダメ\nかもしれない'),
        ('37.5℃', 'think_chin_paw_orange_cat', '薬飲んで\n寝れば治る', 'blank_black_cat_zoning_out', '遺言を\n書く'),
        ('37.8℃', 'listen_dancing_dog', 'おかゆ\n作るね', 'smug_squint_bicolor_cat', 'アイス\n買ってきて'),
        ('38.0℃', 'stare_interviewer_cat', 'ちょっと\nしんどい', 'scream_phone_orange_cat', '救急車\n呼んで'),
        ('38.5℃', 'cocky_dj_cat', 'ご飯\n作るね', 'sad_banana_cat_cry', '人生を\n振り返る'),
        ('39.0℃', 'confused_i_dont_know_cat', 'さすがに\n病院行く', 'stare_lying_tabby_cat', '天に\n召される'),
        ('次の日', 'money_counting_orange_cat', 'まだ\nちょっとだるい', 'happy_hamster_open_arms', '全快！\n焼肉行こう'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}彼氏vs彼女", 96, Wd.BLACK, 95), ("{y}風邪をひいた時", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_125_kaze_danjo.mp4"), os.path.join(Wd.HERE, "out", "short_125_kaze_danjo_preview"))
