;==========================================================
; chap2_sister.ks - 4F「シスター」
;==========================================================
*sister_start

; [bg storage="bg_chapel.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
居住区の一角に、小さな礼拝堂がある。蝋燭の光が揺れ、静謐な空気が漂っていた。[l]

[nm t="ナレーション"]
修道服の女性が祈りを捧げていた。その手元に——奇妙な魔法書が開かれている。[p]

; [chara_show name="sister" storage="chara/sister_normal.png" pos="center" time="500"]

[nm t="シスター" color="#ddddff"]
「……勇者様？ よくここまで来られました」[l]

[nm t="シスター" color="#ddddff"]
「私は魔族の神に仕える者です。でも……あなたのことは、嫌いではありません」[l]

[nm t="シスター" color="#ddddff"]
「この礼拝堂を通るには、清めの儀式が必要なのです。……私が執り行います」[p]

[select text="どう対処する？"
  option="「儀式とは何をするのか」→ 聞く" target="*sister_ask"
  option="「儀式は結構」→ 強引に通り抜ける" target="*sister_force"
  option="「わかりました」→ 儀式を受ける" target="*sister_accept"
]

*sister_ask

[nm t="シスター" color="#ddddff"]
「……精を奉納していただきます。神への供物として」[l]

[nm t="シスター" color="#ddddff"]
「女神の加護を受けた勇者様の精は……この上ない供物になります」[p]

[select text="どうする？"
  option="「……わかった、受けよう」" target="*sister_accept"
  option="「信仰は違っても、神への供物は断る」" target="*sister_force"
]

*sister_force

[nm t="ナレーション"]
強引に礼拝堂を通り抜けようとした。[l]

[nm t="ナレーション"]
シスターが呪文を唱え始める——しかし女神の加護が呪いを弾いた。[p]

[nm t="シスター" color="#ddddff"]
「……さすが、女神の勇者様」[l]

[nm t="ナレーション"]
シスターが静かに道を開ける。[p]

[eval exp="f.resist_count=f.resist_count+1"]
[jump target="*sister_clear"]

*sister_accept

[eval exp="f.surrender_count=f.surrender_count+1"]

[nm t="シスター" color="#ddddff"]
「では……神のお名前のもとに、儀式を始めます」[p]

; ====【Hシーン：シスター・儀式的搾精】====
; [cutin storage="event/sister_h01.jpg"]

[nm t="シスター" color="#ddddff"]
「……祈りの中で行います。お声は出しても構いません。神は全てをお聞きになっています」[p]

[nm t="ナレーション"]
蝋燭の灯り。静寂。シスターが目を閉じ、低く祈りを唱え始めた。[p]

[nm t="ナレーション"]
その手が、祈りの言葉と共に触れてくる。神聖な場所で、神聖な行為として捧げられる——なのに、身体は確かに反応していた。[p]

[nm t="シスター" color="#ddddff"]
「……緊張しなくて大丈夫です。これは神への奉仕。あなたは何も恥じることはない」[l]

[nm t="勇者" color="#aaddff"]
「……いや、でも……」[l]

[nm t="シスター" color="#ddddff"]
「神の御名のもとに、全てを受け入れなさい」[p]

[nm t="ナレーション"]
静かな声で命じられると、抗えなかった。礼拝堂の神聖な空気と、シスターの慈しむような手つき——相反する要素が混ざり合い、独特の陶酔感が生まれる。[p]

[nm t="勇者" color="#aaddff"]
「……っ……すみません……」[l]

[nm t="シスター" color="#ddddff"]
「謝らないで。これが神の御意志です……」[p]

[nm t="ナレーション"]
祈りの言葉が続く中、勇者は静かに限界を迎えた。[p]
; ==========================================

[nm t="シスター" color="#ddddff"]
「……供物、確かに受け取りました。道をお通りください」[l]

[nm t="シスター" color="#ddddff"]
「……どうか、ご無事で」[p]

[call storage="system/init.ks" target="*squeeze_event"]

*sister_clear

[eval exp="f.f4_sister=1"]
[nm t="ナレーション"]
——礼拝堂を通り抜けた。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_4f"]
