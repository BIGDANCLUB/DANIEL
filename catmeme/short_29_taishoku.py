"""ショート29：退職日は要注意 月末と前日で手取りが変わる（world_short.py・10/26 参考「4〜6月は残業禁止 特に最後の点は要注意」の作りをまねる）。59.9秒。

python3 catmeme/short_29_taishoku.py → out/short_29_taishoku.mp4
- 作り：オフィスの絵いっぱい。上に赤い四角の白い題名2行。社長と正社員の2匹（足もとに白い四角の役名、正社員は青い字）。
  セリフは白い縁の黒い字、正社員の心の声は緑の字。表で数字を見せる。後半に「社保」の犬が出てくる。最後に登録ボタン（参考どおり）
- 台本は変える（10/26 ユーザー指定）。話題：退職日を月末にするか前日にするかで社会保険料が変わる
- 事実：社会保険の資格をなくす日は「退職日の次の日」。保険料はその日がある月の前の月の分まで。
  10/31 退職 → 11/1 に資格をなくす → 10月分の保険料がかかる。10/30 退職 → 10/31 に資格をなくす → 10月分はかからない。
  ただし10/30退職だと、10月分は国民健康保険と国民年金に入って自分で払う（会社の半分負担もなくなる）。
  保険料を前の月の分として次の月の給料から引く会社では、月末退職の最後の給料で2か月分引かれることがある
- 数字は月給25万のざっくりの目安。実在の会社・人は出さない。BGM なし（10/23 ルール）
"""
import os

from PIL import Image

import world_short as Wd

OFF = "bg25_office_desk"
BLACK_, GREEN_, BLUE_, RED_ = (20, 20, 20), (40, 200, 40), (20, 40, 220), (220, 20, 20)


