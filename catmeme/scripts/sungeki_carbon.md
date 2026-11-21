# 【寸劇】飛行機の半分は“日本の糸”？　ボーイング787を支える炭素繊維（原稿 v1）

- 調査・台本: 別セッション（猫ミーム時事ネタ分析）。番号は制作側で振る
- 形式: **「寸劇」シリーズ**（README・`docs/sungeki_reference.md`・`story_style.py`・見本 `story_18_demo.py`）。書き方は `sungeki_semicon.md` と同じ
- ジャンル: 「日本の素材シリーズ」その2（半導体の素材の回の続編）。国旗つきの猫で国どうしが会話する型
- 想定尺: 約5〜6分
- 書き方: `intro「」`（黒＋白文字・音なし）／`photo[写真名]「」`（黒＋写真＋字幕・BGM）／`Scene[背景名]（役名=位置）`（役名は上に固定、札に小さい国旗）／`say`・`add`／`zoom L「」(白/黄/赤, 集中線, 吹き出し=イラスト名)`／`zoom L mid「」「」`／`ending`。［猫］は仮

## ルール（必ず守る）
- 冒頭で「再構成したお話」と書く。会話は作り話
- **実在の会社の人を猫で演じない**。役は「アメリカ」「ヨーロッパ」「日本」（日本は“素材メーカーの社員”・架空）。会社名（ボーイング・東レ・三菱重工など）は**語りの事実説明の中だけ**
- 他国をバカにしない。アメリカは“頼りにしてくれるお得意さん”、ヨーロッパは“ライバルだけど仲間”
- 数字は確認メモどおり。「約半分」「35％超」「約7割」は**「と言われている」「とされる」**で出す（一次資料で確定していないため）
- 語尾に「にゃ」なし。単語の途中で改行しない。AIで作った背景・写真は概要欄に

## 配役
| 役名（札） | キャラ | 猫の例 |
|---|---|---|
| アメリカ 🇺🇸 | 飛行機の大国。燃費の悪さに悩んでいる | rage_talking_cat／surprise_big_pupils_cat／cocky_dj_cat |
| ヨーロッパ 🇪🇺 | ライバル。ちょっと皮肉屋 | glare_disgusted_cat／slack_nail_filing_cat |
| 日本 🇯🇵 | 素材メーカーの社員（架空）。半導体の回と同じ“地味で謙虚”キャラ | talk_orange_white_sitting_cat／sleepy_old_memories_cat／meow_gray_white_kitten |

---

## 0. 冒頭
intro「これは、飛行機と“ある素材”をめぐる国と企業の関係を」
intro「もとに再構成したお話です。」
photo[ph01_airplane_sky]「空を飛ぶ旅客機。その体は、ずっと“金属”で作られてきました。」
photo[ph01_airplane_sky]「ところが今、その半分近くが\n“糸”から作られている飛行機があります。」

## 1. アメリカ、燃料代に泣く
Scene[bg01_us_hangar]（アメリカ=L, ヨーロッパ=R）
say L「燃料代、高すぎる……」［despair_dramatic_kitten］
add L「機体がもっと軽ければ……」
say R「アルミより軽くて、鉄より強いもの？　そんな都合のいいもの、あるわけないでしょ」［slack_nail_filing_cat］
zoom L「……あるらしいんだよ」(白)［realize_wet_cat_stare］
say R「は？」［huh_huh_cat］

## 2. 日本の“黒い糸”
Scene[bg02_jp_fiber_plant]（アメリカ=L, 日本=R）
say R「いらっしゃいませ。こちら、うちの“糸”です」［talk_orange_white_sitting_cat］
zoom L「糸！？　飛行機を糸で作れって！？」(黄)［surprise_big_pupils_cat］
photo[ph02_carbon_fiber]「炭素繊維。髪の毛の10分の1ほどの細さの、黒い糸です。」
photo[ph02_carbon_fiber]「樹脂で固めると、軽いのに、鉄より強くなると言われています。」
Scene[bg02_jp_fiber_plant]（アメリカ=L, 日本=R）
say R「釣りざおや、テニスのラケットにも使われてまして」［sleepy_old_memories_cat］
zoom L mid「軽い…」「強い…」「しかもサビない…」［stare_big_eyes_tabby_kitten］
zoom L「それで飛行機、作って！！」(赤, 集中線)［angry_aiming_cat］
say R「……がんばります」［meow_gray_white_kitten］

