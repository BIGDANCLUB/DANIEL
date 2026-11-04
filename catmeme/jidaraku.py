"""「自堕落シリーズ」の長尺横動画（1920x1080）。10/24 ユーザー提供の参考動画3本（30代独身が快活CLUBで過ごす1日）の作りをまねる。

参考の作り
- 場所ごとに背景の絵（写真ふう）を画面いっぱい。場所が変わるまで同じ背景
- 猫は1匹だけ（主人公の「俺」）。セリフ1つごとに別の猫ミームに差しかえる。真ん中に大きく、ふち取りなし
- 下に字幕：明朝体の太字・白・黒い縁。1〜2行。ひとりごとの語り（「〜だ。」「〜する。」）、声に出すセリフは「」
- 1つの字幕は2.5〜3秒くらい。ナレーションの声はない（猫ミームの音と小さめのBGM）
- 最後にチャンネル登録の画面は入れない（参考どおり）。長尺のルールで最後に subscribe.png を付ける
使い方は jidaraku_01_yakiniku.py
"""
import math
import os
import subprocess
import urllib.request

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import income_short as I
import render as R

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
SERIF = os.path.join(HERE, "fonts", "NotoSerifJP.ttf")
BGS = [os.path.join(HERE, "backgrounds", d) for d in ("jidaraku", "jidaraku/01_yakiniku", "02_october", "04_leak", "14_japan",
                                                       "01_todai", "16_tenchim", "15_vambi", "17_imamori")]
STANDIN = {}   # 背景が届くまでの仮（名前 → 手もちの背景）
_F = {}


def font(size):
    if size not in _F:
        if not os.path.exists(SERIF):
            os.makedirs(os.path.dirname(SERIF), exist_ok=True)
            urllib.request.urlretrieve("https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifjp/NotoSerifJP%5Bwght%5D.ttf",
                                       SERIF)
        f = ImageFont.truetype(SERIF, size)
        f.set_variation_by_name("Black")
        _F[size] = f
    return _F[size]


def bg_path(n):
    for d in BGS:
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            p = os.path.join(d, n + ext)
            if os.path.exists(p):
                return p
    if n in STANDIN:
        return bg_path(STANDIN[n])
    raise FileNotFoundError(n)


def cover(name):
    im = Image.open(bg_path(name)).convert("RGB")
    k = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * k + 0.5), int(im.height * k + 0.5)), Image.LANCZOS)
    x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    return np.asarray(im.crop((x0, y0, x0 + W, y0 + H)))[:, :, ::-1].astype(np.float32) / 255


