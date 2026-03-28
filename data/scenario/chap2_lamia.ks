;==========================================================
; chap2_lamia.ks - 2F「ラミア」
;==========================================================
*lamia_start

; [bg storage="bg_upper_corridor_lamia.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
上層回廊の一角。床に大きな鱗の跡がある。[l]

[nm t="ナレーション"]
天井から、するりと長い身体が降りてきた——上半身は女性、下半身は巨大な蛇のラミアだ。[p]

; [chara_show name="lamia" storage="chara/lamia_normal.png" pos="center" time="500"]

[nm t="ラミア" color="#88ff88"]
「……迷い込んだの？ 可哀想に」[l]

[nm t="ラミア" color="#88ff88"]
「でもちょうどよかった。あなた、いい匂いがするわ」[l]

[nm t="ラミア" color="#88ff88"]
「私の目を見て……ほら、楽になるわよ？」[p]

[nm t="ナレーション"]
ラミアの瞳が渦を巻くように光る——催眠だ！[p]

[select text="どう対処する？"
  option="目を逸らして女神に祈る" target="*lamia_avert"
  option="（目を見てしまった……）" target="*lamia_hypno"
  option="剣を投げて注意を引き、逃げる" target="*lamia_distract"
]

*lamia_avert

[nm t="勇者" color="#aaddff"]
「（見るな……女神様、力を！）」[l]

[nm t="ナレーション"]
女神の加護が金色の光で目を守る。ラミアの催眠が弾かれた。[p]

[nm t="ラミア" color="#88ff88"]
「……！ 女神の加護を持っているの」[l]

[nm t="ナレーション"]
怯んだ隙に走り抜けた。[p]

[eval exp="f.resist_count=f.resist_count+1"]
[jump target="*lamia_clear"]

*lamia_distract

[nm t="ナレーション"]
剣を遠くに投げつけた——ラミアが音に反応して視線を逸らす。[l]

[nm t="ナレーション"]
その瞬間、横を全力で駆け抜けた。[p]

[nm t="ラミア" color="#88ff88"]
「あ、逃げた……」[l]

[eval exp="f.resist_count=f.resist_count+1"]
[jump target="*lamia_clear"]

*lamia_hypno

[nm t="ナレーション"]
ラミアの瞳に引き込まれた。意識がぼんやりとする……[l]

[nm t="ラミア" color="#88ff88"]
「いい子ね……おいで」[l]

[nm t="ナレーション"]
ラミアの尾が身体に巻きついてきた。拘束される。でも——なぜか怖くない。[p]

; ====【Hシーン：ラミア・催眠拘束搾精】====
; [cutin storage="event/lamia_h01.jpg"]

[nm t="ナレーション"]
意識はある。だが身体が言うことを聞かない——催眠に落ちた身体は、ラミアの誘導通りに動く。[p]

[nm t="ラミア" color="#88ff88"]
「怖くないわよ……ほら、楽になって。気持ちよくしてあげる」[l]

[nm t="ナレーション"]
ラミアの長い尾が、勇者の身体にゆっくりと絡みついてくる。蛇の鱗は思ったより滑らかで、締め付けはごく穏やかだった。[p]

[nm t="ナレーション"]
催眠の効果で、触れられるだけで快感が増幅される。ラミアはそれを知っていて、わざとゆっくりと動いていた。[p]

[nm t="勇者" color="#aaddff"]
「……あ……これ……だめだ……」[l]

[nm t="ラミア" color="#88ff88"]
「うふふ……素直な反応。可愛い」[l]

[nm t="ナレーション"]
尾の締め付けが、リズムを刻む。そのたびに意識が遠のきそうになる——しかしラミアは絶頂の直前で止めた。[p]

[nm t="ラミア" color="#88ff88"]
「……もっと欲しい？ お願いしてみて」[p]

[nm t="勇者" color="#aaddff"]
「……た、頼む……」[l]

[nm t="ラミア" color="#88ff88"]
「いい子♪」[p]

[nm t="ナレーション"]
尾が再び動き始め——今度は、止まらなかった。[p]
; ==========================================

[nm t="ナレーション"]
しばらくして意識が戻ると、ラミアは満足そうに尾を緩めていた。[p]

[call storage="system/init.ks" target="*squeeze_event"]

*lamia_clear

[eval exp="f.f2_lamia=1"]
[nm t="ナレーション"]
——ラミアの回廊を突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_2f"]
