"""「もしもカラスが消えたら？」全場面の3D（Blender / bpy）。新幹線版（../mach）の部品（人・ベンチ・けむり）を使う。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]
座標: z=上（m）。カメラはおおむね -y から +y を見る。"""
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
F = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(F)
F.SUBDIV = 3
F.SOFT = True

bpy = W.bpy
from mathutils import Vector  # noqa: E402

RES = (540, 960)
FPS = TL.FPS
W.TEXTURED.update({"asphalt": 1.5, "tatami": 4.0, "snow": 0.8, "gravel": 3.0, "leafy": 1.2})

GRANDPA = {"hair": (0.78, 0.78, 0.76), "top": (0.45, 0.36, 0.28), "bottom": (0.30, 0.30, 0.33)}
KID = {"top": (0.95, 0.75, 0.20), "bottom": (0.20, 0.30, 0.55)}


def sec(f):
    return (f - 1) / FPS


# ---------- 人（参考元に寄せた角ばった体。顔は今の丸い頭のまま＝ユーザー指定） ----------
_BLOCK = {}


def person_block_mesh(variant, pose, look=None):
    look = look or {}
    key = (variant, pose, tuple(sorted(look.items())))
    if key in _BLOCK:
        return _BLOCK[key]
    r = random.Random(variant * 31 + 7)
    skin = W.mat(f"skin{variant % 3}", F.SKIN[variant % 3], 0.8)
    top = W.mat(f"top_{look.get('top', F.CLOTH[variant % 6])}", look.get("top", F.CLOTH[variant % 6]), 0.9)
    bcol = look.get("bottom", F.CLOTH[(variant + 3) % 6])
    bottom = W.mat(f"bottom_{bcol}", bcol, 0.9)
    hcol = look.get("hair", (0.06, 0.045, 0.035))
    hair = W.mat(f"hair_{hcol}", hcol, 0.8)
    white = W.mat("eye_white", (0.95, 0.95, 0.93), 0.4)
    black = W.mat("eye_black", (0.02, 0.02, 0.02), 0.3)
    shoe = W.mat("shoe", (0.12, 0.10, 0.09), 0.7)
    bv = 0.015
    p = []
    if pose == "sit":
        hip = 0.2
        for sx in (-1, 1):
            p.append(W.box((sx * 0.1, 0.2, hip), (0.15, 0.46, 0.16), bottom, bevel=bv))          # もも（前へ）
            p.append(W.box((sx * 0.1, 0.42, hip - 0.24), (0.13, 0.14, 0.44), bottom, bevel=bv))  # すね
            p.append(W.box((sx * 0.1, 0.47, hip - 0.47), (0.13, 0.24, 0.07), shoe, bevel=bv))
    else:
        hip = 0.86
        for sx in (-1, 1):
            p.append(W.box((sx * 0.095, 0, 0.47), (0.15, 0.16, 0.8), bottom, bevel=bv))
            p.append(W.box((sx * 0.095, 0.04, 0.035), (0.14, 0.26, 0.07), shoe, bevel=bv))
    p.append(W.box((0, 0, hip + 0.06), (0.36, 0.2, 0.16), bottom, bevel=bv))                     # 腰
    p.append(W.box((0, 0, hip + 0.36), (0.42, 0.23, 0.5), top, bevel=bv))                         # 胴
    sh = hip + 0.54
    for sx in (-1, 1):
        p.append(W.box((sx * 0.27, 0, sh - 0.27), (0.12, 0.13, 0.56), top, rot=(0, math.radians(sx * 4), 0), bevel=bv))
        p.append(W.box((sx * 0.285, 0.01, sh - 0.6), (0.1, 0.11, 0.12), skin, bevel=bv))
    p.append(W.box((0, 0, sh + 0.05), (0.1, 0.1, 0.1), skin, bevel=0))
    hc = sh + 0.22
    p.append(F._ball(0.135, (0, 0, hc), skin, sub=2, sc=(1.0, 0.95, 1.12)))
    if look.get("bald"):
        p.append(F._ball(0.14, (0, -0.02, hc - 0.02), hair, sub=2, sc=(1.03, 0.98, 0.7)))
        p.append(F._ball(0.12, (0, 0.01, hc + 0.05), skin, sub=2, sc=(1.05, 1.0, 1.0)))
    else:
        p.append(F._ball(0.145, (0, -0.025, hc + 0.045), hair, sub=2, sc=(1.02, 0.98, 0.85)))
    fy = 0.125
    for sx in (-1, 1):
        p.append(F._ball(0.042, (sx * 0.052, fy, hc + 0.01), white, sub=2, sc=(1, 0.6, 1.1)))
        p.append(F._ball(0.02, (sx * 0.05, fy + 0.022, hc + 0.0), black, sub=1))
        p.append(W.box((sx * 0.055, fy + 0.005, hc + 0.07), (0.07, 0.02, 0.018), hair, rot=(0, math.radians(-sx * 8), 0), bevel=0))
    p.append(F._ball(0.025, (0, fy + 0.03, hc - 0.045), skin, sub=1))
    me = F._join(p, f"pblock_{variant}_{pose}")
    _BLOCK[key] = me
    return me


def person(loc, facing_deg, seed=0, pose="stand", scale=1.0, look=None, hat=None):
    """hat: None / "cap"（作業帽）/ "straw"（麦わら帽子）。帽子は頭の上にのせて体と一緒に動く。"""
    me = person_block_mesh(seed % 12, pose, look)
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    body = bpy.data.objects.new(f"person{seed}", me)
    bpy.context.collection.objects.link(body)
    body.parent = root
    body.scale = (scale,) * 3
    root.rotation_euler = (0, 0, math.radians(-facing_deg))
    if hat:
        top_z = (0.86 if pose != "sit" else 0.2) + 0.54 + 0.22 + 0.13
        if hat == "straw":
            m = W.mat("straw", (0.86, 0.74, 0.45), 0.9)
            band = W.mat("hat_band", (0.55, 0.12, 0.10), 0.8)
            parts = [F._cyl(0.27, 0.27, 0.02, (0, 0, top_z - 0.02), m, verts=16),
                     F._cyl(0.14, 0.13, 0.11, (0, -0.01, top_z + 0.04), m, verts=12),
                     F._cyl(0.142, 0.142, 0.03, (0, -0.01, top_z + 0.0), band, verts=12)]
        else:
            m = W.mat("cap", (0.15, 0.25, 0.45), 0.8)
            parts = [F._ball(0.15, (0, -0.02, top_z - 0.03), m, sub=2, sc=(1.0, 1.0, 0.6)),
                     W.box((0, 0.13, top_z - 0.06), (0.2, 0.14, 0.015), m, bevel=0)]
        hm = F._join(parts, f"hat_{hat}")
        h = bpy.data.objects.new("hat", hm)
        bpy.context.collection.objects.link(h)
        h.parent = body
    return root, None


def frame_of(t):
    return int(round(t * FPS)) + 1


# ---------- 光と空 ----------
def daylight(elev=38.0, az=-35.0, strength=4.0, col=(1.0, 0.95, 0.88), sky=0.35):
    strength *= 1.15
    col = (min(1, col[0]), col[1] * 0.95, col[2] * 0.86)       # 参考元のような、あたたかい光
    bpy.ops.object.light_add(type='SUN')
    s = bpy.context.object
    e, a = math.radians(elev), math.radians(az)
    d = Vector((-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e)))   # 光の向き（+y 側の空から手前へ）
    s.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    s.data.energy = strength
    s.data.color = col
    s.data.angle = math.radians(2.0)
    w = bpy.data.worlds.new("sky")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.elements[0].position = 0.0
    cr.elements[0].color = (0.96, 0.90, 0.80, 1)
    cr.elements[1].position = 0.5
    cr.elements[1].color = (0.42, 0.62, 0.88, 1)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], bg.inputs[0])
    bg.inputs[1].default_value = sky * 1.3
    return s


EXPOSURE = -0.3


def night():
    global EXPOSURE
    EXPOSURE = -1.0
    bpy.ops.object.light_add(type='SUN')
    s = bpy.context.object
    s.rotation_euler = (math.radians(50), 0, math.radians(30))
    s.data.energy = 0.06
    s.data.color = (0.55, 0.65, 1.0)
    w = bpy.data.worlds.new("night")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.012, 0.016, 0.04, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 1.0


def point_light(loc, power, col=(1.0, 0.8, 0.55), radius=0.2):
    bpy.ops.object.light_add(type='POINT', location=loc)
    o = bpy.context.object
    o.data.energy = power
    o.data.color = col
    o.data.shadow_soft_size = radius
    return o


