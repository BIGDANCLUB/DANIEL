"""ショート139：日本vs世界　親への仕送りの金額への反応（world_short.py・段階でくらべる型・11/24 ユーザー指定：「生々しい話題」候補4番）。59.9秒。

python3 catmeme/short_139_shiokuri.py → out/short_139_shiokuri.mp4
- 11/24 分析：自分の上位は日本vs世界と男女・夫婦。お金やトラブルがからむ「生々しい」題材で、札は数字
- 11/24 ユーザー指定：少し前の形に戻す（猫は大きくしない・字幕はそれぞれの側・Wd.vs_rows の ref=False）
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どの国・人もけなさない
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg14_home_night'


def cuts():
    # (札, 右の猫＝世界, 右の字幕, 左の猫＝日本, 左の字幕)
    rows = [
        ('月0円', 'calm_black_face_sheep', 'ふつう', 'sad_looking_away_tabby', 'ちょっと\n罪悪感'),
        ('月1万円', 'happy_hamster_open_arms', 'やさしいね', 'work_typing_cat', '親孝行\nしてる気分'),
        ('月3万円', 'dance_cute_dog', '家族だから\n当然', 'think_chin_paw_orange_cat', '自分の貯金が\n減っていく'),
        ('月5万円', 'listen_dancing_dog', '兄弟みんなで\n出し合う', 'stare_tabby_wide_eyes_cat', '誰にも\n相談できない'),
        ('月10万円', 'cocky_dj_cat', '実家を\nリフォーム', 'despair_dramatic_kitten', '結婚が\n遠のく'),
        ('親の入院', 'stare_interviewer_cat', '保険で\nまかなう', 'scream_phone_orange_cat', '有給が\n消える'),
        ('実家の車検', 'rizz_cat_rizz', '親が\n自分で払う', 'money_counting_orange_cat', 'なぜか\n自分が払う'),
        ('お正月', 'dance_edm_cat', '家族で\nパーティー', 'sad_banana_cat_cry', 'おいめいに\nお年玉'),
        ('親の一言', 'dance_filmed_by_gray_cat', 'ありがとう', 'blank_black_cat_zoning_out', 'そろそろ\n結婚は？'),
    ]
    return Wd.vs_rows(ST, rows, heads=('日本', '世界'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}親への仕送りの金額への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_139_shiokuri.mp4"), os.path.join(Wd.HERE, "out", "short_139_shiokuri_preview"))
