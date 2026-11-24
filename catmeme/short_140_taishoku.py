"""ショート140：日本vs世界　退職を伝えてからの反応（world_short.py・段階でくらべる型・11/24 ユーザー指定：「生々しい話題」候補7番）。59.9秒。

python3 catmeme/short_140_taishoku.py → out/short_140_taishoku.mp4
- 11/24 分析：自分の上位は日本vs世界と男女・夫婦。お金やトラブルがからむ「生々しい」題材で、札は数字
- Wd.vs_rows（絵文字なし・線がゆれる・背景が流れる・猫大きめ・字幕は下まん中で色分け）
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どの国・人もけなさない
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg25_office_desk'


def cuts():
    # (札, 右の猫＝世界, 右の字幕, 左の猫＝日本, 左の字幕)
    rows = [
        ('当日', 'dance_cute_dog', '今日で\n辞めます', 'stare_tabby_wide_eyes_cat', '「少し\nいいですか」'),
        ('翌日', 'happy_hamster_open_arms', '次の仕事\nスタート', 'think_chin_paw_orange_cat', '上司の\n上司と面談'),
        ('1週間後', 'calm_black_face_sheep', 'もう\n覚えてない', 'sad_looking_away_tabby', '引き止め\n2回目'),
        ('2週間後', 'listen_dancing_dog', '法律どおり\n退職', 'confused_i_dont_know_cat', '「後任が\n決まるまで」'),
        ('1か月後', 'cocky_dj_cat', '新しい職場に\nなじむ', 'work_typing_cat', '引き継ぎ\n資料100枚'),
        ('有給', 'rizz_cat_rizz', '全部消化', 'despair_dramatic_kitten', '使えるか\n空気を読む'),
        ('送別会', 'dance_edm_cat', 'パーティー', 'money_counting_orange_cat', '花束代を\n自分も出す'),
        ('最終日', 'showoff_gojo_cosplay_cat', 'See you!', 'sad_banana_cat_cry', '全員に\nお菓子を配る'),
        ('退職後', 'dance_filmed_by_gray_cat', '元同僚と\n友達', 'blank_black_cat_zoning_out', 'まだ\n仕事のLINEが来る'),
    ]
    return Wd.vs_rows(ST, rows, heads=('日本', '世界'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}退職を伝えてからの反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_140_taishoku.mp4"), os.path.join(Wd.HERE, "out", "short_140_taishoku_preview"))
