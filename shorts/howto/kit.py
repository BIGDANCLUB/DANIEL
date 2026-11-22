"""作り方シリーズの共通部品（Blender / bpy）。参考元（0秒博士）の写実寄りの絵に近づける。
- 関節のある人（Person）：歩く・走る・登る・落ちる・手を振る など
- 空（雲つき）・地面・遠くの田畑と山
- カメラの道すじ（キーを時間でなめらかにつなぐ）
- 図解：伸びていく線、動く点線の矢印、三角（狙える範囲）、火、煙、飛ぶ矢
座標：z=上（m）。人の正面は +y（向き face=0）。時間は「場面の頭からの秒」。"""
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "mach"))
import world as W  # noqa: E402

bpy = W.bpy
import bmesh  # noqa: E402
from mathutils import Vector  # noqa: E402

FPS = 30
RES = (540, 960)
D2R = math.pi / 180


def fr(t):
    """場面の頭からの秒 → コマ番号（1から）。"""
    return int(round(t * FPS)) + 1


def smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


# ---------- 材質 ----------
def mat(name, col, rough=0.8, **kw):
    return W.mat(name, col, rough, **kw)


def noisy(name, col, scale=1.0, var=0.35, bump=0.25, rough=0.85, attr=False, coord="Object", spec=0.3):
    """むらのある材質（石・土・草・しっくい）。attr=True なら頂点の色 "col" を掛ける（石ごとの色の違い）。"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = rough
    try:
        b.inputs["Specular IOR Level"].default_value = spec
    except Exception:
        pass
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = 10.0
    nz.inputs["Roughness"].default_value = 0.62
    nt.links.new(tc.outputs[coord], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.elements[0].position = 0.25
    cr.elements[0].color = (*(c * (1 - var) for c in col), 1)
    cr.elements[1].position = 0.78
    cr.elements[1].color = (*(min(1, c * (1 + var * 0.7)) for c in col), 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs[0])
    out = ramp.outputs[0]
    if attr:
        at = nt.nodes.new("ShaderNodeAttribute")
        at.attribute_name = "col"
        mx = nt.nodes.new("ShaderNodeMix")
        mx.data_type = 'RGBA'
        mx.blend_type = 'MULTIPLY'
        mx.inputs["Factor"].default_value = 1.0
        nt.links.new(out, mx.inputs[6])
        nt.links.new(at.outputs["Color"], mx.inputs[7])
        out = mx.outputs[2]
    nt.links.new(out, b.inputs["Base Color"])
    if bump:
        nz2 = nt.nodes.new("ShaderNodeTexNoise")
        nz2.inputs["Scale"].default_value = scale * 6
        nz2.inputs["Detail"].default_value = 6.0
        nt.links.new(tc.outputs[coord], nz2.inputs["Vector"])
        bp = nt.nodes.new("ShaderNodeBump")
        bp.inputs["Strength"].default_value = bump
        nt.links.new(nz2.outputs["Fac"], bp.inputs["Height"])
        nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def glow(name, col, strength=3.0, alpha=1.0):
    """光る材質（図解の線・矢印・火）。影は落とさない。"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL':
            nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*col, 1)
    em.inputs["Strength"].default_value = strength
    if alpha < 1:
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        mx.inputs[0].default_value = alpha
        nt.links.new(tr.outputs[0], mx.inputs[1])
        nt.links.new(em.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], out.inputs["Surface"])
    else:
        nt.links.new(em.outputs[0], out.inputs["Surface"])
    return m


def fade_mat(m, f_on, f_full, f_off=None, f_gone=None, name=None):
    """光る材質の透明度をコマで変える（線や三角を出したり消したり）。材質を複製して返す。"""
    m2 = m.copy()
    m2.name = name or f"{m.name}_{f_on}"
    nt = m2.node_tree
    mx = next((n for n in nt.nodes if n.type == 'MIX_SHADER'), None)
    if mx is None:
        out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
        em = next(n for n in nt.nodes if n.type == 'EMISSION')
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(tr.outputs[0], mx.inputs[1])
        nt.links.new(em.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], out.inputs["Surface"])
    a1 = mx.inputs[0].default_value if mx.inputs[0].default_value < 1 else 1.0
    seq = [(f_on - 1, 0.0), (f_full, a1)]
    if f_off:
        seq += [(f_off, a1), (f_gone or f_off + 6, 0.0)]
    for f, a in seq:
        mx.inputs[0].default_value = a
        mx.inputs[0].keyframe_insert("default_value", frame=max(0, f))
    return m2


# ---------- 形（共有メッシュ） ----------
_MESH = {}


def capsule_mesh(r1, r2, length, sx=1.0, sy=1.0, cz=1.0, seg=14, rings=4):
    """上端（z=0）が半径 r1、下へ length 伸びて半径 r2 のカプセル。sx/sy で横・前後に押しつぶす。cz は丸い端の高さの倍率。"""
    key = ("cap", r1, r2, length, sx, sy, cz, seg)
    if key in _MESH:
        return _MESH[key]
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings * 2, radius=1.0)
    for v in bm.verts:
        x, y, z = v.co
        if z >= -1e-6:
            v.co = (x * r1 * sx, y * r1 * sy, z * r1 * cz)
        else:
            v.co = (x * r2 * sx, y * r2 * sy, z * r2 * cz - length)
    me = bpy.data.meshes.new(f"cap{len(_MESH)}")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(None)
    _MESH[key] = me
    return me


def ellip_mesh(rx, ry, rz, seg=16, rings=10):
    key = ("ell", rx, ry, rz, seg)
    if key in _MESH:
        return _MESH[key]
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    for v in bm.verts:
        v.co = (v.co.x * rx, v.co.y * ry, v.co.z * rz)
    me = bpy.data.meshes.new(f"ell{len(_MESH)}")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(None)
    _MESH[key] = me
    return me


def cyl_mesh(r1, r2, h, seg=16, smooth_sides=True):
    """下端 z=0 が半径 r1、上端 z=h が半径 r2（円すい台）。"""
    key = ("cyl", r1, r2, h, seg)
    if key in _MESH:
        return _MESH[key]
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r1, radius2=r2, depth=h)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, h / 2))
    me = bpy.data.meshes.new(f"cyl{len(_MESH)}")
    bm.to_mesh(me)
    bm.free()
    if smooth_sides:
        for p in me.polygons:
            p.use_smooth = abs(p.normal.z) < 0.9
    me.materials.append(None)
    _MESH[key] = me
    return me


def box_mesh(sx, sy, sz, bevel=0.0):
    key = ("box", sx, sy, sz, bevel)
    if key in _MESH:
        return _MESH[key]
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = (v.co.x * sx, v.co.y * sy, v.co.z * sz)
    if bevel:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=2, affect='EDGES')
    me = bpy.data.meshes.new(f"box{len(_MESH)}")
    bm.to_mesh(me)
    bm.free()
    me.materials.append(None)
    _MESH[key] = me
    return me


