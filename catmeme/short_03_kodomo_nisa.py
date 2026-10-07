"""こどもNISA のショート（縦 1080x1920・60秒以内）。「普通のNISAと何が違う⁉」→ かんたん比較。

python3 catmeme/short_03_kodomo_nisa.py → out/short_03_kodomo_nisa.mp4

画面の作り（縦）
  上   0〜380  ずっと出ているタイトル帯「普通のNISAと何が違う⁉」
  中 400〜1300 横長の場面（猫）の真ん中を切り出して置く。比較の場面は大きな比較パネル
  下 1300〜1680 そのカットのセリフ・字幕を大きく（下の 240px は YouTube の表示と重なるので空ける）
"""
import os
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw

import parts as P
import render as R

R.NYAS_STYLE = True
R.FG_DUCK = -9
SW, SH = 1080, 1920
SHORT_MIN, SHORT_MAX = 45.0, 58.0   # ショートの長さ（秒）
HERE = os.path.dirname(os.path.abspath(__file__))
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("03_kodomo_nisa", "02_october", "01_todai")]
BGM = os.path.join(HERE, "bgm")
NORA = os.path.join(BGM, "野良猫は宇宙を目指した.mp3")
OUT = os.path.join(HERE, "out", "short_03_kodomo_nisa.mp4")

NEWS, SAGE = (215, 35, 35), (40, 90, 200)
YELLOW, RED, WHITE, BLACK, NAVY = (255, 222, 0), (235, 25, 25), (255, 255, 255), (0, 0, 0), (25, 32, 56)
ORANGE = (240, 110, 40)


def bg(n):
    for d in BGS:
        p = os.path.join(d, n + ".png")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(n)


def text_img(text, w, h, size, fill=WHITE, stroke=BLACK, sw=None):
    """w×h の透過画像の真ん中に、縁取りつきの大きな文字（\\n で改行。入らなければ小さくする）。"""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines = text.split("\n")
    while True:
        f = P.font("black", size)
        if (max(d.textlength(ln, font=f) for ln in lines) <= w - 40 and size * 1.2 * len(lines) <= h) or size < 40:
            break
        size -= 4
    sw = sw or max(6, size // 9)
    y = h / 2 - size * 1.2 * len(lines) / 2 + size * 0.6
    for ln in lines:
        if stroke != BLACK:
            d.text((w / 2, y), ln, font=f, fill=stroke, stroke_width=sw + 5, stroke_fill=BLACK, anchor="mm")
        d.text((w / 2, y), ln, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor="mm")
        y += size * 1.2
    return img


def title_band():
    img = Image.new("RGBA", (SW, 400), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, SW, 400), fill=NAVY)
    d.polygon([(0, 330), (SW, 300), (SW, 400), (0, 400)], fill=RED)
    img.alpha_composite(text_img("普通のNISAと", SW, 150, 110, fill=WHITE), (0, 40))
    img.alpha_composite(text_img("何が違う⁉", SW, 170, 150, fill=YELLOW), (0, 170))
    return img


