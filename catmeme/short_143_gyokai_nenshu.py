"""ショート143：業界別 平均年収 勝ち抜きバトル（11/24 ユーザー指定：棒グラフで比べる・順位は出さない）。

python3 catmeme/short_143_gyokai_nenshu.py → out/short_143_gyokai_nenshu.mp4
- 11/24 ユーザー指定（最新）：平均年収 TOP9 の業界で作る＋最後に総合商社を「別格」で登場させる・59.9秒
  数字：上場企業の有価証券報告書をもとにした業種別の中央値（kinmyakucode・JPX 32業種・2026年版）
    海運 1,030万／証券 977万／保険 923万／医薬品 826万／鉱業 778万／電気・ガス 772万／建設 768万／銀行 716万／不動産 703万（9位）
  総合商社 1,857万＝5大商社（三菱商事 2,033・三井物産 1,996・伊藤忠 1,804・住友商事 1,744・丸紅 1,708）の平均。基準が違うので「別格」として最後に
- 構成：冒頭は最後の「うちの業界〜」の場面の最後2秒 → 低い順に勝ち抜き（棒がのび切ったらすぐ勝ち負け・勝った猫のテキストボックス・
  負けた猫は悲しみのひとこと・字幕なしの猫もいる）→ 全業界を左から右へ流す → 「うちの業界〜」の場面
- 画面：Wd.chain_cut（参考動画どおりの配置・比べるたびに上下いっぱい・背景は渋谷の映像）。BGM なし
"""
import os

import world_short as Wd

W_ = 1080

ST = "bg25_office_desk"
FUDO, GIN, KEN, DEN = ("不動産", 703), ("銀行", 716), ("建設", 768), ("電気・ガス", 772)
KOU, IYAKU, HOKEN = ("鉱業", 778), ("医薬品", 826), ("保険", 923)
SHOKEN, KAIUN, SOGO = ("証券", 977), ("海運", 1030), ("総合商社", 1857)
NERV = ["confused_i_dont_know_cat", "stare_tabby_wide_eyes_cat", "peek_what_happen_cat", "think_chin_paw_orange_cat"]
JOY = ["happy_hamster_open_arms", "dance_edm_cat", "rizz_cat_rizz", "dance_filmed_by_gray_cat", "showoff_gojo_cosplay_cat",
       "happy_girlfriend_dance_cat"]
SAD = ["sad_banana_cat_cry", "despair_dramatic_kitten", "blank_black_cat_zoning_out", "sad_looking_away_tabby"]
INTRO = "うちの業界\n平均より\n上だよね…？"


def rnd(k, old, new, win_line, lose_lines, say=None):
    """old＝前の勝者（なければ None）、new＝新しく出る業界（低い順）。いちばん高い業界が勝つ。
    lose_lines＝負けた業界ごとのひとこと（{業界名: 文 か None}）"""
    items = ([old] if old else []) + new
    win = max(items, key=lambda x: x[1])
    xs = {2: (295, 785), 3: (200, 540, 880)}[len(items)]
    grow = [(n, v, (n, v) != old, False) for n, v in items]
    nerv = [(("smug_squint_bicolor_cat" if (n, v) == old else NERV[(k + i) % 4]), False, 420) for i, (n, v) in enumerate(items)]
    out = [Wd.chain_cut(ST, grow, nerv, 2.5, say=say, se="drumroll")]
    res = [(n, v, False, (n, v) == win) for n, v in items]
    cats, talks, j = [], [], 0
    for x, (n, v) in zip(xs, items):
        if (n, v) == win:
            cats.append((JOY[k % len(JOY)], True, 560))
            talks.insert(0, (x, 650, win_line, True))
        else:
            cats.append((SAD[(k + j) % len(SAD)], False, 420))
            talks.append((x, 840, lose_lines.get(n), False))
            j += 1
    c = Wd.chain_cut(ST, res, cats, 4.6, se="explosion_chudoon")
    c["talks"] = talks
    out.append(c)
    return out, win


