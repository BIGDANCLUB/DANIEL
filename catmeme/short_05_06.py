"""5本目（ペスト研究所）のショート2本と、6本目（絶望ライン工）のショート1本（縦 1080x1920・45〜58秒）。

python3 catmeme/short_05_06.py 5a  → out/short_05a_what.mp4（研究所で何が起きた？ 結論から）
python3 catmeme/short_05_06.py 5b  → out/short_05b_cure.mp4（ペストって今も治るの？）
python3 catmeme/short_05_06.py 6   → out/short_06_zetsubou.mp4（実は既婚で炎上…なにが問題だった？）
画面の作りは short_04_leak.py と同じ（上：話題の札つきタイトル帯／中：場面かパネル／下：大きな字幕）。

注意：5本目は亡くなった方を笑いにしない・名前を出さない・猫で演じない。「当局はペストを確認していない」を必ず入れる。
6本目は本人・家族をバカにしない。本人の言葉は報道の要旨だけ（本人役は落ち着いた猫）。
"""
import os
import sys

import short_03_kodomo_nisa as S
import short_04_leak as Q

HERE = S.HERE
PURPLE, NORA, COCOA = Q.PURPLE, Q.NORA, Q.COCOA
KAMI = os.path.join(S.BGM, "神の怒り.mp3")
NEWS, SAGE = S.NEWS, S.SAGE
NET, HONNIN = (120, 50, 170), (35, 140, 65)
YELLOW, RED, NAVY = S.YELLOW, S.RED, S.NAVY
one, two, panel, items, big, flow = Q.one, Q.two, Q.panel, Q.items, Q.big, Q.flow


# ---- 5A：研究所で何が起きた？（結論から） ----
def cuts_5a():
    return [
        one("bg11_tsukuba", "surprise_big_pupils_cat", "ニュース猫", NEWS, "ペスト研究所で\n職員が死亡！？", cap_col=RED,
            dur=2.8, fx=["lines", "shake"], se=["jan", "doon_heavy"], bgm={"file": PURPLE, "gain": -6}),
        panel(big("先に結論（10月7日時点）", "ペストは\n検出されず", col=NAVY, note="ロシア当局の発表"), "当局は\nペストを否定",
              dur=3.4, se="pinpon_notice"),
        two("bg02_room", "huh_huh_cat", "eat_pop_cat", "え、じゃあ\nなんで騒ぎに？", who="L", dur=2.4, se="question_hatena_maou"),
        panel(items("何が起きたか", ["9月末　職員（28歳）が体調をくずす", "10/2　重い肺炎で亡くなる", "接触した約200人を隔離・観察",
                                     "当局「原因不明の肺炎」"]), "時系列で見ると", dur=4.2, se="card_flip"),
        two("bg11_tsukuba", "weird_meowing_cat", "think_bike_front_seat_cat", "現地メディアは\n「肺ペストの可能性」\nと報道", who="R",
            dur=3.0, se="doon_movie", bgm={"file": NORA, "gain": -6}),
        two("bg18_backyard", "surprise_big_pupils_cat", "think_bike_front_seat_cat", "「試験管を割った」\nという話も\n（確認されていない）",
            who="L", dur=3.0, fx=["lines"], se="glass_break_01"),
        panel(items("報道と発表が食い違う", ["報道：肺ペストの可能性", "当局：原因不明の肺炎", "報道：約200人を隔離",
                                         "当局：感染者なし→ほぼ解除"]), "情報が\n食い違った", cap_col=RED, dur=4.4, se="buzzer_wrong"),
        two("bg02_room", "spin_spinning_cat", "eat_pop_cat", "情報が二転三転して\nもうわからん", who="L", dur=2.6, se="spring_byoin"),
        panel(items("その後わかったこと", ["約5,000件の検査で　危険な病原体なし", "隔離された人の約9割が解除",
                                         "接触者に感染者なし（当局）"], note="WHOは死因についてさらに情報を求めている"),
              "ひとまず\n広がってはいない", dur=4.4, se="pinpoon_correct"),
        two("bg09_sns", "glare_disgusted_cat", "calm_black_face_sheep", "研究所で\n隔離ってなると\nコロナを思い出す", who="L", dur=2.8,
            se="kon"),
        two("bg09_sns", "glare_disgusted_cat", "calm_black_face_sheep", "研究所から漏れた・\n隠してる…などの声は\nどれも確認されていない",
            who="R", dur=3.4, se="pinpon_notice"),
        two("bg02_room", "sleepy_sleepy_cat", "think_bike_front_seat_cat", "怖がりすぎず\n続報は公式の発表で\n確認な", who="R",
            dur=3.0, se="tv_professional_poon", bgm={"file": COCOA, "gain": -6, "fade": 0.8}),
        one("bg02_room", "sleepy_old_memories_cat", "博識な猫", SAGE, "亡くなった方の\nご冥福を\nお祈りします", dur=3.0, se="chiin_01"),
        one("bg03_blackboard", "wave_waving_cat", "ニュース猫", NEWS, "ペストってどんな病気？\n本編で解説！", cap_col=YELLOW,
            h=760, dur=3.0, se="chirin"),
    ]


