"""「もしも桃太郎が光の速さで鬼ヶ島に向かったら？」全場面の3D（Blender / bpy）。新幹線版（../mach）の部品を使う。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]
座標: y=鬼ヶ島の方向（夕日も+y）。出発点は原点の浜辺、y>12 が海。"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, "..", "mach"))
import timeline as TL  # noqa: E402  （この動画の時間割）
import world as W  # noqa: E402
import film as F  # noqa: E402  （新幹線版の部品：人・飛ぶ物・けむり・書き出し）

bpy = W.bpy
from mathutils import Vector  # noqa: E402


# ---------- 部品 ----------
def flag_texture(path):
    """のぼり旗「日本一」の絵（PIL で作る）。"""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (256, 768), (245, 242, 235))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(os.path.join(HERE, "..", "fonts", "NotoSerifJP[wght].ttf"), 170)
    f.set_variation_by_name("Black")
    for i, ch in enumerate("日本一"):
        d.text((128, 150 + i * 215), ch, font=f, fill=(20, 20, 20), anchor="mm")
    d.ellipse((88, 20, 168, 90), fill=(235, 130, 140))     # 桃の印
    im.save(path)
    return path


def img_mat(name, path):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path)
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    return m


def runner(loc, facing_deg=0, pose="stand", fire=False):
    """桃太郎：ローポリの人＋はちまき＋背中ののぼり旗。pose='run' で走る姿。"""
    skin = W.mat("momo_skin", (0.82, 0.60, 0.45), 0.8)
    top = W.mat("momo_kimono", (0.85, 0.82, 0.74), 0.9)
    hakama = W.mat("momo_hakama", (0.16, 0.20, 0.42), 0.9)
    hair = W.mat("hair", (0.05, 0.04, 0.03), 0.8)
    band = W.mat("momo_band", (0.95, 0.95, 0.95), 0.8)
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    parts = []

    def limb(pos, size, m, ang):
        bpy.ops.object.empty_add(location=pos)
        piv = bpy.context.object
        piv.parent = root
        o = W.box((pos[0], pos[1], pos[2] - size[2] / 2), size, m, bevel=0.02)
        o.parent = piv
        o.matrix_parent_inverse = piv.matrix_world.inverted()
        piv.rotation_euler.x = ang
        parts.append(o)

    lean = 0.35 if pose == "run" else 0.0
    if pose == "run":
        limb((0.12, 0, 0.92), (0.18, 0.2, 0.9), hakama, -0.9)
        limb((-0.12, 0, 0.92), (0.18, 0.2, 0.9), hakama, 0.7)
        limb((0.32, 0, 1.45), (0.13, 0.14, 0.6), top, 1.1)
        limb((-0.32, 0, 1.45), (0.13, 0.14, 0.6), top, -1.1)
    else:
        limb((0.12, 0, 0.92), (0.2, 0.22, 0.9), hakama, 0)
        limb((-0.12, 0, 0.92), (0.2, 0.22, 0.9), hakama, 0)
        limb((0.32, 0, 1.45), (0.13, 0.14, 0.6), top, 0.1)
        limb((-0.32, 0, 1.45), (0.13, 0.14, 0.6), top, -0.1)
    body = [W.box((0, 0, 1.2), (0.48, 0.28, 0.62), top, bevel=0.04),
            W.box((0, 0, 0.88), (0.5, 0.32, 0.25), hakama, bevel=0.03),
            W.box((0, 0, 1.68), (0.28, 0.30, 0.32), skin, bevel=0.04),
            W.box((0, -0.03, 1.83), (0.31, 0.32, 0.1), hair, bevel=0.03),
            W.box((0, 0, 1.76), (0.32, 0.33, 0.05), band, bevel=0.01),
            W.box((0, -0.18, 1.78), (0.12, 0.05, 0.12), band, bevel=0)]
    # のぼり旗
    pole = W.box((0.0, -0.22, 2.0), (0.04, 0.04, 2.0), W.mat("pole_wood", (0.35, 0.22, 0.12), 0.8), bevel=0)
    tex = flag_texture(os.path.join(os.environ.get("TMPDIR", "/tmp"), "momo_flag.png"))
    fm = bpy.data.materials.get("momo_flag") or img_mat("momo_flag", tex)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0.0, -0.24, 2.3), rotation=(math.radians(90), 0, 0))
    fl = bpy.context.object
    fl.scale = (0.32, 0.95, 1)
    fl.location.x = -0.18
    fl.data.materials.append(fm)
    for o in body + [pole, fl]:
        o.parent = root
        parts.append(o)
    root.rotation_euler = (lean, 0, math.radians(-facing_deg))
    if fire:
        flame = W.mat("flame", (1, 0.5, 0.1), emit=(1.0, 0.45, 0.08), emit_strength=25)
        for o in body[:2]:
            o.data.materials[0] = flame if random.random() < 0.0 else o.data.materials[0]
    return root


def dog(loc, facing=0):
    w = W.mat("dog", (0.88, 0.85, 0.78), 0.9)
    k = W.mat("dog_dark", (0.25, 0.18, 0.12), 0.9)
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    ps = [W.box((0, 0, 0.45), (0.3, 0.7, 0.3), w), W.box((0, 0.4, 0.68), (0.26, 0.3, 0.26), w),
          W.box((0, 0.58, 0.62), (0.14, 0.14, 0.12), k)]
    for sx in (-0.1, 0.1):
        for sy in (-0.25, 0.25):
            ps.append(W.box((sx, sy, 0.17), (0.08, 0.08, 0.34), w, bevel=0.01))
        ps.append(W.box((sx, 0.36, 0.86), (0.06, 0.04, 0.1), w, bevel=0))
    ps.append(W.box((0, -0.42, 0.62), (0.06, 0.06, 0.25), w, bevel=0))
    for p in ps:
        p.parent = root
    root.rotation_euler.z = math.radians(-facing)
    return root


def monkey(loc, facing=0):
    b = W.mat("monkey", (0.42, 0.28, 0.16), 0.9)
    f = W.mat("monkey_face", (0.85, 0.55, 0.45), 0.8)
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    ps = [W.box((0, 0, 0.35), (0.36, 0.3, 0.45), b), W.box((0, 0.02, 0.72), (0.28, 0.26, 0.26), b),
          W.box((0, 0.15, 0.7), (0.18, 0.04, 0.16), f), W.box((0, 0.12, 0.08), (0.36, 0.3, 0.14), b)]
    for sx in (-0.22, 0.22):
        ps.append(W.box((sx, 0.05, 0.35), (0.08, 0.08, 0.35), b, bevel=0.01))
    for p in ps:
        p.parent = root
    root.rotation_euler.z = math.radians(-facing)
    return root


def pheasant(loc, facing=0):
    g = W.mat("pheasant_g", (0.10, 0.32, 0.22), 0.6)
    r = W.mat("pheasant_r", (0.75, 0.10, 0.08), 0.6)
    br = W.mat("pheasant_b", (0.45, 0.32, 0.18), 0.8)
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    ps = [W.box((0, 0, 0.3), (0.2, 0.36, 0.2), br), W.box((0, 0.2, 0.45), (0.12, 0.12, 0.2), g),
          W.box((0, 0.24, 0.55), (0.1, 0.1, 0.08), r), W.box((0, -0.38, 0.33), (0.06, 0.5, 0.04), br, bevel=0)]
    for sx in (-0.05, 0.05):
        ps.append(W.box((sx, 0, 0.1), (0.03, 0.03, 0.2), r, bevel=0))
    for p in ps:
        p.parent = root
    root.rotation_euler.z = math.radians(-facing)
    return root


def oni(loc, facing=0, color=(0.75, 0.18, 0.12), sit=True, seed=0):
    root, _ = F.person(loc, facing, seed=seed, pose="sit" if sit else "stand", scale=1.45)
    sk = W.mat(f"oni_skin_{color}", color, 0.8)
    tiger = W.mat("tiger", (0.85, 0.62, 0.12), 0.8)
    for c in root.children:
        n = c.data.materials[0].name if c.data.materials else ""
        if n.startswith("skin"):
            c.data.materials[0] = sk
        elif n.startswith("cloth"):
            c.data.materials[0] = tiger if c.location.z < 1.0 else sk
    tz = (0.55 if sit else 1.2) * 1.45
    horn = W.mat("horn", (0.9, 0.85, 0.7), 0.6)
    for sx in (-0.08, 0.08):
        bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.06, depth=0.25,
                                        location=(loc[0] + sx, loc[1], loc[2] + tz + 0.95))
        bpy.context.object.data.materials.append(horn)
    return root


def club(loc, rot=(0, 0, 0)):
    m = W.mat("club", (0.12, 0.10, 0.10), 0.5)
    o = W.box(loc, (0.16, 0.16, 1.5), m, rot=rot, bevel=0.02)
    for i in range(10):
        s = W.box((loc[0] + 0.09 * (1 if i % 2 else -1), loc[1], loc[2] + 0.1 + 0.06 * i), (0.05, 0.05, 0.05), m, bevel=0)
        s.parent = o
        s.matrix_parent_inverse = o.matrix_world.inverted()
    return o


def sea(y_from=12):
    water = W.mat("sea", (0.06, 0.10, 0.13), 0.04)
    W.box((0, (y_from + 60000) / 2, -0.6), (80000, 60000 - y_from, 1.0), water, bevel=0)
    sand = W.mat("sand", (0.62, 0.50, 0.34), 1.0)
    W.box((0, y_from / 2 - 30, -0.3), (2000, y_from + 60, 0.6), sand, bevel=0)
    F.ground_y(-3000, -50, z=0.0)


def islands(seed=1, n=40, y_from=1500, y_to=40000):
    r = random.Random(seed)
    cols = [W.mat("isl_a", (0.16, 0.18, 0.08), 1.0), W.mat("isl_b", (0.22, 0.20, 0.10), 1.0)]
    for _ in range(n):
        y = r.uniform(y_from, y_to)
        x = r.uniform(-8000, 8000)
        rad = r.uniform(150, 900)
        bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=rad, depth=rad * r.uniform(0.25, 0.5), location=(x, y, 0))
        bpy.context.object.data.materials.append(r.choice(cols))


def village(seed=2):
    r = random.Random(seed)
    wall = W.mat("vwall", (0.55, 0.45, 0.32), 0.9)
    thatch = W.mat("thatch", (0.45, 0.36, 0.20), 1.0)
    for _ in range(26):
        x = r.choice((-1, 1)) * r.uniform(12, 160)
        y = r.uniform(-260, -40)
        w, d, h = r.uniform(6, 9), r.uniform(5, 8), r.uniform(2.6, 3.4)
        W.box((x, y, h / 2), (w, d, h), wall, bevel=0.05)
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=max(w, d) * 0.8, depth=h * 1.2, location=(x, y, h + h * 0.6),
                                        rotation=(0, 0, math.radians(45)))
        bpy.context.object.data.materials.append(thatch)
    F.trees(seed + 7, -400, -30, x_min=15, x_max=300, n=50)


def onigashima():
    """鬼ヶ島（女木島）：岩山と洞窟の入り口。場面の原点＝洞窟の前。"""
    rock = W.mat("rock", (0.30, 0.26, 0.22), 1.0)
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=180, depth=120, location=(0, 120, 0))
    bpy.context.object.data.materials.append(rock)
    cave = W.mat("cave", (0.02, 0.02, 0.02), 1.0)
    W.box((0, 34, 4), (9, 6, 8), cave, bevel=0.5)
    ground = W.mat("island_ground", (0.36, 0.30, 0.22), 1.0)
    W.box((0, 0, -0.25), (300, 80, 0.5), ground, bevel=0)
    water = W.mat("sea", (0.06, 0.10, 0.13), 0.04)
    W.box((0, -20000, -0.6), (60000, 40000, 1.0), water, bevel=0)
    F.trees(91, 10, 60, x_min=20, x_max=120, n=18)


def flash(loc, frames_on):
    m = W.mat("flash", (1, 1, 1), emit=(1.0, 0.95, 0.85), emit_strength=200)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.8, location=loc)
    o = bpy.context.object
    o.data.materials.append(m)
    o.visible_shadow = False
    for f in range(1, 400):
        k = 1.0 if f in frames_on else 0.001
        o.scale = (k, k, k)
        o.keyframe_insert("scale", frame=f)
    return o


def glow_trail(root, length=60, n=60, seed=3):
    """光の速さで走ったあとに残る光の線。"""
    m = W.mat("trail", (1, 0.9, 0.7), emit=(1.0, 0.85, 0.6), emit_strength=30)
    o = W.box((0, -length / 2, 1.2), (0.25, length, 0.25), m, bevel=0)
    o.visible_shadow = False
    o.parent = root
    return o


def set_pos(obj, tm, y0=0.0, off=0.0, stop=None):
    for f, t in enumerate(tm, start=1):
        p = TL.pos(t) if stop is None else min(TL.pos(t), stop)
        obj.location.y = y0 + p + off
        obj.keyframe_insert("location", index=1, frame=f)


def tmap_of(name):
    s = TL.shot(name)
    return [TL.t_of(s, i)[0] for i in range(s["frames"])]


# ---------- 場面 ----------
def m01_open(tm):
    sea()
    islands()
    village()
    W.sunset()
    runner((0, 0, 0), 0)
    dog((-1.4, -0.4, 0), 10)
    monkey((1.3, -0.3, 0), -10)
    pheasant((2.1, -0.6, 0), 5)
    cam = W.camera((0.6, -9.0, 1.6), (0.0, 30, 2.6), lens=30)
    cam.keyframe_insert("location", frame=1)
    cam.location.y += 0.8
    cam.keyframe_insert("location", frame=len(tm))


def m02_foot(tm):
    sea()
    islands()
    W.sunset()
    runner((0, 0, 0), 0, pose="run")
    pts = [(random.uniform(-0.4, 0.4), random.uniform(-0.3, 0.3), 0.05, 0.0, 0) for _ in range(30)]
    F.puffs(pts, [i * 1e-9 for i in range(len(tm))], size=(0.05, 0.12), rise=(0, 0), grow=0.5, col=(0.7, 0.58, 0.4))
    W.camera((-1.2, -1.6, 0.25), (0.1, 0.2, 0.5), lens=20)


def m03a_vanish(tm):
    sea()
    islands()
    village()
    W.sunset()
    m = runner((0, 0, 0), 0)
    for f in range(1, len(tm) + 1):     # 5コマ目で消える
        k = 1.0 if f < 6 else 0.0001
        m.scale = (k, k, k)
        m.keyframe_insert("scale", frame=f)
    flash((0, 0.5, 1.2), {6, 7})
    for i, (mk, p, fac) in enumerate([(dog, (-1.4, -0.4, 0), 10), (monkey, (1.3, -0.3, 0), -10), (pheasant, (2.1, -0.6, 0), 5)]):
        o = mk(p, fac)
        o.keyframe_insert("rotation_euler", frame=12 + i * 4)
        o.rotation_euler.z += math.radians(60 if i % 2 else -60)
        o.keyframe_insert("rotation_euler", frame=30 + i * 4)
        o.rotation_euler.z -= math.radians(120 if i % 2 else -120)
        o.keyframe_insert("rotation_euler", frame=55 + i * 4)
    pts = [(random.uniform(-1.5, 1.5), random.uniform(-0.5, 3), 0.1, 5 / 30, 0) for _ in range(60)]
    F.puffs(pts, tm, size=(0.15, 0.5), rise=(0.3, 1.5), grow=2.0, col=(0.72, 0.6, 0.42))
    W.camera((0.6, -9.0, 1.6), (0.0, 30, 2.6), lens=30)


def m03b_island(tm):
    onigashima()
    W.sunset()
    runner((0, 20, 0), 0)
    for i, (x, y, c) in enumerate([(-6, 28, (0.75, 0.18, 0.12)), (5, 30, (0.18, 0.28, 0.6)), (9, 26, (0.75, 0.18, 0.12))]):
        oni((x, y, 0), 180 + (30 if x > 0 else -30), color=c, seed=i)
    cam = W.camera((3.0, 4.0, 2.2), (0, 26, 2.5), lens=28)
    cam.keyframe_insert("location", frame=1)
    cam.location.y += 1.5
    cam.keyframe_insert("location", frame=len(tm))


def m03c_animals(tm):
    sea()
    islands()
    village()
    W.sunset()
    objs = [dog((-1.4, -0.4, 0), 10), monkey((1.3, -0.3, 0), -10), pheasant((2.1, -0.6, 0), 5)]
    for i, o in enumerate(objs):
        o.keyframe_insert("rotation_euler", frame=1)
        o.rotation_euler.z += math.radians(25 * (1 if i % 2 else -1))
        o.keyframe_insert("rotation_euler", frame=25)
        o.rotation_euler.z -= math.radians(50 * (1 if i % 2 else -1))
        o.keyframe_insert("rotation_euler", frame=50)
    W.camera((0.4, 3.5, 0.9), (0.4, -1.0, 0.6), lens=26)


def run_scene(tm, cam_off, look_off, lens=24, fire=False, trail=True, hot=0.0):
    sea()
    islands(seed=5)
    W.sunset()
    m = runner((0, 0, 0), 0, pose="run")
    set_pos(m, tm)
    if trail:
        glow_trail(m)
    if fire or hot:
        F.flames(m, len(tm), n=40, speed=0.15, length=3.0)
        for c in m.children_recursive:
            if c.type == 'MESH' and c.data.materials and c.data.materials[0].name == "momo_kimono" and fire:
                c.data.materials[0] = W.mat("kimono_hot", (0.85, 0.5, 0.3), emit=(1.0, 0.35, 0.08), emit_strength=6)
    cam = W.camera((0, 0, 0), (0, 1, 0), lens=lens)
    cam.parent = m
    cam.location = cam_off
    cam.rotation_euler = (Vector(look_off) - Vector(cam_off)).to_track_quat('-Z', 'Y').to_euler()
    return m


def m06_run(tm):
    # 横から（カメラは止めて、桃太郎が13m横切る）
    sea()
    islands(seed=5)
    W.sunset()
    m = runner((0, 0, 0), 0, pose="run")
    set_pos(m, tm, off=-200.0 - 6.0)
    glow_trail(m, length=40)
    W.camera((-9.0, 0.0, 1.4), (0, 0.0, 1.3), lens=24)


def m07_fire(tm):
    run_scene(tm, (-2.4, 3.2, 1.9), (0, 0, 1.4), lens=24, fire=True)


def m08_safe(tm):
    run_scene(tm, (0.8, -6.0, 2.4), (0, 20, 1.6), lens=28, fire=True)


def m09_light(tm):
    run_scene(tm, (-6.0, -1.0, 1.6), (0, 1.0, 1.3), lens=28, fire=True)


def m10_sound(tm):
    sea()
    islands()
    village()
    W.sunset()
    for mk, p, fac in [(dog, (-1.4, -0.4, 0), 10), (monkey, (1.3, -0.3, 0), -10), (pheasant, (2.1, -0.6, 0), 5)]:
        mk(p, fac)
    # 音の波：出発点から秒速340mで広がる、すき通った半球
    m = F.puff_mat("soundwave", (1, 0.95, 0.9), 0.08)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0, location=(0, 0, 0))
    s = bpy.context.object
    s.data.materials.append(m)
    s.visible_shadow = False
    for f, t in enumerate(tm, start=1):
        r = max(0.01, TL.SOUND * t)
        s.scale = (r, r, r)
        s.keyframe_insert("scale", frame=f)
    W.camera((6.0, -40.0, 14.0), (0, 200, 0), lens=24)


def m11_sea(tm):
    sea()
    islands(seed=6)
    W.sunset()
    pts = []
    y0 = 20000
    for y in range(-400, 400, 6):
        for x in (-4, -8, -13, -19, 4, 8, 13, 19):
            ts = TL.t_at(y0 + y) + abs(x) / TL.SOUND * 0.02
            pts.append((x, y, -0.2, ts, 1 if x > 0 else -1))
    F.puffs(pts, tm,
            seed=9, col=(0.85, 0.88, 0.9), alpha=0.55, size=(1.0, 2.5), rise=(4, 12), grow=2.0, life=2.5, out=(2, 8),
            name="spray")
    W.camera((0, -180, 22), (0, 200, 0), lens=26)


def m12_clock(tm):
    run_scene(tm, (1.6, 2.6, 1.9), (0, 0, 1.7), lens=26, fire=True)


def m13_oni(tm):
    onigashima()
    W.sunset()
    m = runner((0, 0, 0), 0, pose="run")
    for f, t in enumerate(tm, start=1):   # 到着点 y=20 に向かって走り込み、止まる
        m.location.y = 20.0 - max(0.0, (TL.T_ARRIVE - t) * TL.C)
        m.keyframe_insert("location", index=1, frame=f)
    glow_trail(m, length=30)
    for i, (x, y, c) in enumerate([(-6, 28, (0.75, 0.18, 0.12)), (5, 30, (0.18, 0.28, 0.6)), (9, 26, (0.75, 0.18, 0.12))]):
        oni((x, y, 0), 180 + (30 if x > 0 else -30), color=c, seed=i)
    W.camera((-10.0, 12.0, 2.6), (2.0, 24, 1.8), lens=24)


def m14_club(tm):
    onigashima()
    W.sunset()
    runner((0, 20, 0), 0)
    clubs = []
    for i, (x, y, c) in enumerate([(-6, 28, (0.75, 0.18, 0.12)), (5, 30, (0.18, 0.28, 0.6)), (9, 26, (0.75, 0.18, 0.12))]):
        oni((x, y, 0), 180 + (30 if x > 0 else -30), color=c, seed=i)
        clubs.append(club((x + 0.6, y - 0.4, 1.0), rot=(0.3, 0, 0)))
    F.fly(clubs, lambda o: TL.T_ARRIVE + 0.02, tm, seed=3, vx=(3, 8), vy=(6, 14), vz=(6, 12), spin=6, drag=0.3,
          side=lambda o: 1 if o.location.x > 0 else -1)
    pts = [(random.uniform(-10, 10), random.uniform(15, 32), 0.2, TL.T_ARRIVE + 0.01, 0) for _ in range(60)]
    F.puffs(pts, tm, size=(0.4, 1.2), rise=(0.5, 2.0), grow=2.0, col=(0.6, 0.5, 0.38))
    W.camera((2.0, 6.0, 2.0), (0, 28, 2.2), lens=24)


def m15_end(tm):
    sea()
    islands()
    village()
    W.sunset()
    dog((-0.5, -0.4, 0), 0)
    monkey((0.6, -0.3, 0), 0)
    pheasant((1.4, -0.6, 0), 0)
    cam = W.camera((0.4, -6.5, 1.1), (0.4, 30, 2.2), lens=30)
    cam.keyframe_insert("location", frame=1)
    cam.location.y += 0.8
    cam.keyframe_insert("location", frame=len(tm))


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
