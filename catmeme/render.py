"""猫ミーム長尺動画の書き出し。

カット（場面）の並びを受け取り、背景イラスト → 猫ミーム（緑を抜く）→ 画面部品（字幕・吹き出し・解説カード）
の順に重ね、BGM と効果音を混ぜて mp4 にする。カットの並びは動画ごとのスクリプト（例 cuts_01_todai.py）で書く。

カットの書き方（dict）:
  bg       背景PNGのパス（None なら黒）
  dur      秒数（省略時は文字数から自動）
  sub      ナレーション字幕
  say      猫のセリフ（吹き出し）。say_name で役名の札、say_color で札の色
  card     解説カードPNGのパス（parts/ の画像）
  layers   さらに重ねる透過PNGのパス or PIL画像のリスト
  cats     [{"a": 素材名, "x": 中心X, "h": 高さ, "bottom": 足元のY, "still": 止め絵, "flip": 左右反転, "ss": 開始秒}]
  se       効果音 "pop" / "don" / "drum" / "chime"（カットの頭で鳴る）
  bgm      {"file": 曲, "gain": dB, "fade": 秒} … このカットから曲を切り替え。{"file": None} で止める
  sting    {"file": 曲, "len": 秒, "gain": dB} … このカットの頭で短く鳴らす曲（BGMとは別）
"""
import os
import subprocess

import cv2
import numpy as np
from PIL import Image

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
FPS = 30
SR = 44100
W, H = P.W, P.H
STYLE = "meme"      # "meme" … 参考動画ふう（大きな縁取り文字・役名札・白飛び転換） / "box" … 字幕帯＋吹き出し
WHITE_DIP = 0.25    # 場所が変わる時の白飛び（片側の秒数）
BGM_GAIN = -10      # BGM 全体をさらに下げる量（dB）。「かすかに聞こえる程度」


def music_assets():
    """CATALOG.md で ⚠（曲つき）の素材。元の音は鳴らさない。"""
    path = os.path.join(HERE, "assets", "CATALOG.md")
    out = set()
    for ln in open(path, encoding="utf-8"):
        if ln.startswith("| ") and ".mp4" in ln and "⚠" in ln:
            out.add(ln.split("|")[1].strip()[:-4])
    return out


MUSIC = music_assets()

# 素材ごとの切り取り（左, 上, 右, 下 のピクセル）。端の黒い帯・線を落とす
CROP = {
    "excited_hodomoe_city_cat": (12, 0, 0, 0),
    "itchy_kitten_butt": (100, 0, 100, 0),
    "listen_dancing_dog": (0, 0, 0, 10),
    "sad_banana_cat_cry": (0, 0, 0, 14),
}


# ---------- 猫ミーム（クロマキー） ----------

