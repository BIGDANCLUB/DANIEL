"""ショート148：業界別 残業時間 勝ち抜きバトル（勝ち抜きシリーズ・11/25 ユーザー指定：候補15番）。59.9秒。

python3 catmeme/short_148_zangyo_gyokai.py → out/short_148_zangyo_gyokai.mp4
- 作り方は RULES_kachinuki_short.md（143 が完成形）。11/25 ユーザー指定：確かめられた7業界で作る・1対1だけで比べる回数を増やす
- 数字：厚生労働省「毎月勤労統計調査」令和6年分結果確報（事業所規模5人以上・就業形態計の所定外労働時間・月あたり）
  卸売・小売 7.1／建設 12.7／金融・保険 12.9／鉱業 14.1／電気・ガス 15.8／情報通信 15.8／運輸・郵便 21.7（全体 10.0）
  電気・ガスと情報通信は同じ値 → 「引き分け」にして情報通信が次へ
- 11/25 修正：冒頭の猫はスマホ猫と踊る猫・横流しを速く・今回だけ勝った（残業が多い）側の猫を悲しませる
- 11/25 修正2：「うちの会社〜」の場面をなくし、全体平均（10.0時間）との比べを足して7回に・帯の間は警告音
- 構成：冒頭＝流れるランキングが右はしに着く（1秒止めてファンファーレ）→「うちの会社〜」→ 1対1の勝ち抜き6回 → 流れるランキング
"""
import os

import world_short as Wd

W_ = 1080
ST = "bg25_office_desk"
VID = "v01_typing_keyboard_desk"
FMT = "%.1f時間"
OROSHI, KEN, KIN = ("卸売・小売", 7.1), ("建設", 12.7), ("金融・保険", 12.9)
KOU, DEN, JOHO, UNYU = ("鉱業", 14.1), ("電気・ガス", 15.8), ("情報通信", 15.8), ("運輸・郵便", 21.7)
HEIKIN = ("全体平均", 10.0)   # 11/25：同じ調査の全産業の平均（比べる回数を増やすため）
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
    grow = [(a[0], a[1], k == 0, False), (b[0], b[1], True, False)]
    nerv = [("smug_squint_bicolor_cat" if k else NERV[k % 4], False, 420), (NERV[(k + 1) % 4], False, 420)]
    out = [cc(grow, nerv, 2.5, se="drumroll")]
    if tie:
        res = [(a[0], a[1], False, True), (b[0], b[1], False, True)]
        cats = [(SAD[k % len(SAD)], True, 520), (SAD[(k + 1) % len(SAD)], False, 520)]   # 11/25：残業が多い側は悲しむ
        c = cc(res, cats, 4.6, say="引き分け", se="explosion_chudoon")
        c.update(say_mid_y=455, say_mid_size=110, say_mid_col=Wd.RED, say_mid_scol=Wd.WHITE, say_mid_stroke=14)
        c["talks"] = [(xs[0], 650, tie[0], True), (xs[1], 650, tie[1], True)]
        out.append(c)
        return out, b
    win, lose_x, win_x = (b, xs[0], xs[1]) if b[1] > a[1] else (a, xs[1], xs[0])
    res = [(a[0], a[1], False, a == win), (b[0], b[1], False, b == win)]
    cats = [((SAD[k % len(SAD)], True, 560) if q == win else (JOY[k % len(JOY)], False, 420)) for q in (a, b)]   # 11/25：今回だけ勝った（残業が多い）側が悲しむ
    c = cc(res, cats, 4.6, se="explosion_chudoon")
    c["talks"] = [(win_x, 650, win_line, True), (lose_x, 840, lose_line, False)]
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
    w = OROSHI
    rounds = [
        (HEIKIN, "これが\n日本の\n平均…", "シフト制で\n帰れる…\n(土日はない)", None),
        (KEN, "工期前は\n土曜も\n現場", "ふつうの\nはずが…", None),
        (KIN, "決算期は\n終電コース", "0.2時間差で\n負けた…", None),
        (KOU, "交代勤務で\n夜も\n動いてる", "上には\n上が…", None),
        (DEN, "台風の夜は\n家に\n帰れない", "地上の人も\n大変だ…", None),
        (JOHO, None, None, ("まさかの\n同点…", "障害対応は\n深夜2時")),
        (UNYU, "荷物は\n待って\nくれない", "6時間差は\n無理…", None),
    ]
    for k, (new, wl, ll, tie) in enumerate(rounds):
        cs, w = rnd(k, w, new, wl, ll, tie)
        body += cs
    allv = [OROSHI, HEIKIN, KEN, KIN, KOU, DEN, JOHO, UNYU]
    scats = ["happy_hamster_open_arms", "dance_edm_cat", "rizz_cat_rizz", "think_chin_paw_orange_cat", "blank_black_cat_zoning_out",
             "sad_looking_away_tabby", "despair_dramatic_kitten", "sad_banana_cat_cry"]   # 残業が多いほど悲しい
    HOLD = 1.0
    T = 6.5   # 11/25：横流しを速く（前は約13秒）。余った時間は本編の勝ち負けの場面に足す
    extra = 59.9 - full - sum(c["dur"] for c in body) - HOLD - T
    res_cuts = [c for c in body if c.get("talks")]
    for c in res_cuts:
        c["dur"] += extra / len(res_cuts)
    n = len(allv)
    strip = n * 280
    u_enter = (75 + (n - 1) * 280 - W_ + 0.0) / (strip + 75 - W_)
    tA = round(T * u_enter, 2)

    def scroll(t0, dur, se=None):
        c = cc([KEN + (False, False), UNYU + (False, True)], [(None, False, 0), (None, False, 0)], dur, se=se)
        c.pop("bars")
        c["cats"] = []
        c.update(scroll=[(nm, v, (nm, v) == UNYU, cat) for (nm, v), cat in zip(allv, scats)], scroll_t0=t0, scroll_T=T)
        return c
    head = scroll(tA, T - tA + HOLD, se=[{"f": "doon_movie", "at": 0.0, "len": T - tA + HOLD, "gain": -4},   # 11/25：帯の音は派手で重厚に（映画風ドーン＋ゴゴゴ＋サイレン）。帯が消えるところでフェードアウト
                                          {"f": "rumble_gogogo", "at": 0.0, "len": T - tA + HOLD, "gain": -6},
                                          {"f": "siren_police", "at": 0.1, "len": T - tA + HOLD - 0.1, "gain": -10},
                                          {"f": "fanfare_pararappara", "at": T - tA}])   # 帯が出ている間は警告音
    head["danger"] = ("業界別！\n残業時間バトル", 960)   # 猫と下の業界名にかからない高さ・横いっぱい   # 11/25 ユーザー指定：冒頭に危険の帯ふうの題名
    tail = scroll(0.0, tA)
    out = [head] + body + [tail]
    for c in out:
        c["free_len"] = True
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}業界別{r}残業時間", 96, Wd.BLACK, 95), ("{y}勝ち抜きバトル", 96, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_148_zangyo_gyokai.mp4"), os.path.join(Wd.HERE, "out", "short_148_zangyo_gyokai_preview"))
