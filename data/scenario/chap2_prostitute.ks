;=== chap2_prostitute.ks - 娼婦 ===
*prostitute_start
[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]
[fadein time="800"]
[nm t="ナレーション"]
4階の一室。豪奢な調度品。扉を開けると、経験豊かそうな女性がソファに座っていた。[p]
[nm t="娼婦"]
「いらっしゃい、勇者様。……特別なサービスをご用意してますよ」[p]
*prostitute_c1_prompt
どうする？[r]
[link target="*prostitute_c1_safe"]用件だけ聞いて立ち去ろうとする[endlink][r]
[link target="*prostitute_c1_wrong"]値段を聞いてみる[endlink][r]
[s]
*prostitute_c1_safe
[nm t="ナレーション"]
素っ気なく断った。娼婦が面白そうに目を細めた。[p]
[jump target="*prostitute_c2_prompt"]
*prostitute_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
値段を聞いた途端、「お支払いは現物で」と言って近づいてきた。[p]
[nm t="娼婦"]
「お金より……あなたの精力の方が価値があるの」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*prostitute_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*prostitute_c2_prompt"]
*prostitute_c2_prompt
どうする？[r]
[link target="*prostitute_c2_safe"]契約書の内容を確認する[endlink][r]
[link target="*prostitute_c2_wrong"]サービスの内容を聞いてしまう[endlink][r]
[s]
*prostitute_c2_safe
[nm t="ナレーション"]
契約書に罠を発見して断った。[p]
[jump target="*prostitute_c3_prompt"]
*prostitute_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
詳細を聞いている間に、いつの間にか座らされていた。[p]
[nm t="娼婦"]
「座ったということは……契約成立ね♪」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*prostitute_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*prostitute_c3_prompt"]
*prostitute_c3_prompt
どうする？[r]
[link target="*prostitute_c3_safe"]娼婦の話術に乗らないよう意識する[endlink][r]
[link target="*prostitute_c3_wrong"]話の流れで飲み物を受け取る[endlink][r]
[s]
*prostitute_c3_safe
[nm t="ナレーション"]
話術を分析して冷静に対処した。[p]
[jump target="*prostitute_c4_prompt"]
*prostitute_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
飲み物に何か入っていたようだ。身体が熱くなってきた。[p]
[nm t="娼婦"]
「特製のドリンクよ。効いてきたでしょ？」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*prostitute_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*prostitute_c4_prompt"]
*prostitute_c4_prompt
どうする？[r]
[link target="*prostitute_c4_safe"]部屋から出ようとする[endlink][r]
[link target="*prostitute_c4_wrong"]娼婦の技術に引き込まれてしまう[endlink][r]
[s]
*prostitute_c4_safe
[nm t="ナレーション"]
素早く扉へ向かった。娼婦が苦笑いした。[p]
[jump target="*prostitute_c5_prompt"]
*prostitute_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
娼婦の手が触れた瞬間、脚から力が抜けた。[p]
[nm t="娼婦"]
「逃げなくていいのよ。気持ちよくしてあげるから」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*prostitute_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*prostitute_c5_prompt"]
*prostitute_c5_prompt
どうする？[r]
[link target="*prostitute_c5_safe"]加護で体の熱を冷ます[endlink][r]
[link target="*prostitute_c5_wrong"]完全に熱に負けてしまう[endlink][r]
[s]
*prostitute_c5_safe
[nm t="ナレーション"]
加護の力で薬の効果を中和した。[p]
[jump target="*prostitute_win"]
*prostitute_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
熱で思考が定まらないまま、娼婦に押し倒された。[p]
[nm t="娼婦"]
「観念して。プロの技を見せてあげる」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*prostitute_h_dispatch"][endif]
[jump target="*prostitute_h_dispatch"]
*prostitute_h_dispatch
[if exp="f.enemy_last_mistake==1"][jump target="*prostitute_h1"][endif]
[if exp="f.enemy_last_mistake==2"][jump target="*prostitute_h2"][endif]
[if exp="f.enemy_last_mistake==3"][jump target="*prostitute_h3"][endif]
[if exp="f.enemy_last_mistake==4"][jump target="*prostitute_h4"][endif]
[jump target="*prostitute_h5"]
*prostitute_h1
[eval exp="f.scene_prostitute_h1=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="prostitute_h1_01"]              ← CG①（最初）
[nm t="ナレーション"]
娼婦が椅子から立ち上がり、ゆっくりと近づいてきた。急がない。慌てない。この職業で長年磨いた「相手のペースに合わせる」技術が、全身の動きに出ていた。[p]
; [cg f="prostitute_h1_02"]              ← CG②
[nm t="娼婦" color="#ffaacc"]
「怖くないよ。……ねえ、こっちおいで。ゆっくりしよ」[l]
[nm t="ナレーション"]
温かい手が引かれた。抵抗できない理由が見当たらない——それが娼婦の技術だった。誘導する言葉、安心させる体温、急所への誘い込みが自然すぎて、気づいた時には全て始まっていた。[l]
「うん、そう。力抜いて」娼婦は経験の積み上げだけで動いていた。一切の迷いなく、一切の遠慮なく——でも一切の痛みなく。全てがプロの仕事として完遂された。「こんな反応久しぶりに見た♪」満足そうな声が聞こえた。[p]
; [cg f="prostitute_h1_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて娼婦は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_4f"]
*prostitute_h2
[eval exp="f.scene_prostitute_h2=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="prostitute_h2_01"]              ← CG①（最初）
[nm t="ナレーション"]
部屋に引き込まれた。豪華ではないが、細部まで計算された空間——明かりの角度、香りの種類、寝台の硬さ。全てが目的のために最適化されている。[p]
; [cg f="prostitute_h2_02"]              ← CG②
[nm t="娼婦" color="#ffaacc"]
「横になって。客のもてなしは慣れてるから、任せてよ♪」[l]
[nm t="ナレーション"]
言われた通りにした途端、全ての主導権が娼婦に移った。どこに手を置くべきか、どの体勢が最も効果的か——娼婦はそれを知り尽くしている。淫紋の位置も、一度触れた瞬間に把握していた。[l]
「こっちの方が気持ちいいでしょ」と言いながら、試すように位置を変える。体が反応するたびに「ほら」と言って笑う。この仕事のプロフェッショナルは、相手の身体のことを当人より詳しかった。[p]
; [cg f="prostitute_h2_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて娼婦は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_4f"]
*prostitute_h3
[eval exp="f.scene_prostitute_h3=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="prostitute_h3_01"]              ← CG①（最初）
[nm t="ナレーション"]
「あのね」と娼婦が言った。「私、淫紋持ちの客は初めてなの」話しながら、手は動いていた。話と手が完全に別々に機能している。[p]
; [cg f="prostitute_h3_02"]              ← CG②
[nm t="娼婦" color="#ffaacc"]
「だから逆に興味あって。どこが一番反応するか、ちゃんと確かめたいなって♪」[l]
[nm t="ナレーション"]
言葉で注意を引きながら、手は別のことをする。これも技術だ。会話で緊張を解きながら、身体への侵入を自然にする。気づいた時には既にペースが完全に掌握されていた。[l]
「こういう子、好きよ」娼婦が言った。感情的な言葉なのか、営業的な言葉なのか判断できない。でもその声は温かかった。そしてその後の処置は、容赦がなかった。[p]
; [cg f="prostitute_h3_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて娼婦は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_4f"]
*prostitute_h4
[eval exp="f.scene_prostitute_h4=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="prostitute_h4_01"]              ← CG①（最初）
[nm t="ナレーション"]
脚の力が完全に抜けた。壁に倒れかかったところを、娼婦が片腕で支えた。力持ちだった。事もなげに支えながら、「ほら、こっち来て」と部屋の奥へ誘導する。[p]
; [cg f="prostitute_h4_02"]              ← CG②
[nm t="娼婦" color="#ffaacc"]
「動けない客も珍しくないよ。大丈夫、私が全部やるから」[l]
[nm t="ナレーション"]
横たえられた。全ての判断と動作を娼婦に委ねることになった——というより、そうなるように誘導されていた。こちらが何もしなくていい状況で、娼婦はより本来の仕事をし始めた。[l]
受け身でいるだけで全てが進んだ。娼婦の技術は、相手が動けない時の方がむしろ真価を発揮するのかもしれない。「特別サービス♪」と言いながら進める処置は、選択の余地なく全てを引き出していった。[p]
; [cg f="prostitute_h4_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて娼婦は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_4f"]
*prostitute_h5
[eval exp="f.scene_prostitute_h5=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="prostitute_h5_01"]              ← CG①（最初）
[nm t="ナレーション"]
「今夜はゆっくりしてって」娼婦が言った。それは宣言だった。[p]
; [cg f="prostitute_h5_02"]              ← CG②
[nm t="娼婦" color="#ffaacc"]
「珍しい客だから、ちゃんとサービスしたいの。……嫌？」[l]
[nm t="ナレーション"]
嫌という理由がなかった。それが娼婦の設定した状況だった。抵抗する理由を消し、留まる理由だけを残す。「全部サービスに含まれてるから」と言いながら、夜が更けても娼婦の手は止まらなかった。[l]
一度限界を迎えるたびに「もう一回♪」と笑顔で続ける。職業的な笑顔のはずが、長い夜の後半には本物の表情が混じってきた。「……あなた、面白い人ね」最後にそう言った声は、営業ではなかった。[p]
; [cg f="prostitute_h5_03"]              ← CG③（必要なら下に ④⑤... と追加可）
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて娼婦は離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_4f"]
*prostitute_win
[eval exp="f.f4_prostitute=1"]
[nm t="ナレーション"]
娼婦が優雅にお辞儀した。「またいつでも♪」先へ進む。[p]
[fadeout time="800" color="0x000000"][wait time=300]
[jump storage="chap2_explore.ks" target="*hub_4f"]