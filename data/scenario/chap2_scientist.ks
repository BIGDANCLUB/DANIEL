;==========================================================
; chap2_scientist.ks - 3F「科学者」
;==========================================================
*scientist_start

; [bg storage="bg_laboratory.jpg" time="500"]

[fadein time="800"]

[nm t="ナレーション"]
研究棟の実験室。様々な機械と薬品が並んでいる。[l]

[nm t="ナレーション"]
白衣の女性が顕微鏡を覗いていた——魔法と科学を組み合わせた研究者のようだ。[p]

; [chara_show name="scientist" storage="chara/scientist_normal.png" pos="left" time="500"]

[nm t="科学者" color="#aaffff"]
「あら……不法侵入者ね。でも丁度いいかも」[l]

[nm t="科学者" color="#aaffff"]
「女神の加護を持つ生体サンプル——長年欲しかったの。採取させてもらうわよ」[p]

[nm t="勇者" color="#aaddff"]
「……採取？」[p]

[nm t="科学者" color="#aaffff"]
「精液よ。魔法的に非常に希少なサンプルなの。論文が書けるわ」[l]

[nm t="科学者" color="#aaffff"]
「安心して。痛くしないから。科学的に、効率よく」[p]

どう対処する？[r]
[link target="*scientist_escape"]「絶対に嫌だ」→ 逃げる[endlink][r]
[link target="*scientist_talk"]「……研究の内容を教えてくれ」→ 話を聞く[endlink][r]
[link target="*scientist_offer"]「（まあ、科学の発展のためなら）」→ 同意[endlink][r]
[s]

*scientist_escape

[nm t="ナレーション"]
踵を返して走り出した。科学者が「待って！」と叫ぶが、追いつける速さではない。[l]

[nm t="ナレーション"]
実験器具を蹴散らしながら出口へ。[p]

[eval exp="f.resist_count=f.resist_count+1"]
[jump target="*scientist_clear"]

*scientist_talk

[nm t="科学者" color="#aaffff"]
「魔物と人間の身体の違いを研究しているの。共存できる社会のために」[l]

[nm t="科学者" color="#aaffff"]
「女神の加護のサンプルは、解析できればすごい発見になる。魔法医学の革命よ」[p]

[nm t="勇者" color="#aaddff"]
「……その研究が、戦争を終わらせる役に立つ？」[l]

[nm t="科学者" color="#aaffff"]
「……確実ではないけど。可能性はある」[p]

[nm t="勇者" color="#aaddff"]
「……わかった。協力する」[p]

[eval exp="f.surrender_count=f.surrender_count+1"]
[jump target="*scientist_offer_exec"]

*scientist_offer

[eval exp="f.surrender_count=f.surrender_count+1"]

*scientist_offer_exec

; ====【Hシーン：科学者・実験的搾精】====
; [cutin storage="event/scientist_h01.jpg"]

[nm t="科学者" color="#aaffff"]
「では採取を開始します。……緊張しないで。私は専門家よ」[p]

[nm t="ナレーション"]
科学者が手順書を確認するように手元を見る。それから勇者を向いて、白衣のポケットから手袋を取り出した。[p]

[nm t="科学者" color="#aaffff"]
「まず全体的な反応を確認して……それから部位ごとに——」[l]

[nm t="勇者" color="#aaddff"]
「……実況しながらやるの？」[l]

[nm t="科学者" color="#aaffff"]
「記録が大事なの。……あ、でも、あなたが嫌なら口頭はやめるわ」[l]

[nm t="科学者" color="#aaffff"]
「代わりに、自分で感じることに集中してちょうだい」[p]

[nm t="ナレーション"]
白衣の袖をまくり上げ、科学者が作業を始めた。[l]

[nm t="ナレーション"]
医学的な知識に裏打ちされた手技は——予想外に巧みだった。身体のどこに神経が集中しているかを知り尽くしている。[p]

[nm t="勇者" color="#aaddff"]
「……これ、科学的じゃないだろ……」[l]

[nm t="科学者" color="#aaffff"]
「何でもやってみなければわからないのが科学よ。……さあ、もう少し」[p]

[nm t="ナレーション"]
論文を書く手と同じ手で、科学者は勇者を丁寧に、確実に追い詰めた。[p]
; ==========================================

[nm t="科学者" color="#aaffff"]
「……データ取得完了。ありがとう、最高のサンプルだったわ」[l]

[nm t="科学者" color="#aaffff"]
「お礼に、この通行証を持っていって。研究棟内は自由に動けるようになるわ」[p]

[call storage="system/init.ks" target="*squeeze_event"]

*scientist_clear

[eval exp="f.f3_scientist=1"]
[nm t="ナレーション"]
——科学者の実験室を突破した。[p]

[fadeout time="800" color="0x000000"]
[jump storage="chap2_explore.ks" target="*hub_3f"]
