"""ショート26：給料日の前と後（world_short.py・10/26 参考「給料日の感じ方 みんなも同じ？」の作りをまねる）。59.9秒。

python3 catmeme/short_26_kyuryobi.py → out/short_26_kyuryobi.mp4
- 作り（上の黒い帯2行・赤い札「3日前」など・白い太字のセリフ・ステッカーふうの猫・スマホを持つ手・考えごとの雲・集中線）は参考どおり
- 展開と台本は変える（10/26 ユーザー指定）：参考は「残業→明細が5万多い→浮かれて使う→翌日カード引き落とし」。
  こちらは「もやし生活→0時に残高確認→明細で住民税と社会保険料にがっかり→それでも浮かれる→家賃・スマホ代・サブスク引き落とし→
  あと23日」の流れ。札は「○日前／○日後」でそろえる（10/26 ユーザー指定）
- 実在の人は出さない。会話は作り話。「にゃ」なし。BGM なし（10/23 ルール）
"""
import os

import income_short as I
import world_short as Wd

ROOM, CONBINI, OFFICE, NIGHT, TRAIN, YAKI, ROOM_M = ("bg02_room", "bg15_convenience", "bg25_office_desk", "bg14_home_night",
                                                    "bg53_shinkansen", "bg22_yakiniku", "bg02_room")


