# -*- coding: utf-8 -*-
"""MiniMax-H3 による image-to-video (工程4 ルートD / Colab 実行)

ローカル(RTX 4060 8GB / RAM 16GB)では重みが 42.5GB あって載らないため、
Colab L4 上の ComfyUI をトンネル越しに叩く。接続先は環境変数で切り替える:

    $env:UGOIRA_COMFY_URL = "https://xxxx.trycloudflare.com"

ノード定義は実機の /object_info から採取済み（推測値は使っていない）。

■ WAN 2.2 との決定的な違い
  1. negative conditioning が存在しない。MiniMaxH3ImageToVideo は
     ('positive', 'LATENT') しか返さず、BasicGuider は CFG を持たない。
     → ネガティブプロンプトによる安全層が使えない。
       安全性は「開始画像(SDXL側のガードレール済み)」と「動き記述の内容」
       および「生成後の目視確認」で担保する。
  2. 音声を同時生成する（32kHz ステレオ）。VAE が動画用と音声用で別。
  3. length は 4n+1 ではなく **(length - 5) % 17 == 0**（step=17, min=5）。
"""
from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

import cv2

import config as C
import comfy_client as cc
import parallax


# ---------------------------------------------------------------- モデル
UNET      = "minimax_h3_fl2va_pruned_fp8_scaled.safetensors"
CLIP      = "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"
CLIP_TYPE = "minimax"
VAE_VIDEO = "minimax_h3_video_vae_fp16.safetensors"
VAE_AUDIO = "minimax_h3_audio_vae_fp32.safetensors"
# Turbo LoRA は2系統ある。プリセットで切り替える。
#   drbaph : 公式テンプレートに近い構成。steps 8-10 / res_multistep / strength 1.0
#   lightx2v : Kijai 変換版。steps 4 / er_sde / strength 0.75 で 3.9倍速の報告あり
#              (luta_ai 実測: 1280x736 14秒が 15:57 -> 4:03)
LORA_PRESETS = {
    "drbaph": {
        "file": "minimax_h3_turbo_4step_ckpt500_pruned_comfyui.safetensors",
        "strength": 1.0, "steps": 10,
        "sampler": "res_multistep", "scheduler": "simple",
    },
    "lightx2v": {
        "file": "minimax_h3_fl2v_lightx2v_turbo_4step_v0.1_comfy.safetensors",
        "strength": 0.75, "steps": 4,
        "sampler": "er_sde", "scheduler": "simple",
    },
}
# drbaph の重み(ckpt500_pruned)は 2026-08-25 時点で配布元から消えている。
# 実際に使ってきたのも lightx2v(4step / er_sde / strength 0.75)なのでこちらを既定にする。
DEFAULT_LORA = "lightx2v"

TURBO_LORA = LORA_PRESETS[DEFAULT_LORA]["file"]  # 後方互換

FPS = 24                      # H3 は 24fps 固定
SAMPLER   = "res_multistep"   # 公式テンプレート準拠
SCHEDULER = "simple"

# SigmaShift。LoRA 作者の実ワークフロー(fl_minimax_h3_turbo_lora_example_workflow.json)
# が shift_video=12 / shift_audio=6 を使っている。README も video=12 / audio=4-6。
# audio を低くすると音割れ・ノイズ状の音声・音量の暴走が起きると明記されている。
SHIFT_VIDEO = 12.0
SHIFT_AUDIO = 6.0

# ファイル名は "4step" だが、作者の推奨は 8〜10（ckpt500 なら 6〜8）、
# 実ワークフローは 10。4 で回すと画が崩壊する（2026-08-07 に実測で確認）。
STEPS_TURBO = 10
STEPS_PLAIN = 20

# ComfyUI v0.35.0 の Model Sparse Attention（node_id BlockSparseAttention・PR #16072）。
# attention の大半を省く。長い本ほど効く（294f は1ステップの約7割が attention という推定）。
# 書式: "sol:1.3" … 学習不要。tau が大きいほど省く（1.0で約16%・1.5で約7%を残す）
#       "sla:15"  … 残す割合(%)。SLA で学習した LoRA 専用
# A100(SM80) では Triton 実装で動く見込み（2026-09-16 時点で未実測）。
# カーネルが無い・トークンが min_tokens 未満だと黙って密に戻るので、実行後のログで確かめる。
SPARSE_START = 0.2   # 序盤はこの割合まで密のまま（H3 は序盤を削るのに弱い）


def sparse_inputs(spec: str, start: float = SPARSE_START) -> dict:
    """"sol:1.3" / "sla:15" を BlockSparseAttention の入力に直す。

    DynamicCombo は API では "selection" に方式、"selection.tau" のように
    ドット付きの別キーに中身を入れる（comfy_api/latest/_io.py の finalize_prefix）。
    advanced の入力も必須扱いなので、既定値を全部書く。
    """
    mode, _, val = spec.partition(":")
    mode = {"sol": "sol-attn", "sol-attn": "sol-attn", "sla": "sla"}.get(mode.strip().lower())
    if mode is None:
        raise ValueError(f"--sparse は sol:<tau> か sla:<残す%> で指定してください: {spec}")
    inp = {"selection": mode, "start_percent": start, "end_percent": 1.0,
           "dense_blocks": "", "min_tokens": 12288, "extra_tokens": 256,
           "sink_conditioning": "exact_kv_and_rows", "verbose": True}
    if mode == "sol-attn":
        inp["selection.tau"] = float(val or 1.3)
    else:
        inp["selection.keep_percent"] = float(val or 15.0)
    return inp


def sparse_log_lines(limit: int = 40) -> list[str]:
    """サーバーのログから BlockSparseAttention の行を拾う（疎で走ったか・密に戻った理由・トークン数）。"""
    try:
        raw = cc._get("/internal/logs/raw")
    except Exception as e:
        return [f"(ログを取得できません: {e})"]
    entries = raw.get("entries", []) if isinstance(raw, dict) else []
    lines = [e.get("m", "") if isinstance(e, dict) else str(e) for e in entries]
    hits = [ln.strip() for ln in lines if "BlockSparseAttention" in ln or "sol_attn" in ln]
    return hits[-limit:]

