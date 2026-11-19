"""「もしも日本から富士山が消えたら？」全場面の3D（Blender / bpy）。カラス版（../crow/film.py）の部品を使う。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]
座標: z=上（m）。富士山はおおむね +y の遠く。"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timeline as TL  # noqa: E402  （カラス版より先に読み込む＝こちらの時間割を使わせる）
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("crow_film", os.path.join(HERE, "..", "crow", "film.py"))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)
W, F, bpy = C.W, C.F, C.bpy
from mathutils import Vector  # noqa: E402

FPS = TL.FPS
FONT = os.path.join(HERE, "..", "fonts", "NotoSansJP[wght].ttf")
ASSETS = os.path.join(HERE, "assets")
GRANDPA = C.GRANDPA
KID = C.KID
MOM = {"top": (0.85, 0.50, 0.55), "bottom": (0.30, 0.32, 0.40), "hair": (0.10, 0.07, 0.05)}
WORKER = {"top": (0.40, 0.48, 0.55), "bottom": (0.30, 0.34, 0.40)}
TROUT = {"top": (0.25, 0.35, 0.30), "bottom": (0.20, 0.22, 0.25)}
fr = C.frame_of

# ---------- カメラ：カット割りと、全カットでゆっくり動くカメラ（参考元に合わせる） ----------
_camera0 = W.camera


def _camera(loc, look_at, lens=28):
    c = _camera0(loc, look_at, lens)
    c["at"] = tuple(look_at)
    c["f0"] = 1
    return c


W.camera = _camera


def cut(f0, loc, at, lens=28, orbit=None, push=None, piv=None, focus=None, fixat=None, zoom=None):
    """f0 コマ目から別のカメラに切りかえる。focus：ピントを合わせる点（"far"＝遠く）。fixat：ねらう点を動かさない。"""
    keep = bpy.context.scene.camera
    c = W.camera(loc, at, lens)
    c["f0"] = f0
    for k, v in (("orbit", orbit), ("push", push), ("piv", piv), ("focus", focus), ("fixat", fixat), ("zoom", zoom)):
        if v is not None:
            c[k] = v
    if keep:
        bpy.context.scene.camera = keep
    return c


def cams():
    return sorted([o for o in bpy.data.objects if o.type == 'CAMERA' and "at" in o], key=lambda o: o["f0"])


BLUR = 0.012        # 遠くの背景のボケの大きさ（画面の横幅に対する割合）
FAR = 25.0          # ねらう点がこれより遠いときは、遠くにピントを合わせる


def setup_dof(c):
    """ボケ（被写界深度）。近くをねらうカメラは背景がボケ、遠くをねらうカメラは手前が少しボケる。"""
    fo = c.get("focus")
    if isinstance(fo, str) and fo == "none":
        return None
    dof = c.data.dof
    dof.use_dof = True
    if isinstance(fo, str) or (fo is None and (Vector(c["at"]) - Vector(c.location)).length > FAR):
        dof.focus_distance = 10000.0
        dof.aperture_fstop = 4.0 if c.data.lens < 45 else 2.8
        return None
    target = Vector(fo) if fo is not None else None
    s = ((target or Vector(c["at"])) - Vector(c.location)).length
    f = c.data.lens / 1000.0
    width = 0.036 * C.RES[0] / C.RES[1]
    dof.aperture_fstop = min(16.0, max(0.5, f * f / (BLUR * width * max(0.05, s - f))))
    dof.focus_distance = s
    return target


def move_cams(nf):
    """各カメラを、ねらう点のまわりに回りこみながら寄せる（ゆっくり加速・減速）。ピントも追いかける。"""
    cs = cams()
    for i, c in enumerate(cs):
        target = setup_dof(c)
        if c.get("keep"):
            continue
        f0 = c["f0"]
        f1 = cs[i + 1]["f0"] - 1 if i + 1 < len(cs) else nf
        if c.animation_data:
            c.animation_data_clear()
        p0, at = Vector(c.location), Vector(c["at"])
        d = at - p0
        dist = d.length
        fwd = d.normalized()
        piv = p0 + fwd * min(dist, c.get("piv", 10.0))
        orbit = math.radians(c.get("orbit", 13.0)) * (1 if i % 2 == 0 else -1)
        push = min(c.get("push", 0.3) * (piv - p0).length, 2.5)
        track = c.data.dof.use_dof and c.data.dof.focus_distance < 9999
        lens0, zoom = c.data.lens, c.get("zoom", 1.0)
        for f in list(range(f0, f1 + 1, 2)) + [f1]:
            t = (f - f0) / max(1, f1 - f0)
            u = t * t * (3 - 2 * t)
            a = orbit * (u - 0.5)
            ca, sa = math.cos(a), math.sin(a)

            def rot(v):
                w = v - piv
                return piv + Vector((w.x * ca - w.y * sa, w.x * sa + w.y * ca, w.z))
            c.location = rot(p0) + fwd * push * u
            W.aim(c, at if c.get("fixat") else rot(at))
            c.keyframe_insert("location", frame=f)
            c.keyframe_insert("rotation_euler", frame=f)
            if zoom != 1.0:
                c.data.lens = lens0 * (1 + (zoom - 1) * u)
                c.data.keyframe_insert("lens", frame=f)
            if track:
                ft = target if target is not None else (at if c.get("fixat") else rot(at))
                c.data.dof.focus_distance = (ft - c.location).length
                c.data.dof.keyframe_insert("focus_distance", frame=f)


def set_interp(o, kind):
    """キーフレームの補間をまとめて変える（Blender 4.4 以降の新しいアクション形式にも対応）。"""
    ad = o.animation_data
    if not ad or not ad.action:
        return
    act = ad.action
    fcs = []
    if hasattr(act, "fcurves") and len(getattr(act, "fcurves", [])):
        fcs = list(act.fcurves)
    else:
        for layer in getattr(act, "layers", []):
            for strip in layer.strips:
                for cb in strip.channelbags:
                    fcs += list(cb.fcurves)
    for fc in fcs:
        for kp in fc.keyframe_points:
            kp.interpolation = kind


# ---------- 人（腕のポーズつき。顔は今の丸い頭のまま） ----------
_PM = {}


def limb(p0, p1, t, m):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    rot = d.to_track_quat('Z', 'Y').to_euler()
    return W.box(tuple((p0 + p1) / 2), (t, t * 1.08, d.length), m, rot=tuple(rot), bevel=0.012)


def person_mesh(variant, pose="stand", arms="down", look=None):
    look = look or {}
    key = (variant, pose, arms, tuple(sorted(look.items())))
    if key in _PM:
        return _PM[key]
    skin = W.mat(f"skin{variant % 3}", F.SKIN[variant % 3], 0.8)
    tc = look.get("top", F.CLOTH[variant % 6])
    top = W.mat(f"top_{tc}", tc, 0.9)
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
            p.append(W.box((sx * 0.1, 0.2, hip), (0.15, 0.46, 0.16), bottom, bevel=bv))
            p.append(W.box((sx * 0.1, 0.42, hip - 0.24), (0.13, 0.14, 0.44), bottom, bevel=bv))
            p.append(W.box((sx * 0.1, 0.47, hip - 0.47), (0.13, 0.24, 0.07), shoe, bevel=bv))
    else:
        hip = 0.86
        for sx in (-1, 1):
            p.append(W.box((sx * 0.095, 0, 0.47), (0.15, 0.16, 0.8), bottom, bevel=bv))
            p.append(W.box((sx * 0.095, 0.04, 0.035), (0.14, 0.26, 0.07), shoe, bevel=bv))
    p.append(W.box((0, 0, hip + 0.06), (0.36, 0.2, 0.16), bottom, bevel=bv))
    p.append(W.box((0, 0, hip + 0.36), (0.42, 0.23, 0.5), top, bevel=bv))
    sh = hip + 0.54
    hc = sh + 0.22
    for sx in (-1, 1):
        s0 = (sx * 0.265, 0, sh - 0.03)
        a = arms if isinstance(arms, str) else arms[0 if sx < 0 else 1]
        if a == "pray":
            e = (sx * 0.16, 0.2, sh - 0.3)
            h = (sx * 0.035, 0.27, sh - 0.12)
        elif a == "up":
            e = (sx * 0.38, 0.02, sh + 0.22)
            h = (sx * 0.44, 0.04, sh + 0.5)
        elif a == "head":
            e = (sx * 0.36, 0.1, sh + 0.12)
            h = (sx * 0.12, 0.04, hc + 0.1)
        elif a == "brow":
            e = (sx * 0.3, 0.2, sh - 0.05)
            h = (sx * 0.05, 0.2, hc + 0.07)
        elif a == "wave":
            e = (sx * 0.42, 0.0, sh + 0.12)
            h = (sx * 0.52, 0.0, sh + 0.42)
        elif a == "hold":
            e = (sx * 0.24, 0.16, sh - 0.32)
            h = (sx * 0.1, 0.34, sh - 0.3)
        else:
            e = (sx * 0.28, 0, sh - 0.3)
            h = (sx * 0.285, 0.01, sh - 0.56)
        p.append(limb(s0, e, 0.12, top))
        p.append(limb(e, h, 0.11, top))
        p.append(W.box(h, (0.1, 0.11, 0.11), skin, bevel=bv))
    p.append(W.box((0, 0, sh + 0.05), (0.1, 0.1, 0.1), skin, bevel=0))
    p.append(F._ball(0.135, (0, 0, hc), skin, sub=2, sc=(1.0, 0.95, 1.12)))
    p.append(F._ball(0.145, (0, -0.025, hc + 0.045), hair, sub=2, sc=(1.02, 0.98, 0.85)))
    fy = 0.125
    for sx in (-1, 1):
        p.append(F._ball(0.042, (sx * 0.052, fy, hc + 0.01), white, sub=2, sc=(1, 0.6, 1.1)))
        p.append(F._ball(0.02, (sx * 0.05, fy + 0.022, hc + 0.0), black, sub=1))
        p.append(W.box((sx * 0.055, fy + 0.005, hc + 0.07), (0.07, 0.02, 0.018), hair, rot=(0, math.radians(-sx * 8), 0), bevel=0))
    p.append(F._ball(0.025, (0, fy + 0.03, hc - 0.045), skin, sub=1))
    me = F._join(p, f"pm_{variant}_{pose}_{arms}")
    _PM[key] = me
    return me


def hat_mesh(kind):
    key = ("hat", kind)
    if key in _PM:
        return _PM[key]
    tz = 0.86 + 0.54 + 0.22 + 0.13
    if kind == "white":
        m = W.mat("cap_white", (0.92, 0.92, 0.90), 0.6)
    else:
        m = W.mat("cap", (0.15, 0.25, 0.45), 0.8)
    parts = [F._ball(0.15, (0, -0.02, tz - 0.03), m, sub=2, sc=(1.0, 1.0, 0.6)),
             W.box((0, 0.13, tz - 0.06), (0.2, 0.14, 0.015), m, bevel=0)]
    _PM[key] = F._join(parts, f"hat_{kind}")
    return _PM[key]


def person(loc, facing, seed=0, arms="down", look=None, pose="stand", scale=1.0, hat=None, alt=None, nf=0, period=10):
    """facing 0 = +y（富士山の方）。alt に別の腕のポーズを渡すと、period コマごとに切り替える（ばんざい・手をふる）。"""
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    root.rotation_euler.z = math.radians(-facing)
    bodies = []
    for a in ([arms] + ([alt] if alt else [])):
        b = bpy.data.objects.new(f"p{seed}_{a}", person_mesh(seed % 12, pose, a, look))
        bpy.context.collection.objects.link(b)
        b.parent = root
        b.scale = (scale,) * 3
        if hat:
            h = bpy.data.objects.new("hat", hat_mesh(hat))
            bpy.context.collection.objects.link(h)
            h.parent = b
        bodies.append(b)
    if alt:
        for f in range(1, nf + 2, period):
            on = (f // period) % 2
            for k, b in enumerate(bodies):
                v = scale if k == on else 1e-4
                b.scale = (v,) * 3
                b.keyframe_insert("scale", frame=f)
        for b in bodies:
            set_interp(b, 'CONSTANT')
    return root


# ---------- 空と光 ----------
SKY_K, SUN_K = 0.6, 1.3     # 参考元の「強い日差し・濃い影」に寄せる（空の光を弱く、太陽を強く）


def sky(lo=(0.96, 0.90, 0.80), hi=(0.42, 0.62, 0.88), strength=0.45):
    """空。カメラに見える空は明るいまま、まわりを照らす光だけ弱くする（影が濃くなる）。"""
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
    cr.elements[0].color = (*lo, 1)
    cr.elements[1].position = 0.5
    cr.elements[1].color = (*hi, 1)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], bg.inputs[0])
    bg.inputs[1].default_value = strength * SKY_K
    bg2 = nt.nodes.new("ShaderNodeBackground")
    nt.links.new(ramp.outputs[0], bg2.inputs[0])
    bg2.inputs[1].default_value = strength * 1.7
    lp = nt.nodes.new("ShaderNodeLightPath")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0])
    nt.links.new(bg.outputs[0], mix.inputs[1])
    nt.links.new(bg2.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], nt.nodes["World Output"].inputs[0])


def sun(elev, az, strength=4.5, col=(1.0, 0.93, 0.80)):
    """az=0 で +y の空から手前（-y）へ照らす。"""
    bpy.ops.object.light_add(type='SUN')
    s = bpy.context.object
    e, a = math.radians(elev), math.radians(az)
    d = Vector((-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e)))
    s.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    s.data.energy = strength * SUN_K
    s.data.color = (col[0], col[1] * 0.97, col[2] * 0.9)
    s.data.angle = math.radians(1.0)
    return s


def room(col, strength):
    """室内の背景の光（参考元のように影を濃く、暖かく）。"""
    w = bpy.data.worlds.new("room")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes["Background"].inputs[0].default_value = (*col, 1)
    nt.nodes["Background"].inputs[1].default_value = strength * SKY_K
    bg2 = nt.nodes.new("ShaderNodeBackground")       # カメラに見える部分（天井のない所）は明るいまま
    bg2.inputs[0].default_value = (*col, 1)
    bg2.inputs[1].default_value = 0.9
    lp = nt.nodes.new("ShaderNodeLightPath")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0])
    nt.links.new(nt.nodes["Background"].outputs[0], mix.inputs[1])
    nt.links.new(bg2.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], nt.nodes["World Output"].inputs[0])


def window_sun(elev=30, az=-60, strength=3.5):
    """窓から差しこむ日差し（室内に濃い光と影を作る）。"""
    return sun(elev, az, strength, (1.0, 0.85, 0.65))


def day(elev=35, az=-35, strength=4.6, col=(1.0, 0.93, 0.80)):
    sky()
    return sun(elev, az, strength * 1.15, col)


def morning():
    sky(lo=(1.0, 0.86, 0.68), hi=(0.48, 0.64, 0.88), strength=0.5)
    e, a = (float(v) for v in os.environ.get("MSUN", "28,-70").split(","))
    return sun(e, a, 4.8, (1.0, 0.82, 0.62))


# ---------- 富士山 ----------
def fuji_profile(u):
    """u=0 すそ → 1 山頂。半径（すそ=1）を返す。すそが広く、上が急な形。"""
    return 0.1 + 0.9 * (1 - u) ** 2.1


def fuji_mesh(H=0.27, seed=3):
    key = ("fuji", H, seed)
    if key in _PM:
        return _PM[key]
    import bmesh
    r = random.Random(seed)
    N, RINGS = 40, 14
    rock = W.mat("fuji_rock", (0.30, 0.36, 0.52), 0.95)
    snow = W.mat("fuji_snow", (0.93, 0.95, 0.98), 0.7)
    bm = bmesh.new()
    rings = []
    jit = [[r.uniform(-0.025, 0.025) for _ in range(N)] for _ in range(RINGS + 1)]
    snow_line = [0.58 + 0.12 * abs(math.sin(k * 2.7)) + r.uniform(-0.04, 0.04) for k in range(N)]
    for i in range(RINGS + 1):
        u = i / RINGS
        ring = []
        for k in range(N):
            a = 2 * math.pi * k / N
            rad = fuji_profile(u) * (1 + jit[i][k] * (1 - u) * 0.6)
            ring.append(bm.verts.new((rad * math.cos(a), rad * math.sin(a), H * u + (0 if i < RINGS else -0.012))))
        rings.append(ring)
    bm.verts.ensure_lookup_table()
    for i in range(RINGS):
        for k in range(N):
            f = bm.faces.new((rings[i][k], rings[i][(k + 1) % N], rings[i + 1][(k + 1) % N], rings[i + 1][k]))
            f.material_index = 1 if (i + 0.5) / RINGS > snow_line[k] else 0
    f = bm.faces.new(list(reversed(rings[RINGS])))
    f.material_index = 1
    me = bpy.data.meshes.new("fuji")
    bm.to_mesh(me)
    bm.free()
    me.materials.append(rock)
    me.materials.append(snow)
    for p in me.polygons:
        p.use_smooth = False
    me.use_fake_user = True
    _PM[key] = me
    return me


FUJI_H = 0.27


def fuji(loc, R, name="fuji", ghost=False):
    """富士山（すその半径 R）。ghost=True で白い線だけ（図解用）。"""
    me = fuji_mesh(FUJI_H)
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.scale = (R, R, R)
    o["R"] = R
    if ghost:
        o.data = me.copy()
        o.data.materials.clear()
        o.data.materials.append(W.mat("ghost", (0.9, 0.95, 1.0), emit=(0.85, 0.92, 1.0), emit_strength=2.5))
        wf = o.modifiers.new("wf", "WIREFRAME")
        wf.thickness = 0.004
        o.visible_shadow = False
    return o


def surface_points(o, n, seed, front=None):
    r = random.Random(seed)
    R = o["R"]
    out = []
    for _ in range(n):
        u = 1 - math.sqrt(r.random())
        a = r.uniform(0, 2 * math.pi) if front is None else front + r.uniform(-1.4, 1.4)
        rad = fuji_profile(u) * R
        out.append(Vector(o.location) + Vector((rad * math.cos(a), rad * math.sin(a), FUJI_H * R * u)))
    return out


def particle_meshes(white_only=False):
    """消える演出の粒：参考元のような四角い粒（金色と白）。"""
    key = ("cubes", white_only)
    if key in _PM:
        return _PM[key]
    out = []
    cols = [("cube_white", (1, 0.97, 0.90), (1.0, 0.96, 0.85), 3.0)]
    if not white_only:
        cols.insert(0, ("cube_gold", (1.0, 0.75, 0.3), (1.0, 0.62, 0.18), 5.0))
    for nm, col, em, es in cols:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        tmp = bpy.context.object
        tmp.data.materials.append(W.mat(nm, col, emit=em, emit_strength=es))
        tmp.data.use_fake_user = True
        out.append(tmp.data)
        bpy.data.objects.remove(tmp)
    _PM[key] = out
    return out


def sparkle_points(points, f0, size, rise, mode="out", seed=1, life=(0.7, 1.5), name="sp", trail=(2, 4), center=None,
                   burst=0.0, white=False, gold_ratio=0.6):
    """四角い光の粒。center を渡すと、そこから外向きに飛び散る（burst＝横向きの速さ）。うしろに小さな粒が続いて光の跡になる。"""
    r = random.Random(seed)
    meshes = particle_meshes(white)
    for k, p0 in enumerate(points):
        me = meshes[0 if (not white and r.random() < gold_ratio) else -1]
        sz = size * r.uniform(0.6, 1.5)
        v = Vector((r.uniform(-0.35, 0.35) * rise, r.uniform(-0.35, 0.35) * rise, r.uniform(0.4, 1.1) * rise))
        if center is not None:
            out = Vector((p0.x - center[0], p0.y - center[1], 0))
            if out.length > 1e-6:
                v += out.normalized() * burst * r.uniform(0.4, 1.2)
        spin = Vector((r.uniform(-6, 6), r.uniform(-6, 6), r.uniform(-6, 6)))
        rot0 = Vector((r.uniform(0, 3), r.uniform(0, 3), r.uniform(0, 3)))
        lf = r.uniform(*life)
        nfr = int(lf * FPS)
        start = f0 + (r.randint(0, 10) if mode == "out" else 0)

        def state(f):
            if mode == "out":
                dt = (f - start) / FPS
                vis = 0 <= dt <= lf
            else:
                dt = (start + nfr - f) / FPS
                vis = f >= start and dt >= 0
                dt = max(dt, 0)
            u = min(max(dt / lf, 0), 1)
            # 飛び出してから、空気にブレーキをかけられて ゆっくりになる
            s = (1 - math.exp(-2.2 * dt)) / 2.2
            return p0 + v * s, (sz * (1 - 0.8 * u) if vis else 1e-4), rot0 + spin * dt
        for j, (dl, ks) in enumerate([(0, 1.0)] + [(d, 0.7 ** (i + 1)) for i, d in enumerate(trail)]):
            if j and r.random() < 0.4:
                continue
            o = bpy.data.objects.new(f"{name}{k}_{j}", me)
            bpy.context.collection.objects.link(o)
            o.visible_shadow = False
            for f in range(max(1, start - 1), start + nfr + 2 + dl):
                loc, sc, rt = state(f - dl)
                o.location = loc
                o.rotation_euler = rt
                o.scale = (max(sc * ks, 1e-4),) * 3
                o.keyframe_insert("location", frame=f)
                o.keyframe_insert("scale", frame=f)
                o.keyframe_insert("rotation_euler", frame=f)
            if start - 2 >= 1:
                o.scale = (1e-4,) * 3
                o.keyframe_insert("scale", frame=1)


def fuji_vanish(o, f0, n=650, seed=3):
    R = o["R"]
    sparkle_points(surface_points(o, n, seed), f0, R * 0.01, R * 0.3, seed=seed, center=o.location, burst=R * 0.35)
    C.show_between(o, None, f0 + 4, s=R)


def fuji_appear(o, f0, n=650, seed=4):
    R = o["R"]
    sparkle_points(surface_points(o, n, seed), f0 - 30, R * 0.01, R * 0.3, mode="in", seed=seed, life=(0.8, 1.0),
                   center=o.location, burst=R * 0.35)
    C.show_between(o, f0, None, s=R)


def snow_cap_mesh():
    """富士山の雪の部分だけのメッシュ。"""
    key = ("snowcap",)
    if key in _PM:
        return _PM[key]
    import bmesh
    me = fuji_mesh(FUJI_H).copy()
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index == 0], context='FACES')
    bm.to_mesh(me)
    bm.free()
    me.use_fake_user = True
    _PM[key] = me
    return me


def snow_fall(o, f0, hang=8, fall=36, seed=7):
    """山だけが消えて、雪の部分が一瞬 空中に残る → 重力で落ちて（だんだん速く）、地面で白い粉になって散る。"""
    R = o["R"]
    s = bpy.data.objects.new("snowcap", snow_cap_mesh())
    bpy.context.collection.objects.link(s)
    s.location = o.location
    s.scale = (1e-4,) * 3
    s.keyframe_insert("scale", frame=1)
    s.keyframe_insert("scale", frame=f0 + 2)
    s.scale = (R,) * 3
    s.keyframe_insert("scale", frame=f0 + 3)
    z_top = FUJI_H * R
    z_low = FUJI_H * R * 0.55        # 雪の下のはし
    for k in range(fall + 1):
        u = k / fall
        s.location.z = o.location.z - z_low * u * u      # 等加速度（落ちる距離は時間の2乗）
        s.rotation_euler.x = math.radians(4 * u * u)
        s.keyframe_insert("location", frame=f0 + hang + k)
        s.keyframe_insert("rotation_euler", frame=f0 + hang + k)
    s.location.z = o.location.z
    s.keyframe_insert("location", frame=f0 + hang - 1)
    end = f0 + hang + fall
    s.keyframe_insert("scale", frame=end)
    s.scale = (1e-4,) * 3
    s.keyframe_insert("scale", frame=end + 1)
    # 落ちながら、下のはしから雪のかけらがこぼれる
    r = random.Random(seed)
    for k in range(0, fall, 4):
        u = k / fall
        zc = o.location.z + z_low - z_low * u * u
        pts = []
        for _ in range(14):
            a = r.uniform(0, 2 * math.pi)
            rad = fuji_profile(0.6) * R * r.uniform(0.85, 1.0)
            pts.append(Vector(o.location) + Vector((rad * math.cos(a), rad * math.sin(a), zc - o.location.z)))
        sparkle_points(pts, f0 + hang + k, R * 0.008, R * 0.05, seed=seed + k, life=(0.6, 1.0), white=True,
                       name=f"crumb{k}_", trail=())
    # 地面に落ちたところで、白い粉が横に広がる
    pts = []
    for _ in range(260):
        a = r.uniform(0, 2 * math.pi)
        rad = r.uniform(0.05, 0.55) * R
        pts.append(Vector(o.location) + Vector((rad * math.cos(a), rad * math.sin(a), r.uniform(0, 0.05) * z_top)))
    sparkle_points(pts, end - 4, R * 0.01, R * 0.08, seed=seed, life=(1.0, 1.8), center=o.location, burst=R * 0.5,
                   white=True, name="powder", trail=())
    return s


def cloud_mat():
    return W.mat("cloud", (0.97, 0.97, 0.99), 1.0, emit=(1.0, 1.0, 1.0), emit_strength=0.25)


def cap_cloud(top, R, name="kasa", seed=1):
    """笠雲（山頂にかぶさる、平たいレンズ形の雲）。"""
    r = random.Random(seed)
    pts = [(top[0] + r.uniform(-0.05, 0.05) * R, top[1] + r.uniform(-0.05, 0.05) * R, top[2] + R * (0.01 + 0.012 * k),
            R * (0.17 - 0.03 * k), (1, 1, 0.16)) for k in range(3)]
    return recenter(C.multi_ball(pts, cloud_mat(), name, sub=2), top)


def lens_cloud(loc, R, name="tsurushi"):
    pts = [(loc[0], loc[1], loc[2] + R * 0.012 * k, R * (0.12 - 0.025 * k), (1.4, 0.8, 0.18)) for k in range(3)]
    return recenter(C.multi_ball(pts, cloud_mat(), name, sub=2), loc)


def recenter(o, c):
    """メッシュの中心を c に移す（その場で大きさを変えられるように）。"""
    from mathutils import Matrix
    o.data.transform(Matrix.Translation(-Vector(c)))
    o.location = c
    return o


def grow(o, f0, f1, s1=1.0, s0=1e-4):
    o.scale = (s0,) * 3
    o.keyframe_insert("scale", frame=max(1, f0))
    o.scale = (s1,) * 3
    o.keyframe_insert("scale", frame=f1)


# ---------- 部品 ----------
def foothills(seed=5, y=(900, 1500), x=(-1500, 1500), n=9, col=(0.28, 0.40, 0.36), h=(60, 160), gap=None):
    r = random.Random(seed)
    m = W.mat(f"hill_{col}", col, 1.0)
    for i in range(n):
        xx = r.uniform(*x)
        if gap and gap[0] < xx < gap[1]:
            continue
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=r.uniform(250, 450), depth=r.uniform(*h),
                                        location=(xx, r.uniform(*y), 0))
        o = bpy.context.object
        o.location.z = o.dimensions.z / 2 - 10
        o.data.materials.append(m)


def town(seed=1, y=(40, 400), x=(-260, 260), n=90):
    r = random.Random(seed)
    walls = [W.mat("wall_a", (0.86, 0.82, 0.74)), W.mat("wall_b", (0.78, 0.76, 0.72)), W.mat("wall_c", (0.90, 0.88, 0.82))]
    roofs = [W.mat("roof_a", (0.30, 0.22, 0.20)), W.mat("roof_b", (0.22, 0.26, 0.32)), W.mat("roof_c", (0.45, 0.25, 0.20))]
    for k, (wm, rm) in enumerate(((0, 0), (1, 1), (2, 2), (0, 1), (1, 2))):
        bx, rx = [], []
        for _ in range(n // 5):
            xx, yy = r.uniform(*x), r.uniform(*y)
            w, d, h = r.uniform(6, 11), r.uniform(6, 10), r.uniform(5, 7)
            bx.append((xx, yy, h / 2, w, d, h, 0))
            rx.append((xx, yy, h + 0.8, w + 1.0, d + 1.0, 1.6, 0))
        C.multi_box(bx, walls[wm], f"town_w{k}")
        C.multi_box(rx, roofs[rm], f"town_r{k}")


def wire(p0, p1, m, r=0.012):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    rot = d.to_track_quat('Z', 'Y').to_euler()
    o = F._cyl(r, r, d.length, tuple((p0 + p1) / 2), m, rot=tuple(rot), verts=5)
    o.visible_shadow = False
    return o


def utility_poles(pts, h=9.0):
    """電柱と電線（日本の町らしさ）。pts = [(x, y)]。"""
    pole = W.mat("pole_conc", (0.62, 0.62, 0.60), 0.9)
    dark = W.mat("wire_black", (0.05, 0.05, 0.05), 0.6)
    for (x, y) in pts:
        F._cyl(0.14, 0.11, h, (x, y, h / 2), pole, verts=8)
        W.box((x, y, h - 0.6), (1.6, 0.1, 0.1), pole, bevel=0)
        F._cyl(0.18, 0.18, 0.45, (x + 0.35, y, h - 1.6), W.mat("transformer", (0.55, 0.58, 0.60), 0.6), verts=10)
    for (a, b) in zip(pts, pts[1:]):
        for dx in (-0.7, 0.0, 0.7):
            mid = ((a[0] + b[0]) / 2 + dx, (a[1] + b[1]) / 2, h - 0.9)
            wire((a[0] + dx, a[1], h - 0.55), mid, dark)
            wire(mid, (b[0] + dx, b[1], h - 0.55), dark)


def cat(loc, facing=0, col=(0.85, 0.55, 0.25)):
    """丸くなって寝ているネコ。"""
    m = W.mat(f"cat_{col}", col, 0.9)
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    root.rotation_euler.z = math.radians(-facing)
    parts = [F._ball(0.16, (0, 0, 0.1), m, sub=2, sc=(1.3, 1.0, 0.65)), F._ball(0.09, (0.17, 0.08, 0.13), m, sub=2),
             F._cyl(0.035, 0.0, 0.07, (0.14, 0.11, 0.22), m, verts=4), F._cyl(0.035, 0.0, 0.07, (0.21, 0.07, 0.22), m, verts=4),
             F._ball(0.04, (-0.12, 0.12, 0.05), m, sub=1, sc=(2.5, 1.0, 0.8))]
    for p in parts:
        p.parent = root
    for f, s in ((1, 1.0), (45, 1.06), (90, 1.0), (135, 1.06), (180, 1.0), (225, 1.06)):     # 寝息でおなかが動く
        parts[0].scale = (1, 1, s)
        parts[0].keyframe_insert("scale", frame=f)
    return root


def engawa_props():
    """縁側の小物（座ぶとん、お茶、盆栽、くつぬぎ石とげた、ネコ）。"""
    W.box((0.2, 0.75, 0.475), (0.55, 0.55, 0.06), W.mat("zabuton", (0.55, 0.18, 0.20), 0.9), bevel=0.02)
    W.box((-0.5, 0.72, 0.475), (0.45, 0.45, 0.06), W.mat("zabuton2", (0.20, 0.30, 0.50), 0.9), bevel=0.02)
    W.box((0.95, 0.55, 0.465), (0.42, 0.3, 0.03), W.mat("tray", (0.30, 0.15, 0.10), 0.4), bevel=0.01)
    F._ball(0.075, (0.88, 0.55, 0.54), W.mat("kyusu", (0.35, 0.22, 0.14), 0.3), sub=2, sc=(1, 1, 0.85))
    F._cyl(0.012, 0.006, 0.09, (0.80, 0.55, 0.56), W.mat("kyusu", (0.35, 0.22, 0.14), 0.3), rot=(0, math.radians(-60), 0))
    for k in range(2):
        F._cyl(0.033, 0.028, 0.07, (1.03 + k * 0.08, 0.5 + k * 0.08, 0.515), W.mat("yunomi", (0.80, 0.78, 0.70), 0.3),
               verts=12)
    F._cyl(0.16, 0.12, 0.16, (-1.5, 0.6, 0.53), W.mat("bonsai_pot", (0.30, 0.32, 0.38), 0.4), verts=12)
    C.multi_ball([(-1.5 + dx, 0.6, 0.78 + dz, rr, (1.4, 1.0, 0.6)) for dx, dz, rr in ((-0.12, 0.05, 0.13), (0.1, 0.12, 0.12),
                                                                                      (0.0, 0.24, 0.1))],
                 W.mat("bonsai_leaf", (0.16, 0.34, 0.12), 0.9), "bonsai")
    F._cyl(0.025, 0.03, 0.25, (-1.5, 0.6, 0.72), W.mat("bonsai_trunk", (0.30, 0.20, 0.12), 0.9), verts=6)
    W.box((0.1, 1.45, 0.12), (1.0, 0.55, 0.24), W.mat("rock_step", (0.55, 0.54, 0.50), 1.0), bevel=0.06)
    geta = W.mat("geta", (0.65, 0.48, 0.30), 0.7)
    for dx in (-0.1, 0.1):
        W.box((dx, 1.42, 0.27), (0.1, 0.24, 0.03), geta, bevel=0.005)
    cat((-1.0, 0.25, 0.45), 200)


def engawa_set(people=True):
    """富士市の家の縁側。縁側の床の端が y=1.0、高さ 0.45。富士山は +y の遠く。"""
    wood = W.mat("engawa", (0.55, 0.38, 0.22), 0.6)
    dark = W.mat("eave", (0.20, 0.17, 0.15), 0.8)
    W.box((0, -0.75, 0.22), (9, 3.5, 0.45), wood, bevel=0.01)
    for x in (-4.2, 4.2):
        W.box((x, 0.9, 1.6), (0.14, 0.14, 3.2), wood, bevel=0.01)
    W.box((0, -1.4, 3.6), (10, 2.4, 0.2), dark, rot=(math.radians(-6), 0, 0), bevel=0.02)
    shoji = W.mat("shoji", (1.0, 0.97, 0.9), emit=(1.0, 0.93, 0.8), emit_strength=0.3)
    W.box((0, -2.5, 1.5), (9, 0.05, 2.2), shoji, bevel=0)
    C.grass_ground(col=(0.30, 0.42, 0.14), tufts=4000, area=(-7, 7, 1.2, 14))
    hedge = W.mat("leafy_hedge", (0.18, 0.36, 0.14), 0.9)
    W.box((0, 14, 0.6), (40, 1.2, 1.2), hedge, bevel=0.2)
    for i, (x, y, h) in enumerate(((-5.5, 10, 4.5), (6.0, 11, 4.0))):
        C.tree((x, y, 0), h=h, seed=40 + i, crowns=[(0.17, 0.36, 0.12)])
    W.box((3.0, 4.5, 0.4), (0.8, 0.8, 0.8), W.mat("stone_lantern", (0.6, 0.6, 0.58), 0.9), bevel=0.05)
    engawa_props()
    utility_poles([(-25, 20), (-8, 20), (9, 20), (26, 20)])
    town(seed=2, y=(40, 500), n=120)
    foothills(seed=3, y=(700, 1200), n=10, col=(0.30, 0.42, 0.34), h=(40, 90))


FUJI_LOC = (200, 4500, 0)
FUJI_R = 3200


def engawa_cam(nf, loc=(-0.4, -2.1, 1.5), at=(0.3, 30, 7.0), lens=28, push=0.4):
    cam = W.camera(loc, at, lens)
    cam["push"] = push * 0.3
    return cam


# ---------- 場面 ----------
def f01_open(nf):
    morning()
    engawa_set()
    person((0.2, 0.8, 0.45), 0, seed=4, arms="pray", look=GRANDPA)
    fj = fuji(FUJI_LOC, FUJI_R)
    fv = fr(TL.T_VANISH)
    fuji_vanish(fj, fv)
    snow_fall(fj, fv)
    # 山頂の笠雲：山が消えても、雲だけがその場に残る → ゆっくり沈んで広がる
    kasa = cap_cloud((FUJI_LOC[0], FUJI_LOC[1], FUJI_H * FUJI_R + 8), FUJI_R)
    kasa.scale = (0.55, 0.55, 0.6)
    kasa.keyframe_insert("scale", frame=fv + 6)
    kasa.keyframe_insert("location", frame=fv + 6)
    kasa.scale = (0.8, 0.8, 0.4)
    kasa.location.z -= FUJI_H * FUJI_R * 0.12
    kasa.keyframe_insert("scale", frame=nf)
    kasa.keyframe_insert("location", frame=nf)
    for k in range(5):     # 朝の小鳥
        b = C.link_copy(C.small_bird_mesh(), (-20 + k * 7, 60 + k * 9, 18 + k), f"bird{k}")
        b.scale = (3,) * 3
        b.keyframe_insert("location", frame=1)
        b.location.x += 40
        b.keyframe_insert("location", frame=nf)
    for k in range(3):     # 手前を横切る小鳥
        b = C.link_copy(C.small_bird_mesh(), (-14 - k * 2.5, 13 + k * 3, 4.5 + k * 0.6), f"birdn{k}")
        b.scale = (1.5,) * 3
        b.keyframe_insert("location", frame=1)
        b.location.x += 34
        b.keyframe_insert("location", frame=110)
    top = (FUJI_LOC[0], FUJI_LOC[1], FUJI_H * FUJI_R * 0.62)
    # 冒頭：おじいさんの肩ごしに、横へ回りこみながら富士山（手前のおじいさんはボケる）
    cut(1, (-0.45, -1.55, 1.6), top, lens=55, orbit=20, push=0.15, piv=2.4, fixat=1, focus="far")
    cut(61, (0.55, 2.7, 1.95), (0.2, 0.8, 1.95), lens=40, orbit=14, push=0.25)
    c = engawa_cam(nf)
    c["f0"] = 121
    # 消えたあと：望遠で、残った雪が落ち、雲だけが残る「何もない空」を文字なしで見せる
    cut(fv + 8, (-0.4, -2.1, 1.5), (FUJI_LOC[0], FUJI_LOC[1], FUJI_H * FUJI_R * 0.45), lens=45, orbit=10, push=0.0, piv=3,
        fixat=1, focus="far", zoom=1.18)
    return nf


def train_set():
    """新幹線の車内（E席側の窓が +x）。"""
    wall = W.mat("train_wall", (0.90, 0.90, 0.88), 0.5)
    seat = W.mat("seat_blue", (0.20, 0.30, 0.60), 0.8)
    floor = W.mat("train_floor", (0.55, 0.52, 0.48), 0.8)
    W.box((0, 0, 0), (3.4, 30, 0.1), floor, bevel=0)
    W.box((0, 0, 2.45), (3.4, 30, 0.1), wall, bevel=0)
    W.box((-1.7, 0, 1.2), (0.1, 30, 2.4), wall, bevel=0)
    W.box((1.7, 0, 0.42), (0.12, 30, 0.84), wall, bevel=0)
    W.box((1.7, 0, 2.05), (0.12, 30, 0.8), wall, bevel=0)
    for y in range(-14, 15, 2):
        W.box((1.7, y + 0.95, 1.25), (0.16, 0.5, 0.9), wall, bevel=0.03)
    for y in range(-12, 13, 1):
        for x0 in (-1.1, 0.95):
            W.box((x0, y, 0.48), (1.0 if x0 > 0 else 1.0, 0.5, 0.12), seat, bevel=0.03)
            W.box((x0, y - 0.25, 0.85), (1.0, 0.1, 0.75), seat, bevel=0.03)
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 2.35))
    a = bpy.context.object
    a.data.energy = 300
    a.data.size = 3
    a.data.size_y = 20
    a.data.shape = 'RECTANGLE'


def f02_train(nf):
    day(elev=30, az=-60, strength=4.4)
    train_set()
    C.grass_ground(col=(0.36, 0.48, 0.18), name="field_rice")
    r = random.Random(4)
    # 窓の外を流れる家と木（-y へ）
    objs = []
    for k in range(14):
        x = r.uniform(15, 70)
        if r.random() < 0.5:
            o = W.box((x, 0, 3), (8, 8, 6), W.mat("wall_c", (0.90, 0.88, 0.82)), bevel=0.1)
        else:
            o = F._cyl(3, 0.5, 9, (x, 0, 4.5), W.mat("leafy_t", (0.2, 0.4, 0.15), 0.9), verts=7)
        objs.append((o, r.uniform(-40, 60)))
    for o, y0 in objs:
        o.location.y = y0
        o.keyframe_insert("location", frame=1)
        o.location.y = y0 - 0.9 * 70 * nf / FPS
        o.keyframe_insert("location", frame=nf)
        set_interp(o, 'LINEAR')
    foothills(seed=6, y=(700, 1100), x=(200, 1400), n=8, col=(0.30, 0.42, 0.36), h=(40, 90))
    fj = fuji((1700, 800, 0), 1200)
    fuji_vanish(fj, 10)
    for k, (y, fac) in enumerate(((-0.6, 80), (0.5, 100), (1.5, 75))):
        person((0.9, y, 0.05), fac, seed=5 + k * 3, arms="hold" if k == 1 else "down")
    W.camera((-1.0, -0.5, 1.15), (1.7, 1.0, 1.35), lens=22)
    cut(61, (1.55, -0.6, 1.4), (0.9, 0.6, 1.5), lens=22, orbit=10)
    return nf


def f03_shadow(nf):
    """朝霧高原：うしろ（+y）の富士山の影が、牧場に長くのびている → 消える。カメラは影の先（-y）を見る。"""
    sky(lo=(1.0, 0.80, 0.58), hi=(0.50, 0.62, 0.86), strength=0.5)
    sun(3, 0, 8.0, (1.0, 0.72, 0.45))
    C.grass_ground(col=(0.34, 0.46, 0.16), size=4000, tufts=3000, area=(-8, 8, -16, 2))
    fj = fuji((0, 200, 0), 100)
    fj.visible_camera = False
    C.show_between(fj, None, 45, s=fj["R"])
    fence = W.mat("fence", (0.55, 0.42, 0.28), 0.9)
    for k in range(-10, 11):
        W.box((k * 2.0, -6, 0.5), (0.1, 0.1, 1.0), fence, bevel=0)
    W.box((0, -6, 0.8), (42, 0.06, 0.08), fence, bevel=0)
    W.box((0, -6, 0.45), (42, 0.06, 0.08), fence, bevel=0)
    r = random.Random(3)
    cow((1.2, -9.0), 100, seed=1, nf=nf)
    cow((-2.6, -12.5), 230, seed=2, nf=nf)
    for k in range(6):
        cow((r.uniform(-14, 14), r.uniform(-40, -16)), r.uniform(0, 360), seed=3 + k)
    # 牧場の牛舎とサイロ、干し草ロール
    W.box((-16, -34, 2.5), (10, 7, 5), W.mat("barn", (0.72, 0.22, 0.16), 0.8), bevel=0.05)
    W.box((-16, -34, 5.4), (10.6, 7.6, 0.9), W.mat("barn_roof", (0.25, 0.27, 0.30), 0.7), bevel=0.05)
    F._cyl(2.0, 2.0, 11, (-9.5, -36, 5.5), W.mat("silo", (0.85, 0.84, 0.80), 0.7), verts=16)
    F._ball(2.0, (-9.5, -36, 11), W.mat("silo_top", (0.30, 0.45, 0.55), 0.5), sub=2, sc=(1, 1, 0.6))
    for k in range(5):
        F._cyl(0.7, 0.7, 1.2, (6 + k * 1.6, -22 - (k % 2) * 1.2, 0.7), W.mat("hay", (0.85, 0.75, 0.45), 0.9),
               rot=(0, math.radians(90), 0), verts=14)
    foothills(seed=9, y=(-1400, -900), x=(-1400, 1400), n=9, col=(0.36, 0.44, 0.50), h=(80, 200))
    for i in range(8):
        C.tree((r.uniform(-60, 60), r.uniform(-120, -50), 0), h=r.uniform(7, 10), seed=60 + i, crowns=[(0.16, 0.32, 0.12)])
    # 手前に牛。富士山の影の中 → 影が消えて、牧場いっぱいに朝日が当たる
    W.camera((2.6, -2.2, 2.1), (-1.0, -40, 0.4), lens=24)
    cut(90, (4.4, -6.6, 1.3), (1.8, -9.3, 0.95), lens=35, orbit=16, push=0.2)
    return nf


def cow(loc, facing, seed=0, nf=0):
    """ホルスタイン（白に黒のもよう、ピンクの鼻、角、しっぽ）。nf を渡すと、首を下げて草を食べる。"""
    r = random.Random(seed)
    white = W.mat("cow_white", (0.92, 0.92, 0.90), 0.8)
    blk = W.mat("cow_black", (0.06, 0.06, 0.06), 0.8)
    pink = W.mat("cow_nose", (0.85, 0.55, 0.55), 0.6)
    horn = W.mat("cow_horn", (0.85, 0.80, 0.65), 0.5)
    bpy.ops.object.empty_add(location=(loc[0], loc[1], 0))
    root = bpy.context.object
    root.rotation_euler.z = math.radians(-facing)
    parts = [W.box((0, 0, 1.05), (0.95, 2.1, 0.95), white, bevel=0.12)]
    for _ in range(4):
        sx = r.choice((-1, 1))
        parts.append(W.box((sx * 0.48, r.uniform(-0.7, 0.7), r.uniform(0.9, 1.25)),
                           (0.04, r.uniform(0.4, 0.8), r.uniform(0.3, 0.5)), blk, bevel=0))
    parts.append(W.box((r.uniform(-0.2, 0.2), r.uniform(-0.5, 0.5), 1.53), (r.uniform(0.4, 0.6), r.uniform(0.5, 0.8), 0.04),
                       blk, bevel=0))
    for dx, dy in ((-0.3, -0.75), (0.3, -0.75), (-0.3, 0.75), (0.3, 0.75)):
        parts.append(W.box((dx, dy, 0.32), (0.17, 0.17, 0.64), white, bevel=0))
        parts.append(W.box((dx, dy, 0.04), (0.18, 0.18, 0.08), blk, bevel=0))
    parts.append(F._cyl(0.03, 0.03, 0.8, (0, -1.1, 0.95), white, rot=(math.radians(-15), 0, 0), verts=6))
    bpy.ops.object.empty_add(location=(0, 1.0, 1.25))
    neck = bpy.context.object
    head = [W.box((0, 0.35, 0.0), (0.5, 0.6, 0.5), blk, bevel=0.08),
            W.box((0, 0.68, -0.08), (0.42, 0.14, 0.3), pink, bevel=0.05),
            F._cyl(0.03, 0.0, 0.16, (-0.2, 0.25, 0.3), horn, rot=(0, math.radians(-30), 0), verts=6),
            F._cyl(0.03, 0.0, 0.16, (0.2, 0.25, 0.3), horn, rot=(0, math.radians(30), 0), verts=6),
            W.box((-0.3, 0.25, 0.12), (0.18, 0.06, 0.1), blk, bevel=0), W.box((0.3, 0.25, 0.12), (0.18, 0.06, 0.1), blk, bevel=0)]
    for h in head:
        h.parent = neck
    for p in parts + [neck]:
        p.parent = root
    if nf:
        for f in range(1, nf + 1, 15):      # 首を下げて草を食べる → 顔を上げる
            neck.rotation_euler.x = math.radians(-45 if (f // 45) % 2 == 0 else -5)
            neck.keyframe_insert("rotation_euler", frame=f)
    return root


def mural_texture():
    from PIL import Image, ImageDraw
    p = os.path.join(ASSETS, "mural.png")
    if os.path.exists(p):
        return p
    os.makedirs(ASSETS, exist_ok=True)
    w, h = 1600, 800
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        u = y / h
        d.line((0, y, w, y), fill=(int(90 + 120 * u), int(150 + 80 * u), int(225 + 20 * u)))
    d.polygon([(250, 640), (720, 170), (880, 170), (1350, 640)], fill=(70, 95, 150))
    d.polygon([(600, 290), (720, 170), (880, 170), (1000, 290), (930, 260), (860, 300), (800, 255), (730, 300), (670, 262)],
              fill=(250, 250, 252))
    d.rectangle((0, 600, w, h), fill=(60, 120, 170))
    for x in range(0, w, 60):
        d.arc((x, 610, x + 60, 650), 180, 360, fill=(230, 240, 250), width=4)
    for (cx, s) in ((120, 1.0), (1480, 1.1)):
        d.rectangle((cx - 10, 380, cx + 10, 640), fill=(90, 60, 40))
        for k in range(4):
            yy = 400 + k * 55
            d.ellipse((cx - 110 * s + k * 10, yy - 25, cx + 110 * s - k * 10, yy + 25), fill=(40, 100, 50))
    im.save(p)
    return p


def f04_sento(nf):
    room((0.85, 0.88, 0.9), 0.3)
    window_sun(elev=38, az=150, strength=3.0)
    tile = W.mat("tile", (0.85, 0.90, 0.92), 0.3)
    W.box((0, 0, -0.05), (8, 8, 0.1), W.mat("tile_floor", (0.70, 0.78, 0.80), 0.3), bevel=0)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 3.0, 2.2))
    mu = bpy.context.object
    mu.scale = (6.4, 3.2, 1)
    mu.rotation_euler.x = math.radians(90)
    mu.data.materials.append(C.img_mat("mural", mural_texture()))
    W.box((0, 3.05, 0.35), (8, 0.1, 0.7), tile, bevel=0)
    W.box((-3.9, 0, 2), (0.1, 8, 4), tile, bevel=0)
    W.box((0, 1.6, 0.3), (5.0, 2.6, 0.6), W.mat("tub", (0.40, 0.62, 0.70), 0.3), bevel=0.05)
    W.box((0, 1.6, 0.56), (4.8, 2.4, 0.04), W.mat("water", (0.55, 0.80, 0.85), 0.05), bevel=0)
    for k in range(5):
        W.box((-3.8, -2 + k * 0.8, 0.9), (0.12, 0.1, 0.12), W.mat("faucet", (0.8, 0.8, 0.82), 0.2), bevel=0.01)
    man = person((0.4, 1.2, 0.0), 0, seed=6, pose="sit", look={"top": (0.86, 0.68, 0.55), "bottom": (0.86, 0.68, 0.55)})
    # 黄色い湯おけと、いす
    oke = W.mat("oke_yellow", (0.95, 0.75, 0.10), 0.4)
    stool = W.mat("stool", (0.85, 0.85, 0.82), 0.4)
    for k in range(5):
        F._cyl(0.15, 0.12, 0.13, (-3.3, -2 + k * 0.8, 0.065), oke, verts=14)
        W.box((-2.9, -2 + k * 0.8, 0.13), (0.32, 0.3, 0.26), stool, bevel=0.03)
    for k in range(4):
        F._cyl(0.15, 0.12, 0.13, (1.9, 0.0, 0.065 + k * 0.1), oke, verts=14)
    W.box((-1.0, -0.2, 0.13), (0.32, 0.3, 0.26), stool, bevel=0.03)
    F._cyl(0.15, 0.12, 0.13, (-1.0, -0.2, 0.33), oke, verts=14)
    W.box((-0.4, 0.15, 0.62), (0.35, 0.1, 0.03), W.mat("towel", (0.95, 0.95, 0.95), 0.9), bevel=0.01)
    W.box((-3.84, -0.4, 1.5), (0.04, 3.4, 0.6), W.mat("mirror", (0.8, 0.85, 0.9), 0.05), bevel=0)
    man.location.z = 0.05
    bpy.ops.object.light_add(type='AREA', location=(0, 0.5, 3.8))
    a = bpy.context.object
    a.data.energy = 500
    a.data.size = 5
    F.puffs([(0.0, 1.6, 0.6, 0.0, 0)], [C.sec(f) for f in range(1, nf + 1)], seed=2, col=(1, 1, 1), alpha=0.08,
            size=(0.3, 0.6), rise=(0.2, 0.4), grow=2.0, life=3.0, name="steam")
    W.camera((-1.2, -2.6, 1.3), (0.2, 3.0, 1.7), lens=24)
    return nf


def banner_texture(text, name, bg=(245, 245, 240), fg=(200, 30, 30)):
    from PIL import Image, ImageDraw, ImageFont
    p = os.path.join(ASSETS, f"{name}.png")
    if os.path.exists(p):
        return p
    os.makedirs(ASSETS, exist_ok=True)
    im = Image.new("RGB", (600, 300), bg)
    d = ImageDraw.Draw(im)
    fnt = ImageFont.truetype(FONT, 150)
    fnt.set_variation_by_axes([900])
    d.text((300, 150), text, font=fnt, fill=fg, anchor="mm")
    im.save(p)
    return p


def f05_kitadake(nf):
    day(elev=40, az=-30, strength=4.6)
    rock = W.mat("rock_peak", (0.48, 0.45, 0.42), 1.0)
    bpy.ops.mesh.primitive_cone_add(vertices=9, radius1=40, depth=22, location=(0, 18, -11.2))
    bpy.context.object.data.materials.append(rock)
    r = random.Random(5)
    C.multi_ball([(r.uniform(-3, 3), r.uniform(-2, 3), 0.0, r.uniform(0.2, 0.5), (1, 1, 0.6)) for _ in range(30)],
                 rock, "rocks")
    W.box((0, 0, -0.2), (8, 8, 0.4), rock, bevel=0.2)
    mt = W.mat("mountain_far", (0.40, 0.48, 0.60), 1.0)
    for i in range(10):
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=r.uniform(120, 260), depth=r.uniform(120, 260),
                                        location=(-900 + i * 200, r.uniform(500, 1200), -160))
        bpy.context.object.data.materials.append(mt)
    C.multi_ball([(r.uniform(-700, 700), r.uniform(150, 600), -40, r.uniform(40, 90), (1.6, 1.0, 0.25)) for _ in range(30)],
                 cloud_mat(), "sea_of_clouds", sub=1)
    pole = W.mat("pole_wood", (0.55, 0.42, 0.28), 0.9)
    W.box((0.6, 1.2, 0.8), (0.12, 0.12, 1.6), pole, bevel=0)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0.6, 1.1, 1.0))
    sign = bpy.context.object
    sign.scale = (0.8, 0.4, 1)
    sign.rotation_euler.x = math.radians(90)
    sign.data.materials.append(C.img_mat("sign_peak", banner_texture("日本一", "nihonichi")))
    F._cyl(0.02, 0.02, 1.8, (-0.6, 1.4, 0.9), pole)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(-0.25, 1.4, 1.55))
    fl = bpy.context.object
    fl.scale = (0.7, 0.45, 1)
    fl.rotation_euler.x = math.radians(90)
    fl.data.materials.append(W.mat("flag_red", (0.85, 0.15, 0.12), 0.7))
    for f in range(1, nf + 1, 6):
        fl.rotation_euler.z = math.radians(8 * math.sin(f / 4))
        fl.keyframe_insert("rotation_euler", frame=f)
    person((-0.3, 0.3, 0), 160, seed=2, arms=("down", "up"), hat="cap")
    W.camera((-1.0, -3.4, 1.3), (0.0, 1.2, 1.2), lens=26)
    return nf


def arrow_mesh():
    if ("arrow",) in _PM:
        return _PM[("arrow",)]
    m = W.mat("wind", (0.85, 0.95, 1.0), 0.5, emit=(0.8, 0.93, 1.0), emit_strength=2.0)
    a = F._cyl(0.05, 0.05, 0.9, (-0.45, 0, 0), m, rot=(0, math.radians(90), 0), verts=6)
    b = F._cyl(0.14, 0.0, 0.3, (0.12, 0, 0), m, rot=(0, math.radians(90), 0), verts=8)
    me = F._join([a, b], "arrow")
    me.use_fake_user = True
    _PM[("arrow",)] = me
    return me


def wind_arrows(nf, x0, x1, heights, path, f_switch, scale, speed, seed=1, y=0.0):
    """path(x, z0, before) → z。f_switch コマ目から before=False（山なし）。"""
    me = arrow_mesh()
    r = random.Random(seed)
    span = x1 - x0
    for k, z0 in enumerate(heights):
        for j in range(4):
            o = C.link_copy(me, (0, 0, 0), f"arw{k}_{j}")
            o.scale = (scale,) * 3
            off = span * (j / 4 + r.uniform(0, 0.1))
            for f in range(1, nf + 1, 2):
                x = x0 + (off + speed * f / FPS) % span
                before = f < f_switch
                z = path(x, z0, before)
                z2 = path(x + span * 0.01, z0, before)
                o.location = (x, y, z)
                o.rotation_euler.y = -math.atan2(z2 - z, span * 0.01)
                o.keyframe_insert("location", frame=f)
                o.keyframe_insert("rotation_euler", frame=f)
            set_interp(o, 'CONSTANT')


def f06_cloud(nf):
    """図解：風が山にぶつかって上がり、山頂に笠雲・風下につるし雲 → 山がないと素通り。"""
    day(elev=45, az=-30, strength=4.2)
    R = 100.0
    C.grass_ground(col=(0.30, 0.42, 0.26), size=6000, name="field_far")
    g = fuji((0, 0, 0), R, ghost=True)
    f_sw = 102
    C.show_between(g, None, f_sw, s=R)
    sparkle_points(surface_points(g, 80, 5, front=-math.pi / 2), f_sw, R * 0.01, R * 0.1, seed=5)
    top = (0, 0, FUJI_H * R)
    kasa = cap_cloud((0, 0, FUJI_H * R + 2), R)
    lens = lens_cloud((95, 0, FUJI_H * R + 12), R)
    for o in (kasa, lens):
        o.keyframe_insert("scale", frame=f_sw - 1)
        o.scale = (1e-4,) * 3
        o.keyframe_insert("scale", frame=f_sw + 20)

    def path(x, z0, before):
        if not before:
            return z0
        bump = FUJI_H * R * 1.05 * math.exp(-(x / (0.35 * R)) ** 2)
        lee = 6 * math.sin((x - 30) / 18) * math.exp(-((x - 90) / 50) ** 2) if x > 20 else 0
        return z0 + bump * (1 - 0.15 * (z0 / 30)) + lee

    wind_arrows(nf, -140, 160, [6, 18, 32, 46], path, f_sw, scale=10.0, speed=60, y=-40)
    c = W.camera((10, -175, 28), (10, 0, 30), lens=30)
    c["piv"], c["orbit"] = 175, 14
    cut(61, (20, -110, 42), (0, 0, 31), lens=55, piv=110, orbit=10)
    c = cut(102, (10, -175, 28), (10, 0, 30), lens=30, piv=175, orbit=14)
    return nf


def f07_spring(nf, flowing=True, sparse=False):
    """断面図：富士山にふった雨が地下をゆっくり流れ、柿田川でわき出す。"""
    day(elev=40, az=-20, strength=4.2)
    soil = W.mat("dirt_layer", (0.45, 0.32, 0.20), 1.0)
    lava = W.mat("rock_lava", (0.46, 0.42, 0.40), 1.0)
    bed = W.mat("rock_bed", (0.48, 0.50, 0.58), 1.0)
    W.box((0, 3, -0.6), (40, 6, 1.2), soil, bevel=0)
    W.box((0, 3, -4.0), (40, 6, 5.6), lava, bevel=0)
    W.box((0, 3, -10), (40, 6, 6.4), bed, bevel=0)
    W.box((0, 3, 0.03), (40, 6, 0.06), W.mat("grass_top", (0.30, 0.45, 0.16), 1.0), bevel=0)
    river = W.mat("water_river", (0.25, 0.55, 0.80), 0.05, emit=(0.2, 0.45, 0.7), emit_strength=0.3)
    W.box((10.5, 3, 0.05), (4.0, 6, 0.3 if not sparse else 0.12), river, bevel=0)
    g = fuji((-7.5, 3, 0), 7.0, ghost=True)
    g.modifiers["wf"].thickness = 0.01
    drop = W.mat("drop", (0.35, 0.65, 1.0), 0.2, emit=(0.3, 0.6, 1.0), emit_strength=3.0)
    tmp = F._ball(0.16, (0, 0, 0), drop, sub=1)
    dm = tmp.data
    bpy.data.objects.remove(tmp)
    r = random.Random(2)
    path = [(-7.5, 1.6), (-7.0, -0.8), (-4.5, -3.0), (0.0, -4.4), (5.0, -3.4), (8.5, -1.5), (10.0, 0.1)]
    seglen = [math.dist(path[i], path[i + 1]) for i in range(len(path) - 1)]
    total = sum(seglen)

    def at(u):
        d = u * total
        for i, L in enumerate(seglen):
            if d <= L:
                a = d / L
                return (path[i][0] + (path[i + 1][0] - path[i][0]) * a, path[i][1] + (path[i + 1][1] - path[i][1]) * a)
            d -= L
        return path[-1]

    n = 18 if sparse else 48
    for k in range(n):
        o = C.link_copy(dm, (0, 0, 0), f"drop{k}")
        u0 = k / n + r.uniform(0, 0.01)
        dz = r.uniform(-0.5, 0.5)
        for f in range(1, nf + 1, 2):
            u = (u0 + 0.06 * f / FPS) % 1.0
            x, z = at(u)
            o.location = (x, -0.12, z + dz * (0.3 < u < 0.8))
            o.keyframe_insert("location", frame=f)
        set_interp(o, 'CONSTANT')
    rain = W.mat("rain", (0.7, 0.85, 1.0), 0.3, emit=(0.7, 0.85, 1.0), emit_strength=2.0)
    if not sparse:
        for k in range(30):     # 山にふる雨と雪
            o = W.box((0, 0, 0), (0.04, 0.04, 0.35), rain if k % 3 else W.mat("snowflake", (1, 1, 1), 0.5, emit=(1, 1, 1),
                                                                                     emit_strength=2), bevel=0)
            x0 = -7.5 + r.uniform(-4, 4)
            ph = r.uniform(0, 1)
            for f in range(1, nf + 1, 2):
                u = (ph + f / FPS * 0.8) % 1
                o.location = (x0, 0.5, 9 - 7 * u)
                o.keyframe_insert("location", frame=f)
            set_interp(o, 'CONSTANT')
    for i in range(3):
        C.tree((13 + i * 1.5, 4.5, 0), h=3, seed=90 + i)
    W.camera((1.2, -27, -1.5), (1.2, 0, -1.8), lens=30)
    cut(91, (8.0, -11, -0.3), (9.5, 0, -1.0), lens=30, orbit=12)
    return nf


def f08_snow(nf):
    day(elev=62, az=-20, strength=5.0, col=(1.0, 0.96, 0.86))
    C.grass_ground(col=(0.32, 0.46, 0.15), tufts=4000, area=(-7, 7, -4, 10))
    town(seed=5, y=(60, 400), n=60)
    utility_poles([(-20, 14), (-5, 14), (10, 14), (25, 14)])
    for i, (x, y) in enumerate(((-2.5, 9), (5.0, 8), (-6.5, 12))):
        C.tree((x, y, 0), h=4.0, seed=70 + i)
    foothills(seed=4, y=(800, 1300), n=8, col=(0.30, 0.42, 0.34), h=(40, 90), gap=(-500, 500))
    g = fuji(FUJI_LOC, FUJI_R, ghost=True)
    g.modifiers["wf"].thickness = 0.0015
    C.show_between(g, None, 75, s=FUJI_R)
    person((-0.2, 1.2, 0), 10, seed=3, arms=("down", "brow"), hat="cap")
    W.camera((-1.4, -2.6, 1.3), (6.0, 40, 7), lens=28)
    cut(96, (0.7, 2.4, 1.65), (0.4, 0.5, 1.55), lens=34, orbit=14)
    return nf


def hazard_texture():
    from PIL import Image, ImageDraw, ImageFont
    p = os.path.join(ASSETS, "hazard.png")
    if os.path.exists(p):
        return p
    os.makedirs(ASSETS, exist_ok=True)
    im = Image.new("RGB", (700, 1000), (245, 240, 225))
    d = ImageDraw.Draw(im)
    fnt = ImageFont.truetype(FONT, 64)
    fnt.set_variation_by_axes([900])
    d.text((350, 90), "火山ハザードマップ", font=fnt, fill=(40, 40, 40), anchor="mm")
    d.rectangle((50, 170, 650, 940), fill=(215, 230, 200))
    for rr, col in ((300, (250, 235, 120)), (220, (250, 180, 90)), (140, (235, 100, 80))):
        d.ellipse((350 - rr, 560 - rr * 1.1, 350 + rr, 560 + rr * 1.1), fill=col)
    d.polygon([(290, 600), (350, 520), (410, 600)], fill=(110, 90, 80))
    im.save(p)
    return p


def f09_hazard(nf):
    day(elev=40, az=-40, strength=4.6)
    C.grass_ground(col=(0.32, 0.44, 0.15), tufts=3000, area=(-6, 6, -3, 8))
    town(seed=7, y=(40, 300), n=50)
    utility_poles([(-18, 12), (-3, 12), (12, 12)])
    for i, (x, y) in enumerate(((3.5, 7), (-5.0, 9))):
        C.tree((x, y, 0), h=4.5, seed=80 + i)
    foothills(seed=5, y=(800, 1300), n=8, col=(0.30, 0.42, 0.34), h=(40, 90), gap=(-500, 500))
    board = W.mat("board", (0.45, 0.32, 0.20), 0.8)
    W.box((0, 2.0, 1.4), (1.6, 0.1, 1.2), board, bevel=0.02)
    for x in (-0.7, 0.7):
        W.box((x, 2.0, 0.6), (0.08, 0.08, 1.2), board, bevel=0)
    W.box((0, 2.0, 2.1), (1.9, 0.4, 0.08), W.mat("board_roof", (0.25, 0.25, 0.28), 0.8), bevel=0)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 1.93, 1.4))
    pp = bpy.context.object
    pp.scale = (0.6, 0.86, 1)
    pp.rotation_euler.x = math.radians(90)
    pp.data.materials.append(C.img_mat("hazard", hazard_texture()))
    pp.keyframe_insert("location", frame=1)
    pp.keyframe_insert("rotation_euler", frame=1)
    pp.keyframe_insert("location", frame=30)
    pp.keyframe_insert("rotation_euler", frame=30)
    for f in range(32, nf + 1, 3):
        u = (f - 30) / FPS
        pp.location = (0 + 3.0 * u + 0.3 * math.sin(u * 5), 1.93 + 0.8 * u, 1.4 + 1.2 * u + 0.3 * math.sin(u * 7))
        pp.rotation_euler = (math.radians(90 + 50 * math.sin(u * 4)), math.radians(30 * u), math.radians(40 * math.sin(u * 3)))
        pp.keyframe_insert("location", frame=f)
        pp.keyframe_insert("rotation_euler", frame=f)
    person((-0.9, 0.0, 0), 30, seed=8, arms=("down", "brow"))
    W.camera((-2.2, -3.2, 1.5), (0.6, 2.0, 1.6), lens=26)
    cut(80, (0.2, -1.2, 0.7), (3.5, 4.5, 4.2), lens=22, orbit=10)
    return nf


def chalk_texture():
    from PIL import Image, ImageDraw
    p = os.path.join(ASSETS, "chalk.png")
    if os.path.exists(p):
        return p
    os.makedirs(ASSETS, exist_ok=True)
    im = Image.new("RGB", (1200, 600), (35, 70, 50))
    d = ImageDraw.Draw(im)
    wht = (235, 235, 225)
    d.line([(200, 500), (430, 220), (520, 220), (750, 500)], fill=wht, width=6)
    d.line([(150, 500), (1100, 500)], fill=wht, width=4)
    d.line([(900, 150), (870, 420)], fill=wht, width=4)
    d.ellipse((850, 410, 890, 450), outline=wht, width=4)
    d.line([(900, 150), (900, 450)], fill=(240, 200, 90), width=3)
    d.line([(860, 300), (780, 300)], fill=(240, 120, 110), width=5)
    d.polygon([(770, 300), (795, 288), (795, 312)], fill=(240, 120, 110))
    im.save(p)
    return p


def f10_plumb(nf):
    room((0.9, 0.88, 0.82), 0.35)
    window_sun(elev=28, az=150, strength=3.2)
    W.box((0, 0, -0.05), (8, 8, 0.1), W.mat("floor_wood", (0.60, 0.45, 0.30), 0.6), bevel=0)
    W.box((0, 2.5, 1.6), (8, 0.1, 3.2), W.mat("room_wall", (0.88, 0.86, 0.80), 0.9), bevel=0)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(-0.6, 2.44, 1.75))
    bb = bpy.context.object
    bb.scale = (2.4, 1.2, 1)
    bb.rotation_euler.x = math.radians(90)
    bb.data.materials.append(C.img_mat("chalk", chalk_texture()))
    desk = W.mat("desk", (0.55, 0.40, 0.25), 0.6)
    W.box((0.4, 0.6, 0.8), (1.6, 0.9, 0.06), desk, bevel=0.01)
    for x, y in ((-0.3, 0.2), (1.1, 0.2), (-0.3, 1.0), (1.1, 1.0)):
        W.box((x, y, 0.4), (0.06, 0.06, 0.8), desk, bevel=0)
    metal = W.mat("stand_metal", (0.70, 0.70, 0.72), 0.3)
    W.box((0.4, 0.75, 0.84), (0.4, 0.3, 0.03), metal, bevel=0)
    F._cyl(0.012, 0.012, 0.9, (0.55, 0.75, 1.28), metal)
    W.box((0.42, 0.75, 1.72), (0.3, 0.02, 0.02), metal, bevel=0)
    bpy.ops.object.empty_add(location=(0.3, 0.75, 1.72))
    piv = bpy.context.object
    s = F._cyl(0.006, 0.006, 0.62, (0, 0, -0.31), W.mat("string", (0.95, 0.95, 0.9), 0.6))
    s.parent = piv
    b = F._cyl(0.035, 0.0, 0.08, (0, 0, -0.66), W.mat("bob", (0.80, 0.60, 0.20), 0.3), verts=10)
    b.parent = piv
    ref = F._cyl(0.0015, 0.0015, 0.7, (0.3, 0.735, 1.37), W.mat("refline", (0.95, 0.3, 0.3), 0.5, emit=(1, 0.3, 0.3),
                                                                emit_strength=2))
    for f, deg in ((1, 7), (40, 7), (80, -1.2), (95, 0.6), (110, 0)):
        piv.rotation_euler.y = math.radians(deg)
        piv.keyframe_insert("rotation_euler", frame=f)
    person((1.4, 0.0, 0), 300, seed=1, scale=0.85, look=KID)
    # 理科室の棚（ビーカー、フラスコ、地球儀）
    shelf = W.mat("shelf_wood", (0.50, 0.36, 0.22), 0.7)
    glassm = W.mat("beaker", (0.80, 0.90, 0.95), 0.05, alpha=0.5)
    W.box((2.3, 2.2, 1.0), (1.6, 0.4, 2.0), shelf, bevel=0.01)
    for k in range(3):
        W.box((2.3, 2.0, 0.45 + k * 0.55), (1.5, 0.36, 0.03), W.mat("shelf_board", (0.62, 0.48, 0.32), 0.7), bevel=0)
        for j in range(5):
            F._cyl(0.06, 0.06, 0.16, (1.75 + j * 0.27, 2.0, 0.55 + k * 0.55), glassm, verts=10)
    F._ball(0.18, (-1.6, 0.9, 1.05), W.mat("globe_sea", (0.20, 0.45, 0.75), 0.4), sub=2)
    F._cyl(0.02, 0.03, 0.85, (-1.6, 0.9, 0.42), W.mat("stand_metal", (0.70, 0.70, 0.72), 0.3), verts=8)
    W.box((-1.6, 0.9, 0.0), (0.5, 0.6, 0.04), W.mat("floor_wood", (0.60, 0.45, 0.30), 0.6), bevel=0)
    for k, col in enumerate(((0.95, 0.85, 0.35), (0.45, 0.70, 0.90))):
        W.box((1.2 + k * 0.9, 2.44, 2.2), (0.7, 0.02, 0.9), W.mat(f"poster{k}", col, 0.8), bevel=0)
    W.camera((0.25, -0.55, 1.45), (0.3, 0.75, 1.3), lens=30)
    return nf


def f11_diamond(nf):
    sky(lo=(1.0, 0.62, 0.35), hi=(0.38, 0.40, 0.66), strength=1.0)
    sun(4, 0, 3.5, (1.0, 0.60, 0.32))
    W.box((0, 608, -0.06), (6000, 1200, 0.1), W.mat("lake", (0.40, 0.48, 0.62), 0.15), bevel=0)
    C.grass_ground(col=(0.30, 0.38, 0.16), size=40, tufts=1500, area=(-6, 6, -6, 2))
    foothills(seed=12, y=(1100, 1500), x=(-1600, 1600), n=10, col=(0.22, 0.24, 0.32), h=(60, 160), gap=(-350, 350))
    sd = W.mat("sun_disc2", (1, 0.8, 0.5), emit=(1.0, 0.75, 0.40), emit_strength=25)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=45, location=(0, 1900, 260))
    s = bpy.context.object
    s.data.materials.append(sd)
    s.visible_shadow = False
    s.keyframe_insert("location", frame=1)
    s.location.z = -30
    s.keyframe_insert("location", frame=nf)
    blk = W.mat("tripod", (0.08, 0.08, 0.08), 0.5)
    TX, TY = -0.4, 1.4
    legs = []
    for k in range(3):
        a = k * 2 * math.pi / 3
        bpy.ops.object.empty_add(location=(TX, TY, 1.35))
        lg = bpy.context.object
        c = F._cyl(0.015, 0.015, 1.4, (0, 0, -0.7), blk)
        c.parent = lg
        lg.rotation_euler = (0, 0, a)
        legs.append(lg)
    W.box((TX, TY, 1.45), (0.18, 0.12, 0.12), blk, bevel=0.01)
    for lg in legs:
        lg.rotation_euler.x = math.radians(22)
        lg.keyframe_insert("rotation_euler", frame=70)
        lg.rotation_euler.x = math.radians(3)
        lg.keyframe_insert("rotation_euler", frame=100)
    person((-1.0, 0.8, 0), 30, seed=10, arms="hold", hat="cap")
    W.camera((-1.9, -2.0, 1.55), (0.6, 12, 1.5), lens=26)
    cut(68, (-1.3, -0.4, 1.35), (-0.5, 1.3, 1.15), lens=30, orbit=12)
    return nf


def ichifuji_texture():
    from PIL import Image, ImageDraw
    p = os.path.join(ASSETS, "ichifuji.png")
    if os.path.exists(p):
        return p
    os.makedirs(ASSETS, exist_ok=True)
    w, h = 1024, 640
    im = Image.new("RGB", (w, h), (250, 240, 215))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, h * 0.55), fill=(240, 120, 70))
    d.ellipse((780, 60, 900, 180), fill=(255, 225, 120))
    d.polygon([(40, 420), (250, 140), (330, 140), (500, 420)], fill=(60, 80, 140))
    d.polygon([(190, 220), (250, 140), (330, 140), (380, 220), (330, 200), (290, 230), (240, 200)], fill=(250, 250, 252))
    d.polygon([(560, 260), (690, 200), (760, 240), (690, 260), (720, 330)], fill=(110, 70, 40))
    d.ellipse((620, 420, 760, 560), fill=(90, 40, 110))
    d.rectangle((675, 390, 705, 430), fill=(60, 120, 50))
    d.line((512, 0, 512, h), fill=(200, 160, 120), width=6)
    im.save(p)
    return p


def bill_texture():
    from PIL import Image, ImageDraw
    p = os.path.join(ASSETS, "bill.png")
    if os.path.exists(p):
        return p
    os.makedirs(ASSETS, exist_ok=True)
    im = Image.new("RGB", (640, 300), (200, 220, 230))
    d = ImageDraw.Draw(im)
    d.rectangle((14, 14, 626, 286), outline=(90, 110, 140), width=6)
    for k in range(5):
        d.arc((60 + k * 40, 120 - k * 10, 300 + k * 40, 330), 200, 330, fill=(40, 70, 130), width=10)
    d.polygon([(380, 230), (450, 140), (480, 140), (550, 230)], fill=(70, 90, 140))
    d.polygon([(430, 165), (450, 140), (480, 140), (500, 165)], fill=(250, 250, 252))
    im.save(p)
    return p


def f12_kid(nf):
    C.book_texture = ichifuji_texture
    C.c10_book(nf)
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[1].default_value *= SKY_K
    window_sun(elev=25, az=150, strength=2.6)
    W.box((-0.9, 0.5, 0.18), (0.36, 0.36, 0.36), W.mat("teapot_box", (0.30, 0.20, 0.14), 0.5), bevel=0.03)
    F._cyl(0.035, 0.03, 0.08, (0.32, 0.25, 0.4), W.mat("yunomi", (0.80, 0.78, 0.70), 0.3), verts=12)
    F._ball(0.05, (-0.25, 0.2, 0.39), W.mat("mikan", (0.98, 0.55, 0.10), 0.5), sub=2)
    F._ball(0.05, (-0.15, 0.28, 0.39), W.mat("mikan", (0.98, 0.55, 0.10), 0.5), sub=2)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0.42, 0.55, 0.37))
    b = bpy.context.object
    b.scale = (0.16, 0.075, 1)
    b.rotation_euler.z = math.radians(-20)
    b.data.materials.append(C.img_mat("bill", bill_texture()))
    cut(90, (0.3, -0.35, 1.05), (0.25, 0.45, 0.36), lens=30, orbit=12)
    return nf


def river_set(level0, level1, nf, fish=True):
    gm = W.mat("grass_bank", (0.30, 0.44, 0.15), 1.0)
    for sx in (-1, 1):
        W.box((sx * 152.3, 15, -0.05), (300, 400, 0.1), gm, bevel=0)
    C.grass_tufts(3000, (-6, 6, -4, 14), (0.30, 0.44, 0.15), avoid=[(-2.4, 2.4, -10, 40)])
    bank = W.mat("bank", (0.40, 0.36, 0.28), 1.0)
    for sx in (-1, 1):
        W.box((sx * 2.6, 15, -0.3), (0.9, 50, 0.9), bank, rot=(0, math.radians(sx * 30), 0), bevel=0)
    W.box((0, 15, -0.9), (5, 50, 0.4), W.mat("gravel_bed", (0.55, 0.50, 0.42), 1.0), bevel=0)
    r = random.Random(6)
    C.multi_ball([(r.uniform(-1.8, 1.8), r.uniform(-2, 30), -0.7, r.uniform(0.2, 0.45), (1.2, 1, 0.6)) for _ in range(60)],
                 W.mat("rock_river", (0.50, 0.50, 0.50), 0.9), "river_rocks")
    wm = W.mat("water_clear", (0.30, 0.62, 0.70), 0.03, alpha=0.75)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 15, level0))
    wt = bpy.context.object
    wt.scale = (4.6, 50, 1)
    wt.data.materials.append(wm)
    wt.keyframe_insert("location", frame=1)
    wt.location.z = level1
    wt.keyframe_insert("location", frame=nf)
    green = W.mat("waterweed", (0.20, 0.45, 0.20), 0.8)
    C.multi_box([(r.uniform(-1.6, 1.6), r.uniform(0, 20), -0.55, 0.05, 0.5, 0.35, r.uniform(-0.3, 0.3)) for _ in range(40)],
                green, "weeds")
    if fish:
        fm = W.mat("fish", (0.45, 0.48, 0.45), 0.5)
        for k in range(8):
            o = F._ball(0.08, (0, 0, 0), fm, sub=1, sc=(0.6, 1.8, 0.6))
            x0, y0 = r.uniform(-1.2, 1.2), r.uniform(1, 8)
            for f in range(1, nf + 1, 3):
                o.location = (x0 + 0.2 * math.sin(f / 9 + k), y0 + 0.4 * math.sin(f / 13 + k), -0.45)
                o.keyframe_insert("location", frame=f)
    for i in range(6):
        C.tree((r.choice((-1, 1)) * r.uniform(4, 9), r.uniform(3, 30), 0), h=r.uniform(5, 8), seed=30 + i)


def heron(loc, facing, nf=0):
    """川に立つシラサギ（首をのばして、ときどき水をつつく）。"""
    wm = W.mat("heron", (0.97, 0.97, 0.95), 0.6)
    ym = W.mat("heron_beak", (0.95, 0.75, 0.15), 0.5)
    km = W.mat("heron_leg", (0.10, 0.10, 0.10), 0.6)
    bpy.ops.object.empty_add(location=loc)
    root = bpy.context.object
    root.rotation_euler.z = math.radians(-facing)
    parts = [F._ball(0.16, (0, 0, 0.62), wm, sub=2, sc=(0.8, 1.5, 0.8))]
    for dx in (-0.04, 0.04):
        parts.append(F._cyl(0.01, 0.01, 0.55, (dx, 0, 0.28), km, verts=5))
    bpy.ops.object.empty_add(location=(0, 0.18, 0.7))
    neck = bpy.context.object
    for h in (F._cyl(0.03, 0.03, 0.4, (0, 0.05, 0.2), wm, rot=(math.radians(-15), 0, 0), verts=6),
              F._ball(0.06, (0, 0.1, 0.42), wm, sub=2, sc=(0.8, 1.3, 0.8)),
              F._cyl(0.015, 0.0, 0.16, (0, 0.24, 0.41), ym, rot=(math.radians(-90), 0, 0), verts=6)):
        h.parent = neck
    for p in parts + [neck]:
        p.parent = root
    for f in range(1, nf + 1, 6):
        neck.rotation_euler.x = math.radians(-70 if (f // 36) % 3 == 1 else 0)
        neck.keyframe_insert("rotation_euler", frame=f)
    return root


def f13_lowwater(nf):
    day(elev=40, az=-30, strength=4.6)
    river_set(-0.1, -0.5, nf)
    C.multi_ball([(0.3, 6.0, -0.65, 0.32, (1.3, 1.0, 0.8))], W.mat("rock_river", (0.50, 0.50, 0.50), 0.9), "heron_rock")
    heron((0.3, 6.0, -0.42), 200, nf)
    # 川をのぞきこむ、地元のおじいさん（柵と看板）
    person((2.9, 4.2, 0), 250, seed=4, arms="hold", look=GRANDPA)
    rail = W.mat("rail_wood", (0.50, 0.38, 0.25), 0.8)
    for k in range(6):
        W.box((2.4, -1 + k * 2.0, 0.45), (0.1, 0.1, 0.9), rail, bevel=0)
    W.box((2.4, 4, 0.85), (0.08, 12, 0.08), rail, bevel=0)
    W.box((3.4, 6.0, 1.2), (0.06, 0.9, 0.6), W.mat("sign_board", (0.95, 0.93, 0.85), 0.8), bevel=0.01)
    W.box((3.4, 6.0, 0.5), (0.06, 0.06, 1.0), rail, bevel=0)
    # 水面すれすれから：手前の石と水草がボケて、奥のサギとおじいさん
    W.camera((1.5, -1.0, 0.25), (1.8, 6.0, -0.1), lens=30)
    cut(76, (1.4, 1.0, 0.15), (-0.2, 12, -0.4), lens=26, orbit=8)
    return nf


def trout_set(nf, level0, level1, worker_arms, alt=None, jump=False):
    day(elev=45, az=-30, strength=4.6)
    C.grass_ground(col=(0.32, 0.44, 0.15), tufts=2000, area=(-6, 6, -4, 1.5))
    conc = W.mat("concrete", (0.70, 0.70, 0.68), 0.9)
    for k in range(3):
        y = 2 + k * 3.4
        W.box((0, y - 1.5, 0.3), (8, 0.2, 0.6), conc, bevel=0)
        W.box((0, y + 1.5, 0.3), (8, 0.2, 0.6), conc, bevel=0)
        W.box((0, y, 0.03), (8, 3.2, 0.06), W.mat("pond_floor", (0.40, 0.45, 0.42), 0.9), bevel=0)
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y, level0))
        wt = bpy.context.object
        wt.scale = (7.8, 2.9, 1)
        wt.data.materials.append(W.mat("water_pond", (0.30, 0.55, 0.62), 0.03, alpha=0.8))
        wt.keyframe_insert("location", frame=1)
        wt.location.z = level1
        wt.keyframe_insert("location", frame=nf)
        r = random.Random(k)
        C.multi_ball([(r.uniform(-3.5, 3.5), y + r.uniform(-1.2, 1.2), 0.14, 0.06, (0.6, 1.8, 0.6)) for _ in range(40)],
                     W.mat("fish", (0.45, 0.48, 0.45), 0.5), f"trout{k}")
    W.box((-4.2, 2, 0.35), (0.12, 4 * 3.4, 0.7), conc, bevel=0)
    pipe = W.mat("pipe", (0.30, 0.45, 0.60), 0.4)
    F._cyl(0.08, 0.08, 0.6, (-3.6, 2, 0.75), pipe, rot=(0, math.radians(90), 0))
    if jump:
        fo = F._ball(0.12, (0, 0, 0), W.mat("fish", (0.45, 0.48, 0.45), 0.5), sub=1, sc=(0.6, 1.8, 0.6))
        for f in range(1, nf + 1, 2):
            u = ((f - 8) % 30) / 30
            fo.location = (0.6, 1.6 + u * 0.8, 0.5 + 1.0 * 4 * u * (1 - u))
            fo.rotation_euler.x = math.radians(-60 + 120 * u)
            fo.keyframe_insert("location", frame=f)
            fo.keyframe_insert("rotation_euler", frame=f)
    foothills(seed=3, y=(800, 1300), n=8, col=(0.30, 0.42, 0.34), h=(40, 90), gap=(-500, 500))
    person((0.3, -0.7, 0), 200, seed=11, arms=worker_arms, alt=alt, nf=nf, period=8, look=TROUT, hat="cap")
    # 養殖場の小物（青いバケツ、たも網、ホース、えさの袋）
    bucket = W.mat("bucket_blue", (0.15, 0.40, 0.75), 0.5)
    for k in range(3):
        F._cyl(0.17, 0.14, 0.32, (-1.6 + k * 0.45, -1.4, 0.16), bucket, verts=14)
    F._cyl(0.015, 0.015, 1.8, (1.6, -0.9, 0.9), W.mat("net_pole", (0.75, 0.70, 0.55), 0.6), rot=(math.radians(25), 0, 0))
    F._ball(0.2, (1.6, -0.5, 1.75), W.mat("net", (0.15, 0.30, 0.20), 0.9), sub=1, sc=(1, 1, 0.5))
    W.box((-2.6, -1.2, 0.2), (0.5, 0.35, 0.4), W.mat("feed_bag", (0.85, 0.80, 0.65), 0.9), bevel=0.05)
    W.box((-3.1, -1.1, 0.2), (0.5, 0.35, 0.4), W.mat("feed_bag", (0.85, 0.80, 0.65), 0.9), bevel=0.05)


def f14_trout(nf):
    trout_set(nf, 0.55, 0.2, "head")
    W.camera((-1.0, -3.7, 1.6), (0.3, 0.6, 0.7), lens=26)
    return nf


def factory_set(nf, running, workers):
    day(elev=40, az=150, strength=4.6)
    C.grass_ground(col=(0.42, 0.42, 0.42), name="asphalt")
    wall = W.mat("factory", (0.78, 0.80, 0.82), 0.8)
    W.box((0, 14, 5), (30, 12, 10), wall, bevel=0.1)
    W.box((0, 14, 10.4), (30.5, 12.5, 0.8), W.mat("factory_roof", (0.35, 0.45, 0.55), 0.7), bevel=0.1)
    for k in range(6):
        W.box((-12 + k * 4.8, 7.98, 6.5), (3.0, 0.05, 1.8), W.mat("win_day", (0.25, 0.32, 0.40)), bevel=0)
    stack = W.mat("chimney", (0.85, 0.82, 0.78), 0.8)
    for x in (-8, 6):
        F._cyl(1.2, 1.0, 26, (x, 18, 13), stack, verts=12)
        W.box((x, 18, 24), (2.3, 2.3, 1.2), W.mat("chimney_red", (0.8, 0.2, 0.15), 0.7), bevel=0)
        if running:
            F.puffs([(x, 18, 26.5, 0.0, 0)], [C.sec(f) for f in range(1, nf + 1)], seed=x + 20, col=(0.95, 0.95, 0.95),
                    alpha=0.35, size=(1.5, 3.0), rise=(2, 4), grow=2.5, life=3.0, name=f"steam{x}")
    white = W.mat("roll", (0.97, 0.97, 0.95), 0.8)
    core = W.mat("roll_core", (0.70, 0.55, 0.35), 0.8)
    r = random.Random(3)
    rolls = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                rolls.append((-4.5 + i * 0.5 + 0.0, 3.0 + j * 0.5, 0.25 + k * 0.5))
    for (x, y, z) in rolls:
        F._cyl(0.22, 0.22, 0.45, (x, y, z), white, verts=12)
    # パレットに積んだ紙、フォークリフト、トラック
    pal = W.mat("pallet", (0.70, 0.55, 0.35), 0.8)
    for k in range(3):
        W.box((-7 + k * 1.4, 4.5, 0.08), (1.2, 1.2, 0.16), pal, bevel=0)
        W.box((-7 + k * 1.4, 4.5, 0.6), (1.1, 1.1, 0.9), white, bevel=0.02)
    W.box((6.5, 2.0, 0.7), (1.2, 2.0, 1.0), W.mat("forklift", (0.95, 0.70, 0.10), 0.5), bevel=0.05)
    W.box((6.5, 1.4, 1.9), (1.1, 0.9, 0.08), W.mat("forklift_roof", (0.15, 0.15, 0.15), 0.6), bevel=0)
    for dx in (-0.5, 0.5):
        F._cyl(0.04, 0.04, 1.4, (6.5 + dx, 1.0, 1.2), W.mat("forklift_roof", (0.15, 0.15, 0.15), 0.6), verts=6)
    W.box((-10, 9.0, 1.6), (2.4, 6.5, 2.6), W.mat("truck_box", (0.85, 0.86, 0.88), 0.6), bevel=0.05)
    W.box((-10, 5.0, 1.2), (2.3, 1.6, 1.8), W.mat("truck_cab", (0.20, 0.40, 0.70), 0.4), bevel=0.08)
    big = F._cyl(1.2, 1.2, 3.0, (3.5, 5.0, 1.3), white, rot=(0, math.radians(90), 0), verts=24)
    bpy.ops.object.empty_add(location=(3.5, 5.0, 1.3))
    piv = bpy.context.object
    big.location = (0, 0, 0)
    big.parent = piv
    F._cyl(0.25, 0.25, 3.1, (0, 0, 0), core, rot=(0, math.radians(90), 0), verts=12).parent = piv
    W.box((3.5, 5.0, 0.05), (3.4, 2.8, 0.1), W.mat("machine", (0.35, 0.45, 0.55), 0.5), bevel=0)
    spins = (6.0 if running else 0.0)
    for f in range(1, nf + 1, 3):
        piv.rotation_euler.x = spins * f / FPS if running else max(0.0, 2.0 * (1 - f / 40)) * f / FPS
        piv.keyframe_insert("rotation_euler", frame=f)
    for k, (x, fac, arms, alt) in enumerate(workers):
        person((x, 1.5 - 0.3 * k, 0), fac, seed=12 + k, arms=arms, alt=alt, nf=nf, period=8, look=WORKER, hat="white")


def f15_paper(nf):
    factory_set(nf, False, [(0.6, 150, "head", None), (-1.2, 200, ("down", "head"), None)])
    W.camera((-1.2, -2.0, 1.55), (0.2, 1.4, 1.55), lens=30)
    cut(46, (-2.8, -5.5, 2.0), (0.4, 4.0, 3.0), lens=24)
    return nf


def kitchen_set(nf, strong, mom_arms, alt=None):
    room((0.95, 0.9, 0.82), 0.22)
    window_sun(elev=35, az=150, strength=3.0)
    W.box((0, 0, -0.05), (6, 6, 0.1), W.mat("floor_wood", (0.60, 0.45, 0.30), 0.6), bevel=0)
    W.box((0, 1.6, 1.4), (6, 0.1, 2.8), W.mat("kitchen_wall", (0.92, 0.90, 0.85), 0.9), bevel=0)
    W.box((0, 1.25, 0.43), (2.4, 0.6, 0.86), W.mat("cabinet", (0.85, 0.82, 0.76), 0.6), bevel=0.01)
    W.box((0, 1.25, 0.88), (2.4, 0.62, 0.04), W.mat("counter", (0.75, 0.76, 0.78), 0.2), bevel=0.005)
    W.box((0.2, 1.25, 0.84), (0.7, 0.45, 0.06), W.mat("sink", (0.55, 0.56, 0.58), 0.15), bevel=0)
    steel = W.mat("faucet", (0.8, 0.8, 0.82), 0.2)
    F._cyl(0.025, 0.025, 0.35, (0.2, 1.5, 1.07), steel)
    F._cyl(0.02, 0.02, 0.22, (0.2, 1.4, 1.24), steel, rot=(math.radians(90), 0, 0))
    wm = W.mat("tapwater", (0.75, 0.88, 0.95), 0.05, emit=(0.6, 0.8, 0.95), emit_strength=0.6)
    rad = 0.016 if strong else 0.0025
    s = F._cyl(rad, rad * 0.9, 0.32, (0.2, 1.3, 1.07), wm, verts=8)
    for f in range(1, nf + 1, 2):
        k = 1.0 + (0.25 * math.sin(f * 1.7) if strong else (0.0 if (f // 6) % 3 else -0.9))
        s.scale = (max(k, 0.05), max(k, 0.05), 1)
        s.keyframe_insert("scale", frame=f)
    glass = W.mat("cup", (0.85, 0.92, 0.95), 0.05, alpha=0.6)
    F._cyl(0.045, 0.04, 0.12, (0.2, 1.3, 0.93), glass, verts=14)
    if strong:
        F.puffs([(0.2, 1.3, 0.95, 0.0, 0)], [C.sec(f) for f in range(1, nf + 1)], seed=4, col=(0.85, 0.93, 1.0), alpha=0.35,
                size=(0.02, 0.05), rise=(0.1, 0.3), grow=1.5, life=0.6, name="splash")
    bpy.ops.object.light_add(type='AREA', location=(0, 0.5, 2.6))
    a = bpy.context.object
    a.data.energy = 80
    a.data.size = 2.5
    person((-0.35, 0.6, 0), 70, seed=9, arms=mom_arms, alt=alt, nf=nf, period=8, look=MOM)
    # 台所の小物（冷蔵庫、食器だな、炊飯器、カレンダー、まな板）
    W.box((-1.8, 1.2, 0.9), (0.7, 0.7, 1.8), W.mat("fridge", (0.92, 0.92, 0.90), 0.3), bevel=0.03)
    W.box((-1.47, 1.2, 1.3), (0.03, 0.05, 0.4), W.mat("handle", (0.6, 0.6, 0.6), 0.3), bevel=0)
    W.box((0.0, 1.45, 1.9), (2.4, 0.3, 0.6), W.mat("cupboard", (0.80, 0.66, 0.48), 0.6), bevel=0.01)
    for k in range(5):
        F._cyl(0.09, 0.09, 0.02, (-0.8 + k * 0.4, 1.3, 1.58), W.mat("plate", (0.95, 0.95, 0.92), 0.3), verts=14)
    F._ball(0.15, (-0.85, 1.25, 1.03), W.mat("ricecooker", (0.95, 0.95, 0.93), 0.3), sub=2, sc=(1, 1, 0.8))
    W.box((0.85, 1.25, 0.915), (0.4, 0.28, 0.03), W.mat("cuttingboard", (0.85, 0.72, 0.50), 0.6), bevel=0.005)
    F._ball(0.06, (0.85, 1.25, 0.96), W.mat("tomato", (0.85, 0.15, 0.10), 0.4), sub=2)
    W.box((1.6, 1.54, 1.7), (0.4, 0.02, 0.55), W.mat("calendar", (0.97, 0.96, 0.92), 0.8), bevel=0)
    W.box((1.6, 1.53, 1.88), (0.4, 0.02, 0.14), W.mat("calendar_top", (0.85, 0.25, 0.20), 0.8), bevel=0)


def f16_tap(nf):
    kitchen_set(nf, False, "hold")
    W.camera((2.2, -0.3, 1.6), (-0.1, 0.9, 1.1), lens=24)
    return nf


def f17_return(nf):
    morning()
    engawa_set()
    person((0.3, 0.8, 0.45), 0, seed=4, arms="down", look=GRANDPA)
    person((-0.5, 0.75, 0.45), 15, seed=1, scale=0.68, look=KID)
    fj = fuji(FUJI_LOC, FUJI_R)
    f_back = 61 + 8
    fuji_appear(fj, f_back)
    kasa = cap_cloud((FUJI_LOC[0], FUJI_LOC[1], FUJI_H * FUJI_R + 8), FUJI_R)
    grow(kasa, f_back + 30, f_back + 90)
    engawa_cam(nf, push=0.8)
    cut(131, (-0.4, -2.1, 1.5), (FUJI_LOC[0], FUJI_LOC[1], FUJI_H * FUJI_R * 0.7), lens=50, orbit=10, push=0.0, piv=3,
        fixat=1, focus="far", zoom=1.15)
    return nf


def j1_home(nf):
    morning()
    engawa_set()
    person((0.3, 0.8, 0.45), 345, seed=4, arms="pray", look=GRANDPA)
    person((-0.5, 0.75, 0.45), 15, seed=1, scale=0.68, arms="up", alt="down", nf=nf, period=8, look=KID)
    W.camera((-0.2, 4.2, 1.35), (-0.1, 0.6, 1.2), lens=30)
    return nf


def j2_trout(nf):
    trout_set(nf, 0.55, 0.55, "up", alt="down", jump=True)
    W.camera((-1.8, -3.3, 1.8), (0.6, 1.0, 0.6), lens=26)
    return nf


def j3_paper(nf):
    factory_set(nf, True, [(0.6, 180, ("down", "wave"), "up"), (-1.2, 170, "up", "down")])
    W.camera((-1.8, -3.6, 1.6), (0.0, 3.0, 2.6), lens=24)
    return nf


def j4_tap(nf):
    kitchen_set(nf, True, "up", alt="down")
    W.camera((2.2, -0.3, 1.6), (-0.1, 0.9, 1.1), lens=24)
    return nf


def j5_wide(nf):
    morning()
    C.grass_ground(col=(0.30, 0.42, 0.14), tufts=4500, area=(-6, 6, -3, 12))
    town(seed=2, y=(40, 500), n=120)
    foothills(seed=3, y=(700, 1200), n=10, col=(0.30, 0.42, 0.34), h=(40, 90))
    fj = fuji(FUJI_LOC, FUJI_R)
    kasa = cap_cloud((FUJI_LOC[0], FUJI_LOC[1], FUJI_H * FUJI_R + 8), FUJI_R)
    cast = [(-1.6, 4, "pray", None, GRANDPA, None, 1.0), (-1.0, 1, "up", "down", KID, None, 0.68),
            (-0.2, 11, "up", "down", TROUT, "cap", 1.0), (0.6, 12, "wave", "up", WORKER, "white", 1.0),
            (1.3, 13, "up", "down", WORKER, "white", 1.0), (2.0, 9, "pray", None, MOM, None, 1.0)]
    for k, (x, seed, a, alt, lk, hat, sc) in enumerate(cast):
        person((x, 1.5 + 0.2 * (k % 2), 0), 0, seed=seed, arms=a, alt=alt, nf=nf, period=8 + k, look=lk, hat=hat, scale=sc)
    utility_poles([(-22, 16), (-6, 16), (10, 16), (26, 16)])
    cat((2.8, 1.2, 0), 120)
    cam = W.camera((0.2, -3.0, 2.1), (0.2, 40, 10.5), lens=26)
    cam.keyframe_insert("location", frame=1)
    cam.location = (0.2, -6.5, 1.9)
    cam.keyframe_insert("location", frame=nf)
    cam["keep"] = 1
    return nf


def render(out, nf, step=1, first=None, last=None):
    os.makedirs(out, exist_ok=True)
    sc = bpy.context.scene
    W.render_setup(os.path.join(out, "f_####.png"), 1, nf, res=C.RES, samples=8)
    sc.view_settings.look = 'AgX - Punchy'
    sc.view_settings.exposure = C.EXPOSURE + 0.1
    move_cams(nf)
    cs = cams()
    for f in range((first or 1), (last or nf) + 1, step):
        sc.camera = [c for c in cs if c["f0"] <= f][-1]
        sc.frame_set(f)
        sc.render.filepath = os.path.join(out, f"f_{f:04d}.png")
        if not os.path.exists(sc.render.filepath):
            bpy.ops.render.render(write_still=True)


SCENES = {k: v for k, v in globals().items() if callable(v) and k[:1] in "fj" and k[1:2].isdigit() and "_" in k}

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
