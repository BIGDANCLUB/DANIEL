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
TRAIN_L = TL.TRAIN_L

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


def crowd_mat():
    """人の頭と服が細かく並んだように見える、色のつぶつぶ。"""
    m = bpy.data.materials.new("people_crowd")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.9
    coord = nt.nodes.new("ShaderNodeTexCoord")
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.inputs["Scale"].default_value = 1.6          # 1m に 1.6 個 ≒ 人の間隔
    nt.links.new(coord.outputs["Object"], vor.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cols = [(0.05, 0.04, 0.03), (0.15, 0.22, 0.45), (0.75, 0.72, 0.68), (0.55, 0.15, 0.12), (0.20, 0.30, 0.20), (0.85, 0.65, 0.20)]
    cr.interpolation = 'CONSTANT'
    cr.elements[0].color = (*cols[0], 1)
    cr.elements[1].position = 0.9
    cr.elements[1].color = (*cols[-1], 1)
    for i, c in enumerate(cols[1:-1], start=1):
        e = cr.elements.new(i / len(cols))
        e.color = (*c, 1)
    nt.links.new(vor.outputs["Color"], nt.nodes.new("ShaderNodeSeparateColor").inputs[0])
    sep = nt.nodes["Separate Color"]
    nt.links.new(sep.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], b.inputs["Base Color"])
    return m


def crowd_disk(tm, center=(0, 0), z=3.0):
    """乗客がぎゅうぎゅうに立った円（半径は TL.radius）。模様は物の座標なので、拡大しても人の大きさは変わらないよう世界座標で付ける。"""
    m = W.mat("crowd", (0.16, 0.11, 0.14), 0.9)      # 遠くから見ると、黒っぽい頭と服の「人の海」
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1.0, depth=z, location=(center[0], center[1], z / 2))
    o = bpy.context.object
    o.data.materials.append(m)
    for f, x in enumerate(tm, start=1):
        r = max(0.3, TL.radius(x))
        o.scale = (r, r, 1)
        o.keyframe_insert("scale", frame=f)
    return o