def obj(me, m, parent=None, loc=(0, 0, 0), rot=(0, 0, 0), scale=None, name="o", shadow=True):
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.material_slots[0].link = 'OBJECT'
    o.material_slots[0].material = m
    if parent is not None:
        o.parent = parent
    o.location = loc
    o.rotation_euler = rot
    if scale is not None:
        o.scale = scale if isinstance(scale, (tuple, list)) else (scale, scale, scale)
    if not shadow:
        o.visible_shadow = False
    return o


def empty(loc=(0, 0, 0), parent=None, name="e"):
    o = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(o)
    o.empty_display_size = 0.1
    if parent is not None:
        o.parent = parent
    o.location = loc
    return o


def key_loc(o, f, loc=None):
    if loc is not None:
        o.location = loc
    o.keyframe_insert("location", frame=f)


def key_rot(o, f, rot=None):
    if rot is not None:
        o.rotation_euler = rot
    o.keyframe_insert("rotation_euler", frame=f)


def key_scale(o, f, s=None):
    if s is not None:
        o.scale = s if isinstance(s, (tuple, list)) else (s, s, s)
    o.keyframe_insert("scale", frame=f)


def show(o, f_on, f_off=None, pop=0):
    """f_on コマ目に出す（pop>0 なら pop コマかけて大きくなる）。f_off で消す。"""
    s1 = tuple(o.scale)
    if f_on > 1:
        key_scale(o, max(0, f_on - 1), (1e-4, 1e-4, 1e-4))
    if pop:
        key_scale(o, f_on, tuple(v * 0.05 for v in s1))
        key_scale(o, f_on + pop, tuple(v * 1.12 for v in s1))
        key_scale(o, f_on + pop + 3, s1)
    else:
        key_scale(o, f_on, s1)
    if f_off:
        key_scale(o, f_off - 1, s1)
        key_scale(o, f_off, (1e-4, 1e-4, 1e-4))


# ---------- 人（関節つき） ----------
SKIN = (0.52, 0.30, 0.20)
DENIM = (0.09, 0.17, 0.32)
HERO = dict(top=(0.62, 0.02, 0.015), bottom=DENIM, shorts=True, sleeves="short", hat="straw", shoes=(0.80, 0.80, 0.78),
            print=(0.90, 0.55, 0.04))
ENEMY = dict(top=(0.13, 0.12, 0.12), bottom=(0.17, 0.16, 0.16), sleeves="long", hat="jingasa", shoes=(0.35, 0.28, 0.18),
             armor=(0.08, 0.08, 0.09))
ALLY_R = dict(top=(0.62, 0.08, 0.06), bottom=(0.20, 0.18, 0.17), sleeves="long", hat="jingasa", shoes=(0.35, 0.28, 0.18),
              armor=(0.55, 0.06, 0.05))
ALLY_B = dict(top=(0.10, 0.20, 0.50), bottom=(0.20, 0.18, 0.17), sleeves="long", hat="jingasa", shoes=(0.35, 0.28, 0.18),
              armor=(0.08, 0.16, 0.42))
WORKER = dict(top=(0.95, 0.42, 0.05), bottom=(0.22, 0.22, 0.25), sleeves="long", hat="hachimaki", shoes=(0.25, 0.22, 0.2))


