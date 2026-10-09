"""ショートの「最初の5秒」を派手にする“つかみ”の試作（5案）。名フレーズ6選のショートで試す。

python3 catmeme/short_hooks.py        → out/hook_A.mp4 〜 hook_E.mp4（どれも最初の約10秒だけ）
python3 catmeme/short_hooks.py C      → hook_C だけ

各案とも 0〜5秒が つかみ（自前で1コマずつ描く）、5秒以降は今のショートの続き（①553＞1107のパネル）。
  A 連打フラッシュ   … 6つのフレーズが0.5秒ずつ、色が切り替わりながら叩きつけられる → 「6連発!!」
  B スロット        … フレーズがスロットのように高速で流れ、「553＞1107」でピタッと止まる
  C クイズ          … 「553＞1107　意味わかる？」＋3秒のカウントダウン、猫が左右から飛び出す
  D 猫ミーム乱入    … 回る集中線の上に猫ミームが次々飛び込み、フレーズの札がドンドン貼られる
  E ズーム＆グリッチ … 「＞」の超アップから一気に引いて「553＞1107」→ 色ずれ → 6つが周りを回る
"""
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

import parts as P
import render as R
import short_03_kodomo_nisa as S
import short_04_leak as Q
import short_meme_phrases as M

SW, SH = S.SW, S.SH
HERE = S.HERE
YELLOW, RED, WHITE, BLACK, NAVY = S.YELLOW, S.RED, S.WHITE, S.BLACK, S.NAVY
GREEN, ORANGE = (30, 140, 70), (230, 130, 20)
PHRASES = [("553＞1107", RED), ("古古古米", ORANGE), ("2億円トイレ", RED), ("ジャンボ\nタニシ農法", GREEN), ("のり弁", NAVY),
           ("GoTo\nトラブル", RED)]
HOOK = 5.0


# ---------- 描画の道具 ----------
def blank(rgb):
    out = np.zeros((SH, SW, 3), np.float32)
    out[:] = np.array(rgb[::-1], np.float32) / 255
    return out


_RAYS = {}


def rays(out, t, cols=((255, 60, 60), (255, 210, 0)), speed=25, cy=0.45, alpha=0.75):
    """回る集中線。"""
    key = cols
    if key not in _RAYS:
        n = 2600
        im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        c = n / 2
        for i in range(40):
            a0, a1 = math.radians(i * 9), math.radians(i * 9 + 4.5)
            d.polygon([(c, c), (c + n * math.cos(a0), c + n * math.sin(a0)), (c + n * math.cos(a1), c + n * math.sin(a1))],
                      fill=cols[i % 2] + (255,))
        _RAYS[key] = R.to_np(im)
    img, a = _RAYS[key]
    n = img.shape[0]
    M_ = cv2.getRotationMatrix2D((n / 2, n / 2), t * speed, 1.0)
    img2 = cv2.warpAffine(img, M_, (n, n))
    a2 = cv2.warpAffine(a, M_, (n, n)) * alpha
    x, y = int(SW / 2 - n / 2), int(SH * cy - n / 2)
    S.vover(out, img2, a2, x, y)


_SPR = {}


def sprite(key, fn):
    if key not in _SPR:
        _SPR[key] = fn()
    return _SPR[key]


def text(t, size, fill=WHITE, stroke=BLACK, w=SW, h=None):
    h = h or int(size * 1.35 * (t.count("\n") + 1)) + 40
    return sprite(("txt", t, size, fill, stroke, w, h), lambda: S.text_img(t, w, h, size, fill=fill, stroke=stroke))


def tag(t, col, size=110):
    """白地に色枠の札。"""
    def make():
        f = P.font("black", size)
        lines = t.split("\n")
        d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        tw = int(max(d0.textlength(ln, font=f) for ln in lines)) + 90
        th = int(size * 1.25 * len(lines)) + 60
        im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, tw - 1, th - 1), 30, fill=WHITE, outline=col, width=14)
        for i, ln in enumerate(lines):
            d.text((tw / 2, 30 + size * 0.62 + i * size * 1.25), ln, font=f, fill=col, anchor="mm")
        return im
    return sprite(("tag", t, col, size), make)


