"""浦島太郎 長尺版の解説図（1920x1080 PNG）を作る。描き方・配色は make_zu.py（桃太郎）と共通。

  python3 make_zu_urashima.py            … 全部の図を zu_urashima/ に書き出す
  python3 make_zu_urashima.py shisso     … 指定した図だけ
"""
import os
import subprocess
import sys
import tempfile

from make_zu import (AI, CHA, FONT_DIR, INK, KI, KOKE, MOMO, PAGE, PAPER, SHU, arrow, bars, box, chrome,
                     ensure_fonts, svg, t)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "zu_urashima")
UMI = "#9cc3d8"

Z = {}

Z["kame"] = ("カメに乗ると…", "アカウミガメの場合", svg(
    bars([("浦島太郎", 60, "#c9b79c", "約60kg"), ("アカウミガメ", 100, KOKE, "100kgを超えることも"),
          ("合わせて", 160, SHU, "約160kg")], 40, 40, 1700, 400, 180, bar_h=100, gap=50, label_w=330)
    + box(40, 470, 1660, 150, "#fffaf0")
    + t(870, 535, "ウミガメの多くは、絶滅が心配されている種類", 42, weight=900, fill=SHU)
    + t(870, 595, "地域によっては、捕まえることが規則で禁止されている", 34)
))

Z["miseinen"] = ("カメの売買は「契約」", "もし子どもが親の同意なしに売っていたら", svg(
    box(40, 40, 420, 180, "#fffaf0") + t(250, 120, "子どもたち", 48, weight=900) + t(250, 180, "（未成年）", 34)
    + box(1280, 40, 420, 180, "#fffaf0") + t(1490, 120, "浦島太郎", 48, weight=900) + t(1490, 180, "（買い手）", 34)
    + arrow(470, 100, 1270, 100, KOKE, 8, 30) + t(870, 80, "カメ", 40, weight=900, fill=KOKE)
    + arrow(1270, 170, 470, 170, KI, 8, 30) + t(870, 215, "お金", 40, weight=900, fill="#8a5a00")
    + box(40, 290, 1660, 330, "#fdecea", SHU)
    + t(870, 370, "親の同意がない未成年の契約は、あとから取り消せる", 46, weight=900, fill=SHU)
    + t(870, 430, "（民法5条）", 32)
    + f'<line x1="120" y1="470" x2="1620" y2="470" stroke="{INK}" stroke-width="2" opacity=".3"/>'
    + t(870, 535, "取り消されたら、浦島太郎はカメを返すことに", 42, weight=900)
    + t(870, 595, "→ でもカメは、もう海の中", 42, fill=SHU, weight=900)
))

Z["iki"] = ("人は何分、息を止められる？", "目安", svg(
    bars([("ふつうの人", 1, "#c9b79c", "1分前後"), ("訓練した人", 5, AI, "数分"),
          ("世界記録", 24, SHU, "20分以上（酸素を吸ってから）")], 40, 60, 1700, 480, 40, bar_h=110, gap=70, label_w=330)
    + t(1700, 630, "※まねしないでください", 30, "end")
))

depths = [(0, "1気圧"), (10, "2気圧"), (20, "3気圧"), (30, "4気圧")]
Z["suiatsu"] = ("水深と水圧", "10メートルごとに約1気圧ずつ増える", svg(
    f'<rect x="300" y="40" width="700" height="600" fill="{UMI}" opacity=".8"/>'
    + f'<rect x="300" y="40" width="700" height="600" fill="url(#g)" opacity=".6"/>'
    + '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0"/>'
      f'<stop offset="1" stop-color="{AI}" stop-opacity="1"/></linearGradient></defs>'
    + "".join(f'<line x1="280" y1="{50 + i * 190}" x2="1020" y2="{50 + i * 190}" stroke="{INK}" stroke-width="3" stroke-dasharray="10 8"/>'
              + t(250, 64 + i * 190, f"{dpt}m", 44, "end", weight=900)
              + t(1060, 66 + i * 190, atm, 52, "start", weight=900, fill=SHU if i == 3 else INK)
              for i, (dpt, atm) in enumerate(depths))
    + box(1300, 200, 420, 260, "#fffaf0") + t(1510, 290, "水深30mで", 42) + t(1510, 380, "地上の4倍", 64, fill=SHU, weight=900)
))