def sub_img(t, size=84):
    """字幕：明朝体の太字・白・黒い縁（参考どおり）。"""
    f = font(size)
    t = t.replace("。", "").replace("、", " ")   # 自堕落シリーズの字幕は句読点なし（10/26 ユーザー指定）
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    lines = t.split("\n")
    ws = [d0.textlength(ln, font=f) for ln in lines]
    st = 8
    lh = int(size * 1.22)
    im = Image.new("RGBA", (int(max(ws)) + st * 2 + 10, lh * len(lines) + st * 2 + 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (ln, w) in enumerate(zip(lines, ws)):
        d.text(((im.width - w) / 2, st + 4 + i * lh), ln, font=f, fill=(255, 255, 255), stroke_width=st, stroke_fill=(0, 0, 0))
    return im.crop(im.getbbox())


def line(bg, cat, text, dur=3.0, h=760, x=960, bottom=1010, se=None, bgm=None, mute=False, flip=False, item=None):
    """字幕1つ＝1カット。猫は1匹。item＝料理の写真の名前（右上に白いふちの写真を出し、猫は左によせる・10/31 スシロー）。"""
    if item:
        x, h = 600, min(h, 700)
    c = dict(bg=bg, text=text, dur=dur, fixed=True, no_pop=True, cats=[dict(a=cat, h=h, x=x, bottom=bottom, mute=mute, flip=flip)])
    if item:
        c["item"] = item
    if se:
        c["se"] = se
    if bgm:
        c["bgm"] = bgm
    return c


END_BGM = {"file": os.path.join(HERE, "bgm", "野良猫は宇宙を目指した.mp3"), "from": 9.0, "gain": 2, "fade": 0.3}   # 盛り上がる所から


CONT = tuple("にがをはでとてどもへやずばの") + ("から", "けど", "……", "ひと口", "そこへ")


def tempo(c, nxt):
    """字幕の文字数で長さを決める。文が次の字幕に続くときは短く（中だるみをなくす・11/2 ユーザー指定）。"""
    t = c["text"].replace("\n", "")
    n = len(t)
    if t.endswith(CONT) and nxt is not None and nxt.get("text"):
        return min(max(0.9 + 0.08 * n, 1.4), 2.2)
    return min(max(1.2 + 0.1 * n, 1.8), 3.0)


def auto_tempo(cs):
    for i, c in enumerate(cs):
        if c.pop("auto", False) and c.get("text"):
            c["dur"] = tempo(c, cs[i + 1] if i + 1 < len(cs) else None)
    return cs


ARRIVE_T = 1.2   # 料理が届いた演出の長さ
ARRIVE_SE = "jan"   # 版権の心配がない音（se/README.md で無印）
IMPACT_SE = "explosion_chudoon"
_LINES = {}


def _lines(out, t):
    """集中線（画面のふちから中心へ向かう黒と白の線）。3通りの線を少しずつ入れかえて、ゆらゆら動かす。"""
    if "ov" not in _LINES:
        sets = []
        for seed in (3, 5, 8):
            rng = np.random.default_rng(seed)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(ov)
            cx, cy, R0 = W / 2, H / 2 - 40, 1300
            for j in range(110):
                ang = rng.uniform(0, 2 * math.pi)
                r1 = rng.uniform(330, 520)
                wd = rng.uniform(0.006, 0.02)
                col = (255, 255, 255, 230) if j % 3 else (20, 20, 20, 200)
                d.polygon([(cx + math.cos(ang) * r1, cy + math.sin(ang) * r1),
                           (cx + math.cos(ang - wd) * R0, cy + math.sin(ang - wd) * R0),
                           (cx + math.cos(ang + wd) * R0, cy + math.sin(ang + wd) * R0)], fill=col)
            sets.append(R.to_np(ov))
        _LINES["ov"] = sets
    img, a = _LINES["ov"][int(t * 12) % 3]
    I.over(out, img, a, 0, 0)
    return out


def _cat_len(a):
    """素材の使える長さ（play.json の until があればそれ＝1回分：チピチピ猫など）。"""
    cfg = R.ASSET_PLAY.get(a, {})
    au = R.cat_audio(a)
    n = len(au) / R.SR if au is not None else R.Clip(a).n / R.Clip(a).fps
    return min(n, cfg["until"]) if cfg.get("until") else n


def chain(cs):
    """1つの文を何行かに分けて出す所は、文が終わるまで同じ素材を流し続ける（11/2 ユーザー指定）。
    素材の長さ（くり返す素材は1回分）が足りなくなったら、そこからは次の行の素材にもどす。"""
    i = 0
    while i < len(cs):
        c = cs[i]
        grp = [c]
        while (grp[-1].get("text") and grp[-1]["text"].replace("\n", "").endswith(CONT) and i + len(grp) < len(cs)
               and cs[i + len(grp)].get("text") and cs[i + len(grp)].get("bg") == c.get("bg") and c.get("cats")):
            nxt = cs[i + len(grp)]
            used = sum(x["dur"] for x in grp) + nxt["dur"] + 0.25
            if used > _cat_len(c["cats"][0]["a"]):
                break
            grp.append(nxt)
        if len(grp) > 1:
            head = c["cats"][0]
            item = any(x.get("item") for x in grp)
            off = 0.0
            for x in grp:
                q = dict(head, ss=off)
                if item:
                    q.update(x=600, h=min(head["h"], 700))
                x["cats"] = [q]
                off += x["dur"]
        i += len(grp)
    return cs


HOLD = 0   # 11/4 ユーザー指定：1つの素材を2〜3文つづけて使う（0＝使わない）。台本で J.HOLD = 3 にする


def hold(cs, n=None):
    """同じ素材を2〜3文（n文まで）つづけて流す。素材の長さ（くり返す素材は1回分）が足りなくなったら、そこで次の素材に替える。
    文が次の字幕に続くときは n をこえても同じ素材のまま（素材の長さまで）。場所（背景）が変わったら替える。"""
    n = n or HOLD
    i = 0
    while i < len(cs):
        c = cs[i]
        if not c.get("cats") or not c.get("text") or c.get("solo"):   # solo：まとめない場面（テンポよく切り替える所）
            i += 1
            continue
        head = c["cats"][0]
        limit = _cat_len(head["a"])
        grp = [c]
        used = c["dur"] + 0.25
        while i + len(grp) < len(cs):
            nxt = cs[i + len(grp)]
            if not nxt.get("text") or not nxt.get("cats") or nxt.get("bg") != c.get("bg") or nxt.get("solo"):
                break
            cont = grp[-1]["text"].replace("\n", "").endswith(CONT)
            if len(grp) >= n and not cont:
                break
            if used + nxt["dur"] > limit:
                break
            grp.append(nxt)
            used += nxt["dur"]
        off = 0.0
        for x in grp:
            q = dict(head, ss=off)
            if x.get("item"):
                q.update(x=600, h=min(head["h"], 700))
            else:
                q.update(x=960, h=c["cats"][0]["h"] if not c.get("item") else 760)
            x["cats"] = [q]
            off += x["dur"]
        i += len(grp)
    return cs


def effects(cs):
    """演出と SE（11/2 ユーザー指定）：料理が初めて出る所は「届いた」演出＋ジャン！／「!」「!?」の所は集中線＋ゆれ＋チュドーン。
    最後に、版権の心配がある SE（se/README.md の ⚠・✕、game_ などで始まる音）が入っていないか確かめる。"""
    seen = set()
    for c in cs:
        se = c.get("se")
        lst = [] if not se else ([se] if isinstance(se, (str, dict)) else list(se))
        it = c.get("item")
        try:
            has = bool(it) and bool(bg_path(it))
        except FileNotFoundError:   # 写真がまだない料理は演出しない
            has = False
        if has and it not in seen:
            seen.add(it)
            c["arrive"] = True
            lst.append({"f": ARRIVE_SE, "gain": -2})
        t = (c.get("text") or "").replace("\n", "")
        names = [x if isinstance(x, str) else x.get("f", "") for x in lst]
        big = any(n.startswith(("explosion", "gong")) for n in names)
        if ("!" in t or "！" in t or big) and not c.get("arrive"):
            c["impact"] = True
            if not lst:
                lst.append({"f": IMPACT_SE, "gain": -4})
        if lst:
            c["se"] = lst
    on, t0 = False, 0.0
    for i, c in enumerate(cs):   # 驚き・届いた所から、その文が終わるまで集中線を出す
        if c.get("impact") or c.get("arrive"):
            on, t0 = True, 0.0
        if on:
            c["lines_on"], c["lines_t0"] = True, t0
            t0 += c["dur"]
            if not (c.get("text") or "").replace("\n", "").endswith(CONT):
                on = False
    prev = None
    for c in cs:   # 場所が変わる所はシュッ（ほかの音がないときだけ）
        if prev is not None and c.get("bg") != prev and not c.get("se") and c.get("text"):
            c["se"] = [{"f": "whoosh_shu", "gain": -8}]
        prev = c.get("bg")
    bad = R.risky_se()
    found = sorted({(s if isinstance(s, str) else s.get("f")) for c in cs for s in
                    ([c["se"]] if isinstance(c.get("se"), (str, dict)) else (c.get("se") or []))} & bad)
    if found:
        raise SystemExit("自堕落シリーズでは使わない SE（版権の心配）：" + "、".join(found))
    return cs


def end_card(dur=4.0, bgm=END_BGM):
    """長尺の決まり：最後は subscribe.png。チャンネル登録の画面では決まった曲を流す（11/2 ユーザー指定）。"""
    c = dict(bg=None, end=True, text=None, dur=dur, fixed=True, no_pop=True, cats=[])
    if bgm:
        c["bgm"] = bgm
    return c


class Renderer:
    def __init__(self, c):
        self.c = c
        if c.get("end"):
            im = Image.open(os.path.join(HERE, "parts", "common", "subscribe.png")).convert("RGB").resize((W, H), Image.LANCZOS)
            self.base = np.asarray(im)[:, :, ::-1].astype(np.float32) / 255
        else:
            self.base = cover(c["bg"])
            if c.get("dark"):   # 同じ絵を夜っぽく暗くして使いまわす
                self.base = self.base * (1 - c["dark"]) + np.array([0.25, 0.08, 0.05], np.float32) * c["dark"] * 0.4
        self.sub = sub_img(c["text"]) if c.get("text") else None
        self.item = None
        if c.get("item"):
            try:
                src = Image.open(bg_path(c["item"])).convert("RGBA")   # 背景が透明な写真は白で埋める
                im = Image.new("RGB", src.size, (255, 255, 255))
                im.paste(src, (0, 0), src)
            except FileNotFoundError:   # 写真がまだ届いていない料理は出さない
                im = None
            if im is not None:
                k = min(760 / im.width, 560 / im.height)
                im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
                fr = Image.new("RGBA", (im.width + 28, im.height + 28), (255, 255, 255, 255))
                fr.paste(im, (14, 14))
                sh = Image.new("RGBA", (fr.width + 16, fr.height + 16), (0, 0, 0, 0))
                ImageDraw.Draw(sh).rectangle((10, 10, sh.width - 1, sh.height - 1), fill=(0, 0, 0, 110))
                sh.alpha_composite(fr, (0, 0))
                self.item = sh.rotate(-3, expand=True, resample=Image.BICUBIC)
        self.clips = [R.Clip(k["a"]) for k in c["cats"]]

    def frame(self, t):
        out = self.base.copy()
        for cl, k in zip(self.clips, self.c["cats"]):
            fr, a = cl.frame(t + 0.25 + k.get("ss", 0.0))
            y0, y1, x0, x1 = I.clip_bbox(k["a"])
            fr, a = fr[y0:y1, x0:x1], a[y0:y1, x0:x1]
            if k.get("flip"):
                fr, a = fr[:, ::-1], a[:, ::-1]
            s = min(k["h"] / fr.shape[0], 1100 / fr.shape[1])
            w, h = max(1, int(fr.shape[1] * s)), max(1, int(fr.shape[0] * s))
            img = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
            al = cv2.resize(a.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA)
            xx = min(max(int(k["x"] - w / 2), 0), W - w)
            I.over(out, img, al, xx, int(k["bottom"] - h))
        arr = self.c.get("arrive") and self.item is not None and t < ARRIVE_T
        if self.c.get("lines_on") and not self.c.get("arrive"):   # 集中線：文が終わるまで出しっぱなしで少しゆらす（11/2 ユーザー指定）
            out = _lines(out, t + self.c.get("lines_t0", 0.0))
        if arr:   # 注文した料理が届いた：画面のまん中に大きく＋集中線（11/2 ユーザー指定）
            out = out * 0.6
            out = _lines(out, t)
            u = min(1.0, t / 0.16)
            k = (0.6 + 0.5 * (1 - (1 - u) ** 3)) * (1 if t < ARRIVE_T - 0.25 else 1 - 0.45 * (t - ARRIVE_T + 0.25) / 0.25)
            big = self.item.resize((int(self.item.width * 1.25 * k), int(self.item.height * 1.25 * k)), Image.BILINEAR)
            img, a = R.to_np(big)
            I.over(out, img, a, int(W / 2 - big.width / 2), int(H / 2 - 40 - big.height / 2))
        if self.c.get("impact") and t < 0.3:
            dx, dy = int(16 * math.sin(t * 90) * (1 - t / 0.3)), int(10 * math.cos(t * 70) * (1 - t / 0.3))
            out = np.roll(np.roll(out, dx, axis=1), dy, axis=0)
        if (self.c.get("impact") or arr) and t < 0.1:
            out = out + (1 - out) * (0.55 * (1 - t / 0.1))
        if self.c.get("arrive") and t >= ARRIVE_T:   # 届いたあとも文が終わるまで集中線
            out = _lines(out, t)
        if self.item is not None and not arr:   # 料理の写真：ポンと出て少し縮む
            k = 1.18 - 0.18 * min(1.0, t / 0.18)
            it = self.item.resize((int(self.item.width * k), int(self.item.height * k)), Image.BILINEAR)
            img, a = R.to_np(it)
            I.over(out, img, a, int(1390 - it.width / 2), int(max(10, 400 - it.height / 2)))
        if self.sub is not None:
            img, a = R.to_np(self.sub)
            I.over(out, img, a, int(W / 2 - self.sub.width / 2), int(1040 - self.sub.height))
        return out

    def close(self):
        for cl in self.clips:
            if getattr(cl, "cap", None) is not None:
                cl.cap.release()


def run(cs, out_path, prev=None, only=None):
    cs = effects(hold(cs) if HOLD else chain(cs))
    durs = [c["dur"] for c in cs]
    total = float(sum(durs))
    starts = list(np.cumsum([0] + durs[:-1]))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wav = out_path + ".audio.f32"
    R.build_audio(cs, starts, durs, total).tofile(wav)
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(R.FPS), "-i", "-",
         "-f", "f32le", "-ar", str(R.SR), "-ac", "2", "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", out_path],
        stdin=subprocess.PIPE)
    if prev:
        os.makedirs(prev, exist_ok=True)
    nframes = int(round(total * R.FPS))
    fno = 0
    for i, c in enumerate(cs):
        rd = Renderer(c)
        end = min(nframes, int(round((starts[i] + durs[i]) * R.FPS)))
        shot = False
        while fno < end:
            tt = fno / R.FPS - starts[i]
            u8 = (np.clip(rd.frame(tt), 0, 1) * 255).astype(np.uint8)
            proc.stdin.write(u8.tobytes())
            if prev and not shot and tt > 1.0:
                cv2.imwrite(os.path.join(prev, f"{i:03d}.jpg"), cv2.resize(u8, (640, 360)), [cv2.IMWRITE_JPEG_QUALITY, 80])
                shot = True
            fno += 1
        rd.close()
        print(f"\r{i + 1}/{len(cs)}  {fno / R.FPS:6.1f}s / {total:.1f}s", end="", flush=True)
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    print(f"\n-> {out_path} ({total:.1f}s)")
