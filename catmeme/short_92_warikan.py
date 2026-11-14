"""ショート92：日本vs世界 割り勘（world_short.py・段階でくらべる型・11/12 ユーザー指定：候補7番）。59.9秒。

python3 catmeme/short_92_warikan.py → out/short_92_warikan.mp4
- 11/12 ユーザー指定：1000円の段を削除・1万円の日本「1人3333円」・1円足らない・ウーロン茶・徹夜飲み（両側スマホ猫と踊る猫）を追加・次の日の世界は猫なしで「↓この辺に↓↓寝ている↓」
- 段階ごとに「札だけ → 右の猫 → 左の猫」の3段。段階が上がるほどずれが大きくなる。どの国・人もけなさない
- ライバル3チャンネルと被らないことを確認ずみ（11/6 一覧を取り直して確認）
- 数字・反応は「よくあるイメージ」としての目安（実際の統計ではない）。BGM なし
"""
import os

import world_short as Wd

ST = "bg13_izakaya"
K = 59.9 / 58.5


def cuts():
    out = []
    # (札, 右の猫, 右の説明, 左の猫, 左の説明)
    rows = [
        ('3000円', 'cocky_dj_cat', 'おごるよ', 'think_chin_paw_orange_cat', '1人1000円'),
        ('1万円', 'smug_squint_bicolor_cat', '順番に\nおごる', 'money_counting_orange_cat', '1人\n3333円'),
        ('1万3千円', 'stare_aloha_gray_cat', 'だいたいで\nいい', 'money_counting_cream_cat', '1人\n4333円'),
        ('1円足らない', 'calm_black_face_sheep', '気にしない', 'stare_lying_tabby_cat', '誰が\n払うか\n相談'),
        ('飲まない人', 'listen_dancing_dog', '気にしない', 'sad_looking_away_tabby', '俺ウーロン茶\nだけなのに\n同じ金額…？'),
        ('上司がいる', 'rizz_cat_rizz', '割り勘', 'surprise_big_pupils_cat', '上司が\n多めに払う'),
        ('スマホ送金', 'dance_cute_dog', 'すぐ送る', 'despair_dramatic_kitten', 'あとで送ると\n言って\n1か月'),
        ('徹夜飲み', 'dance_filmed_by_gray_cat', '賭けで\n負けたヤツ\n払いな！', 'dance_filmed_by_gray_cat', '漢気ジャンケン\nいくぞぉぉぉ‼︎\n（UOOOO‼︎）'),
        ('次の日', None, '↓この辺に↓\n↓寝ている↓', 'blank_black_cat_zoning_out', 'まだ\n1円が\n気になる'),
    ]
    for k, (lv, wcat, wcap, jcat, jcap) in enumerate(rows):
        big = k >= len(rows) - 4
        out.append(Wd.split(ST, lv, dur=1.2 * K, se=["explosion_chudoon"] if big else ["pi"]))
        out.append(Wd.split(ST, lv, right=wcat, cap=wcap, cap_side="R", sound="R", dur=2.3 * K, se="don_hit"))
        last = Wd.split(ST, lv, left=jcat, right=wcat, cap=jcap, cap_side="L", sound="L", dur=3.0 * K)
        if wcat is None:   # 11/12 ユーザー指定：猫なしの段は世界の説明も出したまま
            last["cap2"] = wcap
        out.append(last)
    for c in out:
        c.update(blur=9, band_y=0, tag_y=460)
    return out


if __name__ == "__main__":
    Wd.run(cuts(), Wd.rich_band([("{y}日本vs世界", 96, Wd.BLACK, 95), ("{y}割り勘", 90, Wd.BLACK, 245)], 0, 330),
           os.path.join(Wd.HERE, "out", "short_92_warikan.mp4"), os.path.join(Wd.HERE, "out", "short_92_warikan_preview"))
