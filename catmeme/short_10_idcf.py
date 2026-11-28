"""10本目（IDCFクラウドのランサムウェア攻撃）のショート。作りは最新の参考マネ（short_refstyle.py / short_dame_rent.py と同じ）。

python3 catmeme/short_10_idcf.py → out/short_10_idcf.mp4

本編（cuts_10_idcf.py・原稿 scripts/10_idcf.md）のルールをそのまま守る
- 「7時間気づいていない」「7分で暗号化」「ひたすら再起動」は確かめられていない → 最後に「※ハッカーの主張・言われていること」を出す
- 運用の人をバカにしない（深夜に呼び出されて必死な人）。笑いはハッカーの上から目線とリアクション
- 実際のメッセージ画像は、侵入の手順にあたる下の部分を切ったもの（parts/10_idcf/r*.png）だけを使う
- 役名（足元の黄緑の文字）は生き物だけ：ハッカー・運用の人
"""
import os

from PIL import Image

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M

HERE = M.HERE
NAME = "short_10_idcf"
TITLE = ("IDCF、7時間", "気づかずハッカーに報告されるwww")
C, L, Rr = M.C, M.L, M.Rr
LIME = M.LIME
NORA = os.path.join(S.BGM, "野良猫は宇宙を目指した.mp3")
COCOA = os.path.join(S.BGM, "星降る夜のホットココア.mp3")
SERVER, HACKER, PHONE, HOME = "bg24_server_room", "bg23_hacker_room", "bg26_phone_alert", "bg14_home_night"
HK, OPS = "ハッカー", "運用の人"


def shot(name, w=1040):
    """本編の解説画面から、実際のメッセージ画像（手順の部分は切ってある）を読み込んで縦動画の幅に合わせる。"""
    im = Image.open(os.path.join(HERE, "parts", "10_idcf", name + ".png")).convert("RGBA")
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)


def one(bg, say, a, dur, h=1100, **kw):
    """1匹だけ（ニュースを見ている猫のリアクション）。"""
    return M.cut(bg, say, [(a, C, h, kw.pop("flip", False))], dur, **kw)


def vs(say, ops, hack, dur, speaker, **kw):
    """運用の人（左）とハッカー（右）。足元に両方の役名。speaker=0 なら運用の人、1 ならハッカーがしゃべる。"""
    c = M.cut(kw.pop("bg", SERVER), say, [(ops, L, 950, False), (hack, Rr, 1050, True)], dur, label=HK, label_x=830, speaker=speaker,
              col=LIME if speaker == 1 else M.WHITE, **kw)
    c["labels"] = [(OPS, 250)]
    return c


def hk(say, a, dur, **kw):
    """ハッカーのひとり語り。"""
    return M.cut(kw.pop("bg", HACKER), say, [(a, C, 1100, False)], dur, label=HK, label_x=540, col=LIME, **kw)


def pic(say, img, dur, cats, **kw):
    """実際の画像を見せるカット（猫は小さめに下へ）。"""
    c = M.cut(HACKER, say, [(a, x, 700, fl) for a, x, fl in cats], dur, size=kw.pop("size", 90), **kw)
    c["img"], c["img_y"] = shot(img), kw.get("img_y", 1080)
    return c


def cuts():
    return [
        # つかみ
        one(SERVER, "10月7日　午前3時40分\n*495の企業・自治体*の\nクラウドが止まった", "surprise_big_pupils_cat", 3.2, shake=True,
            se=["jan", "explosion_chudoon"], bgm={"file": NORA, "gain": -6}),
        one(SERVER, "原因は\n*ランサムウェア*攻撃", "blank_black_cat_zoning_out", 2.4, size=120, se="pc_warning"),
        pic("管理画面には\nこのメッセージが……", "r1_top", 3.0, [("huh_huh_cat", L, False), ("cocky_dj_cat", Rr, True)],
            se="anime_yugioh_summon_powerful_appearance"),
        hk("YOUR CLOUD\nIS OURS.", "cocky_dj_cat", 2.4, size=130, se="shine_kiraan_maou"),
        hk("東日本リージョン1\n*7分*で暗号化\nしてやった", "cocky_dj_cat", 2.6, se="game_persona5_cutin_dramatic_entrance"),
        # 深夜の現場（再現）
        vs("と、とりあえず\n*再起動*……", "work_typing_cat", "rizz_cat_rizz", 2.4, 0, se="click_tap_select_button"),
        vs("……動かない\nもう一回……", "work_typing_cat", "rizz_cat_rizz", 2.4, 0, se="click_tap_select_button"),
        vs("いや\nメッセージ見て？", "work_typing_cat", "rizz_cat_rizz", 2.2, 1, se="question_mark_pop_confused_huh"),
        vs("再起動……", "work_dog_staring_computer", "rizz_cat_rizz", 1.8, 0, size=140, se="click_tap_select_button"),
        vs("いや\n見て？？", "work_dog_staring_computer", "rizz_cat_rizz", 1.8, 1, size=150, shake=True, se="tsukkomi_bashi"),
        hk("*7時間*たっても\nまだ気づいてない\nとかwww", "laugh_laughing_dog", 2.8, se="game_yoshi_detteiu_so_what_bored"),
        one(HACKER, "ハッカーに\n*報告されてる*！？", "surprise_big_pupils_cat", 2.2, size=130, shake=True, se="explosion_dokaan"),
        pic("「IDCFの運用チームへ\n*そう、お前たちのことだ*」", "r3_noc", 3.2, [("glare_disgusted_cat", L, False), ("laugh_laughing_dog", Rr, True)],
            se="game_mgs_alert"),
        pic("やったことを\n数字で全部*暴露*", "r2_stats", 3.0, [("huh_huh_cat", L, False), ("shady_dancing_man", Rr, False)],
            se="price_display"),
        # 本当にヤバいところ
        one(SERVER, "しかもデータは\n*取り出し・復元が困難*\n（公式の発表）", "sad_banana_cat_cry", 3.0, se="shock_piano",
            bgm={"file": COCOA, "gain": -6, "fade": 0.6}),
        one(SERVER, "戻せるのは\n*自分のバックアップ*\nからだけ", "sad_banana_cat_cry", 2.6, se="pinpon_notice"),
        one(HOME, "クラウドに預けたら\n安心じゃ\nなかったの！？", "despair_dramatic_kitten", 2.8, se="deflate_hyororo"),
        one(PHONE, "JR東日本グループも\n最大約609万件\n*漏えいの可能性*", "realize_wet_cat_stare", 3.0, se="pc_warning"),
        one(SERVER, "深夜に呼び出された\n現場の人\nほんとお疲れさまです", "sleepy_old_memories_cat", 2.8, se="chirin"),
        one(HOME, "バックアップは\n*別の場所にも*！", "eat_pop_cat", 2.6, size=130, se="idea_newtype_01"),
        one(HOME, "※7時間・7分・被害の数字は\nハッカーの主張（確認されていません）\n※再現は演出です", "eat_pop_cat", 2.8, size=60,
            se="pinpon_notice"),
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
