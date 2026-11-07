"""「もしも新幹線がマッハ10で走っていたら？」全場面の3D（Blender / bpy）。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]   （step=2 なら1つおきに書き出し、合成で2回使う）
座標: x=横、y=線路の進行方向（新横浜側が+、夕日も+y の地平線）、z=上（m）。"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timeline as TL  # noqa: E402
import world as W  # noqa: E402

bpy = W.bpy
from mathutils import Vector  # noqa: E402

RES = (540, 960)


# ---------- 部品 ----------
def ground_y(y_from, y_to, x_half=4000, z=0.0):
    g = W.mat("ground", (0.20, 0.15, 0.08), 1.0)
    W.box((0, (y_from + y_to) / 2, z - 0.5), (2 * x_half, y_to - y_from, 1.0), g, bevel=0)


def fields(seed, y_from, y_to, x_min=12, x_max=900, n=160):
    """田んぼ・畑のパッチ（参考の草地の代わり）。"""
    r = random.Random(seed)
    cols = [W.mat("field_a", (0.30, 0.26, 0.10), 1.0), W.mat("field_b", (0.22, 0.24, 0.10), 1.0),
            W.mat("field_c", (0.40, 0.31, 0.12), 1.0), W.mat("field_d", (0.26, 0.20, 0.09), 1.0)]
    for _ in range(n):
        side = r.choice((-1, 1))
        w, d = r.uniform(25, 70), r.uniform(25, 90)
        x = side * r.uniform(x_min + w / 2, x_max)
        y = r.uniform(y_from, y_to)
        W.box((x, y, 0.02), (w, d, 0.04), r.choice(cols), bevel=0)


def trees(seed, y_from, y_to, x_min=10, x_max=600, n=80):
    r = random.Random(seed)
    leaf = [W.mat("leaf_a", (0.10, 0.16, 0.06), 0.9), W.mat("leaf_b", (0.16, 0.18, 0.07), 0.9)]
    trunk = W.mat("trunk", (0.18, 0.12, 0.07), 1.0)
    for _ in range(n):
        x = r.choice((-1, 1)) * r.uniform(x_min, x_max)
        y = r.uniform(y_from, y_to)
        h = r.uniform(6, 14)
        W.box((x, y, 1.0), (0.4, 0.4, 2.0), trunk, bevel=0)
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=h * 0.32, depth=h, location=(x, y, 1.5 + h / 2))
        bpy.context.object.data.materials.append(r.choice(leaf))


def track_z(x, y_from, y_to, z):
    ballast = W.mat("ballast", (0.32, 0.29, 0.25), 1.0)
    rail = W.mat("rail", (0.55, 0.52, 0.5), 0.3)
    slab = W.mat("slab", (0.5, 0.48, 0.45), 0.9)
    L, yc = y_to - y_from, (y_to + y_from) / 2
    W.box((x, yc, z + 0.1), (4.2, L, 0.2), ballast, bevel=0)
    W.box((x, yc, z + 0.24), (2.6, L, 0.08), slab, bevel=0)
    for s in (-0.7175, 0.7175):
        W.box((x + s, yc, z + 0.36), (0.08, L, 0.16), rail, bevel=0)


SKIN = [(0.78, 0.55, 0.40), (0.70, 0.48, 0.34), (0.82, 0.62, 0.48)]
CLOTH = [(0.20, 0.24, 0.36), (0.55, 0.50, 0.42), (0.80, 0.78, 0.72), (0.30, 0.30, 0.32), (0.55, 0.22, 0.18), (0.25, 0.35, 0.28)]


def person(loc, facing_deg, seed=0, pose="stand", hat=False, scale=1.0):
    """ローポリの人。facing_deg は顔の向き（0=+y）。帽子は飛ばせるよう別のオブジェクトで返す。"""
    r = random.Random(seed)
    skin = W.mat(f"skin{seed % 3}", SKIN[seed % 3], 0.8)
    top = W.mat(f"cloth{seed % 6}", CLOTH[seed % 6], 0.9)
    bottom = W.mat(f"cloth{(seed + 3) % 6}", CLOTH[(seed + 3) % 6], 0.9)
    hair = W.mat("hair", (0.05, 0.04, 0.03), 0.8)
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    s = scale
    parts = []
    if pose == "sit":   # 地面に座る（足を前に）
        parts += [W.box((sx * 0.12 * s, 0.35 * s, 0.12 * s), (0.15 * s, 0.75 * s, 0.16 * s), bottom, bevel=0.02) for sx in (-1, 1)]
        tz = 0.55
    else:
        parts += [W.box((sx * 0.12 * s, 0, 0.45 * s), (0.15 * s, 0.17 * s, 0.9 * s), bottom, bevel=0.02) for sx in (-1, 1)]
        tz = 1.2
    parts.append(W.box((0, 0, tz * s), (0.46 * s, 0.26 * s, 0.62 * s), top, bevel=0.04))
    for sx in (-1, 1):
        parts.append(W.box((sx * 0.31 * s, 0.02 * s, (tz - 0.05) * s), (0.13 * s, 0.14 * s, 0.6 * s), top, bevel=0.02))
    parts.append(W.box((0, 0, (tz + 0.48) * s), (0.27 * s, 0.29 * s, 0.31 * s), skin, bevel=0.04))
    parts.append(W.box((0, -0.03 * s, (tz + 0.62) * s), (0.3 * s, 0.31 * s, 0.1 * s), hair, bevel=0.03))
    for p in parts:
        p.parent = root
    root.rotation_euler = (0, 0, math.radians(-facing_deg))
    hat_obj = None
    if hat:
        hm = W.mat("hat", r.choice([(0.85, 0.82, 0.70), (0.15, 0.18, 0.30)]), 0.9)
        c = Vector(loc) + Vector((0, 0, (tz + 0.72) * s))
        hat_obj = W.box(tuple(c), (0.42 * s, 0.42 * s, 0.08 * s), hm, bevel=0.02)
        W.box(tuple(c + Vector((0, 0, 0.08 * s))), (0.26 * s, 0.26 * s, 0.14 * s), hm, bevel=0.02).parent = hat_obj
        bpy.context.object.matrix_parent_inverse = hat_obj.matrix_world.inverted()
    return root, hat_obj


def bench(loc, rot_deg=0):
    wood = W.mat("bench_wood", (0.45, 0.28, 0.14), 0.8)
    metal = W.mat("bench_metal", (0.3, 0.3, 0.32), 0.5)
    seat = W.box(loc, (0.5, 1.8, 0.08), wood, bevel=0.01)
    seat.location.z += 0.45
    W.box((loc[0] + 0.22, loc[1], loc[2] + 0.75), (0.06, 1.8, 0.45), wood, bevel=0.01).parent = seat
    for sy in (-0.75, 0.75):
        W.box((loc[0], loc[1] + sy, loc[2] + 0.22), (0.45, 0.06, 0.44), metal, bevel=0).parent = seat
    for c in seat.children:
        c.matrix_parent_inverse = seat.matrix_world.inverted()
    seat.rotation_euler.z = math.radians(rot_deg)
    return seat


def papers(seed, n, x0, x1, y0, y1, z):
    r = random.Random(seed)
    m = W.mat("paper", (0.92, 0.90, 0.85), 0.9)
    out = []
    for _ in range(n):
        o = W.box((r.uniform(x0, x1), r.uniform(y0, y1), z + 0.01), (0.25, 0.35, 0.01), m, bevel=0)
        o.rotation_euler.z = r.uniform(0, 6.28)
        out.append(o)
    return out


def fly(objs, trigger, tmap, seed=1, vx=(5, 20), vy=(-5, 25), vz=(3, 12), spin=8.0, side=None, drag=0.0):
    """物を飛ばす。trigger(o) がその物が風を受ける t。tmap はフレームごとの t。
    side(o) が ±1 を返せば x の向きをそれに合わせる（線路から離れる向き）。"""
    r = random.Random(seed)
    for o in objs:
        p0 = o.location.copy()
        r0 = o.rotation_euler.copy()
        sgn = side(o) if side else 1
        v = Vector((sgn * r.uniform(*vx), r.uniform(*vy), r.uniform(*vz)))
        w = Vector((r.uniform(-spin, spin), r.uniform(-spin, spin), r.uniform(-spin, spin)))
        t0 = trigger(o)
        for f, t in enumerate(tmap, start=1):
            dt = max(0.0, t - t0)
            if drag:
                k = (1 - math.exp(-drag * dt)) / drag
            else:
                k = dt
            o.location = p0 + v * k + Vector((0, 0, -4.9 * dt * dt))
            if o.location.z < 0 and dt > 0:
                o.location.z = 0.0
            o.rotation_euler = (r0.x + w.x * dt, r0.y + w.y * dt, r0.z + w.z * dt)
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("rotation_euler", frame=f)


def puff_mat(name, col, alpha):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = 1.0
    b.inputs["Alpha"].default_value = alpha
    return m


def puffs(points, tmap, seed=3, col=(0.75, 0.62, 0.48), alpha=0.35, size=(1.5, 4.0), rise=(1.0, 4.0), grow=3.0,
          life=3.0, out=(0.0, 0.0), name="dust"):
    """土けむり・水しぶき。points = [(x, y, z, t_spawn, sx)]（sx は外へ広がる向き ±1 か 0）。"""
    r = random.Random(seed)
    m = puff_mat(name, col, alpha)
    for (x, y, z, ts, sx) in points:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(x, y, z))
        o = bpy.context.object
        o.data.materials.append(m)
        o.visible_shadow = False
        s0 = r.uniform(*size)
        vz = r.uniform(*rise)
        vx = sx * r.uniform(*out) if out != (0.0, 0.0) else r.uniform(-0.5, 0.5)
        for f, t in enumerate(tmap, start=1):
            dt = t - ts
            if dt < 0:
                o.scale = (0.001, 0.001, 0.001)
            else:
                a = min(dt / life, 1.0)
                sc = s0 * (0.3 + grow * (1 - math.exp(-dt * 2.5)))
                o.scale = (sc, sc, sc * 0.8)
                o.location = (x + vx * min(dt, 1.5), y, z + vz * min(dt, 2.0) - (4.9 * dt * dt if name.startswith("spray") else 0))
                if name.startswith("spray") and o.location.z < z:
                    o.location.z = z
                    o.scale = (sc * (1 - a), sc * (1 - a), 0.2)
            o.keyframe_insert("scale", frame=f)
            o.keyframe_insert("location", frame=f)


def cone(train, length, radius, start=-1.0, alpha=0.18, name="cone", emit=0.0):
    """新幹線の先頭から後ろへ広がる、すき通った円すい（衝撃波・雲の輪）。"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (1, 0.95, 0.9, 1)
    b.inputs["Alpha"].default_value = alpha
    b.inputs["Roughness"].default_value = 0.5
    if emit:
        b.inputs["Emission Color"].default_value = (1, 0.85, 0.7, 1)
        b.inputs["Emission Strength"].default_value = emit
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=radius, radius2=0.3, depth=length, end_fill_type='NOTHING',
                                    location=(0, start - length / 2, 1.9), rotation=(math.radians(-90), 0, 0))
    o = bpy.context.object
    o.data.materials.append(m)
    o.visible_shadow = False
    o.parent = train
    return o


