"""自堕落シリーズ #5：30代独身男、急な休みにひとりで極楽湯へ（10/31 ユーザー指定・スシローと同じ作り）。約8分。

python3 catmeme/jidaraku_05_gokurakuyu.py → out/jidaraku_05_gokurakuyu.mp4
- 流れ（ユーザー指定）：急に休みになった → 行きたい所はない、でも心身をメンテナンスしたという結果を残さないと負けた気分 →
  そうだスーパー銭湯に行こう → こういう時でないと行く機会がない → 最高！ → 2度風呂も最高・メシもうまい・漫画も読めて一日中いられる →
  平日なのに休憩スペースに大学生カップルがちらほら → 体はポカポカ、なのに心は寒い。情緒が押し寄せる魔界だった
- 口コミ・公式の情報（2026年ごろ・店舗によってちがう）：店舗数日本一のスーパー銭湯チェーン／高濃度炭酸泉（血のめぐり・むくみに）／
  オートロウリュのサウナと水風呂が人気／食事処は湯上がりの十割そば・うどん・ビールに合うおつまみ・サウナ後の辛めの「サ飯」／
  漫画2万冊以上の店も・大型リクライニングチェア・寝ころび休憩スペース／平日は土日より少し安い・平日の昼はすいていてゆっくり入れる
- 字幕に句読点・カギかっこなし（スシローと同じ）。「にゃ」なし。単語の途中で改行しない。値段は書かない
- 背景・料理の写真はユーザーがあとでくれる（backgrounds/jidaraku/05_gokurakuyu/）。届くまでは手もちの背景で代わりにする
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "05_gokurakuyu"))
J.BGS += [os.path.join(J.HERE, "backgrounds", d) for d in ("17_imamori", "24_chudo", "25_world")]
ROOM, FRONT, LOBBY, BATH, ROTEN, SAUNA, DINING, MANGA, REST, ROAD, ROOM_N = (
    "j01_room", "g01_front", "g02_lobby", "g03_bath", "g04_roten", "g05_sauna", "g06_dining", "g07_manga", "g08_rest", "g09_road",
    "g10_room_night")
J.STANDIN.update({FRONT: "bg61_snow_onsen", LOBBY: "bg100_lounge_night", BATH: "bg61_snow_onsen", ROTEN: "bg61_snow_onsen",
                  SAUNA: "bg61_snow_onsen", DINING: "bg98_izakaya_night", MANGA: "bg100_lounge_night", REST: "bg100_lounge_night",
                  ROAD: "bg51_night_street", ROOM_N: ROOM})
NIGHT = {ROOM_N: 0.72, ROAD: 0.62}   # 帰り道：車のとまった外観の絵を夜っぽく暗くして使う（11/1）
J.STANDIN[ROAD] = "g01_front_cars"
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
CATLIFE = os.path.join(L.BGM, "nc102462_Cat_life.mp3")
# 料理などの写真（届いたら backgrounds/jidaraku/05_gokurakuyu に同じ名前で置く）
BEER, SOBA, KARAAGE, KARAI, ICE, MILK = "f_beer", "f_soba", "f_karaage", "f_karai_men", "f_ice", "f_coffee_milk"


def cuts():
    def s(*a, **k):   # 1つの字幕は3.4秒（8分前後にする）
        k.setdefault("dur", 3.4)
        return J.line(*a, **k)
    return [
        # ---- 急な休み ----
        s(ROOM, "sleep_sleeping_cat", "火曜の朝7時\nスマホが鳴った", se="pikon", bgm={"file": L.NORA, "gain": -12}),
        s(ROOM, "stare_big_eyes_tabby_kitten", "会社からの連絡\n今日は急に休みになった"),
        s(ROOM, "excited_hodomoe_city_cat", "平日の\n急な休み"),
        s(ROOM, "dance_three_kittens", "なんて\nぜいたくな響きだ", se="sparkle_kirakira_01"),
        s(ROOM, "blank_black_cat_zoning_out", "だが\n行きたい所は特にない"),
        s(ROOM, "think_chin_paw_orange_cat", "やりたいことも\n思いつかない"),
        s(ROOM, "slack_nail_filing_cat", "このまま寝ていても\nいい"),
        s(ROOM, "sleepy_old_memories_cat", "スマホを見ていたら\n昼になっていた"),
        s(ROOM, "realize_wet_cat_stare", "……いや\nそれは負けだ"),
        s(ROOM, "angry_aiming_cat", "こんな日には\n何かを残さなければならない"),
        s(ROOM, "think_bike_front_seat_cat", "心と体を\nメンテナンスしたという\n結果を"),
        s(ROOM, "sad_looking_away_tabby", "それがないと\n休みに負けた気分になるのだ"),
        s(ROOM, "think_chin_paw_orange_cat", "ジムは\n続かなかった"),
        s(ROOM, "sulk_hungry_cat", "マッサージは\nひとりで入るのが少しこわい"),
        s(ROOM, "stare_tabby_wide_eyes_cat", "……そうだ", se="pikon"),
        s(ROOM, "yell_orange_fat_cat", "スーパー銭湯\n行こう", se="explosion_dokaan"),
        s(ROOM, "read_book_orange_kitten", "向かうのは極楽湯\n店舗数日本一の\nスーパー銭湯チェーンだ"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "公式サイトを開く\n高濃度炭酸泉\nサウナ\n食事処"),
        s(ROOM, "excited_hodomoe_city_cat", "漫画も読める\n一日中いられる"),
        s(ROOM, "realize_wet_cat_stare", "こういう時でないと\nなかなか行く機会がない"),
        s(ROOM, "showoff_gojo_cosplay_cat", "タオルは向こうで借りる\n手ぶらで行ける"),
        s(ROOM, "dance_happy_banana_cat", "ジャージのまま\n家を出る", se="whoosh_shu"),
        # ---- 到着 ----
        s(FRONT, "ride_kitten_bike", "昼の1時\n極楽湯に到着"),
        s(FRONT, "peek_what_happen_cat", "平日の昼は\nすいていると口コミにあった"),
        s(FRONT, "happy_hamster_open_arms", "しかも平日は\n土日より少し安い"),
        s(FRONT, "showoff_gojo_cosplay_cat", "平日休みの\n特権だ"),
        s(LOBBY, "work_typing_cat", "券売機で\n入館券を買う"),
        s(LOBBY, "stare_interviewer_cat", "げた箱の鍵と\nリストバンドをもらう"),
        s(LOBBY, "dance_tabby_standing_cat", "このリストバンドで\n館内の会計は後払い"),
        s(LOBBY, "realize_wet_cat_stare", "危険なシステムだ"),
        s(LOBBY, "stare_big_eyes_tabby_kitten", "館内着を借りる\n上下セットのやつだ"),
        s(LOBBY, "showoff_gojo_cosplay_cat", "着替えると\n一気にくつろぎモード"),
        s(LOBBY, "peek_what_happen_cat", "館内の案内図を見る\n思ったより広い"),
        s(LOBBY, "calmdown_dancing_cat", "まずは\n風呂だ", se="pinpon_notice"),
        # ---- 風呂 ----
        s(BATH, "leave_cat_leaves_home", "体を洗って\nいざ湯船へ", bgm={"file": L.PURPLE, "gain": -12, "fade": 0.8}),
        s(BATH, "sleepy_old_memories_cat", "最初は\nあつ湯で体を慣らす"),
        s(BATH, "blank_black_cat_zoning_out", "ふぅ……"),
        s(BATH, "peek_what_happen_cat", "続いて\n口コミで評判の\n高濃度炭酸泉"),
        s(BATH, "surprise_big_pupils_cat", "肌に細かい泡が\nびっしりつく", se="sparkle_kirakira_01"),
        s(BATH, "happy_chipi_chapa_cat", "血のめぐりがよくなって\nむくみにもいいらしい"),
        s(BATH, "sleep_sleeping_cat", "ぬるめのお湯で\nいつまでも入っていられる"),
        s(BATH, "sleepy_sleepy_cat", "まぶたが\n重くなってくる"),
        s(BATH, "surprise_big_pupils_cat", "あぶない\n湯船で寝るところだった"),
        s(BATH, "realize_wet_cat_stare", "気づけば\n20分たっていた"),
        s(ROTEN, "walk_white_duck", "露天風呂へ\n移動する", se="whoosh_shu"),
        s(ROTEN, "happy_hamster_open_arms", "平日の昼の空\n誰も働けとは言わない"),
        s(ROTEN, "sleepy_old_memories_cat", "今ごろ同期は\n会議中だろう"),
        s(ROTEN, "showoff_gojo_cosplay_cat", "俺は\n露天風呂だ"),
        s(ROTEN, "stare_lying_tabby_cat", "寝ころび湯で\n空を見上げる"),
        s(ROTEN, "sleepy_old_memories_cat", "つぼ湯もある\nひとり用の丸いお風呂"),
        s(ROTEN, "happy_chipi_chapa_cat", "ひとり用\n今の俺にぴったりだ"),
        s(ROTEN, "realize_wet_cat_stare", "肩までつかって\n目を閉じる"),
        s(ROTEN, "happy_girlfriend_dance_cat", "最高！", se="pinpoon_correct"),
        # ---- サウナ ----
        s(SAUNA, "think_bike_front_seat_cat", "そして\nサウナ", se="gong_dora_jaan"),
        s(SAUNA, "stare_tabby_wide_eyes_cat", "オートロウリュで\n熱い蒸気が降ってくる", se="explosion_doon"),
        s(SAUNA, "despair_dramatic_kitten", "あつい……\nでも出たら負けだ"),
        s(SAUNA, "sulk_hungry_cat", "テレビの時計を\nにらむ"),
        s(SAUNA, "glare_disgusted_cat", "となりのおじさんと\n無言の我慢比べ"),
        s(SAUNA, "sad_banana_cat_cry", "……先に出たのは\n俺だった"),
        s(SAUNA, "surprise_big_pupils_cat", "水風呂へ\nドボン", se="freeze_kochiin"),
        s(SAUNA, "blank_black_cat_zoning_out", "外の椅子で\n休憩する"),
        s(SAUNA, "happy_chipi_chapa_cat", "体がじんじんする\nこれが\nととのうか", se="shine_kiraan_maou"),
        s(SAUNA, "dance_maxwell_cat", "3セット\nくり返した"),
        s(SAUNA, "think_bike_front_seat_cat", "サウナ好きの口コミでも\nロウリュと水風呂は人気だ"),
        s(SAUNA, "rizz_cat_rizz", "サウナハットの人もいる\n上級者だ"),
        s(SAUNA, "blank_black_cat_zoning_out", "俺は\nタオルを頭にのせるだけ"),
        # ---- 食事 ----
        s(DINING, "eat_pop_cat", "湯上がりは\n食事処へ", bgm={"file": L.COCOA, "gain": -12, "fade": 0.8}),
        s(DINING, "read_book_orange_kitten", "メニューが\n多すぎて迷う"),
        s(DINING, "cocky_dj_cat", "まずは\n生ビール", item=BEER),
        s(DINING, "eat_crunchy_cat_luna", "ゴクッ……\nくぅ〜！", item=BEER, se="drink_gulp_gokugoku_thirsty_chug"),
        s(DINING, "happy_hamster_open_arms", "湯上がりのビールは\n反則だ", item=BEER),
        s(DINING, "work_typing_cat", "つまみは\n唐揚げ", item=KARAAGE),
        s(DINING, "eat_chips_cat", "外はカリッ\n中はジュワッ", item=KARAAGE),
        s(DINING, "stare_big_eyes_tabby_kitten", "サウナのあとの\n辛いメシは\nサ飯と呼ぶらしい", item=KARAI),
        s(DINING, "despair_dramatic_kitten", "からい……\nでも汗がまた気持ちいい", item=KARAI),
        s(DINING, "realize_wet_cat_stare", "しめは\n十割そば", item=SOBA),
        s(DINING, "sleepy_old_memories_cat", "湯上がりの体に\nするする入る", item=SOBA),
        s(DINING, "happy_chipi_chapa_cat", "メシも\nうまい！", se="pinpoon_correct"),
        s(DINING, "stare_interviewer_cat", "となりのテーブルは\n常連のおじいさんたち"),
        s(DINING, "laugh_laughing_dog", "昼から\n楽しそうに飲んでいる"),
        s(DINING, "sleepy_old_memories_cat", "老後は\nこういう暮らしもいい"),
        # ---- 漫画・休憩 ----
        s(MANGA, "read_book_orange_kitten", "休憩処には\n漫画がずらり"),
        s(MANGA, "stare_tabby_wide_eyes_cat", "店によっては\n2万冊以上もあるらしい"),
        s(MANGA, "excited_hodomoe_city_cat", "大型の\nリクライニングチェアに\nしずみこむ"),
        s(MANGA, "read_book_orange_kitten", "昔読んでいた漫画を\n1巻から"),
        s(MANGA, "sleepy_sleepy_cat", "……気づけば\n寝ていた", se="cuckoo_pappo"),
        s(MANGA, "stare_big_eyes_tabby_kitten", "起きたら夕方\n漫画は5巻まで進んでいた"),
        s(MANGA, "dance_three_kittens", "一日中\nいられる"),
        s(MANGA, "work_dog_staring_computer", "マッサージチェアも\nためしてみる"),
        s(MANGA, "stare_tabby_wide_eyes_cat", "思ったより\n強い", se="gugi"),
        s(MANGA, "dance_wop_cat", "肩と腰が\nごりごりほぐれる"),
        s(MANGA, "peek_what_happen_cat", "岩盤浴のエリアもある\nあたたかい石の床"),
        s(MANGA, "sleep_sleeping_cat", "ねころんで\nじわじわ汗をかく"),
        # ---- 2度風呂 ----
        s(BATH, "walk_white_duck", "そして\nもう一度風呂へ", se="whoosh_shu"),
        s(BATH, "happy_hamster_open_arms", "2度風呂も\n最高！"),
        s(BATH, "sleepy_old_memories_cat", "夕方の露天風呂は\n空がオレンジ色だ"),
        s(BATH, "happy_chipi_chapa_cat", "サウナも\nもう1セット"),
        s(LOBBY, "eat_pop_cat", "風呂上がりの\nコーヒー牛乳", item=MILK),
        s(LOBBY, "showoff_gojo_cosplay_cat", "腰に手を当てて\n一気に飲む", item=MILK, se="drink_gulp_gokugoku_thirsty_chug"),
        s(DINING, "work_typing_cat", "ついでに\nソフトクリームも", item=ICE),
        s(DINING, "happy_hamster_open_arms", "ほてった体に\nつめたいソフト", item=ICE),
        s(DINING, "eat_pop_cat", "これも\n最高だ", item=ICE),
        # ---- 大学生カップル ----
        s(REST, "stare_lying_tabby_cat", "寝ころび休憩スペースに\n戻る", bgm={"file": LOFI, "gain": -14, "fade": 1.0}),
        s(REST, "peek_what_happen_cat", "ふと\nまわりを見る"),
        s(REST, "stare_interviewer_cat", "おそろいの館内着の\n2人組"),
        s(REST, "surprise_big_pupils_cat", "大学生の\nカップルだ", se="question_hatena_maou"),
        s(REST, "stare_tabby_wide_eyes_cat", "あっちにも"),
        s(REST, "despair_dramatic_kitten", "こっちにも"),
        s(REST, "confused_i_dont_know_cat", "平日だからか\n大学生カップルが\nちらほら"),
        s(REST, "sad_looking_away_tabby", "2人で1冊の\n漫画を読んでいる"),
        s(REST, "blank_black_cat_zoning_out", "俺は\nひとりで5巻まで読んだ"),
        s(REST, "think_bike_front_seat_cat", "大学生のころの俺は\n平日の昼に\n何をしていただろう"),
        s(REST, "sleepy_old_memories_cat", "たしか\nバイトと\nひとりでゲームだ"),
        s(REST, "realize_wet_cat_stare", "今も\nあまり変わっていない"),
        s(REST, "think_chin_paw_orange_cat", "いや\n今の俺には\n平日休みと極楽湯がある"),
        s(REST, "glare_disgusted_cat", "……カップルの笑い声が\n聞こえる"),
        s(REST, "sad_banana_cat_cry", "リクライニングを\nそっともどす"),
        # ---- 帰る ----
        s(LOBBY, "money_counting_orange_cat", "リストバンドを\nフロントに返す"),
        s(LOBBY, "stare_tabby_wide_eyes_cat", "後払いの会計は\n思ったより\nふくらんでいた", se="price_display"),
        s(LOBBY, "despair_dramatic_kitten", "入館料より\n食事のほうが高い"),
        s(LOBBY, "realize_wet_cat_stare", "ビールと唐揚げと\nソフトクリームのせいだ"),
        s(ROAD, "leave_cat_leaves_home", "外に出る\nもう夜だ", se="whoosh_shu"),
        s(ROAD, "happy_hamster_open_arms", "体は\nポカポカだ"),
        s(ROAD, "sleepy_old_memories_cat", "肌もつるつる\n肩も軽い"),
        s(ROAD, "showoff_gojo_cosplay_cat", "心と体のメンテナンス\n大成功だ"),
        s(ROAD, "stare_interviewer_cat", "前を歩く\n大学生カップルが\n手をつないでいる"),
        s(ROAD, "blank_black_cat_zoning_out", "……"),
        s(ROAD, "sad_looking_away_tabby", "体はポカポカに\nなった"),
        s(ROAD, "sad_banana_cat_cry", "なのに\n心には寒さを感じる", se="chin_bell_failure_sad_ending",
          bgm={"file": os.path.join(L.BGM, "手紙のさよなら.mp3"), "gain": -14, "fade": 1.0}),
        s(ROAD, "despair_dramatic_kitten", "スーパー銭湯は\n情緒が押し寄せる\n魔界だった"),
        # ---- 夜 ----
        s(ROOM_N, "sleep_sleeping_cat", "家に帰る\n返事はない"),
        s(ROOM_N, "slack_nail_filing_cat", "布団に入る\n体がまだあたたかい"),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "極楽湯のアプリを\n入れていた"),
        s(ROOM_N, "realize_wet_cat_stare", "クーポンが\n届いている"),
        s(ROOM_N, "think_chin_paw_orange_cat", "次の休みは"),
        s(ROOM_N, "excited_hodomoe_city_cat", "漫画の6巻から\n読もう", se="pikon", dur=3.4),
        J.end_card(),
    ]


def place(cs):
    for c in cs:
        if c.get("text"):   # スシローと同じ：字幕にカギかっこはつけない
            c["text"] = c["text"].replace("「", "").replace("」", "")
        if c.get("bg") in NIGHT:
            c["dark"] = NIGHT[c["bg"]]
    return cs


if __name__ == "__main__":
    cs = place(cuts())
    if os.environ.get("LEN"):
        print(len(cs), round(sum(c["dur"] for c in cs), 1))
    else:
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_05_gokurakuyu.mp4"),
              os.path.join(J.HERE, "out", "jidaraku_05_gokurakuyu_preview"))
