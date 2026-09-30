"""桃太郎 長尺版の解説図（1920x1080 PNG）を HTML/SVG から作る。

  python3 make_zu.py            … 全部の図を zu_momotaro/ に書き出す
  python3 make_zu.py danmen fall … 指定した図だけ

- 描画は Chromium のヘッドレス版（PLAYWRIGHT_BROWSERS_PATH 配下、または環境変数 CHROME）
- フォントは Zen Maru Gothic（無ければ ../fonts/ に取得）
- 画面の下 230px は字幕用に空けてある
"""
import glob
import math
import os
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "zu_momotaro")
FONT_DIR = os.path.join(HERE, "..", "fonts")
FONTS = {
    "ZenMaruGothic-Bold.ttf": "ofl/zenmarugothic/ZenMaruGothic-Bold.ttf",
    "ZenMaruGothic-Black.ttf": "ofl/zenmarugothic/ZenMaruGothic-Black.ttf",
}

# 和紙・墨・朱・藍・桃の配色（イラストの水彩タッチに合わせる）
INK, PAPER, SHU, AI, MOMO, KI, KOKE, CHA = "#2b2622", "#f4ecdc", "#c8442f", "#2f5d7c", "#f2a7a0", "#d9a441", "#6b8f5e", "#8a5a3c"

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Maru;font-weight:700;src:url("file://FONTDIR/ZenMaruGothic-Bold.ttf")}
@font-face{font-family:Maru;font-weight:900;src:url("file://FONTDIR/ZenMaruGothic-Black.ttf")}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden}
body{font-family:Maru,sans-serif;font-weight:700;color:INK;
 background:
  radial-gradient(circle at 18% 22%,rgba(160,120,70,.10),transparent 38%),
  radial-gradient(circle at 82% 68%,rgba(160,120,70,.10),transparent 42%),
  radial-gradient(circle at 55% 110%,rgba(120,90,50,.16),transparent 55%),
  PAPER;}
