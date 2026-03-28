;==========================================================
; chap2_fighter.ks - 1F「女戦士」
;==========================================================
*fighter_start

; [bg storage="bg_training_hall.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
鍛錬場のような広い部屋。中央に、鎧姿の女戦士が一人、剣を振っていた。[p]

; [chara_show name="fighter" storage="chara/fighter_normal.png" pos="center" time="500"]

[nm t="女戦士" color="#ffcc88"]
「……勇者か。待っていた」[l]

[nm t="女戦士" color="#ffcc88"]
「私はここの衛兵隊長だ。通るなら私を倒してからにしろ」[l]

[nm t="女戦士" color="#ffcc88"]
「……ただし、倒し方は問わない。魔王様は生きて連れてこいと言っていたが……私個人は、強い者が好きだ」[p]

どう対処する？[r]
[link target="*fighter_duel"]正々堂々と剣で戦う[endlink][r]
[link target="*fighter_ambush"]女神の加護を使って奇襲する[endlink][r]
[link target="*fighter_talk"]「話し合いで解決できないか」と申し出る[endlink][r]
[s]

*fighter_duel

[nm t="ナレーション"]
互いに剣を構える。女戦士は強い——だが女神の加護が勇者の剣に力を与える。[l]

[nm t="ナレーション"]
激しい打ち合いの末、女戦士の剣が弾かれた。[p]

[nm t="女戦士" color="#ffcc88"]
「……負けた。見事だ、勇者」[l]

[nm t="女戦士" color="#ffcc88"]
「……通っていい。ただし——」[l]

[nm t="女戦士" color="#ffcc88"]
「勇者、あなたの精を少し分けてくれ。戦士として、あなたの力の根源が知りたい」[p]

どうする？[r]
[link target="*fighter_offer"]「……わかった」→ 同意[endlink][r]
[link target="*fighter_pass"]「それは断る」→ そのまま通る[endlink][r]
[s]

*fighter_ambush

[nm t="ナレーション"]
女神の光を一気に放出——！ 女戦士が目を眩ませた隙に、横を駆け抜けた。[p]

[nm t="女戦士" color="#ffcc88"]
「……ッ！ 卑怯な！」[l]

[nm t="ナレーション"]
「戦場に卑怯はない——そう教わっただろう」[l]

[nm t="ナレーション"]
振り返らず走り抜けた。[p]

[eval exp="f.resist_count=f.resist_count+1"]
[jump target="*fighter_clear"]

*fighter_talk

[nm t="勇者" color="#aaddff"]
「……俺はあなたと戦いたくない」[l]

[nm t="女戦士" color="#ffcc88"]
「……なぜだ」[l]

[nm t="勇者" color="#aaddff"]
「あなたは強い。こんな場所で戦うより、もっと価値ある戦い場があるはずだ」[p]

[nm t="女戦士" color="#ffcc88"]
「……」[l]

[nm t="女戦士" color="#ffcc88"]
「……面白いことを言う。ならば、その言葉の代償を払え」[l]

[nm t="女戦士" color="#ffcc88"]
「戦いの代わりに、あなたの精を一度いただく。それで見逃してやる」[p]

[jump target="*fighter_offer"]

*fighter_offer

[eval exp="f.surrender_count=f.surrender_count+1"]

; ====【Hシーン：女戦士・武人搾精】====
; [cutin storage="event/fighter_h_offer01.jpg"]

[nm t="女戦士" color="#ffcc88"]
「……では、始める。正々堂々とな」[p]

[nm t="ナレーション"]
女戦士が鎧の手袋を外した。素手になった手は、武器を握り続けてきた武人の手——しかし今は、別の使い方をする。[p]

[nm t="女戦士" color="#ffcc88"]
「……ふむ。確かに、これは特別な力だ」[l]

[nm t="ナレーション"]
一切の遠慮がない。戦士として相手を試すように、正面から向き合ってくる。[l]

[nm t="ナレーション"]
その真剣さが、かえって恥ずかしかった。[p]

[nm t="勇者" color="#aaddff"]
「……そんな真剣な顔でしないでくれ……」[l]

[nm t="女戦士" color="#ffcc88"]
「何事も真剣にやるのが私の流儀だ。……我慢するな。勇者も、限界を見せろ」[p]

[nm t="ナレーション"]
命令口調で言われると、逆らえない気持ちになった。[l]

[nm t="ナレーション"]
女戦士の手が、ためらいなく追い詰めてくる。[p]
; ==========================================

[nm t="女戦士" color="#ffcc88"]
「……満足した。行け」[p]

[call storage="system/init.ks" target="*squeeze_event"]
[jump target="*fighter_clear"]

*fighter_pass

[nm t="ナレーション"]
女戦士は黙ってうなずき、道を開けた。[p]

*fighter_clear

[eval exp="f.f1_fighter=1"]
[nm t="ナレーション"]
——女戦士を突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_1f"]
