"""シリーズ「ネットで生まれた名フレーズ」ショートのサムネ（縦 1080x1920）。

python3 catmeme/make_thumb_short_meme.py → thumbs/short_meme_<キー>.png
作りは make_thumb_short_05_06.py と同じ（いちばん上に「ネットで生まれた名フレーズ」の帯／小さな前置き／大きなフレーズ／札／猫2匹）。
"""
from PIL import ImageDraw

from make_thumb_03 import fit_text
from make_thumb_short_04 import BLACK, NAVY, RED, W, WHITE, YELLOW, base, cats, save, topic_band, words
from make_thumb_short_05_06 import board

RAYS = ((255, 60, 60, 150), (255, 210, 0, 130))
THUMBS = {
    # キー: (背景フォルダ, 背景, 前置き, フレーズ, 札, 札の色, 左の猫, 右の猫, ひとこと)
    "todai": ("01_todai", "bg01_campus", "東大の総長選で生まれた", "553＞1107", "票が少ないほうが\n勝った⁉", RED,
              ("huh_huh_cat", 1.0, False), ("surprise_big_pupils_cat", 0.6, True), [("は？", 230, 1250, 130, WHITE, 10),
                                                                                   ("算数どこいった", 800, 1260, 70, RED, -8)]),
    "kome": ("02_october", "bg16_food_aisle", "令和の米騒動で生まれた", "古古古米", "「古」いくつ\n付くの⁉", RED,
             ("weird_meowing_cat", 1.0, False), ("eat_pop_cat", 0.5, True), [("古古古古米！？", 290, 1250, 70, WHITE, 8),
                                                                                       ("味は普通？", 820, 1260, 84, RED, -8)]),
    "toilet": ("01_todai", "bg06_spotlight", "大阪・関西万博で生まれた", "2億円トイレ", "本当に\n2億円だった⁉", RED,
               ("surprise_big_pupils_cat", 0.6, False), ("huh_huh_cat", 1.0, True), [("2億！？", 280, 1250, 110, WHITE, 8),
                                                                                    ("実は46基", 820, 1260, 90, RED, -8)]),
    "tanishi": ("02_october", "bg18_backyard", "SNSで広まった", "ジャンボ\nタニシ農法", "農水省が\n「やめて」⁉", RED,
                ("huh_huh_cat", 1.0, False), ("weird_meowing_cat", 1.0, True), [("農法！？", 280, 1250, 100, WHITE, 8),
                                                                               ("国が止めた", 820, 1260, 84, RED, -8)]),
    "noriben": ("02_october", "bg15_convenience", "黒塗りの公文書を", "のり弁", "国の書類が\n真っ黒⁉", NAVY,
                ("surprise_big_pupils_cat", 0.6, False), ("huh_huh_cat", 1.0, True), [("読めない！？", 290, 1250, 84, WHITE, 8),
                                                                                     ("おかずは？", 820, 1260, 90, RED, -8)]),
    "goto": ("03_kodomo_nisa", "bg20_counter", "GoToトラベルが", "GoTo\nトラブル", "変更につぐ\n変更⁉", RED,
             ("weird_meowing_cat", 1.0, False), ("huh_huh_cat", 1.0, True), [("また変更！？", 290, 1250, 84, WHITE, 8),
                                                                            ("1文字ちがい", 790, 1260, 76, RED, -8)]),
}


def make(key):
    bg_dir, bg, pre, phrase, note, col, left, right, wds = THUMBS[key]
    img = base(bg, RAYS, bg_dir=bg_dir)
    d = ImageDraw.Draw(img)
    topic_band(img, "ネットで生まれた名フレーズ")
    fit_text(d, (W / 2, 320), pre, 1000, 100, WHITE, BLACK, double=None)
    lines = phrase.split("\n")
    if len(lines) == 1:
        fit_text(d, (W / 2, 510), phrase, 1040, 230, YELLOW, BLACK, double=WHITE)
        y_board = 680
    else:
        for i, ln in enumerate(lines):
            fit_text(d, (W / 2, 480 + i * 190), ln, 1040, 180, YELLOW, BLACK, double=WHITE)
        y_board = 800
    board(img, note, y_board, col, WHITE, 96, -2)
    cats(img, left, right)
    words(img, wds)
    save(img, "short_meme_" + key)


if __name__ == "__main__":
    for k in THUMBS:
        make(k)
