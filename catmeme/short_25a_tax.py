"""ショート25a：日本vsシンガポール 税金のちがい（world_short.py・10/24 参考「日本vs海外 税金格差の違い」の作りをまねる）。59.9秒。

python3 catmeme/short_25a_tax.py → out/short_25a_tax.mp4
- 作り・登場人物（「税金」の札の猫と、話を聞く猫）は参考どおり。帯・セリフは参考と変える
- 数字（2026年の目安）：日本 所得税の最高45%＋住民税10%＝55%、相続税の最高55%、消費税10%。
  シンガポール 個人所得税の最高24%（2024年分から）、住民税なし、株の売却益に税金なし、相続税は2008年に廃止、GST（消費税）9%
- BGM なし（10/23 ルール）
"""
import os

import world_short as Wd

JP, SG = "bg113_fuji_town", "bg114_singapore_bay"
T = "税金"


def cuts():
    t, s = Wd.talk, Wd.solo
    j = dict(tag="日本", flag="jp")
    g = dict(tag="シンガポール", flag="sg")
    return [
        # ---- 日本 ----
        s(JP, say="かせぐほど\n*税率*が上がっていくよ", cat="laugh_laughing_dog", label=T, se="don_hit", **j),
        t(JP, say="所得税と住民税で\n最高*55%*いただきます", left="huh_huh_cat", right="yell_orange_fat_cat", rlabel=T, **j),
        t(JP, say="半分以上！？\nがんばった意味は…", left="stare_tabby_wide_eyes_cat", right="yell_orange_fat_cat", who="L",
          rlabel=T, **j),
        t(JP, say="買い物のたびに\n*消費税10%*もね", left="stare_tabby_wide_eyes_cat", right="cocky_dj_cat", rlabel=T, **j),
        t(JP, say="給料明細の\n“引かれる欄”が長すぎる…", left="sulk_hungry_cat", right="cocky_dj_cat", who="L", rlabel=T, **j),
        t(JP, say="社会保険料も\n毎月しっかり引きますね", left="sulk_hungry_cat", right="money_counting_orange_cat", rlabel=T, **j),
        t(JP, say="亡くなったあとも\n*相続税*が最高55%", left="blank_black_cat_zoning_out", right="money_counting_orange_cat",
          rlabel=T, **j),
        t(JP, say="最後まで\nついてくるの！？", left="despair_dramatic_kitten", right="money_counting_orange_cat", who="L",
          rlabel=T, **j),
        t(JP, say="そのかわり\n道も病院もきちんとしてるでしょ", left="despair_dramatic_kitten", right="talk_orange_white_sitting_cat",
          rlabel=T, **j),
        s(JP, say="……は？", cat="huh_huh_cat", big_say=True, se="question_mark_pop_confused_huh", **j),
        # ---- シンガポール ----
        s(SG, say="所得税の最高は\n*24%*だよ！", cat="happy_hamster_open_arms", label=T, se="don_hit", **g),
        t(SG, say="日本の半分以下！？", left="surprise_big_pupils_cat", right="happy_hamster_open_arms", who="L", rlabel=T, **g),
        t(SG, say="住民税は\nそもそも*ない*よ", left="surprise_big_pupils_cat", right="dance_tabby_standing_cat", rlabel=T, **g),
        t(SG, say="じゃあ別のところで\nがっつり取るんでしょ？", left="glare_disgusted_cat", right="dance_tabby_standing_cat", who="L",
          rlabel=T, **g),
        t(SG, say="株でもうけても\n税金は*かからない*よ", left="glare_disgusted_cat", right="showoff_gojo_cosplay_cat", rlabel=T, **g),
        t(SG, say="相続税も\n2008年に*やめた*よ", left="stare_big_eyes_tabby_kitten", right="showoff_gojo_cosplay_cat", rlabel=T, **g),
        t(SG, say="うそでしょ…\n日本とまるで逆！", left="stare_big_eyes_tabby_kitten", right="dance_orange_gray_cats", who="L",
          rlabel=T, **g),
        t(SG, say="消費税にあたる\nGSTは*9%*だけどね", left="think_bike_front_seat_cat", right="talk_orange_white_sitting_cat",
          rlabel=T, **g),
        t(SG, say="でも家賃と車が\nめちゃくちゃ高いって…", left="think_bike_front_seat_cat", right="talk_orange_white_sitting_cat",
          who="L", rlabel=T, **g),
        t(SG, say="それは税金じゃなくて\n*物価*の話だからね", left="realize_wet_cat_stare", right="cocky_dj_cat", rlabel=T, **g),
        t(SG, say="税金が安いぶん\n自分で備えるのが前提だよ", left="realize_wet_cat_stare", right="talk_orange_white_sitting_cat",
          rlabel=T, **g),
        s(SG, say="どっちがいいかは\n*人それぞれ*…", cat="sleepy_old_memories_cat", **g),
        t(SG, say="とりあえず…\n移住のパンフ見とこ", left="read_book_orange_kitten", right="sleep_sleeping_cat", who="L", rlabel=T, **g),
        t(SG, say="（税金は寝てる）", left="read_book_orange_kitten", right="sleep_sleeping_cat", rlabel=T, dur=2.4, **g),
    ]


if __name__ == "__main__":
    Wd.run(cuts(), Wd.band_vs("{r}日本{w}vs{c}シンガポール", "{y}とられる税金ここまで差"),
           os.path.join(Wd.HERE, "out", "short_25a_tax.mp4"), os.path.join(Wd.HERE, "out", "short_25a_tax_preview"))