cols = [("赤", "#d9412b", 5), ("オレンジ", "#e8892b", 10), ("黄", "#e8c62b", 20), ("緑", "#5aa05a", 45), ("青", "#2f6fb0", 95)]
Z["iro"] = ("海の中では色が消えていく", "深くなるほど、赤い光から届かなくなる（目安）", svg(
    '<defs><linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9d3ea"/>'
    '<stop offset=".6" stop-color="#2f5d7c"/><stop offset="1" stop-color="#0d1b2a"/></linearGradient></defs>'
    + '<rect x="40" y="20" width="1000" height="620" fill="url(#sea)"/>'
    + "".join(f'<rect x="{80 + i * 190}" y="20" width="140" height="{min(600, 20 + d * 6)}" fill="{c}" opacity=".9"/>'
              + t(150 + i * 190, 60, n, 34, fill="#fff", weight=900)
              + t(150 + i * 190, min(600, 20 + d * 6) + 60 if d < 90 else 600, f"〜{d}m" if d < 90 else "最後まで残る", 28, fill="#fff", weight=900)
              for i, (n, c, d) in enumerate(cols))
    + box(1100, 20, 620, 290, "#fffaf0")
    + t(1410, 100, "赤い鯛も、深い海では", 40) + t(1410, 170, "黒っぽく見える", 56, fill=SHU, weight=900)
    + t(1410, 250, "（深い海の魚に赤が多い理由とされる）", 28)
    + box(1100, 350, 620, 290, "#fffaf0")
    + t(1410, 440, "水深200mより深いと", 40) + t(1410, 520, "太陽の光はほぼ届かない", 46, weight=900) + t(1410, 590, "（深海）", 30)
))

Z["urashima"] = ("ウラシマ効果", "とても速く動くと、時間はゆっくり進む", svg(
    box(40, 30, 760, 300, "#e6f0f6", AI) + t(420, 120, "竜宮城（超高速で移動）", 44, weight=900, fill=AI)
    + t(420, 250, "3年", 120, weight=900, fill=AI)
    + box(940, 30, 760, 300, "#fdecea", SHU) + t(1320, 120, "地上（ふつうの時間）", 44, weight=900, fill=SHU)
    + t(1320, 250, "300年", 120, weight=900, fill=SHU)
    + box(40, 370, 1660, 230, "#fffaf0")
    + t(870, 445, "時間の進みを100分の1にするには", 44)
    + t(870, 545, "光の速さの 99.995％", 80, weight=900, fill=SHU)
    + t(1700, 648, "※重力が強い場所でも時間はゆっくり進む（GPS衛星はこのズレを補正している）", 26, "end")
))

Z["energy"] = ("ほぼ光速まで加速すると", "浦島太郎＋カメ＝約160kg", svg(
    box(40, 40, 1660, 220, "#fffaf0")
    + t(870, 130, "必要なエネルギー ＝（100 − 1）× 160kg ×（光の速さ）²", 44, weight=900)
    + t(870, 210, "≒ 1.4 × 10²¹ ジュール", 60, weight=900, fill=SHU)
    + bars([("人類が1年に使う量", 1, "#c9b79c", "約6 × 10²⁰ ジュール"), ("加速1回分", 2.3, KI, "約2年分"),
            ("止まる分も入れると", 4.6, SHU, "約4年半分")],
           40, 300, 1700, 340, 6, bar_h=90, gap=30, label_w=420)
))

Z["shisso"] = ("失踪宣告", "行方不明の人を、法律上「死亡したもの」とみなす制度", svg(
    box(40, 30, 800, 260, "#fffaf0") + t(440, 110, "ふつうの行方不明", 44, weight=900)
    + t(440, 220, "7年", 110, weight=900, fill=INK)
    + box(900, 30, 800, 260, "#fdecea", SHU) + t(1300, 110, "海の事故などの危険にあった", 44, weight=900, fill=SHU)
    + t(1300, 220, "1年", 110, weight=900, fill=SHU)
    + t(870, 350, "→ 家族などの申し立てで「死亡したもの」とみなされる（民法30条・31条）", 38, weight=900)
    + box(40, 400, 1660, 230, "#e6f0f6", AI)
    + t(870, 480, "本人が生きていれば、家庭裁判所で取り消せる（民法32条）", 44, weight=900, fill=AI)
    + t(870, 560, "相続された財産も、残っている分は返してもらえる", 40)
))

Z["dryice"] = ("箱から白い煙…の正体", "現代ならドライアイス", svg(
    box(40, 40, 520, 300, "#e6f0f6", AI) + t(300, 130, "ドライアイス", 48, weight=900)
    + t(300, 250, "−78.5℃", 90, weight=900, fill=AI)
    + box(600, 40, 1100, 300, "#fffaf0")
    + t(1150, 130, "白い煙の正体は", 44)
    + t(1150, 220, "冷やされた空気中の水分（小さな水滴）", 48, weight=900)
    + t(1150, 295, "二酸化炭素そのものは目に見えない", 34)
    + box(40, 390, 1660, 240, "#fdecea", SHU)
    + t(870, 480, "密閉した箱やびんに入れると、破裂するおそれがあって危険", 46, weight=900, fill=SHU)
    + t(870, 570, "せまい部屋では換気を（二酸化炭素がたまる）", 38)
))

Z["jumyo"] = ("鶴は千年、亀は万年？", "実際の寿命（目安）", svg(
    bars([("ツル（野生）", 30, "#c9b79c", "20〜30年ほど"), ("ウミガメ", 60, KOKE, "50年以上と考えられている"),
          ("人（日本の平均）", 84, AI, "約84年"), ("ゾウガメ", 190, SHU, "190歳を超える長生きも")],
         40, 40, 1700, 560, 300, bar_h=100, gap=45, label_w=360)
))


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
