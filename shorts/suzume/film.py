"""「もしも日本からスズメが消えたら？」全場面の3D（Blender / bpy）。スギ版（../sugi/film.py）・富士山版の部品を使う。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]
座標: z=上（m）。カメラはおおむね -y から +y を見る。"""
import math
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timeline as TL  # noqa: E402  （スギ版より先に読み込む＝こちらの時間割を使わせる）
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("sugi_film", os.path.join(HERE, "..", "sugi", "film.py"))
SG = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SG)
FJ, C, W, F, bpy = SG.FJ, SG.C, SG.W, SG.F, SG.bpy
from mathutils import Vector  # noqa: E402

FPS = TL.FPS
fr = C.frame_of
ASSETS = os.path.join(HERE, "assets")
FJ.ASSETS = ASSETS
FONT = FJ.FONT
cut, sky, sun, person, fill, puffs = FJ.cut, FJ.sky, FJ.sun, SG.person, SG.fill, SG.puffs

FARMER = {"hair": (0.80, 0.80, 0.78), "top": (0.30, 0.38, 0.50), "bottom": (0.32, 0.30, 0.26)}
FARMER_OLD = {"hair": (0.92, 0.92, 0.90), "top": (0.30, 0.38, 0.50), "bottom": (0.32, 0.30, 0.26)}
GRANDMA = {"hair": (0.75, 0.74, 0.73), "top": (0.62, 0.42, 0.50), "bottom": (0.35, 0.32, 0.38)}
TEACHER = {"top": (0.85, 0.82, 0.70), "bottom": (0.30, 0.32, 0.40), "hair": (0.10, 0.08, 0.06)}
CN = {"top": (0.30, 0.38, 0.52), "bottom": (0.28, 0.30, 0.38)}
KIDS = [{"top": (0.95, 0.75, 0.20), "bottom": (0.20, 0.30, 0.55)}, {"top": (0.90, 0.35, 0.35), "bottom": (0.25, 0.25, 0.30)},
        {"top": (0.35, 0.65, 0.85), "bottom": (0.30, 0.30, 0.35)}, {"top": (0.55, 0.80, 0.45), "bottom": (0.25, 0.28, 0.40)}]


# ---------- スズメ ----------
_SP = {}


def sparrow_mesh(kind="perch"):
    """スズメ（全長約15cm）：茶色の頭、白いほお＋黒い点、黒いのど、灰色のおなか。kind = perch / up / down / puff。"""
    if kind in _SP:
        return _SP[kind]
    brown = W.mat("sp_brown", (0.46, 0.30, 0.18), 0.8)
    cap = W.mat("sp_cap", (0.50, 0.25, 0.13), 0.8)
    belly = W.mat("sp_belly", (0.80, 0.77, 0.70), 0.9)
    white = W.mat("sp_cheek", (0.95, 0.94, 0.90), 0.8)
    black = W.mat("sp_black", (0.04, 0.04, 0.04), 0.5)
    wingm = W.mat("sp_wing", (0.38, 0.24, 0.13), 0.8)
    beak = W.mat("sp_beak", (0.15, 0.14, 0.13), 0.4)
    k = 1.25 if kind == "puff" else 1.0
    p = [F._ball(0.045 * k, (0, 0, 0.06), brown, sub=2, sc=(0.85, 1.45, 0.9)),
         F._ball(0.04 * k, (0, 0.012, 0.047), belly, sub=2, sc=(0.85, 1.15, 0.8)),
         F._ball(0.033, (0, 0.062, 0.1 + (0.008 if kind == "puff" else 0)), cap, sub=2),
         F._ball(0.015, (0, 0.087, 0.078), black, sub=1, sc=(1.0, 0.6, 1.2)),
         F._cyl(0.008, 0.0, 0.02, (0, 0.1, 0.098), beak, rot=(math.radians(-90), 0, 0), verts=6),
         W.box((0, -0.078, 0.066), (0.034, 0.075, 0.008), wingm, rot=(math.radians(12), 0, 0), bevel=0)]
    for sx in (-1, 1):
        p.append(F._ball(0.021, (sx * 0.019, 0.07, 0.094), white, sub=1, sc=(0.55, 1.0, 0.9)))
        p.append(F._ball(0.0065, (sx * 0.03, 0.074, 0.091), black, sub=1))
        p.append(F._ball(0.0055, (sx * 0.021, 0.088, 0.107), black, sub=1))
        if kind in ("perch", "puff"):
            p.append(F._ball(0.02, (sx * 0.036 * k, -0.005, 0.068), wingm, sub=1, sc=(0.4, 1.4, 0.75)))
            p.append(F._cyl(0.003, 0.003, 0.03, (sx * 0.012, 0.01, 0.012), W.mat("sp_leg", (0.55, 0.42, 0.35), 0.6), verts=4))
        else:
            ang = 30 if kind == "up" else -25
            w = W.box((sx * 0.065, -0.005, 0.075), (0.11, 0.055, 0.006), wingm, rot=(0, math.radians(-sx * ang), 0), bevel=0)
            p.append(w)
    _SP[kind] = F._join(p, f"sparrow_{kind}")
    return _SP[kind]


def perched(pts, name="perch", scale=1.0):
    """止まっているスズメ。pts = [(x, y, z, 向き)]。"""
    out = []
    for k, (x, y, z, rz) in enumerate(pts):
        o = C.link_copy(sparrow_mesh("perch"), (x, y, z), f"{name}{k}")
        o.rotation_euler.z = rz
        o.scale = (scale,) * 3
        out.append(o)
    return out


def peck(o, nf, seed=0, period=24):
    """ときどき首をふる・つつく（体ごと前にかたむける）。"""
    r = random.Random(seed)
    for f in range(1 + r.randint(0, 10), nf, period + r.randint(-4, 4)):
        o.keyframe_insert("rotation_euler", frame=f)
        o.rotation_euler.x = math.radians(35)
        o.keyframe_insert("rotation_euler", frame=f + 3)
        o.rotation_euler.x = 0.0
        o.keyframe_insert("rotation_euler", frame=f + 6)


def smooth(u):
    u = np.clip(u, 0, 1)
    return u * u * (3 - 2 * u)


def flock_track(N, nf, seed, center, size, ground=None, t_off=None, settle=None):
    """群れ（ムクドリのような、うねる群れ）。各鳥は群れの中の決まった場所にいて、群れの形が回り・伸び・波打つ。
    ground と t_off があれば、その時刻に地面（稲の中）から飛び立って群れに合流する。settle=(t0, pts) で着地。
    返り値：位置 (N, nf+1, 3)。"""
    rng = np.random.default_rng(seed)
    U = rng.normal(size=(N, 3))
    U /= np.linalg.norm(U, axis=1, keepdims=True)
    U *= rng.random((N, 1)) ** (1 / 3)
    ph = rng.uniform(0, 6.3, (N, 3))
    P = np.zeros((N, nf + 1, 3))
    for f in range(1, nf + 1):
        t = (f - 1) / FPS
        c = np.array(center(t))
        a, b, h = size(t)
        L = U.copy()
        L[:, 0] += 0.35 * np.sin(2.6 * U[:, 1] - 2.2 * t)        # 群れの中を伝わる波
        L[:, 2] += 0.30 * np.sin(2.0 * U[:, 0] + 1.6 * t)
        L += 0.06 * np.sin(ph + t * np.array([2.1, 1.7, 2.6]))
        S = L * np.array([a, b, h])
        th, tilt = 0.5 * math.sin(0.45 * t) + 0.35 * t, 0.35 * math.sin(0.7 * t)
        ct, st, cx, sx = math.cos(th), math.sin(th), math.cos(tilt), math.sin(tilt)
        R = np.array([[ct, -st, 0], [st, ct, 0], [0, 0, 1]]) @ np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
        Q = c + S @ R.T
        if ground is not None:
            w = smooth((t - t_off) / 0.9)[:, None]
            lift = (4 * w * (1 - w)) * np.array([0, 0, 1.5])
            Q = ground * (1 - w) + Q * w + lift * (w > 0)
        if settle is not None:
            t0, pts = settle
            w = smooth((t - t0) / 1.2)[:, None]
            Q = Q * (1 - w) + pts * w
        P[:, f] = Q
    P[:, 0] = P[:, 1]
    return P


