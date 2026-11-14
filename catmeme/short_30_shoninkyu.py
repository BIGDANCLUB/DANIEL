"""ショート30：新人と2年目の給料のリアル（world_short.py・10/26 参考「社会人1年目と2年目のリアルな違い」の作りをまねる）。59.9秒。

python3 catmeme/short_30_shoninkyu.py → out/short_30_shoninkyu.mp4
- 作りは、いつものショート風（縦型・黒い帯・赤い札・白い字幕・ステッカーの猫・役名の札）。台本だけ参考にする（10/26 ユーザー指定）
- 流れは参考と同じ（1年目より2年目の手取りが少ない：社会保険料と住民税）。そこに「そもそも初任給が上がって、新人の基本給のほうが高い」を
  足す（10/26 ユーザー指定）
- 数字はざっくりの目安（東京・扶養なし・40歳未満）。新人：初任給25万・4月は社会保険料がまだ引かれない（翌月の給料から引く会社が多い）・
  住民税なし → 手取り約24.2万。先輩：基本給23万＋残業代2万・健康保険と厚生年金で約3.5万・住民税は2年目の6月から約1万 → 手取り約19.9万
- 実在の会社・人は出さない。BGM なし（10/23 ルール）
"""
import os

from PIL import Image, ImageDraw

import world_short as Wd

OFF = "bg25_office_desk"
PINK, ORANGE_, NAVY = (230, 60, 140), (240, 130, 0), (20, 40, 160)
BLUE_, RED_ = (20, 40, 200), (220, 20, 20)
BOSS, NEW, SEN = "社長", "新入社員", "先輩（2年目）"


def say1(tag, say, cat, label, **kw):
    return Wd.solo(OFF, tag, say, cat, label=label, tag_style="time", **kw)


def talk(tag, say, left, right, who, ll, rl, **kw):
    return Wd.talk(OFF, tag, say, left, right, who=who, llabel=ll, rlabel=rl, tag_style="time", **kw)


def table(tag, rows, cat, dur=3.4, se=None):
    """給料の内わけ：上に白い表、右下に社長の猫。"""
    lines = []
    for head, items in rows:
        lines.append([(head, Wd.BLACK)])
        lines += [[(k + "  ", Wd.BLACK), (v, col)] for k, v, col in items]
    c = Wd.solo(OFF, tag, None, cat, label=BOSS, tag_style="time", dur=dur, se=se, scale=0.6)
    c["cats"][0].update(x=820, bottom=1560)
    c["tbl"] = lines
    return c


