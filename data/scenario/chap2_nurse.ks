;==========================================================
; chap2_nurse.ks - 3F「ナース」
;==========================================================
*nurse_start

; [bg storage="bg_infirmary.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
魔王城の医務室らしき部屋。白い内装に医療器具が整然と並んでいる。[l]

[nm t="ナレーション"]
白衣に看護帽の女性が、こちらを振り向いた。[p]

; [chara_show name="nurse" storage="chara/nurse_normal.png" pos="right" time="500"]

[nm t="ナース" color="#ffffff"]
「あら——怪我をしているの？ ここは医務室よ」[l]

[nm t="ナース" color="#ffffff"]
「座って。診てあげる」[p]

[nm t="勇者" color="#aaddff"]
「（罠かもしれないが……確かに疲弊している）」[p]

[select text="どう対処する？"
  option="「ありがとう」→ 診てもらう" target="*nurse_accept"
  option="「大丈夫だ」→ 断って通る" target="*nurse_refuse"
  option="「……少し休ませてほしい」" target="*nurse_rest"
]

*nurse_refuse

[nm t="ナース" color="#ffffff"]
「そう……でも、顔色が悪いわよ」[l]

[nm t="ナレーション"]
ナースが道を開けた。通り過ぎようとした——その時、注射器が光った。[p]

[nm t="ナース" color="#ffffff"]
「ちょっとだけ、採血させてもらうわね」[p]

[jump target="*nurse_captured"]

*nurse_rest

[nm t="ナース" color="#ffffff"]
「ベッドで休んで。私が様子を見ているから」[p]

[nm t="ナレーション"]
ベッドに横になった。疲れが出て、すぐに眠くなってくる。[l]

[nm t="ナレーション"]
うとうとしていると——柔らかい感触が。[p]

[jump target="*nurse_captured"]

*nurse_accept

[nm t="ナース" color="#ffffff"]
「傷は大したことないわ。でも……疲労が溜まっているわね」[l]

[nm t="ナース" color="#ffffff"]
「特別な治療をしてあげる。この城の医療は少し……独特なの」[p]

[jump target="*nurse_captured"]

*nurse_captured

; ====【Hシーン：ナース・医療的搾精】====
; [cutin storage="event/nurse_h01.jpg"]

[nm t="ナース" color="#ffffff"]
「では治療を始めますね。……力を抜いて、リラックスしてください」[p]

[nm t="ナレーション"]
柔らかい声。施術台の上、ナースが慣れた手つきで始める。[l]

[nm t="ナース" color="#ffffff"]
「淫紋の影響で、こちらに力が溜まっていますね。解消しないと身体によくないんです」[l]

[nm t="勇者" color="#aaddff"]
「……そういう医療なのか、ここは」[l]

[nm t="ナース" color="#ffffff"]
「魔族の医療は、人間のものとは少し違うんです。でも効果は保証します」[p]

[nm t="ナレーション"]
ナースの手が、プロフェッショナルの動きで触れてくる。[l]

[nm t="ナレーション"]
「治療」としての冷静さがあるはずなのに——勇者の身体は正直に反応していく。[p]

[nm t="ナース" color="#ffffff"]
「……反応が出てきましたね。いい傾向です」[l]

[nm t="ナース" color="#ffffff"]
「このまま、自然に任せてください。……無理に我慢しなくていいですよ」[p]

[nm t="勇者" color="#aaddff"]
「……我慢、できない……」[l]

[nm t="ナース" color="#ffffff"]
「それで大丈夫です。……はい、そのまま——」[p]

[nm t="ナレーション"]
白衣の清潔な香りの中、勇者は「治療」を完了した。[p]
; ==========================================

[nm t="ナース" color="#ffffff"]
「……お疲れ様。体力も回復したはずよ」[l]

; HP回復ボーナス
[eval exp="f.hp = Math.min(f.hp + 20, 100)"]

[nm t="ナース" color="#ffffff"]
「また具合が悪くなったら来てね」[p]

[call storage="system/init.ks" target="*squeeze_event"]

*nurse_clear

[eval exp="f.f3_nurse=1"]
[nm t="ナレーション"]
——医務室を突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_3f"]