def hot_nose(strength=8.0):
    """先頭が熱で光る（オレンジの発光）。"""
    m = bpy.data.materials.get("train_white")
    hot = m.copy()
    hot.name = "train_hot"
    b = hot.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = (1.0, 0.32, 0.06, 1)
    b.inputs["Emission Strength"].default_value = strength
    for o in bpy.data.objects:
        if o.name.endswith("_nose"):
            o.data.materials[0] = hot
    return hot


def flames(train, n_frames, n=50, speed=0.35, seed=5, length=22.0):
    """先頭から後ろへ流れる炎のかけら（列車に付いて動く）。"""
    r = random.Random(seed)
    m = W.mat("flame", (1, 0.5, 0.1), emit=(1.0, 0.45, 0.08), emit_strength=25)
    for i in range(n):
        o = W.box((0, 0, 0), (0.06, 2.0, 0.12), m, bevel=0)
        o.visible_shadow = False
        o.parent = train
        ph = r.random()
        ax = r.uniform(-1.6, 1.6)
        az = r.uniform(0.7, 3.2)
        for f in range(1, n_frames + 1):
            u = (ph + f * speed / length) % 1.0
            o.location = (ax * (1 + u * 0.6), -1.0 - u * length, az + u * 0.8)
            k = max(0.05, 1 - u)
            o.scale = (k, 1 + u * 2, k)
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("scale", frame=f)
            # ループの継ぎ目で一瞬で戻るよう、補間を一定に
        if o.animation_data and o.animation_data.action:
            pass


