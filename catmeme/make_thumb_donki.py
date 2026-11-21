"""自堕落シリーズ #25 ドン・キホーテのサムネ案（11/21）。吉野家・競馬回と同じ形：
写真を全面・左に猫・右上に白ふちの商品写真・黄色い角丸の帯に赤い太字・帯の上に白地の札。

python3 catmeme/make_thumb_donki.py → thumbs/jidaraku_25_donki_thumb_c1〜c3.png
"""
import os

import make_thumb_long_ref as T
import make_thumb_short_ref as S
import make_thumb_yoshinoya as Y

S.BGS.insert(0, os.path.join(T.HERE, "backgrounds", "jidaraku", "25_donki"))


def main():
    Y.one("jidaraku_25_donki_thumb_c1.png", "dk01_front", "surprise_big_pupils_cat", "歯ブラシだけのはずが", tag="30代独身　休日の夜", item="dk06_basket")
    Y.one("jidaraku_25_donki_thumb_c2.png", "dk02_aisle", "happy_hamster_open_arms", "ドンキは大人の遊園地", tag="30代独身　予定なし", item="f_blanket")
    Y.one("jidaraku_25_donki_thumb_c3.png", "dk01_front", "stare_tabby_wide_eyes_cat", "予定がない夜はドンキ", tag="30代独身", item="f_karaage")


if __name__ == "__main__":
    main()
