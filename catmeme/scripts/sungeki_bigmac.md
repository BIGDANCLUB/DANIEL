# 【寸劇】ビッグマックが“世界の半額”　日本は安い国になった？（原稿 v1）

- 調査・台本: 別セッション（猫ミーム時事ネタ分析）。番号は制作側で振る
- 形式: **「寸劇」シリーズ**（README・`docs/sungeki_reference.md`・`story_style.py`・見本 `story_18_demo.py`）。書き方は `sungeki_semicon.md` と同じ
- ジャンル: 「日本と世界」型（世界との比較）＋30〜40代の「お金」（物価・給料）
- **想定尺: 約8分（約130カット）**。目安：冒頭0:40／1 1:00／2 1:00／3 1:20／4 1:00／5 1:30／6 0:50／締め0:40
- 書き方: `intro「」`／`photo[写真名]「」`／`Scene[背景名]（役名=位置）`（札に小さい国旗）／`say`・`add`／`zoom`／`zoom mid`／`ending`。［猫］は仮

## ルール（必ず守る）
- 冒頭で「再構成したお話」と書く。登場人物はすべて架空。店員は「ハンバーガー店の店員」（実在の会社の社員として描かない）。会社名は語りの事実説明だけ
- 他国をバカにしない（スイス・アメリカは“物価の高い国の人”として明るく）
- ビッグマック指数は「物価と為替の目安」であって、給料を直接比べるものではない → 台詞で「〜ってことかも」くらいに
- 暗くしすぎない。最後は「少し明るい数字」で終える
- 数字は確認メモどおり（版・時点を必ず書く）
- 語尾に「にゃ」なし。単語の途中で改行しない。AIで作った背景・写真・イラストは概要欄に

## 配役
| 役名（札） | キャラ | 猫の例 |
|---|---|---|
| アメリカの旅行者 🇺🇸 | 日本は安くて天国だと思っている | dance_edm_cat／surprise_big_pupils_cat／happy_chipi_chapa_cat |
| 日本の友だち 🇯🇵 | 30代の会社員。値上げに疲れている | work_typing_cat／sulk_hungry_cat／blank_black_cat_zoning_out |
| スイスの旅行者 🇨🇭 | 物価の高い国から来た。余裕がある | showoff_gojo_cosplay_cat／cocky_dj_cat |
| ハンバーガー店の店員 🇯🇵 | 明るい | wave_waving_cat／happy_girlfriend_dance_cat |

---

## 0. 冒頭（約40秒）
intro「これは、世界中で売られている“ある食べ物”の値段を」
intro「もとに再構成したお話です。」
photo[ph01_burger]「どの国でも、ほぼ同じ材料、同じ作り方で売られているハンバーガー。」
photo[ph01_burger]「その値段を比べると、\nその国の“物価”と“お金の強さ”が見えてくると言われています。」

## 1. 「安っ！！」（約1分）
Scene[bg01_burger_shop]（アメリカの旅行者=L, ハンバーガー店の店員=C, 日本の友だち=R）
say C「いらっしゃいませ！」［wave_waving_cat］
say L「ビッグマックください！」［happy_chipi_chapa_cat］
say C「500円です！」［wave_waving_cat］
say L「500円って……ドルでいくら？」［think_bike_front_seat_cat］
say R「1ドル160円くらいだから……3ドルちょっと」［work_typing_cat］
zoom L「安っ！！！」(赤, 集中線)［surprise_big_pupils_cat］
say L「アメリカの半分くらいじゃない！？」［dance_edm_cat］
add L「日本、天国じゃん！」
say R「え……安いの……？」［huh_huh_cat］
add R「2月に値上げしたばっかりなんだけど……」
zoom R mid「…毎月」「…何かしら」「…値上げしてるんだけど…」［blank_black_cat_zoning_out］

## 2. ビッグマック指数ってなに？（約1分）
photo[ph02_economist_chart]「“ビッグマック指数”。イギリスの経済誌エコノミストが\n1986年から発表している、世界のビッグマックの値段の比べ方です。」
photo[ph02_economist_chart]「同じものが、国によっていくらで売られているかを比べて、\nその国のお金が“高すぎるか、安すぎるか”の目安にします。」
Scene[bg01_burger_shop]（アメリカの旅行者=L, 日本の友だち=R）
say L「つまり、日本のビッグマックが安いってことは……」［think_bike_front_seat_cat］
say R「円が、ドルに比べて“安く見られてる”ってこと」［work_typing_cat］
photo[ph03_yen_dollar]「2026年1月の調査では、円はドルに対して\nおよそ5割“割安”とされています。」
zoom R「5割引き！？」(黄)［surprise_big_pupils_cat］
say L「日本、まるごとセール中！」［cocky_dj_cat］
say R「言い方……」［glare_disgusted_cat］

