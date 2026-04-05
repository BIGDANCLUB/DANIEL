;=== chap2_thief.ks - 女盗賊 ===
*thief_start
[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]
[fadein time="800"]
[nm t="ナレーション"]
1階中央廊下。人影が横切った——素早い動きだ。[p]
[nm t="ナレーション"]
気づけば腰の財布が消えていた。振り返ると、壁際に若い女盗賊が立っている。[p]
[nm t="女盗賊"]
「あら、気づいてたの？勇者サマは鋭いわね。でも……遅かったわ」[p]
*thief_c1_prompt
どうする？[r]
[link target="*thief_c1_safe"]財布を返すよう毅然と要求する[endlink][r]
[link target="*thief_c1_wrong"]財布を返してもらおうと近づく[endlink][r]
[s]
*thief_c1_safe
[nm t="ナレーション"]
堂々と要求すると、盗賊が苦笑いした。交渉の余地がありそうだ。[p]
[jump target="*thief_c2_prompt"]
*thief_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
近づいた途端、足元のワイヤートラップが作動した。[p]
[nm t="女盗賊"]
「罠にかかった。甘いわ、勇者サマ♪」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*thief_h_dispatch"]
[endif]
[nm t="ナレーション"]
かろうじて脱する。しかし状況は悪化している。[p]
[jump target="*thief_c2_prompt"]
*thief_c2_prompt
どうする？[r]
[link target="*thief_c2_safe"]周囲の罠を加護の光で探知する[endlink][r]
[link target="*thief_c2_wrong"]追いかけて路地に入る[endlink][r]
[s]
*thief_c2_safe
[nm t="ナレーション"]
光で罠の位置を把握。盗賊の動きが読めてきた。[p]
[jump target="*thief_c3_prompt"]
*thief_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
路地の奥は行き止まり——と思ったら天井から盗賊が降ってきた。[p]
[nm t="女盗賊"]
「上も見なきゃダメよ？基本でしょ♪」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*thief_h_dispatch"]
[endif]
[nm t="ナレーション"]
かろうじて脱する。しかし状況は悪化している。[p]
[jump target="*thief_c3_prompt"]
*thief_c3_prompt
どうする？[r]
[link target="*thief_c3_safe"]盗賊の動きを読んで先回りする[endlink][r]
[link target="*thief_c3_wrong"]盗賊の挑発に乗って正面から向かう[endlink][r]
[s]
*thief_c3_safe
[nm t="ナレーション"]
先読みして通路を塞ぐ。盗賊が舌打ちした。[p]
[jump target="*thief_c4_prompt"]
*thief_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
正面から向かった瞬間、煙幕が焚かれ視界を失った。[p]
[nm t="女盗賊"]
「正直者ね。でもそれじゃ盗賊には勝てないわ」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*thief_h_dispatch"]
[endif]
[nm t="ナレーション"]
かろうじて脱する。しかし状況は悪化している。[p]
[jump target="*thief_c4_prompt"]
*thief_c4_prompt
どうする？[r]
[link target="*thief_c4_safe"]煙の中で気配に集中する[endlink][r]
[link target="*thief_c4_wrong"]煙の中で手探りで進む[endlink][r]
[s]
*thief_c4_safe
[nm t="ナレーション"]
気配を感じて振り払う。盗賊が驚いた顔をした。[p]
[jump target="*thief_c5_prompt"]
*thief_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
手探りしていたら、後ろから羽交い締めにされた。[p]
[nm t="女盗賊"]
「背後よ。盗賊の基本よ？♪」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*thief_h_dispatch"]
[endif]
[nm t="ナレーション"]
かろうじて脱する。しかし状況は悪化している。[p]
[jump target="*thief_c5_prompt"]
*thief_c5_prompt
どうする？[r]
[link target="*thief_c5_safe"]加護の力で一気に突破する[endlink][r]
[link target="*thief_c5_wrong"]疲弊した状態で向かっていく[endlink][r]
[s]
*thief_c5_safe
[nm t="ナレーション"]
加護の光で煙を吹き飛ばし、盗賊を追い詰めた。[p]
[jump target="*thief_win"]
*thief_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
力尽きて膝をついた瞬間、盗賊が覆いかぶさってきた。[p]
[nm t="女盗賊"]
「あら、もう動けないの？じゃあ……いただくわ♪」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*thief_h_dispatch"]
[endif]
[jump target="*thief_h_dispatch"]
*thief_h_dispatch
[if exp="f.enemy_last_mistake==1"][jump target="*thief_h1"][endif]
[if exp="f.enemy_last_mistake==2"][jump target="*thief_h2"][endif]
[if exp="f.enemy_last_mistake==3"][jump target="*thief_h3"][endif]
[if exp="f.enemy_last_mistake==4"][jump target="*thief_h4"][endif]
[jump target="*thief_h5"]
*thief_h1
[eval exp="f.scene_thief_h1=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="thief_h1_01"]              ← 最初のCG
[nm t="ナレーション"]
煙の中、盗賊に押し倒された。身軽な手が素早く動き、あっという間に拘束される。「勇者の精液って高く売れるって聞いたけど……自分でもらうことにしたわ」そう言いながら、慣れた手つきで勇者を翻弄してくる。[p]
; [cg f="thief_h1_02"]              ← 中盤CG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて女盗賊は離れていった。[p]
; [cg f="thief_h1_03"]              ← クライマックスCG
[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_1f"]
*thief_h2
[eval exp="f.scene_thief_h2=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="thief_h2_01"]              ← 最初のCG
[nm t="ナレーション"]
羽交い締めにされたまま壁に押しつけられた。盗賊の身体が背中から密着し、器用な指が前から動き始める。「大人しくしてれば、痛くしないわよ♪」[p]
; [cg f="thief_h2_02"]              ← 中盤CG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて女盗賊は離れていった。[p]
; [cg f="thief_h2_03"]              ← クライマックスCG
[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_1f"]
*thief_h3
[eval exp="f.scene_thief_h3=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="thief_h3_01"]              ← 最初のCG
[nm t="ナレーション"]
煙の中で感覚が鋭くなっている。盗賊の手の動きがやけにはっきり伝わってくる。見えない分だけ、触覚が増幅される。「暗闇は盗賊のお庭よ。逆らわない方がいいわ」[p]
; [cg f="thief_h3_02"]              ← 中盤CG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて女盗賊は離れていった。[p]
; [cg f="thief_h3_03"]              ← クライマックスCG
[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_1f"]
*thief_h4
[eval exp="f.scene_thief_h4=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="thief_h4_01"]              ← 最初のCG
[nm t="ナレーション"]
罠に絡まったまま、盗賊に翻弄された。身動きできない状態で、盗賊はじっくり時間をかけて「いただいて」いく。[p]
; [cg f="thief_h4_02"]              ← 中盤CG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて女盗賊は離れていった。[p]
; [cg f="thief_h4_03"]              ← クライマックスCG
[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_1f"]
*thief_h5
[eval exp="f.scene_thief_h5=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="thief_h5_01"]              ← 最初のCG
[nm t="ナレーション"]
押し倒されたまま、盗賊は勇者の全てを奪っていった。「やっぱり勇者サマは上物ね」満足そうに笑いながら、颯爽と去っていった。[p]
; [cg f="thief_h5_02"]              ← 中盤CG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて女盗賊は離れていった。[p]
; [cg f="thief_h5_03"]              ← クライマックスCG
[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_1f"]
*thief_win
[eval exp="f.f1_thief=1"]
[nm t="ナレーション"]
盗賊が舌打ちして逃げていった。財布を回収し、先へ進む。[p]
[fadeout time="800" color="0x000000"]
[wait time=300]
[jump storage="chap2_explore.ks" target="*hub_1f"]