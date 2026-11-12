"""ショート90：日本vs世界 半額シールの時間（world_short.py・段階でくらべる型・11/12 ユーザー指定：候補2番）。59.9秒。

python3 catmeme/short_90_hangaku.py → out/short_90_hangaku.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg16_food_aisle"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('17時', 'stare_interviewer_cat', 'ふつうに\n買う', 'think_chin_paw_orange_cat', '様子見'),
        ('18時', 'calm_black_face_sheep', 'もう\n家で料理', 'stare_lying_tabby_cat', '惣菜コーナーを\nうろうろ'),
        ('19時', 'glare_disgusted_cat', 'セール？', 'peek_what_happen_cat', '店員さんの\n動きを見張る'),
        ('19時半', 'sleepy_sleepy_cat', 'もう寝る', 'surprise_big_pupils_cat', '2割引の\nシール発見'),
        ('20時', 'dance_cute_dog', '気にしない', 'angry_aiming_cat', '半額を待つか\n2割引で買うか'),
        ('20時半', 'listen_dancing_dog', '？', 'scream_standing_marmot', '半額シール\n貼られた!!'),
        ('20時31分', 'huh_huh_cat', 'なにごと？', 'fight_cat_fight', '争奪戦'),
        ('閉店前', 'stare_aloha_gray_cat', 'お店\n閉まってる', 'despair_dramatic_kitten', '残っているのは\nパセリだけ'),
        ('家で', 'happy_hamster_open_arms', '手料理', 'eat_pop_cat', '半額のお寿司が\n人生の\nごほうび'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}半額シールの時間", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_90_hangaku.mp4"), os.path.join(Wd.HERE, "out", "short_90_hangaku_preview"))
