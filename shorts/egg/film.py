"""「もしも人間がタマゴで生まれたら？」全場面の3D（Blender / bpy）。フェロモン版（PH-001）の部品と人を使う。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]"""
import importlib.util
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timeline as TL  # noqa: E402  （フェロモン版より先に読み込む＝こちらの時間割を使わせる）

_spec = importlib.util.spec_from_file_location("ph_film", os.path.join(HERE, "..", "pheromone", "film.py"))
PF = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PF)
FJ, C, W, F, SG, bpy = PF.FJ, PF.C, PF.W, PF.F, PF.SG, PF.bpy
import bmesh  # noqa: E402
from mathutils import Vector  # noqa: E402

FPS = TL.FPS
fr = C.frame_of
cut, fill = FJ.cut, PF.fill
L, actor, person, crowd_look, vis = PF.L, PF.actor, PF.person, PF.crowd_look, PF.vis
KACHO, YOUNG_M, YOUNG_W = PF.KACHO, PF.YOUNG_M, PF.YOUNG_W
smooth, lerp3 = PF.smooth, PF.lerp3
NURSE = {"hair": (0.10, 0.07, 0.05), "top": (0.95, 0.80, 0.85), "bottom": (0.95, 0.80, 0.85), "long": True}
ER, EZ = 0.11, 1.32            # 人のタマゴ：半径 0.11m、たて 1.32倍（直径 22cm・高さ 29cm）


# ---------- タマゴ ----------
def egg_mat(name="egg_shell", col=(0.96, 0.93, 0.86)):
    return W.mat(name, col, 0.45)


def egg_mesh(r=ER, z=EZ, cut=None, keep="all", name="eggm"):
    """タマゴの形（下が少し太い）。cut＝高さ（-1〜1 の割合）で切り、keep="bottom"/"top" の半分だけ。"""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=20, radius=1.0)
    for v in bm.verts:
        x, y, zz = v.co
        k = 1.0 - 0.12 * zz                   # 上ほど細く
        v.co = (x * r * k, y * r * k, zz * r * z)
    if cut is not None:
        zc = cut * r * z
        if keep == "bottom":
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > zc + 1e-6], context='VERTS')
        else:
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < zc - 1e-6], context='VERTS')
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(None)
    return me


def egg(loc, r=ER, z=EZ, name="egg", m=None):
    o = bpy.data.objects.new(name, egg_mesh(r, z, name=f"{name}_m"))
    bpy.context.collection.objects.link(o)
    o.active_material = m or egg_mat()
    o.location = (loc[0], loc[1], loc[2] + r * z)
    return o


def baby(loc, name="baby", face=0.0):
    """おくるみの赤ちゃん（白い布の体＋丸い頭、ねむった目）。"""
    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    root.location = loc
    root.rotation_euler = (0, 0, math.radians(face))
    cloth = W.mat("swaddle", (0.95, 0.90, 0.80), 0.8)
    skin = W.mat("baby_skin", (0.95, 0.76, 0.62), 0.6)
    b = F._ball(0.1, (0, -0.08, 0.08), cloth, sub=2, sc=(0.9, 1.6, 0.8))
    b.parent = root
    h = F._ball(0.075, (0, 0.12, 0.1), skin, sub=2)
    h.parent = root
    for sx in (-1, 1):
        e = W.box((sx * 0.025, 0.19, 0.115), (0.025, 0.006, 0.004), W.mat("baby_eye", (0.15, 0.1, 0.08), 0.5), bevel=0)
        e.parent = root
    return root


def bassinet(loc, name="bas"):
    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    root.location = loc
    clear = W.mat("bas_clear", (0.85, 0.92, 0.95), 0.1, alpha=0.35)
    W.box((0, 0, 0.78), (0.45, 0.75, 0.14), clear, bevel=0.02).parent = root
    W.box((0, 0, 0.7), (0.47, 0.77, 0.03), W.mat("bas_base", (0.85, 0.85, 0.88), 0.4), bevel=0.01).parent = root
    for sx in (-1, 1):
        W.box((sx * 0.2, 0, 0.35), (0.03, 0.6, 0.7), W.mat("bas_leg", (0.75, 0.76, 0.78), 0.3), bevel=0).parent = root
    W.box((0, 0, 0.73), (0.4, 0.7, 0.04), W.mat("bas_mat", (0.70, 0.85, 0.95), 0.8), bevel=0.01).parent = root
    return root


