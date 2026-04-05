;==========================================================
; chap2_slime.ks - 地下水路「スライムの巣」
; バトルシステム対応版: 5択、2ミスでHシーン
;==========================================================
*slime_start

[eval exp="f.enemy_mistakes=0"]
[eval exp="f.enemy_last_mistake=0"]

[fadein time="800"]

[nm t="ナレーション"]
地下水路。水が滴る薄暗いトンネルを進む。足元が濡れており、滑りやすい。[p]

[nm t="ナレーション"]
その時——壁際に張り付いていた半透明の塊が、ぶるりと動いた。[p]

[nm t="スライム"]
「……ぷるぷる」[l]

[nm t="ナレーション"]
大柄なスライム。半透明の身体の中に、おぼろげながら女性的なシルエットが見える。鼻に甘い匂いが漂ってきた——淫紋が反応する気がする。[p]

[nm t="スライム"]
「……いいにおい。ぷるぷる……勇者のにおい。メシ……いっぱい」[p]

;==========================================================
; 選択肢1: 接近への対応
;==========================================================
*slime_c1_prompt

[nm t="ナレーション"]
スライムがじわじわとこちらへ迫ってくる。どう対応する？[p]

どうする？[r]
[link target="*slime_c1_safe"]剣を向けて牽制しながら間合いを取る[endlink][r]
[link target="*slime_c1_wrong"]珍しいので少し観察してみる[endlink][r]
[s]

*slime_c1_safe
[nm t="ナレーション"]
剣を構え、スライムとの距離を保つ。スライムは動きが読みやすい——少し観察すれば突破口が見える。[p]
[jump target="*slime_c2_prompt"]

*slime_c1_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=1"]
[nm t="ナレーション"]
観察しようとした瞬間、スライムが一気に距離を詰めてきた。思わず後退するが、背中が壁に当たる。[p]
[nm t="スライム"]
「……ぷるぷる。におい、強い」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*slime_h_dispatch"]
[endif]
[nm t="ナレーション"]
かろうじて壁を蹴って横に逃げる。一瞬、スライムの粘体が腕に触れた——ぬるりとした感触が残る。[p]
[jump target="*slime_c2_prompt"]

;==========================================================
; 選択肢2: 物理攻撃
;==========================================================
*slime_c2_prompt

[nm t="ナレーション"]
スライムが再び動き始めた。物理攻撃は効かないとわかっている。どうする？[p]

どうする？[r]
[link target="*slime_c2_safe"]女神の加護の光を手に集めて押し返す[endlink][r]
[link target="*slime_c2_wrong"]とにかく剣で切り裂いてみる[endlink][r]
[s]

*slime_c2_safe
[nm t="ナレーション"]
手に加護の光を集めると、スライムが怯んで後退した。効いている。[p]
[jump target="*slime_c3_prompt"]

*slime_c2_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=2"]
[nm t="ナレーション"]
剣を振るが、スライムの身体を通り抜けるだけだ。そして引き抜こうとした瞬間、腕ごと絡め取られた。[p]
[nm t="スライム"]
「……剣、いらない。ぷるぷる」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*slime_h_dispatch"]
[endif]
[nm t="ナレーション"]
剣を捨てて腕を引き抜く。スライムの粘液が腕に絡みついたまま、じわじわと広がってくる。[p]
[jump target="*slime_c3_prompt"]

;==========================================================
; 選択肢3: 体温上昇への対応
;==========================================================
*slime_c3_prompt

[nm t="ナレーション"]
スライムの体温が伝わってきてか、全身が妙に火照ってきた。淫紋が反応しているのかもしれない。どうする？[p]

どうする？[r]
[link target="*slime_c3_safe"]精神を集中させて加護に意識を向ける[endlink][r]
[link target="*slime_c2_wrong2"]……心地よい。少し身体の感覚に従ってみる[endlink][r]
[s]

*slime_c3_safe
[nm t="ナレーション"]
深呼吸して加護に集中する。火照りが引いていく。スライムが不満そうに揺れた。[p]
[jump target="*slime_c4_prompt"]

*slime_c2_wrong2
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=3"]
[nm t="ナレーション"]
身体の感覚に従った瞬間、スライムが一気に絡みついてきた。温かく、柔らかく——抵抗しようとしても力が入らない。[p]
[nm t="スライム"]
「……やわらかくなった。ぷるぷる……もっと」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*slime_h_dispatch"]
[endif]
[nm t="ナレーション"]
はっと我に返り、必死に引き剥がす。身体は熱いままだが、意識だけは取り戻した。[p]
[jump target="*slime_c4_prompt"]

;==========================================================
; 選択肢4: 局所への集中攻撃への対応
;==========================================================
*slime_c4_prompt

