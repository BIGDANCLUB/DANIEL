"""ショート155：首都圏vs北海道　気温ごとの反応（world_short.py・段階でくらべる型・11/28 ユーザー指定）。59.9秒。

python3 catmeme/short_155_kion_hokkaido.py → out/short_155_kion_hokkaido.mp4
- 11/28 自分のチャンネル分析：伸びるのは「全員に自分の数字がある」×「札が時間・気温などの段階」
- 11/28 作り直し：伸びた動画（睡眠時間・お風呂・遅刻・プレゼント・ランチ）の字幕に合わせる＝短い言い切り（ふつう・ありえない）と具体的な行動の対比、段階が進むほど極端、最後は札をひねって（失神）とスマホ猫と踊る猫
- 11/28 ユーザー修正：15℃ カーディガンじゃ寒い・北海道は余裕そうな素材／10℃ 秋到来・ヒートテック重ね着／5℃ まだ換気で窓を開ける・ここ日本か？／0℃ Yahooニュースになる／-15℃ 雪かきダルい・(凍結済み)／-20℃ 釧路（寒そうな素材）／家の中 こたつでアイス（眠る猫）・こたつで一人パピコ(寂しい)（ぽつんとしたヒツジ）
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
        ('15℃', 'stare_aloha_gray_cat', '半袖', 'showoff_gojo_cosplay_cat', 'カーディガンじゃ\n寒い'),
        ('10℃', 'stare_interviewer_cat', '秋到来', 'punch_tabby_cat_reach', 'ヒートテック\n重ね着'),
        ('5℃', 'ride_kitten_bike', 'まだ換気で\n窓を開ける', 'sulk_hungry_cat', 'ここ日本か？'),
        ('0℃', 'dance_white_dog', 'やっと冬', 'scream_standing_marmot', 'Yahoo\nニュースになる'),
        ('-5℃', 'mock_swinging_cat', 'サンダルで\nコンビニ', 'confused_i_dont_know_cat', '水道管が\n破裂'),
        ('-10℃', 'drive_driving_cat', 'まだ\nふつう', 'despair_dramatic_kitten', '電車が\n全部止まる'),
        ('-15℃', 'stare_standing_marmot', '雪かき\nダルい', 'blank_black_cat_zoning_out', '(凍結済み)'),
        ('-20℃', 'sad_banana_cat_cry', '釧路', 'sad_black_dog', '南極'),
        ('家の中', 'sleep_sleeping_cat', 'こたつで\nアイス', 'stand_real_sheep', 'こたつで\n一人パピコ\n(寂しい)'),
    ]
    return Wd.vs_rows(ST, rows, heads=('首都圏', '北海道'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}首都圏vs北海道", 96, Wd.BLACK, 95), ("{y}気温ごとの反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_155_kion_hokkaido.mp4"), os.path.join(Wd.HERE, "out", "short_155_kion_hokkaido_preview"))