# 9:16 縦。width/height は step=32 なので両方 32 の倍数
V_W, V_H = 768, 1344          # 768/32=24, 1344/32=42
# 公式既定は 1344x768（横）
H_W, H_H = 1344, 768

DEFAULT_LENGTH = 124          # 5 + 17*7 = 124 frames ≈ 5.17秒


# ---------------------------------------------------------------- 尺
def valid_lengths(min_sec: float = 3.0, max_sec: float = 15.2) -> list[tuple[int, float]]:
    """(frames, seconds) の一覧。frames は 5 + 17k のみ許される。"""
    out = []
    k = 0
    while True:
        n = 5 + 17 * k
        s = n / FPS
        if s > max_sec:
            break
        if s >= min_sec:
            out.append((n, s))
        k += 1
    return out


def snap_length(seconds: float) -> int:
    """秒数を最も近い有効フレーム数に丸める。"""
    raw = max(5, round(seconds * FPS))
    k = round((raw - 5) / 17)
    return max(5, 5 + 17 * int(k))


def check_models(lora_preset: str | None = DEFAULT_LORA, sparse: bool = False) -> None:
    """接続先にモデルが揃っているか、投げる前に確かめる。

    Colab のランタイムが作り直されるとモデル 39.5GB が丸ごと消える。
    それに気づかず投げると ComfyUI から巨大な validation エラーが返り、
    原因が読み取りにくい（2026-08-11 に実際に踏んだ）。
    """
    oi = cc.object_info()

    def opts(node: str, field: str) -> list:
        try:
            v = oi[node]["input"]["required"][field][0]
            return v if isinstance(v, list) else []
        except Exception:
            return []

    missing = []
    if UNET not in opts("UNETLoader", "unet_name"):
        missing.append(f"拡散モデル {UNET}")
    if CLIP not in opts("CLIPLoader", "clip_name"):
        missing.append(f"テキストエンコーダ {CLIP}")
    vaes = opts("VAELoader", "vae_name")
    for v in (VAE_VIDEO, VAE_AUDIO):
        if v not in vaes:
            missing.append(f"VAE {v}")
    if lora_preset:
        f = LORA_PRESETS[lora_preset]["file"]
        if f not in opts("LoraLoaderModelOnly", "lora_name"):
            missing.append(f"LoRA {f}")
    if sparse and "BlockSparseAttention" not in oi:
        missing.append("ノード BlockSparseAttention（ComfyUI v0.35.0 以降。Colab の ComfyUI が古い）")

    if missing:
        raise cc.ComfyError(
            "接続先にモデルがありません:\n"
            + "".join(f"  - {m}\n" for m in missing)
            + "  ランタイムが作り直された可能性があります。\n"
            "  Colab のセル1〜5 を順に実行し直してください（モデル約44GB の再取得が必要）。"
        )

    # UNET の読み取り確認は取りやめた。出力ノードの無いワークフローは
    # ComfyUI が prompt_no_outputs で弾くため意味がなく、
    # 破損は SHA256 照合（COLAB_DRIVE.md）で確実に検出できる。


_UNET_OK: str | None = None


def _check_unet_readable() -> None:
    """UNET が実際に読めるかを、投げる前に軽く確かめる。

    存在確認だけでは中身の破損を見抜けない。aria2c は領域を先に確保するので
    虫食いでもファイルサイズは正常に見え、生成に入った直後に UNETLoader が
    UnicodeDecodeError で落ちる（2026-08-16 / 08-24 / 08-25 に3回踏んだ）。
    ここでモデルの読み込みだけ試せば、壊れていれば数十秒で分かる。

    一度通ったら同じ接続先では繰り返さない。
    """
    global _UNET_OK
    url = getattr(C, "COMFY_URL", "")
    if _UNET_OK == url:
        return
    wf = {"1": {"class_type": "UNETLoader",
                "inputs": {"unet_name": UNET, "weight_dtype": "default"}}}
    try:
        cc.run(wf, timeout=420)
    except Exception as e:
        m = str(e)
        if "utf-32" in m or "UnicodeDecodeError" in m or "codec" in m:
            raise cc.ComfyError(
                chr(10).join([
                    "拡散モデルのファイルが壊れています（ヘッダが読めません）。",
                    "  ダウンロードが虫食いです。サイズは正常に見えるので",
                    "  存在確認では分かりません。",
                    "  Colab で colab_dl.py のセルを実行し直してください。",
                    "  壊れたものを削除して取り直し、最後に6件すべて OK になります。",
                ]))
        # 確認そのものが通らない場合（出力の無いワークフローを拒否する等）は素通り
        return
    _UNET_OK = url


def check_length(length: int) -> None:
    if (length - 5) % 17 != 0:
        near = snap_length(length / FPS)
        raise ValueError(
            f"length は (length-5)%17==0 でなければなりません: {length}\n"
            f"  近い有効値: {near} ({near/FPS:.2f}秒)")


# ---------------------------------------------------------------- プロンプト
# H3 は negative を取れないので、ここが唯一の制御点になる。
# 「何が起きるか」を肯定形で書き切ることで逸脱を抑える。
#
# 安全用の固定文と、動きの強さの指定は分けておくこと。
# 混ぜていると「動き激しめ」の指示と "Subtle" が矛盾する（2026-08-07 に発覚）。
SAFETY_SUFFIX = ("The character stays fully clothed and the composition stays "
                 "as in the reference image.")
# 画風や光を途中で変えたい時はこちら。着衣の条件だけ残し、構図の固定を外す。
SAFETY_SUFFIX_DRIFT = "The character stays fully clothed."
MOTION_CALM    = "Subtle, natural, cinematic motion."
MOTION_DYNAMIC = ("Energetic, full-bodied motion with a clear range of movement "
                  "throughout, while the character and framing stay consistent.")

