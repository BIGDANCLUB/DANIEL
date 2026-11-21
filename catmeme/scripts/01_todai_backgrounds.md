# 背景イラスト発注メモ：01_todai_president（東大総長）

猫ミーム（グリーンバックを抜いた猫）を上にのせるための背景イラスト。

## 共通の仕様
- サイズ: **1920x1080 の PNG**（横長）
- 置き場所: `catmeme/backgrounds/01_todai/`、ファイル名は下の表の `bg01_campus.png` など
- 絵柄: 全部そろえる。やわらかい手描き風のアニメ背景（明るめ・彩度ひかえめ）。**人物・動物は描かない**（猫は後からのせる）
- **画像の中に文字を入れない**（看板・ロゴ・校章・新聞の見出しもなし。字幕は後から入れる）
- 実在の大学は「それっぽい雰囲気」までにする。校章・正式名称・特定の建物そっくりにはしない
- 構図: **画面の中央下あたりを空ける**（猫を立たせる場所）。**下から1/4は字幕が乗る**ので、細かい描き込みを避ける
- AIで作った場合は、そのことを記録しておく（動画の概要欄に「AI生成」と表示するため）

## 背景リスト（11枚）

| ファイル名 | 使う場面 | 内容 | 生成用プロンプト（英語） |
|---|---|---|---|
| bg01_campus.png | 1 つかみ／3 候補者 | 大学の正門と、奥に時計台のある古いレンガの講堂。秋の晴れた日 | Anime-style background illustration, a prestigious old Japanese university campus, brick lecture hall with a clock tower behind the main gate, ginkgo trees, clear autumn day, soft colors, empty open space at center bottom, no people, no animals, no text, no logos, 16:9 |
| bg02_room.png | ニュース猫の場面すべて | ふつうの家のリビング。ソファ、ローテーブル、窓 | Anime-style background illustration, cozy Japanese apartment living room, sofa, low table, window with daylight, warm soft colors, empty floor space at center bottom, no people, no animals, no text, 16:9 |
| bg03_blackboard.png | 2 総長ってだれ？／11 まとめ | 教室の黒板の前（黒板は無地） | Anime-style background illustration, front of a classroom with a large blank green chalkboard, teacher's desk, soft lighting, blank board with nothing written, no people, no animals, no text, 16:9 |
| bg04_voting.png | 4 先生たちの投票 | 講堂の中に投票箱と記入台が並ぶ | Anime-style background illustration, inside a university hall set up for an internal vote, ballot boxes and voting booths in a row, wooden floor, calm lighting, empty space at center bottom, no people, no animals, no text, 16:9 |
| bg05_meeting.png | 5 会議／7 会議の言い分 | 長い会議机とたくさんの椅子、資料の束 | Anime-style background illustration, formal university boardroom, long conference table with many chairs and stacks of documents, large windows, serious atmosphere, no people, no animals, no text, 16:9 |
| bg06_spotlight.png | 5「そして選ばれたのは——」 | 暗い舞台に1本のスポットライト | Anime-style background illustration, dark empty stage with a single bright spotlight shining on the center floor, dramatic, no people, no animals, no text, 16:9 |
| bg07_press.png | 7 議長の会見／8 藤垣さんの会見 | 記者会見場。机にマイク、後ろは無地のパネル | Anime-style background illustration, press conference room, table with microphones, plain blank backdrop panel behind, camera flashes in the foreground, no people, no animals, no text, no logos, 16:9 |
| bg08_study.png | 6 藤垣さんってどんな人？ | 本棚と地球儀、科学の本と社会の本が並ぶ研究室 | Anime-style background illustration, university professor's study, bookshelves full of books, globe, microscope and documents on the desk, warm light, no people, no animals, no readable text, 16:9 |
| bg09_sns.png | 9 世の中の反応 | 大きなスマホ画面と、飛び交う空の吹き出し・ハートやびっくりマーク | Anime-style background illustration, abstract social media theme, a giant smartphone screen with many empty speech bubbles, hearts and exclamation icons floating, pastel colors, no text, no logos, 16:9 |
| bg10_kyoto.png | 10 京都大学 | 京都っぽい古い大学。時計台と紅葉、遠くに山 | Anime-style background illustration, historic university in Kyoto, old clock tower building, red autumn maple leaves, mountains in the distance, no people, no animals, no text, no logos, 16:9 |
| bg11_tsukuba.png | 10 筑波大学 | 広々とした郊外のキャンパス。まっすぐな並木道と近代的な建物 | Anime-style background illustration, large modern suburban university campus, long straight tree-lined path, modern buildings, wide sky, no people, no animals, no text, no logos, 16:9 |

## イラストがいらない場面（こちらでプログラムで作る）
- 4 投票結果の棒グラフ（1,107票／553票／451票）
- 7 選考理由の箇条書き
- 10 京大・筑波大の票数の比較
- 冒頭の注意書き（※実在の人物の言葉は…）

## 使い回しについて
- この動画の中では、同じ背景を複数の場面で使ってよい（例: bg02 はニュース猫の場面で何度も出る）
- 次の動画で同じ場所（会議室など）が出る場合も使い回してよいが、できれば色や時間帯（夕方・夜）を変えた別バージョンを作る