def cuts():
    """10/26 ユーザー指定：いつものショート風（縦型・黒い帯・赤い札・白い字幕・ステッカーの猫）で作り直す。"""
    return [
        talk("4月25日", "新人くん 今日は\nいよいよ初任給だね", "stare_interviewer_cat", "excited_hodomoe_city_cat", "L", BOSS, NEW, se="don_hit"),
        talk("4月25日", "楽しみです！", "talk_orange_white_sitting_cat", "happy_hamster_open_arms", "R", BOSS, NEW, dur=2.0),
        talk("4月25日", "今年から初任給を\n上げたからね！", "cocky_dj_cat", "dance_three_kittens", "L", BOSS, NEW),
        talk("4月25日", "ホイ *25万円*", "money_counting_orange_cat", "surprise_big_pupils_cat", "L", BOSS, NEW, se="price_display"),
        say1("4月25日", "やったー！", "dance_tabby_standing_cat", NEW, dur=2.0, lines=True),
        talk("4月25日", "次 2年目くん", "rizz_cat_rizz", "stare_big_eyes_tabby_kitten", "L", BOSS, SEN, dur=2.0),
        talk("4月25日", "昇給もしたし\n残業も頑張ってたからね", "read_book_orange_kitten", "showoff_gojo_cosplay_cat", "L", BOSS, SEN),
        talk("4月25日", "ホイ *25万円*", "money_counting_orange_cat", "dance_wop_cat", "L", BOSS, SEN, se="price_display"),
        say1("4月25日", "……え？\n新人と同じ？", "huh_huh_cat", SEN, se="question_mark_pop_confused_huh"),
        talk("4月25日", "ちなみに基本給は\n新人のほうが*2万*高いよ", "stare_interviewer_cat", "stare_tabby_wide_eyes_cat", "L", BOSS, SEN),
        talk("4月25日", "は？どゆこと？\n1年がんばったのに", "calmdown_dancing_cat", "rage_talking_cat", "R", BOSS, SEN),
        talk("4月25日", "人手不足で\nどこも*初任給*を上げてるからね", "realize_wet_cat_stare", "glare_disgusted_cat", "L", BOSS, SEN, dur=2.8),
        talk("6月25日", "しかも6月からは\n手取りがもっと差がつく", "talk_orange_white_sitting_cat", "peek_what_happen_cat", "L", BOSS, SEN),
        table("4月の新人", [("新人（4月）", [("基本給", "250,000円", BLUE_), ("雇用保険", "-1,375円", RED_), ("所得税", "-6,500円", RED_),
                                               ("手取り", "約24.2万円", BLUE_)])], "read_book_orange_kitten", se="card_place"),
        table("6月の2年目", [("2年目（6月）", [("基本給+残業", "250,000円", BLUE_), ("健康保険", "-12,300円", RED_),
                                                ("厚生年金", "-22,900円", RED_), ("雇用保険", "-1,375円", RED_), ("所得税", "-4,800円", RED_),
                                                ("住民税", "-10,000円", RED_), ("手取り", "約19.9万円", BLUE_)])],
              "money_counting_orange_cat", dur=4.4, se="card_place"),
        talk("6月25日", "新人は社会保険料が翌月から\n住民税は2年目から", "stare_interviewer_cat", "sad_banana_cat_cry", "L", BOSS, SEN, dur=2.8),
        talk("6月25日", "同じ25万でも\n手取りは*4万*以上ちがう", "cocky_dj_cat", "despair_dramatic_kitten", "R", BOSS, SEN, dur=2.6),
        say1("6月25日", "あんまりだあああ", "sad_black_dog", SEN, dur=2.2, big_say=True),
        talk("6月25日", "新人くんも来年は\n同じ道を通るけどね", "rizz_cat_rizz", "stare_tabby_wide_eyes_cat", "L", BOSS, NEW),
        say1("6月25日", "……え", "huh_huh_cat", NEW, dur=1.8, se="question_mark_pop_confused_huh"),
        talk("6月25日", "2年目の住民税は\n1年目の給料で決まるからね", "talk_orange_white_sitting_cat", "confused_i_dont_know_cat", "L", BOSS, SEN, dur=2.6),
        talk("6月25日", "2年目の6月は\n手取りが下がりやすい", "read_book_orange_kitten", "sulk_hungry_cat", "L", BOSS, SEN, dur=2.4),
        say1("6月25日", "みんなも給料明細\nよく見ておこう！", "happy_hamster_open_arms", BOSS, dur=3.0, se="pinpoon_correct"),
    ]


class R30(Wd.Renderer):
    def __init__(self, c, band_):
        super().__init__(c, band_)
        self.tbl = None
        if c.get("tbl"):
            tx = Wd.rich(c["tbl"], 56, stroke=4, stroke_col=Wd.WHITE, max_w=900, lh=1.3)
            self.tbl = Image.new("RGBA", (tx.width + 60, tx.height + 40), (255, 255, 255, 225))
            self.tbl.alpha_composite(tx, (30, 20))

    def frame(self, t):
        out = super().frame(t)
        if self.tbl is not None:
            Wd.I.put(out, self.tbl, Wd.W / 2 - 60, 700 + self.tbl.height / 2)
        return out


if __name__ == "__main__":
    Wd.I.run(Wd.dedupe(cuts()), None, None, os.path.join(Wd.HERE, "out", "short_30_shoninkyu.mp4"),
             os.path.join(Wd.HERE, "out", "short_30_shoninkyu_preview"),
             band=Wd.rich_band([("{r}新人と2年目", 150, Wd.WHITE, 300), ("{y}給料のリアル", 110, Wd.BLACK, 440)], *Wd.I.BAND), renderer=R30)
