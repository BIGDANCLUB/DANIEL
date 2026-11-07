"""ショート25b：日本vs世界 有給を取りたいと言ったら（world_short.py・10/24 参考「日本vs海外 有給取得時の反応の違い」を1カットずつまねる）。59.9秒。

python3 catmeme/short_25b_yukyu.py → out/short_25b_yukyu.mp4
- 10/24 ユーザー指定「口調や素材の使い方をもっと厳密に」：国ごとに「私（集中線）→ 国 → 職場の上司・同僚・お局」の順、
  役名は左右とも札、私の猫・国の猫の選び方、最後の「チャンネル登録」ボタンまで参考どおり。文は書きかえる
- 国旗は付けない（参考どおり）。札の色は 日本＝赤・フランス＝黄・アメリカ＝オレンジ
- 決まりの目安：日本 年10日以上もらえる人は年5日取らせるのが会社の義務。フランス 年5週間（30日）が法律、
  夏（5〜10月）に12日以上続けて休む。アメリカ 有給を決めた国の法律はない（会社しだい）
- BGM なし（10/23 ルール）
"""
import os

import world_short as Wd

JP_GOV, JP_OFF = "bg115_japan_diet", "bg25_office_desk"
FR_GOV, FR_OFF = "bg116_paris_assembly", "bg117_paris_office"
US_GOV, US_OFF = "bg118_us_capitol", "bg119_us_office"
K = 59.9 / 68.0   # 参考の長さ（68秒）→ 59.9秒
ME = "laugh_laughing_dog"   # 参考の「私」（にっこり笑う犬）に近い素材


def cuts():
    def s(bg, d, say, cat, **kw):
        return Wd.solo(bg, kw.pop("tag"), say, cat, dur=d * K, label="私", lines=True, se="don_hit", **kw)

    def t(bg, d, say, left, right, ll, rl, **kw):
        return Wd.talk(bg, kw.pop("tag"), say, left, right, dur=d * K, llabel=ll, rlabel=rl, **kw)

    j = dict(tag="日本")
    f = dict(tag="フランス", tag_style="yellow")
    u = dict(tag="アメリカ", tag_style="orange")
    return [
        # ---- 日本 ----
        s(JP_GOV, 1.6, "*有給*使いたいです！", ME, **j),
        t(JP_GOV, 3.0, "どうぞどうぞ！\n年5日は取らせる*義務*です！！", "yell_orange_fat_cat", ME, "国", "私", who="L", **j),
        t(JP_OFF, 3.0, "有給？\n*半日*くらいならいいよ", "talk_orange_white_sitting_cat", "call_customer_service_cat", "上司", "私",
          who="L", **j),
        t(JP_OFF, 2.6, "え、休んでる間の仕事\n*だれが*やるの？", "talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten",
          "上司", "同僚", who="R", **j),
        t(JP_OFF, 2.6, "すみません…\nご迷惑おかけします…", "confused_i_dont_know_cat", "stare_big_eyes_tabby_kitten", "私", "同僚",
          who="L", **j),
        t(JP_OFF, 3.4, "悪いけどこの仕事\n*あなたしか*分からないのよ", "confused_i_dont_know_cat", "rizz_cat_rizz", "私", "お局", who="R", **j),
        t(JP_OFF, 2.2, "*連休*とかは\nやめてよね!!", "confused_i_dont_know_cat", "meow_ragdoll_chubby_cat", "私", "お局", who="R", **j),
        t(JP_OFF, 3.4, "有給って使いづらいな…\n*おみやげ*買っとかなきゃ…", "despair_dramatic_kitten", "yell_orange_fat_cat", "私", "お局",
          who="L", **j),
        # ---- フランス ----
        s(FR_GOV, 1.6, "*有給*使いたいです！", ME, **f),
        t(FR_GOV, 3.4, "もちろん！\n*年5週間*は\n法律で決まってますから！！", "happy_girlfriend_dance_cat", ME, "国", "私", who="L", **f),
        t(FR_OFF, 3.0, "有給を使いたいって？", "angry_aiming_cat", "call_customer_service_cat", "上司", "私", who="L", **f),
        t(FR_OFF, 3.0, "はい、\nできれば*2週間*ほど…", "angry_aiming_cat", "calmdown_dancing_cat", "上司", "私", who="R", **f),
        t(FR_OFF, 3.4, "いいよいいよ！\n夏は*長く休む*のが当たり前！", "joy_happy_happy_happy_cat", "calmdown_dancing_cat", "上司", "私",
          who="L", **f),
        t(FR_OFF, 2.0, "夏は*12日以上*続けて\n休む決まりだもん！", "surprise_big_pupils_cat", "calmdown_dancing_cat", "上司", "私",
          who="L", **f),
        t(FR_OFF, 3.4, "ありがとうございます！\nご迷惑おかけします…", "work_typing_cat", "confused_i_dont_know_cat", "同僚", "私", who="R", **f),
        t(FR_OFF, 3.6, "迷惑なんて思わないよww\nお互いさまだし、\nみんな*夏休みのため*に働いてるじゃん！",
          "dance_tabby_standing_cat", "confused_i_dont_know_cat", "同僚", "私", who="L", **f),
        # ---- アメリカ ----
        s(US_GOV, 1.8, "*有給*使いたいです！", ME, **u),
        t(US_GOV, 3.4, "で？\n有給の法律なんて*ない*よ", "sleepy_old_memories_cat", "sad_banana_cat_cry", "国", "私", who="L", **u),
        t(US_OFF, 4.6, "休みたい？\n今月の*ノルマ*は大丈夫？", "stare_interviewer_cat", "call_customer_service_cat", "上司", "私",
          who="L", **u),
        t(US_OFF, 4.2, "はい、達成ずみです！\n休みの間の*引きつぎ*もばっちり", "stare_interviewer_cat", "realize_wet_cat_stare", "上司", "私",
          who="R", **u),
        t(US_OFF, 4.4, "*結果*さえ出してくれれば文句なし！\n好きなだけ休んで！", "eat_pop_cat", "realize_wet_cat_stare", "上司", "私",
          who="L", **u),
        dict(t(US_OFF, 3.4, "*持ちつ持たれつ*でいこう！\nおれが休むときはよろしくな", "slack_nail_filing_cat", ME, "同僚", "私",
               who="L", se="pikon", **u), subscribe=True),
    ]


if __name__ == "__main__":
    Wd.run(cuts(), Wd.band_vs("{r}日本{w}vs{c}世界", "{g}有給{y}を取りたいと言ったら"),
           os.path.join(Wd.HERE, "out", "short_25b_yukyu.mp4"), os.path.join(Wd.HERE, "out", "short_25b_yukyu_preview"))
