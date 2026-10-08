"""シリーズ「ネットで生まれた名フレーズ」のショート（縦 1080x1920・45〜58秒）。
ニュースへのネットの反応から生まれて広まったフレーズを、1本1フレーズで紹介する。

python3 catmeme/short_meme_phrases.py           → 全部
python3 catmeme/short_meme_phrases.py kome toilet → 指定したものだけ（キー：todai kome toilet tanishi noriben goto）
→ out/short_meme_<キー>.mp4
画面の作りは short_04_leak.py と同じ（上：話題の札つきタイトル帯／中：場面かパネル／下：大きな字幕）。

ルール：笑うのは「言葉の面白さ」と「出来事のおかしさ」まで。実在の人の発言は報道の要旨だけで、個人をバカにしない。
賛否が分かれた話（2億円トイレなど）は、両方の言い分を出す。
"""
import os
import sys

import short_03_kodomo_nisa as S
import short_04_leak as Q

HERE = S.HERE
PURPLE, NORA, COCOA = Q.PURPLE, Q.NORA, Q.COCOA
MIRAI = os.path.join(S.BGM, "未来を創る君たちへ.mp3")
NEWS, SAGE, NET = S.NEWS, S.SAGE, (120, 50, 170)
YELLOW, RED, NAVY = S.YELLOW, S.RED, S.NAVY
one, two, panel, items, big = Q.one, Q.two, Q.panel, Q.items, Q.big
LABEL = "ネットで生まれた名フレーズ"


def net(b, a, cap, **kw):
    return dict(kind="scene", bg=Q.bg(b), cats=[Q.cat(a, "ネットの声", 960, NET, h=860)], cap=cap, **kw)


def intro(b, a, cap, **kw):
    return one(b, a, "ニュース猫", NEWS, cap, cap_col=RED, fx=["lines", "shake"], **kw)


def outro(cap="ほかに知ってる\n名フレーズは？\nコメントで教えて！"):
    return one("bg03_blackboard", "wave_waving_cat", "ニュース猫", NEWS, cap, cap_col=YELLOW, h=760, dur=3.2, se="chirin",
               bgm={"file": MIRAI, "gain": -8, "fade": 0.8})


# ---- 553＞1107（東大の総長選・2026） ----
def cuts_todai():
    return [
        intro("bg01_campus", "surprise_big_pupils_cat", "553＞1107\nってなに！？", dur=2.6, se=["jan", "doon_heavy"],
              bgm={"file": PURPLE, "gain": -6}),
        panel(big("東大の総長選（2026年9月）", "1位：1,107票\n2位：553票", col=NAVY, note="学内の先生たちの投票（決選投票）"),
              "1位は半分以上の票", dur=3.6, se="card_flip"),
        two("bg02_room", "joy_happy_happy_happy_cat", "eat_pop_cat", "2位の倍よ倍！\nはい優勝！", who="L", dur=2.6, until=3.0,
            se="game_mario_1up"),
        panel(big("ところが選ばれたのは", "2位の人", note="最後に決めるのは16人の会議。投票は「参考の一つ」"), "えっ", cap_col=RED,
              dur=3.6, se="doon_heavy"),
        intro("bg06_spotlight", "weird_meowing_cat", "553が1107に\n勝った！？", dur=2.4, se="explosion_chudoon"),
        net("bg09_sns", "cocky_dj_cat", "「553＞1107という\n不等式が東大によって\n示された」", dur=3.6, se="kon"),
        two("bg09_sns", "huh_huh_cat", "think_bike_front_seat_cat", "数学の不等式に\nしちゃったのか", who="L", dur=2.4, se="pikon"),
        two("bg09_sns", "huh_huh_cat", "think_bike_front_seat_cat", "東大＝受験の\n数学のイメージと\n重なって一気に広まった", who="R", dur=3.4,
            se="page_turn_01"),
        panel(items("なぜウケた？", ["数字だけで状況がわかる", "算数ではありえない式", "「東大なのに」というギャップ"]), "ウケたポイント",
              dur=4.2, se="xylophone_transition", bgm={"file": COCOA, "gain": -6}),
        two("bg02_room", "spin_spinning_cat", "eat_pop_cat", "ルール違反じゃないけど\n選んだ理由の説明が\nほしかった、という声も", who="R",
            dur=3.4, se="hyoshigi_01"),
        two("bg02_room", "sleepy_sleepy_cat", "eat_pop_cat", "笑いのなかに\nモヤモヤが入ってるのが\n名フレーズの条件だな", who="R",
            dur=3.4, se="tv_professional_poon"),
        net("bg09_sns", "dance_trending_cat", "不等式の向き\n逆じゃない？\nって二度見した", dur=2.8, se="boing_01"),
        outro(),
    ]