class Person:
    """関節のある人。root（足もと）→ pelvis（腰）→ spine（胴）→ neck（頭）、肩・ひじ、股・ひざ。
    角度は度。腕・脚の x 回転は「前へ振る」がプラス、ひざは「曲げる」がマイナス、胴の x は「前かがみ」がマイナス。"""
    JOINTS = ("pelvis", "spine", "neck", "shL", "shR", "elL", "elR", "hipL", "hipR", "kneeL", "kneeR")

    def __init__(self, loc=(0, 0, 0), face=0.0, look=None, scale=1.0, name="p", seed=0):
        look = dict(look or ENEMY)
        self.look = look
        self.name = name
        r = random.Random(seed)
        self.root = empty(loc, name=f"{name}_root")
        self.root.rotation_euler = (0, 0, face * D2R)
        self.root.scale = (scale, scale, scale)
        sk = look.get("skin", SKIN)
        skin = mat(f"skin_{sk}", sk, 0.55)
        top = noisy(f"top_{look['top']}", look["top"], 18.0, 0.18, 0.08, 0.9)
        bot = noisy(f"bot_{look['bottom']}", look["bottom"], 22.0, 0.25 if look.get("shorts") else 0.15, 0.1, 0.9)
        hair = mat(f"hair_{look.get('hair', (0.03, 0.025, 0.02))}", look.get("hair", (0.03, 0.025, 0.02)), 0.6)
        shoe = mat(f"shoe_{look['shoes']}", look["shoes"], 0.6)
        dark = mat("face_dark", (0.03, 0.02, 0.02), 0.4)
        self.j = {}
        J = self.j
        J["pelvis"] = empty((0, 0, 0.93), self.root, f"{name}_pelvis")
        obj(ellip_mesh(0.16, 0.10, 0.11), bot, J["pelvis"], (0, 0, 0.0), name=f"{name}_hips")
        J["spine"] = empty((0, 0, 0.02), J["pelvis"], f"{name}_spine")
        obj(capsule_mesh(0.17, 0.145, 0.36, sy=0.62, cz=0.45), top, J["spine"], (0, 0, 0.44), name=f"{name}_torso")
        if look.get("print"):
            obj(ellip_mesh(0.075, 0.012, 0.085), mat(f"print_{look['print']}", look["print"], 0.7), J["spine"], (0, 0.097, 0.27),
                name=f"{name}_print")
        if look.get("armor"):   # 胴（よろい）：胸と腹に横板
            am = mat(f"armor_{look['armor']}", look["armor"], 0.45)
            obj(capsule_mesh(0.178, 0.155, 0.22, sy=0.66, cz=0.3), am, J["spine"], (0, 0, 0.36), name=f"{name}_do")
            for k in range(3):
                obj(box_mesh(0.30 - 0.02 * k, 0.03, 0.035), am, J["spine"], (0, 0.085, 0.02 - 0.07 * k), name=f"{name}_kusazuri")
        obj(capsule_mesh(0.05, 0.05, 0.05), skin, J["spine"], (0, 0, 0.53), name=f"{name}_neckm")
        J["neck"] = empty((0, 0, 0.52), J["spine"], f"{name}_neck")
        H = J["neck"]
        obj(ellip_mesh(0.098, 0.108, 0.125), skin, H, (0, 0, 0.14), name=f"{name}_head")
        obj(ellip_mesh(0.104, 0.112, 0.105), hair, H, (0, -0.016, 0.172), name=f"{name}_hair")
        for sx in (-1, 1):
            obj(ellip_mesh(0.013, 0.008, 0.016), dark, H, (sx * 0.036, 0.098, 0.15), name=f"{name}_eye")
            obj(box_mesh(0.035, 0.008, 0.009), hair, H, (sx * 0.037, 0.099, 0.178), rot=(0, sx * 6 * D2R, 0), name=f"{name}_brow")
            obj(ellip_mesh(0.016, 0.022, 0.03), skin, H, (sx * 0.097, 0.0, 0.135), name=f"{name}_ear")
        obj(ellip_mesh(0.016, 0.02, 0.026), skin, H, (0, 0.105, 0.118), name=f"{name}_nose")
        obj(box_mesh(0.03, 0.006, 0.007), mat("mouth", (0.35, 0.10, 0.08), 0.5), H, (0, 0.1, 0.078), name=f"{name}_mouth")
        hat = look.get("hat")
        if hat == "straw":
            st = noisy("straw", (0.86, 0.68, 0.33), 60.0, 0.25, 0.4, 0.9)
            obj(cyl_mesh(0.112, 0.105, 0.095, 20), st, H, (0, -0.005, 0.2), name=f"{name}_crown")
            obj(cyl_mesh(0.24, 0.235, 0.012, 24), st, H, (0, -0.005, 0.205), name=f"{name}_brim")
            obj(cyl_mesh(0.114, 0.114, 0.025, 20), mat("hatband", (0.55, 0.05, 0.04), 0.6), H, (0, -0.005, 0.212), name=f"{name}_band")
        elif hat == "jingasa":
            jm = mat("jingasa", (0.05, 0.045, 0.04), 0.35)
            obj(cyl_mesh(0.26, 0.03, 0.11, 20, False), jm, H, (0, -0.005, 0.2), name=f"{name}_jingasa")
        elif hat == "hachimaki":
            obj(cyl_mesh(0.11, 0.108, 0.03, 18), mat("hachimaki", (0.95, 0.95, 0.92), 0.7), H, (0, -0.01, 0.2), name=f"{name}_hm")
        elif hat == "helmet":
            obj(ellip_mesh(0.13, 0.14, 0.1), mat("helmet_y", (0.95, 0.70, 0.05), 0.3), H, (0, -0.005, 0.2), name=f"{name}_helmet")
        long_sl = look.get("sleeves") == "long"
        for side, sx in (("L", -1), ("R", 1)):
            s = J[f"sh{side}"] = empty((sx * 0.205, 0, 0.42), J["spine"], f"{name}_sh{side}")
            obj(capsule_mesh(0.05, 0.043, 0.25), top if long_sl else skin, s, (0, 0, 0), name=f"{name}_uarm")
            if not long_sl:
                obj(capsule_mesh(0.066, 0.062, 0.1), top, s, (0, 0, 0.0), name=f"{name}_sleeve")
            e = J[f"el{side}"] = empty((0, 0, -0.28), s, f"{name}_el{side}")
            obj(capsule_mesh(0.043, 0.035, 0.21), top if long_sl else skin, e, (0, 0, 0), name=f"{name}_farm")
            obj(ellip_mesh(0.032, 0.026, 0.055), skin, e, (0, 0.005, -0.27), name=f"{name}_hand")
            self.j[f"hand{side}"] = empty((0, 0.01, -0.28), e, f"{name}_hand{side}")
            h = J[f"hip{side}"] = empty((sx * 0.095, 0, -0.05), J["pelvis"], f"{name}_hip{side}")
            sh_ = look.get("shorts")
            obj(capsule_mesh(0.075, 0.06, 0.34), skin if sh_ else bot, h, (0, 0, 0), name=f"{name}_thigh")
            if sh_:
                obj(capsule_mesh(0.088, 0.083, 0.2), bot, h, (0, 0, 0.0), name=f"{name}_short")
            k = J[f"knee{side}"] = empty((0, 0, -0.41), h, f"{name}_knee{side}")
            obj(capsule_mesh(0.056, 0.04, 0.3), skin if sh_ else bot, k, (0, 0, 0), name=f"{name}_shin")
            obj(ellip_mesh(0.052, 0.12, 0.045), shoe, k, (0, 0.045, -0.425), name=f"{name}_shoe")
        self.rest = {"shL": (0, 6, 0), "shR": (0, -6, 0), "elL": (12, 0, 0), "elR": (12, 0, 0)}
        self.pose_now = {}
        for k_ in self.JOINTS:
            self._apply(k_, (0, 0, 0))
        _ = r

    # 角度の指定：数字なら x（前後）だけ、タプルなら (x, 外へ開く, ねじり)
    def _apply(self, k, v):
        if isinstance(v, (int, float)):
            v = (v, 0, 0)
        v = tuple(v) + (0,) * (3 - len(v))
        rx, ry, rz = v
        if k in ("shL", "elL", "hipL", "kneeL"):
            ry = ry
        elif k in ("shR", "elR", "hipR", "kneeR"):
            ry = -ry
            rz = -rz
        b = self.rest.get(k, (0, 0, 0))
        self.j[k].rotation_euler = ((b[0] + rx) * D2R, (b[1] + ry) * D2R, (b[2] + rz) * D2R)
        self.pose_now[k] = v

    def pose(self, f, **kw):
        """f コマ目の姿勢をキーにする。kw にないところは今の姿勢のまま、キーも打つ。"""
        for k in self.JOINTS:
            self._apply(k, kw.get(k, self.pose_now.get(k, (0, 0, 0))))
            self.j[k].keyframe_insert("rotation_euler", frame=f)
        if "hz" in kw:
            self.j["pelvis"].location.z = 0.93 + kw["hz"]
            self.j["pelvis"].keyframe_insert("location", frame=f)

    def place(self, f, loc=None, face=None, tilt=None):
        if loc is not None:
            self.root.location = loc
            self.root.keyframe_insert("location", frame=f)
        if face is not None or tilt is not None:
            rx, ry, rz = self.root.rotation_euler
            if face is not None:
                rz = face * D2R
            if tilt is not None:
                rx, ry = tilt[0] * D2R, tilt[1] * D2R
            self.root.rotation_euler = (rx, ry, rz)
            self.root.keyframe_insert("rotation_euler", frame=f)

    def stand(self, f, **kw):
        base = dict(pelvis=0, spine=0, neck=0, shL=0, shR=0, elL=0, elR=0, hipL=0, hipR=0, kneeL=0, kneeR=0, hz=0)
        base.update(kw)
        self.pose(f, **base)

    # ---- 動き ----
    def walk(self, f0, f1, pts, run=False, step=2, face_path=True, phase=0.0, stride=None, arms=None):
        """pts（地面の点の列）を f0〜f1 コマでたどる。run=True で走る。"""
        pts = [Vector(p) for p in pts]
        seg = [(pts[i + 1] - pts[i]).length for i in range(len(pts) - 1)]
        total = sum(seg) or 1e-6
        stride = stride or (2.2 if run else 1.4)
        A = 38 if run else 24
        for f in list(range(f0, f1 + 1, step)) + [f1]:
            u = (f - f0) / max(1, f1 - f0)
            d = u * total
            i = 0
            while i < len(seg) - 1 and d > seg[i]:
                d -= seg[i]
                i += 1
            p = pts[i] + (pts[i + 1] - pts[i]) * (d / max(1e-6, seg[i]))
            dirv = (pts[i + 1] - pts[i])
            ph = 2 * math.pi * (u * total / stride) + phase
            s, c = math.sin(ph), math.cos(ph)
            kw = dict(hipL=A * s, hipR=-A * s, kneeL=-(8 + (55 if run else 35) * max(0, c)), kneeR=-(8 + (55 if run else 35) * max(0, -c)),
                      spine=-12 if run else -3, neck=6 if run else 2, hz=-0.03 * abs(s) - (0.05 if run else 0))
            if arms is None:
                kw.update(shL=-A * 0.9 * s, shR=A * 0.9 * s, elL=(65 if run else 15), elR=(65 if run else 15))
            else:
                kw.update(arms)
            self.pose(f, **kw)
            face = math.degrees(math.atan2(-dirv.x, dirv.y)) if face_path and dirv.length > 1e-6 else None
            self.place(f, tuple(p), face)

    def climb(self, f0, f1, p0, p1, face, step=2, rate=1.6, tilt=0.0):
        """梯子や石垣を登る（体は face の向き＝壁の方）。tilt は体の傾き（前へ倒れる角度）。"""
        for f in list(range(f0, f1 + 1, step)) + [f1]:
            u = (f - f0) / max(1, f1 - f0)
            ph = 2 * math.pi * rate * (f - f0) / FPS
            s = math.sin(ph)
            self.pose(f, shL=(150 + 22 * s, 10), shR=(150 - 22 * s, 10), elL=25 + 20 * max(0, -s), elR=25 + 20 * max(0, s),
                      hipL=45 + 30 * s, hipR=45 - 30 * s, kneeL=-(60 + 30 * s), kneeR=-(60 - 30 * s), spine=-8, neck=-25, hz=-0.08)
            self.place(f, lerp(p0, p1, u), face, (tilt, 0))

    def fall(self, f0, f1, p0, v0, spin=(360, 0), ground=0.0, step=2, flail=True):
        """放り出されて落ちる。v0＝最初の速さ（m/秒）。spin＝回る角度（前後、左右）。地面に着いたら寝転ぶ。"""
        rx0, ry0, rz = self.root.rotation_euler
        landed = None
        for f in list(range(f0, f1 + 1, step)) + [f1]:
            t = (f - f0) / FPS
            T = (f1 - f0) / FPS
            p = (p0[0] + v0[0] * t, p0[1] + v0[1] * t, p0[2] + v0[2] * t - 4.9 * t * t)
            if p[2] <= ground and t > 0.05:
                if landed is None:
                    landed = (p[0], p[1], ground)
                p = landed
                self.root.rotation_euler = (-90 * D2R, 0, rz)
                self.stand(f, shL=(20, 60), shR=(20, 60), hipL=10, hipR=-5)
            else:
                u = t / max(T, 1e-6)
                self.root.rotation_euler = (rx0 + spin[0] * u * D2R, ry0 + spin[1] * u * D2R, rz)
                if flail:
                    w = math.sin(t * 22)
                    self.pose(f, shL=(160 + 30 * w, 40), shR=(160 - 30 * w, 40), elL=30, elR=30, hipL=30 * w, hipR=-30 * w,
                              kneeL=-40, kneeR=-30, spine=10, neck=15)
            self.root.keyframe_insert("rotation_euler", frame=f)
            self.root.location = p
            self.root.keyframe_insert("location", frame=f)

    def wave(self, f0, f1, side="R", step=2):
        for f in list(range(f0, f1 + 1, step)) + [f1]:
            w = math.sin((f - f0) / FPS * 2 * math.pi * 2.2)
            kw = {f"sh{side}": (165, 25 + 15 * w), f"el{side}": 20 + 15 * w}
            self.pose(f, **kw)

    def hold(self, item, side="R", offset=(0, 0, 0), rot=(0, 0, 0)):
        """道具を手に持たせる（手の空オブジェクトの子にする）。"""
        item.parent = self.j[f"hand{side}"]
        item.location = offset
        item.rotation_euler = tuple(a * D2R for a in rot)
        return item


