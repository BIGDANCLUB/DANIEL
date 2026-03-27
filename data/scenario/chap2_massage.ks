;==========================================================
; chap2_massage.ks - 4F「マッサージ師」
;==========================================================
*massage_start

; [bg storage="bg_massage_room.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
扉を開けると、アロマの香りが漂う部屋だった。[l]

[nm t="ナレーション"]
施術台が一つ。手技の達人と思われる女性が振り向いた。[p]

; [chara_show name="massage" storage="chara/massage_normal.png" pos="right" time="500"]

[nm t="マッサージ師" color="#ffddaa"]
「……随分疲れた顔をしているわね」[l]

[nm t="マッサージ師" color="#ffddaa"]
「私はこの城の専属マッサージ師。戦士たちのコンディションを管理しているの」[l]

[nm t="マッサージ師" color="#ffddaa"]
「あなた……施術を受けてみない？ ただし、私のやり方で」[p]

[select text="どう対処する？"
  option="「……少しだけなら」→ 受ける" target="*massage_accept"
  option="「結構だ」→ 断って通る" target="*massage_refuse"
  option="「やり方とは？」→ 確認する" target="*massage_ask"
]

*massage_ask

[nm t="マッサージ師" color="#ffddaa"]
「全身のコンディションを整えるわ。……特に、溜め込んでいる部分を重点的に」[l]

[nm t="マッサージ師" color="#ffddaa"]
「あなた、淫紋の影響で身体が張っているでしょう。解してあげる」[p]

[select text="どうする？"
  option="「……お願いする」" target="*massage_accept"
  option="「断る」" target="*massage_refuse"
]

*massage_refuse

[nm t="マッサージ師" color="#ffddaa"]
「そう。……でも、帰り道に必ずここを通るのよ？ 覚悟しておいて」[l]

[nm t="ナレーション"]
マッサージ師が静かに道を開けた。[p]

[set f.resist_count=f.resist_count+1]
[jump target="*massage_clear"]

*massage_accept

[set f.surrender_count=f.surrender_count+1]

[nm t="マッサージ師" color="#ffddaa"]
「では、横になって。全部任せていいわ」[p]

; ====【Hシーン：マッサージ・手技搾精】====
; (ここにHシーン本文・CG挿入)
; [cutin storage="event/massage_h01.jpg"]
; ==========================================

[nm t="マッサージ師" color="#ffddaa"]
「……施術完了。スッキリしたでしょ？」[p]

; 体力・充填量を整える
[eval exp="f.hp = Math.min(f.hp + 15, 100)"]

[call storage="system/init.ks" target="*squeeze_event"]

*massage_clear

[set f.f4_massage=1]
[nm t="ナレーション"]
——マッサージ室を通り抜けた。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_4f"]
