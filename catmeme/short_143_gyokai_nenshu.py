"""ショート143：業界別 平均年収 勝ち抜きバトル（11/24 ユーザー指定：棒グラフで比べる・順位は出さない）。59.9秒。

python3 catmeme/short_143_gyokai_nenshu.py → out/short_143_gyokai_nenshu.mp4
- 低い順に3つ（8・7・6番目）を比べる → いちばん高い業界が喜ぶ → そこに次の2つ（5・4番目）を足して比べる → 勝った業界が喜ぶ →
  次の1つ（3番目）と比べる → … と1つずつ勝ち抜く。画面に順位は出さず、平均年収の棒グラフだけで見せる
- 数字：国税庁「令和6年分 民間給与実態統計調査」（令和7年9月公表）業種別の平均給与（1年を通じて勤務した給与所得者）を万円に四捨五入
  電気・ガス・熱供給・水道 8,324千円／金融・保険 7,023／情報通信 6,595／製造 5,676／建設 5,654／
  学術研究・専門技術サービス・教育 549万円／不動産・物品賃貸 4,955／運輸・郵便 4,876。全体平均 478万円
- 画面：Wd.chain_cut（棒は黄色・勝った棒は赤・数字が数え上がる・背景は横に流れる）。BGM なし
"""
import os

import world_short as Wd

ST = "bg25_office_desk"
UNYU, FUDO, GAKU = ("運輸・郵便", 488), ("不動産", 496), ("学術研究\n・教育", 549)
KEN, SEI, JOHO = ("建設", 565), ("製造", 568), ("情報通信", 660)
KIN, DEN = ("金融・保険", 702), ("電気・ガス\n・水道", 832)
NERV = ["confused_i_dont_know_cat", "stare_tabby_wide_eyes_cat", "peek_what_happen_cat", "think_chin_paw_orange_cat"]
JOY = ["happy_hamster_open_arms", "dance_edm_cat", "rizz_cat_rizz", "dance_filmed_by_gray_cat", "showoff_gojo_cosplay_cat"]
SAD = ["sad_banana_cat_cry", "despair_dramatic_kitten", "blank_black_cat_zoning_out", "sad_looking_away_tabby"]


def rnd(k, old, new, comment):
    """old＝前の勝者（なければ None）、new＝新しく出る業界（低い順）。最後の1つが勝つ。"""
    items = ([old] if old else []) + new
    win = max(items, key=lambda x: x[1])
    grow = [(n, v, (n, v) != old, False) for n, v in items]
    nerv = [(("smug_squint_bicolor_cat" if (n, v) == old else NERV[(k + i) % 4]), False, 280) for i, (n, v) in enumerate(items)]
    out = [Wd.chain_cut(ST, grow, nerv, 3.4, se="drumroll")]
    res = [(n, v, False, (n, v) == win) for n, v in items]
    j = 0
    cats = []
    for n, v in items:
        if (n, v) == win:
            cats.append((JOY[k % len(JOY)], True, 380))
        else:
            cats.append((SAD[(k + j) % len(SAD)], False, 270))
            j += 1
    out.append(Wd.chain_cut(ST, res, cats, 3.0, se="explosion_chudoon"))
    cats2 = [((JOY[(k + 2) % len(JOY)], True, 380) if (n, v) == win else (SAD[(k + i + 2) % len(SAD)], False, 270))
             for i, (n, v) in enumerate(items)]
    out.append(Wd.chain_cut(ST, res, cats2, 3.2, say=comment, se="pikon"))
    return out, win


def cuts():
    intro = Wd.solo(ST, "", "業界別\n平均年収で\n勝負！", "scream_standing_marmot_fast", dur=3.4, se="gong_dora_jaan", big_say=True)
    intro.update(no_tag=True, ref=True, blur=8, say_y=420, band_y=0)
    out = [intro]
    w = None
    for k, (new, com) in enumerate([([UNYU, FUDO, GAKU], "専門知識はお金になる"),
                                    ([KEN, SEI], "製造と建設はたった3万円差"),
                                    ([JOHO], "ITが一気に抜き去る"),
                                    ([KIN], "金融はさすがの貫禄"),
                                    ([DEN], "差は130万円 インフラ最強")]):
        cs, w = rnd(k, w, new, com)
        out += cs
    end = [(KIN[0], KIN[1], False, False), (DEN[0], DEN[1], False, True)]
    out.append(Wd.chain_cut(ST, end, [("sad_looking_away_tabby", False, 270), ("happy_girlfriend_dance_cat", True, 380)], 4.0,
                            say="全体の平均は478万円", se="pikon"))
    out.append(Wd.chain_cut(ST, end, [("think_chin_paw_orange_cat", False, 270), ("dance_tabby_standing_cat", True, 380)], 4.5,
                            say="あなたの業界はどうだった？"))
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}業界別", 96, Wd.BLACK, 95), ("{y}平均年収 勝ち抜きバトル", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_143_gyokai_nenshu.mp4"), os.path.join(Wd.HERE, "out", "short_143_gyokai_nenshu_preview"))
