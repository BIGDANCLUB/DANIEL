;===========================================================
; chap2_mermaid.ks - 人魚
; バトルシステム対応版: 5択、2ミスでHシーン
;===========================================================
*mermaid_start

[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]

[fadein time="800"]

[nm t="ナレーション"]
地下水路の奥に広がる暗い水面。水底が見えないほど深い、黒い水だ。[p]

[nm t="ナレーション"]
その時——水面から美しい声が響いてきた。歌声。人間の言葉ではないが、どこか心地よい。[p]

[nm t="人魚"]
「……♪……おいで、勇者……水の中は、気持ちいいよ……♪」[p]

;===========================================================
; 選択肢1
;===========================================================
*mermaid_c1_prompt

どうする？[r]
[link target="*mermaid_c1_safe"]耳を塞いで歌声を遮断する[endlink][r]
[link target="*mermaid_c1_wrong"]歌声の方向を調べようと耳を傾ける[endlink][r]
[s]

*mermaid_c1_safe
[nm t="ナレーション"]
耳を塞ぐと歌の魅力が薄れた。冷静に水面を観察できる。[p]
[jump target="*mermaid_c2_prompt"]

*mermaid_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
歌声に引き寄せられ、気づけば水辺まで歩み寄っていた。[p]
[nm t="人魚"]
「……ちかい。もうすこし……♪」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*mermaid_h_dispatch"]
[endif]
[nm t="ナレーション"]
かろうじて状況から抜け出す。だが状況は悪化している。[p]
[jump target="*mermaid_c2_prompt"]

;===========================================================
; 選択肢2
;===========================================================
*mermaid_c2_prompt

どうする？[r]
[link target="*mermaid_c2_safe"]水辺に落ちた石を投げて様子を見る[endlink][r]
[link target="*mermaid_c2_wrong"]水面を覗き込んで何がいるか見ようとする[endlink][r]
[s]

*mermaid_c2_safe
[nm t="ナレーション"]
石が落ちると水面が揺れ、人魚の輪郭が水中に見えた。[p]
[jump target="*mermaid_c3_prompt"]

*mermaid_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
水面に映る自分の顔——その瞬間、水中から手が伸びてきた。[p]
[nm t="人魚"]
「……かお、みえた。かわいい……ひっぱる」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*mermaid_h_dispatch"]
[endif]
[nm t="ナレーション"]
かろうじて状況から抜け出す。だが状況は悪化している。[p]
[jump target="*mermaid_c3_prompt"]

;===========================================================
; 選択肢3
;===========================================================
*mermaid_c3_prompt

どうする？[r]
[link target="*mermaid_c3_safe"]加護の力で水を押しのけながら進む[endlink][r]
[link target="*mermaid_c3_wrong"]人魚の歌に合わせて口ずさんでしまう[endlink][r]
[s]

*mermaid_c3_safe
[nm t="ナレーション"]
加護の光が水面を照らし、人魚が怯んで水中に沈んだ。[p]
[jump target="*mermaid_c4_prompt"]

*mermaid_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
歌に合わせると、身体が勝手に水辺へ引き寄せられる。[p]
[nm t="人魚"]
「……いっしょに、うたった。なかまだ……ついてきて……♪」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*mermaid_h_dispatch"]
[endif]
[nm t="ナレーション"]
かろうじて状況から抜け出す。だが状況は悪化している。[p]
[jump target="*mermaid_c4_prompt"]

;===========================================================
; 選択肢4
;===========================================================
*mermaid_c4_prompt

どうする？[r]
[link target="*mermaid_c4_safe"]岸壁の突起を掴んで身体を固定する[endlink][r]
[link target="*mermaid_c4_wrong"]水の中から伸びてくる手に手を伸ばしてしまう[endlink][r]
[s]

*mermaid_c4_safe
[nm t="ナレーション"]
岸壁を掴んで固定し、引っ張られても動かない。人魚が諦めた。[p]
[jump target="*mermaid_c5_prompt"]

*mermaid_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
手を取った瞬間、強い力で水中へ引き込まれた。[p]
[nm t="人魚"]
「……て、つないだ。いっしょに、いこう……♪」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*mermaid_h_dispatch"]
[endif]
[nm t="ナレーション"]
かろうじて状況から抜け出す。だが状況は悪化している。[p]
[jump target="*mermaid_c5_prompt"]

;===========================================================
; 選択肢5
;===========================================================
*mermaid_c5_prompt

