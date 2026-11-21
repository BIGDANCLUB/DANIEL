"""ショート54：日本vs世界 チップを求められたときの反応の差（world_short.py・地震の反応と同じ作り・10/31 ユーザー指定）。59.9秒。

python3 catmeme/short_54_chip.py → out/short_54_chip.mp4
- チップの場面ごとに「だれもいない（札と線だけ）→ 世界の猫＋説明 → 日本の猫＋説明（世界の猫は残る）」の3段（地震と同じ）
- 世界はさらっと払う、日本人は計算でパニック、のずれで笑わせる。どの国もけなさない。最後は「みんなも海外では気をつけよう」
- アメリカのレストランは15〜20%前後がよくある目安（2026年ごろ）。BGM なし
"""
import os

import world_short as Wd
import income_short as I

I.BGS.append(os.path.join(Wd.HERE, "backgrounds", "28_nihon_sekai"))   # ニューヨークのダイナー（日米比較の長尺の背景）
ST = "bg28_ny_diner"
K = 59.9 / 58.5


def cuts():
    out = []
    # (場面, 世界の猫, 世界の説明, 日本の猫, 日本の説明)
    rows = [
        ("チップ10%", "calm_black_face_sheep", "さらっと\n小銭を置く", "think_chin_paw_orange_cat", "10%って\nいくらだっけ"),
        ("チップ15%", "slack_nail_filing_cat", "ふつう", "work_typing_cat", "スマホの電卓を\n出す"),
        ("チップ18%", "talk_orange_white_sitting_cat", "サービスが\nよかったから", "confused_i_dont_know_cat", "18%は\nもう暗算できない"),
        ("チップ20%", "happy_chipi_chapa_cat", "笑顔で\n払う", "sad_looking_away_tabby", "料理より\nチップが気になる"),
        ("チップ25%", "cocky_dj_cat", "最高の夜\nだったから", "stare_tabby_wide_eyes_cat", "ラーメン1杯分が\nチップに消える"),
        ("画面でチップ", "peek_what_happen_cat", "ボタンを\nポンと押す", "scream_phone_orange_cat", "店員さんに\n見られて押せない"),
        ("コーヒー1杯", "eat_chips_cat", "まあ\nいつものこと", "glare_disgusted_cat", "持ち帰りでも\nチップ!?"),
        ("セルフレジ", "walk_white_duck", "スキップする\n人もいる", "despair_dramatic_kitten", "誰に払う\nチップなの…"),
        ("帰国後", "dance_happy_banana_cat", "チップの\nない国も楽しい", "happy_hamster_open_arms", "みんなも\n海外では\n気をつけよう"),
    ]
    for lv, wcat, wcap, jcat, jcap in rows:
        big = lv in ("チップ25%", "画面でチップ", "コーヒー1杯", "セルフレジ")
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}チップへの反応", 96, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_54_chip.mp4"), os.path.join(Wd.HERE, "out", "short_54_chip_preview"))