def put(out, pil, cx, cy, scale=1.0, angle=0.0, alpha=1.0):
    """PIL の RGBA を、中心・倍率・角度を指定して重ねる。"""
    if scale <= 0.01 or alpha <= 0:
        return
    im = pil
    if abs(scale - 1) > 0.01:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if abs(angle) > 0.1:
        im = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    img, a = R.to_np(im)
    S.vover(out, img, a * alpha, int(cx - im.width / 2), int(cy - im.height / 2))


_CLIPS = {}


def cat(out, name, t, cx, bottom, h, scale=1.0, flip=False):
    """猫ミーム（緑抜き）を、下端と高さを指定して重ねる。"""
    key = (name, flip)
    if key not in _CLIPS:
        _CLIPS[key] = R.Clip(name, flip=flip)
    fr, a = _CLIPS[key].frame(t)
    k = h * scale / fr.shape[0]
    if k <= 0.01:
        return
    w, hh = max(1, int(fr.shape[1] * k)), max(1, int(fr.shape[0] * k))
    img = cv2.resize(fr, (w, hh), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    al = cv2.resize(a.astype(np.float32), (w, hh), interpolation=cv2.INTER_AREA)
    S.vover(out, img, al, int(cx - w / 2), int(bottom - hh))


def shake(out, t, t0, amp=40, dur=0.3):
    if t0 <= t < t0 + dur:
        k = 1 - (t - t0) / dur
        dx, dy = amp * k * math.sin(t * 95), amp * k * math.cos(t * 77)
        return cv2.warpAffine(out, np.float32([[1, 0, dx], [0, 1, dy]]), (SW, SH), borderMode=cv2.BORDER_REPLICATE)
    return out


def flash(out, t, t0, dur=0.12, col=(1, 1, 1)):
    if t0 <= t < t0 + dur:
        k = 1 - (t - t0) / dur
        out = out * (1 - k) + np.array(col, np.float32) * k
    return out


def slam(t, t0, big=2.6, d=0.12):
    """叩きつけ：大きい所から一気に等倍へ（少し跳ね返る）。"""
    if t < t0:
        return 0.0
    u = (t - t0) / d
    if u < 1:
        return big - (big - 1) * R.ease_out(u)
    u2 = (t - t0 - d) / 0.12
    return 1.0 + 0.06 * math.sin(min(u2, 1) * math.pi) if u2 < 1 else 1.0


def pop(t, t0, d=0.18):
    """ポン：小さい所から少し大きくなって等倍へ。"""
    if t < t0:
        return 0.0
    u = (t - t0) / d
    if u >= 1:
        return 1.0
    return 1.25 * R.ease_out(u) if u < 0.7 else 1.25 - 0.25 * (u - 0.7) / 0.3


def finish(out):
    return np.clip(out, 0, 1)


# ---------- 5つの案 ----------
def hook_A(t):
    """連打フラッシュ。"""
    bgs = [(220, 30, 30), (255, 200, 0), (25, 32, 56), (20, 20, 20), (220, 30, 30), (255, 200, 0)]
    if t < 3.0:
        i = min(int(t / 0.5), 5)
        t0 = i * 0.5
        out = blank(bgs[i])
        rays(out, t, cols=((255, 255, 255), bgs[i]), speed=60, alpha=0.25)
        put(out, text(f"{i + 1}", 300, fill=YELLOW if i % 2 == 0 else WHITE), 180, 260, slam(t, t0, 3, 0.1))
        put(out, tag(*PHRASES[i], size=130), SW / 2, SH * 0.48, slam(t, t0, 2.8, 0.1), angle=(-6 if i % 2 else 6))
        out = shake(out, t, t0, 45, 0.25)
        out = flash(out, t, t0, 0.08)
        return finish(out)
    out = blank((20, 20, 20))
    rays(out, t, speed=40)
    put(out, text("ニュースから生まれた", 100), SW / 2, 420, pop(t, 3.0))
    put(out, text("名フレーズ", 200, fill=YELLOW), SW / 2, 640, slam(t, 3.15, 3, 0.12), angle=-4)
    put(out, text("6連発!!", 260, fill=RED, stroke=WHITE), SW / 2, 900, slam(t, 3.35, 3.2, 0.12), angle=4)
    if t > 3.6:
        cat(out, "surprise_big_pupils_cat", t - 3.6, 280, SH + 40, 700, pop(t, 3.6))
        cat(out, "huh_huh_cat", t - 3.6, 820, SH + 40, 700, pop(t, 3.75), flip=True)
    out = shake(out, t, 3.35, 60, 0.4)
    out = flash(out, t, 3.35, 0.15)
    return finish(out)


def hook_B(t):
    """スロット。"""
    out = blank((25, 32, 56))
    rays(out, t, cols=((60, 80, 160), (25, 32, 56)), speed=15, alpha=0.6)
    put(out, text("ネットで生まれた名フレーズ", 80, fill=YELLOW), SW / 2, 230, pop(t, 0.0))
    # スロットの窓
    win = sprite("win", lambda: _window())
    put(out, win, SW / 2, SH * 0.45)
    stop = 3.0
    # 位置（行数）：最初は速く、だんだん遅く、stop で「553＞1107」（0番）に止まる
    total_rows = 6 * 5
    if t < stop:
        u = t / stop
        pos = total_rows * (1 - (1 - u) ** 3)
    else:
        pos = total_rows
    row_h = 330
    for k in range(-2, 3):
        idx = int(math.floor(pos)) + k
        frac = pos - math.floor(pos)
        y = SH * 0.45 + (k - frac) * row_h
        if abs(y - SH * 0.45) > 520:
            continue
        ph, col = PHRASES[idx % 6]
        sc = 0.85 if k != 0 or t < stop else slam(t, stop, 1.6, 0.12)
        alpha = 1.0 if (t >= stop and k == 0) else 0.55
        put(out, tag(ph.replace("\n", ""), col, size=118), SW / 2, y, sc, alpha=alpha)
    if t >= stop:
        put(out, text("これ、意味わかる？", 110, fill=WHITE), SW / 2, 1430, pop(t, stop + 0.25))
        cat(out, "weird_meowing_cat", t - stop, 260, SH + 60, 560, pop(t, stop + 0.4))
        cat(out, "surprise_big_pupils_cat", t - stop, 830, SH + 60, 560, pop(t, stop + 0.55), flip=True)
        out = shake(out, t, stop, 50, 0.35)
        out = flash(out, t, stop, 0.12, (0.6, 0.9, 1.0))
    return finish(out)


def _window():
    im = Image.new("RGBA", (SW - 60, 520), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, 519), 40, fill=(250, 248, 240, 235), outline=YELLOW, width=16)
    d.polygon([(10, 230), (60, 260), (10, 290)], fill=RED)
    d.polygon([(im.width - 10, 230), (im.width - 60, 260), (im.width - 10, 290)], fill=RED)
    return im


