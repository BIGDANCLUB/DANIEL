"""ショート121用：スマホの残高画面の絵（自作・実在の銀行名やロゴは使わない）→ backgrounds/shorts_pic/pic_bank_<金額>.png（透過）"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(HERE, "fonts", "NotoSansJP[wght].ttf")


def font(size, w=800):
    f = ImageFont.truetype(F, size)
    try:
        f.set_variation_by_axes([w])
    except Exception:
        pass
    return f


def make(yen):
    Wp, Hp = 520, 860
    im = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, Wp - 1, Hp - 1), 64, fill=(30, 30, 34, 255))          # 本体
    d.rounded_rectangle((18, 18, Wp - 19, Hp - 19), 50, fill=(246, 248, 252, 255))   # 画面
    d.rounded_rectangle((Wp / 2 - 70, 34, Wp / 2 + 70, 62), 14, fill=(30, 30, 34, 255))  # カメラ
    d.rounded_rectangle((18, 90, Wp - 19, 210), 0, fill=(40, 120, 200, 255))
    d.text((Wp / 2, 150), "マイ口座", font=font(46), fill="white", anchor="mm")
    d.text((Wp / 2, 300), "残高", font=font(52, 600), fill=(90, 90, 100), anchor="mm")
    col = (20, 20, 30) if yen >= 50000 else (210, 30, 30)
    s = "¥{:,}".format(yen)
    size = 96
    while font(size).getlength(s) > Wp - 70:
        size -= 4
    d.text((Wp / 2, 410), s, font=font(size, 900), fill=col, anchor="mm")
    d.line((50, 500, Wp - 50, 500), fill=(210, 214, 222), width=3)
    for i, lab in enumerate(["入金", "振込", "明細"]):
        x = 105 + i * 155
        d.rounded_rectangle((x - 62, 560, x + 62, 680), 24, fill=(225, 233, 245))
        d.text((x, 620), lab, font=font(36, 700), fill=(40, 120, 200), anchor="mm")
    d.rounded_rectangle((Wp / 2 - 90, Hp - 50, Wp / 2 + 90, Hp - 40), 5, fill=(30, 30, 34))
    out = os.path.join(HERE, "backgrounds", "shorts_pic", "pic_bank_%d.png" % yen)
    im.save(out)
    return out


if __name__ == "__main__":
    for y in (220000, 150000, 98000, 82000, 76000, 61000, 38000, 21000, 8000, 1200):
        print(make(y))
