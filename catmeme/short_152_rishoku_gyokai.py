"""ショート152：業界別 離職率 勝ち抜きバトル（勝ち抜きシリーズ・148/149 が手本・11/26 ユーザー指定：候補5番）。59.9秒。

python3 catmeme/short_152_rishoku_gyokai.py → out/short_152_rishoku_gyokai.mp4
- 11/26 ユーザー指定：離職率の高い順に勝ち抜く・勝った（離職率が高い）側が悲しむ
- 数字：厚生労働省「令和6年雇用動向調査結果の概要」表4-2 産業別離職率（常用労働者計・令和6年1年間）TOP10
  宿泊・飲食 25.1／サービス業（他に分類されないもの）20.3／生活関連・娯楽 19.0／卸売・小売 15.1／医療・福祉 13.8／
  不動産 13.5／教育 13.1／学術研究 11.1／情報通信 10.2／運輸・郵便 10.2（産業計 14.2）。情報通信と運輸は同率 → 引き分け
- 11/26 修正：負けた側のセリフ（情報通信「そっちノルマあるの？」・不動産「0.3差でセーフ！(アウト)」・医療「わかる」・卸売「そんな高いの？」（とまどう猫）・派遣「そらそうよ」）と卸売の勝ちセリフ「土日休みくださぁい！」
- 冒頭は 149 と同じ（チリン・帯は最初から・1位だけ？？？・2秒・流れるランキングはアップ）
"""
import os

import world_short as Wd

W_ = 1080
ST = "bg25_office_desk"
VID = "v09_shibuya_crossing_aerial"
FMT = "%.1f%%"
UNYU, JOHO, GAKU = ("運輸・郵便", 10.2), ("情報通信", 10.2), ("学術研究", 11.1)
KYOIKU, FUDO, IRYO = ("教育", 13.1), ("不動産", 13.5), ("医療・福祉", 13.8)
OROSHI, SEIKATSU, SERV, SHUKU = ("卸売・小売", 15.1), ("美容・娯楽", 19.0), ("派遣・警備など", 20.3), ("宿泊・飲食", 25.1)
NERV = ["confused_i_dont_know_cat", "stare_tabby_wide_eyes_cat", "peek_what_happen_cat", "think_chin_paw_orange_cat"]
JOY = ["happy_hamster_open_arms", "dance_edm_cat", "rizz_cat_rizz", "dance_filmed_by_gray_cat", "showoff_gojo_cosplay_cat",
       "happy_girlfriend_dance_cat"]
SAD = ["sad_banana_cat_cry", "despair_dramatic_kitten", "blank_black_cat_zoning_out", "sad_looking_away_tabby"]
INTRO = "うちの会社の残業\n平均より\n少ないよね…？"


def cc(*a, **k):
    c = Wd.chain_cut(ST, *a, bgvid=VID, **k)
    c["unit_fmt"] = FMT
    return c


def rnd(k, a, b, win_line, lose_line, tie=None):
    """1対1。a が前の勝者（左）、b が新しく出る業界（右）。tie＝(左のセリフ, 右のセリフ) なら引き分け（両方赤）。"""
    xs = (295, 785)
    grow = [(a[0], a[1], k == 0, False, {} if k == 0 else {"slide_from": 785}), (b[0], b[1], True, False)]   # 11/25：前の勝者の札は右から左へスッと動く（色はふつうに戻してから）
    nerv = [("smug_squint_bicolor_cat" if k else NERV[k % 4], False, 420), (NERV[(k + 1) % 4], False, 420)]
    g0 = cc(grow, nerv, 2.5, se="drumroll")
    if k:
        g0["cats"][0]["slide_from"] = 785   # 猫も一緒に動く
        g0["cats"][1]["appear"] = Wd.SLIDE_T   # 新しい業界の猫は動き終わってから
    out = [g0]
    if tie:
        res = [(a[0], a[1], False, True), (b[0], b[1], False, True)]
        cats = [(SAD[k % len(SAD)], True, 520), (SAD[(k + 1) % len(SAD)], False, 520)]   # 11/25：残業が多い側は悲しむ
        c = cc(res, cats, 4.6, say="引き分け", se="explosion_chudoon")
        c.update(say_mid_y=1060, say_mid_size=110, say_mid_col=Wd.RED, say_mid_scol=Wd.WHITE, say_mid_stroke=14)
        c["talks"] = [(xs[0], 590, tie[0], True), (xs[1], 590, tie[1], True)]
        out.append(c)
        return out, b
    win, lose_x, win_x = (b, xs[0], xs[1]) if b[1] > a[1] else (a, xs[1], xs[0])
    res = [(a[0], a[1], False, a == win), (b[0], b[1], False, b == win)]
    cats = [((SAD[k % len(SAD)], True, 560) if q == win else (JOY[k % len(JOY)], False, 420)) for q in (a, b)]   # 離職率が高い（勝った）側が悲しむ
    c = cc(res, cats, 4.6, se="explosion_chudoon")
    c["talks"] = [(win_x, 590, win_line, True), (lose_x, 770, lose_line, False)]   # 11/25：猫にかからないよう少し上に
    out.append(c)
    return out, win