# ---------- まとめて作る（速くするため、1つのメッシュに） ----------
def multi_ball(points, m, name, sub=1):
    """points = [(x, y, z, r, (sx, sy, sz))]。たくさんの玉を1つのメッシュに。"""
    import bmesh
    bm = bmesh.new()
    for (x, y, z, r, sc) in points:
        res = bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r)
        for v in res["verts"]:
            v.co = Vector((v.co.x * sc[0] + x, v.co.y * sc[1] + y, v.co.z * sc[2] + z))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    return o


def multi_box(boxes, m, name):
    """boxes = [(x, y, z, sx, sy, sz, rot_z)]。"""
    import bmesh
    bm = bmesh.new()
    for (x, y, z, sx, sy, sz, rz) in boxes:
        res = bmesh.ops.create_cube(bm, size=1.0)
        c, s = math.cos(rz), math.sin(rz)
        for v in res["verts"]:
            px, py, pz = v.co.x * sx, v.co.y * sy, v.co.z * sz
            v.co = Vector((px * c - py * s + x, px * s + py * c + y, pz + z))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    return o


def link_copy(me, loc, name):
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.location = loc
    return o


def show_between(o, f_on=None, f_off=None, n=None, s=1.0):
    """f_on コマ目から見え、f_off コマ目から消える（大きさ 0 で隠す）。"""
    keys = {1: s if (f_on is None or f_on <= 1) else 0.0}
    if f_on and f_on > 1:
        keys[f_on - 1] = 0.0
        keys[f_on] = s
    if f_off:
        keys[f_off - 1] = s
        keys[f_off] = 0.0
    for f, v in sorted(keys.items()):
        o.scale = (max(v, 1e-4),) * 3
        o.keyframe_insert("scale", frame=f)


