"""② 映像生成：ローカルの ComfyUI（MiniMax H3 i2v）に【】ごとの画像とプロンプトを投げる。

ナレーションの実測尺（out/timeline.json）から各クリップの秒数を決めるので、先に tts_gemini.py を実行すること。

  python tools/comfy_h3.py 01-keiba                 # 全クリップ生成（生成済みはスキップ）
  python tools/comfy_h3.py 01-keiba --only 06_ochi  # 1本だけ
  python tools/comfy_h3.py 01-keiba --redo 03_seitai --seed 1234   # 撮り直し
  python tools/comfy_h3.py 01-keiba --plan          # 投げずに秒数の計画だけ表示
  python tools/comfy_h3.py 01-keiba --mock          # ComfyUIなしでダミー映像を作る（動作確認用）
"""
import argparse
import copy
import json
import math
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

from common import ROOT, find_image, load_config, load_episode, load_json, out_dir, run_ffmpeg, save_json

VIDEO_EXTS = (".mp4", ".webm", ".mov", ".mkv", ".gif")


def plan_seconds(narr, c):
    """ナレーション尺を覆う秒数（整数）。上限を超えた分は assemble でスロー再生して埋める。"""
    return max(c["min_seconds"], min(c["max_seconds"], math.ceil(narr)))


def h3_frames(sec, c):
    """H3 の length は (length - 5) % 17 == 0 のみ有効（ugoira の h3.valid_lengths と同じ規則）。
    sec 秒を覆う最小の有効フレーム数を返す。例: 8秒 → 192。"""
    base, step = c["length_base"], c["length_step"]
    need = sec * c["fps"]
    return base + step * max(0, math.ceil((need - base) / step))


def http(url, data=None, headers=None, timeout=60):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def upload_image(base, path):
    boundary = uuid.uuid4().hex
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{path.name}\"\r\n"
            f"Content-Type: application/octet-stream\r\n\r\n").encode() + path.read_bytes() + \
           (f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue"
            f"\r\n--{boundary}--\r\n").encode()
    res = json.loads(http(f"{base}/upload/image", body, {"Content-Type": f"multipart/form-data; boundary={boundary}"}))
    return f"{res['subfolder']}/{res['name']}" if res.get("subfolder") else res["name"]


def set_input(wf, mapping, key, value):
    m = mapping.get(key)
    if not m or m.get("node") in (None, "", "REPLACE_ME"):
        if key in ("image", "prompt", "duration"):
            sys.exit(f"config.json の comfy.nodes.{key} にノードIDを設定してください（comfy/README.md 参照）。")
        return
    node = wf.get(str(m["node"]))
    if node is None:
        sys.exit(f"ワークフローにノード {m['node']} がありません（comfy.nodes.{key}）。API形式で保存したJSONか確認してください。")
    node["inputs"][m["input"]] = value


def collect_videos(outputs):
    found = []
    for node_out in outputs.values():
        for items in node_out.values():
            if isinstance(items, list):
                for it in items:
                    if isinstance(it, dict) and str(it.get("filename", "")).lower().endswith(VIDEO_EXTS):
                        found.append(it)
    return found


