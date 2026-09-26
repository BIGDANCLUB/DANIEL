"""② 映像生成：水無瀬（ugoira）の h3.py をそのまま使い、Colab の ComfyUI（MiniMax H3）で【】ごとに1クリップ作る。

ワークフロー・トンネル越しのアップロード・音声の別取り・真っ黒検知などは ugoira 側の実装に任せる。
ナレーションの実測尺（out/timeline.json）から各クリップの長さを決めるので、先に tts_gemini.py を実行すること。

  $env:UGOIRA_COMFY_URL = "https://....trycloudflare.com"   # Colab の起動セルが出す URL
  python tools/comfy_h3.py 01-keiba --plan          # 投げずに長さの計画だけ表示
  python tools/comfy_h3.py 01-keiba --only 02_hakken
  python tools/comfy_h3.py 01-keiba                 # 残りを全部（生成済みはスキップ）
  python tools/comfy_h3.py 01-keiba --redo 06_ochi --seed 1234
  python tools/comfy_h3.py 01-keiba --mock          # Colab なしでダミー映像（動作確認用）
"""
import argparse
import math
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path

from common import ffmpeg_exe, find_image, load_config, load_episode, load_json, out_dir, run_ffmpeg, save_json

FPS = 24  # H3 は 24fps 固定