def band():
    im = Image.new("RGBA", (Wd.W, 220), (0, 0, 0, 0))
    box = Image.new("RGBA", (980, 200), (220, 20, 20, 255))
    for i, t in enumerate(("退職日は月末か前日か", "特に最後の点は要注意")):
        tx = Wd.rich([[(t, Wd.WHITE)]], 74, stroke=4, stroke_col=(120, 0, 0), max_w=940)
        box.alpha_composite(tx, ((box.width - tx.width) // 2, 14 + i * 92))
    im.alpha_composite(box, ((Wd.W - box.width) // 2, 10))
    return im


def sc(say, left, right, ll="社長", rl="正社員", who=None, col=BLACK_, think=None, table=None, dur=2.5, se=None, subscribe=False):
    cats = []
    if left:
        cats.append(dict(a=left, x=300, h=780, w=560, bottom=1440, label=ll, mute=who != "L"))
    if right:
        cats.append(dict(a=right, x=780, h=780, w=560, bottom=1440, label=rl, mute=who != "R"))
    c = dict(kind="solo", bg=OFF, tag=" ", say=None, cats=cats, dur=dur, fixed=True, no_pop=True, say3=(say, col), think=think,
             table=table, subscribe=subscribe)
    if se:
        c["se"] = se
    return c


def table_img(rows):
    lines = [[(a, BLACK_), ("  " + b, col)] for a, b, col in rows]
    tx = Wd.rich(lines, 50, stroke=4, stroke_col=Wd.WHITE, max_w=960, lh=1.3)
    im = Image.new("RGBA", (tx.width + 60, tx.height + 40), (255, 255, 255, 215))
    im.alpha_composite(tx, (30, 20))
    return im


def role_img(t):
    col = {"社長": BLACK_, "正社員": BLUE_, "社保": (255, 140, 0)}[t]
    tx = Wd.rich([[(t, col)]], 70, stroke=5, stroke_col=Wd.WHITE)
    im = Image.new("RGBA", (tx.width + 30, tx.height + 16), (255, 255, 255, 230))
    im.alpha_composite(tx, (15, 8))
    return im


class R29(Wd.Renderer):
    def __init__(self, c, band_):
        super().__init__(c, band_)
        say, col = c["say3"]
        self.s3 = Wd.rich([[(ln, col)] for ln in say.split("\n")], 74, stroke=7, stroke_col=Wd.WHITE, max_w=1000) if say else None
        self.th = Wd.rich([[(ln, GREEN_)] for ln in c["think"].split("\n")], 64, stroke=6, stroke_col=(0, 60, 0), max_w=600) \
            if c.get("think") else None
        self.tb = table_img(c["table"]) if c.get("table") else None
        self.roles = [role_img(q["label"]) for q in c["cats"]]

    def frame(self, t):
        c = self.c
        out = self.base.copy()
        for i, q in enumerate(c["cats"]):
            img, al = self.cat_img(i, q, t)
            h, w = al.shape
            Wd.I.over(out, img, al, min(max(int(q["x"] - w / 2), 20), Wd.W - w - 20), int(q["bottom"] - h))
            Wd.I.put(out, self.roles[i], q["x"], 1470)
        if self.tb is not None:
            Wd.I.put(out, self.tb, Wd.W / 2, 330 + self.tb.height / 2)
        if self.s3 is not None:
            y = 330 + (self.tb.height + 20 if self.tb is not None else 0)
            Wd.I.put(out, self.s3, Wd.W / 2, y + self.s3.height / 2)
        if self.th is not None:
            Wd.I.put(out, self.th, 760, 1200)
        b = Wd.R.to_np(self.band)
        Wd.I.over(out, b[0], b[1], 0, 90)
        if self.subs is not None:
            Wd.I.put(out, self.subs[1 if t > 1.3 else 0], Wd.W / 2, 1300)
        return out


def cuts():
    return [
        sc("今月末で辞めます！\n最後の給料も楽しみ！", "cocky_dj_cat", "dance_tabby_standing_cat", who="R", col=BLUE_, se="don_hit"),
        sc("は？", "huh_huh_cat", "dance_tabby_standing_cat", who="L", dur=1.6, se="question_mark_pop_confused_huh"),
        sc("月末に辞めると\n最後の手取り減るけど", "talk_orange_white_sitting_cat", "dance_tabby_standing_cat", who="L",
           think="何言ってんの？"),
        sc("社会保険料は\n辞めた日の「次の日」で決まる", "talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten", who="L"),
        sc(None, "read_book_orange_kitten", "stare_big_eyes_tabby_kitten", dur=3.6, se="card_place",
           table=[("10月31日に退職", "→ 10月分 かかる", RED_), ("10月30日に退職", "→ 10月分 かからない", BLUE_)]),
        sc("1日ちがうだけで？", "read_book_orange_kitten", "stare_tabby_wide_eyes_cat", who="R", col=BLUE_, dur=2.2),
        sc("辞めた日の次の日に\n社会保険の資格がなくなる", "talk_orange_white_sitting_cat", "stare_tabby_wide_eyes_cat", who="L", dur=2.6),
        sc("保険料は\nその前の月の分まで", "talk_orange_white_sitting_cat", "stare_tabby_wide_eyes_cat", who="L", dur=2.4),
        sc("だから31日に辞めると\n10月分も引かれる", "stare_interviewer_cat", "sad_black_dog", who="L", dur=2.6, think="まじで嫌い"),
        sc("会社によっては最後の給料で\n2か月分まとめて引かれる", "rizz_cat_rizz", "stare_tabby_wide_eyes_cat", who="L", dur=2.8),
        sc(None, "rizz_cat_rizz", "sad_banana_cat_cry", dur=3.4, se="card_place",
           table=[("健康保険", "-12,300円 × 2", RED_), ("厚生年金", "-22,900円 × 2", RED_), ("合計", "約-7万円", RED_)]),
        sc("最後の給料が\nほとんど消える…", "rizz_cat_rizz", "sad_banana_cat_cry", who="R", col=BLUE_, dur=2.2),
        sc("じゃあ30日に\n辞めます！", "rizz_cat_rizz", "showoff_gojo_cosplay_cat", who="R", col=BLUE_, think="勝った", dur=2.4),
        sc("わかるよな？ww", "rizz_cat_rizz", "showoff_gojo_cosplay_cat", who="L", dur=2.2, think="ま、まさかこいつ"),
        sc("ちょっと待った", "laugh_laughing_dog", "showoff_gojo_cosplay_cat", ll="社保", who="L", col=(255, 120, 0), dur=2.0,
           se="jan"),
        sc("10月分は国民健康保険と\n国民年金を自分で払ってね", "laugh_laughing_dog", "stare_tabby_wide_eyes_cat", ll="社保", who="L", dur=2.8,
           think="なにこいつ"),
        sc("会社が半分出してた分も\n全部自分で払うよww", "laugh_laughing_dog", "stare_tabby_wide_eyes_cat", ll="社保", who="L", dur=2.6),
        sc("結局払うの！？", "laugh_laughing_dog", "despair_dramatic_kitten", ll="社保", who="R", col=BLUE_, dur=2.2,
           se="question_mark_pop_confused_huh"),
        sc("次の会社に11月1日入社なら\n月末退職のほうがおトクなことが多い", "talk_orange_white_sitting_cat", "despair_dramatic_kitten", who="L",
           dur=3.0),
        sc("言うの遅くね？", "talk_orange_white_sitting_cat", "glare_disgusted_cat", who="R", col=GREEN_, dur=2.4, subscribe=True),
        sc("なんでいつも\nちゃんと説明しないんだよ", "talk_orange_white_sitting_cat", "rage_talking_cat", who="R", col=GREEN_, dur=2.4),
        sc("聞いてこないしww", "laugh_laughing_dog", "rage_talking_cat", ll="社保", who="L", dur=2.2),
        sc("そもそも辞める日なんて\n選べる空気じゃない", None, "sleepy_old_memories_cat", who="R", col=GREEN_, dur=3.0),
    ]


if __name__ == "__main__":
    Wd.I.run(cuts(), None, None, os.path.join(Wd.HERE, "out", "short_29_taishoku.mp4"),
             os.path.join(Wd.HERE, "out", "short_29_taishoku_preview"), band=band(), renderer=R29)
