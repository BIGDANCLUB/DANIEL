# 【寸劇】世界2位の“最強パスポート”　なのに日本人の5人に4人が持っていない？（原稿 v1）

- 調査・台本: 別セッション（猫ミーム時事ネタ分析）。番号は制作側で振る
- 形式: **「寸劇」シリーズ**（README・`docs/sungeki_reference.md`・`story_style.py`・見本 `story_18_demo.py`）。書き方は `sungeki_semicon.md` と同じ
- ジャンル: 国旗つきの猫が並ぶ“ランキング発表”型の寸劇＋30〜40代向けの「お金（手数料が7月から安くなった・出国税は上がった）」
- 想定尺: 約5〜6分
- 書き方: `intro「」`／`photo[写真名]「」`／`Scene[背景名]（役名=位置）`／`say`・`add`／`zoom`／`zoom mid`／`ending`。［猫］は仮

## ルール（必ず守る）
- 冒頭で「再構成したお話」と書く。国どうしの会話は作り話
- 他国をバカにしない（順位の低い国をいじらない）。登場する国は上位の国だけ
- 数字は確認メモどおり。順位は**「2026年1月版」「7月版」と版を書く**
- パスポートを取らない理由は**「と言われている」**（調査の数字ではないため）
- 語尾に「にゃ」なし。単語の途中で改行しない。AIで作った背景・写真は概要欄に

## 配役
| 役名（札） | キャラ | 猫の例 |
|---|---|---|
| シンガポール 🇸🇬 | 1位。余裕がある | showoff_gojo_cosplay_cat／cocky_dj_cat |
| 韓国 🇰🇷 | 2位タイ。日本と仲良くライバル | dance_trending_cat／happy_girlfriend_dance_cat |
| 日本 🇯🇵 | 2位タイ。なぜかあまり使っていない | sleepy_sleepy_cat／blank_black_cat_zoning_out／surprise_big_pupils_cat |
| 日本の会社員 🇯🇵 | 30代（架空）。海外に行きたいけど行けない | sulk_hungry_cat／work_typing_cat／happy_chipi_chapa_cat |

---

## 0. 冒頭
intro「これは、世界の“パスポートの強さ”ランキングを」
intro「もとに再構成したお話です。」
photo[ph01_passports]「パスポートの強さは、ビザなしで行ける国や地域の数で比べられます。」
photo[ph01_passports]「毎年発表される世界ランキングで、\n日本はずっと上位の常連です。」

## 1. ランキング発表
Scene[bg01_award_stage]（シンガポール=L, 韓国=C, 日本=R）
photo[ph02_ranking_board]「2026年1月版。1位はシンガポール、192か所。」
photo[ph02_ranking_board]「2位は日本と韓国、188か所。」
Scene[bg01_award_stage]（シンガポール=L, 韓国=C, 日本=R）
say L「今年も1位、いただきました」［showoff_gojo_cosplay_cat］
say C「日本、2位タイだって！　やったね！」［dance_trending_cat］
say R「……あ、うん」［sleepy_sleepy_cat］
zoom C「テンション低っ！！」(黄)［huh_huh_cat］
say R「いや……うちの国民、あんまり持ってないから……」［blank_black_cat_zoning_out］
zoom L「は？」(白)［glare_disgusted_cat］

## 2. 5人に4人が持っていない
photo[ph03_empty_passport_office]「日本で有効なパスポートを持っている人は、\n2025年末で約17.8％。（外務省の旅券統計から計算）」
photo[ph03_empty_passport_office]「5人のうち4人は、\n“今すぐ海外に行ける状態”ではないことになります。」
Scene[bg01_award_stage]（シンガポール=L, 韓国=C, 日本=R）
zoom C「世界2位の最強パスポートなのに！？」(赤, 集中線)［surprise_big_pupils_cat］
say L「伝説の剣を持ってるのに、家の押し入れにしまってる勇者……」［slack_nail_filing_cat］
say R「……返す言葉もない」［sad_banana_cat_cry］

## 3. 日本の会社員に聞いてみた
Scene[bg02_jp_office]（韓国=L, 日本の会社員=R）
say L「なんでパスポート取らないの？」［think_bike_front_seat_cat］
say R「まず、休みが取れない……」［sulk_hungry_cat］
add R「円安で、海外が高い……」
add R「英語も、ちょっと不安……」
add R「あと、パスポート代も高かった……」
photo[ph04_yen_coins]「休みの取りにくさ、円安、言葉の不安。\nパスポートを持たない理由として、よく挙げられると言われています。」
Scene[bg02_jp_office]（韓国=L, 日本の会社員=R）
zoom L mid「わかる…」「でも…」「もったいない…」［realize_wet_cat_stare］