## 3. 787、誕生
intro「そして——」
photo[ph03_787_assembly]「ボーイング787。機体の重さのおよそ半分に、\n炭素繊維の複合材料が使われていると言われています。」
photo[ph03_787_assembly]「その炭素繊維は、日本の東レが長期契約で供給。」
photo[ph03_787_assembly]「主翼は三菱重工が作り、2007年に最初の主翼を出荷しました。」
photo[ph03_787_assembly]「日本の会社の受け持ちは35％を超えるとも言われ、\n“準国産機”と呼ばれることもあります。」
Scene[bg03_airport_gate]（アメリカ=L, ヨーロッパ=C, 日本=R）
say L「どう？　うちの787」［cocky_dj_cat］
say C「……ほぼ日本製じゃない？」［glare_disgusted_cat］
zoom L「言うな！！」(赤)［rage_talking_cat］
say R「いえいえ、アメリカさんの飛行機です」［talk_orange_white_sitting_cat］
say C「……で、うちにも糸、売ってくれる？」［slack_nail_filing_cat］
zoom L「ずるい！！」(黄)［sad_banana_cat_cry］

## 4. なぜ日本が強い？
photo[ph04_factory_furnace]「炭素繊維は、糸を何千度という高温で焼いて作ります。」
photo[ph04_factory_furnace]「東レ・帝人・三菱ケミカルなど日本の会社で、\n世界の過半から約7割を占めるとされています。」
photo[ph04_factory_furnace]「何十年も前、まだ使い道がはっきりしない頃から、\n作り続けてきたことが強みになった、と言われています。」
Scene[bg02_jp_fiber_plant]（アメリカ=L, 日本=R）
say L「なんでそんなに長く続けられたの？」［think_bike_front_seat_cat］
say R「最初は、釣りざおくらいしか売れなかったんですけどね」［sleepy_old_memories_cat］
add R「“いつか飛行機に”って、言い続けてたら……」
zoom L mid「……ほんとに」「飛んだ…」［realize_wet_cat_stare］

## 5. 締め
photo[ph05_sunset_runway]「派手な飛行機の陰で、黒い糸を作り続けてきた日本の会社。」
photo[ph05_sunset_runway]「空の上の“軽さ”は、地上の長い我慢から\n生まれたのかもしれません。」
Scene[bg04_rainbow_meadow]（アメリカ=L, ヨーロッパ=C, 日本=R）
say L「次は車も糸で作って！」［happy_chipi_chapa_cat］
say C「うちは自転車！」［dance_trending_cat］
say R「……順番にお作りします」［meow_gray_white_kitten］
ending［happy_girlfriend_dance_cat］

---

## 背景・写真（AIで作る・PHOTO:/ILLUST:）※実在の会社のロゴ・機体の塗装に似せない
- ph01_airplane_sky（PHOTO）… 青空を飛ぶ白い旅客機（ロゴなし）
- ph02_carbon_fiber（PHOTO）… 黒く光る炭素繊維の束・織物のアップ
- ph03_787_assembly（PHOTO）… 工場で組み立て中の大きな旅客機の胴体（ロゴなし）
- ph04_factory_furnace（PHOTO）… 工場の焼成炉、オレンジ色の光
- ph05_sunset_runway（PHOTO）… 夕焼けの滑走路と飛行機のシルエット
- bg01_us_hangar（ILLUST）… 飛行機の格納庫
- bg02_jp_fiber_plant（ILLUST）… 日本の素材工場、黒い糸の巻かれたボビンが並ぶ
- bg03_airport_gate（ILLUST）… 空港のゲート、窓の外に旅客機
- bg04_rainbow_meadow … 見本の st05_rainbow_meadow を使い回し可

## 確認メモ（2026-10-20 確認）
- 787 の機体重量のおよそ半分が炭素繊維複合材、日本企業の部品供給割合35%超、東レとボーイングの長期（16年）独占調達契約：投資テーマのまとめサイト（asset-alive）の記述のみ → 動画では「と言われています」「とも言われ」。**公開前にボーイング・東レの発表で確認**
- 三菱重工が787の複合材主翼を担当、2007年に初号機を出荷：三菱重工の公式プレスリリース
- 炭素繊維の日本勢シェア：「過半」（ニュースイッチ）〜「約7割」（Monoist、2012年）→「世界の過半から約7割を占めるとされています」
- 「髪の毛の10分の1ほどの細さ」「鉄より強い」「何十年も前から作り続けた」は一般的な説明として「と言われています」
- 「準国産機」は通称（報道でよく使われる呼び方）

## 出典
- 三菱重工 プレスリリース（787主翼の初号機出荷）https://www.mhi.com/jp/news/200705134581.html
- asset-alive（787と日本企業）https://www.asset-alive.com/thema/thema.php?tid=2358
- ニュースイッチ（炭素繊維）https://newswitch.jp/p/717
- Monoist「炭素繊維で世界シェア7割を占める日本企業」https://monoist.itmedia.co.jp/mn/articles/1205/31/news001.html
