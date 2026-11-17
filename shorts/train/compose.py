"""電車版の合成。新幹線版（../mach/compose_all.py）の仕組みを使い、文字と効果音だけ差し替える。
usage: python3 compose.py frames_root out.mp4 [bgm.mp3]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, "..", "mach"))
import timeline as TL  # noqa: E402
import compose_all as C  # noqa: E402
import overlay as O  # noqa: E402
from grade import grade  # noqa: E402
from PIL import Image  # noqa: E402

WHITE, OR = (255, 255, 255), O.ORANGE
C.REWIND_PREFIX = "e03"


def _rewind_timer(g, u):
    O.timer(g, "発車してから", (f"{int(round(33 * (1 - u)))}", "駅目"))


C.rewind_timer = _rewind_timer


def fmt_n(v):
    v = int(v)
    if v < 10000:
        return f"{v:,}"
    if v < 100000000:
        return f"{v // 10000:,}万"
    oku, man = divmod(v, 100000000)
    return f"{oku}億{man // 10000:,}万" if oku < 10 else f"{oku}億"


def draw_shot(s, i, base, sun):
    if sun and s["name"] in TL.AERIAL:
        g = grade(base, sun=tuple(sun), glow=0.25, haze=0.2)      # 上から見下ろす場面は太陽のにじみを弱く
    elif sun:
        g = grade(base, sun=tuple(sun))
    else:
        g = grade(base, sun=(base.width / 2, -base.height * 0.4), glow=0.4, haze=0.12)
    g = g.resize((O.W, O.H), Image.LANCZOS).convert("RGBA")
    sec = i / TL.FPS
    O.watermark(g)
    if s.get("kind") == "open":
        count = 5 - int(sec)
        O.opening(g, [("もしも", WHITE), ("電車の乗客", OR), ("が", WHITE)], [("1駅ごとに2倍", OR), ("になったら？", WHITE)],
                  count if count >= 1 else None, ["最初の乗客は、たった1人。", "山手線は1周30駅"], "JR山手線の路線図より")
        return g
    x, tag = TL.t_of(s, i)
    O.timer(g, "発車してから", (f"{int(x)}", "駅目"), tag[0],
            O.TAG_GREEN if tag[1] == "green" else O.TAG_ORANGE, max_w=440 if s.get("info") else 850)
    O.speed(g, "乗客", "", fmt_n(TL.n(x)), "人")
    if s.get("note") and s["note"][0] <= sec < s["note"][1]:
        O.note(g, s["note"][2])
    for a, b, lines in s.get("captions", []):
        if a <= sec < b:
            O.caption(g, lines)
    if s.get("info"):
        title, rows = s["info"]
        O.info_box(g, title, [(ic, tx, col) for (at, ic, tx, col) in rows if sec >= at])
    return g


def build_audio(total, st):
    import numpy as np
    a = np.zeros(int(total * C.SR) + C.SR)

    def put(x, at, gain=1.0):
        i = int(at * C.SR)
        j = min(len(a), i + len(x))
        a[i:j] += gain * x[: j - i]

    def chime():      # 発車の「ピンポーン」
        n1 = int(0.45 * C.SR)
        return np.concatenate([C.tone(0.45, 1046) * C.env(n1, 0.005, 0.25), C.tone(0.6, 784) * C.env(int(0.6 * C.SR), 0.005, 0.3)]) * 0.5

    for k in range(5):
        put(C.sfx_tick(), k + 0.05, 0.6)
    put(chime(), st["e02_one"], 0.8)
    for name in ("e03a_car", "e03b_platform", "e03c_city", "e03d_wide"):
        nsec = TL.shot(name)["frames"] / TL.FPS
        put(C.sfx_whoosh(nsec, True, hash(name) % 50), st[name], 0.5)          # ざわめき
        for k in range(int(nsec * 3)):
            put(chime() * 0.4, st[name] + k / 3, 0.4)
    put(C.sfx_whoosh(0.7, False, 5), st["e05_rewind"], 0.8)
    for k, name in enumerate(["e06_five", "e07_ten", "e08_full", "e09_dome", "e10_tokyo", "e11_japan", "e12_loop", "e13_world"]):
        put(chime(), st[name] + 0.2, 0.6)
        put(C.sfx_whoosh(3.5, True, 10 + k), st[name] + 0.4, 0.4)
    a = a / max(1e-6, abs(a).max()) * 0.8
    return a


C.draw_shot = draw_shot
C.build_audio = build_audio

if __name__ == "__main__":
    C.main()
