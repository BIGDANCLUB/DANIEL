"""ショート45：日本vs世界 電車が遅れたときの反応の差（world_short.py・short_25d_jishin「地震の反応」と同じ作り・10/29 ユーザー指定）。59.9秒。

python3 catmeme/short_45_densha.py → out/short_45_densha.mp4
- 遅れの時間ごとに「だれもいない（札と線だけ）→ 世界の猫＋説明 → 日本の猫＋説明（世界の猫は残る）」の3段（地震と同じ）
- 地震とは逆に、世界はのんびり・日本はたった1分でも大さわぎ、のずれで笑わせる。最後のまとめは入れない
- 実在の鉄道会社・路線の名前は出さない。BGM なし
"""
import os

import world_short as Wd

ST = "bg54_station_crowd_map"
K = 59.9 / 58.5


def cuts():
    out = []
    # (遅れ, 世界の猫, 世界の説明, 日本の猫, 日本の説明, 日本の小道具)
    rows = [
        ("1分", "peek_what_happen_cat", "遅れた？\nだれも気づかない", "call_customer_service_cat", "おわびの放送が\n流れる", None),
        ("3分", "calm_black_face_sheep", "時間どおりの\nうちに入る", "sad_looking_away_tabby", "駅員さんが\n何度も頭を下げる", None),
        ("5分", "slack_nail_filing_cat", "今日は\n早いほう", "stare_tabby_wide_eyes_cat", "遅延証明書を\nもらう列ができる", None),
        ("10分", "eat_chips_cat", "のんびり\nおやつタイム", "scream_phone_orange_cat", "会社に\n「遅れます」と連絡", None),
        ("15分", "walk_white_duck", "ホームを\nお散歩", "work_typing_cat", "SNSで\n「電車 遅延」と検索", None),
        ("30分", "stare_lying_tabby_cat", "ホームで\nごろ寝", "despair_dramatic_kitten", "振替輸送の\n案内に大行列", None),
        ("1時間", "dance_happy_banana_cat", "電車が来たら\nラッキー", "stare_big_eyes_tabby_kitten", "テレビで\nニュースになる", "tv"),
        ("2時間", "sleep_sleeping_cat", "家に帰って\nまた明日", "sulk_hungry_cat", "タクシー乗り場に\n長い行列", None),
        ("半日", "dance_three_kittens", "そのまま\nお休みにする", "sad_banana_cat_cry", "それでも\n歩いて会社へ", None),
    ]
    for lv, wcat, wcap, jcat, jcap, prop in rows:
        big = lv in ("30分", "1時間", "2時間", "半日")
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["chime_announce"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        c = Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K)
        if prop == "tv":   # テレビの前の猫
            c["props"] = [("tv", 200, 1150, 260)]
        out.append(c)
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}電車が遅れたときの反応", 96, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_45_densha.mp4"), os.path.join(Wd.HERE, "out", "short_45_densha_preview"))
