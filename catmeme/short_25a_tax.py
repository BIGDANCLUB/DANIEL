"""ショート25a：日本vs世界 税金の取られ方（world_short.py・10/24 参考「日本vs海外 税金格差の違い」を1カットずつまねる）。59.9秒。

python3 catmeme/short_25a_tax.py → out/short_25a_tax.mp4
- 10/24 ユーザー指定「口調や素材の使い方をもっと厳密に」：カットの順番・長さの比率・猫の役（左＝私・札なし、右＝「税金」の札）・
  素材の選び方（参考と同じミームがあればそれ、なければ近い動きのもの）・口調（「www」「！！」「、、」）を参考どおりにする。文は書きかえる
- 参考に国旗はないので付けない。集中線もなし（参考どおり）
- 数字（2026年の目安）：日本 所得税の最高45%＋住民税10%＝55%。シンガポール 所得税の最高24%・住民税なし・株の売却益に税金なし・
  銀行の利息も個人は基本非課税・相続税は2008年に廃止
- BGM なし（10/23 ルール）
"""
import os

import world_short as Wd

JP, SG = "bg113_fuji_town", "bg114_singapore_bay"
T = "税金"
K = 59.9 / 64.5   # 参考の長さ（64.5秒）→ 59.9秒


def cuts():
    def s(bg, tag, d, say, cat, **kw):
        return Wd.solo(bg, tag, say, cat, dur=d * K, **kw)

    def t(bg, tag, d, say, left, right, **kw):
        return Wd.talk(bg, tag, say, left, right, dur=d * K, **kw)

    HUH = dict(say_size=230, say_y=680)
    j, g = (JP, "日本"), (SG, "シンガポール")
    return [
        # ---- 日本 ----
        s(*j, 2.0, "所得税に住民税、\nいろいろ取りますwww", "laugh_laughing_dog", label=T, se="don_hit"),
        dict(t(*j, 1.2, "は？", "huh_huh_cat", "laugh_laughing_dog", who="L", rlabel=T, se="question_mark_pop_confused_huh"), **HUH),
        t(*j, 3.4, "所得税＋住民税で\n最高*55%*いただきます", "huh_huh_cat", "glare_disgusted_cat", rlabel=T),
        t(*j, 3.0, "世界でも\n*トップクラス*の高さだよww", "huh_huh_cat", "mock_swinging_cat", rlabel=T),
        t(*j, 3.4, "ほんとに\nどっか行ってくれない？", "call_customer_service_cat", "mock_swinging_cat", who="L", rlabel=T),
        t(*j, 1.8, "でもお前\nそんなに*稼いでない*だろ？", "call_customer_service_cat", "meow_ragdoll_chubby_cat", rlabel=T),
        t(*j, 2.5, "年収*1000万*くらい\nまでの人なら", "call_customer_service_cat", "rizz_cat_rizz", rlabel=T),
        t(*j, 3.4, "世界で見ても\n*そこまで高くない*ぞ", "call_customer_service_cat", "stare_interviewer_cat", rlabel=T),
        t(*j, 3.5, "なんだ疑ってごめん！\n会社員には*やさしい国*だね！！", "stand_real_sheep", "stare_interviewer_cat", who="L",
          rlabel=T),
        s(*j, 3.0, "そのかわり*社会保険料*で\nしっかりいただくけどねwwww", "dance_tabby_standing_cat", label=T),
        dict(s(*j, 2.5, "は？", "huh_huh_cat", se="question_mark_pop_confused_huh"), **HUH),
        # ---- シンガポール ----
        s(*g, 2.5, "所得税の最高は\n*日本の半分*くらいです！！", "eat_pop_cat", label=T, se="don_hit"),
        t(*g, 2.0, "そのぶん*別の税金*で\nがっぽり取るんでしょ？", "talk_orange_white_sitting_cat", "eat_pop_cat", who="L", rlabel=T),
        t(*g, 4.0, "取らないよ！住民税もないよ！\nそのかわり*自分で備えて*ね！", "talk_orange_white_sitting_cat",
          "realize_wet_cat_stare", rlabel=T),
        t(*g, 2.0, "ほかには？", "rage_talking_cat", "realize_wet_cat_stare", who="L", rlabel=T),
        t(*g, 5.0, "株でもうけても*非課税*だよ！！\n銀行の利息にも\n基本かからないよ！", "rage_talking_cat", "dance_wop_cat", rlabel=T),
        t(*g, 3.5, "まじか、、じゃあ\n*相続*のときにがっつり\n取るんでしょ", "blank_black_cat_zoning_out", "dance_wop_cat", who="L", rlabel=T),
        t(*g, 3.0, "相続で税金？？\nそれ*2008年にやめた*よ、、", "blank_black_cat_zoning_out", "confused_i_dont_know_cat", rlabel=T),
        t(*g, 4.0, "親の財産を受けついだだけで\n税金取ったりしないでしょww", "blank_black_cat_zoning_out", "yell_orange_fat_cat",
          rlabel=T, rscale=1.15),
        s(*g, 3.5, "日本と*まるで逆*すぎる！！", "despair_dramatic_kitten"),
        s(*g, 3.0, "そういえば最近\n*お金持ち*がシンガポールに\n引っこすって聞くよね\nなんでだと思う？", "leave_cat_leaves_home", label=T),
        t(*g, 2.5, "……そういうことか", "sad_black_dog", "leave_cat_leaves_home", who="L"),
    ]


if __name__ == "__main__":
    Wd.run(cuts(), Wd.band_vs("{r}日本{w}vs{c}世界", "{y}税金の取られ方ちがいすぎ"),
           os.path.join(Wd.HERE, "out", "short_25a_tax.mp4"), os.path.join(Wd.HERE, "out", "short_25a_tax_preview"))
