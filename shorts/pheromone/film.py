"""「もしも男女がフェロモンを出すようになったら？」全場面の3D（Blender / bpy）。スギ・スズメ版（富士山版）の部品を使う。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]
座標: z=上（m）。カメラはおおむね -y から +y を見る。フェロモンは目に見えないので、ピンクのけむりで見せる。"""
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
cut, sky, sun, fill = FJ.cut, FJ.sky, FJ.sun, SG.fill
sys.path.insert(0, os.path.join(HERE, "..", "voxel"))
import people as VP  # noqa: E402

VP.install(FJ)          # 人は参考元のようなブロック体（四角い頭・ドットの顔）

PINK = (1.0, 0.40, 0.66)


def L(base, **kw):
    d = dict(base)
    d.update(kw)
    return d


KACHO = {"hair": (0.42, 0.42, 0.42), "top": (0.12, 0.15, 0.26), "bottom": (0.12, 0.15, 0.26), "glasses": True}    # 課長 52歳
WIFE = {"hair": (0.30, 0.24, 0.20), "top": (0.80, 0.55, 0.42), "bottom": (0.42, 0.36, 0.40), "long": True}
SCIENTIST = {"hair": (0.12, 0.10, 0.09), "top": (0.93, 0.93, 0.90), "bottom": (0.25, 0.24, 0.24), "glasses": True}
CLERK = {"hair": (0.10, 0.07, 0.05), "top": (0.20, 0.22, 0.34), "bottom": (0.20, 0.22, 0.34), "long": True}
TOPS = [(0.85, 0.85, 0.82), (0.20, 0.22, 0.30), (0.75, 0.35, 0.35), (0.35, 0.55, 0.75), (0.90, 0.75, 0.35), (0.30, 0.30, 0.32),
        (0.55, 0.70, 0.45), (0.85, 0.55, 0.65), (0.45, 0.35, 0.60), (0.95, 0.95, 0.95)]
BOTTOMS = [(0.18, 0.20, 0.28), (0.25, 0.25, 0.27), (0.40, 0.36, 0.30), (0.15, 0.15, 0.16), (0.30, 0.35, 0.50)]
HAIRS = [(0.06, 0.045, 0.035), (0.12, 0.08, 0.05), (0.25, 0.17, 0.10), (0.45, 0.45, 0.45), (0.06, 0.045, 0.035)]


def crowd_look(r, face="neutral"):
    return {"top": r.choice(TOPS), "bottom": r.choice(BOTTOMS), "hair": r.choice(HAIRS), "long": r.random() < 0.45, "face": face}


def person(loc, facing, pose="stand", **kw):
    root = SG.person(loc, facing, pose=pose, **kw)
    root["hc0"] = VP.HC_SIT if pose == "sit" else VP.HC_STAND
    return root