どうする？[r]
[link target="*mermaid_c5_safe"]一気に走り抜けて水場を通過する[endlink][r]
[link target="*mermaid_c5_wrong"]水の心地よさに一瞬足を止めてしまう[endlink][r]
[s]

*mermaid_c5_safe
[nm t="ナレーション"]
全速力で走り抜けた。人魚の歌も足には追いつかない。[p]
[jump target="*mermaid_win"]

*mermaid_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
足を止めた瞬間、水面下から複数の腕が伸びてきた。[p]
[nm t="人魚"]
「……とまった。もうにがさない……ずっと、いっしょ……♪」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*mermaid_h_dispatch"]
[endif]
[jump target="*mermaid_h_dispatch"]

;===========================================================
; Hシーン振り分け
;===========================================================
*mermaid_h_dispatch
[if exp="f.enemy_last_mistake==1"]
[jump target="*mermaid_h1"]
[endif]
[if exp="f.enemy_last_mistake==2"]
[jump target="*mermaid_h2"]
[endif]
[if exp="f.enemy_last_mistake==3"]
[jump target="*mermaid_h3"]
[endif]
[if exp="f.enemy_last_mistake==4"]
[jump target="*mermaid_h4"]
[endif]
[jump target="*mermaid_h5"]

;===========================================================
; Hシーン1
;===========================================================
*mermaid_h1
[eval exp="f.scene_mermaid_h1=1"]

[nm t="ナレーション"]
水中に引き込まれ、人魚に抱きしめられた。水の中でも息ができる——人魚の魔法か。美しい尾が身体に絡みつき、水中をゆっくりと踊るように動く。冷たいはずの水が、不思議と温かく感じる。人魚の歌声が水中に響き、全身の感覚が鋭くなっていく。[p]

[call storage="system/init.ks" target="*squeeze_event"]

[nm t="ナレーション"]
やがて人魚は満足し、静かに離れていった。[p]

[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

;===========================================================
; Hシーン2
;===========================================================
*mermaid_h2
[eval exp="f.scene_mermaid_h2=1"]

[nm t="ナレーション"]
手を引かれたまま深みへ。水圧が全身を優しく押し包む。人魚の長い銀髪が全身に絡みつき、滑らかな肌が密着する。水の中でこそ、人魚は本来の力を発揮する——全身で絡み合い、奥深くまで引き込んでいく。[p]

[call storage="system/init.ks" target="*squeeze_event"]

[nm t="ナレーション"]
やがて人魚は満足し、静かに離れていった。[p]

[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

;===========================================================
; Hシーン3
;===========================================================
*mermaid_h3
[eval exp="f.scene_mermaid_h3=1"]

[nm t="ナレーション"]
人魚の歌が脳に直接響くような感覚。水中で感度が増し、人魚の動きに全身が反応してしまう。美しい歌に包まれながら、深い水の底で——意識が溶けていく。[p]

[call storage="system/init.ks" target="*squeeze_event"]

[nm t="ナレーション"]
やがて人魚は満足し、静かに離れていった。[p]

[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

;===========================================================
; Hシーン4
;===========================================================
*mermaid_h4
[eval exp="f.scene_mermaid_h4=1"]

[nm t="ナレーション"]
水面から引き込まれる瞬間、人魚と目が合った。深い青の瞳。水中で見つめ合いながら、尾びれが足に絡みつく。人魚は丁寧に、慈しむように——全身を使って搾り取っていく。[p]

[call storage="system/init.ks" target="*squeeze_event"]

[nm t="ナレーション"]
やがて人魚は満足し、静かに離れていった。[p]

[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

;===========================================================
; Hシーン5
;===========================================================
*mermaid_h5
[eval exp="f.scene_mermaid_h5=1"]

[nm t="ナレーション"]
深い水底まで引き込まれた。上を見ると、遠く水面の光が見える。人魚が歌いながら、全身で抱きしめてくる。水の中、時間を忘れた空間で、長い長い時間をかけて。[p]

[call storage="system/init.ks" target="*squeeze_event"]

[nm t="ナレーション"]
やがて人魚は満足し、静かに離れていった。[p]

[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

;===========================================================
; 勝利
;===========================================================
*mermaid_win
[eval exp="f.b1f_mermaid=1"]

[nm t="ナレーション"]
水面が静まり返った。人魚は深みに引き退いていった。水場を越え、先の通路へ進む。[p]

[fadeout time="800" color="0x000000"]
[wait time=300]
[jump storage="chap2_explore.ks" target="*hub_b1f"]