def poof_sparkle(points, f0, seed=1):
    PF.pink_burst(points, f0, size=0.04, rise=0.8, seed=seed, spread=0.5)


def nursery(rows=3, cols=6, seed=1):
    FJ.room((0.98, 0.96, 0.92), 1.1)
    FJ.window_sun(30, 210, 2.2)
    W.box((0, 4, -0.05), (16, 18, 0.1), W.mat("nur_floor", (0.80, 0.82, 0.78), 0.5), bevel=0)
    W.box((0, 11.0, 1.6), (16, 0.2, 3.2), W.mat("nur_wall", (0.98, 0.92, 0.88), 0.9), bevel=0)
    W.box((-6.5, 4, 1.6), (0.2, 18, 3.2), W.mat("nur_wall2", (0.88, 0.94, 0.98), 0.9), bevel=0)
    W.box((0, 4, 3.2), (16, 18, 0.1), W.mat("nur_ceiling", (0.97, 0.97, 0.96), 0.9), bevel=0)
    for k in range(4):
        W.box((-3 + 2.5 * k, 4, 3.14), (1.2, 0.3, 0.02), W.mat("nur_light", (1, 1, 1), 0.3, emit=(1, 0.98, 0.94), emit_strength=3.0),
              bevel=0)
    spots = []
    for i in range(rows):
        for j in range(cols):
            x, y = -3.75 + 1.5 * j, 1.0 + 2.2 * i
            bassinet((x, y, 0), f"bas{i}{j}")
            spots.append((x, y))
    return spots


def living_room():
    FJ.room((0.95, 0.82, 0.62), 0.5)
    W.box((0, 2, -0.05), (10, 10, 0.1), W.mat("living_floor", (0.50, 0.36, 0.22), 0.6), bevel=0)
    W.box((0, 4.6, 1.4), (10, 0.15, 2.8), W.mat("living_wall", (0.90, 0.86, 0.76), 0.9), bevel=0)
    W.box((-3.5, 2, 1.4), (0.15, 10, 2.8), W.mat("living_wall", (0.90, 0.86, 0.76), 0.9), bevel=0)
    W.box((2.2, 4.5, 1.6), (1.4, 0.05, 1.1), W.mat("window_night", (0.3, 0.45, 0.65), 0.3, emit=(0.5, 0.65, 0.85), emit_strength=0.8),
          bevel=0)
    sofa = W.mat("sofa", (0.55, 0.42, 0.36), 0.9)
    W.box((0, 2.6, 0.22), (2.2, 0.85, 0.44), sofa, bevel=0.05)
    W.box((0, 3.0, 0.62), (2.2, 0.25, 0.75), sofa, bevel=0.05)
    for sx in (-1, 1):
        W.box((sx * 1.15, 2.6, 0.45), (0.2, 0.85, 0.5), sofa, bevel=0.05)
    W.box((0, 1.3, 0.22), (1.0, 0.6, 0.44), W.mat("low_table", (0.42, 0.30, 0.20), 0.6), bevel=0.02)
    C.point_light((-2.4, 3.6, 1.8), 60, (1.0, 0.80, 0.55), 0.3)
    W.box((-2.4, 3.6, 0.8), (0.08, 0.08, 1.6), W.mat("lamp_pole", (0.3, 0.3, 0.3), 0.4), bevel=0)
    W.box((-2.4, 3.6, 1.75), (0.45, 0.45, 0.35), W.mat("lamp_shade", (1.0, 0.9, 0.7), 0.6, emit=(1.0, 0.85, 0.6), emit_strength=2.0),
          bevel=0)


def nest(loc, name="nest"):
    """毛布の巣（タマゴを置く）。"""
    o = F._ball(0.26, (loc[0], loc[1], loc[2] + 0.05), W.mat("nest_blanket", (0.85, 0.70, 0.75), 0.9), sub=2, sc=(1.0, 1.0, 0.35))
    o.name = name
    return o