def smooth(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


# ---------- 歩く人（足を交互に出す。止まると立ち姿に） ----------
def _body(seed, pose, arms, look, parent):
    b = bpy.data.objects.new(f"b{seed}_{pose}", FJ.person_mesh(seed % 12, pose, arms, look))
    bpy.context.collection.objects.link(b)
    b.parent = parent
    return b


def actor(seed, look, way, nf, arms="down", alt=None, period=7, alt_period=16, face_at=None, bob=0.025):
    """way = [(コマ, x, y)] か [(コマ, x, y, 向き)]。点の間は歩き、同じ場所なら立つ。向きは進む方向（止まると4番目の値）。
    face_at = (コマ, 表情)：そのコマから立ち姿の表情を変える。"""
    root = bpy.data.objects.new(f"actor{seed}", None)
    bpy.context.collection.objects.link(root)
    w1, w2 = _body(seed, "walk1", "down", look, root), _body(seed, "walk2", "down", look, root)
    st = [_body(seed, "stand", arms, look, root)] + ([_body(seed, "stand", alt, look, root)] if alt else [])
    st2 = None
    if face_at:
        lk2 = L(look, face=face_at[1])
        arms2 = face_at[2] if len(face_at) > 2 else arms
        st2 = [_body(seed, "stand", arms2, lk2, root)] + ([_body(seed, "stand", alt, lk2, root)] if alt else [])
    allb = [w1, w2] + st + (st2 or [])

    def pos(f):
        if f <= way[0][0]:
            return Vector((way[0][1], way[0][2], 0))
        for a, b in zip(way, way[1:]):
            if a[0] <= f <= b[0]:
                u = (f - a[0]) / max(1, b[0] - a[0])
                return Vector((a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u, 0))
        return Vector((way[-1][1], way[-1][2], 0))

    def face_dir(f):
        for a, b in zip(way, way[1:]):
            if a[0] <= f <= b[0] and len(b) > 3 and abs(b[1] - a[1]) + abs(b[2] - a[2]) < 1e-6:
                return b[3]
        if f >= way[-1][0] and len(way[-1]) > 3:
            return way[-1][3]
        if f <= way[0][0] and len(way[0]) > 3:
            return way[0][3]
        return None
    head = None
    last_vis = None
    for f in range(1, nf + 1):
        p0, p1 = pos(f - 1), pos(f + 1)
        v = p1 - p0
        moving = v.length > 0.012
        want = math.degrees(math.atan2(v.x, v.y)) if moving else face_dir(f)
        if want is None:
            want = head if head is not None else 0.0
        if head is None:
            head = want
        d = (want - head + 180) % 360 - 180
        head += max(-14.0, min(14.0, d))
        p = pos(f)
        if moving:
            p.z += bob * abs(math.sin(math.pi * f / period))
        root.location = p
        root.rotation_euler.z = math.radians(-head)
        if f % 2 == 1 or f == nf:
            root.keyframe_insert("location", frame=f)
            root.keyframe_insert("rotation_euler", frame=f)
        if moving:
            vis = w1 if (f // period) % 2 == 0 else w2
        else:
            group = st2 if (st2 and f >= face_at[0]) else st
            vis = group[(f // alt_period) % len(group)] if alt else group[0]
        if vis is not last_vis:
            for b in allb:
                b.scale = (1.0,) * 3 if b is vis else (1e-4,) * 3
                b.keyframe_insert("scale", frame=f)
            last_vis = vis
    for b in allb:
        FJ.set_interp(b, 'CONSTANT')
    return root


# ---------- フェロモン（ピンクのけむりと光の粒） ----------
def pink_mat(alpha=0.30, col=PINK, name="phero", glow=0.35):
    key = f"{name}_{alpha}_{col}_{glow}"
    new = bpy.data.materials.get(key) is None
    m = F.puff_mat(key, col, alpha)
    if new and glow:
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Emission Color"].default_value = (*col, 1)
        b.inputs["Emission Strength"].default_value = glow
    return m


def pink_particles():
    """光の粒をピンクと白に（消える演出の金色の代わり）。"""
    key = ("cubes", False)
    if key in FJ._PM and FJ._PM.get("pink_set"):
        return
    _gold, white = FJ.particle_meshes(False)
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    tmp = bpy.context.object
    tmp.data.materials.append(W.mat("cube_pink", (1.0, 0.5, 0.75), emit=(1.0, 0.35, 0.65), emit_strength=4.0))
    tmp.data.use_fake_user = True
    pk = tmp.data
    bpy.data.objects.remove(tmp)
    FJ._PM[key] = [pk, white]
    FJ._PM["pink_set"] = True


def pink_burst(points, f0, size=0.05, rise=1.2, seed=1, spread=0.8, center=None):
    pink_particles()
    FJ.sparkle_points([Vector(p) for p in points], f0, size, rise, mode="out", seed=seed, center=center, burst=spread,
                      gold_ratio=0.75, life=(0.6, 1.3))


def puff_objs(births, nf, fn, mat, name="pf", every=3):
    """births = [生まれるコマ]。fn(k, f0, f) → (位置, 大きさ) か None（見えない）。"""
    me = SG.ico_mesh()
    out = []
    for k, f0 in enumerate(births):
        o = bpy.data.objects.new(f"{name}{k}", me)
        bpy.context.collection.objects.link(o)
        o.material_slots[0].link = 'OBJECT'
        o.material_slots[0].material = mat
        o.visible_shadow = False
        fs = sorted(set([max(1, f0 - 1)] + list(range(max(1, f0), nf + 1, every)) + [nf]))
        for f in fs:
            res = fn(k, f0, f) if f >= f0 else None
            if res is None:
                o.scale = (1e-4,) * 3
            else:
                loc, s = res
                o.location = loc
                o.scale = (max(s[0], 1e-4), max(s[1], 1e-4), max(s[2], 1e-4)) if isinstance(s, tuple) else (max(s, 1e-4),) * 3
                o.keyframe_insert("location", frame=f)
            o.keyframe_insert("scale", frame=f)
        out.append(o)
    return out


def body_plume(src, f_from, f_to, nf, every=4, rise=0.35, size=(0.10, 0.18), grow=2.4, life=75, mat=None, seed=1, swirl=0.25,
               drift=(0.0, 0.0), spread=0.22, name="plume", z_lo=0.4, z_hi=1.5):
    """人の体からわき上がって、頭の上へのぼるピンクのけむり（体温の上昇気流）。src = (x, y) か 関数 f → (x, y)。"""
    r = random.Random(seed)
    mat = mat or pink_mat(0.26)
    births = list(range(f_from, f_to, every))
    par = [(r.uniform(-spread, spread), r.uniform(-spread * 0.6, spread * 0.6), r.uniform(z_lo, z_hi), r.uniform(*size),
            r.uniform(0, 6.3), r.uniform(0.8, 1.2)) for _ in births]

    def fn(k, f0, f):
        dx, dy, z0, s0, ph, sp = par[k]
        t = (f - f0) / FPS
        if f - f0 > life:
            return None
        sx, sy = src(f0) if callable(src) else src
        z = z0 + rise * sp * t + 0.5 * 0.12 * t * t
        w = swirl * min(1.0, max(0.0, z - 1.5)) * math.sin(2.2 * t + ph)
        loc = (sx + dx * (1 + 0.6 * t) + w + drift[0] * t, sy + dy * (1 + 0.6 * t) + w * 0.6 + drift[1] * t, z)
        fade = 1.0 - ((f - f0) / life) ** 3
        s = s0 * (0.5 + grow * (1 - math.exp(-t * 0.9))) * fade
        return loc, s
    return puff_objs(births, nf, fn, mat, name)


# ---------- ガ ----------
_MOTH = {}


def _wing(pts, m, sx, ang, k, name="wing"):
    """平らな羽（2Dの多角形）。sx=±1 で左右、ang だけ持ち上げる。"""
    verts = [(sx * x * k, y * k, 0.0) for x, y in pts]
    me = bpy.data.meshes.new(name)
    face = list(range(len(verts))) if sx > 0 else list(range(len(verts)))[::-1]
    me.from_pydata(verts, [], [face])
    me.materials.append(m)
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.rotation_euler = (0, math.radians(-sx * ang), 0)
    o.location = (0, 0, 0.004 * k)
    return o


FORE = [(0.006, 0.014), (0.040, 0.034), (0.074, 0.030), (0.078, 0.012), (0.050, -0.004), (0.012, -0.010)]
HIND = [(0.006, -0.006), (0.040, -0.006), (0.058, -0.020), (0.050, -0.042), (0.024, -0.046), (0.008, -0.030)]


def moth_mesh(kind="up", col=(0.42, 0.30, 0.20), wing=(0.62, 0.46, 0.30), name="moth", k=1.0):
    """ガ（大きめに見せる）：太い毛深い胴、前ばね・うしろばね（目玉もよう）、オスの大きなくし形の触角。kind = up / down / rest。"""
    key = (kind, col, wing, name, k)
    if key in _MOTH:
        return _MOTH[key]
    bm = W.mat(f"{name}_body", col, 0.95)
    wm = W.mat(f"{name}_wing", wing, 0.9)
    eye = W.mat("moth_eye", (0.05, 0.04, 0.03), 0.4)
    ring = W.mat(f"{name}_ring", (0.95, 0.88, 0.70), 0.8)
    dark = W.mat(f"{name}_dark", tuple(c * 0.45 for c in wing), 0.9)
    p = [F._ball(0.018 * k, (0, -0.012 * k, 0), bm, sub=2, sc=(0.9, 2.2, 0.9)),
         F._ball(0.016 * k, (0, 0.022 * k, 0.003 * k), bm, sub=2, sc=(1.1, 1.0, 1.0)),
         F._ball(0.011 * k, (0, 0.036 * k, 0.004 * k), bm, sub=2)]
    ang = {"up": 40, "down": -25, "rest": 4}[kind]
    for sx in (-1, 1):
        p.append(F._ball(0.0045 * k, (sx * 0.008 * k, 0.044 * k, 0.006 * k), eye, sub=1))
        fore = FORE if kind != "rest" else [(x, y - 0.6 * x) for x, y in FORE]
        hind = HIND if kind != "rest" else [(x * 0.9, y - 0.3 * x) for x, y in HIND]
        p.append(_wing(fore, wm, sx, ang, k))
        p.append(_wing(hind, wm, sx, ang, k))
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        for (wx, wy, rr) in ((0.048, 0.014 if kind != "rest" else -0.014, 0.010), (0.034, -0.026, 0.008)):
            p.append(F._ball(rr * k, (sx * wx * ca * k, wy * k, (wx * sa + 0.005) * k), ring, sub=1, sc=(1, 1, 0.12)))
            p.append(F._ball(rr * 0.55 * k, (sx * wx * ca * k, wy * k, (wx * sa + 0.0062) * k), dark, sub=1, sc=(1, 1, 0.12)))
        # くし形の触角（オス）：細い軸に短い枝
        for i in range(6):
            u = (i + 1) / 7
            ax = sx * (0.006 + 0.024 * u) * k
            ay = (0.046 + 0.03 * u) * k
            az = (0.012 + 0.018 * u) * k
            p.append(W.box((ax, ay, az), (0.016 * (1.25 - u) * k, 0.003 * k, 0.003 * k), bm, rot=(0, 0, math.radians(sx * 35)), bevel=0))
        p.append(W.box((sx * 0.018 * k, 0.062 * k, 0.021 * k), (0.0025 * k, 0.038 * k, 0.0025 * k), bm,
                       rot=(math.radians(30), 0, math.radians(-sx * 35)), bevel=0))
    _MOTH[key] = F._join(p, f"{name}_{kind}")
    return _MOTH[key]


def fly_moths(P, nf, near=None, scale=3.0, name="mo", col=(0.42, 0.30, 0.20), wing=(0.62, 0.46, 0.30), flap=2):
    """P = (N, nf+1, 3) の位置。進む向きを向いて飛ぶ。near の番号のガは、羽を上下にはばたく（2コマごと）。"""
    up = moth_mesh("up", col, wing, name)
    dn = moth_mesh("down", col, wing, name)
    objs = []
    N = P.shape[0]
    near = set(range(N)) if near is None else near
    for i in range(N):
        root = bpy.data.objects.new(f"{name}{i}", None)
        bpy.context.collection.objects.link(root)
        root.scale = (scale,) * 3
        bodies = [C.link_copy(up, (0, 0, 0), f"{name}{i}u")]
        if i in near:
            bodies.append(C.link_copy(dn, (0, 0, 0), f"{name}{i}d"))
        for b in bodies:
            b.parent = root
        for f in list(range(1, nf + 1, 2)) + [nf]:
            p = Vector(P[i, f])
            q = Vector(P[i, min(nf, f + 2)]) - Vector(P[i, max(1, f - 2)])
            root.location = p
            if q.length > 1e-5:
                root.rotation_euler = q.to_track_quat('Y', 'Z').to_euler()
            root.keyframe_insert("location", frame=f)
            root.keyframe_insert("rotation_euler", frame=f)
        if len(bodies) > 1:
            ph = i % 2
            for f in range(1, nf + 1, flap):
                on = ((f // flap) + ph) % 2
                for k, b in enumerate(bodies):
                    b.scale = (1.0,) * 3 if k == on else (1e-4,) * 3
                    b.keyframe_insert("scale", frame=f)
            for b in bodies:
                FJ.set_interp(b, 'CONSTANT')
        objs.append(root)
    return objs


# ---------- 文字の板（看板・ラベル） ----------
def text_texture(fname, lines, size=(1024, 384), bg=(250, 120, 170), fg=(255, 255, 255), font_px=150, weight=900, border=None):
    from PIL import Image, ImageDraw, ImageFont
    p = os.path.join(ASSETS, fname)
    if os.path.exists(p):
        return p
    os.makedirs(ASSETS, exist_ok=True)
    im = Image.new("RGB", size, bg)
    d = ImageDraw.Draw(im)
    if border:
        d.rectangle((10, 10, size[0] - 11, size[1] - 11), outline=border, width=12)
    n = len(lines)
    for i, (txt, px) in enumerate(lines):
        fnt = ImageFont.truetype(FONT, px or font_px)
        fnt.set_variation_by_axes([weight])
        d.text((size[0] / 2, size[1] * (i + 0.5) / n), txt, font=fnt, fill=fg, anchor="mm")
    im.save(p)
    return p


def sign(loc, w, h, path, name, rot_x=90, rot_z=0, emit=0.0):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = (w, h, 1)
    o.rotation_euler = (math.radians(rot_x), 0, math.radians(rot_z))
    m = C.img_mat(name, path)
    if emit:
        nt = m.node_tree
        b = nt.nodes["Principled BSDF"]
        tx = [n for n in nt.nodes if n.type == 'TEX_IMAGE'][0]
        nt.links.new(tx.outputs["Color"], b.inputs["Emission Color"])
        b.inputs["Emission Strength"].default_value = emit
    o.data.materials.append(m)
    return o


# ---------- 交差点（東京・駅前のスクランブル交差点。架空の街） ----------
def crossing_set(seed=3, haze=False):
    asph = W.mat("asphalt_x", (0.14, 0.14, 0.15), 0.9)
    bpy.ops.mesh.primitive_plane_add(size=900, location=(0, 0, 0))
    bpy.context.object.data.materials.append(asph)
    white = W.mat("zebra", (0.86, 0.86, 0.84), 0.7)
    R = 11.0
    bars = []
    for side in (-1, 1):
        for k in range(23):
            x = -9.9 + k * 0.9
            bars.append((x, side * 9.6, 0.006, 0.45, 2.6, 0.012, 0.0))          # 北・南の横断歩道
            bars.append((side * 9.6, x, 0.006, 2.6, 0.45, 0.012, 0.0))          # 東・西
    for diag in (1, -1):
        for k in range(-11, 12):
            if diag < 0 and abs(k) <= 1:
                continue
            t = k * 0.9
            bars.append((t * 0.7071, diag * t * 0.7071, 0.007, 0.45, 2.6, 0.012, math.radians(-45 * diag)))
    C.multi_box(bars, white, "zebra_bars")
    stop = W.mat("stopline", (0.85, 0.85, 0.83), 0.7)
    for sx in (-1, 1):
        W.box((sx * 5.5, sx * 11.6, 0.006), (11.0, 0.3, 0.012), stop, bevel=0)
        W.box((sx * -11.6, sx * 5.5, 0.006), (0.3, 11.0, 0.012), stop, bevel=0)
    walk = W.mat("platform_sidewalk", (0.56, 0.55, 0.52), 0.9)
    for sx in (-1, 1):
        for sy in (-1, 1):
            W.box((sx * (R + 30), sy * (R + 30), 0.08), (60, 60, 0.16), walk, bevel=0)
    # ビル（角ごとに。大きな画面・看板つき）
    r = random.Random(seed)
    mats = [C.windows_mat("bld_x1", (0.80, 0.80, 0.82)), C.windows_mat("bld_x2", (0.72, 0.68, 0.62)),
            C.windows_mat("bld_x3", (0.62, 0.66, 0.72), glass=(0.18, 0.24, 0.32)), C.windows_mat("bld_x4", (0.85, 0.82, 0.76))]
    screens = [W.mat(f"led{k}", c, 0.4, emit=c, emit_strength=2.2) for k, c in
               enumerate([(0.95, 0.35, 0.45), (0.25, 0.55, 0.95), (0.95, 0.80, 0.25), (0.35, 0.85, 0.55)])]
    for sx in (-1, 1):
        for sy in (-1, 1):
            x = sx * (R + 4.5)
            for j in range(3):
                w, d, h = r.uniform(9, 14), r.uniform(9, 14), r.uniform(18, 45)
                cx = sx * (R + 3 + w / 2 + j * 0.0)
                cy = sy * (R + 3 + d / 2 + j * 14)
                W.box((cx, cy, h / 2), (w, d, h), r.choice(mats), bevel=0)
                if j == 0:
                    W.box((cx - sx * (w / 2 + 0.05), cy, h * 0.62), (0.1, d * 0.7, h * 0.28), r.choice(screens), bevel=0)
                    W.box((cx, cy - sy * (d / 2 + 0.05), h * 0.62), (w * 0.7, 0.1, h * 0.28), r.choice(screens), bevel=0)
                cx2 = sx * (R + 3 + w / 2 + 14 * (j + 1))
                w2, h2 = r.uniform(9, 14), r.uniform(15, 40)
                W.box((cx2, sy * (R + 3 + 6), h2 / 2), (w2, 11, h2), r.choice(mats), bevel=0)
            _ = x
    C.skyline(seed=seed + 4, y_from=90, y_to=200, x=(-220, 220), n=40, hmin=30, hmax=90)
    pole = W.mat("pole_grey", (0.45, 0.46, 0.48), 0.5)
    sig = W.mat("signal_box", (0.15, 0.15, 0.16), 0.6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = sx * (R + 0.6), sy * (R + 0.6)
            F._cyl(0.08, 0.08, 4.2, (px, py, 2.1), pole)
            W.box((px, py, 3.6), (0.35, 0.35, 0.9), sig, bevel=0.03)
            W.box((px, py, 2.4), (0.25, 0.25, 0.55), sig, bevel=0.03)
            C.point_light((px - sx * 0.2, py - sy * 0.2, 2.45), 2.0, (0.2, 1.0, 0.5), 0.05)
    # 止まっている車（信号待ち）
    car_cols = [(0.85, 0.85, 0.85), (0.15, 0.20, 0.35), (0.65, 0.12, 0.12), (0.92, 0.92, 0.90)]
    glass = W.mat("car_glass", (0.08, 0.10, 0.12), 0.2)
    for k, (cx, cy, rz) in enumerate([(-3.5, -15.0, 0), (3.5, 16.0, 180), (-16.0, 3.0, 90), (16.5, -3.0, 270), (-3.5, -21.0, 0)]):
        m = W.mat(f"car{k}", car_cols[k % 4], 0.35)
        rot = (0, 0, math.radians(rz))
        a = math.radians(rz)
        W.box((cx, cy, 0.62), (1.8, 4.4, 0.75), m, rot=rot, bevel=0.12)
        W.box((cx - 0.0 * math.sin(a), cy - 0.3 * math.cos(a), 1.25), (1.6, 2.2, 0.6), glass, rot=rot, bevel=0.1)
    if haze:
        pass


def crowd_way(r, fo, nf, area=9.0, speed=1.35, start_f=1, stop=True):
    """交差点をわたる人の道すじ：8方向のどれかへまっすぐ。fo で立ち止まる（stop）。"""
    ang = math.radians(r.choice([0, 45, 90, 135, 180, 225, 270, 315]) + r.uniform(-8, 8))
    d = Vector((math.sin(ang), math.cos(ang)))
    c = Vector((r.uniform(-area, area), r.uniform(-area, area)))
    t_go = (fo - start_f) / FPS
    p0 = c - d * speed * t_go * 0.6
    p1 = p0 + d * speed * t_go
    face = math.degrees(math.atan2(d.x, d.y))
    if stop:
        return [(start_f, p0.x, p0.y, face), (fo, p1.x, p1.y, face), (nf, p1.x, p1.y, face + r.uniform(-120, 120))]
    p2 = p0 + d * speed * (nf - start_f) / FPS
    return [(start_f, p0.x, p0.y), (nf, p2.x, p2.y)]


def look_around(r, pos, f0, nf, face0, n=3):
    """立ち止まったあと、まわりをきょろきょろ見回す（向きだけ変える）。"""
    way = [(1, pos[0], pos[1], face0), (f0, pos[0], pos[1], face0)]
    f = f0
    fc = face0
    for k in range(n):
        f += r.randint(14, 30)
        fc += r.choice([-1, 1]) * r.uniform(50, 140)
        if f >= nf:
            break
        way.append((f, pos[0], pos[1], fc))
    way.append((nf, pos[0], pos[1], fc))
    return way


def shake(cam, f0, f1, amp=1.0, seed=1):
    r = random.Random(seed)
    ph = [r.uniform(0, 6.3) for _ in range(6)]
    sc = bpy.context.scene
    for f in range(f0, f1 + 1, 2):
        sc.frame_set(f)
        t = f / FPS
        e = cam.rotation_euler.copy()
        e.x += math.radians(amp * (0.6 * math.sin(7.3 * t + ph[0]) + 0.4 * math.sin(13.1 * t + ph[1])))
        e.y += math.radians(amp * 0.5 * math.sin(9.7 * t + ph[2]))
        e.z += math.radians(amp * (0.6 * math.sin(6.1 * t + ph[3]) + 0.4 * math.sin(11.3 * t + ph[4])))
        cam.rotation_euler = e
        cam.keyframe_insert("rotation_euler", frame=f)
    sc.frame_set(1)


def track_cam(loc_fn, aim_fn, f0, f1, lens, focus="none"):
    c = W.camera(loc_fn(f0), aim_fn(f0), lens=lens)
    c["f0"], c["keep"], c["focus"] = f0, 1, focus
    for f in list(range(f0, f1 + 1, 2)) + [f1]:
        c.location = loc_fn(f)
        W.aim(c, Vector(aim_fn(f)))
        c.keyframe_insert("location", frame=f)
        c.keyframe_insert("rotation_euler", frame=f)
    return c


def lerp3(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(3))


# ============================ 冒頭1：夕暮れの林、ガの群れ ============================
def forest_set(seed=5):
    C.grass_ground(col=(0.16, 0.24, 0.10), name="grass_forest", tufts=900, area=(-10, 22, -4, 16), seed=seed)
    r = random.Random(seed)
    for k in range(34):
        x, y = r.uniform(-30, 40), r.uniform(9, 45)
        if abs(x - 12) < 3 and abs(y - 7) < 3:
            continue
        C.tree((x, y, 0), h=r.uniform(7, 12), crowns=[(0.12, 0.22, 0.10)], seed=seed * 10 + k)
    for k in range(8):
        x, y = r.uniform(-12, 30), r.uniform(-6, 2)
        if -3 < x < 9:
            continue
        C.tree((x, y, 0), h=r.uniform(6, 9), crowns=[(0.10, 0.18, 0.08)], seed=seed * 20 + k)
    FJ.foothills(seed=seed + 2, y=(400, 700), x=(-800, 800), n=10, col=(0.20, 0.22, 0.30), h=(60, 120))


FEMALE = Vector((12.0, 7.0, 1.75))


def p00_moth(nf):
    sky(lo=(1.0, 0.62, 0.42), hi=(0.30, 0.36, 0.62), strength=0.55)
    sun(7, 230, 4.2, (1.0, 0.58, 0.36))
    forest_set()
    # メスのガ：木の枝にとまり、ピンクのにおいを出す
    br = W.mat("trunk", (0.32, 0.22, 0.14), 0.9)
    F._cyl(0.2, 0.14, 5.0, (FEMALE.x + 0.6, FEMALE.y + 0.4, 2.5), br)
    W.box((FEMALE.x + 0.25, FEMALE.y + 0.2, FEMALE.z - 0.06), (0.9, 0.06, 0.06), br, rot=(0, 0, math.radians(-20)), bevel=0)
    fem = C.link_copy(moth_mesh("rest", (0.50, 0.36, 0.24), (0.70, 0.52, 0.34), "female", k=1.3), tuple(FEMALE), "female")
    fem.scale = (3.0,) * 3
    fem.rotation_euler.z = math.radians(80)
    C.point_light(tuple(FEMALE + Vector((0, -0.4, 0.3))), 40, (1.0, 0.5, 0.75), 0.3)
    # においのすじ：メスから風下（-x）へ、くねりながら広がる
    mat = pink_mat(0.14)
    r = random.Random(3)
    births = list(range(-250, nf, 2))
    par = [(r.uniform(0, 6.3), r.uniform(0.10, 0.18)) for _ in births]
    wind = 2.2

    def fn(k, f0, f):
        ph, s0 = par[k]
        t = (f - f0) / FPS
        x = FEMALE.x - wind * t
        if x < -6:
            return None
        sway = 0.14 * t * math.sin(0.9 * (f0 / FPS) + ph * 0.15) + 0.08 * t * math.sin(1.7 * t + ph)
        loc = (x, FEMALE.y + sway, FEMALE.z + 0.15 * t * math.sin(1.3 * t + ph) - 0.03 * t)
        return loc, s0 * (0.6 + 0.28 * t)
    puff_objs(births, nf, fn, mat, "trail", every=3)
    # オスの群れ：風上（+x）へ、ジグザグに飛ぶ。カメラのすぐ横を追いぬく
    N = 90
    rng = np.random.default_rng(4)
    x0 = rng.uniform(-7, 4, N)
    y0 = FEMALE.y + rng.normal(0, 1.6, N)
    z0 = rng.uniform(0.8, 2.6, N)
    close = rng.random(N) < 0.18
    y0[close] = rng.uniform(4.2, 5.4, close.sum())          # カメラの0.5〜2mを通る
    z0[close] = rng.uniform(1.2, 1.9, close.sum())
    x0[close] = rng.uniform(-4.5, 0.5, close.sum())
    v = rng.uniform(2.6, 3.8, N)
    za, zf, zph = rng.uniform(0.25, 0.6, N), rng.uniform(5, 8, N), rng.uniform(0, 6.3, N)
    P = np.zeros((N, nf + 1, 3))
    for f in range(nf + 1):
        t = f / FPS
        x = np.minimum(x0 + v * t, FEMALE.x - 0.35 - 0.25 * np.sin(zph))
        u = np.clip((x - x0) / np.maximum(0.1, FEMALE.x - x0), 0, 1)
        P[:, f, 0] = x
        P[:, f, 1] = y0 + (FEMALE.y - y0) * u ** 1.5 + za * np.sin(zf * t + zph)          # ジグザグ（左右に行ったり来たり）
        P[:, f, 2] = z0 + (FEMALE.z - z0) * u ** 1.5 + 0.12 * np.sin(1.7 * zf * t + zph)
    cam_p = lambda f: lerp3((-3.4, 3.6, 1.0), (2.6, 4.0, 1.25), smooth((f - 1) / (nf - 1)))
    near = {i for i in range(N) if np.min(np.linalg.norm(P[i, 1:] - np.array(cam_p(40)), axis=1)) < 6.0}
    fly_moths(P, nf, near=near, scale=2.0, name="male")
    c = track_cam(cam_p, lambda f: lerp3((0.5, 7.0, 2.0), (11.0, 7.0, 2.0), smooth((f - 1) / (nf - 1)) ** 0.8), 1, nf, 24)
    shake(c, 1, nf, 1.3, seed=3)
    fill((-1.0, -2.0, 2.0), (2.0, 3.0, 1.5), power=60, col=(1.0, 0.75, 0.6))
    return nf


# ============================ 冒頭2：朝の交差点 → フェロモンが出る ============================
T_OPEN0 = 2.6
F_ON = fr(TL.T_VANISH - T_OPEN0)          # この場面の中で、出はじめるコマ


def kacho_open_way(nf):
    return [(1, 0.4, 3.2, 180), (F_ON, 0.2, -3.0, 180), (nf, 0.2, -3.0, 180)]


def crossing_crowd(r, nf, fo, n=70, area=9.0, surprised=True, stop=True, avoid=None):
    roots = []
    for k in range(n):
        way = crowd_way(r, fo, nf, area=area, stop=stop)
        if avoid and any(abs(w[1] - a[0]) < a[2] and abs(w[2] - a[1]) < a[2] for a in avoid for w in way[:2]):
            continue
        lk = crowd_look(r)
        if stop:
            way = way[:2] + look_around(r, (way[1][1], way[1][2]), fo + r.randint(4, 14), nf, way[1][3])[2:]
        roots.append(actor(40 + k, lk, way, nf, face_at=(fo + 3, "surprised") if surprised else None, period=r.choice([7, 8])))
    return roots


def onset_fx(roots, f_on, nf, seed=1, plume_every=7, life=70, burst_n=5):
    """出はじめる瞬間：一人ひとりの体からピンクの粒が飛び出し、けむりがわき上がる。"""
    r = random.Random(seed)
    pts = []
    sc = bpy.context.scene
    sc.frame_set(f_on)
    locs = [Vector(o.matrix_world.translation) for o in roots]
    sc.frame_set(1)
    for p in locs:
        for _ in range(burst_n):
            pts.append((p.x + r.uniform(-0.22, 0.22), p.y + r.uniform(-0.15, 0.15), r.uniform(0.6, 1.6)))
    pink_burst(pts, f_on, size=0.06, rise=1.4, seed=seed, spread=0.7)
    m = pink_mat(0.30)
    for k, p in enumerate(locs):
        body_plume((p.x, p.y), f_on + r.randint(0, 3), nf, nf, every=plume_every, life=life, mat=m, seed=seed * 100 + k,
                   name=f"bp{k}_", size=(0.14, 0.24), rise=0.45)
    return locs


def cp(f):
    """冒頭2のカメラの位置：人波の中を進み、課長に寄る → 出た瞬間から少し上がる。"""
    if f <= F_ON:
        return lerp3((-0.6, -15.5, 1.2), (-0.25, -5.4, 1.6), smooth((f - 1) / (F_ON - 1)) * 0.85 + 0.15 * (f - 1) / (F_ON - 1))
    return lerp3((-0.25, -5.4, 1.6), (-0.45, -5.9, 1.95), smooth((f - F_ON) / 70))


def ca(f):
    if f <= F_ON:
        return lerp3((0.4, 0.0, 1.5), (0.2, -3.0, 1.5), smooth((f - 1) / (F_ON - 1)))
    return lerp3((0.2, -3.0, 1.5), (0.1, -2.6, 1.95), smooth((f - F_ON) / 70))


def p01_open(nf):
    FJ.morning()
    crossing_set()
    r = random.Random(11)
    kacho = actor(1, L(KACHO, face="neutral"), kacho_open_way(nf), nf, face_at=(F_ON + 3, "surprised"))
    roots = crossing_crowd(r, nf, F_ON, n=70, avoid=[(0.3, 0.0, 1.2), (0.2, -3.0, 1.3), (-0.4, -6.0, 1.6)])
    # カメラのすぐ前（1.5〜4m）を横切る人（動きを強く）：カメラが進むのに合わせて、次々に前を通る
    for k in range(16):
        tk = 0.15 + k * 0.19 + r.uniform(-0.05, 0.05)
        fk = 1 + tk * FPS
        cy = cp(min(fk, F_ON))[1]
        y = cy + r.uniform(1.6, 3.8)
        if y > -4.5:
            continue
        sx = 1 if k % 2 else -1
        sp = r.uniform(1.5, 1.9)
        x_at = lambda f: -0.5 + sx * sp * (f - fk) / FPS
        way = [(1, x_at(1), y), (nf, x_at(nf), y)]
        actor(200 + k, crowd_look(r), way, nf, period=7)
    onset_fx(roots + [kacho], F_ON, nf, seed=2, plume_every=10)
    # カメラ：人波の中を進み、課長に寄る → 出た瞬間に少し下がって見上げる
    c = track_cam(cp, ca, 1, nf, 24)
    shake(c, 1, F_ON + 10, 1.1, seed=5)
    fill((-1.5, -7.0, 2.4), (0.2, -3.0, 1.5), power=70)
    return nf


# ============================ 2) 同じ瞬間：交差点の全員から ============================
def p02_burst(nf):
    FJ.morning()
    crossing_set()
    r = random.Random(12)
    roots = []
    for k in range(80):
        x, y = r.uniform(-10, 10), r.uniform(-10, 10)
        face = r.uniform(0, 360)
        way = look_around(r, (x, y), r.randint(1, 20), nf, face, n=3)
        arms = r.choice(["down", "down", "cheek", "head"])
        roots.append(actor(40 + k, crowd_look(r, "surprised"), way, nf, arms=arms))
    roots.append(actor(1, L(KACHO, face="surprised"), look_around(r, (0.2, -3.0), 10, nf, 180, n=2), nf))
    m = pink_mat(0.28)
    for k, o in enumerate(roots):
        p = way_xy(o)
        body_plume(p, 1, nf, nf, every=8, life=80, mat=m, seed=500 + k, name=f"bq{k}_", rise=0.5, size=(0.16, 0.26))
    W.camera((-13.0, -17.0, 6.5), (0.0, -1.0, 1.0), lens=26)
    fill((-6.0, -12.0, 5.0), (0, 0, 1.2), power=200, size=4)
    return nf


def way_xy(o):
    sc = bpy.context.scene
    sc.frame_set(1)
    p = o.matrix_world.translation
    return (p.x, p.y)


# ============================ 3) においは頭の上へ（課長のアップ） ============================
def p03_plume(nf):
    FJ.morning()
    crossing_set()
    r = random.Random(13)
    k_root = actor(1, L(KACHO, face="surprised"), [(1, 0.0, 0.0, 200), (nf, 0.0, 0.0, 200)], nf, arms="down", alt="brow",
                   alt_period=40)
    _ = k_root
    for k in range(26):         # うしろの人（ボケる）
        x, y = r.uniform(-8, 8), r.uniform(3, 14)
        actor(40 + k, crowd_look(r, "surprised"), look_around(r, (x, y), r.randint(1, 30), nf, r.uniform(0, 360)), nf)
    m = pink_mat(0.30)
    body_plume((0.0, 0.0), 1, nf, nf, every=2, rise=0.38, size=(0.07, 0.13), grow=2.2, life=90, mat=m, seed=31, swirl=0.35,
               spread=0.24, z_lo=0.2, z_hi=1.55, name="kp")
    body_plume((0.0, 0.0), 1, nf, nf, every=6, rise=0.30, size=(0.12, 0.2), grow=2.0, life=120, mat=pink_mat(0.16), seed=32,
               swirl=0.45, spread=0.3, z_lo=1.4, z_hi=2.0, name="kq")
    W.camera((1.1, -2.9, 1.05), (0.0, 0.0, 1.85), lens=32)
    fill((1.5, -2.5, 1.6), (0, 0, 1.5), power=90)
    return nf


# ============================ 4) 通勤電車：車内にたまり、ドアから流れ出す ============================
CAR_W, CAR_H = 2.9, 2.35


def train_car(length=20.0, door_open_f=None, nf=0):
    floor = W.mat("train_floor", (0.42, 0.40, 0.36), 0.8)
    wall = W.mat("train_wall", (0.86, 0.86, 0.82), 0.6)
    seat = W.mat("seat_blue", (0.20, 0.30, 0.55), 0.9)
    steel = W.mat("steel", (0.75, 0.76, 0.78), 0.25)
    sky_w = W.mat("window_light", (0.85, 0.92, 1.0), 0.3, emit=(0.80, 0.88, 1.0), emit_strength=2.4)
    hw = CAR_W / 2
    W.box((0, 0, -0.05), (CAR_W, length, 0.1), floor, bevel=0)
    W.box((0, 0, CAR_H + 0.05), (CAR_W, length, 0.1), wall, bevel=0)
    doors = []
    door_ys = [-6.5, 0.0, 6.5]
    for sx in (-1, 1):
        # 壁（窓の上下。ドアのところは開ける）と窓（右側は外の明るい光、左側はホーム）
        edges = [-length / 2] + sum([[y - 0.66, y + 0.66] for y in door_ys], []) + [length / 2]
        for a, b in zip(edges[::2], edges[1::2]):
            W.box((sx * hw, (a + b) / 2, 0.45), (0.08, b - a, 0.9), wall, bevel=0)
            W.box((sx * hw, (a + b) / 2, 2.1), (0.08, b - a, 0.5), wall, bevel=0)
            for yy in np.arange(a + 0.9, b - 0.3, 1.6):
                W.box((sx * hw, yy, 1.35), (0.07, 0.08, 0.9), wall, bevel=0)
        for y in door_ys:
            W.box((sx * hw, y, 2.18), (0.08, 1.32, 0.34), wall, bevel=0)
        if sx > 0:
            W.box((sx * (hw + 0.3), 0, 1.35), (0.05, length, 1.1), sky_w, bevel=0)
        for y in door_ys:
            for s in (-1, 1):       # ドア（2枚）
                d = W.box((sx * (hw - 0.02), y + s * 0.33, 1.0), (0.06, 0.64, 2.0), W.mat("door_steel", (0.70, 0.72, 0.74), 0.3), bevel=0)
                doors.append((d, sx, s, y))
        for k in range(len(door_ys) + 1):
            y0 = -length / 2 if k == 0 else door_ys[k - 1] + 0.9
            y1 = length / 2 if k == len(door_ys) else door_ys[k] - 0.9
            if y1 - y0 < 1:
                continue
            W.box((sx * (hw - 0.3), (y0 + y1) / 2, 0.42), (0.5, y1 - y0, 0.14), seat, bevel=0.03)
            W.box((sx * (hw - 0.08), (y0 + y1) / 2, 0.7), (0.12, y1 - y0, 0.45), seat, bevel=0.03)
            W.box((sx * (hw - 0.45), (y0 + y1) / 2, 1.95), (0.03, y1 - y0, 0.03), steel, bevel=0)       # つり革の棒
            for j in range(int((y1 - y0) / 0.45)):
                yy = y0 + 0.2 + j * 0.45
                W.box((sx * (hw - 0.45), yy, 1.82), (0.01, 0.01, 0.22), W.mat("strap", (0.95, 0.95, 0.95), 0.6), bevel=0)
                F._cyl(0.06, 0.06, 0.02, (sx * (hw - 0.45), yy, 1.68), W.mat("strap", (0.95, 0.95, 0.95), 0.6),
                       rot=(0, math.radians(90), 0), verts=10)
            W.box((sx * (hw - 0.55), (y0 + y1) / 2, 2.12), (0.35, y1 - y0, 0.03), steel, bevel=0)      # 網棚
        for y in door_ys:
            F._cyl(0.02, 0.02, CAR_H, (sx * 0.0 + sx * 0.6, y + 0.9, CAR_H / 2), steel)
    for k in range(6):
        W.box((0, -length / 2 + 2 + k * 3.3, CAR_H - 0.01), (0.3, 1.6, 0.03),
              W.mat("ceiling_light", (1, 1, 1), 0.3, emit=(1.0, 0.98, 0.94), emit_strength=3.0), bevel=0)
    W.box((0, length / 2 + 0.05, CAR_H / 2), (CAR_W, 0.1, CAR_H), wall, bevel=0)
    W.box((0, -length / 2 - 0.05, CAR_H / 2), (CAR_W, 0.1, CAR_H), wall, bevel=0)
    if door_open_f:
        for d, sx, s, y in doors:
            if sx != -1 or y != -6.5:
                continue
            d.keyframe_insert("location", frame=door_open_f)
            d.location.y += s * 0.62
            d.keyframe_insert("location", frame=door_open_f + 12)
    return doors


def p04_train(nf):
    FJ.room((0.95, 0.95, 0.95), 0.9)
    f_open = 92
    train_car(door_open_f=f_open, nf=nf)
    # ホーム（開いたドアの外）
    W.box((-CAR_W / 2 - 3.0, -6.5, -0.1), (6.0, 20, 0.2), W.mat("platform_home", (0.70, 0.68, 0.62), 0.8), bevel=0)
    W.box((-CAR_W / 2 - 0.4, -6.5, 0.004), (0.3, 20, 0.01), W.mat("tactile", (0.95, 0.80, 0.15), 0.7), bevel=0)
    W.box((-CAR_W / 2 - 6.0, -6.5, 2.0), (0.2, 20, 4.0), W.mat("home_wall", (0.88, 0.86, 0.80), 0.8), bevel=0)
    C.point_light((-CAR_W / 2 - 2.0, -6.5, 2.8), 300, (1.0, 0.98, 0.95), 1.0)
    r = random.Random(14)
    people = []
    # すわっている人
    for k in range(10):
        sx = -1 if k % 2 else 1
        y = r.choice([-4.5, -3.8, -3.1, -2.4, 2.4, 3.1, 3.8, 4.5, 7.5, 8.2])
        o = person((sx * (CAR_W / 2 - 0.42), y, 0.28), 90 * sx + 180, seed=60 + k, pose="sit",
                   look=crowd_look(r, "worried" if k % 3 else "surprised"))
        people.append((sx * (CAR_W / 2 - 0.5), y))
        _ = o
    # 立っている人（つり革）
    stand_pts = [(0.75, -4.6), (-0.7, -3.4), (0.6, -1.6), (-0.65, -1.2), (0.7, 1.2), (-0.6, 2.0), (0.1, 3.5), (0.65, 4.4),
                 (-0.7, 5.0), (0.0, -0.5)]
    for k, (x, y) in enumerate(stand_pts):
        arms = ("down", "up") if x > 0 else ("up", "down")
        face = r.choice([0, 180, 90, 270]) + r.uniform(-30, 30)
        actor(80 + k, crowd_look(r, r.choice(["surprised", "worried"])), look_around(r, (x, y), r.randint(10, 40), nf, face, n=2),
              nf, arms=arms)
        people.append((x, y))
    k_pos = (-0.35, -5.4)
    actor(1, L(KACHO, face="worried"), look_around(r, k_pos, 20, nf, 160, n=2), nf, arms=("hold", "up"))
    people.append(k_pos)
    # たまるけむり：最初は体のまわり → 車内に広がる。ドアが開くと、ドアへ吸い寄せられて外へ
    door = Vector((-CAR_W / 2, -6.5, 1.1))
    cam0 = Vector((0.9, -9.5, 1.65))
    m = pink_mat(0.16)
    births, par = [], []
    for k, (x, y) in enumerate(people):
        for j in range(9):
            births.append(1 + j * 9 + r.randint(0, 6))
            par.append((x + r.uniform(-0.2, 0.2), y + r.uniform(-0.2, 0.2), r.uniform(0.6, 1.5), r.uniform(0.10, 0.17),
                        r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(0, 6.3)))

    def fn(k, f0, f):
        x, y, z, s0, vx, vy, ph = par[k]
        t = (min(f, f_open) - f0) / FPS
        spread = 1 - math.exp(-t * 0.5)
        px = x + vx * 0.9 * spread
        py = y + vy * 2.2 * spread
        pz = min(CAR_H - 0.25, z + 0.9 * spread)
        s = s0 * (0.6 + 2.2 * spread)
        if (Vector((px, py, pz)) - cam0).length < 1.2 and f < 80:
            s *= 0.3
        if f > f_open:
            to = door - Vector((px, py, pz))
            dist = to.length
            t2 = (f - f_open) / FPS
            pull = min(1.0, t2 * (2.4 / max(1.0, dist)) ** 1.0 * 1.4)
            q = Vector((px, py, pz)) + to * min(1.0, pull)
            if pull >= 1.0:             # ドアを出たら、ホームへ流れて広がる
                t3 = t2 - dist / 2.4 / 1.4
                q = door + Vector((-1.6 * t3, (ph - 3.1) * 0.25 * t3, 0.3 * t3))
                s *= 1 + 0.6 * t3
            return tuple(q), s
        return (px, py, pz), s
    puff_objs(births, nf, fn, m, "tp", every=3)
    W.camera((0.9, -9.5, 1.65), (-0.4, -3.0, 1.3), lens=24)
    cut(80, (0.85, -3.0, 1.75), (-1.3, -6.6, 1.15), lens=24, orbit=4, push=0.1)
    fill((0.5, -9.0, 2.0), (0, -4, 1.4), power=60)
    return nf


# ============================ 5) 会社：課長に人が集まる ============================
def office_set(nf, seed=6):
    FJ.room((0.95, 0.93, 0.90), 1.0)
    FJ.window_sun(30, 200, 2.6)
    carpet = W.mat("carpet", (0.36, 0.40, 0.46), 1.0)
    W.box((0, 4, -0.05), (24, 24, 0.1), carpet, bevel=0)
    wall = W.mat("office_wall", (0.90, 0.89, 0.86), 0.9)
    W.box((0, 9.0, 0.5), (24, 0.2, 1.0), wall, bevel=0)
    W.box((0, 9.0, 2.85), (24, 0.2, 0.3), wall, bevel=0)
    W.box((0, 9.35, 1.9), (40, 0.05, 2.0), W.mat("city_light", (0.70, 0.82, 0.95), 0.3, emit=(0.70, 0.82, 0.95), emit_strength=1.6),
          bevel=0)
    C.skyline(seed=seed, y_from=60, y_to=140, x=(-120, 120), n=30, hmin=20, hmax=70)
    for x in range(-11, 12, 2):
        W.box((x, 9.0, 1.9), (0.12, 0.22, 2.0), wall, bevel=0)
    W.box((-12.0, 4, 1.5), (0.2, 24, 3.0), wall, bevel=0)
    W.box((12.0, 4, 1.5), (0.2, 24, 3.0), wall, bevel=0)
    desk = W.mat("desk_white", (0.88, 0.88, 0.86), 0.5)
    mon = W.mat("monitor", (0.06, 0.06, 0.07), 0.3)
    scr = W.mat("screen_glow", (0.6, 0.75, 0.9), 0.3, emit=(0.55, 0.70, 0.90), emit_strength=1.2)
    chair = W.mat("chair", (0.12, 0.12, 0.14), 0.7)
    r = random.Random(seed)
    for row in range(3):
        for col in range(5):
            x, y = -6 + col * 3.0, 2.5 + row * 2.2
            if row == 0 and col == 2:
                continue
            W.box((x, y, 0.72), (1.4, 0.75, 0.04), desk, bevel=0.01)
            W.box((x, y + 0.2, 0.95), (0.55, 0.04, 0.35), mon, bevel=0.01)
            W.box((x, y + 0.175, 0.95), (0.5, 0.01, 0.3), scr, bevel=0)
            W.box((x, y - 0.6, 0.45), (0.5, 0.5, 0.1), chair, bevel=0.03)
            _ = r
    # 課長の机（窓を背に、こちら向き）
    W.box((0, 1.6, 0.72), (1.8, 0.8, 0.04), desk, bevel=0.01)
    W.box((0, 1.6, 0.36), (1.7, 0.7, 0.7), W.mat("desk_side", (0.78, 0.78, 0.76), 0.6), bevel=0.01)
    W.box((0.45, 1.75, 0.95), (0.55, 0.04, 0.35), mon, bevel=0.01)
    W.box((-0.5, 1.5, 0.76), (0.3, 0.22, 0.04), W.mat("papers", (0.97, 0.97, 0.95), 0.8), bevel=0)
    W.box((0, 2.3, 0.45), (0.55, 0.55, 0.1), chair, bevel=0.03)
    W.box((0, 2.55, 0.8), (0.5, 0.08, 0.65), chair, bevel=0.03)
    for k in range(6):
        W.box((-9 + k * 3.6, 5, 2.98), (2.0, 0.4, 0.03), W.mat("ceiling_light", (1, 1, 1), 0.3, emit=(1, 0.98, 0.94), emit_strength=3.0),
              bevel=0)


def kacho_desk(nf, face, arms="down", alt=None, period=18):
    return person((0, 2.25, 0.3), 180, seed=1, pose="sit", look=L(KACHO, face=face), arms=arms, alt=alt, nf=nf, period=period)


def p05_office(nf):
    office_set(nf)
    kacho_desk(nf, "surprised", arms="down", alt="brow", period=26)
    r = random.Random(15)
    cup = W.mat("teacup", (0.95, 0.95, 0.92), 0.4)
    targets = [(-1.2, 1.35), (1.2, 1.4), (-1.3, 2.35), (1.35, 2.4), (-0.95, 0.55), (1.0, 0.5)]
    starts = [(-7.0, 4.0), (7.0, 3.0), (-5.0, -1.0), (5.5, -1.5), (0.0, -4.5), (-8.0, 7.0)]
    for k, ((tx, ty), (sx_, sy_)) in enumerate(zip(targets, starts)):
        fc = math.degrees(math.atan2(0.0 - tx, 2.25 - ty))
        f_arr = 30 + k * 12 + r.randint(0, 6)
        lk = L(crowd_look(r, "happy"), top=r.choice([(0.85, 0.85, 0.82), (0.30, 0.32, 0.40), (0.75, 0.55, 0.60), (0.40, 0.50, 0.62)]))
        a = actor(70 + k, lk, [(1, sx_, sy_), (f_arr, tx, ty, fc), (nf, tx, ty, fc)], nf, arms="hold", period=7)
        _ = a
        # 手に持つもの（お茶・書類）
        o = C.link_copy(SG.ico_mesh(), (0, 0.33, 1.0), f"gift{k}")
        o.parent = a
        o.scale = (0.05, 0.05, 0.06)
        o.material_slots[0].link = 'OBJECT'
        o.material_slots[0].material = cup
    body_plume((0.0, 2.25), 1, nf, nf, every=4, rise=0.3, life=80, mat=pink_mat(0.18), seed=51, name="op", z_lo=0.6, z_hi=1.2)
    W.camera((0.5, -2.7, 1.7), (0.0, 1.7, 1.05), lens=28)
    fill((0.5, -2.5, 2.2), (0, 1.8, 1.0), power=80)
    return nf


# ============================ 6) 公園：においは風下へ ============================
def park_set(seed=7):
    C.grass_ground(col=(0.30, 0.46, 0.17), name="grass_park", tufts=1400, area=(-14, 16, -6, 14), seed=seed)
    W.box((0, 4.2, 0.01), (60, 2.4, 0.02), W.mat("dirt_path", (0.62, 0.55, 0.42), 1.0), bevel=0)
    r = random.Random(seed)
    for k in range(16):
        x, y = r.uniform(-30, 30), r.uniform(12, 40)
        C.tree((x, y, 0), h=r.uniform(6, 10), seed=seed * 10 + k)
    wood = W.mat("bench_wood", (0.55, 0.36, 0.20), 0.8)
    iron = W.mat("bench_iron", (0.15, 0.15, 0.16), 0.5)
    bx, by = -5.0, 5.8
    W.box((bx, by, 0.45), (0.45, 1.8, 0.05), wood, bevel=0.01)
    W.box((bx - 0.25, by, 0.75), (0.05, 1.8, 0.35), wood, bevel=0.01)
    for sy in (-1, 1):
        W.box((bx, by + sy * 0.8, 0.22), (0.45, 0.06, 0.45), iron, bevel=0)
    C.skyline(seed=seed + 1, y_from=160, y_to=260, x=(-250, 250), n=30, hmin=20, hmax=70)
    return bx, by


def p06_wind(nf):
    FJ.day(elev=40, az=150)
    bx, by = park_set()
    kacho = person((bx - 0.05, by, 0.27), 90, seed=1, pose="sit", look=L(KACHO, face="surprised"), arms="hold")
    _ = kacho
    W.box((bx + 0.32, by, 0.82), (0.16, 0.25, 0.06), W.mat("bento", (0.85, 0.25, 0.20), 0.5), bevel=0.01)
    # においの帯：風下（+x）へ流れ、ゆっくり左右にゆれる（ホースの水のように）
    src = Vector((bx + 0.15, by, 1.2))
    mat = pink_mat(0.24)
    r = random.Random(16)
    births = list(range(-260, nf, 2))
    par = [(r.uniform(0.12, 0.2), r.uniform(0, 6.3)) for _ in births]
    U = 2.0

    def fn(k, f0, f):
        s0, ph = par[k]
        t = (f - f0) / FPS
        x = src.x + U * t
        if x > 26:
            return None
        aim = 0.32 * math.sin(0.55 * f0 / FPS) + 0.15 * math.sin(1.3 * f0 / FPS + 1)
        y = src.y + aim * U * t + 0.2 * t * math.sin(1.1 * t + ph)
        z = src.z + 0.06 * t + 0.1 * math.sin(0.8 * t + ph)
        return (x, y, z), s0 * (1.0 + 0.32 * t)
    puff_objs(births, nf, fn, mat, "wp", every=3)
    # 風下から、ジグザグに歩いてくる人
    for k, (x0, y0) in enumerate([(4.5, 4.8), (6.0, 7.2), (3.5, 7.4)]):
        way = [(1, x0, y0)]
        f = 1
        x, y = x0, y0
        side = 1 if k % 2 else -1
        while f < nf:
            f += 22
            x -= 1.05
            y = src.y + side * r.uniform(0.9, 1.6)
            side = -side
            way.append((min(f, nf), x, y))
        actor(90 + k, crowd_look(r, "happy"), way, nf, period=8)
    # 風で飛ぶ葉っぱ
    leaf = W.mat("leaf_fly", (0.55, 0.65, 0.20), 0.8)
    for k in range(40):
        o = W.box((0, 0, 0), (0.08, 0.05, 0.004), leaf, bevel=0)
        x0, y0, z0 = r.uniform(-16, 10), r.uniform(0, 12), r.uniform(0.3, 3.5)
        sp = r.uniform(3.0, 5.0)
        for f in range(1, nf + 1, 4):
            t = f / FPS
            o.location = (x0 + sp * t, y0 + 0.3 * math.sin(2 * t + k), z0 + 0.4 * math.sin(3 * t + k))
            o.rotation_euler = (3 * t + k, 2 * t, 4 * t)
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("rotation_euler", frame=f)
    W.camera((bx - 2.2, by - 1.5, 2.1), (bx + 6.0, by + 0.4, 0.9), lens=28)
    fill((bx + 3.0, by - 2.0, 2.2), (bx + 6, by, 1.0), power=120)
    return nf


# ============================ 7) デパート：フェロモン香水をかたづける ============================
def p07_perfume(nf):
    FJ.room((1.0, 0.96, 0.92), 1.1)
    floor = W.mat("store_floor", (0.92, 0.90, 0.86), 0.25)
    W.box((0, 2, -0.05), (16, 14, 0.1), floor, bevel=0)
    W.box((0, 5.5, 1.7), (16, 0.2, 3.4), W.mat("store_wall", (0.95, 0.90, 0.88), 0.8), bevel=0)
    shelf = W.mat("shelf_white", (0.96, 0.95, 0.93), 0.4)
    gold = W.mat("gold_trim", (0.85, 0.65, 0.30), 0.3)
    W.box((0, 5.0, 1.2), (3.6, 0.7, 2.4), shelf, bevel=0.02)
    for z in (0.75, 1.25, 1.75):
        W.box((0, 4.62, z), (3.4, 0.5, 0.03), gold, bevel=0)
    sign((0, 4.63, 2.65), 3.2, 0.9, text_texture("sign_perfume.png", [("フェロモン香水", 150), ("異性をひきつける香り", 70)],
                                                   bg=(235, 90, 150)), "perfume_sign", emit=0.6)
    W.box((0, 2.6, 0.5), (3.0, 0.8, 1.0), shelf, bevel=0.02)
    W.box((0, 2.6, 1.01), (3.0, 0.8, 0.02), gold, bevel=0)
    cols = [(0.95, 0.45, 0.70), (0.70, 0.45, 0.90), (0.95, 0.75, 0.40), (0.90, 0.35, 0.55)]
    r = random.Random(17)
    bottles = []
    for z in (0.77, 1.27, 1.77):
        for k in range(9):
            x = -1.5 + k * 0.37
            col = cols[(k + int(z * 10)) % 4]
            m = W.mat(f"bottle_{col}", col, 0.1, emit=col, emit_strength=0.4)
            b = F._cyl(0.075, 0.075, 0.2, (x, 4.7, z + 0.1), m, verts=8)
            cap = F._cyl(0.035, 0.035, 0.07, (x, 4.7, z + 0.24), gold, verts=8)
            cap.parent = b
            cap.location = (0, 0, 0.135)
            bottles.append(b)
    # 店員が上の段から箱へ移す
    box_m = W.mat("cardboard", (0.72, 0.56, 0.36), 0.9)
    W.box((1.0, 2.6, 1.17), (0.6, 0.45, 0.3), box_m, bevel=0.01)
    sign((1.0, 2.37, 1.2), 0.5, 0.2, text_texture("label_henpin.png", [("返品", 150)], size=(512, 200), bg=(220, 30, 40)), "henpin")
    order = [b for b in bottles if b.location.z > 1.6][::-1][:7]
    for k, b in enumerate(order):
        f0 = 22 + k * 13
        p0 = b.location.copy()
        b.keyframe_insert("location", frame=f0)
        b.location = (0.6, 3.7, 1.6)
        b.keyframe_insert("location", frame=f0 + 6)
        b.location = (1.0 + r.uniform(-0.15, 0.15), 2.6 + r.uniform(-0.1, 0.1), 1.2)
        b.keyframe_insert("location", frame=f0 + 11)
        _ = p0
    actor(1, L(CLERK, face="worried"), [(1, 0.95, 3.75, 330), (nf, 0.95, 3.75, 330)], nf, arms="up", alt="hold", alt_period=7)
    # 通りすぎる客（見向きもしない）
    actor(3, crowd_look(r, "neutral"), [(1, -5.0, 1.3), (60, -5.0, 1.3), (nf, 2.0, 1.3)], nf, period=8)
    for x in (-3, 0, 3):
        C.point_light((x, 2.0, 3.2), 120, (1.0, 0.95, 0.88), 0.5)
    W.camera((0.45, 0.1, 1.7), (0.35, 4.6, 1.7), lens=26)
    fill((1.5, 0.5, 2.0), (0.8, 3.8, 1.5), power=70)
    return nf


# ============================ 8) 【実話】1959年：カイコから最初のフェロモン ============================
def p08_silk(nf):
    FJ.room((0.95, 0.88, 0.75), 0.8)
    FJ.window_sun(35, 240, 2.4)
    wood = W.mat("lab_wood", (0.48, 0.34, 0.22), 0.7)
    W.box((0, 3, -0.05), (12, 10, 0.1), W.mat("lab_floor", (0.55, 0.50, 0.44), 0.8), bevel=0)
    W.box((0, 6.0, 1.6), (12, 0.2, 3.2), W.mat("lab_wall", (0.85, 0.82, 0.74), 0.9), bevel=0)
    W.box((0, 2.2, 0.85), (3.4, 1.2, 0.06), wood, bevel=0.01)
    for sx in (-1, 1):
        for sy in (-1, 1):
            W.box((sx * 1.6, 2.2 + sy * 0.5, 0.42), (0.08, 0.08, 0.84), wood, bevel=0)
    # 木箱とまゆの山（日本から）
    crate = W.mat("crate_wood", (0.62, 0.48, 0.30), 0.8)
    cocoon = W.mat("cocoon", (0.97, 0.96, 0.90), 0.9)
    r = random.Random(18)
    for k, (x, y, z) in enumerate([(-1.6, 3.7, 0.3), (-1.6, 4.5, 0.3), (-1.6, 4.1, 0.9), (2.1, 4.2, 0.3), (2.1, 4.2, 0.9)]):
        W.box((x, y, z), (1.0, 0.75, 0.6), crate, bevel=0.01)
        if k in (0, 3):
            sign((x, y - 0.38, z), 0.8, 0.3, text_texture("crate_japan.png", [("日本　カイコ", 120)], size=(800, 300), bg=(200, 170, 120),
                                                         fg=(60, 30, 20), border=(60, 30, 20)), f"crate_label{k}")
    pts = []
    for k in range(260):
        x, y = r.uniform(-1.4, -0.3), r.uniform(1.85, 2.6)
        h = 0.25 * max(0.0, 1 - ((x + 0.85) / 0.6) ** 2 - ((y - 2.2) / 0.4) ** 2)
        pts.append((x, y, 0.9 + r.uniform(0, h), 0.03, (1.0, 1.6, 1.0)))
    for k in range(120):
        x, y, z = -1.6 + r.uniform(-0.45, 0.45), 4.1 + r.uniform(-0.3, 0.3), 1.22 + r.uniform(0, 0.06)
        pts.append((x, y, z, 0.03, (1.0, 1.6, 1.0)))
    C.multi_ball(pts, cocoon, "cocoons", sub=1)
    glass = W.mat("lab_glass", (0.85, 0.92, 0.95), 0.05, alpha=0.45)
    for k, (x, h, rr) in enumerate([(0.6, 0.3, 0.07), (0.85, 0.22, 0.05), (1.15, 0.35, 0.06)]):
        F._cyl(rr, rr, h, (x, 2.5, 0.88 + h / 2), glass, verts=12)
    F._ball(0.12, (1.35, 2.3, 1.0), glass, sub=2)
    F._cyl(0.03, 0.03, 0.2, (1.35, 2.3, 1.18), glass, verts=10)
    # 研究者：小びんを持ち上げる
    sci = person((0.25, 3.2, 0), 180, seed=3, look=L(SCIENTIST, face="happy"), arms="hold")
    vial = F._cyl(0.025, 0.025, 0.09, (0.25, 2.82, 1.0), W.mat("vial", (0.95, 0.95, 0.85), 0.1, emit=(1.0, 0.6, 0.8), emit_strength=0.8),
                  verts=10)
    _ = sci
    # 机の上のオスのカイコガ：小びんのほうを向いて羽をふるわせる（はばたきダンス）
    N = 6
    nfm = nf
    P = np.zeros((N, nfm + 1, 3))
    for i in range(N):
        a0 = r.uniform(0, 6.3)
        rad = r.uniform(0.3, 0.55)
        for f in range(nfm + 1):
            a = a0 + 0.5 * f / FPS
            P[i, f] = (0.35 + rad * math.cos(a), 2.15 + 0.6 * rad * math.sin(a), 0.89)
    fly_moths(P, nfm, near=set(range(N)), scale=2.2, name="silk", col=(0.96, 0.95, 0.90), wing=(0.97, 0.96, 0.92), flap=2)
    _ = vial
    C.point_light((0.5, 1.5, 2.2), 80, (1.0, 0.85, 0.6), 0.4)
    W.camera((-0.9, -0.5, 1.6), (-0.1, 3.0, 1.2), lens=24)
    fill((-0.5, 0.5, 1.8), (0.25, 3.0, 1.3), power=60)
    return nf


# ============================ 9) 青森のリンゴ畑：交信かく乱 ============================
def apple_tree(x, y, seed):
    r = random.Random(seed)
    trunk = W.mat("trunk", (0.32, 0.22, 0.14), 0.9)
    F._cyl(0.12, 0.09, 1.4, (x, y, 0.7), trunk)
    leaf = W.mat("leafy_apple", (0.20, 0.38, 0.14), 0.9)
    pts = [(x + r.uniform(-0.9, 0.9), y + r.uniform(-0.9, 0.9), 1.9 + r.uniform(-0.2, 0.6), r.uniform(0.7, 1.0), (1, 1, 0.8))
           for _ in range(5)]
    C.multi_ball(pts, leaf, f"crown{seed}", sub=1)
    red = W.mat("apple_red", (0.75, 0.08, 0.06), 0.4)
    ap = []
    for k in range(14):
        a = r.uniform(0, 6.3)
        rr = r.uniform(1.0, 1.3)
        ap.append((x + rr * math.cos(a), y + rr * math.sin(a), r.uniform(1.4, 2.4), 0.06, (1, 1, 1)))
    C.multi_ball(ap, red, f"apples{seed}", sub=1)
    tube = W.mat("dispenser_red", (0.90, 0.08, 0.08), 0.5, emit=(0.9, 0.05, 0.05), emit_strength=0.6)
    disp = []
    for k in range(3):
        a = r.uniform(0, 6.3)
        p = (x + 1.15 * math.cos(a), y + 1.15 * math.sin(a), 1.35)
        F._cyl(0.022, 0.022, 0.32, p, tube, rot=(math.radians(25), 0, a), verts=6)
        disp.append(p)
    return disp


def p09_orchard(nf):
    FJ.day(elev=38, az=160)
    C.grass_ground(col=(0.32, 0.46, 0.17), name="grass_orchard", tufts=900, area=(-8, 8, -4, 18), seed=9)
    disp = []
    for row in range(-2, 3):
        for j in range(8):
            disp += apple_tree(row * 5.0, 1.5 + j * 3.5, seed=row * 20 + j + 50)
    FJ.foothills(seed=12, y=(500, 900), x=(-900, 900), n=10, col=(0.30, 0.40, 0.48), h=(80, 220))
    # 管から出るにおい（畑じゅうにうっすら）
    r = random.Random(19)
    mat = pink_mat(0.20)
    births, par = [], []
    for k, p in enumerate(disp):
        for j in range(3):
            births.append(1 + j * 40 + r.randint(0, 30))
            par.append((p, r.uniform(0.2, 0.35), r.uniform(-0.3, 0.3), r.uniform(-0.3, 0.3)))

    def fn(k, f0, f):
        p, s0, vx, vy = par[k]
        t = (f - f0) / FPS
        return (p[0] + vx * t + 0.4 * t, p[1] + vy * t, p[2] + 0.05 * t), s0 * (1 + 0.5 * t)
    puff_objs(births, nf, fn, mat, "orp", every=4)
    # 迷うガ：行ったり来たり、ぐるぐる
    N = 30
    P = np.zeros((N, nf + 1, 3))
    rng = np.random.default_rng(9)
    c = np.column_stack([rng.uniform(0.8, 4.2, N), rng.uniform(0.0, 9, N), rng.uniform(1.1, 2.2, N)])
    w = rng.uniform(1.5, 3.5, (N, 3))
    ph = rng.uniform(0, 6.3, (N, 3))
    for f in range(nf + 1):
        t = f / FPS
        P[:, f, 0] = c[:, 0] + 0.6 * np.sin(w[:, 0] * t + ph[:, 0])
        P[:, f, 1] = c[:, 1] + 0.6 * np.sin(w[:, 1] * t + ph[:, 1])
        P[:, f, 2] = c[:, 2] + 0.35 * np.sin(w[:, 2] * t + ph[:, 2])
    fly_moths(P, nf, near=set(range(N)), scale=2.0, name="apm", col=(0.50, 0.40, 0.28), wing=(0.66, 0.55, 0.38))
    W.camera((2.5, -3.2, 1.65), (2.3, 6.0, 1.55), lens=26)
    fill((1.0, -1.0, 2.0), (0, 4, 1.6), power=40)
    return nf


# ============================ 10) 1か月後：街じゅうがにおいだらけ ============================
def p10_confuse(nf):
    FJ.morning()
    crossing_set()
    r = random.Random(20)
    roots = []
    for k in range(70):
        cx, cy = r.uniform(-10, 10), r.uniform(-10, 10)
        rad = r.uniform(0.8, 2.2)
        a0 = r.uniform(0, 6.3)
        sp = r.choice([-1, 1]) * r.uniform(0.5, 0.8)
        way = [(f, cx + rad * math.cos(a0 + sp * f / FPS), cy + rad * math.sin(a0 + sp * f / FPS)) for f in range(1, nf + 1, 10)]
        if way[-1][0] != nf:
            way.append((nf, cx + rad * math.cos(a0 + sp * nf / FPS), cy + rad * math.sin(a0 + sp * nf / FPS)))
        roots.append(actor(40 + k, crowd_look(r, "worried"), way, nf, period=8))
    kway = [(f, 0.3 + 0.9 * math.cos(1.0 + 0.6 * f / FPS), -2.5 + 0.9 * math.sin(1.0 + 0.6 * f / FPS)) for f in range(1, nf + 1, 10)]
    kway.append((nf, 0.3 + 0.9 * math.cos(1.0 + 0.6 * nf / FPS), -2.5 + 0.9 * math.sin(1.0 + 0.6 * nf / FPS)))
    actor(1, L(KACHO, face="worried"), kway, nf, period=8)
    # 街をおおうピンクのもや（大きなけむりが重なる）
    mat = pink_mat(0.06, col=(1.0, 0.62, 0.80), glow=1.6)
    births, par = [], []
    for k in range(120):
        births.append(1)
        par.append((r.uniform(-16, 16), r.uniform(-14, 22), r.uniform(0.5, 3.5), r.uniform(1.3, 2.6), r.uniform(0, 6.3)))

    def fn(k, f0, f):
        x, y, z, s, ph = par[k]
        t = f / FPS
        return (x + 0.3 * math.sin(0.4 * t + ph), y + 0.3 * math.cos(0.3 * t + ph), z), s * (1 + 0.05 * math.sin(t + ph))
    puff_objs(births, nf, fn, mat, "haze", every=6)
    m2 = pink_mat(0.18)
    for k, o in enumerate(roots[::3]):
        body_plume(way_xy(o), 1, nf, nf, every=14, life=70, mat=m2, seed=700 + k, name=f"bc{k}_")
    W.camera((-9.0, -15.0, 4.2), (0.0, -1.0, 1.2), lens=28)
    fill((-5.0, -10.0, 4.0), (0, -2, 1.2), power=160, size=4)
    return nf


# ============================ 11) 3か月後：モテ期おわり ============================
def p11_used(nf):
    office_set(nf)
    kacho_desk(nf, "worried", arms="down", alt="cheek", period=40)
    r = random.Random(21)
    for k, (y, d) in enumerate([(0.2, 1), (-0.8, -1), (3.6, 1)]):
        x0 = -8 * d
        f0 = 1 + k * 25
        actor(70 + k, crowd_look(r, "neutral"), [(1, x0 - d * 1.4 * f0 / FPS, y), (nf, x0 + d * 1.4 * (nf - f0) / FPS, y)], nf, period=8)
    body_plume((0.0, 2.25), 1, nf, nf, every=8, rise=0.25, life=70, mat=pink_mat(0.10), seed=61, name="up", z_lo=0.6, z_hi=1.2)
    W.camera((0.6, -3.6, 1.75), (0.0, 1.6, 1.0), lens=28)
    cut(80, (-0.6, -0.4, 1.3), (0.0, 2.3, 1.15), lens=32, orbit=3, push=0.12)
    fill((0.5, -2.5, 2.2), (0, 1.8, 1.0), power=80)
    return nf


# ============================ 12) 1年後：玄関で妻が迎える ============================
def p12_home(nf):
    FJ.room((0.95, 0.80, 0.60), 0.5)
    wood = W.mat("floor_wood", (0.58, 0.40, 0.24), 0.6)
    tile = W.mat("genkan_tile", (0.45, 0.44, 0.42), 0.8)
    wall = W.mat("home_wall", (0.92, 0.88, 0.78), 0.9)
    W.box((0, 0.0, 0.1), (4, 5.0, 0.3), wood, bevel=0)              # 上がりかまち（板の間）
    W.box((0, 3.3, -0.02), (4, 1.6, 0.04), tile, bevel=0)           # たたき
    W.box((-2.0, 1.8, 1.4), (0.1, 8, 2.8), wall, bevel=0)
    W.box((2.0, 1.8, 1.4), (0.1, 8, 2.8), wall, bevel=0)
    W.box((0, 1.8, 2.85), (4.2, 8, 0.1), wall, bevel=0)
    # 玄関のドア（開いている）と、外の夜
    W.box((-1.1, 4.15, 1.2), (1.8, 0.1, 2.4), wall, bevel=0)
    W.box((1.6, 4.15, 1.2), (0.8, 0.1, 2.4), wall, bevel=0)
    W.box((1.15, 3.65, 1.05), (0.06, 0.9, 2.1), W.mat("door_wood", (0.30, 0.20, 0.12), 0.6), bevel=0.01)
    W.box((0.45, 6.0, 1.5), (6, 0.1, 3), W.mat("night_out", (0.05, 0.07, 0.15), 0.8, emit=(0.06, 0.09, 0.20), emit_strength=1.0), bevel=0)
    # げた箱・花・写真
    W.box((-1.65, 2.6, 0.5), (0.6, 1.4, 1.0), W.mat("getabako", (0.62, 0.45, 0.28), 0.6), bevel=0.01)
    F._cyl(0.06, 0.05, 0.2, (-1.65, 2.2, 1.1), W.mat("vase", (0.30, 0.45, 0.65), 0.3), verts=10)
    C.multi_ball([(-1.65 + dx, 2.2 + dy, 1.28, 0.05, (1, 1, 1)) for dx, dy in ((0, 0), (0.06, 0.04), (-0.05, 0.03))],
                 W.mat("flower_pink", (0.95, 0.45, 0.60), 0.6), "flowers")
    sign((-1.62, 2.85, 1.2), 0.3, 0.22, text_texture("photo_wedding.png", [("1995", 140)], size=(500, 360), bg=(240, 235, 225),
                                                       fg=(150, 120, 90), border=(120, 90, 60)), "photo", rot_z=90)
    C.point_light((0, 1.6, 2.5), 90, (1.0, 0.82, 0.55), 0.6)
    C.point_light((0.4, 3.2, 2.5), 60, (1.0, 0.80, 0.55), 0.2)
    # 課長（入ってくる）と妻（迎える）
    f_in = 40
    f_give = 75
    actor(1, L(KACHO, face="happy"), [(1, 0.5, 5.2), (f_in, 0.55, 3.05, 217), (nf, 0.55, 3.05, 217)], nf, arms="hold",
          face_at=(f_give + 12, "happy", "down"), period=8)
    wife = actor(2, L(WIFE, face="happy"), [(1, -0.02, 2.3, 37), (nf, -0.02, 2.3, 37)], nf, arms="down", face_at=(f_give, "happy", "hold"))
    lift = bpy.data.objects.new("lift", None)
    bpy.context.collection.objects.link(lift)
    lift.location = (0, 0, 0.25)
    wife.parent = lift
    jacket = W.box((0.5, 4.85, 1.0), (0.45, 0.12, 0.5), W.mat("jacket", (0.12, 0.15, 0.26), 0.8), bevel=0.02)
    for f, p in ((1, (0.5, 4.85, 1.0)), (f_in, (0.33, 2.76, 1.0)), (f_give, (0.33, 2.76, 1.0)), (f_give + 12, (0.2, 2.59, 1.23)),
                 (nf, (0.2, 2.59, 1.23))):
        jacket.location = p
        jacket.keyframe_insert("location", frame=f)
    for o in (jacket,):
        o.location.z += 0.25 * 0
    # ふたりのけむりが、上で ひとつにまざる
    mA, mB = pink_mat(0.16), pink_mat(0.16, (1.0, 0.55, 0.70), "phero2")
    body_plume(lambda f: (0.55, 3.05) if f > f_in else (0.5, 4.5), 1, nf, nf, every=8, rise=0.25, life=60, mat=mA, seed=71,
               drift=(-0.10, -0.12), name="ha", size=(0.06, 0.11), z_lo=1.2, z_hi=1.7, spread=0.15)
    body_plume((-0.02, 2.3), 1, nf, nf, every=8, rise=0.25, life=60, mat=mB, seed=72, drift=(0.10, 0.12), name="hb",
               size=(0.06, 0.11), z_lo=1.45, z_hi=1.95, spread=0.15)
    W.camera((1.8, 1.5, 1.6), (0.2, 2.62, 1.4), lens=21)
    cut(132, (1.65, 1.75, 1.65), (0.24, 2.66, 1.5), lens=26, orbit=3, push=0.12)
    fill((1.3, 1.2, 2.0), (0.1, 2.8, 1.4), power=50, col=(1.0, 0.85, 0.7))
    return nf


SCENES = {k: v for k, v in globals().items() if callable(v) and k[:1] == "p" and k[1:3].isdigit() and "_" in k}

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
    if os.environ.get("DRY"):
        print("built", name, len(bpy.data.objects), "objects", flush=True)
        sys.exit(0)
    FJ.render(out, nf, step, first, last)
    print("rendered", name, flush=True)
