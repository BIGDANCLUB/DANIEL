# 【寸劇】中国からの観光客が半分以下に　日本の観光地はどうなった？（原稿 v1）

- 調査・台本: 別セッション（猫ミーム時事ネタ分析）。番号は制作側で振る
- 形式: **「寸劇」シリーズ**（README の「寸劇」シリーズ／`docs/sungeki_reference.md`／`story_style.py`／見本 `story_18_demo.py`）。書き方は `sungeki_semicon.md` と同じ
- ジャンル: 競合の「国旗つきの猫で国どうしが会話する」型。**時事**（2025年11月〜2026年の訪日中国人の激減）
- 想定尺: 約6〜7分
- 書き方:
  - `intro「」` 黒い画面に白い文字だけ（音なし）／`photo[写真名]「」` 黒い画面＋写真＋字幕の語り（BGM 続く）
  - `Scene[背景名]（役名=位置）` 役名は画面の上に固定（L/C/R）。**役名の札に小さい国旗**（日本の役は 🇯🇵）
  - `say L「」`／`add`（下に足す）／`zoom L「」(白/黄/赤, 集中線, 吹き出し=イラスト名)`／`zoom L mid「」「」`／`ending`
  - ［猫］は仮の素材名

## ルール（必ず守る）
- 冒頭で「再構成したお話」と書く。登場する会話は作り話
- **政治のどちらかの肩を持たない**。発端（首相の答弁 → 中国が反発 → 渡航の注意喚起）は語りで事実だけ。首相・中国の外交官など**実在の人物は猫で演じない**（語りの字幕のみ）
- **中国の人をバカにしない・「ざまぁ」にしない**（このジャンルでいちばん炎上・制限されやすいところ）。中国の役は「日本が大好きで、行けなくなって困っている旅行好き」として描く（報道で紹介された“親日の中国人の困惑”をもとに）
- 「困ったのはどっち？」のような勝ち負けの決めつけはしない。**日本の中でも「困った所」と「意外と大丈夫だった所」がある**、という見せ方
- 数字は確認メモどおり（期間や地域で数字が違うので、字幕に期間を必ず書く）
- 語尾に「にゃ」は使わない。単語の途中で改行しない。AIで作った背景・写真・イラストは概要欄に書く

## 配役
| 役名（札） | 位置 | キャラ | 猫の例 |
|---|---|---|---|
| 中国の旅行好き 🇨🇳 | 場面による | 日本が大好き。京都と温泉が夢。半年前から計画していた | happy_chipi_chapa_cat／sad_banana_cat_cry／sulk_hungry_cat |
| 大阪の店主 🇯🇵 | 場面による | 心斎橋のドラッグストア。にぎやかで正直 | rage_talking_cat／despair_dramatic_kitten／blank_black_cat_zoning_out |
| 京都の女将 🇯🇵 | 場面による | 町家の宿。落ち着いている | slack_nail_filing_cat／talk_orange_white_sitting_cat |
| 韓国の旅行者 🇰🇷 | 場面による | 週末に気軽に来る。福岡が好き | dance_trending_cat／happy_girlfriend_dance_cat |
| 欧米の旅行者 🇺🇸 | 場面による | 京都の寺と抹茶に夢中 | excited_hodomoe_city_cat／surprise_big_pupils_cat |

## BGM
- intro は音なし。前半（自粛〜大阪）は少し寂しめ、京都〜締めは明るめ

---

## 0. 冒頭
intro「これは、2025年秋から続く“訪日の自粛”を」
intro「もとに再構成したお話です。」
photo[ph01_crowded_kyoto]「少し前まで、日本の観光地には\n中国からのお客さんがたくさんいました。」
photo[ph01_crowded_kyoto]「その数が、ある日を境に\n半分以下になります。」

## 1. 行けなくなった旅行好き
Scene[bg01_china_home]（中国の旅行好き=L）
say L「来月はいよいよ京都！！」［happy_chipi_chapa_cat］
add L「温泉も！！」
add L「抹茶パフェも！！」
zoom L「半年前から計画したんだから！！」(黄, 吹き出し=il_kyoto_matcha)［dance_edm_cat］
（スマホの通知の音）
say L「……ん？」［peek_what_happen_cat］
photo[ph02_news_phone]「2025年11月7日、国会で首相が台湾有事をめぐって答弁。」
photo[ph02_news_phone]「中国は強く反発し、11月14日、\n自国民に“日本への渡航を当面控えるよう”呼びかけました。」
photo[ph02_news_phone]「理由として、日本の“治安の悪化”などを挙げました。」
Scene[bg01_china_home]（中国の旅行好き=L）
zoom L「え……行けないの……？」(白)［sad_banana_cat_cry］
say L「日本の治安、すごくいいって聞いてたのに……」［sulk_hungry_cat］
zoom L mid「旅行計画は…」「半年前に…」「決めたのに…」［blank_black_cat_zoning_out］
photo[ph03_airport_line]「当時、日本と行き来のある中国の人たちからは\n“すぐには計画を変えられない”“日本の治安はとても良い”と\n戸惑う声も報じられました。」

