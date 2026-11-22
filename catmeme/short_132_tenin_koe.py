"""ショート132：日本vs世界　店員さんの声かけ回数（world_short.py・段階でくらべる型・11/22 ユーザー指定：候補11（差し替え案）番）。59.9秒。

python3 catmeme/short_132_tenin_koe.py → out/short_132_tenin_koe.mp4
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どの国・人もけなさない
- ベンチマーク3チャンネルの全タイトル（ほのぼの248・40代独身229・おひとりさま7）と被らないことを確認ずみ（11/22）
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg15_convenience'
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1回', 'happy_hamster_open_arms', 'How are you?\nから雑談', 'work_typing_cat', 'いらっしゃい\nませ'),
        ('2回', 'dance_cute_dog', '名前を\n覚えられる', 'stare_tabby_wide_eyes_cat', 'ポイントカード\nお持ちですか？'),
        ('3回', 'listen_dancing_dog', '家族の話に\nなる', 'think_chin_paw_orange_cat', '袋は\nご利用ですか？'),
        ('5回', 'cocky_dj_cat', 'もう友達', 'calm_black_face_sheep', '温めますか？'),
        ('7回', 'rizz_cat_rizz', 'パーティーに\n誘われる', 'confused_i_dont_know_cat', 'お箸\nおつけしますか？'),
        ('10回', 'dance_edm_cat', '結婚式に\n呼ばれる', 'stare_interviewer_cat', 'レシートは\nいりますか？'),
        ('15回', 'smug_squint_bicolor_cat', 'ほぼ親戚', 'blank_black_cat_zoning_out', '全部\n大丈夫です'),
        ('20回', 'showoff_gojo_cosplay_cat', '店を継ぐ', 'sad_looking_away_tabby', 'セルフレジを\n探す'),
        ('帰り際', 'dance_filmed_by_gray_cat', 'See you!', 'despair_dramatic_kitten', 'またお越し\nくださいませ'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}店員さんの声かけ回数", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_132_tenin_koe.mp4"), os.path.join(Wd.HERE, "out", "short_132_tenin_koe_preview"))
