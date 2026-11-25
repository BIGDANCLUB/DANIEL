"""再審査用：ショートごとに「台本（Word）・見本動画・背景・猫ミーム素材・効果音・フォント」を1つのフォルダにまとめる（11/18 ユーザー指定）。

python3 catmeme/tools/make_rereview.py → catmeme/rereview/short_<番号>_<名前>/
- 対象：world_short.py で作ったショートのうち、release/ に完成版があり、ボツでないもの
- ファイルは同じ中身を何回も持たないよう、できればハードリンクで置く（git でも1回分しか増えない）
"""
import glob
import importlib
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
os.chdir(HERE)

from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Pt  # noqa: E402

import income_short as I  # noqa: E402
import world_short as W  # noqa: E402

OUT = os.path.join(HERE, "rereview")
BOTSU = {"75_karasa", "87_manin", "89_natsuyasumi", "99_oshikatsu", "101_fukugyo",
         # 11/25 ユーザー指定「141まで全ボツ」：未修正のまま残っていた 141 までのショート
         "113_tsukin", "117_okinawa", "119_conbini_yoru", "124_ryoko_nimotsu", "125_kaze_danjo", "126_chikoku_danjo",
         "130_sanrenkyu_yoru", "133_denchi", "136_gohan_ryo", "137_kotsuhi", "139_shiokuri", "140_taishoku", "141_kozukai_fufu"}


def place(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        os.remove(dst)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def se_file(kind):
    for ext in (".mp3", ".wav", ".m4a"):
        p = os.path.join(HERE, "se", kind + ext)
        if os.path.isfile(p):
            return p
    return None


def youtube_texts():
    """scripts/short_*_youtube.md から 番号 → (タイトル, 概要欄)。"""
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, "scripts", "short_*_youtube.md"))):
        txt = open(f, encoding="utf-8").read()
        for sec in re.split(r"\n## ", txt)[1:]:
            name = sec.split("\n", 1)[0].strip().split()[0]
            m = re.search(r"タイトル：(.+)", sec)
            d = re.search(r"```\n(.*?)\n```", sec, re.S)
            if m:
                out[name] = (m.group(1).strip(), d.group(1).strip() if d else "")
    return out


def band_text(src):
    return [m for m in re.findall(r'\("\{[a-z]\}([^"]+)"', src)][:2]


def jp(run, size=10.5, bold=False):
    run.font.size = Pt(size)
    run.bold = bold
    run.font.name = "Meiryo"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Meiryo")


def para(doc, text, size=10.5, bold=False):
    p = doc.add_paragraph()
    jp(p.add_run(text), size, bold)
    return p


