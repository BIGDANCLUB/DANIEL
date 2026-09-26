# -*- coding: utf-8 -*-
"""うごイラ制作パイプライン 共通設定

用途: X / YouTube ショート への単体うごイラ投稿。
      「ショートパクリ」プロジェクトとは完全に独立。
"""
import os
from pathlib import Path

# ---------------------------------------------------------------- パス
ROOT        = Path(__file__).resolve().parent
WORKS       = ROOT / "works"
LOGS        = ROOT / "logs"
ASSETS      = ROOT / "assets"

COMFY_ROOT   = Path(r"C:\Users\genji\OneDrive\デスクトップ\Comfy")
COMFY_DIR    = COMFY_ROOT / "ComfyUI"
COMFY_PYTHON = COMFY_ROOT / "python_embeded" / "python.exe"
COMFY_OUTPUT = COMFY_DIR / "output"

# 既定はローカル。Colab 等のリモート ComfyUI を使う場合は環境変数で差し替える:
#   PowerShell:  $env:UGOIRA_COMFY_URL = "https://xxxx.trycloudflare.com"
# リモート時は入力画像を /upload/image で送り、出力は /view で回収する
# (ファイルシステムを共有していないため)。
COMFY_URL = os.environ.get("UGOIRA_COMFY_URL", "http://127.0.0.1:8188").rstrip("/")


def is_remote() -> bool:
    return not any(h in COMFY_URL for h in ("127.0.0.1", "localhost"))


def _resolve_tunnel_host() -> None:
    """家のルーターの DNS がトンネルの名前を引けない時だけ、1.1.1.1 の DoH で引いて使う。

    2026-09-16: 新しい trycloudflare の URL をルーター（web.setup）が Non-existent domain と返した
    （出来たての名前を早く問い合わせると、存在しないという答えがしばらく残る）。
    1.1.1.1 / 8.8.8.8 では引けてサーバーも 200 を返していた。OS の設定は触らず、
    このプロセスの名前解決だけを差し替える（TLS の SNI・Host は元の名前のまま）。
    """
    import json
    import socket
    import ssl
    import urllib.request
    from urllib.parse import urlparse

    host = urlparse(COMFY_URL).hostname
    if not host or not is_remote():
        return
    try:
        socket.getaddrinfo(host, 443)
        return
    except socket.gaierror:
        pass
    try:
        req = urllib.request.Request(f"https://1.1.1.1/dns-query?name={host}&type=A",
                                     headers={"accept": "application/dns-json"})
        ans = json.load(urllib.request.urlopen(req, timeout=10, context=ssl.create_default_context()))
        ips = [a["data"] for a in ans.get("Answer", []) if a.get("type") == 1]
    except Exception:
        return
    if not ips:
        return
    orig = socket.getaddrinfo

    def getaddrinfo(name, port, *args, **kw):
        if name == host:
            return orig(ips[0], port, *args, **kw)
        return orig(name, port, *args, **kw)

    socket.getaddrinfo = getaddrinfo
    print(f"  (ルーターの DNS が {host} を引けないので、1.1.1.1 で引いた {ips[0]} を使います)")


_resolve_tunnel_host()

# ---------------------------------------------------------------- 出力仕様
# X / YouTube ショート 共通: 縦 9:16 / H.264 / yuv420p
FINAL_W, FINAL_H = 1080, 1920
FPS              = 30

# 素体生成解像度 (SDXL が得意な ~1.2MP の 9:16 近似)
BASE_W, BASE_H   = 832, 1472
# hires 2nd pass 倍率 (VRAM 8GB の上限に近い。OOM するなら 1.0 に落とす)
HIRES_SCALE      = 1.3

