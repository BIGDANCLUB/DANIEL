# 【寸劇】外国人旅行者が日本で驚いた3つのこと　財布が戻る／7分で新幹線がピカピカ／ビッグマックが“半額”（原稿 v1）

- 調査・台本: 別セッション（猫ミーム時事ネタ分析）。番号は制作側で振る
- 形式: **「寸劇」シリーズ**（README・`docs/sungeki_reference.md`・`story_style.py`・見本 `story_18_demo.py`）。書き方は `sungeki_semicon.md` と同じ
- ジャンル: 「日本と世界」型。1人の旅行者が日本で3つの驚きに出会う**3話構成**（候補 7・4・9 を1本に）
- **想定尺: 約8分（約130カット）**。目安：冒頭0:40／第1話2:20／第2話2:20／第3話2:00／締め0:40
- 書き方: `intro「」`（黒＋白文字・音なし）／`photo[写真名]「」`（黒＋写真＋字幕・BGM 続く）／`Scene[背景名]（役名=位置）`（役名は上に固定、札に小さい国旗）／`say`・`add`／`zoom L「」(白/黄/赤, 集中線, 吹き出し=イラスト名)`／`zoom L mid「」「」`／`ending`。［猫］は仮
- 各話の頭に `intro` で「驚き その1」などの区切りを入れる

## ルール（必ず守る）
- 冒頭で「再構成したお話」と書く。登場人物はすべて架空（実在の人物・実在の会社の社員を猫で演じない）。会社名（JR東日本テクノハートTESSEI・日本マクドナルド）は**語りの事実説明の中だけ**
- 第2話の清掃チームの言葉は作り話の台詞（実在の人の発言としない）
- 第3話は「日本すごい」で終わらせず、**30〜40代の“お金”の気づき**（日本が安くなった＝給料が上がっていない）につなげる。ただし暗くしすぎない
- 他国をバカにしない。旅行者は“素直に驚いて感心する人”
- 数字は確認メモどおり。不確かなものは「と言われている」「とも」
- 語尾に「にゃ」なし。単語の途中で改行しない。AIで作った背景・写真・イラストは概要欄に

## 配役
| 役名（札） | 出る話 | キャラ | 猫の例 |
|---|---|---|---|
| アメリカの旅行者 🇺🇸 | 全部 | 初めての日本。リアクションが大きい | surprise_big_pupils_cat／dance_edm_cat／despair_dramatic_kitten／stare_big_eyes_tabby_kitten |
| 日本の友だち 🇯🇵 | 全部 | 30代の会社員。案内役。ちょっと疲れている | work_typing_cat／slack_nail_filing_cat／sulk_hungry_cat |
| 交番のおまわりさん 🇯🇵 | 第1話 | 落ち着いていて親切 | talk_orange_white_sitting_cat／calmdown_dancing_cat |
| 清掃チームのリーダー 🇯🇵 | 第2話 | きびきびしていて誇り高い | stare_interviewer_cat／showoff_gojo_cosplay_cat |
| ハンバーガー店の店員 🇯🇵 | 第3話 | 明るい | wave_waving_cat／happy_chipi_chapa_cat |

## BGM
- intro は音なし。第1話は少しハラハラ→ほっこり、第2話はテンポよく、第3話は明るめ→少ししんみり、締めは明るく

---

## 0. 冒頭（約40秒）
intro「これは、日本を訪れた外国人旅行者が驚いたと言われる」
intro「3つの出来事をもとに再構成したお話です。」
photo[ph01_airport_arrival]「日本に住む私たちには、何でもない毎日。」
photo[ph01_airport_arrival]「でも、海の向こうから来た人には、\n信じられない光景に見えることがあります。」
Scene[bg01_airport]（アメリカの旅行者=L, 日本の友だち=R）
say L「ついに来たぞ、日本！！」［dance_edm_cat］
say R「ようこそ。1週間、案内するよ」［work_typing_cat］
say L「“日本で驚いたこと”を3つ集めて、国に帰って自慢するんだ！」［happy_chipi_chapa_cat］
say R「3つも驚くかなあ。ふつうの国だよ？」［slack_nail_filing_cat］
zoom L「ぜったい驚く！！」(黄)［cocky_dj_cat］