def windows_mat(name, wall, glass=(0.12, 0.16, 0.22)):
    """ビルの壁に窓の格子（レンガの模様を窓に見立てる）。"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.5
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0
    br.inputs["Color1"].default_value = (*glass, 1)
    br.inputs["Color2"].default_value = (*[c * 0.9 for c in glass], 1)
    br.inputs["Mortar"].default_value = (*wall, 1)
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Mortar Size"].default_value = 0.55
    br.inputs["Brick Width"].default_value = 3.0
    br.inputs["Row Height"].default_value = 4.0
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    add = nt.nodes.new("ShaderNodeMath")
    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    nt.links.new(sep.outputs["X"], add.inputs[0])
    nt.links.new(sep.outputs["Y"], add.inputs[1])
    nt.links.new(add.outputs[0], comb.inputs["X"])
    nt.links.new(sep.outputs["Z"], comb.inputs["Y"])
    nt.links.new(comb.outputs[0], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    return m


# ---------- カラス ----------
_CROW = {}


def crow_meshes():
    if _CROW:
        return _CROW
    blk = W.mat("crow_black", (0.012, 0.012, 0.016), 0.38)
    beak = W.mat("crow_beak", (0.02, 0.02, 0.022), 0.22)
    white = W.mat("eye_white", (0.95, 0.95, 0.93), 0.4)
    pupil = W.mat("crow_eye", (0.0, 0.0, 0.0), 0.15)
    # 体（尾・足を含む）。原点は足もと、くちばしが +y
    p = [F._ball(0.13, (0, 0, 0.21), blk, sub=2, sc=(0.85, 1.55, 0.95))]
    p[-1].rotation_euler.x = math.radians(15)
    p.append(W.box((0, -0.27, 0.17), (0.13, 0.24, 0.03), blk, rot=(math.radians(18), 0, 0), bevel=0))
    for sx in (-1, 1):
        p.append(F._cyl(0.012, 0.012, 0.13, (sx * 0.045, 0.02, 0.065), beak))
        p.append(W.box((sx * 0.045, 0.05, 0.006), (0.05, 0.09, 0.012), beak, bevel=0))
    _CROW["body"] = F._join(p, "crow_body")
    # 頭（原点が首のつけね。つつく動きはここで回す）
    h = [F._ball(0.085, (0, 0.03, 0.06), blk, sub=2, sc=(0.95, 1.1, 1.0))]
    h.append(F._cyl(0.038, 0.004, 0.13, (0, 0.17, 0.045), beak, rot=(math.radians(-96), 0, 0), verts=6))
    for sx in (-1, 1):
        h.append(F._ball(0.019, (sx * 0.06, 0.07, 0.08), white, sub=1))
        h.append(F._ball(0.013, (sx * 0.072, 0.077, 0.08), pupil, sub=1))
    _CROW["head"] = F._join(h, "crow_head")
    # 翼（原点が肩。はばたきで回す）
    for sx, nm in ((-1, "wing_l"), (1, "wing_r")):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        o = bpy.context.object
        o.scale = (0.17, 0.13, 0.012)
        bpy.ops.object.transform_apply(scale=True)
        for v in o.data.vertices:
            v.co.x += sx * 0.17
        o.data.materials.append(blk)
        me = o.data
        me.name = "crow_" + nm
        me.use_fake_user = True
        bpy.data.objects.remove(o)
        _CROW[nm] = me
    return _CROW


def crow(loc, facing_deg=0.0, name="crow", flying=False, scale=1.0):
    """カラス1羽。root（空）を返す。root["head"] で頭、root["wings"] で翼。facing 0 = +y。"""
    m = crow_meshes()
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    root.name = name
    root.rotation_euler.z = math.radians(-facing_deg)
    root.scale = (scale,) * 3
    body = link_copy(m["body"], (0, 0, 0), name + "_body")
    body.parent = root
    head = link_copy(m["head"], (0, 0.17, 0.27), name + "_head")
    head.parent = root
    wings = []
    for sx, nm in ((-1, "wing_l"), (1, "wing_r")):
        if flying:
            w = link_copy(m[nm], (sx * 0.08, 0.0, 0.24), name + nm)
        else:   # とまっている時は、体の横にたたむ
            w = link_copy(m[nm], (sx * 0.095, 0.06, 0.25), name + nm)
            w.rotation_euler = (math.radians(90), math.radians(-sx * 12), math.radians(-sx * 90 - sx * 6))
            w.scale = (0.85, 0.55, 1.0)
        w.parent = root
        wings.append(w)
    root["head"] = head.name
    root["wings"] = [w.name for w in wings]
    return root


def head_of(root):
    return bpy.data.objects[root["head"]]


def peck(root, f0, dur=8):
    """つつく：頭を前下へ下げて戻す。"""
    h = head_of(root)
    base = Vector((0, 0.17, 0.27))
    for f, (dy, dz, rx) in ((f0, (0, 0, 0)), (f0 + dur // 2, (0.1, -0.17, -55)), (f0 + dur, (0, 0, 0))):
        h.location = base + Vector((0, dy, dz))
        h.rotation_euler.x = math.radians(rx)
        h.keyframe_insert("location", frame=f)
        h.keyframe_insert("rotation_euler", frame=f)


def look(root, f0, deg, dur=6):
    h = head_of(root)
    h.keyframe_insert("rotation_euler", frame=f0)
    h.rotation_euler.z = math.radians(deg)
    h.keyframe_insert("rotation_euler", frame=f0 + dur)


def hop(root, f0, dpos, height=0.12, dur=8, turn=None):
    """ぴょんと跳ねる（dpos だけ動く）。"""
    p0 = root.location.copy()
    r0 = root.rotation_euler.z
    root.keyframe_insert("location", frame=f0)
    root.keyframe_insert("rotation_euler", frame=f0)
    for k in range(1, dur + 1):
        u = k / dur
        root.location = p0 + Vector(dpos) * u + Vector((0, 0, height * 4 * u * (1 - u)))
        if turn is not None:
            root.rotation_euler.z = r0 + (math.radians(-turn) - r0) * u
        root.keyframe_insert("location", frame=f0 + k)
        root.keyframe_insert("rotation_euler", frame=f0 + k)


def flap(root, f_from, f_to, period=8, amp=55):
    for i, wn in enumerate(root["wings"]):
        w = bpy.data.objects[wn]
        sx = -1 if i == 0 else 1
        for f in range(f_from, f_to + 1, 2):
            a = math.sin(2 * math.pi * (f - f_from) / period)
            w.rotation_euler = (0, math.radians(-sx * amp * a), 0)
            w.keyframe_insert("rotation_euler", frame=f)


def sparkles(center, f0, n=40, mode="out", seed=1, spread=0.18, rise=(0.4, 1.4), life=(0.6, 1.1), size=0.03, z_off=0.2):
    """光の粒。mode="out" は f0 から散って消える。"in" は集まって f0 で消える（もどってくる時）。"""
    r = random.Random(seed)
    m = W.mat("sparkle", (1, 0.97, 0.85), emit=(1.0, 0.95, 0.75), emit_strength=12)
    for k in range(n):
        o = F._ball(size * r.uniform(0.6, 1.3), (0, 0, 0), m, sub=1)
        o.visible_shadow = False
        p0 = Vector(center) + Vector((r.uniform(-spread, spread), r.uniform(-spread, spread), z_off + r.uniform(-0.08, 0.15)))
        v = Vector((r.uniform(-0.4, 0.4), r.uniform(-0.4, 0.4), r.uniform(*rise)))
        lf = r.uniform(*life)
        nfr = int(lf * FPS)
        frames = range(f0 - 1, f0 + nfr + 2)
        for f in frames:
            if mode == "out":
                dt = (f - f0) / FPS
                vis = 0 <= dt <= lf
                u = min(max(dt / lf, 0), 1)
            else:
                dt = (f0 + nfr - f) / FPS     # 時間を逆に（外から集まってくる）
                vis = f >= f0 and dt >= 0
                u = min(max(dt / lf, 0), 1)
                dt = max(dt, 0)
            o.location = p0 + v * dt
            sc = (1 - u) if vis else 0.0
            o.scale = (max(sc, 1e-4),) * 3
            o.keyframe_insert("location", frame=max(1, f))
            o.keyframe_insert("scale", frame=max(1, f))
        if f0 - 2 >= 1:
            o.scale = (1e-4,) * 3
            o.keyframe_insert("scale", frame=1)


def vanish(root, f0, seed=1, n=40):
    """カラスが光の粒になって消える。"""
    sparkles(root.location, f0, n=n, seed=seed)
    show_between(root, None, f0, s=root.scale.x)


def appear(root, f0, seed=2, n=40):
    """光の粒が集まって、カラスが現れる。"""
    sparkles(root.location, f0 - 24, n=n, mode="in", seed=seed, life=(0.6, 0.8))
    show_between(root, f0, None, s=root.scale.x)


# ---------- 町の部品 ----------
def grass_ground(size=600, col=(0.30, 0.45, 0.16), name="grass", tufts=0, area=(-8, 8, -6, 14), seed=3, avoid=None):
    m = W.mat(name, col, 1.0)
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    bpy.context.object.data.materials.append(m)
    if tufts:
        grass_tufts(tufts, area, col, seed, avoid)
    return bpy.context.object


def grass_tufts(n, area, col, seed=3, avoid=None):
    """参考元のような草の葉（細い板を少しかたむけて、たくさん立てる）。"""
    import bmesh
    r = random.Random(seed)
    bm = bmesh.new()
    x0, x1, y0, y1 = area
    for _ in range(n):
        cx, cy = r.uniform(x0, x1), r.uniform(y0, y1)
        if avoid and any(a0 <= cx <= a1 and b0 <= cy <= b1 for a0, a1, b0, b1 in avoid):
            continue
        for k in range(3):
            h = r.uniform(0.04, 0.11)
            a = r.uniform(0, 6.28)
            tilt = r.uniform(-0.4, 0.4)
            w = 0.012
            ca, sa = math.cos(a), math.sin(a)
            v1 = bm.verts.new((cx - w * ca, cy - w * sa, 0))
            v2 = bm.verts.new((cx + w * ca, cy + w * sa, 0))
            v3 = bm.verts.new((cx + tilt * h * sa * 0.5, cy - tilt * h * ca * 0.5, h))
            bm.faces.new((v1, v2, v3))
    me = bpy.data.meshes.new("tufts")
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("tufts", me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(W.mat("tuft", (col[0] * 1.05, col[1] * 1.1, col[2] * 0.9), 0.9))
    return o


def tree(loc, h=5.0, crowns=None, seed=0):
    """ローポリの木。crowns = [色...]（季節ごとに切り替える時は複数、戻り値で切り替え）。"""
    r = random.Random(seed)
    trunk = W.mat("trunk", (0.32, 0.22, 0.14), 0.9)
    F._cyl(0.18, 0.12, h * 0.55, (loc[0], loc[1], h * 0.275), trunk)
    crowns = crowns or [(0.22, 0.42, 0.14)]
    out = []
    pts = [(r.uniform(-0.6, 0.6), r.uniform(-0.6, 0.6), h * 0.62 + r.uniform(0, 0.9), r.uniform(1.0, 1.5)) for _ in range(4)]
    for i, col in enumerate(crowns):
        m = W.mat(f"leafy_{col}", col, 0.9)
        o = multi_ball([(x, y, z, rr, (1, 1, 0.85)) for x, y, z, rr in pts], m, f"crown_{seed}_{i}", sub=1)
        o.location = (loc[0], loc[1], 0)
        out.append(o)
    return out


def skyline(seed=3, y_from=260, y_to=480, x=(-300, 300), n=50, hmin=25, hmax=85):
    r = random.Random(seed)
    mats = [windows_mat("bld_w1", (0.78, 0.78, 0.80)), windows_mat("bld_w2", (0.70, 0.68, 0.64)),
            windows_mat("bld_w3", (0.62, 0.66, 0.72), glass=(0.18, 0.24, 0.32))]
    for _ in range(n):
        w, d, h = r.uniform(14, 30), r.uniform(14, 30), r.uniform(hmin, hmax)
        W.box((r.uniform(*x), r.uniform(y_from, y_to), h / 2), (w, d, h), r.choice(mats), bevel=0)


def pole_and_wires(y=12.0, x_poles=(-14, 14), z=8.0, n_wires=3):
    m = W.mat("pole", (0.62, 0.62, 0.60), 0.8)
    wire = W.mat("wire", (0.05, 0.05, 0.05), 0.6)
    for x in x_poles:
        F._cyl(0.16, 0.13, z + 1.5, (x, y, (z + 1.5) / 2), m)
        W.box((x, y, z + 0.2), (0.15, 2.2, 0.15), m, bevel=0)
    zs = []
    for k in range(n_wires):
        yy = y - 0.8 + k * 0.8
        W.box((0, yy, z + 0.3), (80, 0.03, 0.03), wire, bevel=0)
        zs.append((yy, z + 0.3))
    return zs


def crumbs(seed, n, x0, x1, y0, y1, z=0.005):
    r = random.Random(seed)
    m = W.mat("crumb", (0.85, 0.70, 0.45), 0.9)
    return multi_box([(r.uniform(x0, x1), r.uniform(y0, y1), z + 0.01, 0.03, 0.03, 0.02, r.uniform(0, 3)) for _ in range(n)],
                     m, f"crumbs{seed}")


def path(x0, x1, y0, y1):
    W.box(((x0 + x1) / 2, (y0 + y1) / 2, 0.01), (x1 - x0, y1 - y0, 0.02), W.mat("gravel", (0.74, 0.62, 0.45), 1.0), bevel=0)


def grandpa(loc=(0.05, 0.05, 0.05), facing=180, seed=4):
    root, _ = person(loc, facing, seed=seed, pose="sit", look=GRANDPA)
    for c in root.children:
        c.location.z += 0.25
    return root


# ---------- 公園（冒頭・静かな朝・毎朝・再会） ----------
def park_set(season=None, wire_crows=0, seed=1):
    """ベンチは原点（座る人は -y を向く）。うしろに電線と新宿のビル。"""
    grass_ground(col=(0.30, 0.42, 0.14), tufts=5000, area=(-7, 7, -7, 8), avoid=[(-2.7, 2.7, -2.7, 1.1)])
    path(-2.6, 2.6, -2.6, 1.0)
    F.bench((0, 0, 0), rot_deg=90)
    crowns = [(0.22, 0.42, 0.14)] if season is None else [(0.95, 0.72, 0.80), (0.20, 0.42, 0.13), (0.85, 0.42, 0.10), (0.50, 0.42, 0.34)]
    trees = []
    for i, (x, y, h) in enumerate(((-5.5, 3.5, 6.0), (5.0, 4.5, 5.5), (-11, 9, 7), (10, 10, 6.5), (-3.0, 14, 6.0), (16, 5, 6))):
        trees.append(tree((x, y, 0), h=h, crowns=crowns, seed=seed * 10 + i))
    zs = pole_and_wires(y=12.0)
    skyline()
    lamp = W.mat("pole", (0.62, 0.62, 0.60), 0.8)
    F._cyl(0.06, 0.06, 3.5, (2.6, 0.4, 1.75), lamp)
    W.box((2.6, 0.4, 3.55), (0.35, 0.35, 0.25), W.mat("lamp_head", (0.9, 0.9, 0.85), 0.5), bevel=0.03)
    crows_on_wire = []
    r = random.Random(seed)
    xs = sorted(r.uniform(-12, 12) for _ in range(wire_crows))
    for i, x in enumerate(xs):
        yy, z = zs[i % len(zs)]
        crows_on_wire.append(crow((x, yy, z + 0.01), facing_deg=180 + r.uniform(-30, 30), name=f"wire{i}"))
    return trees, crows_on_wire


def park_cam(loc=(-1.7, -4.3, 1.0), at=(0.1, -0.5, 1.0), lens=34):
    return W.camera(loc, at, lens)


def c01_open(nf):
    daylight(elev=24, az=-50, strength=4.2, col=(1.0, 0.82, 0.62), sky=0.4)
    trees, wc = park_set(wire_crows=9)
    grandpa()
    crumbs(1, 60, -0.8, 0.9, -1.9, -0.7)
    kuro = crow((0.35, -1.25, 0.0), facing_deg=170, name="kuro", scale=1.2)
    fv = frame_of(TL.T_VANISH)
    for f in (10, 52, 92, 130):
        peck(kuro, f)
    look(kuro, 70, 25)
    look(kuro, 112, -10)
    hop(kuro, 140, (-0.18, 0.12, 0), turn=200, dur=8)
    vanish(kuro, fv, seed=3, n=50)
    for i, c in enumerate(wc):
        vanish(c, fv + i % 4, seed=20 + i, n=18)
    park_cam()
    return nf


def c02_wire(nf):
    """同じ瞬間、新宿の電線にとまっていた群れが消える（下から見上げる）。"""
    daylight(elev=20, az=-40, strength=4.0, col=(1.0, 0.86, 0.68), sky=0.4)
    grass_ground(col=(0.42, 0.42, 0.42), name="asphalt")
    zs = pole_and_wires(y=6.0, x_poles=(-9, 9), z=8.0, n_wires=3)
    skyline(seed=5, y_from=70, y_to=220, x=(-120, 120), n=30, hmin=30, hmax=90)
    r = random.Random(4)
    cs = []
    for i in range(22):
        yy, z = zs[i % 3]
        x = -8.5 + i * 0.8 + r.uniform(-0.2, 0.2)
        cs.append(crow((x, yy, z + 0.01), facing_deg=180 + r.uniform(-40, 40), name=f"w{i}", scale=1.1))
    for i in range(4):     # 空を飛んでいたカラスも
        c = crow((-6 + i * 4.0, 14 + i * 3, 13 + i * 1.5), facing_deg=90 + r.uniform(-20, 20), name=f"fly{i}", flying=True, scale=1.2)
        flap(c, 1, 40, period=7 + i)
        c.keyframe_insert("location", frame=1)
        c.location.x += 1.2
        c.keyframe_insert("location", frame=30)
        cs.append(c)
    for i, c in enumerate(cs):
        vanish(c, 4 + (i * 7) % 16, seed=40 + i, n=24)
    W.camera((0.6, -0.8, 5.6), (0.0, 6.0, 8.2), lens=30)
    return nf


def c03_quiet(nf):
    daylight(elev=24, az=-50, strength=4.2, col=(1.0, 0.82, 0.62), sky=0.4)
    park_set()
    g = grandpa()
    crumbs(1, 60, -0.8, 0.9, -1.9, -0.7)
    for f, d in ((1, 180), (30, 180), (45, 215), (75, 215), (90, 150), (120, 150)):
        g.rotation_euler.z = math.radians(-d)
        g.keyframe_insert("rotation_euler", frame=f)
    W.camera((1.6, -3.6, 1.05), (0.0, 0.0, 1.0), lens=35)
    return nf


def c11_bench(nf):
    """毎朝パンくずをまく（春・夏・秋・冬で SEG コマずつ）。"""
    SEG = nf // 4
    daylight(elev=24, az=-50, strength=4.2, col=(1.0, 0.84, 0.66), sky=0.4)
    trees, _ = park_set(season=True)
    grandpa()
    snow = W.mat("snow", (0.92, 0.93, 0.96), 0.9)
    bpy.ops.mesh.primitive_plane_add(size=120, location=(0, 0, 0.03))
    sn = bpy.context.object
    sn.data.materials.append(snow)
    show_between(sn, 3 * SEG + 1, None)
    for ts in trees:
        for k, o in enumerate(ts):
            show_between(o, 1 + SEG * k if k else None, 1 + SEG * (k + 1) if k < 3 else None)
    for k in range(4):
        c = crumbs(10 + k, 40, -0.8, 0.9, -1.9, -0.7, z=0.04)
        show_between(c, 1 + SEG * k + 10, 1 + SEG * (k + 1) if k < 3 else None)
    W.camera((-2.6, -5.6, 1.35), (0.0, -0.2, 0.8), lens=32)
    return nf


def c12_return(nf):
    daylight(elev=24, az=-50, strength=4.2, col=(1.0, 0.82, 0.62), sky=0.4)
    trees, wc = park_set(wire_crows=9)
    g = grandpa()
    crumbs(1, 60, -0.8, 0.9, -1.9, -0.7)
    f_back = 61                                   # 10年ちょうど（×1 の2秒後）
    kuro = crow((0.45, -1.6, 0.0), facing_deg=20, name="kuro", scale=1.2)
    appear(kuro, f_back + 6, seed=5, n=60)
    for i, c in enumerate(wc):
        appear(c, f_back + 6 + i % 5, seed=60 + i, n=14)
    look(kuro, 90, 30)
    peck(kuro, 105)
    hop(kuro, 125, (-0.1, 0.25, 0), dur=8, turn=0)
    hop(kuro, 140, (-0.1, 0.25, 0), dur=8)
    hop(kuro, 162, (0.35, 1.05, 0.49), height=0.35, dur=12, turn=-90)   # ベンチの上（おじいさんの右どなり）へ
    look(kuro, 200, -40)
    peck(kuro, 230, dur=10)
    for f, d in ((1, 180), (150, 180), (175, 125), (270, 125)):     # おじいさんがクロの方を向く
        g.rotation_euler.z = math.radians(-d)
        g.keyframe_insert("rotation_euler", frame=f)
    cam = W.camera((-2.6, -6.2, 1.2), (0.0, -0.4, 0.8), lens=32)
    cam.keyframe_insert("location", frame=1)
    cam.keyframe_insert("location", frame=120)
    cam.location = (-1.7, -4.2, 1.15)
    cam.keyframe_insert("location", frame=270)
    return nf


# ---------- ゴミ置き場 ----------
def garbage_station(torn=False, seed=1):
    wall = W.mat("block_wall", (0.68, 0.67, 0.64), 0.9)
    W.box((0, 1.4, 0.75), (7, 0.2, 1.5), wall, bevel=0.01)
    W.box((-2.2, 0.4, 0.06), (8, 3.5, 0.12), W.mat("sidewalk", (0.66, 0.64, 0.60), 0.9), bevel=0)
    r = random.Random(seed)
    bag = W.mat("bag", (0.80, 0.86, 0.92), 0.3)
    bag2 = W.mat("bag_y", (0.95, 0.92, 0.70), 0.3)
    pts = [(r.uniform(-1.0, 1.0), r.uniform(0.3, 1.1), 0.3 + 0.2 * (k > 8), r.uniform(0.25, 0.33), (1, 1, 0.85)) for k in range(14)]
    multi_ball(pts[::2], bag, "bags_a", sub=2)
    multi_ball(pts[1::2], bag2, "bags_b", sub=2)
    if not torn:
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0.7, 0.62))
        net = bpy.context.object
        net.scale = (2.8, 1.6, 1)
        net.rotation_euler.x = math.radians(-10)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=24)
        bpy.ops.object.mode_set(mode='OBJECT')
        wf = net.modifiers.new("wf", "WIREFRAME")
        wf.thickness = 0.012
        wf.thickness = 0.02
        net.data.materials.append(W.mat("net", (0.05, 0.55, 0.30), 0.7))
    else:
        cols = [(0.85, 0.30, 0.20), (0.95, 0.85, 0.30), (0.40, 0.60, 0.25), (0.75, 0.55, 0.35)]
        for i, c in enumerate(cols):
            multi_box([(r.uniform(-1.8, 1.8), r.uniform(-1.4, 0.4), 0.13, r.uniform(0.05, 0.14), r.uniform(0.05, 0.12), 0.03,
                        r.uniform(0, 3)) for _ in range(14)], W.mat(f"scrap{i}", c, 0.8), f"scraps{i}")
    sign = W.mat("sign", (0.95, 0.95, 0.92), 0.6)
    F._cyl(0.03, 0.03, 1.6, (1.6, 1.25, 0.8), W.mat("pole", (0.62, 0.62, 0.60), 0.8))
    W.box((1.6, 1.2, 1.5), (0.6, 0.03, 0.4), sign, bevel=0)
    W.box((1.6, 1.18, 1.5), (0.5, 0.02, 0.08), W.mat("sign_green", (0.15, 0.5, 0.25), 0.6), bevel=0)


def street_back(seed=7, night_mode=False):
    grass_ground(col=(0.36, 0.36, 0.37), name="asphalt")
    r = random.Random(seed)
    wall = [W.mat("wall_a", (0.86, 0.82, 0.74)), W.mat("wall_b", (0.78, 0.76, 0.72)), W.mat("wall_c", (0.90, 0.88, 0.82))]
    roof = [W.mat("roof_a", (0.30, 0.22, 0.20)), W.mat("roof_b", (0.22, 0.26, 0.32))]
    win = W.mat("win_night" if night_mode else "win_day", (0.95, 0.80, 0.50) if night_mode else (0.25, 0.32, 0.40),
                emit=(1.0, 0.75, 0.45) if night_mode else None, emit_strength=1.5 if night_mode else 0)
    for i in range(10):
        x = -16 + i * 3.6 + r.uniform(-0.3, 0.3)
        y = 9 + r.uniform(0, 3)
        h = r.uniform(4.5, 6.5)
        W.box((x, y, h / 2), (3.2, 6, h), r.choice(wall), bevel=0.03)
        W.box((x, y, h + 0.5), (3.6, 6.4, 1.0), r.choice(roof), bevel=0.3)
        for k in range(2):
            if r.random() < 0.7:
                W.box((x + r.uniform(-0.8, 0.8), y - 3.01, 1.8 + k * 2.6), (0.9, 0.04, 1.0), win, bevel=0)
    skyline(seed=8)


def c04_garbage(nf):
    daylight(elev=22, az=-55, strength=4.2, col=(1.0, 0.88, 0.72), sky=0.4)
    street_back()
    garbage_station()
    p, _ = person((-1.3, -0.5, 0.12), 150, seed=7, hat="cap")
    W.camera((-2.4, -4.2, 1.4), (-0.2, 0.6, 0.8), lens=30)
    return nf


def c08_rats(nf):
    night()
    street_back(night_mode=True)
    garbage_station(torn=True, seed=3)
    pole = W.mat("pole", (0.62, 0.62, 0.60), 0.8)
    F._cyl(0.08, 0.08, 4.5, (-2.5, 1.0, 2.25), pole)
    W.box((-2.1, 1.0, 4.45), (0.9, 0.3, 0.12), W.mat("lamp_glow", (1, 0.9, 0.7), emit=(1.0, 0.85, 0.6), emit_strength=20), bevel=0)
    point_light((-1.8, 0.8, 4.2), 140, radius=0.3)
    rats(nf)
    W.camera((-2.4, -4.4, 1.3), (0.0, 0.3, 0.3), lens=30)
    return nf


def rat_mesh():
    if "rat" in _CROW:
        return _CROW["rat"]
    g = W.mat("rat_fur", (0.30, 0.27, 0.25), 0.9)
    pink = W.mat("rat_pink", (0.75, 0.50, 0.48), 0.7)
    blk = W.mat("crow_eye", (0, 0, 0), 0.15)
    p = [F._ball(0.07, (0, 0, 0.07), g, sub=2, sc=(0.85, 1.6, 0.8))]
    p.append(F._cyl(0.05, 0.012, 0.1, (0, 0.13, 0.07), g, rot=(math.radians(-90), 0, 0), verts=7))
    for sx in (-1, 1):
        p.append(F._ball(0.025, (sx * 0.035, 0.1, 0.12), pink, sub=1, sc=(1, 0.4, 1)))
        p.append(F._ball(0.01, (sx * 0.028, 0.15, 0.09), blk, sub=1))
    p.append(F._cyl(0.008, 0.004, 0.25, (0, -0.22, 0.04), pink, rot=(math.radians(80), 0, 0), verts=5))
    _CROW["rat"] = F._join(p, "rat")
    return _CROW["rat"]


def rats(nf, n=14, seed=5):
    me = rat_mesh()
    r = random.Random(seed)
    for k in range(n):
        o = link_copy(me, (0, 0, 0), f"rat{k}")
        x, y = r.uniform(-1.6, 1.6), r.uniform(-1.2, 0.6)
        tx, ty = x, y
        ang = r.uniform(0, 6.28)
        t_next = 0
        for f in range(1, nf + 1, 2):
            if f >= t_next:
                tx, ty = r.uniform(-1.9, 1.9), r.uniform(-1.4, 0.7)
                t_next = f + r.randint(14, 40)
            dx, dy = tx - x, ty - y
            d = math.hypot(dx, dy)
            if d > 0.05:
                step = min(d, 0.07)
                x += dx / d * step
                y += dy / d * step
                ang = math.atan2(dy, dx) - math.pi / 2
            o.location = (x, y, 0.12 + 0.015 * abs(math.sin(f * 0.9 + k)))
            o.rotation_euler.z = ang
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("rotation_euler", frame=f)
        if k >= 8:     # だんだん増える
            show_between(o, 20 + (k - 8) * 12, None)


# ---------- りんご畑 ----------
def c05_orchard(nf):
    daylight(elev=40, az=-35, strength=4.5)
    grass_ground(col=(0.32, 0.44, 0.15), tufts=3500, area=(-5, 5, -5, 4))
    r = random.Random(3)
    trunk = W.mat("trunk", (0.32, 0.22, 0.14), 0.9)
    leaf = W.mat("leafy_apple", (0.20, 0.42, 0.14), 0.9)
    red = W.mat("apple", (0.78, 0.08, 0.06), 0.45)
    crowns, apples = [], []
    for row in range(5):
        for col in range(-3, 4):
            x, y = col * 4.2 + (row % 2) * 1.2, 2 + row * 4.5
            F._cyl(0.15, 0.1, 1.6, (x, y, 0.8), trunk)
            for k in range(3):
                crowns.append((x + r.uniform(-0.6, 0.6), y + r.uniform(-0.6, 0.6), 2.2 + r.uniform(0, 0.6), r.uniform(0.9, 1.2), (1, 1, 0.8)))
            for k in range(18):
                a, el = r.uniform(0, 6.28), r.uniform(-0.5, 0.6)
                rr = 1.12
                apples.append((x + rr * math.cos(a) * math.cos(el), y + rr * math.sin(a) * math.cos(el), 2.5 + 0.8 * rr * math.sin(el), 0.085, (1, 1, 1)))
    multi_ball(crowns, leaf, "orchard_leaves", sub=1)
    multi_ball(apples, red, "apples", sub=1)
    mt = W.mat("mountain", (0.35, 0.45, 0.55), 1.0)
    for i in range(7):
        bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=r.uniform(60, 110), depth=r.uniform(45, 80),
                                        location=(-250 + i * 85, 330 + r.uniform(0, 60), 20))
        bpy.context.object.data.materials.append(mt)
    p, _ = person((0.6, -1.0, 0), 200, seed=2, hat="straw")
    W.box((0.95, -0.8, 0.85), (0.4, 0.3, 0.25), W.mat("basket", (0.55, 0.38, 0.18), 0.9), bevel=0.02)
    multi_ball([(0.95 + r.uniform(-0.12, 0.12), -0.8 + r.uniform(-0.08, 0.08), 1.0, 0.07, (1, 1, 1)) for _ in range(6)], red, "basket_apples")
    W.camera((-1.0, -3.8, 1.45), (0.4, -0.3, 1.35), lens=32)
    return nf


# ---------- 国道沿いの死がい ----------
def tanuki():
    fur = W.mat("tanuki", (0.42, 0.34, 0.26), 0.95)
    dark = W.mat("tanuki_dark", (0.10, 0.08, 0.07), 0.9)
    p = [F._ball(0.16, (0, 0, 0.12), fur, sub=2, sc=(1.0, 1.9, 0.75))]
    p.append(F._ball(0.11, (0.02, 0.33, 0.1), fur, sub=2, sc=(1.0, 1.1, 0.8)))
    p.append(F._ball(0.05, (0.0, 0.43, 0.08), dark, sub=1, sc=(1, 1.2, 0.8)))
    p.append(F._ball(0.06, (0.0, -0.36, 0.08), fur, sub=1, sc=(0.9, 1.8, 0.8)))
    for sx, sy in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
        p.append(F._cyl(0.03, 0.025, 0.2, (sx * 0.12, sy * 0.15, 0.1), dark, rot=(0, math.radians(sx * 70), 0)))
    me = F._join(p, "tanuki")
    o = link_copy(me, (0, 1.4, 0.05), "tanuki_obj")
    o.rotation_euler = (0, math.radians(75), math.radians(20))
    return o


def flies(nf, center, n, radius=0.6, seed=7, grow=None, spread_up=0.5, swarm=None, name="fly"):
    """ハエ（小さな黒い点）。grow=(f_from, f_to) で数がふえていく。swarm(f) が中心を返せば群れが動く。"""
    r = random.Random(seed)
    m = W.mat("fly", (0.02, 0.02, 0.02), 0.4)
    me = bpy.data.meshes.get("fly_mesh")
    if me is None:
        o = F._ball(0.012, (0, 0, 0), m, sub=1, sc=(1.0, 1.4, 0.8))
        me = o.data
        me.name = "fly_mesh"
        me.use_fake_user = True
        bpy.data.objects.remove(o)
    for k in range(n):
        o = link_copy(me, (0, 0, 0), f"{name}{k}")
        rad = radius * r.uniform(0.3, 1.0)
        w = r.uniform(3, 7) * r.choice((-1, 1))
        ph = r.uniform(0, 6.28)
        zb = r.uniform(0.05, spread_up)
        for f in range(1, nf + 1, 3):
            t = f / FPS
            c = Vector(swarm(f)) if swarm else Vector(center)
            o.location = c + Vector((rad * math.cos(w * t + ph), rad * math.sin(w * t * 1.3 + ph), zb + 0.15 * math.sin(t * 5 + k)))
            o.keyframe_insert("location", frame=f)
        if grow:
            f_on = int(grow[0] + (grow[1] - grow[0]) * k / n)
            show_between(o, f_on, None)


def road_set(seed=5):
    grass_ground(col=(0.32, 0.42, 0.14), tufts=3000, area=(-5, 5, -4, 0.9))
    W.box((0, 5.0, 0.02), (300, 7.5, 0.04), W.mat("asphalt", (0.25, 0.25, 0.26), 0.9), bevel=0)
    W.box((0, 1.6, 0.045), (300, 0.12, 0.01), W.mat("line_white", (0.95, 0.95, 0.92), 0.6), bevel=0)
    W.box((0, 5.0, 0.045), (300, 0.12, 0.01), W.mat("line_yellow", (0.95, 0.75, 0.15), 0.6), bevel=0)
    rail = W.mat("guard", (0.88, 0.88, 0.86), 0.4)
    W.box((0, 9.3, 0.7), (300, 0.06, 0.3), rail, bevel=0)
    for x in range(-60, 61, 4):
        W.box((x, 9.35, 0.35), (0.1, 0.1, 0.7), rail, bevel=0)
    zs = pole_and_wires(y=11.5, x_poles=(-30, 0, 30), z=8.0)
    r = random.Random(seed)
    mt = W.mat("mountain", (0.32, 0.45, 0.30), 1.0)
    for i in range(6):
        bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=r.uniform(50, 90), depth=r.uniform(40, 70),
                                        location=(-200 + i * 80, 260 + r.uniform(0, 60), 15))
        bpy.context.object.data.materials.append(mt)
    for i in range(10):
        tree((r.uniform(-40, 40), r.uniform(16, 40), 0), h=r.uniform(5, 7), seed=50 + i)
    return r


def car(y, color=(0.75, 0.12, 0.10)):
    """ローポリの乗用車（+x へ走る）。root を返す。"""
    body = W.mat(f"car_{color}", color, 0.3)
    glass = W.mat("car_glass2", (0.08, 0.10, 0.13), 0.1)
    tire = W.mat("tire", (0.05, 0.05, 0.05), 0.8)
    bpy.ops.object.empty_add(location=(0, y, 0))
    root = bpy.context.object
    parts = [W.box((0, 0, 0.55), (4.2, 1.7, 0.6), body, bevel=0.12),
             W.box((-0.2, 0, 1.05), (2.3, 1.55, 0.5), glass, bevel=0.1),
             W.box((-0.2, 0, 1.33), (2.2, 1.5, 0.08), body, bevel=0.04)]
    for x in (-1.35, 1.35):
        for yy in (-0.8, 0.8):
            parts.append(F._cyl(0.33, 0.33, 0.22, (x, yy, 0.33), tire, rot=(math.radians(90), 0, 0), verts=12))
    for p in parts:
        p.parent = root
    return root


# ---------- クルミが割れない（宮城・仙台） ----------
def c05b_walnut(nf):
    daylight(elev=45, az=-30, strength=4.6)
    r = road_set(seed=12)
    nut = W.mat("walnut", (0.42, 0.30, 0.17), 0.8)
    multi_ball([(r.uniform(-0.4, 2.6), r.uniform(1.6, 3.6), 0.065, 0.065, (1, 1, 0.9)) for _ in range(10)], nut, "walnuts", sub=2)
    tree((-3.5, 0.0, 0), h=7.5, seed=21)
    tree((3.8, -1.0, 0), h=6.5, seed=22)
    multi_ball([(r.uniform(-4.5, -2.5), r.uniform(-1, 1), 0.04, 0.05, (1, 1, 0.9)) for _ in range(12)], nut, "walnuts_grass", sub=1)
    c = car(3.0)
    for f, x in ((1, -40.0), (nf, 40.0)):
        c.location.x = x
        c.keyframe_insert("location", frame=f)
    c2 = car(6.5, color=(0.85, 0.85, 0.88))
    c2.rotation_euler.z = math.pi
    for f, x in ((1, 60.0), (nf, -30.0)):
        c2.location.x = x
        c2.keyframe_insert("location", frame=f)
    W.camera((-0.8, -0.2, 0.65), (1.1, 2.6, 0.1), lens=30)
    return nf


# ---------- トビがやってきた ----------
def kite_bird(loc, name, flying=True):
    """トビ：カラスの形を茶色にして、翼を長く。"""
    m = crow_meshes()
    br = W.mat("kite_brown", (0.30, 0.20, 0.13), 0.7)
    root = crow(loc, 0, name=name, flying=flying, scale=1.5)
    for ch in root.children:
        ch.data = ch.data.copy()
        ch.data.materials[0] = br
        if "wing" in ch.name and flying:
            ch.scale = (1.7, 1.0, 1.0)
    return root


def c06b_kite(nf):
    daylight(elev=50, az=-20, strength=4.8, col=(1.0, 0.95, 0.85))
    r = road_set()
    tanuki()
    flies(nf, (0, 1.4, 0.1), 40, radius=0.5)
    for k in range(2):
        kb = kite_bird((0, 0, 0), f"kite{k}")
        flap(kb, 1, nf, period=26, amp=18)
        for f in range(1, nf + 1, 3):
            a = f / 40 + k * 3.1
            kb.location = (math.cos(a) * (6 + k * 3), 8 + math.sin(a) * 4, 9 + k * 2)
            kb.rotation_euler.z = a + math.pi
            kb.keyframe_insert("location", frame=f)
            kb.keyframe_insert("rotation_euler", frame=f)
    k3 = kite_bird((0.6, 1.7, 0), "kite_ground", flying=False)       # 死がいに降りたトビ
    k3.rotation_euler.z = math.radians(-120)
    for f in range(20, nf, 28):
        peck(k3, f, dur=10)
    W.camera((-2.0, -1.9, 1.0), (0.2, 1.8, 0.6), lens=30)
    return nf


# ---------- 熊野の神社と八咫烏 ----------
def crest_texture():
    from PIL import Image, ImageDraw
    p = os.path.join(HERE, "assets", "crest.png")
    if os.path.exists(p):
        return p
    os.makedirs(os.path.dirname(p), exist_ok=True)
    im = Image.new("RGB", (512, 512), (240, 236, 225))
    d = ImageDraw.Draw(im)
    d.ellipse((40, 40, 472, 472), fill=(200, 40, 35))
    k = (15, 15, 18)
    d.ellipse((190, 170, 330, 330), fill=k)                              # 体
    d.ellipse((290, 120, 370, 200), fill=k)                              # 頭
    d.polygon([(360, 150), (420, 165), (360, 180)], fill=k)              # くちばし
    d.polygon([(200, 230), (90, 120), (150, 260)], fill=k)               # 翼
    d.polygon([(310, 240), (430, 300), (300, 300)], fill=k)
    d.polygon([(200, 300), (130, 380), (230, 320)], fill=k)              # 尾
    for x in (235, 260, 285):                                            # 三本の足
        d.line((x, 320, x - 10, 400), fill=k, width=10)
    im.save(p)
    return p


def c10b_shrine(nf):
    daylight(elev=35, az=-40, strength=4.4)
    grass_ground(col=(0.30, 0.40, 0.14), tufts=1200, area=(-6, 6, -6, 0), avoid=[(-1.6, 1.6, -7, 12)])
    path(-1.5, 1.5, -8, 12)
    red = W.mat("torii_red", (0.80, 0.20, 0.10), 0.6)
    blk = W.mat("torii_black", (0.08, 0.07, 0.07), 0.6)
    for x in (-1.9, 1.9):
        F._cyl(0.18, 0.18, 4.6, (x, 3.0, 2.3), red, verts=12)
    W.box((0, 3.0, 4.75), (5.6, 0.45, 0.3), blk, bevel=0.03)
    W.box((0, 3.0, 4.45), (5.0, 0.35, 0.25), red, bevel=0.02)
    W.box((0, 3.0, 3.7), (4.4, 0.3, 0.22), red, bevel=0.02)
    wood = W.mat("shrine_wood", (0.50, 0.32, 0.18), 0.8)
    roof = W.mat("shrine_roof", (0.20, 0.28, 0.26), 0.7)
    W.box((0, 11, 1.6), (6, 4.5, 3.2), wood, bevel=0.05)
    W.box((0, 11, 3.6), (7.4, 5.8, 0.8), roof, rot=(0, 0, 0), bevel=0.3)
    flag = img_mat("crest", crest_texture())
    for x in (-3.2, 3.2):
        F._cyl(0.05, 0.05, 4.2, (x, 5.0, 2.1), W.mat("pole", (0.62, 0.62, 0.60), 0.8))
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x + (0.55 if x < 0 else -0.55), 4.98, 3.3))
        fl = bpy.context.object
        fl.scale = (0.95, 1.0, 1.4)
        fl.rotation_euler.x = math.radians(90)
        fl.data.materials.append(flag)
    r = random.Random(8)
    for i in range(14):
        tree((r.choice((-1, 1)) * r.uniform(5, 14), r.uniform(-2, 18), 0), h=r.uniform(8, 12), seed=80 + i,
             crowns=[(0.14, 0.30, 0.12)])
    person((-0.4, 1.0, 0), 0, seed=5)
    person((0.5, 0.6, 0), 10, seed=8, look={"top": (0.85, 0.85, 0.82)})
    W.camera((0.3, -5.5, 1.5), (0.0, 4.0, 2.6), lens=28)
    return nf


def c06_road(nf):
    daylight(elev=55, az=-20, strength=4.8, col=(1.0, 0.95, 0.85))
    r = road_set()
    tanuki()
    # くさる時のガス（緑がかったもや）
    pts = [(r.uniform(-0.25, 0.25), 1.4 + r.uniform(-0.25, 0.25), 0.12, 1.0 + i * 0.16, 0) for i in range(28)]
    F.puffs(pts, [sec(f) for f in range(1, nf + 1)], seed=8, col=(0.62, 0.72, 0.28), alpha=0.10, size=(0.05, 0.09),
            rise=(0.35, 0.8), grow=2.2, life=3.0, name="gas")
    flies(nf, (0, 1.4, 0.1), 70, radius=0.55, grow=(20, 160))
    cam = W.camera((-2.3, -2.4, 1.1), (0.0, 1.5, 0.45), lens=30)
    return nf


# ---------- ハエの大発生 ----------
def c07_flies(nf):
    daylight(elev=50, az=-30, strength=4.6)
    grass_ground(col=(0.32, 0.44, 0.15), tufts=3500, area=(-6, 5, -8, 2))
    r = random.Random(9)
    wall = W.mat("wall_c", (0.90, 0.88, 0.82))
    roof = W.mat("roof_b", (0.22, 0.26, 0.32))
    glass = W.mat("win_day", (0.25, 0.32, 0.40))
    for i, x in enumerate((-8, 0, 8)):
        W.box((x, 6, 2.8), (6.5, 6, 5.6), wall, bevel=0.03)
        W.box((x, 6, 6.1), (7.2, 6.6, 1.2), roof, bevel=0.4)
        W.box((x - 1.2, 2.98, 1.6), (1.8, 0.04, 1.3), glass, bevel=0)
        W.box((x + 1.6, 2.98, 4.2), (1.4, 0.04, 1.1), glass, bevel=0)
    W.box((0, 2.0, 0.5), (24, 0.15, 1.0), W.mat("block_wall", (0.68, 0.67, 0.64), 0.9), bevel=0)
    skyline(seed=11, y_from=60, y_to=160, n=22, hmin=20, hmax=70)
    for i in range(3):
        tree((-11 + i * 11, 10, 0), h=6, seed=70 + i)
    # 網戸にとまるハエ（だんだん増える）
    me_dots = []
    for k in range(4):
        o = multi_box([(-1.2 + r.uniform(-0.85, 0.85), 2.95, 1.6 + r.uniform(-0.6, 0.6), 0.025, 0.01, 0.018, 0) for _ in range(30)],
                      W.mat("fly", (0.02, 0.02, 0.02), 0.4), f"screen_flies{k}")
        show_between(o, 20 + k * 35, None)
    p, _ = person((1.4, 0.3, 0), 205, seed=9)
    # 大きな群れ：庭の上を雲のようにうねって動く
    flies(nf, (0, 0, 0), 520, radius=1.6, grow=(1, 120), spread_up=1.2, seed=13,
          swarm=lambda f: (-2.5 + 3.0 * f / nf, 0.5 + 0.6 * math.sin(f / 25), 1.4 + 0.4 * math.sin(f / 17)))
    W.camera((-4.2, -8.5, 1.6), (-0.6, 2.0, 2.1), lens=28)
    return nf


# ---------- キャベツ畑と小鳥 ----------
def small_bird_mesh():
    if "bird" in _CROW:
        return _CROW["bird"]
    g = W.mat("bird_gray", (0.42, 0.40, 0.40), 0.8)
    br = W.mat("bird_brown", (0.45, 0.30, 0.22), 0.8)
    p = [F._ball(0.06, (0, 0, 0.08), g, sub=2, sc=(0.85, 1.5, 0.9))]
    p.append(F._ball(0.04, (0, 0.08, 0.13), g, sub=1))
    p.append(F._ball(0.012, (0.026, 0.1, 0.14), br, sub=1))
    p.append(F._cyl(0.012, 0.002, 0.04, (0, 0.13, 0.13), W.mat("crow_beak", (0.02, 0.02, 0.022), 0.22), rot=(math.radians(-90), 0, 0), verts=5))
    p.append(W.box((0, -0.12, 0.08), (0.05, 0.12, 0.012), br, bevel=0))
    _CROW["bird"] = F._join(p, "bird")
    wing = W.box((0, 0, 0), (0.18, 0.07, 0.008), br, bevel=0)
    _CROW["bird_wing"] = wing.data
    wing.data.use_fake_user = True
    bpy.data.objects.remove(wing)
    return _CROW["bird"]


def c09_birds(nf):
    daylight(elev=45, az=-30, strength=4.6)
    grass_ground(col=(0.45, 0.36, 0.22), name="dirt")
    r = random.Random(4)
    cab = W.mat("cabbage", (0.45, 0.68, 0.30), 0.7)
    cab2 = W.mat("cabbage_out", (0.25, 0.48, 0.20), 0.8)
    inner, outer = [], []
    for row in range(-14, 15):
        for k in range(0, 34):
            x, y = row * 0.9, -2 + k * 0.85
            inner.append((x, y, 0.18, 0.2, (1, 1, 0.9)))
            outer.append((x, y, 0.1, 0.32, (1, 1, 0.45)))
    multi_ball(inner, cab, "cabbage_in", sub=2)
    multi_ball(outer, cab2, "cabbage_outer", sub=1)
    mt = W.mat("mountain", (0.32, 0.45, 0.30), 1.0)
    for i in range(6):
        bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=r.uniform(50, 90), depth=r.uniform(40, 70),
                                        location=(-200 + i * 80, 240 + r.uniform(0, 60), 15))
        bpy.context.object.data.materials.append(mt)
    p, _ = person((0.4, -1.2, 0), 190, seed=3, hat="straw")
    me = small_bird_mesh()
    wing = _CROW["bird_wing"]
    # 群れ：右上から左手前へ低く横切る（地面に影が流れる）
    for k in range(70):
        o = link_copy(me, (0, 0, 0), f"b{k}")
        o.scale = (1.6,) * 3
        ws = []
        for sx in (-1, 1):
            w = link_copy(wing, (sx * 0.09, 0, 0.1), f"b{k}w{sx}")
            w.parent = o
            ws.append((sx, w))
        dx, dy, dz = r.uniform(-3, 3), r.uniform(-3, 3), r.uniform(-1.2, 1.2)
        lag = r.uniform(0, 12)
        for f in range(1, nf + 1, 2):
            u = (f - lag) / nf
            o.location = (9 - 16 * u + dx, 14 - 10 * u + dy, 4.5 - 1.5 * u + dz + 0.3 * math.sin(f / 6 + k))
            o.rotation_euler.z = math.radians(150)
            o.keyframe_insert("location", frame=f)
            for sx, w in ws:
                w.rotation_euler.y = math.radians(-sx * 50 * math.sin(f * 1.3 + k))
                w.keyframe_insert("rotation_euler", frame=f)
    for k in range(12):      # 畑で野菜をついばむ鳥
        o = link_copy(me, (r.uniform(-4, 4), r.uniform(0, 6), 0.3), f"g{k}")
        o.scale = (1.6,) * 3
        o.rotation_euler.z = r.uniform(0, 6.28)
        for f in range(1, nf + 1, 6):
            o.rotation_euler.x = math.radians(25 if (f // 6 + k) % 3 == 0 else 0)
            o.keyframe_insert("rotation_euler", frame=f)
    W.camera((-1.5, -6.0, 1.5), (0.5, 2.0, 2.2), lens=26)
    return nf


# ---------- おじいさんの家（絵本） ----------
def book_texture():
    from PIL import Image, ImageDraw
    p = os.path.join(HERE, "assets", "book.png")
    if os.path.exists(p):
        return p
    os.makedirs(os.path.dirname(p), exist_ok=True)
    w, h = 1024, 640
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):                       # 夕焼けの空
        u = y / h
        d.line((0, y, w, y), fill=(int(250 - 20 * u), int(150 + 40 * u), int(70 + 60 * u)))
    d.ellipse((620, 330, 760, 470), fill=(255, 220, 120))
    d.polygon([(0, 640), (0, 470), (180, 380), (330, 470), (520, 360), (760, 470), (1024, 400), (1024, 640)], fill=(90, 60, 70))
    d.line((512, 0, 512, h), fill=(200, 160, 120), width=6)       # 本のまん中の折り目
    for (cx, cy, s) in ((260, 230, 2.0), (420, 130, 1.3), (780, 170, 1.6)):     # 飛ぶカラス
        d.ellipse((cx - 40 * s, cy - 14 * s, cx + 40 * s, cy + 14 * s), fill=(15, 15, 18))
        d.polygon([(cx - 10 * s, cy), (cx - 60 * s, cy - 50 * s), (cx + 20 * s, cy - 4 * s)], fill=(15, 15, 18))
        d.polygon([(cx + 10 * s, cy), (cx + 70 * s, cy - 45 * s), (cx + 25 * s, cy + 2 * s)], fill=(15, 15, 18))
        d.polygon([(cx + 40 * s, cy - 6 * s), (cx + 62 * s, cy), (cx + 40 * s, cy + 6 * s)], fill=(15, 15, 18))
    im.save(p)
    return p


def img_mat(name, path):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.8
    tx = nt.nodes.new("ShaderNodeTexImage")
    tx.image = bpy.data.images.load(path)
    nt.links.new(tx.outputs["Color"], b.inputs["Base Color"])
    return m


def c10_book(nf):
    w = bpy.data.worlds.new("room")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.9, 0.8, 0.65, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.25
    tat = W.mat("tatami", (0.66, 0.62, 0.40), 0.9)
    edge = W.mat("tatami_edge", (0.12, 0.16, 0.10), 0.8)
    for i in range(-2, 3):
        W.box((i * 1.0, 0.5, 0.0), (0.98, 1.9, 0.06), tat, bevel=0)
        W.box((i * 1.0 + 0.49, 0.5, 0.032), (0.04, 1.9, 0.005), edge, bevel=0)
    shoji = W.mat("shoji", (1.0, 0.97, 0.9), emit=(1.0, 0.93, 0.8), emit_strength=0.7)
    frame = W.mat("shoji_frame", (0.50, 0.36, 0.22), 0.8)
    W.box((0, 2.0, 1.1), (5, 0.04, 2.2), shoji, bevel=0)
    for k in range(-6, 7):
        W.box((k * 0.4, 1.97, 1.1), (0.03, 0.03, 2.2), frame, bevel=0)
    for k in range(6):
        W.box((0, 1.97, 0.2 + k * 0.4), (5, 0.03, 0.03), frame, bevel=0)
    W.box((-2.5, 0.5, 1.2), (0.06, 4, 2.4), W.mat("room_wall", (0.88, 0.82, 0.70), 0.9), bevel=0)
    bpy.ops.object.light_add(type='AREA', location=(0, 1.7, 1.3))
    a = bpy.context.object
    a.data.energy = 120
    a.data.size = 3.0
    a.data.color = (1.0, 0.9, 0.75)
    a.rotation_euler.x = math.radians(-90)
    wood = W.mat("chabudai", (0.40, 0.24, 0.12), 0.5)
    F._cyl(0.5, 0.5, 0.04, (0, 0.4, 0.34), wood, verts=24)
    for sx, sy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
        W.box((sx * 0.3, 0.4 + sy * 0.3, 0.17), (0.05, 0.05, 0.32), wood, bevel=0)
    bk = img_mat("book", book_texture())
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0.0, 0.32, 0.365))
    b = bpy.context.object
    b.scale = (0.48, 0.30, 1)
    b.rotation_euler.z = math.radians(8)
    b.data.materials.append(bk)
    W.box((0.0, 0.32, 0.358), (0.5, 0.32, 0.012), W.mat("book_cover", (0.85, 0.30, 0.20), 0.7), rot=(0, 0, math.radians(8)), bevel=0)
    gp, _ = person((0.55, 0.85, 0.0), 215, seed=4, pose="sit", look=GRANDPA)
    kid, _ = person((-0.45, 0.85, 0.0), 160, seed=1, pose="sit", scale=0.68, look=KID)
    for f, d in ((1, 160), (60, 160), (75, 125), (180, 125)):       # 子がおじいさんの方を見る
        kid.rotation_euler.z = math.radians(-d)
        kid.keyframe_insert("rotation_euler", frame=f)
    W.camera((0.05, -1.05, 1.40), (0.0, 0.55, 0.45), lens=24)
    return nf


# ---------- 書き出し ----------
def render(out, nf, step=1, first=None, last=None):
    os.makedirs(out, exist_ok=True)
    sc = bpy.context.scene
    W.render_setup(os.path.join(out, "f_####.png"), 1, nf, res=RES, samples=8)
    sc.view_settings.look = 'AgX - Base Contrast'
    sc.view_settings.exposure = EXPOSURE + 0.15
    cam = sc.camera
    if not (cam.animation_data and cam.animation_data.action):
        fwd = cam.rotation_euler.to_quaternion() @ Vector((0, 0, -1))
        cam.keyframe_insert("location", frame=1)
        cam.location += fwd * 0.35
        cam.keyframe_insert("location", frame=nf)
    for f in range((first or 1), (last or nf) + 1, step):
        sc.frame_set(f)
        sc.render.filepath = os.path.join(out, f"f_{f:04d}.png")
        if not os.path.exists(sc.render.filepath):
            bpy.ops.render.render(write_still=True)


SCENES = {"c05b_walnut": c05b_walnut, "c06b_kite": c06b_kite, "c10b_shrine": c10b_shrine, "c01_open": c01_open, "c02_wire": c02_wire, "c03_quiet": c03_quiet, "c04_garbage": c04_garbage,
          "c05_orchard": c05_orchard, "c06_road": c06_road, "c07_flies": c07_flies, "c08_rats": c08_rats,
          "c09_birds": c09_birds, "c10_book": c10_book, "c11_bench": c11_bench, "c12_return": c12_return}

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    first = int(sys.argv[4]) if len(sys.argv) > 4 else None
    last = int(sys.argv[5]) if len(sys.argv) > 5 else None
    W.reset()
    nf = TL.shot(name)["frames"]
    SCENES[name](nf)
    render(out, nf, step, first, last)
    print("rendered", name, flush=True)
