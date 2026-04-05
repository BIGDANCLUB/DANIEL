;==========================================================
; chap2_tentacle.ks - B1F「触手植物魔物」
;==========================================================
*tentacle_start

[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]

[fadein time="800"]

[nm t="ナレーション"]
水路の奥深く、光の届かない暗がりに足を踏み入れた。壁面を覆う蔦のようなものが、かすかに脈動している。[p]

[nm t="ナレーション"]
その瞬間——壁の裂け目から、ぬるりと触手が伸びてきた。一本、二本、三本……数え切れないほど。[p]

[nm t="触手魔物"]
「……ずるずる……」[l]

[nm t="ナレーション"]
暗闇から低い振動音が響く。植物と獣の中間のような存在——触手系の魔物。光を嫌い、暗所に潜む捕食者だ。[p]

[nm t="触手魔物"]
「……においがする……やわらかい……」[p]

[nm t="ナレーション"]
触手が勇者のにおいを嗅ぐように空中を揺れている。本能だけで動く捕食者の動きを読め——！[p]

;==========================================================
; 選択肢1: 光源の確保
;==========================================================
*tentacle_c1_prompt

[nm t="ナレーション"]
暗闇が広がる通路。触手は光を嫌がるようだが、手持ちの松明は残り一本だ。どう使う？[p]

どうする？[r]
[link target="*tentacle_c1_safe"]松明を前方に掲げて進む[endlink][r]
[link target="*tentacle_c1_wrong"]松明を節約して暗闇の中を進む[endlink][r]
[s]

*tentacle_c1_safe
[nm t="ナレーション"]
松明を高く掲げると、触手が光を避けて壁際へ引き下がった。光の円の中を慎重に進む。触手は近づいてこない。[p]
[nm t="勇者" color="#aaddff"]
「（光が有効だ……火を絶やさないようにしなければ）」[p]
[jump target="*tentacle_c2_prompt"]

*tentacle_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
暗闇の中を忍び足で進む——その足首に、冷たく湿った感触が巻きついた。[p]
[nm t="触手魔物"]
「……つかまえた……ずるずる」[l]
[nm t="ナレーション"]
引き倒される寸前、松明に火をつけて床に叩きつけた。炎の光に触手が引き退く。辛うじて逃れたが、足首に粘液の感触が残っている。[p]
[if exp="f.enemy_mistakes>=2"]
[jump target="*tentacle_h_dispatch"]
[endif]
[nm t="ナレーション"]
震える手で松明を構え直す。暗闇の中で光を節約しようとした判断が命取りになるところだった。[p]
[jump target="*tentacle_c2_prompt"]

;==========================================================
; 選択肢2: 通路の選択
;==========================================================
*tentacle_c2_prompt

[nm t="ナレーション"]
分岐点に出た。左の通路は狭いが明かり窓がある。右は広いが真っ暗だ。触手の気配は両方から漂ってくる。[p]

どうする？[r]
[link target="*tentacle_c2_safe"]光のある左の通路を選ぶ[endlink][r]
[link target="*tentacle_c2_wrong"]広い右の通路を突き進む[endlink][r]
[s]

*tentacle_c2_safe
[nm t="ナレーション"]
狭い左の通路へ入ると、壁の小窓から外光が差し込んでいた。触手は光の中に入ってこない。体を横にしながら慎重に進む。[p]
[nm t="勇者" color="#aaddff"]
「狭いが……安全だ」[p]
[jump target="*tentacle_c3_prompt"]

*tentacle_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
広い通路に踏み込んだ途端、四方から触手が迫ってきた。暗闇に目が慣れないまま、腰に太い触手が巻きつく。[p]
[nm t="触手魔物"]
「……あたたかい……はなさない……」[l]
[nm t="ナレーション"]
剣を一閃——触手を切り離して転がった。切断された触手が床を這い回る中、壁沿いに走り抜ける。全身に粘液が付着した。[p]
[if exp="f.enemy_mistakes>=2"]
[jump target="*tentacle_h_dispatch"]
[endif]
[nm t="ナレーション"]
なんとか分岐点まで引き返し、改めて左の通路へ向かった。[p]
[jump target="*tentacle_c3_prompt"]

