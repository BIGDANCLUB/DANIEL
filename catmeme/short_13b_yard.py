"""13本目（盗難ハイエース・ヤード）のショート2本目「盗難が減った理由は海峡!?」。作りは short_13_yard.py と同じ。

python3 catmeme/short_13b_yard.py → out/short_13b_yard.mp4

- 「海峡の閉鎖で減った」は報道・専門家の見方として「と言われている」で出す
- 横浜港の件（ランドクルーザー）も容疑の段階。国籍は出さない
- 主語になる団体（茨城県・税関・警察庁）は団体名の札つきの猫で出す（10/14 ユーザー指定）
"""
import os

import render as R
import short_03_kodomo_nisa as S
import short_refstyle as M
from short_13_yard import CITY, GARAGE, POLICE, POLICE_CAR, RAID, RUN, SCRAP, one, org

HERE = M.HERE
NAME = "short_13b_yard"
TITLE = ("車の盗難が減った理由", "まさかの“海峡”!?", M.RED, M.YELLOW, M.WHITE)
COCOA = os.path.join(S.BGM, "星降る夜のホットココア.mp3")
PRESS, PORT = "bg07_press", "bg20_counter"


def cuts():
    return [
        one(POLICE_CAR, "車の盗難\n最近*減ってる*らしい", "surprise_big_pupils_cat", 2.6, shake=True,
            se=["jan", "explosion_chudoon"], bgm={"file": COCOA, "gain": -6}),
        org(PRESS, "茨城県", "茨城県は\n2019年\n*全国ワースト1位*", "work_typing_cat", 2.6, se="page_turn_01"),
        org(PRESS, "茨城県", "条例と取り締まりで\n2024年は*4位*に", "work_typing_cat", 2.6, se="pinpoon_correct"),
        one(PRESS, "やれば\n*できるじゃん！*", "excited_hodomoe_city_cat", 2.2, size=130, se="idea_newtype_01"),
        one(RAID, "ところが……", "realize_wet_cat_stare", 1.8, size=130, se="shock_piano"),
        one(SCRAP, "最近減った理由のひとつは\n*ホルムズ海峡の閉鎖*\nと言われている", "think_bike_front_seat_cat", 3.2, size=84,
            se="pc_warning"),
        one(SCRAP, "盗んだ車を\n中東に*運べない*から\nと言われている", "think_bike_front_seat_cat", 2.8, size=90, se="kon"),
        one(RAID, "対策じゃなくて\n*海峡*！？", "rage_talking_cat", 2.4, size=130, se="game_aceattorney_desk_slam"),
        one(RAID, "海峡が開いたら\nまた*増える*かも\nとも", "despair_dramatic_kitten", 2.6, se="chin_bell_failure_sad_ending"),
        org(PORT, "税関", "一方　横浜港では\n盗難車のランクルを\n*X線検査*で見抜いた", "angry_aiming_cat", 3.0, size=86,
            se="pinpoon_correct"),
        org(PORT, "税関", "“ミニバン”と偽って\n輸出しようとした疑いで\n*4人逮捕*", "angry_aiming_cat", 3.0, size=86, se="page_turn_02"),
        one(PORT, "税関\n*有能*！", "happy_chipi_chapa_cat", 2.2, size=130, se="game_coin_get_money_gain_happy"),
        org(POLICE, "警察庁", "ヤードへの\n立ち入り検査を\n*強める*と表明", "showoff_gojo_cosplay_cat", 2.8, se="siren_police"),
        one(GARAGE, "自分の車は\nどう守る？", "think_bike_front_seat_cat", 2.2, size=130, se="quiz_question_02"),
        one(GARAGE, "*ハンドルロック*\nタイヤロックで\n“盗るのが面倒な車”に", "calm_black_face_sheep", 3.0, size=86, se="pikon"),
        one(RUN, "防犯カメラ・GPS\n*車両保険*の補償も確認", "calm_black_face_sheep", 2.8, size=90, se="pikon"),
        one(CITY, "日本の防犯\n*中東まかせ*で\nいいの？", "eat_pop_cat", 2.6, size=120, se="chirin"),
        one(CITY, "※盗難が減った理由は報道・専門家の見方です\n※横浜港の件は容疑の段階です\n※対策は一般的な方法です", "eat_pop_cat",
            3.0, size=48, se="pinpon_notice"),
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
