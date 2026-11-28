"""ショート155：首都圏vs北海道　気温ごとの反応（world_short.py・段階でくらべる型・11/28 ユーザー指定）。59.9秒。

python3 catmeme/short_155_kion_hokkaido.py → out/short_155_kion_hokkaido.mp4
- 11/28 自分のチャンネル分析：伸びるのは「全員に自分の数字がある」×「札が時間・気温などの段階」
- 11/28 ユーザー指定：コメントを増やすため、字幕は極端かつ具体的でウケ狙い（iPhone18ProMAX のように）
- 右＝北海道、左＝首都圏。冬の季節もの（55 雪が伸びた続き）。※よくあるイメージです（地域や人によって違います）
- Wd.vs_rows（少し前の形・左に移っても右の字幕は残す・右の字幕は赤）。どの地域・国・人もけなさない
"""
import os

import world_short as Wd

ST = 'bg61_snow_onsen'


def cuts():
    # (札, 右の猫, 右の字幕, 左の猫, 左の字幕)
    rows = [
        ('15℃', 'eat_pop_cat', '暑い\n半袖でアイス', 'showoff_gojo_cosplay_cat', 'ダウン\n解禁！'),
        ('10℃', 'walk_white_duck', 'まだ\n秋', 'punch_tabby_cat_reach', 'ヒートテック\n3枚重ね'),
        ('5℃', 'ride_kitten_bike', '窓を開けて\n換気', 'sulk_hungry_cat', '寒すぎて\n会社休みたい'),
        ('0℃', 'dance_white_dog', 'やっと\n冬っぽい', 'scream_standing_marmot', '今季一番の\n寒さ速報'),
        ('-5℃', 'mock_swinging_cat', 'コンビニまで\nサンダル', 'confused_i_dont_know_cat', '水道管が凍って\n大さわぎ'),
        ('-10℃', 'drive_driving_cat', 'エンジンを\n10分あたためる', 'sad_black_dog', '生きて\nいけない'),
        ('-15℃', 'stare_standing_marmot', 'まつ毛が\n凍る', 'stare_big_eyes_tabby_kitten', '冷凍庫と\nほぼ同じ'),
        ('-20℃', 'happy_hamster_open_arms', '家の中は\n半袖で25℃', 'despair_dramatic_kitten', 'もはや\n南極'),
        ('本音', 'talk_orange_white_sitting_cat', '東京の家\n寒すぎない？', 'call_customer_service_cat', '北海道の家\nあったかすぎない？'),
    ]
    return Wd.vs_rows(ST, rows, heads=('首都圏', '北海道'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}首都圏vs北海道", 96, Wd.BLACK, 95), ("{y}気温ごとの反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_155_kion_hokkaido.mp4"), os.path.join(Wd.HERE, "out", "short_155_kion_hokkaido_preview"))