;==========================================================
; 選択肢3: 触手の特性を見極める
;==========================================================
*tentacle_c3_prompt

[nm t="ナレーション"]
前方に巨大な触手の巣のような空間が広がっている。無数の触手が天井から垂れ下がり、床を這い回っている。正面突破は無謀だ。[p]

どうする？[r]
[link target="*tentacle_c3_safe"]触手の動きを観察して隙間を探す[endlink][r]
[link target="*tentacle_c3_wrong"]剣を振りながら強引に突き進む[endlink][r]
[s]

*tentacle_c3_safe
[nm t="ナレーション"]
壁際に身を潜め、触手の動きのパターンを観察する。一定のリズムで波打っている——その間隔に合わせて走れば抜けられる。[p]
[nm t="勇者" color="#aaddff"]
「三、二、一——今だ！」[l]
[nm t="ナレーション"]
タイミングを計って一気に駆け抜けた。触手がわずかに服の裾を掠めたが、捕まらずに済んだ。[p]
[jump target="*tentacle_c4_prompt"]

*tentacle_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
剣を振りながら突進する——しかし切っても切っても触手は再生し、むしろ動きが激しくなる。腕に、肩に、胴体に、次々と巻きつかれた。[p]
[nm t="触手魔物"]
「……きもちいい……もっと……ずるずる」[l]
[nm t="ナレーション"]
全身の力を振り絞って叫ぶと、淫紋が一瞬強く輝いた。その光に触手が怯み、拘束が緩む。隙を突いて転がり出た。膝が笑っている。[p]
[if exp="f.enemy_mistakes>=2"]
[jump target="*tentacle_h_dispatch"]
[endif]
[nm t="ナレーション"]
粘液まみれになりながらも、なんとかその場を切り抜けた。剣で切るのは逆効果だと身をもって学んだ。[p]
[jump target="*tentacle_c4_prompt"]

;==========================================================
; 選択肢4: 粘液の罠
;==========================================================
*tentacle_c4_prompt

[nm t="ナレーション"]
床に粘液が広がっている区画に出た。一歩踏み出すと足が吸いつく感触。粘液の中を触手が泳いでいる。[p]

どうする？[r]
[link target="*tentacle_c4_safe"]壁の突起を足場に伝い歩きする[endlink][r]
[link target="*tentacle_c4_wrong"]粘液の上を素早く走り抜ける[endlink][r]
[s]

*tentacle_c4_safe
[nm t="ナレーション"]
壁面に突き出た岩の出っ張りを足場にして、粘液のある床を避けながら進む。ゆっくりだが確実だ。触手は床から来られない。[p]
[nm t="勇者" color="#aaddff"]
「……この方法なら触れずに済む」[p]
[jump target="*tentacle_c5_prompt"]

*tentacle_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
勢いよく踏み込んだ途端、粘液が足首を捉えて速度がゼロになった。床の粘液から触手がにゅるりと這い上がり、足を絡め取る。[p]
[nm t="触手魔物"]
「……にげられない……ずるずる……」[l]
[nm t="ナレーション"]
短剣で粘液を引き裂きながら強引に引き抜く。靴が脱げそうになったが、なんとか粘液地帯を脱した。足首に紫色の痕が残っている。[p]
[if exp="f.enemy_mistakes>=2"]
[jump target="*tentacle_h_dispatch"]
[endif]
[nm t="ナレーション"]
呼吸を整えながら壁伝いに進んだ。粘液の罠を軽く見た代償は大きかった。[p]
[jump target="*tentacle_c5_prompt"]

;==========================================================
; 選択肢5: 母体との対峙
;==========================================================
*tentacle_c5_prompt

