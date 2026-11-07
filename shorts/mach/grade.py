"""レンダリングした絵に、参考動画の「夕日のもや・光のにじみ・暖色の色味」を足す。"""
import numpy as np
from PIL import Image, ImageFilter


def find_sun(img):
    a = np.asarray(img.convert("L"), dtype=np.float32)
    h = a.shape[0]
    top = a[: int(h * 0.75)]
    ys, xs = np.where(top >= top.max() - 3)
    return int(xs.mean()), int(ys.mean())


def grade(img, sun=None, glow=1.0, warmth=1.0, haze=0.35):
    img = img.convert("RGB")
    w, h = img.size
    a = np.asarray(img, dtype=np.float32) / 255.0
    sx, sy = sun if sun else find_sun(img)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - sx) / w) ** 2 + ((yy - sy) / w) ** 2)
    # 太陽のまわりの大きなにじみ（黄→オレンジ）
    core = np.exp(-(d / 0.07) ** 2)
    wide = np.exp(-(d / 0.45) ** 2)
    glow_col = np.array([1.0, 0.78, 0.45])
    a = a + glow * (0.6 * core[..., None] * np.array([1.0, 0.93, 0.75]) + 0.32 * wide[..., None] * glow_col)
    # 地平線のもや（太陽の高さで一番濃く、上下に薄く）
    band = np.exp(-((yy - sy) / (h * 0.18)) ** 2)
    a = a * (1 - haze * band[..., None]) + haze * band[..., None] * np.array([1.0, 0.72, 0.42])
    # 全体を暖色に（参考の色味）
    a = a * np.array([1.0 + 0.06 * warmth, 1.0, 1.0 - 0.12 * warmth])
    # 明るい所の光のにじみ（ブルーム）
    out = Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))
    bright = out.point(lambda v: max(0, v - 200) * 3)
    bloom = bright.filter(ImageFilter.GaussianBlur(w * 0.03))
    b = np.asarray(bloom, dtype=np.float32) / 255.0
    a = np.clip(a + 0.45 * b, 0, 1)
    # 周辺を少し暗く
    vig = 1 - 0.28 * np.clip(((xx - w / 2) / (w * 0.75)) ** 2 + ((yy - h / 2) / (h * 0.75)) ** 2, 0, 1)
    a = a * vig[..., None]
    return Image.fromarray((a * 255).astype(np.uint8))