class Clip:
    """猫ミーム素材1本。緑を抜いた RGBA フレームを返す。"""

    _info = {}

    def __init__(self, name, ss=0.0, still=False, flip=False):
        self.name, self.ss, self.still, self.flip = name, ss, still, flip
        self.path = os.path.join(ASSETS, name + ".mp4")
        self.crop = CROP.get(name, (0, 0, 0, 0))
        info = Clip._info.get(name) or self._analyze()
        Clip._info[name] = info
        self.key, self.bbox, self.fps, self.n, self.cut = info
        self.cap = None
        self.cur_i = -1
        self.cur = None
        self.still_frame = None

    def _raw(self, cap):
        ok, fr = cap.read()
        if not ok:
            return None
        l, t, r, b = self.crop
        h, w = fr.shape[:2]
        return fr[t:h - b, l:w - r]

    def _analyze(self):
        cap = cv2.VideoCapture(self.path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        samples = []
        for i in np.linspace(0, max(n - 2, 0), 8).astype(int):
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(i))
            fr = self._raw(cap)
            if fr is not None:
                samples.append(fr)
        cap.release()
        # 緑の色：はっきり緑の画素の中央値（黒い帯などは除く）
        px = np.concatenate([s.reshape(-1, 3) for s in samples])
        b, g, r = px[:, 0].astype(int), px[:, 1].astype(int), px[:, 2].astype(int)
        green = px[(g > r + 40) & (g > b + 40)]
        ycc = cv2.cvtColor(np.median(green, 0).astype(np.uint8).reshape(1, 1, 3), cv2.COLOR_BGR2YCrCb)[0, 0]
        key = (int(ycc[1]), int(ycc[2]))
        # 猫が写っている範囲（全サンプルの和）
        mask = np.zeros(samples[0].shape[:2], bool)
        for s in samples:
            mask |= key_alpha(s, key) > 0.5
        mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)) > 0
        ys, xs = np.nonzero(mask)
        hh, ww = mask.shape
        bbox = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1) if len(xs) else (0, 0, ww, hh)
        # 体の途中で切れている素材（下の辺がまっすぐ）か：一番下あたりの行がどれだけ埋まっているか
        x0, y0, x1, y1 = bbox
        row = mask[max(y1 - 4, y0), x0:x1]
        cut = bool(y1 >= hh - 4 or row.mean() > 0.45)
        return key, bbox, fps, n, cut

    def frame(self, t):
        """カット内の経過秒 t のフレーム（BGR, alpha）。素材より長いときは頭に戻る。"""
        if self.still:
            if self.still_frame is None:
                cap = cv2.VideoCapture(self.path)
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(self.ss * self.fps))
                self.still_frame = self._prep(self._raw(cap))
                cap.release()
            return self.still_frame
        want = int((self.ss + t) * self.fps) % max(self.n - 1, 1)
        if self.cap is None or want < self.cur_i:
            if self.cap is not None:
                self.cap.release()
            self.cap = cv2.VideoCapture(self.path)
            if want:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, want)
            self.cur_i = want - 1
        while self.cur_i < want:
            fr = self._raw(self.cap)
            self.cur_i += 1
            if fr is None:
                break
            self.cur = fr
        if self.cur is None:
            self.cur = self._raw(cv2.VideoCapture(self.path))
        return self._prep(self.cur)

    def _prep(self, fr):
        x0, y0, x1, y1 = self.bbox
        fr = fr[y0:y1, x0:x1]
        a = key_alpha(fr, self.key)
        fr = despill(fr)
        if self.flip:
            fr, a = fr[:, ::-1], a[:, ::-1]
        return fr, a

    def close(self):
        if self.cap is not None:
            self.cap.release()


def key_alpha(bgr, key, t1=14.0, t2=34.0):
    ycc = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb).astype(np.float32)
    d = np.hypot(ycc[..., 1] - key[0], ycc[..., 2] - key[1])
    a = np.clip((d - t1) / (t2 - t1), 0, 1)
    a = cv2.erode(a, np.ones((3, 3), np.uint8))
    return cv2.GaussianBlur(a, (3, 3), 0)


def despill(bgr):
    """縁に残る緑のにじみを消す（緑を赤・青の大きいほうまで下げる）。"""
    out = bgr.copy()
    b, g, r = out[..., 0], out[..., 1], out[..., 2]
    m = np.maximum(b, r)
    out[..., 1] = np.minimum(g, m)
    return out


# ---------- 合成 ----------

def to_np(img):
    a = np.asarray(img.convert("RGBA"), np.float32) / 255.0
    return a[..., :3][..., ::-1].copy(), a[..., 3:4].copy()   # BGR, alpha


def over(dst, src, alpha, x, y):
    """dst(HxWx3 float) の (x,y) に src を alpha で重ねる（はみ出しは切る）。"""
    h, w = src.shape[:2]
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    a = alpha[y0 - y:y1 - y, x0 - x:x1 - x]
    if a.ndim == 2:
        a = a[..., None]
    d = dst[y0:y1, x0:x1]
    d *= 1 - a
    d += s * a


def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def auto_dur(cut):
    text = (cut.get("sub") or "") + (cut.get("say") or "")
    n = len(text.replace("　", "").replace(" ", ""))
    return max(cut.get("min", 1.5), 0.6 + n * 0.09)


