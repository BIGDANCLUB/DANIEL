"""ショート25b：日本vs欧米 有給を申請したときの反応（world_short.py・10/24 参考「日本vs海外 有給取得時の反応の違い」の作りをまねる）。59.9秒。

python3 catmeme/short_25b_yukyu.py → out/short_25b_yukyu.mp4
- 登場人物は参考どおり（私・国・上司・同僚・お局）。国の順番（日本→フランス→アメリカ）も同じ。帯・セリフは変える
- 決まりの目安：日本 年10日以上もらえる人は年5日取らせるのが会社の義務（2019年から）。
  フランス 年5週間（30日）が法律で決まっている、夏（5〜10月）に続けて12日以上休む。アメリカ 有給を決めた国の法律はない（会社しだい）
- BGM なし（10/23 ルール）。最後にチャンネル登録の画面は入れない
"""
import os

import world_short as Wd

JP_GOV, JP_OFF = "bg115_japan_diet", "bg25_office_desk"
FR_GOV, FR_OFF = "bg116_paris_assembly", "bg117_paris_office"
US_GOV, US_OFF = "bg118_us_capitol", "bg119_us_office"


def cuts():
    t, s = Wd.talk, Wd.solo
    j = dict(tag="日本", flag="jp")
    f = dict(tag="フランス", flag="fr", tag_style="yellow")
    u = dict(tag="アメリカ", flag="us", tag_style="orange")
    return [
        # ---- 日本 ----
        s(JP_GOV, say="有給って\n使っていいんですよね？", cat="laugh_laughing_dog", label="私", lines=True, se="don_hit", **j),
        t(JP_GOV, say="もちろん！\n年*5日*は取らせる*決まり*です", left="money_counting_orange_cat", right="laugh_laughing_dog",
          who="L", llabel="国", rlabel="私", **j),
        t(JP_OFF, say="有給？\n*月末*じゃなければね…", left="meow_ragdoll_chubby_cat", right="huh_huh_cat", who="L",
          llabel="上司", rlabel="私", **j),
        t(JP_OFF, say="*1日*だけ\nなんですけど…", left="meow_ragdoll_chubby_cat", right="confused_i_dont_know_cat", who="R",
          llabel="上司", rlabel="私", **j),
        t(JP_OFF, say="その日の会議\nだれが出るの…？", left="meow_ragdoll_chubby_cat", right="stare_big_eyes_tabby_kitten", who="R",
          llabel="上司", rlabel="同僚", **j),
        t(JP_OFF, say="すみません…\nご*迷惑*おかけします", left="sad_black_dog", right="stare_big_eyes_tabby_kitten", who="L",
          llabel="私", rlabel="同僚", **j),
        t(JP_OFF, say="私の若いころは\n有給なんて*なかった*わよ", left="sad_black_dog", right="glare_disgusted_cat", llabel="私",
          rlabel="お局", **j),
        t(JP_OFF, say="休むなら\n仕事は全部終わらせてね", left="sulk_hungry_cat", right="rage_talking_cat", llabel="私", rlabel="お局", **j),
        t(JP_OFF, say="休み明けは\n*おみやげ*配らなきゃ…", left="despair_dramatic_kitten", right="rage_talking_cat", who="L",
          llabel="私", rlabel="お局", **j),
        # ---- フランス ----
        t(FR_GOV, say="有給は年*5週間*！\n*法律*で決まってるよ", left="happy_hamster_open_arms", right="laugh_laughing_dog", who="L",
          llabel="国", rlabel="私", se="don_hit", **f),
        t(FR_OFF, say="休み？いいよ！\nいつから？", left="talk_orange_white_sitting_cat", right="huh_huh_cat", who="L",
          llabel="上司", rlabel="私", **f),
        t(FR_OFF, say="えっと…\n*3日*だけです…", left="talk_orange_white_sitting_cat", right="meow_gray_white_kitten", who="R",
          llabel="上司", rlabel="私", **f),
        t(FR_OFF, say="3日！？\nそれは休みと言わないよ", left="surprise_big_pupils_cat", right="meow_gray_white_kitten", who="L",
          llabel="上司", rlabel="私", **f),
        t(FR_OFF, say="夏は*2週間*\nつづけて休むのがふつう！", left="dance_tabby_standing_cat", right="stare_tabby_wide_eyes_cat",
          who="L", llabel="上司", rlabel="私", **f),
        t(FR_OFF, say="ご迷惑を\nおかけします…", left="stare_interviewer_cat", right="sad_black_dog", who="R", llabel="同僚",
          rlabel="私", **f),
        t(FR_OFF, say="お互いさま！\nみんな*夏休み*のために働いてる", left="dance_orange_gray_cats", right="sad_black_dog", who="L",
          llabel="同僚", rlabel="私", **f),
        # ---- アメリカ ----
        t(US_GOV, say="有給の法律？\n国としては*ない*よ", left="cocky_dj_cat", right="sad_banana_cat_cry", who="L", llabel="国",
          rlabel="私", se="don_hit", **u),
        t(US_OFF, say="休みたい？\n*成果*は出てる？", left="stare_interviewer_cat", right="huh_huh_cat", who="L", llabel="上司",
          rlabel="私", **u),
        t(US_OFF, say="はい！\n引きつぎも*完了*です", left="stare_interviewer_cat", right="showoff_gojo_cosplay_cat", who="R",
          llabel="上司", rlabel="私", **u),
        t(US_OFF, say="結果さえ出せば\nいつ休んでもOK！", left="happy_girlfriend_dance_cat", right="showoff_gojo_cosplay_cat", who="L",
          llabel="上司", rlabel="私", **u),
        t(US_OFF, say="ただし休みの日数は\n*会社しだい*だよ", left="talk_orange_white_sitting_cat", right="think_bike_front_seat_cat",
          who="L", llabel="同僚", rlabel="私", **u),
        t(US_OFF, say="休みのあいだ\n私の仕事もよろしく！", left="rizz_cat_rizz", right="think_bike_front_seat_cat", who="L",
          llabel="同僚", rlabel="私", **u),
        t(US_OFF, say="*取引*ってことね", left="rizz_cat_rizz", right="realize_wet_cat_stare", who="R", llabel="同僚", rlabel="私",
          dur=2.4, **u),
        s(US_OFF, say="休みかたも\n国によって*全然ちがう*", cat="realize_wet_cat_stare", label="私", dur=3.0, **u),
    ]


if __name__ == "__main__":
    Wd.run(cuts(), Wd.band_vs("{r}日本{w}vs{c}欧米", "{g}有給{y}を申請したら…"),
           os.path.join(Wd.HERE, "out", "short_25b_yukyu.mp4"), os.path.join(Wd.HERE, "out", "short_25b_yukyu_preview"))
