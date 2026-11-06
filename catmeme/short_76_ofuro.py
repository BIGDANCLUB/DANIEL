"""ショート76：日本vs世界 お風呂の時間（world_short.py・段階でくらべる型・11/6 ユーザー指定：候補13番）。59.9秒。

python3 catmeme/short_76_ofuro.py → out/short_76_ofuro.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg14_home_night"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('3分', 'stare_interviewer_cat', 'ふつう', 'surprise_big_pupils_cat', 'カラスの\n行水'),
        ('5分', 'work_typing_cat', 'ちょうどいい', 'sad_looking_away_tabby', 'まだ\n頭だけ'),
        ('10分', 'think_chin_paw_orange_cat', '長いかも', 'calm_black_face_sheep', 'シャワーだけは\nさびしい'),
        ('15分', 'glare_disgusted_cat', '水道代が\n心配', 'sleepy_sleepy_cat', '湯船に\nお湯をためる'),
        ('20分', 'call_customer_service_cat', '家族に\n怒られる', 'sleepy_old_memories_cat', '肩まで\nつかる'),
        ('30分', 'peek_what_happen_cat', '大丈夫？', 'read_book_orange_kitten', '湯船で\nスマホ'),
        ('1時間', 'scream_standing_marmot', 'ありえない', 'snore_snoring_dog', '寝落ち'),
        ('2時間', 'fight_cat_fight', '救急車を\n呼ぶ', 'showoff_gojo_cosplay_cat', '入浴剤を\n3つ入れる'),
        ('毎日', 'stare_aloha_gray_cat', 'シャワーで\n十分', 'dance_three_kittens', 'お風呂は\n心の洗濯'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}お風呂の時間", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_76_ofuro.mp4"), os.path.join(Wd.HERE, "out", "short_76_ofuro_preview"))
