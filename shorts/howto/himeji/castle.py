"""姫路城の部品（Blender / bpy）：扇の勾配の石垣、家、塀（しっくい＋瓦）、櫓と石落とし、門、天守。
座標：z=上（m）。石垣の上面の中心が (cx, cy, z0+H)。"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import kit as K  # noqa: E402

bpy = K.bpy
import bmesh  # noqa: E402
from mathutils import Vector  # noqa: E402

D2R = K.D2R


# ---------- 材質 ----------
def stone_mat():
    return K.noisy("stone", (0.56, 0.50, 0.41), 1.3, 0.38, 0.8, 0.92, attr=True)


def plaster_mat(name="plaster", col=(0.78, 0.77, 0.73)):
    return K.noisy(name, col, 2.0, 0.05, 0.04, 0.9)


def wood_mat():
    return K.noisy("wood_dark", (0.075, 0.05, 0.03), 5.0, 0.3, 0.15, 0.75)


def wood_raw_mat():
    """しっくいを塗る前の板壁（火が付く）。"""
    return K.noisy("wood_raw", (0.36, 0.22, 0.11), 3.0, 0.35, 0.3, 0.85)


def tile_mat(name="tile", col=(0.15, 0.16, 0.17), joint=(0.42, 0.42, 0.41), pitch=0.30):
    """瓦：屋根の流れにそって白いしっくいの目地が走る（姫路城の屋根の白い筋）。"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.55
    tc = nt.nodes.new("ShaderNodeTexCoord")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sp.inputs[0])
    sn = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Normal"], sn.inputs[0])
    ax = nt.nodes.new("ShaderNodeMath")
    ax.operation = 'ABSOLUTE'
    nt.links.new(sn.outputs[0], ax.inputs[0])
    ay = nt.nodes.new("ShaderNodeMath")
    ay.operation = 'ABSOLUTE'
    nt.links.new(sn.outputs[1], ay.inputs[0])
    gt = nt.nodes.new("ShaderNodeMath")
    gt.operation = 'GREATER_THAN'
    nt.links.new(ax.outputs[0], gt.inputs[0])
    nt.links.new(ay.outputs[0], gt.inputs[1])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'FLOAT'
    nt.links.new(gt.outputs[0], mix.inputs[0])
    nt.links.new(sp.outputs[0], mix.inputs[2])
    nt.links.new(sp.outputs[1], mix.inputs[3])
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = 'MULTIPLY'
    mul.inputs[1].default_value = 2 * math.pi / pitch
    nt.links.new(mix.outputs[0], mul.inputs[0])
    sin = nt.nodes.new("ShaderNodeMath")
    sin.operation = 'SINE'
    nt.links.new(mul.outputs[0], sin.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.86
    ramp.color_ramp.elements[0].color = (*col, 1)
    ramp.color_ramp.elements[1].position = 0.96
    ramp.color_ramp.elements[1].color = (*joint, 1)
    nt.links.new(sin.outputs[0], ramp.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 3.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    mm = nt.nodes.new("ShaderNodeMix")
    mm.data_type = 'RGBA'
    mm.blend_type = 'MULTIPLY'
    mm.inputs["Factor"].default_value = 0.35
    nt.links.new(ramp.outputs[0], mm.inputs[6])
    nt.links.new(nz.outputs["Color"], mm.inputs[7])
    nt.links.new(mm.outputs[2], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = 0.5
    nt.links.new(sin.outputs[0], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


def soil_mat():
    return K.noisy("soil_top", (0.36, 0.30, 0.22), 0.6, 0.3, 0.3, 0.95)


# ---------- 扇の勾配の石垣 ----------
class Ishigaki:
    """上面 Wt×Dt（中心 cx,cy、高さ z0+H）。下は外へ D 広がる。外へのはみ出し o(h)=D(1-h/H)^2：
    下はゆるい坂、上へ行くほど急、てっぺんはほぼ垂直。段（course）ごとに1つのオブジェクト（積み上げのアニメ用）。"""

    def __init__(self, cx, cy, Wt, Dt, H, D, z0=0.0, course=0.78, seed=1, name="ishi", dep=1.0, sides=(1, 1, 1, 1), parent=None):
        self.cx, self.cy, self.Wt, self.Dt, self.H, self.D, self.z0 = cx, cy, Wt, Dt, H, D, z0
        self.root = K.empty((cx, cy, z0), parent, f"{name}_root")
        r = random.Random(seed)
        n = max(1, int(round(H / course)))
        ch = H / n
        sm = stone_mat()
        self.courses = []
        for k in range(n):
            zl, zh = k * ch, (k + 1) * ch
            zc = (zl + zh) / 2
            o, t = self.off(zc), self.slope(zc)
            hx, hy = Wt / 2 + o, Dt / 2 + o
            bm = bmesh.new()
            cl = bm.loops.layers.float_color.new("col")
            even = k % 2 == 0
            # 辺：(始点, 向き, 外向き, 長さの半分, 角を持つか)
            S = [((0, -hy), (1, 0), (0, -1), hx, even), ((hx, 0), (0, 1), (1, 0), hy, not even),
                 ((0, hy), (-1, 0), (0, 1), hx, even), ((-hx, 0), (0, -1), (-1, 0), hy, not even)]
            for si, (c0, av, nv, half, own) in enumerate(S):
                if not sides[si]:
                    continue
                a0, a1 = (-half, half) if own else (-half + dep, half - dep)
                a = a0
                first = True
                while a < a1 - 0.05:
                    L = r.uniform(1.9, 2.4) if (own and first) else r.uniform(0.9, 1.9)
                    if a1 - (a + L) < 0.5:
                        L = a1 - a
                    if own and a1 - (a + L) < 1.7 and a1 - a > 2.2:
                        L = a1 - a - r.uniform(1.6, 2.0)
                    s0, s1 = a, a + L
                    end0 = own and abs(s0 - (-half)) < 1e-6
                    end1 = own and abs(s1 - half) < 1e-6
                    self._stone(bm, cl, r, c0, av, nv, s0, s1, zl, zh, zc, t, dep, end0, end1)
                    a = s1
                    first = False
            bmesh.ops.bevel(bm, geom=list(bm.edges), offset=0.07, segments=2, affect='EDGES', clamp_overlap=True)
            me = bpy.data.meshes.new(f"{name}_c{k}")
            bm.to_mesh(me)
            bm.free()
            for p in me.polygons:
                p.use_smooth = False
            me.materials.append(sm)
            ob = bpy.data.objects.new(f"{name}_c{k}", me)
            bpy.context.collection.objects.link(ob)
            ob.parent = self.root
            self.courses.append(ob)
        self.core = self._core(name, 0.32)
        self.core.parent = self.root

    def off(self, h):
        u = max(0.0, min(1.0, h / self.H))
        return self.D * (1 - u) ** 2

    def slope(self, h):
        """高さ1m上がるごとに内へ入る量（=坂のゆるさ）。"""
        return 2 * self.D / self.H * (1 - max(0.0, min(1.0, h / self.H)))

    def face_point(self, side, a, h):
        """辺 side（0=-y 1=+x 2=+y 3=-x）の、辺にそった位置 a、高さ h の石垣の表面の点（ワールド座標）。"""
        o = self.off(h)
        hx, hy = self.Wt / 2 + o, self.Dt / 2 + o
        p = [(a, -hy), (hx, a), (-a, hy), (-hx, -a)][side]
        return (self.cx + p[0], self.cy + p[1], self.z0 + h)

    def corner_point(self, sx, sy, h):
        o = self.off(h)
        return (self.cx + sx * (self.Wt / 2 + o), self.cy + sy * (self.Dt / 2 + o), self.z0 + h)

    def _stone(self, bm, cl, r, c0, av, nv, s0, s1, zl, zh, zc, t, dep, end0, end1):
        g = 0.025
        pb, pt = r.uniform(0.0, 0.09), r.uniform(0.0, 0.09)      # 下と上で出っぱりを変える（石の面のでこぼこ）
        z0, z1 = zl + g + r.uniform(-0.05, 0.05), zh - g + r.uniform(-0.05, 0.05)
        a0, a1 = s0 + g, s1 - g
        if end0:
            a0 = s0
        if end1:
            a1 = s1
        verts = []
        for z in (z0, z1):
            sh = -t * (z - zc)                 # 上ほど内へ（坂）
            prot = pb if z == z0 else pt
            for aa, isend in ((a0, end0), (a1, end1)):
                for nn in (prot, -dep):
                    a_ = aa
                    if isend:                  # 角の石：となりの辺の坂にそって端も傾ける
                        a_ = aa + (sh if aa > 0 else -sh)
                    n_ = nn + sh
                    x = c0[0] + av[0] * a_ + nv[0] * n_
                    y = c0[1] + av[1] * a_ + nv[1] * n_
                    verts.append(bm.verts.new((x, y, z)))
        # 頂点の並び：z0(a0 前,a0 後,a1 前,a1 後), z1(同じ)
        v = verts
        faces = [(0, 2, 6, 4), (1, 5, 7, 3), (0, 4, 5, 1), (2, 3, 7, 6), (0, 1, 3, 2), (4, 6, 7, 5)]
        shade = r.uniform(0.6, 1.3)
        warm = r.uniform(-0.04, 0.18)
        col = (shade * (1 + warm), shade, shade * (1 - warm * 0.8), 1.0)
        for fi in faces:
            try:
                f = bm.faces.new([v[i] for i in fi])
            except ValueError:
                continue
            for lp in f.loops:
                lp[cl] = col
        bmesh.ops.recalc_face_normals(bm, faces=[f for f in bm.faces if f.verts[0] in v])

    def _core(self, name, inset):
        """石のすき間から見える奥の黒い中身（曲面の台）。"""
        bm = bmesh.new()
        n = 24
        rings = []
        for i in range(n + 1):
            h = self.H * i / n
            o = self.off(h) - inset
            hx, hy = self.Wt / 2 + o, self.Dt / 2 + o
            rings.append([bm.verts.new((sx * hx, sy * hy, h)) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))])
        for i in range(n):
            for j in range(4):
                bm.faces.new((rings[i][j], rings[i][(j + 1) % 4], rings[i + 1][(j + 1) % 4], rings[i + 1][j]))
        bm.faces.new(rings[-1])
        me = bpy.data.meshes.new(f"{name}_core")
        bm.to_mesh(me)
        bm.free()
        me.materials.append(K.mat("stone_core", (0.035, 0.033, 0.03), 0.95))
        ob = bpy.data.objects.new(f"{name}_core", me)
        bpy.context.collection.objects.link(ob)
        return ob

    def stack(self, f0, f1, drop=2.5):
        """段を下から順に f0〜f1 で落として積む（参考元の「1段ずつ積み上がる」）。"""
        n = len(self.courses)
        cores = self.core
        for k, ob in enumerate(self.courses):
            fk = int(f0 + (f1 - f0) * k / max(1, n - 1))
            K.key_scale(ob, max(0, fk - 5), 1e-4)
            K.key_loc(ob, max(0, fk - 5), (0, 0, drop))
            K.key_scale(ob, fk - 4, 1.0)
            K.key_loc(ob, fk, (0, 0, -0.04))
            K.key_loc(ob, fk + 2, (0, 0, 0))
        # 中身は積んだ高さまで伸ばす
        K.key_scale(cores, max(0, f0 - 1), (1, 1, 1e-3))
        K.key_scale(cores, f1, (1, 1, 1))
        return [int(f0 + (f1 - f0) * k / max(1, n - 1)) for k in range(n)]


def slab(cx, cy, z, w, d, th=0.4, m=None, name="slab", parent=None):
    return K.obj(K.box_mesh(w, d, th), m or soil_mat(), parent, (cx, cy, z - th / 2), name=name)


# ---------- 屋根 ----------
def hip_roof(cx, cy, z, w, d, h, over=0.8, sori=0.35, th=0.28, m=None, name="roof", parent=None, gable=False):
    """寄棟（gable=True で入母屋ふう：棟の両はしに三角の破風）。w×d は壁の外の大きさ、over は軒の出、sori は軒の角の反り上がり。"""
    m = m or tile_mat()
    bm = bmesh.new()
    W, Dd = w / 2 + over, d / 2 + over
    rx = max(0.0, (w - d) / 2) if w >= d else 0.0
    ry = max(0.0, (d - w) / 2) if d > w else 0.0
    corners = [(-W, -Dd), (W, -Dd), (W, Dd), (-W, Dd)]
    if w >= d:
        ridge = [(-rx, 0), (rx, 0)]
        rmap = [0, 1, 1, 0]
    else:
        ridge = [(0, -ry), (0, ry)]
        rmap = [0, 0, 1, 1]
    zr = h
    eave = [bm.verts.new((x, y, sori)) for x, y in corners]
    mids = []
    for (x, y), ri in zip(corners, rmap):
        p = (x + (ridge[ri][0] - x) * 0.45, y + (ridge[ri][1] - y) * 0.45)
        mids.append(bm.verts.new((p[0], p[1], zr * 0.36 + sori * 0.2)))
    # 辺の真ん中も少し反らす（軒先の曲線）
    emid = []
    for i in range(4):
        a, b = corners[i], corners[(i + 1) % 4]
        emid.append(bm.verts.new(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0.0)))
    mmid = []
    for i in range(4):
        a, b = mids[i].co, mids[(i + 1) % 4].co
        mmid.append(bm.verts.new(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, zr * 0.36)))
    rv = [bm.verts.new((x, y, zr)) for x, y in ridge]
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((eave[i], emid[i], mmid[i], mids[i]))
        bm.faces.new((emid[i], eave[j], mids[j], mmid[i]))
        ri, rj = rmap[i], rmap[j]
        if ri != rj:
            bm.faces.new((mids[i], mmid[i], rv[rj], rv[ri]) if True else ())
            bm.faces.new((mmid[i], mids[j], rv[rj]))
        else:
            bm.faces.new((mids[i], mmid[i], rv[ri]))
            bm.faces.new((mmid[i], mids[j], rv[ri]))
    # 軒の厚み（下へ）と軒裏
    low = [bm.verts.new((v.co.x, v.co.y, v.co.z - th)) for v in eave]
    lmid = [bm.verts.new((v.co.x, v.co.y, v.co.z - th)) for v in emid]
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((low[i], lmid[i], emid[i], eave[i]))
        bm.faces.new((lmid[i], low[j], eave[j], emid[i]))
    bm.faces.new([low[0], lmid[0], low[1], lmid[1], low[2], lmid[2], low[3], lmid[3]][::-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.location = (cx, cy, z)
    if parent is not None:
        ob.parent = parent
    # 棟（しっくいの白い棟＋黒い瓦の上端）
    L = (rx * 2 if w >= d else ry * 2) + 0.6
    rid = K.obj(K.box_mesh(L if w >= d else 0.42, 0.42 if w >= d else L, 0.36), plaster_mat("ridge_white", (0.70, 0.70, 0.68)), ob,
                (0, 0, zr + 0.02), name=f"{name}_ridge")
    K.obj(K.box_mesh(L + 0.1 if w >= d else 0.3, 0.3 if w >= d else L + 0.1, 0.14), K.mat("ridge_top", (0.07, 0.07, 0.08), 0.5), rid,
          (0, 0, 0.22), name=f"{name}_ridgetop")
    if gable:
        gw = (d if w >= d else w) * 0.42
        for s in (-1, 1):
            p = (s * (rx + 0.05), 0, zr * 0.55) if w >= d else (0, s * (ry + 0.05), zr * 0.55)
            g = hafu(gw, zr * 0.55, name=f"{name}_hafu{s}")
            g.parent = ob
            g.location = p
            g.rotation_euler = (0, 0, (-90 if s > 0 else 90) * D2R if w >= d else (0 if s > 0 else 180) * D2R)
    return ob


def hafu(w, h, name="hafu", depth=0.6):
    """三角の破風（白いしっくいの三角＋黒い縁の屋根）。原点は三角の底辺の真ん中、+y が正面。"""
    root = K.empty(name=name)
    me = bpy.data.meshes.new(name)
    vs = [(-w / 2, 0, 0), (w / 2, 0, 0), (0, 0, h), (-w / 2, -depth, 0), (w / 2, -depth, 0), (0, -depth, h)]
    me.from_pydata(vs, [], [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1)])
    me.materials.append(plaster_mat())
    o = bpy.data.objects.new(name + "_tri", me)
    bpy.context.collection.objects.link(o)
    o.parent = root
    tm = tile_mat()
    sl = math.hypot(w / 2, h)
    ang = math.atan2(h, w / 2)
    for s in (-1, 1):
        K.obj(K.box_mesh(sl + 0.5, depth + 0.9, 0.18), tm, root, (s * w / 4, -depth / 2 + 0.2, h / 2 + 0.12),
              rot=(0, s * ang, 0), name=name + "_eave")
    K.obj(K.box_mesh(0.12, 0.05, 0.12), wood_mat(), root, (0, 0.02, h * 0.6), name=name + "_gegyo")
    return root


def chidori(roof, x, y, z, face_deg, w, h, name="chidori"):
    """屋根の上にのる三角の破風（千鳥破風）。face_deg：正面の向き。"""
    g = hafu(w, h, name=name, depth=w * 0.7)
    g.parent = roof
    g.location = (x, y, z)
    g.rotation_euler = (0, 0, face_deg * D2R)
    return g


# ---------- 壁・家 ----------
def wall_box(p0, p1, z, h, t, m, name="wall", parent=None):
    """p0→p1 の直線の壁（厚さ t、高さ h、下の高さ z）。"""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    L = d.length
    ang = math.atan2(d.y, d.x)
    c = (p0 + p1) / 2
    return K.obj(K.box_mesh(L, t, h), m, parent, (c.x, c.y, z + h / 2), rot=(0, 0, ang), name=name)


def coping(p0, p1, z, t, name="cope", parent=None, over=0.28, h=0.32):
    """塀の上の瓦屋根（両側へ流れる小さな切妻）。"""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    L = d.length + 0.2
    ang = math.atan2(d.y, d.x)
    c = (p0 + p1) / 2
    hw = t / 2 + over
    me = bpy.data.meshes.new(name)
    vs = [(-L / 2, -hw, 0), (L / 2, -hw, 0), (L / 2, 0, h), (-L / 2, 0, h), (L / 2, hw, 0), (-L / 2, hw, 0),
          (-L / 2, -hw, -0.08), (L / 2, -hw, -0.08), (L / 2, hw, -0.08), (-L / 2, hw, -0.08)]
    fs = [(0, 1, 2, 3), (3, 2, 4, 5), (6, 7, 1, 0), (5, 4, 8, 9), (9, 8, 7, 6), (0, 3, 5, 9, 6), (1, 7, 8, 4, 2)]
    me.from_pydata(vs, [], fs)
    me.materials.append(tile_mat())
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.location = (c.x, c.y, z)
    o.rotation_euler = (0, 0, ang)
    if parent is not None:
        o.parent = parent
    K.obj(K.box_mesh(L, 0.2, 0.12), K.mat("ridge_top", (0.07, 0.07, 0.08), 0.5), o, (0, 0, h), name=name + "_r")
    return o


def dobei(pts, z=0.0, h=2.3, t=0.42, name="dobei", parent=None, closed=True, gap=None):
    """しっくいの塀（白い壁＋下の黒い腰板＋上の瓦）。pts の折れ線にそって作る。gap=(辺の番号, 中心の位置, 幅) で門の口をあける。
    戻り値：辺ごとの [オブジェクトの list]（立ち上がりのアニメ用）。"""
    pm = plaster_mat()
    km = K.noisy("koshi", (0.07, 0.065, 0.06), 4.0, 0.2, 0.1, 0.7)
    segs = []
    P = list(pts) + ([pts[0]] if closed else [])
    for i in range(len(P) - 1):
        a, b = Vector(P[i]), Vector(P[i + 1])
        pieces = [(a, b)]
        if gap and gap[0] == i:
            d = (b - a).normalized()
            c = a + d * gap[1]
            pieces = [(a, c - d * gap[2] / 2), (c + d * gap[2] / 2, b)]
        objs = []
        for (p0, p1) in pieces:
            root = K.empty((0, 0, 0), parent, f"{name}_{i}")
            wall_box(p0, p1, z, h, t, pm, f"{name}_{i}_w", root)
            wall_box(p0, p1, z, 0.7, t + 0.04, km, f"{name}_{i}_k", root)
            coping(p0, p1, z + h, t, f"{name}_{i}_c", root)
            objs.append(root)
        segs.append(objs)
    return segs


def house(cx, cy, z, w=11.0, d=8.0, h=3.0, face=0.0, name="house", parent=None):
    """農家ふうの家（白い壁・黒い柱・黒い瓦の寄棟屋根）。"""
    root = K.empty((cx, cy, z), parent, name)
    root.rotation_euler = (0, 0, face * D2R)
    pm = plaster_mat()
    wm = wood_mat()
    K.obj(K.box_mesh(w, d, h), pm, root, (0, 0, h / 2 + 0.4), name=f"{name}_body")
    K.obj(K.box_mesh(w + 0.3, d + 0.3, 0.45), K.noisy("foundation", (0.35, 0.34, 0.32), 1.5, 0.2, 0.3), root, (0, 0, 0.2), name=f"{name}_base")
    for sx in (-1, 1):
        for sy in (-1, 1):
            K.obj(K.box_mesh(0.22, 0.22, h), wm, root, (sx * w / 2, sy * d / 2, h / 2 + 0.4), name=f"{name}_post")
    for k in range(5):
        x = -w / 2 + w * (k + 0.5) / 5
        K.obj(K.box_mesh(0.16, 0.06, h), wm, root, (x, -d / 2 - 0.02, h / 2 + 0.4), name=f"{name}_p")
        K.obj(K.box_mesh(0.16, 0.06, h), wm, root, (x, d / 2 + 0.02, h / 2 + 0.4), name=f"{name}_p")
    K.obj(K.box_mesh(w, 0.08, 0.18), wm, root, (0, -d / 2 - 0.03, h + 0.25), name=f"{name}_beam")
    K.obj(K.box_mesh(w * 0.42, 0.08, h * 0.72), K.noisy("shoji_dark", (0.16, 0.10, 0.06), 3.0, 0.2, 0.1), root, (0, -d / 2 - 0.04, h * 0.36 + 0.4),
          name=f"{name}_door")
    hip_roof(0, 0, h + 0.4, w, d, d * 0.42, over=1.0, sori=0.12, m=tile_mat(), name=f"{name}_roof", parent=root, gable=True)
    return root


def windows(parent, w, d, z, rows=1, n_long=6, n_short=4, size=(0.9, 0.7), name="win"):
    """白い壁に黒い格子窓を並べる。"""
    wm = K.mat("window_dark", (0.03, 0.03, 0.035), 0.5)
    fm = wood_mat()
    for r_ in range(rows):
        zz = z + r_ * 1.4
        for side, n, L in (((0, -1), n_long, w), ((0, 1), n_long, w), ((1, 0), n_short, d), ((-1, 0), n_short, d)):
            for k in range(n):
                a = -L / 2 + L * (k + 0.5) / n
                if side[1]:
                    p = (a, side[1] * (d / 2 + 0.02), zz)
                    sz = (size[0], 0.06, size[1])
                else:
                    p = (side[0] * (w / 2 + 0.02), a, zz)
                    sz = (0.06, size[0], size[1])
                K.obj(K.box_mesh(*sz), wm, parent, p, name=f"{name}")
                for j in range(3):
                    off = (j - 1) * size[0] / 3.2
                    pp = (p[0] + (off if side[1] else 0), p[1] + (0 if side[1] else off), zz)
                    K.obj(K.box_mesh(0.05 if side[1] else 0.08, 0.08 if side[1] else 0.05, size[1]), fm, parent, pp, name=f"{name}_bar")


def yagura(cx, cy, z, w=7.0, d=6.0, h1=3.6, h2=3.0, face=0.0, name="yagura", parent=None, ishiotoshi=True, so_x=None):
    """2階建ての隅櫓。1階の角に石落とし（外へ張り出した出窓、床に蓋）。部品を下から順に返す（組み上がるアニメ用）。"""
    root = K.empty((cx, cy, z), parent, name)
    root.rotation_euler = (0, 0, face * D2R)
    pm = plaster_mat()
    parts = []
    f1 = K.empty((0, 0, 0), root, f"{name}_f1")
    K.obj(K.box_mesh(w, d, h1), pm, f1, (0, 0, h1 / 2), name=f"{name}_w1")
    windows(f1, w, d, h1 * 0.55, 1, 3, 2, name=f"{name}_win1")
    parts.append(f1)
    r1 = hip_roof(0, 0, h1, w, d, 1.3, over=1.1, sori=0.3, name=f"{name}_r1", parent=root)
    parts.append(r1)
    f2 = K.empty((0, 0, h1 + 0.2), root, f"{name}_f2")
    K.obj(K.box_mesh(w * 0.72, d * 0.72, h2), pm, f2, (0, 0, h2 / 2), name=f"{name}_w2")
    windows(f2, w * 0.72, d * 0.72, h2 * 0.5, 1, 2, 2, name=f"{name}_win2")
    parts.append(f2)
    r2 = hip_roof(0, 0, h1 + 0.2 + h2, w * 0.72, d * 0.72, 2.4, over=1.0, sori=0.35, name=f"{name}_r2", parent=root, gable=True)
    parts.append(r2)
    info = {"root": root, "parts": parts}
    if ishiotoshi:
        # 石落とし：-y 側の壁の下に、外へ張り出した箱。下の面は石垣へ向かって斜め。斜めの面の外寄りに口と蓋（下へ開く）
        sx_ = w * 0.18 if so_x is None else so_x
        so = K.empty((sx_, -d / 2, 0.0), root, f"{name}_so")
        bw, bd, bh = 2.4, 0.9, 1.9
        K.obj(K.box_mesh(bw, bd, bh), pm, so, (0, -bd / 2, 0.9 + bh / 2), name=f"{name}_so_box")
        me = bpy.data.meshes.new(f"{name}_so_slope")
        vs = [(-bw / 2, 0, 0.9), (bw / 2, 0, 0.9), (bw / 2, -bd, 0.9), (-bw / 2, -bd, 0.9), (-bw / 2, 0, -0.2), (bw / 2, 0, -0.2)]
        me.from_pydata(vs, [], [(0, 1, 2, 3), (4, 5, 1, 0), (3, 2, 5, 4), (0, 3, 4), (1, 5, 2)])
        me.materials.append(pm)
        sl = bpy.data.objects.new(f"{name}_so_slope", me)
        bpy.context.collection.objects.link(sl)
        sl.parent = so
        ang = math.atan2(1.1, -0.9)                       # 斜めの面の向き（内下 → 外上）
        u0, u1 = 0.35, 0.85                               # 口の位置（斜めの面にそった割合）
        L = math.hypot(0.9, 1.1)

        def on_slope(u, out=0.0):
            return (0, -0.9 * u + out * -0.77, -0.2 + 1.1 * u + out * -0.63)
        c = on_slope((u0 + u1) / 2, 0.015)
        K.obj(K.box_mesh(bw * 0.7, (u1 - u0) * L, 0.02), K.mat("hole_dark", (0.01, 0.01, 0.01), 0.9), so, c, rot=(ang, 0, 0),
              name=f"{name}_so_hole")
        hinge = K.empty(on_slope(u1, 0.05), so, f"{name}_so_hinge")
        hinge.rotation_euler = (ang, 0, 0)
        lid = K.obj(K.box_mesh(bw * 0.74, (u1 - u0) * L + 0.06, 0.06), K.noisy("lid_wood", (0.30, 0.18, 0.09), 3.0, 0.3, 0.2), hinge,
                    (0, -((u1 - u0) * L) / 2, 0.0), name=f"{name}_so_lid")
        K.obj(K.box_mesh(bw + 0.5, bd + 0.5, 0.16), tile_mat(), so, (0, -bd / 2 - 0.1, 0.9 + bh + 0.1), rot=(-12 * D2R, 0, 0),
              name=f"{name}_so_roof")
        info.update(so=so, hinge=hinge, lid=lid, hinge_rest=ang, so_world=(sx_, -d / 2 - 0.9 * (u0 + u1) / 2, -0.2 + 1.1 * (u0 + u1) / 2))
        parts.insert(1, so)
    return info


def rise_parts(parts, f0, f1, drop=4.0):
    """部品を下から順に、上から落として組み上げる（参考元の「櫓が下から組み上がる」）。"""
    n = len(parts)
    for k, p in enumerate(parts):
        fk = int(f0 + (f1 - f0) * k / max(1, n - 1))
        loc = tuple(p.location)
        K.key_scale(p, max(0, fk - 4), 1e-4)
        K.key_loc(p, max(0, fk - 4), (loc[0], loc[1], loc[2] + drop))
        K.key_scale(p, fk - 3, 1.0)
        K.key_loc(p, fk, (loc[0], loc[1], loc[2] - 0.05))
        K.key_loc(p, fk + 2, loc)


def tenshu(cx, cy, z, s=1.0, face=0.0, name="tenshu", parent=None):
    """大天守（白い壁、5重の屋根、千鳥破風・唐破風ふうの三角、てっぺんは入母屋＋金のしゃちほこ）。"""
    root = K.empty((cx, cy, z), parent, name)
    root.rotation_euler = (0, 0, face * D2R)
    root.scale = (s, s, s)
    pm = plaster_mat()
    tiers = [(23, 18, 6.2, 2.4, 1.9), (20.5, 15.5, 4.4, 2.2, 1.7), (17.5, 13, 4.2, 2.2, 1.6), (14, 10.5, 4.0, 2.0, 1.5), (11, 8, 3.8, 4.2, 1.6)]
    zz = 0.0
    tops = []
    for i, (w, d, wh, rh, ov) in enumerate(tiers):
        K.obj(K.box_mesh(w, d, wh), pm, root, (0, 0, zz + wh / 2), name=f"{name}_w{i}")
        windows(root, w, d, zz + wh * 0.55, 1, max(3, int(w / 3.2)), max(2, int(d / 3.2)), size=(1.0, 0.8), name=f"{name}_win{i}")
        last = i == len(tiers) - 1
        r = hip_roof(0, 0, zz + wh, w, d, rh, over=ov, sori=0.45, name=f"{name}_r{i}", parent=root, gable=last)
        tops.append(r)
        # 破風：段ごとに向きと数を変えて、姫路城らしいにぎやかな屋根に
        if i == 0:
            for x in (-w * 0.25, w * 0.25):
                chidori(r, x, -(d / 2 + ov * 0.35), 0.6, 0, 4.2, 2.3, f"{name}_cd0a{x}")
                chidori(r, x, (d / 2 + ov * 0.35), 0.6, 180, 4.2, 2.3, f"{name}_cd0b{x}")
        elif i == 1:
            chidori(r, 0, -(d / 2 + ov * 0.3), 0.5, 0, 6.5, 2.6, f"{name}_cd1a")
            chidori(r, (w / 2 + ov * 0.3), 0, 0.5, -90, 5.0, 2.2, f"{name}_cd1b")
            chidori(r, -(w / 2 + ov * 0.3), 0, 0.5, 90, 5.0, 2.2, f"{name}_cd1c")
        elif i == 2:
            for x in (-w * 0.22, w * 0.22):
                chidori(r, x, -(d / 2 + ov * 0.3), 0.5, 0, 3.6, 2.0, f"{name}_cd2a{x}")
            chidori(r, 0, (d / 2 + ov * 0.3), 0.5, 180, 5.0, 2.2, f"{name}_cd2b")
        elif i == 3:
            chidori(r, 0, -(d / 2 + ov * 0.3), 0.4, 0, 4.0, 2.0, f"{name}_cd3a")
        zz += wh + rh * 0.55
    # しゃちほこ（金）
    gold = K.mat("gold", (0.85, 0.60, 0.15), 0.25)
    w, d = tiers[-1][0], tiers[-1][1]
    ztop = zz - tiers[-1][3] * 0.55 + tiers[-1][3] + 0.4
    for sx in (-1, 1):
        K.obj(K.ellip_mesh(0.35, 0.25, 0.7, 10, 8), gold, root, (sx * (w - d) / 2 * 1.02, 0, ztop + 0.3), rot=(0, sx * 25 * D2R, 0),
              name=f"{name}_shachi")
    info = {"root": root, "height": ztop + 1.0, "tops": tops}
    return info


def town(cx, cy, r_in, r_out, n=200, seed=4, name="town"):
    """城下町（白壁と黒い瓦の小さな家）。"""
    rr = random.Random(seed)
    hm = [plaster_mat("town_wall", (0.62, 0.60, 0.56)), K.noisy("town_wood", (0.20, 0.13, 0.08), 3.0, 0.3, 0.2)]
    tm = tile_mat("town_tile", (0.12, 0.12, 0.13), (0.30, 0.30, 0.30))
    houses = []
    for i in range(n):
        a = rr.uniform(0, 2 * math.pi)
        dd = rr.uniform(r_in, r_out)
        x, y = cx + dd * math.cos(a), cy + dd * math.sin(a)
        w, d, h = rr.uniform(6, 11), rr.uniform(5, 8), rr.uniform(3.0, 5.5)
        ang = rr.choice((0, 90)) + rr.uniform(-4, 4)
        root = K.empty((x, y, 0), None, f"{name}{i}")
        root.rotation_euler = (0, 0, ang * D2R)
        K.obj(K.box_mesh(w, d, h), hm[i % 2], root, (0, 0, h / 2), name=f"{name}{i}_b")
        hip_roof(0, 0, h, w, d, d * 0.35, over=0.5, sori=0.05, th=0.15, m=tm, name=f"{name}{i}_r", parent=root)
        houses.append(root)
    return houses