def curve(pts, width, m, name="crv"):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = width
    cu.bevel_resolution = 2
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts):
        p.co = (*q, 1)
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    o.visible_shadow = False
    return o


def grow(o, f0, f1):
    cu = o.data
    cu.bevel_factor_end = 0.0
    cu.keyframe_insert("bevel_factor_end", frame=max(1, f0 - 1))
    cu.keyframe_insert("bevel_factor_end", frame=f0)
    cu.bevel_factor_end = 1.0
    cu.keyframe_insert("bevel_factor_end", frame=f1)


# ============================ 冒頭：新生児室の列をカメラが走る → 5.6秒でタマゴに ============================
F_ON = fr(TL.T_VANISH)


def e00_open(nf):
    spots = nursery()
    r = random.Random(41)
    babies, eggs = [], []
    for k, (x, y) in enumerate(spots):
        b = baby((x, y, 0.76), f"baby{k}", face=r.uniform(-10, 10))
        e = egg((x, y, 0.76), name=f"egg{k}")
        f_k = F_ON + int(abs(x) * 0.6)            # 近い列から順に
        vis(b, [(1, True), (f_k, False)])
        K = e.scale.copy()
        e.scale = (1e-4,) * 3
        e.keyframe_insert("scale", frame=f_k - 1)
        e.scale = K * 1.2
        e.keyframe_insert("scale", frame=f_k + 3)
        e.scale = K
        e.keyframe_insert("scale", frame=f_k + 6)
        babies.append(b)
        eggs.append(e)
        poof_sparkle([(x + r.uniform(-0.2, 0.2), y + r.uniform(-0.2, 0.2), 0.9 + r.uniform(0, 0.3)) for _ in range(4)], f_k, seed=410 + k)
    # 看護師が通る（前景を横切る）
    for k in range(5):
        x0 = -7.0 if k % 2 else 7.0
        y = -1.2 + 2.2 * (k % 3)
        f0 = 1 + 30 * k
        actor(60 + k, L(NURSE, face="happy"), [(1, x0, y), (f0, x0, y), (min(nf, f0 + 120), -x0, y)], nf, period=8,
              face_at=(F_ON + 4, "surprised", "cheek"))

    def cp(f):          # 赤ちゃんの列のすぐ横を、ベッドの高さで走る → タマゴになったら少し引く
        if f <= F_ON:
            u = smooth((f - 1) / (F_ON - 1)) * 0.8 + 0.2 * (f - 1) / (F_ON - 1)
            return lerp3((-5.6, 0.25, 1.12), (0.6, 0.25, 1.12), u)
        return lerp3((0.6, 0.25, 1.12), (1.4, -0.9, 1.6), smooth((f - F_ON) / 40))

    def ca(f):
        if f <= F_ON:
            u = smooth((f - 1) / (F_ON - 1)) * 0.8 + 0.2 * (f - 1) / (F_ON - 1)
            return lerp3((-4.2, 1.0, 0.82), (1.8, 1.4, 0.82), u)
        return lerp3((1.8, 1.4, 0.82), (0.8, 2.6, 0.8), smooth((f - F_ON) / 40))
    c = PF.track_cam(cp, ca, 1, nf, 24)
    PF.shake(c, 1, F_ON + 10, 0.8, seed=6)
    fill((0.0, -2.0, 2.6), (0, 3, 0.9), power=150, size=3)
    return nf


# ============================ 同じ瞬間：看護師がおどろく ============================
def e01_burst(nf):
    spots = nursery()
    r = random.Random(42)
    for k, (x, y) in enumerate(spots):
        egg((x, y, 0.76), name=f"egg{k}")
    for k, (x, y, fc) in enumerate([(-1.5, 0.0, 160), (1.0, 2.2, 200), (2.8, 4.4, 220), (-2.6, 4.6, 150)]):
        actor(60 + k, L(NURSE, face="surprised"), PF.look_around(r, (x, y), 10, nf, fc, n=2), nf, arms=r.choice(["cheek", "head"]))
    W.camera((-4.5, -4.0, 2.6), (0.0, 3.0, 0.9), lens=24)
    fill((0.0, -2.0, 2.6), (0, 3, 0.9), power=150, size=3)
    return nf


