"""自堕落シリーズ #6：30代独身男、ひとりでブロンコビリーに野菜を食べに行く（11/2 ユーザー指定・焼肉きんぐ/スシローと同じ作り）。約8分。

python3 catmeme/jidaraku_06_bronco.py → out/jidaraku_06_bronco.mp4
- 流れ（ユーザー指定）：最近忙しくてバランスの良い食事ができていない → 「そんな時はあそこだ」→ ブロンコビリーへ →
  「俺は今日 このステーキハウスに 野菜を食べに来た」（矛盾していない・緑黄色の森・あとついでに肉もあるらしい）→
  口コミを参考にした感想をまじえて実食 → サラダバーでいろいろな組み合わせを試す → ライスもおかわり → 大満足で帰る →
  オチ「この野菜レストラン 肉が美味かった」
- 口コミ・記事の声（2026年ごろ）：サラダバーは2026年春から「ブロンコビュッフェ」に（夜はカリーと焼き芋も食べ放題）／
  季節ごとに入れかわる期間限定のサラダが楽しみという声／魚沼産コシヒカリを大かまどで炊いたごはん／
  炭焼きのハンバーグはつなぎなしの牛肉100％で肉々しい。値段は書かない（焼肉きんぐ・スシローと同じ）
- 実在の人の名前は出さない。字幕にカギかっこ・句読点なし。「にゃ」なし。単語の途中で改行しない
- 料理の写真は右上に白いふちで出す（item）。写真が届いていない料理は字幕だけ
"""
import os

import cuts_04_leak as L
import jidaraku as J

J.BGS.insert(0, os.path.join(J.HERE, "backgrounds", "jidaraku", "06_bronco"))
J.BGS += [os.path.join(J.HERE, "backgrounds", "jidaraku", d) for d in ("04_sushiro", "05_gokurakuyu")]
OFFICE, ROOM, FRONT, IN, TABLE, BAR, ROAD, ROOM_N = ("b01_office_night", "j01_room", "b02_front", "b03_inside", "b04_table",
                                                     "b05_salad_bar", "b06_road_night", "b07_room_night")
# 絵が届くまでの代わり
J.STANDIN.update({OFFICE: "bg25_office_desk", FRONT: "j02_store_front", IN: "s02_inside", TABLE: "j04_table",
                  BAR: "j06_dessert", ROAD: "g09_road", ROOM_N: "j01_room"})
NIGHT = {OFFICE: 0.85}   # 夜の部屋・帰り道はユーザーの夜の絵なので暗くしない
LOFI = os.path.join(L.BGM, "2_23_AM.mp3")
CATLIFE = os.path.join(L.BGM, "nc102462_Cat_life.mp3")
# 料理の写真（届いた順に backgrounds/jidaraku/06_bronco に置く）
SALAD1, SALAD2, POTESARA, CURRY, IMO, SOUP, RICE, HAMBURG, STEAK, BEER, DESSERT, CURRYSALAD = (
    "f_salad_first", "f_salad_tower", "f_potesara", "f_curry", "f_yakiimo", "f_soup", "f_rice", "f_hamburg", "f_steak",
    "f_beer", "f_dessert", "f_curry_salad")
GARLIC = "f_garlic_rice"   # こぼれるビーフガーリックライス（11/2 ユーザー指定：最初のごはんをこれにグレードアップ）


