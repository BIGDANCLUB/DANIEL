"""ショート121：給料日のあと 大体こうなる（テンポ系・11/20 ユーザー指定：候補15番）。

python3 catmeme/short_121_kyuryobi_tsukimatsu.py → out/short_121_kyuryobi_tsukimatsu.mp4
- テンポ系：枠なし・右にスマホの残高画面（自作の絵 tools/make_pic_bank.py）＋何に使ったか・左に大きな猫・白い太字・59.9秒でなくてよい
- 前半は笑うハムスターのまま残高だけ減る→27日とまどう猫→28日ハムスター「飲み会最高！」・15日 飲み会で終電逃す→16日 もやし生活・最後は「レギュラー満タン！w」（11/20 ユーザー指定）
- 11/20 修正2：画面だけの「ため」を0.7→0.35秒に短く・字幕を整理
- 金額は手取り22万・ひとり暮らしのざっくりのイメージ。BGM なし
"""
import os

import world_short as Wd

ST = "bg14_home_night"


def cuts():
    out = []
    for day, yen, why, cat, cap in (("25日", 220000, "給料日", "happy_hamster_open_arms", "まだ\n余裕www"),
                                    ("26日", 150000, "家賃", "happy_hamster_open_arms", "まだ\n余裕www"),
                                    ("27日", 98000, "カードの\n引き落とし", "confused_i_dont_know_cat", "あれ…？")):
        c = Wd.split(ST, day, left=cat, sound="L", dur=1.6, se="pi")   # 同じ素材を続けるときも毎回最初から
        c["cats"][0].update(x=270, h=640, w=520, bottom=1400)
        c.update(skit=True, pic=("pic_bank_%d" % yen, 0.72), pic_cap=why, cat_cap=cap)
        out.append(c)
    rows = [
        ("28日", 82000, "飲み会", "happy_hamster_open_arms", "飲み会\n最高！"),
        ("1日", 76000, "サブスク\n引き落とし", "think_chin_paw_orange_cat", "いつ\n入ったっけ"),
        ("5日", 61000, "コンビニ\n毎日", "scream_standing_marmot", "やばい\nやばい"),
        ("10日", 38000, "週末の\n外食", "despair_dramatic_kitten", "なんで？"),
        ("15日", 21000, "終電逃し\nタクシー", "scream_phone_orange_cat", "終電\n逃す"),
        ("16日", 13000, "", "blank_black_cat_zoning_out", "もやし\n生活"),
        ("20日", 8000, "あと\n5日", "sad_banana_cat_cry", "給料日\nまだ？"),
        ("24日", 1200, "明日まで", "stare_lying_tabby_cat", "息を\nひそめる"),
        ("25日", 220000, "給料日", "dance_filmed_by_gray_cat", "レギュラー\n満タン！w"),
    ]
    for k, (day, yen, rcap, cat, lcap) in enumerate(rows):
        big = k >= len(rows) - 3
        a = Wd.split(ST, day, dur=0.35, se=["explosion_chudoon"] if big else ["pi"])
        b = Wd.split(ST, day, left=cat, sound="L", dur=2.2, se="don_hit")
        b["cats"][0].update(x=270, h=640, w=520, bottom=1400)
        for c in (a, b):
            c.update(skit=True, pic=("pic_bank_%d" % yen, 0.72), pic_cap=rcap)
        b.update(pic_cont=True, cat_cap=lcap)
        out += [a, b]
    for c in out:
        c.update(blur=4, band_y=0, skit_bottom=1390, pic_max_h=800, cat_cap_y=560, free_len=True, pic_right=True, pic_cap_below=True)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{r}給料日{y}のあと", 132, Wd.BLACK, 100), ("{y}大体こうなる", 132, Wd.BLACK, 250)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_121_kyuryobi_tsukimatsu.mp4"), os.path.join(Wd.HERE, "out", "short_121_kyuryobi_tsukimatsu_preview"))
