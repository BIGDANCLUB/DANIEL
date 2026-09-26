# -*- coding: utf-8 -*-
"""うごイラ制作 オーケストレータ

  python ugoira.py new    001                       作業フォルダを作る
  python ugoira.py image  001 --batch 4             工程2: 候補生成 (画像+深度)
  python ugoira.py pick   001 3                     工程3: 候補を採用
  python ugoira.py video  001 --motion float        工程4: パララックス動画
  python ugoira.py check  001                       工程5: 検証用フレーム抜き出し
  python ugoira.py all    001                       image → pick(1) → video
  python ugoira.py bench                            RAM/VRAM 判断材料の実測
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

# 記録をファイルに流すと Windows の既定（cp932）になり、英語の記号（— など）で落ちる。
# 2026-09-20: 060n の作り直しが、指示文を表示するところで止まった。出口は常に UTF-8 にして、書けない字は置き換える。
for _out in (sys.stdout, sys.stderr):
    try:
        _out.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import config as C
import comfy_client as cc
import prompts as P


def work_dir(wid: str) -> Path:
    return C.WORKS / wid


# ---------------------------------------------------------------- new
def cmd_new(a) -> None:
    d = work_dir(a.wid)
    d.mkdir(parents=True, exist_ok=True)
    brief = d / "brief.md"
    if not brief.exists():
        brief.write_text(
            (C.ROOT / "prompt_template.md").read_text(encoding="utf-8"),
            encoding="utf-8")
    if not (d / "prompt.json").exists():
        P.save(d, positive="1girl, solo", negative="",
               model=C.DEFAULT_MODEL, motion=C.DEFAULT_MOTION)
    print(f"作成: {d}\n  brief.md を書いたら `image` へ")


# ---------------------------------------------------------------- image
def cmd_image(a) -> None:
    d = work_dir(a.wid)
    if not (d / "prompt.json").exists():
        sys.exit(f"prompt.json がありません: {d}")
    data = P.load(d)
    model = a.model or data.get("model") or C.DEFAULT_MODEL

    print(f"[{a.wid}] 工程2 画像生成  model={model} batch={a.batch}")
    print(f"  POS: {data['_positive'][:110]}...")
    print(f"  NEG: {data['_negative'][:110]}...")

    cc.wait_for_server()
    if a.from_image:
        # 既存画像を下敷きに描き直す（構図を保ったまま部分的に変えたい時）
        src = Path(a.from_image)
        if not src.is_absolute():
            src = d / a.from_image
        if not src.exists():
            sys.exit(f"下敷き画像が見つかりません: {src}")
        name = cc.upload_image(src, f"i2i_{a.wid}_{src.stem}.png")
        print(f"  img2img: {src.name}  denoise={a.denoise}")
        wf, seed = cc.build_img2img_workflow(
            name, data["_positive"], data["_negative"],
            model_key=model,
            seed=a.seed if a.seed is not None else data.get("seed"),
            denoise=a.denoise, batch_size=a.batch,
            prefix=f"ugoira_{a.wid}",
        )
        img_node, dep_node = "11", "13"
    else:
        wf, seed = cc.build_workflow(
            data["_positive"], data["_negative"],
            model_key=model,
            seed=a.seed if a.seed is not None else data.get("seed"),
            hires_scale=1.0 if a.no_hires else C.HIRES_SCALE,
            batch_size=a.batch,
            prefix=f"ugoira_{a.wid}",
        )
        img_node, dep_node = "10", "12"
    (d / "workflow_api.json").write_text(
        json.dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")

    t0 = time.time()
    outs = cc.run(wf, timeout=a.timeout,
                  on_progress=lambda s: print(f"  ...{s:.0f}s", flush=True))
    dt = time.time() - t0

    imgs = cc.collect(outs, img_node)
    deps = cc.collect(outs, dep_node)
    if not imgs:
        sys.exit("画像が生成されませんでした")

    # OneDrive 配下だとフォルダごと消す rmtree が PermissionError になることがある
    # (同期プロセスがハンドルを掴む)。ディレクトリは残してファイルだけ消す。
    cand = d / "candidates"
    cand.mkdir(parents=True, exist_ok=True)
    for old in cand.glob("*"):
        try:
            old.unlink()
        except OSError as e:
            print(f"  (旧候補を削除できません: {old.name} {e})")
    for i, (ip, dp) in enumerate(zip(imgs, deps), 1):
        shutil.copy2(ip, cand / f"cand_{i:02d}.png")
        shutil.copy2(dp, cand / f"cand_{i:02d}_depth.png")

    data["seed"] = seed
    (d / "prompt.json").write_text(
        json.dumps({k: v for k, v in data.items() if not k.startswith("_")},
                   ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"  完了 {dt:.0f}s / {len(imgs)}枚 → {cand}  (seed={seed})")
    print(f"  次: python ugoira.py pick {a.wid} <番号>")


# ---------------------------------------------------------------- pick
def cmd_pick(a) -> None:
    d = work_dir(a.wid)
    src_i = d / "candidates" / f"cand_{a.index:02d}.png"
    src_d = d / "candidates" / f"cand_{a.index:02d}_depth.png"
    if not src_i.exists():
        sys.exit(f"候補が見つかりません: {src_i}")
    shutil.copy2(src_i, d / "image.png")
    shutil.copy2(src_d, d / "depth.png")
    print(f"採用: cand_{a.index:02d} → {d/'image.png'}")


# ---------------------------------------------------------------- video
def cmd_video(a) -> None:
    import parallax

    d = work_dir(a.wid)
    img, dep = d / "image.png", d / "depth.png"
    if not img.exists():
        sys.exit(f"image.png がありません。先に pick してください: {d}")

    data = json.loads((d / "prompt.json").read_text(encoding="utf-8"))
    motion = a.motion or data.get("motion") or C.DEFAULT_MOTION
    out = d / f"{a.wid}_{motion}.mp4"

    print(f"[{a.wid}] 工程4 パララックス  motion={motion} "
          f"loop={a.loop}s target={a.target}s layers={a.layers} dust={a.dust}")

    # 動画工程の前に ComfyUI が抱えている VRAM を解放させる
    if cc.is_alive():
        cc.free_memory()

    t0 = time.time()
    parallax.render(
        img, dep, out,
        motion=motion, loop_seconds=a.loop, target_seconds=a.target,
        n_layers=a.layers, gain=a.gain, dust=a.dust,
        invert_depth=a.invert_depth,
        audio=Path(a.audio) if a.audio else None,
    )
    print(f"  完了 {time.time()-t0:.1f}s → {out}")
    print(f"  次: python ugoira.py check {a.wid}")


# ---------------------------------------------------------------- wanvideo
def cmd_wanvideo(a) -> None:
    """WAN 2.2 TI2V-5B で動画化 (ルートC)。パララックスとは別物。"""
    import wan

    d = work_dir(a.wid)
    data = json.loads((d / "prompt.json").read_text(encoding="utf-8"))
    motion = a.motion_prompt or data.get("wan_motion")
    if not motion:
        sys.exit(
            "動きを記述した英文が必要です。\n"
            "  prompt.json に \"wan_motion\" を書くか --motion-prompt で渡してください。\n"
            "  例: The woman's long hair sways gently in the night breeze. "
            "She blinks slowly and smiles. The camera pushes in very slightly.")

    print(f"[{a.wid}] 工程4 WAN 2.2 TI2V-5B  {'LIGHT' if a.light else 'NATIVE'}")
    t0 = time.time()
    out = wan.render(
        d, motion,
        light=a.light, width=a.width, height=a.height, length=a.length,
        steps=a.steps, cfg=a.cfg, shift=a.shift, seed=a.seed,
        clip_device=a.clip_device, tiled_decode=not a.full_decode,
        tile_size=a.tile_size, temporal_size=a.temporal_size,
        target_seconds=a.target, timeout=a.timeout,
    )
    dt = time.time() - t0

    data["wan_motion"] = motion
    (d / "prompt.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"  完了 {dt/60:.1f}分 → {out}")
    print(f"  次: python ugoira.py check {a.wid} --file \"{out}\"")


# ---------------------------------------------------------------- check
def cmd_check(a) -> None:
    """ループ継ぎ目とフリッカーを数値検証し、目視用フレームを抜き出す。"""
    import numpy as np
    import cv2

    d = work_dir(a.wid)
    vids = sorted(d.glob("*.mp4"))
    if not vids:
        sys.exit(f"mp4 がありません: {d}")
    v = vids[-1] if a.file is None else Path(a.file)

    # cv2.VideoCapture も日本語パスで転ぶので ffmpeg のパイプから読む
    SW, SH = 270, 480
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(v),
         "-vf", f"scale={SW}:{SH}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
        capture_output=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg 読み込み失敗:\n{r.stderr.decode('utf-8','replace')}")
    fsz = SW * SH * 3
    n = len(r.stdout) // fsz
    if n < 4:
        sys.exit("フレームが読めません")
    buf = np.frombuffer(r.stdout[:n * fsz], np.uint8).reshape(n, SH, SW, 3)
    small = [buf[i].astype(np.float32) for i in range(n)]

    # ループ継ぎ目: 末尾→先頭 の差 vs 平均的なフレーム間の差
    seam = float(np.abs(small[-1] - small[0]).mean())
    step = float(np.mean([np.abs(small[i + 1] - small[i]).mean()
                          for i in range(min(n - 1, 120))]))
    # フリッカー: 平均輝度の変動
    lum = np.array([s.mean() for s in small])
    flicker = float(lum.std())

    print(f"検証: {v.name}  frames={n}")
    print(f"  ループ継ぎ目 差分 = {seam:.3f}  (通常フレーム間 = {step:.3f})")
    ratio = seam / step if step > 1e-6 else 0.0
    # 注意: これはエンコード後の映像を測っている。先頭は I フレーム、末尾は P フレーム
    # なので、動きが小さい素材では圧縮ノイズが比を押し上げる（実測で 1.74 まで出た）。
    # パララックスの運動は全て sin の整数倍音なので生成側は数学的に完全ループする
    # （生フレームでの実測比 1.004）。閾値はその分を見込んで 2.0 にしてある。
    print(f"  継ぎ目比 = {ratio:.2f}  → " +
          ("OK 完全ループ" if ratio <= 2.0 else "要確認 継ぎ目が見える可能性"))
    if 1.6 < ratio <= 2.0:
        print("     (動きが小さい素材では H.264 の I/P フレーム差でこの程度は出る)")
    print(f"  輝度フリッカー σ = {flicker:.3f}  → " +
          ("OK" if flicker < 2.0 else "要確認"))

    # 目視用は原寸で抜く (Claude が見て破綻判定するため)
    shots = d / "checkshots"
    shots.mkdir(exist_ok=True)
    for name, idx in [("first", 0), ("q1", n // 4), ("mid", n // 2),
                      ("q3", 3 * n // 4), ("last", n - 1)]:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(v),
             "-vf", f"select=eq(n\\,{idx})", "-vframes", "1",
             "-q:v", "2", str(shots / f"{name}.jpg")],
            capture_output=True)
    print(f"  目視用フレーム → {shots}")


# ---------------------------------------------------------------- all
def cmd_all(a) -> None:
    cmd_image(a)
    a.index = 1
    cmd_pick(a)
    cmd_video(a)
    cmd_check(a)


# ---------------------------------------------------------------- h3video
def cmd_h3video(a) -> None:
    """MiniMax-H3 で動画化 (ルートD / Colab 実行)。"""
    import h3

    d = work_dir(a.wid)
    data = json.loads((d / "prompt.json").read_text(encoding="utf-8"))
    motion = a.motion_prompt or data.get("h3_motion") or data.get("wan_motion")
    if not motion:
        sys.exit("動きを記述した英文が必要です。prompt.json の \"h3_motion\" "
                 "か --motion-prompt で渡してください。")

    if a.list_lengths:
        print("有効な length （(length-5)%17==0 のみ）:")
        for n, s in h3.valid_lengths():
            print(f"  {n:4d} frames = {s:5.2f}秒")
        return

    if C.is_remote():
        print(f"[{a.wid}] 工程4 MiniMax-H3  (リモート: {C.COMFY_URL})")
    else:
        sys.exit("UGOIRA_COMFY_URL が未設定です。Colab のトンネル URL を指定してください:\n"
                 '  $env:UGOIRA_COMFY_URL = "https://xxxx.trycloudflare.com"')

    # 途中のコマに固定する画像: --guide 画像@コマ番号（複数可）。無ければ prompt.json の _gen.guides
    guides = []
    for g in (a.guide or data.get("_gen", {}).get("guides") or []):
        if isinstance(g, str):
            f, _, n = g.rpartition("@")
            g = (f, int(n))
        guides.append((Path(g[0]), int(g[1])))

    t0 = time.time()
    out = h3.render(
        d, motion,
        guides=guides,
        soundscape=a.soundscape or data.get("soundscape"),
        music=a.music or data.get("music_prompt"),
        legacy_prompt=a.legacy_prompt,
        chest=not a.no_chest, expressive=not a.no_expressive,
        drift=a.allow_drift,
        width=a.width, height=a.height,
        length=a.length, seconds=a.seconds,
        steps=a.steps, seed=a.seed,
        turbo=not a.no_turbo, sigma_shift=not a.no_shift,
        shift_video=a.shift_video, shift_audio=a.shift_audio,
        lora_preset=a.lora, lora_strength=a.lora_strength, sampler=a.sampler,
        clip_device=a.clip_device, audio=not a.no_audio,
        upscale=not a.no_upscale, add_style=not a.no_style,
        dynamic=a.dynamic, tag=a.tag, timeout=a.timeout,
        sparse=a.sparse, sparse_start=a.sparse_start,
    )
    dt = time.time() - t0

    # --tag 付き（=パラメータ探索）のときは prompt.json を書き換えない。
    # 書き換えると次の実験が前回のプロンプトを引き継いで条件が崩れる（実際に踏んだ）。
    if not a.tag:
        data["h3_motion"] = motion
        (d / "prompt.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print(f"  (--tag 指定のため prompt.json は更新しません)")

    print(f"  完了 {dt/60:.1f}分 → {out}")
    print(f"  次: python ugoira.py check {a.wid} --file \"{out}\"")


# ---------------------------------------------------------------- h3chain
def cmd_h3chain(a) -> None:
    """既存クリップの続きを生成して繋ぐ（動きと音が継続する）。"""
    import h3

    d = work_dir(a.wid)
    prev = Path(a.prev) if a.prev else None
    if prev is None:
        cands = sorted(d.glob("*_1080.mp4")) or sorted(d.glob("*.mp4"))
        if not cands:
            sys.exit(f"前クリップが見つかりません: {d}")
        prev = max(cands, key=lambda p: p.stat().st_mtime)
    elif not prev.is_absolute():
        prev = d / a.prev

    data = json.loads((d / "prompt.json").read_text(encoding="utf-8"))
    motion = a.motion_prompt or data.get("h3_continue") or data.get("h3_motion")
    if not motion:
        sys.exit("続きの動きを記述した英文が必要です（--motion-prompt か prompt.json の h3_continue）")

    if not C.is_remote():
        sys.exit("UGOIRA_COMFY_URL が未設定です")

    print(f"[{a.wid}] 連結生成  セグメント{a.segments}本")
    parts = [prev]
    for i in range(1, a.segments + 1):
        print(f"\n--- セグメント {i}/{a.segments} ---")
        t0 = time.time()
        seg = h3.render_chain(
            d, parts[-1], motion,
            soundscape=a.soundscape or data.get("soundscape"),
            music=a.music or data.get("music_prompt"),
            width=a.width, height=a.height,
            length=a.length, seconds=a.seconds,
            steps=a.steps, seed=a.seed,
            lora_preset=a.lora, sampler=a.sampler,
            clip_device=a.clip_device, audio=not a.no_audio,
            dynamic=a.dynamic, context_length=a.context_length,
            chest=not a.no_chest, expressive=not a.no_expressive,
            drift=a.allow_drift, tag=f"{i}", timeout=a.timeout)
        print(f"  完了 {(time.time()-t0)/60:.1f}分 → {seg.name}")
        parts.append(seg)

    out = d / f"{a.wid}_chained.mp4"
    h3.concat_segments(parts, out)
    print(f"\n連結: {out}")
    if not a.no_upscale:
        fin = h3._to_final(out, audio=not a.no_audio)
        print(f"仕上げ: {fin}")


# ---------------------------------------------------------------- recover
def cmd_recover(a) -> None:
    """トンネル断で取りこぼした出力を /history から回収する。

    trycloudflare のクイックトンネルは頻繁に切れる（実測で1日3回）。
    クライアントが落ちても ComfyUI 側では生成が完走していることが多いので、
    prompt_id・seed・プロンプト内容を照合して正しいものを選んで拾う。
    先頭を機械的に取ると古い結果を掴む（実際に一度やらかした）。
    """
    import shutil
    import urllib.request

    if not C.is_remote():
        print(f"注意: 接続先がローカルです ({C.COMFY_URL})")
    cc.check_reachable()

    h = json.loads(urllib.request.urlopen(
        f"{C.COMFY_URL}/history?max_items={a.max_items}", timeout=120).read())
    rows = []
    for pid, e in h.items():
        st = e.get("status", {}).get("status_str")
        pr = e.get("prompt", [None, None, {}])[2]
        seed = pr.get("12", {}).get("inputs", {}).get("noise_seed")
        ln = pr.get("8", {}).get("inputs", {}).get("length")
        txt = pr.get("8", {}).get("inputs", {}).get("prompt", "")
        files = [(nid, v) for nid, o in e.get("outputs", {}).items()
                 for k in ("images", "videos", "gifs") for v in o.get(k, [])
                 if v["filename"].lower().endswith((".mp4", ".webm"))]
        rows.append((pid, st, seed, ln, txt, files))

    print(f"history {len(rows)}件  (接続先 {C.COMFY_URL})\n")
    for i, (pid, st, seed, ln, txt, files) in enumerate(rows):
        print(f"[{i}] {pid[:8]} {st:8s} seed={seed} length={ln} 出力{len(files)}件")
        print(f"     {txt[:110].replace(chr(10),' ')}")

    if a.index is None:
        print("\n--index N で選んで回収してください（-1 で最新）")
        return

    pid, st, seed, ln, txt, files = rows[a.index]
    if not files:
        sys.exit(f"[{a.index}] に動画出力がありません (status={st})")

    d = work_dir(a.wid)
    d.mkdir(parents=True, exist_ok=True)
    src = cc.fetch_output(files[0][1])
    dst = d / f"{a.wid}_recovered{('_' + a.tag) if a.tag else ''}.mp4"
    shutil.copy2(src, dst)
    print(f"\n回収: {dst}  ({dst.stat().st_size/2**20:.2f} MB)")

    if not a.no_upscale:
        import h3
        out = h3._to_final(dst, audio=not a.no_audio)
        print(f"仕上げ: {out}  ({out.stat().st_size/2**20:.2f} MB)")


# ---------------------------------------------------------------- h3nodes
def cmd_h3nodes(a) -> None:
    """接続先 ComfyUI の H3 関連ノード定義を吸い出す。

    Colab 側で H3 を立てたあと、ワークフローを書くために使う。
    ノード名を推測で書くと必ず外すので、必ず実物から取る。
    """
    print(f"接続先: {C.COMFY_URL}  (remote={C.is_remote()})")
    cc.wait_for_server(300)
    oi = cc.object_info()
    keys = sorted(k for k in oi if any(t in k.lower() for t in
                  ("minimax", "h3", "qwen3vl", "audio")))
    print(f"該当ノード {len(keys)}件\n")
    for k in keys:
        d = oi[k]["input"]
        req = {kk: (vv[0] if not isinstance(vv[0], list) else f"LIST[{len(vv[0])}]")
               for kk, vv in d.get("required", {}).items()}
        print(f"-- {k}")
        print(f"   required: {json.dumps(req, ensure_ascii=False)}")
        if d.get("optional"):
            print(f"   optional: {list(d['optional'].keys())}")
        print(f"   returns : {oi[k]['output_name']}")

    out = C.ROOT / "h3_nodes.json"
    out.write_text(json.dumps({k: oi[k] for k in keys}, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"\n保存: {out}")


# ---------------------------------------------------------------- bench
def cmd_bench(a) -> None:
    """RAM 増設を判断するための実測。VRAM/RAM のピークと所要時間を出す。"""
    import numpy as np

    cc.wait_for_server()
    s = cc.system_stats()
    dev = s["devices"][0]
    print("=== 環境 ===")
    print(f"  GPU        : {dev['name']}")
    print(f"  VRAM total : {dev['vram_total']/1024**3:.2f} GB")
    print(f"  VRAM free  : {dev['vram_free']/1024**3:.2f} GB")
    print(f"  ComfyUI    : {s['system'].get('comfyui_version')}")

    pos, neg = P.compose("1girl, solo, standing, city street, night, neon lights, "
                         "detailed background, cinematic lighting")
    results = []
    for label, hires, batch in [("素体のみ 832x1472", 1.0, 1),
                                ("hires 1.3x (≈1080x1912)", C.HIRES_SCALE, 1)]:
        cc.free_memory()
        time.sleep(2)
        before = cc.system_stats()["devices"][0]["vram_free"]
        wf, seed = cc.build_workflow(pos, neg, hires_scale=hires,
                                     batch_size=batch, prefix="ugoira_bench")
        t0 = time.time()
        try:
            cc.run(wf, timeout=1800)
            dt = time.time() - t0
            after = cc.system_stats()["devices"][0]["vram_free"]
            used = (before - after) / 1024**3
            results.append((label, dt, used, "OK"))
            print(f"  {label:28s} {dt:6.1f}s  VRAM消費 {used:4.2f} GB  OK")
        except Exception as e:
            results.append((label, time.time() - t0, 0.0, f"NG {e}"))
            print(f"  {label:28s} 失敗: {str(e)[:200]}")

    print("\n=== 判定 ===")
    ok = [r for r in results if r[3] == "OK"]
    if len(ok) == len(results):
        print("  8GB VRAM + 16GB RAM で画像工程は問題なし。")
        print("  → ルートA(パララックス)だけを使うなら RAM 増設は不要。")
        print("  → WAN 2.2 5B などの動画モデルに進む場合のみ 32GB を検討。")
    else:
        print("  hires で失敗 → config.py の HIRES_SCALE を 1.0 に落とすか RAM 増設。")


# ---------------------------------------------------------------- CLI
def main() -> None:
    ap = argparse.ArgumentParser(description="うごイラ制作パイプライン")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_wid(p):
        p.add_argument("wid", help="作品ID 例: 001")

    p = sub.add_parser("new");  add_wid(p);  p.set_defaults(func=cmd_new)

    p = sub.add_parser("image"); add_wid(p)
    p.add_argument("--batch", type=int, default=4)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--model", default=None, choices=list(C.MODELS))
    p.add_argument("--no-hires", action="store_true")
    p.add_argument("--from-image", default=None,
                   help="既存画像を下敷きに描き直す (img2img)。works/NNN/ からの相対でも可")
    p.add_argument("--denoise", type=float, default=0.55,
                   help="img2img の変化量。0.4=質感のみ / 0.55=手や小物が動く / 0.7=大きく変わる")
    p.add_argument("--timeout", type=int, default=1800)
    p.set_defaults(func=cmd_image)

    p = sub.add_parser("pick"); add_wid(p)
    p.add_argument("index", type=int)
    p.set_defaults(func=cmd_pick)

    p = sub.add_parser("video"); add_wid(p)
    p.add_argument("--motion", default=None, choices=list(C.MOTION_PRESETS))
    p.add_argument("--loop", type=float, default=C.LOOP_SECONDS)
    p.add_argument("--target", type=float, default=C.TARGET_SECONDS)
    p.add_argument("--layers", type=int, default=C.DEPTH_LAYERS)
    p.add_argument("--gain", type=float, default=C.PARALLAX_GAIN)
    p.add_argument("--dust", type=int, default=0)
    p.add_argument("--invert-depth", action="store_true")
    p.add_argument("--audio", default=None)
    p.set_defaults(func=cmd_video)

    p = sub.add_parser("wanvideo", help="WAN 2.2 TI2V-5B で動画化 (ルートC)")
    add_wid(p)
    p.add_argument("--motion-prompt", default=None,
                   help="動きを記述した英文。UMT5 は booru タグを読まない")
    p.add_argument("--light", action="store_true",
                   help="480x832 / 49frames(約2秒)。まずこれで通すのを推奨")
    p.add_argument("--width", type=int, default=None)
    p.add_argument("--height", type=int, default=None)
    p.add_argument("--length", type=int, default=None, help="4n+1 のみ")
    p.add_argument("--steps", type=int, default=30)
    p.add_argument("--cfg", type=float, default=5.0)
    p.add_argument("--shift", type=float, default=8.0)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--clip-device", default="default", choices=["default", "cpu"],
                   help="cpu にすると UMT5(6.7GB) を VRAM に載せない。OOM 時の逃げ道")
    p.add_argument("--full-decode", action="store_true",
                   help="VAE を一括デコード。8GB では 704x1280x121 で確実に落ちる")
    p.add_argument("--tile-size", type=int, default=512, help="VAE タイルの空間サイズ")
    p.add_argument("--temporal-size", type=int, default=16,
                   help="一度にデコードするフレーム数。落ちるなら 8 まで下げる")
    p.add_argument("--target", type=float, default=None,
                   help="指定すると往復ループでこの尺まで伸ばす")
    p.add_argument("--timeout", type=int, default=5400)
    p.set_defaults(func=cmd_wanvideo)

    p = sub.add_parser("check"); add_wid(p)
    p.add_argument("--file", default=None)
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("all"); add_wid(p)
    p.add_argument("--batch", type=int, default=4)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--model", default=None, choices=list(C.MODELS))
    p.add_argument("--no-hires", action="store_true")
    p.add_argument("--from-image", default=None,
                   help="既存画像を下敷きに描き直す (img2img)。works/NNN/ からの相対でも可")
    p.add_argument("--denoise", type=float, default=0.55,
                   help="img2img の変化量。0.4=質感のみ / 0.55=手や小物が動く / 0.7=大きく変わる")
    p.add_argument("--timeout", type=int, default=1800)
    p.add_argument("--motion", default=None, choices=list(C.MOTION_PRESETS))
    p.add_argument("--loop", type=float, default=C.LOOP_SECONDS)
    p.add_argument("--target", type=float, default=C.TARGET_SECONDS)
    p.add_argument("--layers", type=int, default=C.DEPTH_LAYERS)
    p.add_argument("--gain", type=float, default=C.PARALLAX_GAIN)
    p.add_argument("--dust", type=int, default=0)
    p.add_argument("--invert-depth", action="store_true")
    p.add_argument("--audio", default=None)
    p.add_argument("--file", default=None)
    p.set_defaults(func=cmd_all)

    p = sub.add_parser("h3video", help="MiniMax-H3 で動画化 (Colab 実行)")
    add_wid(p)
    p.add_argument("--motion-prompt", default=None, help="動きを記述した英文")
    p.add_argument("--seconds", type=float, default=None,
                   help="秒で指定（有効フレーム数に自動で丸める）")
    p.add_argument("--length", type=int, default=124,
                   help="フレーム数。(length-5)%%17==0 のみ。既定124=5.17秒")
    p.add_argument("--width", type=int, default=768)
    p.add_argument("--height", type=int, default=1344)
    p.add_argument("--steps", type=int, default=None,
                   help="既定: turbo時10 / 非turbo時20。turbo で 4 は少なすぎて崩壊する")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--no-turbo", action="store_true",
                   help="Turbo LoRA を使わない（20steps・CU約5倍）")
    p.add_argument("--no-shift", action="store_true",
                   help="MiniMaxH3SigmaShift を挟まない")
    p.add_argument("--shift-video", type=float, default=12.0,
                   help="既定12.0（LoRA作者の実ワークフロー準拠）")
    p.add_argument("--shift-audio", type=float, default=6.0,
                   help="既定6.0。下げすぎると音割れ・ノイズ状の音声になる")
    # drbaph の重みは 2026-08-25 に配布元から消えた。既定は lightx2v。
    p.add_argument("--lora", default="lightx2v", choices=["drbaph", "lightx2v"],
                   help="Turbo LoRA のプリセット。lightx2v は steps4/er_sde/0.75")
    p.add_argument("--lora-strength", type=float, default=None,
                   help="未指定ならプリセットの既定値")
    p.add_argument("--sampler", default=None,
                   help="未指定ならプリセットの既定値（drbaph=res_multistep / lightx2v=er_sde）")
    p.add_argument("--no-style", action="store_true",
                   help="安全用の固定文をプロンプト末尾に足さない")
    p.add_argument("--dynamic", action="store_true",
                   help="動きを大きくする（既定の Subtle 指定を Energetic に切替）")
    p.add_argument("--soundscape", default=None,
                   help="公式書式の overall_soundscape。環境音・動作音のみ1〜4文。"
                        "完全無音は N/A")
    p.add_argument("--music", default=None,
                   help="公式書式の non_diegetic_music（BGM）。既定 N/A")
    p.add_argument("--legacy-prompt", action="store_true",
                   help="旧来の自由文プロンプトで送る（比較用）")
    p.add_argument("--no-chest", action="store_true",
                   help="バストの重量感・揺れの記述を足さない")
    p.add_argument("--no-expressive", action="store_true",
                   help="表情を豊かにする記述を足さない")
    p.add_argument("--allow-drift", action="store_true",
                   help="参照画像の構図を保つ指定を外す。画風や光を途中で変えたい時に使う")
    p.add_argument("--tag", default="", help="出力ファイル名に付ける識別子")
    p.add_argument("--guide", action="append", default=None, metavar="画像@コマ番号",
                   help="途中のコマに画像を固定する（MiniMaxH3AddGuide）。作業フォルダからの相対パス可・複数指定可。"
                        "未指定なら prompt.json の _gen.guides を使う")
    p.add_argument("--no-audio", action="store_true", help="音声を生成しない")
    p.add_argument("--no-upscale", action="store_true",
                   help="1080x1920 への引き伸ばしをしない")
    p.add_argument("--clip-device", default="default", choices=["default", "cpu"])
    p.add_argument("--list-lengths", action="store_true",
                   help="有効な length の一覧を表示して終了")
    p.add_argument("--timeout", type=int, default=5400)
    p.add_argument("--sparse", default=None,
                   help='Model Sparse Attention（ComfyUI v0.35.0〜）。"sol:1.3"=学習不要（tau大ほど省く）'
                        ' / "sla:15"=SLA学習LoRA専用（残す%%）。未指定は密')
    p.add_argument("--sparse-start", type=float, default=0.2,
                   help="この割合までは密のまま（既定0.2）")
    p.set_defaults(func=cmd_h3video)

    p = sub.add_parser("h3chain", help="既存クリップの続きを生成して繋ぐ")
    add_wid(p)
    p.add_argument("--prev", default=None, help="前クリップ。省略で最新の mp4")
    p.add_argument("--segments", type=int, default=1, help="追加するセグメント数")
    p.add_argument("--motion-prompt", default=None,
                   help="続きの動き。省略で prompt.json の h3_continue → h3_motion")
    p.add_argument("--seconds", type=float, default=None)
    p.add_argument("--length", type=int, default=124)
    p.add_argument("--width", type=int, default=704)
    p.add_argument("--height", type=int, default=1248)
    p.add_argument("--context-length", type=int, default=22, choices=[5, 22, 39],
                   help="接続に使うフレーム数。22 が推奨")
    p.add_argument("--steps", type=int, default=None)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--lora", default="lightx2v", choices=["drbaph", "lightx2v"])
    p.add_argument("--sampler", default=None)
    p.add_argument("--clip-device", default="default", choices=["default", "cpu"])
    p.add_argument("--soundscape", default=None)
    p.add_argument("--music", default=None)
    p.add_argument("--dynamic", action="store_true")
    p.add_argument("--no-chest", action="store_true")
    p.add_argument("--no-expressive", action="store_true")
    p.add_argument("--allow-drift", action="store_true",
                   help="参照画像の構図を保つ指定を外す")
    p.add_argument("--no-audio", action="store_true")
    p.add_argument("--no-upscale", action="store_true")
    p.add_argument("--timeout", type=int, default=7200)
    p.set_defaults(func=cmd_h3chain)

    p = sub.add_parser("recover", help="トンネル断で取りこぼした出力を回収する")
    add_wid(p)
    p.add_argument("--index", type=int, default=None,
                   help="一覧の番号。省略すると一覧表示のみ")
    p.add_argument("--max-items", type=int, default=20)
    p.add_argument("--tag", default="")
    p.add_argument("--no-upscale", action="store_true")
    p.add_argument("--no-audio", action="store_true")
    p.set_defaults(func=cmd_recover)

    p = sub.add_parser("h3nodes", help="接続先の H3 ノード定義を吸い出す")
    p.set_defaults(func=cmd_h3nodes)

    p = sub.add_parser("bench"); p.set_defaults(func=cmd_bench)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
