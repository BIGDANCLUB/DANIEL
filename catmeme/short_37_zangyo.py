"""ショート37：日本vs世界 定時直前に残業を頼まれたら（world_short.py・有給の反応ショート25bと同じ作り）。59.9秒。

python3 catmeme/short_37_zangyo.py → out/short_37_zangyo.mp4
- 国ごとに「私（集中線）→ 国 → 職場の上司・同僚」の順。札の色は 日本＝赤・ドイツ＝黄・アメリカ＝オレンジ
- 決まりの目安：日本 残業は36協定を結べば可能・上限は原則 月45時間。ドイツ 1日の労働は原則8時間・最長10時間、
  多くの会社で残業は「労働時間口座」にためて休みで返す。アメリカ 時給の人などは週40時間をこえると1.5倍の残業代、
  一部の月給の人は残業代の対象外
- チャンネル登録のボタンは入れない（10/26 ユーザー指定）。締めは「みんなも働きすぎに気をつけよう」
- BGM なし（10/23 ルール）
"""
import os

import world_short as Wd

JP_GOV, JP_OFF = "bg115_japan_diet", "bg25_office_desk"
DE_GOV, DE_OFF = "bg116_paris_assembly", "bg78_agency_office"
US_GOV, US_OFF = "bg118_us_capitol", "bg119_us_office"
ME = "laugh_laughing_dog"


def cuts():
    def s(bg, d, say, cat, **kw):
        kw.setdefault("se", "don_hit")
        return Wd.solo(bg, kw.pop("tag"), say, cat, dur=d, label="私", lines=True, **kw)

    def t(bg, d, say, left, right, ll, rl, **kw):
        return Wd.talk(bg, kw.pop("tag"), say, left, right, dur=d, llabel=ll, rlabel=rl, **kw)

    j = dict(tag="日本")
    g = dict(tag="ドイツ", tag_style="yellow")
    u = dict(tag="アメリカ", tag_style="orange")
    return [
        # ---- 日本 ----
        s(JP_OFF, 1.8, "よし！\n*定時*で帰るぞ！", ME, **j),
        t(JP_GOV, 2.6, "残業は\n*月45時間*までが原則です", "stare_interviewer_cat", "dance_tabby_standing_cat", "国", "私", who="L", **j),
        t(JP_OFF, 2.6, "あ ちょっといい？\nこれ*明日の朝*までに", "rizz_cat_rizz", "stare_tabby_wide_eyes_cat", "上司", "私", who="L", **j),
        t(JP_OFF, 2.4, "……\nわかりました", "rizz_cat_rizz", "sulk_hungry_cat", "上司", "私", who="R", **j),
        t(JP_OFF, 2.6, "みんな残ってるし\n*先に帰りづらい*よね", "blank_black_cat_zoning_out", "sad_black_dog", "同僚", "私", who="L", **j),
        t(JP_OFF, 2.6, "若いうちは\n*残ってなんぼ*よ", "meow_ragdoll_chubby_cat", "sad_banana_cat_cry", "お局", "私", who="L", **j),
        t(JP_OFF, 2.6, "気づけば*夜10時*\n今日も終電…", "work_typing_cat", "despair_dramatic_kitten", "同僚", "私", who="R", **j),
        # ---- ドイツ ----
        s(DE_OFF, 1.8, "よし！\n*定時*で帰るぞ！", ME, **g),
        t(DE_GOV, 2.6, "1日の仕事は\n原則*8時間*まで！", "talk_orange_white_sitting_cat", "happy_hamster_open_arms", "国", "私", who="L", **g),
        t(DE_OFF, 2.6, "あ ちょっといい？\nこれ*明日*お願いできる？", "stare_interviewer_cat", "peek_what_happen_cat", "上司", "私", who="L", **g),
        t(DE_OFF, 2.4, "今日やらなくて\nいいんですか？", "stare_interviewer_cat", "surprise_big_pupils_cat", "上司", "私", who="R", **g),
        t(DE_OFF, 2.8, "残業したら\nその分*休み*で返すからね", "calmdown_dancing_cat", "stare_big_eyes_tabby_kitten", "上司", "私", who="L", **g),
        t(DE_OFF, 2.6, "たまった時間で\n*夏休み*をのばそう！", "happy_chipi_chapa_cat", "dance_three_kittens", "同僚", "私", who="L", **g),
        t(DE_OFF, 2.6, "まだいるの？\n早く帰りなよww", "dance_orange_gray_cats", "confused_i_dont_know_cat", "同僚", "私", who="L", **g),
        # ---- アメリカ ----
        s(US_OFF, 1.8, "よし！\n*定時*で帰るぞ！", ME, **u),
        t(US_GOV, 2.6, "時給の人は残業代\n*1.5倍*だよ！", "cocky_dj_cat", "happy_girlfriend_dance_cat", "国", "私", who="L", **u),
        t(US_OFF, 2.6, "残業してくれたら\n*1.5倍*払うよ", "money_counting_orange_cat", "showoff_gojo_cosplay_cat", "上司", "私", who="L", **u),
        t(US_OFF, 2.4, "やります！\n*稼げる*なら！", "money_counting_orange_cat", "yell_orange_fat_cat", "上司", "私", who="R", **u),
        t(US_OFF, 2.6, "でも結果が出ないと\n*すぐクビ*もあるよ", "angry_aiming_cat", "stare_big_eyes_tabby_kitten", "上司", "私", who="L", **u),
        t(US_OFF, 2.8, "でも月給の人は\n残業代*出ない*こともあるよ", "glare_disgusted_cat", "stare_tabby_wide_eyes_cat", "同僚", "私", who="L", **u),
        t(US_OFF, 2.4, "えっ\nぼく月給…", "glare_disgusted_cat", "huh_huh_cat", "同僚", "私", who="R", **u),
        # ---- まとめ ----
        s(JP_OFF, 2.6, "国によって\n残業の考え方が*全然ちがう*", "realize_wet_cat_stare", **j),
        s(JP_OFF, 2.8, "みんなも\n*働きすぎ*に気をつけよう！", "happy_hamster_open_arms", se="pinpoon_correct", **j),
    ]


def fit(cs):
    k = 59.9 / sum(c["dur"] for c in cs)   # 59.9秒ちょうどに
    for c in cs:
        c["dur"] *= k
    return cs


if __name__ == "__main__":
    Wd.run(fit(cuts()), Wd.band_vs("{r}日本{w}vs{c}世界", "{y}定時直前に{g}残業{y}を頼まれたら"),
           os.path.join(Wd.HERE, "out", "short_37_zangyo.mp4"), os.path.join(Wd.HERE, "out", "short_37_zangyo_preview"))
