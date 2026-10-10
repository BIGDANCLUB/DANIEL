"""参考ショート（reference/short_ref の5本：「閲覧注意 相続税がヤバすぎる」「日本VS海外 夏休み」など）の作りをほぼマネしたショート。
題材は 4本目の「免許証が漏れると…」。

python3 catmeme/short_refstyle.py → out/short_refstyle_license.mp4

参考の作り（マネしたところ）
  - 背景イラストを縦いっぱいに敷く（図やパネルは出さない。全部セリフで進める）
  - 上の黒い帯に2行のタイトル（1行目は赤い大きな文字、2行目は黄色）。帯の上に背景が少し見える
  - 猫ミームは画面の下半分に大きく1〜2匹、下の辺から生やす
  - セリフは帯のすぐ下に、白（または黄緑）の太い文字＋黒い縁取り。大事な言葉だけ赤
  - 擬人化した相手役（参考では「相続税」「ママ」）は、猫の足元に黄緑の大きな文字で役名
  - 1セリフ2〜3秒でテンポよく切り替え、猫ミームの元の音を鳴らす
"""
import os

import numpy as np
from PIL import Image, ImageDraw

import parts as P
import render as R
import short_03_kodomo_nisa as S
import short_hooks as H

SW, SH = S.SW, S.SH
HERE = S.HERE
OUT = os.path.join(HERE, "out", "short_refstyle_license.mp4")
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("04_leak", "03_kodomo_nisa", "02_october", "01_todai")]
WHITE, BLACK, RED, YELLOW = (255, 255, 255), (0, 0, 0), (235, 25, 25), (255, 230, 0)
LIME = (120, 235, 40)
BAND = (210, 470)   # 黒い帯の上下（この上には背景が見える）
TEXT_Y = 640        # セリフの中心


def bg_path(n):
    for d in BGS:
        p = os.path.join(d, n + ".png")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(n)


_BG = {}


def vbg(n):
    """横長の背景を、縦いっぱいに拡大して真ん中を切り出す。"""
    if n not in _BG:
        im = Image.open(bg_path(n)).convert("RGB")
        im = im.resize((int(im.width * SH / im.height), SH), Image.LANCZOS)
        x0 = (im.width - SW) // 2
        _BG[n] = np.asarray(im.crop((x0, 0, x0 + SW, SH)))[:, :, ::-1].astype(np.float32) / 255
    return _BG[n]


