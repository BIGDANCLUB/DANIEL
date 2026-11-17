"""雪の版の合成。新幹線版（../mach/compose_all.py）の仕組みを使い、文字と効果音だけ差し替える。
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
C.REWIND_PREFIX = "n03"


def fmt_h(m):
    if m < 1:
        return f"{m * 100:.0f}", "cm"
    if m < 10:
        return f"{m:.1f}", "m"
    if m < 1000:
        return f"{m:.0f}", "m"
    km = m / 1000
    if km < 10:
        return f"{km:.1f}", "km"
    return f"{km:,.0f}", "km"


def draw_shot(s, i, base, sun):
    if s["name"] in TL.SPACE:
        g = grade(base, sun=(base.width * 1.2, -base.height), glow=0.0, warmth=0.2, haze=0.0)
    elif sun:
        g = grade(base, sun=tuple(sun))
    else:
        g = grade(base, sun=(base.width / 2, -base.height * 0.4), glow=0.4, haze=0.15)
    g = g.resize((O.W, O.H), Image.LANCZOS).convert("RGBA")
    sec = i / TL.FPS
    O.watermark(g)
    if s.get("kind") == "open":
        count = 5 - int(sec)
        O.opening(g, [("もしも", WHITE), ("日本中の雪", OR), ("が", WHITE)], [("毎日2倍", OR), ("に積もったら？", WHITE)],
                  count if count >= 1 else None, ["日本の積雪の最高記録は、", "伊吹山の11.82m"], "1927年2月14日の観測より")
        return g
    t, tag = TL.t_of(s, i)
    hours = int(round((t % 1) * 24)) % 24
    O.timer(g, "降り始めから", (f"{int(t)}日", f"{hours}時間"), tag[0],
            O.TAG_GREEN if tag[1] == "green" else O.TAG_ORANGE, max_w=440 if s.get("info") else 850)
    num, unit = fmt_h(TL.h(t))
    O.speed(g, "積雪", "", num, unit)
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

    for k in range(5):
        put(C.sfx_tick(), k + 0.05, 0.6)
    for name in ("n03a_village", "n03b_town", "n03c_tokyo", "n03d_fuji", "n03e_space"):
        n = TL.shot(name)["frames"] / TL.FPS
        put(C.sfx_whoosh(n, True, hash(name) % 50), st[name], 0.6)      # 吹雪の風
    put(C.sfx_whoosh(0.7, False, 5), st["n05_rewind"], 0.8)
    for k, name in enumerate(["n06_winter", "n07_house", "n08_record", "n09_town", "n10_tokyo", "n11_fuji"]):
        put(C.sfx_whoosh(4.0, k % 2 == 0, 10 + k), st[name], 0.45)
        put(C.sfx_boom(2.0, 20 + k), st[name] + 2.0, 0.35)
    put(C.sfx_boom(3.0, 30), st["n14_moon"] + 1.5, 0.6)
    a = a / max(1e-6, abs(a).max()) * 0.8
    return a


C.draw_shot = draw_shot
C.build_audio = build_audio

if __name__ == "__main__":
    C.main()
