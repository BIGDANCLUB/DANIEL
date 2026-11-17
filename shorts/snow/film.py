"""「もしも日本中の雪が毎日2倍に積もったら？」全場面の3D（Blender / bpy）。新幹線版（../mach）の部品を使う。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]
地上の場面は m 単位（夕日は +y）。宇宙の場面は km 単位（地球の中心が原点、日本は真上 +z）。"""
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

W.TEXTURED["snow"] = 2.5
W.TEXTURED["earth"] = 0.002


# ---------- 部品 ----------
def snow_layer(tm, size=4000.0, scale=1.0, base=(0, 0, 0)):
    """雪の層：上の面の高さ = 積雪 h(t)×scale。"""
    m = W.mat("snow", (0.90, 0.92, 0.96), 0.55)
    o = W.box((base[0], base[1], 0.0), (size, size, 1.0), m, bevel=0)
    zs = [v.co.z for v in o.data.vertices]
    for v in o.data.vertices:          # 箱の下端を z=0、上の面を z=1 にそろえる
        v.co.z = 0.0 if v.co.z <= (min(zs) + max(zs)) / 2 else 1.0
    for f, t in enumerate(tm, start=1):
        hh = max(0.001, TL.h(t) * scale)
        o.scale.z = hh
        o.location.z = base[2]           # 下端が地面、上の面が積雪の高さ
        o.keyframe_insert("scale", index=2, frame=f)
        o.keyframe_insert("location", index=2, frame=f)
    return o


def flakes(cam, n_frames, n=140, seed=3):
    """カメラの前に降る雪（カメラに付けて動かす）。"""
    r = random.Random(seed)
    m = W.mat("flake", (1, 1, 1), 0.8, emit=(1, 1, 1), emit_strength=0.6)
    for _ in range(n):
        o = W.box((0, 0, 0), (0.03, 0.03, 0.03), m, bevel=0)
        o.visible_shadow = False
        o.parent = cam
        x, z = r.uniform(-3, 3), r.uniform(-14, -2.5)
        y0, sp, ph = r.uniform(-5, 5), r.uniform(0.02, 0.05), r.uniform(0, 6.28)
        for f in range(1, n_frames + 1):
            y = ((y0 - sp * f) + 5) % 10 - 5
            o.location = (x + 0.15 * math.sin(ph + f * 0.08), y, z)
            o.keyframe_insert("location", frame=f)


def rise_camera(cam, tm, look, scale=1.0, look_rise=1.0):
    """カメラを雪の面に合わせて持ち上げる（目の高さを保つ）。look は最初の注視点。"""
    p0 = cam.location.copy()
    for f, t in enumerate(tm, start=1):
        hh = TL.h(t) * scale
        cam.location = (p0.x, p0.y, p0.z + hh)
        W.aim(cam, (look[0], look[1], look[2] + hh * look_rise))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)


def poles(y_from, y_to, x=4.5, step=25):
    m = W.mat("pole_c", (0.45, 0.43, 0.40), 0.8)
    w = W.mat("wire", (0.1, 0.1, 0.1), 0.5)
    for y in range(y_from, y_to, step):
        W.box((x, y, 5.5), (0.3, 0.3, 11), m, bevel=0)
        W.box((x, y, 10.2), (1.6, 0.15, 0.15), m, bevel=0)
    for dz in (9.6, 10.2):
        W.box((x, (y_from + y_to) / 2, dz), (0.03, y_to - y_from, 0.03), w, bevel=0)


def signal(loc):
    pole = W.mat("pole_c", (0.45, 0.43, 0.40), 0.8)
    box = W.mat("signal", (0.2, 0.2, 0.22), 0.5)
    W.box((loc[0], loc[1], 2.7), (0.2, 0.2, 5.4), pole, bevel=0)
    W.box((loc[0] - 1.6, loc[1], 5.3), (3.2, 0.15, 0.15), pole, bevel=0)
    W.box((loc[0] - 2.8, loc[1], 5.3), (1.3, 0.35, 0.45), box, bevel=0.03)
    for i, c in enumerate([(0.1, 0.9, 0.3), (0.9, 0.7, 0.1), (1.0, 0.15, 0.1)]):
        lm = W.mat(f"lamp{i}", c, emit=c, emit_strength=4 if i == 2 else 0.3)
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.12, depth=0.05, location=(loc[0] - 3.2 + i * 0.4, loc[1] - 0.2, 5.3),
                                            rotation=(math.radians(90), 0, 0))
        bpy.context.object.data.materials.append(lm)