# ---- 古古古米（令和の米騒動・2025） ----
def cuts_kome():
    return [
        intro("bg16_food_aisle", "surprise_big_pupils_cat", "「古古古米」\nってなに！？", dur=2.6, se=["jan", "doon_heavy"],
              bgm={"file": PURPLE, "gain": -6}),
        panel(items("2025年　令和の米騒動", ["お米の値段が大きく上がった", "国が「備蓄米」を放出", "5kg　2,000円前後で店頭へ"]),
              "国のストックを放出", dur=4.0, se="page_turn_01"),
        panel(big("備蓄米の年産", "2022年産＝古古米\n2021年産＝古古古米", col=NAVY, note="2020年産の「古古古古米」も"),
              "古が増えていく", dur=3.8, se="card_flip"),
        intro("bg16_food_aisle", "weird_meowing_cat", "古古古古米！？\n“古”が多すぎる", dur=2.6, se="explosion_chudoon"),
        net("bg09_sns", "cocky_dj_cat", "「古」が\nいくつあるか\n数えられない", dur=2.8, se="kon"),
        net("bg09_sns", "dance_trending_cat", "早口言葉みたいに\n言いたくなる", dur=2.6, se="pikon"),
        two("bg14_home_night", "huh_huh_cat", "eat_pop_cat", "で、味はどうなの？", who="L", dur=2.2, se="question_hatena_maou"),
        two("bg14_home_night", "huh_huh_cat", "eat_pop_cat", "「言われなければ普通」\n「毎日食べられる」\nという声が多かった", who="R", dur=3.4,
            se="pinpoon_correct"),
        two("bg14_home_night", "happy_chipi_chapa_cat", "eat_pop_cat", "古いけど\n普通においしいのか", who="L", dur=2.4, until=2.8,
            se="eat_paku"),
        panel(items("なぜウケた？", ["「古」が重なる響きの面白さ", "米の値段への不満とセット", "買ってみたら意外とおいしい"]),
              "ウケたポイント", dur=4.2, se="xylophone_transition", bgm={"file": COCOA, "gain": -6}),
        two("bg02_room", "sleepy_sleepy_cat", "think_bike_front_seat_cat", "笑いのネタになりつつ\nお米の値段を考える\nきっかけにもなった", who="R",
            dur=3.4, se="tv_professional_poon"),
        net("bg09_sns", "laugh_laughing_dog", "そのうち\n古古古古古米も\n出てくるのでは", dur=3.0, se="boing_01"),
        two("bg16_food_aisle", "huh_huh_cat", "eat_pop_cat", "古い米は\n低温の倉庫で\n保管されてたんだ", who="R", dur=3.0, se="page_turn_02"),
        outro(),
    ]


# ---- 2億円トイレ（大阪・関西万博・2024） ----
def cuts_toilet():
    return [
        intro("bg06_spotlight", "surprise_big_pupils_cat", "2億円の\nトイレ！？", dur=2.6, se=["jan", "doon_heavy"],
              bgm={"file": PURPLE, "gain": -6}),
        panel(items("大阪・関西万博（2024年に話題）", ["会場に若手建築家のデザイナーズトイレ", "「1か所で約2億円」と報道", "SNSで一気に広まった"]),
              "万博のトイレ", dur=4.0, se="page_turn_01"),
        net("bg09_sns", "angry_cat_hits_cat", "トイレに2億円！？\n税金の使い方\nおかしくない？", dur=3.0, se="buzzer_wrong"),
        net("bg09_sns", "glare_disgusted_cat", "どんな金のトイレ\nなんだよ", dur=2.6, se="kon"),
        two("bg02_room", "huh_huh_cat", "think_bike_front_seat_cat", "ところが　これには\n反論もあったんだ", who="R", dur=2.6,
            se="hyoshigi_01", bgm={"file": NORA, "gain": -6}),
        panel(items("設計した人・府の説明（要旨）", ["実際は便器46基の大きなトイレ", "見直しで約1.5億円（解体費込み・税抜）", "閉幕後は移して使う前提"]),
              "1か所で46基！", dur=4.4, se="card_flip"),
        panel(big("府知事の説明（要旨）", "1㎡あたりは\n一般の公共トイレより\n安い", col=NAVY, note="面積あたりの単価で比べると…という説明"),
              "面積で比べると…", dur=3.8, se="pinpoon_note"),
        two("bg02_room", "weird_meowing_cat", "think_bike_front_seat_cat", "1個のトイレじゃ\nなかったのか！", who="L", dur=2.4,
            se="pikon"),
        panel(items("なぜウケた？", ["「2億円」と「トイレ」のギャップ", "写真の一部だけが広まった", "万博の費用への不満とセット"]),
              "ウケたポイント", dur=4.2, se="xylophone_transition", bgm={"file": COCOA, "gain": -6}),
        two("bg02_room", "sleepy_sleepy_cat", "think_bike_front_seat_cat", "数字だけが一人歩きすると\n中身が伝わらない\nいい例だな", who="R",
            dur=3.4, se="tv_professional_poon"),
        net("bg09_sns", "dance_trending_cat", "結局いくらなの？\nってみんな混乱", dur=2.8, se="question_hatena_maou"),
        two("bg02_room", "weird_meowing_cat", "think_bike_front_seat_cat", "「2億円」は最初の報道の数字\n見直し後は約1.5億円\nどちらも1か所の金額", who="R", dur=3.6, se="page_turn_02"),
        outro(),
    ]


