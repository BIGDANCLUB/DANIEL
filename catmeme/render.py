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

参考動画（ニャースインフォ）ふうの追加オプション（03_kodomo_nisa から）:
  cats の各猫に label（足元の役名札）、label_color（札の色。None は白地に黒字）
  say_style "red"   … セリフを赤い文字＋白い縁取りに（強調）
  fx       ["lines"] 集中線、["shake"] 頭で画面を揺らす、["zoom"] ゆっくり寄る
  pop_in   True で文字がポンと飛び出す（既定は NYAS_STYLE）
  inset    {"card": 解説カードPNG, "box": (x0,y0,x1,y1)} … 図だけ切り出して画面の中ほどに置く
  place    画面左上の小さな地名・場所の字幕
  explain  説明モード：画面を灰色の小窓に縮め、黒地の下に説明文を出す
  chapter  黒い画面の中央に小さな文字（「本題に入るその前に…」など）
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
BGM_GAIN = -10
NYAS_STYLE = False  # True で文字の飛び出しなど参考動画ふうの動きを既定にする（動画ごとのスクリプトで切り替え）
TEMPO = 1.15        # 全カットの長さにかける倍率（大きいほどゆっくり）      # BGM 全体をさらに下げる量（dB）。「かすかに聞こえる程度」


def music_assets():
    """CATALOG.md で ⚠（曲つき）の素材。元の音は鳴らさない。"""
    path = os.path.join(HERE, "assets", "CATALOG.md")
    out = set()
    for ln in open(path, encoding="utf-8"):
        if ln.startswith("| ") and ".mp4" in ln and "⚠" in ln:
            out.add(ln.split("|")[1].strip()[:-4])
    return out


MUSIC = music_assets()


def load_play():
    """assets/play.json … 素材ごとの流し方（最後まで流す／何秒で切る）。どの動画でも共通。"""
    import json
    path = os.path.join(HERE, "assets", "play.json")
    if not os.path.exists(path):
        return {}
    return {k: v for k, v in json.load(open(path, encoding="utf-8")).items() if not k.startswith("_")}


ASSET_PLAY = load_play()
AUTO_PLAY = True   # True なら play.json の設定を、その素材を使う全カットに自動で当てる
PLAY_MUSIC_ASSETS = True   # 曲つき素材の音も鳴らす（鳴っている間は BGM を下げる）
MUSIC_DUCK = -14
FG_DUCK = -20              # 猫の音・SEが鳴っている間の全体BGMの下げ幅（dB）
FG_THRESHOLD = -45         # これより大きい音（dBFS）が鳴っていたら「鳴っている」とみなす
SE_GAIN = -4               # 効果音の基本の音量（dB、ピーク0.6にそろえた後）           # 曲つき素材が鳴っている間の BGM の下げ幅（dB）


def sounding(k):
    """このカットの猫 k の元の音を鳴らすか。"""
    if k.get("still") or k.get("mute"):
        return False
    return PLAY_MUSIC_ASSETS or k["a"] not in MUSIC or k.get("sound")

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


_DUR_CACHE = {}


def cut_dur(cut):
    """カットの長さ。猫ミームの音が鳴るカットは、音が途中で切れないよう、近くの「音の切れ目」まで伸び縮みさせる。"""
    for k in cut.get("cats", []):
        cfg = ASSET_PLAY.get(k["a"])
        if AUTO_PLAY and cfg and not k.get("still") and not k.get("small") and "full" not in k:
            k["full"] = True
            if cfg.get("until") and "until" not in k:
                k["until"] = cfg["until"]
    full = [k for k in cut.get("cats", []) if k.get("full")]
    if full:   # 素材を最後まで流す
        lens = [len(cat_audio(k["a"])) / SR - k.get("ss", 0.0) if cat_audio(k["a"]) is not None
                else Clip(k["a"]).n / Clip(k["a"]).fps - k.get("ss", 0.0) for k in full]
        lens = [min(l, k["until"] - k.get("ss", 0.0)) if k.get("until") else l for l, k in zip(lens, full)]
        return max(lens)
    base = (cut.get("dur") or auto_dur(cut)) * TEMPO
    if cut.get("fixed"):
        return base
    for k in cut.get("cats", []):
        if not sounding(k):
            continue
        key = (k["a"], round(k.get("ss", 0.0), 2), round(base, 3))
        if key not in _DUR_CACHE:
            _DUR_CACHE[key] = natural_end(k["a"], k.get("ss", 0.0), base)
        return _DUR_CACHE[key]
    return base


