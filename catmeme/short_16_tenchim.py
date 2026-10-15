"""16本目（てんちむ モテフィット裁判）のショート1本目「3億8,000万円が0円に」。作りは short_13_yard.py と同じ。

python3 catmeme/short_16_tenchim.py → out/short_16_tenchim.mp4

本編（cuts_16_tenchim.py・原稿 scripts/16_tenchim.md）のルールをそのまま守る
- 控訴審の結果は本人の報告と報道。判決の理由は推測しない。上告・確定は未確認
- 金額の意味を混ぜない。本人の主張と会社の主張を分ける
- 本人は猫で演じない（ユーザー提供の写真を背景に。猫は顔にかけない）
- 主語の団体（東京地裁・東京高裁・販売元）は札つきの猫で出す
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M

HERE = M.HERE
NAME = "short_16_tenchim"
TITLE = ("てんちむ3.8億円の", "支払い命令が0円に", M.WHITE, M.YELLOW, M.RED)
C, L, Rr = M.C, M.L, M.Rr
PURPLE = os.path.join(S.BGM, "著作権フリー BGM ジャズ 「Purple」（ピアノ、アップテンポ）.mp3")
M.BGS[:0] = [os.path.join(HERE, "backgrounds", d) for d in ("16_tenchim", "15_vambi")]
NEON, FEATHER, EVENT, CHILD, YOUNG = ("bg81_tenchim_neon", "bg82_tenchim_feather", "bg83_tenchim_event", "bg92_tenchim_child",
                                      "bg93_tenchim_young")
COURT, ROOMC, SHELF, MONEY, PAPERS, ADSTUDIO, POST = ("bg84_courthouse", "bg85_courtroom", "bg86_product_shelf",
                                                      "bg87_refund_money", "bg88_contract_papers", "bg89_ad_studio",
                                                      "bg90_phone_post")


def one(bg, say, a, dur, h=1100, **kw):
    return M.cut(bg, say, [(a, C, h, kw.pop("flip", False))], dur, **kw)


def photo_img(name, w=1000):
    """本人の写真を白いふち付きで、縦動画の幅に合わせる。"""
    from PIL import Image, ImageOps
    im = Image.open(M.bg_path(name)).convert("RGB")
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    return ImageOps.expand(im, border=10, fill=(255, 255, 255)).convert("RGBA")


def side(bg, say, a, dur, **kw):
    """本人の写真の場面：写真はセリフの下に枠つきで見せ、猫は右下に小さく（顔にも字幕にもかけない）。"""
    c = M.cut("bg79_timeline", say, [(a, 900, 520, False)], dur, **kw)
    c["img"], c["img_y"] = photo_img(bg), 1380
    return c


def org(bg, who, say, a, dur, **kw):
    return M.cut(bg, say, [(a, C, 1100, False)], dur, label=who, label_x=540, **kw)


def cuts():
    return [
        one(MONEY, "3億8,000万円の\n支払い命令が\n*0円*に！？", "surprise_big_pupils_cat", 2.8, shake=True,
            se=["jan", "explosion_chudoon"], bgm={"file": PURPLE, "gain": -6}),
        side(NEON, "人気YouTuber\n*てんちむ*さん", "huh_huh_cat", 2.2, se="pi"),
        one(SHELF, "ナイトブラ\n「モテフィット」を\n宣伝していた", "think_bike_front_seat_cat", 2.6, se="page_turn_01"),
        one(ADSTUDIO, "2020年\n*豊胸手術*を隠して\n宣伝していたと発覚", "glare_disgusted_cat", 2.8, size=90, se="pc_warning"),
        one(MONEY, "購入者に\n*自腹で返金*", "realize_wet_cat_stare", 2.4, size=120, se="kon"),
        org(PAPERS, "販売元", "でも販売元と\nお金のことで\n*対立*", "work_typing_cat", 2.6, se="page_turn_02"),
        org(ROOMC, "販売元", "販売元は\n*約5億円*を請求", "work_typing_cat", 2.4, size=110, se="buzzer_wrong"),
        org(COURT, "東京地裁", "2024年12月の一審\n*3億8,457万円*の\n支払い命令", "stare_standing_marmot", 3.0, size=86,
            shake=True, se=["explosion_dokaan"]),
        one(COURT, "ほぼ\n会社の言い分どおり", "despair_dramatic_kitten", 2.4, se="chin_bell_failure_sad_ending"),
        one(MONEY, "“2億とか3億とか\nそんなやさしい額じゃない”\n（本人・報道）", "sad_banana_cat_cry", 2.8, size=80, se="tear_drop"),
        org(COURT, "東京高裁", "そして\n2026年10月14日\n*控訴審*", "showoff_gojo_cosplay_cat", 2.4, se="jan"),
        org(COURT, "東京高裁", "一審の支払い命令は\n*すべて取り消し*\n（本人の報告）", "showoff_gojo_cosplay_cat", 2.8, size=90,
            shake=True, se=["explosion_chudoon"]),
        one(COURT, "逆に販売元に\n*約224万円*の\n支払い命令", "yell_orange_fat_cat", 2.8, se="game_coin_get_money_gain_happy"),
        one(COURT, "負けてたのが\n払ってもらう側に！？", "stare_big_eyes_tabby_kitten", 2.4, size=100, se="shock_piano"),
        side(FEATHER, "“諦めずに闘い続けて\n*本当によかった*”\n（本人・報道）", "excited_hodomoe_city_cat", 2.8, size=84,
             se="pinpoon_correct"),
        one(COURT, "ただし理由や\n*確定したか*は\nまだ分からない", "stare_interviewer_cat", 2.8, size=90, se="kon"),
        one(POST, "宣伝の問題が\n消えたわけじゃない", "meow_ragdoll_chubby_cat", 2.6, size=100, se="pi"),
        one(POST, "あなたは\n*どう思う？*", "eat_pop_cat", 2.2, size=130, se="chirin"),
        one(POST, "※控訴審の結果は本人の報告と報道によるものです\n※判決の理由・上告・確定は未確認（10月14日時点）\n"
                  "※本人の主張と会社の主張は分けて紹介しています", "eat_pop_cat", 3.0, size=46, se="pinpon_notice"),
    ]


def main():
    cs = M.keep_going(cuts())
    title = M.title_band(*TITLE)
    for c in cs:
        c["draw"] = M.make_draw(c, title)
    print(f"{len(cs)} カット・{sum(R.cut_dur(c) for c in cs):.1f}秒")
    S.run(cs, title, os.path.join(HERE, "out", NAME + ".mp4"), os.path.join(HERE, "out", NAME + "_preview"))


if __name__ == "__main__":
    main()
