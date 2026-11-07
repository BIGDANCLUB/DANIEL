"""ショート79：日本vs世界 家の広さ（world_short.py・段階でくらべる型・11/6 ユーザー指定：候補3番（日本vs世界の追加20個から））。59.9秒。

python3 catmeme/short_79_hirosa.py → out/short_79_hirosa.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
- 11/7 ユーザー指定：15平米「ひとり暮らしはなんとかできる」・20平米「全然いける」・300平米の日本はハムスター「15平米で20人住める！」（世界は別の猫に）
"""
import os

import world_short as Wd

ST = "bg02_room"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('15平米', 'surprise_big_pupils_cat', '物置？', 'happy_chipi_chapa_cat', 'ひとり暮らしは\nなんとか\nできる'),
        ('20平米', 'glare_disgusted_cat', 'せまい', 'joy_happy_happy_happy_cat', '全然いける'),
        ('30平米', 'think_chin_paw_orange_cat', 'ひとり用', 'money_counting_orange_cat', '家賃が\n心配'),
        ('50平米', 'stare_interviewer_cat', 'ふつう', 'happy_girlfriend_dance_cat', '2人で\n住める'),
        ('70平米', 'work_typing_cat', 'ちょっと\nせまい', 'showoff_gojo_cosplay_cat', '家族4人の\n夢の家'),
        ('100平米', 'calm_black_face_sheep', 'ふつうの家', 'scream_phone_orange_cat', '豪邸'),
        ('150平米', 'cocky_dj_cat', '庭は\n別でほしい', 'despair_dramatic_kitten', 'そうじが\n終わらない'),
        ('200平米', 'dance_edm_cat', 'パーティー\nできる', 'blank_black_cat_zoning_out', '家の中で\n迷う'),
        ('300平米', 'rizz_cat_rizz', 'プールも\nほしい', 'happy_hamster_open_arms', '15平米で\n20人住める！'),
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
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}家の広さ", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_79_hirosa.mp4"), os.path.join(Wd.HERE, "out", "short_79_hirosa_preview"))