def train_at(train, tmap, y0=0.0, off=0.0):
    """t ごとの位置に列車を置く（y = y0 + 進んだ距離 + off）。"""
    for f, t in enumerate(tmap, start=1):
        train.location.y = y0 + TL.pos(t) + off
        train.keyframe_insert("location", index=1, frame=f)


def station(y_from=-170, y_to=40, both=True, people=0, seed=1, roof_to=-45):
    W.track(0, y_from - 400, y_to + 6000)
    W.platform(x_side=+1, y_from=y_from, y_to=y_to, roof_to=roof_to)
    if both:
        W.track(-5.0, y_from - 400, y_to + 6000)
        W.platform(x_side=-1, y_from=y_from, y_to=y_to, x_track=-5.0, roof_to=roof_to)


def motion_blur(on=True, shutter=0.5):
    sc = bpy.context.scene
    sc.render.use_motion_blur = on
    sc.render.motion_blur_shutter = shutter


def sun_obj():
    return next(o for o in bpy.data.objects if o.type == 'MESH' and o.data.materials and o.data.materials[0].name == "sun_disc")


def render(out, n_frames, step=1, first=None, last=None):
    """フレームごとに書き出し、太陽の画面上の位置を sun.json に残す（色味の仕上げで使う）。"""
    from bpy_extras.object_utils import world_to_camera_view
    os.makedirs(out, exist_ok=True)
    sc = bpy.context.scene
    W.render_setup(os.path.join(out, "f_####.png"), 1, n_frames, res=RES, samples=10)
    sun = sun_obj()
    cam = sc.camera
    if not cam.parent and not (cam.animation_data and cam.animation_data.action):
        # 止まったカメラは、参考動画のようにゆっくり前へ寄せる（見ている方向へ距離の4%）
        fwd = cam.rotation_euler.to_quaternion() @ Vector((0, 0, -1))   # matrix_world はまだ更新前なので向きから計算
        cam.keyframe_insert("location", frame=1)
        cam.location += fwd * max(0.6, 0.04 * cam.location.length if cam.location.length < 60 else 2.5)
        cam.keyframe_insert("location", frame=n_frames)
    info = {}
    first = first or 1
    last = last or n_frames
    for f in range(first, last + 1, step):
        sc.frame_set(f)
        v = world_to_camera_view(sc, sc.camera, sun.matrix_world.translation)
        vis = v.z > 0 and -0.3 < v.x < 1.3 and -0.3 < v.y < 1.3
        info[f] = [v.x * RES[0], (1 - v.y) * RES[1]] if vis else None
        sc.render.filepath = os.path.join(out, f"f_{f:04d}.png")
        if not os.path.exists(sc.render.filepath):
            bpy.ops.render.render(write_still=True)
    old = {}
    p = os.path.join(out, "sun.json")
    if os.path.exists(p):
        old = json.load(open(p))
    old.update({str(k): v for k, v in info.items()})
    json.dump(old, open(p, "w"))


