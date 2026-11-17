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
C.REWIND_PREFIX = "none"


def fmt_n(v):
    v = int(v)
    if v < 10000:
        return f"{v:,}"
    if v < 100000000:
        return f"{v // 10000:,}万"
    oku, man = divmod(v, 100000000)
    return f"{oku}億{man // 10000:,}万" if oku < 10 else f"{round(v / 100000000)}億"


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

    def chime():      # 駅の「ピンポーン」
        n1 = int(0.45 * C.SR)
        return np.concatenate([C.tone(0.45, 1046) * C.env(n1, 0.005, 0.25), C.tone(0.6, 784) * C.env(int(0.6 * C.SR), 0.005, 0.3)]) * 0.5

    def clank():      # 床板が屋根に付く「ガシャン」
        n = int(0.35 * C.SR)
        x = C.lp(C.noise(0.35, 7), 2500) * C.env(n, 0.002, 0.12) + 0.6 * C.tone(0.35, 180) * C.env(n, 0.002, 0.15)
        return x * 0.8

    def gatan(seed):  # 走る音「ガタンゴトン」
        n = int(0.12 * C.SR)
        return C.lp(C.noise(0.12, seed), 600) * C.env(n, 0.002, 0.05)

    for k in range(5):
        put(C.sfx_tick(), k + 0.05, 0.6)
    # 駅に着くたび（数字が1つ増えるたび）に小さなチャイム、節目で大きなチャイム
    t = st["f02_car"]
    for s in TL.SHOTS[1:]:
        last = None
        for i in range(s["frames"]):
            x, _ = TL.t_of(s, i)
            if last is not None and int(x) != int(last):
                put(C.sfx_tick(), st[s["name"]] + i / TL.FPS, 0.35)
            last = x
        for a0, b0, lines in s.get("captions", []):
            put(chime(), st[s["name"]] + a0, 0.55)
    # 走る音（床板の場面から最後まで）
    t0 = st["f04_deck"]
    k = 0
    while t0 + k * 0.9 < total - 0.5:
        put(gatan(k), t0 + k * 0.9, 0.35)
        put(gatan(k + 100), t0 + k * 0.9 + 0.16, 0.3)
        k += 1
    put(C.sfx_whoosh(total - t0, True, 3) , t0, 0.25)
    # 床板が1枚ずつ付く（film.py の f0 + 14 コマ目）
    for c in range(11):
        put(clank(), t0 + (8 + c * 6 + 14) / TL.FPS, 0.5)
    put(C.sfx_whoosh(1.2, True, 8), st["f05_wide"], 0.5)
    a = a / max(1e-6, abs(a).max()) * 0.8
    return a


C.draw_shot = draw_shot
C.build_audio = build_audio

if __name__ == "__main__":
    C.main()
