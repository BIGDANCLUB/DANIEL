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

どう対処する？[r]
[link target="*massage_accept"]「……少しだけなら」→ 受ける[endlink][r]
[link target="*massage_refuse"]「結構だ」→ 断って通る[endlink][r]
[link target="*massage_ask"]「やり方とは？」→ 確認する[endlink][r]
[s]

*massage_ask

[nm t="マッサージ師" color="#ffddaa"]
「全身のコンディションを整えるわ。……特に、溜め込んでいる部分を重点的に」[l]

[nm t="マッサージ師" color="#ffddaa"]
「あなた、淫紋の影響で身体が張っているでしょう。解してあげる」[p]

どうする？[r]
[link target="*massage_accept"]「……お願いする」[endlink][r]
[link target="*massage_refuse"]「断る」[endlink][r]
[s]

*massage_refuse

[nm t="マッサージ師" color="#ffddaa"]
「そう。……でも、帰り道に必ずここを通るのよ？ 覚悟しておいて」[l]

[nm t="ナレーション"]
マッサージ師が静かに道を開けた。[p]

[eval exp="f.resist_count=f.resist_count+1"]
[jump target="*massage_clear"]

*massage_accept

[eval exp="f.surrender_count=f.surrender_count+1"]

[nm t="マッサージ師" color="#ffddaa"]
「では、横になって。全部任せていいわ」[p]

; ====【Hシーン：マッサージ・手技搾精】====
; [cutin storage="event/massage_h01.jpg"]

[nm t="マッサージ師" color="#ffddaa"]
「……うつ伏せになって。まず全体を解してから」[p]

[nm t="ナレーション"]
施術台に横になると、オイルの滑らかな感触が背中に広がった。[l]

[nm t="ナレーション"]
マッサージ師の手は確かだった。筋肉のどこが張っているかを指先で読み取り、ピンポイントで圧をかける。[p]

[nm t="マッサージ師" color="#ffddaa"]
「……随分疲れているわね。ここ、凝り固まってる」[l]

[nm t="ナレーション"]
押されるたびに、身体の奥から力が抜けていく感覚。[l]

[nm t="マッサージ師" color="#ffddaa"]
「では仰向けになって。次は……こちらを解消しましょうか」[p]

[nm t="ナレーション"]
その言い方は穏やかだったが、向かう場所は明確だった。[l]

[nm t="勇者" color="#aaddff"]
「……あの、それは——」[l]

[nm t="マッサージ師" color="#ffddaa"]
「溜め込んでいると身体によくないの。任せて」[p]

[nm t="ナレーション"]
プロの技術は、こういう場所にも遺憾なく発揮された。[l]

[nm t="ナレーション"]
弛緩した身体に、じわじわと快感が積み上がっていく。抵抗するような筋肉はすでに解されていた。[p]

[nm t="マッサージ師" color="#ffddaa"]
「……もう少し。ほら、力を抜いて——」[p]

[nm t="ナレーション"]
ため息のように、静かに限界が来た。[p]
; ==========================================

[nm t="マッサージ師" color="#ffddaa"]
「……施術完了。スッキリしたでしょ？」[p]

; 体力・充填量を整える
[eval exp="f.hp = Math.min(f.hp + 15, 100)"]

[call storage="system/init.ks" target="*squeeze_event"]

*massage_clear

[eval exp="f.f4_massage=1"]
[nm t="ナレーション"]
——マッサージ室を通り抜けた。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_4f"]
