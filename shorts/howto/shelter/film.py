"""「核シェルターの作り方」全場面の3D（Blender / bpy）。参考元（0秒博士）と同じく、地面を縦に切った断面図（茶色の土の層）で見せる。
断面は y=0 の面。カメラは手前（-y）から見る。地面の上（z>0）は空と草地、下は土。主人公は赤いT・ジーンズの半ズボン・黄色いヘルメット。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import kit as K  # noqa: E402
from htimeline import Timeline  # noqa: E402

bpy = K.bpy
import bmesh  # noqa: E402
from mathutils import Vector  # noqa: E402

D2R = K.D2R
TL = Timeline(HERE)
SC = None
YELLOW = (1.0, 0.82, 0.05)
ORANGE = (1.0, 0.38, 0.02)
BLUE = (0.15, 0.55, 1.0)
RAD = (0.75, 1.0, 0.12)          # 放射線（黄緑に光る点線）
fr = K.fr
campath = K.campath

# 部屋（中の寸法）：x -3〜3、奥行 y 0〜4、床 -2.9、天井 -0.7。壁の厚さ：はじめ 0.15 → 鉄筋コンクリートで 0.45
RX, RY, RF, RC = 3.0, 4.0, -2.9, -0.7
THIN, THICK = 0.15, 0.45
DEPTH = 14.0                     # 土の断面の奥行き


def lt(i):
    L = SC["lines"][i]
    return L["t"], L["t_end"]


# ---------- 材質 ----------
def soil_layers():
    """土の断面：上から 黒っぽい表土 → 茶色 → 明るい茶 → 灰色がかった深い層（参考元の茶色い層）。"""
    name = "soil_layers"
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.95
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.6
    nz.inputs["Detail"].default_value = 8.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs[1].default_value = -12.0
    mr.inputs[2].default_value = 0.0
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = 'ADD'
    sub = nt.nodes.new("ShaderNodeMath")
    sub.operation = 'SUBTRACT'
    sub.inputs[1].default_value = 0.5
    nt.links.new(nz.outputs["Fac"], sub.inputs[0])
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = 'MULTIPLY'
    mul.inputs[1].default_value = 0.05
    nt.links.new(sub.outputs[0], mul.inputs[0])
    nt.links.new(sep.outputs["Z"], mr.inputs[0])
    nt.links.new(mr.outputs[0], add.inputs[0])
    nt.links.new(mul.outputs[0], add.inputs[1])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = 'CONSTANT'
    stops = [(0.0, (0.20, 0.17, 0.14)), (0.45, (0.30, 0.20, 0.11)), (0.72, (0.38, 0.25, 0.13)), (0.93, (0.16, 0.10, 0.06))]
    cr.elements[0].position, cr.elements[0].color = stops[0][0], (*stops[0][1], 1)
    cr.elements[1].position, cr.elements[1].color = stops[1][0], (*stops[1][1], 1)
    for p, c in stops[2:]:
        e = cr.elements.new(p)
        e.color = (*c, 1)
    nt.links.new(add.outputs[0], ramp.inputs[0])
    # 小石のつぶつぶ
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.inputs["Scale"].default_value = 9.0
    nt.links.new(tc.outputs["Object"], vor.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.blend_type = 'MULTIPLY'
    mix.inputs["Factor"].default_value = 0.35
    nt.links.new(ramp.outputs[0], mix.inputs[6])
    nt.links.new(vor.outputs["Distance"], mix.inputs[7])
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    return m


def M(key):
    tab = {
        "concrete": lambda: K.noisy("concrete", (0.56, 0.56, 0.54), 3.0, 0.08, 0.25, 0.9),
        "thin": lambda: K.noisy("thin_wall", (0.66, 0.64, 0.60), 3.0, 0.06, 0.15, 0.9),
        "floor": lambda: K.noisy("shelter_floor", (0.42, 0.42, 0.42), 4.0, 0.08, 0.1, 0.8),
        "steel": lambda: K.noisy("steel_door", (0.30, 0.32, 0.34), 6.0, 0.08, 0.15, 0.4),
        "mound": lambda: K.noisy("mound_soil", (0.24, 0.16, 0.09), 1.2, 0.25, 0.4, 0.95),
        "ash": lambda: K.mat("ash", (0.55, 0.55, 0.53), 0.9),
        "pipe": lambda: K.noisy("pipe", (0.45, 0.47, 0.50), 6.0, 0.05, 0.1, 0.4),
        "wood": lambda: K.noisy("plank", (0.48, 0.32, 0.17), 3.0, 0.25, 0.2, 0.7),
        "white": lambda: K.mat("white_plastic", (0.85, 0.86, 0.85), 0.4),
        "water": lambda: K.mat("water_tank", (0.20, 0.45, 0.75), 0.3),
        "can": lambda: K.mat("can", (0.70, 0.12, 0.08), 0.35),
        "blanket": lambda: K.noisy("blanket", (0.25, 0.38, 0.22), 6.0, 0.08, 0.1, 0.9),
    }
    return tab[key]()


def hl(name, f_on, f_full, f_off=None, f_gone=None, col=ORANGE, alpha=0.6, strength=2.2):
    alpha = min(alpha, 0.97)
    return K.fade_mat(K.glow(f"hl_{name}", col, strength, alpha), f_on, f_full, f_off, f_gone, f"hl_{name}_{f_on}")


def box(size, loc, m, name="b", parent=None, rot=(0, 0, 0), shadow=True):
    return K.obj(K.box_mesh(*size), m, parent, loc, rot=rot, name=name, shadow=shadow)


def xz_prism(poly, y0, y1, m, name="xzp", hide=False):
    """断面（x, z）の多角形を、奥行き y0〜y1 にのばした柱。"""
    bm = bmesh.new()
    a = [bm.verts.new((x, y0, z)) for x, z in poly]
    b = [bm.verts.new((x, y1, z)) for x, z in poly]
    bm.faces.new(a)
    bm.faces.new(b[::-1])
    n = len(poly)
    for k in range(n):
        bm.faces.new((a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m)
    o = K.obj(me, m, None, (0, 0, 0), name=name)
    if hide:
        o.hide_render = True
        o.display_type = 'WIRE'
    return o


def cutter_box(x0, x1, z0, z1, y0=-1.0, y1=None, name="cut"):
    o = box((x1 - x0, (y1 if y1 is not None else RY + 0.6) - y0, z1 - z0), ((x0 + x1) / 2, (y0 + (y1 if y1 is not None else RY + 0.6)) / 2, (z0 + z1) / 2),
            K.mat("cutter", (1, 0, 1)), name)
    o.hide_render = True
    o.display_type = 'WIRE'
    return o


def subtract(target, cutters):
    for k, c in enumerate(cutters):
        md = target.modifiers.new(f"cut{k}", 'BOOLEAN')
        md.operation = 'DIFFERENCE'
        md.object = c
        md.solver = 'EXACT'


# 入口の通路：はじめはまっすぐの坂道（地面から扉までまっすぐ）。あとで「直角に曲げた」縦穴＋横の通路に作りかえる
SLANT = [(RX + 0.3, RF), (RX + 0.3, RF + 2.05), (RX + 2.12, 0.05), (RX + 6.5, 0.05)]
SHAFT = (RX + 4.0, RX + 5.2)       # 縦穴の x
LPASS = [(RX + 0.3, RF), (SHAFT[1], RF), (SHAFT[1], 0.05), (SHAFT[0], 0.05), (SHAFT[0], RF + 2.05), (RX + 0.3, RF + 2.05)]


def ground_and_soil(cutters):
    """土の断面（手前の面が y=0）と、その上の草地。cutters で部屋・通路の穴をあける。"""
    soil = box((80.0, DEPTH, 14.0), (0, DEPTH / 2, -7.0), soil_layers(), "soil")
    subtract(soil, cutters)
    grass = box((80.0, DEPTH, 0.08), (0, DEPTH / 2, 0.0), K.grass_mat(), "grass_top")
    subtract(grass, cutters)
    far = box((6000, 3000, 0.2), (0, DEPTH + 1500, -0.1), K.grass_mat(), "ground_far")
    _ = far
    # 奥の地面の下（断面の奥の続き）
    return soil, grass


def world(elev=50, az=215, seed=3, flash=None):
    K.daylight(elev=elev, az=az)
    K.clouds(seed=seed)
    K.countryside(seed=seed, keep_out=0, r_max=650, n_fields=90, n_trees=260, center=(0, 760))
    sun = next(o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'SUN')
    return sun


def fill_light(loc, at, energy=2500, size=10.0, col=(1.0, 0.96, 0.9), name="fill"):
    l_ = bpy.data.lights.new(name, 'AREA')
    l_.energy = energy
    l_.size = size
    l_.color = col
    o = bpy.data.objects.new(name, l_)
    bpy.context.collection.objects.link(o)
    o.location = loc
    K.W.aim(o, at)
    return o


def room(thick=False, name="room"):
    """コンクリートの部屋（手前 y=0 で切った断面）。戻り値：壁の部品の list（厚さを変えるアニメ用、原点は部屋の中心）。"""
    t = THICK if thick else THIN
    m = M("concrete") if thick else M("thin")
    root = K.empty((0, 0, 0), None, name)
    parts = []
    # 天井・床・左右の壁・奥の壁（右の壁には扉の口：RF〜RF+2.05）
    parts.append(box((2 * RX + 2 * t, RY + t, t), (0, (RY + t) / 2, RC + t / 2), m, f"{name}_roof", root))
    parts.append(box((2 * RX + 2 * t, RY + t, t), (0, (RY + t) / 2, RF - t / 2), m, f"{name}_floor", root))
    parts.append(box((t, RY + t, RC - RF), (-RX - t / 2, (RY + t) / 2, (RC + RF) / 2), m, f"{name}_lwall", root))
    parts.append(box((t, RY + t, RC - (RF + 2.05)), (RX + t / 2, (RY + t) / 2, (RC + RF + 2.05) / 2), m, f"{name}_rwall_top", root))
    parts.append(box((t, RY - 1.4, 2.05), (RX + t / 2, 1.4 + (RY - 1.4) / 2, RF + 1.025), m, f"{name}_rwall_back", root))
    parts.append(box((2 * RX, t, RC - RF), (0, RY + t / 2, (RC + RF) / 2), m, f"{name}_back", root))
    box((2 * RX - 0.1, RY - 0.1, 0.04), (0, RY / 2, RF + 0.02), M("floor"), f"{name}_floorfin", root)
    # 天井の明かり
    K.obj(K.box_mesh(0.9, 0.3, 0.06), K.glow("lamp", (1.0, 0.92, 0.75), 6.0), root, (0, RY * 0.5, RC - 0.04), name=f"{name}_lamp", shadow=False)
    lt_ = bpy.data.lights.new(f"{name}_lampl", 'POINT')
    lt_.energy = 250
    lt_.color = (1.0, 0.9, 0.75)
    lo = bpy.data.objects.new(f"{name}_lampl", lt_)
    bpy.context.collection.objects.link(lo)
    lo.location = (0, RY * 0.4, RC - 0.4)
    # 鉄筋（断面に見える赤茶の点）
    if thick:
        rb = K.mat("rebar", (0.45, 0.18, 0.08), 0.5)
        pts = []
        for k in range(13):
            x = -RX - t + 0.12 + (2 * RX + 2 * t - 0.24) * k / 12
            pts += [(x, RC + t - 0.1), (x, RC + 0.1), (x, RF - t + 0.1), (x, RF - 0.1)]
        for k in range(7):
            z = RF + (RC - RF) * k / 6
            pts += [(-RX - t + 0.1, z), (-RX - 0.1, z)]
            if z > RF + 2.1:
                pts += [(RX + 0.1, z), (RX + t - 0.1, z)]
        for x, z in pts:
            K.obj(K.cyl_mesh(0.035, 0.035, 0.03, 8), rb, root, (x, -0.012, z), rot=(90 * D2R, 0, 0), name=f"{name}_rebar", shadow=False)
    return root, parts


def blast_door(closed=True, name="door"):
    """鋼鉄の防爆扉（右の壁の口。奥の端の縦の軸で回る）。"""
    hinge = K.empty((RX + 0.08, 1.4, RF), None, f"{name}_hinge")
    d = box((0.16, 1.38, 2.0), (0, -0.69, 1.0), M("steel"), name, hinge)
    for k in range(3):
        box((0.04, 1.2, 0.08), (0.1, -0.69, 0.4 + 0.6 * k), K.mat("door_band", (0.18, 0.19, 0.2), 0.4), f"{name}_band", d)
    K.obj(K.cyl_mesh(0.12, 0.12, 0.06, 16), K.mat("wheel", (0.7, 0.15, 0.1), 0.4), d, (0.1, 0.0, 0.1), rot=(0, 90 * D2R, 0), name=f"{name}_wheel")
    hinge.rotation_euler = (0, 0, 0 if closed else -95 * D2R)
    return hinge, d


def mound(name="mound"):
    """部屋の上の盛り土（高さ 1m）。"""
    return xz_prism([(-6.0, 0.0), (6.0, 0.0), (4.6, 1.0), (-4.6, 1.0)], 0.0, DEPTH, M("mound"), name)


def text3d(s, loc, size=0.6, m=None, name="txt"):
    cu = bpy.data.curves.new(name, 'FONT')
    cu.body = s
    cu.size = size
    cu.align_x = 'CENTER'
    cu.extrude = 0.02
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m or K.glow("txt_white", (1, 1, 1), 3.0))
    o.location = loc
    o.rotation_euler = (90 * D2R, 0, 0)
    o.visible_shadow = False
    return o


def ash_fall(n, f0, f1, xr=(-14, 14), yr=(0.3, 9.0), land=None, seed=1, name="ash", glow_m=None):
    """死の灰：空から降ってきて地面に積もる。land(x)＝その x の地面の高さ。"""
    r = random.Random(seed)
    m = glow_m or ash_mat()
    obs = []
    for i in range(n):
        x, y = r.uniform(*xr), r.uniform(*yr)
        s = r.uniform(0.05, 0.1)
        o = K.obj(K.ellip_mesh(s, s, s * 0.8, 6, 4), m, None, (x, y, 18), name=f"{name}{i}", shadow=False)
        t0 = f0 + r.uniform(0, (f1 - f0) * 0.75)
        zl = (land(x) if land else 0.0) + s * 0.6
        K.key_loc(o, 1, (x, y, 30))
        K.key_loc(o, int(t0), (x + r.uniform(-1, 1), y, 16))
        K.key_loc(o, int(t0) + r.randint(30, 50), (x, y, zl))
        obs.append(o)
    return obs


def ash_mat(strength=1.2):
    """灰：灰色で、うすく黄緑に光る（放射性）。"""
    m = bpy.data.materials.get("ash_glow")
    if m:
        return m
    m = K.mat("ash_glow", (0.55, 0.56, 0.50), 0.9, emit=RAD, emit_strength=strength)
    return m


def rays(paths, f0, f1, name="ray", speed=5.0, width=0.07):
    """放射線：黄緑に光る点線が、道すじにそって流れる。"""
    m = K.glow("ray_m", RAD, 6.0)
    for k, p in enumerate(paths):
        K.flow_arrow(p, m, f0 + 2 * k, f1, width=width, dash=0.45, gap=0.35, speed=speed, head=0.25, f_grow=10, name=f"{name}{k}")


def hero_in_room(look=None, loc=(-1.2, 1.4, RF), face=0, name="hero"):
    h = K.Person(loc, face, look or K.HERO_HELMET, name=name)
    h.stand(1)
    return h


def standard_cam_front(z=-1.2, y=-17.0, x=0.8, lens=26):
    return (x, y, z), (x, 2.0, -1.4), lens


# ============================ 1) 穴を掘って、部屋を埋める ============================
def s01_hole(nf):
    sun = world()
    _ = sun
    T = SC["dur"]
    a0, _ = lt(0)
    a1, _ = lt(1)
    a2, _ = lt(2)
    a3, _ = lt(3)
    t_dig = a0 + 0.1
    # 穴（部屋の外まわりと同じ大きさ）：地面から下へ、いっきに掘れる
    hole = cutter_box(-RX - THIN - 0.02, RX + THIN + 0.02, RF - THIN - 0.02, 0.2, name="cut_hole")
    room_cut = cutter_box(-RX - THIN - 0.02, RX + THIN + 0.02, RF - THIN - 0.02, RC + THIN + 0.02, name="cut_room")
    slant = xz_prism(SLANT, -1.0, 1.6, K.mat("cutter", (1, 0, 1)), "cut_slant", hide=True)
    soil, grass = ground_and_soil([hole, room_cut, slant])
    _ = (soil, grass)
    hz_full = (RF - THIN - 0.02 + 0.2) / 2
    hy = (RY + 0.6 - 1.0) / 2
    h_tot = 0.2 - (RF - THIN - 0.02)

    def hole_state(f, u):
        """u=0：深さ 3%（地面より上で何も切らない）、u=1：部屋の底まで。"""
        sz = 0.03 + 0.97 * u
        K.key_scale(hole, f, (1, 1, sz))
        K.key_loc(hole, f, (0, hy, 0.2 - h_tot * sz / 2))
    _ = hz_full
    hole_state(1, 0.0)
    hole_state(fr(t_dig), 0.0)
    hole_state(fr(t_dig + 0.45), 1.0)
    t_drop = a1 + 0.05
    hole_state(fr(t_drop + 0.45), 1.0)
    hole_state(fr(t_drop + 0.6), 0.0)
    # 部屋の穴と坂道の穴は、部屋が入るまで空の上へどけておく
    rc0 = tuple(room_cut.location)
    K.key_loc(room_cut, 1, (rc0[0], rc0[1], rc0[2] + 60))
    K.key_loc(room_cut, fr(t_drop + 0.4), (rc0[0], rc0[1], rc0[2] + 60))
    K.key_loc(room_cut, fr(t_drop + 0.41), rc0)
    K.key_loc(slant, 1, (0, 0, 60))
    K.key_loc(slant, fr(t_drop + 0.55), (0, 0, 60))
    K.key_loc(slant, fr(t_drop + 0.56), (0, 0, 0))
    # 土が飛び散る
    r = random.Random(2)
    dm = K.noisy("clod", (0.30, 0.20, 0.11), 2.0, 0.3, 0.3)
    for k in range(40):
        c = K.obj(K.ellip_mesh(0.25, 0.22, 0.2, 8, 6), dm, None, (0, 0, -5), name=f"clod{k}")
        p0 = (r.uniform(-2.5, 2.5), r.uniform(0.3, 3.5), 0.0)
        p1 = (p0[0] * 3 + r.uniform(-4, 4), r.uniform(0.5, 8.0), 0.1)
        K.key_scale(c, fr(t_dig) - 1, 1e-4)
        K.key_scale(c, fr(t_dig), r.uniform(0.6, 1.4))
        K.projectile(c, fr(t_dig + r.uniform(0, 0.25)), fr(t_dig + 0.8), p0, p1, arc=r.uniform(2.5, 6.0), align=False)
    for k in range(6):
        K.smoke_puffs((r.uniform(-3, 3), r.uniform(0.5, 3.5), 0.3), fr(t_dig), n=4, seed=10 + k, col=(0.55, 0.45, 0.32), size=2.0, rise=2.5,
                      life=24, spread=1.5, alpha=0.85, name=f"dig{k}")
    # 部屋（うすい壁）が空から落ちてきて、穴へストン
    rr, parts = room(False, "room")
    K.key_loc(rr, 1, (0, 0, 40))
    K.key_loc(rr, fr(t_drop), (0, 0, 22))
    K.key_loc(rr, fr(t_drop + 0.35), (0, 0, -0.1))
    K.key_loc(rr, fr(t_drop + 0.42), (0, 0, 0.05))
    K.key_loc(rr, fr(t_drop + 0.48), (0, 0, 0))
    for k in range(5):
        K.smoke_puffs((-3 + 1.5 * k, 1.5, 0.2), fr(t_drop + 0.5), n=3, seed=30 + k, col=(0.55, 0.45, 0.32), size=1.8, rise=1.5, life=18,
                      spread=1.0, alpha=0.85, name=f"fill{k}")
    # 主人公：穴の横でスコップをかまえる → 坂道を下りて部屋へ → ガッツポーズ → 空を見上げる
    hero = K.Person((-4.8, 1.2, 0.0), 30, K.HERO_HELMET, name="hero")
    sh = K.empty(name="shovel")
    K.obj(K.cyl_mesh(0.025, 0.025, 1.1, 8), M("wood"), sh, (0, 0, -0.55), name="shovel_h")
    K.obj(K.box_mesh(0.25, 0.03, 0.3), M("pipe"), sh, (0, 0, -0.65), name="shovel_b")
    hero.hold(sh, "R", (0, 0.02, 0), (0, 0, 0))
    hero.stand(1, shR=(40, 10), elR=40, shL=(40, -10), elL=40)
    hero.pose(fr(t_dig), shR=(120, 10), elR=20, shL=(110, -10), elL=20, spine=-25)
    hero.pose(fr(t_dig + 0.3), shR=(20, 10), elR=20, shL=(20, -10), elL=20, spine=-5)
    hero.pose(fr(a1), shL=(100, 70), shR=(100, 70), elL=5, elR=5)
    K.key_scale(sh, fr(a1) - 1, 1.0)
    K.key_scale(sh, fr(a1), 1e-4)
    path = [(-4.8, 1.2, 0.0), (RX + 6.0, 0.8, 0.0), (RX + 2.4, 0.8, -0.1), (RX + 0.4, 0.8, RF), (1.0, 0.9, RF)]
    hero.walk(fr(a1 + 0.3), fr(a2 + 0.6), path, run=True)
    hero.place(fr(a2 + 0.65), (1.0, 0.9, RF), 0)
    hero.pose(fr(a2 + 0.7), shL=(15, 10), shR=(150, 20), elR=95)
    hero.pose(fr(a3 - 0.1), shR=(165, 15), elR=70)
    hero.pose(fr(a3 + 0.5), shL=(10, 8), shR=(10, 8), elL=12, elR=12, neck=-30)                # 上を見上げる
    hero.pose(nf, shL=(135, 45), shR=(135, 45), elL=120, elR=120, neck=-20, spine=6)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    # 核ミサイル：空を左から右の奥へ
    mis = K.empty(name="missile")
    K.obj(K.cyl_mesh(0.6, 0.6, 7.0, 12), K.mat("missile", (0.85, 0.85, 0.82), 0.4), mis, (0, -3.5, 0), rot=(-90 * D2R, 0, 0), name="mis_body")
    K.obj(K.cyl_mesh(0.6, 0.0, 1.8, 12), K.mat("missile_nose", (0.75, 0.1, 0.08), 0.4), mis, (0, 3.5, 0), rot=(-90 * D2R, 0, 0), name="mis_nose")
    K.obj(K.ellip_mesh(0.7, 2.5, 0.7, 10, 6), K.glow("exhaust", (1.0, 0.7, 0.3), 12.0), mis, (0, -5.5, 0), name="mis_fire", shadow=False)
    t_m = a3 + 0.2
    K.show(mis, fr(t_m))
    K.projectile(mis, fr(t_m), fr(T), (180, 500, 160), (-260, 700, 40), arc=30, align=True)
    for k in range(18):
        K.smoke_puffs((180 - 25 * k, 500 + 11 * k, 160 - 4 * k), fr(t_m + 0.1 * k), n=2, seed=60 + k, col=(0.85, 0.85, 0.85), size=6.0, rise=2.0,
                      life=40, spread=2.0, alpha=0.8, name=f"trail{k}")
    fill_light((0.0, -24.0, -1.0), (0, 0, -1.5), 3000, 16.0)
    keys = [(0.0, (-3.0, -4.0, 1.7), (-4.6, 1.4, 1.3), 30),
            (0.3, (-2.0, -7.0, 2.0), (-2.5, 1.2, 0.2), 28),
            (a1, (0.5, -16.0, 1.5), (0.5, 2.0, -0.8), 26),
            (a2 + 0.6, (1.0, -15.5, -1.0), (0.6, 2.0, -1.6), 26),
            (a3 + 0.3, (1.0, -15.0, -0.6), (0.8, 2.0, -0.8), 26),
            (T, (1.0, -14.0, 0.2), (20.0, 300.0, 80.0), 24)]
    campath(keys, nf, shake=0.02)


# ============================ 2) 爆風 → 鉄筋コンクリート → 防爆扉 ============================
def s02_blast(nf):
    sun = world()
    T = SC["dur"]
    a4, _ = lt(4)
    a5, _ = lt(5)
    a6, e6 = lt(6)
    a7, _ = lt(7)
    a8, _ = lt(8)
    # 光る爆発（遠く）とキノコ雲
    C = Vector((-420.0, 900.0, 0.0))
    fl = K.obj(K.ellip_mesh(1, 1, 1, 24, 16), K.fade_mat(K.glow("flash", (1.0, 0.95, 0.85), 60.0, 0.99), fr(a4), fr(a4) + 2, fr(a4) + 12, fr(a4) + 30, "flash_f"),
               None, tuple(C + Vector((0, 0, 40))), name="flash", shadow=False)
    K.key_scale(fl, fr(a4) - 1, 1e-3)
    K.key_scale(fl, fr(a4) + 4, 140)
    K.key_scale(fl, fr(a4) + 30, 200)
    se = sun.data.energy
    sun.data.keyframe_insert("energy", frame=fr(a4) - 1)
    sun.data.energy = se * 6
    sun.data.keyframe_insert("energy", frame=fr(a4) + 2)
    sun.data.energy = se
    sun.data.keyframe_insert("energy", frame=fr(a4) + 20)
    cm = K.smoke_mat("mush", (0.62, 0.55, 0.50), 0.95)
    core = K.glow("mush_core", (1.0, 0.45, 0.12), 12.0, 0.9)
    r = random.Random(5)
    for k in range(26):                     # 柱
        z = 20 + k * 14
        o = K.obj(K.ellip_mesh(1, 1, 1, 12, 8), cm if k > 4 else core, None, tuple(C + Vector((0, 0, z * 0.2))), name=f"stem{k}", shadow=False)
        K.key_scale(o, fr(a4) + 2, 1e-3)
        K.key_loc(o, fr(a4) + 2, tuple(C + Vector((0, 0, 10))))
        K.key_scale(o, fr(T), 34 + r.uniform(-5, 5))
        K.key_loc(o, fr(T), tuple(C + Vector((r.uniform(-8, 8), r.uniform(-8, 8), z))))
    for k in range(30):                     # かさ
        a = k / 30 * 2 * math.pi
        o = K.obj(K.ellip_mesh(1, 1, 0.6, 12, 8), cm if k % 3 else core, None, tuple(C), name=f"cap{k}", shadow=False)
        K.key_scale(o, fr(a4) + 4, 1e-3)
        K.key_loc(o, fr(a4) + 4, tuple(C + Vector((0, 0, 30))))
        rad = 80 + r.uniform(-15, 15)
        K.key_scale(o, fr(T), 70 + r.uniform(-10, 10))
        K.key_loc(o, fr(T), tuple(C + Vector((rad * math.cos(a), rad * math.sin(a), 380 + r.uniform(-30, 30)))))
    # 地面の上：家と木。爆風（土けむりの壁）が左から右へ吹き抜け、家と木が飛ぶ
    hut = K.empty((-10.0, 6.0, 0.0), None, "hut")
    box((5.0, 4.0, 2.6), (0, 0, 1.3), K.noisy("hut_wall", (0.72, 0.66, 0.55), 2.0, 0.08, 0.05), "hut_body", hut)
    box((5.8, 4.8, 0.3), (0, 0, 2.8), K.noisy("hut_roof", (0.25, 0.20, 0.18), 3.0, 0.2, 0.2), "hut_roof", hut)
    trees = []
    for k, (x, y, kind) in enumerate([(-16, 4, 5), (8, 5, 1), (14, 3, 6), (-5, 10, 2), (18, 9, 0)]):
        trees.append(K.tree(x, y, kind, 1.0, k * 50 * D2R, name=f"tr{k}"))
    t_w = a5 - 0.3
    for k in range(40):
        y = 0.3 + k * 0.6
        o = K.obj(K.ellip_mesh(1, 1, 1, 10, 8), K.smoke_mat("blast_dust", (0.62, 0.52, 0.40), 0.9), None, (-60, y, 1.5), name=f"wave{k}",
                  shadow=False)
        K.key_scale(o, fr(t_w) - 1, 1e-3)
        K.key_scale(o, fr(t_w), 3.0 + r.uniform(0, 1.5))
        K.key_loc(o, fr(t_w), (-45 + r.uniform(-2, 2), y, r.uniform(1.0, 4.0)))
        K.key_loc(o, fr(t_w + 1.6), (60 + r.uniform(-2, 2), y, r.uniform(1.0, 5.0)))
        K.key_scale(o, fr(t_w + 1.6), 4.5)
        K.key_scale(o, fr(t_w + 1.7), 1e-3)
    def x_at(t):
        return -45 + 105 * (t - t_w) / 1.6
    th = t_w + (-10 + 45) / 105 * 1.6
    for ch in [hut]:
        K.key_loc(ch, fr(th), (-10, 6, 0))
        K.key_rot(ch, fr(th), (0, 0, 0))
        K.key_loc(ch, fr(th + 0.8), (30, 8, 9))
        K.key_rot(ch, fr(th + 0.8), (0.8, -2.4, 0.6))
    for tr in trees:
        tt = t_w + (tr.location.x + 45) / 105 * 1.6
        K.key_rot(tr, fr(tt), tuple(tr.rotation_euler))
        K.key_rot(tr, fr(tt + 0.25), (0, 75 * D2R, tr.rotation_euler.z))
    _ = x_at
    # 地面の下：部屋の壁が うすい → 分厚い鉄筋コンクリートに。入口に鋼鉄の扉
    room_cut = cutter_box(-RX - THIN - 0.02, RX + THIN + 0.02, RF - THIN - 0.02, RC + THIN + 0.02, name="cut_room")
    slant = xz_prism(SLANT, -1.0, 1.6, K.mat("cutter", (1, 0, 1)), "cut_slant", hide=True)
    soil, grass = ground_and_soil([room_cut, slant])
    _ = (soil, grass)
    t_rc = a6 + 1.3
    thin_r, thin_p = room(False, "thin")
    thick_r, thick_p = room(True, "thick")
    K.key_scale(thin_r, fr(t_rc) - 1, 1.0)
    K.key_scale(thin_r, fr(t_rc), 1e-4)
    K.show(thick_r, fr(t_rc))
    sx = (RX + THICK + 0.02) / (RX + THIN + 0.02)
    sz = (RC - RF + 2 * THICK + 0.04) / (RC - RF + 2 * THIN + 0.04)
    K.key_scale(room_cut, fr(t_rc) - 1, 1.0)
    K.key_scale(room_cut, fr(t_rc), (sx, 1.0, sz))
    # 鉄筋の格子（オレンジ）が先に出て、コンクリートが流しこまれる
    rbm = hl("rebar", fr(a6 + 0.5), fr(a6 + 0.7), fr(e6 + 0.3), fr(e6 + 0.6), ORANGE, 0.97, 4.0)
    for k in range(9):
        x = -RX - THICK / 2 + (2 * RX + THICK) * k / 8
        K.poly_curve([(x, -0.03, RF - THICK / 2), (x, -0.03, RC + THICK / 2)], 0.025, rbm, f"rb_v{k}")
    for k in range(5):
        z = RF - THICK / 2 + (RC - RF + THICK) * k / 4
        K.poly_curve([(-RX - THICK / 2, -0.03, z), (RX + THICK / 2, -0.03, z)], 0.025, rbm, f"rb_h{k}")
    shell_hl = box((2 * RX + 2 * THICK + 0.1, 0.05, RC - RF + 2 * THICK + 0.1), (0, -0.05, (RC + RF) / 2),
                   hl("shell", fr(t_rc), fr(t_rc + 0.15), fr(e6 + 0.4), fr(e6 + 0.7)), "shell_hl", shadow=False)
    _ = shell_hl
    door_h, door = blast_door(closed=False)
    K.key_rot(door_h, 1, (0, 0, -95 * D2R))
    K.show(door_h, fr(a7))
    K.key_rot(door_h, fr(a7 + 0.6), (0, 0, -95 * D2R))
    K.key_rot(door_h, fr(a7 + 1.1), (0, 0, 0))
    K.obj(K.box_mesh(0.22, 1.42, 2.06), hl("door", fr(a7 + 0.1), fr(a7 + 0.3), fr(a8 + 0.9), fr(a8 + 1.2)), door, (0, 0, 0), name="door_hl",
          shadow=False)
    K.marker("door", (0.1, 0, 0), door)
    # 爆風が通路から入ってきても、扉はびくともしない（ドン！ゆれる）
    for k in range(10):
        o = K.obj(K.ellip_mesh(1, 1, 1, 10, 8), K.smoke_mat("tun_dust", (0.62, 0.52, 0.40), 0.85), None, (RX + 6, 0.8, 0.5), name=f"tw{k}",
                  shadow=False)
        t0 = a8 + 0.05 + 0.03 * k
        K.key_scale(o, fr(t0) - 1, 1e-3)
        K.key_scale(o, fr(t0), 0.6)
        K.key_loc(o, fr(t0), (RX + 6.0, 0.8, 0.3))
        K.key_loc(o, fr(t0 + 0.35), (RX + 0.6 + 0.1 * k, 0.8, RF + 1.0 + 0.05 * k))
        K.key_scale(o, fr(t0 + 0.35), 1.2)
        K.key_scale(o, fr(t0 + 0.6), 1e-3)
    hero = hero_in_room(loc=(-1.5, 1.4, RF), face=0)
    hero.pose(fr(a4) + 2, shL=(150, 40), shR=(150, 40), elL=120, elR=120, neck=10, spine=8)    # 頭をかかえる
    hero.pose(fr(a6), shL=(150, 40), shR=(150, 40), elL=120, elR=120, neck=10, spine=8)
    hero.pose(fr(t_rc + 0.3), shL=(15, 10), shR=(150, 20), elR=95, neck=0, spine=0)
    hero.pose(fr(a8 + 0.6), shL=(10, 10), shR=(10, 10), elL=10, elR=10)
    hero.pose(nf, shL=(10, 10), shR=(160, 20), elR=60)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    fill_light((0.0, -24.0, -1.0), (0, 0, -1.5), 3000, 16.0)
    cut1 = a6 - 0.05
    cut2 = a7 + 0.1
    keys = [(0.0, (-2.0, -20.0, 6.0), (-120.0, 400.0, 60.0), 26),
            (a5, (-4.0, -24.0, 5.0), (-10.0, 50.0, 8.0), 24),
            (cut1 - 0.02, (2.0, -24.0, 4.0), (5.0, 40.0, 5.0), 24),
            (cut1, (0.8, -17.0, -1.3), (0.8, 2.0, -1.6), 26),
            (cut2 - 0.02, (1.4, -15.5, -1.3), (1.2, 2.0, -1.6), 27),
            (cut2, (RX + 3.6, -3.2, RF + 1.6), (RX + 0.1, 0.9, RF + 1.0), 26),
            (a8 + 0.5, (RX + 3.8, -3.6, RF + 1.7), (RX + 0.1, 0.9, RF + 1.0), 26),
            (T, (RX + 3.6, -5.5, RF + 2.2), (RX - 0.5, 0.9, RF + 1.0), 26)]
    campath(keys, nf, shake=0.03, cuts=[cut1, cut2])


# ============================ 3) 死の灰 → 1mの土 ============================
def s03_soil(nf):
    world()
    T = SC["dur"]
    a9, _ = lt(9)
    a10, _ = lt(10)
    a11, _ = lt(11)
    a12, _ = lt(12)
    a13, _ = lt(13)
    room_cut = cutter_box(-RX - THICK - 0.02, RX + THICK + 0.02, RF - THICK - 0.02, RC + THICK + 0.02, name="cut_room")
    slant = xz_prism(SLANT, -1.0, 1.6, K.mat("cutter", (1, 0, 1)), "cut_slant", hide=True)
    ground_and_soil([room_cut, slant])
    room(True, "room")
    blast_door(True)
    # 盛り土：空から落ちてきて、ドスン
    t_m = a12 + 1.2
    mo = mound()
    K.key_loc(mo, 1, (0, 0, 30))
    K.key_loc(mo, fr(t_m), (0, 0, 14))
    K.key_loc(mo, fr(t_m + 0.3), (0, 0, -0.08))
    K.key_loc(mo, fr(t_m + 0.36), (0, 0, 0.04))
    K.key_loc(mo, fr(t_m + 0.42), (0, 0, 0))
    xz_prism([(-6.05, -0.02), (6.05, -0.02), (4.62, 1.02), (-4.62, 1.02)], -0.08, -0.04,
             hl("mound", fr(t_m + 0.3), fr(t_m + 0.4), fr(a13 + 1.2), fr(a13 + 1.5)), "mound_hl")
    for k in range(6):
        K.smoke_puffs((-5 + 2 * k, 1.0, 0.4), fr(t_m + 0.35), n=3, seed=20 + k, col=(0.45, 0.35, 0.24), size=1.8, rise=1.2, life=18,
                      spread=1.0, alpha=0.85, name=f"md{k}")
    # 寸法「1m」（白いかぎ線と字）
    wm = K.fade_mat(K.glow("dim_white", (1, 1, 1), 4.0, 0.97), fr(t_m + 0.5), fr(t_m + 0.6), None, None, "dim_f")
    K.poly_curve([(-5.2, -0.1, 0.0), (-5.7, -0.1, 0.0), (-5.7, -0.1, 1.0), (-5.2, -0.1, 1.0)], 0.03, wm, "dim")
    tx = text3d("1m", (-6.6, -0.12, 0.3), 0.55, wm, "dim_txt")
    _ = tx
    # 死の灰が降って、地面（と盛り土）に積もる
    land = lambda x: (min(1.0, max(0.0, (6.0 - abs(x)) / 1.4)) if abs(x) < 6.0 else 0.0)   # noqa: E731
    ash_fall(110, fr(a9), fr(a9 + 2.2), land=None, seed=3, name="ashA")
    am = ash_mat()
    am2 = K.mat("ash_glow2", (0.55, 0.56, 0.50), 0.9, emit=RAD, emit_strength=1.2)
    obs = ash_fall(40, fr(t_m + 0.4), fr(t_m + 0.9), xr=(-4.5, 4.5), land=land, seed=9, name="ashB", glow_m=am2)
    for o in obs:
        K.show(o, fr(t_m + 0.4))
    _ = am
    # 放射線：灰から下へ。土をかぶせる前は、うすい土とコンクリートの屋根を通りぬけて部屋の中まで → 盛り土のあとは、土の中で止まる
    p_before = [[(x, 0.5, 0.1), (x + 0.3, 0.5, RF + 0.6)] for x in (-2.4, -1.2, 0.0, 1.2, 2.4)]
    rays(p_before, fr(a10 + 0.1), fr(t_m + 0.25), "rayA", speed=6.0)
    p_after = [[(x, 0.5, 1.15), (x + 0.1, 0.5, 0.25 - 0.08 * (k % 3))] for k, x in enumerate((-3.2, -1.6, 0.0, 1.6, 3.2))]
    rays(p_after, fr(t_m + 0.6), nf, "rayB", speed=2.5)
    hero = hero_in_room(loc=(-0.6, 1.4, RF), face=0)
    hero.pose(fr(a11 + 0.2), shL=(150, 40), shR=(150, 40), elL=120, elR=120, neck=-20, spine=8)
    hero.pose(fr(t_m + 0.5), shL=(150, 40), shR=(150, 40), elL=120, elR=120, neck=-20, spine=8)
    hero.pose(fr(a13 + 0.3), shL=(15, 10), shR=(150, 20), elR=95, neck=-5, spine=0)
    hero.pose(nf, shL=(10, 10), shR=(160, 20), elR=60)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    fill_light((0.0, -24.0, -1.0), (0, 0, -1.5), 3000, 16.0)
    keys = [(0.0, (0.5, -22.0, 4.0), (0.0, 3.0, 2.0), 26),
            (a10, (0.5, -19.0, 1.0), (0.0, 2.0, -0.6), 26),
            (a11 + 0.5, (0.2, -15.0, -0.8), (0.0, 2.0, -1.4), 27),
            (a12, (0.5, -18.0, 0.8), (0.0, 2.0, -0.4), 26),
            (t_m + 0.6, (-1.5, -19.0, 0.8), (-0.6, 2.0, -0.2), 26),
            (T, (-1.0, -18.5, 0.4), (-0.3, 2.0, -0.6), 26)]
    campath(keys, nf, shake=0.02)


# ============================ 4) 曲がった入口 ============================
def s04_entrance(nf):
    world()
    T = SC["dur"]
    a14, _ = lt(14)
    a15, _ = lt(15)
    a16, _ = lt(16)
    a17, _ = lt(17)
    room_cut = cutter_box(-RX - THICK - 0.02, RX + THICK + 0.02, RF - THICK - 0.02, RC + THICK + 0.02, name="cut_room")
    slant = xz_prism(SLANT, -1.0, 1.6, K.mat("cutter", (1, 0, 1)), "cut_slant", hide=True)
    lp = xz_prism(LPASS, -1.0, 1.6, K.mat("cutter", (1, 0, 1)), "cut_L", hide=True)
    ground_and_soil([room_cut, slant, lp])
    room(True, "room")
    blast_door(True)
    mound()
    # 灰（入口のまわり）
    ash_fall(70, 1, 2, xr=(RX + 0.5, RX + 12), yr=(0.3, 6.0), seed=21, name="ashE")
    ash_fall(50, 1, 2, xr=(-12, -6.5), yr=(0.3, 6.0), seed=22, name="ashW")
    # まっすぐの坂道 → 直角に曲げた通路（縦穴＋横の通路）に作りかえる
    t_c = a16 + 0.6
    K.key_loc(lp, 1, (0, 0, -60))
    K.key_loc(lp, fr(t_c + 0.2), (0, 0, -60))
    K.key_loc(lp, fr(t_c + 0.21), (0, 0, 0))
    K.key_loc(slant, 1, (0, 0, 0))
    K.key_loc(slant, fr(t_c), (0, 0, 0))
    K.key_loc(slant, fr(t_c + 0.4), (0, 0, 6.0))
    K.key_loc(slant, fr(t_c + 0.41), (0, 0, 60.0))
    # 新しい通路のふちを、オレンジでなぞる
    om = hl("lpass", fr(t_c + 0.2), fr(t_c + 0.35), fr(a17 + 1.6), fr(a17 + 2.0), ORANGE, 0.97, 4.0)
    K.poly_curve([(x, -0.05, z) for x, z in LPASS], 0.05, om, "lpass_line", cyclic=True)
    for k in range(4):
        K.smoke_puffs((RX + 1.5 + 1.2 * k, 0.6, RF + 1.0 + 0.6 * k), fr(t_c), n=3, seed=40 + k, col=(0.45, 0.35, 0.24), size=1.0, rise=0.6,
                      life=14, spread=0.6, alpha=0.85, name=f"lpd{k}")
    # 縦穴のはしご
    lad = K.ladder(3.1, 0.5, "lad")
    lad.location = ((SHAFT[0] + SHAFT[1]) / 2, 1.2, RF)
    K.show(lad, fr(t_c + 0.25))
    # 放射線：坂道ではまっすぐ扉まで届く → 曲げたあとは、縦穴の底と曲がり角で止まる
    dx, dz = SLANT[0][0] - (RX + 6.3), RF + 1.0 - 0.6
    p1 = [[(RX + 6.3 + 0.2 * k, 0.7, 0.6 + 0.25 * k), (RX + 0.35, 0.7, RF + 0.8 + 0.25 * k)] for k in range(3)]
    _ = (dx, dz)
    rays(p1, fr(a15), fr(t_c), "rayS", speed=7.0)
    p2 = [[(SHAFT[0] + 0.3 + 0.3 * k, 0.7, 1.4), (SHAFT[0] + 0.3 + 0.3 * k, 0.7, RF + 0.3)] for k in range(3)]
    p2 += [[(SHAFT[1] + 1.2, 0.7, 1.4), (SHAFT[0] + 0.6, 0.7, RF + 0.9)]]
    rays(p2, fr(t_c + 0.4), nf, "rayL", speed=4.0)
    # 曲がり角に「×」（止まる）
    xm = hl("xmark", fr(a17 + 0.2), fr(a17 + 0.35), None, None, (1.0, 0.25, 0.15), 0.97, 5.0)
    cx_, cz_ = SHAFT[0] - 0.3, RF + 1.0
    K.poly_curve([(cx_ - 0.35, -0.08, cz_ - 0.35), (cx_ + 0.35, -0.08, cz_ + 0.35)], 0.06, xm, "x1")
    K.poly_curve([(cx_ - 0.35, -0.08, cz_ + 0.35), (cx_ + 0.35, -0.08, cz_ - 0.35)], 0.06, xm, "x2")
    hero = hero_in_room(loc=(1.6, 1.4, RF), face=-90)
    hero.pose(fr(a15 + 0.4), shL=(30, 30), shR=(30, 30), elL=20, elR=20, spine=-5)
    hero.pose(fr(a17 + 0.4), shL=(15, 10), shR=(150, 20), elR=95)
    hero.pose(nf, shR=(165, 15), elR=70)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    fill_light((4.0, -20.0, -1.0), (4.0, 0, -1.5), 3000, 16.0)
    keys = [(0.0, (5.0, -16.0, 0.5), (5.5, 2.0, -0.6), 26),
            (a15, (5.5, -15.0, 0.0), (5.8, 2.0, -0.9), 26),
            (a16, (6.0, -16.0, 0.0), (6.0, 2.0, -0.9), 26),
            (a17, (5.8, -15.0, -0.4), (6.0, 2.0, -1.2), 27),
            (T, (5.2, -15.5, -0.2), (5.6, 2.0, -1.1), 27)]
    campath(keys, nf, shake=0.02)


# ============================ 5) 換気フィルター ============================
VX = -2.0      # 換気のパイプの x


def vent(name="vent"):
    """地上の吸気口（キノコ形のふた）→ 土の中のパイプ → 天井のフィルター箱 → ファン。"""
    pm = M("pipe")
    root = K.empty((0, 0, 0), None, name)
    K.obj(K.cyl_mesh(0.18, 0.18, 2.6 - RC, 12), pm, root, (VX, 0.9, RC), name=f"{name}_pipe")
    K.obj(K.cyl_mesh(0.42, 0.05, 0.3, 16), pm, root, (VX, 0.9, 2.6), name=f"{name}_cap")
    filt = box((1.0, 0.7, 0.55), (VX, 0.9, RC - 0.32), K.mat("filter", (0.88, 0.86, 0.78), 0.8), f"{name}_filter", root)
    for k in range(7):
        box((0.02, 0.72, 0.5), (VX - 0.45 + 0.15 * k, 0.9, RC - 0.32), K.mat("filter_pleat", (0.55, 0.53, 0.47), 0.8), f"{name}_pleat", root)
    fan = K.empty((VX + 0.85, 0.9, RC - 0.32), root, f"{name}_fan")
    box((0.5, 0.5, 0.5), (VX + 0.85, 0.9, RC - 0.32), K.mat("fan_box", (0.35, 0.37, 0.4), 0.5), f"{name}_fanbox", root)
    blades = K.empty((0.26, 0, 0), fan, f"{name}_blades")
    for k in range(4):
        box((0.02, 0.36, 0.08), (0, 0, 0), K.mat("blade_fan", (0.85, 0.85, 0.85), 0.4), f"{name}_blade", blades, rot=(k * 45 * D2R, 0, 0))
    return root, filt, blades


def s05_air(nf):
    world()
    T = SC["dur"]
    a18, _ = lt(18)
    a19, _ = lt(19)
    a20, _ = lt(20)
    a21, _ = lt(21)
    a22, _ = lt(22)
    a23, _ = lt(23)
    room_cut = cutter_box(-RX - THICK - 0.02, RX + THICK + 0.02, RF - THICK - 0.02, RC + THICK + 0.02, name="cut_room")
    lp = xz_prism(LPASS, -1.0, 1.6, K.mat("cutter", (1, 0, 1)), "cut_L", hide=True)
    ground_and_soil([room_cut, lp])
    room(True, "room")
    blast_door(True)
    mound()
    ash_fall(80, 1, 2, xr=(-12, 12), yr=(0.3, 6.0), land=lambda x: (min(1.0, max(0.0, (6.0 - abs(x)) / 1.4)) if abs(x) < 6.0 else 0.0),
             seed=31, name="ashG")
    t_v = a20 - 0.4
    vr, filt, blades = vent()
    K.show(vr, fr(t_v), pop=6)
    K.key_rot(blades, fr(a20), (0, 0, 0))
    K.key_rot(blades, fr(T), (6 * 2 * math.pi * (T - a20), 0, 0))
    _ = K.obj(K.box_mesh(1.05, 0.75, 0.6), hl("filter", fr(a21), fr(a21 + 0.2), fr(a23 + 1.0), fr(a23 + 1.3)), filt, (0, 0, 0), name="filter_hl",
              shadow=False)
    K.marker("filter", (0, -0.4, 0), filt)
    # 外の空気：灰まじり（灰色の点）がパイプに吸いこまれて、フィルターで止まる
    r = random.Random(4)
    am = ash_mat()
    for k in range(26):
        o = K.obj(K.ellip_mesh(0.07, 0.07, 0.07, 6, 4), am, None, (0, 0, -50), name=f"air_ash{k}", shadow=False)
        t0 = a20 + 0.1 + 0.12 * k
        x0 = VX + r.uniform(-3, 3)
        K.key_loc(o, fr(t0) - 1, (x0, 0.9, 3.5 + r.uniform(0, 1.5)))
        K.key_loc(o, fr(t0), (x0, 0.9, 3.5 + r.uniform(0, 1.5)))
        K.key_loc(o, fr(t0 + 0.4), (VX + r.uniform(-0.1, 0.1), 0.9, 2.5))
        K.key_loc(o, fr(t0 + 1.0), (VX + r.uniform(-0.1, 0.1), 0.9, RC + 0.3))
        stop = (VX - 0.3 + r.uniform(-0.15, 0.4), 0.6, RC - 0.12 - r.uniform(0, 0.3))
        K.key_loc(o, fr(t0 + 1.25), stop)
    # きれいな空気（青い点線）：外 → パイプ → フィルター → ファン → 部屋の中へ
    bm = K.glow("air_blue", BLUE, 4.0)
    K.flow_arrow([(VX - 1.5, 0.9, 3.4), (VX, 0.9, 2.9), (VX, 0.9, RC + 0.1)], bm, fr(a20), nf, width=0.12, dash=0.4, gap=0.3, speed=3.0, head=0.3,
                 name="air_in")
    K.flow_arrow([(VX + 1.2, 0.6, RC - 0.32), (VX + 2.6, 0.6, RC - 0.9), (2.2, 0.6, RF + 1.2)], bm, fr(a22), nf, width=0.12, dash=0.4, gap=0.3,
                 speed=3.0, head=0.3, name="air_out")
    hero = hero_in_room(loc=(1.0, 1.4, RF), face=-20)
    hero.pose(fr(a18 + 0.2), shL=(40, 10), shR=(120, -20), elR=120, spine=-15, neck=10)          # 苦しい（のどに手）
    hero.pose(fr(a22), shL=(40, 10), shR=(120, -20), elR=120, spine=-15, neck=10)
    hero.pose(fr(a22 + 0.4), shL=(100, 70), shR=(100, 70), elL=5, elR=5, spine=5, neck=-15)       # 深呼吸
    hero.pose(fr(a23 + 0.3), shL=(15, 10), shR=(150, 20), elR=95, spine=0, neck=0)
    hero.pose(nf, shR=(165, 15), elR=70)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    fill_light((0.0, -22.0, -0.5), (0, 0, -1.2), 3000, 16.0)
    keys = [(0.0, (0.8, -11.0, -1.6), (0.4, 2.0, -1.8), 28),
            (a19, (-1.0, -14.0, 0.8), (-1.5, 2.0, 0.6), 27),
            (a20, (-1.2, -15.0, 0.4), (-1.5, 2.0, 0.2), 27),
            (a21, (-1.4, -9.5, -0.4), (VX + 0.2, 0.9, -0.9), 28),
            (a22 + 0.3, (0.2, -11.0, -1.0), (0.0, 2.0, -1.4), 27),
            (T, (0.2, -12.0, -0.8), (0.0, 2.0, -1.4), 27)]
    campath(keys, nf, shake=0.02)


# ============================ 6) 2週間 ============================
def s06_days(nf):
    world()
    T = SC["dur"]
    a24, _ = lt(24)
    a25, _ = lt(25)
    a26, _ = lt(26)
    a27, _ = lt(27)
    a28, _ = lt(28)
    room_cut = cutter_box(-RX - THICK - 0.02, RX + THICK + 0.02, RF - THICK - 0.02, RC + THICK + 0.02, name="cut_room")
    lp = xz_prism(LPASS, -1.0, 1.6, K.mat("cutter", (1, 0, 1)), "cut_L", hide=True)
    ground_and_soil([room_cut, lp])
    room(True, "room")
    blast_door(True)
    mound()
    vent()
    # 地上の灰の光が、時間とともに弱まる（7時間で 1/10、2日で 1/100、2週間で 1/1000）
    land = lambda x: (min(1.0, max(0.0, (6.0 - abs(x)) / 1.4)) if abs(x) < 6.0 else 0.0)   # noqa: E731
    am = ash_mat(3.0)
    ash_fall(150, 1, 2, xr=(-14, 14), yr=(0.3, 9.0), land=land, seed=41, name="ashD", glow_m=am)
    b = am.node_tree.nodes["Principled BSDF"]
    for t, v in ((0.0, 3.0), (a25 + 0.2, 3.0), (a25 + 1.2, 0.9), (a26 + 0.6, 0.25), (a27 + 1.0, 0.0)):
        b.inputs["Emission Strength"].default_value = v
        b.inputs["Emission Strength"].keyframe_insert("default_value", frame=fr(t))
    # 壁の時計とカレンダー（ページがめくれる）
    clock = K.empty((-2.2, RY - 0.05, RF + 1.75), None, "clock")
    K.obj(K.cyl_mesh(0.28, 0.28, 0.04, 24), K.mat("clock_face", (0.95, 0.95, 0.92), 0.4), clock, (0, 0, 0), rot=(90 * D2R, 0, 0), name="clock_f")
    hand = K.empty((0, -0.05, 0), clock, "hand")
    box((0.03, 0.02, 0.22), (0, 0, 0.1), K.mat("hand_m", (0.05, 0.05, 0.05), 0.4), "clock_h", hand)
    K.key_rot(hand, fr(a25), (0, 0, 0))
    K.key_rot(hand, fr(a28), (0, 2 * math.pi * 14, 0))
    cal = K.empty((-1.2, RY - 0.05, RF + 1.6), None, "cal")
    box((0.5, 0.02, 0.6), (0, 0, 0), K.mat("cal_back", (0.9, 0.9, 0.88), 0.6), "cal_b", cal)
    box((0.5, 0.025, 0.12), (0, -0.005, 0.24), K.mat("cal_top", (0.8, 0.1, 0.08), 0.6), "cal_t", cal)
    pages = []
    for k in range(14):
        pg = K.empty((0, -0.015 - 0.001 * k, 0.18), cal, f"page{k}")
        box((0.46, 0.004, 0.42), (0, 0, -0.21), K.mat("cal_page", (0.97, 0.97, 0.95), 0.7), f"page_b{k}", pg)
        pages.append(pg)
    for k, pg in enumerate(reversed(pages)):
        t0 = a26 + (a28 - a26) * k / 14
        K.key_rot(pg, fr(t0), (0, 0, 0))
        K.key_rot(pg, fr(t0) + 4, (-170 * D2R, 0, 0))
    # 2週間分の水と食料：棚に、ポンポンと並ぶ
    shelf = K.empty((2.3, RY - 0.4, RF), None, "shelf")
    for k in range(4):
        box((1.3, 0.5, 0.04), (0, 0, 0.35 + 0.5 * k), M("wood"), "shelf_board", shelf)
    for sx in (-1, 1):
        box((0.04, 0.5, 2.0), (sx * 0.63, 0, 1.0), M("wood"), "shelf_side", shelf)
    items = []
    for k in range(4):
        for j in range(5):
            if k < 2:
                o = K.obj(K.cyl_mesh(0.09, 0.09, 0.32, 12), M("water"), shelf, (-0.5 + 0.25 * j, 0, 0.37 + 0.5 * k), name="bottle")
            else:
                o = K.obj(K.cyl_mesh(0.07, 0.07, 0.12, 12), M("can"), shelf, (-0.5 + 0.25 * j, 0, 0.37 + 0.5 * k), name="can")
            items.append(o)
    K.show(shelf, fr(a28 - 0.1), pop=5)
    for i, o in enumerate(items):
        K.show(o, fr(a28 + 0.1 + 0.04 * i), pop=3)
    tank = K.obj(K.cyl_mesh(0.35, 0.35, 1.2, 16), M("water"), None, (1.1, RY - 0.5, RF), name="tank")
    K.show(tank, fr(a28 + 0.2), pop=5)
    sh_hl = box((1.6, 0.7, 2.1), (2.3, RY - 0.4, RF + 1.0), hl("food", fr(a28 + 0.3), fr(a28 + 0.5), fr(T) + 5, fr(T) + 9), "food_hl", shadow=False)
    _ = sh_hl
    hero = hero_in_room(loc=(-0.5, 1.6, RF), face=30)
    hero.pose(1, hipL=90, hipR=90, kneeL=-90, kneeR=-90, hz=-0.45, shL=(20, 10), shR=(20, 10), elL=40, elR=40)      # すわる
    K.obj(K.box_mesh(1.4, 0.45, 0.45), M("wood"), None, (-0.5, 2.0, RF + 0.22), name="bench")
    hero.pose(fr(a24 + 0.3), hipL=90, hipR=90, kneeL=-90, kneeR=-90, hz=-0.45, shL=(20, 10), shR=(120, -10), elR=110, neck=10)  # 考える
    hero.pose(fr(a28), hipL=90, hipR=90, kneeL=-90, kneeR=-90, hz=-0.45, shL=(20, 10), shR=(120, -10), elR=110, neck=10)
    hero.pose(fr(a28 + 0.5), hipL=0, hipR=0, kneeL=0, kneeR=0, hz=0, shL=(15, 10), shR=(150, 20), elR=95, neck=0)
    hero.pose(nf, shR=(165, 15), elR=70)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    fill_light((0.0, -22.0, -0.5), (0, 0, -1.2), 3000, 16.0)
    keys = [(0.0, (-0.6, -9.0, -1.4), (-1.2, 2.0, -1.6), 28),
            (a25, (-1.0, -16.0, 0.6), (-0.5, 2.0, -0.4), 26),
            (a26, (-1.4, -8.0, -1.2), (-1.6, RY, -1.3), 30),
            (a27 + 0.6, (-1.2, -8.5, -1.3), (-1.5, RY, -1.3), 30),
            (a28, (0.8, -10.5, -1.4), (1.2, 2.5, -1.8), 28),
            (T, (0.8, -11.5, -1.3), (1.2, 2.5, -1.8), 28)]
    campath(keys, nf, shake=0.02)


# ============================ 7) 完成 ============================
def s07_final(nf):
    world()
    T = SC["dur"]
    a29, _ = lt(29)
    a30, _ = lt(30)
    room_cut = cutter_box(-RX - THICK - 0.02, RX + THICK + 0.02, RF - THICK - 0.02, RC + THICK + 0.02, name="cut_room")
    lp = xz_prism(LPASS, -1.0, 1.6, K.mat("cutter", (1, 0, 1)), "cut_L", hide=True)
    ground_and_soil([room_cut, lp])
    room(True, "room")
    blast_door(True)
    mound()
    vent()
    lad = K.ladder(3.1, 0.5, "lad")
    lad.location = ((SHAFT[0] + SHAFT[1]) / 2, 1.2, RF)
    # 棚（水と食料）
    shelf = K.empty((2.3, RY - 0.4, RF), None, "shelf")
    for k in range(4):
        box((1.3, 0.5, 0.04), (0, 0, 0.35 + 0.5 * k), M("wood"), "shelf_board", shelf)
        for j in range(5):
            if k < 2:
                K.obj(K.cyl_mesh(0.09, 0.09, 0.32, 12), M("water"), shelf, (-0.5 + 0.25 * j, 0, 0.37 + 0.5 * k), name="bottle")
            else:
                K.obj(K.cyl_mesh(0.07, 0.07, 0.12, 12), M("can"), shelf, (-0.5 + 0.25 * j, 0, 0.37 + 0.5 * k), name="can")
    for sx in (-1, 1):
        box((0.04, 0.5, 2.0), (sx * 0.63, 0, 1.0), M("wood"), "shelf_side", shelf)
    K.obj(K.cyl_mesh(0.35, 0.35, 1.2, 16), M("water"), None, (1.1, RY - 0.5, RF), name="tank")
    # 2段ベッドとトイレが、ポンと出る
    bed = K.empty((-2.0, 2.6, RF), None, "bed")
    for z in (0.45, 1.45):
        box((1.0, 2.0, 0.12), (0, 0, z), M("wood"), "bed_board", bed)
        box((0.9, 1.9, 0.14), (0, 0, z + 0.13), M("blanket"), "bed_mat", bed)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box((0.07, 0.07, 1.9), (sx * 0.48, sy * 0.95, 0.95), M("wood"), "bed_post", bed)
    bed.rotation_euler = (0, 0, 90 * D2R)
    K.show(bed, fr(a29 + 0.3), pop=5)
    toilet = K.empty((-0.4, RY - 0.5, RF), None, "toilet")
    K.obj(K.cyl_mesh(0.22, 0.2, 0.42, 16), M("white"), toilet, (0, 0, 0), name="toilet_b")
    box((0.42, 0.18, 0.45), (0, 0.22, 0.45), M("white"), "toilet_t", toilet)
    K.show(toilet, fr(a29 + 0.6), pop=5)
    box((2.2, 2.3, 2.0), (-1.7, 2.6, RF + 1.0), hl("bed", fr(a29 + 0.3), fr(a29 + 0.5), fr(a30 + 0.6), fr(a30 + 0.9)), "bed_hl", shadow=False)
    hero = hero_in_room(loc=(0.6, 1.2, RF), face=0)
    hero.pose(fr(a30 - 0.2), shL=(10, 8), shR=(10, 8), elL=12, elR=12)
    hero.wave(fr(a30), fr(a30 + 1.0), "R")
    hero.pose(fr(a30 + 1.1), shL=(150, 40), shR=(150, 40), elL=15, elR=15)
    hero.pose(nf, shL=(160, 45), shR=(160, 45), elL=10, elR=10)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    fill_light((0.0, -24.0, -1.0), (0, 0, -1.5), 3000, 16.0)
    keys = [(0.0, (-0.4, -10.0, -1.2), (-1.0, 2.0, -1.6), 28),
            (a30, (0.6, -13.0, -1.0), (0.2, 2.0, -1.4), 27),
            (T, (1.5, -26.0, 1.0), (1.5, 2.0, -0.8), 25)]
    campath(keys, nf, shake=0.02)


SCENES = {k: v for k, v in globals().items() if callable(v) and k[:1] == "s" and k[1:3].isdigit()}

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    first = int(sys.argv[4]) if len(sys.argv) > 4 else None
    last = int(sys.argv[5]) if len(sys.argv) > 5 else None
    K.W.reset()
    SC = TL.scene(name)
    SCENES[name](SC["nf"])
    if os.environ.get("DRY"):
        print("built", name, len(bpy.data.objects), "objects", flush=True)
        sys.exit(0)
    K.render(out, SC["nf"], step, first, last, exposure=-0.8)
    print("rendered", name, flush=True)
