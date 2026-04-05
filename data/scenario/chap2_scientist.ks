;=== chap2_scientist.ks - 科学者 ===
*scientist_start
[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]
[fadein time="800"]
[nm t="ナレーション"]
3階研究棟の奥。実験器具が所狭しと並んでいる。[p]
[nm t="ナレーション"]
白衣の女性科学者が振り返った。冷静な目でこちらを見ている。[p]
[nm t="科学者"]
「勇者のサンプルを採取できるとは。これは貴重なデータになる」[p]
*scientist_c1_prompt
どうする？[r]
[link target="*scientist_c1_safe"]科学者の意図を警戒して距離を保つ[endlink][r]
[link target="*scientist_c1_wrong"]興味本位で実験器具を触る[endlink][r]
[s]
*scientist_c1_safe
[nm t="ナレーション"]
距離を保ちながら科学者の行動を観察する。[p]
[jump target="*scientist_c2_prompt"]
*scientist_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
触れた途端、器具が起動して拘束装置が作動した。[p]
[nm t="科学者"]
「トラップです。データ収集開始します」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*scientist_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*scientist_c2_prompt"]
*scientist_c2_prompt
どうする？[r]
[link target="*scientist_c2_safe"]申し出た実験を断固として断る[endlink][r]
[link target="*scientist_c2_wrong"]実験の詳細を聞いてみる[endlink][r]
[s]
*scientist_c2_safe
[nm t="ナレーション"]
断固として断った。科学者は少し残念そうだ。[p]
[jump target="*scientist_c3_prompt"]
*scientist_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
詳細を聞いている間に、ガスが充満してきた。[p]
[nm t="科学者"]
「説明中に気体麻酔を投与しました。効率的でしょう？」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*scientist_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*scientist_c3_prompt"]
*scientist_c3_prompt
どうする？[r]
[link target="*scientist_c3_safe"]ガスを感知して息を止める[endlink][r]
[link target="*scientist_c3_wrong"]ガスの影響で意識が朦朧とする[endlink][r]
[s]
*scientist_c3_safe
[nm t="ナレーション"]
素早く布で口を覆い、ガスの影響を最小限にした。[p]
[jump target="*scientist_c4_prompt"]
*scientist_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
ガスで視界がぼやけてきた。膝が震える。[p]
[nm t="科学者"]
「麻酔は身体に残ります。もうすぐ動けなくなります」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*scientist_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*scientist_c4_prompt"]
*scientist_c4_prompt
どうする？[r]
[link target="*scientist_c4_safe"]加護でガスを無効化する[endlink][r]
[link target="*scientist_c4_wrong"]测定器に近づいてしまう[endlink][r]
[s]
*scientist_c4_safe
[nm t="ナレーション"]
加護の光がガスを中和した。科学者が驚いた。[p]
[jump target="*scientist_c5_prompt"]
*scientist_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
測定器に捕まり、拘束ベルトが自動で巻きついた。[p]
[nm t="科学者"]
「よく来てくれました。測定開始します」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*scientist_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*scientist_c5_prompt"]
*scientist_c5_prompt
どうする？[r]
[link target="*scientist_c5_safe"]一気に脱出を図る[endlink][r]
[link target="*scientist_c5_wrong"]拘束された状態で抵抗する[endlink][r]
[s]
*scientist_c5_safe
[nm t="ナレーション"]
全力で走り抜けて実験室を脱出した。[p]
[jump target="*scientist_win"]
*scientist_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
拘束を解こうとするが、科学者に押さえられた。[p]
[nm t="科学者"]
「逃がしません。サンプル採取が完了するまでは」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*scientist_h_dispatch"][endif]
[jump target="*scientist_h_dispatch"]
*scientist_h_dispatch
[if exp="f.enemy_last_mistake==1"][jump target="*scientist_h1"][endif]
[if exp="f.enemy_last_mistake==2"][jump target="*scientist_h2"][endif]
[if exp="f.enemy_last_mistake==3"][jump target="*scientist_h3"][endif]
[if exp="f.enemy_last_mistake==4"][jump target="*scientist_h4"][endif]
[jump target="*scientist_h5"]
*scientist_h1
[eval exp="f.scene_scientist_h1=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="scientist_h1_01"]              ← 最初のCG
[nm t="ナレーション"]
冷たい金属製の拘束台に仰向けにされ、ベルトが胸・腹・太腿の三箇所を固定した。白衣の科学者がゴム手袋を両手に嵌めながら近づいてくる。[p]
; [cg f="scientist_h1_02"]              ← 中盤CG
[nm t="科学者"]
「では、採取を始めます。苦痛は最小限に抑えますので安心してください——とはいえ、この淫紋の特性上、多少の刺激は必要です」[l]
[nm t="ナレーション"]
電極パッドが数カ所に貼られ、細いケーブルが測定装置へと伸びる。モニターが点灯し、脈拍・皮膚電気抵抗・体温のグラフがリアルタイムで描かれ始めた。[p]
; [cg f="scientist_h1_03"]              ← クライマックスCG
[nm t="科学者"]
「ベースライン計測完了。……では、刺激フェーズに移ります」[l]
[nm t="ナレーション"]
手袋越しの指が淫紋に触れた瞬間、全身に電流のような感覚が走った。科学者はモニターから目を離さず、数値の変化を声に出して読み上げながら、正確な動きで採取を進めていく。感情を持ち込む隙間が一切ない処置だった。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
採取完了の電子音が鳴った。科学者はサンプルをラベル付きのチューブに収め、データをタブレットへ転送した。やがて科学者は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*scientist_h2
[eval exp="f.scene_scientist_h2=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="scientist_h2_01"]              ← 最初のCG
[nm t="ナレーション"]
「感度増幅ガスです。閾値が三倍になります」科学者が告げた。既に吸い込んでいた。空気が変わったのはわかったが、選択の余地はなかった。数十秒で、全身の神経がナイフのように研ぎ澄まされた感覚がした。[p]
; [cg f="scientist_h2_02"]              ← 中盤CG
[nm t="科学者" color="#aaddcc"]
「……数値が急上昇しています。予測モデルとほぼ一致。では比較データを取ります」[l]
[nm t="ナレーション"]
ガス吸引前のデータとの比較実験——要するに、同じ刺激を倍の感度で受けるということだった。科学者はクリップボードを持ったまま一手ずつ確かめ、「こちらの反応は増幅係数二・九倍、こちらは三・一倍」と淡々と記録する。[l]
数字として語られる自分の反応が、逆に羞恥を刺激した。感度が三倍の状態でその羞恥が加わり、科学者の淡々とした観察の下で——全てのデータが揃った。「採取完了。回収量も増加、仮説を支持します」[p]
; [cg f="scientist_h2_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて科学者は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*scientist_h3
[eval exp="f.scene_scientist_h3=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="scientist_h3_01"]              ← 最初のCG
[nm t="ナレーション"]
「精神的刺激と身体的反応の相関を測定します」科学者が言いながら、パソコンの画面を向けた。そこには問いが表示されている。質問に答えるたびに、別の装置から刺激が来る。[p]
; [cg f="scientist_h3_02"]              ← 中盤CG
[nm t="科学者" color="#aaddcc"]
「……淫紋と感情の連動性を検証します。正直に答えてください。データの精度に関わります」[l]
[nm t="ナレーション"]
「怖い？」「悔しい？」「気持ちいい？」そういった問いに答えるたびに、科学者の装置がその答えと逆相関で刺激を調整する。正直に答えるほど、より確実に追い詰められる設計になっていた。[l]
「……面白い設計だと思うでしょう」科学者が言った。「答えれば答えるほど採取が進む。意欲的に協力するインセンティブになります」その合理性に言葉が出なかった。科学者は実験を完遂した。[p]
; [cg f="scientist_h3_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて科学者は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*scientist_h4
[eval exp="f.scene_scientist_h4=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="scientist_h4_01"]              ← 最初のCG
[nm t="ナレーション"]
拘束台の上で、科学者が新しい装置を取り出した。「直接採取装置です。効率が向上します」説明しながら、慣れた手つきで装置を設置していく。[p]
; [cg f="scientist_h4_02"]              ← 中盤CG
[nm t="科学者" color="#aaddcc"]
「これにより採取時間が従来の半分になります。……不快感は最小限です。データ収集のご協力に感謝します」[l]
[nm t="ナレーション"]
「不快感は最小限」という言葉の裏が、すぐにわかった。不快ではない——むしろ逆だった。装置は淫紋の反応を読み取りながら、最も効率的な刺激を自動的に選択して与え続ける。人間の手よりも精密で、疲れることもない。[l]
科学者はモニターを見ながら時折メモを取った。「……これは実用的なデータですね」と呟いた声に、感情の揺れはなかった。でも——採取が終わった後、科学者は一瞬だけ視線をそらした。[p]
; [cg f="scientist_h4_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて科学者は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*scientist_h5
[eval exp="f.scene_scientist_h5=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="scientist_h5_01"]              ← 最初のCG
[nm t="ナレーション"]
「今日は総合評価実験を行います。フェーズは七段階です」科学者が白板に工程を書き出した。七段階。その文字が頭に刻まれた。[p]
; [cg f="scientist_h5_02"]              ← 中盤CG
[nm t="科学者" color="#aaddcc"]
「各フェーズで異なる変数を検証します。所要時間は約三時間。途中で中断するとデータが無効になりますので、ご了承ください」[l]
[nm t="ナレーション"]
三時間、七フェーズ。科学者はタイマーをセットし、第一フェーズを開始した。ガス、装置、手技、各種測定——段階を追うごとに手法が変わり、刺激の質が変わり、限界が何度も更新された。[l]
第七フェーズが終わった時、科学者は全データを整理しながら言った。「……これほどのデータが取れるとは思いませんでした。本当に規格外ですね、勇者サンプルは」その言葉の中に、初めて——感嘆の色があった。[p]
; [cg f="scientist_h5_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて科学者は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_3f"]
*scientist_win
[eval exp="f.f3_scientist=1"]
[nm t="ナレーション"]
科学者がデータを記録している隙に脱出した。[p]
[fadeout time="800" color="0x000000"][wait time=300]
[jump storage="chap2_explore.ks" target="*hub_3f"]