# ============================ 大きさくらべ（ニワトリ・ダチョウ・人） ============================
def e02_size(nf):
    FJ.room((0.98, 0.96, 0.92), 1.0)
    W.box((0, 2, -0.05), (10, 10, 0.1), W.mat("lab_floor3", (0.80, 0.82, 0.78), 0.5), bevel=0)
    W.box((0, 4.0, 1.6), (10, 0.2, 3.2), W.mat("nur_wall", (0.98, 0.92, 0.88), 0.9), bevel=0)
    W.box((0, 1.6, 0.4), (1.6, 0.8, 0.8), W.mat("size_table", (0.90, 0.90, 0.88), 0.5), bevel=0.02)
    eggs = [(-0.55, 0.028, 1.28, "ニワトリ", "60g"), (-0.15, 0.065, 1.22, "ダチョウ", "1.5kg"), (0.4, ER, EZ, "人", "4.5kg")]
    for k, (x, rr, zz, lab, wgt) in enumerate(eggs):
        o = egg((x, 1.6, 0.8), rr, zz, name=f"cmp{k}", m=egg_mat(f"egg_c{k}", (0.96, 0.93, 0.86) if k != 0 else (0.90, 0.75, 0.55)))
        K = o.scale.copy()
        o.scale = (1e-4,) * 3
        o.keyframe_insert("scale", frame=max(1, 10 + 18 * k))
        o.scale = K
        o.keyframe_insert("scale", frame=16 + 18 * k)
        PF.sign((x, 1.18, 0.62), 0.36, 0.16, PF.text_texture(f"egglab{k}.png", [(lab, 120), (wgt, 90)], size=(400, 260),
                                                             bg=(40, 40, 50)), f"lab{k}")
    W.camera((-0.05, -1.3, 1.3), (-0.05, 1.6, 0.9), lens=30)
    fill((0.0, 0.0, 2.0), (0, 1.6, 0.9), power=80)
    return nf


# ============================ 37℃で温め続ける（転卵） ============================
def e03_warm(nf):
    living_room()
    nest((0.0, 2.55, 0.44), "nest")
    eg = egg((0.0, 2.55, 0.46), name="our_egg")
    for f, a in ((1, 0), (fr(2.2), 0), (fr(2.8), 70), (fr(3.6), 70), (fr(4.2), 0), (nf, 0)):        # 向きを変える
        eg.rotation_euler = (0, math.radians(a), 0)
        eg.keyframe_insert("rotation_euler", frame=f)
    pm = PF.person((0.55, 2.55, 0.3), 225, seed=2, pose="sit", look=L(YOUNG_M, face="love"), arms="hold")
    pw = PF.person((-0.55, 2.55, 0.3), 135, seed=3, pose="sit", look=L(YOUNG_W, face="happy"), arms="hold", alt="cheek", nf=nf, period=40)
    _ = (pm, pw)
    th = PF.sign((0.0, 0.99, 0.32), 0.36, 0.16, PF.text_texture("temp37.png", [("37℃", 150)], size=(500, 220), bg=(230, 70, 60)), "temp")
    _ = th
    PF.pink_burst([(0.0 + random.uniform(-0.2, 0.2), 2.5, 0.8 + random.uniform(0, 0.3)) for _ in range(8)], fr(1.2), size=0.03, rise=0.5,
                  seed=43, spread=0.4)
    W.camera((1.3, -0.4, 1.45), (0.0, 2.4, 0.75), lens=26)
    cut(fr(2.6), (-0.5, 0.6, 1.1), (0.0, 2.55, 0.62), lens=30, orbit=3, push=0.1)
    fill((0.6, 0.6, 1.8), (0, 2.55, 0.6), power=60, col=(1.0, 0.85, 0.7))
    return nf