# ---- 5B：ペストって今も治るの？ ----
def cuts_5b():
    return [
        one("bg11_tsukuba", "weird_meowing_cat", "ニュース猫", NEWS, "ペストって\n歴史の教科書の\nあれ！？", cap_col=RED, dur=2.8,
            fx=["lines", "shake"], se=["jan", "question_hatena_maou"], bgm={"file": NORA, "gain": -6}),
        panel(items("そもそも「ペスト」って？", ["細菌（ペスト菌）がおこす感染症", "ネズミ → ノミ → 人", "肺ペストは　せき・飛沫で人へ"]),
              "細菌の感染症", dur=4.0, se="page_turn_01"),
        two("bg02_room", "huh_huh_cat", "eat_pop_cat", "ネズミとノミ……", who="L", dur=2.2, se="boing_01"),
        panel(items("ペストの3つの種類", ["腺ペスト：リンパ節が腫れる", "敗血症ペスト：血液に菌が回る", "肺ペスト：人から人へうつる"]),
              "種類は3つ", dur=4.0, se="card_flip"),
        panel(big("黒死病（14世紀）", "ヨーロッパの\n3分の1〜半分が\n亡くなったとされる", note="当時は抗生物質がなかった"),
              "歴史に残る\n大流行", cap_col=RED, dur=4.0, se="doon_heavy", bgm={"file": KAMI, "gain": -12}),
        one("bg10_kyoto", "surprise_big_pupils_cat", "ニュース猫", NEWS, "半分！？\nスケールがバグってる", cap_col=RED, dur=2.4,
            fx=["lines", "shake"], se="explosion_dokaan"),
        two("bg02_room", "spin_spinning_cat", "think_bike_front_seat_cat", "でも今は\n早めに抗生物質で\n治療すれば治る", who="R",
            dur=3.2, se="pinpoon_correct", bgm={"file": COCOA, "gain": -6}),
        two("bg02_room", "spin_spinning_cat", "think_bike_front_seat_cat", "治るのか！\nちょっと安心", who="L", dur=2.2, se="pikon"),
        panel(items("今もペストはある？", ["世界では毎年患者が出ている", "マダガスカル・コンゴ民主共和国・ペルーなど",
                                       "日本は1926年を最後に　国内での発生なし"]), "日本は約100年\n発生なし", dur=4.4, se="page_turn_02"),
        panel(items("じゃあロシアの件は？", ["研究所の職員が亡くなった", "当局は「ペストは検出されず」", "死因は「原因不明の肺炎」（10/7時点）"]),
              "当局は\nペストを否定", dur=4.2, se="pinpon_notice"),
        two("bg20_counter", "weird_meowing_cat", "calm_black_face_sheep", "北海道から\n近くない？", who="L", dur=2.4,
            se="question_hatena_maou"),
        two("bg20_counter", "weird_meowing_cat", "calm_black_face_sheep", "札幌まで直線で約2,900km\nペストは日本の検疫感染症で\n空港や港で見張ってる",
            who="R", dur=3.6, se="page_turn_01"),
        two("bg02_room", "sleepy_sleepy_cat", "think_bike_front_seat_cat", "怖がりすぎず\n続報は公式の発表で\n確認な", who="R",
            dur=3.0, se="tv_professional_poon"),
        one("bg03_blackboard", "wave_waving_cat", "ニュース猫", NEWS, "なぜ騒がれた？\n本編で解説！", cap_col=YELLOW, h=760,
            dur=3.0, se="chirin", bgm={"file": COCOA, "gain": -6, "fade": 0.8}),
    ]


