"""35〜38本目（くらべる長尺4本）の解説画面を書き出す（11/1）。

python3 catmeme/make_parts_35_38.py → catmeme/parts/<名前>/*.png（＋ preview/）
"""
import os

from PIL import Image, ImageDraw

import parts as P

HERE = os.path.dirname(os.path.abspath(__file__))

VIDEOS = {
    "35_tower": dict(
        today="※エレベーター待ちも家賃のうち",
        notice2="※首都圏・同じ6500万円で買った場合で計算",
        title=(["タワマンと一戸建て", "住むだけでいくら違う？"], "管理費・修繕積立金・駐車場・税金\nぜんぶ足してみた"),
        premise=("今回の計算の前提（目安）", ["首都圏・どちらも6500万円で購入", "ローンの返済は同じなのでのぞく",
                                       "タワマン：湾岸・70㎡・駐車場あり", "一戸建て：郊外・4LDK・駐車場は家に",
                                       "30年住んだ場合でくらべる"]),
        points=("今回のポイント", ["住むだけで　タワマン年117万・一戸建て年48万", "タワマンは管理費・修繕積立金・駐車場が大きい",
                                 "一戸建ては修繕を自分で　30年で約800万", "売るならタワマンが取り戻しやすいことも"]),
        ending=["住み続けるか", "売るかで答えが変わる"]),
    "36_chiho": dict(
        today="※雪かきは無料のジム",
        notice2="※30代・ひとり暮らしの会社員で計算",
        title=(["東京と地方移住", "1年でいくら残る？"], "家賃・車・生活費・給料\nぜんぶ足してみた"),
        premise=("今回の計算の前提（目安）", ["30代・ひとり暮らしの会社員", "東京：年収500万・ワンルーム月9万・車なし",
                                       "地方：年収420万・1LDK月5万・軽自動車", "地方は県庁所在地くらいの町"]),
        points=("今回のポイント", ["家賃は地方が年48万安い", "でも車で年40万・光熱費も少し高い",
                                 "給料の差で　東京のほうが年34万多く残る", "東京の給料のまま移住できたら最強"]),
        ending=["移住は", "給料しだい"]),
    "37_hitori": dict(
        today="※ティッシュは自然には増えない",
        notice2="※20代・都市部の会社員で計算",
        title=(["ひとり暮らしと実家暮らし", "1年でいくら違う？"], "家賃・食費・光熱費・家に入れるお金\nぜんぶ足してみた"),
        premise=("今回の計算の前提（目安）", ["20代・都市部の会社員", "ひとり暮らし：家賃 月7.5万",
                                       "実家暮らし：家に入れるお金 月4万", "遊び・交際・通信はどちらも同じ"]),
        points=("今回のポイント", ["ひとり暮らし年195万・実家年98万", "最初の引っ越しで約60万かかる",
                                 "実家は通勤時間や自由がコストになることも", "実家にいる間はしっかり貯めよう"]),
        ending=["実家にいるあいだは", "貯めるチャンス"]),
    "38_hybrid": dict(
        today="※給油の回数が少ないのは正義",
        notice2="※同じくらいの大きさのコンパクトカーで計算",
        title=(["ガソリン車とハイブリッド", "本当に得なのはどっち？"], "車の値段・ガソリン代・税金・売るとき\nぜんぶ足してみた"),
        premise=("今回の計算の前提（目安）", ["同じくらいの大きさのコンパクトカー", "車の値段：ガソリン車200万・ハイブリッド260万",
                                       "燃費：18km/L と 30km/L", "ガソリン170円/L・年8000km走る"]),
        points=("今回のポイント", ["車の値段の差は約60万", "年8000kmなら取り戻すのに約19年",
                                 "売るときはハイブリッドが高く売れやすい", "たくさん走る人ほどハイブリッドが得"]),
        ending=["1年に走る距離で", "えらぼう"]),
}


def notice(today, line2):
    lines = ["※金額は2026年ごろのざっくりの目安です", line2, "※猫は演出です　※背景の一部はAIで作っています", today]
    img = Image.new("RGBA", (P.W, P.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = P.font("black", 64)
    y = (P.H - len(lines) * 100) // 2
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((P.W - w) / 2, y), ln, font=f, fill=(255, 255, 255), stroke_width=7, stroke_fill=(0, 0, 0))
        y += 100
    return img


def main():
    for name, v in VIDEOS.items():
        out = os.path.join(HERE, "parts", name)
        prev = os.path.join(out, "preview")
        os.makedirs(prev, exist_ok=True)
        items = {
            "e00_notice": notice(v["today"], v["notice2"]),
            "e01_title": P.message(v["title"][0], sub=v["title"][1], size=88),
            "e02_premise": P.bullets(v["premise"][0], v["premise"][1], size=50),
            "e07_points": P.bullets(v["points"][0], v["points"][1], size=50),
            "e10_ending": P.message(v["ending"], size=96),
        }
        for n, img in items.items():
            img.save(os.path.join(out, n + ".png"))
            b = P.placeholder_bg("背景")
            b.alpha_composite(img)
            b.convert("RGB").save(os.path.join(prev, n + ".jpg"), quality=85)
        print(name, len(items))


if __name__ == "__main__":
    main()
