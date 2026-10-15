"""長尺動画のサムネ：参考フォーマット（ユーザー指定 10/13）をマネして作る。横 1280x720。

参考3枚の作り
- A（「山本由伸の季節到来に…」型）：上6割は写真2枚（左にアップ、右に場面）。左の写真の下に白い札＋赤い文字の小見出しを少し傾けて。
  下4割は黄色の地に、黒い極太文字2行（大事な言葉だけ青・赤）、白い縁取り
- B（「ここは大人の遊園地だ！」型）：写真4枚を縦に切って横に並べる。赤い矢印と黄色の書き文字で写真の中を指す。
  下に白〜黄色のグラデーションの帯、赤い文字と紺の文字の2行、白い太縁＋影
- C（「全員日本に連れてけ」型）：写真を全面に。上の端の黒い帯に黄色い小さめの1行（黒縁）、下に黄色グラデーションの超巨大文字1行（黒い太縁）
- 右下（約1060〜1270, 640〜700）は再生時間の表示で隠れるので、大事な文字は置かない
- 猫ミームは写真の中に入れ込む

python3 catmeme/make_thumb_long_ref.py → thumbs/12_akaihane_ref_a.png / _b / _c
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import parts as P
from make_thumb_01 import cat_img
from make_thumb_short_ref import bg_path

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, YELLOW, BLUE, NAVY = (226, 30, 30), (255, 236, 40), (36, 90, 220), (20, 30, 110)


def fill_photo(name, w, h, cx=0.5, zoom=1.0):
    im = Image.open(bg_path(name)).convert("RGB")
    k = max(w / im.width, h / im.height) * zoom
    im = im.resize((int(im.width * k) + 1, int(im.height * k) + 1), Image.LANCZOS)
    x0 = int((im.width - w) * cx)
    y0 = (im.height - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h)).convert("RGBA")


def put_cat(img, name, t, x, bottom, h, flip=False):
    c = cat_img(name, t, h, flip)
    img.alpha_composite(c, (int(x - c.width / 2), int(bottom - c.height)))


def runs(parts, size, sw, max_w, shadow=False, grad=None):
    """色ちがいの文字を1行に並べる。parts=[(文字, 色)]。grad=(上の色, 下の色) で文字をグラデーションに。"""
    f = P.font("black", size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    while sum(d0.textlength(t, font=f) for t, _ in parts) > max_w - sw * 2 and size > 30:
        size -= 3
        f = P.font("black", size)
    tw = int(sum(d0.textlength(t, font=f) for t, _ in parts)) + sw * 2 + 20
    th = int(size * 1.3) + sw * 2
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = sw + 10
    for t, col in parts:
        stroke = col[1] if isinstance(col, tuple) and isinstance(col[0], tuple) else WHITE
        fill = col[0] if isinstance(col[0], tuple) else col
        if shadow:
            d.text((x + 6, sw + 6), t, font=f, fill=(0, 0, 0, 160), stroke_width=sw, stroke_fill=(0, 0, 0, 160))
        d.text((x, sw), t, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
        x += d.textlength(t, font=f)
    if grad:
        mask = Image.new("L", im.size, 0)
        md = ImageDraw.Draw(mask)
        x = sw + 10
        for t, _ in parts:
            md.text((x, sw), t, font=f, fill=255)
            x += d.textlength(t, font=f)
        g = Image.new("RGBA", im.size)
        gd = ImageDraw.Draw(g)
        for y in range(im.height):
            u = y / im.height
            gd.line((0, y, im.width, y), fill=tuple(int(a + (b - a) * u) for a, b in zip(grad[0], grad[1])) + (255,))
        im.paste(g, (0, 0), mask)
    return im.crop(im.getbbox())


def arrow(img, x0, y0, x1, y1, col=RED, w=22):
    d = ImageDraw.Draw(img)
    v = np.array([x1 - x0, y1 - y0], float)
    n = v / np.linalg.norm(v)
    p = np.array([-n[1], n[0]])
    tip = np.array([x1, y1])
    base = tip - n * 48
    d.line((x0, y0, *base), fill=WHITE, width=w + 10)
    d.line((x0, y0, *base), fill=col, width=w)
    tri = [tuple(tip + n * 6), tuple(base + p * 40), tuple(base - p * 40)]
    d.polygon([tuple(tip + n * 12), tuple(base + p * 48 - n * 6), tuple(base - p * 48 - n * 6)], fill=WHITE)
    d.polygon(tri, fill=col)


def scribble(img, text, x, y, size, col=YELLOW, angle=0):
    t = runs([(text, (col, BLACK))], size, max(6, size // 9), 900)
    t = t.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(t, (int(x - t.width / 2), int(y - t.height / 2)))


def save(img, name):
    p = os.path.join(HERE, "thumbs", name)
    img.convert("RGB").save(p)
    print("->", p)


def type_a(name, left_bg, right_bg, left_cat, right_cats, tag, line1, line2, split=500):
    """split＝左の写真の幅（人物の写真を大きく見せたい時は広げる）。"""
    img = Image.new("RGBA", (W, H), WHITE)
    top_h = 410
    img.alpha_composite(fill_photo(left_bg, split, top_h, cx=0.5), (0, 0))
    img.alpha_composite(fill_photo(right_bg, W - split - 4, top_h), (split + 4, 0))
    put_cat(img, *left_cat)
    for c in right_cats:
        put_cat(img, *c)
    # 小見出しの札
    t = runs([(tag, (RED, WHITE))], 52, 2, 640)
    box = Image.new("RGBA", (t.width + 50, t.height + 34), WHITE + (255,))
    ImageDraw.Draw(box).rectangle((0, 0, box.width - 1, box.height - 1), outline=BLACK, width=5)
    box.alpha_composite(t, (25, 17))
    box = box.rotate(2, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(box, (14, top_h - box.height + 40))
    # 下の黄色い地と2行
    ImageDraw.Draw(img).rectangle((0, top_h + 18, W, H), fill=(255, 245, 60, 255), outline=BLACK, width=6)
    l1 = runs(line1, 150, 8, W - 40)
    l2 = runs(line2, 150, 8, W - 40)
    img.alpha_composite(l1, ((W - l1.width) // 2, top_h + 40))
    img.alpha_composite(l2, ((W - l2.width) // 2, top_h + 50 + l1.height))
    save(img, name)


def type_b(name, panels, notes, line1, line2):
    img = Image.new("RGBA", (W, H), WHITE)
    pw = W // len(panels)
    for i, (bg, cats) in enumerate(panels):
        ph = fill_photo(bg, pw - 6, 470, cx=0.5)
        for c in cats:
            put_cat(ph, *c)
        img.alpha_composite(ph, (i * pw + 3, 0))
    for kind, *a in notes:
        if kind == "arrow":
            arrow(img, *a)
        else:
            scribble(img, *a)
    g = Image.new("RGBA", (W, H - 455))
    gd = ImageDraw.Draw(g)
    for y in range(g.height):
        u = y / g.height
        gd.line((0, y, W, y), fill=(255, 255, int(235 - 160 * u), 255))
    img.alpha_composite(g, (0, 455))
    l1 = runs(line1, 104, 9, W - 30, shadow=True)
    l2 = runs(line2, 104, 9, W - 30, shadow=True)
    gap = (H - 455 - l1.height - l2.height) // 3
    img.alpha_composite(l1, ((W - l1.width) // 2, 455 + gap))
    img.alpha_composite(l2, ((W - l2.width) // 2, 455 + gap * 2 + l1.height))
    save(img, name)


def type_c(name, bg, cats, top, big):
    img = fill_photo(bg, W, H)
    for c in cats:
        put_cat(img, *c)
    shade = Image.new("RGBA", (W, H))
    sd = ImageDraw.Draw(shade)
    for y in range(H):
        a = int(150 * max(0, (y - 420) / 300))
        sd.line((0, y, W, y), fill=(0, 0, 0, a))
    img.alpha_composite(shade)
    t = runs([(top, (YELLOW, BLACK))], 64, 6, W - 30)
    ImageDraw.Draw(img).rectangle((0, 0, W, t.height + 22), fill=BLACK + (255,))   # 上の1行は黒い帯にのせる（参考どおり・10/13）
    img.alpha_composite(t, ((W - t.width) // 2, 11))
    b = runs([(big, (YELLOW, BLACK))], 230, 12, W - 40, grad=((255, 250, 210), (245, 200, 30)))
    img.alpha_composite(b, ((W - b.width) // 2, H - b.height - 22))
    save(img, name)


def akaihane():
    """12本目（赤い羽根）で3案。元事務局長は描かない。"""
    type_a("12_akaihane_ref_a.png", "bg35_akaihane_box", "bg36_akaihane_bow",
           ("surprise_big_pupils_cat", 0.6, 480, 330, 200, False),
           [("sad_banana_cat_cry", 1.0, 1180, 410, 300, True)],
           "国税が来て初めて発覚…",
           [("赤い羽根募金", BLACK), ("2.5億円", BLUE)], [("が行方不明になっていた", RED)])   # 何が起きたか分かる文言に（10/13 ユーザー指定）
    type_b("12_akaihane_ref_b.png",
           [("bg36_akaihane_bow", [("huh_huh_cat", 1.0, 160, 470, 300, False)]),
            ("bg35_akaihane_box", [("sad_banana_cat_cry", 1.0, 160, 470, 300, False)]),
            ("bg37_akaihane_hands", [("glare_disgusted_cat", 1.0, 160, 470, 300, False)]),
            ("bg21_school_gate", [("sad_black_dog", 1.0, 160, 470, 330, False)])],
           [("txt", "!!", 110, 130, 140, RED, -8), ("txt", "羽根なし!!", 120, 330, 48, YELLOW, -6),
            ("arrow", 420, 110, 500, 200), ("txt", "お釣り入れてたのに", 470, 330, 38, YELLOW, 4),
            ("arrow", 860, 110, 900, 230), ("txt", "1人で管理!?", 820, 60, 46, YELLOW, -4),
            ("txt", "お弁当半分…", 1130, 260, 40, YELLOW, 6)],
           [("赤い羽根2.5億円が", RED)], [("行方不明に大激怒", NAVY)])
    type_c("12_akaihane_ref_c.png", "bg34_akaihane_full",
           [("surprise_big_pupils_cat", 0.6, 960, 560, 330, False)],
           "赤い羽根2.5億円が行方不明 通帳も印鑑も1人で管理", "善意どこ行った")


if __name__ == "__main__" and os.environ.get("THUMB", "12") == "12":
    akaihane()


def yard():
    """13本目（盗難ハイエース・ヤード）で3案。逮捕された人は描かない。背景は 10/13 ユーザー提供の写真（backgrounds/13_yard）。猫はニュース猫と車を盗まれた猫。"""
    type_a("13_yard_ref_a.png", "bg39_hiace_black_garage", "bg41_yard_scrap",
           ("surprise_big_pupils_cat", 0.6, 250, 470, 520, False),
           [("sad_banana_cat_cry", 1.0, 760, 410, 330, True), ("glare_disgusted_cat", 1.0, 1080, 410, 300, True)],
           "条例違反は30万円…",
           [("盗難ハイエース", BLACK), ("300台", BLUE)], [("塀の中で解体し海外へ", RED)])
    type_b("13_yard_ref_b.png",
           [("bg39_hiace_black_garage", [("sad_banana_cat_cry", 1.0, 160, 470, 360, False)]),
            ("bg42_yard_raid_ai", [("huh_huh_cat", 1.0, 160, 470, 360, False)]),
            ("bg41_yard_scrap", [("glare_disgusted_cat", 1.0, 160, 470, 340, False)]),
            ("bg26_phone_alert", [("sad_black_dog", 1.0, 160, 470, 330, False)])],
           [("txt", "車がない…", 160, 60, 46, YELLOW, -6), ("txt", "!!", 420, 130, 110, RED, 8),
            ("txt", "容疑は1台!?", 480, 330, 44, YELLOW, 4), ("arrow", 860, 110, 900, 230),
            ("txt", "条例違反30万円", 820, 60, 44, YELLOW, -4), ("txt", "自分で探す…", 1130, 260, 40, YELLOW, 6)],
           [("盗難車300台が塀の中へ", RED)], [("日本は盗難天国なのか", NAVY)])
    type_c("13_yard_ref_c.png", "bg42_yard_raid_ai",
           [("surprise_big_pupils_cat", 0.6, 250, 560, 500, False), ("sad_banana_cat_cry", 1.0, 660, 560, 470, True),
            ("rage_talking_cat", 1.0, 1040, 560, 470, True)],
           "盗難ハイエース300台が塀の中で解体され海外へ", "日本ナメられすぎ")


if __name__ == "__main__" and os.environ.get("THUMB") == "13":
    yard()


def japan():
    """14本目（日本が世界で最も魅力的な国 4年連続1位）で3案。背景は AI 生成のイラスト（backgrounds/14_japan）。"""
    type_a("14_japan_ref_a.png", "bg59_sakura_park", "bg46_sushi_counter",
           ("surprise_big_pupils_cat", 0.6, 250, 470, 520, False),
           [("excited_hodomoe_city_cat", 1.0, 760, 410, 330, True), ("happy_girlfriend_dance_cat", 0.5, 1080, 410, 300, True)],
           "米旅行誌の読者投票",
           [("日本が世界1位", BLACK), ("4年連続", RED)], [("海外が驚く“当たり前”", BLUE)])
    type_b("14_japan_ref_b.png",
           [("bg46_sushi_counter", [("excited_hodomoe_city_cat", 1.0, 160, 470, 360, False)]),
            ("bg49_public_toilet", [("huh_huh_cat", 1.0, 160, 470, 360, False)]),
            ("bg52_koban", [("surprise_big_pupils_cat", 0.6, 160, 470, 340, False)]),
            ("bg65_crowded_kyoto", [("sad_banana_cat_cry", 1.0, 160, 470, 330, False)])],
           [("txt", "満足度96.9%", 160, 60, 44, YELLOW, -6), ("txt", "ゴミ箱どこ!?", 480, 70, 44, YELLOW, 4),
            ("txt", "財布が戻る!!", 800, 330, 44, YELLOW, -4), ("arrow", 860, 110, 900, 230),
            ("txt", "混雑は不満…", 1130, 260, 40, YELLOW, 6)],
           [("世界で最も魅力的な国", RED)], [("日本が4年連続1位", NAVY)])
    type_c("14_japan_ref_c.png", "bg59_sakura_park",
           [("surprise_big_pupils_cat", 0.6, 250, 560, 500, False), ("excited_hodomoe_city_cat", 1.0, 660, 560, 470, True),
            ("happy_girlfriend_dance_cat", 0.5, 1040, 560, 470, True)],
           "米旅行誌の読者投票で日本が4年連続世界1位", "なぜ日本なの？")


if __name__ == "__main__" and os.environ.get("THUMB") == "14":
    japan()


def vambi():
    """15本目（ヴァンビの経歴と逮捕報道）で3案。本人・関係者の写真や似顔絵は使わない。背景は AI 生成（backgrounds/15_vambi）。
    逮捕は容疑の段階なので、有罪のように見える言葉は使わない。"""
    type_a("15_vambi_ref_a.png", "bg80_counter_rocket", "bg76_roppongi_night",
           ("surprise_big_pupils_cat", 0.6, 250, 470, 520, False),
           [("huh_huh_cat", 1.0, 760, 410, 330, True), ("peek_what_happen_cat", 1.0, 1080, 410, 300, True)],
           "日本人最速1,000万人",
           [("人気YouTuber", BLACK), ("ヴァンビ", RED)], [("成功から逮捕報道まで", BLUE)])
    type_b("15_vambi_ref_b.png",
           [("bg69_vkei_stage", [("surprise_big_pupils_cat", 0.6, 160, 470, 340, False)]),
            ("bg71_wedding_chapel", [("huh_huh_cat", 1.0, 160, 470, 360, False)]),
            ("bg80_counter_rocket", [("excited_hodomoe_city_cat", 1.0, 160, 470, 360, False)]),
            ("bg77_police_station", [("peek_what_happen_cat", 1.0, 160, 470, 340, False)])],
           [("txt", "元バンドマン", 160, 60, 44, YELLOW, -6), ("txt", "結婚企画で炎上", 480, 70, 42, YELLOW, 4),
            ("txt", "1,000万人!!", 800, 330, 46, YELLOW, -4), ("arrow", 860, 110, 900, 230),
            ("txt", "逮捕報道…", 1130, 260, 42, YELLOW, 6)],
           [("ヴァンビの経歴", RED)], [("成功と騒動のくり返し", NAVY)])
    type_c("15_vambi_ref_c.png", "bg76_roppongi_night",
           [("surprise_big_pupils_cat", 0.6, 250, 560, 500, False), ("huh_huh_cat", 1.0, 660, 560, 470, True),
            ("peek_what_happen_cat", 1.0, 1040, 560, 470, True)],
           "登録者1,000万人のYouTuberヴァンビ 逮捕報道と事務所退所", "何があった？")


if __name__ == "__main__" and os.environ.get("THUMB") == "15":
    vambi()


def tenchim():
    """16本目（てんちむ モテフィット裁判の逆転）で3案。背景はユーザー提供の本人の写真（backgrounds/16_tenchim）。
    猫は顔にかけない。控訴審の結果は本人の報告なので「確定」とは書かない。"""
    type_a("16_tenchim_ref_a.png", "bg81_tenchim_neon", "bg84_courthouse",
           ("surprise_big_pupils_cat", 0.6, 90, 470, 300, False),
           [("huh_huh_cat", 1.0, 1130, 410, 300, True)],
           "ナイトブラ裁判",
           [("てんちむ3.8億円賠償", BLACK), ("が0円に", RED)], [("控訴審で支払い命令取り消し", BLUE)], split=780)
    type_b("16_tenchim_ref_b.png",
           [("bg82_tenchim_feather", []),
            ("bg87_refund_money", [("surprise_big_pupils_cat", 0.6, 160, 470, 340, False)]),
            ("bg84_courthouse", [("sad_banana_cat_cry", 1.0, 160, 470, 330, False)]),
            ("bg85_courtroom", [("excited_hodomoe_city_cat", 1.0, 160, 470, 360, False)])],
           [("txt", "豊胸隠し発覚", 160, 330, 42, YELLOW, -6), ("txt", "自腹で返金", 480, 70, 44, YELLOW, 4),
            ("txt", "一審3.8億円…", 800, 70, 42, YELLOW, -4), ("arrow", 860, 110, 900, 230),
            ("txt", "逆転!!", 1130, 260, 54, RED, 6)],
           [("3億8,000万円が0円に", RED)], [("てんちむ　6年越しの逆転", NAVY)])
    type_c("16_tenchim_ref_c.png", "bg81_tenchim_neon",
           [("surprise_big_pupils_cat", 0.6, 170, 560, 420, False), ("huh_huh_cat", 1.0, 1130, 560, 420, True)],
           "てんちむ ナイトブラ裁判 3億8,000万円の支払い命令が控訴審で取り消し", "まさかの逆転")


if __name__ == "__main__" and os.environ.get("THUMB") == "16":
    tenchim()


def imamori():
    """17本目（今森茉耶）で3案。ユーザー提供の写真（backgrounds/17_imamori/photos）。猫は顔にかけない。疑惑は疑惑と書く。"""
    type_a("17_imamori_ref_a.png", "p5_event_smile", "p1_cast_and_hero",
           ("stare_big_eyes_tabby_kitten", 1.0, 90, 470, 300, False),
           [("stare_interviewer_cat", 1.0, 1200, 410, 280, True)],
           "元戦隊ヒロイン",
           [("再出発からわずか", BLACK), ("6日", RED)], [("今森茉耶がSNS発信休止", BLUE)], split=700)
    type_b("17_imamori_ref_b.png",
           [("p2_missmagazine_gp", []),
            ("p1_cast_and_hero", []),
            ("bg98_izakaya_night", [("sad_banana_cat_cry", 1.0, 160, 470, 330, False)]),
            ("bg101_phone_chat", [("realize_wet_cat_stare", 1.0, 160, 470, 340, False)])],
           [("txt", "ミスマガGP", 160, 330, 44, YELLOW, -6), ("txt", "戦隊ヒロイン", 480, 330, 42, YELLOW, 4),
            ("txt", "20歳未満飲酒で降板", 800, 60, 38, YELLOW, -4), ("arrow", 860, 110, 900, 230),
            ("txt", "発信休止…", 1130, 60, 44, YELLOW, 6)],
           [("元戦隊ヒロインの1年", RED)], [("今森茉耶に何があった？", NAVY)])
    type_c("17_imamori_ref_c.png", "p5_event_smile",
           [("stare_big_eyes_tabby_kitten", 1.0, 150, 560, 380, False), ("stare_interviewer_cat", 1.0, 1130, 560, 380, True)],
           "元戦隊ヒロイン今森茉耶 YouTube再出発から6日で発信休止", "何があった？")


if __name__ == "__main__" and os.environ.get("THUMB") == "17":
    imamori()