def crowd(n, center, spread, look, seed=1, face=0.0, scale=1.0, prefix="c"):
    r = random.Random(seed)
    out = []
    for i in range(n):
        p = (center[0] + r.uniform(-spread[0], spread[0]), center[1] + r.uniform(-spread[1], spread[1]), center[2])
        lk = look[i % len(look)] if isinstance(look, list) else look
        out.append(Person(p, face + r.uniform(-15, 15), lk, scale, name=f"{prefix}{i}", seed=seed * 100 + i))
    return out


# ---------- 道具 ----------
def ladder(length=4.5, width=0.5, name="ladder"):
    """梯子（原点は下の端の真ん中、+z へ伸びる）。"""
    wood = noisy("ladder_wood", (0.45, 0.32, 0.18), 8.0, 0.25, 0.2)
    root = empty(name=name)
    for sx in (-1, 1):
        obj(box_mesh(0.06, 0.06, length), wood, root, (sx * width / 2, 0, length / 2), name=f"{name}_rail")
    n = int(length / 0.35)
    for i in range(1, n):
        obj(cyl_mesh(0.022, 0.022, width, 8), wood, root, (-width / 2, 0, i * length / n), rot=(0, 90 * D2R, 0), name=f"{name}_rung")
    return root


def spear(length=2.6):
    root = empty(name="spear")
    obj(cyl_mesh(0.018, 0.018, length, 8), mat("spear_shaft", (0.25, 0.15, 0.08), 0.6), root, (0, 0, -length * 0.35))
    obj(cyl_mesh(0.03, 0.0, 0.22, 6), mat("steel", (0.7, 0.72, 0.75), 0.25), root, (0, 0, length * 0.65))
    return root


def gun():
    """火縄銃（原点は手、+y が銃口の向き）。"""
    root = empty(name="gun")
    wood = mat("gun_wood", (0.30, 0.16, 0.07), 0.5)
    obj(box_mesh(0.05, 0.45, 0.07), wood, root, (0, -0.05, 0))
    obj(cyl_mesh(0.016, 0.014, 0.85, 8), mat("gun_barrel", (0.12, 0.12, 0.13), 0.3), root, (0, 0.1, 0.02), rot=(-90 * D2R, 0, 0))
    return root


def bow():
    root = empty(name="bow")
    m = mat("bow", (0.2, 0.08, 0.05), 0.5)
    for k in range(9):
        a = (k - 4) / 4 * 0.55
        obj(cyl_mesh(0.012, 0.012, 0.28, 6), m, root, (0, 0.18 * math.cos(a) - 0.18, 1.0 * math.sin(a)), rot=(a, 0, 0))
    return root


# ---------- 空・光・地面 ----------
def daylight(elev=48, az=215, strength=3.0, sky_strength=0.2, col=(1.0, 0.91, 0.76), haze=1.0):
    """晴れた昼の光（太陽＋写実的な空の色）。az は太陽のある方角（0＝+y、90＝+x、180＝-y、215＝手前左＝-y と -x の間）。"""
    bpy.ops.object.light_add(type='SUN')
    s = bpy.context.object
    e = elev * D2R
    a = az * D2R
    dvec = Vector((-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e)))   # 光が進む向き
    s.rotation_euler = dvec.to_track_quat('-Z', 'Y').to_euler()
    s.data.energy = strength
    s.data.color = col
    s.data.angle = 2.0 * D2R
    w = bpy.data.worlds.new("sky")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    sky = nt.nodes.new("ShaderNodeTexSky")
    sky.sky_type = 'MULTIPLE_SCATTERING'
    sky.sun_elevation = e
    sky.sun_rotation = math.atan2(math.cos(a), math.sin(a))      # 太陽のある方角（+x から左回り）
    sky.sun_disc = False
    try:
        sky.air_density = 1.0
        sky.aerosol_density = haze
    except Exception:
        pass
    nt.links.new(sky.outputs[0], bg.inputs[0])
    bg.inputs[1].default_value = sky_strength
    return s


