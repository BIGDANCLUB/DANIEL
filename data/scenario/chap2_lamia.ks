;=== chap2_lamia.ks - ラミア ===
*lamia_start
[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]
[fadein time="800"]
[nm t="ナレーション"]
2階廊下。床が石畳から滑らかな大理石に変わった。[p]
[nm t="ナレーション"]
蛇のような気配——ラミアだ。上半身は美しい女性、下半身は巨大な蛇。[p]
[nm t="ラミア"]
「あら……勇者様？こんなところまで来るなんて。でも——ここから先には行かせないわ」[p]
*lamia_c1_prompt
どうする？[r]
[link target="*lamia_c1_safe"]ラミアの目を見ないように視線を逸らす[endlink][r]
[link target="*lamia_c1_wrong"]ラミアの美しい上半身に見惚れてしまう[endlink][r]
[s]
*lamia_c1_safe
[nm t="ナレーション"]
視線を逸らすことで催眠の影響を受けずに済んだ。[p]
[jump target="*lamia_c2_prompt"]
*lamia_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
目が合った瞬間、視界が揺らぎ始めた——催眠の目だ。[p]
[nm t="ラミア"]
「……視線が合った。もう逃げられないわ♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*lamia_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*lamia_c2_prompt"]
*lamia_c2_prompt
どうする？[r]
[link target="*lamia_c2_safe"]蛇体の動きを読んで距離を保つ[endlink][r]
[link target="*lamia_c2_wrong"]ラミアの話に耳を傾ける[endlink][r]
[s]
*lamia_c2_safe
[nm t="ナレーション"]
蛇体の動きを予測して距離を保てた。[p]
[jump target="*lamia_c3_prompt"]
*lamia_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
会話に集中している間に、いつの間にか尾で足首を囲まれていた。[p]
[nm t="ラミア"]
「おしゃべりしている間に……ね♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*lamia_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*lamia_c3_prompt"]
*lamia_c3_prompt
どうする？[r]
[link target="*lamia_c3_safe"]加護の光でラミアの拘束を防ぐ[endlink][r]
[link target="*lamia_c3_wrong"]ラミアの滑らかな尾の感触に気が散る[endlink][r]
[s]
*lamia_c3_safe
[nm t="ナレーション"]
光の障壁がラミアの尾を阻んだ。[p]
[jump target="*lamia_c4_prompt"]
*lamia_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
尾の感触が不思議と心地よく、抵抗する気が薄れてしまう。[p]
[nm t="ラミア"]
「……抵抗する気が失せてきた？それでいいのよ」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*lamia_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*lamia_c4_prompt"]
*lamia_c4_prompt
どうする？[r]
[link target="*lamia_c4_safe"]催眠から覚めるよう強く意識を集中する[endlink][r]
[link target="*lamia_c4_wrong"]催眠の心地よさに身を任せてしまう[endlink][r]
[s]
*lamia_c4_safe
[nm t="ナレーション"]
強い意志で催眠を振り払った。ラミアが驚いた顔をした。[p]
[jump target="*lamia_c5_prompt"]
*lamia_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
催眠に深く落ちていく——全身の力が抜けていく。[p]
[nm t="ラミア"]
「……もっと深く。ラミアの声を聞いていて……」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*lamia_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*lamia_c5_prompt"]
*lamia_c5_prompt
どうする？[r]
[link target="*lamia_c5_safe"]加護を解放して一気に突破する[endlink][r]
[link target="*lamia_c5_wrong"]催眠状態のまま動けない[endlink][r]
[s]
*lamia_c5_safe
[nm t="ナレーション"]
加護の光が催眠を打ち破った。ラミアが怯んだ。[p]
[jump target="*lamia_win"]
*lamia_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
催眠で身動きができないまま、ラミアに近づかれた。[p]
[nm t="ラミア"]
「……動けないのね。じゃあ、ゆっくり味わわせてもらうわ」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*lamia_h_dispatch"][endif]
[jump target="*lamia_h_dispatch"]
*lamia_h_dispatch
[if exp="f.enemy_last_mistake==1"][jump target="*lamia_h1"][endif]
[if exp="f.enemy_last_mistake==2"][jump target="*lamia_h2"][endif]
[if exp="f.enemy_last_mistake==3"][jump target="*lamia_h3"][endif]
[if exp="f.enemy_last_mistake==4"][jump target="*lamia_h4"][endif]
[jump target="*lamia_h5"]
*lamia_h1
[eval exp="f.scene_lamia_h1=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="lamia_h1_01"]              ← CG①（最初）
[nm t="ナレーション"]
気づけば、ラミアの長い尾が足元から絡みついていた。締め付けるのではない——まるで愛しいものを包むように、しっとりと冷たい鱗が全身に巻き付いていく。その感触は不思議なほど心地よく、恐怖より先に安堵に似た感覚が広がった。[p]
; [cg f="lamia_h1_02"]              ← CG②
[nm t="ラミア"]
「苦しくしないから……安心して。ただ……全部、いただくだけよ」[l]
[nm t="ナレーション"]
ゆっくりと、歌うように囁く声が鼓膜に溶け込む。ラミアの瞳が深く輝き、視線が絡み合ったまま離れられなくなる。滑らかな鱗肌の感触が腰から胸へ、腕へと這い上がり、淫紋の箇所に触れるたびに甘い電流が走った。[p]
; [cg f="lamia_h1_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[nm t="ラミア"]
「……そう、力を抜いて。私のものになるの。今だけでいい……今だけで、いいから」[l]
[nm t="ナレーション"]
催眠の甘い霞の中で、抵抗する意思が綿菓子のように溶けていく。ラミアの尾が優しく、しかし確実に全てを包み込み、逃げ道を塞ぎながら——深く、深く引き込んでいった。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてラミアは離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_2f"]
*lamia_h2
[eval exp="f.scene_lamia_h2=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="lamia_h2_01"]              ← CG①（最初）
[nm t="ナレーション"]
催眠の霧の中で、意識は夢と現の境界を漂っていた。ラミアの腕が背中に回り、美しい上半身が胸に密着してくる。蛇の鱗を持つ彼女の肌は人間のものとは違う温度で、その違和感がかえって意識を引き戻そうとする。[p]
; [cg f="lamia_h2_02"]              ← CG②
[nm t="ラミア"]
「大丈夫よ……怖くない。気持ちよくしてあげるから、ね？」[l]
[nm t="ナレーション"]
甘く蕩けるような声で囁きながら、長い尾が下半身にゆっくりと絡みついていく。催眠で弛緩した神経に、鱗の一枚一枚の感触が直接届く。ラミアが顔を近づけ、額に唇を寄せた——その瞬間、淫紋が激しく反応した。[p]
; [cg f="lamia_h2_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[nm t="ラミア"]
「……感じているのね。この紋、すてき。あなたのことが、もっと好きになってしまいそう」[l]
[nm t="ナレーション"]
うっとりと呟きながら、ラミアは尾の圧力を少しずつ高めていく。逃げようという思考が生まれる前に、催眠の甘さがそれを消し去ってしまう。彼女の腕の中で、全ては溶けるように進んでいった。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてラミアは離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_2f"]
*lamia_h3
[eval exp="f.scene_lamia_h3=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="lamia_h3_01"]              ← CG①（最初）
[nm t="ナレーション"]
視線が合った瞬間、足が止まった。ラミアの瞳——深い翡翠色の、渦を巻くような瞳が、こちらの意識を引き込んでいく。逃げなければと思うのに、その思考自体がまるで水の中を漂うように遠くなっていく。[p]
; [cg f="lamia_h3_02"]              ← CG②
[nm t="ラミア"]
「逃げなくていいのよ……ここが、一番安全な場所だから」[l]
[nm t="ナレーション"]
ゆっくりとラミアが近づいてくる。尾が床を滑る音だけが静かに響く。動こうとするたびに、その瞳の渦がわずかに回転して、思考を絡め取ってしまう。彼女の指先がそっと頬に触れた。[p]
; [cg f="lamia_h3_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[nm t="ラミア"]
「私の目を見ていて。……ずっと見ていれば、何も怖くない。私がいるから……大丈夫よ」[l]
[nm t="ナレーション"]
催眠の声が耳の奥まで染み込む。尾が膝の後ろに回り、ゆっくりと床へと誘われる。視線は離せない。ラミアの目の中に、吸い込まれるように落ちていきながら——全てが、彼女の望む形に整えられていった。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてラミアは離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_2f"]
*lamia_h4
[eval exp="f.scene_lamia_h4=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="lamia_h4_01"]              ← CG①（最初）
[nm t="ナレーション"]
催眠の快感の中で、ラミアの尾が全身を包んだ。蛇の力が全身を締め上げ、そして——解放する、を繰り返す。[p]
; [cg f="lamia_h4_02"]              ← CG②
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてラミアは離れていった。[p]
; [cg f="lamia_h4_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_2f"]
*lamia_h5
[eval exp="f.scene_lamia_h5=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="lamia_h5_01"]              ← CG①（最初）
[nm t="ナレーション"]
全身を絡めとられたまま、ラミアは時間をかけてゆっくりと搾り取っていった。催眠の夢の中にいるような、あの長い時間。[p]
; [cg f="lamia_h5_02"]              ← CG②
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてラミアは離れていった。[p]
; [cg f="lamia_h5_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_2f"]
*lamia_win
[eval exp="f.f2_lamia=1"]
[nm t="ナレーション"]
ラミアが尾を解いた。「……強い意志ね。行きなさい」道を開けた。[p]
[fadeout time="800" color="0x000000"][wait time=300]
[jump storage="chap2_explore.ks" target="*hub_2f"]