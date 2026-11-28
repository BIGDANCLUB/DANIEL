"""ショート136：日本vs世界　ご飯の量への反応（world_short.py・段階でくらべる型・11/23 ユーザー指定：候補2番）。59.9秒。

python3 catmeme/short_136_gohan_ryo.py → out/short_136_gohan_ryo.mp4
- 11/23 分析（research/own_shorts_20261123.md）：札が数字の日本vs世界がいちばん強い → 数字の段で作る
- 11/23 ユーザー指定：ベンチマークのようにエフェクト増し（Wd.vs_rows：絵文字スタンプは抜いた・線がゆれる・背景が流れる・猫大きめ・字幕は下まん中で色分け）
- 11/24 ユーザー指定：少し前の形に戻す（猫は大きくしない・字幕はそれぞれの側・Wd.vs_rows の ref=False）
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どの国・人もけなさない
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg67_food_sample'


def cuts():
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('150g', 'glare_disgusted_cat', '子ども用？', 'happy_hamster_open_arms', 'ふつう盛り', '🍚', '🍚'),
        ('200g', 'calm_black_face_sheep', '前菜', 'smug_squint_bicolor_cat', '大盛り無料', '🥗', '🍚'),
        ('300g', 'dance_cute_dog', 'やっと\nふつう', 'stare_tabby_wide_eyes_cat', '特盛', '🍛', '🍚'),
        ('400g', 'listen_dancing_dog', 'パンも\nつける', 'think_chin_paw_orange_cat', '残したら\nどうしよう', '🍞', '😰'),
        ('500g', 'cocky_dj_cat', 'おかわり', 'sad_looking_away_tabby', '苦しい', '🍽️', '🤢'),
        ('700g', 'rizz_cat_rizz', '持ち帰り用の\n箱をもらう', 'scream_standing_marmot', '完食したら\n無料', '📦', '🏆'),
        ('1kg', 'dance_edm_cat', '家族で\nシェア', 'despair_dramatic_kitten', '写真を\n撮られる', '👨‍👩‍👧', '📸'),
        ('2kg', 'showoff_gojo_cosplay_cat', 'パーティー用', 'blank_black_cat_zoning_out', 'テレビの\n大食い企画', '🎉', '📺'),
        ('残したら', 'dance_filmed_by_gray_cat', '持って帰る', 'sad_banana_cat_cry', '罪悪感', '🥡', '😢'),
    ]
    return Wd.vs_rows(ST, rows)


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}ご飯の量への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_136_gohan_ryo.mp4"), os.path.join(Wd.HERE, "out", "short_136_gohan_ryo_preview"))