def natural_end(name, ss, target, lo=0.85, hi=1.5, extra=1.5):
    """target 秒の近くで、素材の音が静かになる所（ひと区切り）を探して、その秒数を返す。
    見つからなければ target のまま（その場合は終わりを長めにフェードする）。"""
    a = cat_audio(name)
    if a is None:
        return target
    st = int(ss * SR) % max(len(a), 1)
    need = int((target * hi + extra) * SR)
    buf = np.concatenate([a[st:], np.tile(a, (need // max(len(a), 1) + 1, 1))])[:need].mean(1)
    hop = int(0.02 * SR)
    n = len(buf) // hop
    env = 20 * np.log10(np.sqrt((buf[: n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-6)
    loud = np.percentile(env, 95)
    quiet = env < max(loud - 26, -55)
    # 素材の音が target より前に自然に終わっている → そのままでよい
    if quiet[int(target / 0.02) - 1:].all() if int(target / 0.02) - 1 < n else True:
        return target
    # 60ms 以上続く静かな所の始まりを候補にする
    cands = [i * 0.02 for i in range(1, n - 3) if quiet[i] and quiet[i + 1] and quiet[i + 2] and not quiet[i - 1]]
    lo_t, hi_t = max(1.0, target * lo), min(target * hi, target + extra)
    inside = [t for t in cands if lo_t <= t <= hi_t]
    if inside:
        return min(inside, key=lambda t: abs(t - target) * (1.0 if t >= target else 1.4)) + 0.06
    # 静かな所が無い（ずっと鳴っている）素材は、音がいちばん深く落ち込む所（言葉や拍の切れ目）で切る
    sm = np.convolve(env, np.ones(5) / 5, "same")
    best, best_score = target, -1e9
    for i in range(int(lo_t / 0.02), min(int(hi_t / 0.02), n - 15)):
        if sm[i] <= sm[i - 1] and sm[i] <= sm[i + 1]:
            depth = min(sm[max(0, i - 15):i].max(), sm[i + 1:i + 16].max()) - sm[i]
            score = depth - 3.0 * abs(i * 0.02 - target)
            if depth >= 4 and score > best_score:
                best, best_score = i * 0.02 + 0.02, score
    return best


def auto_dur(cut):
    text = (cut.get("sub") or "") + (cut.get("say") or "")
    n = len(text.replace("　", "").replace(" ", ""))
    return max(cut.get("min", 1.5), 0.6 + n * 0.09)


class CutRenderer:
    def __init__(self, cut):
        self.cut = cut
        self.dur = cut_dur(cut)
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
        # 足元の役名札
        self.labels = []
        for (clip, scale, cx, bottom), c in zip(self.cats, cut.get("cats", [])):
            if c.get("label"):
                tag = P.label_tag(c["label"], c.get("label_color"), size=c.get("label_size", 58))
                y = min(bottom, H) - tag.height - c.get("label_up", 40)
                self.labels.append((to_np(tag), int(cx - tag.width / 2), int(y)))
        # 集中線（数枚を切り替えてチラつかせる）
        fx = cut.get("fx", [])
        self.lines = [to_np(P.speed_lines(cut.get("lines_c", (960, 540)), cut.get("lines_color", (255, 255, 255)), seed=k))
                      for k in range(3)] if "lines" in fx else []
        self.fx = fx
        # 図の差し込み（解説カードから図の部分だけ切り出す）
        self.inset = None
        if cut.get("inset"):
            im = Image.open(cut["inset"]["card"]).convert("RGBA")
            im = im.crop(im.getbbox())
            x0, y0, x1, y1 = cut["inset"]["box"]
            k = min((x1 - x0) / im.width, (y1 - y0) / im.height)
            im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
            self.inset = (to_np(im), int((x0 + x1 - im.width) / 2), int((y0 + y1 - im.height) / 2))
        # 部品（カード → 名前など → 吹き出し → 字幕 の順に重ねる）
        layers = []
        if cut.get("card"):   # カードは猫の下に敷く（右下の小さい猫がカードに隠れないように）
            self.card, self.card_a = to_np(Image.open(cut["card"]))
        else:
            self.card = None
        for ly in cut.get("layers", []):
            layers.append(Image.open(ly) if isinstance(ly, str) else ly)
        self.style = cut.get("style", STYLE)
        txt = []
        if self.style == "meme":
            txt += self._meme_layers(cut)
        else:
            if cut.get("say"):
                cx = cut.get("say_x") or (self.cats[0][2] if self.cats else 960)
                layers.append(P.bubble(cut["say"], name=cut.get("say_name", ""), cat_x=cx,
                                       top=cut.get("say_top", 110), color=cut.get("say_color", P.ACCENT)))
            if cut.get("sub"):
                layers.append(P.subtitle(cut["sub"]))
        # 決まった時間だけ出す短いセリフ（例：猫が鳴いた瞬間の「はい」）
        self.pop_in = cut.get("pop_in", NYAS_STYLE)
        self.pops = []
        for pp in cut.get("pops", []):
            red = pp.get("style") == "red"
            im = P.big_text(pp["text"], pp["box"], max_size=pp.get("size", 110), max_lines=pp.get("lines", 1),
                            fill=P.RED_TEXT if red else P.WHITE, stroke=P.WHITE if red else (0, 0, 0))
            self.pops.append((pp["t"], pp["t"] + pp.get("dur", 0.9), self._crop(im)))
        if cut.get("place"):
            pl = P.canvas()
            from PIL import ImageDraw
            ImageDraw.Draw(pl).text((44, 30), cut["place"], font=P.font("black", 46), fill=P.WHITE,
                                    stroke_width=5, stroke_fill=(0, 0, 0))
            layers.append(pl)
        if cut.get("chapter"):
            txt.append(P.plain_text(cut["chapter"], (160, 400, 1760, 680), size=cut.get("chapter_size", 64)))
        comp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for ly in layers:
            comp.alpha_composite(ly.convert("RGBA"))
        self.ov, self.ov_a = to_np(comp)
        tc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for ly in txt:
            tc.alpha_composite(ly.convert("RGBA"))
        self.txt = self._crop(tc)
        self.explain = None
        if cut.get("explain"):
            self.explain = to_np(P.plain_text(cut["explain"], (120, 700, 1800, 1050), size=cut.get("explain_size", 62)))

    @staticmethod
    def _crop(im):
        """透過画像を中身の部分だけに切り出す（飛び出し表示で拡大縮小するため）。"""
        bb = im.getbbox()
        if not bb:
            return None
        return to_np(im.crop(bb)) + (bb[0], bb[1])

    def _pop(self, out, item, t, start=0.0):
        """文字を重ねる。pop_in の時は頭の0.2秒で小さい所からポンと大きくなる。"""
        if item is None:
            return
        img, a, x, y = item
        dt = t - start
        if self.pop_in and dt < 0.2:
            s = 0.55 + 0.6 * ease_out(dt / 0.12) if dt < 0.12 else 1.15 - 0.15 * ease_out((dt - 0.12) / 0.08)
            h, w = img.shape[:2]
            nw, nh = max(1, int(w * s)), max(1, int(h * s))
            img2 = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
            a2 = cv2.resize(a, (nw, nh), interpolation=cv2.INTER_LINEAR)
            over(out, img2, a2, int(x + w / 2 - nw / 2), int(y + h / 2 - nh / 2))
        else:
            over(out, img, a, x, y)

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
            red = cut.get("say_style") == "red"
            out.append(P.big_text(cut["say"], box, max_size=cut.get("say_size", 150),
                                  fill=P.RED_TEXT if red else P.WHITE, stroke=P.WHITE if red else (0, 0, 0)))
            if cut.get("say_name") and not any(c.get("label") for c in cut.get("cats", [])):
                px, py = cut.get("plate_xy") or (max(40, int(cat_x - 330)), 770)
                out.append(P.name_plate(cut["say_name"], px, py))
        if cut.get("sub"):
            if cut.get("sub_box"):
                red = cut.get("say_style") == "red"
                out.append(P.big_text(cut["sub"], cut["sub_box"], max_size=cut.get("sub_size", 90), min_size=44,
                                      max_lines=3, fill=P.RED_TEXT if red else P.WHITE, stroke=P.WHITE if red else (0, 0, 0)))
            elif self.card is not None:
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
        if self.lines:
            ln, la = self.lines[int(t * FPS / 3) % len(self.lines)]
            over(out, ln, la, 0, 0)
        if self.card is not None:
            over(out, self.card, self.card_a * k, 0, 0)
        if self.inset is not None:
            (im, ia), x, y = self.inset
            if self.cut.get("inset_still"):   # 前のカットと同じ図なら飛び出さずにそのまま
                over(out, im, ia, x, y)
            else:
                self._pop(out, (im, ia, x, y), t)
        for clip, scale, cx, bottom in self.cats:
            fr, a = clip.frame(t)
            pop = 1.0 if self.style == "meme" else 0.88 + 0.12 * ease_out(t / 0.18)
            s = scale * pop
            w, h = max(1, int(fr.shape[1] * s)), max(1, int(fr.shape[0] * s))
            img = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
            al = cv2.resize(a, (w, h), interpolation=cv2.INTER_AREA)
            over(out, img, al, int(cx - w / 2), int(bottom - h))
        for (im, ia), x, y in self.labels:
            over(out, im, ia, x, y)
        over(out, self.ov, self.ov_a * k, 0, 0)
        self._pop(out, self.txt, t)
        for t0, t1, item in self.pops:
            if t0 <= t < t1:
                self._pop(out, item, t, t0)
        if "zoom" in self.fx:   # ゆっくり寄る
            z = 1.0 + 0.06 * (t / self.dur)
            bw, bh = int(W * z), int(H * z)
            big = cv2.resize(out, (bw, bh), interpolation=cv2.INTER_LINEAR)
            ox, oy = (bw - W) // 2, (bh - H) // 2
            out = big[oy:oy + H, ox:ox + W].copy()
        if "shake" in self.fx and t < 0.35:   # 頭で小刻みに揺らす
            amp = 18 * (1 - t / 0.35)
            dx, dy = amp * np.sin(t * 90), amp * np.cos(t * 70)
            out = cv2.warpAffine(out, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REPLICATE)
        if self.explain is not None:   # 説明モード：灰色の小窓＋黒地に説明文
            g = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
            g = np.repeat(g[..., None], 3, 2)
            sc = 0.55 if t >= 0.18 else 1.0 - 0.45 * ease_out(t / 0.18)
            sw, sh = int(W * sc), int(H * sc)
            small = cv2.resize(g, (sw, sh), interpolation=cv2.INTER_AREA)
            out = np.zeros((H, W, 3), np.float32)
            y0 = int(40 * (1 - sc) / 0.45) if sc < 1 else 0
            out[y0:y0 + sh, (W - sw) // 2:(W - sw) // 2 + sw] = small
            if t >= 0.18:
                ei, ea = self.explain
                over(out, ei, ea, 0, 0)
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


SE_DIR = os.path.join(HERE, "se")


def synth(kind):
    """効果音。se/ に同じ名前のファイル（例 se/don.mp3）があればそれを使い、無ければ合成する。"""
    for ext in (".mp3", ".wav", ".m4a", ""):
        path = os.path.join(SE_DIR, kind + ext)
        if ext != "" or os.path.splitext(kind)[1]:
            if os.path.isfile(path):
                a = load_audio(path).mean(1)
                return a / max(np.abs(a).max(), 1e-6) * 0.6
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
    # 曲つき素材が鳴るカットの間は BGM を下げる
    duck = np.ones(n, np.float32)
    ramp = int(0.25 * SR)
    for i, c in enumerate(cuts):
        if any(sounding(k) and k["a"] in MUSIC for k in c.get("cats", [])):
            a0, a1 = int(starts[i] * SR), int((starts[i] + durs[i]) * SR)
            g = db(MUSIC_DUCK)
            duck[a0:a1] = np.minimum(duck[a0:a1], g)
            r0 = np.linspace(1, g, ramp)
            seg = duck[max(0, a0 - ramp):a0]
            duck[max(0, a0 - ramp):a0] = np.minimum(seg, r0[-len(seg):] if len(seg) else seg)
            seg = duck[a1:a1 + ramp]
            duck[a1:a1 + ramp] = np.minimum(seg, r0[::-1][:len(seg)])
    bgm_mix = np.zeros((n, 2), np.float32)
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
        bgm_mix[i0:i0 + len(seg)] += seg
    # BGM は最後に混ぜる（猫の音・SEが鳴っている所で下げるため）
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
            for sp in ([ses] if isinstance(ses, (str, dict)) else ses):
                sp = {"f": sp} if isinstance(sp, str) else sp
                s = synth(sp["f"]).astype(np.float32) * db(sp.get("gain", SE_GAIN))
                # 長いSEはカットの終わり（＋少し）で切ってフェード
                ln = int(min(len(s) / SR, sp.get("len", durs[i] + 0.4)) * SR)
                if ln < len(s):
                    s = s[:ln].copy()
                    fo = min(int(0.25 * SR), ln // 2)
                    s[-fo:] *= np.linspace(1, 0, fo)
                j = i0 + int(sp.get("at", 0.0) * SR)
                mix[j:j + len(s)] += np.stack([s, s], 1)[: max(0, n - j)]
        has_cat_sound = False
        for k in c.get("cats", []):
            if not sounding(k):
                continue
            a = cat_audio(k["a"])
            if a is None:
                continue
            ln = int(durs[i] * SR)
            st = int(k.get("ss", 0.0) * SR) % max(len(a), 1)
            a = np.concatenate([a[st:], np.tile(a, (ln // max(len(a), 1) + 1, 1))])[:ln].copy()
            f, fo = min(int(0.02 * SR), len(a) // 2), min(int(0.2 * SR), len(a) // 2)
            if f:
                a[:f] *= np.linspace(0, 1, f)[:, None]
                a[-fo:] *= np.linspace(1, 0, fo)[:, None]
            g = k.get("gain", -6 if k.get("small") else -3)
            mix[i0:i0 + len(a)] += a[: n - i0] * db(g)
            has_cat_sound = True
        if c.get("say") and not c.get("no_pop") and not has_cat_sound:
            s = synth("pop").astype(np.float32) * 0.7
            j = i0 + int(0.03 * SR)
            mix[j:j + len(s)] += np.stack([s, s], 1)[: n - j]
    # 猫ミームの音・SE・短い曲が鳴っている間は、全体BGMを大きく下げる（ダッキング）
    hop = int(0.02 * SR)
    m = n // hop
    lvl = 20 * np.log10(np.sqrt((mix[: m * hop].mean(1).reshape(m, hop) ** 2).mean(1)) + 1e-9)
    target = np.where(lvl > FG_THRESHOLD, db(FG_DUCK), 1.0).astype(np.float32)
    g = np.empty_like(target)
    cur = 1.0
    a_att, a_rel = 1 - np.exp(-1 / (0.04 / 0.02)), 1 - np.exp(-1 / (0.5 / 0.02))   # 下げるのは速く、戻すのはゆっくり
    for i in range(m):
        cur += (target[i] - cur) * (a_att if target[i] < cur else a_rel)
        g[i] = cur
    env = np.repeat(g, hop)
    env = np.concatenate([env, np.full(n - len(env), env[-1] if len(env) else 1.0)])
    mix += bgm_mix * np.minimum(env, duck)[:, None]
    mix = mix[: int(total * SR)]
    peak = np.abs(mix).max()
    if peak > 0.85:
        mix *= 0.85 / peak
    return mix


# ---------- 書き出し ----------

def render(cuts, out_path, preview_dir=None):
    starts, t = [], 0.0
    durs = []
    for c in cuts:
        d = cut_dur(c)
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
        dip_in = WHITE_DIP > 0 and i > 0 and bgs[i] != bgs[i - 1] and c.get("dip", True)
        dip_out = WHITE_DIP > 0 and i + 1 < len(cuts) and bgs[i + 1] != bgs[i] and cuts[i + 1].get("dip", True)
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
        d = cut_dur(c)
        starts.append(t)
        durs.append(d)
        t += d
    wav = out_path + ".audio.f32"
    build_audio(cuts, starts, durs, t).tofile(wav)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video_in, "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", out_path], check=True)
    os.remove(wav)
