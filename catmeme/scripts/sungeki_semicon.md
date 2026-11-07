# 【寸劇】AIブームの陰の主役　「日本の素材がないと、半導体が作れない？」（原稿 v1）

- 調査・台本: 別セッション（猫ミーム時事ネタ分析）。番号は制作側で振る
- 形式: **「寸劇」シリーズ**（README の「寸劇」シリーズ／`docs/sungeki_reference.md`／`story_style.py`／見本 `story_18_demo.py` と同じ作り）
- ジャンル: 競合チャンネルの「国旗つきの猫で国どうしが会話する」型（日本の企業・技術が世界で効いている話）。動画の中身は競合と別の題材
- 想定尺: 約6〜7分
- 書き方（story_style に合わせた書き方）:
  - `intro「」` 黒い画面に白い文字だけ（音なし）
  - `photo[写真名]「」` 黒い画面＋写真＋字幕の語り（BGM 続く）
  - `Scene[背景名]（役名=位置）` 場面。役名は画面の上に固定（L=左上・C=真ん中上・R=右上）。**役名の白い札に小さい国旗を付ける**（競合と同じ見せ方）
  - `say L「」` セリフ（話す猫を表情に合わせて差しかえ）／`add` 同じ役の下に足す
  - `zoom L「」(白/黄/赤, 集中線, 吹き出し=イラスト名)` 強調カット／`zoom L mid「」「」` 顔のアップ＋真ん中に黄色を1行ずつ
  - `ending` 全員同じ踊る猫＋「チャンネル登録、お願いしまーす」
  - ［猫］は仮の素材名（`assets/` から表情に合わせて選び直してOK）

## ルール（必ず守る）
- 冒頭で「再構成したお話」と書く。**国どうし・会社どうしの会話は作り話**（実際にこういう会話があったわけではない）
- **実在の人物・実在の会社の人を猫で演じない**。役は「アメリカ」「台湾」「日本」という“国”と、「日本の素材メーカー」という“架空の会社の人”。会社名（信越化学・SUMCO・東京応化・JSR・TSMC など）は**語り（photo）の事実説明の中だけ**で出す
- 「他国をバカにする」方向にしない（競合ジャンルで炎上しやすいところ）。アメリカ・台湾は“頼りにしてくれる仲間”として描く。日本は“地味で謙虚な職人”
- 数字は確認メモのとおり。「日本で9割」は**「と言われることも」**まで（出典が1件のみ）
- 語尾に「にゃ」は使わない。単語の途中で改行しない。AIで作った背景・写真・イラストは概要欄に書く

## 配役
| 役名（札） | 位置 | キャラ | 猫の例 |
|---|---|---|---|
| アメリカ 🇺🇸 | L | AIで世界を取りたい。せっかちで声が大きい | dance_edm_cat／cocky_dj_cat／rage_talking_cat／surprise_big_pupils_cat |
| 台湾 🇹🇼 | C | 世界一の半導体工場。仕事はできるが材料にはうるさい | work_typing_cat／stare_interviewer_cat／slack_nail_filing_cat |
| 日本 🇯🇵 | R | 地方の素材メーカーの社員（架空）。地味・謙虚・ずっと同じものを作り続けている | talk_orange_white_sitting_cat／sleepy_old_memories_cat／meow_gray_white_kitten |

## BGM
- intro は音なし。photo と寸劇は BGM 続く（README の使える曲から。前半は軽め、熊本の場面から明るめに）

---

## 0. 冒頭
intro「これは、半導体をめぐる国と企業の関係を」
intro「もとに再構成したお話です。」
photo[ph01_smartphone_ai]「スマホにも、AIにも欠かせない“半導体”。」
photo[ph01_smartphone_ai]「その“材料”の多くが日本から届いていることは、\nあまり知られていません。」

## 1. アメリカ「AIチップ、今すぐ！」
Scene[bg01_us_ai_office]（アメリカ=L, 台湾=R）
say L「AIチップ、あと10万個！！」［dance_edm_cat］
add L「いや20万個！！」
add L「今すぐ！！」
say R「作れるよ。材料さえ届けばね」［work_typing_cat］
zoom L「材料？そんなのどこでも買えるでしょ」(白)［cocky_dj_cat］
say R「……それが、そうでもないんだよね」［slack_nail_filing_cat］
say L「え？」［huh_huh_cat］

