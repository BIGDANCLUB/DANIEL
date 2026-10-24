"""ショート25d：日本と世界 揺れたときの温度差（world_short.py・10/24 参考「日本vs海外 地震に対する反応の違い」の作りをまねる）。59.9秒。

python3 catmeme/short_25d_jishin.py → out/short_25d_jishin.mp4
- 作り（上に「震度○」の札・左「日本」右「世界」・まん中の黒い線・下に緑の枠の説明）は参考どおり。帯・説明の文は変える
- 震度ごとに「世界の反応 → 日本の反応」の順に出す（参考どおり）
- 実在のテレビ局・番組・人は出さない。被害や亡くなった方は笑いにしない（6強・7はまじめに締める）
- 説明の箱は下のすきま（1540より下）に入れない。BGM なし（10/23 ルール）
"""
import os

import world_short as Wd

ST = "bg48_clean_street"


def cuts():
    out = []
    # (震度, 世界の猫, 世界の説明, 日本の猫, 日本の説明)
    rows = [
        ("震度1", "sleep_sleeping_cat", "だれも\n気づかない", "stare_big_eyes_tabby_kitten", "「今ゆれた？」\nで会話が止まる"),
        ("震度2", "surprise_big_pupils_cat", "みんなが\nびっくりする", "sleepy_sleepy_cat", "「2くらいかな」\nと当てにいく"),
        ("震度3", "confused_i_dont_know_cat", "あわてて\n外へ飛び出す", "eat_chips_cat", "震度当てクイズが\n始まる"),
        ("震度4", "rage_talking_cat", "街じゅうが\n大さわぎ", "think_bike_front_seat_cat", "とりあえず\nテレビをつける"),
        ("震度5弱", "stare_tabby_wide_eyes_cat", "世界のニュースで\n速報になる", "work_dog_staring_computer", "SNSで\n「地震」と検索"),
        ("震度5強", "despair_dramatic_kitten", "街の動きが\n止まる", "punch_tabby_cat_reach", "火を止めて\n家具から離れる"),
        ("震度6弱", "sad_banana_cat_cry", "立って\nいられない", "realize_wet_cat_stare", "すぐ机の下へ\n頭を守る"),
        ("震度6強", "blank_black_cat_zoning_out", "ことばが\n出ない", "stare_interviewer_cat", "おさまるまで\nじっと待つ"),
        ("震度7", "sad_black_dog", "どうしていいか\nわからない", "talk_orange_white_sitting_cat", "すぐ避難！\n命を守る行動を"),
    ]
    for lv, wcat, wcap, jcat, jcap in rows:
        se = ["rumble_gogogo"] if lv in ("震度5強", "震度6弱", "震度6強", "震度7") else ["don_hit"]
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=3.0, se=se))
        out.append(Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.4))
    out.append(Wd.split(ST, "まとめ", left="happy_hamster_open_arms", right="dance_three_kittens",
                        cap="ふだんの備えが\nいちばん大事", cap_side="L", sound="L", dur=2.7, se="pinpoon_correct"))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本と世界", 96, Wd.BLACK, 95), ("{y}揺れたときの温度差", 96, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_25d_jishin.mp4"), os.path.join(Wd.HERE, "out", "short_25d_jishin_preview"))
