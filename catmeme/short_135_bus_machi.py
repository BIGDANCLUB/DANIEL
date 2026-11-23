"""ショート135：日本vs世界　バスの待ち時間への反応（world_short.py・段階でくらべる型・11/23 ユーザー指定：候補1番）。59.9秒。

python3 catmeme/short_135_bus_machi.py → out/short_135_bus_machi.mp4
- 11/23 分析（research/own_shorts_20261123.md）：札が数字の日本vs世界がいちばん強い → 数字の段で作る
- 11/23 ユーザー指定：ベンチマークのようにエフェクト増し（Wd.vs_rows：絵文字スタンプは抜いた・線がゆれる・背景が流れる・猫大きめ・字幕は下まん中で色分け）
- 11/23 修正：2時間 日本「バス会社がクレームで溢れる」・時刻表の段だけ日本→世界の順（世界の猫が上）
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どの国・人もけなさない
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg48_clean_street'


def cuts():
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1分', 'dance_cute_dog', '奇跡', 'smug_squint_bicolor_cat', '時刻表どおり', '🚌', '⏱️'),
        ('3分', 'happy_hamster_open_arms', '今日は\nついてる', 'work_typing_cat', '遅れのおわびが\n流れる', '🚌', '📢'),
        ('5分', 'calm_black_face_sheep', 'すぐ来た', 'stare_tabby_wide_eyes_cat', 'アプリで\n位置を確認', '🚌', '📱'),
        ('10分', 'listen_dancing_dog', 'ふつう', 'think_chin_paw_orange_cat', '歩いたほうが\n早い？', '🚌', '🚶'),
        ('20分', 'cocky_dj_cat', 'まだ\n早いほう', 'sad_looking_away_tabby', 'タクシーを\n考える', '🚌', '🚕'),
        ('30分', 'rizz_cat_rizz', '座って\n昼寝', 'scream_phone_orange_cat', '会社に\n遅刻の連絡', '😴', '☎️'),
        ('1時間', 'dance_edm_cat', '2台まとめて\n来る', 'despair_dramatic_kitten', '時刻表を\n疑う', '🚌', '📋'),
        ('2時間', 'showoff_gojo_cosplay_cat', '今日は\n来ない日', 'blank_black_cat_zoning_out', 'バス会社が\nクレームで溢れる', '🚫', '📺'),
        ('時刻表', 'dance_filmed_by_gray_cat', 'そもそも\nない', 'money_counting_orange_cat', '1分単位', '❓', '🕐', 'J'),
    ]
    return Wd.vs_rows(ST, rows)


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}バスの待ち時間への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_135_bus_machi.mp4"), os.path.join(Wd.HERE, "out", "short_135_bus_machi_preview"))