# ============================ 会社：お父さんもタマゴをかかえて出勤 ============================
def sling(root, name="sling"):
    """抱っこひもに入れたタマゴ（胸の前）。"""
    s = W.box((0, 0.2, 1.0), (0.34, 0.16, 0.34), W.mat("sling_cloth", (0.35, 0.45, 0.60), 0.9), bevel=0.06)
    s.parent = root
    e = bpy.data.objects.new(f"{name}_egg", egg_mesh(ER, EZ, name=f"{name}_em"))
    bpy.context.collection.objects.link(e)
    e.active_material = egg_mat()
    e.parent = root
    e.location = (0, 0.24, 1.12)
    for sx in (-1, 1):
        W.box((sx * 0.14, 0.05, 1.3), (0.05, 0.3, 0.05), W.mat("sling_cloth", (0.35, 0.45, 0.60), 0.9), bevel=0).parent = root
    return s


def e04_office(nf):
    PF.office_set(nf)
    r = random.Random(44)
    k1 = PF.kacho_desk(nf, "surprised", arms="down", alt="brow", period=26)
    _ = k1
    dads = []
    for k, ((x0, y0), (x1, y1)) in enumerate([((-7.0, 0.3), (-1.35, 0.2)), ((7.0, 0.5), (1.35, 0.3)), ((7.0, -1.0), (0.75, -0.9))]):
        lk = L(crowd_look(r, "happy"), top=(0.85, 0.85, 0.82), long=False)
        if k == 0:
            lk = L(YOUNG_M, face="happy")
        fc = 185 - 10 * k                    # こちら向き（抱っこひものタマゴが見える）
        a = actor(70 + k, lk, [(1, x0, y0), (40 + 15 * k, x1, y1, fc), (nf, x1, y1, fc)], nf, period=8)
        sling(a, f"sl{k}")
        dads.append(a)
    # タマゴ置き場（ほかほかの棚）
    W.box((4.0, 4.2, 0.6), (1.6, 0.5, 1.2), W.mat("egg_shelf", (0.85, 0.80, 0.70), 0.6), bevel=0.02)
    for j in range(4):
        egg((3.4 + 0.4 * j, 4.2, 1.2), name=f"shelf_egg{j}")
    PF.sign((4.0, 3.93, 1.55), 0.9, 0.25, PF.text_texture("egg_place.png", [("タマゴ置き場", 120)], size=(800, 220), bg=(240, 150, 60)),
            "egg_place")
    W.camera((-0.3, -4.4, 1.8), (0.1, 1.2, 1.05), lens=24)
    fill((0.5, -2.5, 2.2), (0, 1.8, 1.0), power=80)
    return nf


# ============================ 【実話】南極：コウテイペンギンの父 ============================
def penguin(loc, face, name="pg", with_egg=True, s=1.0):
    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    root.location = loc
    root.rotation_euler = (0, 0, math.radians(face))
    root.scale = (s, s, s)
    black = W.mat("pg_black", (0.04, 0.05, 0.07), 0.5)
    white = W.mat("pg_white", (0.95, 0.95, 0.93), 0.6)
    yel = W.mat("pg_yellow", (0.98, 0.72, 0.15), 0.5)
    F._ball(0.3, (0, -0.03, 0.55), black, sub=3, sc=(0.85, 0.8, 1.7)).parent = root
    F._ball(0.27, (0, 0.06, 0.52), white, sub=3, sc=(0.8, 0.75, 1.6)).parent = root
    F._ball(0.15, (0, 0.02, 1.08), black, sub=3).parent = root
    for sx in (-1, 1):
        F._ball(0.05, (sx * 0.1, 0.07, 1.0), yel, sub=2, sc=(0.6, 0.6, 1.3)).parent = root
        W.box((sx * 0.25, -0.02, 0.6), (0.05, 0.16, 0.5), black, bevel=0.02).parent = root
        F._ball(0.07, (sx * 0.08, 0.12, 0.03), W.mat("pg_foot", (0.15, 0.13, 0.12), 0.6), sub=2, sc=(1.0, 1.5, 0.4)).parent = root
    W.box((0, 0.2, 1.06), (0.04, 0.14, 0.04), W.mat("pg_beak", (0.12, 0.10, 0.10), 0.5), bevel=0.01).parent = root
    if with_egg:
        e = bpy.data.objects.new(f"{name}_egg", egg_mesh(0.06, 1.25, name=f"{name}_em"))
        bpy.context.collection.objects.link(e)
        e.active_material = egg_mat()
        e.parent = root
        e.location = (0, 0.14, 0.12)
    return root