def tmap_of(name):
    s = TL.shot(name)
    return [TL.t_of(s, i)[0] for i in range(s["frames"])]


# ---------- 場面 ----------
def s01_open(tm):
    W.ground()
    station()
    W.catenary(40, 4000, 50)
    W.buildings(seed=3, n=70, y_from=-200, y_to=900, x_min=30, x_max=500)
    W.houses(seed=4, n=120, y_from=900, y_to=3500, x_min=20, x_max=600)
    W.shinkansen(y0=0.0, cars=4)
    W.sunset()
    cam = W.camera((1.6, -160, 3.6), (-0.3, 300, 4.8), lens=40)
    cam.keyframe_insert("location", frame=1)
    cam.location.y += 1.5
    cam.keyframe_insert("location", frame=len(tm))


def s02_wheel(tm):
    W.ground()
    W.track(0, -400, 6000)
    W.platform(x_side=+1, y_from=-170, y_to=40, roof_to=-45)
    W.buildings(seed=3, n=70, y_from=-200, y_to=900, x_min=30, x_max=500)
    train = W.shinkansen(y0=0.0, cars=2)
    W.sunset()
    wheel_m = W.mat("wheel", (0.25, 0.24, 0.24), 0.35)
    for y in (-16.4, -19.0):
        for sx in (-0.7175, 0.7175):
            bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.43, depth=0.14, location=(sx, y, 0.87),
                                                rotation=(0, math.radians(90), 0))
            bpy.context.object.data.materials.append(wheel_m)
            bpy.context.object.parent = train
    r = random.Random(7)
    stone = W.mat("stone", (0.42, 0.38, 0.33), 1.0)
    spark = W.mat("spark", (1, 0.6, 0.2), emit=(1.0, 0.55, 0.15), emit_strength=80)
    n = len(tm)
    for i in range(80):
        is_spark = i < 35
        s = r.uniform(0.03, 0.06) if is_spark else r.uniform(0.05, 0.14)
        sx = r.choice((-0.7175, 0.7175))
        p0 = Vector((sx + r.uniform(-0.15, 0.15), -16.4 + r.uniform(-0.6, 0.6), 0.45))
        v = Vector((r.uniform(-3.5, -0.8), r.uniform(-2.5, 1.0), r.uniform(1.0, 3.5)))
        o = W.box(tuple(p0), (s, s * r.uniform(0.6, 2.5), s), spark if is_spark else stone, bevel=0)
        start = r.randint(1, 14)
        for f in range(1, n + 1):
            dt = max(0, f - start) / 30 * 0.5
            o.location = p0 + v * dt + Vector((0, 0, -4.9 * dt * dt))
            o.location.z = max(o.location.z, 0.32)
            o.rotation_euler = (dt * 9, dt * 7, dt * 5)
            o.scale = (1, 1, 1) if f >= start else (0, 0, 0)
            for k in ("location", "rotation_euler", "scale"):
                o.keyframe_insert(k, frame=f)
    train.keyframe_insert("location", frame=1)
    train.location.y += 0.2
    train.keyframe_insert("location", frame=n)
    W.camera((-2.4, -19.6, 0.32), (-0.4, -10.0, 1.4), lens=17)


