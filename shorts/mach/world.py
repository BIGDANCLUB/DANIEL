"""「もしも新幹線がマッハ10で走っていたら？」の3Dの舞台（Blender / bpy）。
参考動画と同じローポリ（角ばった形）＋夕日の低い光。座標は x=横、y=線路の進行方向（新横浜側が+）、z=上（m）。"""
import math

import bpy
import bmesh

SUN_ELEV = 6.0          # 夕日の高さ（度）
SUN_AZ = 0.0            # 進行方向（+y）の正面に沈む


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'   # キーの間は等速


def mat(name, col, rough=0.85, emit=None, emit_strength=0.0, alpha=1.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = emit_strength
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    return m


def box(loc, size, m, rot=(0, 0, 0), bevel=0.03, name=None):
    """size は全長（x, y, z）。"""
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(m)
    if bevel:
        bv = o.modifiers.new("bevel", "BEVEL")
        bv.width = bevel
        bv.segments = 1
    if name:
        o.name = name
    return o


def mesh_from(name, verts, faces, m):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    return o


# ---------- 新幹線（N700系っぽいローポリ） ----------
W_CAR, H_CAR = 3.38, 3.6


def nose_mesh(name, m, length=12.0):
    """先頭のくちばし形。断面（幅・高さ・床からの高さ）を前に向かって細くした角ばったメッシュ。"""
    secs = []   # (y, half_w, top, bottom)
    n = 7
    for i in range(n + 1):
        t = i / n                   # 0=車体側 1=先端
        hw = W_CAR / 2 * (1 - 0.82 * t ** 1.6)
        top = 0.45 + (H_CAR - 0.45) * (1 - t ** 0.7) * (1 - 0.25 * t)
        top = max(top, 0.9 - 0.3 * t)
        bot = 0.45 + 0.25 * t
        secs.append((length * t, hw, top, bot))
    verts, faces = [], []
    for y, hw, top, bot in secs:
        # 断面は角を落とした6角形
        verts += [(-hw, y, bot), (hw, y, bot), (hw, y, top * 0.72 + bot * 0.28),
                  (hw * 0.62, y, top), (-hw * 0.62, y, top), (-hw, y, top * 0.72 + bot * 0.28)]
    k = 6
    for i in range(n):
        a, b = i * k, (i + 1) * k
        for j in range(k):
            faces.append((a + j, a + (j + 1) % k, b + (j + 1) % k, b + j))
    faces.append(tuple(range(k))[::-1])
    faces.append(tuple(range(n * k, n * k + k)))
    return mesh_from(name, verts, faces, m)


def shinkansen(y0=0.0, cars=4, name="train"):
    """先頭が +y を向いた編成。y0 = 先頭の鼻先の位置。親（empty）を返すので、それを動かす。"""
    white = mat("train_white", (0.92, 0.92, 0.90), 0.35)
    blue = mat("train_blue", (0.04, 0.16, 0.55), 0.4)
    glass = mat("train_glass", (0.02, 0.03, 0.05), 0.15)
    dark = mat("train_dark", (0.08, 0.08, 0.09), 0.7)
    bpy.ops.object.empty_add(location=(0, y0, 0))
    root = bpy.context.object
    root.name = name
    parts = []
    nose_len, car_len = 12.0, 25.0
    nose = nose_mesh(name + "_nose", white)
    nose.location = (0, -nose_len, 0)
    parts.append(nose)
    # 運転席の窓
    parts.append(box((0, -nose_len + 3.2, 2.25), (1.6, 2.2, 0.35), glass, rot=(math.radians(-18), 0, 0), bevel=0.05))
    y = -nose_len
    for c in range(cars):
        yc = y - car_len / 2
        parts.append(box((0, yc, 0.45 + (H_CAR - 0.45) / 2), (W_CAR, car_len - 0.4, H_CAR - 0.45), white, bevel=0.25))
        # 青い帯（窓の下）と窓の列
        for sx in (-1, 1):
            parts.append(box((sx * (W_CAR / 2 + 0.005), yc, 1.45), (0.02, car_len - 0.6, 0.22), blue, bevel=0))
            parts.append(box((sx * (W_CAR / 2 + 0.005), yc, 2.25), (0.02, car_len - 2.0, 0.55), glass, bevel=0))
        parts.append(box((0, yc, 0.25), (W_CAR - 0.6, car_len - 3, 0.5), dark, bevel=0.05))   # 床下
        y -= car_len
    # 最後尾もくちばし形（新幹線は両端が先頭車）
    tail = nose_mesh(name + "_tail", white)
    tail.scale.y = -1
    tail.location = (0, y, 0)
    parts.append(tail)
    parts.append(box((0, y - 3.2, 2.25), (1.6, 2.2, 0.35), glass, rot=(math.radians(18), 0, 0), bevel=0.05))
    for p in parts:
        p.parent = root
        p.location.y -= 0   # 親の原点＝鼻先
    root["length"] = 2 * nose_len + cars * car_len
    return root


# ---------- 線路・ホーム・まわり ----------
def ground(size=6000):
    g = mat("ground", (0.20, 0.15, 0.08), 1.0)
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, size / 2 - 400, 0))
    bpy.context.object.data.materials.append(g)
    return bpy.context.object