def flat_sky(top=(0.18, 0.42, 0.85), horizon=(0.72, 0.84, 0.96), strength=1.0):
    """空の色を上下のグラデーションで決める（写実的な空の代わり／夜や夕方の色を作るとき）。"""
    w = bpy.context.scene.world
    nt = w.node_tree
    bg = nt.nodes["Background"]
    for n in list(nt.nodes):
        if n.type not in ('BACKGROUND', 'OUTPUT_WORLD'):
            nt.nodes.remove(n)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (*horizon, 1)
    ramp.color_ramp.elements[1].position = 0.45
    ramp.color_ramp.elements[1].color = (*top, 1)
    nt.links.new(sep.outputs[2], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], bg.inputs[0])
    bg.inputs[1].default_value = strength


def clouds(seed=1, cover=0.56, height=600.0, radius=6000.0, bright=2.6, col=(1, 1, 1), shade=(0.55, 0.60, 0.70)):
    """白い雲（半球の内側に描く。雲の層を下から見上げたような遠近になるよう、高さで割った座標で模様を作る）。"""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=radius)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -radius * 0.02], context='VERTS')
    me = bpy.data.meshes.new("clouds")
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("clouds", me)
    bpy.context.collection.objects.link(o)
    o.visible_shadow = False
    o.visible_diffuse = False
    o.visible_glossy = False
    m = bpy.data.materials.new(f"clouds{seed}")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL':
            nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs[0])
    zc = nt.nodes.new("ShaderNodeMath")
    zc.operation = 'MAXIMUM'
    zc.inputs[1].default_value = radius * 0.035
    nt.links.new(sep.outputs[2], zc.inputs[0])
    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    for i, ax in enumerate((0, 1)):
        dv = nt.nodes.new("ShaderNodeMath")
        dv.operation = 'DIVIDE'
        nt.links.new(sep.outputs[ax], dv.inputs[0])
        nt.links.new(zc.outputs[0], dv.inputs[1])
        mu = nt.nodes.new("ShaderNodeMath")
        mu.operation = 'MULTIPLY'
        mu.inputs[1].default_value = height / 1000.0
        nt.links.new(dv.outputs[0], mu.inputs[0])
        nt.links.new(mu.outputs[0], comb.inputs[i])
    comb.inputs[2].default_value = seed * 3.7
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.noise_dimensions = '3D'
    nz.inputs["Scale"].default_value = 0.9
    nz.inputs["Detail"].default_value = 5.0
    nz.inputs["Roughness"].default_value = 0.5
    nt.links.new(comb.outputs[0], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = cover
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = cover + 0.12
    ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs[0])
    # 地平線の近くはうすく
    hz = nt.nodes.new("ShaderNodeMapRange")
    hz.inputs[1].default_value = radius * 0.02
    hz.inputs[2].default_value = radius * 0.16
    nt.links.new(sep.outputs[2], hz.inputs[0])
    al = nt.nodes.new("ShaderNodeMath")
    al.operation = 'MULTIPLY'
    nt.links.new(ramp.outputs[0], al.inputs[0])
    nt.links.new(hz.outputs[0], al.inputs[1])
    # 雲の濃いところは少し灰色（立体感）
    nz2 = nt.nodes.new("ShaderNodeTexNoise")
    nz2.inputs["Scale"].default_value = 2.6
    nz2.inputs["Detail"].default_value = 6.0
    nt.links.new(comb.outputs[0], nz2.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = 0.35
    cr.color_ramp.elements[0].color = (*shade, 1)
    cr.color_ramp.elements[1].position = 0.7
    cr.color_ramp.elements[1].color = (*col, 1)
    nt.links.new(nz2.outputs["Fac"], cr.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = bright
    nt.links.new(cr.outputs[0], em.inputs["Color"])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(al.outputs[0], mx.inputs[0])
    nt.links.new(tr.outputs[0], mx.inputs[1])
    nt.links.new(em.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs["Surface"])
    me.materials.append(m)
    return o


def grass_mat(name="grass2"):
    """芝・草地：大きなまだら（濃い緑〜黄緑）＋草の株のむら＋細かい草のざらつき（参考元の写真のような芝に近づける）。"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.92
    try:
        b.inputs["Specular IOR Level"].default_value = 0.2
    except Exception:
        pass
    tc = nt.nodes.new("ShaderNodeTexCoord")

    def nz(scale, detail, rough=0.6):
        n = nt.nodes.new("ShaderNodeTexNoise")
        n.inputs["Scale"].default_value = scale
        n.inputs["Detail"].default_value = detail
        n.inputs["Roughness"].default_value = rough
        nt.links.new(tc.outputs["Object"], n.inputs["Vector"])
        return n
    big, mid, fine = nz(0.025, 4), nz(0.6, 6), nz(45.0, 2, 0.5)
    r1 = nt.nodes.new("ShaderNodeValToRGB")
    r1.color_ramp.elements[0].position = 0.35
    r1.color_ramp.elements[0].color = (0.085, 0.17, 0.045, 1)
    r1.color_ramp.elements[1].position = 0.68
    r1.color_ramp.elements[1].color = (0.25, 0.33, 0.10, 1)
    nt.links.new(big.outputs["Fac"], r1.inputs[0])
    r2 = nt.nodes.new("ShaderNodeValToRGB")
    r2.color_ramp.elements[0].position = 0.3
    r2.color_ramp.elements[0].color = (0.62, 0.62, 0.62, 1)
    r2.color_ramp.elements[1].position = 0.75
    r2.color_ramp.elements[1].color = (1.15, 1.12, 1.0, 1)
    nt.links.new(mid.outputs["Fac"], r2.inputs[0])
    m1 = nt.nodes.new("ShaderNodeMix")
    m1.data_type = 'RGBA'
    m1.blend_type = 'MULTIPLY'
    m1.inputs["Factor"].default_value = 1.0
    nt.links.new(r1.outputs[0], m1.inputs[6])
    nt.links.new(r2.outputs[0], m1.inputs[7])
    r3 = nt.nodes.new("ShaderNodeValToRGB")
    r3.color_ramp.elements[0].position = 0.35
    r3.color_ramp.elements[0].color = (0.7, 0.72, 0.6, 1)
    r3.color_ramp.elements[1].position = 0.65
    r3.color_ramp.elements[1].color = (1.2, 1.2, 1.05, 1)
    nt.links.new(fine.outputs["Fac"], r3.inputs[0])
    m2 = nt.nodes.new("ShaderNodeMix")
    m2.data_type = 'RGBA'
    m2.blend_type = 'MULTIPLY'
    m2.inputs["Factor"].default_value = 1.0
    nt.links.new(m1.outputs[2], m2.inputs[6])
    nt.links.new(r3.outputs[0], m2.inputs[7])
    nt.links.new(m2.outputs[2], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = 0.7
    bp.inputs["Distance"].default_value = 0.05
    nt.links.new(fine.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def ground(size=8000, col=(0.22, 0.34, 0.11), name="grass"):
    m = grass_mat()
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    g = bpy.context.object
    g.data.materials.append(m)
    return g


def countryside(seed=3, keep_out=60.0, r_max=900.0, n_fields=160, n_trees=220, center=(0, 0)):
    """遠くの田畑（色ちがいの四角）と木のかたまり、さらに遠くの山なみ。中心から keep_out m までは何も置かない。"""
    r = random.Random(seed)
    cols = [(0.20, 0.30, 0.08), (0.30, 0.34, 0.11), (0.17, 0.26, 0.07), (0.36, 0.32, 0.15), (0.24, 0.31, 0.12)]
    fm = [noisy(f"field{i}", c, 0.25, 0.25, 0.1, 0.95) for i, c in enumerate(cols)]
    for i in range(n_fields):
        a = r.uniform(0, 2 * math.pi)
        d = r.uniform(keep_out + 20, r_max)
        x, y = center[0] + d * math.cos(a), center[1] + d * math.sin(a)
        w, h = r.uniform(20, 60), r.uniform(15, 45)
        me = bpy.data.meshes.new("field")
        me.from_pydata([(-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0)], [], [(0, 1, 2, 3)])
        me.materials.append(None)
        obj(me, fm[i % len(fm)], None, (x, y, 0.03 + 0.002 * i), rot=(0, 0, r.choice((0, 0.05, -0.04))), name="field")
    tm = [noisy(f"tree{i}", c, 0.6, 0.3, 0.3, 0.9) for i, c in enumerate([(0.10, 0.20, 0.06), (0.14, 0.25, 0.08), (0.08, 0.16, 0.06)])]
    for i in range(n_trees):
        a = r.uniform(0, 2 * math.pi)
        d = r.uniform(keep_out + 10, r_max)
        x, y = center[0] + d * math.cos(a), center[1] + d * math.sin(a)
        for k in range(r.randint(1, 4)):
            s = r.uniform(3, 7)
            obj(ellip_mesh(s, s, s * 1.1, 10, 6), tm[(i + k) % 3], None, (x + r.uniform(-6, 6), y + r.uniform(-6, 6), s * 0.8), name="tree")
    hm = noisy("hills", (0.16, 0.26, 0.14), 0.01, 0.25, 0.0, 0.95)
    for i in range(26):
        a = i / 26 * 2 * math.pi + r.uniform(-0.1, 0.1)
        d = r.uniform(2600, 3600)
        s = r.uniform(500, 900)
        obj(ellip_mesh(s, s * 0.8, r.uniform(160, 330), 16, 8), hm, None, (center[0] + d * math.cos(a), center[1] + d * math.sin(a), -20),
            rot=(0, 0, a), name="hill")


# ---------- カメラ ----------
def _herm(keys, t, idx):
    """キー（時間, 値のタプル）をなめらかにつなぐ（中のキーは通りぬけ、最初と最後はゆっくり）。"""
    n = len(keys)
    if t <= keys[0][0]:
        return Vector(keys[0][idx])
    if t >= keys[-1][0]:
        return Vector(keys[-1][idx])
    i = max(k for k in range(n - 1) if keys[k][0] <= t)
    t0, t1 = keys[i][0], keys[i + 1][0]
    u = (t - t0) / (t1 - t0)
    p0, p1 = Vector(keys[i][idx]), Vector(keys[i + 1][idx])

    def tan(k):
        if k == 0 or k == n - 1:
            return Vector((0, 0, 0))
        return (Vector(keys[k + 1][idx]) - Vector(keys[k - 1][idx])) / (keys[k + 1][0] - keys[k - 1][0]) * (t1 - t0)
    m0, m1 = tan(i), tan(i + 1)
    h00 = 2 * u ** 3 - 3 * u ** 2 + 1
    h10 = u ** 3 - 2 * u ** 2 + u
    h01 = -2 * u ** 3 + 3 * u ** 2
    h11 = u ** 3 - u ** 2
    return p0 * h00 + m0 * h10 + p1 * h01 + m1 * h11


def campath(keys, nf, shake=0.0, seed=1, name="cam", dof=None, cuts=None):
    """keys = [(秒, 位置, ねらう点, レンズmm), ...]。cuts＝その秒で前のキーとつながず切りかえる（カット）。
    shake＝手持ちのような小さなゆれ（m）。dof＝(ピントの点, F値)。"""
    cam_data = bpy.data.cameras.new(name)
    cam_data.clip_end = 20000
    cam_data.clip_start = 0.05
    c = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(c)
    bpy.context.scene.camera = c
    cuts = sorted(cuts or [])
    groups, cur = [], []
    for k in keys:
        if cuts and cur and any(cur[-1][0] < ct <= k[0] for ct in cuts):
            groups.append(cur)
            cur = []
        cur.append(k)
    groups.append(cur)
    rr = random.Random(seed)
    ph = [rr.uniform(0, 6.28) for _ in range(6)]
    for f in range(1, nf + 1):
        t = (f - 1) / FPS
        g = groups[0]
        for gg in groups:
            if gg[0][0] <= t + 1e-6:
                g = gg
        lk = [(k[0], k[1], k[2], (k[3], 0, 0)) for k in g]
        loc = _herm(lk, t, 1)
        at = _herm(lk, t, 2)
        lens = _herm(lk, t, 3)[0]
        if shake:
            loc = loc + Vector((math.sin(t * 2.1 + ph[0]) + 0.5 * math.sin(t * 5.3 + ph[1]),
                                math.sin(t * 1.7 + ph[2]) * 0.6, math.sin(t * 2.6 + ph[3]) + 0.4 * math.sin(t * 6.1 + ph[4]))) * shake
        c.location = loc
        W.aim(c, at)
        c.data.lens = lens
        c.keyframe_insert("location", frame=f)
        c.keyframe_insert("rotation_euler", frame=f)
        c.data.keyframe_insert("lens", frame=f)
        if dof:
            c.data.dof.use_dof = True
            c.data.dof.aperture_fstop = dof[1]
            fp = Vector(dof[0](t)) if callable(dof[0]) else Vector(dof[0])
            c.data.dof.focus_distance = (fp - loc).length
            c.data.dof.keyframe_insert("focus_distance", frame=f)
    _fix_euler(c)
    return c


def _fix_euler(o):
    """回転のキーが ±180 度でとばないように、となりのキーと近い角度へそろえる。"""
    ad = o.animation_data
    if not ad or not ad.action:
        return
    fcs = []
    act = ad.action
    if hasattr(act, "fcurves") and len(getattr(act, "fcurves", [])):
        fcs = list(act.fcurves)
    else:
        for layer in getattr(act, "layers", []):
            for strip in layer.strips:
                for cb in strip.channelbags:
                    fcs += list(cb.fcurves)
    for fc in fcs:
        if fc.data_path != "rotation_euler":
            continue
        prev = None
        for kp in fc.keyframe_points:
            v = kp.co[1]
            if prev is not None:
                while v - prev > math.pi:
                    v -= 2 * math.pi
                while v - prev < -math.pi:
                    v += 2 * math.pi
            kp.co[1] = v
            kp.handle_left[1] = v
            kp.handle_right[1] = v
            kp.interpolation = 'LINEAR'
            prev = v


# ---------- 図解 ----------
def poly_curve(pts, width, m, name="line", cyclic=False):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = width
    cu.bevel_resolution = 2
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts):
        p.co = (*q, 1)
    sp.use_cyclic_u = cyclic
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    o.visible_shadow = False
    return o


def grow_line(o, f0, f1, f_off=None):
    """線を f0〜f1 で先へ伸ばす。f_off で消す。"""
    cu = o.data
    cu.bevel_factor_end = 0.0
    cu.keyframe_insert("bevel_factor_end", frame=max(0, f0 - 1))
    cu.bevel_factor_end = 0.0
    cu.keyframe_insert("bevel_factor_end", frame=f0)
    cu.bevel_factor_end = 1.0
    cu.keyframe_insert("bevel_factor_end", frame=f1)
    if f_off:
        cu.keyframe_insert("bevel_factor_end", frame=f_off - 1)
        cu.bevel_factor_start = 0.0
        cu.keyframe_insert("bevel_factor_start", frame=f_off - 1)
        cu.bevel_factor_start = 1.0
        cu.keyframe_insert("bevel_factor_start", frame=f_off)
    return o


def arrow_head(m, size=1.0, name="ah"):
    """平たい三角の矢じり（+y が先、xy 平面）。"""
    me = bpy.data.meshes.new(name)
    me.from_pydata([(-0.6 * size, 0, 0), (0.6 * size, 0, 0), (0, 1.1 * size, 0)], [], [(0, 1, 2)])
    me.materials.append(m)
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.visible_shadow = False
    return o


def path_point(pts, d):
    pts = [Vector(p) for p in pts]
    for i in range(len(pts) - 1):
        L = (pts[i + 1] - pts[i]).length
        if d <= L or i == len(pts) - 2:
            u = min(1.0, d / max(L, 1e-6))
            return pts[i] + (pts[i + 1] - pts[i]) * u, (pts[i + 1] - pts[i]).normalized()
        d -= L
    return pts[-1], (pts[-1] - pts[-2]).normalized()


def path_len(pts):
    return sum((Vector(pts[i + 1]) - Vector(pts[i])).length for i in range(len(pts) - 1))


def flow_arrow(pts, m, f0, f1, width=0.25, dash=1.2, gap=0.8, speed=4.0, head=1.0, f_grow=12, up=(0, 0, 1), name="flow"):
    """動く点線の矢印（参考元の青い点線・オレンジの矢印）。pts の上を、f0 で伸び始め f1 で消える。"""
    L = path_len(pts)
    n = int(L / (dash + gap)) + 1
    objs = []
    upv = Vector(up)
    for i in range(n):
        me = box_mesh(width, dash, width * 0.35)
        o = obj(me, m, None, (0, 0, -999), name=f"{name}_d{i}", shadow=False)
        objs.append(o)
        for f in range(max(1, f0 - 1), f1 + 2, 2):
            t = (f - f0) / FPS
            d = (i * (dash + gap) + speed * t) % (n * (dash + gap))
            vis_len = L * min(1.0, max(0.0, (f - f0) / max(1, f_grow)))
            visible = f0 <= f <= f1 and d <= vis_len and d <= L - head * 0.6
            p, dv = path_point(pts, d)
            o.location = p if visible else (0, 0, -999)
            yaw = dv.to_track_quat('Y', 'Z')
            o.rotation_euler = yaw.to_euler()
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("rotation_euler", frame=f)
    h = arrow_head(m, head, f"{name}_head")
    p, dv = path_point(pts, L - head)
    h.location = p
    h.rotation_euler = dv.to_track_quat('Y', 'Z').to_euler()
    show(h, f0 + f_grow, f1 + 1)
    _ = upv
    return objs + [h]


def fan(apex, direction, half_angle, length, m, name="fan", width_at_apex=0.0, up=(0, 0, 1)):
    """平たい三角（狙える範囲）。apex から direction へ、開き角 ±half_angle 度。"""
    d = Vector(direction).normalized()
    upv = Vector(up)
    side = d.cross(upv).normalized()
    a = Vector(apex)
    tanh = math.tan(half_angle * D2R)
    verts = [a + side * width_at_apex / 2, a - side * width_at_apex / 2,
             a + d * length - side * (width_at_apex / 2 + tanh * length), a + d * length + side * (width_at_apex / 2 + tanh * length)]
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [(0, 1, 2, 3)])
    me.materials.append(m)
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.visible_shadow = False
    return o


def flame(loc, size=1.0, seed=1, f0=1, f1=None, parent=None, name="flame"):
    """ゆらめく炎（光る玉を縦にのばして重ねる）。f0 で燃え始め、f1 で消える。"""
    r = random.Random(seed)
    root = empty(loc, parent, name)
    mats = [glow("flame_core", (1.0, 0.72, 0.18), 7.0), glow("flame_mid", (1.0, 0.36, 0.03), 5.0), glow("flame_out", (0.85, 0.12, 0.01), 3.0, 0.75)]
    parts = []
    for k in range(8):
        m = mats[0] if k < 2 else (mats[1] if k < 5 else mats[2])
        s = size * (0.18 if k < 2 else 0.26 if k < 5 else 0.3)
        o = obj(ellip_mesh(s, s, s * 3.6, 10, 8), m, root, (r.uniform(-0.35, 0.35) * size, r.uniform(-0.15, 0.15) * size, s * 3.0),
                name=f"{name}_{k}", shadow=False)
        o.rotation_euler = (r.uniform(-0.25, 0.25), r.uniform(-0.25, 0.25), 0)
        parts.append(o)
    f1 = f1 or 99999
    for o in parts:
        ph = r.uniform(0, 6)
        sc0 = tuple(o.scale)
        key_scale(o, max(0, f0 - 1), 1e-4)
        for f in range(f0, min(f1, f0 + 900), 3):
            w = 0.75 + 0.35 * math.sin((f - f0) * 0.55 + ph) + 0.15 * math.sin((f - f0) * 1.7 + ph * 2)
            g = min(1.0, (f - f0 + 1) / 8)
            key_scale(o, f, (sc0[0] * g * (0.9 + 0.2 * w), sc0[1] * g * (0.9 + 0.2 * w), sc0[2] * g * w))
        if f1 < 99999:
            key_scale(o, f1, 1e-4)
    light = bpy.data.lights.new(f"{name}_l", 'POINT')
    light.energy = 400 * size * size
    light.color = (1.0, 0.5, 0.15)
    lo = bpy.data.objects.new(f"{name}_light", light)
    bpy.context.collection.objects.link(lo)
    lo.parent = root
    lo.location = (0, 0, size)
    light.keyframe_insert("energy", frame=max(0, f0 - 1)) if f0 > 1 else None
    if f0 > 1:
        light.energy = 0
        light.keyframe_insert("energy", frame=f0 - 1)
        light.energy = 400 * size * size
        light.keyframe_insert("energy", frame=f0 + 6)
    if f1 < 99999:
        light.keyframe_insert("energy", frame=f1 - 1)
        light.energy = 0
        light.keyframe_insert("energy", frame=f1)
    return root


def smoke_puffs(loc, f0, n=6, seed=1, col=(0.45, 0.43, 0.42), size=0.8, rise=1.5, life=40, spread=0.6, alpha=0.6, name="smoke"):
    """もくもくと上がって消えるけむり。"""
    r = random.Random(seed)
    m = smoke_mat(f"{name}_m{seed}", col, alpha)
    for i in range(n):
        s = size * r.uniform(0.6, 1.2)
        o = obj(ellip_mesh(1, 1, 1, 12, 8), m, None, loc, name=f"{name}{i}", shadow=False)
        fs = f0 + int(i * life / n / 2)
        p0 = Vector(loc) + Vector((r.uniform(-spread, spread), r.uniform(-spread, spread), 0))
        p1 = p0 + Vector((r.uniform(-1, 1), r.uniform(-1, 1), rise * r.uniform(0.7, 1.3)))
        key_scale(o, max(0, fs - 1), 1e-4)
        key_loc(o, fs, tuple(p0))
        key_scale(o, fs, s * 0.4)
        key_loc(o, fs + life, tuple(p1))
        key_scale(o, fs + life, s * 1.6)
        key_scale(o, fs + life + 1, 1e-4)


def smoke_mat(name, col, alpha):
    """けむり・土けむり：ふちが透けて、まだらに抜ける（ボールに見えないように）。"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = 1.0
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.5
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation = 'SUBTRACT'
    inv.inputs[0].default_value = 1.0
    nt.links.new(lw.outputs["Facing"], inv.inputs[1])
    pw = nt.nodes.new("ShaderNodeMath")
    pw.operation = 'POWER'
    pw.inputs[1].default_value = 2.5
    nt.links.new(inv.outputs[0], pw.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 2.5
    nz.inputs["Detail"].default_value = 4.0
    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.inputs[1].default_value = 0.35
    ramp.inputs[2].default_value = 0.65
    nt.links.new(nz.outputs["Fac"], ramp.inputs[0])
    mu = nt.nodes.new("ShaderNodeMath")
    mu.operation = 'MULTIPLY'
    nt.links.new(pw.outputs[0], mu.inputs[0])
    nt.links.new(ramp.outputs[0], mu.inputs[1])
    mu2 = nt.nodes.new("ShaderNodeMath")
    mu2.operation = 'MULTIPLY'
    mu2.inputs[1].default_value = alpha
    nt.links.new(mu.outputs[0], mu2.inputs[0])
    nt.links.new(mu2.outputs[0], b.inputs["Alpha"])
    return m


def projectile(o, f0, f1, p0, p1, arc=3.0, align=True, step=1):
    """o を p0 から p1 へ放物線で飛ばす（arc＝真ん中の高さの上乗せ）。align で進む向きへ向ける（+y が前）。"""
    p0, p1 = Vector(p0), Vector(p1)
    prev = None
    for f in list(range(f0, f1 + 1, step)) + [f1]:
        u = (f - f0) / max(1, f1 - f0)
        p = p0 + (p1 - p0) * u + Vector((0, 0, 4 * arc * u * (1 - u)))
        o.location = p
        o.keyframe_insert("location", frame=f)
        if align:
            u2 = min(1.0, u + 0.02)
            q = p0 + (p1 - p0) * u2 + Vector((0, 0, 4 * arc * u2 * (1 - u2)))
            dv = (q - p) if (q - p).length > 1e-6 else (p - prev if prev is not None else p1 - p0)
            o.rotation_euler = dv.to_track_quat('Y', 'Z').to_euler()
            o.keyframe_insert("rotation_euler", frame=f)
        prev = p
    return o


def arrow_obj(fire=False, name="arrow"):
    root = empty(name=name)
    obj(cyl_mesh(0.012, 0.012, 0.9, 6), mat("arrow_shaft", (0.55, 0.45, 0.3), 0.6), root, (0, -0.45, 0), rot=(-90 * D2R, 0, 0))
    obj(cyl_mesh(0.025, 0.0, 0.08, 6), mat("steel", (0.7, 0.72, 0.75), 0.25), root, (0, 0.45, 0), rot=(-90 * D2R, 0, 0))
    for k in range(2):
        obj(box_mesh(0.005 if k else 0.08, 0.16, 0.08 if k else 0.005), mat("fletch", (0.9, 0.9, 0.88), 0.8), root, (0, -0.4, 0))
    if fire:
        obj(ellip_mesh(0.07, 0.16, 0.07, 10, 6), glow("fire_mid", (1.0, 0.45, 0.08), 12.0), root, (0, 0.33, 0), shadow=False)
        obj(ellip_mesh(0.04, 0.1, 0.04, 8, 6), glow("fire_core", (1.0, 0.85, 0.35), 18.0), root, (0, 0.35, 0), shadow=False)
    return root


def marker(name, loc, parent=None):
    """画面上の位置を compose へ渡す目印（白い輪や数字を重ねる場所）。"""
    return empty(loc, parent, f"mk_{name}")


# ---------- 書き出し ----------
def render(out, nf, step=2, first=None, last=None, samples=10, exposure=-0.8, look="AgX - Punchy"):
    from bpy_extras.object_utils import world_to_camera_view
    os.makedirs(out, exist_ok=True)
    sc = bpy.context.scene
    W.render_setup(os.path.join(out, "f_####.png"), 1, nf, res=RES, samples=samples)
    try:
        sc.view_settings.look = look
    except Exception:
        sc.view_settings.look = 'AgX - Punchy'
    sc.view_settings.exposure = exposure
    sc.cycles.max_bounces = 6
    sc.cycles.transparent_max_bounces = 16
    mks = [o for o in bpy.data.objects if o.name.startswith("mk_")]
    info = {}
    p = os.path.join(out, "markers.json")
    if os.path.exists(p):
        info = json.load(open(p))
    first, last = first or 1, last or nf
    frames = list(range(first, last + 1, step))
    if frames[-1] != last and last == nf:
        frames.append(last)
    for f in frames:
        sc.frame_set(f)
        d = {}
        for o in mks:
            v = world_to_camera_view(sc, sc.camera, o.matrix_world.translation)
            d[o.name[3:]] = [round(v.x * RES[0], 1), round((1 - v.y) * RES[1], 1), round(v.z, 2)]
        info[str(f)] = d
        sc.render.filepath = os.path.join(out, f"f_{f:04d}.png")
        if not os.path.exists(sc.render.filepath):
            bpy.ops.render.render(write_still=True)
    json.dump(info, open(p, "w"))