def village():
    F.ground_y(-500, 4000)
    road = W.mat("road_v", (0.25, 0.24, 0.23), 0.9)
    W.box((0, 1500, 0.01), (6, 4000, 0.02), road, bevel=0)
    r = random.Random(5)
    wall = [W.mat("wall_a", (0.80, 0.74, 0.62)), W.mat("wall_b", (0.62, 0.55, 0.46)), W.mat("wall_c", (0.85, 0.80, 0.72))]
    roof = [W.mat("roof_a", (0.30, 0.22, 0.20)), W.mat("roof_b", (0.20, 0.24, 0.30)), W.mat("roof_c", (0.45, 0.25, 0.18))]
    for i in range(70):
        side = 1 if i % 2 else -1
        y = 8 + (i // 2) * 16 + r.uniform(-3, 3)
        x = side * r.uniform(9, 14)
        w, d, hh = r.uniform(7, 10), r.uniform(7, 9), r.uniform(5.5, 6.5)
        W.box((x, y, hh / 2), (w, d, hh), r.choice(wall), bevel=0.05)
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=max(w, d) * 0.78, depth=2.6, location=(x, y, hh + 1.3),
                                        rotation=(0, 0, math.radians(45)))
        bpy.context.object.data.materials.append(r.choice(roof))
    poles(0, 600)
    signal((3.6, 70))
    F.trees(7, 50, 3000, x_min=25, x_max=500, n=120)
    W.houses(seed=8, n=150, y_from=600, y_to=3500, x_min=20, x_max=700)


def town():
    F.ground_y(-500, 6000)
    road = W.mat("road_v", (0.25, 0.24, 0.23), 0.9)
    W.box((0, 2000, 0.01), (16, 5000, 0.02), road, bevel=0)
    r = random.Random(9)
    cols = [W.mat("bld_a", (0.55, 0.55, 0.58), 0.6), W.mat("bld_b", (0.68, 0.64, 0.58), 0.7), W.mat("bld_c", (0.42, 0.45, 0.5), 0.5)]
    win = W.mat("window_lit", (1.0, 0.8, 0.5), emit=(1.0, 0.75, 0.4), emit_strength=1.5)
    for i in range(90):
        side = 1 if i % 2 else -1
        y = 20 + (i // 2) * 30
        x = side * r.uniform(20, 30)
        w, d, hh = r.uniform(14, 22), r.uniform(14, 22), r.uniform(12, 70)
        W.box((x, y, hh / 2), (w, d, hh), r.choice(cols), bevel=0.15)
        for k in range(int(hh // 6)):
            W.box((x - side * (w / 2 + 0.02), y, 3 + k * 6), (0.02, w * 0.7, 1.2), win, bevel=0)
    for y in range(30, 900, 60):
        signal((7.5, y))
    poles(0, 900, x=-7.5, step=30)
    W.buildings(seed=10, n=80, y_from=900, y_to=4000, x_min=40, x_max=700)


def skytree(loc=(0, 1500, 0)):
    steel = W.mat("skytree", (0.85, 0.87, 0.90), 0.4)
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=40, radius2=12, depth=350, location=(loc[0], loc[1], 175))
    bpy.context.object.data.materials.append(steel)
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=12, depth=280, location=(loc[0], loc[1], 490))
    bpy.context.object.data.materials.append(steel)
    for z, r in ((350, 22), (450, 17)):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=r, depth=12, location=(loc[0], loc[1], z))
        bpy.context.object.data.materials.append(steel)
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=4, radius2=0.5, depth=40, location=(loc[0], loc[1], 614))
    bpy.context.object.data.materials.append(steel)


def tokyo():
    F.ground_y(-3000, 9000, x_half=8000)
    skytree()
    W.buildings(seed=13, n=420, y_from=-1500, y_to=7000, x_min=30, x_max=4000)
    river = W.mat("water", (0.30, 0.34, 0.38), 0.12)
    W.box((-300, 1500, 0.02), (90, 9000, 0.04), river, bevel=0)