## 2. 大阪の店主、頭を抱える
intro「そして2026年——」
Scene[bg02_osaka_drugstore]（大阪の店主=L）
say L「最近、お店、静かすぎひん？」［blank_black_cat_zoning_out］
photo[ph04_osaka_street]「大阪を訪れた中国の人は、2026年1〜8月で\n前の年より61.5％減りました。（大阪観光局）」
photo[ph04_osaka_street]「関西空港の中国との便も、約7割減ったと報じられています。」
Scene[bg02_osaka_drugstore]（大阪の店主=L）
zoom L「お客さん、どこ行ったん！？」(赤, 集中線)［rage_talking_cat］
say L「爆買いの棚、ガラガラやで……」［despair_dramatic_kitten］
photo[ph05_jnto_graph]「全国でも、中国からの訪日客は\n2026年1〜8月で56.7％減。」
photo[ph05_jnto_graph]「8月の訪日客全体も、前の年より9.6％減りました。（日本政府観光局）」

## 3. ……ところが
intro「ところが——」
Scene[bg03_fukuoka_street]（大阪の店主=L, 韓国の旅行者=R）
say R「週末だし、福岡でラーメン食べて帰ろ〜」［dance_trending_cat］
zoom L「……え、めっちゃ来てるやん」(白)［surprise_big_pupils_cat］
say R「近いし、安いし、最高！」［happy_girlfriend_dance_cat］
photo[ph06_airport_arrival]「同じ8月、韓国や台湾など14の国と地域は\n8月として過去最多を記録しました。」
photo[ph06_airport_arrival]「韓国の秋の連休では、福岡行きの予約が\n前の年より約7割増えたとも。」

## 4. 京都の女将は落ち着いていた
Scene[bg04_kyoto_machiya]（京都の女将=L, 欧米の旅行者=R）
say R「Kyoto……ビューティフル……」［excited_hodomoe_city_cat］
add R「マッチャ、もう一杯……」
say L「おおきに。ゆっくりしていっておくれやす」［slack_nail_filing_cat］
photo[ph07_kyoto_temple]「京都のホテルでは、約6割が“前の年より減った”と答えたものの、\n“大きく減った”は12.3％にとどまりました。」
photo[ph07_kyoto_temple]「外国人の宿泊客のうち、欧米やオーストラリアの人が\n約4割を占めるようになっています。」
Scene[bg04_kyoto_machiya]（大阪の店主=L, 京都の女将=C, 欧米の旅行者=R）
say L「京都、ずるない？」［glare_disgusted_cat］
say C「うちは前から、いろんな国のお客さんに来てもろてましたさかい」［talk_orange_white_sitting_cat］
zoom L「大阪も、もっといろんな国に来てもらわな！」(黄)［angry_aiming_cat］
say R「オオサカ、タコヤキ、行キタイ！」［wave_waving_cat］
zoom L mid「……ほんまに？」「……うれしい」［realize_wet_cat_stare］

## 5. 減ったのは“人数”
photo[ph08_shopping_bags]「一方で、日本に来ている中国の人の\n1人あたりの支出は、前の年より9.4％増えています。（2026年4〜6月）」
photo[ph08_shopping_bags]「この秋の中国の大型連休の人気の旅行先で、\n日本はトップ10に入りませんでした。（中国の旅行大手）」
Scene[bg05_video_call]（中国の旅行好き=L, 京都の女将=R）
say L「（ビデオ通話）女将さん、ごぶさたしてます……」［sad_banana_cat_cry］
say R「まあ、お元気？」［talk_orange_white_sitting_cat］
say L「行きたいリスト、まだ全部とってあります」［sleepy_old_memories_cat］
add L「京都、温泉、抹茶パフェ……」
zoom R「お部屋、いつでも空けて待ってますえ」(赤, 集中線)［slack_nail_filing_cat］
zoom L mid「……行きたい」「……絶対、行きたい」［stare_big_eyes_tabby_kitten］

## 6. 締め
photo[ph09_sunset_kyoto]「人の行き来は、国と国の関係でかんたんに変わってしまう。」
photo[ph09_sunset_kyoto]「それでも、“あの国にまた行きたい”という気持ちまでは\n止められないのかもしれません。」
Scene[bg06_rainbow_meadow]（中国の旅行好き=L, 京都の女将=C, 大阪の店主=R）
say C「またみなさんで、来ておくれやす」［talk_orange_white_sitting_cat］
say R「たこ焼き、焼いて待っとくで！」［cocky_dj_cat］
say L「絶対行く！！」［happy_chipi_chapa_cat］
ending［happy_girlfriend_dance_cat］

---

