"""横動画用の背景イラスト（1920x1080）を Gemini で作る。shorts/tts_gemini.py の _request を使う（GEMINI_API_KEY）。

python3 catmeme/gen_bg_gemini.py 14_japan   → backgrounds/14_japan/*.png（BG_LIST の名前ごと。あるものは作らない）
AIで作った背景は、動画の概要欄・注意書きで「AI生成」と書く（チャンネルのルール）。
"""
import base64
import io
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shorts"))
from tts_gemini import _request  # noqa: E402

MODEL = "gemini-3.1-flash-lite-image"
STYLE = ("Wide 16:9 anime-style background illustration, bright clean colors, detailed scenery like a Japanese animation "
         "background art. No people, no animals, no text, no letters, no readable signs, no logos, no watermark.")
W, H = 1920, 1080

BG_LIST = {
    "14_japan": {
        "bg43_award_stage": "An elegant award ceremony stage with golden spotlights, a trophy on a pedestal and confetti",
        "bg44_world_map": "A stylized world globe and map on a travel desk with passport, airplane tickets and a camera",
        "bg45_airport_arrival": "A bright modern airport arrival hall in Japan with large windows and planes outside",
        "bg46_sushi_counter": "A traditional sushi restaurant counter with wooden bar, fresh sushi pieces on plates",
        "bg47_ramen_shop": "A cozy small ramen shop interior at night, steaming bowls of ramen on the counter",
        "bg48_clean_street": "A spotless quiet residential street in Tokyo in the morning, neat houses and potted plants",
        "bg49_public_toilet": "A very clean modern public restroom in Japan, shiny tiles and high-tech toilet seat with control panel",
        "bg50_classroom_cleaning": "A Japanese school classroom after class with brooms, mops and buckets near the desks",
        "bg51_night_street": "A safe calm Tokyo side street at night with warm lamps, vending machines glowing",
        "bg52_koban": "A small Japanese police box (koban) on a street corner at dusk with a red lamp",
        "bg53_shinkansen": "A white bullet train (shinkansen) arriving at a clean station platform with neat waiting lines painted on the floor",
        "bg54_station_crowd_map": "A complex Tokyo train route map on a station wall, many colorful lines, abstract with no readable text",
        "bg55_ryokan": "A traditional Japanese ryokan room with tatami mats, low table with tea set and a garden view",
        "bg56_kyoto_temple": "A historic Kyoto temple street with wooden machiya houses and a pagoda in the distance",
        "bg57_tokyo_skyline": "Futuristic Tokyo skyline at dusk with skyscrapers and a tower, neon lights",
        "bg58_akihabara": "A colorful anime and game shop street with bright billboards (no readable text)",
        "bg59_sakura_park": "A park full of cherry blossoms in full bloom with picnic mats under the trees",
        "bg60_autumn_leaves": "A Japanese temple garden with bright red autumn maple leaves and a small bridge over a pond",
        "bg61_snow_onsen": "An outdoor hot spring bath surrounded by snow and pine trees, steam rising",
        "bg62_okinawa_beach": "A clear turquoise Okinawa beach with white sand and a red-roof house",
        "bg63_hokkaido_field": "Rolling colorful flower fields in Hokkaido under a blue sky",
        "bg64_vending_machines": "A row of brightly lit drink vending machines on a quiet street",
        "bg65_crowded_kyoto": "A very crowded narrow sightseeing street in Kyoto packed with tourists' umbrellas and backpacks seen from behind",
        "bg66_hotel_price": "A hotel front desk with a price board and a calculator, abstract numbers, no readable text",
        "bg67_food_sample": "A restaurant window display with realistic plastic food samples of ramen, curry and omurice",
        "bg68_coin_lockers": "A row of coin lockers in a Japanese train station hallway",
    }
}


def generate(prompt):
    res = _request(f"models/{MODEL}:generateContent", {
        "contents": [{"parts": [{"text": f"{prompt}\n\n{STYLE}"}]}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9"}},
    })
    parts = res["candidates"][0]["content"]["parts"]
    data = next(p["inlineData"]["data"] for p in parts if "inlineData" in p)
    img = Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB")
    k = max(W / img.width, H / img.height)
    img = img.resize((int(img.width * k + 0.5), int(img.height * k + 0.5)), Image.LANCZOS)
    x0, y0 = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((x0, y0, x0 + W, y0 + H))


def main(group):
    out = os.path.join(HERE, "backgrounds", group)
    os.makedirs(out, exist_ok=True)
    for name, prompt in BG_LIST[group].items():
        p = os.path.join(out, name + ".png")
        if os.path.exists(p):
            continue
        print(name, flush=True)
        generate(prompt).save(p)


if __name__ == "__main__":
    main(sys.argv[1])
