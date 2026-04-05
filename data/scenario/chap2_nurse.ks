;=== chap2_nurse.ks - ナース ===
*nurse_start
[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]
[fadein time="800"]
[nm t="ナレーション"]
研究棟の一角に白い部屋。医療用ベッドと器具が並んでいる。[p]
[nm t="ナレーション"]
白衣のナースが微笑みながら近づいてきた。[p]
[nm t="ナース"]
「あら、怪我してる？診てあげましょうか♪」[p]
*nurse_c1_prompt
どうする？[r]
[link target="*nurse_c1_safe"]怪我していないと断る[endlink][r]
[link target="*nurse_c1_wrong"]怪我を診てもらう[endlink][r]
[s]
*nurse_c1_safe
[nm t="ナレーション"]
きっぱり断った。ナースが少し悲しそうな顔をした。[p]
[jump target="*nurse_c2_prompt"]
*nurse_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
診察台に座った途端、腕を拘束された。[p]
[nm t="ナース"]
「動かないでください。治療中ですよ♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*nurse_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*nurse_c2_prompt"]
*nurse_c2_prompt
どうする？[r]
[link target="*nurse_c2_safe"]ナースの手が不自然なことに気づく[endlink][r]
[link target="*nurse_c2_wrong"]注射を勧められて受け入れる[endlink][r]
[s]
*nurse_c2_safe
[nm t="ナレーション"]
不自然な動きに気づき、その手を払った。[p]
[jump target="*nurse_c3_prompt"]
*nurse_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
注射を受けた。甘い液体が体内に回っていく感覚。[p]
[nm t="ナース"]
「……効いてきたみたいですね。感度が上がりますよ♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*nurse_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*nurse_c3_prompt"]
*nurse_c3_prompt
どうする？[r]
[link target="*nurse_c3_safe"]薬の影響に抗う[endlink][r]
[link target="*nurse_c3_wrong"]薬の心地よさに流される[endlink][r]
[s]
*nurse_c3_safe
[nm t="ナレーション"]
強い意志で薬に抗った。ナースが驚いた顔をした。[p]
[jump target="*nurse_c4_prompt"]
*nurse_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
薬の影響で身体が言うことを聞かなくなる。[p]
[nm t="ナース"]
「大丈夫ですよ。ナースに任せて♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*nurse_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*nurse_c4_prompt"]
*nurse_c4_prompt
どうする？[r]
[link target="*nurse_c4_safe"]診察台から逃げ出す[endlink][r]
[link target="*nurse_c4_wrong"]ナースの指示に従ってしまう[endlink][r]
[s]
*nurse_c4_safe
[nm t="ナレーション"]
診察台から素早く飛び降りた。[p]
[jump target="*nurse_c5_prompt"]
*nurse_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
ナースの指示通りに動いたら、いつの間にか拘束されていた。[p]
[nm t="ナース"]
「おとなしくて良い患者さんですね♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*nurse_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*nurse_c5_prompt"]
*nurse_c5_prompt
どうする？[r]
[link target="*nurse_c5_safe"]加護の力で脱出する[endlink][r]
[link target="*nurse_c5_wrong"]薬で動けなくなっている[endlink][r]
[s]
*nurse_c5_safe
[nm t="ナレーション"]
加護の力で拘束を壊して脱出した。[p]
[jump target="*nurse_win"]
*nurse_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
薬の影響で完全に動けなくなった。[p]
[nm t="ナース"]
「では……治療を始めましょうか♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*nurse_h_dispatch"][endif]
[jump target="*nurse_h_dispatch"]
*nurse_h_dispatch
[if exp="f.enemy_last_mistake==1"][jump target="*nurse_h1"][endif]
[if exp="f.enemy_last_mistake==2"][jump target="*nurse_h2"][endif]
[if exp="f.enemy_last_mistake==3"][jump target="*nurse_h3"][endif]
[if exp="f.enemy_last_mistake==4"][jump target="*nurse_h4"][endif]
[jump target="*nurse_h5"]
*nurse_h1
[eval exp="f.scene_nurse_h1=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="nurse_h1_01"]              ← 最初のCG
[nm t="ナレーション"]
気づけば診察台の上に寝かされていた。白いベルトが手首と足首に巻き付き、身体をしっかりと台に固定している。ナースが手袋をはめながら、事務的な笑顔を向けてきた。[p]
; [cg f="nurse_h1_02"]              ← 中盤CG
[nm t="ナース"]
「痛くしないですよ。気持ちよくなるだけです♪　淫紋を持つ患者さんには、特別な処置が必要なんです」[l]
[nm t="ナレーション"]
ナースの指先は滑らかで、迷いがない。淫紋の位置をすでに把握しているかのように、最初の一触れから的確に急所を押さえてくる。医療的な所作——押して、撫でて、圧力を微妙に変えながら——が、淫紋を通じて全身に甘い電流を走らせた。[p]
; [cg f="nurse_h1_03"]              ← クライマックスCG
[nm t="ナース"]
「反応がとても良いですね。さすが淫紋持ちの患者さん。では、しっかり採取させていただきます♪」[l]
[nm t="ナレーション"]
抵抗しようにも、拘束されたまま全ての刺激を受け止めるしかなかった。ナースの手は丁寧で、容赦がなく、プロの処置として淡々と目的を果たしていく。熱が下腹部に集まり、理性とは無関係に身体が応えていった。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてナースは離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*nurse_h2
[eval exp="f.scene_nurse_h2=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="nurse_h2_01"]              ← 最初のCG
[nm t="ナレーション"]
点滴の針が腕に刺さった瞬間から、全身の感度が異常なほど鋭くなっていくのを感じた。シーツの布地が皮膚を撫でるだけで鳥肌が立ち、空気の流れさえも刺激に変わる。ナースがその変化を観察しながら、満足げに頷いた。[p]
; [cg f="nurse_h2_02"]              ← 中盤CG
[nm t="ナース"]
「反応が良いですね♪　この点滴は淫紋との相乗効果があって、感度が通常の三倍以上になるんです。採取効率が上がりますよ」[l]
[nm t="ナレーション"]
クリップボードに何かを書き留めながら、ナースは「バイタルを確認しますね」と言って手を伸ばしてきた。その指先が淫紋に触れた瞬間——全身が弧を描くように反応した。声を抑えようとしても、喉が勝手に震えた。[p]
; [cg f="nurse_h2_03"]              ← クライマックスCG
[nm t="ナース"]
「やっぱり効いてますね。では本処置に入りましょうか。記録上は『特殊分泌物採取』になります♪」[l]
[nm t="ナレーション"]
医療的な言葉の羅列が、かえって奇妙な羞恥を呼び起こした。ナースにとってこれは処置であり、こちらの反応は全てデータとして観察されている。それでも——いや、だからこそ——身体は完全に翻弄され、薬と淫紋が相乗して最後の一滴まで引き出されていった。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてナースは離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*nurse_h3
[eval exp="f.scene_nurse_h3=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="nurse_h3_01"]              ← 最初のCG
[nm t="ナレーション"]
「心拍数を確認しますね」聴診器が胸に当てられた。「少し速いですね。……淫紋の影響が出ているようです」ナースが手帳に記録する。その「確認」が終わったはずなのに、聴診器が動かなかった。[p]
; [cg f="nurse_h3_02"]              ← 中盤CG
[nm t="ナース" color="#ffcccc"]
「もう少し様子を見ます。数値が落ち着くまで、バイタルを続けて取らないと♪」[l]
[nm t="ナレーション"]
バイタル確認という名目で、ナースの手は移動し続けた。「血圧」「体温」「反射」——一つ確認するたびに触れる場所が変わり、その度に数値が「乱れる」ので「もう少し確認が必要」になる。[l]
完璧な循環だった。測定が乱れを引き起こし、乱れが測定を正当化する。「心拍数が最高値を更新しました」ナースが言った時、全てが終わりに差し掛かっていた。「採取しますね♪ こうなるのは分かってましたから、準備してきました」[p]
; [cg f="nurse_h3_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてナースは離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*nurse_h4
[eval exp="f.scene_nurse_h4=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="nurse_h4_01"]              ← 最初のCG
[nm t="ナレーション"]
「特別処置に移ります」ナースが言いながら、カーテンを引いた。個室になった。「この処置は他の患者さんには内緒にしてくださいね。……勇者専用のプロトコルなので」[p]
; [cg f="nurse_h4_02"]              ← 中盤CG
[nm t="ナース" color="#ffcccc"]
「淫紋を持つ患者さんには、定期的な精力の解放が必要なんです。溜め込むと副作用が出るという研究があって……だから、これも医療行為なんですよ♪」[l]
[nm t="ナレーション"]
「医療行為」という言葉が、奇妙な安堵をもたらした。抵抗する意味が消えてしまう。ナースは専門家として、淀みない手技で処置を進めた。「副作用が出ないように、しっかりやらないといけませんからね」[l]
医療的な口調と、しかし医療の枠をはるかに超えた処置の内容。その矛盾が、全ての抵抗の言葉を宙に浮かせた。「処置完了♪ お疲れ様でした。定期的に来てくださいね」ナースは笑顔で手袋を外した。[p]
; [cg f="nurse_h4_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてナースは離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*nurse_h5
[eval exp="f.scene_nurse_h5=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="nurse_h5_01"]              ← 最初のCG
[nm t="ナレーション"]
「今日は時間をかけてやりますね」ナースが宣言した。ベッドのリクライニングを調整し、周囲の機器を確認し、新しい手袋を取り出した。全ての準備が整っていた。[p]
; [cg f="nurse_h5_02"]              ← 中盤CG
[nm t="ナース" color="#ffcccc"]
「淫紋の定期メンテナンス、フルコースです♪ 普段は時間の都合で略式なんですけど、今日はちゃんとやります」[l]
[nm t="ナレーション"]
「フルコース」が始まった。点滴、バイタル記録、感度測定、複数段階の刺激と採取——全てが順序立てて行われた。ナースは一切の無駄がなく、休憩も取らず、患者のケアに全力を注いだ。[l]
何度も限界を迎えた。その度にナースは「もう少しありますよ」と確認して続けた。全ての処置が終わった時、ナースは手袋を外しながら言った。「……お疲れ様でした。本当に良いサンプルでした」その声に、珍しく感情の熱があった。[p]
; [cg f="nurse_h5_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがてナースは離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*nurse_win
[eval exp="f.f3_nurse=1"]
[nm t="ナレーション"]
ナースが深々と頭を下げた。「お大事に♪」先へ進む。[p]
[fadeout time="800" color="0x000000"][wait time=300]
[jump storage="chap2_explore.ks" target="*hub_3f"]