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
# 「PHOTO:」で始まる背景は写真ふう（物語形式の動画・18本目〜）。人物は顔を出さない
PHOTO_STYLE = ("Wide 16:9 realistic stock photograph, natural lighting, high resolution, sharp focus. "
               "No faces, no animals, no text, no letters, no readable signs, no logos, no watermark.")
# 「ILLUST:」は吹き出しに入れるイラスト（白い背景の一枚絵）
ILLUST_STYLE = ("Cute simple flat clipart illustration, bold clean outlines, bright colors, centered single subject, "
                "plain pure white background, no text, no letters, no watermark.")
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
    },
    "15_vambi": {
        "bg69_vkei_stage": "A dark rock concert live house stage with purple and red spotlights, smoke, drum set and microphone stand",
        "bg70_youtube_studio": "A bright home video studio room with a camera on a tripod, ring light, colorful wall and sofa",
        "bg71_wedding_chapel": "An empty wedding chapel decorated with white flowers and a long aisle, warm light",
        "bg72_live_stream": "A computer desk at night with two monitors showing a live streaming screen with chat bubbles (no readable text), Christmas decorations",
        "bg73_shorts_phone": "A big smartphone floating with vertical short video frames around it, play icons and heart icons, colorful pop background",
        "bg74_world_viewers": "A glowing world map with many connection lines and play button icons spreading across continents, night",
        "bg75_seminar_hall": "A modern seminar hall with a stage, big screen and rows of chairs, bright business atmosphere",
        "bg76_roppongi_night": "A Tokyo nightlife street in Roppongi at night, neon lights, tall buildings, wet road, no people",
        "bg77_police_station": "The entrance of a Japanese police station building at night with a red lamp and a flagpole",
        "bg78_agency_office": "A talent agency office meeting room with a long table and chairs, papers on the table, serious atmosphere",
        "bg79_timeline": "An abstract timeline background with glowing dots connected by a line on a dark blue gradient",
        "bg80_counter_rocket": "A subscriber counter style display with big numbers rising and a rocket launching, celebratory confetti, no readable text",
    },
    "16_tenchim": {
        "bg84_courthouse": "The exterior of a large modern Japanese courthouse building in daylight with stone steps, no people",
        "bg85_courtroom": "An empty Japanese courtroom with wooden judges' bench, witness stand and seats, solemn atmosphere",
        "bg86_product_shelf": "A pastel pink cosmetics and lingerie shop shelf with plain unbranded boxes, soft lighting, no readable text",
        "bg87_refund_money": "Stacks of Japanese yen banknotes and bank transfer slips on a desk with a calculator, no readable text",
        "bg88_contract_papers": "A desk covered with contract documents, a pen and a red seal stamp, close-up, no readable text",
        "bg89_ad_studio": "A bright advertising photo studio with softbox lights, a camera and a white backdrop, no people",
        "bg90_phone_post": "A smartphone on a table showing a social media post screen with hearts and comment icons, no readable text",
        "bg91_tv_studio_kids": "A colorful children's TV show studio set with bright shapes and cameras, no people",
    },
    "17_imamori": {
        "bg94_magazine_stand": "A convenience store magazine rack full of colorful magazines with blank covers, no readable text, no people",
        "bg95_hero_studio": "A tokusatsu hero TV show filming set in a quarry with smoke effects, camera cranes and colorful lights, no people",
        "bg96_hero_toys": "A shelf of colorful generic hero action figures and transformation belt toys in a toy store, no logos, no readable text",
        "bg97_tabloid_desk": "A weekly tabloid magazine editorial desk with camera, notebooks and printed pages, dramatic lamp light, no readable text",
        "bg98_izakaya_night": "An izakaya table at night with glasses and bottles, warm light, blurred, no people",
        "bg99_tv_station": "A modern TV broadcasting station building exterior at dusk with antenna tower, no logos",
        "bg100_lounge_night": "A calm upscale lounge bar interior at night with sofas and soft lights, no people",
        "bg101_phone_chat": "A smartphone on a bed at night showing a blurred chat app screen, no readable text, dim blue light",
        "bg102_quiet_room": "A quiet dim room with a window and curtains, soft morning light, calm and lonely atmosphere, no people",
        "bg103_timeline2": "An abstract timeline background with glowing dots connected by a line on a dark purple gradient",
    },
    "18_story": {
        "st01_phone_hands": "PHOTO: Close-up of a teenager's hands holding a smartphone in front of a white t-shirt, bright white background, "
                            "small colorful social media heart and comment bubble icons floating around the phone, face not visible",
        "st02_home_kitchen": "PHOTO: A modern home kitchen interior with white upper cabinets, wooden lower cabinets and a wooden counter, "
                             "bright daylight, no people",
        "st03_konbini": "PHOTO: Interior of a bright Japanese convenience store at night, shelves of rice balls, bento boxes and drinks, "
                        "checkout counter, no people, no readable text",
        "st04_konbini_friends": "PHOTO: Two teenage girls in school uniforms seen from behind, looking at a shelf of rice balls in a bright "
                                "Japanese convenience store, faces not visible",
        "st05_rainbow_meadow": "A cute bright illustration of a green meadow with small flowers and a big rainbow in a light blue sky, "
                               "simple flat picture-book style",
        "il_onigiri": "ILLUST: A single cute simple flat illustration of a rice ball (onigiri) and a bento box with steam, "
                      "isolated on a plain white background, clipart style",
    },
}


def generate(prompt):
    style = STYLE
    if prompt.startswith("PHOTO:"):
        prompt, style = prompt[6:].strip(), PHOTO_STYLE
    elif prompt.startswith("ILLUST:"):
        prompt, style = prompt[7:].strip(), ILLUST_STYLE
    res = _request(f"models/{MODEL}:generateContent", {
        "contents": [{"parts": [{"text": f"{prompt}\n\n{style}"}]}],
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