## 2. 半導体って、何でできてる？
photo[ph02_wafer_closeup]「半導体は、薄い“シリコンの板”に\n細かい回路を焼きつけて作ります。」
photo[ph02_wafer_closeup]「その板＝シリコンウエハーや、\n回路を描くための“感光材（フォトレジスト）”。」
photo[ph03_chemical_plant]「こうした材料の多くを、\n日本のメーカーが作っています。」

## 3. 台湾の工場に、いつもの人が来る
Scene[bg02_cleanroom]（台湾=L, 日本=R）
say R「おつかれさまです。今月の“いつものやつ”、お届けにあがりました」［talk_orange_white_sitting_cat］
zoom L「助かる〜〜！！」(黄)［happy_chipi_chapa_cat］
say L「これがないと、うちのライン全部止まるからね」［work_typing_cat］
say R「いえいえ、ただの化学メーカーですので」［sleepy_old_memories_cat］
（アメリカが入ってくる → 役名が3つになる）
Scene[bg02_cleanroom]（台湾=L, アメリカ=C, 日本=R）
say C「台湾、チップまだ？……って、誰その地味な人」［glare_disgusted_cat］
say L「この人がいないと、世界のチップが作れない人」［stare_interviewer_cat］
zoom C「え！？」(黄)［surprise_big_pupils_cat］
say R「いえいえ、とんでもない……」［meow_gray_white_kitten］

## 4. 日本の“地味な”正体
intro「その日本の会社とは——」
photo[ph04_japan_factory_town]「半導体の土台になる“シリコンウエハー”は、\n日本の信越化学工業とSUMCOの2社で、世界の過半を作っていると報じられています。」
photo[ph04_japan_factory_town]「回路を描く“フォトレジスト”でも、\n東京応化工業やJSRなど日本の会社が上位に並びます。」
photo[ph04_japan_factory_town]「“日本の会社で世界の9割”と言われることも。」
Scene[bg03_jp_material_plant]（アメリカ=L, 台湾=C, 日本=R）
say R「うちは、昔から同じものを、ちょっとずつ良くしてきただけで……」［talk_orange_white_sitting_cat］
zoom L mid「な、なんだと…」「地味なのに…」「世界の首根っこを…」［realize_wet_cat_stare］
say C「AIの主役はチップ。でも、チップの主役は材料なのよ」［stare_interviewer_cat］
zoom L「最先端って、そういうことなの！？」(黄)［huh_goat_talks_to_huh_cat］
say R「よく言われます。“地味ですね”って」［sleepy_old_memories_cat］
zoom C「それがいちばん強いのよ！！」(赤, 集中線)［angry_cat_hits_cat］

## 5. なぜ日本は強い？
photo[ph05_cleanroom_workers]「材料に求められるのは、とてつもない“純度”と“同じ品質”。」
photo[ph05_cleanroom_workers]「何十年も、同じものを、少しずつ良くし続けてきたこと。\nそれが、簡単にはまねできない強みになっている、と言われています。」
Scene[bg03_jp_material_plant]（アメリカ=L, 台湾=C, 日本=R）
say L「じゃあ、レシピ教えてよ」［cocky_dj_cat］
say R「……それはちょっと」［blank_black_cat_zoning_out］
say L「ケチ！！」［rage_talking_cat］
say C「何十年分の“ちょっとずつ”は、レシピだけじゃまねできないのよ」［slack_nail_filing_cat］
zoom R mid「……（にっこり）」［joy_happy_happy_happy_cat］

