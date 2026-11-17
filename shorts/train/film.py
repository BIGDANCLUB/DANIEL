"""「もしも電車の乗客が1駅ごとに2倍になったら？」全場面の3D（Blender / bpy）。新幹線版（../mach）の部品を使う。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]
座標: 線路は y 方向（夕日も +y）。車内の場面は、車両の中心が原点。"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, "..", "mach"))
import timeline as TL  # noqa: E402
import world as W  # noqa: E402
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("mach_film", os.path.join(HERE, "..", "mach", "film.py"))
F = importlib.util.module_from_spec(_spec)   # 新幹線版の部品（同じ名前の film.py なので別名で読む）
_spec.loader.exec_module(F)

bpy = W.bpy
from mathutils import Vector  # noqa: E402

W.TEXTURED["crowd"] = 40.0

CAR_L, CAR_W, CAR_H = 20.0, 2.95, 2.4


# ---------- 電車 ----------
def commuter(y0=0.0, cars=3, x=0.0):
    """山手線っぽい通勤電車（銀色の車体に黄緑の帯、片側4ドア）。先頭が +y。"""
    silver = W.mat("car_silver", (0.72, 0.73, 0.74), 0.3)
    green = W.mat("car_green", (0.45, 0.75, 0.20), 0.5)
    glass = W.mat("car_glass", (0.05, 0.07, 0.08), 0.1)
    door = W.mat("car_door", (0.60, 0.61, 0.62), 0.3)
    bpy.ops.object.empty_add(location=(x, y0, 0))
    root = bpy.context.object
    parts = []
    for c in range(cars):
        yc = -CAR_L / 2 - c * (CAR_L + 0.5)
        parts.append(W.box((0, yc, 1.1 + 1.8), (CAR_W, CAR_L, 3.0), silver, bevel=0.15))
        for sx in (-1, 1):
            parts.append(W.box((sx * (CAR_W / 2 + 0.01), yc, 2.0), (0.02, CAR_L - 0.4, 0.25), green, bevel=0))
            parts.append(W.box((sx * (CAR_W / 2 + 0.01), yc, 3.35), (0.02, CAR_L - 0.4, 0.12), green, bevel=0))
            for k in range(4):
                yd = yc - CAR_L / 2 + 2.5 + k * 5.0
                parts.append(W.box((sx * (CAR_W / 2 + 0.015), yd, 2.55), (0.02, 1.3, 2.0), door, bevel=0))
                parts.append(W.box((sx * (CAR_W / 2 + 0.02), yd, 3.0), (0.02, 1.0, 0.7), glass, bevel=0))
                if k < 3:
                    parts.append(W.box((sx * (CAR_W / 2 + 0.015), yd + 2.5, 3.0), (0.02, 3.2, 0.9), glass, bevel=0))
        parts.append(W.box((0, yc, 0.75), (2.4, CAR_L - 3, 0.7), W.mat("train_dark", (0.08, 0.08, 0.09), 0.7), bevel=0.05))
    parts.append(W.box((0, 0.05, 3.0), (2.4, 0.06, 1.0), glass, bevel=0))     # 運転席の窓
    for p in parts:
        p.parent = root
    return root


def interior(seat_rows=True):
    """車内（1両）。床・壁・窓・ロングシート・つり革。中心が原点、床の高さ 0。"""
    floor = W.mat("car_floor", (0.55, 0.50, 0.42), 0.8)
    wall = W.mat("car_wall", (0.88, 0.88, 0.86), 0.6)
    seat = W.mat("car_seat", (0.20, 0.35, 0.55), 0.9)
    glass = W.mat("sunset_glass", (1.0, 0.7, 0.4), emit=(1.0, 0.62, 0.32), emit_strength=1.4)
    metal = W.mat("car_pole", (0.8, 0.8, 0.82), 0.2)
    lamp = W.mat("car_lamp", (1, 1, 1), emit=(1.0, 0.97, 0.9), emit_strength=6)
    W.box((0, 0, -0.05), (CAR_W, CAR_L, 0.1), floor, bevel=0)
    W.box((0, 0, CAR_H + 0.05), (CAR_W, CAR_L, 0.1), wall, bevel=0)
    for sx in (-1, 1):
        W.box((sx * CAR_W / 2, 0, 0.45), (0.06, CAR_L, 0.9), wall, bevel=0)
        W.box((sx * CAR_W / 2, 0, 2.15), (0.06, CAR_L, 0.6), wall, bevel=0)
        W.box((sx * (CAR_W / 2 + 0.01), 0, 1.35), (0.04, CAR_L, 0.95), glass, bevel=0)
        for k in range(5):
            W.box((sx * (CAR_W / 2 - 0.02), -CAR_L / 2 + 0.2 + k * 4.9, 1.35), (0.07, 0.35, 0.95), wall, bevel=0)
        if seat_rows:
            for k in range(4):
                yc = -CAR_L / 2 + 2.55 + k * 4.9
                W.box((sx * (CAR_W / 2 - 0.3), yc, 0.22), (0.5, 3.4, 0.44), seat, bevel=0.04)
                W.box((sx * (CAR_W / 2 - 0.08), yc, 0.65), (0.1, 3.4, 0.45), seat, bevel=0.03)
        W.box((sx * 0.55, 0, 1.98), (0.03, CAR_L, 0.03), metal, bevel=0)
        for k in range(30):
            W.box((sx * 0.55, -CAR_L / 2 + 0.5 + k * 0.65, 1.82), (0.03, 0.12, 0.16), metal, bevel=0)
    for k in range(6):
        W.box((0, -CAR_L / 2 + 1.5 + k * 3.4, CAR_H - 0.02), (0.25, 2.4, 0.04), lamp, bevel=0)
    W.box((0, CAR_L / 2, 1.2), (CAR_W, 0.06, 2.4), wall, bevel=0)
    W.box((0, -CAR_L / 2, 1.2), (CAR_W, 0.06, 2.4), wall, bevel=0)


def seat_slots():
    out = []
    for k in range(4):
        yc = -CAR_L / 2 + 2.55 + k * 4.9
        for sx in (-1, 1):
            for j in range(7):
                out.append(((sx * (CAR_W / 2 - 0.42), yc - 1.4 + j * 0.47, 0.0), 90 if sx > 0 else -90, "sit"))
    random.Random(2).shuffle(out)
    # 最初の1人は、カメラから見える席に
    first = min(out, key=lambda p: (p[0][0] - (-(CAR_W / 2 - 0.42))) ** 2 + (p[0][1] - 1.2) ** 2)
    out.remove(first)
    return [first] + out


def stand_slots():
    r = random.Random(3)
    out = []
    for i in range(16):
        for j in range(40):
            x = -0.85 + i * 0.12 + r.uniform(-0.04, 0.04)
            y = -CAR_L / 2 + 0.6 + j * 0.47 + r.uniform(-0.08, 0.08)
            out.append(((x, y, 0.0), r.uniform(0, 360), "stand"))
    out = [p for p in out if p[0][1] > -CAR_L / 2 + 2.2]          # カメラのいる端には立たせない
    out.sort(key=lambda p: (abs(p[0][0]) > 0.6, r.random()))
    return out


def fill_people(tm, slots, cap, seed=0, scale=0.92):
    """乗客を順番に出す。k 人目は N(x) >= k になったコマで現れる。"""
    shown = min(cap, len(slots))
    people = []
    for k in range(shown):
        (x, y, z), face, pose = slots[k]
        root, _ = F.person((x, y, z if pose == "stand" else 0.0), face, seed=seed + k, pose=pose, scale=scale)
        if pose == "sit":
            for c in root.children:
                c.location.z += 0.25
        appear = next((f for f, xx in enumerate(tm, start=1) if TL.n(xx) >= k + 1), None)
        for f in (1, len(tm)) if appear is None else sorted({1, max(1, appear - 1), appear, len(tm)}):
            sc = 0.0001 if (appear is None or f < appear) else 1.0
            root.scale = (sc, sc, sc)
            root.keyframe_insert("scale", frame=f)
        if root.animation_data and root.animation_data.action:
            for fc in root.animation_data.action.fcurves if hasattr(root.animation_data.action, "fcurves") else []:
                for kp in fc.keyframe_points:
                    kp.interpolation = 'CONSTANT'
        people.append(root)
    return people


def station_set(people_tm=None, cap=0):
    """夕方の駅（島式ホーム）と電車。"""
    W.ground()
    W.track(0, -400, 6000)
    W.track(-8.6, -400, 6000)
    W.platform(x_side=-1, y_from=-80, y_to=60, roof_to=40)
    W.catenary(40, 4000, 50)
    W.buildings(seed=21, n=90, y_from=-300, y_to=1500, x_min=30, x_max=600)
    W.houses(seed=22, n=150, y_from=1000, y_to=4000, x_min=20, x_max=700)
    commuter(y0=30, cars=4)


def crowd_disk(tm, center=(0, 0), z=1.7):
    """乗客がぎゅうぎゅうに立った円（半径は TL.radius）。"""
    m = W.mat("crowd", (0.32, 0.30, 0.34), 0.9)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1.0, depth=z, location=(center[0], center[1], z / 2))
    o = bpy.context.object
    o.data.materials.append(m)
    for f, x in enumerate(tm, start=1):
        r = max(0.3, TL.radius(x))
        o.scale = (r, r, 1)
        o.keyframe_insert("scale", frame=f)
    return o


def city():
    F.ground_y(-60000, 60000, x_half=60000)
    W.buildings(seed=31, n=300, y_from=-6000, y_to=6000, x_min=20, x_max=6000)
    W.buildings(seed=32, n=200, y_from=-30000, y_to=30000, x_min=6000, x_max=30000)
    W.houses(seed=33, n=250, y_from=-30000, y_to=30000, x_min=200, x_max=30000)
    track_m = W.mat("rail", (0.55, 0.52, 0.5), 0.3)
    W.box((0, 0, 0.4), (4, 60000, 0.3), track_m, bevel=0)
    commuter(y0=30, cars=11)


def aerial_cam(tm, k=2.6, min_alt=40, side=0.7):
    cam = W.camera((0, 0, 100), (0, 0, 0), lens=26)
    cam.data.clip_end = 400000
    for f, x in enumerate(tm, start=1):
        r = TL.radius(x)
        alt = max(min_alt, k * r)
        cam.location = (alt * side * 0.3, -alt * 0.95, alt)
        W.aim(cam, (0, r * 0.25, 0))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
    return cam


def tmap_of(name):
    s = TL.shot(name)
    return [TL.t_of(s, i)[0] for i in range(s["frames"])]


# ---------- 場面 ----------
def e01_open(tm):
    station_set()
    W.sunset()
    F.person((-4.2, 8, 1.2), 0, seed=5)
    cam = W.camera((-2.8, -24, 2.9), (-0.8, 120, 3.0), lens=30)
    cam.keyframe_insert("location", frame=1)
    cam.location.y += 1.2
    cam.keyframe_insert("location", frame=len(tm))


def car_scene(tm, cap, cam_loc=(0.2, -CAR_L / 2 + 0.6, 1.55), look=(0.0, CAR_L / 2, 1.2), lens=20):
    interior()
    W.sunset()
    slots = seat_slots() + stand_slots()
    fill_people(tm, slots, cap)
    W.camera(cam_loc, look, lens=lens)


def e02_one(tm):
    car_scene(tm, 1, cam_loc=(0.6, -1.8, 1.3), look=(-1.0, 1.0, 0.8), lens=24)


def e03a_car(tm):
    car_scene(tm, 340)


def e06_five(tm):
    car_scene(tm, 64)


def e07_ten(tm):
    car_scene(tm, 340)


def platform_scene(tm, cam, look, lens=26):
    station_set()
    W.sunset()
    # ホームに並ぶ人（あとから現れる）
    r = random.Random(4)
    slots = []
    for i in range(14):
        for j in range(60):
            slots.append(((-3.2 - i * 0.45 + r.uniform(-0.1, 0.1), -60 + j * 1.8 + r.uniform(-0.3, 0.3), 1.2), r.uniform(-60, 60) + 90, "stand"))
    r.shuffle(slots)
    # ホームの人は「電車に乗りきれなかった人」：乗客が 1万人を超えたあたりから並び始める
    tm2 = [x - 11.5 for x in tm]
    for k, ((x, y, z), face, pose) in enumerate(slots[:600]):
        root, _ = F.person((x, y, z), face, seed=k, pose="stand", scale=0.95)
        appear = next((f for f, xx in enumerate(tm2, start=1) if 2 ** max(xx, 0) * 200 >= k + 1), None)
        for f in sorted({1, len(tm)} | ({max(1, appear - 1), appear} if appear else set())):
            sc = 0.0001 if (appear is None or f < appear) else 1.0
            root.scale = (sc, sc, sc)
            root.keyframe_insert("scale", frame=f)
    W.camera(cam, look, lens=lens)


def e03b_platform(tm):
    platform_scene(tm, (-9.5, -40, 3.5), (-3.0, 40, 1.6))


def e08_full(tm):
    platform_scene(tm, (-9.5, -40, 3.5), (-3.0, 40, 1.6))


def aerial_scene(tm, **kw):
    city()
    W.sunset()
    crowd_disk(tm)
    aerial_cam(tm, **kw)


def e03c_city(tm):
    aerial_scene(tm)


def e03d_wide(tm):
    aerial_scene(tm)


def e09_dome(tm):
    aerial_scene(tm, k=3.2)


def e10_tokyo(tm):
    aerial_scene(tm)


def e11_japan(tm):
    aerial_scene(tm)


def e12_loop(tm):
    aerial_scene(tm, k=2.2)


def e13_world(tm):
    aerial_scene(tm)


def e14_area(tm):
    aerial_scene(tm, k=2.0, side=-0.7)


def e15_end(tm):
    aerial_scene(tm, k=3.0)


if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    first = int(sys.argv[4]) if len(sys.argv) > 4 else None
    last = int(sys.argv[5]) if len(sys.argv) > 5 else None
    W.reset()
    random.seed(1)
    s = TL.shot(name)
    tm = tmap_of(name) if "segs" in s else [0.0] * s["frames"]
    globals()[name](tm)
    F.render(out, s["frames"], step, first, last)
    print("rendered", name)
