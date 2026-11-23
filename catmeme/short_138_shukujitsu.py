"""ショート138：日本vs世界　祝日の数への反応（world_short.py・段階でくらべる型・11/23 ユーザー指定：候補9番）。59.9秒。

python3 catmeme/short_138_shukujitsu.py → out/short_138_shukujitsu.mp4
- 11/23 分析（research/own_shorts_20261123.md）：札が数字の日本vs世界がいちばん強い → 数字の段で作る
- 11/23 ユーザー指定：ベンチマークのようにエフェクト増し（Wd.vs_rows：絵文字スタンプは抜いた・線がゆれる・背景が流れる・猫大きめ・字幕は下まん中で色分け）
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どの国・人もけなさない
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg109_calendar'


def cuts():
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('年5日', 'glare_disgusted_cat', '少ない', 'calm_black_face_sheep', '気づかない', '📅', '🤔'),
        ('年8日', 'calm_black_face_sheep', 'ふつう', 'smug_squint_bicolor_cat', 'まだまだ', '📅', '📅'),
        ('年10日', 'dance_cute_dog', '多いね', 'think_chin_paw_orange_cat', 'やっと\n半分以上', '🎉', '📅'),
        ('年12日', 'listen_dancing_dog', '旅行の\n計画', 'happy_hamster_open_arms', '3連休が\n増える', '✈️', '🎌'),
        ('年14日', 'stare_tabby_wide_eyes_cat', 'もう\n十分', 'work_typing_cat', '連休の予定を\n立てる', '🙆', '📝'),
        ('年16日', 'surprise_big_pupils_cat', 'そんなに？', 'confused_i_dont_know_cat', '日本の\n祝日の数', '😲', '🇯🇵'),
        ('祝日当日', 'cocky_dj_cat', '店も\n全部休み', 'sad_looking_away_tabby', 'サービス業は\n出勤', '🏪', '🏬'),
        ('有給', 'rizz_cat_rizz', '祝日より\n有給で休む', 'despair_dramatic_kitten', '祝日があるから\n有給は使わない', '🏖️', '💼'),
        ('振替休日', 'dance_filmed_by_gray_cat', '何それ', 'dance_edm_cat', '月曜休み\n最高', '❓', '🎉'),
    ]
    return Wd.vs_rows(ST, rows)


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}祝日の数への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_138_shukujitsu.mp4"), os.path.join(Wd.HERE, "out", "short_138_shukujitsu_preview"))