## 4. 2026年7月、パスポートが安くなった
intro「そして2026年7月——」
photo[ph05_passport_counter]「パスポートの手数料が下がりました。」
photo[ph05_passport_counter]「18歳以上は10年用に一本化され、\n窓口の申請で16,300円 → 9,300円に。オンライン申請なら8,900円。」
Scene[bg02_jp_office]（韓国=L, 日本の会社員=R）
zoom R「7,000円も安くなった！？」(赤, 集中線)［happy_chipi_chapa_cat］
say L「よかったじゃん！」［happy_girlfriend_dance_cat］
photo[ph06_departure_gate]「ただし同じ7月から、日本を出るときにかかる“出国税”が\n1,000円 → 3,000円に上がりました。」
Scene[bg02_jp_office]（韓国=L, 日本の会社員=R）
zoom R「……上がってるやつもある！！」(黄)［rage_talking_cat］
say L「でも、10年に1回の手数料が7,000円下がって、出国税は1回2,000円アップ……」［work_typing_cat］
add L「年に1回くらいの旅行なら、まあトントン？」
say R「計算させないで……」［blank_black_cat_zoning_out］

## 5. 実は、少しずつ“弱く”なっている？
photo[ph07_world_map]「実は日本のビザなし渡航先は、前の年の193から188に減りました。」
photo[ph07_world_map]「2026年7月版では、日本は韓国・UAEと並んで2位を保っています。」
Scene[bg01_award_stage]（シンガポール=L, 韓国=C, 日本=R）
say L「持ってるうちに、使わなきゃ」［showoff_gojo_cosplay_cat］
say C「次は一緒に旅行しよ！」［dance_trending_cat］
zoom R mid「……持つか」「……パスポート」［stare_big_eyes_tabby_kitten］

## 6. 締め
photo[ph08_sunset_plane]「世界でも指折りの“強いパスポート”。」
photo[ph08_sunset_plane]「その力を使うかどうかは、\n引き出しの中から取り出す、ほんの少しの勇気なのかもしれません。」
Scene[bg03_rainbow_meadow]（シンガポール=L, 日本=C, 日本の会社員=R）
say R「オンラインで申請してきた！」［happy_chipi_chapa_cat］
say C「えらい！」［dance_trending_cat］
say L「ようこそ、世界へ」［wave_waving_cat］
ending［happy_girlfriend_dance_cat］

---

## 背景・写真（AIで作る・PHOTO:/ILLUST:）※実在のパスポートのデザイン・国章をそのまま描かない（色だけそれっぽく）
- ph01_passports（PHOTO）… 色の違うパスポートが机に並ぶ（表紙の文字・紋章はぼかし）
- ph02_ranking_board（ILLUST）… 表彰台と順位のボード（国名・数字は字幕で出すので絵には書かない）
- ph03_empty_passport_office（PHOTO）… がらんとした役所の窓口
- ph04_yen_coins（PHOTO）… 1円玉・100円玉が散らばる
- ph05_passport_counter（PHOTO）… パスポートの申請窓口（文字なし）
- ph06_departure_gate（PHOTO）… 空港の出国ゲート
- ph07_world_map（ILLUST）… 世界地図に飛行機の線
- ph08_sunset_plane（PHOTO）… 夕焼けを飛ぶ飛行機
- bg01_award_stage（ILLUST）… 表彰式のステージ
- bg02_jp_office（ILLUST）… 日本のオフィス、パソコンの並ぶ机
- bg03_rainbow_meadow … 見本の st05_rainbow_meadow を使い回し可

## 確認メモ（2026-10-20 確認）
- ヘンリー・パスポート・インデックス 2026年1月版：1位シンガポール192、2位日本・韓国188。日本は前回の3位から上昇、渡航先は前年の193から188へ減少（Impress トラベル Watch・Time Out・訪日ラボ）
- 2026年7月版：日本は韓国・UAEと並ぶ2位を維持（8/4付報道）。7月版の日本の渡航先数は未確認 → 動画では数を出さない
- パスポート保有率：2025年末の有効旅券 2,193万302冊、総人口から算出して約17.8%（前年約16.8%）（トラベルボイス・外務省旅券統計）。「約18%・5人に4人は海外へ行ける状態にない」（日本ワーキング・ホリデー協会）
- 手数料：2026年7月1日から、18歳以上は10年用に統一、窓口16,300円→9,300円、電子申請8,900円。18歳未満（5年用）窓口4,800円・電子4,400円（埼玉県・徳島県の案内ほか）。2026年4月に改正旅券法が成立 → **外務省の公式ページで最終確認**
- 出国税（国際観光旅客税）：2026年7月から1,000円→3,000円（報道）→ **公式で最終確認**
- パスポートを持たない理由（休み・円安・言葉）：一般的な説明として「と言われています」

## 出典
- Impress トラベル Watch https://travel.watch.impress.co.jp/docs/news/2077733.html
- Time Out Tokyo（2026年の最強パスポート）https://www.timeout.jp/tokyo/ja/news/in-the-world-the-most-powerful-passports-in-2026-with-one-european-country-jumping-from-sixth-to-third-place-012726
- 訪日ラボ https://yamatogokoro.jp/inbound_data/60879/
- トラベルボイス（旅券統計・保有率）https://www.travelvoice.jp/20260224-159307
- 埼玉県「パスポートの手数料が変わります」https://www.pref.saitama.lg.jp/b0301/202607ryoken.html
- マネーフォワード クラウド（手数料と出国税）https://media.moneyforward.com/articles/10786
