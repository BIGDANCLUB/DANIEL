;=== chap2_sr_succubus.ks - 上級サキュバス ===
*sr_succubus_start
[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]
[fadein time="800"]
[nm t="ナレーション"]
5階最上フロア。魔力が濃く漂う。広い部屋の中央、圧倒的な存在感を持つサキュバスが待っていた。[p]
[nm t="ナレーション"]
普通のサキュバスとは格が違う——上級サキュバス。その瞳が勇者を品定めするように見つめる。[p]
[nm t="上級サキュバス"]
「……来たのね、勇者。この私の前まで。それだけでも賞賛に値するわ。でも——ここから先には進ませない」[p]
*sr_succubus_c1_prompt
どうする？[r]
[link target="*sr_succubus_c1_safe"]上級サキュバスの魔力に抗って正気を保つ[endlink][r]
[link target="*sr_succubus_c1_wrong"]上級サキュバスの美しさに圧倒される[endlink][r]
[s]
*sr_succubus_c1_safe
[nm t="ナレーション"]
強い意志で魔力を押しのけた。上級サキュバスが驚いた顔をした。[p]
[jump target="*sr_succubus_c2_prompt"]
*sr_succubus_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
美しさに見惚れた瞬間、精神に直接魅了の魔法が流れ込んできた。[p]
[nm t="上級サキュバス"]
「……見惚れた。人間は正直ね」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*sr_succubus_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*sr_succubus_c2_prompt"]
*sr_succubus_c2_prompt
どうする？[r]
[link target="*sr_succubus_c2_safe"]夢と現実の境界を保つ[endlink][r]
[link target="*sr_succubus_c2_wrong"]夢幻魔法に引き込まれる[endlink][r]
[s]
*sr_succubus_c2_safe
[nm t="ナレーション"]
女神の加護を盾に夢幻魔法を弾いた。[p]
[jump target="*sr_succubus_c3_prompt"]
*sr_succubus_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
夢の中に引き込まれかけた——美しい夢。[p]
[nm t="上級サキュバス"]
「……もっと深く来て。夢の中は心地よいでしょう？」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*sr_succubus_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*sr_succubus_c3_prompt"]
*sr_succubus_c3_prompt
どうする？[r]
[link target="*sr_succubus_c3_safe"]上級サキュバスの言葉を信じない[endlink][r]
[link target="*sr_succubus_c3_wrong"]上級サキュバスの提案を聞いてしまう[endlink][r]
[s]
*sr_succubus_c3_safe
[nm t="ナレーション"]
言葉の罠を見抜いて応じなかった。[p]
[jump target="*sr_succubus_c4_prompt"]
*sr_succubus_c3_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
提案に耳を傾けた途端、魔法陣に踏み込んでいた。[p]
[nm t="上級サキュバス"]
「……踏み込んだ。契約成立よ」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*sr_succubus_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*sr_succubus_c4_prompt"]
*sr_succubus_c4_prompt
どうする？[r]
[link target="*sr_succubus_c4_safe"]魔力を加護で中和する[endlink][r]
[link target="*sr_succubus_c4_wrong"]魔力の快感に溺れる[endlink][r]
[s]
*sr_succubus_c4_safe
[nm t="ナレーション"]
加護の光が上級サキュバスの魔力を中和した。[p]
[jump target="*sr_succubus_c5_prompt"]
*sr_succubus_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
魔力の快感が全身に広がり、抵抗する気が失われていく。[p]
[nm t="上級サキュバス"]
「……気持ちいいでしょう？これが上級の魔力よ」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*sr_succubus_h_dispatch"][endif]
[nm t="ナレーション"]
かろうじて脱する。[p]
[jump target="*sr_succubus_c5_prompt"]
*sr_succubus_c5_prompt
どうする？[r]
[link target="*sr_succubus_c5_safe"]加護を全力解放で決着をつける[endlink][r]
[link target="*sr_succubus_c5_wrong"]快感の中で意識が溶ける[endlink][r]
[s]
*sr_succubus_c5_safe
[nm t="ナレーション"]
全力の加護解放で上級サキュバスを圧倒した。[p]
[jump target="*sr_succubus_win"]
*sr_succubus_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[nm t="ナレーション"]
意識が溶ける中、上級サキュバスに抱きとめられた。[p]
[nm t="上級サキュバス"]
「……落ちた。では——ゆっくり味わわせてもらうわ」[l]
[if exp="f.enemy_mistakes>=2"][jump target="*sr_succubus_h_dispatch"][endif]
[jump target="*sr_succubus_h_dispatch"]
*sr_succubus_h_dispatch
[if exp="f.enemy_last_mistake==1"][jump target="*sr_succubus_h1"][endif]
[if exp="f.enemy_last_mistake==2"][jump target="*sr_succubus_h2"][endif]
[if exp="f.enemy_last_mistake==3"][jump target="*sr_succubus_h3"][endif]
[if exp="f.enemy_last_mistake==4"][jump target="*sr_succubus_h4"][endif]
[jump target="*sr_succubus_h5"]
*sr_succubus_h1
[eval exp="f.scene_sr_succubus_h1=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="sr_succubus_h1_01"]              ← 最初のCG
[nm t="ナレーション"]
翼が広がった。普通のサキュバスの二倍はある漆黒の翼が、音もなく周囲を覆い尽くした。逃げ場が消え、光が消え、上級サキュバスの翼の内側だけが世界になった。[p]
; [cg f="sr_succubus_h1_02"]              ← 中盤CG
[nm t="上級サキュバス" color="#dd88ff"]
「……あなた、名前は？」[l]
[nm t="ナレーション"]
突然の質問に答える間もなく、翼の内側から魔力が滲み出してきた。下位のサキュバスとは比べ物にならない密度——淫紋が過負荷を起こしたように熱くなり、意識が揺れた。[p]
; [cg f="sr_succubus_h1_03"]              ← クライマックスCG
[nm t="上級サキュバス" color="#dd88ff"]
「覚えておきなさい。あなたから全てをいただくのは私。上級の私が直々に相手をする勇者は、そうそういないのよ」[l]
[nm t="ナレーション"]
格の違いが、刺激の質に出ていた。精密で、深く、出口がない。抵抗の意志を根元から解体するような魔力の圧力の下で、全てが差し出されていった。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて上級サキュバスは翼を静かに閉じ、離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_5f"]
*sr_succubus_h2
[eval exp="f.scene_sr_succubus_h2=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="sr_succubus_h2_01"]              ← 最初のCG
[nm t="ナレーション"]
夢だ——そう気づいたのに、目が覚めない。上級サキュバスが作り上げた夢幻の迷宮は、「夢だと知っている」という事実すら取り込んで使う。[p]
; [cg f="sr_succubus_h2_02"]              ← 中盤CG
[nm t="上級サキュバス" color="#dd88ff"]
「夢の中でも、身体の反応は本物よ。……それが上位の夢幻魔法ね」[l]
[nm t="ナレーション"]
夢の中の廊下を歩くたびに、壁が意識を撫でる。扉を開けるたびに、新しい快感の部屋がある。上級サキュバスはその全ての部屋の設計者として、どこにでも現れた。[l]
どの方向へ走っても彼女がいる。どの出口も彼女に続く。夢幻迷宮の中で、レンは選択の余地なく全てを消耗させられていった。目覚めた時には、翼の中に抱かれていた。[p]
; [cg f="sr_succubus_h2_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
どれほど経ったか——目が覚めた時、上級サキュバスは既にそこにはいなかった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_5f"]
*sr_succubus_h3
[eval exp="f.scene_sr_succubus_h3=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="sr_succubus_h3_01"]              ← 最初のCG
[nm t="ナレーション"]
床の魔法陣が光った。足が動かない。手が動かない。身体の自由が、魔法陣の起動と同時に全て上級サキュバスに委ねられた。[p]
; [cg f="sr_succubus_h3_02"]              ← 中盤CG
[nm t="上級サキュバス" color="#dd88ff"]
「……契約の魔法陣。この城に踏み込んだ瞬間から、あなたはすでに縛られていたの。気づかなかった？」[l]
[nm t="ナレーション"]
優雅に近づいてくる。急がない。拘束された身体が逃げないとわかっているから。長い指が淫紋の上に置かれた——それだけで、全身の制御が崩れた。[l]
「今日は徹底的にいただくわ。あなたの精力は規格外——それだけに、きちんと全て回収しなければ」そう言いながら、上級サキュバスは仕事を始めた。逃げ場はない。抵抗もできない。完全な無力の中で、全てが引き出されていった。[p]
; [cg f="sr_succubus_h3_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
魔法陣の光が消えた時、上級サキュバスは静かに立ち上がって離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_5f"]
*sr_succubus_h4
[eval exp="f.scene_sr_succubus_h4=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="sr_succubus_h4_01"]              ← 最初のCG
[nm t="ナレーション"]
「降参するの？」上級サキュバスが静かに問いかけてきた。その声に——侮蔑はなかった。むしろ、柔らかい。[p]
; [cg f="sr_succubus_h4_02"]              ← 中盤CG
[nm t="上級サキュバス" color="#dd88ff"]
「……いいわ。素直な勇者は嫌いじゃない。ご褒美をあげる」[l]
[nm t="ナレーション"]
「ご褒美」の意味が、直後に理解できた。上級サキュバスが本気で「気持ちよくさせよう」と動き始めた。これまでとは別の、快楽を与えることを目的とした動きだった。[l]
力を入れる必要がない。ただ受け取るだけでいい——そう言われた通りに委ねると、上級サキュバスは丁寧に、贅沢に、惜しみなく全身を扱ってくれた。降参という行為が、こんなにも甘いものだとは知らなかった。[p]
; [cg f="sr_succubus_h4_03"]              ← クライマックスCG
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて上級サキュバスはゆっくりと身を起こし、離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_5f"]
*sr_succubus_h5
[eval exp="f.scene_sr_succubus_h5=1"]
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="sr_succubus_h5_01"]              ← 最初のCG
[nm t="ナレーション"]
「今夜は時間があるの」と上級サキュバスは言った。その言葉の重みが、全身に沁み込んでくる。[p]
; [cg f="sr_succubus_h5_02"]              ← 中盤CG
[nm t="上級サキュバス" color="#dd88ff"]
「一度や二度では満足できないわ。あなたの精力は特別——全部いただいても、また満ちてくるでしょう。何度でも」[l]
[nm t="ナレーション"]
翼に包まれたまま、時間の感覚が薄れていった。一度限界を迎えても、上級サキュバスの魔力が次の充填を促す。また限界を迎える。また促される。どれほど繰り返したか、数えることも諦めた頃——[p]
; [cg f="sr_succubus_h5_03"]              ← クライマックスCG
[nm t="上級サキュバス" color="#dd88ff"]
「……レン」[l]
[nm t="ナレーション"]
名前を呼ばれた。呟くような、かすかな声。翼の内側で、上級サキュバスが初めて人間の目をした。「……また、来なさい」そう言って、静かに翼を開いた。[p]
[call storage="system/init.ks" target="*squeeze_event"]
[nm t="ナレーション"]
やがて上級サキュバスは静かに、何も言わずに離れていった。[p]
[if exp="f.from_recall==1"][eval exp="f.from_recall=0"][jump storage="recollection_room.ks" target="*recollection_start"][endif]
[jump storage="chap2_explore.ks" target="*hub_5f"]
*sr_succubus_win
[eval exp="f.f5_sr_succubus=1"]
[nm t="ナレーション"]
上級サキュバスが深々と一礼した。「……認める。先へ行きなさい」翼を畳んで道を開けた。[p]
[fadeout time="800" color="0x000000"][wait time=300]
[jump storage="chap2_explore.ks" target="*hub_5f"]