def fuji():
    F.ground_y(-5000, 90000, x_half=60000)
    rock = W.mat("fuji_rock", (0.22, 0.20, 0.24), 0.9)
    cap = W.mat("fuji_cap", (0.92, 0.93, 0.97), 0.6)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=22000, radius2=400, depth=3776, location=(0, 40000, 1888))
    bpy.context.object.data.materials.append(rock)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=5500, radius2=400, depth=1000, location=(0, 40000, 3276))
    bpy.context.object.data.materials.append(cap)
    F.trees(17, 300, 8000, x_min=50, x_max=6000, n=200)
    W.houses(seed=18, n=200, y_from=300, y_to=9000, x_min=30, x_max=6000)


def space_world(cam_clip=3e6):
    w = bpy.data.worlds.new("space")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.004, 0.005, 0.01, 1)
    bpy.ops.object.light_add(type='SUN')
    s = bpy.context.object
    s.data.energy = 4.0
    s.data.color = (1.0, 0.95, 0.88)
    s.rotation_euler = Vector((-0.8, 1.0, -0.6)).to_track_quat('-Z', 'Y').to_euler()   # カメラ側の斜め上から照らす
    # 星
    r = random.Random(4)
    star = W.mat("star", (1, 1, 1), emit=(1, 1, 1), emit_strength=8)
    for _ in range(500):
        v = Vector((r.gauss(0, 1), r.gauss(0, 1), r.gauss(0, 1))).normalized() * 2.4e6
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=r.uniform(1500, 3500), location=v)
        bpy.context.object.data.materials.append(star)
        bpy.context.object.visible_shadow = False
    # 太陽の円盤（画面の端に見えるよう、光と同じ向き）とダミー（sun.json 用）
    sm = W.mat("sun_disc", (1, 0.95, 0.85), emit=(1.0, 0.95, 0.85), emit_strength=30)
    sun_dir = Vector((0.8, -1.0, 0.6)).normalized()
    bpy.ops.mesh.primitive_uv_sphere_add(radius=30000, location=sun_dir * 2.2e6)
    bpy.context.object.data.materials.append(sm)
    bpy.context.object.visible_shadow = False      # 光をさえぎらない


def earth_and_pillar(tm, moon=False):
    """地球（半径6371km）と、日本の上に積もった雪の柱（km）。"""
    ocean = W.mat("earth", (0.06, 0.18, 0.42), 0.5, emit=(0.05, 0.12, 0.3), emit_strength=0.4)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=6371, location=(0, 0, 0))
    bpy.context.object.data.materials.append(ocean)
    bpy.ops.object.shade_smooth()
    land = W.mat("land", (0.20, 0.30, 0.14), 0.9)
    r = random.Random(6)
    for _ in range(14):
        d = Vector((r.gauss(0, 1), r.gauss(0, 1), r.gauss(0, 1) - 0.3)).normalized()
        if d.z > 0.4:          # 日本（真上）の近くには置かない（カメラが中に入らないように）
            continue
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=r.uniform(900, 2200), location=d * 5650)
        bpy.context.object.data.materials.append(land)
    # 日本（真上）と雪の柱
    snow = W.mat("snow", (0.90, 0.92, 0.96), 0.55)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=650, depth=1.0, location=(0, 0, 6371))
    p = bpy.context.object
    for v in p.data.vertices:          # 下端を z=0、上を z=1 に
        v.co.z = 0.0 if v.co.z < 0 else 1.0
    p.data.materials.append(snow)
    for f, t in enumerate(tm, start=1):
        H = max(1.0, TL.h(t) / 1000)
        p.scale.z = H
        p.location.z = 6371 - 30
        p.keyframe_insert("scale", index=2, frame=f)
        p.keyframe_insert("location", index=2, frame=f)
    if moon:
        mm = W.mat("moon", (0.55, 0.54, 0.52), 0.9)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1737, location=(2500, 0, 384400))
        bpy.context.object.data.materials.append(mm)
        bpy.ops.object.shade_smooth()
    return p


