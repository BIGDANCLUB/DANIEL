"""ショート25d：日本vs世界 地震のときの反応の差（world_short.py・10/24 参考「日本vs海外 地震に対する反応の違い」を1カットずつまねる）。59.9秒。

python3 catmeme/short_25d_jishin.py → out/short_25d_jishin.mp4
- 10/24 ユーザー指定「口調や素材の使い方をもっと厳密に」：震度ごとに「だれもいない（札と線だけ）→ 世界の猫＋説明 →
  日本の猫＋説明（世界の猫は残る）」の3段。日本の反応は「世界の1つ下の震度の反応」くらい落ち着いている、という作りも参考どおり。
  机・テレビの小道具も参考どおり。最後のまとめは入れない（参考どおり）。文は書きかえる
- 実在のテレビ局・番組・団体の名前は出さない。けが人・亡くなった方のことは書かない（大げさなのは「世界」側の街の様子だけ）
- 説明の箱は下のすきま（1540より下）に入れない。BGM なし（10/23 ルール）
"""
import os

import world_short as Wd

ST = "bg48_clean_street"
K = 59.9 / 58.5


def cuts():
    out = []
    # (震度, 世界の猫, 世界の説明, 日本の猫, 日本の説明, 日本の小道具)
    rows = [
        ("震度1", "talk_orange_white_sitting_cat", "「今ゆれた？」\nとざわつく", "yell_orange_fat_cat", "だれも\n気づかない", None),
        ("震度2", "stare_big_eyes_tabby_kitten", "ほぼ全員が\nびっくり", "meow_ragdoll_chubby_cat", "「今ゆれた？」\nくらい", None),
        ("震度3", "despair_dramatic_kitten", "みんな外へ\n逃げ出す", "glare_disgusted_cat", "ほぼ全員が\n気づく", None),
        ("震度4", "rage_talking_cat", "街じゅうが\n大パニック", "happy_hamster_open_arms", "「おっ、けっこう\nゆれてる」と笑う", None),
        ("震度5弱", "stare_tabby_wide_eyes_cat", "世界中で\n緊急ニュース", "excited_hodomoe_city_cat", "とりあえず\nテレビで速報", "tv"),
        ("震度5強", "surprise_big_pupils_cat", "街の動きが\nぜんぶ止まる", "spit_not_my_taste_cat", "SNSで\n「地震」と検索", None),
        ("震度6弱", "fight_cat_fight", "立て直すのに\n何年もかかる", "sleepy_sleepy_cat", "机の下に\nもぐる", "desk"),
        ("震度6強", "eat_pop_cat", "「この国は\nもうダメだ」", "sleepy_old_memories_cat", "いつものアニメが\n流れてて安心", "tv"),
        ("震度7", "huh_huh_cat", "言葉を\n失う", "sad_banana_cat_cry", "テレビのCMが\n全部お知らせになる", None),
    ]
    for lv, wcat, wcap, jcat, jcap, prop in rows:
        big = lv in ("震度5強", "震度6弱", "震度6強", "震度7")
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["rumble_gogogo"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        c = Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K)
        if prop == "desk":   # 机の下にもぐる猫（机を猫の上にかぶせる）
            c["props"] = [("desk", 275, 820, 470)]
        elif prop == "tv":   # テレビの前の猫
            c["props"] = [("tv", 200, 1150, 260)]
        out.append(c)
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}地震のときの反応の差", 96, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_25d_jishin.mp4"), os.path.join(Wd.HERE, "out", "short_25d_jishin_preview"))