def hook_C(t):
    """クイズ。"""
    out = blank((255, 248, 225))
    rays(out, t, cols=((255, 230, 120), (255, 248, 225)), speed=10, alpha=0.8)
    put(out, text("Q.", 200, fill=RED, stroke=WHITE, w=400), 200, 300, slam(t, 0.0, 2.5, 0.12))
    put(out, text("553＞1107", 180, fill=NAVY, stroke=WHITE), SW / 2, 620, slam(t, 0.15, 3, 0.12), angle=-3)
    put(out, text("この式の意味、わかる？", 92, fill=BLACK, stroke=WHITE), SW / 2, 860, pop(t, 0.5))
    # 3秒のカウントダウン（バーが減っていく＋大きな数字）
    if 0.8 <= t < 3.8:
        u = (t - 0.8) / 3.0
        bar = int((SW - 160) * (1 - u))
        out[960:1000, 80:80 + bar] = np.array(RED[::-1], np.float32) / 255
        n = 3 - int(t - 0.8)
        put(out, text(str(n), 260, fill=RED, stroke=WHITE), SW / 2, 1160, slam(t, 0.8 + (3 - n), 1.8, 0.1))
    # 猫が左右から交互に飛び出す
    for k, (name, x, t0, flip) in enumerate((("huh_huh_cat", 230, 1.0, False), ("weird_meowing_cat", 850, 1.8, True),
                                             ("glare_disgusted_cat", 230, 2.6, False))):
        if t >= t0:
            off = (1 - R.ease_out(min(1, (t - t0) / 0.2))) * (-500 if x < 540 else 500)
            cat(out, name, t - t0, x + off, SH + 40, 600, flip=flip)
    if t >= 3.8:
        put(out, text("答えは…", 120, fill=WHITE), SW / 2, 1300, pop(t, 3.8))
        put(out, text("このあとすぐ！", 150, fill=YELLOW), SW / 2, 1480, slam(t, 4.1, 2.6, 0.12), angle=-3)
        out = shake(out, t, 4.1, 50, 0.35)
        out = flash(out, t, 4.1, 0.12)
    return finish(out)