# ユーザーの常設指示（2026-08-08）:
#   - バストの重量感を出す（振れ幅は控えめ。2026-08-21 に弱めた）
#   - 目を閉じることにこだわらず、表情を豊かにする
# 既定で有効。被写体に人物がいない場合など不適切なら --no-chest / --no-expressive で外す。
# 2026-09-11 ユーザー「揺れすぎ、半分くらいに」→ さらに弱めた（服が押さえ、速く動いても落ち着いている）
CHEST_HINT = ("Her chest has natural weight and her clothing holds it close: it "
              "moves only slightly with her body, a small soft settle that follows "
              "her movement, and the fabric over it moves with her. It stays calm "
              "even when she moves quickly.")
EXPRESSIVE_HINT = ("Her eyes are open and alive for most of the video, and her "
                   "gaze and expression change clearly as the moment develops "
                   "— brows, eyes and mouth all move.")


# ---------------------------------------------------------------- 公式書式
# MiniMax 公式の h3-prompt-writing スキル (github.com/MiniMax-AI/MiniMax-H3)
# より。H3 は自由文ではなく「ラベル付きプレーンテキストの3フィールド」を期待する。
#
#   For the target video, at 0.00 seconds ... <Picture 1> ... is fully referenced.
#
#   integrated_multimodal_description: ...
#   overall_soundscape: ...
#   non_diegetic_music: ...
#
# 重要:
#   - overall_soundscape は環境音・動作音・非言語の人の音のみ。1〜4文。
#     台詞・歌・劇中音楽は multimodal_description 側に書く（＝書かなければ鳴らない）
#   - 完全な無音を求める場合のみ overall_soundscape に N/A
#   - non_diegetic_music は BGM。無ければ N/A
#
# 006 で飲み込む音、007 で笑い声が消せなかったのは、音声の指示を映像の記述に
# 混ぜて書いていたため。フィールドを分ければ制御できる。
I2VA_HEADER = ("For the target video, at 0.00 seconds into the target video, "
               "<Picture 1> (from [Shot 1]) is fully referenced.")
# 終点画像もあるとき（fl2va）の公式の1行目（skills/h3-prompt-writing/references/base-en.txt）。
# 2026-09-17 まで fl2va でも I2VA の1行目を送っていた。テキストエンコーダには
# "<Picture 1>: <画像> <Picture 2>: <画像>" の順で2枚とも入っている。
VIDEO_EXT = (".mp4", ".mov", ".webm", ".mkv")
FL2VA_HEADER = ("How the reference pictures align with the target video — Picture 1 (from Shot 1) "
                "aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) "
                "aligns with the {end:.2f}-second mark of the target video.")


def compose_prompt(visual: str, soundscape: str | None = None,
                   music: str | None = None, add_style: bool = True,
                   dynamic: bool = False, legacy: bool = False,
                   chest: bool = True, expressive: bool = True,
                   drift: bool = False, last_at: float | None = None) -> str:
    """公式書式の I2VA（last_at を渡すと FL2VA）プロンプトを組む。

    legacy=True なら旧来の自由文をそのまま返す（比較用）。
    chest / expressive はユーザーの常設指示。既定で有効。
    last_at は終点画像が揃う秒（＝動画の長さ）。公式どおり本文の頭に [Shot 1] を付ける。
    """
    v = visual.strip().rstrip(".")
    if last_at is not None and not legacy and not v.startswith("[Shot"):
        v = f"[Shot 1] {v}"
    extra = []
    if expressive:
        extra.append(EXPRESSIVE_HINT)
    if chest:
        extra.append(CHEST_HINT)
    if extra:
        v = f"{v}. " + " ".join(extra)
        v = v.rstrip(".")
    if add_style:
        hint = MOTION_DYNAMIC if dynamic else MOTION_CALM
        v = f"{v}. {hint} {SAFETY_SUFFIX_DRIFT if drift else SAFETY_SUFFIX}"
    if legacy:
        return v
    s = (soundscape or "N/A").strip()
    m = (music or "N/A").strip()
    header = FL2VA_HEADER.format(end=last_at) if last_at is not None else I2VA_HEADER
    return (f"{header}\n\n"
            f"integrated_multimodal_description: {v}\n\n"
            f"overall_soundscape: {s}\n\n"
            f"non_diegetic_music: {m}")