## 1. 驚き その1　落とした財布が、戻ってくる（約2分20秒）
intro「驚き その1　落とした財布」
Scene[bg02_shibuya_crossing]（アメリカの旅行者=L, 日本の友だち=R）
say L「すごい人だ！　写真撮ろ！」［dance_trending_cat］
add L「次はあっち！　その次はこっち！」
say R「ちょっと待って、はしゃぎすぎ……」［sulk_hungry_cat］
（間）
say L「……あれ？」［peek_what_happen_cat］
add L「……ない」
add L「財布が、ない！！」
zoom L「現金も、カードも、パスポートのコピーも全部入ってたのに！！」(赤, 集中線)［despair_dramatic_kitten］
say R「落ち着いて。まず交番に行こう」［work_typing_cat］
zoom L「戻ってくるわけないでしょ！！　現金入りだよ！？」(黄)［rage_talking_cat］
say R「……まあ、行ってみようよ」［slack_nail_filing_cat］

Scene[bg03_koban]（アメリカの旅行者=L, 交番のおまわりさん=C, 日本の友だち=R）
say C「どうされましたか？」［talk_orange_white_sitting_cat］
say L「財布を……落として……」［sad_banana_cat_cry］
say C「どんな財布ですか？」［talk_orange_white_sitting_cat］
say L「茶色で……猫のキーホルダーが付いてて……」［sulk_hungry_cat］
say C「……もしかして、これですか？」［calmdown_dancing_cat］
zoom L「あった！！！」(赤, 集中線, 吹き出し=il_wallet)［surprise_big_pupils_cat］
say L「お金……」［stare_big_eyes_tabby_kitten］
add L「……そのまま入ってる……」
zoom L mid「な、なんで…」「なんで戻ってくるの…」［realize_wet_cat_stare］
say C「30分ほど前に、拾った方が届けてくださいました」［talk_orange_white_sitting_cat］
say R「ね、言ったでしょ」［cocky_dj_cat］

photo[ph02_koban_night]「2025年、東京で警察に届けられた現金は、およそ45億円。\n4年連続で過去最高でした。（警視庁）」
photo[ph02_koban_night]「そのうち約7割、およそ32億円が、落とし主のもとに戻っています。」
photo[ph02_koban_night]「落とし主が見つかると、拾った人は\n落とし物の価値の5〜20％のお礼を受け取れる決まりもあります。」

Scene[bg03_koban]（アメリカの旅行者=L, 交番のおまわりさん=C, 日本の友だち=R）
say L「拾ってくれた人に、お礼をしたい！」［happy_chipi_chapa_cat］
say C「では、ご連絡先をお伝えしておきますね」［talk_orange_white_sitting_cat］
say L「国だったら、まず戻ってこないのに……」［sleepy_old_memories_cat］
say R「日本でも、全部戻るわけじゃないけどね」［slack_nail_filing_cat］
add R「でも、“届けるのが当たり前”って思ってる人は多いかも」
zoom L「驚き その1、決定！！」(黄)［dance_edm_cat］

## 2. 驚き その2　新幹線が、7分でピカピカになる（約2分20秒）
intro「驚き その2　7分間の奇跡」
Scene[bg04_shinkansen_platform]（アメリカの旅行者=L, 日本の友だち=R）
say L「新幹線だ！　かっこいい！！」［dance_edm_cat］
say R「あの電車、今着いたやつに、12分後に乗るよ」［work_typing_cat］
say L「12分！？　さっきまでお客さん乗ってたのに？」［huh_huh_cat］
add L「掃除、間に合うわけないでしょ」
say R「……見てて」［slack_nail_filing_cat］

Scene[bg04_shinkansen_platform]（アメリカの旅行者=L, 清掃チームのリーダー=C, 日本の友だち=R）
say C「到着しました。みなさん、よろしくお願いします！」［stare_interviewer_cat］
（清掃チームが並んで、電車に向かっておじぎ）
zoom L「電車に、おじぎした！？」(黄)［surprise_big_pupils_cat］
say C「お客さまが降りるのを待って……開始！」［showoff_gojo_cosplay_cat］
say L「座席を全部回して……」［stare_big_eyes_tabby_kitten］
add L「ゴミを集めて……」
add L「テーブルを拭いて……」
add L「トイレまで……」
say C「完了です！」［stare_interviewer_cat］
zoom L「は、速すぎる！！」(赤, 集中線)［surprise_big_pupils_cat］