## 3. スイスの旅行者、登場（約1分20秒）
Scene[bg01_burger_shop]（アメリカの旅行者=L, スイスの旅行者=C, 日本の友だち=R）
say C「あら、ビッグマック500円？　かわいいお値段」［showoff_gojo_cosplay_cat］
say R「……ちなみに、スイスではいくら？」［sulk_hungry_cat］
say C「1,200円は超えるかしら」［cocky_dj_cat］
zoom R「1,200円！？　ハンバーガー1個で！？」(赤, 集中線)［surprise_big_pupils_cat］
photo[ph04_world_prices]「スイスのビッグマックは、2025年の計算で1個1,207円。\n世界でもいちばん高い国のひとつです。」
photo[ph04_world_prices]「日本は、2017年7月の調査で380円、57か国中33番目。\n2024年7月には480円で、44番目になりました。」
Scene[bg01_burger_shop]（アメリカの旅行者=L, スイスの旅行者=C, 日本の友だち=R）
say R「値段は上がってるのに、順位は下がってる……？」［think_bike_front_seat_cat］
say C「ほかの国が、もっと上がってるのよ」［slack_nail_filing_cat］
zoom R mid「日本だけ…」「ゆっくり…」「置いていかれてる…」［realize_wet_cat_stare］

## 4. 昔は“高い国”だった（約1分）
photo[ph05_old_tokyo]「2000年ごろ、アメリカの人が日本でビッグマックを買えば、\n“日本は物価が高い国だ”と感じたはず、と言われています。」
photo[ph05_old_tokyo]「今は、その関係が逆になりました。」
Scene[bg02_street_night]（アメリカの旅行者=L, 日本の友だち=R）
say L「昔は日本が“高い国”だったの！？」［huh_goat_talks_to_huh_cat］
say R「親の世代は、“海外は安い”って言ってたらしい」［sleepy_old_memories_cat］
add R「今は、海外に行くと全部高い……」
say L「だから、日本の人あんまり海外に来ないのか……」［think_bike_front_seat_cat］
say R「ラーメン1杯が、日本の何倍もするって聞くと、ね」［sad_banana_cat_cry］

## 5. 給料の話（約1分30秒）
Scene[bg03_office]（日本の友だち=L）
say L「（翌日の会社）……そもそも、なんで日本は安くなったんだろ」［work_typing_cat］
photo[ph06_paycheck]「2025年、日本の給料は、金額では前の年より2.3％増えました。」
photo[ph06_paycheck]「でも、物価は3.7％上がりました。」
photo[ph06_paycheck]「物価の上がり方を差し引いた“実質賃金”は1.3％のマイナス。\n4年続けてのマイナスです。（厚生労働省）」
Scene[bg03_office]（日本の友だち=L）
zoom L「給料、上がったのに、減ってる……！？」(赤, 集中線)［despair_dramatic_kitten］
say L「お給料が2％増えても、買うものが4％近く高くなったら……」［blank_black_cat_zoning_out］
add L「そりゃ、生活は苦しくなるよね」
Scene[bg02_street_night]（アメリカの旅行者=L, スイスの旅行者=C, 日本の友だち=R）
say C「わたしたちの国は、物価も高いけど、お給料も高いの」［showoff_gojo_cosplay_cat］
say L「旅行で来るわたしたちには、日本は天国だけど……」［sleepy_old_memories_cat］
add L「住んでる人には、ちょっと大変なんだね」
say R「うれしいような、さみしいような……」［sulk_hungry_cat］

## 6. ちょっとだけ、光（約50秒）
photo[ph07_sunrise_city]「ただ、2026年1〜3月には、\n実質賃金は前の年より1.3％のプラスに転じました。」
Scene[bg02_street_night]（アメリカの旅行者=L, 日本の友だち=R）
zoom R「……プラス！？」(黄)［surprise_big_pupils_cat］
say L「よかったじゃん！」［happy_chipi_chapa_cat］
say R「まだ、ほんの少しだけどね」［work_typing_cat］
add R「でも、ちょっとだけ前向きになれる」
say L「じゃあ、お給料が上がったら、次はアメリカに来てね！　案内するから！」［dance_edm_cat］
zoom R「ハンバーガー、1個いくら……？」(白)［think_bike_front_seat_cat］
say L「……それは聞かないで」［blank_black_cat_zoning_out］

