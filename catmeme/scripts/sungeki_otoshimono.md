# 【寸劇】落とした財布が戻ってくる国　東京で1年に届けられた現金は45億円（原稿 v1）

- 調査・台本: 別セッション（猫ミーム時事ネタ分析）。番号は制作側で振る
- 形式: **「寸劇」シリーズ**（README・`docs/sungeki_reference.md`・`story_style.py`・見本 `story_18_demo.py`）。書き方は `sungeki_semicon.md` と同じ
- ジャンル: 「日本と世界」型（なぜ日本だけ？）
- **想定尺: 約8分（約130カット）**。目安：冒頭0:40／1 0:50／2 0:40／3 1:20／4 0:50／5 1:10／6 1:00／7 0:40／締め0:50
- 書き方: `intro「」`（黒＋白文字・音なし）／`photo[写真名]「」`（黒＋写真＋字幕・BGM）／`Scene[背景名]（役名=位置）`（役名は上に固定、札に小さい国旗）／`say`・`add`／`zoom L「」(白/黄/赤, 集中線, 吹き出し=イラスト名)`／`zoom L mid「」「」`／`ending`。［猫］は仮

## ルール（必ず守る）
- 冒頭で「再構成したお話」と書く。登場人物はすべて架空
- 他国をバカにしない（「アメリカでは盗まれる」などと言わない）。旅行者は「前の旅行で財布が戻らなかった経験がある人」まで
- 「日本では必ず戻る」と言い切らない（日本でも全部は戻らない、を入れる）
- 数字は確認メモどおり。世界の財布実験は「日本は対象外」を必ず言う
- 語尾に「にゃ」なし。単語の途中で改行しない。AIで作った背景・写真・イラストは概要欄に

## 配役
| 役名（札） | キャラ | 猫の例 |
|---|---|---|
| アメリカの旅行者 🇺🇸 | 初めての日本。リアクション大 | dance_edm_cat／despair_dramatic_kitten／surprise_big_pupils_cat |
| 日本の友だち 🇯🇵 | 30代の会社員。案内役 | work_typing_cat／slack_nail_filing_cat／cocky_dj_cat |
| 交番のおまわりさん 🇯🇵 | 落ち着いて親切 | talk_orange_white_sitting_cat／calmdown_dancing_cat |
| 拾った高校生 🇯🇵 | 部活帰り。照れ屋 | meow_gray_white_kitten／itchy_kitten_butt |

---

## 0. 冒頭（約40秒）
intro「これは、日本を訪れた外国人旅行者が驚いたと言われる」
intro「“ある出来事”をもとに再構成したお話です。」
photo[ph01_tokyo_crowd]「人であふれる東京の街。」
photo[ph01_tokyo_crowd]「ここで財布を落としたら、あなたは\n“もう戻ってこない”と思いますか？」

## 1. はしゃぐ旅行者（約50秒）
Scene[bg01_shibuya]（アメリカの旅行者=L, 日本の友だち=R）
say L「これが有名な交差点！！」［dance_edm_cat］
add L「写真！　動画！　自撮り！」
say R「ちょっと、前見て歩いて……」［slack_nail_filing_cat］
say L「次はクレープ！　その次はガチャガチャ！」［happy_chipi_chapa_cat］
say R「元気だなあ……こっちは月曜から仕事なのに……」［sulk_hungry_cat］
say L「ほら、早く早く！」［dance_trending_cat］

## 2. 財布がない（約40秒）
Scene[bg01_shibuya]（アメリカの旅行者=L, 日本の友だち=R）
say L「よし、クレープ買お……」［happy_chipi_chapa_cat］
add L「……あれ？」
add L「……財布が、ない」
zoom L「財布が、ない！！！」(赤, 集中線)［despair_dramatic_kitten］
say L「現金も！　カードも！　ホテルのカードキーも！」［rage_talking_cat］
say R「落ち着いて。最後に使ったのは？」［work_typing_cat］
say L「さっきのガチャガチャ……」［sad_banana_cat_cry］
zoom L mid「終わった…」「旅行…」「終わった…」［blank_black_cat_zoning_out］