## 6. 工場ごと、日本へ
intro「そして2026年——」
photo[ph06_kumamoto_fields]「台湾の半導体大手TSMCは、熊本の第2工場で\n最先端の“3ナノ”の半導体を作る方針を発表しました。」
photo[ph06_kumamoto_fields]「政府は「世界最先端の工場が日本にあることは、\n経済安全保障の面で大きな意義がある」としています。」
Scene[bg04_kumamoto_factory]（台湾=L, 日本=C, アメリカ=R）
say L「材料が近くにあるなら、工場ごと来ちゃえばいいじゃない」［dance_trending_cat］
zoom C「え、来るんですか！？」(白)［surprise_big_pupils_cat］
say L「来た」［cocky_dj_cat］
say R「ずるい！！　うちにも工場ちょうだい！！」［sad_banana_cat_cry］
say C「みなさん、仲良く使ってくださいね……」［talk_orange_white_sitting_cat］

## 7. 締め
photo[ph07_sunset_factory]「派手なAIの陰で、地味な材料を作り続けてきた日本の会社。」
photo[ph07_sunset_factory]「世界の最先端は、案外“いつものやつ”に\n支えられているのかもしれません。」
Scene[bg05_rainbow_meadow]（アメリカ=L, 台湾=C, 日本=R）
say L「来月も“いつものやつ”、よろしく！！」［wave_waving_cat］
say R「……はい。いつも通り、お届けします」［meow_gray_white_kitten］
say C「それが一番ありがたいのよ」［calmdown_dancing_cat］
ending［happy_girlfriend_dance_cat］

---

## 背景・写真・イラスト（AIで作る・`gen_bg_gemini.py` の PHOTO:/ILLUST:）
※実在の会社のロゴ・建物・制服に似せない。人物の顔ははっきり描かない
- ph01_smartphone_ai（PHOTO）… 夜の机、スマホとノートPCの画面が光る（画面に文字なし）
- ph02_wafer_closeup（PHOTO）… 虹色に光るシリコンウエハーのアップ
- ph03_chemical_plant（PHOTO）… 日本の地方の化学工場、昼、タンクと配管
- ph04_japan_factory_town（PHOTO）… 田んぼの向こうに工場が見える地方の町
- ph05_cleanroom_workers（PHOTO）… 白い防塵服の作業員がクリーンルームで作業（顔は見えない）
- ph06_kumamoto_fields（PHOTO）… 畑と山の向こうに大きな新しい工場
- ph07_sunset_factory（PHOTO）… 夕焼けの工場の煙突
- bg01_us_ai_office（ILLUST）… アメリカのIT企業っぽいオフィス、大きなモニター
- bg02_cleanroom（ILLUST）… 半導体工場のクリーンルーム（黄色い照明）
- bg03_jp_material_plant（ILLUST）… 日本の素材メーカーの事務所兼工場、棚に薬品の容器
- bg04_kumamoto_factory（ILLUST）… 田園の中の大きな半導体工場、青空
- bg05_rainbow_meadow … 見本の st05_rainbow_meadow を使い回し可

## 確認メモ（2026-10-19 確認）
- シリコンウエハー：信越化学工業とSUMCOの2社で、金額ベースで世界全体の過半（経産省のSUMCO工場助成に関する報道、ビジネス+IT／東洋経済）。信越単独で約3割（東洋経済）
- フォトレジスト：東京応化工業が世界シェア約23%で首位級。JSR・東京応化・富士フイルム・信越化学が上位（先端向けでは上位5社で約50%という調査も）。「日本の4社で約9割」は1件の記事のみ →「と言われることも」
- TSMC：2026年2月5日、熊本の第2工場で3ナノの半導体を製造する方針。首相官邸「世界最先端の半導体工場が日本にあることは、経済安全保障の観点から大きな意義」（Bloomberg ほか）
- 「何十年も少しずつ良くしてきたことが強み」は一般的な説明として「と言われています」

## 出典
- ビジネス+IT https://www.sbbit.jp/article/st/186887
- 東洋経済 https://toyokeizai.net/articles/-/727560
- ニュースイッチ（フォトレジスト） https://newswitch.jp/keyword/detail/37888
- Global Market Insights（先端リソグラフィ向けフォトレジスト） https://www.gminsights.com/ja/industry-analysis/photoresist-chemicals-for-advanced-lithography-market
- Bloomberg（TSMC 熊本で3ナノ） https://www.bnnbloomberg.ca/business/technology/2026/02/05/tsmc-to-make-advanced-ai-semiconductors-in-japan-in-boost-for-its-chipmaking-ambitions/
