;=== chap2_mimic.ks - ミミック ===
*mimic_start
[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]
[fadein time="800"]
[nm t="ナレーション"]
宝物庫の一角。金貨や宝石が散らばる中、ひときわ大きな宝箱が目を引く。[p]
[nm t="ナレーション"]
鍵穴に淡い光が見える。どこか不自然な輝きだ。[p]
[nm t="ミミック"]
「……ごそごそ……おいで、おいで……」[p]
*mimic_c1_prompt
どうする？[r]
[link target="*mimic_c1_safe"]周囲を調べてから宝箱を観察する[endlink][r]
[link target="*mimic_c1_wrong"]すぐに宝箱に近づいて開けようとする[endlink][r]
[s]
*mimic_c1_safe
[nm t="ナレーション"]
慎重に観察すると、宝箱の隅に微かな粘液の跡を発見した。罠だ。[p]
[jump target="*mimic_c2_prompt"]
*mimic_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
近づいた瞬間、蓋が勢いよく開き触手が飛び出した。[p]
[nm t="ミミック"]
「……おそい。でも、きた」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*mimic_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*mimic_c2_prompt"]
*mimic_c2_prompt
どうする？[r]
[link target="*mimic_c2_safe"]加護の光で鍵穴を調べる[endlink][r]
[link target="*mimic_c2_wrong"]鍵穴に手を入れて確かめる[endlink][r]
[s]
*mimic_c2_safe
[nm t="ナレーション"]
光を当てると粘液が滴っているのが見えた。やはり罠だ。[p]
[jump target="*mimic_c3_prompt"]
*mimic_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
指先が入った途端、ぬめりとした何かが絡みついた。[p]
[nm t="ミミック"]
「……てを、つかまえた。もっと、こっちに」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*mimic_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*mimic_c3_prompt"]
*mimic_c3_prompt
どうする？[r]
[link target="*mimic_c3_safe"]剣で蓋を叩いて反応を見る[endlink][r]
[link target="*mimic_c3_wrong"]蓋の隙間から中を覗き込む[endlink][r]
[s]
*mimic_c3_safe
[nm t="ナレーション"]
剣で叩くと宝箱全体がびくりと震えた。やはり生き物だ。[p]
[jump target="*mimic_c4_prompt"]
*mimic_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
顔を近づけた瞬間、甘い香りで視界がぼやける。[p]
[nm t="ミミック"]
「……かおが、ちかい。いいにおい」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*mimic_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*mimic_c4_prompt"]
*mimic_c4_prompt
どうする？[r]
[link target="*mimic_c4_safe"]一気に距離を取る[endlink][r]
[link target="*mimic_c4_wrong"]宝箱の側面を蹴る[endlink][r]
[s]
*mimic_c4_safe
[nm t="ナレーション"]
素早く後退して触手が空振りした。[p]
[jump target="*mimic_c5_prompt"]
*mimic_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
蹴った足が粘液で固定され引き寄せられた。[p]
[nm t="ミミック"]
「……あし、つかまえた。もうにげられない」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*mimic_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*mimic_c5_prompt"]
*mimic_c5_prompt
どうする？[r]
[link target="*mimic_c5_safe"]加護の光を爆発させて突破する[endlink][r]
[link target="*mimic_c5_wrong"]触手をくぐり抜けようとする[endlink][r]
[s]
*mimic_c5_safe
[nm t="ナレーション"]
光の爆発でミミックが怯んだ隙に走り抜けた。[p]
[jump target="*mimic_win"]
*mimic_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
触手を避けきれず全身に絡みつかれた。[p]
[nm t="ミミック"]
「……ぜんぶ、つかまえた。ゆっくり、たのしむ」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*mimic_h_dispatch"][endif]
[jump target="*mimic_h_dispatch"]
*mimic_h_dispatch
[if exp="f.enemy_last_mistake==1"][jump target="*mimic_h1"][endif]
[if exp="f.enemy_last_mistake==2"][jump target="*mimic_h2"][endif]
[if exp="f.enemy_last_mistake==3"][jump target="*mimic_h3"][endif]
[if exp="f.enemy_last_mistake==4"][jump target="*mimic_h4"][endif]
[jump target="*mimic_h5"]
*mimic_h1
[eval exp="f.scene_mimic_h1=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="mimic_h1_01"]              ← CG①（最初）
[nm t="ナレーション"]
宝箱の中に引き込まれた。内側は広く温かく湿った空間だった。粘液がゆっくりと全身を包み込み、服を溶かすように滲み込んでくる。ミミックの意思なのか、粘液が性感帯を正確に捉えじわじわと刺激し続ける。[p]
; [cg f="mimic_h1_02"]              ← CG②
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてミミックは離れていった。[p]
; [cg f="mimic_h1_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]
*mimic_h2
[eval exp="f.scene_mimic_h2=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="mimic_h2_01"]              ← CG①（最初）
[nm t="ナレーション"]
鍵穴から入り込んだ粘液が腕を這い上がり全身へと広がっていく。ゆっくりと、じっくりと全身に回っていく。ミミックは焦らない——時間をかけて余すことなく味わうように。[p]
; [cg f="mimic_h2_02"]              ← CG②
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてミミックは離れていった。[p]
; [cg f="mimic_h2_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]
*mimic_h3
[eval exp="f.scene_mimic_h3=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="mimic_h3_01"]              ← CG①（最初）
[nm t="ナレーション"]
甘い香りで理性が朦朧とする中、宝箱の蓋が閉まった。暗闇の中粘液が全身を包む。香りがさらに濃くなり身体の感度が増す。ミミックにとってこの状態の獲物こそ最上のご馳走だ。[p]
; [cg f="mimic_h3_02"]              ← CG②
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてミミックは離れていった。[p]
; [cg f="mimic_h3_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]
*mimic_h4
[eval exp="f.scene_mimic_h4=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="mimic_h4_01"]              ← CG①（最初）
[nm t="ナレーション"]
足首を固定されたまま宝箱が近づいてくる。蓋が開き粘液が足首からゆっくり這い上がる——抵抗できない。[p]
; [cg f="mimic_h4_02"]              ← CG②
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてミミックは離れていった。[p]
; [cg f="mimic_h4_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]
*mimic_h5
[eval exp="f.scene_mimic_h5=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="mimic_h5_01"]              ← CG①（最初）
[nm t="ナレーション"]
全身を触手に包まれ宝箱の内部へ引き込まれた。暗く温かい空間でミミックは時間をかけてじっくりと全てを絞り取っていく。[p]
; [cg f="mimic_h5_02"]              ← CG②
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてミミックは離れていった。[p]
; [cg f="mimic_h5_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]
*mimic_win
[eval exp="f.b1f_mimic=1"]
[nm t="ナレーション"]
宝箱が震えながら壁の隅へ這いずっていく。先へ進む。[p]
[fadeout time="800" color="0x000000"][wait time=300]
[jump storage="chap2_explore.ks" target="*hub_b1f"]