## 3. 交番へ（約1分20秒）
say R「とりあえず交番に行こう」［work_typing_cat］
zoom L「交番？　行ってどうするの！？」(黄)［huh_huh_cat］
say L「前に別の国を旅行したとき、財布を落としたけど……」［sleepy_old_memories_cat］
add L「戻ってこなかったよ」
say R「……まあ、行ってみようよ」［slack_nail_filing_cat］
Scene[bg02_koban]（アメリカの旅行者=L, 交番のおまわりさん=C, 日本の友だち=R）
say C「どうされましたか？」［talk_orange_white_sitting_cat］
say L「財布を……落としました……」［sad_banana_cat_cry］
say C「では“遺失届”を出しましょう。どんな財布ですか？」［talk_orange_white_sitting_cat］
say L「茶色で、猫のキーホルダーが付いてます」［sulk_hungry_cat］
say C「中身は？」［talk_orange_white_sitting_cat］
say L「現金が3万円くらいと、カードが2枚と……」［sulk_hungry_cat］
say C「……今のところ、それらしい届けはありませんね」［calmdown_dancing_cat］
zoom L「ほらああああ！！」(赤, 集中線)［despair_dramatic_kitten］
say C「届いたら、すぐにご連絡しますので」［talk_orange_white_sitting_cat］
intro「——1時間後」
Scene[bg03_cafe]（アメリカの旅行者=L, 日本の友だち=R）
say L「カード止めなきゃ……ホテルにも連絡しなきゃ……」［sad_banana_cat_cry］
say R「……あ、電話。交番からだ」［work_typing_cat］
say R「“届きました”って」［cocky_dj_cat］
zoom L「えっ！？」(黄)［surprise_big_pupils_cat］

## 4. 戻ってきた（約50秒）
Scene[bg02_koban]（アメリカの旅行者=L, 交番のおまわりさん=C, 日本の友だち=R）
say C「こちらで、お間違いないですか？」［calmdown_dancing_cat］
zoom L「わたしの財布！！！」(赤, 集中線, 吹き出し=il_wallet)［surprise_big_pupils_cat］
say L「……お金……」［stare_big_eyes_tabby_kitten］
add L「……3万円、そのまま……」
add L「……カードも……キーホルダーも……」
zoom L mid「な、なんで…」「なんで戻ってくるの…」［realize_wet_cat_stare］
say C「高校生の方が、部活の帰りに届けてくれたんですよ」［talk_orange_white_sitting_cat］

## 5. 数字で見ると（約1分10秒）
photo[ph02_koban_night]「2025年、東京で警察に届けられた現金は、およそ45億円。\n4年連続で過去最高でした。（警視庁）」
photo[ph02_koban_night]「そのうち約7割、およそ32億円が\n落とし主のもとに戻っています。」
photo[ph02_koban_night]「落としたと届けられた現金は、およそ83億円。\nその半分を超える額が、誰かの手で届けられたことになります。」
photo[ph03_lost_and_found]「2014年にも、東京で33億円を超える現金が届けられ、\n海外のメディアが驚いて伝えました。」
Scene[bg02_koban]（アメリカの旅行者=L, 交番のおまわりさん=C, 日本の友だち=R）
zoom L「45億円！？　1年で！？」(黄)［surprise_big_pupils_cat］
say R「それだけ落としてる人がいるってことでもあるけどね」［slack_nail_filing_cat］
say C「そして、それだけ届けてくれる人がいる、ということです」［talk_orange_white_sitting_cat］
say R「……でも、日本でも全部戻るわけじゃないからね。気をつけて」［work_typing_cat］
say L「はい……」［meow_gray_white_kitten］

## 6. 拾ってくれた人（約1分）
Scene[bg04_station_exit]（アメリカの旅行者=L, 拾った高校生=R）
say L「あなたが拾ってくれたの！？　ありがとう！！」［happy_chipi_chapa_cat］
say R「あ、いえ……ふつうのことなので……」［meow_gray_white_kitten］
say L「どうして届けたの？　3万円も入ってたのに」［think_bike_front_seat_cat］
say R「小さいころから、“落とし物は交番へ”って言われてて……」［itchy_kitten_butt］
add R「落とした人、困ってるだろうなって」
zoom L mid「……いい子…」「……いい国…」［realize_wet_cat_stare］
say L「お礼をさせて！」［happy_chipi_chapa_cat］
photo[ph04_police_box]「日本では、落とし主が見つかると、拾った人は\n落とし物の価値の5〜20％のお礼を受け取れる決まりがあります。」
photo[ph04_police_box]「3か月たっても落とし主が見つからなければ、\n拾った人のものになるルールもあります。」
Scene[bg04_station_exit]（アメリカの旅行者=L, 拾った高校生=R）
say R「えっ、そんな……じゃあ、部活のみんなとアイス食べます」［itchy_kitten_butt］
zoom L「最高の使い道！！」(黄)［dance_edm_cat］