[nm t="ナレーション"]
スライムの突起が集中し始めた——股間の方向に。淫紋の熱が高まる。どうする？[p]

どうする？[r]
[link target="*slime_c4_safe"]女神の力を全身に流してスライムを弾く[endlink][r]
[link target="*slime_c4_wrong"]……動けない。抵抗しようとするが力が入らない[endlink][r]
[s]

*slime_c4_safe
[nm t="ナレーション"]
加護の力を下腹部に集中させると、スライムの突起が弾かれた。スライムが苦しそうに後退する。[p]
[jump target="*slime_c5_prompt"]

*slime_c4_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=4"]
[nm t="ナレーション"]
スライムの突起が服を押しのけ、直接肌へ到達する。淫紋が激しく反応し、視界が白む。[p]
[nm t="スライム"]
「……みつけた。ここ、いちばん。ぷるぷる」[l]
[if exp="f.enemy_mistakes>=2"]
[jump target="*slime_h_dispatch"]
[endif]
[nm t="ナレーション"]
女神の声が遠くで聞こえる気がした。その声を頼りに意識を繋ぎ止め、かろうじて引き剥がす。[p]
[jump target="*slime_c5_prompt"]

;==========================================================
; 選択肢5: 最後の脱出
;==========================================================
*slime_c5_prompt

[nm t="ナレーション"]
スライムが最後の力で全体で包み込もうとしてくる。最後のチャンスだ。[p]

どうする？[r]
[link target="*slime_c5_safe"]加護を爆発的に解放して一気に突き抜ける[endlink][r]
[link target="*slime_c5_wrong"]……もう力が残っていない[endlink][r]
[s]

*slime_c5_safe
[nm t="ナレーション"]
全身に加護の光を溢れさせ、スライムを強引に押し退けた。弾けるような感覚と共に、通路の先へ抜け出す。[p]
[jump target="*slime_win"]

*slime_c5_wrong
[eval exp="f.enemy_mistakes+=1"]
[eval exp="f.enemy_last_mistake=5"]
[jump target="*slime_h_dispatch"]

;==========================================================
; Hシーン振り分け
;==========================================================
*slime_h_dispatch
[if exp="f.enemy_last_mistake==1"]
[jump target="*slime_h1"]
[endif]
[if exp="f.enemy_last_mistake==2"]
[jump target="*slime_h2"]
[endif]
[if exp="f.enemy_last_mistake==3"]
[jump target="*slime_h3"]
[endif]
[if exp="f.enemy_last_mistake==4"]
[jump target="*slime_h4"]
[endif]
[jump target="*slime_h5"]

;==========================================================
; Hシーン①: 観察中に捕まる（全身包み込み）
;==========================================================
*slime_h1
[eval exp="f.scene_slime_h1=1"]

; ========== CG・BGM挿入箇所 ==========
; [bgm_on f="h_scene"]              ← Hシーン用BGMに切り替え
; [cg f="slime_h1_01"]              ← CG①（最初）
; =====================================

[nm t="ナレーション"]
スライムの身体が勇者の全身を包み込む。ゼリー状の内側は驚くほど温かく、全身をやさしく圧迫する。[l]

[nm t="スライム"]
「……ぷるぷる。やわらかい。いいにおい」[l]

; [cg f="slime_h1_02"]              ← CG②

[nm t="ナレーション"]
密着する感触が全身を這い回る。特に淫紋のある部分へと、無数の細かい突起が集まってくる。本能だけで動くスライムは、一番価値のある場所を正確に知っていた。[p]

[nm t="勇者" color="#aaddff"]
「っ……やめ……！ そんな、全身……」[l]

; [cg f="slime_h1_03"]              ← CG③（必要なら下に ④⑤... と追加可）

[nm t="スライム"]
「……でてきた。あまい。おいしい」[p]

[nm t="ナレーション"]
身体が強張り、やがて力が完全に抜けていく。全身がスライムに優しく揺すられ、蜜が絞り出されていく感覚——抵抗できない。[p]

[call storage="system/init.ks" target="*squeeze_event"]

[nm t="女神" color="#ffffaa"]
「……大丈夫？ スライムは満足したみたい。今のうちに」[p]

