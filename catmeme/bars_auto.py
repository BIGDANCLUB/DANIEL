"""bars_short.py の台本を短く書くための部品（10/27）。ショート27（コロナ前と今）と同じ流れ：
つかみ → 項目ごとに「重りが落ちる → 棒がのびる → セリフ2つ」→ 残り → セリフ → 最後に「マイナス○○」をドン。"""
import bars_short as B

SAME = ("confused_i_dont_know_cat",) * 3   # 重りが落ちる場面は3匹とも戸惑う猫（10/27 ユーザー指定）
# ときどき別の素材3匹でそろえる（楽しそうな素材は使わない・10/27 ユーザー指定）。重りの順番ごとに 戸惑う→驚く→戸惑う→不安→戸惑う…
SAME_ALT = ("confused_i_dont_know_cat", "stare_tabby_wide_eyes_cat", "confused_i_dont_know_cat", "sulk_hungry_cat",
            "confused_i_dont_know_cat", "surprise_big_pupils_cat")
THUDS = ("ズシッ!!", "ドスン!!", "ドンッ!!", "ズドン!!", "ドカッ!!")
WEIGHT_CATS = ("money_counting_orange_cat", "punch_boxing_white_cat", "angry_aiming_cat", "eat_pop_cat", "rage_talking_cat")


def cut(dur, say=None, cats=(None, None, None), shown=0, grow=False, banner=None, take=False, voice=None, box=False, big=None,
        se=None, say_y=640, minus=None):
    c = dict(dur=dur, say=say, cats3=list(cats), shown=shown, grow=grow, banner=banner, take=take, voice=voice, box=box, big=big,
             finish=None, say_y=say_y, finish_word="1位")
    if se:
        c["se"] = se
    if minus:
        c["minus"] = minus
    return c


def build(spec, intro, items, after, minus):
    """intro=[(秒, セリフ, 猫たち, voice)], items=[[(秒, セリフ, 猫たち, voice), ...] 項目ごと], after 同じ形, minus=(大, 小, 猫たち)。"""
    n = len(spec["incomes"])
    same = SAME[:n]
    out = []
    for i, (d, say, cats, v) in enumerate(intro):
        big = v if isinstance(v, int) and "？" in (say or "") else (1 if isinstance(v, tuple) else None)
        out.append(cut(d, say, cats, voice=v, se="jan" if i == 0 and say else None, big=big))
    for k, ((name, _), lines) in enumerate(zip(spec["items"], items)):
        label = spec.get("wlabel", {}).get(name, name)   # 重りの文字（2行にしたいときなど）
        same_k = (SAME_ALT[k % len(SAME_ALT)],) * n
        out.append(cut(2.0, None, same_k, shown=k, banner=(name, label, THUDS[k % 5], WEIGHT_CATS[k % 5]), se="explosion_chudoon"))
        grow = (("realize_wet_cat_stare", "eat_chips_cat", "peek_what_happen_cat"), ("calmdown_dancing_cat", "glare_disgusted_cat",
                 "confused_i_dont_know_cat"))[k % 2][:n]
        out.append(cut(2.4, None, grow, shown=k + 1, grow=True, se="card_place"))
        for d, say, cats, v, *opt in lines:
            c = cut(d, say, cats, shown=k + 1, voice=v)
            if opt:   # 5つ目は掛け声（右の列から）
                c["shout"] = (opt[0], n - 1)
            out.append(c)
    last = len(spec["items"])
    res = cut(2.0, None, same, shown=last, take=True, se="game_mario_1up")   # 結果発表（重りではなく・1UPの音・10/27）
    res["result"] = "結果発表"
    out.append(res)
    for i, (d, say, cats, v) in enumerate(after):
        out.append(cut(d, say, cats, shown=last, take=True, voice=v, box=i == 0, say_y=420, se="price_display" if i == 0 else None))
    fin = cut(3.0, None, minus[2], shown=last, take=True, se="gong_dora_jaan", minus=minus[:2])   # じゃーん（10/27）
    if len(minus) > 3 and minus[3] == "good":
        fin["good"] = True
    out.append(fin)
    k = B.TOTAL / sum(c["dur"] for c in out)   # 全体をのばして 59.9 秒ちょうどに
    for c in out:
        c["dur"] *= k
    return out


def run(spec, cs, name):
    import os
    B.run(spec, cs, os.path.join(B.HERE, "out", name + ".mp4"), os.path.join(B.HERE, "out", name + "_preview"))
