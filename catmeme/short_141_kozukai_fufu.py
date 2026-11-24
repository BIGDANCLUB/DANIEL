"""ショート141：夫vs妻　おこづかいの金額への反応（world_short.py・段階でくらべる型・11/24 ユーザー指定：「生々しい話題」候補12番）。59.9秒。

python3 catmeme/short_141_kozukai_fufu.py → out/short_141_kozukai_fufu.mp4
- 11/24 分析：自分の上位は日本vs世界と男女・夫婦。お金やトラブルがからむ「生々しい」題材で、札は数字
- Wd.vs_rows（絵文字なし・線がゆれる・背景が流れる・猫大きめ・字幕は下まん中で色分け）
- 段階ごとに「札だけ → 右の猫（妻）→ 左の猫（夫）」の3段。どの国・人もけなさない
- 概要欄の注意：※よくあるイメージです。BGM なし
"""
import os

import world_short as Wd

ST = 'bg02_room'


def cuts():
    # (札, 右の猫＝妻, 右の字幕, 左の猫＝夫, 左の字幕)
    rows = [
        ('月1万円', 'calm_black_face_sheep', '十分でしょ', 'sad_looking_away_tabby', '昼ごはんで\n消える'),
        ('月2万円', 'work_typing_cat', '家計は\nきびしい', 'think_chin_paw_orange_cat', '飲み会1回で\n半分'),
        ('月3万円', 'smug_squint_bicolor_cat', '平均くらい', 'happy_hamster_open_arms', 'やっと\n人間らしく'),
        ('月5万円', 'glare_disgusted_cat', '多くない？', 'cocky_dj_cat', '趣味を\n再開'),
        ('値上げ交渉', 'stare_interviewer_cat', '理由は？', 'confused_i_dont_know_cat', '物価が\n上がった'),
        ('ボーナス', 'money_counting_orange_cat', '家のローンへ', 'despair_dramatic_kitten', '1万円だけ\nもらえた'),
        ('飲み会', 'rage_talking_cat', 'また？', 'sad_banana_cat_cry', '断れない\n付き合い'),
        ('へそくり', 'angry_cat_hits_cat', '見つけた', 'scream_standing_marmot', 'なんで\nわかるの'),
        ('月末', 'dance_filmed_by_gray_cat', '家計は黒字', 'blank_black_cat_zoning_out', '財布に\n200円'),
    ]
    return Wd.vs_rows(ST, rows, heads=('夫', '妻'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}夫vs妻", 96, Wd.BLACK, 95), ("{y}おこづかいの金額への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_141_kozukai_fufu.mp4"), os.path.join(Wd.HERE, "out", "short_141_kozukai_fufu_preview"))