# ---------------------------------------------------------------- ワークフロー
def build_workflow(
    image_name: str,
    prompt: str,
    *,
    width: int = V_W,
    height: int = V_H,
    length: int = DEFAULT_LENGTH,
    steps: int | None = None,
    seed: int | None = None,
    turbo: bool = True,
    lora_preset: str = DEFAULT_LORA,
    lora_strength: float | None = None,
    sampler: str | None = None,
    sigma_shift: bool = True,
    shift_video: float = SHIFT_VIDEO,
    shift_audio: float = SHIFT_AUDIO,
    clip_device: str = "default",
    weight_dtype: str = "default",
    audio: bool = True,
    tiled_audio: bool = False,
    last_image_name: str | None = None,
    guides: list[tuple[str, int]] | None = None,
    prefix: str = "h3",
    sparse: str | None = None,
    sparse_start: float = SPARSE_START,
) -> tuple[dict, int]:
    import random

    check_length(length)
    if seed is None:
        seed = random.randint(0, 2**31 - 1)

    pre = LORA_PRESETS[lora_preset]
    if steps is None:
        steps = pre["steps"] if turbo else STEPS_PLAIN
    if lora_strength is None:
        lora_strength = pre["strength"]
    if sampler is None:
        sampler = pre["sampler"] if turbo else SAMPLER

    wf: dict[str, dict] = {}

    # --- ローダー ---
    wf["1"] = {"class_type": "UNETLoader",
               "inputs": {"unet_name": UNET, "weight_dtype": weight_dtype}}
    wf["2"] = {"class_type": "CLIPLoader",
               "inputs": {"clip_name": CLIP, "type": CLIP_TYPE, "device": clip_device}}
    wf["3"] = {"class_type": "VAELoader", "inputs": {"vae_name": VAE_VIDEO}}
    wf["4"] = {"class_type": "VAELoader", "inputs": {"vae_name": VAE_AUDIO}}
    wf["5"] = {"class_type": "LoadImage", "inputs": {"image": image_name}}

    # --- MODEL の加工チェーン: UNET -> (LoRA) -> (SigmaShift) ---
    model = ["1", 0]
    if turbo:
        wf["6"] = {"class_type": "LoraLoaderModelOnly",
                   "inputs": {"model": model, "lora_name": pre["file"],
                              "strength_model": lora_strength}}
        model = ["6", 0]
    if sigma_shift:
        wf["7"] = {"class_type": "MiniMaxH3SigmaShift",
                   "inputs": {"model": model, "shift_video": shift_video,
                              "shift_audio": shift_audio}}
        model = ["7", 0]
    if sparse:
        # サンプラの直前（LoRA・SigmaShift の後）に挟む
        wf["7s"] = {"class_type": "BlockSparseAttention",
                    "inputs": {"model": model, **sparse_inputs(sparse, sparse_start)}}
        model = ["7s", 0]

    # --- 条件付け + 初期 latent（1ノードで両方返す） ---
    i2v = {"clip": ["2", 0], "vae": ["3", 0], "prompt": prompt,
           "width": width, "height": height, "length": length,
           "first_frame": ["5", 0]}
    if last_image_name:
        # H3 は fl2va（First-Last frame）なので終点も渡せる。
        # 指定するとその構図に着地させられる。
        wf["5b"] = {"class_type": "LoadImage",
                    "inputs": {"image": last_image_name}}
        i2v["last_frame"] = ["5b", 0]
    wf["8"] = {"class_type": "MiniMaxH3ImageToVideo", "inputs": i2v}

    # --- 途中のコマに画像を固定する（MiniMaxH3AddGuide を数珠つなぎ） ---
    # 始点・終点と同じ仕組み（minimax_keyframes）で、指定したコマ番号の時刻に置かれる。
    # 違いは、テキストエンコーダには画像が入らないこと（始点・終点だけが <Picture n> になる）。
    # 動画（mp4 など）を渡すと、その連続したコマを frame_idx から固定する（5, 22, 39…枚＝17k+5 に切り詰められる）。
    # 前後のクリップの一部を渡せば、動きの続きとして生成できる（064 のつなぎ直しで使用）。
    cond = ["8", 0]
    for i, (name, frame_idx) in enumerate(guides or []):
        if Path(name).suffix.lower() in VIDEO_EXT:
            wf[f"5g{i}v"] = {"class_type": "LoadVideo", "inputs": {"file": name}}
            wf[f"5g{i}"] = {"class_type": "GetVideoComponents", "inputs": {"video": [f"5g{i}v", 0]}}
        else:
            wf[f"5g{i}"] = {"class_type": "LoadImage", "inputs": {"image": name}}
        wf[f"8g{i}"] = {"class_type": "MiniMaxH3AddGuide",
                        "inputs": {"positive": cond, "latent": ["8", 1],
                                   "frame_idx": int(frame_idx), "vae": ["3", 0],
                                   "image": [f"5g{i}", 0]}}
        cond = [f"8g{i}", 0]

    # --- サンプリング（negative なし・CFG なしの BasicGuider） ---
    wf["9"]  = {"class_type": "BasicGuider",
                "inputs": {"model": model, "conditioning": cond}}
    wf["10"] = {"class_type": "KSamplerSelect",
                "inputs": {"sampler_name": sampler}}
    wf["11"] = {"class_type": "BasicScheduler",
                "inputs": {"model": model, "scheduler": pre["scheduler"],
                           "steps": steps, "denoise": 1.0}}
    wf["12"] = {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}}
    wf["13"] = {"class_type": "SamplerCustomAdvanced",
                "inputs": {"noise": ["12", 0], "guider": ["9", 0],
                           "sampler": ["10", 0], "sigmas": ["11", 0],
                           "latent_image": ["8", 1]}}

    # --- デコード: 同じ latent を映像用と音声用の2つの VAE に通す ---
    wf["14"] = {"class_type": "VAEDecode",
                "inputs": {"samples": ["13", 0], "vae": ["3", 0]}}

    create: dict = {"images": ["14", 0], "fps": float(FPS)}
    if audio:
        if tiled_audio:
            wf["15"] = {"class_type": "VAEDecodeAudioTiled",
                        "inputs": {"samples": ["13", 0], "vae": ["4", 0],
                                   "tile_size": 512, "overlap": 64}}
        else:
            wf["15"] = {"class_type": "VAEDecodeAudio",
                        "inputs": {"samples": ["13", 0], "vae": ["4", 0]}}
        create["audio"] = ["15", 0]

    wf["16"] = {"class_type": "CreateVideo", "inputs": create}
    wf["17"] = {"class_type": "SaveVideo",
                "inputs": {"video": ["16", 0], "filename_prefix": f"{prefix}/vid",
                           "format": "auto", "codec": "auto"}}

    return wf, seed


# ---------------------------------------------------------------- 連結生成
# ComfyUI-H3-Motion-Context（NikoDemon80）を使う。
# 前クリップのフレームと音声 latent を次の生成に食わせることで、
# 動きの方向・速度と音声波形が継ぎ目を越えて継続する（単なる連結ではない）。
#
# ノード定義は実機の /object_info から採取済み:
#   MiniMaxH3MotionContext -> (conditioning, trim_frames)
#     required: conditioning, vae, latent, context_frames, context_length,
#               encode_mode, anchor_mode, crop, audio_context_length, audio_mode
#     optional: context_latent, audio_vae, context_audio
#   MiniMaxH3MotionContextTrim -> (images, audio)
#     required: images, trim_frames / optional: audio, fps, match_tail
#   MiniMaxH3MotionContextSaveLatent -> (latent_path)
#   MiniMaxH3MotionContextLoadLatent -> (LATENT)
CTX_LENGTH = 22      # README 推奨。5/22/39 のうち 22 が「ほぼ継ぎ目なし」
CTX_ENCODE = "video"
CTX_ANCHOR = "head"
CTX_AUDIO_MODE = "timeline"
CTX_AUDIO_LENGTH = 22


