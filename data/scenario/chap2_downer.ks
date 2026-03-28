;==========================================================
; chap2_downer.ks - 4F「ダウナー女性」
;==========================================================
*downer_start

; [bg storage="bg_dark_room.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
薄暗い部屋。窓から差し込む僅かな光の中、女性が壁にもたれて座っていた。[l]

[nm t="ナレーション"]
表情がない。ただ、こちらを見ている。[p]

; [chara_show name="downer" storage="chara/downer_normal.png" pos="center" time="600"]

[nm t="？？？" color="#aaaaaa"]
「……勇者」[l]

[nm t="？？？" color="#aaaaaa"]
「ここに何しに来たの」[p]

[nm t="勇者" color="#aaddff"]
「……魔王を倒しに。通してほしい」[l]

[nm t="？？？" color="#aaaaaa"]
「……別に止めはしない。でも」[l]

[nm t="？？？" color="#aaaaaa"]
「……あなたの匂い、すごく良い。少し、分けてくれない」[p]

[nm t="ナレーション"]
感情のない声。でも——その目に、かすかな何かが灯っている。[p]

[select text="どう対処する？"
  option="「……わかった」→ 同意する" target="*downer_accept"
  option="「急いでいる」→ 断って通る" target="*downer_pass"
  option="「あなたは何者なんだ？」→ 話を聞く" target="*downer_talk"
]

*downer_pass

[nm t="？？？" color="#aaaaaa"]
「……そう」[l]

[nm t="ナレーション"]
女性は何も言わず、道を開けた。[p]

[eval exp="f.resist_count=f.resist_count+1"]
[jump target="*downer_clear"]

*downer_talk

[nm t="？？？" color="#aaaaaa"]
「……私？ 魔王の城で働いている。それだけ」[l]

[nm t="勇者" color="#aaddff"]
「なぜここに？ 望んでここにいるのか？」[l]

[nm t="？？？" color="#aaaaaa"]
「……居場所が、ここしかなかった。外の世界は……疲れた」[p]

[nm t="ナレーション"]
長い沈黙。[p]

[nm t="勇者" color="#aaddff"]
「……そうか」[l]

[nm t="ナレーション"]
それ以上は聞かなかった。[p]

[nm t="？？？" color="#aaaaaa"]
「……優しいのね、勇者」[l]

[nm t="？？？" color="#aaaaaa"]
「……さっきの話。受けてあげる」[p]

[eval exp="f.surrender_count=f.surrender_count+1"]
[jump target="*downer_accept_exec"]

*downer_accept

[eval exp="f.surrender_count=f.surrender_count+1"]

*downer_accept_exec

[nm t="？？？" color="#aaaaaa"]
「……じゃあ、こっちに来て」[p]

; ====【Hシーン：ダウナー・静かな搾精】====
; [cutin storage="event/downer_h01.jpg"]

[nm t="？？？" color="#aaaaaa"]
「……横に、なって」[l]

[nm t="ナレーション"]
命令ではなく、独り言のような言い方だった。[l]

[nm t="ナレーション"]
隣に座った女性が、ゆっくりと手を伸ばしてくる。感情を込めない動き。しかしその手は——驚くほど丁寧だった。[p]

[nm t="？？？" color="#aaaaaa"]
「……あなた、怖くないの。私のこと」[l]

[nm t="勇者" color="#aaddff"]
「……怖くはない」[l]

[nm t="？？？" color="#aaaaaa"]
「……そう」[p]

[nm t="ナレーション"]
それだけ言って、また沈黙。静かな部屋に、小さな音だけが響く。[l]

[nm t="ナレーション"]
急かすことも、煽ることも、声を荒げることもない。ただ静かに、丁寧に——[l]

[nm t="ナレーション"]
それなのに確実に追い詰めてくる。感情がないように見えて、その手は相手のことをよく見ていた。[p]

[nm t="勇者" color="#aaddff"]
「……っ……あの、もうすぐ……」[l]

[nm t="？？？" color="#aaaaaa"]
「……知ってる」[p]

[nm t="ナレーション"]
静寂の中で、勇者は静かに果てた。[l]

[nm t="？？？" color="#aaaaaa"]
「……ありがとう。久しぶりに、少し温かくなった」[p]
; ==========================================

[nm t="？？？" color="#aaaaaa"]
「……ありがとう。久しぶりに、少し温かくなった」[p]

[call storage="system/init.ks" target="*squeeze_event"]

*downer_clear

[eval exp="f.f4_downer=1"]
[nm t="ナレーション"]
——薄暗い部屋を通り抜けた。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_4f"]
