# 【寸劇】江戸の子どもは字が読めた　寺子屋が“世界トップクラスの識字率”を生んだと言われる理由（原稿 v1）

- 調査・台本: 別セッション（猫ミーム時事ネタ分析）。番号は制作側で振る
- 形式: **「寸劇」シリーズ**（README・`docs/sungeki_reference.md`・`story_style.py`・見本 `story_18_demo.py`）。書き方は `sungeki_semicon.md` と同じ
- ジャンル: 「なぜ日本だけ？」の歴史もの。国旗つきの猫（幕末に来た外国人）と江戸の人たちの会話
- 想定尺: 約5〜6分
- 書き方: `intro「」`／`photo[写真名]「」`／`Scene[背景名]（役名=位置）`／`say`・`add`／`zoom`／`zoom mid`／`ending`。［猫］は仮

## ルール（必ず守る）
- 冒頭で「再構成したお話」と書く。登場人物はすべて架空（実在の外国人・歴史上の人物は猫で演じない・名前も出さない）
- **識字率の数字は推計で、資料によって幅がある**。必ず「推計」「〜とも」「と言われている」を付ける。「世界一」と言い切らない（タイトルも「世界トップクラスと言われる」）
- 外国をバカにしない（「ヨーロッパは字が読めなかった」などと言わない）。外国人の役は“素直に驚いて感心する旅行者”
- 語尾に「にゃ」なし。単語の途中で改行しない。AIで作った背景・写真・イラストは概要欄に

## 配役
| 役名（札） | キャラ | 猫の例 |
|---|---|---|
| イギリスの旅行者 🇬🇧 | 幕末の江戸に来た外国人（架空）。驚き役 | surprise_big_pupils_cat／huh_huh_cat／stare_big_eyes_tabby_kitten |
| 江戸の子ども 🇯🇵 | 町人の子（架空）。元気 | happy_chipi_chapa_cat／dance_trending_cat／itchy_kitten_butt |
| 寺子屋の師匠 🇯🇵 | 近所のおじいさん（架空）。おだやか | sleepy_old_memories_cat／talk_orange_white_sitting_cat |
| 八百屋のおかみ 🇯🇵 | 子どもの母（架空）。ちゃっかり者 | slack_nail_filing_cat／laugh_laughing_dog |

---

## 0. 冒頭
intro「これは、幕末の日本を訪れた外国人の驚きを」
intro「もとに再構成したお話です。」
photo[ph01_edo_street]「今から160年ほど前、江戸。」
photo[ph01_edo_street]「海の向こうから来た人たちが、\nある“当たり前の光景”に驚いたと言われています。」

## 1. 子どもが看板を読んでいる
Scene[bg01_edo_shop_street]（イギリスの旅行者=L, 江戸の子ども=R）
say R「“本日、大安売り”だって！　おっかあに言ってこよ！」［happy_chipi_chapa_cat］
zoom L「……今、読んだ？」(白)［surprise_big_pupils_cat］
say R「え？　読めるよ？」［huh_huh_cat］
zoom L「この子、字が読めるの！？」(黄)［stare_big_eyes_tabby_kitten］
say R「みんな読めるよ。寺子屋で習ったもん」［dance_trending_cat］
zoom L「テラコヤ……？」(白, 吹き出し=il_terakoya)［think_bike_front_seat_cat］

## 2. 寺子屋へ
Scene[bg02_terakoya_room]（イギリスの旅行者=L, 寺子屋の師匠=C, 江戸の子ども=R）
say C「ようこそ。今日は手習い（字の練習）の日でしてな」［sleepy_old_memories_cat］
say R「“いろはにほへと”〜！」［itchy_kitten_butt］
add R「そろばんも得意！」
say L「先生は、お坊さん？　武士？」［think_bike_front_seat_cat］
say C「わしはただの隠居じゃよ。町内の子に教えとるだけ」［talk_orange_white_sitting_cat］
zoom L「ふつうの町の人が、先生！？」(黄)［surprise_big_pupils_cat］
photo[ph02_terakoya]「寺子屋は、町や村の人がひらいた、子どものための手習い塾。」
photo[ph02_terakoya]「幕末には全国で1万を超え、1万5千以上とも言われます。\n江戸の町だけでも1,200以上あったとされています。」

## 3. 月謝は野菜でもいい？
Scene[bg02_terakoya_room]（イギリスの旅行者=L, 寺子屋の師匠=C, 八百屋のおかみ=R）
say R「先生、今月のお礼、大根でいいかい？」［slack_nail_filing_cat］
say C「おお、助かる助かる」［sleepy_old_memories_cat］
zoom L「授業料が大根！？」(赤, 集中線)［huh_goat_talks_to_huh_cat］
say R「お金のない家は、それで十分さ」［laugh_laughing_dog］
photo[ph03_daikon]「お礼は、お金でも、季節の野菜や品物でもよかったと言われています。\n身分に関係なく通えたことも、広がった理由のひとつとされます。」

