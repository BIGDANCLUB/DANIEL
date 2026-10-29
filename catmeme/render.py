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
  fx       ["lines"] 集中線、["shake"] 頭で画面を揺らす、["zoom"] ゆっくり寄る、["punch"] 頭でグッと寄る、["flash"] 頭で白く光る、
           ["spark"] キラキラ、["dim"] 画面を半分暗く（その上に layers_top を重ねる）
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
AVOID_TEXT = False   # True で、猫を大きな文字から離して置く
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


def trim(pair):
    """全画面の透過レイヤーを、中身のある範囲だけに切り詰める → (img, alpha, x, y)。
    毎フレームの重ね合わせが画面全体ではなく中身の範囲だけになるので速い（10/14）。中身がなければ None。"""
    img, a = pair
    m = a[..., 0] > 0 if a.ndim == 3 else a > 0
    ys, xs = np.nonzero(m.any(1))[0], np.nonzero(m.any(0))[0]
    if not len(ys):
        return None
    y0, y1, x0, x1 = ys[0], ys[-1] + 1, xs[0], xs[-1] + 1
    return img[y0:y1, x0:x1].copy(), a[y0:y1, x0:x1].copy(), int(x0), int(y0)


def over_t(dst, tr, k=1.0):
    """trim() したレイヤーを重ねる。k は透明度（1 なら掛け算しない）。"""
    if tr is None:
        return
    img, a, x, y = tr
    over(dst, img, a if k >= 1.0 else a * k, x, y)


def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


_DUR_CACHE = {}


# この素材が出るカットは、最低この秒数は見せる（ユーザー指定 10/8：dance_edm_cat は5秒以上）
ASSET_MIN_DUR = {"dance_edm_cat": 5.0}


def cut_dur(cut):
    d = _cut_dur(cut)
    mins = [ASSET_MIN_DUR[k["a"]] for k in cut.get("cats", []) if k["a"] in ASSET_MIN_DUR and not k.get("small")]
    return max([d] + mins)


def _cut_dur(cut):
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


VIDEO_DIR = os.path.join(HERE, "assets_video")


def fitted_video(path, size):
    """動く背景を画面の大きさ（size）に合わせた版を返す。合わせた版は assets_video/_fitted/ に保存して覚えておき、
    2回目からは変換せずにそれを使う（10/14 ユーザー指定「一度使った映像は調整したサイズを記憶」）。"""
    w, h = size
    cap = cv2.VideoCapture(path)
    vw, vh = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    if (vw, vh) == (w, h):
        return path
    d = os.path.join(HERE, "assets_video", "_fitted")
    out = os.path.join(d, f"{os.path.splitext(os.path.basename(path))[0]}_{w}x{h}.mp4")
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(path):
        return out
    os.makedirs(d, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-an",
                    "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}",
                    "-c:v", "libx264", "-crf", "16", "-preset", "fast", out + ".tmp.mp4"], check=True)
    os.replace(out + ".tmp.mp4", out)
    return out


EXPLAIN_TOP = 680   # 説明モードの黒い字幕帯の上の端


# ユーザーが渡した写真（静止画）は、ゆっくり横・縦に動かして動画っぽく見せる（10/14 ユーザー指定）
PAN_DIRS = ("13_yard", "added")
PAN_ZOOM = 1.10


def pan_mode(cut):
    """写真の動かし方を決める。cut["pan"] で指定もできる（"lr" "rl" "ud" "du" "in"、False で止める）。"""
    if "pan" in cut:
        return cut["pan"] or None
    d = os.path.basename(os.path.dirname(cut["bg"]))
    if d not in PAN_DIRS:
        return None
    import zlib
    key = (cut["bg"] + str(cut.get("say") or cut.get("sub") or cut.get("explain") or "")).encode("utf-8")
    return ("lr", "rl", "lr", "rl", "in", "du")[zlib.crc32(key) % 6]