photo[ph03_cleaning_team]「新幹線の折り返しの時間は、およそ12分。」
photo[ph03_cleaning_team]「そのうちの約7分で、20人あまりのチームが\n客席からトイレまでをきれいにしていきます。」
photo[ph03_cleaning_team]「“7分間の奇跡”とも呼ばれ、アメリカのハーバード・ビジネス・スクールの\n教材にも取り上げられました。」
photo[ph03_cleaning_team]「かつては働く人の気持ちも沈みがちだったこの職場は、\n2000年代の半ばからの改革で、誇りを持てる職場に変わったと言われています。」

Scene[bg04_shinkansen_platform]（アメリカの旅行者=L, 清掃チームのリーダー=C, 日本の友だち=R）
say L「どうして、そこまでできるの？」［think_bike_front_seat_cat］
say C「私たちの仕事は、掃除だけじゃありません」［showoff_gojo_cosplay_cat］
add C「次に乗るお客さまの、旅の始まりをつくる仕事です」
zoom R mid「……旅の始まり」「……かっこいい」［realize_wet_cat_stare］
say R「同じ会社員として、ちょっと泣きそう」［sad_banana_cat_cry］
zoom L「驚き その2、決定！！」(黄)［dance_edm_cat］

## 3. 驚き その3　ビッグマックが“半額”（約2分）
intro「驚き その3　ハンバーガーの値段」
Scene[bg05_burger_shop]（アメリカの旅行者=L, ハンバーガー店の店員=C, 日本の友だち=R）
say C「いらっしゃいませ！」［wave_waving_cat］
say L「ビッグマックください！」［happy_chipi_chapa_cat］
say C「500円です！」［wave_waving_cat］
say L「……500円って、ドルでいくら？」［think_bike_front_seat_cat］
say R「3ドルちょっとかな」［work_typing_cat］
zoom L「安っ！！！」(赤, 集中線)［surprise_big_pupils_cat］
say L「アメリカの半分くらいじゃない！？」［dance_edm_cat］
say R「え……安いの……？」［huh_huh_cat］
add R「2月に値上げしたばっかりなんだけど……」

photo[ph04_burger_world]「日本のビッグマックは、2026年2月に480円から500円になりました。」
photo[ph04_burger_world]「それでも、世界の値段と比べる“ビッグマック指数”では、\n2026年1月の調査で、円はドルに対して約5割“割安”とされています。」
photo[ph04_burger_world]「2024年7月の調査では、日本のビッグマックの値段は世界で44番目。\nスイスでは、1個1,200円を超えるとも言われています。」

Scene[bg05_burger_shop]（アメリカの旅行者=L, 日本の友だち=R）
say L「日本、安くて、きれいで、財布も戻ってくる」［happy_chipi_chapa_cat］
add L「天国じゃん！」
say R「……旅行で来る人には、ね」［sulk_hungry_cat］
say L「え？」［huh_huh_cat］
say R「ハンバーガーが世界より安いってことは……」［blank_black_cat_zoning_out］
add R「わたしたちの給料も、世界より安いってことなんだよね……」
zoom R mid「海外旅行…」「高すぎて…」「行けない…」［sad_banana_cat_cry］
say L「……そっか」［sleepy_old_memories_cat］
add L「じゃあ今度は、わたしがアメリカで案内するよ！　泊まるとこも用意する！」
zoom R「神！！」(赤, 集中線)［joy_happy_happy_happy_cat］
zoom L「驚き その3、決定！！」(黄)［dance_edm_cat］

## 4. 締め（約40秒）
photo[ph05_sunset_tokyo]「落とした財布が戻る国。7分でピカピカになる新幹線。\nそして、世界の半分ほどの値段のハンバーガー。」
photo[ph05_sunset_tokyo]「外から見た“日本の驚き”には、\nわたしたちが誇っていいことと、少し考えたいことが、\n一緒に入っているのかもしれません。」
Scene[bg06_rainbow_meadow]（アメリカの旅行者=L, 日本の友だち=C, 交番のおまわりさん=R）
say L「3つ集まった！　国に帰ったら、みんなに話す！」［dance_edm_cat］
say C「次は、財布落とさないでね」［slack_nail_filing_cat］
say R「落としたら、また交番へどうぞ」［talk_orange_white_sitting_cat］
ending［happy_girlfriend_dance_cat］

---