def panel(item, left, right, note=""):
    """比較パネル（1080×880）。左＝ふつうのNISA、右＝こどもNISA（オレンジ）。"""
    img = Image.new("RGBA", (SW, 880), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((24, 10, SW - 24, 870), 40, fill=(252, 250, 244), outline=BLACK, width=7)
    img.alpha_composite(text_img(item, SW - 60, 150, 104, fill=BLACK, stroke=WHITE, sw=4), (30, 30))
    for k, (head, val, col) in enumerate((("ふつうのNISA", left, NAVY), ("こどもNISA", right, ORANGE))):
        x0 = 50 + k * 540
        d.rounded_rectangle((x0, 200, x0 + 440, 290), 24, fill=col)
        d.text((x0 + 220, 245), head, font=P.font("black", 54), fill=WHITE, anchor="mm")
        img.alpha_composite(text_img(val, 440, 420, 128, fill=col if k else BLACK, stroke=WHITE, sw=4), (x0, 300))
    d.text((SW / 2, 510), "VS", font=P.font("black", 64), fill=RED, anchor="mm")
    if note:
        img.alpha_composite(text_img(note, SW - 80, 120, 44, fill=(80, 80, 80), stroke=WHITE, sw=2), (40, 735))
    return img


def cat(a, role, x, color, h=820, flip=False, mute=False):
    return dict(a=a, x=x, h=h, bottom=1080, label=role, label_color=color, label_size=80, flip=flip, mute=mute)


# カット：scene（横長の場面を中段に）か panel（比較パネル）。cap は下段の大きな文字
def cuts():
    return [
        dict(kind="scene", bg=bg("bg19_kids_room"), cats=[cat("surprise_big_pupils_cat", "ニュース猫", 960, NEWS, h=900)],
             cap="こどもNISA\n2027年スタート！", cap_col=YELLOW, dur=2.6, fx=["lines", "shake"],
             se=["jan", "explosion_chudoon"], bgm={"file": NORA, "gain": -2}),
        dict(kind="scene", bg=bg("bg20_counter"),
             cats=[cat("peek_what_happen_cat", "ニュース猫", 520, NEWS), cat("calm_black_face_sheep", "博識な猫", 1430, SAGE, mute=True)],
             cap="子どもが\n投資すんの？", dur=2.2, se="question_hatena_maou"),
        dict(kind="scene", bg=bg("bg20_counter"),
             cats=[cat("peek_what_happen_cat", "ニュース猫", 520, NEWS, mute=True), cat("calm_black_face_sheep", "博識な猫", 1430, SAGE)],
             cap="お金を出すのは親な\n子どもの名前の口座", dur=2.6, se="tsukkomi_bishi"),
        dict(kind="scene", bg=bg("bg06_spotlight"), cats=[cat("confused_i_dont_know_cat", "ニュース猫", 960, NEWS, h=900, flip=True)],
             cap="じゃあ\n普通のNISAと\n何が違うのよ", dur=2.4, se="boing_fail"),
        dict(kind="panel", img=panel("使える人", "18歳以上", "0〜17歳"), cap="① 使える人", dur=3.0, se="xylophone_transition"),
        dict(kind="panel", img=panel("1年に入れられる上限", "360万円", "60万円"), cap="② 1年の上限は\n6分の1", dur=3.2,
             se="game_dq_miss"),
        dict(kind="panel", img=panel("合計の上限", "1,800万円", "600万円"), cap="③ 合計は\n600万円まで", dur=3.0, se="card_flip"),
        dict(kind="panel", img=panel("買えるもの", "投資信託・株", "積立向けの\n投資信託だけ"), cap="④ 株は買えない", dur=3.0,
             se="buzzer_wrong"),
        dict(kind="panel", img=panel("引き出し", "いつでもOK", "12歳まで\n原則NG", note="12歳からは　子どものための出費なら（同意と書類が必要）"),
             cap="⑤ 12歳までは\n引き出せない", cap_col=RED, dur=3.6, se="doon_heavy"),
        dict(kind="scene", bg=bg("bg21_school_gate"), cats=[cat("angry_cat_hits_cat", "ニュース猫", 960, NEWS, h=900)],
             cap="引き出せないの\nキツくね！？", cap_col=RED, dur=2.4, fx=["lines", "shake"], se="game_mgs_alert"),
        dict(kind="panel", img=panel("増えた分の税金", "かからない", "かからない", note="ふつうは約20％かかる。どちらも非課税"),
             cap="⑥ 税金ゼロは\n同じ", dur=3.0, se="pinpoon_correct"),
        dict(kind="panel", img=panel("18歳になったら", "―", "大人のNISAに\n自動で引っ越し", note="こどもNISAで使った枠は　大人の1,800万円に含まれる"),
             cap="⑦ 使った枠は\n大人の枠に含まれる", dur=3.6, se="whoosh_shu"),
        dict(kind="scene", bg=bg("bg20_counter"), cats=[cat("glare_disgusted_cat", "ニュース猫", 960, NEWS, h=900)],
             cap="将来の枠の\n前借りじゃん！", cap_col=RED, dur=2.6, fx=["lines", "shake"], se="game_aceattorney_desk_slam"),
        dict(kind="scene", bg=bg("bg14_home_night"),
             cats=[cat("sleepy_sleepy_cat", "ニュース猫", 520, NEWS, mute=True), cat("eat_pop_cat", "博識な猫", 1430, SAGE)],
             cap="親の枠が埋まりそうな\n家の“追加の箱”\nって考えると◎", dur=3.4, se="idea_newtype_01"),
        dict(kind="scene", bg=bg("bg14_home_night"),
             cats=[cat("sad_banana_cat_cry", "ニュース猫", 520, NEWS), cat("eat_pop_cat", "博識な猫", 1430, SAGE, mute=True)],
             cap="……うち\n親の枠もスカスカだわ", dur=2.6, se="tv_dokkiri_tettere"),
        dict(kind="scene", bg=bg("bg03_blackboard"), cats=[cat("wave_waving_cat", "ニュース猫", 960, NEWS, h=760)],
             cap="お得な家・イマイチな家は\n本編で解説！", cap_col=YELLOW, dur=3.0, se="chirin"),
    ]


def vover(dst, src, alpha, x, y):
    """縦画面用の重ね合わせ（render.over は横画面の大きさで切るため）。"""
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, SW), min(y + h, SH)
    if x1 <= x0 or y1 <= y0:
        return
    a = alpha[y0 - y:y1 - y, x0 - x:x1 - x]
    if a.ndim == 2:
        a = a[..., None]
    d = dst[y0:y1, x0:x1]
    d *= 1 - a
    d += src[y0 - y:y1 - y, x0 - x:x1 - x] * a


