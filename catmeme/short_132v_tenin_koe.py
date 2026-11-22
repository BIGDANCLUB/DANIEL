"""ショート132v：日本vs世界 店員さんの声かけ回数【読み上げ版】（11/22 ユーザー指定：ずんだもん読み上げ形式の1本目）。

python3 catmeme/short_132v_tenin_koe.py → out/short_132v_tenin_koe.mp4
- 中身は132と同じ。voice_short.py で、ずんだもんが「札＋世界」→字幕→「日本」→字幕を読む。長さは読み上げに合わせる
- 台本：scripts/short_132_yomiage_zundamon.txt。概要欄に「VOICEVOX:ずんだもん」
"""
import os

import voice_short as V
import world_short as Wd

ROWS = [
    ('1回', 'happy_hamster_open_arms', 'How are you?\nから雑談', 'work_typing_cat', 'いらっしゃい\nませ'),
    ('2回', 'dance_cute_dog', '名前を\n覚えられる', 'stare_tabby_wide_eyes_cat', 'ポイントカード\nお持ちですか？'),
    ('3回', 'listen_dancing_dog', '家族の話に\nなる', 'think_chin_paw_orange_cat', '袋は\nご利用ですか？'),
    ('5回', 'cocky_dj_cat', 'もう友達', 'calm_black_face_sheep', '温めますか？\n（冷たい）'),
    ('7回', 'rizz_cat_rizz', 'パーティーに\n誘われる', 'confused_i_dont_know_cat', 'お箸\nおつけしますか？'),
    ('10回', 'dance_edm_cat', '結婚式に\n呼ばれる', 'stare_interviewer_cat', 'レシートは\nご入用ですか'),
    ('15回', 'smug_squint_bicolor_cat', 'ほぼ親戚', 'blank_black_cat_zoning_out', '全部\n大丈夫です'),
    ('20回', 'showoff_gojo_cosplay_cat', '従業員として\n誘われる', 'sad_looking_away_tabby', 'セルフレジを\n探す'),
    ('帰り際', 'dance_filmed_by_gray_cat', 'See you!', 'cocky_dj_cat', 'っざぁしたぁ～\n（ｵﾗｲｯｵﾗｲｯ）'),
]


if __name__ == "__main__":
    V.build("132v_tenin_koe", "bg15_convenience", ROWS, ("日本", "世界"),
            Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}店員さんの声かけ回数", 90, Wd.BLACK, 245)], 0, 330),
            os.path.join(Wd.HERE, "scripts", "short_132_yomiage_zundamon.txt"))
