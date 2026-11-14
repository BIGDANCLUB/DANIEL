"""ショート43：日本vs世界 会社を辞めると伝えたら（world_short.py・残業の動画 short_37 と同じ作り）。59.9秒。
目安：日本 民法では2週間前に伝えれば辞められる（就業規則は1〜2か月前が多い）・退職代行もある。
ドイツ 法律で決まった予告期間（はじめは4週間など）、最後は有給を消化して辞めることが多い。アメリカ 多くの州で「いつでも辞められる・辞めさせられる」、2週間前に伝えるのがマナー。"""
import os

import world_short as Wd

JP_OFF, DE_OFF, US_OFF = "bg25_office_desk", "bg78_agency_office", "bg119_us_office"
ME = "laugh_laughing_dog"


def cuts():
    def s(bg, say, cat, **kw):
        kw.setdefault("se", "don_hit")
        return Wd.solo(bg, kw.pop("tag"), say, cat, dur=kw.pop("d", 2.2), label="私", lines=True, **kw)

    def t(bg, say, left, right, ll, rl, **kw):
        return Wd.talk(bg, kw.pop("tag"), say, left, right, dur=kw.pop("d", 2.6), llabel=ll, rlabel=rl, **kw)

    j = dict(tag="日本")
    g = dict(tag="ドイツ", tag_style="yellow")
    u = dict(tag="アメリカ", tag_style="orange")
    return [
        s(JP_OFF, "会社を\n*辞めます*！", ME, **j),
        t(JP_OFF, "え……\nちょっと*会議室*いい？", "stare_interviewer_cat", "stare_tabby_wide_eyes_cat", "上司", "私", who="L", **j),
        t(JP_OFF, "*後任*が見つかるまで\n待ってくれない？", "rage_talking_cat", "sulk_hungry_cat", "上司", "私", who="L", **j),
        t(JP_OFF, "いま辞めたら\n*みんなが困る*よ", "meow_ragdoll_chubby_cat", "sad_banana_cat_cry", "お局", "私", who="L", **j),
        t(JP_OFF, "*送別会*の幹事\nだれがやる？", "talk_orange_white_sitting_cat", "blank_black_cat_zoning_out", "同僚", "私", who="L", **j),
        t(JP_OFF, "結局\n*3か月*引きとめられた…", "talk_orange_white_sitting_cat", "despair_dramatic_kitten", "同僚", "私", who="R", **j),
        s(DE_OFF, "会社を\n*辞めます*！", ME, **g),
        t(DE_OFF, "わかった\n*予告期間*は守ってね", "calmdown_dancing_cat", "stare_big_eyes_tabby_kitten", "上司", "私", who="L", **g),
        t(DE_OFF, "残ってる*有給*も\nぜんぶ使ってから辞めてね", "happy_hamster_open_arms", "surprise_big_pupils_cat", "上司", "私", who="L", **g),
        t(DE_OFF, "最後の1か月\nほぼ*休み*だった", "dance_orange_gray_cats", "dance_tabby_standing_cat", "同僚", "私", who="R", **g),
        t(DE_OFF, "次の会社でも\nがんばれよ！", "dance_three_kittens", "happy_girlfriend_dance_cat", "同僚", "私", who="L", **g),
        s(US_OFF, "会社を\n*辞めます*！", ME, **u),
        t(US_OFF, "OK！\n*2週間後*ね", "cocky_dj_cat", "huh_huh_cat", "上司", "私", who="L", **u),
        t(US_OFF, "引きとめないの！？", "cocky_dj_cat", "stare_tabby_wide_eyes_cat", "上司", "私", who="R", **u),
        t(US_OFF, "*もっといい条件*が\nあったんでしょ？", "rizz_cat_rizz", "realize_wet_cat_stare", "上司", "私", who="L", **u),
        t(US_OFF, "ちなみに会社も\n*いつでも*クビにできるよ", "angry_aiming_cat", "despair_dramatic_kitten", "同僚", "私", who="L", **u),
        s(JP_OFF, "辞め方も\n国によって*全然ちがう*", "realize_wet_cat_stare", d=2.6, **j),
        s(JP_OFF, "みんなも\n辞めるときは*ルール*を\n確認しておこう", "happy_hamster_open_arms", d=3.0, se="pinpoon_correct", **j),
    ]


def fit(cs):
    k = 59.9 / sum(c["dur"] for c in cs)
    for c in cs:
        c["dur"] *= k
    return cs


if __name__ == "__main__":
    Wd.run(fit(cuts()), Wd.band_vs("{r}日本{w}vs{c}世界", "{y}会社を{g}辞める{y}と伝えたら"),
           os.path.join(Wd.HERE, "out", "short_43_yameru.mp4"), os.path.join(Wd.HERE, "out", "short_43_yameru_preview"))
