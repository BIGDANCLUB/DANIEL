;==========================================================
; chap2_prostitute.ks - 4F「娼婦」
;==========================================================
*prostitute_start

; [bg storage="bg_tavern_room.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
居住区の一室——酒の匂いと、妖艶な雰囲気が漂う部屋だった。[l]

[nm t="ナレーション"]
豪華な服をまとった女性が、こちらを見て微笑んだ。[p]

; [chara_show name="prostitute" storage="chara/prostitute_normal.png" pos="right" time="500"]

[nm t="娼婦" color="#ffaadd"]
「あら、珍しいお客様ね。勇者様だって？」[l]

[nm t="娼婦" color="#ffaadd"]
「うふふ……噂は聞いているわよ。城中の子たちがあなたの匂いで大騒ぎ」[l]

[nm t="娼婦" color="#ffaadd"]
「私はプロよ。他の子みたいに無理やりじゃなく……気持ちよく、ゆっくりお相手するわ」[p]

[select text="どう対処する？"
  option="「……お願いする」→ サービスを受ける" target="*prostitute_accept"
  option="「急いでいる、通してくれ」→ 断る" target="*prostitute_refuse"
  option="「あなたはなぜここで働いているのか」→ 話を聞く" target="*prostitute_talk"
]

*prostitute_refuse

[nm t="娼婦" color="#ffaadd"]
「……そう。残念だわ」[l]

[nm t="ナレーション"]
娼婦は名残惜しそうにしながらも、静かに道を開けた。[p]

[eval exp="f.resist_count=f.resist_count+1"]
[jump target="*prostitute_clear"]

*prostitute_talk

[nm t="娼婦" color="#ffaadd"]
「……珍しいことを聞くのね」[l]

[nm t="娼婦" color="#ffaadd"]
「別に不満はないわよ。ここの待遇はいいし、魔王様は優しいし」[l]

[nm t="娼婦" color="#ffaadd"]
「ただ……最近、この戦争が長引いているのは嫌ね。平和な方がいいに決まってる」[p]

[nm t="勇者" color="#aaddff"]
「……そうか」[l]

[nm t="娼婦" color="#ffaadd"]
「あなた、本当に魔王様を止めに来たの？ なら……応援するわ。私なりの方法で」[p]

[eval exp="f.surrender_count=f.surrender_count+1"]

*prostitute_accept

; ====【Hシーン：娼婦・プロの手搾精】====
; [cutin storage="event/prostitute_h01.jpg"]

[nm t="娼婦" color="#ffaadd"]
「……緊張してる？ 大丈夫よ、ゆっくりしていって」[p]

[nm t="ナレーション"]
娼婦が慣れた様子でそっと寄り添ってくる。強引さがない。むしろ、相手が心地よくなるよう空気を作るのが上手かった。[p]

[nm t="娼婦" color="#ffaadd"]
「……本当にいい匂いね。噂に違わず」[l]

[nm t="ナレーション"]
その声も、仕草も、計算されているはずなのに——不思議と安心感があった。[l]

[nm t="娼婦" color="#ffaadd"]
「嫌なことがあったら言って。私はあなたに気持ちよくなってほしいの」[p]

[nm t="ナレーション"]
その言葉を信じてしまう自分がいた。[l]

[nm t="ナレーション"]
娼婦の手は、急かさない。焦らさない。でも確実に、じわじわと追い詰めてくる。プロの技術が随所に光る。[p]

[nm t="勇者" color="#aaddff"]
「……あなた、本当に上手いな……」[l]

[nm t="娼婦" color="#ffaadd"]
「うふふ、ありがとう。……もうすぐよ？」[p]

[nm t="ナレーション"]
教えてくれる優しさに、かえって羞恥心が増した。[l]

[nm t="ナレーション"]
しかし身体はその優しさの中で、素直に限界を迎えた。[p]
; ==========================================

[nm t="娼婦" color="#ffaadd"]
「……どう？ 私のサービス、悪くなかったでしょ」[l]

[nm t="娼婦" color="#ffaadd"]
「頑張ってね、勇者様。……応援してるわ」[p]

[call storage="system/init.ks" target="*squeeze_event"]

*prostitute_clear

[eval exp="f.f4_prostitute=1"]
[nm t="ナレーション"]
——娼婦の部屋を通り抜けた。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_4f"]
