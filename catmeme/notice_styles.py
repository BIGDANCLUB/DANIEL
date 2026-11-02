"""冒頭の注意書き画面（11/2 ユーザー指定）：「今日のひとこと」＋ひとことを真ん中に大きく、下に小さく注意書き。3案。

import notice_styles as NS; NS.make("a", "推しは推せる時に推せ‼", ["※金額は…", ...]) → RGBA の画像（1920x1080）
猫は画面の下のはしに小さく並べる（注意書きの帯にかぶらないよう、帯の上に立たせる）。
"""
from PIL import Image, ImageDraw

import parts as P

W, H = P.W, P.H
NOTE_Y = 960   # 注意書きの帯の上はし


def _fit(text, maxw, size, kind="black", lo=40):
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    while size > lo and d.textlength(text, font=P.font(kind, size)) > maxw:
        size -= 4
    return P.font(kind, size), size


def _ctext(d, y, text, f, fill, stroke=0, sc=(0, 0, 0)):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=sc)


def _notes(img, notes, style):
    d = ImageDraw.Draw(img)
    if style == "band":
        d.rectangle((0, NOTE_Y, W, H), fill=(0, 0, 0, 170))
    f = P.font("round", 34)
    line = "　".join(notes)
    f, _ = _fit(line, W - 120, 34, "round", lo=20)
    _ctext(d, NOTE_Y + (H - NOTE_Y) / 2 - 22, line, f, (235, 235, 235), 4 if style != "band" else 0)