def space_cam(tm, top_frac=0.9, side=1.0, min_d=14000):
    """雪の柱の上の方が画面に入るよう、高さに合わせてカメラを引く。"""
    cam = W.camera((0, 0, 0), (0, 0, 1), lens=30)
    cam.data.clip_end = 3e6
    cam.data.clip_start = 1.0
    for f, t in enumerate(tm, start=1):
        H = TL.h(t) / 1000
        top = 6371 + H
        d = max(min_d, 1.5 * H)
        cam.location = (d * side * 0.55, -d, 6371 + H * top_frac * 0.55 + d * 0.08)
        W.aim(cam, (0, 0, 6371 + H * top_frac * 0.5))
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
    return cam


def tmap_of(name):
    s = TL.shot(name)
    return [TL.t_of(s, i)[0] for i in range(s["frames"])]


# ---------- 場面 ----------
def n01_open(tm):
    village()
    W.sunset()
    snow_layer(tm)
    cam = W.camera((1.2, -12, 1.6), (0, 200, 4.0), lens=30)
    cam.keyframe_insert("location", frame=1)
    cam.location.y += 1.0
    cam.keyframe_insert("location", frame=len(tm))
    flakes(cam, len(tm))


def n02_flake(tm):
    village()
    W.sunset()
    snow_layer(tm)
    post = W.mat("post", (0.75, 0.10, 0.08), 0.5)
    W.box((2.2, 2.0, 0.6), (0.4, 0.35, 1.2), post, bevel=0.04)
    W.box((2.2, 2.0, 1.28), (0.48, 0.42, 0.18), post, bevel=0.06)
    cam = W.camera((3.3, 0.4, 0.5), (2.1, 2.4, 0.9), lens=32)
    flakes(cam, len(tm), n=180)


def ground_scene(tm, setup, cam_pos, look, lens=28, look_rise=1.0):
    setup()
    W.sunset()
    snow_layer(tm, size=200000 if setup is fuji else 40000)
    cam = W.camera(cam_pos, look, lens=lens)
    cam.data.clip_end = 200000
    rise_camera(cam, tm, look, look_rise=look_rise)
    flakes(cam, len(tm))


def n03a_village(tm):
    ground_scene(tm, village, (1.2, -12, 1.6), (0, 200, 4.0), lens=30)


def n03b_town(tm):
    ground_scene(tm, town, (3, -40, 1.7), (0, 300, 20), lens=26)


def n03c_tokyo(tm):
    ground_scene(tm, tokyo, (250, -900, 60), (0, 1500, 300), lens=30, look_rise=0.8)


def n03d_fuji(tm):
    ground_scene(tm, fuji, (0, 0, 40), (0, 40000, 1500), lens=34, look_rise=0.9)


def n03e_space(tm):
    space_world()
    earth_and_pillar(tm, moon=True)
    space_cam(tm)


def n06_winter(tm):
    ground_scene(tm, village, (1.2, -12, 1.6), (0, 200, 4.0), lens=30)


def n07_house(tm):
    ground_scene(tm, village, (-4.0, 20, 1.6), (-12, 40, 3.0), lens=26)


def n08_record(tm):
    ground_scene(tm, village, (2.5, -30, 3.0), (-8, 40, 4.0), lens=26)


def n09_town(tm):
    ground_scene(tm, town, (3, -40, 1.7), (0, 300, 20), lens=26)


def n10_tokyo(tm):
    ground_scene(tm, tokyo, (250, -900, 60), (0, 1500, 300), lens=30, look_rise=0.8)


def n11_fuji(tm):
    ground_scene(tm, fuji, (0, 0, 40), (0, 40000, 1500), lens=34, look_rise=0.9)


def n12_space100(tm):
    space_world()
    earth_and_pillar(tm)
    cam = W.camera((2600, -4200, 6371 + 1100), (0, 0, 6371 + 50), lens=30)
    cam.data.clip_end = 3e6
    cam.data.clip_start = 0.5


def n13_space30(tm):
    space_world()
    earth_and_pillar(tm)
    space_cam(tm, min_d=16000)


def n14_moon(tm):
    space_world()
    earth_and_pillar(tm, moon=True)
    cam = W.camera((9000, -11000, 379000), (1200, 0, 383500), lens=30)
    cam.data.clip_end = 3e6
    cam.data.clip_start = 5


def n15_end(tm):
    space_world()
    earth_and_pillar(tm, moon=True)
    cam = W.camera((250000, -420000, 200000), (0, 0, 195000), lens=30)
    cam.data.clip_end = 3e6
    cam.data.clip_start = 5


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