# ---- 6：実は既婚で炎上 ----
def honnin(a, cap, **kw):
    return dict(kind="scene", bg=Q.bg("bg14_home_night"), cats=[Q.cat(a, "本人（再現）", 960, HONNIN, h=820)], cap=cap, **kw)


def cuts_6():
    return [
        one("bg12_liquor_shelf", "surprise_big_pupils_cat", "ニュース猫", NEWS, "年収240万・独身の\n人気YouTuberが\n実は既婚！？", cap_col=RED,
            dur=3.0, fx=["lines", "shake"], se=["jan", "doon_heavy"], bgm={"file": PURPLE, "gain": -6}),
        panel(items("どんなチャンネル？", ["「年収240万・43歳独身・工場勤務」", "給与明細・婚活・柴犬との暮らし", "登録者　約68万人"]),
              "「絶望ライン工」", dur=3.8, se="page_turn_01"),
        panel(items("炎上までの流れ", ["9/17　「年収240万円『質素な暮らし』」", "9/24　「43歳独身の休日」", "9/28　結婚と子どもの誕生を報告"]),
              "独身動画の\n4日後に", cap_col=RED, dur=4.2, se="doon_heavy", bgm={"file": NORA, "gain": -6}),
        one("bg06_spotlight", "weird_meowing_cat", "ニュース猫", NEWS, "4日後！？\n時空ゆがんでない！？", cap_col=RED, dur=2.4,
            fx=["lines", "shake"], se="explosion_dokaan"),
        two("bg02_room", "huh_huh_cat", "eat_pop_cat", "え、でも結婚って\nおめでたいじゃん", who="L", dur=2.4, se="question_hatena_maou"),
        panel(items("怒りのポイントはここ", ["× 結婚したこと", "○ “独身”の本・アルバムを売り続けた", "○ コメント欄を閉じた"]),
              "結婚が悪いん\nじゃない", dur=4.4, se="card_flip"),
        honnin("calm_black_face_sheep", "「嘘をついて\nおりました」\n（説明動画の要旨）", dur=3.0, se="pi",
               bgm={"file": COCOA, "gain": -6}),
        honnin("sleepy_old_memories_cat", "「“弱者ビジネス”と\n思われても仕方ない\n運営でした」（要旨）", dur=3.2, se="pi"),
        two("bg14_home_night", "think_bike_front_seat_cat", "work_typing_cat", "家族を伏せたのは\n危害や実害から\n守るためとも説明", who="R",
            dur=3.2, se="pinpon_notice"),
        two("bg09_sns", "huh_huh_cat", "work_typing_cat", "10月5日\nチャンネルの\n活動休止を発表", who="R", dur=2.8, se="doon_movie"),
        panel(items("ネットの声", ["批判：今の看板は下ろさないと違和感", "擁護：あなたが幸せならそれでいい", "考察：余裕のない社会の反映では"]),
              "批判も応援も", dur=4.2, se="page_turn_02"),
        two("bg02_room", "sleepy_sleepy_cat", "eat_pop_cat", "“設定”を売るなら\n変わったときの\n畳み方が一番むずかしい", who="R",
            dur=3.4, se="tv_professional_poon"),
        two("bg19_kids_room", "sad_banana_cat_cry", "eat_pop_cat", "おめでたいことが\n炎上になるの\n切ないね", who="L", dur=2.8,
            se="tear_drop"),
        one("bg03_blackboard", "wave_waving_cat", "ニュース猫", NEWS, "本人の説明・ネットの声は\n本編で解説！", cap_col=YELLOW, h=760,
            dur=3.0, se="chirin", bgm={"file": COCOA, "gain": -6, "fade": 0.8}),
    ]


SHORTS = {
    "5a": (cuts_5a, ("ペスト研究所で", "何が起きた⁉"), "ロシア・ペスト研究所", "short_05a_what"),
    "5b": (cuts_5b, ("ペストって", "今も治るの⁉"), "ロシア・ペスト研究所", "short_05b_cure"),
    "6": (cuts_6, ("「年収240万・独身」が", "実は既婚で炎上⁉"), "絶望ライン工　炎上", "short_06_zetsubou"),
}


def main():
    for key in sys.argv[1:] or list(SHORTS):
        fn, title, label, name = SHORTS[key]
        S.run(fn(), Q.title_band(*title, label=label), os.path.join(HERE, "out", name + ".mp4"),
              os.path.join(HERE, "out", name + "_preview"))


if __name__ == "__main__":
    main()