def track(x=0.0, y_from=-400, y_to=4000):
    ballast = mat("ballast", (0.32, 0.29, 0.25), 1.0)
    rail = mat("rail", (0.55, 0.52, 0.5), 0.3)
    slab = mat("slab", (0.5, 0.48, 0.45), 0.9)
    L = y_to - y_from
    yc = (y_to + y_from) / 2
    box((x, yc, 0.1), (4.2, L, 0.2), ballast, bevel=0)
    box((x, yc, 0.24), (2.6, L, 0.08), slab, bevel=0)
    for s in (-0.7175, 0.7175):
        box((x + s, yc, 0.36), (0.08, L, 0.16), rail, bevel=0)


def platform(x_side=1, y_from=-160, y_to=160, x_track=0.0, roof_to=None):
    """線路の横のホーム。x_side=+1 で右側。"""
    conc = mat("platform", (0.62, 0.6, 0.56), 0.9)
    yellow = mat("tactile", (0.95, 0.75, 0.1), 0.8)
    roof = mat("canopy", (0.75, 0.74, 0.72), 0.6)
    pole = mat("pole", (0.35, 0.36, 0.38), 0.5)
    edge = x_track + x_side * 1.85
    w = 9.0
    xc = edge + x_side * w / 2
    L = y_to - y_from
    yc = (y_to + y_from) / 2
    box((xc, yc, 0.6), (w, L, 1.2), conc, bevel=0.02)
    box((edge + x_side * 1.0, yc, 1.205), (0.3, L, 0.01), yellow, bevel=0)
    rt = y_to if roof_to is None else roof_to
    for yy in range(int(y_from) + 8, int(rt), 16):
        box((xc + x_side * 1.5, yy, 3.6), (0.25, 0.25, 4.8), pole, bevel=0.02)
    box((xc + x_side * 1.2, (y_from + rt) / 2, 6.05), (w - 0.5, rt - y_from, 0.25), roof, bevel=0.05)
    return edge


def houses(seed=1, n=40, y_from=100, y_to=1500, x_min=25, x_max=300):
    import random
    r = random.Random(seed)
    wall = [mat("wall_a", (0.80, 0.74, 0.62)), mat("wall_b", (0.70, 0.66, 0.60)), mat("wall_c", (0.85, 0.80, 0.72))]
    roof = [mat("roof_a", (0.30, 0.22, 0.20)), mat("roof_b", (0.20, 0.24, 0.30)), mat("roof_c", (0.45, 0.25, 0.18))]
    for _ in range(n):
        side = r.choice((-1, 1))
        x = side * r.uniform(x_min, x_max)
        y = r.uniform(y_from, y_to)
        w, d, h = r.uniform(7, 12), r.uniform(7, 12), r.uniform(5, 8)
        box((x, y, h / 2), (w, d, h), r.choice(wall), bevel=0.05)
        box((x, y, h + 1.0), (w + 0.6, d + 0.6, 2.0), r.choice(roof), rot=(0, 0, 0), bevel=0.4)


