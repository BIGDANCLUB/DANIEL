"""自堕落シリーズ #9：30代独身男、休日にひとりでコストコ（11/3 ユーザー指定の流れ・鳥貴族/IKEAと同じ作り）。約8分。

python3 catmeme/jidaraku_09_costco.py → out/jidaraku_09_costco.mp4
- 流れ（ユーザー指定）：休日たまたまテレビでコストコ特集 → 1人でコストコもなぁと敬遠 → なにっ!?家電やゲームも売っている!? →
  安いと聞く…これは見に行くしかない → 年会費高いなぁ…元を取るためにまた来なきゃという気持ちにさせる → 乗らせてくれるぜ！ →
  人気の商品（サーモンポキ・プルコギ・ディナーロールなど）を口コミを参考に
- 口コミ・記事の声（2025〜2026年ごろ）：プルコギビーフは「やわらかい牛肉と本格的な甘辛ダレ」／ディナーロールは36個入りで冷凍保存も人気・
  ロティサリーチキンとならんでリピート率が高い／フードコートのホットドッグはドリンク付き180円で10年以上同じ値段／
  年会費（ゴールドスター個人）は2025年に4840円→5280円に
- 「40代独身の何気ない日常」など3チャンネルにコストコの回はない（research/benchmark_channels.md・11/3 確認）
- 写真がない料理は字幕だけ（写真が届いたら backgrounds/jidaraku/09_costco に置く）
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "09_costco"))
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku", d) for d in ("04_sushiro", "05_gokurakuyu", "06_bronco", "07_ikea", "08_torikizoku")]
J.BGS.append(os.path.join(J.HERE, "backgrounds", "26_kuruma"))
ROOM, PARK, FRONT, ENTRY, ELEC, FOOD, DELI, COURT, REGI, ROOM_N = (
    "j01_room", "c01_parking", "c02_front", "c03_entrance", "c04_electronics", "c05_food", "c06_deli", "c07_foodcourt",
    "c08_register", "j07_room_night")
J.STANDIN.update({PARK: "bg26_parking_lot", FRONT: "i01_front", ENTRY: "i05_market", ELEC: "i05_market", FOOD: "i05_market",
                  DELI: "i05_market", COURT: "i06_restaurant", REGI: "i05_market"})
MORNING = os.path.join(L.BGM, "Morning.mp3")
NANDE = os.path.join(L.BGM, "なんでしょう？.mp3")
HIRU = os.path.join(L.BGM, "昼下がり気分.mp3")
JITAKU = os.path.join(L.BGM, "自宅にて.mp3")
# 写真（届いた順に backgrounds/jidaraku/09_costco に置く）
CARD, CART, TV, GAME, POKI, BULGOGI, ROLL, CHICKEN, MUFFIN, HOTDOG = (
    "f_card", "f_cart", "f_tv", "f_game", "f_poki", "f_bulgogi", "f_roll", "f_chicken", "f_muffin", "f_hotdog")


def cuts():
    def s(*a, **k):   # 長さは place() で字幕の文字数から決める
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 休日 ----
        s(ROOM, "sleep_sleeping_cat", "日曜の朝10時\n目が覚めた", bgm={"file": MORNING, "gain": -12}),
        s(ROOM, "blank_black_cat_zoning_out", "予定はない"),
        s(ROOM, "slack_nail_filing_cat", "なんとなく\nテレビをつける"),
        s(ROOM, "stare_tabby_wide_eyes_cat", "コストコ特集\nをやっていた", se="pikon"),
        s(ROOM, "peek_what_happen_cat", "巨大なカートに\n山盛りの食べ物"),
        s(ROOM, "stare_interviewer_cat", "家族連れが\n楽しそうに\n買い物をしている"),
        s(ROOM, "think_chin_paw_orange_cat", "……コストコか"),
        s(ROOM, "read_book_orange_kitten", "アメリカ生まれの\n会員制の\n大きな倉庫型のお店"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "なんでも\n大きい・多い・安い"),
        s(ROOM, "happy_hamster_open_arms", "テレビの中の家族は\nみんな笑顔だ"),
        s(ROOM, "sad_looking_away_tabby", "でも\n1人でコストコに行くのもなぁ"),
        s(ROOM, "sleepy_old_memories_cat", "あれは家族で\n行く場所だ"),
        s(ROOM, "despair_dramatic_kitten", "1人で\nあの量は\n食べきれない"),
        s(ROOM, "glare_disgusted_cat", "チャンネルを\n変えようとした\nそのとき"),
        s(ROOM, "surprise_big_pupils_cat", "なにっ!?", se="explosion_dokaan"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "コストコって\n家電やゲームも\n売っているのか!?"),
        s(ROOM, "read_book_orange_kitten", "テレビ\nパソコン\nゲーム機まで"),
        s(ROOM, "think_bike_front_seat_cat", "コストコは\n安いと聞く"),
        s(ROOM, "excited_hodomoe_city_cat", "安い家電に\nゲーム……"),
        s(ROOM, "angry_aiming_cat", "これは\n見に行くしかない", se="gong_match_start"),
        s(ROOM, "blank_black_cat_zoning_out", "部屋着のまま\n上着だけ羽織る"),
        # ---- 到着 ----
        s(PARK, "drive_driving_cat", "車で30分\nコストコに到着", se="whoosh_shu", bgm={"file": L.PURPLE, "gain": -12, "fade": 0.8}),
        s(PARK, "surprise_big_pupils_cat", "駐車場が\n広すぎる"),
        s(PARK, "peek_what_happen_cat", "どこまでも\n車が並んでいる"),
        s(PARK, "stare_tabby_wide_eyes_cat", "ミニバンから\n家族がぞろぞろ\n降りてくる"),
        s(PARK, "sad_looking_away_tabby", "俺は\n軽自動車から\n1人で降りる"),
        s(FRONT, "showoff_gojo_cosplay_cat", "巨大な倉庫", se="gong_dora_jaan"),
        s(FRONT, "rizz_cat_rizz", "ここが\n戦場か"),
        s(FRONT, "stare_interviewer_cat", "入口の前には\n大きなカートを押す\n人の列"),
        s(FRONT, "think_bike_front_seat_cat", "みんな\n戦いなれた顔をしている"),
        s(FRONT, "sad_looking_away_tabby", "俺は\n初心者マークだ"),
        # ---- 年会費 ----
        s(ENTRY, "stare_interviewer_cat", "入口で止められる"),
        s(ENTRY, "confused_i_dont_know_cat", "コストコは\n会員じゃないと\n入れないらしい"),
        s(ENTRY, "work_typing_cat", "入会カウンターへ"),
        s(ENTRY, "read_book_orange_kitten", "年会費は\n5000円ちょっと", item=CARD),
        s(ENTRY, "despair_dramatic_kitten", "年会費\n高いなぁ……", item=CARD),
        s(ENTRY, "think_chin_paw_orange_cat", "1回だけ来て\nやめたら\nもったいない", item=CARD),
        s(ENTRY, "sleepy_old_memories_cat", "元を取るには\nまた来なきゃ\nいけない", item=CARD),
        s(ENTRY, "stare_big_eyes_tabby_kitten", "……そういう気持ちに\nさせる作戦か", item=CARD),
        s(ENTRY, "excited_hodomoe_city_cat", "乗らせてくれるぜ！", se="explosion_dokaan", item=CARD),
        s(ENTRY, "money_counting_orange_cat", "会員カードの写真を\nその場で撮られる"),
        s(ENTRY, "blank_black_cat_zoning_out", "寝ぐせのまま\n写った"),
        s(ENTRY, "sad_looking_away_tabby", "この顔で\n1年間\n入店することになる"),
        s(ENTRY, "calm_black_face_sheep", "……まあいい\n誰も見ていない"),
        # ---- カート ----
        s(ENTRY, "surprise_big_pupils_cat", "カートが\nでかい", item=CART, se="pikon"),
        s(ENTRY, "think_bike_front_seat_cat", "子どもが2人\n乗れそうな大きさ", item=CART),
        s(ENTRY, "sad_looking_away_tabby", "1人で押すと\nカートが\nスカスカだ", item=CART),
        s(ENTRY, "rizz_cat_rizz", "このカートを\nいっぱいにして帰る", item=CART),
        # ---- 家電・ゲーム ----
        s(ELEC, "cocky_dj_cat", "まずは\n家電コーナーだ", se="whoosh_shu", bgm={"file": NANDE, "gain": -6, "fade": 0.8}),
        s(ELEC, "surprise_big_pupils_cat", "入口すぐに\n巨大なテレビが\nずらり", item=TV),
        s(ELEC, "stare_big_eyes_tabby_kitten", "75インチ", item=TV),
        s(ELEC, "think_chin_paw_orange_cat", "俺の部屋の\n壁より大きい", item=TV),
        s(ELEC, "glare_disgusted_cat", "置く場所が\nない", item=TV),
        s(ELEC, "read_book_orange_kitten", "パソコンや\nタブレットも\n並んでいる"),
        s(ELEC, "think_chin_paw_orange_cat", "家電量販店より\n安いものもあるらしい"),
        s(ELEC, "stare_big_eyes_tabby_kitten", "ロボット掃除機\nマッサージ器\nコーヒーマシン"),
        s(ELEC, "happy_chipi_chapa_cat", "どれも\n独身の部屋を\n豊かにしそうだ"),
        s(ELEC, "glare_disgusted_cat", "……箱が\nでかい"),
        s(ELEC, "despair_dramatic_kitten", "軽自動車に\n入るだろうか"),
        s(ELEC, "stare_tabby_wide_eyes_cat", "そして\nゲームコーナー", item=GAME, se="pikon"),
        s(ELEC, "excited_hodomoe_city_cat", "ゲーム機と\nソフトが\nセットで売っている", item=GAME),
        s(ELEC, "happy_chipi_chapa_cat", "小学生のころの\n夢のセットだ", item=GAME),
        s(ELEC, "sleepy_old_memories_cat", "誕生日まで\n待てなかったあの頃", item=GAME),
        s(ELEC, "think_chin_paw_orange_cat", "でも\nもう持っている", item=GAME),
        s(ELEC, "despair_dramatic_kitten", "家電を見に来たのに\n何も買えない"),
        s(ELEC, "blank_black_cat_zoning_out", "……IKEAでも\nこうだった気がする"),
        s(ELEC, "think_bike_front_seat_cat", "いや\n買わないのも\n立派な選択だ"),
        s(ELEC, "rizz_cat_rizz", "見るだけで\n楽しいのが\n大人の買い物だ"),
        s(ELEC, "angry_aiming_cat", "いや\n今日は食べ物だ"),
        # ---- 食品 ----
        s(FOOD, "dance_three_kittens", "食品コーナーへ", se="whoosh_shu", bgm={"file": HIRU, "gain": -6, "fade": 0.8}),
        s(FOOD, "surprise_big_pupils_cat", "棚が\n天井まである"),
        s(FOOD, "stare_big_eyes_tabby_kitten", "牛乳が\n2本セット"),
        s(FOOD, "confused_i_dont_know_cat", "ヨーグルトが\nバケツ"),
        s(FOOD, "despair_dramatic_kitten", "トイレットペーパーが\n俺の身長くらいある"),
        s(FOOD, "think_chin_paw_orange_cat", "ここは\n巨人の国だ"),
        s(FOOD, "read_book_orange_kitten", "あちこちで\n試食をやっている", se="pikon"),
        s(FOOD, "eat_pop_cat", "ひと口ずつ\n全部もらう"),
        s(FOOD, "happy_hamster_open_arms", "試食だけで\nお昼ごはんに\nなりそうだ"),
        s(FOOD, "glare_disgusted_cat", "いや\nさすがに\n図々しい"),
        s(FOOD, "stare_interviewer_cat", "でも\n店員さんが\nどうぞ〜と言ってくる"),
        s(FOOD, "eat_crunchy_cat_luna", "もらう"),
        s(FOOD, "happy_girlfriend_dance_cat", "チーズ\nソーセージ\nジュース"),
        s(FOOD, "rizz_cat_rizz", "ここは\n試食のテーマパークだ"),
        # ---- プルコギ ----
        s(DELI, "work_typing_cat", "精肉コーナー"),
        s(DELI, "showoff_gojo_cosplay_cat", "口コミで\nいつも上位の\nプルコギ", item=BULGOGI, se="gong_dora_jaan"),
        s(DELI, "stare_big_eyes_tabby_kitten", "大きなパックに\nタレに漬かった牛肉が\nぎっしり", item=BULGOGI),
        s(DELI, "read_book_orange_kitten", "やわらかい牛肉と\n本格的な甘辛ダレ\nらしい", item=BULGOGI),
        s(DELI, "think_chin_paw_orange_cat", "焼くだけで\n晩ごはんが\n完成する", item=BULGOGI),
        s(DELI, "despair_dramatic_kitten", "でも\n何人前だこれ", item=BULGOGI),
        s(DELI, "money_counting_orange_cat", "小分けにして\n冷凍すればいい", item=BULGOGI),
        s(DELI, "rizz_cat_rizz", "カートに入れる", item=BULGOGI, se="pi"),
        s(DELI, "peek_what_happen_cat", "となりで\nステーキ肉を\n選んでいる夫婦"),
        s(DELI, "stare_big_eyes_tabby_kitten", "肉が\nブロックで\n売っている"),
        s(DELI, "think_chin_paw_orange_cat", "フライパンに\n入るのか"),
        # ---- サーモンポキ ----
        s(DELI, "stare_tabby_wide_eyes_cat", "となりの\nお惣菜コーナー"),
        s(DELI, "surprise_big_pupils_cat", "サーモンポキ", item=POKI, se="explosion_dokaan"),
        s(DELI, "eat_pop_cat", "角切りのサーモンが\nタレをまとって\nつやつやしている", item=POKI),
        s(DELI, "happy_girlfriend_dance_cat", "ごはんに乗せたら\nポキ丼", item=POKI),
        s(DELI, "think_bike_front_seat_cat", "でもこれも\n家族サイズだ", item=POKI),
        s(DELI, "angry_aiming_cat", "……今日の晩と\n明日の朝と\n明日の昼だ", item=POKI),
        s(DELI, "rizz_cat_rizz", "カートに入れる", item=POKI, se="pi"),
        s(DELI, "read_book_orange_kitten", "口コミでは\nおつまみにも\nちょうどいいらしい"),
        s(DELI, "cocky_dj_cat", "ビールも\nケースで買うか"),
        # ---- ロティサリーチキン ----
        s(DELI, "peek_what_happen_cat", "いいにおいがする"),
        s(DELI, "stare_big_eyes_tabby_kitten", "まるごと1羽の\nロティサリーチキン", item=CHICKEN, se="pikon"),
        s(DELI, "read_book_orange_kitten", "口コミでも\nリピートする人が\n多いらしい", item=CHICKEN),
        s(DELI, "confused_i_dont_know_cat", "1羽を\n1人で？", item=CHICKEN),
        s(DELI, "think_chin_paw_orange_cat", "……", item=CHICKEN),
        s(DELI, "yell_orange_fat_cat", "クリスマスの\n予行演習だ", item=CHICKEN),
        s(DELI, "rizz_cat_rizz", "カートに入れる", item=CHICKEN, se="pi"),
        # ---- ディナーロール ----
        s(FOOD, "work_typing_cat", "パンのコーナー"),
        s(FOOD, "surprise_big_pupils_cat", "ディナーロール", item=ROLL, se="gong_dora_jaan"),
        s(FOOD, "stare_tabby_wide_eyes_cat", "36個入り", item=ROLL),
        s(FOOD, "despair_dramatic_kitten", "36個", item=ROLL, se="explosion_chudoon"),
        s(FOOD, "read_book_orange_kitten", "ふわふわで\n冷凍しても\nおいしいと評判", item=ROLL),
        s(FOOD, "think_chin_paw_orange_cat", "1日3個食べても\n12日かかる", item=ROLL),
        s(FOOD, "blank_black_cat_zoning_out", "計算するのを\nやめた", item=ROLL),
        s(FOOD, "rizz_cat_rizz", "カートに入れる", item=ROLL, se="pi"),
        s(FOOD, "stare_interviewer_cat", "となりのお母さんも\n2袋入れていた"),
        s(FOOD, "happy_hamster_open_arms", "仲間だ"),
        s(FOOD, "stare_big_eyes_tabby_kitten", "マフィンも\n6個入りで\nこの大きさ", item=MUFFIN),
        s(FOOD, "eat_crunchy_cat_luna", "朝ごはんに\nちょうどいい", item=MUFFIN),
        s(FOOD, "happy_hamster_open_arms", "カートに入れる", item=MUFFIN, se="pi"),
        s(FOOD, "dance_koto_nai_cat", "あれ\nカートが\nスカスカじゃない"),
        s(FOOD, "surprise_big_pupils_cat", "いつの間にか\n山盛りだ"),
        s(FOOD, "despair_dramatic_kitten", "テレビの家族と\n同じカートに\nなっている"),
        s(FOOD, "sleepy_old_memories_cat", "冷凍コーナーで\n大きなピザを見つける"),
        s(FOOD, "think_chin_paw_orange_cat", "うちのオーブンに\n入らない"),
        s(FOOD, "blank_black_cat_zoning_out", "そっと戻す"),
        s(FOOD, "stare_tabby_wide_eyes_cat", "お菓子コーナーで\n巨大なクッキーの缶"),
        s(FOOD, "happy_chipi_chapa_cat", "会社に持って行けば\n人気者になれる"),
        s(FOOD, "rizz_cat_rizz", "カートに入れる"),
        s(FOOD, "work_typing_cat", "洗剤も\nティッシュも\nまとめ買い"),
        s(FOOD, "happy_hamster_open_arms", "1年は\n買わなくていい"),
        # ---- フードコート ----
        s(COURT, "sulk_hungry_cat", "歩きすぎて\n腹が減った", se="whoosh_shu"),
        s(COURT, "work_typing_cat", "レジのあとに\nフードコートがある"),
        s(COURT, "showoff_gojo_cosplay_cat", "ホットドッグと\nドリンクのセット", item=HOTDOG, se="gong_dora_jaan"),
        s(COURT, "stare_tabby_wide_eyes_cat", "180円", item=HOTDOG),
        s(COURT, "surprise_big_pupils_cat", "180円!?", item=HOTDOG, se="explosion_dokaan"),
        s(COURT, "read_book_orange_kitten", "10年以上\n同じ値段らしい", item=HOTDOG),
        s(COURT, "eat_crunchy_cat_luna", "パリッ……", item=HOTDOG),
        s(COURT, "happy_girlfriend_dance_cat", "ソーセージが\nでかい", item=HOTDOG),
        s(COURT, "happy_chipi_chapa_cat", "ドリンクは\nおかわり自由", item=HOTDOG),
        s(COURT, "realize_wet_cat_stare", "ここだけで\n年会費の元が\n取れそうな気がする"),
        s(COURT, "sleepy_old_memories_cat", "まわりのテーブルでは\n家族が大きなピザを\n分けている"),
        s(COURT, "blank_black_cat_zoning_out", "俺は\nホットドッグを\n1人で分けている"),
        s(COURT, "think_chin_paw_orange_cat", "……分けていない\n全部俺のものだ"),
        s(COURT, "happy_chipi_chapa_cat", "ソフトクリームも\n食べる"),
        s(COURT, "eat_pop_cat", "大きい\nそして濃い"),
        # ---- 会計 ----
        s(REGI, "work_typing_cat", "……あ\nまだ会計をしていなかった", se="pi"),
        s(REGI, "stare_interviewer_cat", "レジに並ぶ"),
        s(REGI, "peek_what_happen_cat", "前の家族のカートは\n2台"),
        s(REGI, "money_counting_orange_cat", "俺のカートは\n1台で山盛り"),
        s(REGI, "stare_tabby_wide_eyes_cat", "お会計"),
        s(REGI, "surprise_big_pupils_cat", "2万円", se="explosion_dokaan"),
        s(REGI, "despair_dramatic_kitten", "……2万円？"),
        s(REGI, "think_chin_paw_orange_cat", "1つ1つは安い"),
        s(REGI, "sad_looking_away_tabby", "でも量が多いから\n合計は高い"),
        s(REGI, "realize_wet_cat_stare", "これが\nコストコの魔法か"),
        s(REGI, "think_chin_paw_orange_cat", "レシートを見る"),
        s(REGI, "stare_big_eyes_tabby_kitten", "プルコギ\nサーモンポキ\nチキン\nディナーロール"),
        s(REGI, "despair_dramatic_kitten", "クッキーの缶\n洗剤\nティッシュ\nビール"),
        s(REGI, "blank_black_cat_zoning_out", "家電は\nひとつもない"),
        s(REGI, "happy_hamster_open_arms", "でも\n楽しかった"),
        s(REGI, "stare_interviewer_cat", "出口で\nレシートを\nチェックされる"),
        s(REGI, "sad_looking_away_tabby", "何も悪いことは\nしていないのに\nドキドキする"),
        s(REGI, "drive_driving_cat", "カートのまま\n駐車場へ"),
        s(REGI, "despair_dramatic_kitten", "軽自動車に\n詰めこむ"),
        s(REGI, "blank_black_cat_zoning_out", "テトリスの\n才能が試される"),
        # ---- 家 ----
        s(ROOM, "drive_driving_cat", "車のトランクが\nいっぱいだ", se="whoosh_shu", bgm={"file": JITAKU, "gain": -6, "fade": 1.0}),
        s(ROOM, "stare_tabby_wide_eyes_cat", "家に着いて\n冷蔵庫を開ける"),
        s(ROOM, "despair_dramatic_kitten", "入らない"),
        s(ROOM, "think_chin_paw_orange_cat", "ひとり暮らしの\n冷蔵庫は\nコストコを想定していない"),
        s(ROOM, "work_typing_cat", "プルコギを\n小分けにする"),
        s(ROOM, "sleepy_sleepy_cat", "ディナーロールを\n袋に分けて冷凍する"),
        s(ROOM, "blank_black_cat_zoning_out", "作業だけで\n1時間かかった"),
        s(ROOM, "stare_big_eyes_tabby_kitten", "冷凍庫は\nディナーロールで\nいっぱい"),
        s(ROOM, "think_chin_paw_orange_cat", "氷を作る場所が\nなくなった"),
        s(ROOM, "sad_banana_cat_cry", "アイスも\n入らない"),
        s(ROOM, "realize_wet_cat_stare", "コストコは\n冷凍庫の大きさで\n戦うところだった"),
        s(ROOM_N, "eat_crunchy_cat_luna", "晩ごはんは\nプルコギと\nサーモンポキ", item=BULGOGI),
        s(ROOM_N, "happy_girlfriend_dance_cat", "甘辛いタレが\nごはんに合う", item=BULGOGI),
        s(ROOM_N, "eat_pop_cat", "ポキ丼も\nつやつや", item=POKI),
        s(ROOM_N, "happy_chipi_chapa_cat", "うまい", item=POKI),
        s(ROOM_N, "stare_big_eyes_tabby_kitten", "ロティサリーチキンを\nちぎる", item=CHICKEN),
        s(ROOM_N, "sad_banana_cat_cry", "まだ\n4分の3残っている", item=CHICKEN),
        s(ROOM_N, "sulk_hungry_cat", "満腹だ"),
        s(ROOM_N, "happy_hamster_open_arms", "明日の朝は\nマフィンと\nディナーロール"),
        s(ROOM_N, "eat_crunchy_cat_luna", "明日の昼は\nチキンサンド"),
        s(ROOM_N, "think_chin_paw_orange_cat", "明日の夜は\nプルコギ"),
        s(ROOM_N, "despair_dramatic_kitten", "あさっても\nプルコギ"),
        s(ROOM_N, "think_chin_paw_orange_cat", "冷凍庫を見る"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "ディナーロールが\n33個"),
        s(ROOM_N, "realize_wet_cat_stare", "これを食べきる前に\nまたコストコに\n行きたくなる気がする"),
        s(ROOM_N, "sleepy_old_memories_cat", "テレビの特集を\n思い出す"),
        s(ROOM_N, "happy_hamster_open_arms", "家族で行くと\n楽しい場所だった"),
        s(ROOM_N, "rizz_cat_rizz", "1人で行っても\nちゃんと楽しかった"),
        s(ROOM_N, "sleepy_old_memories_cat", "年会費の元を\n取るために"),
        s(ROOM_N, "excited_hodomoe_city_cat", "コストコは\n独身を\n巨人にする場所だった", se="explosion_dokaan", dur=3.8),
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_09_costco.mp4"), os.path.join(J.HERE, "out", "jidaraku_09_costco_preview"))