.frame{position:absolute;left:0;top:0;width:1920px;height:850px;padding:54px 90px 0}
.tag{display:inline-block;background:SHU;color:#fff;font-weight:900;font-size:34px;padding:4px 22px 6px;border-radius:8px;letter-spacing:.1em}
h1{display:inline-block;margin-left:22px;font-weight:900;font-size:62px;vertical-align:middle;letter-spacing:.02em}
.body{position:absolute;left:90px;top:170px;width:1740px;height:660px}
svg text{font-family:Maru,sans-serif;font-weight:700;fill:INK}
.b{font-weight:900}
.note{position:absolute;right:90px;top:66px;font-size:28px;opacity:.65}
.edge{position:absolute;left:40px;right:40px;top:130px;height:4px;background:INK;opacity:.85;border-radius:2px}
</style></head><body><div class="frame"><span class="tag">図解</span><h1>TITLE</h1><div class="note">NOTE</div></div>
<div class="edge"></div><div class="body">BODY</div></body></html>"""


def svg(inner, w=1740, h=660):
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'


def t(x, y, s, size=40, anchor="middle", fill=INK, weight=700, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
            f'style="fill:{fill};font-weight:{weight}" {extra}>{s}</text>')


def arrow(x1, y1, x2, y2, color=INK, w=6, head=22):
    a = math.atan2(y2 - y1, x2 - x1)
    hx1, hy1 = x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45)
    hx2, hy2 = x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45)
    bx, by = x2 - head * 0.8 * math.cos(a), y2 - head * 0.8 * math.sin(a)
    return (f'<line x1="{x1}" y1="{y1}" x2="{bx}" y2="{by}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{x2},{y2} {hx1},{hy1} {hx2},{hy2}" fill="{color}"/>')


def box(x, y, w, h, fill="#fff", stroke=INK, r=18, sw=4, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def iso_cube(ox, oy, n, s, top=MOMO, left="#e98f86", right="#d9776e"):
    """n×n×n の小立方体でできた立方体（見える3面に格子）。ox,oy は手前下の角。"""
    c, sn = math.cos(math.radians(30)) * s, math.sin(math.radians(30)) * s

    def P(x, y, z):
        return (ox + (x - y) * c, oy + (x + y) * sn - z * s - 2 * n * sn)

    def poly(pts, fill):
        return '<polygon points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + f'" fill="{fill}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'

    def line(p, q):
        return f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{INK}" stroke-width="2" opacity=".55"/>'

    out = [poly([P(0, 0, n), P(n, 0, n), P(n, n, n), P(0, n, n)], top),
           poly([P(0, n, 0), P(n, n, 0), P(n, n, n), P(0, n, n)], left),
           poly([P(n, 0, 0), P(n, n, 0), P(n, n, n), P(n, 0, n)], right)]
    for k in range(1, n):
        out += [line(P(k, 0, n), P(k, n, n)), line(P(0, k, n), P(n, k, n)),
                line(P(k, n, 0), P(k, n, n)), line(P(0, n, k), P(n, n, k)),
                line(P(n, k, 0), P(n, k, n)), line(P(n, 0, k), P(n, n, k))]
    return "".join(out)


def baby(cx, cy, s=1.0, fill="#f7d9b8", dash=False):
    st = f'stroke="{INK}" stroke-width="{4 * s:.1f}"' + (' stroke-dasharray="10 8" fill-opacity=".35"' if dash else "")
    return (f'<ellipse cx="{cx + 12 * s}" cy="{cy + 22 * s}" rx="{58 * s}" ry="{44 * s}" fill="{fill}" {st}/>'
            f'<circle cx="{cx - 40 * s}" cy="{cy - 22 * s}" r="{34 * s}" fill="{fill}" {st}/>')


def person(x, base, h, fill=INK, bun=True):
    """素朴な人影。x は中心、base は足元、h は身長(px)。"""
    hr = h * 0.085
    return (f'<circle cx="{x}" cy="{base - h + hr}" r="{hr}" fill="{fill}"/>'
            + (f'<circle cx="{x + hr * 0.2}" cy="{base - h - hr * 0.35}" r="{hr * 0.55}" fill="{fill}"/>' if bun else "")
            + f'<path d="M{x - h * 0.08},{base - h + 2.3 * hr} L{x + h * 0.08},{base - h + 2.3 * hr} '
              f'L{x + h * 0.15},{base} L{x - h * 0.15},{base} Z" fill="{fill}"/>')


def oni_shape(x, base, h, fill=SHU):
    hr = h * 0.09
    return (person(x, base, h, fill, bun=False)
            + f'<polygon points="{x - hr * 0.6},{base - h + hr * 0.3} {x - hr * 0.35},{base - h - hr * 0.9} {x - hr * 0.05},{base - h + hr * 0.1}" fill="{KI}" stroke="{INK}" stroke-width="3"/>'
            + f'<polygon points="{x + hr * 0.05},{base - h + hr * 0.1} {x + hr * 0.35},{base - h - hr * 0.9} {x + hr * 0.6},{base - h + hr * 0.3}" fill="{KI}" stroke="{INK}" stroke-width="3"/>')


def bars(items, x0, y0, w, h, maxv, unit="", fmt="{:g}", bar_h=70, gap=34, label_w=330):
    """横棒グラフ。items = [(ラベル, 値, 色, 値の表示 or None)]"""
    out = []
    for i, (lab, v, col, shown) in enumerate(items):
        y = y0 + i * (bar_h + gap)
        bw = max(6, (w - label_w - 200) * v / maxv)
        out.append(t(x0 + label_w - 24, y + bar_h * 0.68, lab, 42, "end"))
        out.append(box(x0 + label_w, y, bw, bar_h, col, INK, 10, 4))
        out.append(t(x0 + label_w + bw + 20, y + bar_h * 0.68, shown if shown else fmt.format(v) + unit, 46, "start", weight=900))
    return "".join(out)


# ---------------------------------------------------------------- 各図
Z = {}

Z["nijo"] = ("二乗三乗の法則", "大きさを変えると…", svg(
    iso_cube(250, 560, 1, 110) + t(250, 620, "大きさ 1", 40)
    + iso_cube(620, 560, 2, 110) + t(620, 620, "大きさ 2倍", 40)
    + t(435, 330, "→", 90, weight=900)
    + box(930, 60, 800, 520, "#fffaf0")
    + t(1110, 150, "長さ", 44, weight=900) + t(1330, 150, "面積", 44, weight=900) + t(1580, 150, "体積・重さ", 44, weight=900)
    + f'<line x1="960" y1="180" x2="1700" y2="180" stroke="{INK}" stroke-width="3"/>'
    + "".join(t(1110, 260 + 120 * i, a, 56, weight=900) + t(1330, 260 + 120 * i, b, 56, weight=900, fill=AI)
              + t(1580, 260 + 120 * i, c, 64 if i else 56, weight=900, fill=SHU)
              for i, (a, b, c) in enumerate([("1倍", "1倍", "1倍"), ("2倍", "4倍", "8倍"), ("10倍", "100倍", "1000倍")]))
))

pk = 3.6  # 1cm = 3.6px（全部同じ縮尺）
Z["momo_size"] = ("普通の桃と、桃太郎の桃", "同じ縮尺で比べると", svg(
    f'<line x1="40" y1="600" x2="1700" y2="600" stroke="{INK}" stroke-width="4"/>'
    + f'<circle cx="230" cy="{600 - 4 * pk}" r="{4 * pk}" fill="{MOMO}" stroke="{INK}" stroke-width="4"/>'
    + t(230, 470, "普通の桃", 44, weight=900) + t(230, 520, "直径8cm・約250g", 36)
    + f'<circle cx="760" cy="{600 - 40 * pk}" r="{40 * pk}" fill="{MOMO}" stroke="{INK}" stroke-width="5"/>'
    + f'<path d="M760,{600 - 80 * pk} q-40,-60 -110,-50" stroke="{KOKE}" stroke-width="10" fill="none"/>'
    + baby(760, 450, 1.25, dash=True)
    + t(760, 150, "桃太郎の桃", 48, weight=900) + t(760, 200, "直径80cm", 40)
    + t(990, 330, "大きさ10倍 → 重さ1000倍", 40, "start", weight=900)
    + t(990, 450, "約250kg", 110, "start", fill=SHU, weight=900)
    + person(1600, 600, 145 * pk, "#5a4a3f") + t(1600, 645, "おばあさん（145cm）", 32, weight=900)
))

Z["danmen"] = ("桃の断面図", "桃は「核果」", svg(
    f'<ellipse cx="560" cy="340" rx="330" ry="310" fill="{MOMO}" stroke="{INK}" stroke-width="6"/>'
    + f'<ellipse cx="560" cy="340" rx="310" ry="290" fill="#fbe3c4"/>'
    + f'<ellipse cx="560" cy="340" rx="190" ry="180" fill="#f4b9a0" opacity=".55"/>'
    + f'<path d="M560,160 C680,170 700,260 690,340 C680,450 610,520 560,525 C505,520 440,450 432,340 C425,250 460,168 560,160 Z" fill="{CHA}" stroke="{INK}" stroke-width="5"/>'
    + "".join(f'<path d="M{a} q30,20 0,40" stroke="#5c3a24" stroke-width="5" fill="none"/>' for a in ["500,230", "620,230", "480,330", "640,320", "510,420", "610,430"])
    + f'<ellipse cx="560" cy="345" rx="68" ry="118" fill="#f8ecd2" stroke="{INK}" stroke-width="4"/>'
    + f'<line x1="560" y1="240" x2="560" y2="450" stroke="#d6c29a" stroke-width="3"/>'
    + arrow(1010, 60, 880, 150) + t(1030, 72, "果皮（外果皮）", 44, "start", weight=900)
    + arrow(1010, 200, 840, 250) + t(1030, 212, "果肉（中果皮）", 44, "start", weight=900)
    + arrow(1010, 340, 700, 340) + t(1030, 352, "核（内果皮）…かたい殻", 44, "start", weight=900)
    + arrow(1010, 480, 630, 380, SHU) + t(1030, 492, "種 ← 次の世代はここだけ", 48, "start", fill=SHU, weight=900)
    + t(1030, 580, "果皮・果肉・核は、どれも", 34, "start") + t(1030, 628, "めしべの「子房の壁」が育ったもの", 34, "start")
))

Z["furyoku"] = ("浮いている＝つり合っている", "アルキメデスの原理", svg(
    f'<rect x="0" y="330" width="1000" height="330" fill="#9cc3d8" opacity=".75"/>'
    + f'<path d="M0,330 q60,-18 120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0" stroke="{AI}" stroke-width="5" fill="none"/>'
    + f'<circle cx="500" cy="300" r="200" fill="{MOMO}" stroke="{INK}" stroke-width="6"/>'
    + f'<ellipse cx="500" cy="300" rx="120" ry="100" fill="#fbe3c4" stroke="{INK}" stroke-width="4" stroke-dasharray="12 9"/>'
    + t(500, 312, "空洞", 40, weight=900)
    + arrow(500, 40, 500, 170, SHU, 12, 40) + t(560, 70, "重さ 約250kg", 46, "start", fill=SHU, weight=900)
    + arrow(500, 640, 500, 520, AI, 12, 40) + t(560, 620, "浮力（押しのけた水の重さ）", 42, "start", fill="#12344c", weight=900)
    + box(1080, 40, 640, 560, "#fffaf0")
    + t(1400, 120, "平均の密度で決まる", 46, weight=900)
    + t(1400, 230, "水より小さい → 浮く", 48, fill=AI, weight=900)
    + t(1400, 320, "水より大きい → 沈む", 48, fill=SHU, weight=900)
    + f'<line x1="1120" y1="370" x2="1680" y2="370" stroke="{INK}" stroke-width="3" stroke-dasharray="8 8"/>'
    + t(1400, 450, "浮いている間は", 44) + t(1400, 530, "重さ＝浮力", 70, weight=900)
))

Z["kokyu"] = ("桃の中は、酸素の取り合い", "果物は収穫後も生きている", svg(
    f'<circle cx="760" cy="320" r="265" fill="{MOMO}" stroke="{INK}" stroke-width="6"/>'
    + f'<circle cx="760" cy="320" r="230" fill="#fbe3c4"/>'
    + baby(760, 330, 1.6)
    + t(760, 648, "桃（果肉の細胞）も呼吸している", 36, weight=900)
    + box(40, 180, 330, 150, "#e3f0f6", AI) + t(205, 250, "酸素 O₂", 54, fill=AI, weight=900) + t(205, 305, "入ってくる量は少ない", 28)
    + arrow(380, 255, 500, 290, AI, 10, 34)
    + box(1150, 60, 540, 150, "#f1ece6") + t(1420, 130, "二酸化炭素 CO₂", 50, weight=900) + t(1420, 185, "桃太郎も桃も出す", 28)
    + arrow(1020, 230, 1140, 170, INK, 10, 34)
    + box(1150, 300, 540, 250, "#fdf1d6", KI) + t(1420, 370, "エチレン C₂H₄", 50, fill="#8a5a00", weight=900)
    + t(1420, 440, "熟すときに出るガス", 34) + t(1420, 500, "（果物を熟させる）", 34)
    + arrow(1020, 420, 1140, 420, KI, 10, 34)
))

gw = [("0歳", 25), ("1歳", 12), ("2歳", 8), ("3歳", 7), ("思春期のピーク", 10)]
Z["seicho"] = ("1年で伸びる身長（目安）", "0歳の伸びは別格", svg(
    "".join(box(110 + i * 330, 560 - v * 19, 200, v * 19, SHU if i == 0 else ("#e8b04c" if i == 4 else "#c9b79c"), INK, 8, 4)
            + t(210 + i * 330, 540 - v * 19, f"約{v}cm", 50, weight=900, fill=SHU if i == 0 else INK)
            + t(210 + i * 330, 612, lab, 42 if i < 4 else 36, weight=900)
            for i, (lab, v) in enumerate(gw))
    + f'<line x1="60" y1="560" x2="1700" y2="560" stroke="{INK}" stroke-width="5"/>'
    + t(1690, 660, "※思春期のピークは個人差が大きい", 26, "end")
))

dango = "".join(
    f'<circle cx="{150 + (i % 8) * 125}" cy="{130 + (i // 8) * 160}" r="48" '
    + (f'fill="{KI}" stroke="{INK}" stroke-width="5"/>' if i == 0 else f'fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="10 8" opacity=".6"/>')
    for i in range(15))
Z["dango"] = ("犬のお給料", "体重10kgの犬の場合", svg(
    dango
    + t(150, 250, "報酬", 34, fill=SHU, weight=900)
    + t(600, 450, "1日に必要なぶん ＝ だんご約15個", 52, weight=900)
    + box(1150, 40, 570, 540, "#fffaf0")
    + t(1435, 130, "だんご1個", 44) + t(1435, 210, "約40kcal", 70, fill=SHU, weight=900)
    + t(1435, 320, "犬の1日", 44) + t(1435, 400, "約600kcal", 70, weight=900)
    + t(1435, 510, "＝ 1日分の約15分の1", 42, weight=900)
    + t(600, 560, "※だんご1個20g・犬は安静時の目安で計算", 28)
))

rows = [("人", "○", "感じる"), ("犬", "○", "感じる"), ("猿", "○", "感じる"),
        ("猫", "×", "遺伝子が壊れている"), ("キジ", "？", "鳥の多くは遺伝子そのものが無い")]
Z["amami"] = ("甘みを感じる？", "甘みセンサー（T1R2）の有無", svg(
    box(160, 20, 1420, 610, "#fffaf0")
    + "".join(t(360, 115 + 118 * i, a, 60, weight=900)
              + t(620, 118 + 118 * i, b, 78, weight=900, fill=SHU if b == "×" else (KI if b == "？" else KOKE))
              + t(760, 113 + 118 * i, c, 44, "start")
              + (f'<line x1="200" y1="{150 + 118 * i}" x2="1540" y2="{150 + 118 * i}" stroke="{INK}" stroke-width="2" opacity=".3"/>' if i < 4 else "")
              for i, (a, b, c) in enumerate(rows))
))

Z["funayoi"] = ("船酔いのしくみ", "感覚混乱説", svg(
    f'<path d="M520,560 C300,560 260,380 300,260 C340,120 470,60 600,70 C760,80 860,190 850,330 C845,420 800,470 790,560 Z" fill="#f1ddc5" stroke="{INK}" stroke-width="6"/>'
    + f'<ellipse cx="610" cy="210" rx="170" ry="110" fill="#f6c9c0" stroke="{INK}" stroke-width="4"/>' + t(610, 222, "脳", 50, weight=900)
    + f'<ellipse cx="800" cy="300" rx="26" ry="18" fill="#fff" stroke="{INK}" stroke-width="4"/><circle cx="808" cy="300" r="9" fill="{INK}"/>'
    + f'<path d="M520,330 q-30,-40 10,-60 q40,10 20,50 q-20,30 -30,10" stroke="{AI}" stroke-width="8" fill="none"/>'
    + arrow(790, 280, 700, 250, SHU, 7, 24) + arrow(540, 290, 570, 260, AI, 7, 24)
    + box(980, 40, 740, 180, "#fdecea", SHU) + t(1350, 115, "目「止まって見える」", 50, fill=SHU, weight=900) + t(1350, 180, "（船室の中・手元を見ている）", 32)
    + box(980, 260, 740, 180, "#e6f0f6", AI) + t(1350, 335, "耳の奥「揺れてる！」", 50, fill=AI, weight=900) + t(1350, 400, "（平衡感覚をつかさどる三半規管など）", 30)
    + t(1350, 540, "食い違う → 脳が混乱 → 酔う", 52, weight=900)
))

Z["alcohol"] = ("顔が赤くなるしくみ", "アルコールの分解", svg(
    box(20, 60, 330, 150, "#fff") + t(185, 150, "アルコール", 46, weight=900)
    + arrow(360, 135, 520, 135, INK, 8, 30) + t(440, 105, "ADH", 30)
    + box(530, 40, 460, 190, "#fdecea", SHU, sw=6) + t(760, 125, "アセトアルデヒド", 46, fill=SHU, weight=900) + t(760, 185, "顔が赤くなる・どきどき", 32)
    + arrow(1000, 135, 1160, 135, INK, 8, 30) + t(1080, 105, "ALDH2", 30)
    + box(1170, 60, 330, 150, "#fff") + t(1335, 150, "酢酸", 46, weight=900)
    + arrow(1510, 135, 1600, 135, INK, 6, 24) + t(1665, 130, "水と", 30) + t(1665, 170, "CO₂", 30)
    + t(470, 330, "日本人のALDH2のタイプ（目安）", 42, weight=900)
    + "".join(box(70 + x, 380, w, 110, c, INK, 6, 4) for x, w, c in [(0, 896, KOKE), (896, 640, "#e8b04c"), (1536, 64, SHU)])
    + t(518, 450, "よく働く 約56%", 42, fill="#fff", weight=900) + t(1286, 450, "弱い 約40%", 42, weight=900)
    + t(1602, 540, "ほぼ働かない 約4%", 32, "end", fill=SHU, weight=900)
))

Z["kanabo"] = ("金棒の重さ", "中まで鉄の場合", svg(
    f'<rect x="100" y="160" width="1100" height="110" rx="20" fill="#5a5f66" stroke="{INK}" stroke-width="6"/>'
    + "".join(f'<circle cx="{220 + 110 * i}" cy="{215 + (22 if i % 2 else -22)}" r="15" fill="#8b9097" stroke="{INK}" stroke-width="3"/>' for i in range(9))
    + f'<line x1="100" y1="330" x2="1200" y2="330" stroke="{INK}" stroke-width="3"/>' + t(650, 380, "長さ 1.5m", 44, weight=900)
    + f'<line x1="1250" y1="160" x2="1250" y2="270" stroke="{INK}" stroke-width="3"/>' + t(1275, 230, "直径 8cm", 44, "start", weight=900)
    + t(650, 480, "体積 約7,540cm³ × 鉄 7.87g/cm³", 46, weight=900)
    + t(650, 580, "＝ 約60kg", 80, fill=SHU, weight=900)
    + box(1320, 400, 380, 200, "#fffaf0") + t(1510, 480, "お米の30kg袋", 36) + t(1510, 550, "2袋ぶん", 56, weight=900)
))

Z["oni_hikaku"] = ("人と鬼（背たけ2倍）", "二乗三乗の法則の回収", svg(
    person(170, 620, 280, "#5a4a3f") + t(170, 650, "人", 36, weight=900)
    + oni_shape(430, 620, 560) + t(430, 650, "鬼", 36, weight=900)
    + f'<circle cx="720" cy="210" r="50" fill="{MOMO}" stroke="{INK}" stroke-width="4"/>' + t(720, 300, "人の筋肉", 30)
    + f'<circle cx="720" cy="470" r="100" fill="{SHU}" stroke="{INK}" stroke-width="4" opacity=".85"/>' + t(720, 610, "鬼の筋肉（断面積4倍）", 30)
    + box(900, 20, 820, 610, "#fffaf0")
    + "".join(t(960, 125 + 125 * i, a, 48, "start", weight=900) + t(1660, 128 + 125 * i, b, 64, "end", weight=900, fill=c)
              for i, (a, b, c) in enumerate([("背たけ", "2倍", INK), ("筋肉の太さ＝力", "4倍", AI), ("体重", "8倍", INK), ("体重あたりの力", "半分", SHU)]))
    + f'<line x1="940" y1="435" x2="1680" y2="435" stroke="{INK}" stroke-width="3"/>'
))

Z["hana"] = ("においセンサーの種類", "はたらく嗅覚受容体遺伝子（およその数）", svg(
    bars([("人", 400, "#c9b79c", "約400"), ("犬", 800, KOKE, "約800以上")], 40, 150, 1700, 400, 900, bar_h=130, gap=90, label_w=200)
))

Z["tento"] = ("鬼が転ぶと…", "背たけ2倍で比べる", svg(
    person(160, 600, 230, "#5a4a3f")
    + f'<path d="M190,380 q170,40 200,210" stroke="{INK}" stroke-width="5" fill="none" stroke-dasharray="12 10"/>'
    + oni_shape(560, 600, 460)
    + f'<path d="M620,150 q320,70 380,440" stroke="{SHU}" stroke-width="7" fill="none" stroke-dasharray="14 10"/>'
    + f'<line x1="40" y1="600" x2="1060" y2="600" stroke="{INK}" stroke-width="5"/>'
    + box(1090, 20, 640, 610, "#fffaf0")
    + t(1410, 100, "ぶつかるエネルギー", 40, weight=900) + t(1410, 170, "体重8倍×高さ2倍＝16倍", 40, fill=SHU, weight=900)
    + t(1410, 270, "受け止める骨の断面積", 40, weight=900) + t(1410, 340, "4倍", 56, fill=AI, weight=900)
    + f'<line x1="1130" y1="390" x2="1690" y2="390" stroke="{INK}" stroke-width="3"/>'
    + t(1410, 470, "骨1cm²あたりの負担", 40, weight=900) + t(1410, 570, "人の4倍", 84, fill=SHU, weight=900)
))

Z["mitsudo"] = ("同じバケツ1杯（10L）の重さ", "密度のちがい", svg(
    bars([("水", 10, "#9cc3d8", "10kg"), ("鉄", 78.7, "#8b9097", "約79kg"), ("金", 193, KI, "約193kg")],
         40, 60, 1700, 520, 200, bar_h=120, gap=70, label_w=200)
    + t(1700, 630, "密度：水 1.00 ／ 鉄 7.87 ／ 金 19.32（g/cm³）", 30, "end")
))

Z["fune"] = ("舟に積める重さ", "これも浮力", svg(
    f'<rect x="0" y="330" width="1000" height="330" fill="#9cc3d8" opacity=".75"/>'
    + f'<path d="M150,210 L850,210 L780,430 L220,430 Z" fill="#b98a5e" stroke="{INK}" stroke-width="6"/>'
    + f'<path d="M190,330 L810,330 L780,430 L220,430 Z" fill="{AI}" opacity=".35"/>'
    + f'<line x1="0" y1="330" x2="1000" y2="330" stroke="{AI}" stroke-width="5"/>'
    + t(500, 395, "押しのけた水", 42, fill="#fff", weight=900)
    + f'<rect x="330" y="120" width="340" height="90" fill="{KI}" stroke="{INK}" stroke-width="5"/>' + t(500, 180, "金", 50, weight=900)
    + box(1060, 30, 660, 600, "#fffaf0")
    + t(1390, 110, "積める重さ", 46, weight=900)
    + t(1390, 190, "＝ 押しのけられる水の重さ", 38) + t(1390, 245, "− 舟の重さ", 38)
    + f'<line x1="1100" y1="290" x2="1680" y2="290" stroke="{INK}" stroke-width="3"/>'
    + t(1390, 360, "例）4m×1mの箱形の舟が", 34) + t(1390, 410, "あと40cm沈めるなら 1.6トン", 38, weight=900)
    + t(1390, 510, "金なら 約83L", 60, fill=SHU, weight=900) + t(1390, 580, "（バケツ8杯ちょっと）", 34)
))

ions = ["K", "Ca", "Na", "Mg", "Al", "Zn", "Fe", "Ni", "Sn", "Pb", "(H₂)", "Cu", "Hg", "Ag", "Pt", "Au"]
Z["ion"] = ("金はさびない", "イオン化傾向（金属の反応しやすさ）", svg(
    "".join(box(20 + i * 107, 170, 95, 130, KI if s == "Au" else ("#8b9097" if s == "Fe" else "#fff"), INK, 12, 5 if s in ("Au", "Fe") else 3)
            + t(67 + i * 107, 255, s, 44 if len(s) < 3 else 32, weight=900)
            for i, s in enumerate(ions))
    + arrow(40, 390, 1700, 390, INK, 8, 32)
    + t(40, 460, "反応しやすい（さびやすい）", 42, "start", fill=SHU, weight=900)
    + t(1700, 460, "反応しにくい（さびない）", 42, "end", fill=AI, weight=900)
    + t(710, 120, "鉄（金棒）", 38, weight=900) + t(1625, 120, "金", 42, weight=900, fill="#8a5a00")
    + t(870, 580, "金は酸素や水とほとんど反応しない → 何百年たっても輝いたまま", 42, weight=900)
))

Z["hakko"] = ("発酵のしくみ", "桃の糖 → お酒", svg(
    f'<circle cx="220" cy="300" r="170" fill="{MOMO}" stroke="{INK}" stroke-width="6"/>' + t(220, 290, "桃の糖", 46, weight=900) + t(220, 345, "（ブドウ糖など）", 30)
    + arrow(410, 300, 600, 300, INK, 10, 36)
    + "".join(f'<ellipse cx="{680 + dx}" cy="{300 + dy}" rx="44" ry="34" fill="#efe3b8" stroke="{INK}" stroke-width="4"/>' for dx, dy in [(0, -50), (70, 20), (-20, 60)])
    + t(700, 440, "酵母", 46, weight=900)
    + arrow(800, 300, 990, 300, INK, 10, 36)
    + box(1010, 110, 700, 160, "#fdf1d6", KI) + t(1360, 210, "アルコール", 60, fill="#8a5a00", weight=900)
    + box(1010, 330, 700, 160, "#f1ece6") + t(1360, 430, "二酸化炭素", 60, weight=900)
    + t(870, 600, "C₆H₁₂O₆ → 2C₂H₅OH ＋ 2CO₂", 46, weight=900)
))


def chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    for pat in ("chromium-*/chrome-linux/chrome", "chromium/chrome-linux/chrome", "chromium*/chrome"):
        hits = sorted(glob.glob(os.path.join(base, pat)))
        if hits:
            return hits[-1]
    return "chromium"


def ensure_fonts():
    os.makedirs(FONT_DIR, exist_ok=True)
    for name, path in FONTS.items():
        p = os.path.join(FONT_DIR, name)
        if not os.path.exists(p):
            urllib.request.urlretrieve("https://raw.githubusercontent.com/google/fonts/main/" + path, p)


def render(key):
    title, note, body = Z[key]
    html = (PAGE.replace("FONTDIR", os.path.abspath(FONT_DIR)).replace("TITLE", title).replace("NOTE", note)
            .replace("BODY", body).replace("PAPER", PAPER).replace("SHU", SHU).replace("INK", INK))
    os.makedirs(OUT_DIR, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
    out = os.path.join(OUT_DIR, f"{key}.png")
    subprocess.run([chrome(), "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1920,1080", "--virtual-time-budget=3000",
                    f"--screenshot={out}", "file://" + f.name], check=True, capture_output=True)
    os.unlink(f.name)
    print("wrote", os.path.relpath(out, HERE))


if __name__ == "__main__":
    ensure_fonts()
    for k in (sys.argv[1:] or Z):
        render(k)