def build_chain_workflow(
    prev_video_name: str,
    positive_visual: str,
    *,
    soundscape: str | None = None,
    music: str | None = None,
    width: int = V_W,
    height: int = V_H,
    length: int = DEFAULT_LENGTH,
    steps: int | None = None,
    seed: int | None = None,
    lora_preset: str = DEFAULT_LORA,
    lora_strength: float | None = None,
    sampler: str | None = None,
    sigma_shift: bool = True,
    shift_video: float = SHIFT_VIDEO,
    shift_audio: float = SHIFT_AUDIO,
    clip_device: str = "default",
    audio: bool = True,
    context_length: int = CTX_LENGTH,
    audio_context_length: int = CTX_AUDIO_LENGTH,
    ctx_latent_path: str | None = None,
    add_style: bool = True,
    dynamic: bool = False,
    chest: bool = True,
    expressive: bool = True,
    drift: bool = False,
    prefix: str = "h3chain",
) -> tuple[dict, int]:
    """2本目以降のセグメントを、前クリップに接続して生成する。

    prev_video_name: ComfyUI の input/ に置いた前クリップの mp4 ファイル名。
                     LoadVideo -> GetVideoComponents でフレーム束と音声を取り出す。
    """
    import random

    check_length(length)
    if seed is None:
        seed = random.randint(0, 2**31 - 1)
    pre = LORA_PRESETS[lora_preset]
    if steps is None:
        steps = pre["steps"]
    if lora_strength is None:
        lora_strength = pre["strength"]
    if sampler is None:
        sampler = pre["sampler"]
    if not audio:
        soundscape, music = "N/A", "N/A"

    prompt = compose_prompt(positive_visual, soundscape=soundscape, music=music,
                            add_style=add_style, dynamic=dynamic,
                            chest=chest, expressive=expressive, drift=drift)

    wf: dict[str, dict] = {}
    wf["1"] = {"class_type": "UNETLoader",
               "inputs": {"unet_name": UNET, "weight_dtype": "default"}}
    wf["2"] = {"class_type": "CLIPLoader",
               "inputs": {"clip_name": CLIP, "type": CLIP_TYPE, "device": clip_device}}
    wf["3"] = {"class_type": "VAELoader", "inputs": {"vae_name": VAE_VIDEO}}
    wf["4"] = {"class_type": "VAELoader", "inputs": {"vae_name": VAE_AUDIO}}
    # 前クリップを読み込み、フレーム束と音声に分解する
    wf["5"] = {"class_type": "LoadVideo", "inputs": {"file": prev_video_name}}
    wf["22"] = {"class_type": "GetVideoComponents", "inputs": {"video": ["5", 0]}}
    prev_images = ["22", 0]
    prev_audio = ["22", 1]

    model = ["1", 0]
    if steps and lora_preset:
        wf["6"] = {"class_type": "LoraLoaderModelOnly",
                   "inputs": {"model": model, "lora_name": pre["file"],
                              "strength_model": lora_strength}}
        model = ["6", 0]
    if sigma_shift:
        wf["7"] = {"class_type": "MiniMaxH3SigmaShift",
                   "inputs": {"model": model, "shift_video": shift_video,
                              "shift_audio": shift_audio}}
        model = ["7", 0]

    # 通常どおり conditioning + latent を作り、
    wf["8"] = {"class_type": "MiniMaxH3ImageToVideo",
               "inputs": {"clip": ["2", 0], "vae": ["3", 0], "prompt": prompt,
                          "width": width, "height": height, "length": length}}

    # そこに前クリップの文脈を差し込む
    ctx_inputs = {
        "conditioning": ["8", 0], "vae": ["3", 0], "latent": ["8", 1],
        "context_frames": prev_images,
        # context_length だけは文字列の列挙で受ける（'5'/'22'/'39'/'56'）。
        # latent の段数が整数になる長さしか許されないため。
        # encode_mode / anchor_mode / crop / audio_mode はノード更新で廃止された。
        "context_length": str(context_length),
        "audio_context_length": audio_context_length if audio else 0,
    }
    if ctx_latent_path:
        # 別 run で保存した音声 latent があればそちらが上位（README 推奨）
        wf["18"] = {"class_type": "MiniMaxH3MotionContextLoadLatent",
                    "inputs": {"latent_path": ctx_latent_path, "clip_index": 0}}
        ctx_inputs["context_latent"] = ["18", 0]
    elif audio:
        # 既存クリップを延長する場合は latent が無いので音声そのものを渡す（可逆ではない）
        ctx_inputs["context_audio"] = prev_audio
        ctx_inputs["audio_vae"] = ["4", 0]
    wf["9"] = {"class_type": "MiniMaxH3MotionContext", "inputs": ctx_inputs}

    wf["10"] = {"class_type": "BasicGuider",
                "inputs": {"model": model, "conditioning": ["9", 0]}}
    wf["11"] = {"class_type": "KSamplerSelect", "inputs": {"sampler_name": sampler}}
    wf["12"] = {"class_type": "BasicScheduler",
                "inputs": {"model": model, "scheduler": pre["scheduler"],
                           "steps": steps, "denoise": 1.0}}
    wf["13"] = {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}}
    # latent は MotionContext を通した後のものを使う…のではなく、
    # MotionContext は conditioning 側に文脈を埋め込み、
    # 落とすべき先頭フレーム数を trim_frames として返す設計。
    # latent は 8 の出力をそのまま使う。
    wf["14"] = {"class_type": "SamplerCustomAdvanced",
                "inputs": {"noise": ["13", 0], "guider": ["10", 0],
                           "sampler": ["11", 0], "sigmas": ["12", 0],
                           "latent_image": ["8", 1]}}

    wf["15"] = {"class_type": "VAEDecode",
                "inputs": {"samples": ["14", 0], "vae": ["3", 0]}}

    # 接続に使った先頭フレームを落として繋ぎ目を消す
    trim_inputs = {"images": ["15", 0], "trim_frames": ["9", 1],
                   "fps": float(FPS), "match_tail": True}
    if audio:
        wf["16"] = {"class_type": "VAEDecodeAudio",
                    "inputs": {"samples": ["14", 0], "vae": ["4", 0]}}
        trim_inputs["audio"] = ["16", 0]
    wf["17"] = {"class_type": "MiniMaxH3MotionContextTrim", "inputs": trim_inputs}

    create = {"images": ["17", 0], "fps": float(FPS)}
    if audio:
        create["audio"] = ["17", 1]
    wf["19"] = {"class_type": "CreateVideo", "inputs": create}
    wf["20"] = {"class_type": "SaveVideo",
                "inputs": {"video": ["19", 0], "filename_prefix": f"{prefix}/seg",
                           "format": "auto", "codec": "auto"}}

    # 次セグメント用に音声 latent を保存しておく
    wf["21"] = {"class_type": "MiniMaxH3MotionContextSaveLatent",
                "inputs": {"latent": ["14", 0],
                           "filename_prefix": f"{prefix}/ctx", "clip_index": 0}}
    return wf, seed