# ---- ジャンボタニシ農法（2024） ----
def cuts_tanishi():
    return [
        intro("bg18_backyard", "surprise_big_pupils_cat", "ジャンボタニシ\n農法！？", dur=2.6, se=["jan", "doon_heavy"],
              bgm={"file": PURPLE, "gain": -6}),
        panel(items("ジャンボタニシってなに？", ["正式名：スクミリンゴガイ", "南米から来た外来の巻き貝", "田んぼの稲を食べてしまう"]),
              "外来の巻き貝", dur=4.0, se="page_turn_01"),
        net("bg09_sns", "cocky_dj_cat", "「雑草を食べてくれる\n“生きた除草剤”」\nという投稿が拡散", dur=3.4, se="kon"),
        two("bg02_room", "huh_huh_cat", "eat_pop_cat", "え、便利じゃん", who="L", dur=2.0, se="question_hatena_maou"),
        panel(big("農林水産省（2024年3月）", "「放すのは\nやめてください」", col=RED, note="まわりの田んぼに広がり　稲の被害が出るため"),
              "国が止めた！", cap_col=RED, dur=4.0, se="doon_heavy", bgm={"file": NORA, "gain": -6}),
        intro("bg06_spotlight", "weird_meowing_cat", "農水省が\nSNSで止めた！？", dur=2.4, se="explosion_chudoon"),
        two("bg09_sns", "huh_huh_cat", "think_bike_front_seat_cat", "名前が出た地元のJAも\n「すすめた事実は一切ない」\nと発表", who="R", dur=3.4,
            se="pinpon_notice"),
        net("bg09_sns", "dance_trending_cat", "「〇〇農法」って\n付けるとなんか\nそれっぽく見える", dur=3.0, se="pikon"),
        panel(items("なぜウケた？", ["「ジャンボ」と「農法」の響き", "国が公式に止めるという展開", "「生きた除草剤」のパワーワード"]),
              "ウケたポイント", dur=4.2, se="xylophone_transition", bgm={"file": COCOA, "gain": -6}),
        two("bg02_room", "sleepy_sleepy_cat", "think_bike_front_seat_cat", "それっぽい名前の\n裏ワザほど\n一度調べるのが大事な", who="R",
            dur=3.4, se="tv_professional_poon"),
        net("bg09_sns", "laugh_laughing_dog", "名前のインパクトが\n強すぎる", dur=2.6, se="boing_01"),
        two("bg18_backyard", "huh_huh_cat", "think_bike_front_seat_cat", "一度広がると\n駆除がとても大変な\n外来種なんだ", who="R", dur=3.2, se="page_turn_02"),
        outro(),
    ]


# ---- のり弁（黒塗りの公文書） ----
def cuts_noriben():
    return [
        intro("bg15_convenience", "surprise_big_pupils_cat", "国の書類が\n「のり弁」！？", dur=2.6, se=["jan", "doon_heavy"],
              bgm={"file": PURPLE, "gain": -6}),
        panel(items("情報公開ってなに？", ["国や役所の書類は　請求すれば見られる", "ただし　個人情報などは黒く塗って隠す", "これを「黒塗り」という"]),
              "役所の書類は見られる", dur=4.2, se="page_turn_01"),
        panel(big("ところが…", "ほぼ全部\n真っ黒", col=(30, 30, 30), note="ページのほとんどが黒く塗られた書類も"),
              "読めるところがない", cap_col=RED, dur=3.6, se="doon_heavy"),
        intro("bg07_press", "weird_meowing_cat", "それ見せた\nことになる！？", dur=2.4, se="explosion_chudoon"),
        net("bg09_sns", "cocky_dj_cat", "海苔が\n敷き詰められた\nお弁当みたい", dur=2.8, se="kon"),
        two("bg15_convenience", "huh_huh_cat", "eat_pop_cat", "真っ黒な書類＝のり弁\nたしかに似てる", who="L", dur=2.8, se="pikon"),
        two("bg15_convenience", "huh_huh_cat", "eat_pop_cat", "森友問題などで\n黒塗りの書類が続いて\n一気に広まったんだ", who="R", dur=3.4,
            se="page_turn_02", bgm={"file": NORA, "gain": -6}),
        net("bg09_sns", "dance_trending_cat", "おかずも\n入れてほしい", dur=2.4, se="boing_01"),
        panel(items("なぜウケた？", ["見た目がそっくり", "身近なお弁当にたとえて誰でもわかる", "「隠しすぎ」への皮肉が伝わる"]),
              "ウケたポイント", dur=4.2, se="xylophone_transition", bgm={"file": COCOA, "gain": -6}),
        two("bg02_room", "sleepy_sleepy_cat", "think_bike_front_seat_cat", "隠す理由がある部分もある\nでも隠しすぎると\n信用がなくなるんだよな", who="R",
            dur=3.4, se="tv_professional_poon"),
        net("bg09_sns", "laugh_laughing_dog", "今日のお弁当も\nのり弁でした", dur=2.6, se="boing_01"),
        two("bg07_press", "huh_huh_cat", "think_bike_front_seat_cat", "その後　ニュースでも\n「のり弁」と書かれるくらい\n定着した", who="R", dur=3.2, se="page_turn_01"),
        outro(),
    ]