def e05_penguin(nf):
    FJ.day(elev=12, az=200, strength=2.0)
    W.box((0, 20, -0.05), (400, 400, 0.1), W.mat("snow", (0.92, 0.94, 0.98), 0.6), bevel=0)
    r = random.Random(45)
    for k in range(70):
        a = r.uniform(0, 6.3)
        rad = r.uniform(0, 3.5) ** 0.8 * 1.0
        x, y = rad * math.cos(a), 3.0 + rad * math.sin(a)
        p = penguin((x, y, 0), r.uniform(150, 210), f"pg{k}", with_egg=(k % 3 == 0), s=r.uniform(0.9, 1.05))
        for f in range(1, nf + 1, 6):                      # 少しずつ体をゆらして身を寄せる
            p.rotation_euler = (0, math.radians(2 * math.sin(f / 9 + k)), p.rotation_euler.z)
            p.keyframe_insert("rotation_euler", frame=f)
    hero = penguin((0.0, -0.6, 0), 180, "hero_pg", with_egg=True, s=1.1)
    _ = hero
    snow = W.mat("snowflake", (1, 1, 1), 0.6)
    for k in range(260):                                  # 吹雪（横に流れる雪）
        o = W.box((0, 0, 0), (0.03, 0.03, 0.03), snow, bevel=0)
        x0, y0, z0 = r.uniform(-8, 8), r.uniform(-3, 8), r.uniform(0.1, 3.5)
        sp = r.uniform(4, 8)
        for f in range(1, nf + 1, 3):
            x = ((x0 + sp * f / FPS) + 8) % 16 - 8
            o.location = (x, y0, z0 + 0.2 * math.sin(f / 7 + k))
            o.keyframe_insert("location", frame=f)
    W.camera((0.6, -2.2, 0.5), (0.0, -0.5, 0.42), lens=30)
    cut(fr(2.6), (-3.5, -6.0, 3.5), (0.0, 2.0, 0.8), lens=26, orbit=3, push=0.12)
    fill((1.5, -2.5, 1.5), (0, -0.5, 0.5), power=120, col=(0.85, 0.9, 1.0))
    return nf


# ============================ 上からの力に強い（うっかり座る） ============================
def e06_strong(nf):
    living_room()
    nest((0.3, 2.55, 0.44), "nest")
    eg = egg((0.3, 2.55, 0.46), name="our_egg")
    top = 0.46 + 2 * ER * EZ
    # 夫がうっかり座る（タマゴの上に）
    sitter = PF.person((0.3, 2.55, top - 0.18), 180, seed=2, pose="sit", look=L(YOUNG_M, face="surprised"), arms="up")
    stand = actor(2, L(YOUNG_M, face="neutral"), [(1, 0.3, 1.6, 0), (fr(1.4), 0.3, 1.6, 0), (nf, 0.3, 1.6, 0)], nf)
    vis(stand, [(1, True), (fr(1.5), False)])
    vis(sitter, [(1, False), (fr(1.5), True)])
    for f, sz in ((fr(1.5), 1.0), (fr(1.6), 0.93), (fr(1.75), 1.0)):      # ちょっとだけつぶれて、もどる
        eg.scale = (1.0 / math.sqrt(sz), 1.0 / math.sqrt(sz), sz)
        eg.keyframe_insert("scale", frame=f)
    wife = actor(3, L(YOUNG_W, face="surprised"), [(1, -1.0, 2.0, 120), (nf, -1.0, 2.0, 120)], nf, arms="cheek",
                 face_at=(fr(3.0), "happy", "down"))
    _ = wife
    bm = W.mat("force_blue", (0.15, 0.55, 1.0), 0.3, emit=(0.15, 0.55, 1.0), emit_strength=4.0)
    cz = 0.46 + ER * EZ
    for k in range(10):                                      # 力が殻にそって分かれる（青い線）
        a = 2 * math.pi * k / 10
        pts = []
        for j in range(12):
            th = math.pi * j / 11
            rr = ER * 1.06 * math.sin(th)
            pts.append((0.3 + rr * math.cos(a), 2.55 + rr * math.sin(a), cz + ER * EZ * 1.04 * math.cos(th)))
        cv = curve(pts, 0.006, bm, f"force{k}")
        grow(cv, fr(2.0), fr(2.9))
    W.camera((1.6, 1.3, 0.75), (0.3, 2.55, 0.75), lens=28)
    fill((1.0, 1.0, 1.8), (0.3, 2.55, 0.7), power=60, col=(1.0, 0.85, 0.7))
    return nf