def cuts():
    def s(*a, **k):   # 長さは place() で字幕の文字数から決める（11/2 ユーザー指定：テンポよく）
        auto = "dur" not in k
        c = J.line(*a, **k)
        c["auto"] = auto
        return c
    return [
        # ---- 忙しかった ----
        s(OFFICE, "work_typing_cat", "金曜の夜7時\nやっと仕事が終わった", bgm={"file": LOFI, "gain": -12}),
        s(OFFICE, "blank_black_cat_zoning_out", "最近忙しかったなぁ……"),
        s(OFFICE, "sleepy_old_memories_cat", "今週の晩ごはんを\n思い出してみる"),
        s(OFFICE, "eat_pop_cat", "月曜 カップ麺"),
        s(OFFICE, "eat_chips_cat", "火曜 コンビニのからあげ弁当"),
        s(OFFICE, "sulk_hungry_cat", "水曜 カップ麺"),
        s(OFFICE, "despair_dramatic_kitten", "木曜 記憶がない\nたぶん何か食べた"),
        s(OFFICE, "realize_wet_cat_stare", "……緑色のものを\n1週間 見ていない\nパソコンの画面くらいだ"),
        s(OFFICE, "sad_looking_away_tabby", "バランスの良い食事も\nできていない……"),
        s(OFFICE, "think_chin_paw_orange_cat", "体が野菜を\n求めて叫んでいる"),
        s(OFFICE, "stare_tabby_wide_eyes_cat", "そんな時は……", se="question_hatena_maou"),
        s(OFFICE, "rizz_cat_rizz", "あそこだ", se="shine_kiraan_maou"),
        # ---- 来店 ----
        s(FRONT, "ride_kitten_bike", "そんなわけで\n今日は", se="whoosh_shu", bgm={"file": L.PURPLE, "gain": -12, "fade": 0.8}),
        s(FRONT, "showoff_gojo_cosplay_cat", "ステーキハウス\nブロンコビリーに来た", se="gong_dora_jaan"),
        s(FRONT, "peek_what_happen_cat", "店の前まで\n炭火で焼ける肉のにおい\n決意が早くもゆらぐ"),
        s(FRONT, "stare_interviewer_cat", "だが 勘ちがいしないでほしい"),
        s(FRONT, "angry_aiming_cat", "俺は今日\nこのステーキハウスに"),
        s(FRONT, "excited_hodomoe_city_cat", "野菜を\n食べに来たのである", se="explosion_dokaan"),
        s(FRONT, "confused_i_dont_know_cat", "矛盾したことを\n言っているようだが"),
        s(FRONT, "calm_black_face_sheep", "何も\n矛盾はしていない"),
        s(FRONT, "read_book_orange_kitten", "こういったステーキレストランには\nサラダバーがあることが多い"),
        s(FRONT, "showoff_gojo_cosplay_cat", "当然このブロンコビリーも\n例外ではない"),
        s(FRONT, "think_bike_front_seat_cat", "ここのサラダバーは\n期間限定のものも多く"),
        s(FRONT, "sleepy_old_memories_cat", "来るたびに\n新たな発見を授けてくれる"),
        s(FRONT, "happy_hamster_open_arms", "緑黄色の\n森なのだ", se="sparkle_kirakira_01"),
        s(FRONT, "slack_nail_filing_cat", "あと ついでに\n肉もあるらしい"),
        # ---- 席へ ----
        s(IN, "stare_interviewer_cat", "お1人さまですね\nこちらへどうぞ〜", se="pinpon_notice"),
        s(IN, "calmdown_dancing_cat", "木のぬくもりのある\n落ち着いた店内"),
        s(IN, "peek_what_happen_cat", "まわりは家族連れと\nカップル"),
        s(IN, "rizz_cat_rizz", "ひとりは俺だけ\nだが問題ない\n探検はいつもひとりだ"),
        s(TABLE, "realize_wet_cat_stare", "俺は今日\n森を探検しに来たのだ"),
        s(TABLE, "read_book_orange_kitten", "メニューを開く"),
        s(TABLE, "stare_tabby_wide_eyes_cat", "ステーキ\nハンバーグ\nたまにステーキ"),
        s(TABLE, "glare_disgusted_cat", "……肉ばっかりだな"),
        s(TABLE, "peek_what_happen_cat", "メニューのすみっこに\nサラダバーの文字"),
        s(TABLE, "sad_banana_cat_cry", "肉の中で\n小さく咲く緑"),
        s(TABLE, "happy_hamster_open_arms", "俺は\nお前に会いに来たんだ"),
        s(TABLE, "think_chin_paw_orange_cat", "サラダバーは\n今はブロンコビュッフェ\nという名前になったらしい"),
        s(TABLE, "surprise_big_pupils_cat", "夜はカリーと焼き芋まで\n食べ放題に入っている", se="pikon"),
        s(TABLE, "dance_three_kittens", "森が広がっていた"),
        s(TABLE, "work_typing_cat", "炭焼きハンバーグと\nブロンコビュッフェのセット"),
        s(TABLE, "think_bike_front_seat_cat", "森に入る前に\n作戦を立てる"),
        s(TABLE, "read_book_orange_kitten", "1皿目は\n葉物で胃を整える"),
        s(TABLE, "stare_big_eyes_tabby_kitten", "2皿目は\n色の濃い野菜"),
        s(TABLE, "confused_i_dont_know_cat", "3皿目は……\nその時の気分で決める"),
        s(TABLE, "showoff_gojo_cosplay_cat", "完ぺきな\n作戦だ"),
        s(TABLE, "think_chin_paw_orange_cat", "ごはんは\n魚沼産コシヒカリ……", item=GARLIC),
        s(TABLE, "stare_tabby_wide_eyes_cat", "……をグレードアップして", item=GARLIC),
        s(TABLE, "showoff_gojo_cosplay_cat", "こぼれる\nビーフガーリックライス", item=GARLIC, se="gong_dora_jaan"),
        s(TABLE, "rizz_cat_rizz", "野菜を食べに来た男の\n最初の選択がこれだ", item=GARLIC),
        s(TABLE, "cocky_dj_cat", "そしてビール\n麦も野菜みたいなものだ", item=BEER),
        s(TABLE, "happy_girlfriend_dance_cat", "金曜の夜だ\n許してほしい"),
        s(TABLE, "eat_crunchy_cat_luna", "ゴクッ……\nくぅ〜！", item=BEER, se="drink_gulp_gokugoku_thirsty_chug"),
        # ---- 森へ ----
        s(BAR, "leave_cat_leaves_home", "肉が焼けるまでに\n森へ向かう", se="whoosh_shu"),
        s(BAR, "surprise_big_pupils_cat", "おお……", se="shine_kiraan_maou"),
        s(BAR, "happy_chipi_chapa_cat", "レタスにキャベツ\nトマトにブロッコリー"),
        s(BAR, "stare_big_eyes_tabby_kitten", "かぼちゃのサラダ\nポテトサラダ"),
        s(BAR, "excited_hodomoe_city_cat", "季節ごとに入れかわる\n期間限定のサラダもある"),
        s(BAR, "read_book_orange_kitten", "口コミでも\n来るたびに変わるのが楽しみ\nという声が多い"),
        s(BAR, "think_chin_paw_orange_cat", "ドレッシングも\n何種類も並んでいる"),
        s(BAR, "sleepy_old_memories_cat", "野菜には\n不思議な力がある"),
        s(BAR, "happy_hamster_open_arms", "見ているだけで\n健康になった気がする"),
        s(BAR, "think_chin_paw_orange_cat", "ブロッコリーは\n森に生える小さな木"),
        s(BAR, "stare_big_eyes_tabby_kitten", "ミニトマトは\n森に実る赤い宝石"),
        s(BAR, "excited_hodomoe_city_cat", "コーンは\n森に落ちた金貨"),
        s(BAR, "calmdown_dancing_cat", "レタスは\n森の地面をおおう\nやわらかいじゅうたん"),
        s(BAR, "blank_black_cat_zoning_out", "……俺は何を\n言っているんだ"),
        s(BAR, "sleepy_sleepy_cat", "やっぱり\n疲れているのかもしれない"),
        s(BAR, "showoff_gojo_cosplay_cat", "まずは基本から"),
        s(BAR, "work_typing_cat", "葉物を山にして\nトマトをのせる", item=SALAD1),
        s(TABLE, "eat_pop_cat", "シャキッ……\n1週間ぶりに聞く音だ", item=SALAD1, se="pikon"),
        s(TABLE, "realize_wet_cat_stare", "……みずみずしい", item=SALAD1),
        s(TABLE, "sad_banana_cat_cry", "1週間ぶりの緑が\n体にしみる", item=SALAD1),
        s(TABLE, "surprise_big_pupils_cat", "胃が\n誰だお前はと\n言っている"),
        s(TABLE, "sleepy_old_memories_cat", "細胞が\nよろこんでいる"),
        s(TABLE, "read_book_orange_kitten", "1日に食べたい野菜は\n350gと言われている"),
        s(TABLE, "realize_wet_cat_stare", "今週の俺は\nたぶん20gくらい"),
        s(TABLE, "angry_aiming_cat", "今日ここで\n1週間ぶんを取り返す"),
        s(TABLE, "rizz_cat_rizz", "これは食事ではない\n修行だ"),
        # ---- 肉が来る ----
        s(TABLE, "stare_tabby_wide_eyes_cat", "そこへ……\nジュウウウ", se="explosion_dokaan", item=HAMBURG),
        s(TABLE, "surprise_big_pupils_cat", "炭焼きハンバーグが\n来てしまった", item=HAMBURG),
        s(TABLE, "glare_disgusted_cat", "……いや\n今日の主役は野菜だ", item=HAMBURG),
        s(TABLE, "think_chin_paw_orange_cat", "でも冷めたら\nハンバーグに失礼だ", item=HAMBURG),
        s(TABLE, "eat_crunchy_cat_luna", "ひと口だけ\nこれは味見だ 味見", item=HAMBURG),
        s(TABLE, "realize_wet_cat_stare", "……肉々しい", item=HAMBURG),
        s(TABLE, "surprise_big_pupils_cat", "続けて\nビーフガーリックライス", item=GARLIC),
        s(TABLE, "stare_big_eyes_tabby_kitten", "鉄板の上で\n牛そぼろと卵黄が\nごはんからこぼれている", item=GARLIC),
        s(TABLE, "work_typing_cat", "まぜると\nジュウウウ……", item=GARLIC, se="explosion_bokaan"),
        s(TABLE, "eat_crunchy_cat_luna", "ガーリックの香りが\n一気に立ちのぼる", item=GARLIC),
        s(TABLE, "sad_banana_cat_cry", "……うまい\n野菜はどこへ行った", item=GARLIC),
        s(TABLE, "read_book_orange_kitten", "口コミでは\nつなぎを使わない\n牛肉100％らしい", item=HAMBURG),
        s(TABLE, "happy_hamster_open_arms", "炭火の香りが\n鼻にぬける", item=HAMBURG),
        s(TABLE, "angry_aiming_cat", "……あぶない\n今日は野菜の日だ"),
        s(TABLE, "rizz_cat_rizz", "肉は\n森の入り口にすぎない"),
        # ---- 組み合わせ研究 ----
        s(BAR, "cocky_dj_cat", "ここからは\n組み合わせの研究だ", se="gong_match_start", bgm={"file": CATLIFE, "gain": -12, "fade": 0.8}),
        s(BAR, "work_typing_cat", "その1\nかぼちゃサラダと\nポテトサラダの二刀流", item=POTESARA),
        s(TABLE, "eat_pop_cat", "甘いのと\nしょっぱいのが交互に来る", item=POTESARA),
        s(TABLE, "happy_girlfriend_dance_cat", "これは\n終わらないやつだ", item=POTESARA),
        s(BAR, "work_typing_cat", "その2\nスープ", item=SOUP),
        s(TABLE, "sleepy_old_memories_cat", "あったかいスープで\nひと休み\n森の中の温泉だ", item=SOUP),
        s(TABLE, "calm_black_face_sheep", "冷たい野菜のあとの\nスープは正義", item=SOUP),
        s(BAR, "stare_big_eyes_tabby_kitten", "その3\nカリー", item=CURRY),
        s(BAR, "confused_i_dont_know_cat", "カリーは\n野菜なのか？", item=CURRY),
        s(BAR, "showoff_gojo_cosplay_cat", "玉ねぎもにんじんも\nとけているはずだ\nつまり野菜だ", item=CURRY),
        s(TABLE, "work_typing_cat", "白いごはんを少しもらって\nカリーをかける", item=CURRY),
        s(TABLE, "eat_crunchy_cat_luna", "……うまい", item=CURRY),
        s(TABLE, "sleepy_old_memories_cat", "スパイスの奥に\n野菜のあまみがある", item=CURRY),
        s(TABLE, "realize_wet_cat_stare", "やはりカリーは\n野菜料理だった", item=CURRY),
        s(TABLE, "surprise_big_pupils_cat", "その4\nカリーの上に\nサラダをのせる", item=CURRYSALAD, se="question_mark_pop_confused_huh"),
        s(TABLE, "dance_wop_cat", "ポテサラカリー\nキャベツの食感", item=CURRYSALAD),
        s(TABLE, "laugh_laughing_dog", "家では絶対に\nやらない食べ方", item=CURRYSALAD),
        s(TABLE, "happy_chipi_chapa_cat", "これが\n森の遊び方だ", item=CURRYSALAD),
        s(BAR, "work_typing_cat", "その5\nドレッシングの食べくらべ"),
        s(BAR, "eat_pop_cat", "ごまは\nなんでも美味しくする魔法"),
        s(BAR, "think_chin_paw_orange_cat", "和風はさっぱり\n肉のあとに合う"),
        s(BAR, "happy_girlfriend_dance_cat", "フレンチは\nトマトとの相性が最高"),
        s(BAR, "stare_tabby_wide_eyes_cat", "その6\nブロッコリーに\nポテサラをのせる"),
        s(BAR, "happy_chipi_chapa_cat", "緑と白の\nハーモニー"),
        s(BAR, "surprise_big_pupils_cat", "その7\nスープにコーンを入れる"),
        s(BAR, "showoff_gojo_cosplay_cat", "コーンスープ\n自作完成"),
        s(BAR, "stare_tabby_wide_eyes_cat", "その8\n焼き芋", item=IMO),
        s(TABLE, "eat_pop_cat", "ねっとり甘い\nもうスイーツだろこれ", item=IMO),
        s(TABLE, "think_chin_paw_orange_cat", "芋は野菜\nだから問題ない", item=IMO),
        s(TABLE, "realize_wet_cat_stare", "焼き芋とポテサラ\n芋が芋を呼ぶ", item=IMO),
        s(BAR, "work_typing_cat", "そして\n山盛りサラダ2皿目", item=SALAD2),
        s(BAR, "dance_koto_nai_cat", "ドレッシングを\n3種類かけ分ける", item=SALAD2),
        s(TABLE, "happy_hamster_open_arms", "1皿で3回楽しめる\nサラダのテーマパーク", item=SALAD2),
        # ---- ごはんおかわり ----
        s(TABLE, "stare_big_eyes_tabby_kitten", "……あれ\nごはんがない", se="pi", bgm={"file": os.path.join(L.BGM, "候補_a658b05f.mp3"), "gain": -15, "fade": 0.8}),
        s(TABLE, "think_bike_front_seat_cat", "ハンバーグを\nもうひと口"),
        s(TABLE, "realize_wet_cat_stare", "肉汁と炭火の香りが\nごはんを呼んでいる"),
        s(TABLE, "work_typing_cat", "ごはんを\nおかわりする", item=RICE, se="pikon"),
        s(TABLE, "showoff_gojo_cosplay_cat", "大かまどで炊いた\nつやつやの白いごはん", item=RICE),
        s(TABLE, "eat_crunchy_cat_luna", "ハンバーグと\nいっしょに……", item=RICE),
        s(TABLE, "sad_banana_cat_cry", "うまい……", item=RICE),
        s(TABLE, "glare_disgusted_cat", "いや\nサラダも食べる"),
        s(TABLE, "dance_maxwell_cat", "サラダ\nごはん\nハンバーグ\nサラダ"),
        s(TABLE, "happy_girlfriend_dance_cat", "完ぺきな\nローテーション"),
        s(TABLE, "think_bike_front_seat_cat", "白いごはんにも\nサラダは合う"),
        s(TABLE, "work_typing_cat", "ごはんの上に\nキャベツをのせる"),
        s(TABLE, "dance_wop_cat", "これはもう\nサラダ丼だ"),
        s(TABLE, "yell_orange_fat_cat", "ごはん\n2回目のおかわり", item=RICE),
        s(TABLE, "dance_edm_cat", "もう止まらない\n箸がブレーキを忘れた"),
        # ---- ステーキ追加 ----
        s(TABLE, "sleepy_old_memories_cat", "不思議なことに"),
        s(TABLE, "realize_wet_cat_stare", "野菜を食べるほど\n肉が食べたくなる"),
        s(TABLE, "think_chin_paw_orange_cat", "これは体が\nバランスをとろうと\nしているのだ"),
        s(TABLE, "showoff_gojo_cosplay_cat", "つまり肉を食べるのは\n健康のため"),
        s(TABLE, "stare_tabby_wide_eyes_cat", "となりのテーブルに\nステーキが運ばれていく", se="explosion_bokaan"),
        s(TABLE, "peek_what_happen_cat", "ジュウウウ……"),
        s(TABLE, "think_chin_paw_orange_cat", "……今日は\n野菜の日だ"),
        s(TABLE, "despair_dramatic_kitten", "野菜の日\nなんだけど……"),
        s(TABLE, "work_typing_cat", "ステーキを\n追加した", item=STEAK, se="explosion_dokaan"),
        s(TABLE, "surprise_big_pupils_cat", "炭火で焼いた\n香ばしい表面", item=STEAK),
        s(TABLE, "eat_crunchy_cat_luna", "噛むほどに\nうまみが出てくる", item=STEAK),
        s(TABLE, "happy_hamster_open_arms", "そこに\n山盛りのサラダ", item=STEAK),
        s(TABLE, "rizz_cat_rizz", "肉と野菜を\n交互に食べれば\nプラマイゼロだ"),
        # ---- 限界 ----
        s(TABLE, "sleepy_old_memories_cat", "1時間半がたった\n店員さんに顔を\n覚えられた気がする", se="pi", bgm={"file": LOFI, "gain": -14, "fade": 1.0}),
        s(TABLE, "sulk_hungry_cat", "お腹がパンパンだ\nベルトの穴が\nひとつ引っ越した"),
        s(TABLE, "confused_i_dont_know_cat", "サラダで\n満腹になったのか"),
        s(TABLE, "realize_wet_cat_stare", "ガーリックライスと\nごはん2杯の\nせいなのか"),
        s(TABLE, "blank_black_cat_zoning_out", "考えるのを\nやめた"),
        s(BAR, "stare_big_eyes_tabby_kitten", "でも\nデザートも\nビュッフェに入っている", item=DESSERT),
        s(BAR, "glare_disgusted_cat", "デザートは\n別腹って言うしな", item=DESSERT),
        s(TABLE, "eat_pop_cat", "ひんやり甘い\n口の中がさっぱりする", item=DESSERT),
        s(TABLE, "think_chin_paw_orange_cat", "フルーツも\n野菜の親戚みたいなものだ"),
        s(TABLE, "eat_crunchy_cat_luna", "オレンジ\nパイナップル\nゼリー"),
        s(TABLE, "glare_disgusted_cat", "ゼリーは\n……野菜ではない"),
        s(TABLE, "happy_chipi_chapa_cat", "でも\nおかわりした"),
        s(TABLE, "sleepy_sleepy_cat", "胃袋は\nさっぱりしない"),
        s(TABLE, "stare_interviewer_cat", "最後に\n温かいスープをもう1杯", item=SOUP),
        s(TABLE, "calm_black_face_sheep", "……整った\nサウナより整った", item=SOUP, se="chiin_01"),
        # ---- 会計・帰り ----
        s(IN, "money_counting_orange_cat", "お会計をして店を出る\nお腹が重くて\nドアも重い", se="whoosh_shu", bgm={"file": os.path.join(L.BGM, "手紙のさよなら.mp3"), "gain": -14, "fade": 1.0}),
        s(IN, "stare_interviewer_cat", "ありがとうございました〜"),
        s(ROAD, "leave_cat_leaves_home", "夜風が\n気持ちいい"),
        s(ROAD, "happy_hamster_open_arms", "大満足だ"),
        s(ROAD, "sleepy_old_memories_cat", "1週間ぶんの野菜を\n取り返した気がする"),
        s(ROAD, "happy_hamster_open_arms", "サラダ2皿は\n人生で最多かもしれない"),
        s(ROAD, "sleepy_old_memories_cat", "胃袋の中では\n野菜と肉が\n仲よく暮らしている"),
        s(ROAD, "think_bike_front_seat_cat", "今日食べたものを\n思い出してみる"),
        s(ROAD, "read_book_orange_kitten", "サラダ2皿\nかぼちゃとポテサラ\n焼き芋"),
        s(ROAD, "stare_big_eyes_tabby_kitten", "カリー\nスープ2杯\nデザート"),
        s(ROAD, "realize_wet_cat_stare", "ガーリックライス\nごはん2杯\nハンバーグ ステーキ"),
        s(ROAD, "despair_dramatic_kitten", "……"),
        s(ROOM_N, "sleep_sleeping_cat", "家に着いて\nベッドに倒れこむ", se="whoosh_shu"),
        s(ROOM_N, "peek_what_happen_cat", "冷蔵庫を開ける"),
        s(ROOM_N, "sad_looking_away_tabby", "野菜は\nひとつもない"),
        s(ROOM_N, "blank_black_cat_zoning_out", "あるのは\nマヨネーズと\nビールだけ"),
        s(ROOM_N, "rizz_cat_rizz", "冷蔵庫の砂漠化も\n環境問題で\n取り上げるべきだ"),
        s(ROOM_N, "slack_nail_filing_cat", "今日の感想を\nひとことで言うなら"),
        s(ROOM_N, "stare_tabby_wide_eyes_cat", "野菜を食べに\nステーキハウスに行った"),
        s(ROOM_N, "think_chin_paw_orange_cat", "緑黄色の森は\n最高だった"),
        s(ROOM_N, "showoff_gojo_cosplay_cat", "だが\nひとつだけ言わせてほしい"),
        s(ROOM_N, "surprise_big_pupils_cat", "この野菜レストラン", se="question_hatena_maou"),
        s(ROOM_N, "excited_hodomoe_city_cat", "肉が\n美味かった", se="explosion_dokaan", dur=3.8),
        J.end_card(),
    ]


def place(cs):
    J.auto_tempo(cs)
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
        J.run(cs, os.path.join(J.HERE, "out", "jidaraku_06_bronco.mp4"), os.path.join(J.HERE, "out", "jidaraku_06_bronco_preview"))