def s03a_cab(tm):
    W.ground()
    station()
    W.catenary(40, 6000, 50)
    W.buildings(seed=3, n=120, y_from=-200, y_to=2000, x_min=30, x_max=500)
    W.houses(seed=4, n=260, y_from=1500, y_to=6000, x_min=15, x_max=500)
    train = W.shinkansen(y0=0.0, cars=2)
    W.sunset()
    train_at(train, tm)
    cam = W.camera((0, 0, 0), (0, 1, 0), lens=22)
    cam.parent = train
    cam.location = (0, -4.5, 3.9)
    cam.rotation_euler = Vector((0, 1, -0.06)).to_track_quat('-Z', 'Y').to_euler()
    motion_blur(True, 0.35)


def s03b_shinagawa(tm):
    ground_y(-3000, 6000)
    station(-200, 200, both=False)
    W.catenary(-1000, 3000, 50)
    W.buildings(seed=11, n=120, y_from=-600, y_to=1500, x_min=30, x_max=500)
    train = W.shinkansen(y0=0.0, cars=4)
    W.sunset()
    T0 = TL.T_SHINAGAWA
    for f, t in enumerate(tm, start=1):
        train.location.y = (t - T0) * TL.V
        train.keyframe_insert("location", index=1, frame=f)
    hats, ppl = [], []
    for i, (x, y) in enumerate([(4.0, 6), (5.5, 9), (4.6, 14), (6.5, 18), (4.2, 24), (5.8, 30), (7.2, 12)]):
        root, hat = person((x, y, 1.2), -90 + random.Random(i).uniform(-25, 25), seed=i + 2, hat=(i % 2 == 0))
        if hat:
            hats.append(hat)
    pp = papers(21, 40, 2.4, 9.5, -20, 70, 1.2)
    trig = lambda o: T0 + o.location.y / TL.V + 10 * abs(o.location.x) / TL.V
    fly(hats + pp, trig, tm, seed=4, vx=(6, 18), vy=(5, 30), vz=(4, 12), drag=0.8)
    pts = [(r_x, y, 0.6, T0 + y / TL.V, 0) for y in range(-150, 400, 5) for r_x in (-2.2, 2.2)]
    puffs(pts, tm, size=(0.6, 1.6), rise=(0.5, 2.0), grow=2.5)
    W.camera((8.4, -2, 2.6), (1.0, 30, 1.7), lens=34)
    motion_blur(True, 0.5)


def tama_set():
    """多摩川：川は x の向きに流れる。鉄橋は y=-170〜170、高さ 8m。"""
    water = W.mat("water", (0.30, 0.34, 0.38), 0.12)
    W.box((0, 0, -1.6), (8000, 340, 0.2), water, bevel=0)
    ground_y(-4000, -170)
    ground_y(170, 6000)
    bank = W.mat("bank", (0.30, 0.27, 0.15), 1.0)
    for s in (-1, 1):
        W.box((0, s * 160, -0.8), (8000, 30, 1.6), bank, bevel=0)
    steel = W.mat("bridge", (0.40, 0.40, 0.42), 0.5)
    W.box((0, 0, 7.4), (6.0, 340, 1.2), steel, bevel=0.05)
    for y in range(-160, 170, 40):
        W.box((0, y, 3.0), (4.0, 3.0, 9.5), steel, bevel=0.05)
    for s in (-1, 1):   # トラス（簡単な格子）
        W.box((s * 3.0, 0, 9.6), (0.25, 340, 0.3), steel, bevel=0)
    emb = W.mat("embank", (0.35, 0.30, 0.22), 1.0)
    for s in (-1, 1):
        W.box((0, s * (170 + 1500), 3.75), (14, 3000, 7.5), emb, bevel=0)
    track_z(0, -3200, 3200, 8.0)
    fields(31, -3000, -200, n=120)
    fields(32, 200, 4000, n=150)
    W.houses(seed=33, n=150, y_from=300, y_to=4000, x_min=30, x_max=800)
    W.houses(seed=34, n=120, y_from=-3000, y_to=-300, x_min=30, x_max=800)
    trees(35, -1500, 3000, x_min=40, n=60)


def lift_train(train):
    for c in train.children:
        c.location.z += 8.0


def river_spray(tm, x_list, y_from=-150, y_to=150, step=6, seed=9):
    pts = []
    for y in range(y_from, y_to, step):
        for x in x_list:
            ts = TL.T_TAMA + y / TL.V + 10 * abs(x) / TL.V
            pts.append((x, y, -1.4, ts, 1 if x > 0 else -1))
    puffs(pts, tm, seed=seed, col=(0.85, 0.88, 0.9), alpha=0.55, size=(1.2, 3.0), rise=(8, 22), grow=2.0,
          life=2.5, out=(3, 10), name="spray")


