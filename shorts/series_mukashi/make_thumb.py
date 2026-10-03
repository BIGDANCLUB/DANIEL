"""桃太郎 長尺版のサムネイル（1280x720 PNG）を作る。

  python3 make_thumb.py          … 全案を thumb_momotaro/ に書き出す
  python3 make_thumb.py a c      … 指定した案だけ

イラスト（illust_momotaro/）の上に、太い縁取りの大きな文字を重ねる。描画は make_zu.py と同じく Chromium。
"""
import os
import subprocess
import sys
import tempfile

from make_zu import chrome

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "thumb_momotaro")
FONT_DIR = os.path.abspath(os.path.join(HERE, "..", "fonts"))
ILL = os.path.join(HERE, "illust_momotaro")

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Noto;font-weight:100 900;src:url("file://FONTDIR/NotoSansJP[wght].ttf")}
@font-face{font-family:Maru;font-weight:900;src:url("file://FONTDIR/ZenMaruGothic-Black.ttf")}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1280px;height:720px;overflow:hidden;background:#000}
.bg{position:absolute;inset:0;background:url("file://IMG") POS/ZOOM no-repeat}
.shade{position:absolute;inset:0;background:SHADE}
.t{position:absolute;font-family:Noto,sans-serif;font-weight:900;line-height:1.02;letter-spacing:-.02em;
  paint-order:stroke fill;-webkit-text-stroke:var(--sw) #000;filter:drop-shadow(0 8px 0 rgba(0,0,0,.55))}
.w{color:#fff}.y{color:#ffe600}.r{color:#ff2a2a}
.tag{position:absolute;left:28px;top:24px;background:#c8442f;color:#fff;font-family:Maru,sans-serif;font-weight:900;
  font-size:76px;line-height:1.1;padding:8px 34px 16px;border-radius:18px;border:8px solid #fff;
  box-shadow:0 10px 0 rgba(0,0,0,.5);letter-spacing:.02em}
</style></head><body><div class="bg"></div><div class="shade"></div>
<div class="tag">TAG</div>BODY</body></html>"""

# 案ごとに：背景（絵・位置・拡大）、暗くする向き、文字
T = {
    "a": dict(img="scene_battle.png", pos="62% 40%", zoom="135%",
              shade="linear-gradient(90deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.35) 48%,rgba(0,0,0,0) 70%)",
              tag="桃太郎を現代風に解説",
              body='<div class="t w" style="--sw:20px;left:40px;top:205px;font-size:104px">鬼が<br>負けた理由</div>'
                   '<div class="t r" style="--sw:26px;left:34px;top:445px;font-size:168px">でかすぎ</div>'),
    "b": dict(img="scene_river.png", pos="55% 62%", zoom="150%",
              shade="linear-gradient(0deg,rgba(0,0,0,.65) 0%,rgba(0,0,0,0) 45%),linear-gradient(90deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 45%)",
              tag="桃太郎を現代風に解説",
              body='<div class="t w" style="--sw:20px;left:40px;top:200px;font-size:96px">桃太郎の桃</div>'
                   '<div class="t y" style="--sw:26px;left:30px;top:295px;font-size:190px">250kg</div>'
                   '<div class="t w" style="--sw:16px;left:44px;top:540px;font-size:64px">おばあさん、持てません</div>'),
    "c": dict(img="scene_road.png", pos="30% 5%", zoom="160%",
              shade="linear-gradient(270deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.3) 45%,rgba(0,0,0,0) 65%)",
              tag="桃太郎を現代風に解説",
              body='<div class="t w" style="--sw:20px;right:40px;top:210px;font-size:96px;text-align:right">報酬<br>だんご1個</div>'
                   '<div class="t r" style="--sw:24px;right:34px;top:450px;font-size:150px;text-align:right">ブラック</div>'),
}


def render(key):
    c = T[key]
    html = (PAGE.replace("FONTDIR", FONT_DIR).replace("IMG", os.path.join(ILL, c["img"]))
            .replace("POS", c["pos"]).replace("ZOOM", c["zoom"]).replace("SHADE", c["shade"])
            .replace("TAG", c["tag"]).replace("BODY", c["body"]))
    os.makedirs(OUT_DIR, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
    out = os.path.join(OUT_DIR, f"thumb_{key}.png")
    subprocess.run([chrome(), "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1280,720", "--virtual-time-budget=3000",
                    f"--screenshot={out}", "file://" + f.name], check=True, capture_output=True)
    os.unlink(f.name)
    print("wrote", os.path.relpath(out, HERE))


if __name__ == "__main__":
    for k in (sys.argv[1:] or T):
        render(k)
