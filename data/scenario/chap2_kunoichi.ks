;==========================================================
; chap2_kunoichi.ks - 1F「くのいち」
;==========================================================
*kunoichi_start

; [bg storage="bg_central_hall_shadow.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
気配を感じた瞬間、煙幕が炸裂した。[p]

; [se storage="se_smoke_bomb.ogg"]

[nm t="ナレーション"]
煙が晴れると——目の前に黒装束の女が立っていた。[p]

; [chara_show name="kunoichi" storage="chara/kunoichi_normal.png" pos="center" time="300"]

[nm t="くのいち" color="#ff9999"]
「……見つけた。ターゲット確認」[l]

[nm t="くのいち" color="#ff9999"]
「魔王様の命令——勇者を無力化して連れてこい。……でも私、独自のやり方があってね」[p]

どう対処する？[r]
[link target="*kunoichi_escape_smoke"]煙幕を利用して逃げる[endlink][r]
[link target="*kunoichi_fight"]正面から戦う[endlink][r]
[link target="*kunoichi_captured"]（麻痺針を打たれてしまった）[endlink][r]
[s]

*kunoichi_escape_smoke

[nm t="勇者" color="#aaddff"]
「（煙がまだ残っている……今だ）」[l]

[nm t="ナレーション"]
煙の中に飛び込み、反対方向へ走り抜けた。くのいちが追ってくる気配があるが、曲がり角を連続して曲がり、撒くことができた。[p]

[eval exp="f.resist_count=f.resist_count+1"]
[jump target="*kunoichi_clear"]

*kunoichi_fight

[nm t="ナレーション"]
剣を構えると、くのいちも短刀を抜いた。[l]

[nm t="ナレーション"]
素早い攻撃を受け流し、女神の加護を乗せた一撃が炸裂する——！[p]

[nm t="くのいち" color="#ff9999"]
「……！ 速い」[l]

[nm t="ナレーション"]
たたらを踏んだくのいちの脇をすり抜けた。[p]

[eval exp="f.resist_count=f.resist_count+1"]
[jump target="*kunoichi_clear"]

*kunoichi_captured

[nm t="ナレーション"]
気がつくと背後を取られていた。首元に針の感触——麻痺毒だ。[l]

[nm t="ナレーション"]
身体の力が抜けていく。[p]

[nm t="くのいち" color="#ff9999"]
「……おとなしく。任務だからね」[l]

[nm t="くのいち" color="#ff9999"]
「……それに、あなたの匂いは、思ってたより……ずっといい」[p]

; ====【Hシーン：くのいち・麻痺搾精】====
; [cutin storage="event/kunoichi_h01.jpg"]

[nm t="ナレーション"]
麻痺毒は全身の随意筋を封じていた。倒れることも、声を上げることも、できない。ただ感覚だけが残されている。[p]

[nm t="くのいち" color="#ff9999"]
「……感覚は残る。安心して」[l]

[nm t="ナレーション"]
くのいちが無表情のまま、勇者の前にしゃがむ。[l]

[nm t="くのいち" color="#ff9999"]
「……任務は捕獲だけど。あなたの精力の噂は私も聞いていた」[l]

[nm t="くのいち" color="#ff9999"]
「……少し、いただく。それくらいは許してほしい」[p]

[nm t="ナレーション"]
感情のない声。しかし手の動きは——丁寧だった。[l]

[nm t="ナレーション"]
動けない身体の中で、刺激だけが増していく。抵抗も逃げることもできず、ただ感じるしかない。[p]

[nm t="くのいち" color="#ff9999"]
「……もうすぐ」[l]

[nm t="ナレーション"]
静かな部屋に、勇者の押し殺した息遣いだけが響いた。[p]
; ==========================================

[nm t="ナレーション"]
麻痺が切れた頃、くのいちは満足した様子で姿を消していた。[p]

[call storage="system/init.ks" target="*squeeze_event"]

*kunoichi_clear

[eval exp="f.f1_kunoichi=1"]
[nm t="ナレーション"]
——くのいちの追跡を突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_1f"]