# ============================ ふ化：ひびが広がり、赤ちゃんが自分でわる ============================
def e07_hatch(nf):
    living_room()
    nest((0.0, 2.55, 0.44), "nest")
    z0 = 0.46
    cutz = 0.35
    bot = bpy.data.objects.new("egg_bot", egg_mesh(ER, EZ, cut=cutz, keep="bottom", name="eggb"))
    topo = bpy.data.objects.new("egg_top", egg_mesh(ER, EZ, cut=cutz, keep="top", name="eggt"))
    for o in (bot, topo):
        bpy.context.collection.objects.link(o)
        o.active_material = egg_mat()
        o.location = (0.0, 2.55, z0 + ER * EZ)
    f_open = fr(4.0)
    for f, loc, rot in ((1, (0, 2.55, z0 + ER * EZ), 0), (f_open, (0, 2.55, z0 + ER * EZ), 0),
                        (f_open + 10, (0.18, 2.45, z0 + ER * EZ + 0.15), 50), (nf, (0.25, 2.4, z0 + 0.12), 120)):
        topo.location = loc
        topo.rotation_euler = (0, math.radians(rot), 0)
        topo.keyframe_insert("location", frame=f)
        topo.keyframe_insert("rotation_euler", frame=f)
    for k in range(6):                                       # ゆれる（中から押す）
        f = fr(1.0) + 12 * k
        bot.rotation_euler = (0, math.radians(6 if k % 2 else -6), 0)
        bot.keyframe_insert("rotation_euler", frame=f)
    bot.rotation_euler = (0, 0, 0)
    bot.keyframe_insert("rotation_euler", frame=fr(1.0) + 72)
    crack = W.mat("crack_dark", (0.15, 0.10, 0.08), 0.6)
    zc = z0 + ER * EZ + cutz * ER * EZ
    pts = []
    for j in range(25):                                      # ギザギザのひび（切れ目のまわり）
        a = 2 * math.pi * j / 24
        rr = ER * (1 - 0.12 * cutz) * math.sqrt(1 - cutz ** 2) * 1.02
        pts.append((rr * math.cos(a), 2.55 + rr * math.sin(a), zc + (0.012 if j % 2 else -0.012)))
    cv = curve(pts, 0.004, crack, "crack")
    grow(cv, fr(1.4), fr(3.8))
    # 赤ちゃんの顔（目と口）と手が、殻の上に出る
    skin = W.mat("baby_skin", (0.95, 0.76, 0.62), 0.6)
    bb = bpy.data.objects.new("hatch_baby", None)
    bpy.context.collection.objects.link(bb)
    bb.location = (0.0, 2.55, zc - 0.14)
    F._ball(0.075, (0, 0, 0), skin, sub=2).parent = bb
    for sx in (-1, 1):
        W.box((sx * 0.025, -0.07, 0.01), (0.026, 0.006, 0.005), W.mat("baby_eye", (0.15, 0.1, 0.08), 0.5), bevel=0).parent = bb
    W.box((0, -0.072, -0.025), (0.018, 0.006, 0.01), W.mat("baby_mouth", (0.75, 0.30, 0.30), 0.5), bevel=0).parent = bb
    F._ball(0.028, (0.07, -0.02, 0.07), skin, sub=2).parent = bb
    bb.keyframe_insert("location", frame=f_open)
    bb.location = (0.0, 2.55, zc + 0.02)
    bb.keyframe_insert("location", frame=f_open + 12)
    PF.pink_burst([(random.uniform(-0.2, 0.2), 2.55 + random.uniform(-0.2, 0.2), zc + random.uniform(0, 0.3)) for _ in range(14)], f_open + 6,
                  size=0.035, rise=0.6, seed=47, spread=0.5)
    pm = actor(2, L(YOUNG_M, face="surprised"), [(1, 0.75, 2.1, 300), (nf, 0.75, 2.1, 300)], nf, arms="cheek",
               face_at=(f_open + 8, "love", "up"))
    pw = actor(3, L(YOUNG_W, face="surprised"), [(1, -0.75, 2.1, 60), (nf, -0.75, 2.1, 60)], nf, arms="cheek",
               face_at=(f_open + 8, "love", "pray"))
    _ = (pm, pw)
    W.camera((0.0, 0.8, 1.15), (0.0, 2.55, 0.75), lens=34)
    cut(f_open - 4, (0.0, 0.3, 1.6), (0.0, 2.4, 1.0), lens=26, orbit=3, push=0.1)
    fill((0.6, 1.0, 1.8), (0, 2.55, 0.7), power=60, col=(1.0, 0.85, 0.7))
    return nf


