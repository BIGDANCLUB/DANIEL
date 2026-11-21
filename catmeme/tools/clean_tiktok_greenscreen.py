"""TikTokから保存したグリーンバック素材を、素材フォルダ用にきれいにする。
- 左右・下の黒い帯を切り落とす（緑の部分だけにする）
- TikTokのロゴ・ユーザー名など、小さな白っぽい文字を緑で塗りつぶす（大きな塊＝猫だけ残す）
usage: python3 clean.py in.mp4 out.mp4
"""
import subprocess, sys
import cv2, numpy as np

src, dst = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
frames = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    frames.append(f)
cap.release()
# 緑の範囲（どのフレームでも「はっきり緑」の画素が多い行・列）
def green(f):
    b, g, r = [f[..., i].astype(int) for i in range(3)]
    return (g > 120) & (g > r + 50) & (g > b + 50)
acc = np.zeros(frames[0].shape[:2], np.float32)
for f in frames[::max(1, len(frames) // 12)]:
    acc += green(f)
acc /= len(frames[::max(1, len(frames) // 12)])
# 黒い帯ではない範囲（明るさで判定）。緑が少ない素材（猫が画面いっぱい）でも切れないように
lit = np.mean([(f.max(2) > 30) for f in frames[::max(1, len(frames) // 12)]], 0)
cols = np.where((lit.mean(0) > 0.6) & (acc.mean(0) > 0.05))[0]
rows = np.where(lit[:, cols[0]:cols[-1] + 1].mean(1) > 0.6)[0]
x0, x1, y0, y1 = cols[0] + 4, cols[-1] - 4, rows[0] + 4, rows[-1] - 4
x1 -= (x1 - x0) % 2; y1 -= (y1 - y0) % 2
key = np.median(np.concatenate([f[y0:y1, x0:x1][green(f[y0:y1, x0:x1])] for f in frames[::10]]), 0).astype(np.uint8)
H, W = y1 - y0, x1 - x0
proc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                         "-r", str(fps), "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264",
                         "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", dst],
                        stdin=subprocess.PIPE)
def wipe_text(c):
    """TikTokのロゴ・ユーザー名（白い細い文字）を、出る場所（左上と右下）だけ探して周りの色で埋める。"""
    g = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
    th = cv2.morphologyEx(g, cv2.MORPH_TOPHAT, np.ones((9, 9), np.uint8))
    hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    # 白くて細い（周りより明るい）・色の薄い画素＝文字。小さな塊だけ（毛並みの大きな白は残す）
    m = ((th > 45) & (g > 185) & (hsv[..., 1] < 60)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    small = np.zeros(n, bool)
    small[1:] = (st[1:, cv2.CC_STAT_AREA] < 400) & (st[1:, cv2.CC_STAT_HEIGHT] < 40)
    m = small[lab].astype(np.uint8)
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    return cv2.inpaint(c, m * 255, 5, cv2.INPAINT_TELEA) if m.any() else c


for f in frames:
    c = wipe_text(f[y0:y1, x0:x1].copy())
    fg0 = (~green(c)).astype(np.uint8)
    # 細い線（文字）を消す：太めに削ってから戻し、元の形と重ねる
    core = cv2.morphologyEx(fg0, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23)))
    fg = fg0 & cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg, 8)
    big = st[1:, cv2.CC_STAT_AREA].max() if n > 1 else 0
    keep = np.zeros(n, bool)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= max(0.08 * big, 0.004 * W * H):
            keep[i] = True
    m = keep[lab]
    m = cv2.dilate(m.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    c[~m] = key
    proc.stdin.write(c.tobytes())
proc.stdin.close(); proc.wait()
print(dst, W, H, len(frames))
