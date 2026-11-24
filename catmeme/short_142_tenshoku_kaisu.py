"""ショート142：日本vs世界　転職回数への反応（world_short.py・段階でくらべる型・11/24 ユーザー指定：「生々しい話題」候補25番）。59.9秒。

python3 catmeme/short_142_tenshoku_kaisu.py → out/short_142_tenshoku_kaisu.mp4
- 11/24 分析：自分の上位は日本vs世界と男女・夫婦。お金やトラブルがからむ「生々しい」題材で、札は数字
- 11/24 ユーザー指定：少し前の形に戻す（猫は大きくしない・字幕はそれぞれの側・Wd.vs_rows の ref=False）
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どの国・人もけなさない
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg05_meeting'


def cuts():
    # (札, 右の猫＝世界, 右の字幕, 左の猫＝日本, 左の字幕)
    rows = [
        ('0回', 'calm_black_face_sheep', '挑戦\nしないの？', 'smug_squint_bicolor_cat', '真面目で\nいいね'),
        ('1回', 'dance_cute_dog', 'ふつう', 'work_typing_cat', '理由を\n深く聞かれる'),
        ('2回', 'happy_hamster_open_arms', '経験豊富', 'think_chin_paw_orange_cat', '「すぐ辞めない？」'),
        ('3回', 'listen_dancing_dog', 'キャリア\nアップ', 'stare_tabby_wide_eyes_cat', '書類で\n落ちはじめる'),
        ('4回', 'cocky_dj_cat', '年収も\n上がった', 'sad_looking_away_tabby', '職歴欄が\n足りない'),
        ('5回', 'rizz_cat_rizz', '引っぱりだこ', 'despair_dramatic_kitten', '面接官が\nざわつく'),
        ('7回', 'dance_edm_cat', '管理職に', 'scream_phone_orange_cat', '履歴書が\n2枚目に'),
        ('10回', 'showoff_gojo_cosplay_cat', 'プロの\n転職者', 'blank_black_cat_zoning_out', 'もう\n自分で起業'),
        ('面接の質問', 'dance_filmed_by_gray_cat', '何が\nできますか？', 'money_counting_orange_cat', 'なぜ\n辞めたんですか？'),
    ]
    return Wd.vs_rows(ST, rows, heads=('日本', '世界'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}転職回数への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_142_tenshoku_kaisu.mp4"), os.path.join(Wd.HERE, "out", "short_142_tenshoku_kaisu_preview"))
