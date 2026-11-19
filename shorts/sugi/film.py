"""「もしも日本からスギが消えたら？」全場面の3D（Blender / bpy）。富士山版（../fuji/film.py）の部品を使う。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]
座標: z=上（m）。山はおおむね +y の奥。"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timeline as TL  # noqa: E402  （富士山版より先に読み込む＝こちらの時間割を使わせる）
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("fuji_film", os.path.join(HERE, "..", "fuji", "film.py"))
FJ = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(FJ)
C, W, F, bpy = FJ.C, FJ.W, FJ.F, FJ.bpy
from mathutils import Vector  # noqa: E402

FPS = TL.FPS
fr = C.frame_of
cut, sky, sun, day, room, window_sun = FJ.cut, FJ.sky, FJ.sun, FJ.day, FJ.room, FJ.window_sun


def person(loc, facing, pose="stand", **kw):
    """富士山版の人。頭の高さ（マスク・くしゃみ用）を覚えておく。"""
    root = FJ.person(loc, facing, pose=pose, **kw)
    root["hc0"] = 0.96 if pose == "sit" else 1.62
    return root
ASSETS = os.path.join(HERE, "assets")
FJ.ASSETS = ASSETS

FATHER = {"hair": (0.16, 0.15, 0.14), "top": (0.30, 0.36, 0.48), "bottom": (0.28, 0.27, 0.25)}
FATHER_OLD = {"hair": (0.66, 0.65, 0.63), "top": (0.30, 0.36, 0.48), "bottom": (0.28, 0.27, 0.25)}
MOTHER = {"top": (0.85, 0.55, 0.45), "bottom": (0.30, 0.30, 0.38), "hair": (0.12, 0.08, 0.06)}
DAUGHTER = {"top": (0.95, 0.80, 0.30), "bottom": (0.25, 0.35, 0.60)}
WORKER = {"top": (0.35, 0.42, 0.30), "bottom": (0.25, 0.27, 0.30)}
BREWER = {"top": (0.10, 0.14, 0.30), "bottom": (0.10, 0.14, 0.30), "hair": (0.12, 0.10, 0.09)}
HIKER = {"top": (0.80, 0.30, 0.20), "bottom": (0.25, 0.28, 0.32)}
ORANGE = {"top": (0.95, 0.50, 0.10), "bottom": (0.20, 0.22, 0.28)}
SUGI_SAT = 1.0


# ---------- メッシュを数字から作る（森を1つのメッシュにまとめて速くする） ----------
def ring(r, z, n, rot=0.0):
    return [(r * math.cos(rot + 2 * math.pi * k / n), r * math.sin(rot + 2 * math.pi * k / n), z) for k in range(n)]


def cone_geo(r1, r2, h, z0, n, mi, rot=0.0):
    """側面と底のある円すい台（r2=0 でとがる）。(頂点, 面, 材質番号) を返す。"""
    v = ring(r1, z0, n, rot)
    f = []
    if r2 <= 0:
        v.append((0, 0, z0 + h))
        f += [(k, (k + 1) % n, n) for k in range(n)]
    else:
        v += ring(r2, z0 + h, n, rot)
        f += [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
        f.append(tuple(range(2 * n - 1, n - 1, -1)))
    f.append(tuple(range(n - 1, -1, -1)))
    return v, f, [mi] * len(f)


def merge(parts):
    V, Fc, M = [], [], []
    for v, f, m in parts:
        o = len(V)
        V += v
        Fc += [tuple(i + o for i in face) for face in f]
        M += m
    return V, Fc, M


def sugi_geo(seed):
    """スギ1本（高さ1）：赤茶の幹＋細い円すいを重ねた濃い緑の葉。"""
    r = random.Random(seed)
    parts = [cone_geo(0.028, 0.016, 0.6, 0.0, 6, 0)]
    for k in range(4):
        rr = 0.14 * (1 - 0.2 * k) * r.uniform(0.9, 1.1)
        z0 = 0.2 + 0.17 * k
        top = 0.0 if k == 3 else rr * 0.3
        parts.append(cone_geo(rr, top, 0.33 if k < 3 else 0.42, z0, 7, 1, rot=r.uniform(0, 1)))
    return merge(parts)


def broad_geo(seed):
    """雑木（広葉樹）1本（高さ1）：丸い葉のかたまり。"""
    r = random.Random(seed)
    parts = [cone_geo(0.035, 0.02, 0.45, 0.0, 6, 0)]
    w = 0.33 * r.uniform(0.85, 1.15)
    parts.append(cone_geo(w * 0.55, w, 0.28, 0.32, 7, 1, rot=r.uniform(0, 1)))
    parts.append(cone_geo(w, 0.0, 0.42, 0.6, 7, 1, rot=r.uniform(0, 1)))
    return merge(parts)


def hinoki_geo(seed):
    """ヒノキ1本（高さ1）：スギより丸くて明るい緑。"""
    r = random.Random(seed)
    parts = [cone_geo(0.03, 0.018, 0.5, 0.0, 6, 0)]
    for k in range(3):
        rr = 0.2 * (1 - 0.22 * k) * r.uniform(0.9, 1.1)
        parts.append(cone_geo(rr * 0.6, rr, 0.18, 0.18 + 0.24 * k, 8, 1, rot=r.uniform(0, 1)))
        parts.append(cone_geo(rr, rr * 0.35 if k < 2 else 0.0, 0.2 if k < 2 else 0.3, 0.36 + 0.24 * k, 8, 1, rot=r.uniform(0, 1)))
    return merge(parts)


def mesh_obj(name, geo, mats, smooth=False):
    V, Fc, M = geo
    me = bpy.data.meshes.new(name)
    me.from_pydata(V, [], Fc)
    me.update()
    for m in mats:
        me.materials.append(m)
    for p, mi in zip(me.polygons, M):
        p.material_index = mi
        p.use_smooth = smooth
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    return o


def place(templates, pts):
    """pts = [(x, y, z, 高さ, 回転, 太さ)] に木のひな形を並べて1つの形に。"""
    parts = []
    for k, (x, y, z, h, rot, w) in enumerate(pts):
        V, Fc, M = templates[k % len(templates)]
        c, s = math.cos(rot), math.sin(rot)
        v2 = [(x + (vx * c - vy * s) * h * w, y + (vx * s + vy * c) * h * w, z + vz * h) for vx, vy, vz in V]
        parts.append((v2, Fc, M))
    return merge(parts)


def bark():
    return W.mat("sugi_bark", (0.36, 0.20, 0.12), 0.9)


def needle(col=(0.10, 0.25, 0.11)):
    return W.mat(f"sugi_needle_{col}", col, 0.85)


def sugi_forest(pts, name="sugi", col=(0.10, 0.25, 0.11)):
    return mesh_obj(name, place([sugi_geo(s) for s in range(4)], pts), [bark(), needle(col)])


def broad_forest(pts, name="broad", seed=0):
    r = random.Random(seed)
    cols = [(0.22, 0.36, 0.13), (0.30, 0.40, 0.14), (0.20, 0.30, 0.12)]
    out = []
    for i, col in enumerate(cols):
        sub = [p for p in pts if r.random() < 1 / (len(cols) - i)] if i < len(cols) - 1 else pts
        pts = [p for p in pts if p not in sub]
        if sub:
            out.append(mesh_obj(f"{name}{i}", place([broad_geo(s) for s in range(3)], sub),
                                [W.mat("broad_trunk", (0.30, 0.22, 0.15), 0.9), W.mat(f"leafy_b{i}", col, 0.9)]))
    return out


def hinoki_forest(pts, name="hinoki"):
    return mesh_obj(name, place([hinoki_geo(s) for s in range(3)], pts),
                    [bark(), W.mat("hinoki_leaf", (0.14, 0.32, 0.12), 0.85)])


def ghost(o, col=(0.85, 0.95, 1.0), strength=2.2, thick=0.04):
    """白い線だけ（ここにあった木を図で見せる）。"""
    o.data.materials.clear()
    o.data.materials.append(W.mat(f"ghost_{col}", col, emit=col, emit_strength=strength))
    for p in o.data.polygons:
        p.material_index = 0
    wf = o.modifiers.new("wf", "WIREFRAME")
    wf.thickness = thick
    o.visible_shadow = False
    return o


# ---------- 山（高さの関数から地形を作る） ----------
def mt_h(x, y):
    d = y - 230.0
    if d <= 0:
        return -1.0
    rise = 230 * (1 - math.exp(-d / 260))
    rid = 1 + 0.30 * math.sin(x / 120 + 0.6) + 0.18 * math.sin(x / 45 + y / 85) + 0.10 * math.sin(x / 19 - y / 27)
    e = min(1.0, d / 60.0)
    return rise * rid * e * e


def sugi_zone(x, y):
    return math.sin(x / 85 + 1.3) + math.sin(y / 60 - x / 150) + 0.6 * math.sin(x / 33 + y / 41) > -0.45


def terrain(hf, x0, x1, y0, y1, step, zone=None, name="terrain", cols=((0.22, 0.33, 0.13), (0.40, 0.29, 0.19))):
    nx, ny = int((x1 - x0) / step) + 1, int((y1 - y0) / step) + 1
    V = [(x0 + i * step, y0 + j * step, hf(x0 + i * step, y0 + j * step)) for j in range(ny) for i in range(nx)]
    Fc, M = [], []
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = j * nx + i
            Fc.append((a, a + 1, a + nx + 1, a + nx))
            cx, cy = x0 + (i + 0.5) * step, y0 + (j + 0.5) * step
            M.append(1 if (zone and zone(cx, cy) and hf(cx, cy) > 2) else 0)
    return mesh_obj(name, (V, Fc, M), [W.mat("grass_hill", cols[0], 1.0), W.mat("dirt_slope", cols[1], 1.0)])


def valley(seed=1, cedar=True, broad=True, young=False, x_lim=(150, 0.42), y_max=1400):
    """山あいの町の奥の山。cedar=True でスギ林あり（消える前）。スギ林の位置と、木の点を返す。"""
    terrain(mt_h, -800, 800, 200, 1500, 14, zone=sugi_zone, name="mountain")
    r = random.Random(seed)
    spts, bpts = [], []
    y = 236.0
    while y < y_max:
        sp = 8.5 + (y - 230) * 0.011
        x = -800.0
        while x < 800:
            xx, yy = x + r.uniform(-0.4, 0.4) * sp, y + r.uniform(-0.4, 0.4) * sp
            if abs(xx) < x_lim[0] + x_lim[1] * yy:
                z = mt_h(xx, yy)
                if z > 3:
                    h = r.uniform(17, 25) * (1 + (yy - 230) / 1100)
                    p = (xx, yy, z - 1.0, h, r.uniform(0, 6.3), r.uniform(0.9, 1.15))
                    (spts if sugi_zone(xx, yy) else bpts).append(p)
            x += sp
        y += sp
    forest = sugi_forest(spts, "valley_sugi") if cedar else None
    if broad:
        broad_forest([(x, y, z, h * 0.7, a, w * 1.1) for x, y, z, h, a, w in bpts], "valley_broad", seed)
    if young:
        sugi_forest([(x, y, z, h * 0.25, a, w) for k, (x, y, z, h, a, w) in enumerate(spts) if k % 2 == 0],
                    "young", col=(0.18, 0.34, 0.14))
    FJ.foothills(seed=seed + 4, y=(1700, 2600), x=(-2500, 2500), n=14, col=(0.30, 0.40, 0.42), h=(300, 520))
    return forest, spts


def visible_pts(pts, cam, at, n, seed, max_d=1400):
    """カメラから見える木の点を n こ選ぶ（消える粒を、見える所に集める）。"""
    cam, at = Vector(cam), Vector(at)
    fwd = (at - cam).normalized()
    r = random.Random(seed)
    good = []
    for x, y, z, h, a, w in pts:
        p = Vector((x, y, z + h * 0.7))
        d = p - cam
        if d.length < max_d and d.normalized().dot(fwd) > 0.93:
            good.append(p)
    r.shuffle(good)
    return good[:n]


# ---------- 消える粒（金と緑の四角い粒） ----------
def green_particles():
    gold, _white = FJ.particle_meshes(False)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    tmp = bpy.context.object
    tmp.data.materials.append(W.mat("cube_green", (0.35, 0.85, 0.35), emit=(0.30, 0.95, 0.35), emit_strength=3.5))
    tmp.data.use_fake_user = True
    g = tmp.data
    bpy.data.objects.remove(tmp)
    FJ._PM[("cubes", False)] = [gold, g]


def burst(points, f0, size, rise, seed=1, center=None, spread=0.0, mode="out"):
    green_particles()
    FJ.sparkle_points(points, f0, size, rise, mode=mode, seed=seed, center=center, burst=spread, gold_ratio=0.45,
                      life=(0.7, 1.5) if mode == "out" else (0.8, 1.0))


# ---------- けむり（花粉・土ぼこり・雪けむり・しぶき） ----------
_ICO = {}


def ico_mesh():
    if "ico" not in _ICO:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0)
        o = bpy.context.object
        bpy.ops.object.shade_smooth()
        o.data.materials.append(W.mat("puff_base", (1, 1, 1)))
        o.data.use_fake_user = True
        _ICO["ico"] = o.data
        bpy.data.objects.remove(o)
    return _ICO["ico"]


def puffs(spawns, nf, wind, size, grow=2.5, rate=1.2, mat=None, sink_from=None, sink=0.0, rise=0.0, name="puff", seed=1,
          life=None):
    """spawns = [(コマ, 位置)]。生まれてから大きくなりながら風に流される。sink_from 以降はゆっくり下へ（花粉が沈む）。"""
    r = random.Random(seed)
    me = ico_mesh()
    for k, (f0, p) in enumerate(spawns):
        o = bpy.data.objects.new(f"{name}{k}", me)
        bpy.context.collection.objects.link(o)
        o.material_slots[0].link = 'OBJECT'
        o.material_slots[0].material = mat
        o.visible_shadow = False
        s0 = r.uniform(*size)
        wv = Vector(wind) * r.uniform(0.7, 1.3)
        p = Vector(p)
        o.scale = (1e-4,) * 3
        o.keyframe_insert("scale", frame=max(1, f0 - 1))
        end = nf if life is None else min(nf, f0 + life)
        for f in list(range(f0, end + 1, 3)) + [end]:
            t = (f - f0) / FPS
            sc = s0 * (0.35 + grow * (1 - math.exp(-t * rate)))
            if life is not None:
                sc *= max(0.0, 1 - ((f - f0) / life) ** 3)
            dz = rise * (1 - math.exp(-t * 1.5)) / 1.5
            if sink_from is not None and f > sink_from:
                dz -= sink * (f - max(sink_from, f0)) / FPS
            o.location = p + wv * t + Vector((0, 0, dz))
            o.scale = (max(sc, 1e-4), max(sc, 1e-4), max(sc * 0.75, 1e-4))
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("scale", frame=f)


def pollen_mat(alpha=0.32, col=(0.97, 0.82, 0.36)):
    return F.puff_mat(f"pollen_{alpha}_{col}", col, alpha)


def specks(center, extent, n, nf, col=(1.0, 0.88, 0.45), size=0.012, drift=(0.15, 0.0, -0.03), seed=3, name="speck"):
    """光に浮かぶ花粉のつぶ（カメラの近く）。"""
    r = random.Random(seed)
    m = W.mat(f"speck_{col}", col, emit=col, emit_strength=1.5)
    pts = [(center[0] + r.uniform(-1, 1) * extent[0], center[1] + r.uniform(-1, 1) * extent[1],
            center[2] + r.uniform(-1, 1) * extent[2], size * r.uniform(0.6, 1.4), (1, 1, 1)) for _ in range(n)]
    o = C.multi_ball(pts, m, name, sub=1)
    o.visible_shadow = False
    o.keyframe_insert("location", frame=1)
    o.location = Vector(drift) * (nf / FPS)
    o.keyframe_insert("location", frame=nf)
    return o


def rain(center, extent, n, nf, length=0.5, speed=9.0, seed=5):
    """雨のすじ（2枚を交互にずらして、切れ目なく降らせる）。"""
    r = random.Random(seed)
    m = W.mat("rain", (0.80, 0.85, 0.92), 0.2, emit=(0.75, 0.80, 0.90), emit_strength=0.6, alpha=0.5)
    H = extent[2] * 2
    per = max(2, int(H / speed * FPS))
    for layer in range(2):
        boxes = [(center[0] + r.uniform(-1, 1) * extent[0], center[1] + r.uniform(-1, 1) * extent[1],
                  center[2] + r.uniform(-1, 1) * extent[2], 0.012, 0.012, length, 0) for _ in range(n // 2)]
        o = C.multi_box(boxes, m, f"rain{layer}")
        o.visible_shadow = False
        for f in range(1, nf + per + 1, per):
            o.location.z = 0
            o.keyframe_insert("location", frame=f + layer * per // 2)
            o.location.z = -H / 2
            o.keyframe_insert("location", frame=f + layer * per // 2 + per - 1)
        FJ.set_interp(o, 'LINEAR')


def mask_on(root, off=None, col=(0.93, 0.96, 1.0)):
    """顔に白いマスク。off コマ目でずらしてはずす。"""
    body = root.children[0]
    m = W.mat(f"mask_{col}", col, 0.7)
    mk = W.box((0, 0.14, root.get("hc0", 1.62) - 0.05), (0.21, 0.1, 0.11), m, bevel=0.025)
    mk.parent = body
    if off:
        mk.keyframe_insert("location", frame=max(1, off - 1))
        mk.keyframe_insert("scale", frame=max(1, off + 4))
        mk.location.z -= 0.1
        mk.keyframe_insert("location", frame=off + 4)
        mk.scale = (1e-4,) * 3
        mk.keyframe_insert("scale", frame=off + 5)
    return mk


def sneeze(root, f0, spray=True):
    """はっ…くしょん：うしろにそって息をすい、前にガクッ。口から白いしぶき。"""
    for f, a in ((f0 - 14, 0), (f0 - 3, 7), (f0, -16), (f0 + 5, -8), (f0 + 14, 0)):
        root.rotation_euler.x = math.radians(a)
        root.keyframe_insert("rotation_euler", frame=max(1, f))
    if spray:
        m = F.puff_mat("spray", (1.0, 1.0, 1.0), 0.28)
        bpy.context.view_layer.update()
        mw = root.matrix_world
        face = mw @ Vector((0, 0.3, root.get("hc0", 1.62) - 0.1))
        fwd = (mw.to_3x3() @ Vector((0, 1, -0.25))).normalized()
        puffs([(f0 + k % 3, face) for k in range(8)], f0 + 30, fwd * 1.6, (0.04, 0.08), grow=2.0, rate=3.0, mat=m,
              name=f"spray{f0}", seed=f0, life=24)


def umbrella(root, col=(0.20, 0.30, 0.55)):
    m = W.mat(f"umb_{col}", col, 0.5)
    body = root.children[0]
    top = F._cyl(0.55, 0.0, 0.28, (0.2, 0.15, 2.05), m, verts=8)
    stick = F._cyl(0.012, 0.012, 0.75, (0.2, 0.15, 1.65), W.mat("umb_stick", (0.2, 0.2, 0.2), 0.5), verts=5)
    for o in (top, stick):
        o.parent = body


# ---------- 町と縁側 ----------
def porch_set():
    """秋田の家の縁側（富士山版の縁側に、ティッシュの箱）。奥の町と、スギの山。"""
    wood = W.mat("engawa", (0.55, 0.38, 0.22), 0.6)
    dark = W.mat("eave", (0.20, 0.17, 0.15), 0.8)
    W.box((0, -0.75, 0.22), (9, 3.5, 0.45), wood, bevel=0.01)
    for x in (-4.2, 4.2):
        W.box((x, 0.9, 1.6), (0.14, 0.14, 3.2), wood, bevel=0.01)
    W.box((0, -1.4, 3.6), (10, 2.4, 0.2), dark, rot=(math.radians(-6), 0, 0), bevel=0.02)
    shoji = W.mat("shoji", (1.0, 0.97, 0.9), emit=(1.0, 0.93, 0.8), emit_strength=0.3)
    W.box((0, -2.5, 1.5), (9, 0.05, 2.2), shoji, bevel=0)
    C.grass_ground(col=(0.30, 0.40, 0.14), tufts=4000, area=(-7, 7, 1.2, 14))
    W.box((0, 14, 0.6), (40, 1.2, 1.2), W.mat("leafy_hedge", (0.18, 0.34, 0.14), 0.9), bevel=0.2)
    for i, (x, y, h) in enumerate(((-5.5, 10, 4.5), (6.0, 11, 4.0))):
        C.tree((x, y, 0), h=h, seed=40 + i, crowns=[(0.17, 0.34, 0.12)])
    W.box((3.0, 4.5, 0.4), (0.8, 0.8, 0.8), W.mat("stone_lantern", (0.6, 0.6, 0.58), 0.9), bevel=0.05)
    FJ.engawa_props()
    # ティッシュの箱と、丸めたティッシュ（花粉症の朝）
    W.box((0.75, 0.75, 0.52), (0.24, 0.12, 0.1), W.mat("tissue_box", (0.35, 0.55, 0.85), 0.6), bevel=0.01)
    W.box((0.75, 0.75, 0.59), (0.1, 0.04, 0.05), W.mat("tissue", (1, 1, 1), 0.9), bevel=0.01)
    r = random.Random(3)
    C.multi_ball([(r.uniform(0.4, 1.3), r.uniform(0.3, 0.9), 0.48, 0.035, (1, 1, 0.8)) for _ in range(6)],
                 W.mat("tissue", (1, 1, 1), 0.9), "used_tissue")
    FJ.utility_poles([(-25, 20), (-8, 20), (9, 20), (26, 20)])
    FJ.town(seed=2, y=(40, 210), x=(-220, 220), n=110)


def morning(strength=0.5):
    sky(lo=(1.0, 0.86, 0.68), hi=(0.48, 0.64, 0.88), strength=strength)
    return sun(22, 160, 4.8, (1.0, 0.84, 0.64))      # 朝日はカメラのうしろから（山が順光で見える）


def overcast(strength=0.55, col_lo=(0.62, 0.64, 0.66), col_hi=(0.42, 0.45, 0.50), sun_s=0.8):
    sky(lo=col_lo, hi=col_hi, strength=strength)
    return sun(50, -30, sun_s, (0.85, 0.88, 0.95))


def birds_up(pts, f0, nf, seed=2, scale=6.0, dist=120.0):
    r = random.Random(seed)
    for k, p in enumerate(pts):
        b = C.link_copy(C.small_bird_mesh(), tuple(p), f"bird_up{k}")
        b.scale = (scale,) * 3
        v = Vector((r.uniform(-1, 1), r.uniform(-1.2, -0.2), r.uniform(0.5, 1.0))).normalized() * dist * r.uniform(0.7, 1.2)
        b.keyframe_insert("location", frame=max(1, f0))
        b.scale = (1e-4,) * 3
        b.keyframe_insert("scale", frame=max(1, f0 - 1))
        b.scale = (scale,) * 3
        b.keyframe_insert("scale", frame=f0)
        b.location = Vector(p) + v * ((nf - f0) / FPS) / 3
        b.keyframe_insert("location", frame=nf)


SPOT = (-70, 430)           # 冒頭で花粉が舞い上がる斜面


def pollen_gust(spts, f_from, f_to, nf, every=2, seed=4, sink_from=None, region=None, wind=(16, -6, 5), size=(5, 10)):
    region = region or (SPOT[0] - 160, SPOT[0] + 160, SPOT[1] - 90, SPOT[1] + 160)
    src = [Vector((x, y, z + h * 0.8)) for x, y, z, h, a, w in spts if region[0] < x < region[1] and region[2] < y < region[3]]
    r = random.Random(seed)
    spawns = [(f, r.choice(src)) for f in range(f_from, f_to, every)] if src else []
    puffs(spawns, nf, wind, size, grow=2.2, rate=0.9, mat=pollen_mat(0.26, (1.0, 0.86, 0.38)), sink_from=sink_from, sink=4.0, rise=10.0,
          name="pollen", seed=seed)


# ---------- 場面 ----------
def s01_open(nf):
    morning()
    porch_set()
    forest, spts = valley(seed=1)
    fv = fr(TL.T_VANISH)
    dad = person((0.2, 0.8, 0.33), 0, seed=4, arms="hold", look=FATHER, pose="sit")
    mask_on(dad, off=None)
    sneeze(dad, 95, spray=False)
    # 風がふくたびに、山から黄色い花粉のけむり → 消えたあとも、飛んだ花粉だけ空に残って ゆっくり沈む
    pollen_gust(spts, 4, fv, nf, every=2, sink_from=fv)
    pollen_gust(spts, 30, fv, nf, every=4, seed=9, sink_from=fv, region=(200, 520, 300, 700), wind=(10, -4, 4))
    specks((0.4, 1.6, 1.3), (1.4, 0.9, 0.7), 90, nf, size=0.005)
    C.show_between(forest, None, fv + 4)
    cam_mt = (-0.4, -2.1, 1.6)
    at_mt = (-30, 600, 150)
    burst(visible_pts(spts, cam_mt, at_mt, 900, 7), fv, 3.0, 40, seed=3, center=(-30, 600), spread=25)
    birds_up(visible_pts(spts, cam_mt, at_mt, 18, 11), fv + 2, nf)
    # 1) 風で山から花粉のけむり 2) マスクのお父さんがくしゃみ 3) 肩ごしに山 → 消える 4) 何もない斜面を文字なしで
    cut(1, (40, 40, 25), (SPOT[0], SPOT[1] + 40, 120), lens=45, orbit=8, push=0.15, focus="far")
    cut(61, (0.1, 2.9, 1.15), (0.2, 0.8, 1.15), lens=45, orbit=14, push=0.25)
    cut(121, cam_mt, at_mt, lens=30, orbit=10, push=0.12, focus="far")
    cut(fv + 8, (-0.4, -2.1, 1.5), (-40, 520, 110), lens=50, orbit=8, push=0.0, piv=3, fixat=1, focus="far", zoom=1.12)
    return nf


def shrine_set(sacred=True):
    C.grass_ground(col=(0.30, 0.38, 0.14), tufts=1500, area=(-6, 6, -6, 2), avoid=[(-1.6, 1.6, -7, 12)])
    C.path(-1.5, 1.5, -8, 14)
    wood = W.mat("shrine_wood", (0.50, 0.32, 0.18), 0.8)
    W.box((0, 15, 1.6), (6, 4.5, 3.2), wood, bevel=0.05)
    W.box((0, 15, 3.6), (7.4, 5.8, 0.8), W.mat("shrine_roof", (0.20, 0.26, 0.24), 0.7), bevel=0.3)
    stone = W.mat("stone_lantern", (0.6, 0.6, 0.58), 0.9)
    for x in (-2.4, 2.4):
        W.box((x, 3.0, 0.8), (0.45, 0.45, 1.6), stone, bevel=0.05)
        W.box((x, 3.0, 1.75), (0.7, 0.7, 0.25), stone, bevel=0.05)
    r = random.Random(8)
    broad_forest([(r.choice((-1, 1)) * r.uniform(7, 20), r.uniform(-2, 30), 0, r.uniform(9, 13), r.uniform(0, 6), 1.0)
                  for _ in range(22)], "shrine_broad", 3)


def shimenawa(center, radius, z, name="nawa"):
    """しめ縄（わらの太い輪）と白い紙垂。"""
    bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=0.13, major_segments=28, minor_segments=8,
                                     location=(center[0], center[1], z))
    o = bpy.context.object
    o.name = name
    o.data.materials.append(W.mat("straw", (0.78, 0.66, 0.38), 0.9))
    paper = W.mat("shide", (0.98, 0.98, 0.96), 0.6)
    for k in range(6):
        a = math.radians(-60 + k * 24)
        p = W.box((radius * math.sin(a) * 1.02, -radius * math.cos(a) * 1.02, -0.32), (0.12, 0.01, 0.45), paper,
                  rot=(0, 0, a), bevel=0)
        p.parent = o
        p.location = (radius * math.sin(a) * 1.02, -radius * math.cos(a) * 1.02, -0.32)
    return o


def s02_shrine(nf):
    day(elev=35, az=-40, strength=4.4)
    shrine_set()
    tree = sugi_forest([(0, 8, 0, 34, 0.3, 2.2)], "goshinboku")
    f0 = 12
    C.show_between(tree, None, f0 + 3)
    rs = random.Random(2)
    pts = [Vector((math.cos(a) * rr, 8 + math.sin(a) * rr, z)) for a, rr, z in
           [(rs.uniform(0, 6.3), rs.uniform(0.3, 3.5) * (1.2 - z / 40), z) for z in [rs.uniform(1, 32) for _ in range(420)]]]
    burst(pts, f0, 0.32, 5, seed=5, center=(0, 8), spread=3)
    rope = shimenawa((0, 8), 1.05, 2.2)
    # しめ縄：木が消えても一瞬だけ宙に残る → 落ちる（だんだん速く）→ 地面で土ぼこり
    hang, fall = 7, 9
    rope.keyframe_insert("location", frame=f0 + hang)
    for k in range(fall + 1):
        u = k / fall
        rope.location.z = 2.2 - 2.05 * u * u
        rope.rotation_euler.x = math.radians(6 * u)
        rope.keyframe_insert("location", frame=f0 + hang + k)
        rope.keyframe_insert("rotation_euler", frame=f0 + hang + k)
    for f, a in ((f0 + hang + fall + 2, 3), (f0 + hang + fall + 5, 0)):
        rope.rotation_euler.x = math.radians(a)
        rope.keyframe_insert("rotation_euler", frame=f)
    land = f0 + hang + fall
    r = random.Random(3)
    puffs([(land + r.randint(0, 3), (math.cos(a) * 1.1, 8 + math.sin(a) * 1.1, 0.15)) for a in [r.uniform(0, 6.3) for _ in range(14)]],
          nf, (0, 0, 0.2), (0.15, 0.3), grow=3.0, rate=2.0, mat=F.puff_mat("dust_soil", (0.62, 0.52, 0.40), 0.3), name="ropedust",
          life=40)
    for k, (x, fac, look, arms) in enumerate(((-1.2, 165, C.GRANDPA, "brow"), (-0.3, 190, MOTHER, "head"))):
        person((x, 2.6, 0), fac, seed=20 + k, arms=arms, look=look)
    W.camera((0.6, -4.0, 1.2), (0.0, 8.0, 7.0), lens=22)
    cut(45, (-2.4, 4.4, 1.0), (0.0, 8.0, 0.4), lens=30, orbit=10, push=0.2)
    return nf


def station_set():
    W.platform(x_side=-1, y_from=-60, y_to=60, x_track=0.0)
    C.grass_ground(col=(0.40, 0.38, 0.34), name="ballast", size=400)
    W.track(x=0.0, y_from=-200, y_to=400)
    sign = C.img_mat("sta_sign", FJ.banner_texture("ホーム 1番線", "sta_sign", bg=(30, 60, 120), fg=(255, 255, 255)))
    bpy.ops.mesh.primitive_plane_add(size=1, location=(-6.0, 6.0, 4.6))
    s = bpy.context.object
    s.scale = (1.6, 0.8, 1)
    s.rotation_euler = (math.radians(90), 0, math.radians(90))
    s.data.materials.append(sign)
    C.skyline(seed=4, y_from=-80, y_to=200, x=(-260, -40), n=40, hmin=20, hmax=70)
    C.skyline(seed=5, y_from=200, y_to=420, x=(-200, 200), n=30, hmin=30, hmax=90)


def s03_station(nf):
    day(elev=25, az=-110, strength=4.2)
    station_set()
    r = random.Random(12)
    spots = []
    for k in range(30):
        spots.append((r.uniform(-8.5, -2.6), r.uniform(-4, 26)))
    spots.sort(key=lambda p: p[1])
    for k, (x, y) in enumerate(spots):
        off = 18 + int(k * 3.2) + r.randint(-6, 6)
        arms = r.choice(["down", "down", "hold"])
        alt = "up" if k % 4 == 0 else None
        p = person((x, y, 1.2), 90 + r.uniform(-25, 25), seed=30 + k, arms=arms, alt=alt, nf=nf, period=30 + k % 5,
                   hat=None)
        if k % 9 != 4:
            mask_on(p, off=off)
    W.camera((-0.9, -6.0, 2.9), (-4.5, 8.0, 2.4), lens=30)
    cut(76, (-1.2, 10.0, 2.7), (-5.0, 3.0, 2.6), lens=40, orbit=12, push=0.2)
    return nf


def s04_bare(nf):
    morning(0.5)
    C.grass_ground(col=(0.30, 0.40, 0.14), size=3000)
    FJ.town(seed=2, y=(-200, 210), x=(-300, 300), n=160)
    _, spts = valley(seed=1, cedar=False)
    # むき出しの斜面から、風で土ぼこり
    r = random.Random(4)
    src = [p for p in spts if abs(p[0]) < 300 and p[1] < 800]
    spawns = [(f, Vector((p[0], p[1], p[2] + 3))) for f in range(1, nf, 2) for p in [r.choice(src)]]
    puffs(spawns, nf, (12, -3, 3), (6, 14), grow=2.0, rate=0.8, mat=F.puff_mat("dust_bare", (0.66, 0.54, 0.40), 0.22),
          name="bare_dust", seed=4, life=70)
    cam = W.camera((40, -260, 160), (-20, 600, 120), lens=30)
    cam["push"] = 0.25
    return nf


def log_pile(x, y, n_rows, length=4.0, seed=1):
    bark_m = W.mat("log_bark", (0.40, 0.26, 0.16), 0.9)
    end = W.mat("log_end", (0.85, 0.66, 0.42), 0.8)
    r = random.Random(seed)
    for row in range(n_rows):
        for k in range(n_rows - row):
            rr = r.uniform(0.17, 0.22)
            o = F._cyl(rr, rr, length, (x + (k - (n_rows - row - 1) / 2) * 0.42, y, 0.21 + row * 0.36),
                       bark_m, rot=(math.radians(90), 0, 0), verts=10)
            o.data.materials.append(end)
            for p in o.data.polygons:
                if abs(p.normal.z) > 0.9:
                    p.material_index = 1


def lumber_set(full=False):
    C.grass_ground(col=(0.45, 0.43, 0.40), name="asphalt", size=600)
    post = W.mat("shed_post", (0.55, 0.55, 0.55), 0.6)
    for x in (-5, 5):
        for y in (4, 12):
            W.box((x, y, 2.5), (0.25, 0.25, 5.0), post, bevel=0.02)
    W.box((0, 8, 5.1), (11.5, 10, 0.3), W.mat("shed_roof", (0.35, 0.45, 0.55), 0.6), bevel=0.05)
    W.box((0, 8, 0.45), (2.4, 1.2, 0.9), W.mat("saw_table", (0.55, 0.58, 0.60), 0.5), bevel=0.03)
    saw = F._cyl(0.5, 0.5, 0.03, (0, 7.6, 1.05), W.mat("saw_blade", (0.80, 0.82, 0.85), 0.25), rot=(0, math.radians(90), 0),
                 verts=24)
    bpy.ops.object.transform_apply(rotation=True)
    mark = W.box((0, 7.6, 1.38), (0.05, 0.08, 0.22), W.mat("saw_mark", (0.85, 0.15, 0.10), 0.5), bevel=0)
    mark.parent = saw
    mark.location = (0, 0, 0.33)
    saw.location = (0, 7.6, 1.05)
    log_pile(-7.5, 2.0, 2 if not full else 5, seed=1)
    if full:
        log_pile(7.5, 2.0, 5, seed=2)
        log_pile(-7.5, 8.0, 4, seed=3)
    else:
        log_pile(7.5, 3.0, 1, seed=2)
    yellow = W.mat("forklift", (0.95, 0.75, 0.10), 0.5)
    W.box((4.2, -2.5, 0.7), (1.2, 2.0, 1.0), yellow, bevel=0.08)
    W.box((4.2, -1.4, 1.6), (1.0, 0.1, 2.6), W.mat("mast", (0.2, 0.2, 0.2), 0.5), bevel=0.02)
    for dx in (-0.3, 0.3):
        W.box((4.2 + dx, -0.8, 0.12), (0.12, 1.2, 0.05), W.mat("mast", (0.2, 0.2, 0.2), 0.5), bevel=0)
    FJ.foothills(seed=7, y=(300, 700), x=(-800, 800), n=10, col=(0.36, 0.34, 0.26), h=(80, 160))
    return saw


def s05_lumber(nf):
    day(elev=40, az=150, strength=4.6)
    saw = lumber_set(False)
    # 丸のこ：電源を切ると、まさつで少しずつ遅くなって止まる（回る角度＝ω0・t − ½αt²）
    w0, alpha = 40.0, 40.0 / 2.6
    for f in range(1, nf + 1, 2):
        t = (f - 1) / FPS
        tt = min(t, w0 / alpha)
        saw.rotation_euler.x = w0 * tt - 0.5 * alpha * tt * tt
        saw.keyframe_insert("rotation_euler", frame=f)
    person((-1.0, 9.8, 0), 160, seed=41, arms="head", look=WORKER, hat="white")
    person((1.2, 10.2, 0), 200, seed=42, arms="hold", look=WORKER, hat="white")
    W.camera((-2.6, 2.2, 1.6), (0.3, 9.2, 1.2), lens=30)
    cut(62, (-9.0, -4.0, 2.2), (-6.5, 2.5, 0.6), lens=28, orbit=10, push=0.2)
    return nf


def slope_h(x, y, theta=34.0, y0=12.0):
    if y < y0:
        return 0.0
    return (y - y0) * math.tan(math.radians(theta)) + 0.6 * math.sin(x / 3.1) * min(1, (y - y0) / 6)


def slide_blocks(blocks, hf, th, f0, nf, a, base_y=12.0, deg_per_m=40.0):
    """blocks = [(形, x, 斜面の上の位置 s_up, 大きさ, 止まる位置 s_end, おくれ, 横ずれ)]。
    重力で加速しながら斜面をすべり（距離の3/4）、残りで強くブレーキがかかって止まる（速さはつながる）。s<0 は平らな所。"""
    c = math.cos(math.radians(th))
    for o, x, s_up, sz, s_end, delay, drift in blocks:
        y0 = base_y + s_up * c
        o.location = (x, y0, hf(x, y0) + sz * 0.3)
        o.rotation_euler.x = math.radians(-th)
        f_go = f0 + int(delay)
        o.keyframe_insert("location", frame=f_go)
        o.keyframe_insert("rotation_euler", frame=f_go)
        D = s_up - s_end
        d1 = D * 0.75
        v1 = math.sqrt(2 * a * d1)
        t1 = v1 / a
        dec = v1 * v1 / (2 * (D - d1))
        t2 = v1 / dec
        for f in range(f_go + 2, nf + 1, 2):
            t = (f - f_go) / FPS
            if t < t1:
                d = 0.5 * a * t * t
            else:
                tt = min(t - t1, t2)
                d = d1 + v1 * tt - 0.5 * dec * tt * tt
            sp = s_up - d
            if sp >= 0:
                yy = base_y + sp * c
                zz = hf(x, yy) + sz * 0.3
                tilt = -th
            else:
                yy = base_y + sp
                zz = sz * 0.35
                tilt = -th * max(0.0, 1 + sp)
            o.location = (x + drift * min(t, t1 + t2), yy, zz)
            o.rotation_euler.x = math.radians(tilt - d * deg_per_m / sz)
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("rotation_euler", frame=f)


def s06_rain(nf):
    overcast(0.5, sun_s=0.6)
    C.grass_ground(col=(0.26, 0.32, 0.14), size=800)
    th = 34.0
    terrain(lambda x, y: slope_h(x, y, th), -40, 40, 11.5, 70, 1.5, zone=lambda x, y: abs(x) < 26, name="rain_slope",
            cols=((0.22, 0.30, 0.13), (0.30, 0.22, 0.15)))
    r = random.Random(6)
    broad_forest([(r.choice((-1, 1)) * r.uniform(27, 45), y, slope_h(30, y, th), r.uniform(7, 10), r.uniform(0, 6), 1.0)
                  for y in range(14, 64, 5)], "rain_broad", 2)
    # 道とガードレール、家
    W.box((0, 8.5, 0.02), (90, 5.0, 0.04), W.mat("asphalt_road", (0.22, 0.22, 0.23), 0.7), bevel=0)
    rail = W.mat("guardrail", (0.82, 0.82, 0.80), 0.4)
    W.box((0, 11.0, 0.6), (40, 0.08, 0.3), rail, bevel=0)
    for x in range(-20, 21, 4):
        W.box((x, 11.0, 0.35), (0.1, 0.1, 0.7), rail, bevel=0)
    walls = W.mat("wall_a", (0.80, 0.77, 0.70))
    roofs = W.mat("roof_b", (0.22, 0.26, 0.32))
    for x in (-12, -2, 9):
        W.box((x, 0.0, 2.6), (7, 6, 5.2), walls, bevel=0.05)
        W.box((x, 0.0, 5.5), (7.8, 6.8, 0.8), roofs, bevel=0.1)
    FJ.utility_poles([(-24, 6.2), (-8, 6.2), (8, 6.2), (24, 6.2)], h=8.0)
    # 土砂くずれ：斜面の上のほうの土（四角いかたまり）が、すべって落ちる（重力と摩擦）。ガードレールの手前で止まる
    f_slide = 52
    a = 9.8 * (math.sin(math.radians(th)) - 0.12 * math.cos(math.radians(th)))
    soil = [W.mat("dirt_clod", (0.36, 0.26, 0.17), 1.0), W.mat("dirt_clod2", (0.30, 0.21, 0.14), 1.0)]
    blocks = []
    for k in range(260):
        sz = r.uniform(0.6, 1.3)
        o = W.box((0, 0, 0), (sz, sz, sz * 0.7), soil[k % 2], bevel=0.05)
        stop_y = r.uniform(11.5, 15.5)
        blocks.append((o, r.uniform(-11, 9), r.uniform(18, 34), sz, (stop_y - 12) / math.cos(math.radians(th)) if stop_y > 12
                       else stop_y - 12, r.uniform(0, 8), r.uniform(-0.4, 0.4)))
    slide_blocks(blocks, lambda x, y: slope_h(x, y, th), th, f_slide, nf, a)
    # 泥のしぶき（くずれの先頭）
    spawns = []
    for f in range(f_slide + 6, nf - 10, 2):
        t = (f - f_slide) / FPS
        s_front = max(0.0, 24 - 0.5 * a * t * t)
        yy = 12 + s_front * math.cos(math.radians(th))
        spawns.append((f, (r.uniform(-10, 8), yy, slope_h(0, yy, th) + 0.8)))
    puffs(spawns, nf, (0, -1.5, 1.2), (0.8, 1.6), grow=2.0, rate=1.5, mat=F.puff_mat("mud_spray", (0.42, 0.33, 0.24), 0.3),
          name="mud", seed=6, life=45)
    rain((0, 6, 6), (22, 14, 7), 2600, nf, length=0.55, speed=10.0)
    p = person((14.5, 4.6, 0), 300, seed=50, arms="brow", look={"top": (0.55, 0.50, 0.42), "bottom": (0.25, 0.25, 0.28)})
    umbrella(p, (0.75, 0.20, 0.20))
    W.camera((2.0, -11.0, 3.2), (-1.0, 26.0, 11.0), lens=24)
    cut(96, (12.0, 8.6, 1.7), (14.5, 4.6, 1.55), lens=40, orbit=10, push=0.15, focus=(14.5, 4.6, 1.55))
    return nf


def s07_river(nf):
    overcast(0.45, sun_s=0.5)
    FJ.river_set(-0.35, 0.25, nf, fish=False)
    wm = bpy.data.materials["water_clear"]
    b = wm.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.42, 0.32, 0.20, 1)
    b.inputs["Alpha"].default_value = 0.96
    b.inputs["Roughness"].default_value = 0.25
    conc = W.mat("bridge", (0.62, 0.62, 0.60), 0.8)
    W.box((0, 7.0, 1.6), (7.5, 2.2, 0.35), conc, bevel=0.03)
    W.box((0, 6.0, 2.05), (7.5, 0.1, 0.5), conc, bevel=0.02)
    W.box((0, 8.0, 2.05), (7.5, 0.1, 0.5), conc, bevel=0.02)
    # 流れてくる枝やごみ（速さで、流れの強さを見せる）
    r = random.Random(7)
    wood = W.mat("drift_wood", (0.35, 0.26, 0.16), 0.9)
    for k in range(16):
        o = F._cyl(0.05, 0.04, r.uniform(0.4, 1.2), (0, 0, 0), wood, rot=(math.radians(90), 0, r.uniform(0, 3)), verts=5)
        x0, y0 = r.uniform(-1.8, 1.8), r.uniform(14, 40)
        v = r.uniform(2.5, 4.0)
        for f in (1, nf):
            t = (f - 1) / FPS
            o.location = (x0 + 0.3 * math.sin(t * 2 + k), y0 - v * t, -0.35 + 0.6 * (f - 1) / nf + 0.05)
            o.keyframe_insert("location", frame=f)
    spawns = [(f, (r.uniform(-2, 2), r.uniform(0, 12), 0.0)) for f in range(1, nf, 1)]
    puffs(spawns, nf, (0, -3.0, 0.1), (0.15, 0.35), grow=1.5, rate=2.0, mat=F.puff_mat("foam", (0.75, 0.68, 0.58), 0.35),
          name="foam", seed=8, life=30)
    rain((0, 3, 2.5), (6, 8, 3.5), 1600, nf, length=0.45, speed=9.0)
    p = person((0.8, 7.0, 1.78), 190, seed=51, arms="brow", look={"top": (0.30, 0.42, 0.35), "bottom": (0.25, 0.25, 0.28)})
    umbrella(p, (0.20, 0.30, 0.55))
    W.camera((1.6, -2.6, 0.75), (0.2, 8.0, 1.4), lens=26)
    return nf


def s08_snow(nf):
    overcast(0.6, col_lo=(0.80, 0.84, 0.90), col_hi=(0.52, 0.60, 0.72), sun_s=1.4)
    C.grass_ground(col=(0.88, 0.90, 0.94), name="snow_flat", size=900)
    th = 36.0
    terrain(lambda x, y: slope_h(x, y, th), -50, 50, 11.5, 80, 1.5, zone=lambda x, y: abs(x) < 30, name="snow_slope",
            cols=((0.86, 0.89, 0.94), (0.90, 0.92, 0.96)))
    W.box((0, 6.0, 0.02), (120, 6.0, 0.04), W.mat("asphalt_wet", (0.25, 0.26, 0.28), 0.4), bevel=0)
    snowwall = W.mat("snow_wall", (0.90, 0.92, 0.96), 0.9)
    W.box((0, 2.4, 0.9), (120, 1.2, 1.8), snowwall, bevel=0.3)
    W.box((0, 9.6, 0.7), (120, 1.0, 1.4), snowwall, bevel=0.3)
    r = random.Random(9)
    broad_forest([(r.choice((-1, 1)) * r.uniform(33, 50), y, slope_h(35, y, th), r.uniform(6, 9), 0, 0.9) for y in range(14, 70, 4)],
                 "snow_broad", 4)
    for m in bpy.data.materials:
        if m.name.startswith("leafy_b"):
            m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.42, 0.40, 0.36, 1)
    # 雪崩：上のほうの雪の板が割れて、すべり落ちる（雪けむりが先に走る）。道の上で止まる（車の手前）
    f0 = 40
    a = 9.8 * (math.sin(math.radians(th)) - 0.08 * math.cos(math.radians(th)))
    sm = [W.mat("snow_block", (0.92, 0.94, 0.98), 0.8), W.mat("snow_block2", (0.86, 0.89, 0.95), 0.8)]
    blocks = []
    for k in range(200):
        sz = r.uniform(0.8, 1.8)
        o = W.box((0, 0, 0), (sz, sz, sz * 0.5), sm[k % 2], bevel=0.08)
        blocks.append((o, r.uniform(-5, 20), r.uniform(26, 44), sz, -r.uniform(1.0, 6.5), r.uniform(0, 6), r.uniform(-0.5, 0.5)))
    slide_blocks(blocks, lambda x, y: slope_h(x, y, th), th, f0, nf, a, deg_per_m=25.0)
    spawns = []
    for f in range(f0 + 3, nf - 5, 1):
        t = (f - f0) / FPS
        s_front = max(-3.0, 38 - 0.5 * a * t * t * 1.15)
        yy = 12 + max(s_front, 0) * math.cos(math.radians(th)) - (0 if s_front > 0 else -s_front)
        spawns.append((f, (r.uniform(-6, 20), yy, slope_h(0, max(yy, 12), th) + 1.5)))
    puffs(spawns, nf, (0, -5.0, 2.5), (1.5, 3.0), grow=3.0, rate=1.0, mat=F.puff_mat("snow_smoke", (0.95, 0.96, 1.0), 0.32),
          name="snowsmoke", seed=9, life=70)
    car = C.car(6.0, (0.70, 0.12, 0.10))
    car.location.x = -30
    car.keyframe_insert("location", frame=1)
    car.location.x = -13
    car.keyframe_insert("location", frame=60)
    car.location.x = -11.5
    car.keyframe_insert("location", frame=80)
    for k, x in enumerate((-12.6, -12.6)):
        lamp = W.box((-11.5 + 2.1, 6.0 + (-0.55 if k == 0 else 0.55), 0.62), (0.05, 0.3, 0.12),
                     W.mat("headlight", (1, 1, 0.9), emit=(1, 0.95, 0.8), emit_strength=6), bevel=0)
        lamp.parent = car
        lamp.location = (2.1, (-0.55 if k == 0 else 0.55), 0.62)
    person((-8.6, 4.0, 0), 160, seed=52, arms="brow", look=ORANGE, hat="white")
    W.camera((-14.0, -6.0, 2.2), (2.0, 30.0, 12.0), lens=24)
    cut(90, (-7.4, 0.2, 1.6), (-8.6, 4.0, 1.5), lens=40, orbit=12, push=0.15, focus=(-8.6, 4.0, 1.5))
    return nf


def sugidama(loc, col=(0.50, 0.36, 0.20), r=0.45, name="sugidama", seed=1):
    rr = random.Random(seed)
    pts = [(0, 0, 0, r, (1, 1, 1))]
    for _ in range(70):
        a, b = rr.uniform(0, 6.3), rr.uniform(-1.4, 1.4)
        pts.append((r * math.cos(a) * math.cos(b), r * math.sin(a) * math.cos(b), r * math.sin(b), r * 0.22, (1, 1, 1)))
    o = C.multi_ball(pts, W.mat(f"sugidama_{col}", col, 0.95), name, sub=1)
    o.location = loc
    return o


def brewery_set(fresh=False):
    C.grass_ground(col=(0.45, 0.42, 0.38), name="gravel", size=300)
    white = W.mat("kura_white", (0.92, 0.90, 0.85), 0.8)
    black = W.mat("kura_black", (0.12, 0.10, 0.09), 0.7)
    W.box((0, 6, 3.0), (14, 6, 6.0), white, bevel=0.03)
    W.box((0, 2.98, 0.9), (14, 0.1, 1.8), black, bevel=0)
    W.box((0, 6, 6.4), (15.5, 7.6, 0.9), W.mat("kura_roof", (0.20, 0.21, 0.24), 0.6), bevel=0.15)
    W.box((0, 2.6, 3.4), (15.0, 1.4, 0.18), W.mat("kura_roof", (0.20, 0.21, 0.24), 0.6), rot=(math.radians(-14), 0, 0), bevel=0.05)
    noren = C.img_mat("noren", FJ.banner_texture("酒", "noren_sake", bg=(25, 35, 70), fg=(250, 250, 245)))
    bpy.ops.mesh.primitive_plane_add(size=1, location=(-2.0, 2.92, 2.0))
    n = bpy.context.object
    n.scale = (1.6, 1.0, 1)
    n.rotation_euler.x = math.radians(90)
    n.data.materials.append(noren)
    W.box((-2.0, 2.97, 1.3), (1.4, 0.05, 2.6), W.mat("door_dark", (0.10, 0.08, 0.07), 0.8), bevel=0)
    barrel = W.mat("taru", (0.72, 0.56, 0.34), 0.7)
    hoop = W.mat("taru_hoop", (0.25, 0.20, 0.15), 0.7)
    for k, (x, z) in enumerate(((3.2, 0.4), (4.1, 0.4), (3.65, 1.2))):
        F._cyl(0.42, 0.42, 0.8, (x, 2.3, z), barrel, rot=(math.radians(90), 0, 0), verts=14)
        F._cyl(0.43, 0.43, 0.06, (x, 2.0, z), hoop, rot=(math.radians(90), 0, 0), verts=14)
    rope = F._cyl(0.012, 0.012, 0.55, (0.8, 2.25, 3.18), W.mat("rope", (0.6, 0.5, 0.35), 0.9), verts=5)
    ball = sugidama((0.8, 2.25, 2.55), col=(0.22, 0.42, 0.16) if fresh else (0.50, 0.36, 0.20))
    return ball, rope


def s09_sake(nf):
    sky(lo=(1.0, 0.70, 0.45), hi=(0.36, 0.42, 0.62), strength=0.45)
    sun(8, -95, 5.0, (1.0, 0.62, 0.35))
    ball, rope = brewery_set(False)
    # 杉玉が風でゆれる（ふりこ：長さ0.65m、周期は約1.6秒、だんだん小さく）
    L = 0.65
    w = math.sqrt(9.8 / L)
    piv = Vector((0.8, 2.25, 3.2))
    bpy.ops.object.empty_add(location=piv)
    hinge = bpy.context.object
    for o in (ball, rope):
        o.parent = hinge
        o.location = o.location - piv
    for f in range(1, nf + 1, 2):
        t = (f - 1) / FPS
        hinge.rotation_euler.x = math.radians(14 * math.exp(-t * 0.25) * math.sin(w * t))
        hinge.keyframe_insert("rotation_euler", frame=f)
    r = random.Random(4)
    leaf = W.mat("dry_leaf", (0.55, 0.40, 0.22), 0.9)
    for k in range(10):
        o = W.box((0, 0, 0), (0.05, 0.02, 0.015), leaf, bevel=0)
        f0 = r.randint(1, nf - 30)
        x0, y0 = 0.8 + r.uniform(-0.3, 0.3), 2.25 + r.uniform(-0.3, 0.3)
        o.scale = (1e-4,) * 3
        o.keyframe_insert("scale", frame=max(1, f0 - 1))
        o.scale = (1, 1, 1)
        for f in range(f0, nf + 1, 2):
            t = (f - f0) / FPS
            o.location = (x0 + 0.25 * math.sin(t * 5 + k), y0 - 0.3 * t, max(0.02, 2.4 - 0.5 * t))
            o.rotation_euler = (t * 4, t * 3, t * 2)
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("rotation_euler", frame=f)
            o.keyframe_insert("scale", frame=f)
    person((-0.4, 1.2, 0), 160, seed=60, arms="brow", look=BREWER)
    W.camera((-2.6, -2.8, 1.25), (0.3, 2.3, 2.3), lens=30)
    cut(64, (1.0, -0.6, 1.9), (0.8, 2.25, 2.55), lens=50, orbit=10, push=0.15, focus=(0.8, 2.25, 2.55))
    return nf


def avenue(y0, y1, step=4.5, x=6.5, seed=3):
    r = random.Random(seed)
    pts = []
    y = y0
    while y < y1:
        for sx in (-1, 1):
            pts.append((sx * (x + r.uniform(-0.5, 0.5)), y + r.uniform(-0.8, 0.8), 0.6, r.uniform(32, 40), r.uniform(0, 6),
                        r.uniform(1.0, 1.3)))
        y += step
    return pts


def nikko_set():
    C.grass_ground(col=(0.26, 0.34, 0.13), tufts=3000, area=(-9, 9, -6, 30), avoid=[(-3.2, 3.2, -10, 200)])
    W.box((0, 90, 0.02), (6.0, 220, 0.04), W.mat("asphalt_road", (0.30, 0.30, 0.31), 0.7), bevel=0)
    moss = W.mat("bank", (0.30, 0.38, 0.18), 1.0)
    for sx in (-1, 1):
        W.box((sx * 6.5, 90, 0.3), (3.5, 220, 0.6), moss, bevel=0.2)
        W.box((sx * 4.7, 90, 0.35), (0.4, 220, 0.7), W.mat("stone_wall", (0.52, 0.50, 0.46), 0.9), bevel=0.05)
    sign = C.img_mat("nikko_sign", FJ.banner_texture("日光杉並木", "nikko_sign", bg=(235, 225, 200), fg=(40, 30, 20)))
    bpy.ops.mesh.primitive_plane_add(size=1, location=(3.6, 6.0, 1.5))
    s = bpy.context.object
    s.scale = (1.6, 0.8, 1)
    s.rotation_euler = (math.radians(90), 0, math.radians(-20))
    s.data.materials.append(sign)
    W.box((3.6, 6.05, 0.6), (0.1, 0.1, 1.2), W.mat("sign_post", (0.4, 0.3, 0.2), 0.8), bevel=0)
    FJ.foothills(seed=8, y=(400, 900), x=(-900, 900), n=10, col=(0.30, 0.38, 0.30), h=(120, 220))


def s10_nikko(nf):
    morning(0.5)
    nikko_set()
    ghost(sugi_forest(avenue(-4, 160), "nikko_ghost"))
    for k, (x, look) in enumerate(((-0.6, MOTHER), (0.3, C.GRANDPA))):
        p = person((x, 9.0, 0), 180, seed=62 + k, arms="brow" if k else "down", look=look)
        p.keyframe_insert("location", frame=1)
        p.location.y = 6.5
        p.keyframe_insert("location", frame=nf)
    W.camera((0.6, -1.0, 1.35), (0.0, 40.0, 7.0), lens=24)
    cut(70, (1.6, 3.2, 1.5), (0.0, 7.8, 1.5), lens=40, orbit=12, push=0.15, focus=(0.0, 7.6, 1.5))
    return nf


def s11_jomon(nf):
    sky(lo=(0.70, 0.80, 0.72), hi=(0.40, 0.55, 0.60), strength=0.45)
    sun(50, -20, 3.4, (1.0, 0.92, 0.75))
    C.grass_ground(col=(0.18, 0.28, 0.12), name="grass_moss", size=300)
    r = random.Random(11)
    C.multi_ball([(r.uniform(-12, 12), r.uniform(4, 30), 0, r.uniform(0.5, 1.5), (1.3, 1.0, 0.55)) for _ in range(40)],
                 W.mat("rock_moss", (0.20, 0.34, 0.14), 1.0), "moss_rocks")
    broad_forest([(r.choice((-1, 1)) * r.uniform(6, 22), r.uniform(2, 40), 0, r.uniform(12, 18), r.uniform(0, 6), 1.1)
                  for _ in range(30)], "jomon_broad", 5)
    deck = W.mat("deck", (0.55, 0.40, 0.26), 0.8)
    W.box((0, 2.0, 1.0), (7, 4, 0.15), deck, bevel=0.02)
    for x in (-3.3, 3.3):
        for y in (0.2, 3.8):
            W.box((x, y, 0.5), (0.15, 0.15, 1.0), deck, bevel=0.01)
    W.box((0, 3.95, 1.55), (7, 0.08, 0.08), deck, bevel=0)
    for x in range(-3, 4):
        W.box((x, 3.95, 1.3), (0.08, 0.08, 0.6), deck, bevel=0)
    # 縄文杉（白い線）：太い幹がこぶのようにふくらんだ、背の低い大木
    trunk = [cone_geo(2.6, 1.6, 9.0, 0.0, 10, 0)] + [cone_geo(1.6, 0.9, 6.0, 9.0, 10, 0)]
    for k in range(5):
        a = k * 1.3
        trunk.append(cone_geo(0.5, 0.0, 9.0, 12.0, 6, 0, rot=a))
    for k in range(6):
        a = k * 1.05
        cx, cy = math.cos(a) * 3.5, math.sin(a) * 3.5
        v, f, m = cone_geo(2.4, 0.0, 4.5, 0.0, 7, 0)
        trunk.append(([(x + cx, y + cy, z + 14 + (k % 3) * 2.5) for x, y, z in v], f, m))
    g = mesh_obj("jomon_ghost", merge(trunk), [W.mat("x", (1, 1, 1))])
    g.location = (0.5, 12, 0)
    ghost(g, thick=0.06)
    for k, (x, arms) in enumerate(((-1.6, "brow"), (-0.3, "down"), (1.2, "hold"))):
        p = person((x, 2.6, 1.08), 180 + (k - 1) * 15, seed=70 + k, arms=arms, look=HIKER if k != 1 else WORKER,
                   hat="cap" if k == 0 else None)
        W.box((0, -0.2, 1.3), (0.34, 0.2, 0.45), W.mat("backpack", (0.20, 0.30, 0.45), 0.8), bevel=0.04).parent = p.children[0]
    W.camera((0.8, -3.5, 1.9), (0.4, 8.0, 5.5), lens=24)
    cut(70, (-0.2, -0.8, 1.9), (-0.3, 2.6, 2.4), lens=40, orbit=12, push=0.12, focus=(-0.3, 2.6, 2.5))
    return nf


def park_set(sakura=True, hinoki=False):
    C.grass_ground(col=(0.32, 0.44, 0.16), tufts=4500, area=(-8, 8, -4, 16))
    r = random.Random(13)
    if sakura:
        for i in range(9):
            C.tree((r.choice((-1, 1)) * r.uniform(3.5, 12), r.uniform(2, 24), 0), h=r.uniform(4.5, 6.5), seed=90 + i,
                   crowns=[(0.98, 0.76, 0.84)])
    if hinoki:
        hinoki_forest([(x, y, 0, r.uniform(9, 12), r.uniform(0, 6), 1.0) for x, y in ((-6, 9), (-3.5, 12), (5.5, 10), (8, 14))])
    sheet = W.mat("sheet_blue", (0.15, 0.40, 0.80), 0.6)
    W.box((0.2, 1.6, 0.015), (2.8, 2.2, 0.02), sheet, bevel=0)
    for k, (x, y) in enumerate(((-4.5, 8.0), (4.0, 7.0), (-2.0, 14.0))):
        W.box((x, y, 0.015), (2.4, 2.0, 0.02), W.mat(f"sheet_{k}", [(0.85, 0.25, 0.25), (0.20, 0.60, 0.35), (0.90, 0.75, 0.20)][k], 0.6),
              bevel=0)
        for j in range(3):
            person((x + (j - 1) * 0.6, y + (0.3 if j % 2 else -0.2), 0.15), r.uniform(150, 220), seed=100 + k * 3 + j, pose="sit",
                   arms="up" if j == 0 else "down", alt="down" if j == 0 else None, nf=200, period=14)
    W.box((0.4, 1.7, 0.08), (0.5, 0.35, 0.12), W.mat("jubako", (0.45, 0.08, 0.08), 0.3), bevel=0.01)
    W.box((0.4, 1.7, 0.145), (0.48, 0.33, 0.01), W.mat("bento_food", (0.95, 0.85, 0.55), 0.6), bevel=0)


def petals(nf, center=(0, 3, 3), extent=(6, 7, 3), n=220, seed=4):
    """桜の花びら：空気の抵抗でゆっくり落ちる（秒速 約1m）。ひらひら左右にゆれる。"""
    r = random.Random(seed)
    m = W.mat("petal", (1.0, 0.80, 0.86), 0.6)
    for k in range(n // 20):
        boxes = [(r.uniform(-1, 1) * extent[0], r.uniform(-1, 1) * extent[1], r.uniform(0, 2) * extent[2], 0.035, 0.025, 0.004,
                  r.uniform(0, 3)) for _ in range(20)]
        o = C.multi_box(boxes, m, f"petals{k}")
        o.visible_shadow = False
        ph = r.uniform(0, 6)
        for f in range(1, nf + 1, 3):
            t = (f - 1) / FPS
            o.location = (center[0] + 0.5 * math.sin(t * 1.7 + ph) + 0.4 * t, center[1], center[2] - 1.0 * t + extent[2] * 0.6)
            o.rotation_euler = (0.3 * math.sin(t * 3 + ph), 0.3 * math.cos(t * 2.5 + ph), 0)
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("rotation_euler", frame=f)


def family(nf, dad_arms="up", alt="down", old=False):
    dad = person((-0.3, 1.5, 0.15), 180, seed=4, pose="sit", arms=dad_arms, alt=alt, nf=nf, period=12,
                 look=FATHER_OLD if old else FATHER)
    person((0.7, 1.4, 0.15), 200, seed=21, pose="sit", arms="down", look=MOTHER)
    person((0.25, 2.3, 0.15), 175, seed=1, pose="sit", arms="up", alt="down", nf=nf, period=9, look=DAUGHTER, scale=0.75)
    return dad


def s12_hanami(nf):
    day(elev=45, az=160, strength=4.6)
    park_set()
    family(nf)
    petals(nf)
    W.camera((0.3, -2.4, 1.0), (0.2, 1.8, 0.9), lens=30)
    cut(76, (-2.2, -0.6, 1.6), (0.3, 3.0, 2.6), lens=24, orbit=10, push=0.15)
    return nf


def s13_hinoki(nf):
    day(elev=50, az=160, strength=4.6)
    park_set(sakura=False, hinoki=True)
    dad = family(nf, dad_arms="hold", alt=None)
    sneeze(dad, 62)
    r = random.Random(14)
    spawns = [(f, (x + r.uniform(-1.5, 1.5), y + r.uniform(-1.5, 1.5), r.uniform(5, 9))) for f in range(1, nf, 2)
              for x, y in [r.choice(((-6, 9), (-3.5, 12), (5.5, 10), (8, 14)))]]
    puffs(spawns, nf, (0.8, -1.2, 0.3), (0.6, 1.4), grow=2.2, rate=1.0, mat=pollen_mat(0.22, (0.95, 0.88, 0.55)),
          name="hinoki_pollen", seed=14, life=80)
    specks((0, 1.0, 1.2), (1.5, 1.0, 0.7), 90, nf, col=(1.0, 0.92, 0.6), size=0.005)
    W.camera((0.6, -1.2, 0.95), (-0.3, 1.5, 0.95), lens=35)
    return nf


def s14_plant(nf):
    day(elev=40, az=160, strength=4.4)
    C.grass_ground(col=(0.30, 0.40, 0.14), size=1500)
    terrain(lambda x, y: slope_h(x, y, 24, 2.0), -40, 40, 1.5, 70, 1.5, zone=lambda x, y: True, name="plant_slope",
            cols=((0.30, 0.38, 0.15), (0.42, 0.31, 0.20)))
    _, _ = valley(seed=1, cedar=False, broad=True)
    r = random.Random(15)
    # 苗木：40日の早送りで、少しずつのびる
    pts = []
    for row in range(6):
        for k in range(9):
            x = -9 + k * 2.2 + r.uniform(-0.3, 0.3)
            y = 3.0 + row * 1.8
            pts.append((x, y, slope_h(x, y, 24, 2.0) - 0.05, r.uniform(0.7, 1.0), r.uniform(0, 6), 1.6))
    sap_me = sugi_forest([(0, 0, 0, 1.0, 0, 1.6)], "sapling_base", col=(0.20, 0.42, 0.16))
    me = sap_me.data
    bpy.data.objects.remove(sap_me)
    for k, (x, y, z, h, rot, w) in enumerate(pts):
        o = C.link_copy(me, (x, y, z), f"sap{k}")
        o.rotation_euler.z = rot
        for f, g in ((1, 0.45), (nf, 1.0)):
            o.scale = (h * g,) * 3
            o.keyframe_insert("scale", frame=f)
    cast = [(-3.0, 2.2, "hold", ORANGE, "white"), (-0.8, 3.0, "down", WORKER, "cap"), (1.6, 2.4, "hold", HIKER, None),
            (3.6, 3.3, "up", DAUGHTER, None)]
    for k, (x, y, arms, look, hat) in enumerate(cast):
        person((x, y, slope_h(x, y, 24, 2.0)), 180 + r.uniform(-20, 20), seed=80 + k, arms=arms, alt="down" if arms == "up" else None,
               nf=nf, period=11, look=look, hat=hat, scale=0.75 if look is DAUGHTER else 1.0)
    shovel = W.mat("shovel", (0.5, 0.5, 0.52), 0.4)
    F._cyl(0.02, 0.02, 1.2, (-0.5, 2.6, 1.5), W.mat("shovel_stick", (0.6, 0.45, 0.3), 0.8), rot=(math.radians(15), 0, 0))
    W.box((-0.5, 2.8, 0.95), (0.22, 0.03, 0.28), shovel, bevel=0.01)
    W.camera((1.0, -5.5, 1.4), (0.0, 6.0, 3.0), lens=28)
    cut(70, (-5.5, 0.5, 2.0), (-1.0, 3.0, 2.0), lens=35, orbit=12, push=0.15)
    return nf


def s15_return(nf):
    morning()
    porch_set()
    forest, spts = valley(seed=1, young=True)
    f_back = 61 + 8
    C.show_between(forest, f_back, None)
    cam_mt = (-0.4, -2.1, 1.6)
    at_mt = (-30, 600, 150)
    burst(visible_pts(spts, cam_mt, at_mt, 900, 8), f_back - 30, 3.0, 40, seed=4, center=(-30, 600), spread=25, mode="in")
    young = bpy.data.objects.get("young")
    if young:
        C.show_between(young, None, f_back)
    dad = person((0.2, 0.8, 0.33), 0, seed=4, arms="down", look=FATHER_OLD, pose="sit")
    _ = dad
    # 山が戻ると、また風で花粉のけむり（冒頭と同じ場所）
    pollen_gust(spts, 140, nf, nf, every=2, seed=5)
    cut(1, (-0.4, -2.1, 1.5), (-40, 520, 110), lens=50, orbit=8, push=0.0, piv=3, fixat=1, focus="far", zoom=1.1)
    cut(121, (2.4, 3.0, 1.2), (0.2, 0.8, 1.15), lens=38, orbit=12, push=0.2)
    cut(156, cam_mt, (SPOT[0], SPOT[1] + 40, 110), lens=40, orbit=8, push=0.1, focus="far")
    return nf


def j1_sneeze(nf):
    morning()
    porch_set()
    valley(seed=1)
    dad = person((0.2, 0.8, 0.33), 0, seed=4, arms="hold", look=FATHER_OLD, pose="sit")
    sneeze(dad, 34)
    specks((0.3, 1.6, 1.2), (1.2, 0.8, 0.6), 110, nf, size=0.005)
    W.camera((0.25, 2.5, 1.12), (0.2, 0.8, 1.12), lens=50)
    return nf


def j2_lumber(nf):
    day(elev=40, az=150, strength=4.6)
    lumber_set(True)
    for k, (x, arms, alt) in enumerate(((-1.2, "up", "down"), (0.0, "wave", "up"), (1.2, "up", "down"))):
        person((x, 9.8 + 0.2 * (k % 2), 0), 180, seed=41 + k, arms=arms, alt=alt, nf=nf, period=7 + k, look=WORKER, hat="white")
    W.camera((-1.5, 3.0, 1.6), (0.0, 9.6, 1.4), lens=28)
    return nf


def j3_sake(nf):
    sky(lo=(1.0, 0.70, 0.45), hi=(0.36, 0.42, 0.62), strength=0.45)
    sun(8, -95, 5.0, (1.0, 0.62, 0.35))
    brewery_set(True)
    person((-0.4, 1.2, 0), 180, seed=60, arms="up", alt="down", nf=nf, period=8, look=BREWER)
    person((-1.5, 1.4, 0), 170, seed=61, arms="wave", alt="up", nf=nf, period=9, look=BREWER)
    W.camera((-1.0, -3.2, 1.5), (0.0, 2.3, 2.1), lens=26)
    return nf


def j4_nikko(nf):
    morning(0.5)
    nikko_set()
    sugi_forest(avenue(-4, 160), "nikko_sugi")
    cast = [(-1.2, "wave", "up", MOTHER), (-0.3, "up", "down", C.GRANDPA), (0.6, "up", "down", HIKER), (1.4, "wave", "down", DAUGHTER)]
    for k, (x, a, alt, look) in enumerate(cast):
        person((x, 7.0 + 0.3 * (k % 2), 0), 180, seed=62 + k, arms=a, alt=alt, nf=nf, period=7 + k, look=look,
               scale=0.75 if look is DAUGHTER else 1.0)
    W.camera((0.3, -0.5, 1.4), (0.0, 20.0, 5.0), lens=24)
    return nf


def j5_wide(nf):
    morning()
    C.grass_ground(col=(0.30, 0.40, 0.14), tufts=4500, area=(-6, 6, -3, 12))
    FJ.town(seed=2, y=(40, 210), x=(-220, 220), n=110)
    _, spts = valley(seed=1)
    pollen_gust(spts, 1, nf, nf, every=2, seed=6)
    cast = [(-1.8, "up", "down", FATHER_OLD, 4), (-1.1, "up", "down", DAUGHTER, 1), (-0.3, "wave", "up", WORKER, 41),
            (0.5, "up", "down", BREWER, 60), (1.3, "wave", "down", MOTHER, 21), (2.1, "up", "down", ORANGE, 52)]
    for k, (x, a, alt, look, seed) in enumerate(cast):
        p = person((x, 1.5 + 0.3 * (k % 2), 0), 150, seed=seed, arms=a, alt=alt, nf=nf, period=8 + k, look=look,
                   scale=0.75 if look is DAUGHTER else 1.0, hat="white" if look is WORKER else None)
        if k == 5:
            mask_on(p)
    FJ.utility_poles([(-22, 16), (-6, 16), (10, 16), (26, 16)])
    cam = W.camera((5.5, -3.0, 1.4), (-6.0, 60.0, 14.0), lens=24)
    cam["push"] = 0.15
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
    FJ.render(out, nf, step, first, last)
    print("rendered", name, flush=True)
