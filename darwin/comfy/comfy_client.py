# -*- coding: utf-8 -*-
"""ComfyUI API クライアント + ワークフロー組み立て

ComfyUI を API モードで常駐させておけば、ここから全部叩ける。
起動:  ugoira\start_comfy.ps1
"""
from __future__ import annotations

import json
import random
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

import config as C


# ---------------------------------------------------------------- 低レベル API
class ComfyError(RuntimeError):
    pass


def _post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"{C.COMFY_URL}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def _get(path: str) -> dict:
    with urllib.request.urlopen(f"{C.COMFY_URL}{path}", timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def is_alive() -> bool:
    try:
        _get("/system_stats")
        return True
    except Exception:
        return False


def check_reachable() -> None:
    """接続できない理由を切り分けて、分かりやすく落とす。

    trycloudflare のクイックトンネルは予告なく切れる（実測で1日2回）。
    そのとき Cloudflare が 530 を返すので、ComfyUI 側の障害と区別できる。
    """
    import urllib.error
    try:
        _get("/system_stats")
        return
    except urllib.error.HTTPError as e:
        if e.code in (502, 503, 530):
            raise ComfyError(
                f"トンネルが切れています (HTTP {e.code}): {C.COMFY_URL}\n"
                "  Colab のセル5を再実行して新しい URL を取得し、\n"
                '  $env:UGOIRA_COMFY_URL に設定し直してください。\n'
                "  ※ ランタイムとモデルは残っているので再ダウンロードは不要です。"
            ) from e
        raise ComfyError(f"ComfyUI が HTTP {e.code} を返しました: {C.COMFY_URL}") from e
    except Exception as e:
        raise ComfyError(
            f"ComfyUI に接続できません: {C.COMFY_URL}\n"
            f"  {type(e).__name__}: {e}"
        ) from e


def wait_for_server(timeout: int = 300) -> None:
    """ComfyUI の起動完了を待つ。"""
    t0 = time.time()
    while time.time() - t0 < timeout:
        if is_alive():
            return
        time.sleep(2)
    raise ComfyError(f"ComfyUI が {timeout}s 以内に応答しませんでした ({C.COMFY_URL})")


def system_stats() -> dict:
    return _get("/system_stats")


def object_info(node: str | None = None) -> dict:
    return _get(f"/object_info/{node}" if node else "/object_info")


def free_memory(unload_models: bool = True) -> None:
    """VRAM を解放する。動画工程の前に呼ぶ。"""
    try:
        _post("/free", {"unload_models": unload_models, "free_memory": True})
    except Exception:
        pass


# ---------------------------------------------------------------- ワークフロー
def build_workflow(
    positive: str,
    negative: str,
    *,
    model_key: str = C.DEFAULT_MODEL,
    seed: int | None = None,
    width: int = C.BASE_W,
    height: int = C.BASE_H,
    hires_scale: float = C.HIRES_SCALE,
    hires_denoise: float = 0.45,
    batch_size: int = 1,
    prefix: str = "ugoira",
) -> tuple[dict, int]:
    """画像 + 深度マップ を一度に生成する API ワークフローを組む。

    戻り値: (workflow_dict, 使用した seed)
    """
    m = C.MODELS[model_key]
    if seed is None:
        seed = random.randint(0, 2**31 - 1)

    wf: dict[str, dict] = {}

    wf["1"] = {"class_type": "CheckpointLoaderSimple",
               "inputs": {"ckpt_name": m["ckpt"]}}

    model_src = ["1", 0]
    if m["vpred"]:
        # NoobAI v-pred は必須。無いと出力が真っ白／真っ黒になる
        wf["2"] = {"class_type": "ModelSamplingDiscrete",
                   "inputs": {"model": ["1", 0], "sampling": "v_prediction", "zsnr": True}}
        model_src = ["2", 0]

    wf["3"] = {"class_type": "CLIPTextEncode",
               "inputs": {"text": positive, "clip": ["1", 1]}}
    wf["4"] = {"class_type": "CLIPTextEncode",
               "inputs": {"text": negative, "clip": ["1", 1]}}
    wf["5"] = {"class_type": "EmptyLatentImage",
               "inputs": {"width": width, "height": height, "batch_size": batch_size}}

    wf["6"] = {"class_type": "KSampler",
               "inputs": {"model": model_src, "positive": ["3", 0], "negative": ["4", 0],
                          "latent_image": ["5", 0], "seed": seed, "steps": m["steps"],
                          "cfg": m["cfg"], "sampler_name": m["sampler"],
                          "scheduler": m["scheduler"], "denoise": 1.0}}

    latent_src = ["6", 0]
    if hires_scale and hires_scale > 1.001:
        hw = int(round(width * hires_scale / 8) * 8)
        hh = int(round(height * hires_scale / 8) * 8)
        wf["7"] = {"class_type": "LatentUpscale",
                   "inputs": {"samples": ["6", 0], "upscale_method": "nearest-exact",
                              "width": hw, "height": hh, "crop": "disabled"}}
        wf["8"] = {"class_type": "KSampler",
                   "inputs": {"model": model_src, "positive": ["3", 0], "negative": ["4", 0],
                              "latent_image": ["7", 0], "seed": seed, "steps": m["steps"],
                              "cfg": m["cfg"], "sampler_name": m["sampler"],
                              "scheduler": m["scheduler"], "denoise": hires_denoise}}
        latent_src = ["8", 0]

    wf["9"] = {"class_type": "VAEDecode",
               "inputs": {"samples": latent_src, "vae": ["1", 2]}}
    wf["10"] = {"class_type": "SaveImage",
                "inputs": {"images": ["9", 0], "filename_prefix": f"{prefix}/img"}}

    # 深度マップも同じジョブ内で作る (別途モデルをロードし直さずに済む)
    wf["11"] = {"class_type": "DepthAnythingV2Preprocessor",
                "inputs": {"image": ["9", 0], "ckpt_name": "depth_anything_v2_vitl.pth",
                           "resolution": 1024}}
    wf["12"] = {"class_type": "SaveImage",
                "inputs": {"images": ["11", 0], "filename_prefix": f"{prefix}/depth"}}

    return wf, seed


def build_img2img_workflow(
    image_name: str,
    positive: str,
    negative: str,
    *,
    model_key: str = C.DEFAULT_MODEL,
    seed: int | None = None,
    denoise: float = 0.55,
    width: int | None = None,
    height: int | None = None,
    batch_size: int = 1,
    prefix: str = "ugoira_i2i",
) -> tuple[dict, int]:
    """既存画像を下敷きに描き直す。構図と雰囲気を保ったまま部分的に変えたい時用。

    denoise の目安:
      0.35〜0.45 … 質感の調整のみ。ポーズは変わらない
      0.50〜0.60 … 小物や手の位置が動く。元絵の面影は残る
      0.65〜0.75 … 構図は残るが中身はかなり変わる
    """
    m = C.MODELS[model_key]
    if seed is None:
        seed = random.randint(0, 2**31 - 1)

    wf: dict[str, dict] = {}
    wf["1"] = {"class_type": "CheckpointLoaderSimple",
               "inputs": {"ckpt_name": m["ckpt"]}}

    model_src = ["1", 0]
    if m["vpred"]:
        wf["2"] = {"class_type": "ModelSamplingDiscrete",
                   "inputs": {"model": ["1", 0], "sampling": "v_prediction", "zsnr": True}}
        model_src = ["2", 0]

    wf["3"] = {"class_type": "CLIPTextEncode",
               "inputs": {"text": positive, "clip": ["1", 1]}}
    wf["4"] = {"class_type": "CLIPTextEncode",
               "inputs": {"text": negative, "clip": ["1", 1]}}
    wf["5"] = {"class_type": "LoadImage", "inputs": {"image": image_name}}

    img_src = ["5", 0]
    if width and height:
        wf["6"] = {"class_type": "ImageScale",
                   "inputs": {"image": ["5", 0], "upscale_method": "lanczos",
                              "width": width, "height": height, "crop": "center"}}
        img_src = ["6", 0]

    wf["7"] = {"class_type": "VAEEncode",
               "inputs": {"pixels": img_src, "vae": ["1", 2]}}

    latent_src = ["7", 0]
    if batch_size > 1:
        wf["8"] = {"class_type": "RepeatLatentBatch",
                   "inputs": {"samples": ["7", 0], "amount": batch_size}}
        latent_src = ["8", 0]

    wf["9"] = {"class_type": "KSampler",
               "inputs": {"model": model_src, "positive": ["3", 0], "negative": ["4", 0],
                          "latent_image": latent_src, "seed": seed, "steps": m["steps"],
                          "cfg": m["cfg"], "sampler_name": m["sampler"],
                          "scheduler": m["scheduler"], "denoise": denoise}}
    wf["10"] = {"class_type": "VAEDecode",
                "inputs": {"samples": ["9", 0], "vae": ["1", 2]}}
    wf["11"] = {"class_type": "SaveImage",
                "inputs": {"images": ["10", 0], "filename_prefix": f"{prefix}/img"}}
    wf["12"] = {"class_type": "DepthAnythingV2Preprocessor",
                "inputs": {"image": ["10", 0], "ckpt_name": "depth_anything_v2_vitl.pth",
                           "resolution": 1024}}
    wf["13"] = {"class_type": "SaveImage",
                "inputs": {"images": ["12", 0], "filename_prefix": f"{prefix}/depth"}}
    return wf, seed


# ---------------------------------------------------------------- 実行
def run(workflow: dict, *, timeout: int = 1800, poll: float = 2.0,
        on_progress=None) -> dict:
    """ワークフローを投げて完了まで待ち、history の outputs を返す。"""
    return wait(submit(workflow), timeout=timeout, poll=poll, on_progress=on_progress)


def submit(workflow: dict) -> str:
    """ワークフローを投げて prompt_id を返す（待たない）。続けて投げたものはサーバーで続けて実行される。"""
    cid = str(uuid.uuid4())
    try:
        res = _post("/prompt", {"prompt": workflow, "client_id": cid})
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise ComfyError(f"ワークフローが拒否されました: {detail}") from e
    pid = res["prompt_id"]
    print(f"  prompt_id={pid}", flush=True)
    return pid


def wait(pid: str, *, timeout: int = 1800, poll: float = 2.0, on_progress=None) -> dict:
    """prompt_id の完了を待ち、history の outputs を返す。"""
    t0 = time.time()
    fails = 0
    while True:
        if time.time() - t0 > timeout:
            raise ComfyError(f"タイムアウト ({timeout}s) prompt_id={pid}")
        # 2026-09-19: 待っている間の1回の SSL ハンドシェイクのタイムアウトで落ち、サーバーでは生成が続いていた（068 g2）。
        # 一時的な通信エラーは 1分ほど（30回）続けて失敗するまで待ち直す。落ちても h3fetch.py prompt_id で後から受け取れる。
        try:
            hist = _get(f"/history/{pid}")
            fails = 0
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            fails += 1
            if fails > 30:
                raise ComfyError(f"通信エラーが続いた（{e}）。サーバーでは続いている可能性あり: "
                                 f"python h3fetch.py {pid} 作品 タグ") from e
            time.sleep(poll)
            continue
        if pid in hist:
            entry = hist[pid]
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                msgs = [m for m in status.get("messages", []) if m[0] == "execution_error"]
                raise ComfyError(f"実行エラー: {json.dumps(msgs, ensure_ascii=False)[:1500]}")
            return entry.get("outputs", {})
        if on_progress:
            on_progress(time.time() - t0)
        time.sleep(poll)


def collect(outputs: dict, node_id: str) -> list[Path]:
    """SaveImage ノードの出力ファイルの実パスを返す。

    リモート(Colab)の場合はファイルシステムを共有していないので、
    /view から落としてローカルの一時パスを返す。
    """
    paths = []
    for img in outputs.get(node_id, {}).get("images", []):
        if C.is_remote():
            paths.append(fetch_output(img))
        else:
            sub = img.get("subfolder", "")
            paths.append(C.COMFY_OUTPUT / sub / img["filename"] if sub
                         else C.COMFY_OUTPUT / img["filename"])
    return paths


# ---------------------------------------------------------------- リモート入出力
_REMOTE_CACHE = C.ROOT / ".remote_cache"


def fetch_output(info: dict) -> Path:
    """リモート ComfyUI の出力を /view 経由で落としてローカルパスを返す。"""
    import urllib.parse
    q = urllib.parse.urlencode({
        "filename": info["filename"],
        "subfolder": info.get("subfolder", ""),
        "type": info.get("type", "output"),
    })
    _REMOTE_CACHE.mkdir(parents=True, exist_ok=True)
    dst = _REMOTE_CACHE / info["filename"]
    # 2026-09-17: トンネルが切れた瞬間の 065g が 524288 バイト（7コマ）で止まったのに「完了」になった。
    # Content-Length と受け取った量を突き合わせ、足りなければやり直す（3回まで）。
    last = None
    for attempt in range(3):
        try:
            got = 0
            with urllib.request.urlopen(f"{C.COMFY_URL}/view?{q}", timeout=600) as r, open(dst, "wb") as f:
                want = int(r.headers.get("Content-Length") or 0)
                while chunk := r.read(1 << 20):
                    f.write(chunk)
                    got += len(chunk)
            if want and got != want:
                raise IOError(f"ダウンロードが途中で切れました: {info['filename']} {got}/{want} バイト")
            return dst
        except Exception as e:           # 途中切れ・接続断はやり直す
            last = e
            print(f"  出力の取得に失敗（{attempt + 1}回目）: {e}")
            time.sleep(5)
    raise IOError(f"出力を取得できませんでした: {info['filename']} ({last})")


def upload_image(path: Path, name: str | None = None, overwrite: bool = True) -> str:
    """画像を ComfyUI の input/ に送る。LoadImage に渡す名前を返す。

    ローカルならコピーで済むが、リモートでは /upload/image を使う必要がある。
    """
    name = name or Path(path).name
    if not C.is_remote():
        dst_dir = C.COMFY_DIR / "input"
        dst_dir.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(path, dst_dir / name)
        return name

    body, boundary = _multipart(Path(path), name, overwrite)
    req = urllib.request.Request(
        f"{C.COMFY_URL}/upload/image", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        res = json.loads(r.read().decode("utf-8"))
    sub = res.get("subfolder", "")
    return f"{sub}/{res['name']}" if sub else res["name"]


def _multipart(path: Path, name: str, overwrite: bool) -> tuple[bytes, str]:
    boundary = f"----ugoira{uuid.uuid4().hex}"
    data = path.read_bytes()
    parts = [
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{name}"\r\n'
        f"Content-Type: image/png\r\n\r\n".encode("utf-8"),
        data,
        f"\r\n--{boundary}\r\n"
        f'Content-Disposition: form-data; name="overwrite"\r\n\r\n'
        f"{'true' if overwrite else 'false'}\r\n"
        f"--{boundary}--\r\n".encode("utf-8"),
    ]
    return b"".join(parts), boundary