def s03c_tama(tm):
    tama_set()
    train = W.shinkansen(y0=0.0, cars=4)
    lift_train(train)
    W.sunset()
    for f, t in enumerate(tm, start=1):
        train.location.y = (t - TL.T_TAMA) * TL.V
        train.keyframe_insert("location", index=1, frame=f)
    root, hat = person((46, -172, 0.0), 0, seed=8, pose="sit", hat=True)
    rod = W.box((46.3, -170.5, 1.3), (0.04, 4.0, 0.04), W.mat("rod", (0.1, 0.1, 0.1), 0.4), bevel=0)
    rod.rotation_euler.x = math.radians(35)
    trig = lambda o: TL.T_TAMA + o.location.y / TL.V + 10 * abs(o.location.x) / TL.V
    fly([rod, hat], trig, tm, seed=8, vx=(4, 10), vy=(4, 12), vz=(6, 12), side=lambda o: 1, drag=0.6)
    river_spray(tm, [-6, -12, -20, 6, 12, 20])
    W.camera((56, -166, 1.6), (-12, -10, 7.0), lens=32)
    motion_blur(True, 0.5)


def s03d_town(tm):
    ground_y(-3000, 9000)
    W.track(0, -3000, 9000)
    W.catenary(-500, 6000, 50)
    fields(41, -500, 6000, n=260)
    W.houses(seed=42, n=420, y_from=-300, y_to=7000, x_min=18, x_max=700)
    trees(43, -300, 6000, x_min=15, n=160)
    train = W.shinkansen(y0=0.0, cars=4)
    W.sunset()
    T0 = 4.6
    for f, t in enumerate(tm, start=1):
        train.location.y = (t - T0) * TL.V
        train.keyframe_insert("location", index=1, frame=f)
    pts = [(sx, y, 1.0, T0 + y / TL.V, 0) for y in range(60, 4000, 12) for sx in (-3, 3)]
    puffs(pts, tm, size=(1.5, 3.5), rise=(1.0, 4.0), grow=2.5)
    W.camera((10, 30, 3.5), (-1, 300, 2.0), lens=32)
    motion_blur(True, 0.5)


def s03e_arrive(tm):
    W.ground()
    station(people=0)
    W.catenary(40, 4000, 50)
    W.buildings(seed=51, n=80, y_from=-200, y_to=900, x_min=30, x_max=500)
    W.houses(seed=52, n=120, y_from=900, y_to=3500, x_min=20, x_max=600)
    train = W.shinkansen(y0=0.0, cars=4)
    W.sunset()
    for f, t in enumerate(tm, start=1):
        train.location.y = min(0.0, (t - TL.T_ARRIVE) * TL.V)
        train.keyframe_insert("location", index=1, frame=f)
    hats = []
    for i, (x, y) in enumerate([(4.5, -60), (6.0, -45), (5.0, -30), (7.5, -80), (4.2, -100)]):
        _, hat = person((x, y, 1.2), -60 - i * 10, seed=i + 20, hat=(i % 2 == 0))
        if hat:
            hats.append(hat)
    pp = papers(55, 50, 2.4, 9.5, -150, 30, 1.2)
    fly(hats + pp, lambda o: TL.T_ARRIVE - 0.02 + 10 * abs(o.location.x) / TL.V, tm, seed=6, vx=(4, 14), vy=(10, 30),
        vz=(3, 10), drag=0.8)
    cam = W.camera((1.6, -170, 3.6), (-0.3, 300, 4.8), lens=40)
    cam.keyframe_insert("location", frame=1)
    cam.location.y += 2.0
    cam.keyframe_insert("location", frame=len(tm))
    motion_blur(True, 0.5)


def s06_boom(tm):
    W.ground()
    station()
    W.catenary(40, 4000, 50)
    W.buildings(seed=3, n=70, y_from=-200, y_to=900, x_min=30, x_max=500)
    train = W.shinkansen(y0=0.0, cars=4)
    W.sunset()
    train_at(train, tm)
    c = cone(train, 16.0, 3.4, start=-2.5, alpha=0.35, name="vapor", emit=0.6)
    for f, t in enumerate(tm, start=1):
        k = 0.001 if TL.mach(t) < 1.0 else min(1.0, 0.25 + (TL.mach(t) - 1.0) * 6)
        c.scale = (k, k, k)
        c.keyframe_insert("scale", frame=f)
    W.camera((-13.5, 26, 2.9), (0, 14, 2.0), lens=24)


def tracking_world(seed):
    W.ground()
    W.track(0, -400, 9000)
    W.catenary(-400, 6000, 50)
    fields(seed, -400, 6000, n=300)
    W.houses(seed=seed + 1, n=300, y_from=-200, y_to=6000, x_min=18, x_max=600)
    W.buildings(seed=seed + 2, n=60, y_from=-300, y_to=1200, x_min=60, x_max=500)
    trees(seed + 3, -300, 6000, x_min=12, n=150)