def pan_frame(big, mode, p):
    """少し大きくした写真 big から、進み具合 p（0〜1）の位置を画面の大きさで切り出す。小数の位置も滑らかに。"""
    bh, bw = big.shape[:2]
    mx, my = bw - W, bh - H
    e = p * p * (3 - 2 * p) * 0.6 + p * 0.4   # はじめと終わりを少しゆるやかに
    if mode == "in":   # ゆっくり寄りながら少し右へ
        z = 1.0 + 0.06 * e
        cx, cy = bw / 2 + mx * 0.15 * e, bh / 2
        m = np.float32([[z, 0, W / 2 - cx * z], [0, z, H / 2 - cy * z]])
        return cv2.warpAffine(big, m, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    x = {"lr": mx * e, "rl": mx * (1 - e)}.get(mode, mx / 2)
    y = {"ud": my * e, "du": my * (1 - e)}.get(mode, my / 2)
    m = np.float32([[1, 0, -x], [0, 1, -y]])
    return cv2.warpAffine(big, m, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


class VideoBG:
    """動く背景（assets_video/ の mp4）。カットの頭から順に読み、短ければ頭に戻ってくり返す（10/13 追加）。"""

    def __init__(self, path, size, ss=0.0):
        path = fitted_video(path, size)
        self.path, self.size, self.ss = path, size, ss
        self.cap = cv2.VideoCapture(path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
        self.pos, self.last = -1, None

    def frame(self, t):
        want = int((self.ss + t) * self.fps) % self.n
        if want != self.pos + 1:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, want)
        ok, fr = self.cap.read()
        if not ok:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, fr = self.cap.read()
        self.pos = want
        if ok and fr.shape[1::-1] == tuple(self.size):   # すでに画面の大きさ（変換ずみ）ならそのまま使う
            self.last = fr.astype(np.float32) / 255.0
        elif ok:
            w, h = self.size
            fh, fw = fr.shape[:2]
            k = max(w / fw, h / fh)
            fr = cv2.resize(fr, (int(fw * k + 0.5), int(fh * k + 0.5)), interpolation=cv2.INTER_AREA)
            y0, x0 = (fr.shape[0] - h) // 2, (fr.shape[1] - w) // 2
            self.last = fr[y0:y0 + h, x0:x0 + w].astype(np.float32) / 255.0
        return self.last

    def close(self):
        self.cap.release()


def crack_lines(c, seed=0):
    """ガラスのヒビ：中心から放射状のギザギザの線＋それをつなぐ線。"""
    rng = np.random.default_rng(seed)
    cx, cy = c
    rays, out = [], []
    for k in range(11):
        ang = k / 11 * 2 * np.pi + rng.uniform(-0.2, 0.2)
        pts, r = [(cx, cy)], 0
        while r < 1300:
            r += rng.uniform(60, 140)
            a_ = ang + rng.uniform(-0.12, 0.12)
            pts.append((cx + r * np.cos(a_), cy + r * np.sin(a_)))
        rays.append(np.array(pts))
        out.append(np.array(pts, np.int32))
    for ring in (1, 3):   # 放射の線どうしをつなぐ
        for k in range(len(rays)):
            p1, p2 = rays[k], rays[(k + 1) % len(rays)]
            if len(p1) > ring and len(p2) > ring:
                out.append(np.array([p1[ring], p2[ring]], np.int32))
    return out


QM_COLS = [(255, 60, 90), (255, 205, 0), (40, 200, 255), (150, 90, 255), (60, 225, 120), (255, 120, 210), (255, 140, 30)]


def qmark_img(ch, size, j):
    """色つきの「？」1文字：まわりに同じ色の光（ぼかし）・黒いふち・白いふち。"""
    from PIL import ImageFilter, ImageDraw
    col = QM_COLS[j % len(QM_COLS)]
    f = P.font("black", size)
    pad = size // 3
    im = Image.new("RGBA", (int(size * 1.1) + pad * 2, int(size * 1.3) + pad * 2), (0, 0, 0, 0))
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).text((pad, pad // 2), ch, font=f, fill=col + (255,), stroke_width=26, stroke_fill=col + (255,))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(im)
    d.text((pad, pad // 2), ch, font=f, fill=(20, 20, 30, 255), stroke_width=20, stroke_fill=(20, 20, 30, 255))
    d.text((pad, pad // 2), ch, font=f, fill=col + (255,), stroke_width=9, stroke_fill=(255, 255, 255, 255))
    return im.crop(im.getbbox())


class CutRenderer:
    def __init__(self, cut):
        self.cut = cut
        self.dur = cut_dur(cut)
        self.vbg = None
        self.pan = None
        if cut.get("bg") and cut["bg"].endswith(".mp4"):   # 動く背景
            self.vbg = VideoBG(cut["bg"], (W, H), cut.get("bg_ss", 0.0))
            self.bg = self.vbg.frame(0.0)
        elif cut.get("bg"):
            bg = cv2.imread(cut["bg"], cv2.IMREAD_COLOR)
            self.bg = cv2.resize(bg, (W, H)).astype(np.float32) / 255.0
            self.pan = pan_mode(cut)
            if self.pan:   # 少し大きくしておき、その中をゆっくり動かす
                self.bg_big = cv2.resize(bg, (int(W * PAN_ZOOM), int(H * PAN_ZOOM)),
                                         interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        else:
            self.bg = np.zeros((H, W, 3), np.float32)
        if cut.get("bg2"):   # 画面を左右半分に分けて、左と右で別の背景（比べる動画・10/29）
            halves = []
            for pth in (cut["bg"], cut["bg2"]):
                im_ = cv2.imread(pth, cv2.IMREAD_COLOR)
                k_ = H / im_.shape[0]
                im_ = cv2.resize(im_, (int(im_.shape[1] * k_), H))
                x_ = (im_.shape[1] - W // 2) // 2
                halves.append(im_[:, x_:x_ + W // 2].astype(np.float32) / 255.0)
            self.bg = np.concatenate(halves, axis=1)
            self.pan = None
        self.cats = []
        for c in cut.get("cats", []):
            clip = Clip(c["a"], c.get("ss", 0.0), c.get("still", False), c.get("flip", False))
            bx0, by0, bx1, by1 = clip.bbox
            anchored = (clip.cut or c.get("anchor")) and not c.get("float")
            # 体の途中で切れている素材は画面の下の辺から生やす（少し大きめに）
            scale = c.get("h", 560) * (1.15 if anchored else 1.0) / (by1 - by0)
            bottom = H if anchored else c.get("bottom", 850)
            if cut.get("explain") and bottom > EXPLAIN_TOP - 10:
                # 説明モード：猫は下の黒い字幕帯にかからないよう、帯の上に収める（役名札は帯にかかってもよい）
                # 10/14 ユーザー指定
                hh = min(c.get("h", 560), EXPLAIN_TOP - 10 - 30)
                scale = hh / (by1 - by0)
                bottom = EXPLAIN_TOP - 10
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
        self.lines_t = [trim(x) for x in self.lines]
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
            self.card_t = trim((self.card, self.card_a))
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
                            fill=P.RED_TEXT if red else P.WHITE, stroke=P.WHITE if red else (0, 0, 0),
                            align=pp.get("align", "center"))
            self.pops.append((pp["t"], pp["t"] + pp.get("dur", 0.9), self._crop(im)))
        if cut.get("place"):
            pl = P.canvas()
            from PIL import ImageDraw
            ImageDraw.Draw(pl).text((44, 30), cut["place"], font=P.font("black", 46), fill=P.WHITE,
                                    stroke_width=5, stroke_fill=(0, 0, 0))
            layers.append(pl)
        if cut.get("chapter"):
            txt.append(P.plain_text(cut["chapter"], (160, 300, 1760, 780), size=cut.get("chapter_size", 64)))
        for side_t, box in zip(cut.get("side_text") or (), ((40, 300, 920, 560), (1000, 300, 1880, 560))):   # 左右それぞれの金額など
            if side_t:
                layers.append(P.big_text(side_t, box, max_size=cut.get("side_size", 120), max_lines=2, fill=P.RED_TEXT, stroke=P.WHITE))
        comp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for ly in layers:
            comp.alpha_composite(ly.convert("RGBA"))
        self.ov, self.ov_a = to_np(comp)
        self.ov_t = trim((self.ov, self.ov_a))
        tc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for ly in txt:
            tc.alpha_composite(ly.convert("RGBA"))
        self.txt = self._crop(tc)
        if AVOID_TEXT and self.style == "meme" and not cut.get("keep_overlap"):
            self._avoid_text([ly.convert("RGBA").getbbox() for ly in txt], cut)
        self.top = None
        if cut.get("layers_top"):
            tc2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            for ly in cut["layers_top"]:
                tc2.alpha_composite((Image.open(ly) if isinstance(ly, str) else ly).convert("RGBA"))
            self.top = trim(to_np(tc2))
        fxs = cut.get("fx", [])
        self.crack = crack_lines(cut.get("crack_xy", (960, 560)), seed=len(cut.get("say") or "")) if "crack" in fxs else None
        self.bills = [(np.random.default_rng(i).uniform(0, W), np.random.default_rng(i + 99).uniform(0, 1), i) for i in range(20)] \
            if "money" in fxs else None
        self.slot = cut.get("slot")
        self.slot_cache = {}
        self.split_heads = None
        if cut.get("split"):   # 画面分割：左右の見出し
            self.split_heads = [to_np(P.label_tag(t_, c_, size=cut.get("split_size", 64)))
                                for t_, c_ in zip(cut["split"], cut.get("split_cols", ((200, 30, 30), (0, 110, 210))))]
            self.split_y = cut.get("split_y", 440)
        self.qm = None
        if cut.get("qmarks"):   # 「？？？？？？」をいろいろな色とエフェクトで飾る（コナンの連打の場面・10/28 ユーザー指定）
            self.qm = [qmark_img(cut.get("qmark_char", "？"), cut.get("qmark_size", 230), j) for j in range(cut["qmarks"])]
            self.qm_y = cut.get("qmark_y", 250)
        self.explain = None
        if cut.get("explain"):
            self.explain = to_np(P.plain_text(cut["explain"], (60, 695, 1860, 1070), size=cut.get("explain_size", 100), gap=1.22))
            self.explain_t = trim(self.explain)

    def _avoid_text(self, boxes, cut):
        """猫と大きな文字が重ならないように、猫を文字から離す。
        文字が上にあるときは猫を小さくして下げる。横にあるときは反対側へずらす。"""
        boxes = [b for b in boxes if b]
        if not boxes:
            return
        m = 18   # 文字と猫のすき間
        new = []
        for (clip, scale, cx, bottom), c in zip(self.cats, cut.get("cats", [])):
            if c.get("small"):
                new.append((clip, scale, cx, bottom))
                continue
            bx0, by0, bx1, by1 = clip.bbox
            for tx0, ty0, tx1, ty1 in boxes:
                w, h = (bx1 - bx0) * scale, (by1 - by0) * scale
                x0, x1, y0 = cx - w / 2, cx + w / 2, bottom - h
                if min(x1, tx1 + m) - max(x0, tx0 - m) <= 0 or min(bottom, ty1 + m) - max(y0, ty0 - m) <= 0:
                    continue
                # 文字が猫の真上にかかっているときだけ「上」。猫の横にある文字（1匹＋反対側の文字）は横によける
                # （10/12：横の文字を「上」とみなして猫を画面の下へ押し出し、見切れていたのを直した）
                above = (ty0 + ty1) / 2 < y0 + h * 0.35 and tx0 - m < cx < tx1 + m
                if above:   # 文字が上 → 小さくして、足りない分は下へ
                    need = ty1 + m - y0
                    f = max(0.62, (h - need) / h)
                    scale *= f
                    rest = need - h * (1 - f)
                    if rest > 0:
                        bottom = min(bottom + rest, H + h * f * 0.35)
                else:   # 文字が横 → 反対側へずらす（はみ出す分は小さく）
                    if (tx0 + tx1) / 2 > cx:
                        shift = x1 - (tx0 - m)
                        ncx = max(w * 0.5, cx - shift)   # 画面からはみ出さない（はみ出す分は小さくする）
                    else:
                        shift = (tx1 + m) - x0
                        ncx = min(W - w * 0.5, cx + shift)
                    left = shift - abs(ncx - cx)
                    cx = ncx
                    if left > 0:
                        scale *= max(0.62, (w - 2 * left) / w)
            new.append((clip, scale, cx, bottom))
        self.cats = new
        self.labels = []
        for (clip, scale, cx, bottom), c in zip(self.cats, cut.get("cats", [])):
            if c.get("label"):
                tag = P.label_tag(c["label"], c.get("label_color"), size=c.get("label_size", 58))
                y = min(bottom, H) - tag.height - c.get("label_up", 40)
                self.labels.append((to_np(tag), int(cx - tag.width / 2), int(y)))

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
        if self.vbg is not None:
            self.bg = self.vbg.frame(t)
        # 背景はゆっくり寄る（参考動画ふうの時は止める）
        z = 1.0 + (0.03 * (t / self.dur) if self.style != "meme" else 0)
        if self.pan:
            out = pan_frame(self.bg_big, self.pan, t / max(self.dur, 0.01))
        elif z > 1.001:
            bw, bh = int(W * z), int(H * z)
            big = cv2.resize(self.bg, (bw, bh), interpolation=cv2.INTER_LINEAR)
            ox, oy = (bw - W) // 2, (bh - H) // 2
            out = big[oy:oy + H, ox:ox + W].copy()
        else:
            out = self.bg.copy()
        if "swirl" in self.fx:   # ぐるぐる：背景だけゆっくり回る（混乱の場面・10/29）
            M = cv2.getRotationMatrix2D((W / 2, H / 2), 28 * t, 1.55)
            out = cv2.warpAffine(out, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        if self.split_heads:   # 画面分割：左は赤み・右は青み、まん中に太い線
            tint = self.cut.get("split_tint", 0.2)
            out[:, : W // 2] = out[:, : W // 2] * (1 - tint) + np.float32((0.25, 0.25, 0.9)) * tint
            out[:, W // 2:] = out[:, W // 2:] * (1 - tint) + np.float32((0.9, 0.5, 0.2)) * tint
            cv2.rectangle(out, (W // 2 - 9, 0), (W // 2 + 9, H), (0.05, 0.05, 0.05), -1)
            cv2.rectangle(out, (W // 2 - 4, 0), (W // 2 + 4, H), (1, 1, 1), -1)
        k = 1.0 if self.style == "meme" else ease_out(t / 0.15)
        if self.lines:
            over_t(out, self.lines_t[int(t * FPS / 3) % len(self.lines_t)])
        if self.card is not None:
            over_t(out, self.card_t, k)
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
        over_t(out, self.ov_t, k)
        self._pop(out, self.txt, t)
        if self.split_heads:
            for (im, ia), cx in zip(self.split_heads, (W // 4, 3 * W // 4)):
                over(out, im, ia, int(cx - im.shape[1] / 2), self.split_y)
        if self.slot:   # 金額がスロットのように回って止まる（10/29）
            pre, val, post = self.slot
            v = val if t > 0.9 else int(np.random.default_rng(int(t * FPS)).integers(10, 99))
            key = f"{pre}{v}{post}"
            if key not in self.slot_cache:
                self.slot_cache[key] = trim(to_np(P.big_text(key, (140, 60, 1780, 420), max_size=230, max_lines=1,
                                                              fill=P.RED_TEXT, stroke=P.WHITE)))
            over_t(out, self.slot_cache[key])
        if self.crack is not None and t > 0.05:   # 画面にヒビ（10/29）
            for pts in self.crack:
                cv2.polylines(out, [pts], False, (0.1, 0.1, 0.12), 9, cv2.LINE_AA)
            for pts in self.crack:
                cv2.polylines(out, [pts], False, (1, 1, 1), 3, cv2.LINE_AA)
        if self.bills:   # お札が降る（10/29）
            for x0, ph0, i in self.bills:
                ph = (ph0 + t * 0.45) % 1.0
                cx, cy = x0 + 60 * np.sin(t * 2 + i), -80 + ph * (H + 160)
                ang = (t * 90 + i * 37) % 360
                box = cv2.boxPoints(((cx, cy), (150, 72), ang)).astype(np.int32)
                cv2.fillPoly(out, [box], (0.62, 0.78, 0.82), cv2.LINE_AA)
                cv2.polylines(out, [box], True, (0.25, 0.4, 0.5), 3, cv2.LINE_AA)
                cv2.circle(out, (int(cx), int(cy)), 16, (0.35, 0.5, 0.6), 3, cv2.LINE_AA)
        if self.qm:
            n = len(self.qm)
            for j, im in enumerate(self.qm):
                u = t - 0.06 * j
                if u < 0:
                    break
                k = (1.7 - 0.7 * min(1.0, u / 0.12)) * (1 + 0.07 * np.sin(t * 18 + j * 1.7))   # 大きく出て縮む・脈打つ
                ang = (-14, 10, -6, 15, -10, 7, -15, 12)[j % 8] + 9 * np.sin(t * 11 + j)   # ゆらゆら
                pim = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BILINEAR).rotate(
                    ang, expand=True, resample=Image.BILINEAR)
                cx = 150 + (W - 300) * (j + 0.5) / n + 8 * np.sin(t * 23 + j * 3)
                cy = self.qm_y + 45 * np.sin(j * 1.3) + 8 * np.cos(t * 19 + j)
                img, al = to_np(pim)
                over(out, img, al, int(cx - pim.width / 2), int(cy - pim.height / 2))
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
        if "punch" in self.fx and t < 0.16:   # 頭でグッと寄って戻る（テンポを出す・10/28）
            z = 1.0 + 0.09 * (1 - t / 0.16) ** 2
            bw, bh = int(W * z), int(H * z)
            big = cv2.resize(out, (bw, bh), interpolation=cv2.INTER_LINEAR)
            ox, oy = (bw - W) // 2, (bh - H) // 2
            out = big[oy:oy + H, ox:ox + W].copy()
        if "flash" in self.fx and t < 0.12:   # 頭で白く光る
            a_ = 0.65 * (1 - t / 0.12)
            out = out * (1 - a_) + a_
        if "spark" in self.fx:   # キラキラが飛ぶ
            for i in range(14):
                ph = (t * 1.4 + i * 0.173) % 1.0
                x_ = int((i * 271 + 90) % W)
                y_ = int(H * (0.95 - 0.9 * ph))
                r_ = int(22 * (1 - abs(ph - 0.5) * 2)) + 4
                col = ((0.4, 0.95, 1.0), (1.0, 1.0, 1.0), (0.6, 0.8, 1.0))[i % 3]
                cv2.line(out, (x_ - r_, y_), (x_ + r_, y_), col, 5, cv2.LINE_AA)
                cv2.line(out, (x_, y_ - r_), (x_, y_ + r_), col, 5, cv2.LINE_AA)
        if "ring" in self.fx and t < 0.4:   # 頭で衝撃波の輪が広がる
            u_ = t / 0.4
            for k_, col in ((0, (0.6, 0.95, 1.0)), (0.12, (1.0, 1.0, 1.0))):
                v_ = u_ - k_
                if 0 < v_ < 1:
                    r_ = int(120 + 1100 * v_)
                    th_ = max(2, int(30 * (1 - v_)))
                    cv2.circle(out, (W // 2, H // 2), r_, (0.05, 0.05, 0.1), th_ + 8, cv2.LINE_AA)
                    cv2.circle(out, (W // 2, H // 2), r_, col, th_, cv2.LINE_AA)
        if "border" in self.fx:   # ふちが色をかえながら光る
            hue = (t * 2.5) % 1.0
            col = np.array([0.5 + 0.5 * np.sin(6.28 * (hue + k_ / 3)) for k_ in range(3)], np.float32)
            b_ = 14
            out[:b_] = col
            out[-b_:] = col
            out[:, :b_] = col
            out[:, -b_:] = col
        if "confetti" in self.fx:   # 紙吹雪
            for i in range(26):
                ph = (t * 0.8 + i * 0.137) % 1.0
                x_ = int((i * 151 + 40 * np.sin(t * 3 + i)) % W)
                y_ = int(-30 + ph * (H + 60))
                col = ((0.3, 0.8, 1.0), (1.0, 0.6, 0.3), (0.5, 1.0, 0.6), (1.0, 1.0, 1.0), (0.9, 0.5, 1.0))[i % 5]
                ww = int(8 + 16 * abs(np.sin(t * 8 + i)))
                cv2.rectangle(out, (x_, y_), (x_ + ww, y_ + 22), col, -1)
        if "dim" in self.fx:   # 半分暗くする（注意書きを読みやすく）
            out *= 0.45
        if self.top is not None:   # 暗くしたあとに重ねる部品（注意書きなど）
            over_t(out, self.top)
        if "mono" in self.fx and t < 0.45:   # 一瞬白黒になって色が戻る（「え…」の場面・10/29）
            a_ = 1.0 if t < 0.28 else 1 - (t - 0.28) / 0.17
            g_ = out.mean(axis=2, keepdims=True)
            out = out * (1 - a_) + g_ * a_
        if self.explain is not None:   # 説明モード：画面はそのまま、下に半透明の黒い帯を敷いて説明文
            k = min(1.0, t / 0.15)
            out[EXPLAIN_TOP:] *= 1 - 0.62 * k
            if t >= 0.1:
                over_t(out, self.explain_t)
        return out

    def close(self):
        for clip, *_ in self.cats:
            clip.close()
        if self.vbg is not None:
            self.vbg.close()


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

# ---- ショートの「!?」と「え…」の場面の音（10/28 ユーザー指定のルール） ----
# ・コナンの音／連打：「!?」となる場面（字幕に !? がある）
# ・ポーンの音／連打：「え…」となる戸惑いの場面（「はてな」の音・戸惑う猫・「……え」「えっ」「は？」などの字幕）
# どちらも、そのショートで1回目はふつうの音、2回目からは連打3種類をランダムに（同じものは続けない）
CONAN = "anime_conan_hirameki_idea_realize_truth"
CONAN_REMIX = ["anime_conan_hirameki_remix_a", "anime_conan_hirameki_remix_b", "anime_conan_hirameki_remix_c"]   # 10/29 完成：切らずに流しきる a・b・c をランダムに（d は試し・使わない）
POON = "tv_professional_poon"
POON_REMIX = ["tv_professional_poon_remix_a", "tv_professional_poon_remix_b"]   # 10/29 ユーザー指定：c はボツ、a・b だけ使う
HUH_SE = "question_mark_pop_confused_huh"
HUH_CATS = {"huh_huh_cat", "confused_i_dont_know_cat"}
BANG = ("!?", "！？", "?!", "？！")
REMIX_MAX = 2   # コナン連打・ポーン連打はそれぞれ1本で多くて2回まで（10/29 ユーザー指定）
DOUBT = ("……え", "……は", "……あれ", "あれ", "え…", "えっ", "え？", "は？", "……本当", "……どこ", "……？")   # 「え…」となる字幕の出だし


def _se_list(c):
    ses = c.get("se")
    return [] if not ses else [ses] if isinstance(ses, (str, dict)) else list(ses)


def _se_name(s):
    return s if isinstance(s, str) else s.get("f")


def scene_kind(c):
    """"bang"（!? の場面）／"doubt"（え… の戸惑いの場面）／None。"""
    if c.get("banner") or c.get("kind") == "split" or c.get("no_huh"):   # no_huh=True：コナン・ポーンを鳴らさない場面（10/29）
        return None
    plain = (c.get("say") or "").replace("*", "").replace("\n", "")
    if any(b in plain for b in BANG):
        return "bang"
    names = [_se_name(s) for s in _se_list(c)]
    if HUH_SE in names or POON in names:
        return "doubt"
    if c.get("kind") == "solo" and (plain.startswith(DOUBT) or plain in ("え", "……")):   # 字幕だけで決めるのは1匹の場面（会話は相手のセリフのことがある）
        return "doubt"
    if not names and any(k.get("a") in HUH_CATS and sounding(k) for k in c.get("cats", [])):
        return "doubt"
    return None


def conan_confusion(cs, seed=0):
    """ショートの「!?」の場面はコナン、「え…」の場面はポーン（どちらも1回目はふつう、2回目から連打）。"""
    import random
    rnd = {"bang": random.Random(seed), "doubt": random.Random(seed + 1)}
    n, last = {"bang": 0, "doubt": 0}, {"bang": None, "doubt": None}
    for c in cs:
        k = scene_kind(c)
        if not k:
            continue
        base, remix = (CONAN, CONAN_REMIX) if k == "bang" else (POON, POON_REMIX)
        if n[k] == 0 or n[k] > REMIX_MAX:   # 連打は1本で多くて2回まで（3回目からはふつうの音・10/29 ユーザー指定）
            f = base
        else:
            f = rnd[k].choice([x for x in remix if x != last[k]])
            last[k] = f
            if k == "bang":
                for q in c.get("cats", []):   # コナンの連打の場面は猫の声を消す（「は？」猫の声が高い音に聞こえる・10/28 ユーザー指摘）
                    q["mute"] = True
                c["no_pop"] = True
        n[k] += 1
        c["se"] = [s for s in _se_list(c) if _se_name(s) not in (HUH_SE, POON, CONAN)] + [{"f": f, "len": 2.4}]
        if k == "bang":
            conan_say(c)
    return cs


def conan_say(c):
    """「!?」の場面の字幕は大きく（10/28 ユーザー指定：「40分たってた!?」）。!? だけの字幕は1つずつポンと出るエフェクト。"""
    say = c.get("say")
    if not say or c.get("kind") != "solo":   # 会話の場面（だれかのセリフ）は変えない
        return
    plain = say.replace("*", "").replace("\n", "")
    if set(plain) <= set("!?！？"):
        n = max(1, plain.count("?") + plain.count("？"))
        c["say"], c["say_size"], c["say_fx"] = "!?" * n, 190, "huh"   # 全角だとすき間が空くので半角
    else:
        if len(plain) <= 8:
            say = say.replace("\n", "")
        c["say"] = say.replace("！？", "!?")
        if "\n" not in say:   # 1行なら大きく（画面からはみ出さない大きさまで）
            wid = sum(1 if ord(ch) > 255 else 0.55 for ch in c["say"].replace("*", ""))
            c["say_size"] = int(min(135, 960 / wid))
    c["big_say"] = True


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