## 背景・写真・イラスト（AIで作る・PHOTO:/ILLUST:）
※実在の会社のロゴ・制服・車両の塗装・店の看板に似せない。人物の顔ははっきり描かない
- ph01_airport_arrival（PHOTO）… 空港の到着ロビー、スーツケースを引く旅行者（後ろ姿）
- ph02_koban_night（PHOTO）… 夜の交番の外観（看板の文字なし）
- ph03_cleaning_team（PHOTO）… 新幹線っぽい白い車両の横に、ユニフォームの清掃スタッフが並ぶ（後ろ姿・ロゴなし）
- ph04_burger_world（ILLUST）… いろいろな国旗の前にハンバーガーが並ぶイラスト（値段は字幕で出す）
- ph05_sunset_tokyo（PHOTO）… 夕焼けの東京の街並み
- il_wallet（ILLUST・吹き出し用）… 猫のキーホルダー付きの茶色い財布
- bg01_airport（ILLUST）… 空港のロビー
- bg02_shibuya_crossing（ILLUST）… 人の多い交差点（特定の看板・ビルに似せすぎない）
- bg03_koban（ILLUST）… 交番の中、机と地図
- bg04_shinkansen_platform（ILLUST）… 新幹線っぽい車両の止まるホーム
- bg05_burger_shop（ILLUST）… ハンバーガー店のカウンター（ロゴなし）
- bg06_rainbow_meadow … 見本の st05_rainbow_meadow を使い回し可

## 確認メモ（2026-10-21 確認）
- 落とし物：2025年に警視庁に届けられた現金 約45億円（4,508,824,075円、前年比0.5%増）、4年連続で過去最高。処理分のうち約32億2,958万円が落とし主に返還（約7割）（警視庁「遺失物取扱状況」・nippon.com・英字報道）
- 報労金：落とし主が判明したら価値の5〜20%（施設内で拾った場合は施設と折半で2.5〜10%）、3か月で落とし主が見つからなければ拾った人のものに（警察庁）
- 7分間の奇跡：折り返し約12分、原則23名程度のチームが7分で客席・デッキ・トイレまで清掃（トレたび）。ハーバード・ビジネス・スクールの教材に（ニューズウィーク日本版ほか。教材になった年は資料で食い違うので**年は出さない**）。2006年ごろからの改革で、もとは「3K」職場で士気も低かった（報道）。運営は JR東日本テクノハートTESSEI（旧名を含め、動画では社名を出すなら語りだけ）
- 「電車に向かっておじぎ」「旅の始まりをつくる仕事」：寸劇の演出・作り話の台詞（実在の人の発言としない）
- ビッグマック：2026年2月25日から日本のビッグマック単品500円（480円から20円値上げ、初の500円台。Impress Watch・各報道）
- ビッグマック指数：2026年1月の The Economist の指数で、円はドルに対して約50%割安（statbase・bigmacindex.app などの二次資料で確認）→ **公開前に The Economist の原表で確認**。2024年7月版で日本は44位・−43.9%（ファイナンシャルフィールド）。スイスは1個1,207円（2025年、1ドル151.08円で計算）→「1,200円を超えるとも」
- 「500円＝3ドルちょっと」：1ドル約160円で計算（為替は公開時に確認）。「アメリカの半分くらい」は指数の約5割割安と合わせた表現
- 「ハンバーガーが安い＝給料も安い」は寸劇の台詞としての一般的な説明（指数は購買力の目安で、為替や賃金の比較そのものではない）

## 出典
- 警視庁 遺失物取扱状況 https://www.keishicho.metro.tokyo.lg.jp/about_mpd/jokyo_tokei/kakushu/kaikei.html
- nippon.com（都内の現金の落とし物）https://www.nippon.com/ja/japan-data/h02746/
- 警察庁（落とし物のお礼）https://www.npa.go.jp/bureau/soumu/ishitsubutsu/otoshimono/index.html
- トレたび（7分間の奇跡）https://www.toretabi.jp/railway_info/jikoku-2508.html
- ニューズウィーク日本版 https://www.newsweekjapan.jp/articles/-/19007
- Impress Watch（マクドナルド値上げ・ビッグマック500円）https://www.watch.impress.co.jp/docs/news/2088070.html
- statbase（Big Mac Index 2026年1月）https://statbase.org/datasets/indexes-and-ratings/bigmac-index/
- ファイナンシャルフィールド（ビッグマック指数）https://financial-field.com/living/entry-208598