def stage_prev_video(video: Path, tag: str, tail_seconds: float = 2.0,
                     width: int | None = None, height: int | None = None) -> str:
    """前クリップの末尾だけを切り出して ComfyUI の input/ へ置く。

    全長を送ると転送も GetVideoComponents のデコードも無駄に重い。
    MotionContext が実際に見るのは末尾 context_length フレームだけなので、
    余裕をみて末尾 2 秒程度あれば足りる。
    """
    tmp = C.ROOT / ".stage"
    tmp.mkdir(parents=True, exist_ok=True)
    out = tmp / f"ctx_{tag}.mp4"

    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(video)], capture_output=True).stdout.decode().strip())
    ss = max(0.0, dur - tail_seconds)

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{ss:.3f}", "-i", str(video)]
    if width and height:
        cmd += ["-vf", f"scale={width}:{height}"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", str(out)]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"前クリップの切り出し失敗:\n"
                           f"{r.stderr.decode('utf-8','replace')}")
    return cc.upload_image(out, out.name)


# ---------------------------------------------------------------- 実行
def collect_video(outputs: dict, node_id: str = "17") -> list[Path]:
    """SaveVideo の出力を回収する（リモートなら /view 経由で落ちてくる）。"""
    out = []
    node = outputs.get(node_id, {})
    for key in ("videos", "images", "gifs", "audio"):
        for v in node.get(key, []):
            if C.is_remote():
                out.append(cc.fetch_output(v))
            else:
                sub = v.get("subfolder", "")
                base = C.COMFY_OUTPUT / sub if sub else C.COMFY_OUTPUT
                out.append(base / v["filename"])
    return out


def stage_start_image(src: Path, width: int, height: int, tag: str) -> str:
    img = parallax.imread_u(src, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"開始画像が読めません: {src}")
    img = parallax.fit_cover(img, width, height)

    tmp = C.ROOT / ".stage"
    tmp.mkdir(parents=True, exist_ok=True)
    name = f"h3_start_{tag}.png"
    if not parallax.imwrite_u(tmp / name, img):
        raise RuntimeError(f"開始画像の書き出しに失敗: {tmp / name}")
    return _upload_resilient(tmp / name, img)


# トンネルが細っているとき、大きな本文の POST が Cloudflare の 100秒制限に
# 引っかかって HTTP 524 で落ちる。2026-09-11 の実測では、往復に固定で40秒
# かかる状態で 273KB は通り 486KB は落ちた（トンネルを張り直したら 0.14秒に
# 戻ったので、これはトンネル側の劣化であって回線の細さではない）。
# 健全なときに画質を落とす理由はないので、まず PNG のまま送り、524 で
# 落ちたときだけ JPEG に縮めて送り直す。
UPLOAD_MAX = 280_000


def _upload_resilient(path: Path, img) -> str:
    """PNG をそのまま送る。細いトンネルで弾かれたときだけ縮めて送り直す。"""
    import urllib.error
    try:
        return cc.upload_image(path, path.name)
    except urllib.error.HTTPError as e:
        if e.code != 524:
            raise
        print(f"  アップロードがトンネルで弾かれました (HTTP 524): "
              f"{path.name} {path.stat().st_size / 1024:.0f}KB")
    for q in (92, 86, 80, 72, 64):
        jpg = path.with_suffix(".jpg")
        if not parallax.imwrite_u(jpg, img, [cv2.IMWRITE_JPEG_QUALITY, q,
                                             cv2.IMWRITE_JPEG_SAMPLING_FACTOR,
                                             cv2.IMWRITE_JPEG_SAMPLING_FACTOR_444]):
            break
        if jpg.stat().st_size <= UPLOAD_MAX:
            print(f"  縮小して再送: {jpg.name} "
                  f"{jpg.stat().st_size / 1024:.0f}KB (JPEG 品質{q})")
            return cc.upload_image(jpg, jpg.name)
    raise RuntimeError(f"アップロードに収まる大きさにできません: {path}")