def s07_heat(tm):
    tracking_world(70)
    train = W.shinkansen(y0=0.0, cars=2)
    W.sunset()
    train_at(train, tm)
    hot_nose(10.0)
    flames(train, len(tm), n=70, speed=0.6)
    cone(train, 120, 12, start=-1.0, alpha=0.06, name="shock")
    cam = W.camera((0, 0, 0), (0, 1, 0), lens=22)
    cam.parent = train
    cam.location = (-5.2, 7.0, 2.4)
    cam.rotation_euler = (Vector((0, -5.0, 1.7)) - Vector(cam.location)).to_track_quat('-Z', 'Y').to_euler()
    motion_blur(True, 0.5)


def s08_streak(tm):
    tracking_world(80)
    train = W.shinkansen(y0=0.0, cars=4)
    W.sunset()
    train_at(train, tm)
    hot_nose(16.0)
    flames(train, len(tm), n=50, speed=0.8)
    cone(train, 200, 20, start=-1.0, alpha=0.06, name="shock")
    cam = W.camera((0, 0, 0), (0, 1, 0), lens=30)
    cam.parent = train
    cam.location = (5.0, -150.0, 7.0)
    cam.rotation_euler = (Vector((0, 40.0, 1.0)) - Vector(cam.location)).to_track_quat('-Z', 'Y').to_euler()
    motion_blur(True, 0.5)


def s09_sound(tm):
    tracking_world(90)
    train = W.shinkansen(y0=0.0, cars=3)
    W.sunset()
    train_at(train, tm)
    hot_nose(12.0)
    flames(train, len(tm), n=60, speed=0.5)
    cone(train, 160, 16, start=-1.0, alpha=0.08, name="shock")
    cam = W.camera((0, 0, 0), (0, 1, 0), lens=24)
    cam.parent = train
    cam.location = (-12.0, -24.0, 5.0)
    cam.rotation_euler = (Vector((0, -4.0, 2.2)) - Vector(cam.location)).to_track_quat('-Z', 'Y').to_euler()
    motion_blur(True, 0.5)


def s10_after(tm):
    ground_y(-3000, 6000)
    station(-200, 200, both=False)
    W.catenary(-1000, 3000, 50)
    W.buildings(seed=11, n=120, y_from=-600, y_to=1500, x_min=30, x_max=500)
    train = W.shinkansen(y0=0.0, cars=4)
    W.sunset()
    T0 = TL.T_SHINAGAWA
    for f, t in enumerate(tm, start=1):
        train.location.y = (t - T0) * TL.V
        train.keyframe_insert("location", index=1, frame=f)
    hot_nose(8.0)
    cone(train, 300, 30, start=-1.0, alpha=0.07, name="shock")
    hats = []
    for i, (x, y) in enumerate([(4.5, 40), (6.0, 70), (5.0, 110), (7.0, 150)]):
        _, hat = person((x, y, 1.2), -90, seed=i + 30, hat=True)
        hats.append(hat)
    pp = papers(61, 60, 2.4, 9.5, 10, 200, 1.2)       # カメラの前を横切らないよう少し先から
    trig = lambda o: T0 + o.location.y / TL.V + 10 * abs(o.location.x) / TL.V
    fly(hats + pp, trig, tm, seed=7, vx=(5, 15), vy=(5, 25), vz=(3, 10), drag=0.8)
    pts = [(sx, y, 0.6, T0 + y / TL.V + 10 * 2.2 / TL.V, 0) for y in range(-60, 1100, 6) for sx in (-2.2, 2.2)]
    puffs(pts, tm, size=(0.6, 1.6), rise=(0.5, 2.0), grow=2.5)
    W.camera((6.0, -45, 2.9), (-0.5, 200, 2.0), lens=28)
    motion_blur(True, 0.5)