def outline_text(lines, size, w=SW - 30):
    """参考ふうのセリフ：太い文字＋黒い太縁。lines=[[(文字, 色), ...], ...]（1行の中で色を変えられる）。"""
    f = P.font("black", size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    width = lambda ln: sum(d0.textlength(t, font=f) for t, _ in ln)
    while max(width(ln) for ln in lines) > w - 40 and size > 50:
        size -= 4
        f = P.font("black", size)
    sw = max(8, size // 7)
    lh = int(size * 1.18)
    im = Image.new("RGBA", (w, lh * len(lines) + sw * 2 + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        x = (w - width(ln)) / 2
        y = sw + 5 + i * lh
        for t, col in ln:
            d.text((x, y), t, font=f, fill=col, stroke_width=sw, stroke_fill=BLACK)
            x += d.textlength(t, font=f)
    return im


def parse(text, base=WHITE):
    """「*赤*」で囲んだ所だけ赤。\\n で改行。"""
    out = []
    for raw in text.split("\n"):
        parts, red = [], False
        for k, seg in enumerate(raw.split("*")):
            if seg:
                parts.append((seg, RED if red else base))
            red = not red
        out.append(parts)
    return out


def title_band(top, sub):
    im = Image.new("RGBA", (SW, BAND[1] - BAND[0]), (0, 0, 0, 255))
    t1 = outline_text([[(top, RED)]], 170)
    t2 = outline_text([[(sub, YELLOW)]], 104)
    im.alpha_composite(t1, ((SW - t1.width) // 2, 0))
    im.alpha_composite(t2, ((SW - t2.width) // 2, im.height - t2.height + 4))
    return im


def role_label(name):
    return outline_text([[(name, LIME)]], 110, w=700)


def make_draw(c, title):
    """1カットぶんの絵を描く関数（t はカットの頭からの秒）。"""
    bg = vbg(c["bg"])
    cap = outline_text(parse(c["say"], c.get("col", WHITE)), c.get("size", 100))
    lab = role_label(c["label"]) if c.get("label") else None

    def draw(t):
        out = bg.copy()
        for k in c["cats"]:
            s = H.pop(t, k.get("delay", 0.0), 0.16) if k.get("pop", True) else 1.0
            H.cat(out, k["a"], t + k.get("ss", 0.0), k["x"], SH + k.get("drop", 60), k["h"], s, flip=k.get("flip", False))
        if lab is not None:
            H.put(out, lab, c.get("label_x", 760), SH - 330)
        H.put(out, title, SW / 2, (BAND[0] + BAND[1]) / 2)
        H.put(out, cap, SW / 2, TEXT_Y + cap.height / 2 - 60, H.pop(t, 0.0, 0.14))
        if c.get("shake"):
            out = H.shake(out, t, 0.0, 30, 0.3)
        return H.finish(out)

    return draw


def cut(bg, say, cats, dur=2.4, label=None, label_x=760, se=None, col=WHITE, size=100, shake=False, bgm=None, speaker=0):
    """cats=[(素材, x, 高さ, 左右反転)]。speaker 番目の猫の音だけ鳴らす。"""
    ks = [dict(a=a, x=x, h=h, flip=fl, mute=(i != speaker), full=False, delay=0.0 if i == 0 else 0.08)
          for i, (a, x, h, fl) in enumerate(cats)]
    d = dict(kind="hook", bg=bg, say=say, cats=ks, dur=dur / R.TEMPO, fixed=True, cap="", label=label, label_x=label_x, col=col,
             size=size, shake=shake)
    if se:
        d["se"] = se
    if bgm:
        d["bgm"] = bgm
    return d


L, Rr, C = 300, 790, 540   # 左・右・真ん中
HOME, SHOP, HACK = "bg14_home_night", "bg20_counter", "bg23_hacker_room"
HAN = "なりすまし犯"


def cuts():
    return [
        cut(SHOP, "レンタカー\n予約完了！！", [("dance_maxwell_cat", C, 1100, False)], 2.6, se="jan",
            bgm={"file": os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3"), "gain": -6}),
        cut(SHOP, "免許証も写真で\nアップするだけ！\n楽ちん♪", [("happy_girlfriend_dance_cat", L, 1000, False), ("joy_happy_happy_happy_cat", Rr, 1000, True)],
            2.8, se="pikon"),
        cut(HOME, "【速報】\n免許証など約160万件\n*漏えいのおそれ*", [("surprise_big_pupils_cat", C, 1150, False)], 3.0, se="pc_warning", shake=True),
        cut(HOME, "は？", [("huh_huh_cat", C, 1150, False)], 1.8, size=230, se="question_hatena_maou"),
        cut(HOME, "どうも〜\nあなたで〜す", [("weird_meowing_cat", L, 950, False), ("cocky_dj_cat", Rr, 1050, True)], 2.6, label=HAN, speaker=1,
            se="anime_broly_dedeen"),
        cut(HOME, "は？？誰？？", [("glare_disgusted_cat", L, 1000, False), ("cocky_dj_cat", Rr, 1050, True)], 2.2, label=HAN, size=150,
            se="boing_fail"),
        cut(HOME, "あなたの名前で\n*クレカ*作りました！", [("glare_disgusted_cat", L, 1000, False), ("shady_dancing_man", Rr, 1100, False)], 2.8,
            label=HAN, speaker=1, col=LIME, se="shine_kira_01"),
        cut(HOME, "勝手に！？", [("surprise_big_pupils_cat", L, 1000, False), ("shady_dancing_man", Rr, 1100, False)], 2.0, label=HAN,
            size=170, shake=True, se="explosion_chudoon"),
        cut(HOME, "ついでに\n*キャッシング*も\nしときました〜ww", [("weird_meowing_cat", L, 950, False), ("laugh_laughing_dog", Rr, 1000, True)], 3.0,
            label=HAN, speaker=1, col=LIME, se="anime_shinchan_taraan"),
        cut(HOME, "払った覚えのない\n*督促状*が…", [("sad_banana_cat_cry", C, 1150, False)], 2.8, se="tear_drop"),
        cut(HOME, "延滞の記録で\n*ブラック入り*\nで〜す", [("sad_banana_cat_cry", L, 950, False), ("angry_aiming_cat", Rr, 1050, True)], 3.0,
            label=HAN, speaker=1, col=LIME, se="game_mgs_alert"),
        cut(SHOP, "家を買おうと\nしたら…", [("think_bike_front_seat_cat", C, 1100, False)], 2.4, se="page_turn_01"),
        cut(SHOP, "*ローン*は\n通りません", [("think_bike_front_seat_cat", L, 950, False), ("call_customer_service_cat", Rr, 1050, True)], 2.6,
            label="銀行", speaker=1, se="buzzer_wrong"),
        cut(SHOP, "人生\n詰んだ…", [("despair_dramatic_kitten", C, 1150, False)], 2.4, size=170, se="deflate_hyororo"),
        cut(HOME, "でも安心してください\n*防ぐ方法*があります！", [("despair_dramatic_kitten", L, 900, False), ("eat_pop_cat", Rr, 1050, True)], 3.0,
            label="博識な猫", speaker=1, col=LIME, se="idea_newtype_01",
            bgm={"file": os.path.join(S.BGM, "星降る夜のホットココア.mp3"), "gain": -6, "fade": 0.6}),
        cut(HOME, "信用情報機関に\n*「本人申告」*を\n登録しとけ！", [("realize_wet_cat_stare", L, 950, False), ("eat_pop_cat", Rr, 1050, True)], 3.0,
            label="博識な猫", speaker=1, col=LIME, se="pinpoon_correct"),
        cut(HOME, "なりすましの契約を\n防ぎやすくなる", [("realize_wet_cat_stare", L, 950, False), ("calm_black_face_sheep", Rr, 1050, True)], 2.8,
            label="博識な猫", speaker=1, col=LIME, se="pikon"),
        cut(HOME, "*開示*して\n身に覚えのない契約が\nないかもチェック！", [("happy_girlfriend_dance_cat", L, 1000, False), ("calm_black_face_sheep", Rr, 1050, True)],
            3.0, label="博識な猫", speaker=1, col=LIME, se="page_turn_02"),
        cut(HACK, "本人申告…\nだと…", [("blank_black_cat_zoning_out", C, 1100, False)], 2.6, label=HAN, label_x=540, size=150,
            se="deflate_hyororo"),
        cut(HOME, "※実際は審査で確認もあるので\n必ずこうなるわけではありません", [("eat_pop_cat", C, 1000, False)], 2.8, size=64, se="pinpon_notice"),
        cut(HOME, "今すぐ\nやっとこ！", [("dance_maxwell_cat", L, 1000, False), ("joy_happy_happy_happy_cat", Rr, 1000, True)], 2.6, size=160,
            se="chirin"),
    ]


def main():
    title = title_band("閲覧注意", "免許証が漏れるとヤバすぎる")
    cs = cuts()
    for c in cs:   # 絵を描く関数を用意（タイトル帯を毎フレーム重ねる）
        c["draw"] = make_draw(c, title)
    S.run(cs, title, OUT, os.path.join(HERE, "out", "short_refstyle_license_preview"))


if __name__ == "__main__":
    main()
