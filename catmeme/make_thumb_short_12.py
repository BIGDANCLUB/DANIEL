"""12本目ショートのサムネ（縦 1080x1920・11本目の派手版と同じ作り）。

python3 catmeme/make_thumb_short_12.py → thumbs/short_12_akaihane.png
元事務局長は描かない。猫はニュースに驚く猫と、募金した人（泣くバナナ猫）。
"""
import short_hooks as H
from make_thumb_short_11_dopa import SW, SH, YELLOW, WHITE, RED, BLACK, LIME, outline, stamp, band, save


def main():
    out = H.blank((200, 10, 10))
    H.rays(out, 0.0, cols=((255, 40, 40), (255, 255, 255)), cy=0.5, alpha=0.9)
    H.cat(out, "surprise_big_pupils_cat", 0.6, 270, SH + 300, 900)
    H.cat(out, "sad_banana_cat_cry", 1.0, 820, SH + 60, 820, flip=True)
    H.put(out, outline("赤い羽根募金", 120, WHITE), SW / 2, 230)
    H.put(out, outline("2.5億円", 250, YELLOW), SW / 2, 450)
    H.put(out, stamp("行方不明", 150), SW / 2, 830)
    H.put(out, outline("善意どこ行った！？", 104, RED, WHITE, angle=5), SW / 2, 1065)
    H.put(out, band("通帳も印鑑も1人で管理", BLACK, YELLOW, 66, angle=-4), SW / 2, 1265)
    H.put(out, outline("募金した人", 76, LIME), 830, SH - 110)
    save(out, "short_12_akaihane.png")


if __name__ == "__main__":
    main()
