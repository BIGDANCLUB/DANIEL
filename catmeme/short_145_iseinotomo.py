"""ショート145：彼氏vs彼女　異性の友達と2人で会う回数（world_short.py・段階でくらべる型・11/24 ユーザー指定：候補13番）。59.9秒。

python3 catmeme/short_145_iseinotomo.py → out/short_145_iseinotomo.mp4
- 11/24 の決まり：題材は「生々しさ」「コメントが増えそう」・字幕は生々しく人間味あふれる本音・固定コメント案を付ける
- Wd.vs_rows（少し前の形：猫は大きくしない・字幕はそれぞれの側・左に移っても右の字幕は残す）
- 段階ごとに「札だけ → 右の猫（彼女）→ 左の猫（彼氏）」の3段。どちらもけなさない
- 概要欄の注意：※よくあるイメージです。BGM なし
"""
import os

import world_short as Wd

ST = 'bg13_izakaya'


def cuts():
    # (札, 右の猫＝彼女, 右の字幕, 左の猫＝彼氏, 左の字幕)
    rows = [
        ('年1回', 'calm_black_face_sheep', 'まあいいよ', 'smug_squint_bicolor_cat', '同窓会の\nついでだし'),
        ('半年に1回', 'think_chin_paw_orange_cat', 'どこで\n何食べたの？', 'work_typing_cat', 'ただの\n地元の友達'),
        ('3か月に1回', 'stare_tabby_wide_eyes_cat', 'インスタで\n相手を調べる', 'confused_i_dont_know_cat', '向こうは\n既婚者だよ？'),
        ('月1回', 'glare_disgusted_cat', '「私も行く」', 'sad_looking_away_tabby', 'なんで\n疑うの'),
        ('月2回', 'rage_talking_cat', '私より\n会ってない？', 'despair_dramatic_kitten', '仕事の\n相談なんだって'),
        ('週1回', 'angry_cat_hits_cat', 'スマホを\n見せて', 'scream_phone_orange_cat', '通知を\n裏返して置く'),
        ('サシ飲み', 'sad_banana_cat_cry', '私とは\n行かないのに', 'blank_black_cat_zoning_out', '2軒目は\n行ってない'),
        ('逆の立場', 'cocky_dj_cat', '私の男友達は\nただの友達', 'stare_interviewer_cat', '……それは\nダメだろ'),
        ('結論', 'dance_filmed_by_gray_cat', '許せるのは\n年1回まで', 'money_counting_orange_cat', 'たぶん\nお互いさま'),
    ]
    return Wd.vs_rows(ST, rows, heads=('彼氏', '彼女'))


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}彼氏vs彼女", 96, Wd.BLACK, 95), ("{y}異性の友達と2人で会う回数", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_145_iseinotomo.mp4"), os.path.join(Wd.HERE, "out", "short_145_iseinotomo_preview"))
