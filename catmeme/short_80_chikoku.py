"""ショート80：日本vs世界 遅刻の分数（world_short.py・段階でくらべる型・11/6 ユーザー指定：候補1番（日本vs世界の追加20個から））。59.9秒。

python3 catmeme/short_80_chikoku.py → out/short_80_chikoku.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg25_office_desk"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('1分前', 'sleep_sleeping_cat', 'まだ家', 'work_typing_cat', 'もう\n着いている'),
        ('ちょうど', 'stare_interviewer_cat', '今から出る', 'sad_looking_away_tabby', 'ギリギリで\n反省'),
        ('1分', 'calm_black_face_sheep', '遅刻\nじゃない', 'call_customer_service_cat', '謝罪の\n連絡'),
        ('5分', 'eat_chips_cat', 'コーヒーを\n買ってから', 'despair_dramatic_kitten', '走る'),
        ('10分', 'dance_trending_cat', 'ふつう', 'scream_phone_orange_cat', '上司に\n電話'),
        ('15分', 'smug_squint_bicolor_cat', 'まあまあ', 'realize_wet_cat_stare', '言い訳を\n3つ考える'),
        ('30分', 'think_chin_paw_orange_cat', 'ちょっと\n遅いかな', 'sad_banana_cat_cry', '始末書'),
        ('1時間', 'cocky_dj_cat', 'ランチから\n参加', 'blank_black_cat_zoning_out', 'もう\n行けない'),
        ('電車の遅れ', 'happy_hamster_open_arms', '今日は\nお休み', 'stare_lying_tabby_cat', '遅延証明書を\nもらう'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}遅刻の分数", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_80_chikoku.mp4"), os.path.join(Wd.HERE, "out", "short_80_chikoku_preview"))