# ---- GoToトラブル（2020） ----
def cuts_goto():
    return [
        intro("bg20_counter", "surprise_big_pupils_cat", "GoTo\n“トラブル”！？", dur=2.6, se=["jan", "doon_heavy"],
              bgm={"file": PURPLE, "gain": -6}),
        panel(items("GoToトラベル（2020年）", ["コロナで落ち込んだ旅行を応援", "旅行代金の一部を国が割引", "地域で使えるクーポンも"]),
              "旅行が安くなる", dur=4.0, se="page_turn_01"),
        two("bg20_counter", "happy_chipi_chapa_cat", "eat_pop_cat", "お得じゃん！", who="L", dur=2.0, until=2.4, se="game_mario_1up"),
        panel(items("ところが…（2020年）", ["7月　開始を前倒し", "直前に「東京発着は対象外」", "11月　一部の地域を停止", "12月　全国で一時停止"]),
              "変更につぐ変更", cap_col=RED, dur=4.6, se="doon_heavy", bgm={"file": NORA, "gain": -6}),
        intro("bg06_spotlight", "weird_meowing_cat", "ルール\n変わりすぎ！？", dur=2.4, se="explosion_chudoon"),
        net("bg09_sns", "cocky_dj_cat", "トラベルじゃなくて\n“トラブル”", dur=2.8, se="kon"),
        two("bg20_counter", "huh_huh_cat", "think_bike_front_seat_cat", "始まる前から\nテレビやネットで\nこう言われてたんだ", who="R", dur=3.0,
            se="page_turn_02"),
        net("bg09_sns", "dance_trending_cat", "キャンセル料は\nどうなるの！？", dur=2.4, se="question_hatena_maou"),
        panel(items("なぜウケた？", ["1文字ちがいのダジャレ", "混乱ぶりをひとことで表せる", "旅行する人も宿も振り回された"]),
              "ウケたポイント", dur=4.2, se="xylophone_transition", bgm={"file": COCOA, "gain": -6}),
        two("bg02_room", "sleepy_sleepy_cat", "think_bike_front_seat_cat", "感染の波に合わせた\n判断の難しさも\nあったんだけどな", who="R",
            dur=3.4, se="tv_professional_poon"),
        net("bg09_sns", "laugh_laughing_dog", "予約したのに\n対象外になった……", dur=2.8, se="tear_drop"),
        two("bg20_counter", "huh_huh_cat", "think_bike_front_seat_cat", "キャンセル料は\n国が補う仕組みも\n用意されたんだ", who="R", dur=3.2, se="pinpoon_note"),
        outro(),
    ]


SHORTS = {
    "todai": (cuts_todai, ("東大の総長選で生まれた", "553＞1107")),
    "kome": (cuts_kome, ("令和の米騒動で生まれた", "古古古米")),
    "toilet": (cuts_toilet, ("大阪・関西万博で生まれた", "2億円トイレ")),
    "tanishi": (cuts_tanishi, ("SNSで広まった", "ジャンボタニシ農法")),
    "noriben": (cuts_noriben, ("黒塗りの公文書を", "のり弁")),
    "goto": (cuts_goto, ("GoToトラベルが", "GoToトラブル")),
}


def main():
    for key in sys.argv[1:] or list(SHORTS):
        fn, title = SHORTS[key]
        name = "short_meme_" + key
        S.run(fn(), Q.title_band(*title, label=LABEL), os.path.join(HERE, "out", name + ".mp4"),
              os.path.join(HERE, "out", name + "_preview"))


if __name__ == "__main__":
    main()