def make(style, text, notes):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f, s = _fit(text.split("\n")[0], W - 260, 150)
    if style == "a":   # 黄色の札＋大きな白文字（シンプル）
        tag = P.font("black", 64)
        tw = d.textlength("今日のひとこと", font=tag)
        d.rounded_rectangle(((W - tw) / 2 - 40, 250, (W + tw) / 2 + 40, 350), radius=24, fill=(255, 210, 40, 255),
                            outline=(0, 0, 0, 255), width=6)
        _ctext(d, 258, "今日のひとこと", tag, (30, 30, 30))
        _ctext(d, 470, text, f, (255, 255, 255), 12)
        _notes(img, notes, "band")
    elif style == "b":   # 白いカード＋赤い見出し（黒板・掲示風）
        x0, y0, x1, y1 = 150, 200, W - 150, 820
        d.rounded_rectangle((x0 + 12, y0 + 14, x1 + 12, y1 + 14), radius=40, fill=(0, 0, 0, 110))
        d.rounded_rectangle((x0, y0, x1, y1), radius=40, fill=(255, 253, 245, 250), outline=(40, 40, 40, 255), width=6)
        d.rounded_rectangle((x0, y0, x1, y0 + 130), radius=40, fill=(220, 50, 50, 255))
        d.rectangle((x0, y0 + 90, x1, y0 + 130), fill=(220, 50, 50, 255))
        _ctext(d, y0 + 24, "今日のひとこと", P.font("black", 70), (255, 255, 255))
        f, s = _fit(text, x1 - x0 - 120, 140)
        _ctext(d, (y0 + 130 + y1) / 2 - s * 0.62, text, f, (30, 30, 30))
        _notes(img, notes, "plain")
    else:   # c：ななめの黒×黄の帯（ショート51のbと同じ雰囲気）
        band = Image.new("RGBA", (W + 400, 330), (0, 0, 0, 0))
        bd = ImageDraw.Draw(band)
        bd.rectangle((0, 0, W + 400, 330), fill=(20, 20, 20, 240))
        bd.rectangle((0, 0, W + 400, 22), fill=(255, 210, 40, 255))
        bd.rectangle((0, 308, W + 400, 330), fill=(255, 210, 40, 255))
        band = band.rotate(4, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(band, ((W - band.width) // 2, 440 - band.height // 2 + 40))
        tag = P.font("black", 60)
        tw = d.textlength("今日のひとこと", font=tag)
        rib = Image.new("RGBA", (int(tw + 90), 100), (0, 0, 0, 0))
        rd = ImageDraw.Draw(rib)
        rd.polygon([(0, 0), (rib.width, 0), (rib.width - 30, 100), (30, 100)], fill=(220, 40, 40, 255))
        rd.text((45, 14), "今日のひとこと", font=tag, fill=(255, 255, 255))
        rib = rib.rotate(4, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(rib, (230, 215))
        txt = Image.new("RGBA", (W, 240), (0, 0, 0, 0))
        _d = ImageDraw.Draw(txt)
        w = _d.textlength(text, font=f)
        _d.text(((W - w) / 2, 20), text, font=f, fill=(255, 225, 60), stroke_width=8, stroke_fill=(0, 0, 0))
        txt = txt.rotate(4, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(txt, ((W - txt.width) // 2, 480 - txt.height // 2))
        _notes(img, notes, "band")
    return img


def make_end(style, text, notes, top="チャンネル登録お願いします！"):
    """エンディング画面（11/2 ユーザー指定）：上に「チャンネル登録お願いします！」（中くらい）・まん中に今日のひとこと（大きく）・下に注意書き（小さく）。3案。"""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f, s = _fit(text.split("\n")[0], W - 260, 150)
    if style == "a":   # 赤い登録ボタン風の帯＋黄色の札＋白い大文字
        tf = P.font("black", 78)
        tw = d.textlength(top, font=tf)
        d.rounded_rectangle(((W - tw) / 2 - 60, 90, (W + tw) / 2 + 60, 210), radius=60, fill=(230, 33, 23, 255),
                            outline=(255, 255, 255, 255), width=6)
        _ctext(d, 103, top, tf, (255, 255, 255))
        tag = P.font("black", 56)
        gw = d.textlength("今日のひとこと", font=tag)
        d.rounded_rectangle(((W - gw) / 2 - 36, 330, (W + gw) / 2 + 36, 418), radius=22, fill=(255, 210, 40, 255),
                            outline=(0, 0, 0, 255), width=6)
        _ctext(d, 337, "今日のひとこと", tag, (30, 30, 30))
        lines = text.split("\n")
        if len(lines) == 1:
            _ctext(d, 490, text, f, (255, 255, 255), 12)
        else:   # 2行（2行目は少し小さく）
            f1, s1 = _fit(lines[0], W - 220, 130)
            f2, s2 = _fit(lines[1], W - 220, 130)
            _ctext(d, 455, lines[0], f1, (255, 255, 255), 12)
            _ctext(d, 455 + s1 * 1.25, lines[1], f2, (255, 255, 255), 12)
        _notes(img, notes, "band")
    elif style == "b":   # 上は白文字＋黄色の下線、まん中は黄色の大文字
        tf = P.font("black", 84)
        tw = d.textlength(top, font=tf)
        d.rectangle(((W - tw) / 2, 205, (W + tw) / 2, 228), fill=(255, 210, 40, 255))
        _ctext(d, 100, top, tf, (255, 255, 255), 9)
        _ctext(d, 350, "今日のひとこと", P.font("black", 56), (255, 230, 120), 7)
        _ctext(d, 460, text, f, (255, 220, 50), 12)
        _notes(img, notes, "band")
    else:   # c：上は登録ボタン＋「お願いします！」、まん中は白いカード
        bf = P.font("black", 70)
        bt = "チャンネル登録"
        bw = d.textlength(bt, font=bf)
        rest = top.replace(bt, "")
        rf = P.font("black", 70)
        rw = d.textlength(rest, font=rf)
        x0 = (W - (bw + 80 + 24 + rw)) / 2
        d.rounded_rectangle((x0, 90, x0 + bw + 80, 200), radius=18, fill=(230, 33, 23, 255))
        d.text((x0 + 40, 103), bt, font=bf, fill=(255, 255, 255))
        d.text((x0 + bw + 104, 103), rest, font=rf, fill=(255, 255, 255), stroke_width=8, stroke_fill=(0, 0, 0))
        x0, y0, x1, y1 = 170, 270, W - 170, 860
        d.rounded_rectangle((x0 + 12, y0 + 14, x1 + 12, y1 + 14), radius=40, fill=(0, 0, 0, 110))
        d.rounded_rectangle((x0, y0, x1, y1), radius=40, fill=(255, 253, 245, 250), outline=(40, 40, 40, 255), width=6)
        _ctext(d, y0 + 40, "今日のひとこと", P.font("black", 64), (220, 50, 50))
        f2, s2 = _fit(text, x1 - x0 - 120, 140)
        _ctext(d, (y0 + 130 + y1) / 2 - s2 * 0.62, text, f2, (30, 30, 30))
        _notes(img, notes, "band")
    return img
