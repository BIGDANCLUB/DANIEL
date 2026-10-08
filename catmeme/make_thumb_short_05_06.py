"""5本目のショート2本・6本目のショート1本のサムネ（縦 1080x1920）。

python3 catmeme/make_thumb_short_05_06.py → thumbs/short_05a_what.png, short_05b_cure.png, short_06_zetsubou.png
作りは make_thumb_short_04.py と同じ（いちばん上に話題の帯／大きなタイトル／真ん中の札／下に猫2匹とひとこと）。
注意：5本目は亡くなった方がいるので、ふざけたひとことは入れない。6本目は本人・家族をバカにしない。
"""
from PIL import Image, ImageDraw

import parts as P
from make_thumb_03 import fit_text
from make_thumb_short_04 import BLACK, NAVY, RED, W, WHITE, YELLOW, base, cats, save, topic_band, words


def board(img, text, y, fill, fg, size, rot):
    """真ん中の大きな札（\\n で改行）。"""
    f = P.font("black", size)
    lines = text.split("\n")
    bw, bh = 1000, int(size * 1.25 * len(lines)) + 50
    b = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    bd = ImageDraw.Draw(b)
    bd.rounded_rectangle((0, 0, bw - 1, bh - 1), 28, fill=fill, outline=BLACK if fill == WHITE else WHITE, width=9)
    for n, t in enumerate(lines):
        bd.text((bw / 2, 25 + size * 0.62 + n * size * 1.25), t, font=f, fill=fg, anchor="mm")
    b = b.rotate(rot, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(b, (int(W / 2 - b.width / 2), y))


def thumb_5a():
    img = base("bg11_tsukuba", ((150, 40, 40, 140), (70, 70, 110, 130)), bg_dir="01_todai")
    d = ImageDraw.Draw(img)
    topic_band(img, "ロシア・ペスト研究所")
    fit_text(d, (W / 2, 330), "令和のペスト？　200人隔離", 1030, 110, WHITE, BLACK, double=None)
    fit_text(d, (W / 2, 520), "何が起きた⁉", 1040, 190, YELLOW, BLACK, double=WHITE)
    board(img, "ロシア当局\n「ペストは検出されず」\n⇒本当か？", 640, WHITE, NAVY, 86, -2)
    cats(img, ("surprise_big_pupils_cat", 0.6, False), ("think_bike_front_seat_cat", 1.0, True))
    words(img, [("じゃあ何が…？", 250, 1250, 80, WHITE, 8)])
    save(img, "short_05a_what")


def thumb_5b():
    img = base("bg10_kyoto", ((255, 60, 60, 140), (255, 210, 0, 120)), bg_dir="01_todai")
    d = ImageDraw.Draw(img)
    topic_band(img, "ロシア・ペスト研究所")
    fit_text(d, (W / 2, 330), "黒死病のペストって", 1030, 120, WHITE, BLACK, double=None)
    fit_text(d, (W / 2, 520), "今も治るの⁉", 1040, 190, YELLOW, BLACK, double=WHITE)
    board(img, "抗生物質で\n治療できる", 660, RED, WHITE, 120, -2)
    cats(img, ("weird_meowing_cat", 1.0, False), ("calm_black_face_sheep", 0.5, True))
    words(img, [("治るの！？", 250, 1250, 100, WHITE, 8), ("日本は100年\n発生なし", 800, 1260, 76, RED, -8)])
    save(img, "short_05b_cure")


def thumb_6():
    img = base("bg14_home_night", ((255, 60, 60, 150), (255, 210, 0, 130)), bg_dir="02_october")
    d = ImageDraw.Draw(img)
    topic_band(img, "絶望ライン工　炎上")
    fit_text(d, (W / 2, 330), "「年収240万・独身」が", 1030, 120, WHITE, BLACK, double=None)
    fit_text(d, (W / 2, 520), "実は既婚⁉", 1040, 200, YELLOW, BLACK, double=WHITE)
    board(img, "“独身の休日”の\n4日後に結婚報告", 660, RED, WHITE, 104, -2)
    cats(img, ("surprise_big_pupils_cat", 0.6, False), ("huh_huh_cat", 1.0, True))
    words(img, [("4日後！？", 250, 1250, 110, WHITE, 8), ("なぜ炎上？", 800, 1260, 96, RED, -8)])
    save(img, "short_06_zetsubou")


if __name__ == "__main__":
    thumb_5a()
    thumb_5b()
    thumb_6()
