"""ショート81：日本vs世界 遊園地の待ち時間（world_short.py・段階でくらべる型・11/6 ユーザー指定：候補18番（日本vs世界の追加20個から））。59.9秒。

python3 catmeme/short_81_yuenchi.py → out/short_81_yuenchi.mp4
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
- 11/7 ユーザー指定：10分の日本「何か事件が起きたか疑うレベル」・乗れた→6時間（猫なし・世界「(さすがに帰った)」日本「(↓この辺に↓↓寝ている↓)」・世界の説明も出したまま）
"""
import os

import world_short as Wd

ST = "bg59_sakura_park"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('10分', 'happy_chipi_chapa_cat', 'ラッキー', 'surprise_big_pupils_cat', '何か事件が\n起きたか\n疑うレベル'),
        ('30分', 'stare_interviewer_cat', 'ふつう', 'joy_happy_happy_happy_cat', 'すぐ乗れる'),
        ('1時間', 'glare_disgusted_cat', '長い', 'calm_black_face_sheep', 'ふつう'),
        ('90分', 'leave_cat_leaves_home', 'ほかに行く', 'eat_pop_cat', 'チュロスを\n食べながら'),
        ('2時間', 'peek_what_happen_cat', 'なんで\n並ぶの？', 'read_book_orange_kitten', 'しりとりで\n時間つぶし'),
        ('3時間', 'fight_cat_fight', '大さわぎ', 'sleepy_sleepy_cat', '足が\n棒になる'),
        ('4時間', 'scream_standing_marmot', 'ありえない', 'sleepy_old_memories_cat', '話すことが\nなくなる'),
        ('5時間', 'despair_dramatic_kitten', '帰る', 'happy_hamster_open_arms', '乗れたら\n泣く'),
        ('6時間', None, '(さすがに\n帰った)', None, '↓この辺に↓\n↓寝ている↓'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        last = Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K)
        if wcat is None:   # 11/7 ユーザー指定：猫なしの段は世界の説明も出したまま
            last["cap2"] = wcap
            last["se"] = "pafu"   # 11/7 ユーザー指定：日本の字幕が出るときにパフ
        out.append(last)
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}遊園地の待ち時間", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_81_yuenchi.mp4"), os.path.join(Wd.HERE, "out", "short_81_yuenchi_preview"))