class CutRenderer:
    def __init__(self, cut):
        self.cut = cut
        self.dur = cut.get("dur") or auto_dur(cut)
        if cut.get("bg"):
            bg = cv2.imread(cut["bg"], cv2.IMREAD_COLOR)
            self.bg = cv2.resize(bg, (W, H)).astype(np.float32) / 255.0
        else:
            self.bg = np.zeros((H, W, 3), np.float32)
        self.cats = []
        for c in cut.get("cats", []):
            clip = Clip(c["a"], c.get("ss", 0.0), c.get("still", False), c.get("flip", False))
            bx0, by0, bx1, by1 = clip.bbox
            anchored = (clip.cut or c.get("anchor")) and not c.get("float")
            # 体の途中で切れている素材は画面の下の辺から生やす（少し大きめに）
            scale = c.get("h", 560) * (1.15 if anchored else 1.0) / (by1 - by0)
            bottom = H if anchored else c.get("bottom", 850)
            self.cats.append((clip, scale, c.get("x", 960), bottom))
        # 部品（カード → 名前など → 吹き出し → 字幕 の順に重ねる）
        layers = []
        if cut.get("card"):   # カードは猫の下に敷く（右下の小さい猫がカードに隠れないように）
            self.card, self.card_a = to_np(Image.open(cut["card"]))
        else:
            self.card = None
        for ly in cut.get("layers", []):
            layers.append(Image.open(ly) if isinstance(ly, str) else ly)
        self.style = cut.get("style", STYLE)
        if self.style == "meme":
            layers += self._meme_layers(cut)
        else:
            if cut.get("say"):
                cx = cut.get("say_x") or (self.cats[0][2] if self.cats else 960)
                layers.append(P.bubble(cut["say"], name=cut.get("say_name", ""), cat_x=cx,
                                       top=cut.get("say_top", 110), color=cut.get("say_color", P.ACCENT)))
            if cut.get("sub"):
                layers.append(P.subtitle(cut["sub"]))
        comp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for ly in layers:
            comp.alpha_composite(ly.convert("RGBA"))
        self.ov, self.ov_a = to_np(comp)

    def _meme_layers(self, cut):
        """参考動画ふう：猫の反対側に大きな縁取り文字、猫の足元近くに白い役名札。"""
        out = []
        cat_x = self.cats[0][2] if self.cats else 960
        if cut.get("say"):
            if cut.get("text_box"):
                box = cut["text_box"]
            elif len(self.cats) > 1 or cut.get("text_top"):
                box = (140, 50, 1780, 430)
            elif cat_x < 960:
                box = (900, 140, 1860, 900)
            else:
                box = (60, 140, 1020, 900)
            out.append(P.big_text(cut["say"], box))
            if cut.get("say_name"):
                px, py = cut.get("plate_xy") or (max(40, int(cat_x - 330)), 770)
                out.append(P.name_plate(cut["say_name"], px, py))
        if cut.get("sub"):
            if self.card is not None:
                out.append(P.big_text(cut["sub"], (80, 812, 1840, 1062), max_size=80, min_size=48, max_lines=2))
            elif len(self.cats) > 1:
                out.append(P.big_text(cut["sub"], cut.get("text_box") or (140, 40, 1780, 360), max_size=130))
            elif self.cats:
                box = (900, 140, 1860, 900) if cat_x < 960 else (60, 140, 1020, 900)
                out.append(P.big_text(cut["sub"], cut.get("text_box") or box, max_size=130))
            else:
                out.append(P.big_text(cut["sub"], cut.get("text_box") or (160, 180, 1760, 900), max_size=140))
        return out

    def frame(self, t):
        # 背景はゆっくり寄る（参考動画ふうの時は止める）
        z = 1.0 + (0.03 * (t / self.dur) if self.style != "meme" else 0)
        if z > 1.001:
            bw, bh = int(W * z), int(H * z)
            big = cv2.resize(self.bg, (bw, bh), interpolation=cv2.INTER_LINEAR)
            ox, oy = (bw - W) // 2, (bh - H) // 2
            out = big[oy:oy + H, ox:ox + W].copy()
        else:
            out = self.bg.copy()
        k = 1.0 if self.style == "meme" else ease_out(t / 0.15)
        if self.card is not None:
            over(out, self.card, self.card_a * k, 0, 0)
        for clip, scale, cx, bottom in self.cats:
            fr, a = clip.frame(t)
            pop = 1.0 if self.style == "meme" else 0.88 + 0.12 * ease_out(t / 0.18)
            s = scale * pop
            w, h = max(1, int(fr.shape[1] * s)), max(1, int(fr.shape[0] * s))
            img = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
            al = cv2.resize(a, (w, h), interpolation=cv2.INTER_AREA)
            over(out, img, al, int(cx - w / 2), int(bottom - h))
        over(out, self.ov, self.ov_a * k, 0, 0)
        return out

    def close(self):
        for clip, *_ in self.cats:
            clip.close()


