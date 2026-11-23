"""ショート137：日本vs世界　通勤の交通費への反応（world_short.py・段階でくらべる型・11/23 ユーザー指定：候補3番）。59.9秒。

python3 catmeme/short_137_kotsuhi.py → out/short_137_kotsuhi.mp4
- 11/23 分析（research/own_shorts_20261123.md）：札が数字の日本vs世界がいちばん強い → 数字の段で作る
- 11/23 ユーザー指定：ベンチマークのようにエフェクト増し（Wd.vs_rows：絵文字の小道具が揺れる・線がゆれる・背景が流れる・猫大きめ・字幕は下まん中で色分け）
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どの国・人もけなさない
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg54_station_crowd_map'


def cuts():
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('月5000円', 'calm_black_face_sheep', '自腹で\n払う', 'smug_squint_bicolor_cat', '会社が\n出してくれる', '💸', '🏢'),
        ('月1万円', 'dance_cute_dog', '自転車に\nする', 'work_typing_cat', '定期券で\n寄り道し放題', '🚲', '🎫'),
        ('月2万円', 'think_chin_paw_orange_cat', '会社の近くに\n引っ越す', 'happy_hamster_open_arms', 'まだ\n会社が出す', '🏠', '💴'),
        ('月3万円', 'listen_dancing_dog', '在宅勤務\n一択', 'stare_tabby_wide_eyes_cat', '上限\nギリギリ', '💻', '📏'),
        ('月5万円', 'glare_disgusted_cat', '転職を\n考える', 'confused_i_dont_know_cat', '上限をこえて\n一部自腹', '📝', '💸'),
        ('月8万円', 'cocky_dj_cat', '車を売る', 'rizz_cat_rizz', '新幹線通勤も\n出る会社', '🚗', '🚄'),
        ('月10万円', 'scream_phone_orange_cat', '給料の\n半分', 'money_counting_orange_cat', '税金が\nかからない', '😱', '🙌'),
        ('月15万円', 'despair_dramatic_kitten', '通勤を\nあきらめる', 'stare_interviewer_cat', 'これ以上は\n税金がかかる', '🏳️', '🧾'),
        ('引っ越し', 'dance_filmed_by_gray_cat', '職場の隣に\n住む', 'sad_looking_away_tabby', '通勤2時間でも\n家は郊外', '🏢', '🏡'),
    ]
    return Wd.vs_rows(ST, rows)


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}通勤の交通費への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_137_kotsuhi.mp4"), os.path.join(Wd.HERE, "out", "short_137_kotsuhi_preview"))
