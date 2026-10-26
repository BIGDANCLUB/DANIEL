"""ショート30：新人と2年目の給料のリアル（world_short.py・10/26 参考「社会人1年目と2年目のリアルな違い」の作りをまねる）。59.9秒。

python3 catmeme/short_30_shoninkyu.py → out/short_30_shoninkyu.mp4
- 作り：黒い画面のまん中に横長のオフィスの絵。上に白い四角の題名2行、下に白い四角「これが現実」。社長・新入社員・先輩（2年目）の3匹、
  足もとに色つきの役名。セリフは絵の上のほうに色つきの太字。給料の内わけを表で出す（参考どおり）
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
LB = 640   # 横長の絵の上の位置
PINK, ORANGE_, NAVY = (230, 60, 140), (240, 130, 0), (20, 40, 160)


def band():
    im = Image.new("RGBA", (Wd.W, 330), (0, 0, 0, 255))
    for i, t in enumerate(("新人と2年目の", "給料のリアル")):
        tx = Wd.rich([[(t, Wd.BLACK)]], 96)
        box = Image.new("RGBA", (tx.width + 50, tx.height + 30), (255, 255, 255, 255))
        box.alpha_composite(tx, (25, 15))
        im.alpha_composite(box, ((Wd.W - box.width) // 2, 40 + i * 140))
    return im


def tag_col(t):
    return {"社長": NAVY, "新入社員": PINK, "先輩（2年目）": ORANGE_}[t]


def scene(say, cats, dur=2.5, se=None, col=None, table=None, sound=None):
    """cats = [(素材, 役名, x), ...]。sound = 鳴らす猫の番号。"""
    cs = [dict(a=a, x=x, h=470, w=420, bottom=LB + 600, label=None, mute=(i != sound)) for i, (a, lab, x) in enumerate(cats)]
    c = dict(kind="solo", bg=OFF, tag=None, say=None, cats=cs, dur=dur, fixed=True, no_pop=True, letterbox=LB, foot="これが現実",
             foot_y=1420, band_y=200, labels3=[(lab, x) for a, lab, x in cats])
    if say:
        c["bubbles"] = []
        c["say_col"] = (say, col or NAVY)
    if table:
        c["table"] = table
    if se:
        c["se"] = se
    return c


class R30(Wd.Renderer):
    def __init__(self, c, band_):
        c.setdefault("tag_style", "red")
        tag = c.get("tag")
        c["tag"] = tag or " "
        super().__init__(c, band_)
        self.tag = None
        self.labs = []
        for lab, x in c.get("labels3", []):
            tx = Wd.rich([[(lab, Wd.WHITE)]], 40)
            box = Image.new("RGBA", (tx.width + 24, tx.height + 14), tag_col(lab) + (255,))
            box.alpha_composite(tx, (12, 7))
            self.labs.append((box, x))
        self.sayim = None
        if c.get("say_col"):
            t, col = c["say_col"]
            self.sayim = Wd.rich([[(ln, col)] for ln in t.split("\n")], 56, stroke=6, stroke_col=Wd.WHITE, max_w=1000)
        self.tab = table_img(c["table"]) if c.get("table") else None

    def frame(self, t):
        c = self.c
        out = self.base.copy()
        for i, q in enumerate(c["cats"]):
            img, al = self.cat_img(i, q, t)
            h, w = al.shape
            Wd.I.over(out, img, al, int(q["x"] - w / 2), int(q["bottom"] - h))
        for box, x in self.labs:
            Wd.I.put(out, box, x, LB + 560)
        if self.tab is not None:
            Wd.I.put(out, self.tab, Wd.W / 2, LB + 300)
        if self.sayim is not None:
            Wd.I.put(out, self.sayim, Wd.W / 2, LB + 30 + self.sayim.height / 2)
        b = Wd.R.to_np(self.band)
        Wd.I.over(out, b[0], b[1], 0, 200)
        Wd.I.put(out, self.foot, Wd.W / 2, 1420)
        return out


def table_img(rows):
    """給料の内わけ：[(見出し, [(項目, 金額, 色)])...] を左右にならべる。"""
    cols = []
    for head, items in rows:
        lines = [[(head, Wd.BLACK)]] + [[(f"{k}  {v}", col)] for k, v, col in items]
        cols.append(Wd.rich(lines, 46, stroke=5, stroke_col=Wd.WHITE, max_w=520, lh=1.25))
    w = sum(x.width for x in cols) + 60 * (len(cols) - 1) + 40
    h = max(x.height for x in cols) + 30
    im = Image.new("RGBA", (w, h), (255, 255, 255, 170))
    x = 20
    for col in cols:
        im.alpha_composite(col, (x, 15))
        x += col.width + 60
    return im


def cuts():
    BOSS, NEW, SEN = "社長", "新入社員", "先輩（2年目）"
    trio = lambda b, n, s: [(b, BOSS, 200), (n, NEW, 540), (s, SEN, 880)]
    RED_, BLUE_ = (220, 20, 20), (20, 40, 200)
    return [
        scene("新人くん 今日は\nいよいよ初任給だね", trio("stare_interviewer_cat", "excited_hodomoe_city_cat", "cocky_dj_cat"), sound=2, col=ORANGE_),
        scene("楽しみです！", trio("stare_interviewer_cat", "happy_hamster_open_arms", "cocky_dj_cat"), sound=1, col=PINK, dur=2.0),
        scene("今年から初任給を\n上げたからね！", trio("talk_orange_white_sitting_cat", "happy_hamster_open_arms", "cocky_dj_cat"), sound=0),
        scene("ホイ 25万円", trio("money_counting_orange_cat", "surprise_big_pupils_cat", "cocky_dj_cat"), sound=0, se="price_display"),
        scene("やったー！", trio("money_counting_orange_cat", "dance_tabby_standing_cat", "cocky_dj_cat"), sound=1, col=PINK, dur=2.0),
        scene("次 2年目くん", trio("talk_orange_white_sitting_cat", "dance_tabby_standing_cat", "stare_big_eyes_tabby_kitten"), sound=0, dur=2.0),
        scene("昇給もしたし\n残業も頑張ってたからね", trio("talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten", "showoff_gojo_cosplay_cat"), sound=0),
        scene("給料アップだ！", trio("rizz_cat_rizz", "stare_big_eyes_tabby_kitten", "showoff_gojo_cosplay_cat"), sound=0, se="jan"),
        scene("うぇーい！", trio("rizz_cat_rizz", "stare_big_eyes_tabby_kitten", "dance_wop_cat"), sound=2, col=ORANGE_, dur=2.0),
        scene("ホイ 25万円", trio("money_counting_orange_cat", "stare_big_eyes_tabby_kitten", "dance_wop_cat"), sound=0, se="price_display"),
        scene("……え？\n新人と同じ？", trio("money_counting_orange_cat", "stare_big_eyes_tabby_kitten", "huh_huh_cat"), sound=2, col=ORANGE_,
              se="question_mark_pop_confused_huh"),
        scene("ちなみに基本給は\n新人のほうが2万高いよ", trio("stare_interviewer_cat", "stare_big_eyes_tabby_kitten", "stare_tabby_wide_eyes_cat"), sound=0),
        scene("は？どゆこと？\n1年がんばったのに", trio("stare_interviewer_cat", "stare_big_eyes_tabby_kitten", "rage_talking_cat"), sound=2, col=ORANGE_),
        scene("人手不足で\nどこも初任給を上げてるからね", trio("realize_wet_cat_stare", "stare_big_eyes_tabby_kitten", "rage_talking_cat"), sound=0, dur=2.8),
        scene("しかも手取りは\nもっと差がつくよ", trio("realize_wet_cat_stare", "peek_what_happen_cat", "stare_tabby_wide_eyes_cat"), sound=0),
        scene("説明しよう！", [("read_book_orange_kitten", BOSS, 540)], sound=0, dur=1.8, se="pinpon_notice"),
        scene(None, [("read_book_orange_kitten", BOSS, 900)], sound=None, dur=3.2,
              table=[("新人（4月）", [("基本給", "250,000円", BLUE_), ("雇用保険", "-1,375円", RED_), ("所得税", "-6,500円", RED_),
                                     ("手取り", "約24.2万円", BLUE_)])]),
        scene(None, [("read_book_orange_kitten", BOSS, 900)], sound=None, dur=4.4,
              table=[("新人（4月）", [("基本給", "250,000円", BLUE_), ("雇用保険", "-1,375円", RED_), ("所得税", "-6,500円", RED_),
                                     ("手取り", "約24.2万円", BLUE_)]),
                     ("2年目（6月）", [("基本給+残業", "250,000円", BLUE_), ("健康保険", "-12,300円", RED_), ("厚生年金", "-22,900円", RED_),
                                     ("雇用保険", "-1,375円", RED_), ("所得税", "-4,800円", RED_), ("住民税", "-10,000円", RED_),
                                     ("手取り", "約19.9万円", BLUE_)])], se="card_place"),
        scene("新人は社会保険料が\n翌月から 住民税は2年目から", trio("talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten", "sad_banana_cat_cry"),
              sound=0, dur=2.8),
        scene("同じ25万でも\n手取りは4万以上ちがう", trio("talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten", "sad_banana_cat_cry"), sound=2,
              col=ORANGE_, dur=2.6),
        scene("あんまりだあああ", trio("talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten", "despair_dramatic_kitten"), sound=2,
              col=ORANGE_, dur=2.2),
        scene("新人くんも来年は\n同じ道を通るけどね", trio("rizz_cat_rizz", "stare_tabby_wide_eyes_cat", "despair_dramatic_kitten"), sound=0),
        scene("2年目の住民税は\n1年目の給料で決まるから", trio("talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten", "despair_dramatic_kitten"),
              sound=0, dur=2.4),
        scene("……え", trio("rizz_cat_rizz", "huh_huh_cat", "despair_dramatic_kitten"), sound=1, col=PINK, dur=2.4,
              se="question_mark_pop_confused_huh"),
    ]


if __name__ == "__main__":
    Wd.I.run(cuts(), None, None, os.path.join(Wd.HERE, "out", "short_30_shoninkyu.mp4"),
             os.path.join(Wd.HERE, "out", "short_30_shoninkyu_preview"), band=band(), renderer=R30)
