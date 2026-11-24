"""ショート147：日本vs世界　昇給額への反応（world_short.py・段階でくらべる型・11/24 ユーザー指定：候補18番）。59.9秒。

python3 catmeme/short_147_shokyu.py → out/short_147_shokyu.mp4
- 11/24 の決まり：題材は「生々しさ」「コメントが増えそう」・字幕は生々しく人間味あふれる本音・固定コメント案を付ける
- Wd.vs_rows（少し前の形：猫は大きくしない・字幕はそれぞれの側・左に移っても右の字幕は残す）
- 段階ごとに「札だけ → 右の猫（世界）→ 左の猫（日本）」の3段。どちらもけなさない
- 概要欄の注意：※よくあるイメージです（国や人によって違います）。BGM なし
"""
import os

import world_short as Wd

ST = 'bg25_office_desk'


def cuts():
    # (札, 右の猫＝世界, 右の字幕, 左の猫＝日本, 左の字幕)
    rows = [
        ('月+1000円', 'glare_disgusted_cat', '転職サイトに\n登録する', 'happy_hamster_open_arms', '上がっただけ\nマシ'),
        ('月+3000円', 'calm_black_face_sheep', 'バカに\nしてる？', 'smug_squint_bicolor_cat', '社会保険料で\n消える'),
        ('月+5000円', 'stare_tabby_wide_eyes_cat', '物価のほうが\n上がってる', 'think_chin_paw_orange_cat', '同期と\n100円単位で比べる'),
        ('月+1万円', 'dance_cute_dog', 'ふつう', 'cocky_dj_cat', '今日は\nちょっといいビール'),
        ('月+2万円', 'listen_dancing_dog', 'まあまあ', 'rizz_cat_rizz', '仕事を\n3倍任される'),
        ('月+5万円', 'dance_edm_cat', 'やっと\n交渉が通った', 'surprise_big_pupils_cat', '役職がついて\n残業代が消える'),
        ('月+10万円', 'showoff_gojo_cosplay_cat', '転職した', 'scream_standing_marmot', '社長の親戚'),
        ('昇給なし', 'rage_talking_cat', '明日\n辞めます', 'sad_banana_cat_cry', '「来年は\n期待してて」\n5年目'),
        ('交渉', 'dance_filmed_by_gray_cat', '自分から\n言う', 'blank_black_cat_zoning_out', '言ったら\n空気が凍る'),
    ]
    return Wd.vs_rows(ST, rows, heads=('日本', '世界'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}昇給額への反応", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_147_shokyu.mp4"), os.path.join(Wd.HERE, "out", "short_147_shokyu_preview"))