def build(name, yt):
    mod = importlib.import_module("short_" + name)
    src = open(os.path.join(HERE, "short_%s.py" % name), encoding="utf-8").read()
    if not hasattr(mod, "cuts"):
        return None
    cs = mod.cuts()
    folder = os.path.join(OUT, "short_" + name)
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    bgs, cats, ses, fonts = [], [], [], ["NotoSansJP[wght].ttf"]
    rows, t = [], 0.0
    for c in cs:
        bg = c.get("bg")
        if bg and bg not in bgs:
            bgs.append(bg)
        names = [q.get("a") for q in c.get("cats", []) if q.get("a")]
        for a in names:
            if a not in cats:
                cats.append(a)
        se = c.get("se")
        se = [se] if isinstance(se, (str, dict)) else list(se or [])
        se = [x.get("kind") or x.get("file") or x.get("name") if isinstance(x, dict) else x for x in se]
        se = [x for x in se if isinstance(x, str)]
        for s in se:
            if s not in ses:
                ses.append(s)
        for cap in (c.get("cap"), c.get("cap2")):
            if cap and cap.startswith("{fancy}") and "GreatVibes-Regular.ttf" not in fonts:
                fonts.append("GreatVibes-Regular.ttf")
        left = next((q.get("a") or "" for q in c.get("cats", []) if q.get("x", 540) < 540), "")
        right = next((q.get("a") or "" for q in c.get("cats", []) if q.get("x", 0) >= 540), "")
        rows.append((t, c.get("dur", 0), c.get("tag") or "", left, right, c.get("cap") or "", c.get("cap_side", ""),
                     c.get("cap2") or "", ", ".join(map(str, se)), c.get("heads")))
        t += c.get("dur", 0)
    # 素材
    for bg in bgs:
        p = I.bg_path(W.bg_name(bg))
        place(p, os.path.join(folder, "背景", os.path.basename(p)))
    for a in cats:
        if not os.path.isfile(os.path.join(HERE, "assets", a + ".mp4")):
            continue
        place(os.path.join(HERE, "assets", a + ".mp4"), os.path.join(folder, "猫ミーム素材", a + ".mp4"))
    miss = []
    for s in ses:
        p = se_file(s)
        if p:
            place(p, os.path.join(folder, "効果音", os.path.basename(p)))
        else:
            miss.append(s)
    for f in fonts:
        place(os.path.join(HERE, "fonts", f), os.path.join(folder, "フォント", f))
    rel = os.path.join(HERE, "release", "short_%s.mp4" % name)
    if os.path.isfile(rel):
        place(rel, os.path.join(folder, "見本_short_%s.mp4" % name))
    # 台本（Word）
    doc = Document()
    num = name.split("_")[0]
    title, desc = yt.get(name, ("", ""))
    band = band_text(src)
    para(doc, "ショート%s　台本" % num, 16, True)
    para(doc, "画面：縦 1080×1920・長さ %.1f 秒・BGM なし（猫ミームの音と効果音だけ）" % t)
    para(doc, "上の黒い帯（黄色い文字）：" + "／".join(band))
    heads = next((r[9] for r in rows if r[9]), ("日本", "世界"))
    para(doc, "左右の見出し：左「%s」（青）・右「%s」（赤）" % heads)
    para(doc, "背景（全カット共通・少しぼかす）：" + "、".join(os.path.basename(I.bg_path(W.bg_name(b))) for b in bgs))
    para(doc, "画面全体を150px下にずらす（上は黒で埋める）※95番以降" if int(re.sub(r"\D", "", num) or 0) >= 95 else "")
    if title:
        para(doc, "YouTube タイトル", 12, True)
        para(doc, title)
        para(doc, "概要欄", 12, True)
        for ln in desc.split("\n"):
            para(doc, ln)
    para(doc, "カットの流れ（1段＝「札だけ」→「右の猫と字幕」→「左の猫と字幕」の3カット）", 12, True)
    tb = doc.add_table(rows=1, cols=8)
    tb.style = "Table Grid"
    for i, h in enumerate(["開始(秒)", "長さ(秒)", "札", "左の猫素材", "右の猫素材", "字幕", "字幕の位置", "効果音"]):
        cell = tb.rows[0].cells[i]
        cell.text = ""
        jp(cell.paragraphs[0].add_run(h), 9, True)
    for (st, du, tag, lf, rt, cap, side, cap2, se, _) in rows:
        r = tb.add_row().cells
        capt = cap.replace("\n", "／").replace("{fancy}", "（筆記体）")
        if cap2:
            capt += "　※反対側にも：" + cap2.replace("\n", "／")
        vals = ["%.1f" % st, "%.1f" % du, tag, lf, rt, capt, {"L": "左", "R": "右"}.get(side, "") if cap else "", se]
        for i, v in enumerate(vals):
            r[i].text = ""
            jp(r[i].paragraphs[0].add_run(v), 8.5)
    para(doc, "")
    para(doc, "見た目のルール", 12, True)
    for ln in ["札：白い枠・オレンジのふち・赤い文字（例：1時間・夜）。画面の上のほう中央",
               "字幕：白地に緑の太い枠・青い太字（NotoSansJP）。話している側の猫の下に出す",
               "猫：左右に1匹ずつ（同じ側の猫の音だけ鳴らす）。左右のあいだに黒い縦線",
               "効果音：札のとき pi（最後の4段は explosion_chudoon）、右の猫が出るとき don_hit"]:
        para(doc, "・" + ln, 9.5)
    if miss:
        para(doc, "※ファイルが無く合成で鳴らした効果音：" + "、".join(miss), 9)
    doc.save(os.path.join(folder, "台本_short_%s.docx" % name))
    return len(cats), len(bgs), len(ses)


def main():
    yt = youtube_texts()
    names = []
    for f in sorted(glob.glob(os.path.join(HERE, "short_*.py"))):
        if "import world_short" not in open(f, encoding="utf-8").read():
            continue
        n = os.path.basename(f)[6:-3]
        if n in BOTSU or not os.path.isfile(os.path.join(HERE, "release", "short_%s.mp4" % n)):
            continue
        names.append(n)
    os.makedirs(OUT, exist_ok=True)
    for n in names:
        try:
            r = build(n, yt)
        except Exception as e:   # 作り方がちがう古いショートは飛ばす
            r = None
            print("skip", n, e)
        print(n, *(r or ("skip",)), flush=True)


if __name__ == "__main__":
    main()
