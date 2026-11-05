"""42本目（EVvsガソリン車 10年でいくら違う？）のサムネ候補3つ（11/5）。B を採用（11/5 ユーザー指定）。41と同じ A・B・C の3パターン。

python3 catmeme/make_thumb_42.py → thumbs/42_ev_thumb_a/b/c.png
"""
import glob
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "26_kuruma"))
S.BGS += sorted(x for x in glob.glob(os.path.join(T.HERE, "backgrounds", "*")) if os.path.isdir(x))
R, BK, Y, NV = T.RED, T.BLACK, T.YELLOW, T.NAVY


def main():
    T.type_a("42_ev_thumb_a.png", "bg26_car_dealer", "bg26_gas_station",
             ("think_chin_paw_orange_cat", 1.0, 300, 410, 320, False),
             [("surprise_big_pupils_cat", 1.0, 900, 410, 320, False), ("money_counting_orange_cat", 1.0, 1150, 410, 280, True)],
             "10年乗ったら",
             [("EV", T.TEAL if hasattr(T, "TEAL") else NV), ("vs", BK), ("ガソリン車", R)], [("安いのは", BK), ("ガソリン車!?", R)],
             split=600, size=110)
    T.type_b("42_ev_thumb_b.png",
             [("bg26_car_dealer", [("surprise_big_pupils_cat", 1.0, 160, 470, 320, False)]),
              ("bg26_gas_station", [("despair_dramatic_kitten", 0.8, 160, 470, 320, False)]),
              ("bg14_home_night", [("money_counting_orange_cat", 1.0, 160, 470, 320, False)]),
              ("bg26_rural_road", [("happy_hamster_open_arms", 1.0, 160, 470, 330, False)])],
             [("txt", "EVは80万高い", 160, 60, 38, Y, -6), ("txt", "ガソリン代は2倍", 480, 60, 36, Y, 4),
              ("txt", "充電器15万", 800, 60, 40, Y, -4), ("txt", "乗るほど差が縮む!?", 1120, 60, 36, R, 6)],
             [("EVとガソリン車", R)], [("10年でいくら違う？", NV)])
    T.type_c("42_ev_thumb_c.png", "bg26_car_dealer",
             [("surprise_big_pupils_cat", 1.0, 1040, 620, 470, False), ("think_chin_paw_orange_cat", 1.0, 250, 640, 360, False)],
             "EVとガソリン車　10年乗ってくらべると", "差は約40万!?", zoom=1.05)


if __name__ == "__main__":
    main()
