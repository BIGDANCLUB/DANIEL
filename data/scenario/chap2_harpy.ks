;==========================================================
; chap2_harpy.ks - 2F「ハーピー」
;==========================================================
*harpy_start

; [bg storage="bg_upper_corridor_sky.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
吹き抜けになった廊下の上空から、甲高い鳴き声が聞こえた。[l]

[nm t="ナレーション"]
翼を広げた女性が急降下してくる——ハーピーだ。[p]

; [chara_show name="harpy" storage="chara/harpy_normal.png" pos="center" time="300"]

[nm t="ハーピー" color="#ffdd88"]
「キャー！ 珍しい！ 勇者？」[l]

[nm t="ハーピー" color="#ffdd88"]
「匂い嗅がせて！ いい匂い！ 欲しい！ 欲しい！」[p]

[nm t="ナレーション"]
興奮気味のハーピーが旋回しながら迫ってくる。[p]

[select text="どう対処する？"
  option="上空へ向けて女神の光を放つ" target="*harpy_light"
  option="食べ物を囮にして誘導する" target="*harpy_lure"
  option="（翼で押さえ込まれた）" target="*harpy_captured"
]

*harpy_light

[nm t="ナレーション"]
上空へ向けて女神の光を収束——ハーピーが光を嫌がり上昇した！[l]

[nm t="ナレーション"]
その隙に廊下を駆け抜けた。[p]

[set f.resist_count=f.resist_count+1]
[jump target="*harpy_clear"]

*harpy_lure

[nm t="ナレーション"]
ポーチの中の携帯食を取り出し、廊下の反対方向に投げた。[l]

[nm t="ハーピー" color="#ffdd88"]
「食べ物！」[l]

[nm t="ナレーション"]
ハーピーが食べ物に飛びついた隙に通り過ぎた。[p]

[set f.resist_count=f.resist_count+1]
[jump target="*harpy_clear"]

*harpy_captured

[nm t="ナレーション"]
翼が両腕を押さえつけた。驚くほど力が強い。[p]

[nm t="ハーピー" color="#ffdd88"]
「捕まえた！ やったー！ 絶対離さない！」[p]

; ====【Hシーン：ハーピー・強引搾精】====
; [cutin storage="event/harpy_h01.jpg"]

[nm t="ハーピー" color="#ffdd88"]
「やった！ 捕まえた！ これが勇者の匂いね！ すごい！」[p]

[nm t="ナレーション"]
ハーピーの興奮は本物だった。翼で両腕を押さえつけたまま、羽毛の柔らかさで全身を包み込んでくる。[p]

[nm t="ナレーション"]
翼の羽毛は驚くほど細かく、素肌に触れるとくすぐったいのか気持ちいいのか判断がつかない感触をもたらした。[p]

[nm t="ハーピー" color="#ffdd88"]
「なんでもっと早く来てくれなかったの！ ずっと待ってたのに！」[l]

[nm t="勇者" color="#aaddff"]
「待ってたって……今日初めて会ったろう」[l]

[nm t="ハーピー" color="#ffdd88"]
「細かいことはいい！ それよりここが一番いい匂い！ もっとくれ！」[p]

[nm t="ナレーション"]
無邪気で、悪意がない。それがかえって、抵抗の気持ちを萎えさせた。[l]

[nm t="ナレーション"]
ハーピーは無我夢中で——しかしその本能的な動きは、的確に急所を外さなかった。[p]

[nm t="勇者" color="#aaddff"]
「……っ、ちょっ……待って……！」[l]

[nm t="ハーピー" color="#ffdd88"]
「待たない！ もうちょっと！ もうちょっとだから！」[p]

[nm t="ナレーション"]
まくし立てられながら、あっという間に限界を迎えた。[p]
; ==========================================

[nm t="ナレーション"]
ハーピーがようやく満足して翼を緩めた。[p]

[call storage="system/init.ks" target="*squeeze_event"]

*harpy_clear

[set f.f2_harpy=1]
[nm t="ナレーション"]
——ハーピーを突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_2f"]
