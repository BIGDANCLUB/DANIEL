"""ショート47：日本vs世界 台風が来たときの反応の差（world_short.py・short_25d_jishin「地震の反応」と同じ作り・10/29 ユーザー指定）。59.9秒。

python3 catmeme/short_47_taifu.py → out/short_47_taifu.mp4
- 風速ごとに「だれもいない（札と線だけ）→ 世界の猫＋説明 → 日本の猫＋説明（世界の猫は残る）」の3段（地震と同じ）
- 世界は風が強くなるほど大さわぎ、日本は慣れていて落ち着いて備える、のずれで笑わせる。最後のまとめは入れない
- 被害にあった人のことは書かない。実在のお店・テレビ局の名前は出さない。BGM なし
"""
import os

import world_short as Wd

ST = "bg48_clean_street"
K = 59.9 / 58.5


def cuts():
    out = []
    # (風速, 世界の猫, 世界の説明, 日本の猫, 日本の説明, 日本の小道具)
    rows = [
        ("風速10m", "stare_big_eyes_tabby_kitten", "傘がこわれて\nびっくり", "sleepy_sleepy_cat", "ふつうに\n傘をさす", None),
        ("風速15m", "peek_what_happen_cat", "外出を\nとりやめる", "talk_orange_white_sitting_cat", "「風つよいね」\nで終わり", None),
        ("風速20m", "dance_three_kittens", "学校が\nお休みに", "happy_chipi_chapa_cat", "洗濯物を\n部屋に入れる", None),   # 10/29 ユーザー指定
        ("風速25m", "glare_disgusted_cat", "スーパーが\n空っぽに", "eat_pop_cat", "コンビニで\nカップ麺を買う", None),
        ("風速30m", "dance_filmed_by_gray_cat", "街じゅうが\n大パニック",   # 世界側は踊る猫をスマホで撮る猫（10/30：スターのBGMは流さない）
         "slack_nail_filing_cat", "ベランダの物を\n片づける", None),
        ("風速35m", "stare_tabby_wide_eyes_cat", "国じゅうで\n緊急ニュース", "think_chin_paw_orange_cat", "テレビで\n進路をチェック", "tv"),
        ("風速40m", "fight_cat_fight", "外出\n禁止令", "read_book_orange_kitten", "電車の\n計画運休を確認", None),
        ("風速50m", "surprise_big_pupils_cat", "言葉を\n失う", "call_customer_service_cat", "会社から\n「明日は在宅で」", None),
        ("風速60m", "despair_dramatic_kitten", "「この世の\n終わりだ」", "scream_phone_orange_cat", "SNSで\nスーパー玉手を\n褒め称える", None),   # 10/29 ユーザー指定
    ]
    for lv, wcat, wcap, jcat, jcap, prop in rows:
        big = lv in ("風速35m", "風速40m", "風速50m", "風速60m")
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["rumble_gogogo"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        c = Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K)
        if prop == "tv":   # テレビの前の猫
            c["props"] = [("tv", 200, 1150, 260)]
        out.append(c)
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}台風への反応", 96, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_47_taifu.mp4"), os.path.join(Wd.HERE, "out", "short_47_taifu_preview"))
