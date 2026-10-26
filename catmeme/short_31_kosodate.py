"""ショート31：日本と海外 子育て支援の差（world_short.py・10/26 参考「日本vs海外 子育てするならどの国？」の話題を、
地震比較（short_25d_jishin）と同じ左右くらべの構図で作る（10/26 ユーザー指定））。59.9秒。

python3 catmeme/short_31_kosodate.py → out/short_31_kosodate.mp4
- 作り：上に黒い帯2行、話題ごとに白地オレンジ枠の札、左「日本」右「海外」、まん中の黒い線、下に緑の枠の説明。
  話題ごとに「だれもいない（札と線だけ）→ 海外の猫＋説明 → 日本の猫＋説明（海外の猫は残る）」の3段（地震比較どおり）
- 帯・文は参考と変える。日本が強いところ（3〜5歳の保育料無料・子どもの医療費助成）も入れて、どちらかをけなさない
- 数字は2026年時点のざっくりの目安（概要欄に書く）：
  出産 日本 出産育児一時金50万円／スウェーデン 公的医療でほぼ無料。育休 日本 原則1歳まで（最長2歳）・男性の取得率 約4割（2024年度）／
  スウェーデン 両親で480日・父親の約9割が取得。児童手当 日本 月1万〜1.5万円（第3子から3万円）高校生まで／ドイツ 月255ユーロ（約4万円）。
  保育料 日本 3〜5歳は無料／フランス 収入に応じて負担。子どもの医療費 日本 自治体の助成で高校生まで無料のところも／スウェーデン 18歳未満はほぼ無料。
  大学 日本 国立で年約54万円／ドイツ 州立は授業料ほぼ無料。誕生時の給付 日本 妊婦支援給付金 計10万円／シンガポール ベビーボーナス 最大約1.1万シンガポールドル（約120万円）
- BGM なし（10/23 ルール）
"""
import os

import world_short as Wd

BG = "bg19_kids_room"
K = 59.9 / 59.9


def cuts():
    out = []
    # (話題, 海外の猫, 海外の説明, 日本の猫, 日本の説明)
    rows = [
        ("出産費用", "happy_hamster_open_arms", "スウェーデン\nほぼ無料", "money_counting_orange_cat", "一時金50万円\n足りない地域も"),
        ("育休", "dance_three_kittens", "スウェーデン\n夫婦で480日", "talk_orange_white_sitting_cat", "原則1歳まで\n延長で2歳まで"),
        ("パパの育休", "dance_orange_gray_cats", "スウェーデン\nパパの9割が取る", "confused_i_dont_know_cat", "パパの取得は\n約4割"),
        ("児童手当", "happy_girlfriend_dance_cat", "ドイツ\n月約4万円", "sulk_hungry_cat", "月1万〜1.5万円\n高校生まで"),
        ("保育料", "think_bike_front_seat_cat", "フランス\n収入に応じて負担", "dance_tabby_standing_cat", "3〜5歳は\n無料！"),
        ("子どもの医療費", "realize_wet_cat_stare", "スウェーデン\n18歳までほぼ無料", "showoff_gojo_cosplay_cat", "高校生まで\n無料の自治体も"),
        ("大学の学費", "dance_wop_cat", "ドイツ\n授業料ほぼ無料", "despair_dramatic_kitten", "国立でも\n年約54万円"),
        ("生まれた時のお祝い", "yell_orange_fat_cat", "シンガポール\n約120万円", "sad_banana_cat_cry", "妊婦支援給付\n計10万円"),
    ]
    for topic, wcat, wcap, jcat, jcap in rows:
        out.append(Wd.split(BG, topic, dur=1.0 * K, se=["pi"]))
        out.append(Wd.split(BG, topic, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.4 * K, se="don_hit"))
        out.append(Wd.split(BG, topic, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.2 * K))
    out.append(Wd.split(BG, "まとめ", left="realize_wet_cat_stare", right="stare_interviewer_cat",
                        cap="国ごとに\n強みがちがう", cap_side="L", sound="L", dur=3.0, se="pinpoon_correct"))
    out.append(Wd.split(BG, "まとめ", left="happy_hamster_open_arms", right="dance_three_kittens",
                        cap="制度を知って\nしっかり使おう", cap_side="L", sound="L", dur=3.0))
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=("日本", "海外"))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{r}日本{w}と{c}海外", 110, Wd.BLACK, 95), ("{y}子育て支援の差", 110, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_31_kosodate.mp4"), os.path.join(Wd.HERE, "out", "short_31_kosodate_preview"))
