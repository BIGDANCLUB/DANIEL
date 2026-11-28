"""ショート142：日本vs世界　転職回数への反応（world_short.py・段階でくらべる型・11/24 ユーザー指定：「生々しい話題」候補25番）。59.9秒。

python3 catmeme/short_142_tenshoku_kaisu.py → out/short_142_tenshoku_kaisu.mp4
- 11/24 分析：自分の上位は日本vs世界と男女・夫婦。お金やトラブルがからむ「生々しい」題材で、札は数字
- 11/26 修正：素材を全部見直し（初期の素材も含めて最近使っていないもの中心・150/151 と重ならない）・右の字幕は赤・2回 日本「すぐ辞めない？」
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
        ('0回', 'taunt_cat_and_scared_dog', '挑戦\nしないの？', 'wave_waving_cat', '真面目で\nいいね'),
        ('1回', 'calmdown_dancing_cat', 'ふつう', 'stare_big_eyes_tabby_kitten', '理由を\n深く聞かれる'),
        ('2回', 'laugh_laughing_dog', '経験豊富', 'stare_standing_marmot', 'すぐ\n辞めない？'),
        ('3回', 'dance_trending_cat', 'キャリア\nアップ', 'meow_gray_white_kitten', '書類で\n落ちはじめる'),
        ('4回', 'eat_pop_cat', '年収も\n上がった', 'itchy_kitten_butt', '職歴欄が\n足りない'),
        ('5回', 'dance_happy_banana_cat', '引っぱりだこ', 'scold_talking_cats', '面接官が\nざわつく'),
        ('7回', 'drive_monkey_golf_cart', '管理職に', 'film_phone_orange_white_cats', '履歴書が\n2枚目に'),
        ('10回', 'shady_dancing_man', 'プロの\n転職者', 'walk_approaching_orange_cat', 'もう\n自分で起業'),
        ('面接の質問', 'call_customer_service_cat', '何が\nできますか？', 'tense_two_cats_face_off', 'なぜ\n辞めたんですか？'),
    ]
    return Wd.vs_rows(ST, rows, heads=('日本', '世界'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}転職回数への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_142_tenshoku_kaisu.mp4"), os.path.join(Wd.HERE, "out", "short_142_tenshoku_kaisu_preview"))
