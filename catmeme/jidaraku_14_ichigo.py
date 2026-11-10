"""自堕落シリーズ #14：30代独身男、ひとりでいちご狩り（11/7 ユーザー指定・レビューを参考に8分）。

python3 catmeme/jidaraku_14_ichigo.py → out/jidaraku_14_ichigo.mp4
- 流れ：休日にSNSでいちご狩り → 30分食べ放題で元を取る作戦 → 受付で練乳 → ハウスの中は家族とカップルだらけ →
  開始・最初は勢いよく → 品種の食べくらべ・先っぽが甘い → 10分で満足してくる → 練乳で味変 → 時計がない → 最後の追い込み →
  終了・数えたら25個くらい → 直売所でパックを買う → 家でいちごミルク → 母さんからいちごの宅配便 → 食べ放題よりタダのいちごがうまかったオチ（11/8 ユーザー指定）
- 体験談（口コミ・2025〜2026年ごろ）：30分食べ放題・大人2500〜2600円ほど（農園で変わる）／食べた数は18個〜33個と人それぞれ／
  開始10分ほどでだいぶ満足してしまう／ハウスの中に時計がないので時間がわかるものを持っていく／練乳は受付で買える・つけずに食べるのもおすすめ／
  食べすぎて体調をくずす人も／収穫は12月〜5月ごろ。農園の名前は出さない
- ベンチマーク3チャンネルにいちご狩りの回はない（11/7 確認）
- 写真は backgrounds/jidaraku/14_ichigo に置く。届くまでは手もちのイラストで仮に（ほかの店の写真は使わない）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "14_ichigo"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in sorted(os.listdir(os.path.join(J.HERE, "backgrounds")))
          if os.path.isdir(os.path.join(J.HERE, "backgrounds", d)) and d != "jidaraku"]
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku", "01_yakiniku")]
ROOM, ROOM_N, ROAD, FRONT, RECEPT, HOUSE, SHOP = (
    "j01_room", "j07_room_night", "bg26_rural_road", "ic01_farm", "ic02_reception", "ic03_house", "ic04_shop")
J.STANDIN.update({RECEPT: "ic04_shop"})   # 11/10 背景4枚（ハウスの中・農園・直売所）。受付の写真がないので直売所の小屋で
J.HOLD = 4
J.LOOPS = 1   # 11/9 ユーザー指定：素材はくり返さない
J.SUB_STYLE = "glow"
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
PASTEL = os.path.join(L.BGM, "パステルハウス.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
BERRY, MILK, PACK, DRINK = "f_strawberry", "f_rennyu", "f_pack", "f_ichigo_milk"


def cuts():
    def s(*a, **k):
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 休日 ----
        s(ROOM, "sleep_sleeping_cat", "土曜日の朝9時\n目が覚めた", bgm={"file": MORNING, "gain": -12}),
        s(ROOM, "scream_phone_orange_cat", "ベッドの上で\nSNSを見る"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "流れてくるのは\n真っ赤ないちご", item=BERRY),
        s(ROOM, "dance_three_kittens", "家族やカップルが\nいちご狩りを\n楽しんでいる", item=BERRY),
        s(ROOM, "think_chin_paw_orange_cat", "そういえば俺", item=BERRY),
        s(ROOM, "sad_looking_away_tabby", "いちごを\nおなかいっぱい\n食べたことがない", item=BERRY),
        s(ROOM, "sleepy_old_memories_cat", "子どものころ\nいちごは\nごちそうだった"),
        s(ROOM, "sad_black_dog", "兄弟で\n1粒ずつ\n数えて分けた"),
        s(ROOM, "realize_wet_cat_stare", "今の俺は\n30代独身"),
        s(ROOM, "money_counting_orange_cat", "自分のお金で\n好きなだけ\n食べられる"),
        s(ROOM, "read_book_orange_kitten", "いちご狩りは\n30分食べ放題の\n農園が多い"),
        s(ROOM, "money_counting_orange_cat", "大人1人\n2500円くらい"),
        s(ROOM, "think_bike_front_seat_cat", "スーパーのいちごは\n1パック数百円"),
        s(ROOM, "angry_aiming_cat", "つまり\nたくさん食べれば\n元が取れる", se="explosion_chudoon"),
        s(ROOM, "excited_hodomoe_city_cat", "行くしかない", se="shine_kiraan_maou"),
        s(ROOM, "work_typing_cat", "近くの農園を\n予約する"),
        s(ROOM, "read_book_orange_kitten", "口コミを読む"),
        s(ROOM, "stare_tabby_wide_eyes_cat", "18個で\nおなかいっぱい\n30個食べた"),
        s(ROOM, "cocky_dj_cat", "目標は\n50個", se="gong_match_start"),
        s(ROOM, "calm_black_face_sheep", "朝ごはんは\n抜いていく"),
        s(ROOM, "think_chin_paw_orange_cat", "いちご狩りの\n服装を調べる"),
        s(ROOM, "read_book_orange_kitten", "ハウスの中は\nあたたかいので\n脱ぎやすい服で"),
        s(ROOM, "stare_lying_tabby_cat", "白い服は\nいちごの汁が\nつくのでやめよう"),
        s(ROOM, "calm_black_face_sheep", "クローゼットは\nほぼ白いシャツだ"),
        s(ROOM, "work_typing_cat", "黒いパーカーを\n発掘する"),
        s(ROOM, "leave_cat_leaves_home", "家を出る", se="whoosh_shu"),
        # ---- 農園 ----
        s(ROAD, "drive_driving_cat", "車で1時間\n郊外の農園へ", se="whoosh_shu", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(ROAD, "peek_what_happen_cat", "道ばたに\nいちごの看板が\nふえてくる"),
        s(ROAD, "happy_chipi_chapa_cat", "いちご狩り\nこちら→"),
        s(ROAD, "think_bike_front_seat_cat", "この矢印を\n信じる"),
        s(ROAD, "sleepy_old_memories_cat", "畑の中の\nまっすぐな道"),
        s(FRONT, "leave_cat_leaves_home", "農園に到着", se="gong_dora_jaan"),
        s(FRONT, "surprise_big_pupils_cat", "ビニールハウスが\nずらりとならぶ"),
        s(FRONT, "stare_interviewer_cat", "駐車場には\nミニバンがいっぱい"),
        s(FRONT, "peek_what_happen_cat", "子どもが\nはしゃいでいる"),
        s(FRONT, "stare_lying_tabby_cat", "カップルが\n手をつないでいる"),
        s(FRONT, "sad_black_dog", "30代の男1人は\n俺だけだ"),
        s(FRONT, "rizz_cat_rizz", "だが今日の俺は\nいちごを食べに\n来たのだ"),
        # ---- 受付 ----
        s(RECEPT, "stare_interviewer_cat", "いらっしゃいませー\n何名様ですかー", se="pinpon_notice", bgm={"file": NANDE, "gain": -12, "fade": 0.8}),
        s(RECEPT, "meow_ragdoll_chubby_cat", "1名です"),
        s(RECEPT, "stare_interviewer_cat", "……1名様ですねー", se="pi"),
        s(RECEPT, "huh_huh_cat", "なんだ\n今の間は"),
        s(RECEPT, "despair_dramatic_kitten", "この受付の人からの\n不審者扱いゲージが\n爆上がりしたのを\n感じる", se="explosion_chudoon"),   # 11/8 ユーザー指定
        s(RECEPT, "money_counting_orange_cat", "料金を払う"),
        s(RECEPT, "stare_interviewer_cat", "練乳は\nいかがですかー", item=MILK),
        s(RECEPT, "think_chin_paw_orange_cat", "練乳……", item=MILK),
        s(RECEPT, "read_book_orange_kitten", "口コミでは\nいちごそのものが\n甘いから\nいらないという声も", item=MILK),
        s(RECEPT, "angry_shooting_cat", "でも\n50個食べるなら\n味変は必要だ", item=MILK),
        s(RECEPT, "joy_happy_happy_happy_cat", "練乳ください", item=MILK),
        s(RECEPT, "stare_interviewer_cat", "時間は30分です\nヘタは\nこのカップに\nどうぞー"),
        s(RECEPT, "read_book_orange_kitten", "ハウスの中には\n時計がないらしい"),
        s(RECEPT, "work_typing_cat", "スマホで\nタイマーを30分"),
        s(RECEPT, "read_book_orange_kitten", "注意書きを読む"),
        s(RECEPT, "stare_tabby_wide_eyes_cat", "いちごは\nやさしく\nつみましょう"),
        s(RECEPT, "think_chin_paw_orange_cat", "つまむだけで\nとれるらしい"),
        s(RECEPT, "calm_black_face_sheep", "ひっぱると\nほかの実も\nいたむそうだ"),
        s(RECEPT, "rizz_cat_rizz", "いちごには\nやさしく"),
        s(RECEPT, "sad_black_dog", "人にも\nやさしくされたい"),
        # ---- 開始 ----
        s(HOUSE, "surprise_big_pupils_cat", "ハウスの中は\nあたたかい", bgm={"file": PASTEL, "gain": -12, "fade": 0.8}),
        s(HOUSE, "stare_big_eyes_tabby_kitten", "目の前に\n真っ赤ないちごが\nぶら下がっている", item=BERRY),
        s(HOUSE, "showoff_gojo_cosplay_cat", "いちごの宝石箱だ", item=BERRY, se="gong_dora_jaan"),
        s(HOUSE, "angry_shooting_cat", "スタート", se="gong_match_start"),
        s(HOUSE, "work_typing_cat", "1個目", item=BERRY),
        s(HOUSE, "eat_crunchy_cat_luna", "パクッ", item=BERRY, se="pikon"),
        s(HOUSE, "surprise_big_pupils_cat", "あまい", item=BERRY),
        s(HOUSE, "happy_girlfriend_dance_cat", "みずみずしい", item=BERRY),
        s(HOUSE, "realize_wet_cat_stare", "つみたての\nいちごは\nこんなに\nあたたかいのか", item=BERRY),
        s(HOUSE, "eat_pop_cat", "2個目\n3個目", item=BERRY),
        s(HOUSE, "dance_wop_cat", "4個目\n5個目", item=BERRY),
        s(HOUSE, "cocky_dj_cat", "このペースなら\n50個いける", item=BERRY),
        # ---- 食べくらべ ----
        s(HOUSE, "read_book_orange_kitten", "ハウスによって\n品種がちがうらしい", item=BERRY),
        s(HOUSE, "stare_tabby_wide_eyes_cat", "こっちは\n大きくて\n酸味がある", item=BERRY),
        s(HOUSE, "happy_chipi_chapa_cat", "こっちは\n小さいけど\nとにかく甘い", item=BERRY),
        s(HOUSE, "think_chin_paw_orange_cat", "いちごにも\n個性がある", item=BERRY),
        s(HOUSE, "read_book_orange_kitten", "いちごは\n先っぽがいちばん\n甘いらしい", item=BERRY),
        s(HOUSE, "rizz_cat_rizz", "ヘタのほうから\nかじって\n甘い先っぽで終わる", item=BERRY),
        s(HOUSE, "smug_squint_bicolor_cat", "これが\n大人のいちご狩りだ", item=BERRY),
        s(HOUSE, "peek_what_happen_cat", "となりの子どもが\nこっちを見ている", item=BERRY),
        s(HOUSE, "stare_interviewer_cat", "おじさん\nいっぱい食べるね", item=BERRY),
        s(HOUSE, "sad_looking_away_tabby", "おじさん……", item=BERRY),
        s(HOUSE, "calmdown_dancing_cat", "大人の余裕で\nうなずく", item=BERRY),
        s(HOUSE, "eat_crunchy_cat_luna", "10個目\n11個目", item=BERRY),
        s(HOUSE, "dance_edm_cat", "12個目\n13個目\n14個目", item=BERRY),
        s(HOUSE, "stare_big_eyes_tabby_kitten", "葉っぱのうしろに\nかくれている\nいちごを見つける", item=BERRY),
        s(HOUSE, "happy_hamster_open_arms", "宝さがしみたいだ", item=BERRY),
        s(HOUSE, "surprise_big_pupils_cat", "白い花も\n咲いている", item=BERRY),
        s(HOUSE, "read_book_orange_kitten", "花が終わると\nいちごになるらしい", item=BERRY),
        s(HOUSE, "sleepy_old_memories_cat", "いちごにも\n青春があった", item=BERRY),
        s(HOUSE, "peek_what_happen_cat", "ハチが\n飛んでいる", item=BERRY),
        s(HOUSE, "scream_standing_marmot", "ハチ!?", item=BERRY, se="explosion_chudoon"),
        s(HOUSE, "read_book_orange_kitten", "花粉を運ぶために\n農園でかっている\nハチらしい", item=BERRY),
        s(HOUSE, "calmdown_dancing_cat", "おどかさなければ\n大丈夫", item=BERRY),
        s(HOUSE, "calm_black_face_sheep", "ハチも\n仕事中だ", item=BERRY),
        # ---- 10分 ----
        s(HOUSE, "stare_tabby_wide_eyes_cat", "タイマーを見る", se="pi"),
        s(HOUSE, "surprise_big_pupils_cat", "まだ10分", se="explosion_chudoon"),
        s(HOUSE, "blank_black_cat_zoning_out", "……あれ"),
        s(HOUSE, "despair_dramatic_kitten", "おなかが\nちょっと\nいっぱいだ"),
        s(HOUSE, "read_book_orange_kitten", "口コミにも\nあった", item=BERRY),
        s(HOUSE, "realize_wet_cat_stare", "開始10分で\nだいぶ満足して\nしまうと", item=BERRY),
        s(HOUSE, "sad_black_dog", "いちごは\nほとんど水分だ", item=BERRY),
        s(HOUSE, "huh_huh_cat", "俺は今\n水を食べている", item=BERRY, se="question_mark_pop_confused_huh"),
        s(HOUSE, "think_bike_front_seat_cat", "だが\nまだ20分ある"),
        s(HOUSE, "angry_aiming_cat", "ここで\n練乳の出番だ", item=MILK, se="gong_match_start"),
        # ---- 練乳 ----
        s(HOUSE, "work_typing_cat", "いちごの先に\n練乳をたっぷり", item=MILK),
        s(HOUSE, "eat_crunchy_cat_luna", "パクッ", item=MILK, se="pikon"),
        s(HOUSE, "happy_girlfriend_dance_cat", "あまい\nあますぎる", item=MILK),
        s(HOUSE, "joy_happy_happy_happy_cat", "いちごミルクが\n口の中でできた", item=MILK),
        s(HOUSE, "eat_pop_cat", "15個目\n16個目", item=MILK),
        s(HOUSE, "stare_big_eyes_tabby_kitten", "……あれ", item=MILK),
        s(HOUSE, "sad_looking_away_tabby", "練乳が\nいちごより先に\nなくなった", item=MILK),
        s(HOUSE, "realize_wet_cat_stare", "練乳の配分を\nまちがえた", item=MILK),
        s(HOUSE, "sleepy_old_memories_cat", "人生も\n配分が大事だ", item=MILK),
        s(HOUSE, "think_chin_paw_orange_cat", "ここからは\nいちごそのものと\n向き合う", item=BERRY),
        s(HOUSE, "read_book_orange_kitten", "口コミの言うとおり\n練乳なしでも\nちゃんと甘い", item=BERRY),
        s(HOUSE, "eat_crunchy_cat_luna", "17個目\n18個目", item=BERRY),
        s(HOUSE, "think_chin_paw_orange_cat", "カップのヘタを\nのぞく", item=BERRY),
        s(HOUSE, "stare_tabby_wide_eyes_cat", "思ったより\n少ない", item=BERRY),
        s(HOUSE, "despair_dramatic_kitten", "ペースが\n落ちている", item=BERRY),
        s(HOUSE, "angry_aiming_cat", "小さいいちごを\n選ぶ作戦に\n切りかえる", item=BERRY),
        s(HOUSE, "smug_squint_bicolor_cat", "数で\n勝負だ", item=BERRY),
        # ---- 時計がない ----
        s(HOUSE, "peek_what_happen_cat", "ハウスの中を\n見わたす"),
        s(HOUSE, "dance_three_kittens", "家族は\n写真を撮っている"),
        s(HOUSE, "happy_chipi_chapa_cat", "カップルは\nいちごを\n食べさせあっている"),
        s(HOUSE, "calm_black_face_sheep", "俺は\n黙々と\n食べている"),
        s(HOUSE, "stare_lying_tabby_cat", "ハウスの中は\nあたたかくて\n時間の感覚がなくなる"),
        s(HOUSE, "think_bike_front_seat_cat", "今\n何分だろう"),
        s(HOUSE, "stare_tabby_wide_eyes_cat", "タイマーを見る", se="pi"),
        s(HOUSE, "scream_standing_marmot", "残り5分", se="explosion_chudoon"),
        s(HOUSE, "angry_shooting_cat", "最後の追い込みだ", se="gong_match_start"),
        s(HOUSE, "eat_pop_cat", "19個目", item=BERRY),
        s(HOUSE, "eat_crunchy_cat_luna", "20個目", item=BERRY),
        s(HOUSE, "despair_dramatic_kitten", "21個目", item=BERRY),
        s(HOUSE, "sleepy_sleepy_cat", "22個目", item=BERRY),
        s(HOUSE, "blank_black_cat_zoning_out", "おなかが\nいちごになった", item=BERRY),
        s(HOUSE, "stare_big_eyes_tabby_kitten", "最後の1個を\nさがす", item=BERRY),
        s(HOUSE, "surprise_big_pupils_cat", "いちばん大きくて\n真っ赤な1個", item=BERRY),
        s(HOUSE, "showoff_gojo_cosplay_cat", "これで\nしめる", item=BERRY, se="gong_dora_jaan"),
        s(HOUSE, "eat_crunchy_cat_luna", "パクッ", item=BERRY, se="pikon"),
        s(HOUSE, "sad_banana_cat_cry", "うまい", item=BERRY),
        s(HOUSE, "cocky_dj_cat", "ピピピピ", se="pi"),
        s(HOUSE, "stare_interviewer_cat", "お時間でーす"),
        # ---- 結果 ----
        s(HOUSE, "think_chin_paw_orange_cat", "カップのヘタを\n数える"),
        s(HOUSE, "money_counting_orange_cat", "1個\n2個\n3個……"),
        s(HOUSE, "surprise_big_pupils_cat", "23個", se="explosion_chudoon"),
        s(HOUSE, "sad_looking_away_tabby", "目標の\n半分もいかなかった"),
        s(HOUSE, "stare_tabby_wide_eyes_cat", "口コミの人は\n30個"),
        s(HOUSE, "sad_black_dog", "ネットの人にも\n負けている"),
        s(HOUSE, "calmdown_dancing_cat", "いや\n18個の人には\n勝っている"),
        s(HOUSE, "huh_huh_cat", "元は\n取れたのか"),
        s(HOUSE, "calm_black_face_sheep", "……計算するのは\nやめた"),
        s(HOUSE, "realize_wet_cat_stare", "そもそも\nつみたてのいちごは\nスーパーでは\n買えない"),
        s(HOUSE, "happy_hamster_open_arms", "それだけで\n来た意味がある"),
        s(HOUSE, "peek_what_happen_cat", "となりの子どもが\n自慢している"),
        s(HOUSE, "stare_interviewer_cat", "ぼく25個\n食べた！"),
        s(HOUSE, "despair_dramatic_kitten", "負けた", se="pi"),
        s(HOUSE, "laugh_laughing_dog", "小学生に\n負けた"),
        # ---- 直売所 ----
        s(SHOP, "leave_cat_leaves_home", "ハウスを出る", se="whoosh_shu", bgm={"file": HIRU, "gain": -12, "fade": 0.8}),
        s(SHOP, "stare_big_eyes_tabby_kitten", "出口に\n直売所がある", item=PACK),
        s(SHOP, "surprise_big_pupils_cat", "つみたてのいちごが\nパックで\n売っている", item=PACK),
        s(SHOP, "think_chin_paw_orange_cat", "おなかは\nいっぱいだ", item=PACK),
        s(SHOP, "money_counting_orange_cat", "でも\n買ってしまう", item=PACK),
        s(SHOP, "sad_black_dog", "食べ放題のあとに\nいちごを買う男", item=PACK),
        s(SHOP, "joy_happy_happy_happy_cat", "いちごジャムと\nいちご大福も\n買う", item=PACK),
        # ---- 帰り道 ----
        s(ROAD, "drive_driving_cat", "帰りの車", se="whoosh_shu", bgm={"file": JITAKU, "gain": -8, "fade": 1.0}),
        s(ROAD, "sleepy_sleepy_cat", "車の中が\nいちごの香り"),
        s(ROAD, "despair_dramatic_kitten", "おなかが\nちょっと痛い"),
        s(ROAD, "read_book_orange_kitten", "口コミにも\n食べすぎで\n体調をくずした人が\nいた"),
        s(ROAD, "stare_big_eyes_tabby_kitten", "信号待ちで\nスマホを見る"),
        s(ROAD, "scream_phone_orange_cat", "撮った写真が\nいちごだけ"),
        s(ROAD, "calm_black_face_sheep", "自分が\n1枚も写っていない"),
        s(ROAD, "sad_black_dog", "1人だと\nそうなる"),
        s(ROAD, "sad_looking_away_tabby", "コンビニで\nトイレを借りる"),
        s(ROAD, "calm_black_face_sheep", "いちごは\nほとんど水分だ"),
        # ---- 夜 ----
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nソファに倒れこむ", se="whoosh_shu"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "夜8時\n腹が減った"),
        s(ROOM_N, "huh_huh_cat", "昼はいちごしか\n食べていない"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "冷蔵庫に\nいちごのパック", item=PACK),
        s(ROOM_N, "work_typing_cat", "牛乳と\nいちごをつぶして", item=DRINK),
        s(ROOM_N, "happy_girlfriend_dance_cat", "いちごミルク", item=DRINK, se="shine_kiraan_maou"),
        s(ROOM_N, "eat_crunchy_cat_luna", "ゴクゴク……", item=DRINK, se="drink_gulp_gokugoku_thirsty_chug"),
        s(ROOM_N, "sad_banana_cat_cry", "子どものころに\n夢見た飲みかただ", item=DRINK),
        s(ROOM_N, "realize_wet_cat_stare", "晩ごはんが\nいちごミルク", item=DRINK),
        s(ROOM_N, "think_chin_paw_orange_cat", "健康診断の\n結果のことは\n今は考えない"),
        s(ROOM_N, "stare_lying_tabby_cat", "いちご大福も\n食べる", item=PACK),
        s(ROOM_N, "surprise_big_pupils_cat", "あんこと\nいちごの酸味", item=PACK),
        s(ROOM_N, "happy_girlfriend_dance_cat", "和と洋の\nいいとこどり", item=PACK),
        s(ROOM_N, "despair_dramatic_kitten", "今日1日で\nいちごを\n何個食べたんだ", item=PACK),
        s(ROOM_N, "blank_black_cat_zoning_out", "数えるのは\nやめた", item=PACK),
        s(ROOM_N, "work_typing_cat", "スマホで\nいちごの\n栄養を調べる"),
        s(ROOM_N, "read_book_orange_kitten", "いちごは\nビタミンCが\n多いらしい"),
        s(ROOM_N, "rizz_cat_rizz", "つまり今日の俺は\n健康だ"),
        s(ROOM_N, "calm_black_face_sheep", "練乳のことは\n考えない"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "ピンポーン", se="pinpon_notice"),
        s(ROOM_N, "huh_huh_cat", "こんな時間に\n荷物？"),
        s(ROOM_N, "surprise_big_pupils_cat", "母さんからの\n宅配便だ"),
        s(ROOM_N, "work_typing_cat", "箱を開ける"),
        s(ROOM_N, "scream_standing_marmot", "いちご", item=PACK, se="explosion_chudoon"),
        s(ROOM_N, "despair_dramatic_kitten", "今日1日\nいちごしか\n見ていない", item=PACK),
        s(ROOM_N, "read_book_orange_kitten", "近所の農家さんに\nたくさんもらったので\nおすそわけです\nと手紙", item=PACK),
        s(ROOM_N, "sleepy_old_memories_cat", "子どものころと\n同じ字だ", item=PACK),
        s(ROOM_N, "think_chin_paw_orange_cat", "おなかは\nいっぱいだ", item=PACK),
        s(ROOM_N, "calm_black_face_sheep", "でも\n1個だけ", item=PACK),
        s(ROOM_N, "eat_crunchy_cat_luna", "パクッ", item=PACK, se="pikon"),
        s(ROOM_N, "surprise_big_pupils_cat", "……うまい", item=PACK),
        s(ROOM_N, "realize_wet_cat_stare", "今日食べた\nどのいちごより\nうまい", item=PACK),
        s(ROOM_N, "money_counting_orange_cat", "2500円払って\n23個食べた\nいちごより", item=PACK),
        s(ROOM_N, "sad_banana_cat_cry", "タダで食べる\nいちごのほうが\nうまかった", item=PACK, se="explosion_dokaan"),
        s(ROOM_N, "scream_phone_orange_cat", "母さんにLINE"),
        s(ROOM_N, "happy_chipi_chapa_cat", "いちご届いたよ\nありがとう"),
        s(ROOM_N, "stare_interviewer_cat", "たくさん食べてね"),
        s(ROOM_N, "happy_hamster_open_arms", "今日はもう\nたくさん食べた\nとは言えない"),
        s(ROOM_N, "excited_hodomoe_city_cat", "いちごは\n母さんのが\nいちばん", se="pikon", dur=3.8),
        J.end_card(),
    ]


def place(cs):
    J.diversify(cs)   # 11/9 ユーザー指定：もっと多様な素材を
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_14_ichigo.mp4"), os.path.join(J.HERE, "out", "jidaraku_14_ichigo_preview"))
