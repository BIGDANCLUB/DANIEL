"""ショート44：日本vs世界 お昼休みの過ごし方（world_short.py・残業の動画 short_37 と同じ作り）。59.9秒。
目安：日本 1時間（デスクでコンビニ弁当・昼寝も）。スペイン 昼食がいちばん大事な食事・2時間ほどの長い休みの会社も。
アメリカ デスクで食べながら仕事・サンドイッチやサラダで短く。"""
import os

import world_short as Wd

JP, ES, US, CAFE = "bg25_office_desk", "bg46_sushi_counter", "bg119_us_office", "bg100_lounge_night"
ME = "laugh_laughing_dog"


def cuts():
    def s(bg, say, cat, **kw):
        kw.setdefault("se", "don_hit")
        return Wd.solo(bg, kw.pop("tag"), say, cat, dur=kw.pop("d", 2.2), label="私", lines=True, **kw)

    def t(bg, say, left, right, ll, rl, **kw):
        return Wd.talk(bg, kw.pop("tag"), say, left, right, dur=kw.pop("d", 2.6), llabel=ll, rlabel=rl, **kw)

    j = dict(tag="日本")
    e = dict(tag="スペイン", tag_style="yellow")
    u = dict(tag="アメリカ", tag_style="orange")
    return [
        s(JP, "*お昼休み*だ！", ME, **j),
        t(JP, "コンビニ\n*混んでる*から急ごう", "talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten", "同僚", "私", who="L", **j),
        t(JP, "デスクで\nおにぎりと*カップ麺*", "eat_pop_cat", "eat_crunchy_cat_luna", "同僚", "私", who="R", **j),
        t(JP, "食べながら\nメールの返事…", "work_typing_cat", "eat_crunchy_cat_luna", "同僚", "私", who="R", **j),
        t(JP, "残り15分は\n*机でつっぷして昼寝*", "sleep_sleeping_cat", "sleepy_sleepy_cat", "同僚", "私", who="R", **j),
        t(JP, "昼休みなのに\n*電話*鳴ってるよ", "call_customer_service_cat", "despair_dramatic_kitten", "同僚", "私", who="L", **j),
        s(ES, "*お昼休み*だ！", ME, **e),
        t(ES, "お昼は\n*1日のメイン*の食事！", "happy_hamster_open_arms", "surprise_big_pupils_cat", "同僚", "私", who="L", **e),
        t(ES, "前菜・メイン・デザート\nゆっくり*2時間*", "dance_orange_gray_cats", "stare_tabby_wide_eyes_cat", "同僚", "私", who="L", **e),
        t(ES, "そのあと\n*お昼寝*もいいね", "sleepy_old_memories_cat", "happy_girlfriend_dance_cat", "同僚", "私", who="L", **e),
        t(ES, "そのかわり\n夜まで働くけどね", "cocky_dj_cat", "huh_huh_cat", "同僚", "私", who="L", **e),
        s(US, "*お昼休み*だ！", ME, **u),
        t(US, "サンドイッチ片手に\n*会議*しよう", "rizz_cat_rizz", "stare_big_eyes_tabby_kitten", "上司", "私", who="L", **u),
        t(US, "サラダを\n*10分*で食べて仕事", "work_dog_staring_computer", "think_bike_front_seat_cat", "同僚", "私", who="R", **u),
        t(US, "そのかわり\n*夕方は早く帰る*よ", "showoff_gojo_cosplay_cat", "dance_tabby_standing_cat", "同僚", "私", who="L", **u),
        s(CAFE, "お昼休みも\n国によって*全然ちがう*", "realize_wet_cat_stare", d=2.6, **j),
        s(CAFE, "みんなも\nお昼はちゃんと*休もう*", "happy_hamster_open_arms", d=3.0, se="pinpoon_correct", **j),
    ]


def fit(cs):
    k = 59.9 / sum(c["dur"] for c in cs)
    for c in cs:
        c["dur"] *= k
    return cs


if __name__ == "__main__":
    Wd.run(fit(cuts()), Wd.band_vs("{r}日本{w}vs{c}世界", "{g}お昼休み{y}の過ごし方"),
           os.path.join(Wd.HERE, "out", "short_44_hiru.mp4"), os.path.join(Wd.HERE, "out", "short_44_hiru_preview"))