# ---------- 音 ----------

def load_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


_CAT_AUDIO = {}


def cat_audio(name):
    """猫ミーム素材の元の音（ピークを 0.6 にそろえる）。音が無い素材は None。"""
    if name not in _CAT_AUDIO:
        try:
            a = load_audio(os.path.join(ASSETS, name + ".mp4"))
            pk = np.abs(a).max()
            _CAT_AUDIO[name] = a / pk * 0.6 if pk > 1e-4 else None
        except subprocess.CalledProcessError:
            _CAT_AUDIO[name] = None
    return _CAT_AUDIO[name]


def synth(kind):
    rng = np.random.default_rng(0)
    if kind == "pop":
        n = int(0.09 * SR)
        t = np.arange(n) / SR
        f = 700 + 900 * (t / t[-1])
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40)
        return s * 0.35
    if kind == "don":
        n = int(1.1 * SR)
        t = np.arange(n) / SR
        f = 55 + 90 * np.exp(-t * 14)
        sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4)
        f2 = 200 + 180 * np.exp(-t * 20)
        body = np.sin(2 * np.pi * np.cumsum(f2) / SR) * np.exp(-t * 7)
        noise = rng.standard_normal(n)
        crack = np.convolve(noise, np.ones(4) / 4, "same") * np.exp(-t * 45)
        s = 0.7 * sub + body + 1.4 * crack
        return np.tanh(s / np.abs(s).max() * 1.6) * 0.6
    if kind == "drum":
        n = int(2.2 * SR)
        t = np.arange(n) / SR
        s = np.zeros(n)
        hit = int(0.05 * SR)
        ht = np.arange(hit) / SR
        for st in np.arange(0, 1.9, 0.05):
            i = int(st * SR)
            burst = np.convolve(rng.standard_normal(hit), np.ones(6) / 6, "same") * np.exp(-ht * 60)
            s[i:i + hit] += burst * (0.25 + 0.5 * st / 1.9)
        i = int(1.9 * SR)
        s[i:] += synth("don")[: n - i] * 0.9
        return s * 0.6
    if kind == "chime":
        a = load_audio(os.path.join(HERE, "..", "shorts", "se", "チリン.mp3"))
        return a.mean(1) * 0.5
    raise ValueError(kind)


def db(x):
    return 10 ** (x / 20)


