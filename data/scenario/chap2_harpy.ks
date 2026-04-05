;=== chap2_harpy.ks - ハーピー ===
*harpy_start
[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]
[fadein time="800"]
[nm t="ナレーション"]
2階の吹き抜け。羽音が聞こえたと思ったら、天井から急降下してきた。[p]
[nm t="ナレーション"]
ハーピー——鳥の翼と脚を持つ女性型魔物。[p]
[nm t="ハーピー"]
「きゃあっ！えさ、えさ！勇者のにおい！」[p]
*harpy_c1_prompt
どうする？[r]
[link target="*harpy_c1_safe"]盾で急降下を防ぐ[endlink][r]
[link target="*harpy_c1_wrong"]急降下を避けようとして転ぶ[endlink][r]
[s]
*harpy_c1_safe
[nm t="ナレーション"]
盾で急降下を受け止めた。衝撃は大きいが体勢を保てた。[p]
[jump target="*harpy_c2_prompt"]
*harpy_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
避けようとして転倒。ハーピーが上から覆いかぶさってきた。[p]
[nm t="ハーピー"]
「つかまえた！えさ！えさ！」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*harpy_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*harpy_c2_prompt"]
*harpy_c2_prompt
どうする？[r]
[link target="*harpy_c2_safe"]翼の動きを読んで次の攻撃に備える[endlink][r]
[link target="*harpy_c2_wrong"]ハーピーの羽毛に触れてしまう[endlink][r]
[s]
*harpy_c2_safe
[nm t="ナレーション"]
翼の動きを読んで回避できた。[p]
[jump target="*harpy_c3_prompt"]
*harpy_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
羽毛に触れた瞬間、くすぐったい感触と共に絡め取られた。[p]
[nm t="ハーピー"]
「ふわふわ、気持ちいい？わたしもきもちいい！」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*harpy_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*harpy_c3_prompt"]
*harpy_c3_prompt
どうする？[r]
[link target="*harpy_c3_safe"]加護の光でハーピーを牽制する[endlink][r]
[link target="*harpy_c3_wrong"]ハーピーの歌に聞き惚れる[endlink][r]
[s]
*harpy_c3_safe
[nm t="ナレーション"]
光でハーピーが怯んだ。高い場所への移動を諦めた。[p]
[jump target="*harpy_c4_prompt"]
*harpy_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
ハーピーの鳴き声が不思議と心地よく、足が止まってしまった。[p]
[nm t="ハーピー"]
「すきでしょ？わたしのうた。もっときかせてあげる！」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*harpy_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*harpy_c4_prompt"]
*harpy_c4_prompt
どうする？[r]
[link target="*harpy_c4_safe"]巣への誘導を断固として断る[endlink][r]
[link target="*harpy_c4_wrong"]ハーピーの誘導に従って進む[endlink][r]
[s]
*harpy_c4_safe
[nm t="ナレーション"]
強い意志で誘導を断った。ハーピーが困った顔をした。[p]
[jump target="*harpy_c5_prompt"]
*harpy_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
ハーピーに連れられて行くと、巣の中に引き込まれていた。[p]
[nm t="ハーピー"]
「巣についた！ここがおうち！」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*harpy_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*harpy_c5_prompt"]
*harpy_c5_prompt
どうする？[r]
[link target="*harpy_c5_safe"]一気に走り抜ける[endlink][r]
[link target="*harpy_c5_wrong"]疲弊して動けない[endlink][r]
[s]
*harpy_c5_safe
[nm t="ナレーション"]
全速力で走り抜け、ハーピーの届かない場所へ出た。[p]
[jump target="*harpy_win"]
*harpy_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
力が尽きて立ち止まった瞬間、ハーピーに捕まった。[p]
[nm t="ハーピー"]
「もうにげられない！えさ！えさ！」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*harpy_h_dispatch"][endif]
[jump target="*harpy_h_dispatch"]
*harpy_h_dispatch
[if exp="f.enemy_last_mistake==1"][jump target="*harpy_h1"][endif]
[if exp="f.enemy_last_mistake==2"][jump target="*harpy_h2"][endif]
[if exp="f.enemy_last_mistake==3"][jump target="*harpy_h3"][endif]
[if exp="f.enemy_last_mistake==4"][jump target="*harpy_h4"][endif]
[jump target="*harpy_h5"]
*harpy_h1
[eval exp="f.scene_harpy_h1=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="harpy_h1_01"]              ← 最初のCG
[nm t="ナレーション"]
翼が風を切り、次の瞬間には全身を羽毛に包まれていた。ハーピーの羽根は想像以上に柔らかく温かい。鳥の獣臭と甘い羽毛の匂いが混ざって、奇妙に落ち着く。しかしそれは罠だった——翼の内側で絡みつくように羽根が動き、全身の皮膚を同時に撫で回してくる。[p]
; [cg f="harpy_h1_02"]              ← 中盤CG
[nm t="ハーピー" color="#88ddaa"]
「いいにおい！えさのにおいがする！ここ、ここ！においが一番強い！」[l]
[nm t="ナレーション"]
淫紋の匂いに引き寄せられるように、ハーピーの顔が股間に近づいた。獣としての本能だけで動いている。知性ではなく、食欲と本能で。それなのに——その正直すぎる動きが、計算のある者よりもずっと的確にレンの弱点を突いてくる。[l]
「えさ！えさでてきた！」ハーピーが興奮した声で叫ぶたびに、翼の締め付けが強くなった。[p]
; [cg f="harpy_h1_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてハーピーは満足したように羽根を緩め、離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_2f"]
*harpy_h2
[eval exp="f.scene_harpy_h2=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="harpy_h2_01"]              ← 最初のCG
[nm t="ナレーション"]
気づけば巣の中にいた。ハーピーに運ばれたのか、いつの間にか高い岩棚の上の、羽毛で敷き詰められた巣の中に横たわっている。外の景色が遠く、降りる方法も見当たらない。ハーピーが興奮した目で見下ろしていた。[p]
; [cg f="harpy_h2_02"]              ← 中盤CG
[nm t="ハーピー" color="#88ddaa"]
「わたしの巣！わたしのえさ！ここにいれば、いつでもたべられる！いい！すごくいい！」[l]
[nm t="ナレーション"]
のしかかってくる体は意外に軽い。しかし爪は鋭く、羽根は力強く、逃げようとするたびに翼でぐいと押さえ込まれる。ハーピーは理屈を知らない——ただ本能で、温かいものに、良い匂いのするものに、引き寄せられて絡みつく。[l]
羽毛の感触と、獣の体温と、本能だけで突き動かされる動きが交互に押し寄せてきた。「えさ、えさ！」繰り返されるその言葉が、巣の外まで響いていた。[p]
; [cg f="harpy_h2_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてハーピーはご機嫌で鳴きながら離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_2f"]
*harpy_h3
[eval exp="f.scene_harpy_h3=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="harpy_h3_01"]              ← 最初のCG
[nm t="ナレーション"]
ハーピーが鳴き始めた。歌ではなく、鳴き声——でも耳の奥に染み込んでくるその高い声は、不思議と体の力を奪う。全身から余計な緊張が抜けていって、羽毛の感触がさっきより何倍も柔らかく感じられた。[p]
; [cg f="harpy_h3_02"]              ← 中盤CG
[nm t="ハーピー" color="#88ddaa"]
「なかないで。ここは巣。安全。……においがよくなる。なくと、においがもっとよくなる！」[l]
[nm t="ナレーション"]
声に反応して淫紋が熱を持った。ハーピーはそれを感じ取ったのか、より熱心に鳴き続けながら、鋭い爪とは裏腹に驚くほど優しく羽毛でレンの全身を包んでいく。抵抗の意思が溶けていく。声と羽根と温度に、じわじわと侵食されていく。[l]
「でた！においでた！」ハーピーが嬉しそうに声を上げた時、レンはもう体を起こす力が残っていなかった。[p]
; [cg f="harpy_h3_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてハーピーは鳴きやみ、満足そうに離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_2f"]
*harpy_h4
[eval exp="f.scene_harpy_h4=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="harpy_h4_01"]              ← 最初のCG
[nm t="ナレーション"]
足が地面を離れた。ハーピーの翼が力強く羽ばたき、二人一緒に宙へ舞い上がる。高度が上がるにつれて風が強くなり、レンはハーピーにしがみつくしかなかった——しがみつくことが、ハーピーの望む密着そのものだと気づいた時には、もう遅かった。[p]
; [cg f="harpy_h4_02"]              ← 中盤CG
[nm t="ハーピー" color="#88ddaa"]
「たかいところ！すきなところ！ここでするのがいちばん！においがとおくまでとんでいく！」[l]
[nm t="ナレーション"]
落ちたくない、という本能が体を強ばらせる。その恐怖と、翼に押さえ込まれる圧迫感と、風の中でハーピーの体温だけが異常に温かい感覚が混ざり合う。高所という逃げ場のなさが、全ての抵抗を無意味にした。[l]
ハーピーは空中で器用に動き、レンに絡みついたまま目的を果たしていった。「でた！たかいところでもでた！」その声が風に乗って散っていった。[p]
; [cg f="harpy_h4_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてハーピーはゆっくり降下し、地面に戻ってから離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_2f"]
*harpy_h5
[eval exp="f.scene_harpy_h5=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="harpy_h5_01"]              ← 最初のCG
[nm t="ナレーション"]
今日のハーピーは違った。いつもの衝動的な動きではなく——まるで学習したかのように、どこを触れば一番反応するかを知っている。羽毛で肌を撫でながら、爪の側面でそっと淫紋をなぞる。「においがいちばんつよいばしょ」と低く呟いて、そこに集中し始めた。[p]
; [cg f="harpy_h5_02"]              ← 中盤CG
[nm t="ハーピー" color="#88ddaa"]
「まえより、わかってきた。ここ、ここがいい。こうすると——においがもっと強くなる」[l]
[nm t="ナレーション"]
本能が経験と結びついた時、ハーピーは最も手強くなる。知性はなくても、成功体験は積み上がる。どの動きが最も反応を引き出すか、ハーピーの鳥のような目は正確に観察していた。[l]
「でた！においでた！ぜんぶでた！」ハーピーが興奮して声を上げた。羽毛の温もりの中で、最後の一滴まで引き出された——それも、今までで最も素早く、最も確実に。ハーピーが鳴きながら離れていく声が、遠くなっていった。[p]
; [cg f="harpy_h5_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてハーピーは高らかに鳴いて、空へと飛び去っていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_2f"]
*harpy_win
[eval exp="f.f2_harpy=1"]
[nm t="ナレーション"]
ハーピーが満足そうに飛び去った。先へ進む。[p]
[fadeout time="800" color="0x000000"][wait time=300]
[jump storage="chap2_explore.ks" target="*hub_2f"]