[nm t="ナレーション"]
通路の終わりに、触手の根元——巨大な植物の塊が蠢いていた。これが触手魔物の本体だ。出口はその後ろにある。[p]

どうする？[r]
[link target="*tentacle_c5_safe"]本体の弱点である中心の発光点を狙って一撃で仕留める[endlink][r]
[link target="*tentacle_c5_wrong"]本体を無視して強引に出口へ走る[endlink][r]
[s]

*tentacle_c5_safe
[nm t="ナレーション"]
本体の中心でぼんやりと輝く核。剣に全力を込め——一直線に飛び込んだ。[p]
[nm t="触手魔物"]
「……！！……ずずず……」[l]
[nm t="ナレーション"]
剣が核に突き刺さった瞬間、全ての触手がぐったりと垂れ下がった。本体が収縮し、道が開く。[p]
[jump target="*tentacle_win"]

*tentacle_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
本体を迂回しようとした瞬間、無数の触手が一斉に伸びてきた。腕、脚、胴体——全て同時に捕縛される。[p]
[nm t="触手魔物"]
「……にがさない……たべる……」[p]
[nm t="ナレーション"]
触手に持ち上げられ、本体の前に引き据えられた。抵抗する間もなく、触手が全身に絡みつき始める。[p]
[jump target="*tentacle_h_dispatch"]

;==========================================================
; Hシーン振り分け
;==========================================================
*tentacle_h_dispatch
[if exp="f.enemy_last_mistake==1"]
[jump target="*tentacle_h1"]
[endif]
[if exp="f.enemy_last_mistake==2"]
[jump target="*tentacle_h2"]
[endif]
[if exp="f.enemy_last_mistake==3"]
[jump target="*tentacle_h3"]
[endif]
[if exp="f.enemy_last_mistake==4"]
[jump target="*tentacle_h4"]
[endif]
[jump target="*tentacle_h5"]