def intro_scene(dur, ss=0.0):
    c = Wd.solo(ST, "", INTRO, "dance_filmed_by_gray_cat", dur=dur, se="gong_dora_jaan" if ss == 0 else None, big_say=True)
    c.update(no_tag=True, bgvid=VID, blur=3, dark=0.15, say_y=420, band_y=0)
    c["cats"][0]["ss"] = ss
    return c


def cuts():
    full = 0.0   # 11/25 ユーザー指定：「うちの会社の残業〜」の場面はなし
    body = []
    w = UNYU
    rounds = [
        (JOHO, None, None, ("荷物と一緒に\n人も出ていく", "まさかの\n同率…")),
        (GAKU, "徹夜明けに\n転職サイト", "そっちノルマ\nあるの？", None),
        (KYOIKU, "4月が来るたび\n先生が減る", "研究室は\n辞められない", None),
        (FUDO, "ノルマ未達で\n春に消える", "わずか\n0.4差…", None),
        (IRYO, "夜勤明けに\n退職届", "0.3差でセーフ！\n(アウト)", None),
        (OROSHI, "土日休み\nくださぁい！", "わかる", None),
        (SEIKATSU, "美容師\n3年目の壁", "そんな\n高いの？", None),
        (SERV, "3か月ごとに\n人が\n入れ替わる", "まだ上が\nいた…", None),
        (SHUKU, "4人に1人が\nいなくなる", "そらそうよ", None),
    ]
    for k, (new, wl, ll, tie) in enumerate(rounds):
        cs, w = rnd(k, w, new, wl, ll, tie)
        if new == SEIKATSU:   # 11/26 ユーザー指定：卸売「そんな高いの？」はとまどう猫
            for q in cs[-1]["cats"]:
                if q["x"] < 540:
                    q["a"] = "confused_i_dont_know_cat"
        body += cs
    allv = [UNYU, JOHO, GAKU, KYOIKU, FUDO, IRYO, OROSHI, SEIKATSU, SERV, SHUKU]
    scats = ["happy_hamster_open_arms", "dance_edm_cat", "rizz_cat_rizz", "dance_cute_dog", "think_chin_paw_orange_cat",
             "blank_black_cat_zoning_out", "sad_looking_away_tabby", "despair_dramatic_kitten", "scream_standing_marmot",
             "sad_banana_cat_cry"]   # 離職率が高いほど悲しい
    HOLD = 1.0
    n = len(allv)
    u_enter = (75 + (n - 1) * (Wd.SC_BW + Wd.SC_GAP) - W_ + 0.0) / (n * (Wd.SC_BW + Wd.SC_GAP) + 75 - W_)
    T = round((2.0 - HOLD) / (1 - u_enter), 2)   # 11/26：帯の場面は2秒（右はしに着くまで1秒＋止まって1秒）
    extra = 59.9 - full - sum(c["dur"] for c in body) - HOLD - T
    res_cuts = [c for c in body if c.get("talks")]
    for c in res_cuts:
        c["dur"] += extra / len(res_cuts)
    n = len(allv)
    strip = n * (Wd.SC_BW + Wd.SC_GAP)
    u_enter = (75 + (n - 1) * (Wd.SC_BW + Wd.SC_GAP) - W_ + 0.0) / (strip + 75 - W_)
    tA = round(T * u_enter, 2)

    def scroll(t0, dur, se=None):
        c = cc([UNYU + (False, False), SHUKU + (False, True)], [(None, False, 0), (None, False, 0)], dur, se=se)
        c.pop("bars")
        c["cats"] = []
        c.update(scroll=[(nm, v, (nm, v) == SHUKU, cat) for (nm, v), cat in zip(allv, scats)], scroll_t0=t0, scroll_T=T)
        return c
    head = scroll(tA, T - tA + HOLD, se=[{"f": "doon_movie", "at": 0.0, "len": T - tA + HOLD, "gain": -4},   # 11/25：帯の音は派手で重厚に（映画風ドーン＋ゴゴゴ＋サイレン）。帯が消えるところでフェードアウト
                                          {"f": "rumble_gogogo", "at": 0.0, "len": T - tA + HOLD, "gain": -6},
                                          {"f": "siren_police", "at": 0.1, "len": T - tA + HOLD - 0.1, "gain": -10},
                                          {"f": "fanfare_pararappara", "at": T - tA}])   # 帯が出ている間は警告音
    head["danger"] = ("あなたの業界は\n何位？", 960)   # 11/26：帯の中に問いかけ（大きく読めるよう短く2行）
    head.update(danger_static=True, hide_names="top")   # 11/26：帯は最初から出ている・1位の職業名だけ「？？？」
    head["se"] = [{"f": "chirin", "at": 0.0}] + head["se"]   # 11/26：冒頭にチリン
    tail = scroll(0.0, tA)
    out = [head] + body + [tail]
    for c in out:
        c["free_len"] = True
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}業界別{r}離職率", 96, Wd.BLACK, 95), ("{y}勝ち抜きバトル", 96, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_152_rishoku_gyokai.mp4"), os.path.join(Wd.HERE, "out", "short_152_rishoku_gyokai_preview"))