[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

;==========================================================
; Hシーン②: 剣を捕られて腕から広がる
;==========================================================
*slime_h2
[eval exp="f.scene_slime_h2=1"]

[nm t="ナレーション"]
スライムが腕から全身へと広がっていく。関節の隙間、鎧の隙間——どこにでも入り込んでくる。[l]

[nm t="スライム"]
「……腕から、ぜんぶ。つながってる」[l]

[nm t="ナレーション"]
温かい粘体が肌の上を流れ、服の裏側まで侵食してくる。抵抗しようにも、全身が均一な圧力で固定されている。剣を失った今、これを払う手段がない。[p]

[nm t="勇者" color="#aaddff"]
「離せ……! 腕が……全身が……!」[l]

[nm t="スライム"]
「……いっぱいある。ぜんぶ、もらう」[p]

[nm t="ナレーション"]
少しずつ、全身の感覚が甘く鈍くなっていく。淫紋が熱を持ち、スライムの動きに合わせて快感が増幅される。[p]

[call storage="system/init.ks" target="*squeeze_event"]

[nm t="ナレーション"]
やがてスライムは満足し、静かに退いていった。[p]

[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

;==========================================================
; Hシーン③: 感度上昇状態での搾精
;==========================================================
*slime_h3
[eval exp="f.scene_slime_h3=1"]

[nm t="ナレーション"]
身体の感覚に従った瞬間、スライムが全力で覆いかぶさってきた。火照った身体に温かい粘体が密着し——感度が通常の何倍にも増している。[p]

[nm t="スライム"]
「……やわらかい。においも、もっと濃い」[l]

[nm t="勇者" color="#aaddff"]
「あ……っ、まずい、これ……感覚が……」[l]

[nm t="ナレーション"]
淫紋の影響で高まった感度のせいで、わずかな刺激でも全身が震える。スライムの無数の突起がその感度を余すところなく利用し、あっという間に限界へと追い込んでいく。[p]

[nm t="勇者" color="#aaddff"]
「……っ、く、やだ……もう……ッ」[p]

[call storage="system/init.ks" target="*squeeze_event"]

[nm t="ナレーション"]
身体から力が完全に抜けた。スライムがゆっくりと離れ、満足気に揺れている。[p]

[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

;==========================================================
; Hシーン④: 局所集中責め
;==========================================================
*slime_h4
[eval exp="f.scene_slime_h4=1"]

[nm t="ナレーション"]
スライムの突起が一点に集中する。精密な動きで、淫紋の熱を最大限に引き出していく。[l]

[nm t="スライム"]
「……ここだけ。ぜんぶここから。ぷるぷる」[p]

[nm t="ナレーション"]
身体の他の部分はほぼ自由なのに、その一点だけを集中的に攻められ続ける。逃げられない。スライムの粘体が足首と手首を床に固定している。[l]

[nm t="勇者" color="#aaddff"]
「……っ、やめ……そこだけ……そこだけはっ……」[l]

[nm t="ナレーション"]
限界まで追い詰められ、全身を震わせながら——解放された。[p]

[call storage="system/init.ks" target="*squeeze_event"]

[nm t="スライム"]
「……たくさん。おいしい。またくる」[p]

[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

;==========================================================
; Hシーン⑤: 完全消耗・長時間搾精
;==========================================================
*slime_h5
[eval exp="f.scene_slime_h5=1"]

[nm t="ナレーション"]
すべての力が尽きた。スライムが全身を包み込み、ゆっくり、念入りに——時間をかけて搾り取っていく。[p]

[nm t="スライム"]
「……いっぱい。ずっと、ずっと。いっぱいある」[l]

[nm t="ナレーション"]
もう抵抗できない。スライムの温かい包容に身を委ねるしかない。全身が蕩けるように甘い感覚に包まれ、何度も、何度も——。[p]

[nm t="勇者" color="#aaddff"]
「……もう……もう……ッ」[l]

[nm t="ナレーション"]
どれほど時間が経っただろうか。スライムがようやく満足し、ゆっくりと離れた。全身の力が完全に抜け、床に崩れ落ちた。[p]

[nm t="女神" color="#ffffaa"]
「……無事？ 今行く——待って」[p]

[call storage="system/init.ks" target="*squeeze_event"]

[if exp="f.from_recall==1"]
[eval exp="f.from_recall=0"]
[jump storage="recollection_room.ks" target="*recollection_start"]
[endif]
[jump storage="chap2_explore.ks" target="*hub_b1f"]

;==========================================================
; 勝利
;==========================================================
*slime_win
[eval exp="f.b1f_slime=1"]

[nm t="ナレーション"]
加護の光がスライムを押し退けた。スライムが苦しそうに身体を縮ませ、通路の隅に退いていく。[p]

[nm t="勇者" color="#aaddff"]
「……やった。物理は無効でも、加護の光は効く」[p]

[nm t="ナレーション"]
地下水路を抜け、魔王城の内部通路へと戻る。——地下水路を突破した。[p]

[fadeout time="800" color="0x000000"]
[wait time=300]
[jump storage="chap2_explore.ks" target="*hub_b1f"]