def buildings(seed=2, n=60, y_from=-300, y_to=600, x_min=40, x_max=400):
    import random
    r = random.Random(seed)
    cols = [mat("bld_a", (0.55, 0.55, 0.58), 0.6), mat("bld_b", (0.68, 0.64, 0.58), 0.7), mat("bld_c", (0.42, 0.45, 0.5), 0.5)]
    for _ in range(n):
        side = r.choice((-1, 1))
        x = side * r.uniform(x_min, x_max)
        y = r.uniform(y_from, y_to)
        w, d, h = r.uniform(15, 35), r.uniform(15, 35), r.uniform(20, 90)
        box((x, y, h / 2), (w, d, h), r.choice(cols), bevel=0.2)


def catenary(y_from=-200, y_to=3000, step=50, x=0.0):
    pole = mat("cat_pole", (0.30, 0.30, 0.32), 0.6)
    for yy in range(int(y_from), int(y_to), step):
        box((x - 3.0, yy, 4.0), (0.3, 0.3, 8.0), pole, bevel=0)
        box((x - 1.2, yy, 7.8), (3.8, 0.2, 0.2), pole, bevel=0)


# ---------- 光・空・カメラ・書き出し ----------
def sunset(strength=4.0):
    from mathutils import Vector
    bpy.ops.object.light_add(type='SUN')
    s = bpy.context.object
    e = math.radians(SUN_ELEV)
    # 光は正面（+y の地平線）から手前（-y）へ向かう
    s.rotation_euler = Vector((0, -math.cos(e), -math.sin(e))).to_track_quat('-Z', 'Y').to_euler()
    s.data.energy = strength
    s.data.color = (1.0, 0.62, 0.32)
    s.data.angle = math.radians(1.5)
    w = bpy.data.worlds.new("sky")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    sky = nt.nodes.new("ShaderNodeTexSky")
    sky.sky_type = 'MULTIPLE_SCATTERING'
    sky.sun_elevation = math.radians(SUN_ELEV)
    sky.sun_rotation = math.radians(90 + SUN_AZ)     # +y の方向
    sky.sun_disc = True
    try:
        sky.aerosol_density = 4.0
        sky.air_density = 1.0
    except Exception:
        pass
    nt.links.new(sky.outputs[0], bg.inputs[0])
    bg.inputs[1].default_value = 0.12
    # 太陽の円盤
    sm = mat("sun_disc", (1, 0.8, 0.5), emit=(1.0, 0.85, 0.55), emit_strength=40)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=60, location=(0, 5000, 5000 * math.tan(math.radians(SUN_ELEV)) - 40))
    bpy.context.object.data.materials.append(sm)
    bpy.context.object.visible_shadow = False
    # 夕方のもや
    sc = bpy.context.scene
    return s


def camera(loc, look_at, lens=28):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.data.lens = lens
    c.data.clip_end = 20000
    aim(c, look_at)
    bpy.context.scene.camera = c
    return c


def aim(obj, target):
    from mathutils import Vector
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def render_setup(path, frame_start, frame_end, res=(540, 960), samples=12, fps=30):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.fps = fps
    sc.frame_start, sc.frame_end = frame_start, frame_end
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Punchy'
    sc.view_settings.exposure = -0.3
    sc.render.image_settings.file_format = 'PNG'
    sc.render.filepath = path
    sc.render.use_motion_blur = False