## 背景・写真・イラスト（AIで作る・`gen_bg_gemini.py` の PHOTO:/ILLUST:）
※実在の店・寺・空港のロゴや看板に似せない。人物の顔ははっきり描かない。国旗は役名の札だけ（背景には描かない）
- ph01_crowded_kyoto（PHOTO）… 観光客でにぎわう京都っぽい石畳の坂道（人は後ろ姿・ぼかし）
- ph02_news_phone（PHOTO）… 手に持ったスマホ、画面はぼかし（文字なし）
- ph03_airport_line（PHOTO）… 空港の出発ロビーに並ぶ人の列（後ろ姿）
- ph04_osaka_street（PHOTO）… 人の少ない大阪っぽいアーケード商店街（看板の文字なし）
- ph05_jnto_graph（ILLUST）… 下がる棒グラフのイラスト（数字は字幕で出すので絵には書かない）
- ph06_airport_arrival（PHOTO）… 空港の到着ロビー、スーツケースを引く旅行者たち
- ph07_kyoto_temple（PHOTO）… 京都っぽいお寺の庭、紅葉
- ph08_shopping_bags（PHOTO）… たくさんの買い物袋
- ph09_sunset_kyoto（PHOTO）… 夕焼けの五重塔のシルエット（特定の塔に似せすぎない）
- il_kyoto_matcha（ILLUST・吹き出し用）… 抹茶パフェと温泉のイラスト
- bg01_china_home（ILLUST）… 部屋、壁に日本の旅行ポスター（文字なし）
- bg02_osaka_drugstore（ILLUST）… ドラッグストアの店内、棚がスカスカ
- bg03_fukuoka_street（ILLUST）… 屋台の並ぶ夜の川沿い
- bg04_kyoto_machiya（ILLUST）… 町家の宿の玄関・畳の間
- bg05_video_call（ILLUST）… ノートPCのビデオ通話画面ふう（画面が左右2分割）
- bg06_rainbow_meadow … 見本の st05_rainbow_meadow を使い回し可

## 確認メモ（2026-10-20 確認）
- 発端：2025年11月7日 衆院予算委員会で首相が台湾有事をめぐり「存立危機事態になり得る」と答弁 → 中国が反発 → 11月14日 中国外務省が自国民に日本への渡航を当面控えるよう注意喚起（同時期に留学も慎重に、と）。日本政府は答弁を撤回していない（各紙）
- 理由に「治安の悪化」：秋田魁新報（共同）2025/11/17「親日の中国人『自粛』困惑 治安悪化理由に疑問も」。「旅行計画は半年前に決めた。すぐには計画変更できない」「日本の治安はとても良い」（いずれも報道で紹介された中国人の声）
- JNTO（2026年8月・9/16公表）：訪日外客 309万8,900人（前年同月比9.6%減）。中国 41万8,000人（59.0%減、9か月連続の前年割れ）。韓国・台湾など14市場は8月として過去最多（トラベルボイス）
- 訪日中国人 2026年1〜8月 56.7%減。4〜6月期 52.5%減の97.1万人、1人あたり支出 9.4%増（find-japan ほか。**JNTO・観光庁の原表で確認**）
- 大阪：大阪を訪れた中国人客 2026年1〜8月 61.5%減（大阪観光局）、関西空港の中国便 約7割減（J-CASTニュース）
- 京都：京都市観光協会の調査でホテルの約6割が前年比減、大幅減は12.3%、外国人宿泊客の欧米豪が約4割（ビジネスジャーナル）→ **京都市観光協会の原資料で確認**
- 韓国の秋夕連休：福岡行き予約が前年比70%増（トリップドットコム、訪日ラボ）
- 国慶節：中国旅行大手（途牛）によると中秋節を含む連休の人気旅行先はインドネシア・トルコ・韓国などで、日本はトップ10外（共同・熊日）
- 8月の訪日消費額は前年並み（ビジネスジャーナルの見出し）→ 使うなら原資料で確認

## 出典
- トラベルボイス（Yahoo!ニュース）「訪日外国人数、2026年8月は9.6％減の310万人…14市場で過去最多」https://news.yahoo.co.jp/articles/d1d01b0353fd347090e5c5c8b8883a7e77113e16
- J-CASTニュース（Yahoo!ニュース）「中国人観光客の大阪離れがハンパない」https://news.yahoo.co.jp/articles/1a030b04477031dc835304a0494d1a70b1626787
- ビジネスジャーナル「京都で脱・中国が進行…欧米豪4割時代へ」https://biz-journal.jp/economy/post_393421.html
- ビジネスジャーナル「訪日客8月9.6%減でも消費額は前年並み」https://biz-journal.jp/economy/post_396232.html
- find-japan「中国人観光客減少の影響とは?」https://find-japan.co.jp/blog/china-tourist-decline-impact-2026
- 訪日ラボ（韓国の秋夕連休・福岡便）https://honichi.com/news/2026/09/28/china-korea-gw2026/
- 熊本日日新聞（共同）「中国大型連休、21億人移動 日本は国外旅行の人気圏外」https://kumanichi.com/articles/2044458
- 秋田魁新報（共同）「親日の中国人『自粛』困惑 治安悪化理由に疑問も」https://www.sakigake.jp/news/article/20251117CO0106/
- 秋田魁新報（共同）社説「日中関係悪化 対話の継続で収束図れ」https://www.sakigake.jp/news/article/20251120AK0006/
