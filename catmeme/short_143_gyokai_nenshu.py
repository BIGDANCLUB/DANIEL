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
    nerv = [(("smug_squint_bicolor_cat" if (n, v) == old else NERV[(k + i) % 4]), False, 340) for i, (n, v) in enumerate(items)]
    out = [Wd.chain_cut(ST, grow, nerv, 2.5, say=say, se="drumroll")]
    res = [(n, v, False, (n, v) == win) for n, v in items]
    cats, talks, j = [], [], 0
    for x, (n, v) in zip(xs, items):
        if (n, v) == win:
            cats.append((JOY[k % len(JOY)], True, 460))
            talks.insert(0, (x, 800, win_line, True))
        else:
            cats.append((SAD[(k + j) % len(SAD)], False, 340))
            talks.append((x, 1000, lose_lines.get(n), False))
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
    full = 3.4
    out = [intro_scene(2.0, ss=full - 2.0)]   # 冒頭は最後の場面の最後2秒
    w = None
    rounds = [
        ([FUDO, GIN, KEN], "現場は\n朝6時\n集合", {"不動産": "こちらも\n激務だが？", "銀行": "上には\n上が"}, None),
        ([DEN, KOU], "地下で\n働いてる\nので", {"建設": None, "電気・ガス": "災害時は\n休みなし…"}, None),
        ([IYAKU], "新薬1つに\n10年\nかかるので", {"鉱業": "上には\n上が…"}, None),
        ([HOKEN], "契約1件に\n親戚\n総動員", {"医薬品": "知りたく\nなかった…"}, None),
        ([SHOKEN], "ノルマの\n胃痛代込み", {"保険": "ノルマは\nこっちも\nあるが？"}, None),
        ([KAIUN], "船の上で\n半年\n暮らすので", {"証券": "海の男\nには…"}, None),
        ([SOGO], "24時まで\n働いた後\n飲めますか？", {"海運": "アンタには\n勝てん"}, "別格 参戦"),
    ]
    for k, (new, wl, ll, say) in enumerate(rounds):
        cs, w = rnd(k, w, new, wl, ll, say)
        out += cs
    allv = [FUDO, GIN, KEN, DEN, KOU, IYAKU, HOKEN, SHOKEN, KAIUN, SOGO]
    sc = Wd.chain_cut(ST, [GIN + (False, False), SOGO + (False, True)], [(None, False, 0), (None, False, 0)], 4.8, se="pikon")
    sc.pop("bars")
    sc["scroll"] = [(n, v, (n, v) == SOGO) for n, v in allv]
    out.append(sc)
    out.append(intro_scene(full))
    for c in out:
        c["free_len"] = True   # 長さは各場面で合計 59.9 秒にそろえてある
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}業界別", 96, Wd.BLACK, 95), ("{y}平均年収 勝ち抜きバトル", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_143_gyokai_nenshu.mp4"), os.path.join(Wd.HERE, "out", "short_143_gyokai_nenshu_preview"))