## 7. 締め（約40秒）
photo[ph08_sunset_burger]「500円のハンバーガー。海の向こうの人には“天国の値段”。」
photo[ph08_sunset_burger]「でも、その安さの裏には、わたしたちの給料と暮らしの話が\nかくれているのかもしれません。」
Scene[bg04_rainbow_meadow]（アメリカの旅行者=L, スイスの旅行者=C, 日本の友だち=R）
say C「次はスイスにも来てね」［showoff_gojo_cosplay_cat］
say R「……ビッグマック、2個分の値段で1個か……」［sulk_hungry_cat］
say L「おごるよ！！」［happy_chipi_chapa_cat］
ending［happy_girlfriend_dance_cat］

---

## 背景・写真・イラスト（AIで作る）※実在の店のロゴ・制服・包装に似せない
- ph01_burger（PHOTO）… 白い背景に大きなハンバーガー（包装・ロゴなし）
- ph02_economist_chart（ILLUST）… 世界地図と棒グラフ（数字は字幕で出す）
- ph03_yen_dollar（PHOTO）… 円の硬貨とドルの紙幣が並ぶ
- ph04_world_prices（ILLUST）… 国旗の前にハンバーガーが並ぶ（値段は字幕で出す）
- ph05_old_tokyo（PHOTO）… 少し古い雰囲気の東京の繁華街の夜（2000年ごろ風）
- ph06_paycheck（PHOTO）… 給与明細と電卓（文字・数字はぼかし）
- ph07_sunrise_city（PHOTO）… 朝日が昇る街並み
- ph08_sunset_burger（PHOTO）… 夕焼けの窓辺にハンバーガー
- bg01_burger_shop（ILLUST）… ハンバーガー店のカウンター（ロゴなし）
- bg02_street_night（ILLUST）… 夜の街を歩く道
- bg03_office（ILLUST）… 日本のオフィスの机
- bg04_rainbow_meadow … 見本の st05_rainbow_meadow を使い回し可

## 確認メモ（2026-10-21 確認）
- 日本のビッグマック単品：2026年2月25日から480円 → 500円（初の500円台）（Impress Watch ほか）
- ビッグマック指数：The Economist が1986年から発表、購買力平価の考え方（monex・babypips）。為替の目安で、正確な測定ではない
- 2026年1月版：円はドルに対して約50%割安（statbase・bigmacindex.app などの二次資料）→ **公開前に The Economist の原表で確認**
- スイス 1個1,207円（2025年、1ドル151.08円で計算）（ファイナンシャルフィールド）
- 日本：2017年7月 380円・57か国中33位（limo 等）、2024年7月 480円・44位・−43.9%（ファイナンシャルフィールド）
- 「2000年ごろ、アメリカ人は日本を物価が高いと感じたはず」（東洋経済の記事の趣旨）→「と言われています」。2000年の円価格は出さない
- 実質賃金：2025年（暦年）−1.3%、4年連続マイナス。名目の現金給与総額 +2.3%（5年連続プラス）、消費者物価 +3.7%（厚労省 毎月勤労統計、共同・秋田魁）。2026年1〜3月期 +1.3%（共同・秋田魁）→ **公開前に厚労省の公表値で確認**
- 「1ドル160円くらい」：為替は公開時の値で調整
- 「ラーメン1杯が日本の何倍も」は台詞（一般的な話）。数字は出さない

## 出典
- Impress Watch（ビッグマック500円）https://www.watch.impress.co.jp/docs/news/2088070.html
- statbase（Big Mac Index 2026年1月）https://statbase.org/datasets/indexes-and-ratings/bigmac-index/
- ファイナンシャルフィールド（ビッグマック指数）https://financial-field.com/living/entry-208598
- マネクラ（ビッグマック指数とは）https://media.monex.co.jp/ud/glossary/670f1458a53aefceba000014
- 東洋経済 https://toyokeizai.net/articles/-/208990
- 秋田魁新報（共同）「実質賃金4年連続マイナス 25年、1・3%減」https://www.sakigake.jp/news/article/20260209CO0066/
- 秋田魁新報（共同）「25年度の実質賃金0・5%減 4年連続」https://www.sakigake.jp/news/article/20260522CO0038/