def cuts():
    s, t = Wd.solo, Wd.talk

    def tm(x):
        return dict(tag=x, tag_style="time")

    def ph(label, x=330, y=1200, w=230):
        return [("phone:" + label, x, y, w)]

    return [
        # ---- 給料日前 ----
        s(ROOM, say="今月も\nもやし生活", cat="scream_standing_marmot", dur=2.3, se="don_hit", **tm("5日前")),
        s(CONBINI, say="財布の中\n小銭しかない", cat="scream_standing_marmot", dur=2.0, **tm("3日前")),
        s(OFFICE, say="お昼は\nカップ麺", cat="scream_standing_marmot", dur=2.0, **tm("1日前")),
        s(NIGHT, say="もう寝る時間なのに\n目がさえてる", cat="think_bike_front_seat_cat", dur=2.4, **tm("1日前 23:50")),
        s(NIGHT, say="あと3分で\n日付が変わる…", cat="sleepy_old_memories_cat", dur=2.4, **tm("1日前 23:57")),
        dict(s(NIGHT, say="振りこまれてる！！", cat="dance_tabby_standing_cat", dur=2.4, lines=True, se="pinpoon_correct",
               **tm("給料日 0:00")), props=ph("残高\n増えた", 300, 1200)),
        # ---- 明細を見る ----
        dict(s(OFFICE, say="明細も\n見てみよう", cat="meow_ragdoll_chubby_cat", dur=2.2, **tm("給料日")), props=ph("給料明細", 300, 1200)),
        dict(s(OFFICE, say="……あれ？\n去年より少ない？", cat="stare_tabby_wide_eyes_cat", dur=2.6, **tm("給料日")),
             props=ph("給料明細", 300, 1200)),
        dict(s(OFFICE, say=None, cat="huh_huh_cat", dur=2.6, se="question_mark_pop_confused_huh", **tm("給料日"),
               bubbles=[("住民税", 300, 740, 0.0), ("社会保険料", 300, 880, 0.5)]), props=ph("給料明細", 820, 1100, 200)),
        dict(s(OFFICE, say="知らないうちに\nじわじわ上がってる…", cat="sad_banana_cat_cry", dur=2.6, **tm("給料日")),
             props=ph("給料明細", 300, 1200)),
        t(OFFICE, say="給料日だし\n今日くらい飲み行く？", left="happy_girlfriend_dance_cat", right="realize_wet_cat_stare", who="L",
          llabel="同僚", dur=2.6, **tm("給料日")),
        t(OFFICE, say="行く！！\nもう細かいことはいい！", left="happy_girlfriend_dance_cat", right="yell_orange_fat_cat", who="R",
          llabel="同僚", dur=2.4, **tm("給料日")),
        # ---- 浮かれる ----
        dict(s(TRAIN, say="手取りは減ったけど\n何に使おうかな", cat="laugh_laughing_dog", dur=2.4, **tm("給料日")),
             props=[("cloud:新しい\nスニーカー@R", 300, 1000, 480)], cat_x=790),
        dict(s(TRAIN, say="あとは\n焼肉と…", cat="eat_pop_cat", dur=2.2, **tm("給料日")), props=[("cloud:焼肉\n温泉旅行@R", 300, 1000, 480)], cat_x=790),
        s(TRAIN, say="考えてる時がいちばん\nお金持ちなんだよなww", cat="yell_orange_fat_cat", dur=2.6, **tm("給料日")),
        dict(s(YAKI, say="上カルビ\nもう1皿！！", cat="happy_chipi_chapa_cat", dur=2.4, lines=True, se="jan", **tm("1日後"))),
        s(YAKI, say="会計は\nカードで！", cat="showoff_gojo_cosplay_cat", dur=2.2, **tm("1日後")),
        s(YAKI, say="今だけは\nお金持ち！", cat="happy_hamster_open_arms", dur=2.2, **tm("2日後")),
        s(ROOM, say="コンビニで\n高いアイスも買っちゃう", cat="eat_pop_cat", dur=2.4, **tm("3日後")),
        dict(s(ROOM, say="スニーカーと\nゲームもポチった！", cat="dance_wop_cat", dur=2.4, **tm("3日後")), props=ph("注文確定", 300, 1200)),
        # ---- 引き落とし ----
        dict(s(ROOM, say="家賃\n引き落とし", cat="scream_standing_marmot", dur=2.2, se="pi", **tm("4日後"))),
        dict(s(ROOM, say="スマホ代と\n電気代も", cat="scream_standing_marmot", dur=2.0, **tm("5日後"))),
        dict(s(ROOM, say="サブスク4つ\n全部引き落とし", cat="scream_standing_marmot", dur=2.2, **tm("6日後"))),
        dict(s(ROOM_M, say="……え\nなんで", cat="surprise_big_pupils_cat", dur=2.4, se="question_mark_pop_confused_huh", **tm("7日後")),
             props=ph("残高\n3万", 300, 1200)),
        dict(s(ROOM_M, say="給料日から\nまだ1週間なのに", cat="despair_dramatic_kitten", dur=2.6, **tm("7日後")), props=ph("残高\n3万", 300, 1200)),
        dict(s(ROOM_M, say="次の給料日まで\nあと23日…", cat="sad_black_dog", dur=2.8, se="chin_bell_failure_sad_ending", **tm("7日後"))),
        s(CONBINI, say="今月も\nもやし生活", cat="scream_standing_marmot", dur=2.6, **tm("8日後")),
        s(CONBINI, say="みんなも給料日は\n使いすぎに気をつけよう", cat="realize_wet_cat_stare", dur=2.6, **tm("8日後")),
    ]


def fix(cs):
    for c in cs:   # マーモットは1回叫び終わったら次の場面へ（10/26 ユーザー指定）
        if any(q["a"] == "scream_standing_marmot" for q in c["cats"]):
            c["dur"] = 1.3
    for c in cs:   # 雲の場面は猫を右に（雲・字幕とかさならない）
        if c.get("cat_x"):
            c["cats"][0]["x"], c["cats"][0]["h"], c["cats"][0]["w"] = c["cat_x"], 680, 520
    return cs


if __name__ == "__main__":
    Wd.run(fix(cuts()), Wd.rich_band([("{r}給料日の前と後", 150, Wd.WHITE, 300), ("{y}これ自分だけ？", 104, Wd.BLACK, 440)], *I.BAND),
           os.path.join(Wd.HERE, "out", "short_26_kyuryobi.mp4"), os.path.join(Wd.HERE, "out", "short_26_kyuryobi_preview"))