def s11_bench(tm):
    ground_y(-3000, 6000)
    station(-200, 200, both=False)
    W.catenary(-1000, 3000, 50)
    W.buildings(seed=12, n=120, y_from=-600, y_to=1500, x_min=30, x_max=500)
    train = W.shinkansen(y0=0.0, cars=4)
    W.sunset()
    T0 = TL.T_SHINAGAWA
    for f, t in enumerate(tm, start=1):
        train.location.y = (t - T0) * TL.V
        train.keyframe_insert("location", index=1, frame=f)
    benches = [bench((6.0, y, 1.2), 0) for y in range(14, 120, 12)]
    misc = []
    bin_m = W.mat("bin", (0.2, 0.35, 0.25), 0.7)
    for y in (20, 56, 92):
        misc.append(W.box((7.8, y, 1.75), (0.6, 0.6, 1.1), bin_m, bevel=0.03))
    pp = papers(71, 60, 2.4, 9.5, 0, 140, 1.2)
    trig = lambda o: T0 + o.location.y / TL.V + 10 * abs(o.location.x) / TL.V
    fly(benches + misc, trig, tm, seed=11, vx=(8, 20), vy=(10, 30), vz=(5, 12), spin=6, drag=0.4)
    fly(pp, trig, tm, seed=12, vx=(6, 18), vy=(10, 35), vz=(4, 14), drag=0.8)
    W.camera((9.0, 2, 2.0), (3.5, 60, 1.8), lens=24)
    motion_blur(True, 0.5)


def s12_osaka(tm):
    tracking_world(120)
    train = W.shinkansen(y0=0.0, cars=4)
    W.sunset()
    train_at(train, tm, off=-6000.0)    # 場所は畑の中（t=3 の位置 8.5km を y=2.5km 付近に）
    hot_nose(10.0)
    flames(train, len(tm), n=50, speed=0.5)
    cone(train, 200, 20, start=-1.0, alpha=0.08, name="shock")
    cam = W.camera((0, 0, 0), (0, 1, 0), lens=26)
    cam.parent = train
    cam.location = (10.0, -25.0, 70.0)
    cam.rotation_euler = (Vector((0, -50.0, 0.0)) - Vector(cam.location)).to_track_quat('-Z', 'Y').to_euler()
    motion_blur(True, 0.5)


def s13_fisher(tm):
    tama_set()
    train = W.shinkansen(y0=0.0, cars=4)
    lift_train(train)
    W.sunset()
    for f, t in enumerate(tm, start=1):
        train.location.y = (t - TL.T_TAMA) * TL.V
        train.keyframe_insert("location", index=1, frame=f)
    root, hat = person((46, -172, 0.0), 0, seed=8, pose="sit", hat=True)
    rod = W.box((46.3, -170.5, 1.3), (0.04, 4.0, 0.04), W.mat("rod", (0.1, 0.1, 0.1), 0.4), bevel=0)
    rod.rotation_euler.x = math.radians(35)
    bucket = W.box((47.2, -172.5, 0.25), (0.4, 0.4, 0.5), W.mat("bucket", (0.2, 0.3, 0.6), 0.6), bevel=0.03)
    trig = lambda o: TL.T_TAMA + o.location.y / TL.V + 10 * abs(o.location.x) / TL.V
    fly([rod, hat], trig, tm, seed=8, vx=(3, 8), vy=(4, 10), vz=(5, 10), spin=4, side=lambda o: -1, drag=0.6)   # カメラと反対へ
    river_spray(tm, [-6, -12, -20, 6, 12, 20])
    W.camera((48.6, -176.6, 1.4), (44.0, -165.0, 2.2), lens=28)
    motion_blur(True, 0.5)


def s14_river(tm):
    tama_set()
    train = W.shinkansen(y0=0.0, cars=4)
    lift_train(train)
    W.sunset()
    for f, t in enumerate(tm, start=1):
        train.location.y = (t - TL.T_TAMA) * TL.V
        train.keyframe_insert("location", index=1, frame=f)
    hot_nose(6.0)
    cone(train, 250, 25, start=-1.0, alpha=0.06, name="shock")
    river_spray(tm, [-5, -9, -14, -20, -28, 5, 9, 14, 20, 28], step=5)
    W.camera((0, -235, 26), (0, 60, 0.0), lens=24)
    motion_blur(True, 0.5)


def s15_end(tm):
    W.ground()
    station()
    W.catenary(40, 4000, 50)
    W.buildings(seed=51, n=80, y_from=-200, y_to=900, x_min=30, x_max=500)
    W.houses(seed=52, n=120, y_from=900, y_to=3500, x_min=20, x_max=600)
    W.shinkansen(y0=0.0, cars=4)
    W.sunset()
    for i, (x, y) in enumerate([(4.5, -40), (6.0, -55), (5.0, -70)]):
        person((x, y, 1.2), -90, seed=i + 40)
    cam = W.camera((2.2, -150, 3.2), (-0.3, 300, 5.5), lens=36)
    cam.keyframe_insert("location", frame=1)
    cam.location.y += 4.0
    cam.keyframe_insert("location", frame=len(tm))


if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    first = int(sys.argv[4]) if len(sys.argv) > 4 else None
    last = int(sys.argv[5]) if len(sys.argv) > 5 else None
    W.reset()
    s = TL.shot(name)
    tm = tmap_of(name) if "segs" in s else [0.0] * s["frames"]
    globals()[name](tm)
    render(out, s["frames"], step, first, last)
    print("rendered", name)
