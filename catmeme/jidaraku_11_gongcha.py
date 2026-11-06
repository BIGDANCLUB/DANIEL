"""自堕落シリーズ #11：30代独身男、1人でゴンチャ（タピオカデビュー）（11/6 ユーザー指定：候補8番・精一杯慌てて変な頼み方をする）。約8分。

python3 catmeme/jidaraku_11_gongcha.py → out/jidaraku_11_gongcha.mp4
- 流れ：休日の昼にSNSでタピオカ → 30代男は飲んだことがない → 店の前で3往復 → 注文はお茶・サイズ・甘さ・氷・トッピングを選ぶ →
  うしろに列ができて大あわて → 変な頼み方（店員さんがやさしく助けてくれる）→ 太いストロー・もちもち → 2杯目でリベンジ → 帰り道
- 店や店員さんをけなさない（慌てるのは本人だけ）。メニューの細かい数字は出さない
- ベンチマーク3チャンネルにゴンチャ・タピオカの回はない（11/6 確認）
- 写真がない場面は字幕だけ（写真が届いたら backgrounds/jidaraku/11_gongcha に置く）。ほかの店の写真は使わない
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "11_gongcha"))
ROOM, FRONT, IN, SEAT, STREET, ROOM_N = ("j01_room", "g01_front", "g02_counter", "g03_seat", "bg48_clean_street", "j07_room_night")
J.STANDIN.update({FRONT: "bg48_clean_street", IN: "bg20_counter", SEAT: "bg20_counter"})
# 仮の背景のある場所（ほかの店の写真は使わない。j01_room は自堕落シリーズの部屋）
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in (os.path.join("jidaraku", "01_yakiniku"), "03_kodomo_nisa", "14_japan", "16_tenchim")]
J.HOLD = 3
J.SUB_STYLE = "glow"
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
MENU, MILK, FOAM = "f_menu", "f_milktea", "f_foam"


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 休日 ----
        s(ROOM, "sleep_sleeping_cat", "土曜日の昼12時\n目が覚めた", bgm={"file": MORNING, "gain": -12}),
        s(ROOM, "blank_black_cat_zoning_out", "予定はない"),
        s(ROOM, "scream_phone_orange_cat", "ベッドの上で\nSNSを見る"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "流れてくるのは\nタピオカの写真"),
        s(ROOM, "dance_three_kittens", "若い子たちが\n楽しそうに飲んでいる"),
        s(ROOM, "think_chin_paw_orange_cat", "そういえば俺"),
        s(ROOM, "sad_looking_away_tabby", "タピオカを\n飲んだことがない"),
        s(ROOM, "sleepy_old_memories_cat", "ブームのころは\nどこも大行列だった"),
        s(ROOM, "calm_black_face_sheep", "男1人で\nあの列に並ぶ勇気は\nなかった"),
        s(ROOM, "stare_lying_tabby_cat", "そのまま\n何年もたった"),
        s(ROOM, "realize_wet_cat_stare", "気がつけば\n30代だ"),
        s(ROOM, "think_bike_front_seat_cat", "今なら\n空いているかもしれない"),
        s(ROOM, "angry_aiming_cat", "30代独身男\nタピオカデビュー"),
        s(ROOM, "excited_hodomoe_city_cat", "今日だ", se="shine_kiraan_maou"),
        # ---- 出発 ----
        s(ROOM, "work_typing_cat", "まずは\n着ていく服を選ぶ"),
        s(ROOM, "stare_lying_tabby_cat", "クローゼットには\nグレーのパーカーが3枚"),
        s(ROOM, "calm_black_face_sheep", "どれも同じだ"),
        s(ROOM, "think_chin_paw_orange_cat", "いちばん\n新しく見えるやつにする"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "鏡を見る"),
        s(ROOM, "sad_black_dog", "どう見ても\n休日の30代だ"),
        s(ROOM, "rizz_cat_rizz", "帽子をかぶって\nごまかす"),
        s(ROOM, "read_book_orange_kitten", "地図アプリで\nいちばん近い店をさがす"),
        s(ROOM, "surprise_big_pupils_cat", "駅前にあった"),
        s(ROOM, "huh_huh_cat", "毎日通っている道だ"),
        s(ROOM, "sleepy_old_memories_cat", "何年も\n前を通りすぎていた"),
        s(ROOM, "leave_cat_leaves_home", "家を出る", se="whoosh_shu"),
        # ---- 店の前 ----
        s(FRONT, "leave_cat_leaves_home", "駅前の\nゴンチャ", se="whoosh_shu", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(FRONT, "surprise_big_pupils_cat", "おしゃれだ"),
        s(FRONT, "stare_interviewer_cat", "高校生のグループ\nカップル"),
        s(FRONT, "sad_black_dog", "30代の男は\n俺だけだ"),
        s(FRONT, "stare_lying_tabby_cat", "入口の前を\n3往復する"),
        s(FRONT, "ignore_orange_cat_sniffed", "通りすがりの人に\n見られている気がする"),
        s(FRONT, "think_chin_paw_orange_cat", "いや\n誰も見ていない"),
        s(FRONT, "rizz_cat_rizz", "タピオカは\nみんなのものだ"),
        s(FRONT, "yell_orange_fat_cat", "行くぞ", se="gong_match_start"),
        # ---- 注文 ----
        s(IN, "stare_interviewer_cat", "いらっしゃいませー\nご注文お決まりでしたら\nどうぞー", se="pinpon_notice", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(IN, "surprise_big_pupils_cat", "もう\n俺の番だ"),
        s(IN, "stare_big_eyes_tabby_kitten", "メニューを見る", item=MENU),
        s(IN, "huh_huh_cat", "お茶の種類が\nたくさんある", item=MENU),
        s(IN, "confused_i_dont_know_cat", "ミルクティー\nフルーツティー\nミルクフォーム", item=MENU),
        s(IN, "read_book_orange_kitten", "ここは\nお茶を選んでから\n自分好みにできる店", item=MENU),
        s(IN, "think_chin_paw_orange_cat", "サイズを選んで", item=MENU),
        s(IN, "think_bike_front_seat_cat", "甘さを選んで", item=MENU),
        s(IN, "stare_tabby_wide_eyes_cat", "氷の量を選んで", item=MENU),
        s(IN, "calm_black_face_sheep", "トッピングを選ぶ", item=MENU),
        s(IN, "despair_dramatic_kitten", "選ぶことが\n多すぎる", item=MENU, se="pi"),
        s(IN, "peek_what_happen_cat", "うしろを見る"),
        s(IN, "scream_standing_marmot", "列が\nできている", se="explosion_chudoon"),
        s(IN, "stare_interviewer_cat", "高校生が\n5人"),
        s(IN, "sad_banana_cat_cry", "みんな\n注文が決まっている顔だ"),
        s(IN, "blank_black_cat_zoning_out", "頭が\n真っ白になる"),
        s(IN, "stare_interviewer_cat", "お飲みもの\nどうされますかー？"),
        s(IN, "work_typing_cat", "えっと\nあの……"),
        s(IN, "scream_phone_orange_cat", "タピオカを\nひとつ！", se="explosion_dokaan"),
        s(IN, "huh_goat_talks_to_huh_cat", "タピオカは\nトッピングだ", se="question_mark_pop_confused_huh"),
        s(IN, "stare_interviewer_cat", "ベースのお茶は\nどれにしますかー？"),
        s(IN, "despair_dramatic_kitten", "ベース……"),
        s(IN, "angry_shooting_cat", "ベースで\nお願いします！"),
        s(IN, "huh_huh_cat", "何を言っているんだ\n俺は"),
        s(IN, "stare_interviewer_cat", "では\nミルクティーで\nよろしいですかー？"),
        s(IN, "joy_happy_happy_happy_cat", "店員さんが\n助けてくれた"),
        s(IN, "meow_ragdoll_chubby_cat", "それで\nお願いします"),
        s(IN, "stare_interviewer_cat", "サイズは\nどうしますかー？"),
        s(IN, "angry_aiming_cat", "いちばん\n強いやつで"),
        s(IN, "stare_tabby_wide_eyes_cat", "サイズに\n強さはない"),
        s(IN, "stare_interviewer_cat", "甘さは\nどうしますかー？"),
        s(IN, "scream_phone_orange_cat", "ぜ……\n全部で！"),
        s(IN, "huh_huh_cat", "甘さを全部\nとは"),
        s(IN, "stare_interviewer_cat", "氷の量は\nどうしますかー？"),
        s(IN, "yell_orange_fat_cat", "氷……\nあります！", se="explosion_chudoon"),
        s(IN, "despair_dramatic_kitten", "質問に\n答えていない"),
        s(IN, "stare_interviewer_cat", "ふつうで\nよろしいですかー？"),
        s(IN, "sad_banana_cat_cry", "ふつうで\nお願いします……"),
        s(IN, "stare_interviewer_cat", "トッピングは\nいかがですかー？"),
        s(IN, "blank_black_cat_zoning_out", "トッピングを……"),
        s(IN, "angry_shooting_cat", "トッピングで！", se="explosion_dokaan"),
        s(IN, "huh_goat_talks_to_huh_cat", "もう\n言葉が出てこない", se="question_mark_pop_confused_huh"),
        s(IN, "stare_interviewer_cat", "タピオカで\nよろしいですかー？"),
        s(IN, "happy_hamster_open_arms", "それです！\nそれが言いたかった！"),
        s(IN, "peek_what_happen_cat", "うしろの高校生が\nちょっと笑っている"),
        s(IN, "sad_looking_away_tabby", "汗が止まらない"),
        s(IN, "stare_interviewer_cat", "ミルクティー\n甘さふつう\n氷ふつう\nタピオカでーす"),
        s(IN, "realize_wet_cat_stare", "全部ふつうに\nなっている"),
        s(IN, "joy_happy_happy_happy_cat", "店員さんが\nふつうに\n直してくれた"),
        s(IN, "money_counting_orange_cat", "お会計をして\nレシートを受け取る"),
        s(IN, "calm_black_face_sheep", "番号で\n呼ばれるらしい"),
        s(IN, "stare_lying_tabby_cat", "すみっこで\n小さくなって待つ"),
        # ---- 受け取り ----
        s(IN, "peek_what_happen_cat", "カウンターの奥で\nお茶をシャカシャカ\nふっている", item=MILK),
        s(IN, "surprise_big_pupils_cat", "1杯ずつ\n作っているのか", item=MILK),
        s(IN, "stare_interviewer_cat", "高校生が\n次々と受け取っていく", item=MILK),
        s(IN, "think_chin_paw_orange_cat", "みんな\n迷いがない", item=MILK),
        s(IN, "sad_looking_away_tabby", "俺より\nずっと先輩だ", item=MILK),
        s(IN, "stare_lying_tabby_cat", "レシートの番号を\n10回見る", item=MILK),
        s(IN, "blank_black_cat_zoning_out", "まだかな", item=MILK),
        s(IN, "stare_interviewer_cat", "お待たせしましたー！", se="pinpon_notice", item=MILK),
        s(IN, "surprise_big_pupils_cat", "来た", item=MILK),
        s(IN, "stare_big_eyes_tabby_kitten", "カップの底に\n黒い粒が\nしずんでいる", item=MILK),
        s(IN, "showoff_gojo_cosplay_cat", "これが\nタピオカ", item=MILK, se="gong_dora_jaan"),
        s(IN, "huh_huh_cat", "ストローが\n太い", item=MILK),
        s(IN, "think_chin_paw_orange_cat", "ふたが\nフィルムでとじてある", item=MILK),
        s(IN, "confused_i_dont_know_cat", "これ\nどこに刺すんだ", item=MILK),
        s(IN, "peek_what_happen_cat", "となりの高校生を\nこっそり見る", item=MILK),
        s(IN, "angry_shooting_cat", "ストローを\n真上から\n一気に刺す", item=MILK, se="explosion_chudoon"),
        s(IN, "joy_happy_happy_happy_cat", "刺さった", item=MILK),
        s(IN, "happy_chipi_chapa_cat", "まるで\n剣を抜いた勇者", item=MILK),
        # ---- 初タピオカ ----
        s(SEAT, "work_typing_cat", "窓ぎわの席に座る", item=MILK, bgm={"file": PASTEL, "gain": -12}),
        s(SEAT, "stare_tabby_wide_eyes_cat", "いざ", item=MILK),
        s(SEAT, "eat_crunchy_cat_luna", "ズズッ", item=MILK, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "surprise_big_pupils_cat", "タピオカが\n一気に\n口に飛びこんでくる", item=MILK),
        s(SEAT, "scream_standing_marmot", "いきおいが\nすごい", item=MILK),
        s(SEAT, "eat_pop_cat", "もちもち", item=MILK),
        s(SEAT, "happy_girlfriend_dance_cat", "もちもちもちもち", item=MILK),
        s(SEAT, "realize_wet_cat_stare", "お茶が\nちゃんとおいしい", item=MILK),
        s(SEAT, "read_book_orange_kitten", "ミルクティーの\n香りが強い", item=MILK),
        s(SEAT, "happy_hamster_open_arms", "甘さもふつうで\nちょうどいい", item=MILK),
        s(SEAT, "sad_banana_cat_cry", "全部で\nと言わなくてよかった", item=MILK),
        s(SEAT, "sleepy_old_memories_cat", "あのころ\n並ばなかった俺に\n教えてあげたい", item=MILK),
        s(SEAT, "dance_wop_cat", "タピオカは\nおいしい", item=MILK),
        s(SEAT, "stare_big_eyes_tabby_kitten", "まわりを見る", item=MILK),
        s(SEAT, "dance_three_kittens", "高校生たちは\n写真を撮っている", item=MILK),
        s(SEAT, "think_chin_paw_orange_cat", "俺も撮るか", item=MILK),
        s(SEAT, "work_typing_cat", "カップを持って\nカシャッ", item=MILK, se="pikon"),
        s(SEAT, "calm_black_face_sheep", "写真に\nパーカーの袖が写っている", item=MILK),
        s(SEAT, "sad_black_dog", "送る相手もいない", item=MILK),
        s(SEAT, "happy_hamster_open_arms", "自分のために\n保存しておく", item=MILK),
        s(SEAT, "eat_crunchy_cat_luna", "ズズッ\nもちもち", item=MILK),
        s(SEAT, "think_chin_paw_orange_cat", "飲みものなのに\nかんでいる", item=MILK),
        s(SEAT, "huh_huh_cat", "これは\n飲みものなのか\n食べものなのか", item=MILK),
        s(SEAT, "calm_black_face_sheep", "あごが\n少しつかれてきた", item=MILK),
        s(SEAT, "stare_lying_tabby_cat", "30代のあごには\nちょうどいい運動だ", item=MILK),
        s(SEAT, "stare_big_eyes_tabby_kitten", "……あれ", item=MILK),
        s(SEAT, "despair_dramatic_kitten", "お茶がなくなった", item=MILK, se="pi"),
        s(SEAT, "peek_what_happen_cat", "タピオカだけ\n底に残っている", item=MILK),
        s(SEAT, "angry_aiming_cat", "吸っても\n吸っても\n上がってこない", item=MILK),
        s(SEAT, "yell_orange_fat_cat", "ズゴゴゴゴ", item=MILK, se="explosion_dokaan"),
        s(SEAT, "sad_looking_away_tabby", "店じゅうに\nひびく音", item=MILK),
        s(SEAT, "stare_interviewer_cat", "高校生が\nこっちを見ている", item=MILK),
        s(SEAT, "meow_ragdoll_chubby_cat", "カップをふって\n1粒ずつ救出する", item=MILK),
        s(SEAT, "read_book_orange_kitten", "お茶とタピオカは\n同じペースで\n飲むものらしい", item=MILK),
        s(SEAT, "realize_wet_cat_stare", "人生と同じだ", item=MILK),
        # ---- リベンジ ----
        s(SEAT, "think_bike_front_seat_cat", "このままでは\n帰れない"),
        s(SEAT, "angry_shooting_cat", "2杯目で\nリベンジだ", se="gong_match_start"),
        s(SEAT, "read_book_orange_kitten", "スマホで\n頼み方を予習する"),
        s(SEAT, "think_chin_paw_orange_cat", "お茶\nサイズ\n甘さ\n氷\nトッピング"),
        s(SEAT, "work_typing_cat", "メモアプリに書く"),
        s(SEAT, "stare_big_eyes_tabby_kitten", "口に出して\n3回練習する"),
        s(IN, "stare_interviewer_cat", "いらっしゃいませー", se="pinpon_notice", item=MENU),
        s(IN, "surprise_big_pupils_cat", "さっきの\n店員さんだ", item=MENU),
        s(IN, "sad_black_dog", "覚えられている\n気がする", item=MENU),
        s(IN, "rizz_cat_rizz", "だが今の俺は\nさっきの俺じゃない", item=MENU),
        s(IN, "cocky_dj_cat", "ミルクフォームの\nお茶を\nMサイズで", item=MENU),
        s(IN, "smug_squint_bicolor_cat", "甘さひかえめ\n氷少なめ", item=MENU),
        s(IN, "showoff_gojo_cosplay_cat", "タピオカ\nトッピングで", item=MENU, se="gong_dora_jaan"),
        s(IN, "stare_interviewer_cat", "かしこまりましたー！", item=MENU),
        s(IN, "joy_happy_happy_happy_cat", "言えた", item=MENU),
        s(IN, "happy_hamster_open_arms", "全部\n言えた", item=MENU),
        s(IN, "dance_happy_banana_cat", "心の中で\nガッツポーズ", item=MENU),
        s(IN, "stare_interviewer_cat", "お待たせしましたー！", se="pinpon_notice", item=FOAM),
        s(SEAT, "stare_big_eyes_tabby_kitten", "上に白い\nミルクフォーム", item=FOAM),
        s(SEAT, "eat_crunchy_cat_luna", "ひと口", item=FOAM, se="drink_gulp_gokugoku_thirsty_chug"),
        s(SEAT, "surprise_big_pupils_cat", "ふわっと\nしょっぱい", item=FOAM),
        s(SEAT, "realize_wet_cat_stare", "そのあとに\nお茶が来る", item=FOAM),
        s(SEAT, "happy_girlfriend_dance_cat", "甘いとしょっぱいの\n往復", item=FOAM),
        s(SEAT, "eat_pop_cat", "そして\nもちもち", item=FOAM),
        s(SEAT, "excited_hodomoe_city_cat", "うまい", item=FOAM, se="explosion_dokaan"),
        s(SEAT, "read_book_orange_kitten", "今度は\nお茶とタピオカを\n同じペースで", item=FOAM),
        s(SEAT, "peek_what_happen_cat", "となりの席の高校生が\nこっちを見る", item=FOAM),
        s(SEAT, "stare_interviewer_cat", "おじさん\nさっきの人だ", item=FOAM),
        s(SEAT, "despair_dramatic_kitten", "バレていた", item=FOAM, se="pi"),
        s(SEAT, "stare_interviewer_cat", "それ\nおいしいですよね", item=FOAM),
        s(SEAT, "surprise_big_pupils_cat", "話しかけられた", item=FOAM),
        s(SEAT, "meow_ragdoll_chubby_cat", "おいしいです……", item=FOAM),
        s(SEAT, "happy_chipi_chapa_cat", "タピオカが\n世代をこえて\nつないでくれた", item=FOAM),
        s(SEAT, "calmdown_dancing_cat", "最後の1粒まで\n静かに完飲", item=FOAM),
        s(SEAT, "happy_chipi_chapa_cat", "成長した", item=FOAM),
        # ---- 帰り道 ----
        s(STREET, "leave_cat_leaves_home", "店を出る", se="whoosh_shu", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(STREET, "sleepy_old_memories_cat", "夕方の風が\n気持ちいい"),
        s(STREET, "think_chin_paw_orange_cat", "タピオカは\n若者のものだと\n思っていた"),
        s(STREET, "happy_hamster_open_arms", "でも\n30代の休日にも\nちゃんとやさしかった"),
        s(STREET, "stare_interviewer_cat", "駅前で\n高校生とすれちがう"),
        s(STREET, "peek_what_happen_cat", "みんな手に\nタピオカ"),
        s(STREET, "rizz_cat_rizz", "俺も\n同じ側の人間に\nなった"),
        s(STREET, "smug_squint_bicolor_cat", "すれちがいざまに\nうなずく"),
        s(STREET, "laugh_laughing_dog", "誰も\nうなずき返さない"),
        s(STREET, "think_chin_paw_orange_cat", "スーパーで\n晩ごはんの材料を買う"),
        s(STREET, "stare_big_eyes_tabby_kitten", "飲みもの売り場に\nタピオカの\nペットボトル"),
        s(STREET, "huh_huh_cat", "家でも飲めるのか"),
        s(STREET, "calm_black_face_sheep", "でも\nあの店で\n1杯ずつ作ってもらうのが\nいいのだ"),
        s(STREET, "sleepy_sleepy_cat", "そっと\n棚にもどす"),
        s(STREET, "sad_looking_away_tabby", "最初の注文は\n忘れたい"),
        s(STREET, "huh_huh_cat", "氷……\nあります！"),
        s(STREET, "despair_dramatic_kitten", "思い出して\n顔が熱くなる"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", se="whoosh_shu"),
        s(ROOM_N, "scream_phone_orange_cat", "またSNSを見る"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "新作のお茶が\n出ているらしい"),
        s(ROOM_N, "think_bike_front_seat_cat", "メモアプリを開く"),
        s(ROOM_N, "work_typing_cat", "お茶\nサイズ\n甘さ\n氷\nトッピング"),
        s(ROOM_N, "excited_hodomoe_city_cat", "来週も行こう\nタピオカ", se="pikon", dur=3.8),
        J.end_card(),
    ]


def place(cs):
    J.auto_tempo(cs)
    for c in cs:
        if c.get("text"):
            c["text"] = c["text"].replace("「", "").replace("」", "")
    return cs


if __name__ == "__main__":
    cs = place(cuts())
    if os.environ.get("LEN"):
        print(len(cs), round(sum(c["dur"] for c in cs), 1))
    else:
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_11_gongcha.mp4"), os.path.join(J.HERE, "out", "jidaraku_11_gongcha_preview"))
