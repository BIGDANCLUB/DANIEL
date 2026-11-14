"""自堕落シリーズ #3：30代独身男、金曜の夜にコンビニ3軒はしごで家飲み（jidaraku.py・10/24 参考動画の作り）。約6〜7分。

python3 catmeme/jidaraku_03_conbini.py → out/jidaraku_03_conbini.mp4
- 流れ：金曜の仕事帰り → セブン-イレブン・ファミリーマート・ローソンをはしご → 家で全部並べて家飲み → 調子に乗って夜中にカップ麺 →
  翌朝むくみと胃もたれとゴミの山 → 夕方、新作スイーツの知らせを見てまたコンビニへ
- 具体名（10/26 ユーザー指定）：ななチキ・からあげ棒（セブン）、ファミチキ（ファミマ）、からあげクン（ローソン）、
  プレミアムロールケーキ（ローソン Uchi Café）、おでん、ペヤング、カップヌードル、ピザポテト、ハイボール缶。
  値段は書かない（店や時期で変わるため）。お酒はほどほどに、の一言を最後に入れる
- 主人公は「俺」。猫1匹だけ。語りは「〜だ。」、声に出すのは「」。「にゃ」なし。単語の途中で改行しない
- 背景はユーザーが別途くれる画像を backgrounds/jidaraku/03_conbini/ に入れる。届くまでは手もちの背景で代わりにする
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "03_conbini"))
OFFICE, STREET, SEVEN, FAMIMA, LAWSON, ROOM_N, TABLE, ROOM_LATE, ROOM_M, TRASH = (
    "c01_office_night", "c02_night_street", "c03_seven", "c04_famima", "c05_lawson", "c06_room_night", "c07_room_table",
    "c08_room_late", "c09_room_morning", "c10_trash")
J.STANDIN.update({OFFICE: "bg25_office_desk", STREET: "bg51_night_street", SEVEN: "bg15_convenience", FAMIMA: "bg16_food_aisle",
                  LAWSON: "bg12_liquor_shelf", ROOM_N: "bg14_home_night", TABLE: "bg14_home_night", ROOM_LATE: "bg14_home_night",
                  ROOM_M: "bg02_room", TRASH: "bg02_room"})
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
CATLIFE = os.path.join(L.BGM, "nc102462_Cat_life.mp3")
LETTER = os.path.join(L.BGM, "手紙のさよなら.mp3")


def cuts():
    s = J.line
    return [
        # ---- 会社 ----
        s(OFFICE, "work_typing_cat", "金曜の夜8時。\nやっと仕事が終わった。", bgm={"file": L.NORA, "gain": -12}),
        s(OFFICE, "sulk_hungry_cat", "今週もよく働いた。"),
        s(OFFICE, "talk_orange_white_sitting_cat", "後輩が\n飲み会に誘ってくれた。"),
        s(OFFICE, "calmdown_dancing_cat", "「今日は\nえんりょしとくよ。」"),
        s(OFFICE, "sleepy_old_memories_cat", "気をつかう飲み会より\nひとりの家飲みだ。"),
        s(OFFICE, "blank_black_cat_zoning_out", "晩ごはんを\n作る気力はない。"),
        s(OFFICE, "think_bike_front_seat_cat", "外食するのも\nめんどうだ。"),
        s(OFFICE, "realize_wet_cat_stare", "俺は30代、独身。\n家で待つ人はいない。"),
        s(OFFICE, "rizz_cat_rizz", "ならば今夜は\n好きなものだけ食べる。"),
        s(OFFICE, "excited_hodomoe_city_cat", "「コンビニで\n家飲みだ！」", se="pikon"),
        s(OFFICE, "work_dog_staring_computer", "帰りの電車で\nコンビニのアプリを開く。"),
        s(OFFICE, "stare_big_eyes_tabby_kitten", "クーポンが3枚。\nこれは行けという合図だ。"),
        # ---- 1軒目 セブン ----
        s(STREET, "leave_cat_leaves_home", "駅を出て\n帰り道を歩く。"),
        s(STREET, "peek_what_happen_cat", "最初に見えたのは\nセブン-イレブン。"),
        s(SEVEN, "stare_interviewer_cat", "「いらっしゃいませー」", se="pinpon_notice"),
        s(SEVEN, "read_book_orange_kitten", "まずはお酒コーナー。\nハイボール缶を2本。"),
        s(SEVEN, "think_bike_front_seat_cat", "……いや、\nレモンサワーも1本。"),
        s(SEVEN, "stare_big_eyes_tabby_kitten", "レジ横の\nホットスナックが光っている。"),
        s(SEVEN, "showoff_gojo_cosplay_cat", "「ななチキと\nからあげ棒ください。」"),
        s(SEVEN, "money_counting_orange_cat", "おでんのいい香り。\n大根とたまごも頼む。"),
        s(SEVEN, "cocky_dj_cat", "お菓子の棚で\nピザポテトもかごへ。"),
        s(SEVEN, "peek_what_happen_cat", "冷凍コーナーで\nセブンプレミアムの餃子。"),
        s(SEVEN, "think_bike_front_seat_cat", "フライパンいらずで\n焼けるやつだ。"),
        s(SEVEN, "stare_interviewer_cat", "「袋はご利用ですか？」"),
        s(SEVEN, "showoff_gojo_cosplay_cat", "「大きいのでお願いします。」"),
        s(SEVEN, "realize_wet_cat_stare", "これで十分だ。\n……と思っていた。"),
        # ---- 2軒目 ファミマ ----
        s(STREET, "calmdown_dancing_cat", "袋をさげて\n歩いていると。"),
        s(STREET, "surprise_big_pupils_cat", "50メートル先に\nファミリーマート。"),
        s(FAMIMA, "peek_what_happen_cat", "「ファミチキは\nここでしか買えない……」"),
        s(FAMIMA, "angry_aiming_cat", "吸いこまれるように\n入っていた。", se="store_famima_entry_chime_arrive_welcome"),
        s(FAMIMA, "yell_orange_fat_cat", "「ファミチキ\nひとつ！」", se="jan"),
        s(FAMIMA, "stare_tabby_wide_eyes_cat", "……いや、\n「ふたつで！」"),
        s(FAMIMA, "dance_wop_cat", "ついでに\nカップ焼きそばのペヤング。"),
        s(FAMIMA, "happy_girlfriend_dance_cat", "シメのために\nカップヌードルも。"),
        s(FAMIMA, "laugh_laughing_dog", "シメが2つ。\nでも金曜だからいい。"),
        s(FAMIMA, "stare_big_eyes_tabby_kitten", "ファミマ限定の\nお菓子も目に入る。"),
        s(FAMIMA, "cocky_dj_cat", "限定に弱い。\nそれが俺だ。"),
        # ---- 3軒目 ローソン ----
        s(STREET, "sleepy_old_memories_cat", "家の前の角に\nローソンがある。"),
        s(STREET, "think_bike_front_seat_cat", "ここで\n素通りできるだろうか。"),
        s(LAWSON, "showoff_gojo_cosplay_cat", "できなかった。", se="pinpon_notice"),
        s(LAWSON, "stare_big_eyes_tabby_kitten", "からあげクンの\nレッドを買う。"),
        s(LAWSON, "rizz_cat_rizz", "からあげは\nもう3種類目だ。"),
        s(LAWSON, "happy_chipi_chapa_cat", "スイーツ棚には\nプレミアムロールケーキ。"),
        s(LAWSON, "excited_hodomoe_city_cat", "「デザートは\n別腹って言うしな。」"),
        s(LAWSON, "money_counting_orange_cat", "レシートが\n3枚になった。"),
        # ---- 家で家飲み ----
        s(ROOM_N, "dance_tabby_standing_cat", "家に着いた。\n袋が指にくいこむ。", bgm={"file": L.PURPLE, "gain": -12, "fade": 0.8}),
        s(TABLE, "dance_three_kittens", "テーブルに\n全部ならべてみる。"),
        s(ROOM_N, "work_typing_cat", "先に餃子を\nフライパンで焼く。"),
        s(ROOM_N, "fight_cat_fight", "パチパチと\n油がはねる。", se="explosion_doon"),
        s(ROOM_N, "confused_i_dont_know_cat", "「あつっ！\n手にはねた！」"),
        s(TABLE, "surprise_big_pupils_cat", "……ちょっとした\nパーティーだ。"),
        s(TABLE, "showoff_gojo_cosplay_cat", "でも参加者は\n俺ひとり。"),
        s(TABLE, "work_dog_staring_computer", "好きな動画を\nテレビに映す。"),
        s(TABLE, "yell_orange_fat_cat", "プシュッ。\n「かんぱーい！」", se="tereterere"),
        s(TABLE, "eat_pop_cat", "ハイボールをひと口。\n仕事の疲れがとける。"),
        s(TABLE, "eat_crunchy_cat_luna", "まずはファミチキ。\nかじるとジュワッと肉汁。"),
        s(TABLE, "happy_chipi_chapa_cat", "「ファミチキ\nやっぱうめぇ！」", se="pinpoon_correct"),
        s(TABLE, "dance_koto_nai_cat", "ここで俺の\nスイッチが入った。"),
        s(TABLE, "cocky_dj_cat", "ななチキとからあげクンを\n食べくらべる。"),
        s(TABLE, "rage_talking_cat", "「どれもうまい。\n優勝が決められない。」"),
        s(TABLE, "dance_edm_cat", "からあげ棒を\nハイボールで流しこむ。"),
        s(TABLE, "dance_wop_cat", "おでんの大根に\nからしをつける。"),
        s(TABLE, "sleepy_old_memories_cat", "「しみてる……\n冬の味だ。」"),
        s(TABLE, "happy_hamster_open_arms", "2本目のハイボール。\nピザポテトも開ける。"),
        s(TABLE, "laugh_laughing_dog", "動画を見ながら\nひとりで笑う。"),
        s(TABLE, "dance_maxwell_cat", "楽しい。\n今夜の俺は自由だ。"),
        s(TABLE, "eat_crunchy_cat_luna", "餃子もパリッと\n焼けている。"),
        s(TABLE, "yell_orange_fat_cat", "「コンビニの餃子、\n店レベルじゃん！」"),
        s(TABLE, "work_dog_staring_computer", "写真をとって\nSNSに上げる。"),
        s(TABLE, "dance_three_kittens", "「#金曜の家飲み」"),
        s(TABLE, "peek_what_happen_cat", "いいねは2つ。\nでも気にしない。"),
        # ---- 夜中 ----
        s(ROOM_LATE, "stare_tabby_wide_eyes_cat", "気づけば夜中の1時。", se="pi", bgm={"file": LOFI, "gain": -14, "fade": 1.0}),
        s(ROOM_LATE, "confused_i_dont_know_cat", "テーブルの上は\nからっぽの容器だらけ。"),
        s(ROOM_LATE, "think_bike_front_seat_cat", "でも残っているものがある。"),
        s(ROOM_LATE, "peek_what_happen_cat", "ペヤングと\nカップヌードル。"),
        s(ROOM_LATE, "rizz_cat_rizz", "「シメを食べないと\n終われない。」"),
        s(ROOM_LATE, "work_typing_cat", "お湯をわかす。"),
        s(ROOM_LATE, "stare_big_eyes_tabby_kitten", "夜中の\nカップ麺のにおいは犯罪だ。"),
        s(ROOM_LATE, "eat_pop_cat", "ペヤングをすする。\nソースが濃い。"),
        s(ROOM_LATE, "sulk_hungry_cat", "あれ……\nお腹がいっぱいだ。"),
        s(ROOM_LATE, "despair_dramatic_kitten", "でもカップヌードルは\nもうお湯を入れてしまった。"),
        s(ROOM_LATE, "realize_wet_cat_stare", "お湯を入れたら\n食べるしかない。"),
        s(ROOM_LATE, "sad_banana_cat_cry", "スープまで\n飲みほしてしまった。"),
        s(ROOM_LATE, "blank_black_cat_zoning_out", "最後に\nプレミアムロールケーキ。"),
        s(ROOM_LATE, "eat_crunchy_cat_luna", "ふわふわのクリーム。\nやさしい甘さだ。"),
        s(ROOM_LATE, "sleepy_sleepy_cat", "やさしくないのは\n今の胃の状態だ。"),
        s(ROOM_LATE, "sulk_hungry_cat", "冷蔵庫を開ける。\nもう何も入らない体なのに。"),
        s(ROOM_LATE, "blank_black_cat_zoning_out", "歯みがきをしようと\n思っていた。"),
        s(ROOM_LATE, "sleep_sleeping_cat", "そのまま\nソファで寝落ちした。"),
        # ---- 次の日 ----
        s(ROOM_M, "sleepy_old_memories_cat", "土曜の朝。", se="cuckoo_pappo", bgm={"file": LETTER, "gain": -14, "fade": 1.0}),
        s(ROOM_M, "stare_tabby_wide_eyes_cat", "鏡を見る。"),
        s(ROOM_M, "surprise_big_pupils_cat", "顔がパンパンに\nむくんでいる。", se="question_mark_pop_confused_huh"),
        s(ROOM_M, "despair_dramatic_kitten", "「誰だこれ……」"),
        s(ROOM_M, "sulk_hungry_cat", "胃が重い。\nのどが乾く。"),
        s(ROOM_M, "eat_pop_cat", "水をがぶ飲みする。"),
        s(ROOM_M, "slack_nail_filing_cat", "体重計に乗ってみる。"),
        s(ROOM_M, "despair_dramatic_kitten", "……1.5キロ増えている。", se="question_mark_pop_confused_huh"),
        s(ROOM_M, "realize_wet_cat_stare", "ほとんど\nむくみだと信じたい。"),
        s(TRASH, "confused_i_dont_know_cat", "テーブルを見る。"),
        s(TRASH, "blank_black_cat_zoning_out", "空き缶4本。\nからあげの袋が4つ。"),
        s(TRASH, "sulk_hungry_cat", "カップ麺の容器が2つ。\nお菓子の袋。"),
        s(TRASH, "money_counting_orange_cat", "レシート3枚を\n合計してみる。"),
        s(TRASH, "stare_tabby_wide_eyes_cat", "……外食したほうが\n安かったかもしれない。"),
        s(TRASH, "glare_disgusted_cat", "ゴミ袋がひとつ\nいっぱいになった。"),
        s(TRASH, "think_bike_front_seat_cat", "燃えるゴミの日は\n火曜日。"),
        s(TRASH, "sleepy_old_memories_cat", "それまで\nこの袋と暮らす。"),
        s(TRASH, "work_typing_cat", "フライパンと\nお皿を洗う。"),
        s(TRASH, "sad_black_dog", "家飲みは\n片づけまでが家飲みだ。"),
        s(TRASH, "sad_banana_cat_cry", "「もうしばらく\nコンビニはいい……」"),
        s(ROOM_M, "sleep_sleeping_cat", "昼まで\nもう一度寝る。"),
        # ---- 夕方 ----
        s(ROOM_M, "sleepy_sleepy_cat", "夕方。\nやっと胃が落ち着いてきた。", bgm={"file": CATLIFE, "gain": -12, "fade": 1.0}),
        s(ROOM_M, "eat_crunchy_cat_luna", "晩ごはんは\nおかゆと味噌汁にした。"),
        s(ROOM_M, "realize_wet_cat_stare", "やさしい味が\n体にしみる。"),
        s(ROOM_M, "slack_nail_filing_cat", "なんとなく\nスマホを見る。"),
        s(ROOM_M, "stare_big_eyes_tabby_kitten", "コンビニの\n新作スイーツの記事が流れてきた。"),
        s(ROOM_M, "peek_what_happen_cat", "今週の新作。\n期間限定。"),
        s(ROOM_M, "think_bike_front_seat_cat", "期間限定……\nつまり今しかない。"),
        s(ROOM_M, "realize_wet_cat_stare", "昨日の\n「しばらくいい」は\nどこへ行ったのか。"),
        s(ROOM_M, "rizz_cat_rizz", "「スイーツ1個だけ。\n今日は1軒だけ。」"),
        s(ROOM_M, "excited_hodomoe_city_cat", "「お酒は\nほどほどにしよう。」", se="pikon"),
        s(ROOM_M, "dance_tabby_standing_cat", "俺はサンダルを\nつっかけた。", dur=3.4),
        J.end_card(),
    ]


if __name__ == "__main__":
    J.run(cuts(), os.path.join(J.HERE, "out", "jidaraku_03_conbini.mp4"), os.path.join(J.HERE, "out", "jidaraku_03_conbini_preview"))
