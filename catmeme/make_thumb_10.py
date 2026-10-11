"""10（IDCFクラウドのランサムウェア攻撃）のサムネ（横 1280x720）。作りは make_thumb_05_06.py と同じ。

python3 catmeme/make_thumb_10.py → thumbs/10_idcf.png
注意：「7時間気づいてない」はハッカーの主張なので、札で「ハッカーの主張」と必ず出す。運用担当者・会社をバカにしない。
"""
import os

from make_thumb_03 import make

HERE = os.path.dirname(os.path.abspath(__file__))
NEWS, HACK = (215, 35, 35), (30, 30, 30)
WHITE, YELLOW, RED, NAVY = (255, 255, 255), (255, 222, 0), (235, 25, 25), (25, 32, 56)

THUMB = dict(
    bg_dir="04_leak", bg="bg23_hacker_room", ray_cols=((40, 160, 70), (20, 20, 30)),
    left=("surprise_big_pupils_cat", 0.6, False, "ニュース猫", NEWS), right=("cocky_dj_cat", 1.0, True, "ハッカー猫", HACK),
    top="495の企業・自治体のクラウドが停止", big="7時間気づいてない", sub="ハッカーに煽られた!?", badge="",
    cat_h=470, tags=True,
    stickers=(("YOUR CLOUD IS OURS.", 640, 545, 44, (90, 255, 120), (12, 14, 16), -2),
              ("※ハッカーの主張", 640, 630, 36, NAVY, YELLOW, 2)),
    words=())

if __name__ == "__main__":
    make(os.path.join(HERE, "thumbs", "10_idcf.png"), **THUMB)