## 4. なぜ、みんな字を習った？
Scene[bg01_edo_shop_street]（イギリスの旅行者=L, 江戸の子ども=C, 八百屋のおかみ=R）
say L「どうして、そんなに字を習わせるの？」［think_bike_front_seat_cat］
say R「読めなきゃ、商売にならないからね」［slack_nail_filing_cat］
add R「証文（契約書）も、帳簿も、お触れ（お知らせ）も、全部、字」
say C「それに、貸本屋の本が読みたい！」［happy_chipi_chapa_cat］
photo[ph04_kashihonya]「江戸には本を貸して回る“貸本屋”がいて、\n町の人たちは物語や瓦版を楽しんでいました。」
photo[ph04_kashihonya]「読み・書き・そろばんは、\n暮らしと商売に欠かせない力だったのです。」

## 5. 数字で見ると
photo[ph05_old_books]「幕末の識字率には、正確な統計はありません。」
photo[ph05_old_books]「推計では、庶民の男子で5割前後、女子で2割前後とも、\n江戸の町では7割を超えていたとも言われます。」
photo[ph05_old_books]「当時としては、世界でもトップクラスだったと言われることがあります。\n（数字は資料によって幅があります）」
Scene[bg02_terakoya_room]（イギリスの旅行者=L, 寺子屋の師匠=C, 江戸の子ども=R）
zoom L mid「国のお金じゃなく…」「町の人たちが…」「こんなに…」［realize_wet_cat_stare］
say C「みんな、自分の子に“読める大人”になってほしいだけじゃよ」［talk_orange_white_sitting_cat］
zoom L「国に帰ったら、絶対に書き残す！！」(赤, 集中線)［angry_aiming_cat］
say R「じゃあ、わたしが字、教えてあげる！」［dance_trending_cat］

## 6. その後
intro「そして——」
photo[ph06_meiji_school]「明治5年（1872年）、全国に学校をつくる“学制”が始まります。」
photo[ph06_meiji_school]「学校がすばやく広がった土台には、\n寺子屋の積み重ねがあったと言われています。」

## 7. 締め
photo[ph07_sunset_edo]「看板を読む子ども。大根で払う授業料。\n町のおじいさんの先生。」
photo[ph07_sunset_edo]「日本人には当たり前だった光景が、\n海の向こうの人には“奇跡”に見えたのかもしれません。」
Scene[bg03_rainbow_meadow]（イギリスの旅行者=L, 寺子屋の師匠=C, 江戸の子ども=R）
say R「“い・ろ・は”、書けた？」［happy_chipi_chapa_cat］
say L「……い……ろ……」［meow_gray_white_kitten］
say C「上出来、上出来」［sleepy_old_memories_cat］
ending［happy_girlfriend_dance_cat］

---

## 背景・写真・イラスト（AIで作る・PHOTO:/ILLUST:）※浮世絵ふう・時代劇ふうの絵でもよい。実在の絵の模写にしない
- ph01_edo_street … 江戸の町並み（浮世絵ふうのイラストでも可）
- ph02_terakoya … 寺子屋で子どもたちが机に向かう様子（浮世絵ふう）
- ph03_daikon … 大根などの野菜が並ぶ
- ph04_kashihonya … 本を背負って歩く貸本屋の後ろ姿
- ph05_old_books … 古い和本と筆・すずり
- ph06_meiji_school … 明治の木造の小学校
- ph07_sunset_edo … 夕焼けの江戸の町（浮世絵ふう）
- il_terakoya（ILLUST・吹き出し用）… 寺子屋のイラスト
- bg01_edo_shop_street（ILLUST）… 江戸の商店街、のれん（文字は読めない程度に）
- bg02_terakoya_room（ILLUST）… 畳の部屋に文机が並ぶ寺子屋
- bg03_rainbow_meadow … 見本の st05_rainbow_meadow を使い回し可

## 確認メモ（2026-10-20 確認）
- 寺子屋の数：慶応年間（1865〜68）に全国で1万超、江戸市中1,200以上（moneypost）／江戸末期に全国15,000以上とする資料も → 「1万を超え、1万5千以上とも」
- 1つの寺子屋は寺子20〜30人程度が多い
- 識字率（推計・幅あり）：庶民男子54%・女子20%程度（台湾の論文集録）、国民の50〜60%・江戸は70%超（教育委員会の資料）、江戸の就学率70〜80%とする記事も → 「男子5割前後・女子2割前後とも、江戸は7割超とも」。**正確な統計はない**ことを字幕で明記
- 同時期のロンドンの就学率2割前後という記述もあるが、**動画では他国との比較の数字は出さない**（比較の条件がそろわないため・他国を下げない）
- 幕末の外国人の証言（シュリーマン・ゴローニン等）は原典の文言を確認できず → 名前は出さず「驚いたと言われています」にとどめる
- 月謝が野菜・品物でもよかった、身分に関係なく通えた：一般的な説明として「と言われています」「とされます」
- 学制：明治5年（1872年）公布（一般的な歴史の事実）

## 出典
- マネーポスト（江戸の寺子屋と識字率）https://www.moneypost.jp/1234049
- 和楽web（江戸の識字率）https://intojapanwaraku.com/rock/culture-rock/182791/
- 文部科学省（学制百年史など）https://www.mext.go.jp/b_menu/hakusho/html/others/detail/mext_03454.html
