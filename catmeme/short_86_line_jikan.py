"""ショート86：日本vs世界 上司からのLINEの時間（world_short.py・段階でくらべる型・11/9 ユーザー指定：候補4番）。59.9秒。

python3 catmeme/short_86_line_jikan.py → out/short_86_line_jikan.mp4
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
        ('18時', 'stare_interviewer_cat', '明日\n見る', 'work_typing_cat', 'すぐ返信'),
        ('20時', 'calm_black_face_sheep', '見ない', 'eat_chips_cat', 'ごはん中でも\n返信'),
        ('22時', 'glare_disgusted_cat', 'ありえない', 'scream_phone_orange_cat', 'お風呂で\n返信'),
        ('23時', 'fight_cat_fight', '人事に\n相談', 'think_chin_paw_orange_cat', '既読を\nつけない作戦'),
        ('0時', 'call_customer_service_cat', '弁護士に\n相談', 'sleepy_sleepy_cat', '夢の中で\n返信'),
        ('2時', 'scream_standing_marmot', '警察を\n呼ぶ', 'stare_lying_tabby_cat', '寝たふり'),
        ('休日', 'dance_edm_cat', '通知オフ', 'despair_dramatic_kitten', 'スタンプ\nだけ返す'),
        ('有給中', 'happy_hamster_open_arms', '電話も\n出ない', 'sad_looking_away_tabby', '旅行先で\n資料を作る'),
        ('退職後', 'dance_happy_banana_cat', 'ブロック', 'blank_black_cat_zoning_out', 'まだ\n通知が来る'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}上司からのLINEの時間", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_86_line_jikan.mp4"), os.path.join(Wd.HERE, "out", "short_86_line_jikan_preview"))