# ============================ その夜：殻のゆりかごで眠る赤ちゃん ============================
def e08_home(nf):
    living_room()
    pm = PF.person((0.62, 2.55, 0.3), 200, seed=2, pose="sit", look=L(YOUNG_M, face="happy"))
    pw = PF.person((-0.62, 2.55, 0.3), 160, seed=3, pose="sit", look=L(YOUNG_W, face="happy"))
    _ = (pm, pw)
    cradle = bpy.data.objects.new("cradle", egg_mesh(ER * 1.0, EZ, cut=0.1, keep="bottom", name="cradlem"))
    bpy.context.collection.objects.link(cradle)
    cradle.active_material = egg_mat()
    cradle.location = (0.0, 2.5, 0.44 + ER * EZ * 0.9)
    nest((0.0, 2.5, 0.42), "nest")
    b = baby((0.0, 2.5, 0.52), "sleep_baby", face=180)
    b.scale = (0.75, 0.75, 0.75)
    for f in range(1, nf + 1, 8):                            # すやすや（少しふくらむ）
        s = 0.75 * (1 + 0.03 * math.sin(f / 10))
        b.scale = (s, s, s)
        b.keyframe_insert("scale", frame=f)
    PF.pink_burst([(random.uniform(-0.3, 0.3), 2.5, 0.9 + random.uniform(0, 0.3)) for _ in range(10)], fr(4.4), size=0.03, rise=0.6,
                  seed=48, spread=0.4)
    W.camera((1.4, -0.2, 1.4), (0.0, 2.55, 0.85), lens=24)
    cut(fr(4.4), (0.0, 0.5, 1.25), (0.0, 2.55, 0.85), lens=26, orbit=3, push=0.12)
    fill((1.0, 0.6, 1.8), (0, 2.55, 0.8), power=60, col=(1.0, 0.85, 0.7))
    return nf


SCENES = {k: v for k, v in globals().items() if callable(v) and k[:1] == "e" and k[1:3].isdigit() and "_" in k}

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    first = int(sys.argv[4]) if len(sys.argv) > 4 else None
    last = int(sys.argv[5]) if len(sys.argv) > 5 else None
    W.reset()
    nf = TL.shot(name)["frames"]
    SCENES[name](nf)
    for cam in FJ.cams():
        cam["orbit"] = min(cam.get("orbit", 13.0) * 0.55, 8.0)
        cam["push"] = min(cam.get("push", 0.3), 0.18)
    if os.environ.get("DRY"):
        print("built", name, len(bpy.data.objects), "objects", flush=True)
        sys.exit(0)
    FJ.render(out, nf, step, first, last)
    print("rendered", name, flush=True)
