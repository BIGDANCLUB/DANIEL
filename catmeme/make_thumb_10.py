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

# ユーザー指定の文言（10/11）：「IDCF、7時間ハッキングに気づいていないことをハッカーにばらされるｗｗｗ」
THUMB_C = dict(THUMB, top="IDCF、7時間ハッキングに気づいていないことを", big="ハッカーにばらされる", sub="ｗｗｗ",
               stickers=(("YOUR CLOUD IS OURS.", 640, 520, 44, (90, 255, 120), (12, 14, 16), -2),
                         ("※「7時間気づいていない」はハッカーの主張", 690, 605, 32, NAVY, YELLOW, 2)))
# 10/11 ユーザー指定：赤帯なし・文言を全部入れる（少し小さくてよい）・ｗｗｗあり・「ハッカーの主張」の札はなし（概要欄でカバー）
BLACK = (0, 0, 0)
THUMB_E = dict(THUMB, top="", big="", sub="",
               stickers=(("YOUR CLOUD IS OURS.", 640, 470, 44, (90, 255, 120), (12, 14, 16), -2),),
               cat_h=380,   # 猫の顔に文字が被らないよう、猫を小さめにして文字を上に寄せる（10/11）
               lines=(("IDCF、7時間ハッキングに", 66, 92, YELLOW, BLACK, WHITE),
                      ("気づいていないことを", 170, 92, YELLOW, BLACK, WHITE),
                      ("ハッカーに報告されるwww", 274, 92, YELLOW, BLACK, WHITE)))
# 同じ文言から「ｗｗｗ」だけ外した案（被害を受けた会社を笑う形にしない）
THUMB_D = dict(THUMB_C, sub="", big="ハッカーにばらされる")

if __name__ == "__main__":
    make(os.path.join(HERE, "thumbs", "10_idcf.png"), **THUMB)
    make(os.path.join(HERE, "thumbs", "10_idcf_c.png"), **THUMB_C)
    make(os.path.join(HERE, "thumbs", "10_idcf_d.png"), **THUMB_D)
    make(os.path.join(HERE, "thumbs", "10_idcf_e.png"), **THUMB_E)