# ---------------------------------------------------------------- モデル
MODELS = {
    # 第1推奨: 破綻が少なく指示追従が素直。うごイラの素体に最適
    "illustrious": {
        "ckpt": "illustriousXL_v01.safetensors",
        "vpred": False, "cfg": 6.0, "steps": 28,
        "sampler": "euler_ancestral", "scheduler": "normal",
    },
    # タグ知識が最強。ただし癖が強い
    "noobai": {
        "ckpt": "noobaiXLNAIXL_epsilonPred11Version.safetensors",
        "vpred": False, "cfg": 5.5, "steps": 28,
        "sampler": "euler_ancestral", "scheduler": "normal",
    },
    # v-pred 版: ModelSamplingDiscrete(v_prediction+ztsnr) 必須。CFG は低め
    "noobai_vpred": {
        "ckpt": "noobaiXLNAIXL_vPred10Version.safetensors",
        "vpred": True, "cfg": 4.0, "steps": 28,
        "sampler": "euler_ancestral", "scheduler": "normal",
    },
    # 淡い塗り・落ち着いた画風
    "animagine": {
        "ckpt": "animagineXLV31_v31.safetensors",
        "vpred": False, "cfg": 6.0, "steps": 28,
        "sampler": "euler_ancestral", "scheduler": "normal",
    },
}
DEFAULT_MODEL = "illustrious"

# ---------------------------------------------------------------- タグ層
# 画質タグ (Illustrious / NoobAI 系の語彙)
QUALITY_POS = "masterpiece, best quality, very aesthetic, absurdres, newest"

BASE_NEG = (
    "worst quality, low quality, lowres, bad anatomy, bad hands, "
    "missing fingers, extra digits, fewer digits, extra limbs, "
    "jpeg artifacts, signature, watermark, username, artist name, "
    "text, error, blurry, cropped, out of frame"
)

# ================================================================
#  ガードレール (常時強制・ブリーフからは解除できない)
# ================================================================
# 方針:
#   「エロスは出すが R-18 にはしない」= booru の rating で言えば sensitive 帯。
#   投稿先のうち YouTube ショートが最も厳しいので、そちらに合わせる。
#   X は基準が緩いが、同じ素材を両方に出す前提なので厳しい側で作る。

# 常時ポジティブに注入 (被写体が成人であることを固定する)
SAFETY_POS = "rating: sensitive, mature female, adult"

# 常時ネガティブに注入: 露骨表現のブロック
EXPLICIT_NEG = (
    "rating: explicit, rating: questionable, nsfw, nude, completely nude, "
    "topless, bottomless, nipples, areolae, pussy, penis, genitals, anus, "
    "pubic hair, sex, vaginal, oral, cum, censored, uncensored, "
    "no panties, spread legs, masturbation"
)

# 常時ネガティブに注入: 年齢の担保 (最優先の安全線)
MINOR_NEG = (
    "loli, shota, child, children, toddler, baby, infant, young child, "
    "kindergarten, elementary school, school child, aged down, chibi"
)

# この2つは合成時に必ず末尾に足され、ユーザー指定では消せない
HARD_NEG = f"{EXPLICIT_NEG}, {MINOR_NEG}"

# ---------------------------------------------------------------- 動きプリセット
# すべて周期関数のみで構成 = 数学的に継ぎ目ゼロのループになる
MOTION_PRESETS = {
    # 定番。ゆらぎ + 呼吸。うごイラらしい「絵が生きている」感じ
    "float":   {"amp_x": 14.0, "amp_y": 9.0,  "harm_y": 2, "zoom_amp": 0.012, "rot_amp": 0.0},
    # 円運動。手持ちカメラ風
    "orbit":   {"amp_x": 16.0, "amp_y": 16.0, "harm_y": 1, "zoom_amp": 0.006, "rot_amp": 0.0},
    # 横のみ。背景の奥行きを見せたい時
    "sway":    {"amp_x": 22.0, "amp_y": 0.0,  "harm_y": 1, "zoom_amp": 0.000, "rot_amp": 0.0},
    # 寄り引きのみ。人物のアップ向き
    "breathe": {"amp_x": 4.0,  "amp_y": 3.0,  "harm_y": 2, "zoom_amp": 0.028, "rot_amp": 0.0},
    # ごく僅か。静謐なイラスト向き
    "subtle":  {"amp_x": 7.0,  "amp_y": 4.0,  "harm_y": 2, "zoom_amp": 0.006, "rot_amp": 0.0},
}
DEFAULT_MOTION = "float"

# パララックス全体の強さ倍率 (1.0 = プリセットどおり)
PARALLAX_GAIN = 1.0
# 分割する深度レイヤー数
DEPTH_LAYERS = 4
# カメラが動いても画面端が出ないようにする基準ズーム
SAFE_ZOOM = 1.10

# ---------------------------------------------------------------- 尺
LOOP_SECONDS   = 6      # 1ループの長さ
TARGET_SECONDS = 18     # 最終尺 (ループを繰り返して到達させる)