def intro_scene(dur, ss=0.0):
    c = Wd.solo(ST, "", INTRO, "scream_standing_marmot_fast", dur=dur, se="gong_dora_jaan" if ss == 0 else None, big_say=True)
    c.update(no_tag=True, bgvid="v09_shibuya_crossing_aerial", blur=3, dark=0.15, say_y=420, band_y=0)
    c["cats"][0]["ss"] = ss
    return c


def cuts():
    """11/24 ユーザー指定：ループする構成。
    冒頭＝流れるランキングが総合商社に届くところ（ファンファーレ）→「うちの業界〜」→ 本編の勝ち抜き → 流れるランキング（総合商社が出る前で終わる）
    合計 59.9 秒（TOP9。各場面は少し長め）"""
    full = 3.4
    body = []
    w = None
    rounds = [
        ([FUDO, GIN, KEN], "現場は\n朝6時\n集合", {"不動産": "こちらも\n激務だが？", "銀行": "建設より\n下なの？"}, None),
        ([DEN, KOU], "40年間\n地下行き…‼\n(の場合も)", {"建設": None, "電気・ガス": "災害時は\n休みなし…"}, None),
        ([IYAKU], "新薬1つに\n10年\nかかるので", {"鉱業": "清潔で\n高年収…"}, None),
        ([HOKEN], "契約1件に\n親戚\n総動員", {"医薬品": "それは\nヤバイ"}, None),
        ([SHOKEN], "ノルマの\n胃痛代込み", {"保険": "ノルマは\nこっちも\nあるが？"}, None),
        ([KAIUN], "1000万超え\nFOOO～↑", {"証券": "フィジカルで\n負けてそう"}, None),
        ([SOGO], "24時まで\n働いた後\n飲めますか？", {"海運": "アンタには\n勝てん"}, "※別格"),
    ]
    for k, (new, wl, ll, say) in enumerate(rounds):
        cs, w = rnd(k, w, new, wl, ll, say)
        body += cs
    for c in body:
        if c.get("say_mid") == "※別格":   # 11/24 ユーザー指定：「※別格」を極大に
            c.update(say_mid_size=200, say_mid_col=(255, 236, 40), say_mid_y=470)
    # 流れるランキング（左の業界から読み、総合商社で止まる）
    allv = [FUDO, GIN, KEN, DEN, KOU, IYAKU, HOKEN, SHOKEN, KAIUN, SOGO]
    scats = ["sad_banana_cat_cry", "despair_dramatic_kitten", "happy_hamster_open_arms", "blank_black_cat_zoning_out",
             "dance_edm_cat", "rizz_cat_rizz", "dance_filmed_by_gray_cat", "showoff_gojo_cosplay_cat", "happy_girlfriend_dance_cat",
             "dance_tabby_standing_cat"]
    HOLD = 1.0   # 11/24 ユーザー指定：右はしに着いたら1秒止める（止まった瞬間にパラララッパラー）
    T = 59.9 - full - sum(c["dur"] for c in body) - HOLD
    n = len(allv)
    strip = n * (230 + 50)
    u_enter = (75 + (n - 1) * 280 - W_ + 0.0) / (strip + 75 - W_)   # 総合商社の棒が右はしから入りはじめる位置
    tA = round(T * u_enter, 2)

    def scroll(t0, dur, se=None):
        c = Wd.chain_cut(ST, [GIN + (False, False), SOGO + (False, True)], [(None, False, 0), (None, False, 0)], dur, se=se)
        c.pop("bars")
        c["cats"] = []
        c.update(scroll=[(nm, v, (nm, v) == SOGO, cat) for (nm, v), cat in zip(allv, scats)], scroll_t0=t0, scroll_T=T)
        return c
    head = scroll(tA, T - tA + HOLD, se=[{"f": "fanfare_pararappara", "at": T - tA}])   # 右はしに着いて止まる瞬間 → パラララッパラー
    tail = scroll(0.0, tA)
    out = [head, intro_scene(full)] + body + [tail]
    for c in out:
        c["free_len"] = True
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}業界別", 96, Wd.BLACK, 95), ("{y}平均年収 勝ち抜きバトル", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_143_gyokai_nenshu.mp4"), os.path.join(Wd.HERE, "out", "short_143_gyokai_nenshu_preview"))