def build_audio(cuts, starts, durs, total):
    n = int(total * SR) + SR
    mix = np.zeros((n, 2), np.float32)
    # BGM：カットで切り替え。切り替え時は前の曲を fade 秒で下げ、次の曲を上げる
    events = [(starts[i], c["bgm"]) for i, c in enumerate(cuts) if "bgm" in c]
    for k, (t0, spec) in enumerate(events):
        if not spec.get("file"):
            continue
        last = k + 1 == len(events)
        t1 = total if last else events[k + 1][0]
        a = load_audio(spec["file"])[int(spec.get("from", 0) * SR):] * db(spec.get("gain", -6) + BGM_GAIN)
        fade = spec.get("fade", 1.0)
        out_f = 2.0 if last else (events[k + 1][1].get("fade", 1.0))
        ln = int((t1 - t0 + (0 if last else out_f)) * SR)
        a = np.tile(a, (ln // len(a) + 1, 1))[:ln]
        env = np.ones(ln, np.float32)
        fi, fo = int((0.8 if k == 0 else fade) * SR), int(out_f * SR)
        env[:fi] = np.linspace(0, 1, fi)
        env[-fo:] *= np.linspace(1, 0, fo)
        i0 = int(t0 * SR)
        seg = (a * env[:, None])[: n - i0]
        mix[i0:i0 + len(seg)] += seg
    for i, c in enumerate(cuts):
        i0 = int(starts[i] * SR)
        if c.get("sting"):
            sp = c["sting"]
            a = load_audio(sp["file"])[: int(sp.get("len", 6) * SR)] * db(sp.get("gain", -8))
            fo = int(min(1.5, sp.get("len", 6) / 3) * SR)
            a[-fo:] *= np.linspace(1, 0, fo)[:, None]
            mix[i0:i0 + len(a)] += a[: n - i0]
        ses = c.get("se")
        if ses:
            for kind in ([ses] if isinstance(ses, str) else ses):
                s = synth(kind).astype(np.float32)
                mix[i0:i0 + len(s)] += np.stack([s, s], 1)[: n - i0]
        has_cat_sound = False
        for k in c.get("cats", []):
            if k.get("still") or k.get("mute") or (k["a"] in MUSIC and not k.get("sound")):
                continue
            a = cat_audio(k["a"])
            if a is None:
                continue
            ln = int(durs[i] * SR)
            st = int(k.get("ss", 0.0) * SR) % max(len(a), 1)
            a = np.concatenate([a[st:], np.tile(a, (ln // max(len(a), 1) + 1, 1))])[:ln].copy()
            f = min(int(0.03 * SR), len(a) // 2)
            if f:
                a[:f] *= np.linspace(0, 1, f)[:, None]
                a[-f:] *= np.linspace(1, 0, f)[:, None]
            g = k.get("gain", -6 if k.get("small") else -3)
            mix[i0:i0 + len(a)] += a[: n - i0] * db(g)
            has_cat_sound = True
        if c.get("say") and not c.get("no_pop") and not has_cat_sound:
            s = synth("pop").astype(np.float32) * 0.7
            j = i0 + int(0.03 * SR)
            mix[j:j + len(s)] += np.stack([s, s], 1)[: n - j]
    mix = mix[: int(total * SR)]
    peak = np.abs(mix).max()
    if peak > 0.98:
        mix *= 0.98 / peak
    return mix


# ---------- 書き出し ----------

def render(cuts, out_path, preview_dir=None):
    starts, t = [], 0.0
    durs = []
    for c in cuts:
        d = c.get("dur") or auto_dur(c)
        starts.append(t)
        durs.append(d)
        t += d
    total = t
    work = out_path + ".work"
    os.makedirs(work, exist_ok=True)
    wav = os.path.join(work, "audio.f32")
    build_audio(cuts, starts, durs, total).tofile(wav)

    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y",
         "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", wav,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out_path],
        stdin=subprocess.PIPE)
    frame_no = 0
    bgs = [c.get("bg") for c in cuts]
    for i, c in enumerate(cuts):
        r = CutRenderer(c)
        dip_in = i > 0 and bgs[i] != bgs[i - 1] and c.get("dip", True)
        dip_out = i + 1 < len(cuts) and bgs[i + 1] != bgs[i] and cuts[i + 1].get("dip", True)
        end = int(round((starts[i] + durs[i]) * FPS))
        first = True
        while frame_no < end:
            tt = frame_no / FPS - starts[i]
            img = r.frame(tt)
            w = 0.0
            if dip_in and tt < WHITE_DIP:
                w = 1 - tt / WHITE_DIP
            if dip_out and tt > durs[i] - WHITE_DIP:
                w = max(w, (tt - (durs[i] - WHITE_DIP)) / WHITE_DIP)
            if w > 0:
                img = img * (1 - w) + w
            u8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
            proc.stdin.write(u8.tobytes())
            if preview_dir and first:
                os.makedirs(preview_dir, exist_ok=True)
                mid = r.frame(min(durs[i] * 0.6, durs[i] - 0.05))
                cv2.imwrite(os.path.join(preview_dir, f"{i:03d}.jpg"),
                            (np.clip(mid, 0, 1) * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 80])
                first = False
            frame_no += 1
        r.close()
        print(f"\r{i + 1}/{len(cuts)} cuts  {frame_no / FPS:6.1f}s / {total:.1f}s", end="", flush=True)
    proc.stdin.close()
    proc.wait()
    print(f"\n-> {out_path}  ({total:.1f}s)")
    return starts, durs


def remux_audio(cuts, video_in, out_path):
    """映像はそのまま、音だけ作り直して差し替える（音量調整だけの時に速い）。"""
    starts, durs, t = [], [], 0.0
    for c in cuts:
        d = c.get("dur") or auto_dur(c)
        starts.append(t)
        durs.append(d)
        t += d
    wav = out_path + ".audio.f32"
    build_audio(cuts, starts, durs, t).tofile(wav)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video_in, "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", out_path], check=True)
    os.remove(wav)
