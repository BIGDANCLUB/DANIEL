;=== chap2_alraune.ks - アルラウネ ===
*alraune_start
[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]
[fadein time="800"]
[nm t="ナレーション"]
3階研究棟。植物の香りが強くなってきた。廊下の中央に巨大な花が咲いている。[p]
[nm t="ナレーション"]
その花の中心から、上半身だけの女性が顔を出した——アルラウネ。[p]
[nm t="アルラウネ"]
「……客人。花の蜜はいかが？とても……甘いわよ」[p]
*alraune_c1_prompt
どうする？[r]
[link target="*alraune_c1_safe"]花粉を吸わないよう息を止めて通り抜ける[endlink][r]
[link target="*alraune_c1_wrong"]花の美しさに引き寄せられて近づく[endlink][r]
[s]
*alraune_c1_safe
[nm t="ナレーション"]
息を止めて素早く通り抜けた。花粉の影響を受けずに済んだ。[p]
[jump target="*alraune_c2_prompt"]
*alraune_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
近づいた瞬間、大量の花粉が噴き出した。[p]
[nm t="アルラウネ"]
「……来てくれた。もう、動けないでしょう？」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*alraune_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*alraune_c2_prompt"]
*alraune_c2_prompt
どうする？[r]
[link target="*alraune_c2_safe"]加護の光で花粉を払う[endlink][r]
[link target="*alraune_c2_wrong"]花の蜜の甘い香りに誘われる[endlink][r]
[s]
*alraune_c2_safe
[nm t="ナレーション"]
光が花粉を焼き払った。アルラウネが悲鳴を上げた。[p]
[jump target="*alraune_c3_prompt"]
*alraune_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
甘い香りに引き寄せられ、気づけば花弁の中に半分入っていた。[p]
[nm t="アルラウネ"]
「……香り、気に入ってくれた？もっと、深く来て」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*alraune_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*alraune_c3_prompt"]
*alraune_c3_prompt
どうする？[r]
[link target="*alraune_c3_safe"]蔓の動きに注意しながら迂回する[endlink][r]
[link target="*alraune_c3_wrong"]アルラウネと会話しようとする[endlink][r]
[s]
*alraune_c3_safe
[nm t="ナレーション"]
蔓を避けながら迂回路を見つけた。[p]
[jump target="*alraune_c4_prompt"]
*alraune_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
会話中に蔓が足首を捕らえていた。[p]
[nm t="アルラウネ"]
「……お話、ありがとう。でも逃さないわ」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*alraune_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*alraune_c4_prompt"]
*alraune_c4_prompt
どうする？[r]
[link target="*alraune_c4_safe"]強引に蔓を切り払って進む[endlink][r]
[link target="*alraune_c4_wrong"]蔓の引力に抵抗できない[endlink][r]
[s]
*alraune_c4_safe
[nm t="ナレーション"]
剣で蔓を次々と切り払い、道を作った。[p]
[jump target="*alraune_c5_prompt"]
*alraune_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
蔓の力が強すぎて、引き寄せられてしまった。[p]
[nm t="アルラウネ"]
「……植物の力は侮れないでしょう？」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*alraune_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*alraune_c5_prompt"]
*alraune_c5_prompt
どうする？[r]
[link target="*alraune_c5_safe"]加護の力で一気に突破する[endlink][r]
[link target="*alraune_c5_wrong"]花粉で感覚が麻痺してきた[endlink][r]
[s]
*alraune_c5_safe
[nm t="ナレーション"]
加護の力で花粉と蔓を同時に押しのけた。[p]
[jump target="*alraune_win"]
*alraune_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
感覚が麻痺し、動けなくなったところを捕まった。[p]
[nm t="アルラウネ"]
「……もう動けない。花の中で、ゆっくり休んでいって」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*alraune_h_dispatch"][endif]
[jump target="*alraune_h_dispatch"]
*alraune_h_dispatch
[if exp="f.enemy_last_mistake==1"][jump target="*alraune_h1"][endif]
[if exp="f.enemy_last_mistake==2"][jump target="*alraune_h2"][endif]
[if exp="f.enemy_last_mistake==3"][jump target="*alraune_h3"][endif]
[if exp="f.enemy_last_mistake==4"][jump target="*alraune_h4"][endif]
[jump target="*alraune_h5"]
*alraune_h1
[eval exp="f.scene_alraune_h1=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="alraune_h1_01"]              ← 最初のCG
[nm t="ナレーション"]
蔓に引かれるまま、気づけば花弁の内側にいた。外の世界が閉ざされていく。花びらが一枚、また一枚と重なって、ほのかな光だけが残る。温かい。甘い香りが充満していて、深呼吸するたびに頭が少しずつ霞んでくる。[p]
; [cg f="alraune_h1_02"]              ← 中盤CG
[nm t="アルラウネ" color="#88cc66"]
「……来てくれた。嬉しい。……この花の中、気持ちよくない？　ここにいる間は、ゆっくりできるから。……美味しそう。ゆっくり、いただくわ」[l]
[nm t="ナレーション"]
蔓が足首から腰へと這い上がる。締め付けるのではなく、撫でるように。花びらの内壁からは甘い蜜が滲み出していて、それが肌に触れるたびに温かく溶けていくような感覚がある。抵抗しようとした手が、気づけば蔓に優しく絡め取られていた。[l]
「……ゆっくり。急がなくていい。花の時間は、ゆっくり流れるから」アルラウネの声は花弁越しに響いて、それ自体が眠り薬のようだった。[p]
; [cg f="alraune_h1_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて花弁がゆっくりと開き、アルラウネは蔓を引き戻した。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*alraune_h2
[eval exp="f.scene_alraune_h2=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="alraune_h2_01"]              ← 最初のCG
[nm t="ナレーション"]
花粉だ——と気づいた時には既に吸い込んだ後だった。全身の感覚が一段階鋭くなる。空気が肌に触れるだけで分かる。蔓が足首を包んだ感触が、通常の何倍も鮮明に届く。アルラウネが静かに近づいてきた。その目が、わずかに輝いていた。[p]
; [cg f="alraune_h2_02"]              ← 中盤CG
[nm t="アルラウネ" color="#88cc66"]
「……花粉、吸ったのね。……今は、全部が気持ちよく感じるでしょう。わたしの花粉は、そういうもの。……ちゃんと分かってる。どこを、どうすれば——」[l]
[nm t="ナレーション"]
言葉が終わる前に蔓が動いた。軽い接触だった。それだけなのに、全身に電流に似た何かが走り抜ける。淫紋と花粉の効果が重なって、感覚が際限なく増幅されている。アルラウネは一度触れてから少し間を置き、反応を確認して、また触れる。[l]
丁寧すぎる。まるで花の世話をするような手つきで、アルラウネはレンのあらゆる反応を静かに引き出し続けた。[p]
; [cg f="alraune_h2_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてアルラウネは蔓を解き、静かに離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*alraune_h3
[eval exp="f.scene_alraune_h3=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="alraune_h3_01"]              ← 最初のCG
[nm t="ナレーション"]
蔓が絡みついてきた。足首、膝、腰、腕——順番に、ひとつひとつ。痛くない。締め付けも強くない。ただ「逃げられない」という事実だけが積み重なっていく。甘い蜜の匂いが花から滲み出して、しだいに頭の中が甘く霞んでいった。[p]
; [cg f="alraune_h3_02"]              ← 中盤CG
[nm t="アルラウネ" color="#88cc66"]
「……逃げなくていい。逃げても、また蔓が引き戻すから。……それより、ここにいて。わたしと一緒に、ゆっくり。蜜をあげる。全部、気持ちよくしてあげるから」[l]
[nm t="ナレーション"]
蔓の先端から蜜が滲み出した。それが淫紋に触れた瞬間、全身が甘い熱に包まれる。アルラウネは急がない。花の世界には別の時間が流れている。蔓はゆっくりと動き、蜜はゆっくりと広がり、感覚はじわじわと積み上がっていった。[l]
「……いい音がする。花にも、聞こえてる」アルラウネが呟いた。その頃にはレンは蔓に全体重を預けることしかできなくなっていた。[p]
; [cg f="alraune_h3_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて蔓がゆっくりとほどけ、アルラウネは静かに離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*alraune_h4
[eval exp="f.scene_alraune_h4=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="alraune_h4_01"]              ← 最初のCG
[nm t="ナレーション"]
花弁が四方から迫って、やがて外の光を完全に閉ざした。蕾の内側——アルラウネと二人きりの、甘い密閉空間。根の網目が床に広がっていて、足の裏から微弱な振動が伝わってくる。この花全体がアルラウネの体の一部なのだと、その瞬間に理解した。[p]
; [cg f="alraune_h4_02"]              ← 中盤CG
[nm t="アルラウネ" color="#88cc66"]
「ここは、わたしの中。……外からは見えない。声も聞こえない。あなただけを、感じられる場所。……好き。ここが一番、あなたのにおいがする」[l]
[nm t="ナレーション"]
根から蜜が染み出してくる。蔓が動く。花弁の内壁が呼吸するように膨らんだり縮んだりする。アルラウネの体そのものに包まれているという感覚が、ひとつひとつの接触を倍増させる。[l]
外の世界が遠い。時間も遠い。この花の中にだけ、甘くて逃げ場のない今があった。アルラウネは囁き続けた——「もっと、聞かせて。あなたの声、わたしの根まで届いてる」[p]
; [cg f="alraune_h4_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて花弁がゆっくりと開き、アルラウネはそっと離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*alraune_h5
[eval exp="f.scene_alraune_h5=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="alraune_h5_01"]              ← 最初のCG
[nm t="ナレーション"]
花の中に取り込まれた。蔓が全身に絡まり、花弁が周囲を包み、外の光が完全に遮断された。アルラウネの身体——この花全体がアルラウネそのもの——に完全に囲まれた状態で、根が床から這い上がってきた。[p]
; [cg f="alraune_h5_02"]              ← 中盤CG
[nm t="アルラウネ" color="#88cc66"]
「……根は、わたしの一番奥。……根がつながった相手は、特別。ゆっくり、じっくり、全部いただく」[l]
[nm t="ナレーション"]
根の感触は蔓より細く、温かく、至る所から同時に触れてくる。花全体が一つの生命体として脈動し、その脈動に合わせて蜜が分泌され、香りが濃くなり、全身の感覚が溶けていく。時間の流れが変わった——花の時間は、外の世界より遅い。[l]
どのくらい経っただろうか。アルラウネが静かに言った。「……全部、もらった。ありがとう」その声は花弁の向こうから聞こえた。やがて花が開き、ぐったりした身体が外へ戻された。花の中は、温かかった。[p]
; [cg f="alraune_h5_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてアルラウネは離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*alraune_win
[eval exp="f.f3_alraune=1"]
[nm t="ナレーション"]
アルラウネが花弁を閉じた。道が開いた。先へ進む。[p]
[fadeout time="800" color="0x000000"][wait time=300]
[jump storage="chap2_explore.ks" target="*hub_3f"]