def hook_D(t):
    """猫ミーム乱入。"""
    out = blank((220, 30, 30))
    rays(out, t, cols=((255, 220, 0), (220, 30, 30)), speed=50, alpha=0.9)
    plan = [("surprise_big_pupils_cat", 200, 900, 0.0, 0), ("huh_huh_cat", 860, 950, 0.45, 1), ("weird_meowing_cat", 240, 1500, 0.9, 2),
            ("glare_disgusted_cat", 850, 1550, 1.35, 3), ("spin_spinning_cat", 540, 1180, 1.8, 4), ("joy_happy_happy_happy_cat", 540, 1880, 2.25, 5)]
    for name, x, bottom, t0, i in plan:
        if t >= t0:
            fx = x + (1 - R.ease_out(min(1, (t - t0) / 0.18))) * (-700 if x < 540 else 700)
            cat(out, name, t - t0, fx, bottom, 520 if i != 4 else 460, flip=x > 540)
            ph, col = PHRASES[i]
            put(out, tag(ph, col, size=70), x, bottom - 520 + 40, slam(t, t0 + 0.12, 2.4, 0.1), angle=(-10 if i % 2 else 10))
    if t >= 3.0:
        out = out * 0.55
        put(out, text("全部", 220, fill=WHITE), SW / 2, 700, slam(t, 3.0, 3, 0.12), angle=-5)
        put(out, text("わかる？", 260, fill=YELLOW), SW / 2, 960, slam(t, 3.2, 3, 0.12), angle=4)
        put(out, text("ネットで生まれた名フレーズ6選", 70, fill=WHITE), SW / 2, 1200, pop(t, 3.6))
    for t0 in (0.0, 0.45, 0.9, 1.35, 1.8, 2.25):
        out = shake(out, t, t0 + 0.12, 25, 0.15)
    out = shake(out, t, 3.2, 60, 0.4)
    out = flash(out, t, 3.2, 0.15)
    return finish(out)


