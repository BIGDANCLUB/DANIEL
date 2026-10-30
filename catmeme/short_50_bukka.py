"""ショート50：昔と今 物価はどれだけ上がった？ ハンバーガーから一軒家まで（world_short.py の左右くらべ・10/30 ユーザー指定）。59.9秒。

python3 catmeme/short_50_bukka.py → out/short_50_bukka.mp4
- 地震の反応と同じ3段：「品物の札だけ → 左に『昔（2000年ごろ）』の棒と猫 → 右に『今（2026年）』の棒と猫（左は残る）」
- 棒グラフ：左右の棒の高さは値段の比（品物ごとに今の値段をいちばん高くそろえる）。棒の中に値段、猫は棒の上に立つ。下の説明に「今は約○倍」
- 最後は大卒初任給：物価ほど給料は上がっていない、でオチ。最後のまとめは入れない
値段はざっくりの目安（全国平均や代表的なお店のおおよそ）：
  ハンバーガー 59円（2002年ごろ）→ 約190円／牛丼並 約280円 → 約500円／ラーメン 約550円 → 約1000円／缶ジュース 120円 → 約180円／
  たまご10個 約200円 → 約300円／ガソリン1L 約100円 → 約170円／軽自動車 約100万 → 約170万／
  首都圏の新築一戸建て 約3500万 → 約5000万／大卒初任給 約19.6万 → 約23万
実在の会社・お店の名前は出さない（「ハンバーガー」「牛丼」と書く）。BGM なし
"""
import os

import world_short as Wd

ST = "bg48_clean_street"
K = 59.9 / 58.5
MAXH = 380   # いちばん高い棒（px）。猫が上に立っても札にかからない高さ


def cuts():
    out = []
    # (品物, 昔の値段, 今の値段, 比（今=1）, 昔の猫, 今の猫)
    rows = [
        ("ハンバーガー", "59円", "約190円", 59 / 190, "happy_chipi_chapa_cat", "stare_tabby_wide_eyes_cat"),
        ("牛丼 並", "約280円", "約500円", 280 / 500, "eat_pop_cat", "despair_dramatic_kitten"),
        ("ラーメン", "約550円", "約1000円", 550 / 1000, "eat_chips_cat", "scream_phone_orange_cat"),
        ("缶ジュース", "120円", "約180円", 120 / 180, "dance_happy_banana_cat", "sulk_hungry_cat"),
        ("たまご10個", "約200円", "約300円", 200 / 300, "talk_orange_white_sitting_cat", "stare_big_eyes_tabby_kitten"),
        ("ガソリン1L", "約100円", "約170円", 100 / 170, "ride_kitten_bike", "glare_disgusted_cat"),
        ("軽自動車", "約100万円", "約170万円", 100 / 170, "drive_driving_cat", "sad_looking_away_tabby"),
        ("一軒家", "約3500万円", "約5000万円", 3500 / 5000, "dance_three_kittens", "surprise_big_pupils_cat"),
        ("大卒の初任給", "約19.6万円", "約23万円", 19.6 / 23, "think_chin_paw_orange_cat", "sad_banana_cat_cry"),
    ]
    for item, old, new, r, ocat, ncat in rows:
        last = item == "大卒の初任給"
        ho, hn = MAXH * r, MAXH
        bar_o = ("bar:%d:blue:%s" % (ho, old), 275, 1290 - ho / 2, 300)   # 棒の中に値段
        bar_n = ("bar:%d:red:%s" % (hn, new), 805, 1290 - hn / 2, 300)
        times = 1 / r
        out.append(Wd.split(ST, item, dur=1.2 * K, se=["game_mario_1up"] if last else ["pi"]))
        c = Wd.split(ST, item, left=ocat, cap="2000年ごろ", cap_side="L", sound="L", dur=2.3 * K,
                     se=["game_coin_get_money_gain_happy"])
        c["props"] = [bar_o]
        out.append(c)
        c = Wd.split(ST, item, left=ocat, right=ncat, cap="今は\n約%.1f倍" % times, cap_side="R", sound="R", dur=3.0 * K,
                     se=["anime_conan_hirameki_idea_realize_truth" if last else "explosion_chudoon"])
        c["props"] = [bar_o, bar_n]
        out.append(c)
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=("昔", "今"))
        for q, hb in zip(c["cats"], [p_ for p_ in c.get("props", [])]):   # 猫は棒の上に立つ（少し小さめ）
            q["h"], q["w"] = 300, 300
            q["bottom"] = int(hb[2] - (1290 - hb[2]) + 40)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}昔と今", 120, Wd.BLACK, 95), ("{y}物価はどれだけ上がった？", 100, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_50_bukka.mp4"), os.path.join(Wd.HERE, "out", "short_50_bukka_preview"))