def generate(base, wf, c, timeout, dest):
    client_id = uuid.uuid4().hex
    res = json.loads(http(f"{base}/prompt", json.dumps({"prompt": wf, "client_id": client_id}).encode(),
                          {"Content-Type": "application/json"}))
    if res.get("node_errors"):
        sys.exit(f"ComfyUI がワークフローを拒否しました: {json.dumps(res['node_errors'], ensure_ascii=False)[:1500]}")
    pid = res["prompt_id"]
    t0 = time.time()
    while True:
        hist = json.loads(http(f"{base}/history/{pid}"))
        if pid in hist:
            entry = hist[pid]
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                sys.exit(f"ComfyUI 実行エラー: {json.dumps(status.get('messages', []), ensure_ascii=False)[:1500]}")
            vids = collect_videos(entry.get("outputs", {}))
            if vids:
                v = vids[-1]
                q = urllib.parse.urlencode({"filename": v["filename"], "subfolder": v.get("subfolder", ""),
                                            "type": v.get("type", "output")})
                dest.write_bytes(http(f"{base}/view?{q}", timeout=600))
                return
            if status.get("completed"):
                sys.exit("生成は完了しましたが動画出力が見つかりません。ワークフローに動画保存ノード（VHS_VideoCombine / SaveVideo 等）があるか確認してください。")
        if time.time() - t0 > timeout:
            sys.exit(f"タイムアウト（{timeout}秒）: prompt_id={pid}")
        time.sleep(3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--only", nargs="*", default=[])
    ap.add_argument("--redo", nargs="*", default=[])
    ap.add_argument("--seed", type=int)
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--mock", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    c = cfg["comfy"]
    ep_dir, ep = load_episode(args.episode)
    tl_path = Path(ep_dir, "out", "timeline.json")
    if not tl_path.exists():
        sys.exit("out/timeline.json がありません。先に tools/tts_gemini.py を実行してください。")
    narr = {s["id"]: s["duration"] for s in load_json(tl_path)["sections"]}

    clip_dir = out_dir(ep_dir, "clips")
    plan_path = clip_dir / "plan.json"
    plan = load_json(plan_path) if plan_path.exists() else {}

    targets = [s for s in ep["sections"] if not args.only or s["id"] in args.only]
    missing = [s["id"] for s in targets if not find_image(ep_dir, s["id"])]
    print("クリップ計画（ナレーション実測 → H3 生成秒数）")
    for s in targets:
        sec = plan_seconds(narr[s["id"]], c)
        slow = narr[s["id"]] / sec
        note = f"  ※{slow:.2f}倍に引き伸ばし" if slow > 1.0 else ""
        print(f"  {s['id']:<12} ナレ {narr[s['id']]:5.2f}秒 → 生成 {sec:2d}秒{note}")
    if args.plan:
        return
    if missing and not args.mock:
        sys.exit(f"画像がありません: {', '.join(missing)}\n  {ep_dir / 'images'} に <セクションID>.png を置いてください。")

    # Colab の起動セルが出す trycloudflare の URL は環境変数で渡す（水無瀬と同じ UGOIRA_COMFY_URL も読む）
    base = (os.environ.get("DARWIN_COMFY_URL") or os.environ.get("UGOIRA_COMFY_URL") or c["url"]).rstrip("/")
    print(f"ComfyUI: {base if 'trycloudflare' not in base else base[:12] + '…(tunnel)'}")
    if not args.mock:
        wf_path = ROOT / c["workflow"]
        if not wf_path.exists():
            sys.exit(f"ワークフローがありません: {wf_path}\n  ComfyUI で H3 i2v ワークフローを「API形式で保存」して置いてください。")
        workflow = load_json(wf_path)
        try:
            http(f"{base}/system_stats", timeout=5)
        except (urllib.error.URLError, OSError):
            sys.exit(f"ComfyUI に接続できません: {base}（起動しているか確認してください）")

    for s in targets:
        dest = clip_dir / f"{s['id']}.mp4"
        if dest.exists() and s["id"] not in args.redo:
            print(f"  skip {s['id']}（生成済み。撮り直すなら --redo {s['id']}）")
            continue
        sec = plan_seconds(narr[s["id"]], c)
        seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
        if args.mock:
            run_ffmpeg(["-f", "lavfi", "-i", f"testsrc2=size=720x1280:rate={c['fps']}:duration={sec}",
                        "-f", "lavfi", "-i", f"anoisesrc=d={sec}:c=pink:a=0.05",
                        "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", dest])
        else:
            wf = copy.deepcopy(workflow)
            nodes = c["nodes"]
            set_input(wf, nodes, "image", upload_image(base, find_image(ep_dir, s["id"])))
            set_input(wf, nodes, "prompt", s["video_prompt"])
            set_input(wf, nodes, "negative", ep.get("video_negative", ""))
            d = nodes["duration"]
            dur_val = h3_frames(sec, c) if d.get("unit", "frames") == "frames" else sec
            set_input(wf, nodes, "duration", dur_val)
            set_input(wf, nodes, "seed", seed)
            set_input(wf, nodes, "width", c["width"])
            set_input(wf, nodes, "height", c["height"])
            print(f"  生成中 {s['id']}（{sec}秒, seed={seed}）…")
            generate(base, wf, c, c["timeout_sec"], dest)
        plan[s["id"]] = {"seconds": sec, "seed": seed, "narration": narr[s["id"]], "mock": args.mock}
        save_json(plan_path, plan)
        print(f"  ✓ {dest.name}")


if __name__ == "__main__":
    main()
