;=== chap2_massage.ks - マッサージ師 ===
*massage_start
[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]
[fadein time="800"]
[nm t="ナレーション"]
4階の一室。香油の香りが漂う。マッサージ台が置かれ、女性が待っている。[p]
[nm t="マッサージ師"]
「あら、お疲れでしょう？全身ほぐしてあげますよ♪」[p]
*massage_c1_prompt
どうする？[r]
[link target="*massage_c1_safe"]マッサージを断る[endlink][r]
[link target="*massage_c1_wrong"]少しだけなら、と台に横になる[endlink][r]
[s]
*massage_c1_safe
[nm t="ナレーション"]
断った。マッサージ師が残念そうな顔をした。[p]
[jump target="*massage_c2_prompt"]
*massage_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
横になった途端、腰と手首が柔らかく固定された。[p]
[nm t="マッサージ師"]
「動かないでくださいね。これがベースポジションです♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*massage_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*massage_c2_prompt"]
*massage_c2_prompt
どうする？[r]
[link target="*massage_c2_safe"]固定を外そうとする[endlink][r]
[link target="*massage_c2_wrong"]固定が気持ちよくて抵抗できない[endlink][r]
[s]
*massage_c2_safe
[nm t="ナレーション"]
固定を外して起き上がった。[p]
[jump target="*massage_c3_prompt"]
*massage_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
固定の感触が心地よく、力が抜けていく。[p]
[nm t="マッサージ師"]
「そう、力を抜いて。それが正しいマッサージの受け方です♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*massage_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*massage_c3_prompt"]
*massage_c3_prompt
どうする？[r]
[link target="*massage_c3_safe"]香油の匂いが怪しいと気づく[endlink][r]
[link target="*massage_c3_wrong"]香油の心地よさに身を任せる[endlink][r]
[s]
*massage_c3_safe
[nm t="ナレーション"]
香油を避けた。マッサージ師が苦笑いした。[p]
[jump target="*massage_c4_prompt"]
*massage_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
香油が肌に染み込むと、全身の感度が上がった。[p]
[nm t="マッサージ師"]
「特製の香油ですの。効果が出てきましたね♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*massage_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*massage_c4_prompt"]
*massage_c4_prompt
どうする？[r]
[link target="*massage_c4_safe"]起き上がって逃げようとする[endlink][r]
[link target="*massage_c4_wrong"]指圧の気持ちよさに抗えない[endlink][r]
[s]
*massage_c4_safe
[nm t="ナレーション"]
素早く起き上がって台から降りた。[p]
[jump target="*massage_c5_prompt"]
*massage_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
指圧の快感で身体が動かない。[p]
[nm t="マッサージ師"]
「もう少しですよ。ほら、もっと気持ちよくなりますから♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*massage_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*massage_c5_prompt"]
*massage_c5_prompt
どうする？[r]
[link target="*massage_c5_safe"]加護の力で感覚を遮断する[endlink][r]
[link target="*massage_c5_wrong"]完全に脱力してしまう[endlink][r]
[s]
*massage_c5_safe
[nm t="ナレーション"]
加護で感覚を遮断し、正気を保った。[p]
[jump target="*massage_win"]
*massage_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
全身の力が完全に抜け、身動きできなくなった。[p]
[nm t="マッサージ師"]
「完全にリラックスできましたね♪ では——仕上げです」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*massage_h_dispatch"][endif]
[jump target="*massage_h_dispatch"]
*massage_h_dispatch
[if exp="f.enemy_last_mistake==1"][jump target="*massage_h1"][endif]
[if exp="f.enemy_last_mistake==2"][jump target="*massage_h2"][endif]
[if exp="f.enemy_last_mistake==3"][jump target="*massage_h3"][endif]
[if exp="f.enemy_last_mistake==4"][jump target="*massage_h4"][endif]
[jump target="*massage_h5"]
*massage_h1
[eval exp="f.scene_massage_h1=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="massage_h1_01"]              ← CG①（最初）
[nm t="ナレーション"]
台に横になった途端、腰と手首が「固定用クッション」で柔らかく押さえられた。逃げられない、というより——逃げようという考えが浮かばないくらい心地よかった。[p]
; [cg f="massage_h1_02"]              ← CG②
[nm t="マッサージ師" color="#ffddaa"]
「では始めますね♪ 首から肩、背中、腰の順番で……。あ、ここ凝ってますね。ほぐします」[l]
[nm t="ナレーション"]
最初は本当に、ただのマッサージだった。筋肉の緊張が解けていく感覚。力が抜けていく感覚。それが「気持ちよさ」として蓄積され始めた頃、マッサージ師の手が少しだけ、普通とは違う方向へ動いた。[l]
「コリがほぐれると、ここも解放されますよ♪」穏やかな声で言いながら、その手は淫紋の位置に辿り着いた。コリをほぐすように、丁寧に、繰り返し。台に固定された身体で、全てが搾り取られていった。[p]
; [cg f="massage_h1_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてマッサージ師は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_4f"]
*massage_h2
[eval exp="f.scene_massage_h2=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="massage_h2_01"]              ← CG①（最初）
[nm t="ナレーション"]
温かい液体が背中に垂らされた。香油——そう言われたが、皮膚に染み込んだ瞬間、全身の温度が一段上がった。「特製ブレンドですの。血行を促進します♪」[p]
; [cg f="massage_h2_02"]              ← CG②
[nm t="マッサージ師" color="#ffddaa"]
「あら、もう効いてきましたね。……こちらの香油、淫紋との相性がいいんです。感度が上がるみたいで——お客様の反応を見ると、いつも確信します♪」[l]
[nm t="ナレーション"]
香油が全身に塗り広げられた。その手が経路を辿るたびに、全ての皮膚が過敏になっていく。通常のマッサージでは何も感じないはずの場所が、燃えるように反応し始めた。[l]
「感度が上がると施術の効果も高まりますよ♪」マッサージ師は笑顔で言いながら、その「効果」を最大限に活用した。香油の熱と淫紋の熱が重なり、マッサージ師の手の動きに全身が応えていった。[p]
; [cg f="massage_h2_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてマッサージ師は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_4f"]
*massage_h3
[eval exp="f.scene_massage_h3=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="massage_h3_01"]              ← CG①（最初）
[nm t="ナレーション"]
「坐骨神経のツボを押しますね」マッサージ師が言い、親指で一点を押した。通常ならただの圧迫感のはずが——淫紋に接続されたように、下腹部に電気が走った。[p]
; [cg f="massage_h3_02"]              ← CG②
[nm t="マッサージ師" color="#ffddaa"]
「あ、反応しましたね♪ ここが第三の快感点です。……お客様には初めて教えますけど、実はこのツボ、淫紋と繋がってるんですよ」[l]
[nm t="ナレーション"]
「第三の快感点」という言葉の意味を、身体が先に理解した。マッサージ師が教えながら別のツボも押し始めた。「こちらは第五の、こちらは第七の」——という説明が続く中で、それぞれの場所が淫紋へ信号を送っていく。[l]
「これは医学的に証明されているんですよ♪」明るい声で言いながら、マッサージ師は確実に全てのツボを使い切った。最後のツボが押された瞬間、全身の快感点が同時に鳴り響いた。[p]
; [cg f="massage_h3_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてマッサージ師は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_4f"]
*massage_h4
[eval exp="f.scene_massage_h4=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="massage_h4_01"]              ← CG①（最初）
[nm t="ナレーション"]
施術が進むにつれて、身体の力が完全に抜けていた。抵抗したくても、筋肉が言うことを聞かない。マッサージ師の「筋肉をほぐす」技術は、本当に全ての緊張を解いていた。[p]
; [cg f="massage_h4_02"]              ← CG②
[nm t="マッサージ師" color="#ffddaa"]
「あら、すっかりリラックスできましたね♪ これが正しい状態です。では、ここからが本施術になりますよ」[l]
[nm t="ナレーション"]
「本施術」の意味が、直後にわかった。力が抜けて動けない状態こそが、マッサージ師にとって「準備完了」のサインだった。[l]
抵抗できない身体の全てを使い、マッサージ師は「本施術」を行った。プロの技術は、相手が力を失った時にこそ真価を発揮する。「リラックスしたまま委ねてください♪ それが一番効率的です」その言葉に従うしか選択肢がなかった。[p]
; [cg f="massage_h4_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてマッサージ師は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_4f"]
*massage_h5
[eval exp="f.scene_massage_h5=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="massage_h5_01"]              ← CG①（最初）
[nm t="ナレーション"]
「仕上げです♪」マッサージ師が言った。その言葉がクライマックスの宣言だと、すでに理解していた。「仕上げ」に何が行われるかも。[p]
; [cg f="massage_h5_02"]              ← CG②
[nm t="マッサージ師" color="#ffddaa"]
「完全にリラックスできた状態で行う仕上げは、特別な効果があるんです。……淫紋の方には特に。回収量が通常の倍になることもありますよ♪」[l]
[nm t="ナレーション"]
倍。その数字が頭の中で響いた。マッサージ師は言葉通りに「完全にリラックスした状態」を最大限に活用した。動けない、抵抗できない、声を上げる力も残っていない——その全てを使って、最後の一滴まで丁寧に。[l]
「また大変お疲れでしたね。またどうぞ♪」と最後に笑顔で言ったが、帰る力はなかった。しばらく台の上で横たわったまま、マッサージ師が後片付けをする音だけを聞いていた。[p]
; [cg f="massage_h5_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてマッサージ師は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_4f"]
*massage_win
[eval exp="f.f4_massage=1"]
[nm t="ナレーション"]
マッサージ師が満足そうに頷いた。「では、お気をつけて♪」先へ進む。[p]
[fadeout time="800" color="0x000000"][wait time=300]
[jump storage="chap2_explore.ks" target="*hub_4f"]