class ShortCut:
    def __init__(self, c):
        self.c = c
        self.dur = R.cut_dur(c)
        self.scene = None
        if c["kind"] == "scene":
            sc = {k: v for k, v in c.items() if k not in ("cap", "cap_col", "kind", "img")}
            self.scene = R.CutRenderer(sc)
        else:
            self.panel = R.to_np(c["img"])
        cap = text_img(c["cap"], SW - 40, 380, 120, fill=c.get("cap_col", WHITE),
                       stroke=WHITE if c.get("cap_col") == RED else BLACK)
        self.cap = R.to_np(cap)

    def frame(self, t, title):
        out = np.zeros((SH, SW, 3), np.float32)
        out[:] = np.array(NAVY[::-1], np.float32) / 255 * 0.6
        if self.scene is not None:
            f = self.scene.frame(t)
            f = cv2.resize(f, (1600, 900), interpolation=cv2.INTER_AREA)[:, 260:260 + SW]   # 縦長に合わせて真ん中を切り出す
            out[400:1300] = f
        else:
            pi, pa = self.panel
            k = 1.0 if t > 0.15 else 0.6 + 0.4 * R.ease_out(t / 0.15)
            if k < 1:
                h, w = pi.shape[:2]
                pi = cv2.resize(pi, (int(w * k), int(h * k)))
                pa = cv2.resize(pa, (int(w * k), int(h * k)))
            vover(out, pi, pa, int(SW / 2 - pi.shape[1] / 2), int(850 - pi.shape[0] / 2))
        ti, ta = title
        vover(out, ti, ta, 0, 0)
        ci, ca = self.cap
        s = 1.0 if t > 0.15 else 0.6 + 0.4 * R.ease_out(t / 0.15)
        if s < 1:
            h, w = ci.shape[:2]
            ci = cv2.resize(ci, (int(w * s), int(h * s)))
            ca = cv2.resize(ca, (int(w * s), int(h * s)))
        vover(out, ci, ca, int(SW / 2 - ci.shape[1] / 2), int(1490 - ci.shape[0] / 2))
        return out

    def close(self):
        if self.scene is not None:
            self.scene.close()


def main():
    run(cuts(), title_band(), OUT, os.path.join(HERE, "out", "short_03_preview"))


def run(cs, title_img, out_path, prev):
    """カット一覧を縦動画に書き出す（ほかのショートからも使う）。"""
    OUT = out_path
    durs = [R.cut_dur(c) for c in cs]
    starts = list(np.cumsum([0] + durs[:-1]))
    total = sum(durs)
    if not SHORT_MIN <= total <= SHORT_MAX:   # ショートは45〜58秒（チャンネルのルール）
        raise SystemExit(f"ショートの長さ {total:.1f}秒 が {SHORT_MIN}〜{SHORT_MAX}秒の範囲外です。カットを足すか削ってください")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    wav = OUT + ".audio.f32"
    R.build_audio(cs, starts, durs, total).tofile(wav)
    title = R.to_np(title_img)
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{SW}x{SH}", "-r", str(R.FPS), "-i", "-",
         "-f", "f32le", "-ar", str(R.SR), "-ac", "2", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    frame_no = 0
    os.makedirs(prev, exist_ok=True)
    for i, c in enumerate(cs):
        sc = ShortCut(c)
        end = int(round((starts[i] + durs[i]) * R.FPS))
        first = True
        while frame_no < end:
            tt = frame_no / R.FPS - starts[i]
            img = sc.frame(tt, title)
            u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
            proc.stdin.write(u8.tobytes())
            if first and tt > 0.5:
                cv2.imwrite(os.path.join(prev, f"{i:02d}.jpg"), u8, [cv2.IMWRITE_JPEG_QUALITY, 80])
                first = False
            frame_no += 1
        sc.close()
        print(f"\r{i + 1}/{len(cs)}  {frame_no / R.FPS:5.1f}s / {total:.1f}s", end="", flush=True)
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    print(f"\n-> {OUT} ({total:.1f}s)")


if __name__ == "__main__":
    main()
