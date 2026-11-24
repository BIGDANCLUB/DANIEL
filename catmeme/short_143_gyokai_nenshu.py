"""ショート143：業界別 平均年収 勝ち抜きバトル（11/24 ユーザー指定：棒グラフで比べる・順位は出さない）。

python3 catmeme/short_143_gyokai_nenshu.py → out/short_143_gyokai_nenshu.mp4
- 低い順に3つを比べる → いちばん高い業界が喜ぶ → 次の2つを足して比べる → … と勝ち抜く。画面に順位は出さない
- 11/24 ユーザー指定：証券・商社など年収の高い業界を入れる（専門商社と総合商社は分ける）・テンポよく
  （棒がのび切ったらすぐ勝ち負けの場面・字幕は勝った猫がしゃべる吹き出しで勝った側に寄せる・負けた猫も悲しみのひとこと）
- 数字（上場企業の有価証券報告書をもとにした集計サイトの値・11/24 調べ。業界によって中央値／平均の違いあり → 概要欄に明記）
  情報・通信 647万（kinmyakucode 32業種の中央値）／不動産 703万・銀行 716万・建設 768万・電気・ガス 772万（同）／
  専門商社 834万（業界ダイジェスト 32社平均）／証券 974万（証券・商品先物 37社平均）／
  総合商社 1857万（5大商社の平均：三菱商事 2,033・三井物産 1,996・伊藤忠 1,804・住友商事 1,744・丸紅 1,708）
- 画面：Wd.chain_cut（参考動画どおりの配置・比べるたびに上下いっぱい・背景は渋谷の映像）。BGM なし
"""
import os

import world_short as Wd

ST = "bg25_office_desk"
JOHO, FUDO, GIN = ("情報・通信", 647), ("不動産", 703), ("銀行", 716)
KEN, DEN, SENMON = ("建設", 768), ("電気・ガス", 772), ("専門商社", 834)
SHOKEN, SOGO = ("証券", 974), ("総合商社", 1857)
NERV = ["confused_i_dont_know_cat", "stare_tabby_wide_eyes_cat", "peek_what_happen_cat", "think_chin_paw_orange_cat"]
JOY = ["happy_hamster_open_arms", "dance_edm_cat", "rizz_cat_rizz", "dance_filmed_by_gray_cat", "showoff_gojo_cosplay_cat"]
SAD = ["sad_banana_cat_cry", "despair_dramatic_kitten", "blank_black_cat_zoning_out", "sad_looking_away_tabby"]


LOSE = ["低い…", "上には\n上が…", "比べないで…", "知りたく\nなかった…", "うちも\nがんばってる…"]


def rnd(k, old, new, comment):
    """old＝前の勝者（なければ None）、new＝新しく出る業界（低い順）。いちばん高い業界が勝つ。
    11/24 ユーザー指定：テンポよく。棒がのび切ったらすぐ勝ち負けの場面へ。字幕は勝った猫がしゃべる吹き出し（勝った側に寄せる・3行まで）、
    負けた猫も悲しみのひとこと"""
    items = ([old] if old else []) + new
    win = max(items, key=lambda x: x[1])
    xs = {2: (295, 785), 3: (200, 540, 880)}[len(items)]
    grow = [(n, v, (n, v) != old, False) for n, v in items]
    nerv = [(("smug_squint_bicolor_cat" if (n, v) == old else NERV[(k + i) % 4]), False, 340) for i, (n, v) in enumerate(items)]
    out = [Wd.chain_cut(ST, grow, nerv, 2.5, se="drumroll")]
    res = [(n, v, False, (n, v) == win) for n, v in items]
    cats, talks, j = [], [], 0
    for x, (n, v) in zip(xs, items):
        if (n, v) == win:
            cats.append((JOY[k % len(JOY)], True, 460))
            talks.insert(0, (x, 800, comment, True))
        else:
            cats.append((SAD[(k + j) % len(SAD)], False, 340))
            talks.append((x, 1000, LOSE[(k * 2 + j) % len(LOSE)], False))
            j += 1
    c = Wd.chain_cut(ST, res, cats, 4.2, se="explosion_chudoon")
    c["talks"] = talks
    out.append(c)
    return out, win


def cuts():
    intro = Wd.solo(ST, "", "うちの業界\n平均より\n上だよね…？", "scream_standing_marmot_fast", dur=3.4, se="gong_dora_jaan", big_say=True)
    intro.update(no_tag=True, bgvid="v09_shibuya_crossing_aerial", blur=3, dark=0.15, say_y=420, band_y=0)
    out = [intro]
    w = None
    for k, (new, com) in enumerate([([JOHO, FUDO, GIN], "転勤3回で\nやっと\nこの額"),
                                    ([KEN, DEN], "4万差…\n台風の夜は\n帰れないけど"),
                                    ([SENMON], "海外出張\n年10回の\n手当込み"),
                                    ([SHOKEN], "ノルマの\n胃痛代込み"),
                                    ([SOGO], "桁が\nちがって\nすみません")]):
        cs, w = rnd(k, w, new, com)
        out += cs
    end = [(SHOKEN[0], SHOKEN[1], False, False), (SOGO[0], SOGO[1], False, True)]
    out.append(Wd.chain_cut(ST, end, [("sad_looking_away_tabby", False, 340), ("happy_girlfriend_dance_cat", True, 460)], 3.0,
                            say="上場企業でもこの差", se="pikon"))
    out.append(Wd.chain_cut(ST, end, [("think_chin_paw_orange_cat", False, 340), ("dance_tabby_standing_cat", True, 460)], 3.4,
                            say="あなたの業界、平均より上？"))
    for c in out:
        c["free_len"] = True   # 11/24 テンポ優先（59.9秒にしない）
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}業界別", 96, Wd.BLACK, 95), ("{y}平均年収 勝ち抜きバトル", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_143_gyokai_nenshu.mp4"), os.path.join(Wd.HERE, "out", "short_143_gyokai_nenshu_preview"))