def fly_objects(P, nf, f_on=1, f_off=None, scale=1.0, flap_near=None, name="fl", step=2):
    """位置の表から鳥を作って動かす。flap_near=(カメラ位置, 距離)：近い鳥だけ羽ばたき（羽の上下を入れかえ）。"""
    N = P.shape[0]
    objs = []
    for i in range(N):
        near = flap_near is not None and np.linalg.norm(P[i, f_on] - np.array(flap_near[0])) < flap_near[1]
        kinds = ("up", "down") if near else ("up",)
        group = []
        for j, kd in enumerate(kinds):
            o = C.link_copy(sparrow_mesh(kd), tuple(P[i, f_on]), f"{name}{i}_{j}")
            group.append(o)
        frames = list(range(f_on, (f_off or nf) + 1, step))
        if frames[-1] != (f_off or nf):
            frames.append(f_off or nf)
        for f in frames:
            v = P[i, min(f + 1, nf)] - P[i, max(f - 1, 1)]
            yaw = math.atan2(-v[0], v[1]) if np.linalg.norm(v[:2]) > 1e-6 else 0.0
            pitch = math.atan2(v[2], np.linalg.norm(v[:2]) + 1e-6)
            for j, o in enumerate(group):
                o.location = tuple(P[i, f])
                o.rotation_euler = (pitch, 0.0, yaw)
                vis = scale if (len(group) == 1 or ((f // 3) % 2) == j) else 1e-4
                o.scale = (vis,) * 3
                o.keyframe_insert("location", frame=f)
                o.keyframe_insert("rotation_euler", frame=f)
                o.keyframe_insert("scale", frame=f)
        for o in group:
            if f_on > 1:
                o.scale = (1e-4,) * 3
                o.keyframe_insert("scale", frame=f_on - 1)
            if f_off:
                o.scale = (1e-4,) * 3
                o.keyframe_insert("scale", frame=f_off + 1)
            if len(group) > 1:
                FJ.set_interp(o, 'CONSTANT')
        objs.append(group)
    return objs


def feathers(pts, f0, nf, seed=3, name="feather"):
    """消えたあとに残る羽：空気の抵抗で、ひらひらゆっくり落ちる（秒速 約0.4m）。"""
    r = random.Random(seed)
    mats = [W.mat("feather_b", (0.50, 0.34, 0.20), 0.8), W.mat("feather_w", (0.85, 0.82, 0.76), 0.8)]
    for k, p in enumerate(pts):
        o = W.box((0, 0, 0), (0.012, 0.045, 0.002), mats[k % 2], bevel=0, name=f"{name}{k}")
        o.visible_shadow = False
        ph, vz, amp = r.uniform(0, 6.3), r.uniform(0.3, 0.5), r.uniform(0.1, 0.25)
        o.scale = (1e-4,) * 3
        o.keyframe_insert("scale", frame=max(1, f0 - 1))
        for f in range(f0, nf + 1, 2):
            t = (f - f0) / FPS
            o.location = (p[0] + amp * math.sin(2.5 * t + ph) + 0.3 * t, p[1] + amp * 0.6 * math.cos(2.0 * t + ph),
                          max(0.05, p[2] - vz * t))
            o.rotation_euler = (0.6 * math.sin(3 * t + ph), 0.5 * math.cos(2.5 * t + ph), t * 1.5 + ph)
            o.scale = (3.0, 3.0, 3.0)
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("rotation_euler", frame=f)
            o.keyframe_insert("scale", frame=f)


def vanish_flock(P, objs, fv, n_particles=320, n_feathers=60, nf=None, seed=5, size=0.16, rise=2.0):
    """群れが四角い光の粒になって消える（金と白）。羽だけ残って落ちる。"""
    alive = [i for i in range(P.shape[0])]
    r = random.Random(seed)
    r.shuffle(alive)
    pts = [Vector(tuple(P[i, fv])) for i in alive[:n_particles]]
    FJ.sparkle_points(pts, fv, size, rise, seed=seed, life=(0.6, 1.2), trail=(2,))
    feathers([tuple(P[i, fv]) for i in alive[:n_feathers]], fv + 2, nf or fv + 90, seed=seed)


# ---------- 田んぼ・村 ----------
def rice_field(area, n, h=(0.75, 0.95), col=(0.80, 0.64, 0.24), ear=(0.86, 0.70, 0.30), seed=3, name="rice", avoid=None,
               stubble=False):
    """稲（黄金色の穂がたれる）。stubble=True で刈りあとの株。"""
    import bmesh
    r = random.Random(seed)
    bm = bmesh.new()
    x0, x1, y0, y1 = area
    for _ in range(n):
        cx, cy = r.uniform(x0, x1), r.uniform(y0, y1)
        if avoid and any(a0 <= cx <= a1 and b0 <= cy <= b1 for a0, a1, b0, b1 in avoid):
            continue
        hh = r.uniform(*h) * (0.18 if stubble else 1.0)
        for k in range(4 if not stubble else 5):
            a = r.uniform(0, 6.28)
            lean = r.uniform(0.05, 0.25)
            ca, sa = math.cos(a), math.sin(a)
            w = 0.012
            v1 = bm.verts.new((cx - w * ca, cy - w * sa, 0))
            v2 = bm.verts.new((cx + w * ca, cy + w * sa, 0))
            tip = (cx + lean * hh * sa, cy - lean * hh * ca, hh)
            v3 = bm.verts.new(tip)
            f = bm.faces.new((v1, v2, v3))
            f.material_index = 0
            if not stubble and k < 2:      # 実った穂（先がたれる）
                e1 = bm.verts.new((tip[0] - 0.012, tip[1], tip[2] - 0.01))
                e2 = bm.verts.new((tip[0] + 0.012, tip[1], tip[2] - 0.01))
                e3 = bm.verts.new((tip[0] + 2.2 * lean * hh * sa * 0.5, tip[1] - 2.2 * lean * hh * ca * 0.5, tip[2] - 0.16))
                f2 = bm.faces.new((e1, e2, e3))
                f2.material_index = 1
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    me.materials.append(W.mat(f"rice_leaf_{col}", col, 0.9))
    me.materials.append(W.mat(f"rice_ear_{ear}", ear, 0.8))
    return o


def hasa(x, y, length=6.0, rows=2):
    """はさ掛け（刈った稲を干す木の棒）。"""
    wood = W.mat("hasa_wood", (0.45, 0.33, 0.22), 0.9)
    straw = W.mat("hasa_straw", (0.78, 0.63, 0.30), 0.9)
    for dx in (-length / 2, 0, length / 2):
        F._cyl(0.05, 0.05, 2.4, (x + dx, y, 1.2), wood, verts=6)
    for k in range(rows):
        z = 1.0 + k * 0.7
        F._cyl(0.03, 0.03, length + 0.4, (x, y, z), wood, rot=(0, math.radians(90), 0), verts=6)
        C.multi_box([(x - length / 2 + 0.15 + i * 0.22, y, z - 0.25, 0.18, 0.12, 0.5, 0) for i in range(int(length / 0.22))],
                    straw, f"hasa_b{x}_{k}")


def kakashi_texture():
    from PIL import Image, ImageDraw, ImageFont
    p = os.path.join(ASSETS, "henohenomoheji.png")
    if os.path.exists(p):
        return p
    os.makedirs(ASSETS, exist_ok=True)
    im = Image.new("RGB", (400, 400), (235, 230, 215))
    d = ImageDraw.Draw(im)
    fnt = ImageFont.truetype(FONT, 90)
    fnt.set_variation_by_axes([700])
    for ch, (x, y) in (("へ", (125, 95)), ("へ", (275, 95)), ("の", (125, 175)), ("の", (275, 175)), ("も", (200, 245)),
                       ("へ", (200, 320)), ("じ", (355, 210))):
        d.text((x, y), ch, font=fnt, fill=(30, 30, 30), anchor="mm")
    im.save(p)
    return p


def kakashi(loc, facing=180):
    """案山子（へのへのもへじの顔、かさ、着物）。根元を中心にした empty を返す。"""
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    root.rotation_euler.z = math.radians(-facing)
    wood = W.mat("hasa_wood", (0.45, 0.33, 0.22), 0.9)
    parts = [F._cyl(0.04, 0.04, 2.0, (0, 0, 1.0), wood, verts=6),
             F._cyl(0.03, 0.03, 1.6, (0, 0, 1.35), wood, rot=(0, math.radians(90), 0), verts=6),
             W.box((0, 0, 1.1), (0.55, 0.22, 0.6), W.mat("kakashi_kimono", (0.25, 0.35, 0.60), 0.9), bevel=0.04),
             F._cyl(0.4, 0.05, 0.22, (0, 0, 1.92), W.mat("kasa_straw", (0.80, 0.66, 0.35), 0.9), verts=12)]
    face = C.img_mat("kakashi_face", kakashi_texture())
    bpy.ops.mesh.primitive_plane_add(size=0.34, location=(0, 0.06, 1.65))
    fc = bpy.context.object
    fc.rotation_euler.x = math.radians(90)
    fc.rotation_euler.z = math.radians(180)
    fc.data.materials.append(face)
    parts.append(fc)
    F._ball(0.17, (0, -0.02, 1.65), W.mat("kakashi_cloth", (0.92, 0.90, 0.84), 0.9), sub=2, sc=(1, 0.5, 1))
    parts.append(bpy.context.object)
    for o in parts:
        o.parent = root
    return root


def straw_hat(root):
    body = root.children[0]
    hc = root.get("hc0", 1.62)
    m = W.mat("mugiwara", (0.86, 0.74, 0.45), 0.9)
    for o in (F._cyl(0.27, 0.27, 0.015, (0, 0, hc + 0.1), m, verts=16), F._cyl(0.14, 0.12, 0.11, (0, 0, hc + 0.16), m, verts=12)):
        o.parent = body


def farmer(loc, facing, nf, arms="up", alt="down", look=None, period=18):
    p = person(loc, facing, seed=4, arms=arms, alt=alt, nf=nf, period=period, look=look or FARMER)
    straw_hat(p)
    return p


def dusk(strength=0.6):
    sky(lo=(1.0, 0.66, 0.40), hi=(0.38, 0.48, 0.72), strength=strength)
    return sun(9, 205, 5.6, (1.0, 0.62, 0.36))


def village(seed=2, field=True, harvested=False, green=False, road=False):
    """米どころの村：手前に稲田、はさ掛け、遠くに農家と山。"""
    soil = W.mat("dirt_paddy", (0.36, 0.28, 0.18), 1.0)
    bpy.ops.mesh.primitive_plane_add(size=1200, location=(0, 0, 0))
    bpy.context.object.data.materials.append(soil)
    if green:
        col, ear = (0.30, 0.52, 0.18), (0.40, 0.58, 0.22)
        far = W.mat("field_green", (0.30, 0.48, 0.16), 1.0)
    else:
        col, ear = (0.80, 0.64, 0.24), (0.86, 0.70, 0.30)
        far = W.mat("field_gold", (0.78, 0.62, 0.26), 1.0)
    W.box((0, 260, 0.35), (900, 480, 0.7), far, bevel=0)
    for sx in (-1, 1):
        W.box((sx * 163, 9, 0.35), (300, 22, 0.7), far, bevel=0)
    avoid = [(-0.6, 0.6, -3, 20)] + ([(-14, 14, 2.0, 4.6)] if road else [])
    if road:
        W.box((0, 3.3, 0.03), (40, 2.4, 0.06), W.mat("gravel_road", (0.62, 0.56, 0.46), 1.0), bevel=0)
    if field:
        rice_field((-13, 13, -2, 20), 13000, col=col, ear=ear, stubble=harvested, avoid=avoid)
    W.box((0, 9, 0.12), (1.0, 30, 0.24), W.mat("bank_aze", (0.32, 0.40, 0.18), 1.0), bevel=0.05)
    if not green:
        hasa(-6.5, 16, 6.0)
        hasa(5.5, 22, 7.0)
    walls = W.mat("wall_a", (0.84, 0.80, 0.72))
    roofs = W.mat("roof_kawara", (0.25, 0.28, 0.32), 0.6)
    r = random.Random(seed)
    for k in range(10):
        x, y = r.uniform(-60, 60), r.uniform(40, 90)
        W.box((x, y, 2.5), (8, 7, 5), walls, bevel=0.05)
        W.box((x, y, 5.6), (9, 8, 1.4), roofs, bevel=0.2)
    SG.broad_forest([(r.uniform(-120, 120), r.uniform(95, 140), 0, r.uniform(9, 14), r.uniform(0, 6), 1.0) for _ in range(40)],
                    "village_trees", seed)
    FJ.utility_poles([(-30, 30), (-10, 30), (10, 30), (30, 30)], h=8.0)
    FJ.foothills(seed=seed + 3, y=(1100, 1600), x=(-1600, 1600), n=14, col=(0.34, 0.38, 0.46), h=(70, 130))


def sky_flock_center(t):
    """冒頭の群れの通り道：目の前の稲の中から上がり、夕空を大きく回る。"""
    return (-2 + 10 * math.sin(0.6 * t), 8 + 20 * (1 - math.exp(-t / 1.6)), 2.5 + 6 * (1 - math.exp(-t / 1.0)) + 2 * math.sin(0.9 * t))


def sky_flock_size(t):
    return (8 + 3 * math.sin(1.1 * t), 5 + 2 * math.cos(0.8 * t), 2.2 + 0.8 * math.sin(1.4 * t))


# ---------- 場面 ----------
def s01_open(nf):
    dusk()
    village()
    fv = fr(TL.T_VANISH)
    r = np.random.default_rng(1)
    N = 520
    G = np.column_stack([r.uniform(-7, 7, N), r.uniform(0.5, 14, N), r.uniform(0.55, 0.85, N)])
    near = r.random(N) < 0.35          # 3分の1は、カメラのすぐ前から飛び立つ
    G[near, 0] = r.uniform(-2.2, 2.2, near.sum())
    G[near, 1] = r.uniform(0.3, 3.5, near.sum())
    t_off = 0.1 + np.hypot(G[:, 0], G[:, 1] - 1.0) * 0.06 + r.uniform(0, 0.25, N)
    P = flock_track(N, nf, 3, sky_flock_center, sky_flock_size, ground=G, t_off=t_off)
    objs = fly_objects(P, nf, f_off=fv + 3, scale=1.4, flap_near=((0.3, -1.5, 0.55), 6.0))
    vanish_flock(P, objs, fv, nf=nf)
    farmer((2.2, 6.0, 0.24), 200, nf)
    kakashi((-2.8, 9.0, 0.0), 190)
    fill((1.0, 3.0, 2.0), (2.2, 6.0, 1.5), power=80)
    # 1) 稲の中から目の前で飛び立つ群れを、カメラも追って上がる 2) うねる群れを左右に追う（おじいさんも画面に）
    # 3) 消える → 羽だけ落ちる（文字なし）
    cen = P[:, :, :].mean(axis=0)
    c1 = W.camera((0.3, -1.5, 0.5), (0.0, 10.0, 2.8), lens=20)
    c1["keep"], c1["focus"] = 1, "none"
    for f in list(range(1, 61, 2)) + [60]:
        u = float(smooth((f - 1) / 59))
        c1.location = (0.3 + 0.3 * u, -1.5 + 2.6 * u, 0.5 + 1.3 * u)
        W.aim(c1, Vector((0.0, 10.0, 2.8)).lerp(Vector(tuple(cen[f])), min(1.0, (f - 1) / 25)))
        c1.keyframe_insert("location", frame=f)
        c1.keyframe_insert("rotation_euler", frame=f)
    c2 = W.camera((3.6, 2.8, 1.4), (-1.0, 22.0, 6.5), lens=22)
    c2["f0"], c2["keep"], c2["focus"] = 61, 1, "none"
    for f in list(range(61, 121, 2)) + [120]:
        u = (f - 61) / 59
        c2.location = (3.6 - 0.8 * u, 2.8 - 1.0 * u, 1.4 + 0.25 * u)
        W.aim(c2, Vector(tuple(cen[f])) * 0.75 + Vector((2.2, 6.0, 1.8)) * 0.25)
        c2.keyframe_insert("location", frame=f)
        c2.keyframe_insert("rotation_euler", frame=f)
    cut(121, (-1.0, 8.0, 1.6), (-1.0, 27.0, 7.5), lens=28, orbit=0, push=0.0, fixat=1, zoom=1.08)
    return nf


def wire_curve(x0, x1, y, z, sag, n=40, name="wire"):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = 0.008
    sp = cu.splines.new('POLY')
    sp.points.add(n - 1)
    for i, p in enumerate(sp.points):
        u = i / (n - 1)
        p.co = (x0 + (x1 - x0) * u, y, z - sag * 4 * u * (1 - u), 1)
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    cu.materials.append(W.mat("wire_black", (0.05, 0.05, 0.05), 0.6))
    return o


def wire_bounce(o, x0, x1, z, sag0, sag1, f0, nf, freq=1.6, damp=1.3):
    """重さが変わった電線：たるみが sag0 → sag1 へ、行き過ぎながら（ゆれながら）落ちつく。"""
    pts = o.data.splines[0].points
    n = len(pts)
    for f in [max(1, f0 - 1)] + list(range(f0, nf + 1, 2)):
        t = max(0.0, (f - f0) / FPS)
        sag = sag1 + (sag0 - sag1) * math.cos(2 * math.pi * freq * t) * math.exp(-damp * t) if f >= f0 else sag0
        for i, p in enumerate(pts):
            u = i / (n - 1)
            p.co = (p.co[0], p.co[1], z - sag * 4 * u * (1 - u), 1)
            p.keyframe_insert("co", frame=f)


def wire_scene(nf, f_event, arrive=False):
    dusk(0.65)
    village(field=False)
    rice_field((-14, 14, -2, 30), 7000, avoid=None, seed=8)
    span = (-15.0, 15.0)
    z0 = 6.6
    for k, (y, nb) in enumerate(((6.0, 14), (6.7, 9))):
        sag_with, sag_without = 0.62, 0.56
        o = wire_curve(span[0], span[1], y, z0 + k * 0.05, sag_with if not arrive else sag_without, name=f"wire{k}")
        r = random.Random(4 + k)
        xs = sorted(r.uniform(-1.3, 1.5) for _ in range(nb))
        pts = []
        for x in xs:
            u = (x - span[0]) / (span[1] - span[0])
            pts.append((x, y, z0 + k * 0.05 - sag_with * 4 * u * (1 - u) + 0.008, math.radians(r.uniform(150, 210))))
        birds = perched(pts, name=f"wb{k}_", scale=1.0)
        for j, b in enumerate(birds):
            peck(b, nf, seed=j + 10 * k, period=30)
        if arrive:
            wire_bounce(o, span[0], span[1], z0 + k * 0.05, sag_without, sag_with, f_event + 6, nf)
            for b in birds:
                C.show_between(b, f_event + 4, None)
            FJ.sparkle_points([Vector(p[:3]) for p in pts], f_event - 24, 0.025, 0.25, mode="in", seed=7 + k, life=(0.7, 0.9))
        else:
            wire_bounce(o, span[0], span[1], z0 + k * 0.05, sag_with, sag_without, f_event + 3, nf)
            for b in birds:
                C.show_between(b, None, f_event + 2)
            FJ.sparkle_points([Vector(p[:3]) for p in pts], f_event, 0.025, 0.3, seed=7 + k, life=(0.6, 1.1), trail=(2,))
            feathers([p[:3] for p in pts[::2]], f_event + 2, nf, seed=11 + k, name=f"wf{k}_")
    F._cyl(0.14, 0.11, 8.5, (span[1], 6.3, 4.25), W.mat("pole_conc", (0.62, 0.62, 0.60), 0.9), verts=8)
    W.box((span[1], 6.35, 7.3), (0.1, 1.6, 0.1), W.mat("pole_conc", (0.62, 0.62, 0.60), 0.9), bevel=0)


def s02_wire(nf):
    wire_scene(nf, 10)
    W.camera((0.9, 4.2, 6.1), (0.0, 6.2, 6.0), lens=42)
    cut(66, (4.0, 1.0, 5.6), (0.0, 6.3, 6.0), lens=30, orbit=4, push=0.05)
    return nf


def grains(hand, f0, nf, n=40, seed=1, name="grain"):
    """投げた米つぶ：放物線をえがいて落ちる（重力）。地面で止まる。"""
    r = random.Random(seed)
    m = W.mat("rice_grain", (0.97, 0.96, 0.92), 0.5)
    boxes = []
    for k in range(n):
        v = Vector((r.uniform(-0.8, 0.8), r.uniform(1.6, 3.0), r.uniform(1.0, 2.2)))
        o = W.box((0, 0, 0), (0.012, 0.02, 0.01), m, bevel=0, name=f"{name}{f0}_{k}")
        o.visible_shadow = False
        o.scale = (1e-4,) * 3
        o.keyframe_insert("scale", frame=max(1, f0 - 1))
        o.scale = (1.5, 1.5, 1.5)
        for f in range(f0, nf + 1, 2):
            t = (f - f0) / FPS
            p = Vector(hand) + v * t + Vector((0, 0, -4.9 * t * t))
            if p.z <= 0.01:
                tl = (v.z + math.sqrt(v.z * v.z + 2 * 9.8 * (hand[2] - 0.01))) / 9.8
                p = Vector(hand) + v * tl + Vector((0, 0, -4.9 * tl * tl))
                p.z = 0.01
            o.location = p
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("scale", frame=f)
        boxes.append(o)
    return boxes


def garden(nf, birds=False):
    sky(lo=(1.0, 0.90, 0.75), hi=(0.48, 0.64, 0.88), strength=0.6)
    sun(30, 25, 4.6, (1.0, 0.90, 0.75))
    FJ.engawa_set()
    gm = person((0.4, 0.85, 0.45), 0, seed=31, arms="wave", alt="hold", nf=nf, period=20, look=GRANDMA)
    for k, f0 in enumerate((14, 54, 94)):
        grains((0.75, 1.1, 1.5), f0, nf, seed=k, name=f"g{k}_")
    if birds:
        r = random.Random(5)
        bs = perched([(r.uniform(-1.2, 1.6), r.uniform(2.0, 3.6), 0.0, r.uniform(0, 6.3)) for _ in range(9)], name="gb", scale=1.2)
        for j, b in enumerate(bs):
            peck(b, nf, seed=j, period=14)
    fill((0.6, 4.0, 1.8), (0.4, 0.85, 1.5), power=70)
    return gm


def s03_feed(nf):
    garden(nf)
    W.camera((1.6, 4.6, 1.2), (0.4, 1.0, 1.0), lens=30)
    cut(76, (-1.4, 3.8, 0.6), (0.4, 2.6, 0.1), lens=28, orbit=4, push=0.05)
    return nf


def s04_scare(nf):
    sky(lo=(1.0, 0.88, 0.70), hi=(0.45, 0.62, 0.88), strength=0.55)
    sun(28, 200, 4.8, (1.0, 0.88, 0.70))
    village(harvested=True)
    k = kakashi((0.9, 4.0, 0.0), 180)
    # 引きぬく：少し持ち上がって、かたむく
    k.keyframe_insert("location", frame=40)
    k.keyframe_insert("rotation_euler", frame=40)
    k.location.z = 0.45
    k.rotation_euler.y = math.radians(-12)
    k.keyframe_insert("location", frame=70)
    k.keyframe_insert("rotation_euler", frame=70)
    farmer((0.1, 3.9, 0.0), 160, nf, arms="hold", alt=None)
    W.camera((0.4, 0.2, 1.4), (0.5, 4.0, 1.4), lens=30)
    cut(76, (-2.6, 1.4, 1.3), (1.0, 8.0, 1.6), lens=24, orbit=4, push=0.05)
    return nf


def haiku_texture():
    from PIL import Image, ImageDraw, ImageFont
    p = os.path.join(ASSETS, "haiku_board.png")
    if os.path.exists(p):
        return p
    os.makedirs(ASSETS, exist_ok=True)
    im = Image.new("RGB", (1200, 600), (32, 70, 52))
    d = ImageDraw.Draw(im)
    fnt = ImageFont.truetype(FONT, 78)
    fnt.set_variation_by_axes([700])
    small = ImageFont.truetype(FONT, 56)
    small.set_variation_by_axes([600])
    cols = ["雀の子", "そこのけそこのけ", "御馬が通る"]
    x = 900
    for col in cols:
        y = 60
        for ch in col:
            d.text((x, y), ch, font=fnt, fill=(240, 240, 232), anchor="mt")
            y += 64
        x -= 150
    y = 300
    for ch in "小林一茶":
        d.text((360, y), ch, font=small, fill=(240, 240, 232), anchor="mt")
        y += 60
    im.save(p)
    return p


def classroom(nf, kids_look="window", outside_birds=False):
    SG.room((0.95, 0.90, 0.82), 0.9)
    SG.window_sun(28, 270, 3.0)
    floor = W.mat("floor_wood", (0.62, 0.46, 0.30), 0.6)
    wall = W.mat("class_wall", (0.90, 0.88, 0.82), 0.9)
    W.box((0, 2, -0.05), (10, 10, 0.1), floor, bevel=0)
    W.box((0, 7.0, 1.6), (10, 0.2, 3.2), wall, bevel=0)
    W.box((5.0, 2, 1.6), (0.2, 10, 3.2), wall, bevel=0)
    for z in (0.45, 2.75):
        W.box((-5.0, 2, z), (0.2, 10, 0.9 if z < 1 else 0.9), wall, bevel=0)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0.6, 6.88, 1.75))
    b = bpy.context.object
    b.scale = (3.4, 1.7, 1)
    b.rotation_euler.x = math.radians(90)
    b.data.materials.append(C.img_mat("haiku", haiku_texture()))
    desk = W.mat("desk", (0.72, 0.58, 0.40), 0.6)
    metal = W.mat("desk_leg", (0.35, 0.36, 0.38), 0.5)
    r = random.Random(6)
    kids = []
    for row in range(3):
        for col in range(4):
            x, y = -2.6 + col * 1.5, 1.2 + row * 1.4
            W.box((x, y + 0.35, 0.68), (0.6, 0.45, 0.04), desk, bevel=0.01)
            W.box((x, y + 0.35, 0.34), (0.05, 0.05, 0.68), metal, bevel=0)
            fac = 270 + r.uniform(-25, 15) if kids_look == "window" else r.uniform(-10, 10)
            kids.append(person((x, y, 0.28), fac, seed=10 + row * 4 + col, pose="sit", scale=0.72, look=KIDS[(row + col) % 4],
                               arms="down"))
    person((1.4, 6.2, 0), 200, seed=33, arms=("down", "wave"), look=TEACHER)
    for k in range(3):     # 窓
        W.box((-5.0, -1.5 + k * 3.0, 1.6), (0.05, 0.12, 1.4), W.mat("frame_w", (0.85, 0.85, 0.82), 0.5), bevel=0)
    return kids


def s05_issa(nf):
    classroom(nf)
    W.camera((0.9, 3.2, 1.55), (0.5, 6.9, 1.8), lens=32)
    cut(70, (-4.3, 6.2, 1.3), (-0.5, 2.2, 0.8), lens=26, orbit=4, push=0.05)
    return nf


def snowfall(center, extent, n, nf, seed=8):
    r = random.Random(seed)
    m = W.mat("snowflake", (1, 1, 1), 0.8, emit=(1, 1, 1), emit_strength=0.4)
    for layer in range(3):
        pts = [(center[0] + r.uniform(-1, 1) * extent[0], center[1] + r.uniform(-1, 1) * extent[1],
                center[2] + r.uniform(-1, 1) * extent[2], r.uniform(0.012, 0.025), (1, 1, 1)) for _ in range(n // 3)]
        o = C.multi_ball(pts, m, f"snow{layer}", sub=1)
        o.visible_shadow = False
        for f in (1, nf):
            t = (f - 1) / FPS
            o.location = (0.3 * t * (layer + 1) * 0.5, 0, -0.8 * t * (0.8 + layer * 0.15))
            o.keyframe_insert("location", frame=f)


def s06_fukura(nf):
    SG.overcast(1.0, col_lo=(0.82, 0.86, 0.92), col_hi=(0.55, 0.62, 0.75), sun_s=2.0)
    C.grass_ground(col=(0.90, 0.92, 0.96), name="snow_flat", size=900)
    r = random.Random(3)
    walls = W.mat("wall_a", (0.84, 0.80, 0.72))
    snowroof = W.mat("snow_roof", (0.92, 0.94, 0.98), 0.8)
    for k in range(8):
        x, y = r.uniform(-30, 30), r.uniform(14, 45)
        W.box((x, y, 2.5), (8, 7, 5), walls, bevel=0.05)
        W.box((x, y, 5.7), (9, 8, 1.6), snowroof, bevel=0.3)
    span = (-15.0, 15.0)
    o = wire_curve(span[0], span[1], 6.0, 6.6, 0.56, name="wire_snow")
    _ = o
    F._cyl(0.14, 0.11, 8.5, (span[1], 6.3, 4.25), W.mat("pole_conc", (0.62, 0.62, 0.60), 0.9), verts=8)
    # 白い線：いたはずの「ふくら雀」（羽に空気をためて、丸くふくらむ）
    for k, x in enumerate((-1.6, -0.9, -0.2, 0.6, 1.3)):
        u = (x - span[0]) / (span[1] - span[0])
        g = C.link_copy(sparrow_mesh("puff"), (x, 6.0, 6.6 - 0.56 * 4 * u * (1 - u) + 0.008), f"ghost_sp{k}")
        g.data = g.data.copy()
        g.rotation_euler.z = math.radians(180 + (k - 2) * 8)
        g.scale = (1.3,) * 3
        SG.ghost(g, col=(0.80, 0.92, 1.0), strength=1.4, thick=0.002)
    snowfall((0, 5, 4), (6, 6, 4), 900, nf)
    person((1.2, 3.2, 0), 200, seed=12, arms="down", look={"top": (0.75, 0.20, 0.20), "bottom": (0.25, 0.25, 0.30)}, scale=0.75)
    fill((2.0, 0.8, 1.6), (1.2, 3.2, 1.0), power=60, col=(0.9, 0.93, 1.0))
    W.camera((0.1, 3.6, 6.12), (-0.2, 6.0, 6.08), lens=35)
    cut(70, (2.8, -0.6, 1.0), (0.4, 6.0, 4.5), lens=26, orbit=4, push=0.05)
    return nf


def cabbage(loc, holes=True):
    g1 = W.mat("cabbage", (0.55, 0.75, 0.38), 0.7)
    g2 = W.mat("cabbage_out", (0.40, 0.62, 0.30), 0.8)
    F._ball(0.16, (loc[0], loc[1], 0.15), g1, sub=2)
    r = random.Random(int(loc[0] * 100 + loc[1] * 10))
    for k in range(6):
        a = k * 1.05 + r.uniform(-0.2, 0.2)
        F._ball(0.16, (loc[0] + 0.12 * math.cos(a), loc[1] + 0.12 * math.sin(a), 0.1), g2, sub=1, sc=(1.2, 1.2, 0.35))
    if holes:
        hm = W.mat("leaf_hole", (0.12, 0.16, 0.08), 0.9)
        for k in range(5):
            a = r.uniform(0, 6.3)
            F._ball(0.018, (loc[0] + 0.2 * math.cos(a), loc[1] + 0.2 * math.sin(a), 0.135), hm, sub=1, sc=(1, 1, 0.3))


def caterpillar(loc, rz, nf, seed=0):
    """青虫：体を波打たせて少しずつ進む。"""
    m = W.mat("aomushi", (0.45, 0.78, 0.25), 0.6)
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    root.rotation_euler.z = rz
    segs = []
    for k in range(7):
        s = F._ball(0.016, (0, -k * 0.022, 0.016), m, sub=1)
        s.parent = root
        s.location = (0, -k * 0.022, 0.016)
        segs.append(s)
    for f in range(1, nf + 1, 3):
        t = (f - 1) / FPS
        for k, s in enumerate(segs):
            s.location.z = 0.016 + 0.012 * max(0.0, math.sin(4 * t - k * 0.8 + seed))
            s.keyframe_insert("location", frame=f)
        root.location = (loc[0] - math.sin(rz) * 0.01 * t, loc[1] + math.cos(rz) * 0.01 * t, loc[2])
        root.keyframe_insert("location", frame=f)


def butterflies(n, nf, area, seed=4):
    r = random.Random(seed)
    m = W.mat("monshiro", (0.97, 0.97, 0.92), 0.7)
    for k in range(n):
        wl = W.box((0, 0, 0), (0.05, 0.035, 0.002), m, bevel=0, name=f"bf{k}")
        x0, y0, z0 = r.uniform(area[0], area[1]), r.uniform(area[2], area[3]), r.uniform(0.3, 1.2)
        ph = r.uniform(0, 6.3)
        for f in range(1, nf + 1, 2):
            t = (f - 1) / FPS
            wl.location = (x0 + 0.5 * math.sin(0.8 * t + ph), y0 + 0.4 * math.cos(0.6 * t + ph), z0 + 0.15 * math.sin(3 * t + ph))
            wl.rotation_euler = (0, 0.9 * math.sin(14 * t + ph), 0.8 * t + ph)
            wl.keyframe_insert("location", frame=f)
            wl.keyframe_insert("rotation_euler", frame=f)


def s07_spring(nf):
    sky(lo=(1.0, 0.92, 0.78), hi=(0.48, 0.64, 0.88), strength=0.6)
    sun(40, 200, 4.6, (1.0, 0.92, 0.78))
    C.grass_ground(col=(0.36, 0.28, 0.18), name="dirt_garden", size=300)
    for row in range(3):
        W.box((0, 1.0 + row * 0.9, 0.06), (6, 0.6, 0.12), W.mat("dirt_ridge", (0.40, 0.30, 0.20), 1.0), bevel=0.05)
        for k in range(8):
            cabbage((-2.8 + k * 0.75, 1.0 + row * 0.9, 0))
    r = random.Random(2)
    for k in range(26):
        cx, cy = (-0.55, 1.0) if k < 5 else ((-1.3, 1.0) if k < 8 else (-2.8 + r.randint(0, 7) * 0.75, 1.0 + r.randint(0, 2) * 0.9))
        a = r.uniform(0, 6.3)
        rr = 0.1 if k < 8 else 0.17
        caterpillar((cx + rr * math.cos(a), cy + rr * math.sin(a), 0.2 if k < 8 else 0.13), r.uniform(0, 6.3), nf, seed=k)
    butterflies(10, nf, (-3, 3, 0.5, 3.5))
    W.box((0, 6.5, 0.6), (14, 0.1, 1.2), W.mat("fence_w", (0.70, 0.62, 0.50), 0.8), bevel=0)
    FJ.town(seed=5, y=(12, 120), x=(-80, 80), n=60)
    person((0.6, 3.9, 0), 190, seed=31, arms="head", look=GRANDMA)
    W.camera((-0.9, 0.3, 0.42), (-0.6, 1.0, 0.15), lens=40)
    cut(76, (1.2, -0.6, 1.3), (0.6, 3.9, 1.1), lens=28, orbit=4, push=0.05, focus=(0.6, 3.9, 1.4))
    return nf


def hoppers(path_pts, nf, seed=5, n=60, name="hop"):
    """バッタ・イナゴ：人が近づくと、放物線をえがいてはね上がる。path_pts = [(コマ, x, y)] 人の通り道。"""
    r = random.Random(seed)
    m = W.mat("inago", (0.45, 0.58, 0.20), 0.6)
    me = None
    for k in range(n):
        f0, x, y = r.choice(path_pts)
        x += r.uniform(-1.2, 1.2)
        y += r.uniform(0.3, 1.5)
        if me is None:
            o = F._ball(0.012, (0, 0, 0), m, sub=1, sc=(0.6, 2.6, 0.7))
            me = o.data
        else:
            o = C.link_copy(me, (0, 0, 0), f"{name}{k}")
        v = Vector((r.uniform(-1.2, 1.2), r.uniform(0.5, 2.0), r.uniform(2.0, 3.2)))
        p0 = Vector((x, y, 0.6))
        o.scale = (1e-4,) * 3
        o.keyframe_insert("scale", frame=max(1, f0 - 1))
        o.scale = (1.6,) * 3
        T = 2 * v.z / 9.8
        for f in range(f0, min(nf, f0 + int(T * FPS) + 2) + 1, 1):
            t = min((f - f0) / FPS, T)
            o.location = p0 + v * t + Vector((0, 0, -4.9 * t * t))
            o.rotation_euler.z = math.atan2(-v.x, v.y)
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("rotation_euler", frame=f)
            o.keyframe_insert("scale", frame=f)
        o.scale = (1e-4,) * 3
        o.keyframe_insert("scale", frame=min(nf, f0 + int(T * FPS) + 3))


def gnats(center, extent, n, nf, seed=6, name="unka"):
    """稲の上を飛ぶ小さな虫（ウンカ）の群れ。"""
    r = random.Random(seed)
    m = W.mat("gnat", (0.15, 0.15, 0.10), 0.6)
    for layer in range(4):
        pts = [(r.uniform(-1, 1) * extent[0], r.uniform(-1, 1) * extent[1], r.uniform(-1, 1) * extent[2], 0.006, (1, 1, 1))
               for _ in range(n // 4)]
        o = C.multi_ball(pts, m, f"{name}{layer}", sub=1)
        o.visible_shadow = False
        ph = r.uniform(0, 6.3)
        for f in range(1, nf + 1, 3):
            t = (f - 1) / FPS
            o.location = (center[0] + 0.3 * math.sin(1.3 * t + ph), center[1] + 0.3 * math.cos(1.1 * t + ph),
                          center[2] + 0.1 * math.sin(2.1 * t + ph))
            o.keyframe_insert("location", frame=f)


def s08_paddy(nf):
    sky(lo=(1.0, 0.88, 0.70), hi=(0.42, 0.60, 0.88), strength=0.6)
    sun(35, 195, 4.8, (1.0, 0.88, 0.72))
    village(green=True)
    leaf_bad = W.mat("rice_bad", (0.62, 0.55, 0.22), 0.9)
    r = random.Random(7)
    C.multi_ball([(r.choice((-1, 1)) * r.uniform(1.5, 9), r.uniform(7, 18), r.uniform(0.7, 0.85), r.uniform(0.12, 0.25),
                   (1.4, 1.0, 0.4)) for _ in range(40)], leaf_bad, "damaged")
    walker = farmer((0.0, 6.0, 0.24), 180, nf, arms="down", alt=None)
    walker.keyframe_insert("location", frame=1)
    walker.location.y = 3.0
    walker.keyframe_insert("location", frame=nf)
    path = [(f, 0.0, 6.0 - 3.0 * (f - 1) / nf) for f in range(1, nf - 20, 3)]
    hoppers([(f, x - 0.3, y - 1.2) for f, x, y in path], nf, n=90)
    gnats((1.5, 4.0, 1.1), (2.0, 2.0, 0.4), 600, nf)
    gnats((-2.0, 7.0, 1.2), (2.0, 2.0, 0.4), 500, nf, seed=8, name="unkb")
    W.camera((0.6, -0.6, 1.5), (0.0, 6.0, 1.2), lens=30)
    cut(90, (-2.4, 2.4, 0.9), (0.6, 4.6, 0.8), lens=26, orbit=4, push=0.05)
    return nf


def s09_china(nf):
    sky(lo=(0.95, 0.85, 0.70), hi=(0.60, 0.62, 0.66), strength=0.7)
    sun(35, 190, 4.4, (1.0, 0.92, 0.80))
    C.grass_ground(col=(0.50, 0.42, 0.26), name="dirt_cn", size=900)
    rice_field((-14, 14, 4, 40), 9000, col=(0.72, 0.62, 0.30), ear=(0.80, 0.68, 0.32), seed=12)
    r = random.Random(9)
    red = W.mat("flag_red", (0.80, 0.12, 0.10), 0.7)
    pan = W.mat("pan", (0.35, 0.35, 0.36), 0.3)
    for k in range(14):
        x, y = -6 + k * 0.9 + r.uniform(-0.2, 0.2), 1.0 + r.uniform(-0.6, 1.2)
        p = person((x, y, 0), 180 + r.uniform(-25, 25), seed=40 + k, arms="up", alt="down", nf=nf, period=18 + k % 4, look=CN)
        disc = F._cyl(0.14, 0.14, 0.03, (0.3, 0.1, 1.95), pan, verts=10)
        disc.parent = p.children[0]
        if k % 4 == 0:
            F._cyl(0.02, 0.02, 2.4, (x + 0.3, y, 1.2), W.mat("flagpole", (0.5, 0.4, 0.3), 0.8), verts=5)
            W.box((x + 0.75, y, 2.15), (0.9, 0.02, 0.55), red, bevel=0)
    # 空をおおう虫の群れが、奥から田んぼへ降りてくる
    m = W.mat("locust_dark", (0.20, 0.18, 0.12), 0.8)
    for layer in range(6):
        pts = [(r.uniform(-25, 25), r.uniform(-12, 12), r.uniform(-4, 4), 0.07, (1, 2, 1)) for _ in range(600)]
        o = C.multi_ball(pts, m, f"swarm{layer}", sub=1)
        o.visible_shadow = False
        for f, (y, z) in ((1, (140, 30)), (50, (110, 22)), (nf, (40 + layer * 4, 6 + layer))):
            o.location = (r.uniform(-3, 3), y + layer * 6, z)
            o.keyframe_insert("location", frame=f)
    W.camera((1.0, -6.0, 1.6), (0.0, 30.0, 6.0), lens=24)
    cut(80, (3.0, -1.0, 1.4), (-1.0, 1.4, 1.6), lens=30, orbit=4, push=0.05)
    return nf


def drone(nf, path, z=2.2, name="drone"):
    body = W.mat("drone_white", (0.92, 0.92, 0.94), 0.4)
    dark = W.mat("drone_dark", (0.15, 0.15, 0.16), 0.5)
    blur = W.mat("rotor_blur", (0.2, 0.2, 0.2), 0.5, alpha=0.35)
    bpy.ops.object.empty_add(location=(0, 0, z))
    root = bpy.context.object
    parts = [W.box((0, 0, 0), (0.5, 0.5, 0.2), body, bevel=0.06), W.box((0, 0, -0.18), (0.3, 0.3, 0.2), W.mat("tank", (0.3, 0.6, 0.85), 0.5), bevel=0.04)]
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(W.box((sx * 0.45, sy * 0.45, 0.02), (0.6, 0.06, 0.05), dark, rot=(0, 0, math.radians(45 * sx * sy)), bevel=0))
            parts.append(F._cyl(0.38, 0.38, 0.01, (sx * 0.7, sy * 0.7, 0.1), blur, verts=16))
    for o in parts:
        o.parent = root
    for f in (1, nf):
        u = (f - 1) / max(1, nf - 1)
        root.location = (path[0][0] + (path[1][0] - path[0][0]) * u, path[0][1] + (path[1][1] - path[0][1]) * u, z)
        root.keyframe_insert("location", frame=f)
    return root


def s10_drone(nf):
    sky(lo=(1.0, 0.88, 0.70), hi=(0.42, 0.60, 0.88), strength=0.6)
    sun(35, 195, 4.8, (1.0, 0.88, 0.72))
    village(green=True)
    drone(nf, ((-3.0, 5.5), (3.0, 5.5)))
    r = random.Random(4)
    spawns = []
    for f in range(1, nf, 1):
        u = (f - 1) / max(1, nf - 1)
        x = -3.0 + 6.0 * u
        spawns.append((f, (x + r.uniform(-0.6, 0.6), 5.5 + r.uniform(-0.6, 0.6), 1.7)))
    puffs(spawns, nf, (0.0, 0.0, -0.9), (0.18, 0.35), grow=2.6, rate=1.5, mat=F.puff_mat("mist", (0.95, 0.96, 1.0), 0.22),
          name="mist", seed=4, life=50)
    farmer((1.8, 2.2, 0.24), 200, nf, arms="hold", alt=None)
    W.camera((1.6, -1.4, 1.3), (0.0, 5.5, 2.0), lens=26)
    cut(70, (0.2, 0.0, 1.5), (1.8, 2.2, 1.5), lens=36, orbit=4, push=0.05, focus=(1.8, 2.2, 1.6))
    return nf


def poster_texture():
    from PIL import Image, ImageDraw, ImageFont
    p = os.path.join(ASSETS, "suzume_poster.png")
    if os.path.exists(p):
        return p
    os.makedirs(ASSETS, exist_ok=True)
    im = Image.new("RGB", (600, 800), (250, 245, 225))
    d = ImageDraw.Draw(im)
    d.ellipse((150, 250, 450, 520), fill=(150, 100, 60))
    d.ellipse((230, 160, 400, 330), fill=(130, 70, 40))
    d.ellipse((250, 230, 300, 280), fill=(250, 250, 245))
    d.ellipse((330, 230, 380, 280), fill=(250, 250, 245))
    d.ellipse((265, 245, 285, 265), fill=(20, 20, 20))
    d.ellipse((345, 245, 365, 265), fill=(20, 20, 20))
    d.polygon([(400, 270), (450, 285), (400, 295)], fill=(60, 50, 40))
    d.ellipse((220, 380, 380, 500), fill=(235, 225, 205))
    fnt = ImageFont.truetype(FONT, 72)
    fnt.set_variation_by_axes([800])
    d.text((300, 640), "すずめの", font=fnt, fill=(200, 60, 40), anchor="mm")
    d.text((300, 730), "がっこう", font=fnt, fill=(200, 60, 40), anchor="mm")
    im.save(p)
    return p


def s11_song(nf):
    SG.room((0.98, 0.90, 0.80), 0.9)
    SG.window_sun(30, 160, 3.0)
    W.box((0, 2, -0.05), (10, 10, 0.1), W.mat("floor_wood", (0.62, 0.46, 0.30), 0.6), bevel=0)
    W.box((0, 6.0, 1.6), (10, 0.2, 3.2), W.mat("kinder_wall", (0.98, 0.92, 0.80), 0.9), bevel=0)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(-1.4, 5.88, 1.7))
    ps = bpy.context.object
    ps.scale = (0.9, 1.2, 1)
    ps.rotation_euler.x = math.radians(90)
    ps.data.materials.append(C.img_mat("poster", poster_texture()))
    W.box((2.2, 5.4, 0.55), (1.6, 0.6, 1.1), W.mat("piano", (0.12, 0.10, 0.10), 0.3), bevel=0.03)
    person((2.2, 4.6, 0), 200, seed=34, arms="hold", look=TEACHER)
    for k in range(6):
        person((-2.2 + k * 0.75, 3.0 + 0.25 * (k % 2), 0), 180 + (k - 2.5) * 5, seed=50 + k, arms="up", alt="down", nf=nf,
               period=20 + k, look=KIDS[k % 4], scale=0.62)
    W.camera((0.0, -0.8, 1.0), (-0.4, 3.4, 0.9), lens=28)
    cut(70, (-2.6, 1.0, 1.2), (-1.4, 5.8, 1.7), lens=30, orbit=4, push=0.05)
    return nf


def s12_return(nf):
    dusk()
    village()
    f_back = 61 + 8
    N = 520
    P = flock_track(N, nf, 3, lambda t: sky_flock_center(t + 2.0), sky_flock_size)
    objs = fly_objects(P, nf, f_on=f_back, scale=1.4)
    _ = objs
    FJ.sparkle_points([Vector(tuple(P[i, f_back])) for i in range(0, N, 2)], f_back - 30, 0.08, 1.5, mode="in", seed=4,
                      life=(0.8, 1.0))
    farmer((2.2, 6.0, 0.24), 200, nf, look=FARMER_OLD)
    kakashi((-2.8, 9.0, 0.0), 190)
    fill((1.0, 3.0, 2.0), (2.2, 6.0, 1.5), power=80)
    cut(1, (-2.0, -4.5, 1.3), (-3.0, 30.0, 8.0), lens=26, orbit=0, push=0.0, fixat=1, focus="far")
    cut(121, (4.4, 2.4, 1.3), (1.0, 14.0, 4.0), lens=26, orbit=4, push=0.05)
    return nf


def j1_chase(nf):
    dusk()
    village()
    P = flock_track(300, nf, 7, lambda t: (1.0 + 3 * math.sin(t), 9 + 2 * math.cos(t), 3.0 + 0.8 * math.sin(2 * t)),
                    lambda t: (3.0, 2.0, 1.0))
    fly_objects(P, nf, scale=1.3, flap_near=((2.0, 2.5, 1.5), 5.0))
    farmer((2.2, 6.0, 0.24), 200, nf, look=FARMER_OLD, period=18)
    fill((1.6, 3.4, 2.0), (2.2, 6.0, 1.5), power=90)
    W.camera((1.4, 2.6, 1.55), (2.2, 6.0, 1.6), lens=32)
    return nf


def j2_garden(nf):
    garden(nf, birds=True)
    W.camera((-1.2, 4.2, 0.9), (0.2, 2.0, 0.5), lens=28)
    return nf


def j3_wire(nf):
    wire_scene(nf, 12, arrive=True)
    W.camera((0.9, 4.2, 6.1), (0.0, 6.2, 6.0), lens=42)
    return nf


def j4_school(nf):
    classroom(nf)
    W.box((-5.3, 2.5, 0.88), (0.5, 9.0, 0.06), W.mat("sill", (0.80, 0.80, 0.78), 0.6), bevel=0.01)
    r = random.Random(3)
    birds = perched([(-5.35, 1.6 + k * 0.45 + r.uniform(-0.1, 0.1), 0.91, math.radians(r.uniform(60, 120))) for k in range(5)],
                    name="sill_b", scale=1.2)
    for j, b in enumerate(birds):
        peck(b, nf, seed=j, period=16)
    P = flock_track(30, nf, 9, lambda t: (-8.0 + 0.8 * math.sin(2 * t), 2.5 + 1.5 * t, 2.6), lambda t: (1.6, 1.4, 0.5))
    fly_objects(P, nf, scale=1.2)
    for k in range(4):
        person((-3.4 + k * 0.6, 1.4 + 0.5 * (k % 2), 0.0), 270 + (k - 1.5) * 10, seed=60 + k, arms="up", alt="down", nf=nf,
               period=18 + k, look=KIDS[k % 4], scale=0.7)
    W.camera((-6.6, 2.6, 1.45), (0.0, 2.2, 1.0), lens=28)
    return nf


def j5_wide(nf):
    dusk()
    village(road=True)
    P = flock_track(520, nf, 3, lambda t: sky_flock_center(t + 6.0), sky_flock_size)
    fly_objects(P, nf, scale=1.4)
    cast = [(-1.6, "up", "down", FARMER_OLD, 4), (-0.8, "wave", "up", GRANDMA, 31), (0.0, "up", "down", KIDS[0], 10),
            (0.8, "wave", "down", TEACHER, 33), (1.6, "up", "down", KIDS[2], 12)]
    for k, (x, a, alt, look, seed) in enumerate(cast):
        p = person((x, 3.0 + 0.4 * (k % 2), 0.06), 180 + (k - 2) * 6, seed=seed, arms=a, alt=alt, nf=nf, period=18 + k, look=look,
                   scale=0.72 if look in KIDS else 1.0)
        if seed == 4:
            straw_hat(p)
    fill((0.0, 0.5, 2.0), (0.0, 3.2, 1.4), power=90)
    W.camera((0.4, -1.6, 1.2), (-1.0, 30.0, 7.0), lens=24)
    return nf


SCENES = {k: v for k, v in globals().items() if callable(v) and k[:1] in "sj" and k[1:2].isdigit() and "_" in k}

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    first = int(sys.argv[4]) if len(sys.argv) > 4 else None
    last = int(sys.argv[5]) if len(sys.argv) > 5 else None
    W.reset()
    nf = TL.shot(name)["frames"]
    SCENES[name](nf)
    for cam in FJ.cams():      # 最初の5秒以外は、参考元に合わせておだやかに
        cam["orbit"] = min(cam.get("orbit", 13.0) * 0.55, 8.0)
        cam["push"] = min(cam.get("push", 0.3), 0.18)
    FJ.render(out, nf, step, first, last)
    print("rendered", name, flush=True)