def hook_E(t):
    """ズーム＆グリッチ。"""
    out = blank((10, 10, 20))
    if t < 1.2:   # 「＞」の超アップから引く
        u = R.ease_out(t / 1.2)
        sc = 9 - 8 * u
        put(out, text("553＞1107", 210, fill=YELLOW), SW / 2, SH * 0.42, sc)
    else:
        rays(out, t, cols=((40, 40, 90), (10, 10, 20)), speed=30, alpha=0.8)
        put(out, text("553＞1107", 210, fill=YELLOW), SW / 2, SH * 0.42)
        if t >= 1.5:
            put(out, text("ありえない式!?", 130, fill=RED, stroke=WHITE), SW / 2, SH * 0.42 + 230, slam(t, 1.5, 2.6, 0.12), angle=-5)
        if t >= 2.4:   # ほかの5つが周りを回る
            for i in range(1, 6):
                ang = (t - 2.4) * 120 + i * 72
                r = 430 + 40 * math.sin(t * 3 + i)
                k = min(1, (t - 2.4) / 0.4)
                x = SW / 2 + r * math.cos(math.radians(ang)) * 0.95 * k
                y = SH * 0.42 + 60 + r * math.sin(math.radians(ang)) * 1.5 * k
                ph, col = PHRASES[i]
                put(out, tag(ph, col, size=78), x, y, 0.4 + 0.6 * k)
        if t >= 3.8:
            out = out * 0.5
            put(out, text("ネットで生まれた", 110, fill=WHITE), SW / 2, 380, pop(t, 3.8))
            put(out, text("名フレーズ6選", 190, fill=YELLOW), SW / 2, 560, slam(t, 4.0, 3, 0.12), angle=-3)
    # 色ずれ（グリッチ）
    for g in (1.2, 1.5, 2.4, 4.0):
        if g <= t < g + 0.18:
            d = int(30 * (1 - (t - g) / 0.18))
            out = out.copy()
            out[:, :, 2] = np.roll(out[:, :, 2], d, axis=1)
            out[:, :, 0] = np.roll(out[:, :, 0], -d, axis=1)
    out = shake(out, t, 1.5, 50, 0.3)
    out = shake(out, t, 4.0, 50, 0.3)
    out = flash(out, t, 1.2, 0.1)
    return finish(out)


# 効果音（秒, 音）
SE = {
    "A": [(i * 0.5, "taiko_don") for i in range(6)] + [(3.15, "jan"), (3.35, "explosion_chudoon"), (3.6, "puni"), (3.75, "puni")],
    "B": [(0.0, "drumroll"), (3.0, "chiin_01"), (3.0, "doon_heavy"), (3.25, "question_hatena_maou")],
    "C": [(0.0, "quiz_question_01"), (0.15, "don_hit"), (0.8, "pi"), (1.8, "pi"), (2.8, "pi"), (1.0, "boing_01"), (1.8, "boing_01"),
          (2.6, "boing_01"), (3.8, "quiz_den"), (4.1, "jan")],
    "D": [(t0, "whoosh_shu") for t0 in (0.0, 0.45, 0.9, 1.35, 1.8, 2.25)] + [(t0 + 0.12, "don_hit") for t0 in (0.0, 0.45, 0.9, 1.35, 1.8, 2.25)]
         + [(3.0, "taiko_don"), (3.2, "explosion_dokaan")],
    "E": [(0.0, "dash_super_fast"), (1.2, "glass_break_01"), (1.5, "doon_heavy"), (2.4, "shine_kira_01"), (4.0, "jan")],
}
DRAW = {"A": hook_A, "B": hook_B, "C": hook_C, "D": hook_D, "E": hook_E}


def cuts(key):
    hook = dict(kind="hook", draw=DRAW[key], dur=HOOK / R.TEMPO, fixed=True, cap="",
                se=[{"f": f, "at": a, "gain": -4} for a, f in SE[key]], bgm={"file": M.PURPLE, "gain": -4})
    rest = M.cuts()[1:2]   # 今のショートの続き（①553＞1107のパネル）
    rest[0].pop("bgm", None)
    return [hook] + rest


def main():
    title = Q.title_band("ニュースから生まれた", "ネット名フレーズ6選", label="ネットで生まれた名フレーズ")
    for key in sys.argv[1:] or list(DRAW):
        out = os.path.join(HERE, "out", f"hook_{key}.mp4")
        S.run(cuts(key), title, out, os.path.join(HERE, "out", f"hook_{key}_preview"), check=False)


if __name__ == "__main__":
    main()