def city_ground():
    """遠くから見た街：道路の格子と色のちがう区画（レンガ模様のテクスチャ）。"""
    m = bpy.data.materials.new("citymap")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.9
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.inputs["Scale"].default_value = 0.012       # 区画 約80m
    brick.inputs["Mortar Size"].default_value = 0.012
    brick.inputs["Color1"].default_value = (0.36, 0.33, 0.30, 1)
    brick.inputs["Color2"].default_value = (0.24, 0.26, 0.22, 1)
    brick.inputs["Mortar"].default_value = (0.12, 0.12, 0.13, 1)
    brick.offset = 0.0
    nt.links.new(geo.outputs["Position"], brick.inputs["Vector"])
    # 遠くから見たときの、緑（公園・山）と街のまだら（数km単位）
    noi = nt.nodes.new("ShaderNodeTexNoise")
    noi.inputs["Scale"].default_value = 0.0004
    noi.inputs["Detail"].default_value = 6
    nt.links.new(geo.outputs["Position"], noi.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.45
    ramp.color_ramp.elements[0].color = (0.09, 0.15, 0.07, 1)
    ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[1].color = (0.30, 0.29, 0.27, 1)
    nt.links.new(noi.outputs["Fac"], ramp.inputs[0])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.inputs["Factor"].default_value = 0.55
    nt.links.new(brick.outputs["Color"], mix.inputs[6])
    nt.links.new(ramp.outputs["Color"], mix.inputs[7])
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    bpy.ops.mesh.primitive_plane_add(size=30000000, location=(0, 0, 0))
    bpy.context.object.data.materials.append(m)


def dense_blocks(half=1500, step=80, seed=7):
    r = random.Random(seed)
    cols = [W.mat("bld_a", (0.55, 0.55, 0.58), 0.6), W.mat("bld_b", (0.68, 0.64, 0.58), 0.7), W.mat("bld_c", (0.42, 0.45, 0.5), 0.5)]
    for gx in range(-half, half, step):
        for gy in range(-half, half, step):
            if abs(gx) < 30:
                continue                          # 線路のところは空ける
            d = math.hypot(gx, gy)
            hh = r.uniform(8, 25) + (60 * math.exp(-d / 500) * r.random())
            W.box((gx + step / 2, gy + step / 2, hh / 2), (step * 0.7, step * 0.7, hh), r.choice(cols), bevel=0)


def city():
    city_ground()
    dense_blocks()
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


# ---------- 床板つきで走る電車 ----------
V_TRAIN = 14.0          # 走る速さ m/s（約50km/h）
FRONT0 = 30.0           # 1コマ目の先頭の位置
CARS = 11


D = 1.0                 # 先頭から後ろへ向かう向き（+y）。電車は -y へ走り、カメラは前から夕日の方を見る


def front_y(f):
    return FRONT0 - V_TRAIN * (f - 1) / TL.FPS


def people_mat(name="people_top"):
    """床板の上の人の海。模様は世界座標で付け、電車と一緒に動くよう位置をキーフレームでずらす。"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.85
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    mp = nt.nodes.new("ShaderNodeMapping")
    nt.links.new(geo.outputs["Position"], mp.inputs["Vector"])
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.inputs["Scale"].default_value = 1.8
    nt.links.new(mp.outputs["Vector"], vor.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = 'CONSTANT'
    cols = [(0.04, 0.03, 0.03), (0.16, 0.22, 0.42), (0.70, 0.68, 0.64), (0.50, 0.14, 0.12), (0.18, 0.28, 0.18), (0.80, 0.62, 0.22)]
    cr.elements[0].color = (*cols[0], 1)
    cr.elements[1].position = 0.92
    cr.elements[1].color = (*cols[-1], 1)
    for i, c in enumerate(cols[1:-1], start=1):
        cr.elements.new(i / len(cols)).color = (*c, 1)
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(vor.outputs["Color"], sep.inputs[0])
    nt.links.new(sep.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], b.inputs["Base Color"])
    bump = nt.nodes.new("ShaderNodeBump")       # 頭のでこぼこ
    bump.inputs["Strength"].default_value = 0.6
    nt.links.new(vor.outputs["Distance"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m, mp


def unit_box(m, name):
    """1m の箱（拡大は scale で）。"""
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(m)
    return o


def deck_train(tm, boards=False, far=False):
    """走る電車と、屋根の上の床板・人の海。tm は各コマの駅数。"""
    nf = len(tm)
    root = commuter(y0=FRONT0, cars=CARS)
    root.rotation_euler.z = math.pi
    for f in range(1, nf + 1):
        root.location.y = front_y(f)
        root.keyframe_insert("location", frame=f)
    steel = W.mat("deck_steel", (0.42, 0.43, 0.45), 0.45)
    plate = W.mat("deck_plate", (0.58, 0.57, 0.54), 0.6)
    yellow = W.mat("deck_yellow", (0.95, 0.72, 0.10), 0.5)
    # 1両ずつの床板（上から降りてきて屋根に付く）
    land_end = 1
    if boards:
        for c in range(CARS):
            yc = -CAR_L / 2 - c * (CAR_L + 0.5)
            f0 = 8 + c * 6
            parts = [W.box((0, yc, 4.75), (2.0, CAR_L - 2, 0.7), steel, bevel=0.03)]        # 屋根の上の台
            for sy in (-1, 1):
                parts.append(W.box((0, yc + sy * (CAR_L / 2 - 2.5), 4.75), (2.6, 0.5, 0.7), steel, bevel=0.03))
            pl = W.box((0, yc, 5.25), (4.2, CAR_L + 0.4, 0.3), plate, bevel=0.03)
            parts.append(pl)
            for sx in (-1, 1):
                parts.append(W.box((sx * 2.05, yc, 5.45), (0.12, CAR_L + 0.4, 0.12), yellow, bevel=0))
            bpy.ops.object.empty_add(location=(0, 0, 0))
            grp = bpy.context.object
            grp.parent = root
            for p in parts:
                p.parent = grp
            for f, z in ((1, 18.0), (f0, 18.0), (f0 + 14, 0.0), (nf, 0.0)):
                grp.location.z = z
                grp.keyframe_insert("location", frame=f)
            land_end = max(land_end, f0 + 14)
    # 床板（広がっていく1枚の板）と、その上の人の海
    deck = unit_box(plate, "deck")
    pm, mp = people_mat()
    near = boards and not far
    FRONT_FIG = 42.0             # 前から 42m は本物の人形が立つので、人の海は後ろと両わきだけ
    top = unit_box(pm, "people")
    sides = [unit_box(pm, "people_l"), unit_box(pm, "people_r")] if near else []
    edge = unit_box(yellow, "deck_edge")
    column = unit_box(steel, "deck_column")          # 屋根から床板を持ち上げる柱
    bpy.ops.object.empty_add(location=(0, 0, 0))
    lifter = bpy.context.object                      # 人形を床板と一緒に持ち上げる
    lifter.parent = root
    mid = D * (CAR_L * CARS + 0.5 * (CARS - 1)) / 2
    for f in range(1, nf + 1):
        x = tm[f - 1]
        w, L = TL.deck_size(x)
        if boards and f < land_end:
            w = 0.001                                 # 板が全部付くまでは1枚板は出さない
        th = 0.3 if not far else max(0.3, 0.004 * max(w, L))
        yc = front_y(f) + mid
        base = 5.1 + lift(w)
        deck.location = (0, yc, base + th / 2)
        deck.scale = (w, L + 0.4, th)
        edge.location = (0, yc, base + th * 0.4)
        ch = max(0.001, base - 4.4)
        column.location = (0, yc, 4.4 + ch / 2)
        column.scale = (min(2.0, w), min(L, 3 * TRAIN_L) * 0.92, ch)
        column.keyframe_insert("location", frame=f)
        column.keyframe_insert("scale", frame=f)
        lifter.location.z = base - 5.1
        lifter.keyframe_insert("location", frame=f)
        edge.scale = (w * (1.004 if far else 1) + 0.25, L * (1.004 if far else 1) + 0.65, th * 0.8)
        # 人：板が付いてから乗り込む（高さ 0→1.7m）
        ph = 1.7 if not far else max(1.7, 0.002 * max(w, L))
        k = 1.0
        if boards:
            k = min(1.0, max(0.0, (f - land_end) / 20))
        hz = max(0.001, ph * k)
        z = base + th + hz / 2
        on = 1 if k > 0 else 0.001
        if near:
            back_L = L - FRONT_FIG
            top.location = (0, front_y(f) - FRONT_FIG - back_L / 2 , z)
            top.location.y = yc + D * FRONT_FIG / 2
            top.scale = (max(0.001, (w - 0.3) * on), back_L, hz)
            sw = max(0.001, (w - 4.4) / 2) * on
            for sx, o in zip((-1, 1), sides):
                o.location = (sx * (2.2 + sw / 2), front_y(f) + D * FRONT_FIG / 2, z)
                o.scale = (sw, FRONT_FIG, hz)
                o.keyframe_insert("location", frame=f)
                o.keyframe_insert("scale", frame=f)
        else:
            top.location = (0, yc, z)
            top.scale = (max(0.001, (w - 0.3) * on), L, hz)
        for o in (deck, top, edge):
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("scale", frame=f)
        mp.inputs["Location"].default_value = (0, -(front_y(f) - FRONT0), 0)
        mp.inputs["Location"].keyframe_insert("default_value", frame=f)
    # 前の方の人は本物の人形（近くで見える場所）
    if near:
        r = random.Random(9)
        for k in range(130):
            px = r.uniform(-1.8, 1.8)
            py = -r.uniform(0.6, FRONT_FIG)
            pr, _ = F.person((px, py, 5.4), r.uniform(0, 360), seed=k, pose="stand", scale=0.95)
            pr.parent = lifter
            appear = land_end + 1 + int(20 * (-py / FRONT_FIG) ** 0.7)       # 前から順に乗り込む
            for f in sorted({1, appear - 1, appear, nf}):
                sc = 0.0001 if f < appear else 1.0
                pr.scale = (sc, sc, sc)
                pr.keyframe_insert("scale", frame=f)
    return root


def lift(w):
    """床板が広がったら、家や電柱に当たらないよう持ち上げる（最大120m）。"""
    return min(120.0, max(0.0, 0.32 * (w - 4.2)))


def follow_cam(tm, rel_fn, look_fn, lens=28):
    """電車を追いかけるカメラ。rel_fn(f, x) → 先頭からの位置、look_fn(f, x) → 先頭から見る点。"""
    cam = W.camera((0, 0, 10), (0, 100, 0), lens=lens)
    cam.data.clip_end = 100000000
    for f in range(1, len(tm) + 1):
        x = tm[f - 1]
        fy = front_y(f)
        rx, ry, rz = rel_fn(f, x)
        lx, ly, lz = look_fn(f, x)
        cam.location = (rx, fy + ry, rz)
        W.aim(cam, (lx, fy + ly, lz))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
    return cam


def big_city():
    city_ground()
    dense_blocks()
    track_m = W.mat("rail", (0.55, 0.52, 0.5), 0.3)
    W.box((0, 0, 0.4), (4, 60000, 0.3), track_m, bevel=0)


# ---------- 場面 ----------
def e01_open(tm):
    station_set()
    W.sunset()
    F.person((-4.2, 8, 1.2), 0, seed=5)
    cam = W.camera((-2.8, -24, 2.9), (-0.8, 120, 3.0), lens=30)
    cam.keyframe_insert("location", frame=1)
    cam.location.y += 1.2
    cam.keyframe_insert("location", frame=len(tm))


def per_car(x):
    """1両あたりの乗客（11両に分かれて乗る）。"""
    return TL.n(x) / CARS


def car_scene(tm, cam_loc=(0.2, -CAR_L / 2 + 0.6, 1.55), look=(0.0, CAR_L / 2, 1.2), lens=20, cap=340):
    interior()
    W.sunset()
    slots = seat_slots() + stand_slots()
    # この車両に乗る人数は 全体÷11（最初の1人だけは、この車両に）
    tmc = [math.log2(max(1.0, per_car(x))) if per_car(x) >= 1 else 0.0 for x in tm]
    fill_people(tmc, slots, cap)
    W.camera(cam_loc, look, lens=lens)


def f02_car(tm):
    car_scene(tm, cam_loc=(0.5, -3.6, 1.45), look=(-0.9, 2.5, 0.75), lens=22)


def f03_full(tm):
    car_scene(tm)


def f04_deck(tm):
    W.ground(12000)
    W.track(0, -400, 9000)
    W.catenary(-200, 6000, 50)
    W.buildings(seed=21, n=110, y_from=150, y_to=2500, x_min=40, x_max=350)
    W.houses(seed=22, n=280, y_from=-200, y_to=700, x_min=12, x_max=150)
    W.sunset()
    deck_train(tm, boards=True)

    def rel(f, x):
        w, _ = TL.deck_size(x) if f > 90 else (4.2, 0)
        return (-6 - 0.8 * w, -24 - 0.45 * w, 8.5 + 0.55 * w)

    def look(f, x):
        w, _ = TL.deck_size(x) if f > 90 else (4.2, 0)
        return (1.5 + 0.15 * w, 70 + 0.3 * w, 2.0)

    follow_cam(tm, rel, look, lens=26)


def aerial_follow(tm, k=1.6, side=-0.55, min_r=60):
    """床板を斜め上から見る。r は床板の大きさ。"""
    def rel(f, x):
        w, L = TL.deck_size(x)
        r = max(min_r, 0.5 * max(w, L))
        return (side * k * r * 0.6, -k * r * 1.1, k * r * 0.62)

    def look(f, x):
        w, L = TL.deck_size(x)
        return (0.0, D * (CAR_L * CARS) / 2 + 0.1 * max(w, L), 0.0)
    return follow_cam(tm, rel, look, lens=26)


def hide_sun_disc():
    """遠くから見る場面では、太陽の球（5km 先の小道具）が床板から飛び出すので隠す。"""
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.data.materials and o.data.materials[0] and o.data.materials[0].name.startswith("sun_disc"):
            o.hide_render = True


def deck_aerial(tm, **kw):
    big_city()
    W.sunset()
    hide_sun_disc()
    deck_train(tm, far=True)
    aerial_follow(tm, **kw)


def f05_wide(tm):
    deck_aerial(tm, k=1.9)


def f06_tokyo(tm):
    deck_aerial(tm)


def f07_japan(tm):
    deck_aerial(tm, side=0.55)


def f08_loop(tm):
    deck_aerial(tm, k=1.5)


def f09_world(tm):
    deck_aerial(tm, side=0.55)


def f10_area(tm):
    deck_aerial(tm, k=1.3, side=-0.8)


def f11_end(tm):
    deck_aerial(tm, k=2.2, side=0.3)


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
