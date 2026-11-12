"""自堕落シリーズ #18 ガストひとり飲みのサムネ（11/12）。いつものAパターンで文言3案。

python3 catmeme/make_thumb_gusto.py → thumbs/jidaraku_18_gusto_thumb_a1〜a3.png
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S

for d in (os.path.join("jidaraku", "18_gusto"), "jidaraku"):
    S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", d))
R, BK = T.RED, T.BLACK


def main():
    L = ("happy_hamster_open_arms", 1.0, 125, 410, 280, False)
    for name, left, right, rc, l1, l2 in [
        ("a1", "gs01_front", "f_karaage", "rizz_cat_rizz",
         [("サイゼ", BK), ("だけじゃない", R)], [("ガスト飲み", R), ("がオトクすぎる", BK)]),
        ("a2", "gs02_seat", "f_wine", "showoff_gojo_cosplay_cat",
         [("18時前", R), ("に入るのが", BK)], [("クレバーな", BK), ("ひとり飲み", R)]),
        ("a3", "gs02_seat", "f_karaage", "angry_aiming_cat",
         [("から好しの唐揚げ", R)], [("反則", R), ("のうまさだった", BK)]),
    ]:
        T.type_a("jidaraku_18_gusto_thumb_%s.png" % name, left, right, L, [(rc, 1.0, 1170, 410, 300, False)],
                 "30代独身　ひとりガスト飲み", l1, l2, split=640, size=108)


if __name__ == "__main__":
    main()
