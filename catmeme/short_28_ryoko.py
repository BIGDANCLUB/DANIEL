"""ショート28：友人と旅行中 ど深夜に明日仕事だと思い出した結果（world_short.py・10/26 参考「実家帰省中 ど深夜に明日仕事だと
思い出した結果」の作りをまねる）。59.9秒。

python3 catmeme/short_28_ryoko.py → out/short_28_ryoko.mp4
- 10/26 ユーザー指定：「実家帰省中」を「友人と旅行中」に。締め（オチ）も変える
- 作り：最初に黄色い集中線の画面で大きな題名 → 上に黒い帯「明日仕事」。主人公の猫に「イッチ」の札。紫の集中線の画面で
  「ずる休みの理由」。セリフは青か赤の太字＋白い縁（参考どおり）
- 舞台は札幌のホテル（友人4人旅行）。始発の飛行機で帰る → 会社に着いたら今日は創立記念日で休み → 友人から朝の海鮮丼の写真
- 実在の人は出さない。会話は作り話。BGM なし（10/23 ルール）
"""
import os

import world_short as Wd

HOTEL, YELLOW, PURPLE, AIRPORT, PLANE, OFFICE, SEA = ("bg66_hotel_price", "bg120_yellow_rays", "bg121_purple_rays",
                                                      "bg45_airport_arrival", "bg45_airport_arrival", "bg25_office_desk",
                                                      "bg46_sushi_counter")
BLUE_, RED_ = (20, 40, 220), (220, 20, 20)
ME = "イッチ"


def cuts():
    def s(bg, say, cat, dur=2.4, col=BLUE_, me=True, se=None, **kw):
        c = Wd.solo(bg, " ", None, cat, label=ME if me else None, dur=dur, se=se, **kw)
        c.update(say2=(say, col), tag=None)
        return c

    def t(bg, say, left, right, who="R", col=BLUE_, ll="友人", dur=2.4, se=None):
        c = Wd.talk(bg, " ", None, left, right, who=who, llabel=ll, rlabel=ME, dur=dur, se=se)
        c.update(say2=(say, col), tag=None)
        return c

    return [
        dict(s(YELLOW, "友人と旅行中\nど深夜に\n明日仕事だと\n思い出した結果ww", "yell_orange_fat_cat", dur=3.6, col=RED_, me=False,
               se="don_hit"), intro=True),
        s(HOTEL, "ハッ！明日仕事だと\n思い出した", "stare_tabby_wide_eyes_cat", se="question_mark_pop_confused_huh"),
        s(HOTEL, "今 深夜1時\nここは札幌のホテル", "sleepy_old_memories_cat"),
        s(HOTEL, "会社は東京\n始発の飛行機でも\n着くのは朝9時すぎ", "despair_dramatic_kitten"),
        t(HOTEL, "有給使えば\nええやん", "eat_chips_cat", "sad_banana_cat_cry", who="L", col=RED_),
        t(HOTEL, "有給\nもう残ってないんよ…", "eat_chips_cat", "sad_banana_cat_cry", who="R"),
        s(PURPLE, "間に合わん\nずる休みの理由考えろ！", "rizz_cat_rizz", me=False, col=RED_, se="jan"),
        t(PURPLE, "親戚が\n急に倒れたとか？", "talk_orange_white_sitting_cat", "glare_disgusted_cat", who="L", col=RED_),
        t(PURPLE, "それ今年\nもう3回使った", "talk_orange_white_sitting_cat", "glare_disgusted_cat", who="R"),
        t(PURPLE, "じゃあ飛行機が\n欠航したことにしよ", "laugh_laughing_dog", "glare_disgusted_cat", who="L", col=RED_),
        t(PURPLE, "札幌 明日\n快晴なんよ", "laugh_laughing_dog", "blank_black_cat_zoning_out", who="R"),
        t(HOTEL, "始発の便\nまだ空いてるで", "work_dog_staring_computer", "stare_big_eyes_tabby_kitten", who="L", col=RED_,
          se="pikon"),
        t(HOTEL, "これええやん\n昼前には出社できる！", "work_dog_staring_computer", "happy_hamster_open_arms", who="R"),
        s(HOTEL, "上司に「少し遅れます」\nってLINE送っとこ", "call_customer_service_cat"),
        t(HOTEL, "空港までのタクシー\n朝5時に呼んどいたで", "showoff_gojo_cosplay_cat", "dance_tabby_standing_cat", who="L", col=RED_),
        t(HOTEL, "お前ら\n最高かよ…", "showoff_gojo_cosplay_cat", "sad_banana_cat_cry", who="R"),
        s(HOTEL, "朝5時\n友人は全員寝ている", "sleep_sleeping_cat", se="cuckoo_pappo"),
        s(AIRPORT, "なんとか\n始発の便に乗れた", "leave_cat_leaves_home"),
        s(AIRPORT, "羽田から\nそのまま会社へダッシュ", "ride_kitten_bike", se="dash_super_fast"),
        s(OFFICE, "……あれ？\n会社が真っ暗", "peek_what_happen_cat"),
        s(OFFICE, "上司から返信\n「今日は創立記念日で\n休みだよ？」", "stare_interviewer_cat", col=RED_, me=False, se="pinpon_notice"),
        s(OFFICE, "……は？", "huh_huh_cat", dur=2.2, se="question_mark_pop_confused_huh"),
        t(SEA, "朝から海鮮丼\nうまいww", "dance_three_kittens", "despair_dramatic_kitten", who="L", col=RED_, se="pikon"),
        t(SEA, "グッバイ\nイッチww", "laugh_laughing_dog", "despair_dramatic_kitten", who="L", col=RED_, dur=2.6),
    ]


class R28(Wd.Renderer):
    def __init__(self, c, band):
        c["tag"] = c.get("tag") or " "
        super().__init__(c, band)
        say, col = c["say2"]
        big = c.get("intro")
        self.say2 = Wd.rich([[(ln, col)] for ln in say.split("\n")], 140 if big else 80, stroke=10 if big else 7,
                            stroke_col=Wd.WHITE, max_w=Wd.W - 80)

    def frame(self, t):
        c = self.c
        out = self.base.copy()
        for i, q in enumerate(c["cats"]):
            img, al = self.cat_img(i, q, t)
            h, w = al.shape
            x0 = min(max(int(q["x"] - w / 2), 20), Wd.W - w - 20)
            Wd.I.over(out, img, al, x0, int(q["bottom"] - h))
            if self.labels[i] is not None:
                Wd.I.put(out, self.labels[i], min(q["x"] + 150, Wd.W - self.labels[i].width / 2 - 40), q["bottom"] - h * 0.55)
        if c.get("intro"):
            Wd.I.put(out, self.say2, Wd.W / 2, 560)
            return out
        Wd.I.put(out, self.say2, Wd.W / 2, 330 + self.say2.height / 2)
        b = Wd.R.to_np(self.band)
        Wd.I.over(out, b[0], b[1], 0, 0)
        return out


def band():
    return Wd.rich_band([("{y}明日仕事", 150, Wd.BLACK, 120)], 0, 250)


if __name__ == "__main__":
    Wd.I.run(cuts(), None, None, os.path.join(Wd.HERE, "out", "short_28_ryoko.mp4"),
             os.path.join(Wd.HERE, "out", "short_28_ryoko_preview"), band=band(), renderer=R28)
