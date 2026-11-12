"""ショート94：日本vs世界 渋滞の長さ（world_short.py・段階でくらべる型・11/12 ユーザー指定：候補11番）。59.9秒。

python3 catmeme/short_94_jutai.py → out/short_94_jutai.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg28_jp_highway"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1km', 'calm_black_face_sheep', 'ふつう', 'drive_driving_cat', 'ふつう'),
        ('5km', 'glare_disgusted_cat', 'クラクション', 'think_chin_paw_orange_cat', 'サービスエリアを\n調べる'),
        ('10km', 'fight_cat_fight', '大さわぎ', 'eat_chips_cat', 'お菓子を\n開ける'),
        ('20km', 'leave_cat_leaves_home', '引き返す', 'sleepy_old_memories_cat', 'しりとり\nスタート'),
        ('30km', 'scream_standing_marmot', '警察を\n呼ぶ', 'stare_lying_tabby_cat', 'トイレの\nがまん'),
        ('40km', 'surprise_big_pupils_cat', '車を\n置いて歩く', 'despair_dramatic_kitten', 'しりとりが\n終わらない'),
        ('50km', 'stare_aloha_gray_cat', '旅行を\nやめる', 'sleep_sleeping_cat', '助手席は\n寝る'),
        ('お盆', 'huh_huh_cat', 'なにそれ？', 'blank_black_cat_zoning_out', '毎年\n同じ渋滞に\nならぶ'),
        ('到着', 'dance_cute_dog', 'おつかれ!', 'sad_banana_cat_cry', 'すぐ\n帰りの渋滞'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}渋滞の長さ", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_94_jutai.mp4"), os.path.join(Wd.HERE, "out", "short_94_jutai_preview"))