## 7. 世界の財布実験（約40秒）
photo[ph05_wallets_world]「世界40か国の街で、わざと財布を落とす実験が行われたことがあります。」
photo[ph05_wallets_world]「お金が入っている財布のほうが、戻ってくる割合が高いという結果に。\nいちばん多く戻ったのは、デンマークで82％でした。」
Scene[bg03_cafe]（アメリカの旅行者=L, 日本の友だち=R）
say L「で、日本は何位だったの！？」［dance_edm_cat］
say R「……日本は、実験に入ってなかったらしい」［slack_nail_filing_cat］
zoom L「入ってないんかい！！」(赤, 集中線)［huh_goat_talks_to_huh_cat］
say R「入ってたら、何位だったんだろうね」［cocky_dj_cat］

## 8. 締め（約50秒）
photo[ph06_sunset_street]「落とし物は交番へ。子どものころから教わる、小さな決まり。」
photo[ph06_sunset_street]「その小さな決まりが、年間45億円の\n“戻ってくる安心”を作っているのかもしれません。」
Scene[bg05_rainbow_meadow]（アメリカの旅行者=L, 交番のおまわりさん=C, 日本の友だち=R）
say L「国に帰ったら、みんなに話す！　日本では財布が戻ってくるって！」［dance_edm_cat］
say R「その前に、もう落とさないでね」［slack_nail_filing_cat］
say C「お気をつけて」［talk_orange_white_sitting_cat］
ending［happy_girlfriend_dance_cat］

---

## 背景・写真・イラスト（AIで作る）※実在の店・ビル・看板に似せない。人物の顔ははっきり描かない
- ph01_tokyo_crowd（PHOTO）… 人の多い東京の交差点（後ろ姿・ぼかし）
- ph02_koban_night（PHOTO）… 夜の交番の外観（文字なし）
- ph03_lost_and_found（PHOTO）… 棚に並ぶ落とし物の箱（文字なし）
- ph04_police_box（PHOTO）… 昼の交番の前の自転車
- ph05_wallets_world（ILLUST）… 世界地図の上にいろんな財布
- ph06_sunset_street（PHOTO）… 夕焼けの商店街
- il_wallet（ILLUST・吹き出し用）… 猫のキーホルダー付きの茶色い財布
- bg01_shibuya（ILLUST）… にぎやかな交差点
- bg02_koban（ILLUST）… 交番の中、机と地図
- bg03_cafe（ILLUST）… カフェの席
- bg04_station_exit（ILLUST）… 駅の出口の前、夕方
- bg05_rainbow_meadow … 見本の st05_rainbow_meadow を使い回し可

## 確認メモ（2026-10-21 確認）
- 2025年に警視庁へ届けられた現金 約45億円（4,508,824,075円）で4年連続過去最高。処理分のうち約32億2,958万円が落とし主に返還（約7割）（警視庁 遺失物取扱状況・nippon.com）
- 遺失届の現金 83億2,516万円 → 単純計算で54.2%が警察に届けられた（nippon.com）
- 2014年：届けられた現金 約33億4千万円、持ち主に戻ったのは約24億7千万円。海外メディアが驚いて報道（Lifehacker 日本版）
- 報労金：価値の5〜20%（施設内は2.5〜10%）、3か月で落とし主が見つからなければ拾った人のもの（警察庁）
- 世界の財布実験：40か国、現金入りの方が戻る率が高い（平均 現金なし46%・あり61%）、トップはデンマーク82%、**日本は対象外**（Lifehacker 日本版）。論文名は未確認 → 動画では論文名は出さない
- 「落とし物は交番へと小さいころから」「高校生が届けた」は寸劇の作り話の台詞・設定

## 出典
- 警視庁 遺失物取扱状況 https://www.keishicho.metro.tokyo.lg.jp/about_mpd/jokyo_tokei/kakushu/kaikei.html
- nippon.com https://www.nippon.com/ja/japan-data/h02746/
- 警察庁（落とし物のお礼）https://www.npa.go.jp/bureau/soumu/ishitsubutsu/otoshimono/index.html
- Lifehacker 日本版（財布の実験・東京の落とし物）https://www.lifehacker.jp/article/194813_drop-the-wallet/
- 東京都（英語）lost & found https://www.english.metro.tokyo.lg.jp/w/000-101-006544