def h3_frames(seconds, max_seconds):
    """H3 の length は (length-5) % 17 == 0 のみ。ナレーションを覆う最小値（上限 max_seconds）を返す。"""
    top = 5 + 17 * int((max_seconds * FPS - 5) // 17)
    need = 5 + 17 * max(0, math.ceil((seconds * FPS - 5) / 17))
    return min(need, top)


def is_black(path):
    """2秒おきにコマを抜き出し、全部ほぼ真っ黒なら True（H3 の計算が NaN で壊れたとき）。"""
    raw = subprocess.run([ffmpeg_exe(), "-v", "error", "-i", str(path), "-vf", "select=not(mod(n\\,48)),scale=64:96",
                          "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
    return bool(raw) and max(raw) < 3


def load_ugoira(c):
    """ugoira フォルダの h3.py を読み込む。接続先 URL は ugoira の config が UGOIRA_COMFY_URL から読む。"""
    d = Path(os.environ.get("UGOIRA_DIR") or c["ugoira_dir"]).expanduser()
    if not (d / "h3.py").exists():
        sys.exit(f"ugoira の h3.py が見つかりません: {d}\n"
                 "  config.json の comfy.ugoira_dir（または環境変数 UGOIRA_DIR）を ugoira フォルダにしてください。")
    if os.environ.get("DARWIN_COMFY_URL") and not os.environ.get("UGOIRA_COMFY_URL"):
        os.environ["UGOIRA_COMFY_URL"] = os.environ["DARWIN_COMFY_URL"]
    if not os.environ.get("UGOIRA_COMFY_URL"):
        sys.exit("UGOIRA_COMFY_URL が未設定です。Colab の起動セルが出した URL を指定してください:\n"
                 '  $env:UGOIRA_COMFY_URL = "https://xxxx.trycloudflare.com"')
    sys.path.insert(0, str(d))
    import h3  # noqa: E402  (ugoira 側のモジュール)
    return h3


def render_one(h3, work, s, c, frames, seed):
    return h3.render(
        work, s["video_prompt"],
        soundscape=s.get("soundscape") or "N/A",
        music="N/A",                      # BGM は結合時に入れる
        chest=False, expressive=False,    # ugoira（キャラクター）向けの常設指示は使わない
        add_style=False,                  # 動きの強さ・構図固定の定型文も付けない（プロンプトで書き切る）
        width=c["width"], height=c["height"], length=frames,
        steps=c.get("steps"), seed=seed, lora_preset=c["lora"],
        upscale=False, timeout=c["timeout_sec"],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--only", nargs="*", default=[])
    ap.add_argument("--redo", nargs="*", default=[])
    ap.add_argument("--seed", type=int)
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--check", action="store_true", help="作成済みクリップのうち真っ黒なものを一覧にする（Colab 不要）")
    args = ap.parse_args()

    c = load_config()["comfy"]
    ep_dir, ep = load_episode(args.episode)
    tl_path = Path(ep_dir, "out", "timeline.json")
    if not tl_path.exists():
        sys.exit("out/timeline.json がありません。先に tools/tts_gemini.py を実行してください。")
    narr = {s["id"]: s["duration"] for s in load_json(tl_path)["sections"]}

    clip_dir = out_dir(ep_dir, "clips")
    plan_path = clip_dir / "plan.json"
    plan = load_json(plan_path) if plan_path.exists() else {}
    targets = [s for s in ep["sections"] if not args.only or s["id"] in args.only]

    if args.check:
        bad = []
        for s in targets:
            clip = clip_dir / f"{s['id']}.mp4"
            if not clip.exists():
                print(f"  {s['id']:<12} 未作成")
            elif is_black(clip):
                bad.append(s["id"])
                print(f"  {s['id']:<12} ✗ 真っ黒")
            else:
                print(f"  {s['id']:<12} ✓ OK")
        if bad:
            print(f"\n作り直し: python tools/comfy_h3.py {args.episode} --redo {' '.join(bad)}")
        return

    print(f"クリップ計画（ナレーション実測 → H3 {c['width']}x{c['height']}）")
    for s in targets:
        n = h3_frames(narr[s["id"]], c["max_seconds"])
        slow = narr[s["id"]] / (n / FPS)
        note = f"  ※{slow:.2f}倍に引き伸ばし" if slow > 1.0 else ""
        print(f"  {s['id']:<12} ナレ {narr[s['id']]:5.2f}秒 → {n:3d}フレーム（{n / FPS:5.2f}秒）{note}")
    if args.plan:
        return

    missing = [s["id"] for s in targets if not find_image(ep_dir, s["id"])]
    if missing and not args.mock:
        sys.exit(f"画像がありません: {', '.join(missing)}\n  {ep_dir / 'images'} に <セクションID>.png を置いてください。")
    h3 = None if args.mock else load_ugoira(c)

    for s in targets:
        dest = clip_dir / f"{s['id']}.mp4"
        if dest.exists() and s["id"] not in args.redo:
            if not args.mock and is_black(dest):
                print(f"  {s['id']} は真っ黒なので作り直します")
            else:
                print(f"  skip {s['id']}（生成済み。撮り直すなら --redo {s['id']}）")
                continue
        frames = h3_frames(narr[s["id"]], c["max_seconds"])
        seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
        if args.mock:
            sec = frames / FPS
            run_ffmpeg(["-f", "lavfi", "-i", f"testsrc2=size={c['width']}x{c['height']}:rate={FPS}:duration={sec:.3f}",
                        "-f", "lavfi", "-i", f"anoisesrc=d={sec:.3f}:c=pink:a=0.05",
                        "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", dest])
        else:
            # h3.render は <作業フォルダ>/image.png を起点にする（jpg 等も png にしておく）
            work = out_dir(ep_dir, "h3", s["id"])
            run_ffmpeg(["-i", find_image(ep_dir, s["id"]), "-frames:v", "1", work / "image.png"])
            tries = 1 + int(c.get("black_retries", 2))
            for attempt in range(tries):
                print(f"\n=== {s['id']} {s['label']}（seed={seed}）===")
                out = render_one(h3, work, s, c, frames, seed)
                if not is_black(out):
                    break
                if attempt + 1 < tries:
                    seed = random.randint(0, 2**31 - 1)
                    print(f"  真っ黒だったのでシードを変えて作り直します（{attempt + 1}/{tries - 1}）")
            else:
                print(f"  ✗ {s['id']} は {tries} 回とも真っ黒でした。長さ（max_seconds）やステップ数の見直しが必要です")
                continue
            shutil.copy2(out, dest)
            plan[s["id"]] = {"frames": frames, "seconds": round(frames / FPS, 3), "seed": seed,
                             "narration": narr[s["id"]], "mock": False}
            save_json(plan_path, plan)
            print(f"  ✓ {dest.name}")
            continue
        plan[s["id"]] = {"frames": frames, "seconds": round(frames / FPS, 3), "seed": seed,
                         "narration": narr[s["id"]], "mock": args.mock}
        save_json(plan_path, plan)
        print(f"  ✓ {dest.name}")


if __name__ == "__main__":
    main()