;==========================================================
; Hシーン① ～ ⑤
;==========================================================
*tentacle_h1
[eval exp="f.scene_tentacle_h1=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="tentacle_h1_01"]              ← 最初のCG
[nm t="ナレーション"]
暗闇の中、触手が全身にゆっくりと巻きついてくる。足首から這い上がり、膝、腿、腰へと順番に。冷たく湿った感触が肌に張り付く。そのぬめりが——不思議と熱を帯び始めた。[p]
; [cg f="tentacle_h1_02"]              ← 中盤CG
[nm t="ナレーション"]
「離せ……っ」と叫んでも、触手は止まらない。むしろ声に反応するように動きが増す。服の合わせ目から細い触手が入り込み、ゆっくりとはだかせていく。一本が耳元で揺れ、もう一本が首筋を撫でた。感覚が敏感になっていく。[p]
; [cg f="tentacle_h1_03"]              ← クライマックスCG
[nm t="ナレーション"]
股間に集中した触手が、リズムを刻み始めた。速くも遅くもない——焦らすような動き。じわじわと追い詰められ、やがて抗えなくなった。触手が全てを受け止めた。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
脱力した身体が床に下ろされた。触手は満足したように引いていく。[p]
[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

*tentacle_h2
[eval exp="f.scene_tentacle_h2=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="tentacle_h2_01"]              ← 最初のCG
[nm t="ナレーション"]
広い通路の中央で、触手に四肢を広げた形で固定された。壁に磔にされたかのように身動きが取れない。触手の先端が——まるで観察するように、全身を一センチずつ確認していく。[p]
; [cg f="tentacle_h2_02"]              ← 中盤CG
[nm t="ナレーション"]
特に敏感な部位を発見するたびに、触手の動きが変わった。集中的に、執拗に、同じ場所を繰り返し刺激する。理性で抵抗しようとするのに、身体は反応してしまう。粘液が潤滑剤となり、摩擦が消える。[p]
; [cg f="tentacle_h2_03"]              ← クライマックスCG
[nm t="ナレーション"]
二本の触手が同時に違う場所を攻め、思考が白くなった。深い暗闇の中で、意識が遠のく寸前まで追い詰められた。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
触手が離れると、全身が燃えるように熱かった。[p]
[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

*tentacle_h3
[eval exp="f.scene_tentacle_h3=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="tentacle_h3_01"]              ← 最初のCG
[nm t="ナレーション"]
触手の巣の奥、柔らかい蔦で作られたような空間に引き込まれた。まるで繭の中のようだ。壁全体が息をするように脈動している。[p]
; [cg f="tentacle_h3_02"]              ← 中盤CG
[nm t="ナレーション"]
細い触手が無数に、全身をくまなく這い回る。首から肩、背中から腰、内腿から足先まで——地図を描くように丁寧に。その感触が蓄積されて、全身が熱を帯びていく。服はいつの間にか完全に取り除かれていた。[p]
; [cg f="tentacle_h3_03"]              ← クライマックスCG
[nm t="ナレーション"]
繭の壁が締まるように圧力をかけながら、触手がクライマックスへ誘う。全身の皮膚が感覚器になったかのように、あらゆる刺激が増幅された。もはや抵抗する意志すら搾り取られていた。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
繭が開き、ぐったりした身体を外へ戻した。[p]
[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

*tentacle_h4
[eval exp="f.scene_tentacle_h4=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="tentacle_h4_01"]              ← 最初のCG
[nm t="ナレーション"]
粘液の池に引きずり込まれた。沈まない——粘液が全身を支えているが、全く動けない。浮かんだまま、触手が水面下から這い上がってくる。[p]
; [cg f="tentacle_h4_02"]              ← 中盤CG
[nm t="ナレーション"]
粘液の温度は体温と同じで、境界線がわからなくなってくる。どこが自分の肌でどこが粘液なのか——そんな思考が溶けていく中、触手が中心部に集中し始めた。粘液越しの刺激は、直接よりもじわりとした広がりがある。[p]
; [cg f="tentacle_h4_03"]              ← クライマックスCG
[nm t="ナレーション"]
全身を包んだまま、粘液ごと揺らされるような感覚。逃げる場所も抵抗する支点もない状態で、ゆっくりと限界を超えさせられた。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
粘液が固化し、やがてほどけて床に下ろされた。[p]
[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

*tentacle_h5
[eval exp="f.scene_tentacle_h5=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="tentacle_h5_01"]              ← 最初のCG
[nm t="ナレーション"]
本体の前に引き据えられた。触手の根源——巨大な植物核が目の前で脈動している。核から直接伸びる太い触手が、ゆっくりと服を剥ぎ取った。[p]
; [cg f="tentacle_h5_02"]              ← 中盤CG
[nm t="ナレーション"]
これが本体の行為だ、と本能で理解した。支配的で、確実で、逃げ場がない。触手が全身を包み込み、核の温度が直接伝わってくる——生き物の体温より高く、熱い。[p]
; [cg f="tentacle_h5_03"]              ← クライマックスCG
[nm t="ナレーション"]
核と繋がった触手が精力の全てを引き出すように動く。抵抗は無意味で、もはや快楽に溺れるしかない。全てを搾り取られた後、触手がゆっくりと離れた。核がかすかに輝いた——満足の表現なのかもしれない。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
本体の前に放り出された。全身が脱力している。[p]
[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

;==========================================================
; 勝利
;==========================================================
*tentacle_win
[eval exp="f.b1f_tentacle=1"]
[nm t="ナレーション"]
触手魔物の核が砕け、全ての触手が力なく床に崩れ落ちた。暗がりに静寂が戻る。[p]
[nm t="ナレーション"]
剣を引き抜きながら息を整える。植物知性は侮れない相手だったが——光と急所を見極めれば対処できる。この経験は次に活きるだろう。[p]
[nm t="勇者" color="#aaddff"]
「……触手は光で退けられる。覚えておこう」[p]
[fadeout time="800" color="0x000000"]
[wait time=300]
[jump storage="chap2_explore.ks" target="*hub_b1f"]
