"""ショート149：職業別 平均年収 勝ち抜きバトル（勝ち抜きシリーズ・148 が手本・11/26 ユーザー指定）。59.9秒。

python3 catmeme/short_149_shokugyo_nenshu.py → out/short_149_shokugyo_nenshu.mp4
- 11/26 ユーザー指定（最初の5秒で離脱させない）：冒頭の流れるランキングは職業名を「？？？」で隠す・帯に「あなたの職業は何位？」・
  帯は1フレーム目から出ていて大きく読める（横から入ってこない）・冒頭にチリン・帯の場面は2秒
- 11/26 修正：「？？？」は1位だけ・管理職は「管理的職業従事者」（会社の課長以上など全般）なので「管理職（全般）」
- 数字：厚生労働省「令和6年賃金構造基本統計調査」の職業別の年収（男女計・きまって支給する現金給与額×12＋年間賞与等）を
  まとめた記事（東洋経済・GBase）で確認した値。1〜4位と公認会計士・税理士・法務従事者は東洋経済、それ以外は GBase
  航空機操縦士 1697／医師 1338／歯科医師 1135／大学教授 1093／管理的職業 917／経営・金融・保険専門職 903／獣医師 885／
  大学准教授 881／公認会計士・税理士 856／法務従事者 765（万円）
- 1対1だけ・9回勝ち抜き。勝った職業の猫は喜ぶ（ふつうの向き）
"""
import os

import world_short as Wd

W_ = 1080
ST = "bg25_office_desk"
VID = "v14_business_meeting"
FMT = "%d万"
HOU, KAIKEI, JUN = ("法務従事者", 765), ("会計士・税理士", 856), ("大学准教授", 881)
JUI, KINYU, KANRI = ("獣医師", 885), ("金融専門職", 903), ("管理職（全般）", 917)
KYOJU, SHIKA, ISHI, PILOT = ("大学教授", 1093), ("歯科医師", 1135), ("医師", 1338), ("パイロット", 1697)
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
        c.update(say_mid_y=455, say_mid_size=110, say_mid_col=Wd.RED, say_mid_scol=Wd.WHITE, say_mid_stroke=14)
        c["talks"] = [(xs[0], 590, tie[0], True), (xs[1], 590, tie[1], True)]
        out.append(c)
        return out, b
    win, lose_x, win_x = (b, xs[0], xs[1]) if b[1] > a[1] else (a, xs[1], xs[0])
    res = [(a[0], a[1], False, a == win), (b[0], b[1], False, b == win)]
    cats = [((JOY[k % len(JOY)], True, 560) if q == win else (SAD[k % len(SAD)], False, 420)) for q in (a, b)]
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
    w = HOU
    rounds = [
        (KAIKEI, "確定申告期は\n家に\n帰れない", "司法試験\nあんなに\n頑張ったのに…", None),
        (JUN, "ここまで\n博士で\n10年", "数字には\n強いのに…", None),
        (JUI, "動物は\n夜中も\n待ってくれない", "たった\n4万円差…", None),
        (KINYU, "数字1つで\n億が動く", "犬に\nかまれた分は…", None),
        (KANRI, "部下の分まで\n謝ってる", "上司には\n勝てない…", None),
        (KYOJU, "論文と会議で\n休みゼロ", "部長でも\nこれか…", None),
        (SHIKA, "1日中\n口の中を\n見てる", "研究費は\n自腹…", None),
        (ISHI, "当直明けで\nそのまま外来", "医師には\n勝てない…", None),
        (PILOT, "時差ボケは\n手当込み", "空の上には\n勝てん", None),
    ]
    for k, (new, wl, ll, tie) in enumerate(rounds):
        cs, w = rnd(k, w, new, wl, ll, tie)
        body += cs
    allv = [HOU, KAIKEI, JUN, JUI, KINYU, KANRI, KYOJU, SHIKA, ISHI, PILOT]
    scats = ["sad_banana_cat_cry", "despair_dramatic_kitten", "blank_black_cat_zoning_out", "sad_looking_away_tabby",
             "think_chin_paw_orange_cat", "happy_hamster_open_arms", "dance_edm_cat", "rizz_cat_rizz", "showoff_gojo_cosplay_cat",
             "dance_tabby_standing_cat"]
    HOLD = 1.0
    n = len(allv)
    u_enter = (75 + (n - 1) * 280 - W_ + 0.0) / (n * 280 + 75 - W_)
    T = round((2.0 - HOLD) / (1 - u_enter), 2)   # 11/26：帯の場面は2秒（右はしに着くまで1秒＋止まって1秒）
    extra = 59.9 - full - sum(c["dur"] for c in body) - HOLD - T
    res_cuts = [c for c in body if c.get("talks")]
    for c in res_cuts:
        c["dur"] += extra / len(res_cuts)
    n = len(allv)
    strip = n * 280
    u_enter = (75 + (n - 1) * 280 - W_ + 0.0) / (strip + 75 - W_)
    tA = round(T * u_enter, 2)

    def scroll(t0, dur, se=None):
        c = cc([HOU + (False, False), PILOT + (False, True)], [(None, False, 0), (None, False, 0)], dur, se=se)
        c.pop("bars")
        c["cats"] = []
        c.update(scroll=[(nm, v, (nm, v) == PILOT, cat) for (nm, v), cat in zip(allv, scats)], scroll_t0=t0, scroll_T=T)
        return c
    head = scroll(tA, T - tA + HOLD, se=[{"f": "doon_movie", "at": 0.0, "len": T - tA + HOLD, "gain": -4},   # 11/25：帯の音は派手で重厚に（映画風ドーン＋ゴゴゴ＋サイレン）。帯が消えるところでフェードアウト
                                          {"f": "rumble_gogogo", "at": 0.0, "len": T - tA + HOLD, "gain": -6},
                                          {"f": "siren_police", "at": 0.1, "len": T - tA + HOLD - 0.1, "gain": -10},
                                          {"f": "fanfare_pararappara", "at": T - tA}])   # 帯が出ている間は警告音
    head["danger"] = ("あなたの職業は\n何位？", 960)   # 11/26：帯の中に問いかけ（大きく読めるよう短く2行）
    head.update(danger_static=True, hide_names="top")   # 11/26：帯は最初から出ている・1位の職業名だけ「？？？」
    head["se"] = [{"f": "chirin", "at": 0.0}] + head["se"]   # 11/26：冒頭にチリン
    tail = scroll(0.0, tA)
    out = [head] + body + [tail]
    for c in out:
        c["free_len"] = True
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}職業別{r}平均年収", 96, Wd.BLACK, 95), ("{y}勝ち抜きバトル", 96, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_149_shokugyo_nenshu.mp4"), os.path.join(Wd.HERE, "out", "short_149_shokugyo_nenshu_preview"))
