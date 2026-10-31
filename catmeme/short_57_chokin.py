"""ショート57：年代別 みんなの貯金はいくら？ 平均と中央値（world_short.py の左右くらべ・昔と今の物価と同じ作り・10/31 ユーザー指定）。59.9秒。

python3 catmeme/short_57_chokin.py → out/short_57_chokin.mp4
- 年代ごとに「札だけ → 左に『平均』の棒と猫 → 右に『中央値』の棒と猫（左は残る）」の3段。平均は一部のお金持ちで高くなる、のずれで「えっ」となる
- 数字は単身世帯の金融資産保有額（金融資産を持っていない世帯もふくむ・2024年ごろの調査の目安）：
  20代 平均255万・中央値37万／30代 501万・100万／40代 859万・100万／50代 999万・120万／60代 1364万・300万／全体 919万・130万
- 中央値の棒が小さすぎて値段が読めないときは、読める高さまでのばす（グラフの比はざっくり）。BGM なし
"""
import os

import world_short as Wd

ST = "bg87_refund_money"
MAXH = 380
D = 59.9 / 6


def cuts():
    out = []
    # (年代, 平均, 中央値, 比, 平均の猫, 中央値の猫)
    rows = [
        ("20代", "255万円", "37万円", 37 / 255, "happy_chipi_chapa_cat", "sad_looking_away_tabby"),
        ("30代", "501万円", "100万円", 100 / 501, "money_counting_orange_cat", "stare_tabby_wide_eyes_cat"),
        ("40代", "859万円", "100万円", 100 / 859, "cocky_dj_cat", "despair_dramatic_kitten"),
        ("50代", "999万円", "120万円", 120 / 999, "showoff_gojo_cosplay_cat", "scream_phone_orange_cat"),
        ("60代", "1364万円", "300万円", 300 / 1364, "happy_hamster_open_arms", "surprise_big_pupils_cat"),
        ("単身の全体", "919万円", "130万円", 130 / 919, "dance_three_kittens", "realize_wet_cat_stare"),
    ]
    for item, avg, med, r, acat, mcat in rows:
        last = item == "単身の全体"
        ha, hm = MAXH, max(MAXH * r, 95)
        bar_a = ("bar:%d:yellow:%s" % (ha, avg), 275, 1290 - ha / 2, 300)
        bar_m = ("bar:%d:cred:%s" % (hm, med), 805, 1290 - hm / 2, 300)
        out.append(Wd.split(ST, item, dur=1.4, se=["explosion_chudoon"] if last else ["pi"]))
        c = Wd.split(ST, item, left=acat, cap="平均", cap_side="L", sound="L", dur=3.8, se=["pafu"])
        c["props"] = [bar_a]
        out.append(c)
        cap = "みんなも\n平均の数字に\n気をつけよう" if last else "平均の\n約%d分の1" % round(1 / r)
        c = Wd.split(ST, item, left=acat, right=mcat, cap=cap, cap_side="R", sound="R", dur=D - 5.2, se=["explosion_chudoon"])
        c["props"] = [bar_a, bar_m]
        out.append(c)
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460, heads=("平均", "中央値"))
        for q, hb in zip(c["cats"], [p_ for p_ in c.get("props", [])]):   # 猫は棒の上に立つ
            q["h"], q["w"] = 300, 300
            q["bottom"] = int(hb[2] - (1290 - hb[2]) + 40)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}年代別", 120, Wd.BLACK, 95), ("{y}みんなの貯金はいくら？", 100, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_57_chokin.mp4"), os.path.join(Wd.HERE, "out", "short_57_chokin_preview"))