def render(
    work_dir: Path,
    motion_prompt: str,
    *,
    soundscape: str | None = None,
    music: str | None = None,
    legacy_prompt: bool = False,
    chest: bool = True,
    expressive: bool = True,
    width: int = V_W,
    height: int = V_H,
    length: int = DEFAULT_LENGTH,
    seconds: float | None = None,
    steps: int | None = None,
    seed: int | None = None,
    turbo: bool = True,
    lora_preset: str = DEFAULT_LORA,
    sampler: str | None = None,
    sigma_shift: bool = True,
    shift_video: float = SHIFT_VIDEO,
    shift_audio: float = SHIFT_AUDIO,
    lora_strength: float | None = None,
    clip_device: str = "default",
    audio: bool = True,
    upscale: bool = True,
    add_style: bool = True,
    dynamic: bool = False,
    drift: bool = False,
    tag: str = "",
    timeout: int = 5400,
    verbose: bool = True,
    sparse: str | None = None,
    sparse_start: float = SPARSE_START,
    guides: list[tuple[Path, int]] | None = None,
) -> Path:
    """works/NNN/image.png を起点に H3 で動画化する。

    guides は途中のコマに固定する画像と、そのコマ番号（0 始まり・負数は末尾から）の組。
    """
    src = work_dir / "image.png"
    if not src.exists():
        raise FileNotFoundError(f"image.png がありません。先に pick してください: {work_dir}")

    if seconds is not None:
        length = snap_length(seconds)
    check_length(length)

    # 画像アップロードの前に疎通を確かめる。トンネルが切れていると
    # multipart POST が 530 で落ちてスタックトレースになるだけで原因が分からない。
    cc.check_reachable()
    check_models(lora_preset if turbo else None, sparse=bool(sparse))

    # 音声を出さない指定なら soundscape / music とも N/A に倒す
    if not audio:
        soundscape, music = "N/A", "N/A"
    # image_last.png があれば終点フレームとして渡す（H3 は fl2va）。1行目も公式の FL2VA 形にする。
    last = work_dir / "image_last.png"
    prompt = compose_prompt(motion_prompt, soundscape=soundscape, music=music,
                            add_style=add_style, dynamic=dynamic,
                            legacy=legacy_prompt, chest=chest,
                            expressive=expressive, drift=drift,
                            last_at=(length / FPS) if last.exists() else None)
    name = stage_start_image(src, width, height, work_dir.name)

    last_name = None
    if last.exists():
        last_name = stage_start_image(last, width, height,
                                      work_dir.name + "_last")
        if verbose:
            print(f"  終点フレーム: {last.name} を使用")

    guide_names = []
    for gpath, frame_idx in guides or []:
        gpath = Path(gpath)
        if not gpath.is_absolute():
            gpath = work_dir / gpath
        idx = frame_idx if frame_idx >= 0 else length + frame_idx
        if not 0 <= idx < length:
            raise ValueError(f"途中の画像のコマ番号が範囲外です: {gpath.name}@{frame_idx}（0〜{length - 1}）")
        # 同じフォルダの別ジョブと名前がぶつからないよう、元の画像名とコマ番号を入れる
        if gpath.suffix.lower() in VIDEO_EXT:
            # 動画は生成と同じ大きさに作ってから渡すこと（ここでは縮めない）
            gname = cc.upload_image(gpath, f"h3_guide_{work_dir.name}_g{idx}_{gpath.stem}{gpath.suffix}")
        else:
            gname = stage_start_image(gpath, width, height, f"{work_dir.name}_g{idx}_{gpath.stem}")
        guide_names.append((gname, idx))
        if verbose:
            print(f"  途中の{'動画' if gpath.suffix.lower() in VIDEO_EXT else '画像'}: {gpath.name} → "
                  f"{idx}枚目（{idx / FPS:.2f}秒）から")

    cc.wait_for_server(300)
    # 2026-09-19: 映像と音声を1本の SaveVideo でまとめて書くと、H3 の音声に NaN/Inf が混じったとき AAC の書き出しが
    # 「avcodec_send_frame() returned 22」で落ち、映像まで失われた（060n g1・068 g2）。
    # → 映像だけを書く依頼と、音声だけを書く依頼（SaveAudio・FLAC）を続けて投げる。2本目は 1本目のサンプリング結果が
    #   キャッシュに残っているので、音声のデコードと保存だけで終わる。音声が壊れていても映像は残る。手元で合わせる。
    wf, seed = build_workflow(
        name, prompt, width=width, height=height, length=length,
        steps=steps, seed=seed, turbo=turbo, sigma_shift=sigma_shift,
        shift_video=shift_video, shift_audio=shift_audio,
        lora_preset=lora_preset, lora_strength=lora_strength, sampler=sampler,
        clip_device=clip_device, audio=False, last_image_name=last_name,
        guides=guide_names,
        prefix=f"h3_{work_dir.name}", sparse=sparse, sparse_start=sparse_start)
    wf_audio = None
    if audio:
        wf_audio = {k: v for k, v in wf.items() if k not in ("14", "16", "17")}
        wf_audio["15"] = {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["13", 0], "vae": ["4", 0]}}
        wf_audio["18"] = {"class_type": "SaveAudio",
                          "inputs": {"audio": ["15", 0], "filename_prefix": f"h3_{work_dir.name}/aud"}}

    (work_dir / "h3_workflow_api.json").write_text(
        __import__("json").dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")

    if verbose:
        print(f"  接続先 : {C.COMFY_URL}")
        pre = LORA_PRESETS[lora_preset]
        print(f"  {width}x{height} / {length}frames = {length/FPS:.2f}s @ {FPS}fps")
        print(f"  LoRA  : {lora_preset} ({pre['file'][:52]})")
        print(f"  steps={steps or pre['steps']} strength={lora_strength or pre['strength']} "
              f"sampler={sampler or pre['sampler']} audio={audio} seed={seed}")
        print(f"  shift : {'video=%.2f audio=%.2f' % (shift_video, shift_audio) if sigma_shift else 'なし'}")
        print(f"  sparse: {sparse + ' / start %.2f' % sparse_start if sparse else 'なし（密）'}")
        print(f"  書式  : {'旧(自由文)' if legacy_prompt else '公式3フィールド'}")
        for ln in prompt.split("\n"):
            if ln.strip():
                print(f"    {ln[:150]}")

    pid_v = cc.submit(wf)
    pid_a = cc.submit(wf_audio) if wf_audio else None
    outs = cc.wait(pid_v, timeout=timeout,
                   on_progress=(lambda s: print(f"  ...{s:.0f}s", flush=True))
                   if verbose else None)

    vids = collect_video(outs)
    if not vids:
        raise RuntimeError(f"動画が出力されませんでした。outputs keys={list(outs)}")
    aud = None
    if pid_a:
        try:
            outs_a = cc.wait(pid_a, timeout=1800)
            files = outs_a.get("18", {}).get("audio", [])
            aud = cc.fetch_output(files[0]) if files else None
        except Exception as e:                    # 音声だけ壊れても映像は使う
            print(f"  音声の取り出しに失敗（映像だけ保存する）: {str(e)[:300]}")
    if aud is not None:
        muxed = vids[0].with_name(vids[0].stem + "_av.mp4")
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vids[0]), "-i", str(aud), "-map", "0:v", "-map", "1:a",
                            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(muxed)],
                           capture_output=True, text=True)
        if r.returncode == 0:
            vids = [muxed]
        else:
            print(f"  音声を合わせられなかった（映像だけ保存する）: {r.stderr[-300:]}")

    if sparse and verbose:
        # 疎で走ったか、密に戻ったならその理由（トークン数・カーネル無し等）を必ず見る
        print("  sparse のログ:")
        for ln in sparse_log_lines() or ["(BlockSparseAttention の行が無い)"]:
            print(f"    {ln[:200]}")

    suffix = f"_h3{('_' + tag) if tag else ''}"
    dst = work_dir / f"{work_dir.name}{suffix}.mp4"
    shutil.copy2(vids[0], dst)

    # 2026-09-20: 068 g2 は計算が NaN になり、全コマ画素値 0（真っ黒）の動画が「完了」として届いた。受け取った時点で知らせる。
    try:
        probe = subprocess.run(["ffmpeg", "-v", "error", "-i", str(dst), "-vf", "select=not(mod(n\\,48)),scale=64:96",
                                "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
        if probe and max(probe) < 3:
            print("  警告: 映像が真っ黒です（サンプリングが NaN で壊れた可能性。seed や固定の置き方を変えて作り直す）")
    except Exception:
        pass

    if upscale:
        dst = _to_final(dst, audio=audio)
    return dst


def render_chain(
    work_dir: Path,
    prev_video: Path,
    motion_prompt: str,
    *,
    soundscape: str | None = None,
    music: str | None = None,
    width: int = V_W,
    height: int = V_H,
    length: int = DEFAULT_LENGTH,
    seconds: float | None = None,
    steps: int | None = None,
    seed: int | None = None,
    lora_preset: str = DEFAULT_LORA,
    sampler: str | None = None,
    clip_device: str = "default",
    audio: bool = True,
    dynamic: bool = False,
    chest: bool = True,
    expressive: bool = True,
    context_length: int = CTX_LENGTH,
    drift: bool = False,
    tag: str = "",
    timeout: int = 7200,
    verbose: bool = True,
) -> Path:
    """既存クリップの続きを生成する（動きと音が継続する）。"""
    if not prev_video.exists():
        raise FileNotFoundError(f"前クリップがありません: {prev_video}")
    if seconds is not None:
        length = snap_length(seconds)
    check_length(length)

    cc.check_reachable()
    name = stage_prev_video(prev_video, f"{work_dir.name}{tag}", width=width, height=height)

    wf, seed = build_chain_workflow(
        name, motion_prompt, soundscape=soundscape, music=music,
        width=width, height=height, length=length, steps=steps, seed=seed,
        lora_preset=lora_preset, sampler=sampler, clip_device=clip_device,
        audio=audio, dynamic=dynamic, context_length=context_length,
        chest=chest, expressive=expressive, drift=drift,
        prefix=f"h3chain_{work_dir.name}")

    (work_dir / "h3_chain_workflow.json").write_text(
        __import__("json").dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")

    if verbose:
        pre = LORA_PRESETS[lora_preset]
        print(f"  前クリップ: {prev_video.name}")
        print(f"  {width}x{height} / {length}frames = {length/FPS:.2f}s")
        print(f"  LoRA={lora_preset} steps={steps or pre['steps']} "
              f"sampler={sampler or pre['sampler']} audio={audio} seed={seed}")
        print(f"  context_length={context_length} encode={CTX_ENCODE} "
              f"anchor={CTX_ANCHOR} audio_mode={CTX_AUDIO_MODE}")

    outs = cc.run(wf, timeout=timeout,
                  on_progress=(lambda s: print(f"  ...{s:.0f}s", flush=True))
                  if verbose else None)
    vids = collect_video(outs, "20")
    if not vids:
        raise RuntimeError(f"動画が出力されませんでした: {list(outs)}")

    seg = work_dir / f"{work_dir.name}_seg{('_' + tag) if tag else ''}.mp4"
    shutil.copy2(vids[0], seg)
    return seg


def concat_segments(parts: list[Path], out: Path) -> Path:
    """セグメントを連結する。MotionContextTrim 済みなので単純結合でよい。"""
    lst = out.with_suffix(".txt")
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    r = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(lst), "-c:v", "libx264", "-preset", "slow", "-crf", "16",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", str(out)],
        capture_output=True)
    lst.unlink(missing_ok=True)
    if r.returncode != 0:
        raise RuntimeError(f"連結失敗:\n{r.stderr.decode('utf-8','replace')}")
    return out


def _to_final(src: Path, audio: bool = True) -> Path:
    """投稿用に 1080x1920 へ引き伸ばし、音声を配信標準へ正規化する。

    H3 の音声出力レベルは題材によって大きくばらつく（実測で RMS 0.0742 と
    0.0073 = 10倍差）。毎回 loudnorm を通さないと視聴時に音量差が出る。
    """
    out = src.with_name(src.stem + "_1080.mp4")

    # 比率を無視して引き伸ばすと、9:16 でない素材が横に潰れる。
    # 864x1152(3:4) を 1080x1920 に入れると横幅が正しい寸法の75%になり、
    # 顔も体も細長くなった（038 で発覚）。比率は保ち、はみ出す分を切る。
    # 横長の素材は縦に切ってしまうので、そのまま横長のまま仕上げる。
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height",
                        "-of", "csv=p=0:s=x", str(src)],
                       capture_output=True, text=True).stdout.strip()
    sw, sh = (int(v) for v in p.split("x"))
    if sw > sh:
        tw, th = C.FINAL_H, C.FINAL_W
    else:
        tw, th = C.FINAL_W, C.FINAL_H
    vf = (f"scale={tw}:{th}:force_original_aspect_ratio=increase:flags=lanczos,"
          f"crop={tw}:{th}")

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
           "-vf", vf,
           "-c:v", "libx264", "-preset", "slow", "-crf", "16",
           "-pix_fmt", "yuv420p"]
    if audio:
        cmd += ["-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k"]
    else:
        cmd += ["-an"]
    cmd += ["-movflags", "+faststart", str(out)]

    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"アップスケール失敗:\n{r.stderr.decode('utf-8','replace')}")
    return out
