"""「いかだの作り方」全場面の3D（Blender / bpy）。主人公はレッサーパンダ（黄色いヘルメット・オレンジのベスト・電動ドリル）。
南の島の砂浜と海。海面は z=0。いかだは丸太を y 方向（長さ 4m）に並べ、+y が前。カメラはおおむね -y から見る。
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
FPS = K.FPS
TL = Timeline(HERE)
SC = None
ORANGE = (1.0, 0.38, 0.02)
YELLOW = (1.0, 0.82, 0.05)
BLUE = (0.15, 0.55, 1.0)
fr = K.fr
campath = K.campath
NLOG, LOG_R, LOG_L = 7, 0.2, 4.0          # 丸太 7本（半径 0.2m、長さ 4m）
HALF_W = NLOG * LOG_R                     # いかだの幅の半分


def lt(i):
    L = SC["lines"][i]
    return L["t"], L["t_end"]


# ---------- 材質 ----------
def M(key):
    tab = {
        "sand": lambda: K.noisy("sand", (0.72, 0.62, 0.44), 14.0, 0.10, 0.25, 0.95),
        "heavy": lambda: K.noisy("log_heavy", (0.36, 0.24, 0.14), 6.0, 0.25, 0.4, 0.8),
        "balsa": lambda: K.noisy("log_balsa", (0.72, 0.58, 0.38), 6.0, 0.14, 0.3, 0.8),
        "cut": lambda: K.mat("log_cut", (0.92, 0.82, 0.60), 0.8),
        "rope": lambda: K.noisy("rope", (0.72, 0.60, 0.38), 40.0, 0.2, 0.5, 0.9),
        "wood": lambda: K.noisy("plank", (0.55, 0.38, 0.20), 3.0, 0.25, 0.2, 0.7),
        "dowel": lambda: K.mat("dowel", (0.62, 0.45, 0.25), 0.6),
        "sail": lambda: K.noisy("sail", (0.93, 0.88, 0.76), 10.0, 0.06, 0.2, 0.9),
        "palm": lambda: K.noisy("palm_trunk", (0.48, 0.38, 0.26), 12.0, 0.2, 0.5, 0.9),
        "leaf": lambda: K.mat("palm_leaf", (0.12, 0.38, 0.10), 0.6),
        "foam": lambda: K.mat("foam", (0.95, 0.97, 0.98), 0.5),
    }
    return tab[key]()


def sea_mat(name="sea", col=(0.02, 0.24, 0.36), alpha=1.0):
    """海面：青い光沢＋ゆっくり動く小さな波（バンプ）。"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = 0.06
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        try:
            m.blend_method = 'BLEND'
        except AttributeError:
            pass
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.noise_dimensions = '4D'
    nz.inputs["Scale"].default_value = 0.9
    nz.inputs["Detail"].default_value = 6.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nz.inputs["W"].default_value = 0.0
    nz.inputs["W"].keyframe_insert("default_value", frame=1)
    nz.inputs["W"].default_value = 8.0
    nz.inputs["W"].keyframe_insert("default_value", frame=1800)
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.35
    nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def hl(name, f_on, f_full, f_off=None, f_gone=None, col=ORANGE, alpha=0.6, strength=2.2):
    alpha = min(alpha, 0.97)
    return K.fade_mat(K.glow(f"hl_{name}", col, strength, alpha), f_on, f_full, f_off, f_gone, f"hl_{name}_{f_on}")


def box(size, loc, m, name="b", parent=None, rot=(0, 0, 0), shadow=True):
    return K.obj(K.box_mesh(*size), m, parent, loc, rot=rot, name=name, shadow=shadow)


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


def text3d(s, loc, size=0.6, m=None, name="txt", rot=(90, 0, 0)):
    cu = bpy.data.curves.new(name, 'FONT')
    cu.body = s
    cu.size = size
    cu.align_x = 'CENTER'
    cu.align_y = 'CENTER'
    cu.extrude = 0.02
    fp = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    if os.path.exists(fp):
        try:
            cu.font = bpy.data.fonts.load(fp, check_existing=True)
        except Exception:
            pass
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m or K.glow("txt_white", (1, 1, 1), 3.0))
    o.location = loc
    o.rotation_euler = tuple(a * D2R for a in rot)
    o.visible_shadow = False
    return o


# ---------- 島と海 ----------
def palm(x, y, h=6.0, seed=1, lean=10.0):
    r = random.Random(seed)
    root = K.empty((x, y, 0), None, f"palm{seed}")
    root.rotation_euler = (lean * D2R * r.uniform(0.5, 1.0), 0, r.uniform(0, 6.3))
    n = 8
    for k in range(n):
        u = k / n
        K.obj(K.cyl_mesh(0.22 - 0.08 * u, 0.2 - 0.08 * u, h / n + 0.05, 10), M("palm"), root, (0.25 * u * u, 0, h * (k + 0.5) / n),
              name="palm_seg")
    top = (0.25, 0, h)
    for k in range(9):
        a = k * 2 * math.pi / 9 + r.uniform(-0.2, 0.2)
        lf = K.empty(top, root, "leaf_piv")
        lf.rotation_euler = (0, 0, a)
        K.obj(K.ellip_mesh(0.22, 1.5, 0.03), M("leaf"), lf, (0, 1.3, -0.35), rot=(-25 * D2R, 0, 0), name="palm_leaf")
    K.obj(K.ellip_mesh(0.3, 0.3, 0.25), M("palm"), root, top, name="palm_top")
    return root


def world(beach=True, seed=3, island=True):
    K.daylight(elev=55, az=215)
    K.clouds(seed=seed)
    sea = K.obj(K.box_mesh(4000, 4000, 0.02), sea_mat(), None, (0, 0, -0.01), name="sea", shadow=False)
    _ = sea
    if beach:            # 手前（-y）が砂浜、ゆるい坂で海へ
        sand = K.obj(K.box_mesh(80, 30, 1.0), M("sand"), None, (0, -14.5, 0.077), name="sand")      # 波打ちぎわ y≈0.5
        sand.rotation_euler = (-2.2 * D2R, 0, 0)
        for k, (x, y) in enumerate([(-7, -6), (-11, -9), (8, -7), (12, -11), (-15, -4), (17, -5)]):
            palm(x, y, 6.0 + 0.6 * (k % 3), seed=10 + k)
    if island:           # 沖の小さな島
        isl = K.obj(K.ellip_mesh(40, 18, 6), M("sand"), None, (-60, 180, -3.5), name="island")
        _ = isl
        K.obj(K.ellip_mesh(30, 12, 9), M("leaf"), None, (-60, 182, 1.5), name="island_green")


# ---------- いかだ ----------
def raft(kind="heavy", name="raft", rope=True, outrigger=False, rudder=False, sail=False, boards=False, pegs=False, mast=False):
    """いかだ（中心＝原点、海面にうかべる高さは呼ぶ側で）。parts＝名前ごとの部品（空オブジェクト）。"""
    root = K.empty((0, 0, 0), None, name)
    parts = {}
    lm = M(kind)
    logs = K.empty((0, 0, 0), root, f"{name}_logs")
    parts["logs"] = logs
    xs = [-HALF_W + LOG_R + 2 * LOG_R * i for i in range(NLOG)]
    for i, x in enumerate(xs):
        lg = K.obj(K.cyl_mesh(LOG_R, LOG_R * 0.95, LOG_L - (0.25 if i % 2 else 0.0), 14), lm, logs, (x, 0, 0), rot=(90 * D2R, 0, 0),
                   name=f"{name}_log{i}")
        _ = lg
    if rope:
        rp = K.empty((0, 0, 0), root, f"{name}_ropes")
        parts["rope"] = rp
        for y in (-1.3, 0.0, 1.3):
            box((2 * HALF_W + 0.04, 0.09, 0.06), (0, y, LOG_R + 0.01), M("rope"), f"{name}_rope", rp)
            box((2 * HALF_W + 0.04, 0.09, 0.06), (0, y, -LOG_R - 0.01), M("rope"), f"{name}_rope", rp)
    if pegs:
        pg = K.empty((0, 0, 0), root, f"{name}_pegs")
        parts["pegs"] = pg
        for y in (-1.2, 1.2):
            K.obj(K.cyl_mesh(0.05, 0.05, 2 * HALF_W + 0.5, 10), M("dowel"), pg, (0, y, 0), rot=(0, 90 * D2R, 0), name=f"{name}_peg")
    if outrigger:        # 右に離して、もう1本の丸太（アウトリガー）
        og = K.empty((0, 0, 0), root, f"{name}_out")
        parts["out"] = og
        K.obj(K.cyl_mesh(0.18, 0.15, 3.2, 14), lm, og, (HALF_W + 1.9, 0, -0.04), rot=(90 * D2R, 0, 0), name=f"{name}_float")
        for y in (-0.9, 0.9):
            K.obj(K.cyl_mesh(0.06, 0.06, 2.4, 8), M("wood"), og, (HALF_W + 0.85, y, 0.26), rot=(0, 90 * D2R, 0), name=f"{name}_beam")
    if rudder:           # うしろの舵（長い板）
        rd = K.empty((0, -LOG_L / 2 - 0.1, 0.35), root, f"{name}_rudder")
        parts["rudder"] = rd
        K.obj(K.cyl_mesh(0.045, 0.045, 2.6, 8), M("wood"), rd, (0, -0.6, -0.2), rot=(70 * D2R, 0, 0), name=f"{name}_oar")
        box((0.06, 0.9, 0.45), (0, -1.6, -0.7), M("wood"), f"{name}_blade", rd, rot=(-20 * D2R, 0, 0))
    if mast or sail:     # 帆柱と四角い帆
        ms = K.empty((0, 0.4, LOG_R), root, f"{name}_mast")
        parts["mast"] = ms
        K.obj(K.cyl_mesh(0.07, 0.06, 3.8, 10), M("wood"), ms, (0, 0, 1.9), name=f"{name}_pole")
        box((0.5, 0.5, 0.06), (0, 0, 0.03), M("wood"), f"{name}_mast_base", ms)
        if sail:
            sl = K.empty((0, 0, 3.6), ms, f"{name}_sailpiv")
            parts["sail"] = sl
            K.obj(K.cyl_mesh(0.04, 0.04, 2.6, 8), M("wood"), sl, (0, 0.05, 0), rot=(0, 90 * D2R, 0), name=f"{name}_yard")
            box((2.4, 0.04, 2.5), (0, 0.08, -1.3), M("sail"), f"{name}_cloth", sl)
    if boards:           # 丸太のすき間から、水の中へ差し込む板（センターボード）
        bd = K.empty((0, 0, 0), root, f"{name}_boards")
        parts["boards"] = bd
        for k, y in enumerate((-1.2, 0.0, 1.2)):
            box((0.04, 0.6, 1.6), (xs[3] - LOG_R if k != 1 else xs[3] + LOG_R, y, -0.7), M("wood"), f"{name}_board{k}", bd)
    return root, parts


def bob(o, f0, f1, base=(0, 0, 0), amp=0.06, rock=2.0, rate=0.45, seed=1, face=0.0, step=2):
    """波でゆれる（上下と左右のかたむき）。"""
    r = random.Random(seed)
    ph = [r.uniform(0, 6.3) for _ in range(3)]
    for f in list(range(f0, f1 + 1, step)) + [f1]:
        t = f / FPS
        o.location = (base[0], base[1], base[2] + amp * math.sin(2 * math.pi * rate * t + ph[0]))
        o.rotation_euler = (rock * 0.6 * D2R * math.sin(2 * math.pi * rate * 0.8 * t + ph[1]),
                            rock * D2R * math.sin(2 * math.pi * rate * 1.1 * t + ph[2]), face * D2R)
        o.keyframe_insert("location", frame=f)
        o.keyframe_insert("rotation_euler", frame=f)


def splash(loc, f0, n=24, seed=1, size=0.08, up=2.5, spread=1.2):
    """水しぶき（白い粒が上がって落ちる）＋白いあわ。"""
    r = random.Random(seed)
    me = K.ellip_mesh(size, size, size * 1.3, 8, 6)
    for k in range(n):
        o = K.obj(me, M("foam"), None, (0, 0, -30), name=f"spl{seed}_{k}", shadow=False)
        p0 = Vector(loc) + Vector((r.uniform(-0.3, 0.3), r.uniform(-0.3, 0.3), 0))
        p1 = p0 + Vector((r.uniform(-spread, spread), r.uniform(-spread, spread), -0.2))
        fa = f0 + r.randint(0, 4)
        K.key_scale(o, fa - 1, 1e-4)
        K.key_scale(o, fa, r.uniform(0.6, 1.4))
        K.projectile(o, fa, fa + 16, tuple(p0), tuple(p1), arc=r.uniform(0.4, up), align=False, step=2)
        K.key_scale(o, fa + 16, 0.6)
        K.key_scale(o, fa + 17, 1e-4)
    K.smoke_puffs(tuple(loc), f0, n=4, seed=seed + 300, col=(0.95, 0.97, 1.0), size=0.6, rise=0.6, life=20, spread=0.6, alpha=0.7,
                  name=f"foam{seed}")


def tip_at(d, f):
    sc = bpy.context.scene
    sc.frame_set(f)
    p = bpy.data.objects[d["tip"]].matrix_world.translation.copy()
    sc.frame_set(1)
    return tuple(p)


def panda(loc, face, name="hero", drill_on=True):
    h = K.Person(loc, face, K.PANDA, name=name)
    d = None
    if drill_on:
        d = K.drill(1.6, f"{name}_drill")
        h.hold(d, "R", (0, 0.03, -0.02), (-90, 0, 0))
    h.stand(1)
    return h, d


DRILL_LOG = dict(spine=-22, neck=18, shR=(8, -10), elR=8, shL=(16, -22), elL=18, hipL=12, hipR=12, kneeL=-16, kneeR=-16, hz=-0.04)
DRILL_SIDE = dict(spine=-18, neck=12, shR=(48, -6), elR=20, shL=(45, -22), elL=30, hipL=20, hipR=20, kneeL=-30, kneeR=-30, hz=-0.12)
DRILL_LOG2 = dict(DRILL_LOG, spine=-14, hipL=6, hipR=6, kneeL=-8, kneeR=-8, hz=0.0)


def ride(hero, raft_root, local, face, f0, f1, step=2):
    """主人公をいかだの上に乗せる（いかだといっしょにゆれる）。親子にせず、毎コマ位置を計算してキーを打つ。"""
    sc = bpy.context.scene
    for f in list(range(f0, f1 + 1, step)) + [f1]:
        sc.frame_set(f)
        Mw = raft_root.matrix_world
        hero.root.location = Mw @ Vector(local)
        e = raft_root.matrix_world.to_euler()
        hero.root.rotation_euler = (e.x, e.y, e.z + face * D2R)
        hero.root.keyframe_insert("location", frame=f)
        hero.root.keyframe_insert("rotation_euler", frame=f)
    sc.frame_set(1)


# ============================ 1) 丸太にドリル → 縄でしばる → いかだ → 重くて水びたし ============================
def s01_drill(nf):
    world()
    T = SC["dur"]
    a1, _ = lt(1)
    a2, _ = lt(2)
    a3, _ = lt(3)
    a4, _ = lt(4)
    # 砂浜の上の丸太（はじめはばらばら）→ 縄でしばって、いかだに → 海へ
    rf, parts = raft("heavy", "raft")
    logs = parts["logs"]
    ropes = parts["rope"]
    base0 = (0.0, -3.0, 0.335)
    K.key_loc(rf, 1, base0)
    r = random.Random(4)
    for i, lg in enumerate(logs.children):        # ばらばら → ならぶ
        x1 = lg.location.x
        K.key_loc(lg, 1, (x1 * 1.9 + r.uniform(-0.2, 0.2), r.uniform(-0.3, 0.3), 0))
        K.key_loc(lg, fr(a1), (x1 * 1.9 + r.uniform(-0.2, 0.2), r.uniform(-0.3, 0.3), 0))
        K.key_loc(lg, fr(a1 + 0.5 + 0.04 * i), (x1, 0, 0))
    for k, rp in enumerate(ropes.children):
        K.show(rp, fr(a1 + 0.7 + 0.06 * k), pop=3)
    # 海へすべりこむ → 重くて沈む
    K.key_loc(rf, fr(a2), base0)
    K.key_loc(rf, fr(a2 + 0.8), (0.0, 4.0, 0.0))
    bob(rf, fr(a2 + 0.9), fr(a3 + 0.2), base=(0.0, 4.0, 0.0), amp=0.05)
    bob(rf, fr(a3 + 0.4), nf, base=(0.0, 4.0, -0.12), amp=0.03, rock=1.0)
    # レッサーパンダ：丸太にドリル（最初の 1.7秒：強く動かす）→ いかだに乗る → 水びたし
    hero, dr = panda((0.91, -2.45, 0.135), 180)          # 丸太のむこう側から、カメラのほうを向いて
    hero.stand(1, **DRILL_LOG2)
    for k in range(6):
        f = 2 + 4 * k
        hero.pose(f, **dict(DRILL_LOG2, spine=-14 + (3 if k % 2 else -3)))
    K.spin(dr, 1, fr(a1 - 0.1), 80)
    tip = tip_at(dr, 10)
    print("tip", tip)
    K.drill_fx(tip, 1, fr(a1 - 0.1), "chips", seed=3, n=60, up=(0, -0.4, 1))
    hero.pose(fr(a1 - 0.05), **DRILL_LOG2)
    hero.pose(fr(a1 + 0.3), spine=0, neck=-5, shR=(25, 8), elR=40, shL=(15, -8), elL=20, hipL=0, hipR=0, kneeL=0, kneeR=0, hz=0)
    hero.place(1, face=180)
    hero.place(fr(a2 - 0.2) - 1, face=180)
    hero.walk(fr(a2 - 0.2), fr(a2 + 0.9), [(0.91, -2.45, 0.135), (0.3, 0.5, 0.0), (0.3, 3.8, 0.2)], run=True)
    f_on = fr(a2 + 0.95)
    ride(hero, rf, (0.3, -0.2, LOG_R), 180, f_on, nf)
    hero.pose(f_on, shL=(150, 40), shR=(150, 40), elL=15, elR=15)
    hero.pose(fr(a3 + 0.3), shL=(20, 8), shR=(20, 8), elL=20, elR=20, neck=10)
    hero.pose(fr(a4 + 0.2), shL=(150, 30), shR=(30, 8), elL=110, elR=30, neck=12)            # 足がぬれて困る
    hero.wag(1, nf)
    K.marker("hero", (0, 0, 0.18), hero.j["neck"])
    splash((0.0, 4.0, 0.0), fr(a2 + 0.8), n=30, seed=5, up=1.5)
    splash((0.3, 3.8, 0.0), fr(a3 + 0.4), n=20, seed=6, up=0.8)
    fill_light((2.0, -10.0, 4.0), (0, 0, 0.6), 1800, 10.0)
    keys = [(0.0, (2.0, -5.0, 1.0), (0.8, -2.8, 0.65), 24),
            (0.7, (-0.4, -5.3, 1.2), (0.8, -2.8, 0.7), 24),
            (a1 - 0.1, (-0.9, -6.0, 1.7), (0.6, -2.9, 0.7), 24),
            (a1 + 0.6, (2.5, -9.0, 3.5), (0.0, -2.5, 0.3), 24),
            (a2 + 0.9, (3.0, -6.0, 3.0), (0.0, 3.5, 0.3), 24),
            (a3 + 0.4, (2.6, 0.0, 1.6), (0.0, 4.0, 0.3), 26),
            (T, (2.0, 1.2, 1.2), (0.2, 3.9, 0.4), 28)]
    campath(keys, nf, shake=0.02)


# ============================ 2) とても軽い木（バルサ）→ 水の上に出る ============================
def s02_balsa(nf):
    world()
    T = SC["dur"]
    a5, _ = lt(5)
    a6, _ = lt(6)
    base = (0.0, 4.0, -0.12)
    old, _p = raft("heavy", "old")
    new, _p2 = raft("balsa", "new")
    f_sw = fr(a5 + 0.9)
    bob(old, 1, f_sw, base=base, amp=0.03, rock=1.0)
    K.key_scale(old, f_sw, 1.0)
    K.key_scale(old, f_sw + 1, 1e-4)
    bob(new, f_sw, nf, base=(0.0, 4.0, 0.09), amp=0.05, rock=1.5, seed=2)
    K.show(new, f_sw, pop=5)
    for k in range(3):
        K.smoke_puffs((-0.8 + 0.8 * k, 4.0, 0.4), f_sw, n=3, seed=20 + k, col=(1, 1, 1), size=0.7, rise=0.8, life=16, spread=0.5, alpha=0.8,
                      name=f"poof{k}")
    hero, _d = panda((0, 0, 0), 180)
    ride(hero, old, (0.3, -0.2, LOG_R), 180, 1, f_sw - 1)
    hero.pose(1, shL=(150, 30), shR=(30, 8), elL=110, elR=30, neck=12)
    ride(hero, new, (0.3, -0.2, LOG_R), 180, f_sw, nf)          # 同じ場所の新しいいかだへ
    hero.pose(f_sw + 4, shL=(160, 40), shR=(160, 40), elL=15, elR=15)
    hero.pose(fr(a6 + 0.5), shL=(20, 8), shR=(150, 20), elL=20, elR=20)
    hero.wag(1, nf)
    # 「軽い」の目印：水面の青い点線（いかだの下が見える高さ）
    bm = K.glow("water_blue", BLUE, 5.0)
    wl = K.poly_curve([(-2.2, 1.6, 0.03), (2.2, 1.6, 0.03)], 0.04, bm, "waterline")
    K.grow_line(wl, fr(a6), fr(a6 + 0.6))
    fill_light((2.0, -6.0, 4.0), (0, 4, 0.4), 1800, 10.0)
    keys = [(0.0, (2.6, 0.0, 1.6), (0.0, 4.0, 0.3), 26),
            (a5 + 1.0, (3.4, -1.0, 1.0), (0.0, 4.0, 0.3), 26),
            (a6, (4.5, 2.6, 0.35), (0.0, 4.0, 0.2), 26),
            (T, (4.8, 3.2, 0.3), (0.0, 4.0, 0.2), 26)]
    campath(keys, nf, shake=0.02)


# ============================ 3) 大波でひっくり返る → アウトリガー → 南の島の小舟 ============================
def big_wave(name, f0, f1, x0=16.0, x1=-12.0, y=4.0, h=1.4):
    """横から来る大波（長いうねり＋白い波がしら）。"""
    w = K.empty((x0, y, 0), None, name)
    K.obj(K.ellip_mesh(2.2, 14.0, h), sea_mat("sea_wave", (0.03, 0.28, 0.40)), w, (0, 0, -0.2), name=f"{name}_body")
    K.obj(K.ellip_mesh(0.5, 13.0, 0.25), M("foam"), w, (-1.2, 0, h - 0.5), name=f"{name}_crest")
    K.key_loc(w, 1, (x0, y, -3.0))
    K.key_loc(w, f0, (x0, y, -3.0))
    K.key_loc(w, f0 + 6, (x0 - 2.0, y, 0))
    K.key_loc(w, f1, (x1, y, 0))
    K.key_loc(w, f1 + 6, (x1 - 2.0, y, -3.0))
    return w


def canoe(name="canoe"):
    """南の島のアウトリガーカヌー（細長い船体＋浮き＋三角の帆）。"""
    c = K.empty((0, 0, 0), None, name)
    K.obj(K.ellip_mesh(0.35, 3.2, 0.3), K.mat("canoe_hull", (0.40, 0.22, 0.12), 0.6), c, (0, 0, 0.05), name=f"{name}_hull")
    K.obj(K.ellip_mesh(0.14, 1.8, 0.12), K.mat("canoe_float", (0.50, 0.32, 0.18), 0.6), c, (2.0, 0, 0.0), name=f"{name}_float")
    for y in (-0.8, 0.8):
        K.obj(K.cyl_mesh(0.04, 0.04, 2.2, 8), M("wood"), c, (1.0, y, 0.3), rot=(0, 90 * D2R, 0), name=f"{name}_beam")
    K.obj(K.cyl_mesh(0.04, 0.035, 3.2, 8), M("wood"), c, (0, 0.4, 1.8), name=f"{name}_mast")
    me = bpy.data.meshes.new(f"{name}_sailm")
    me.from_pydata([(0, 0.4, 3.4), (0, 0.4, 0.5), (0, -1.9, 0.5)], [], [(0, 1, 2)])
    me.materials.append(None)
    K.obj(me, K.mat("canoe_sail", (0.92, 0.85, 0.65), 0.8), c, (0.02, 0, 0), name=f"{name}_sail")
    return c


def s03_outrigger(nf):
    world(beach=False)
    T = SC["dur"]
    a7, _ = lt(7)
    a8, _ = lt(8)
    a9, _ = lt(9)
    a10, _ = lt(10)
    a11, _ = lt(11)
    base = (0.0, 4.0, 0.09)
    rf, _p = raft("balsa", "raft")
    rf2, parts2 = raft("balsa", "raft2", outrigger=True)
    f_flip0, f_flip1 = fr(a8 - 0.15), fr(a8 + 0.75)
    big_wave("wave1", fr(a7 + 0.1), fr(a8 + 0.9))
    bob(rf, 1, f_flip0, base=base, seed=3)
    for f in range(f_flip0, f_flip1 + 1):                  # 持ち上げられて、ひっくり返る
        u = (f - f_flip0) / (f_flip1 - f_flip0)
        rf.location = (base[0] - 0.8 * u, base[1], base[2] + 1.4 * math.sin(math.pi * u))
        rf.rotation_euler = (0, -180 * D2R * K.smooth(u), 0)
        rf.keyframe_insert("location", frame=f)
        rf.keyframe_insert("rotation_euler", frame=f)
    bob(rf, f_flip1 + 1, fr(a9), base=(base[0] - 0.8, base[1], base[2]), amp=0.04, seed=4)
    for f in range(f_flip1 + 1, fr(a9) + 1, 2):
        rf.rotation_euler = (rf.rotation_euler.x, math.pi, 0)
        rf.keyframe_insert("rotation_euler", frame=f)
    K.key_scale(rf, fr(a9), 1.0)
    K.key_scale(rf, fr(a9) + 1, 1e-4)
    splash((-0.8, 4.0, 0.0), f_flip1 - 4, n=40, seed=31, up=2.0, spread=2.0)
    # アウトリガーつき（横に もう1本の丸太）
    K.show(rf2, fr(a9) + 1, pop=5)
    bob(rf2, fr(a9) + 1, fr(a10), base=base, seed=5)
    f_w2 = fr(a10 - 0.4)
    big_wave("wave2", f_w2, f_w2 + 40)
    for f in range(fr(a10), fr(a11) + 1, 2):                # 波で少しかたむくが、浮きがささえて戻る
        u = (f - fr(a10)) / max(1, fr(a11) - fr(a10))
        rf2.location = (base[0], base[1], base[2] + 0.5 * math.sin(math.pi * min(1, u * 1.6)))
        rf2.rotation_euler = (0, -12 * D2R * math.sin(math.pi * min(1, u * 1.6)) * math.exp(-1.2 * u), 0)
        rf2.keyframe_insert("location", frame=f)
        rf2.keyframe_insert("rotation_euler", frame=f)
    bob(rf2, fr(a11) + 1, nf, base=base, seed=6)
    hlb = K.obj(K.cyl_mesh(0.26, 0.22, 3.4, 14), hl("float", fr(a9 + 0.6), fr(a9 + 0.9), fr(a10 + 0.6), fr(a10 + 0.9)), parts2["out"],
                (HALF_W + 1.9, 0, -0.04), rot=(90 * D2R, 0, 0), name="float_hl", shadow=False)
    _ = hlb
    # 主人公：いかだと一緒にひっくり返って海へ → アウトリガーのいかだに乗る
    hero, _d = panda((0, 0, 0), 180)
    ride(hero, rf, (0.3, -0.2, LOG_R), 180, 1, f_flip0)
    hero.pose(f_flip0 - 6, shL=(150, 40), shR=(150, 40), elL=30, elR=30)
    hero.fall(f_flip0 + 1, f_flip1 + 8, (0.3, 3.8, 0.9), (-3.0, 0.0, 3.5), spin=(300, 60), ground=-0.6)
    ride(hero, rf2, (0.3, -0.2, LOG_R), 180, fr(a9) + 2, nf)
    hero.stand(fr(a9) + 2)
    hero.pose(fr(a10 + 0.3), shL=(10, 8), shR=(150, 20), elL=12, elR=20)
    hero.pose(fr(a11), shL=(160, 40), shR=(160, 40), elL=15, elR=15)
    hero.wag(1, nf)
    K.marker("hero", (0, 0, 0.18), hero.j["neck"])
    # 南の島の小舟（沖を走る）
    cn = canoe()
    K.key_loc(cn, 1, (-14.0, 40.0, 0.05))
    K.key_loc(cn, fr(a11), (-14.0, 40.0, 0.05))
    K.key_loc(cn, nf, (-6.0, 40.0, 0.05))
    cn.rotation_euler = (0, 0, -90 * D2R)
    fill_light((3.0, -6.0, 4.0), (0, 4, 0.4), 1800, 10.0)
    keys = [(0.0, (3.0, -5.0, 2.2), (0.5, 4.0, 0.6), 24),
            (a8, (2.4, -6.5, 2.6), (0.0, 4.0, 1.0), 24),
            (a9, (3.5, -5.0, 2.4), (0.5, 4.0, 0.4), 24),
            (a10 + 0.8, (5.0, -3.5, 1.8), (1.0, 4.0, 0.4), 24),
            (a11, (-2.5, 31.0, 1.6), (-11.0, 40.0, 1.4), 30),
            (T, (-2.0, 32.0, 1.6), (-8.0, 40.0, 1.4), 32)]
    campath(keys, nf, shake=0.02, cuts=[a11])


# ============================ 4) 縄がこすれて切れる → 横から穴 → 木の棒でつなぐ ============================
def s04_pegs(nf):
    world()
    T = SC["dur"]
    a12, _ = lt(12)
    a13, _ = lt(13)
    a14, _ = lt(14)
    a15, _ = lt(15)
    base = (0.0, 5.0, 0.09)
    rf, parts = raft("balsa", "raft", outrigger=True)
    bob(rf, 1, nf, base=base, amp=0.03, rock=1.0, seed=7)
    ropes = parts["rope"]
    logs = parts["logs"]
    # 縄がこすれて（オレンジ）→ ぷつん
    for k, rp in enumerate(ropes.children):
        K.key_scale(rp, fr(a13), (1, 1, 1))
        K.key_scale(rp, fr(a13) + 2 + k, (1e-3, 1e-3, 1e-3))
    hlr = box((2 * HALF_W + 0.2, 0.3, 0.2), (0, 0, LOG_R + 0.02), hl("rope", fr(a12 + 0.3), fr(a12 + 0.6), fr(a13), fr(a13 + 0.2)), "rope_hl",
              rf, shadow=False)
    _ = hlr
    for i, lg in enumerate(logs.children):            # 丸太が少しはなれる → 棒でもどる
        x = lg.location.x
        K.key_loc(lg, fr(a13), (x, 0, 0))
        K.key_loc(lg, fr(a13 + 0.5), (x * 1.18, 0.1 * (i % 2), 0))
        K.key_loc(lg, fr(a15 + 0.3), (x * 1.18, 0.1 * (i % 2), 0))
        K.key_loc(lg, fr(a15 + 0.9), (x, 0, 0))
    for k in range(3):
        splash((-1.0 + k, 5.0 - 1.3, 0.1), fr(a12 + 0.2 + 0.5 * k), n=14, seed=40 + k, up=0.8, spread=0.8)
    # 木の棒（2本）が横からすべりこむ
    pegs = K.empty((0, 0, 0), rf, "pegs")
    for y in (-1.2, 1.2):
        p = K.obj(K.cyl_mesh(0.05, 0.05, 2 * HALF_W + 0.5, 10), M("dowel"), pegs, (0, y, 0), rot=(0, 90 * D2R, 0), name="peg")
        K.key_loc(p, 1, (-8.0, y, 0))
        K.key_loc(p, fr(a15 + 0.1), (-8.0, y, 0))
        K.key_loc(p, fr(a15 + 0.8), (0, y, 0))
    # 主人公：ひざまで水に入って、丸太の横からドリル
    hero, dr = panda((-HALF_W - 0.95, 3.8, -0.62), -90)
    hero.stand(1, shL=(150, 30), shR=(30, 8), elL=110, elR=30)
    hero.pose(fr(a13 + 0.3), shL=(150, 30), shR=(30, 8), elL=110, elR=30)
    hero.pose(fr(a14), **DRILL_SIDE)
    for k in range(8):
        hero.pose(fr(a14) + 2 + 4 * k, **dict(DRILL_SIDE, spine=-10 + (2 if k % 2 else -2)))
    hero.pose(fr(a15 - 0.1), **DRILL_SIDE)
    hero.pose(fr(a15 + 0.9), shL=(160, 40), shR=(160, 40), elL=15, elR=15, spine=0, hipL=0, hipR=0, kneeL=0, kneeR=0, hz=0)
    hero.wag(1, nf)
    K.spin(dr, fr(a14), fr(a15 - 0.1), 80)
    tip = tip_at(dr, fr(a14) + 6)
    print("side tip", tip)
    K.drill_fx(tip, fr(a14), fr(a15 - 0.1), "chips", seed=44, n=40, up=(-1, 0, 0.6))
    fill_light((-4.0, 0.0, 3.0), (0, 5, 0.3), 1800, 8.0)
    keys = [(0.0, (3.6, -0.6, 2.6), (0.0, 4.8, 0.2), 26),
            (a13, (3.0, 0.2, 2.0), (0.0, 4.8, 0.1), 28),
            (a14, (-3.6, 0.2, 1.6), (-1.6, 4.0, 0.1), 26),
            (a15, (-4.8, 0.4, 3.4), (0.0, 5.0, 0.1), 24),
            (T, (-5.2, 0.0, 3.8), (0.0, 5.0, 0.1), 24)]
    campath(keys, nf, shake=0.02)


# ============================ 5) 流される → 舵 ============================
def s05_rudder(nf):
    world(beach=False)
    T = SC["dur"]
    a16, _ = lt(16)
    a17, _ = lt(17)
    a18, _ = lt(18)
    a19, _ = lt(19)
    rf, parts = raft("balsa", "raft", outrigger=True, pegs=True, rope=False, rudder=True)
    rd = parts["rudder"]
    K.show(rd, fr(a17 + 0.3), pop=5)
    # 目的の島（前方）
    goal = K.obj(K.ellip_mesh(6, 4, 2.0), M("sand"), None, (0.0, 45.0, -1.2), name="goal_island")
    _ = goal
    palm(0.5, 44.0, 6.0, seed=60)
    palm(-2.0, 46.0, 5.5, seed=61)
    # 流される（右へ）→ 舵で曲がって島へ
    pts_drift = [(0.0, 0.0), (2.0, 2.0), (5.0, 3.5), (8.0, 4.5)]
    sc = bpy.context.scene
    f_a, f_b, f_c = fr(a16), fr(a17 + 0.5), fr(a18 + 0.1)
    for f in range(1, nf + 1, 2):
        if f <= f_b:
            u = (f - 1) / max(1, f_b - 1)
            x, y = 8.0 * u, 4.5 * math.sin(u * 1.2)
            face = -60 * u
        elif f <= f_c:
            x, y, face = 8.0, 4.5 + 0.8 * (f - f_b) / max(1, f_c - f_b), -60
        else:
            u = (f - f_c) / max(1, nf - f_c)
            face = -60 + 60 * K.smooth(min(1, u * 1.8))
            x, y = 8.0 - 3.0 * K.smooth(u), 5.3 + 9.0 * u
        t = f / FPS
        rf.location = (x, y, 0.09 + 0.04 * math.sin(2 * math.pi * 0.45 * t))
        rf.rotation_euler = (1.0 * D2R * math.sin(t * 2.1), 1.5 * D2R * math.sin(t * 2.6), face * D2R)
        rf.keyframe_insert("location", frame=f)
        rf.keyframe_insert("rotation_euler", frame=f)
    _ = (pts_drift, sc, f_a)
    for f, a in ((1, 0), (f_c, 0), (f_c + 10, 35), (nf, 35)):        # 舵の板の向き
        rd.rotation_euler = (0, 0, a * D2R)
        rd.keyframe_insert("rotation_euler", frame=f)
    bm = K.glow("current_blue", BLUE, 5.0)
    for k in range(4):
        K.flow_arrow([(-6.0 + 0.0 * k, -3.0 + 3.0 * k, 0.15), (2.0, -1.0 + 3.0 * k, 0.15), (10.0, 1.0 + 3.0 * k, 0.15)], bm, f_a, fr(a17),
                     width=0.12, name=f"current{k}")
    om = K.glow("turn_orange", YELLOW, 5.0)
    path = K.poly_curve([(8.0 - 3.0 * K.smooth(u), 5.3 + 9.0 * u, 0.2) for u in [i / 20 for i in range(21)]], 0.1, om, "turn_path")
    K.grow_line(path, f_c, f_c + 40)
    hl_r = K.obj(K.box_mesh(0.5, 2.2, 0.8), hl("rudder", fr(a17 + 0.3), fr(a17 + 0.6), fr(a18), fr(a18 + 0.3)), rd, (0, -1.1, -0.4),
                 name="rudder_hl", shadow=False)
    _ = hl_r
    hero, _d = panda((0, 0, 0), 180, drill_on=False)
    ride(hero, rf, (0.0, -1.5, LOG_R), 180, 1, nf)
    hero.stand(1, shL=(150, 30), shR=(150, 30), elL=110, elR=110)
    hero.pose(fr(a17 + 0.4), shL=(60, 10), shR=(60, -10), elL=30, elR=30, spine=-10)        # 舵をにぎる
    hero.pose(fr(a19), shL=(60, 10), shR=(165, 20), elL=30, elR=10)
    hero.wag(1, nf)
    fill_light((0.0, -8.0, 10.0), (4, 5, 0), 2500, 14.0)
    keys = [(0.0, (-4.0, -12.0, 14.0), (3.0, 3.0, 0.0), 26),
            (a17, (2.0, -6.0, 9.0), (7.0, 4.0, 0.0), 26),
            (a18, (-2.0, -8.0, 12.0), (5.0, 8.0, 0.0), 24),
            (T, (-3.0, -6.0, 13.0), (4.0, 14.0, 0.0), 24)]
    campath(keys, nf, shake=0.02)


# ============================ 6) こぐと疲れる → 帆 → 風で進む ============================
def s06_sail(nf):
    world(beach=False)
    T = SC["dur"]
    a20, _ = lt(20)
    a21, _ = lt(21)
    a22, _ = lt(22)
    rf, parts = raft("balsa", "raft", outrigger=True, pegs=True, rope=False, rudder=True, sail=True)
    ms, sl = parts["mast"], parts["sail"]
    f_m = fr(a21 + 0.05)
    K.key_scale(ms, 1, (1, 1, 1e-3))
    K.key_scale(ms, f_m, (1, 1, 1e-3))
    K.key_scale(ms, f_m + 8, (1, 1, 1))
    K.key_scale(sl, 1, (1, 1, 1e-3))
    K.key_scale(sl, f_m + 8, (1, 1, 1e-3))
    K.key_scale(sl, f_m + 18, (1, 1, 1))
    # ゆっくり → 風で速く
    for f in range(1, nf + 1, 2):
        t = f / FPS
        if f <= fr(a22):
            y = 0.25 * t
        else:
            y = 0.25 * a22 + 3.0 * (t - a22) ** 1.3
        rf.location = (0, y, 0.09 + 0.04 * math.sin(2 * math.pi * 0.45 * t))
        rf.rotation_euler = (1.0 * D2R * math.sin(t * 2.1), 1.5 * D2R * math.sin(t * 2.6), 0)
        rf.keyframe_insert("location", frame=f)
        rf.keyframe_insert("rotation_euler", frame=f)
    bm = K.glow("wind_blue", BLUE, 5.0)
    for k in range(3):
        K.flow_arrow([(-1.5 + 1.5 * k, -9.0, 2.0 + 0.5 * k), (-1.0 + 1.0 * k, -3.0, 2.2 + 0.3 * k), (-0.5 + 0.5 * k, 2.0, 2.4)], bm, fr(a22),
                     nf, width=0.1, name=f"wind{k}")
    # 主人公：かいでこぐ（汗）→ 帆を見上げる
    hero, _d = panda((0, 0, 0), 0, drill_on=False)
    ride(hero, rf, (0.6, -0.6, LOG_R), 90, 1, nf)
    pad = K.empty(name="paddle")
    K.obj(K.cyl_mesh(0.03, 0.03, 1.6, 8), M("wood"), pad, (0, 0, -0.5), name="paddle_shaft")
    box((0.22, 0.03, 0.45), (0, 0, -1.4), M("wood"), "paddle_blade", pad)
    hero.hold(pad, "R", (0, 0.02, 0), (-20, 0, 0))
    for k in range(int(fr(a21) / 12) + 1):
        f = 1 + 12 * k
        hero.pose(f, shR=(90, 30), elR=20, shL=(60, -20), elL=40, spine=-15)
        hero.pose(f + 6, shR=(10, 30), elR=20, shL=(20, -20), elL=40, spine=-25)
    hero.pose(fr(a21), shL=(150, 30), shR=(30, 8), elL=110, elR=30, spine=0, neck=-25)
    hero.pose(fr(a22 + 0.3), shL=(160, 40), shR=(160, 40), elL=15, elR=15, neck=-20)
    K.key_scale(pad, fr(a21) - 1, 1.0)
    K.key_scale(pad, fr(a21), 1e-4)
    hero.wag(1, nf)
    drops = K.mat("sweat", (0.6, 0.85, 1.0), 0.1)
    for k in range(6):
        d = K.obj(K.ellip_mesh(0.03, 0.03, 0.05), drops, hero.j["neck"], (0.12 * (1 if k % 2 else -1), 0.05, 0.25), name=f"sweat{k}",
                  shadow=False)
        K.key_scale(d, 1, 1e-4)
        K.key_scale(d, 8 + 10 * k, 1.0)
        K.key_loc(d, 8 + 10 * k, (0.12 * (1 if k % 2 else -1), 0.05, 0.25))
        K.key_loc(d, 18 + 10 * k, (0.2 * (1 if k % 2 else -1), 0.05, 0.05))
        K.key_scale(d, 18 + 10 * k, 1e-4)
    for k in range(int((nf - fr(a22)) / 6)):
        K.smoke_puffs((0.0, -2.2, 0.05), fr(a22) + 6 * k, n=2, seed=70 + k, col=(0.95, 0.97, 1.0), size=0.4, rise=0.1, life=24, spread=0.8,
                      alpha=0.7, name=f"wake{k}")
    fill_light((4.0, -4.0, 4.0), (0, 0, 1.0), 2000, 10.0)
    keys = [(0.0, (3.2, -2.8, 1.6), (0.2, 0.0, 0.9), 26),
            (a21, (4.5, -4.5, 2.6), (0.0, 0.8, 2.0), 24),
            (a22, (5.5, -5.5, 3.0), (0.0, 1.5, 1.8), 24),
            (T, (5.5, 1.0, 3.0), (0.0, 6.0, 1.6), 24)]
    campath(keys, nf, shake=0.02)


# ============================ 7) 横風で流される → センターボード ============================
def s07_board(nf):
    world(beach=False)
    T = SC["dur"]
    a23, _ = lt(23)
    a24, _ = lt(24)
    a25, _ = lt(25)
    a26, _ = lt(26)
    a27, _ = lt(27)
    rf, parts = raft("balsa", "raft", outrigger=True, pegs=True, rope=False, rudder=True, sail=True, boards=True)
    bd = parts["boards"]
    for k, b in enumerate(bd.children):              # 板が上から水の中へ
        z1 = b.location.z
        K.key_loc(b, 1, (b.location.x, b.location.y, z1 + 1.8))
        K.key_loc(b, fr(a25 + 0.2 * k), (b.location.x, b.location.y, z1 + 1.8))
        K.key_loc(b, fr(a25 + 0.2 * k + 0.5), (b.location.x, b.location.y, z1))
    # 前へ進みながら、横風で横へ流される → 板を入れると まっすぐ
    for f in range(1, nf + 1, 2):
        t = f / FPS
        drift = min(t, a25 + 0.8) - 0.0
        rf.location = (-0.9 * drift, 1.2 * t, 0.09 + 0.04 * math.sin(2 * math.pi * 0.45 * t))
        rf.rotation_euler = (1.0 * D2R * math.sin(t * 2.1), (4.0 if t < a26 else 1.5) * D2R * math.sin(t * 1.3) - 5 * D2R * (t < a26), 0)
        rf.keyframe_insert("location", frame=f)
        rf.keyframe_insert("rotation_euler", frame=f)
    om = K.glow("side_orange", ORANGE, 6.0)
    for k in range(3):
        K.flow_arrow([(9.0, -1.0 + 3.0 * k, 2.4), (2.0, -1.0 + 3.0 * k + 1.2, 2.4)], om, fr(a23), fr(a25 + 1.0), width=0.14,
                     name=f"side{k}")
    # 断面：水の中が見える（すけた水）
    sea = bpy.data.objects.get("sea")
    if sea:
        sea.scale = (1e-3, 1e-3, 1e-3)
    K.obj(K.box_mesh(400, 400, 0.02), sea_mat("sea_top", (0.03, 0.28, 0.42), alpha=0.55), None, (0, 0, -0.01), name="sea_top", shadow=False)
    K.obj(K.box_mesh(400, 400, 30), K.mat("deep", (0.02, 0.14, 0.24), 0.9, alpha=0.35), None, (0, 0, -15.05), name="deep", shadow=False)
    bm = K.glow("water_push", BLUE, 6.0)
    for k in range(3):
        K.flow_arrow([(-6.0, 1.2 * a26 * 0 + 1.2 * (a26 * 30 / 30) - 2 + 1.5 * k, -0.7), (-1.0, 1.2 * a26 - 2 + 1.5 * k, -0.7)], bm, fr(a26),
                     fr(a27 + 0.8), width=0.12, name=f"push{k}")
    hlb = K.obj(K.box_mesh(0.4, 3.2, 1.8), hl("boards", fr(a25 + 0.5), fr(a25 + 0.8), fr(a26 + 1.2), fr(a26 + 1.5), col=YELLOW, alpha=0.5),
                bd, (0.0, 0.0, -0.7), name="boards_hl", shadow=False)
    _ = hlb
    hero, _d = panda((0, 0, 0), 180, drill_on=False)
    ride(hero, rf, (-0.4, -1.5, LOG_R), 180, 1, nf)
    hero.stand(1, shL=(150, 30), shR=(150, 30), elL=110, elR=110)
    hero.pose(fr(a25), shL=(90, 10), shR=(90, -10), elL=30, elR=30, spine=-20)
    hero.pose(fr(a27), shL=(160, 40), shR=(160, 40), elL=15, elR=15)
    hero.wag(1, nf)
    fill_light((-4.0, -6.0, 2.0), (0, 4, -0.5), 2500, 10.0)
    keys = [(0.0, (8.0, -9.0, 6.0), (0.0, 1.5, 1.0), 24),
            (a24, (-3.0, 1.2 * a24 - 9.0, 0.4), (-1.6, 1.2 * a24, -0.4), 22),
            (a26, (-4.0, 1.2 * a26 - 9.5, 0.1), (-2.0, 1.2 * a26, -0.6), 22),
            (a27, (-3.5, 1.2 * a27 - 9.5, 0.6), (-2.0, 1.2 * a27, -0.3), 22),
            (T, (-3.5, 1.2 * T - 9.5, 1.0), (-2.0, 1.2 * T, 0.0), 22)]
    campath(keys, nf, shake=0.02)


# ============================ 8) 【実話】1947年 コンティキ号：太平洋を101日、約7000km ============================
SAM = [(-79.6, 0.0), (-80.5, -5.0), (-77.0, -12.0), (-70.4, -18.5), (-71.5, -30.0), (-73.5, -40.0), (-74.0, -50.0), (-68.0, -55.0),
       (-65.0, -52.0), (-58.0, -40.0), (-48.0, -26.0), (-39.0, -13.0), (-35.0, -7.0), (-50.0, 0.0), (-60.0, 8.0), (-72.0, 11.0),
       (-77.0, 8.0)]                       # 南アメリカのおおまかな形（経度、緯度）
MAPS = 0.075                                # 地図の大きさ：経度・緯度 1度 → 0.075m


def mp(lon, lat, z=0.0):
    return ((lon + 110.0) * MAPS, (lat + 15.0) * MAPS, z)


def kontiki(name="kt"):
    """コンティキ号のようないかだ（バルサ9本・竹の小屋・四角い帆）と6人。"""
    root = K.empty((0, 0, 0), None, name)
    for i in range(9):
        L = 4.2 if i in (0, 8) else 4.8 + 0.4 * (4 - abs(4 - i)) / 4
        K.obj(K.cyl_mesh(0.22, 0.2, L, 12), M("balsa"), root, (-1.8 + 0.45 * i, 0, 0), rot=(90 * D2R, 0, 0), name=f"{name}_log{i}")
    hut = K.empty((0, -0.6, 0.2), root, f"{name}_hut")
    box((1.6, 1.6, 0.9), (0, 0, 0.45), K.noisy("bamboo", (0.70, 0.60, 0.38), 20.0, 0.15, 0.3, 0.9), f"{name}_hutb", hut)
    box((1.9, 1.9, 0.08), (0, 0, 1.0), K.mat("thatch", (0.55, 0.45, 0.25), 0.9), f"{name}_roof", hut)
    for sx in (-1, 1):
        K.obj(K.cyl_mesh(0.06, 0.05, 3.6, 8), M("wood"), root, (sx * 0.6, 0.9, 1.8), rot=(0, sx * 8 * D2R, 0), name=f"{name}_mast")
    K.obj(K.cyl_mesh(0.05, 0.05, 2.4, 8), M("wood"), root, (0, 0.9, 3.4), rot=(0, 90 * D2R, 0), name=f"{name}_yard")
    box((2.2, 0.04, 2.3), (0, 0.95, 2.2), M("sail"), f"{name}_sail", root)
    looks = [dict(K.WORKER, top=c, hat=None) for c in ((0.85, 0.85, 0.80), (0.35, 0.45, 0.60), (0.60, 0.50, 0.35), (0.85, 0.85, 0.80),
                                                        (0.40, 0.40, 0.42), (0.70, 0.30, 0.25))]
    crew = []
    for k, (x, y, face) in enumerate([(-1.2, 1.6, 160), (1.1, 1.5, 200), (-1.3, -1.8, 120), (1.2, -1.9, 230), (-0.5, 2.0, 180),
                                      (0.6, -1.9, 180)]):
        p = K.Person((x, y, 0.2), face, looks[k], name=f"{name}_crew{k}", scale=0.9)
        p.root.parent = root
        p.stand(1)
        p.wave(1 + 6 * k, 1 + 6 * k + 40, "R")
        crew.append(p)
    return root, crew


def s08_kontiki(nf):
    T = SC["dur"]
    a28, _ = lt(28)
    a29, _ = lt(29)
    a30, _ = lt(30)
    a31, _ = lt(31)
    K.daylight(elev=60, az=200)
    # 地図（太平洋）：海は青、南アメリカは緑、ポリネシアの島は小さな点
    mapo = K.obj(K.box_mesh(11.0, 6.0, 0.05), K.mat("map_sea", (0.10, 0.36, 0.60), 0.7), None, (mp(-110, -15)[0] - 0.4, mp(-110, -15)[1], -0.03),
                 name="map_sea")
    _ = mapo
    grid = []
    for lon in range(-170, -40, 10):
        grid.append(((mp(lon, 0)[0], mp(-110, -15)[1], 0.0), (0.01, 6.0, 0.005)))
    for lat in range(-50, 25, 10):
        grid.append(((mp(-110, lat)[0], mp(-110, lat)[1], 0.0), (11.0, 0.01, 0.005)))
    bmg = bmesh.new()
    for c, s in grid:
        r_ = bmesh.ops.create_cube(bmg, size=1.0)
        for v in r_["verts"]:
            v.co = Vector((v.co.x * s[0] + c[0], v.co.y * s[1] + c[1], v.co.z * s[2] + c[2]))
    me = bpy.data.meshes.new("grid")
    bmg.to_mesh(me)
    bmg.free()
    me.materials.append(None)
    K.obj(me, K.mat("map_grid", (0.45, 0.65, 0.85), 0.6), None, (0, 0, 0), name="map_grid", shadow=False)
    me = bpy.data.meshes.new("sam")
    me.from_pydata([mp(lo, la, 0.02) for lo, la in SAM], [], [list(range(len(SAM)))])
    me.materials.append(None)
    K.obj(me, K.mat("land", (0.42, 0.55, 0.28), 0.8), None, (0, 0, 0), name="south_america")
    isl = K.mat("isl", (0.45, 0.62, 0.30), 0.8)
    for lo, la in [(-142.5, -16.0), (-145, -17.5), (-149.5, -17.6), (-140, -14), (-138, -19), (-151, -16.5), (-147, -15)]:
        K.obj(K.ellip_mesh(0.07, 0.07, 0.03), isl, None, mp(lo, la, 0.02), name="isl")
    # 出発（ペルー・カヤオ）と到着（ラロイア環礁）
    pA, pB = mp(-77.2, -12.0, 0.06), mp(-142.4, -16.0, 0.06)
    rm = K.glow("pin_red", (1.0, 0.15, 0.08), 6.0)
    K.obj(K.ellip_mesh(0.12, 0.12, 0.12), rm, None, pA, name="pinA", shadow=False)
    pinB = K.obj(K.ellip_mesh(0.14, 0.14, 0.14), K.glow("pin_yellow", YELLOW, 8.0), None, pB, name="pinB", shadow=False)
    K.show(pinB, fr(a31 + 0.4), pop=6)
    route_pts = []
    for k in range(31):
        u = k / 30
        lon = -77.2 + (-142.4 + 77.2) * u
        lat = -12.0 + (-16.0 + 12.0) * u - 4.0 * math.sin(math.pi * u)
        route_pts.append(mp(lon, lat, 0.07))
    route = K.poly_curve(route_pts, 0.04, K.glow("route_yellow", YELLOW, 6.0), "route")
    K.grow_line(route, fr(a30), fr(a31 + 0.4))
    mk = K.obj(K.box_mesh(0.18, 0.24, 0.06), M("balsa"), None, route_pts[0], name="raft_marker")
    for k in range(31):
        f = fr(a30) + int((fr(a31 + 0.4) - fr(a30)) * k / 30)
        K.key_loc(mk, f, route_pts[k])
    # いかだ（6人）の場面：L29 のあいだだけ、別の場所の海に
    world_y = 300.0
    sea = K.obj(K.box_mesh(4000, 4000, 0.02), sea_mat(), None, (0, world_y, -0.01), name="sea", shadow=False)
    _ = sea
    kt, crew = kontiki()
    bob(kt, 1, nf, base=(0, world_y, 0.12), amp=0.08, rock=2.5, seed=8)
    K.clouds(seed=9)
    cx, cy = mp(-110, -15)[0], mp(-110, -15)[1]
    keys = [(0.0, (cx + 1.0, cy - 8.0, 7.5), (cx + 0.6, cy, 0.0), 24),
            (a29 - 0.1, (cx + 0.6, cy - 7.4, 7.0), (cx + 0.4, cy, 0.0), 24),
            (a29, (5.5, world_y - 6.5, 2.4), (0.0, world_y, 1.2), 26),
            (a30 - 0.1, (4.0, world_y - 7.5, 2.0), (0.0, world_y, 1.2), 26),
            (a30, (cx + 0.4, cy - 7.6, 7.0), (cx + 0.2, cy, 0.0), 24),
            (T, (cx - 0.8, cy - 7.0, 6.2), (cx - 0.8, cy, 0.0), 24)]
    campath(keys, nf, shake=0.01, cuts=[a29, a30])
    fill_light((cx, cy - 6, 8), (cx, cy, 0), 1500, 12.0)
    _ = crew


# ============================ 9) 最後に帆柱をドリルでとめる → 完成 ============================
def s09_final(nf):
    world(beach=True)
    T = SC["dur"]
    a32, _ = lt(32)
    a33, _ = lt(33)
    base = (0.0, 4.0, 0.09)
    rf, parts = raft("balsa", "raft", outrigger=True, pegs=True, rope=False, rudder=True, sail=True, boards=True)
    bob(rf, 1, fr(a33), base=base, amp=0.03, rock=1.0, seed=9)
    for f in range(fr(a33), nf + 1, 2):             # 完成：沖へ走りだす
        t = (f - fr(a33)) / FPS
        rf.location = (0, 4.0 + 1.2 * t * t, 0.09 + 0.04 * math.sin(2 * math.pi * 0.45 * f / FPS))
        rf.keyframe_insert("location", frame=f)
    hero, dr = panda((0, 0, 0), 180)
    ms = parts["mast"]
    sc = bpy.context.scene
    # 帆柱の根もとの金具（4本のボルト）を、ドリルで
    bolts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            b = K.obj(K.cyl_mesh(0.025, 0.025, 0.05, 6), K.mat("bolt_steel", (0.6, 0.6, 0.62), 0.3), ms, (sx * 0.18, sy * 0.18, 0.07),
                      name="bolt")
            bolts.append(b)
    local = (0.33, 0.4 + 0.52, LOG_R)
    ride(hero, rf, local, 180, 1, nf)
    hero.stand(1, **DRILL_LOG)
    for k in range(10):
        hero.pose(2 + 4 * k, **dict(DRILL_LOG, spine=-22 + (3 if k % 2 else -3)))
    hero.pose(fr(a33 - 0.1), **DRILL_LOG)
    hero.pose(fr(a33 + 0.3), spine=0, neck=-10, shR=(165, 20), elR=10, shL=(20, -8), elL=20, hipL=0, hipR=0, kneeL=0, kneeR=0, hz=0)
    hero.wag(1, nf)
    K.spin(dr, 1, fr(a33 - 0.1), 80)
    tip = tip_at(dr, 10)
    print("final tip", tip)
    K.drill_fx(tip, 2, fr(a33 - 0.1), "chips", seed=91, n=50)
    K.key_rot(bolts[0], 1, (0, 0, 0))
    K.key_rot(bolts[0], fr(a33 - 0.1), (0, 0, 14.0))
    _ = sc
    fill_light((2.0, -2.0, 3.0), (0.2, 4.6, 0.6), 1800, 6.0)
    keys = [(0.0, (1.6, 2.5, 1.2), (0.25, 4.75, 0.75), 24),
            (a32 + 1.0, (-1.1, 2.5, 1.3), (0.25, 4.75, 0.8), 24),
            (a33 - 0.1, (-1.2, 2.3, 1.4), (0.25, 4.75, 0.85), 24),
            (a33 + 0.6, (3.0, -4.0, 2.6), (0.0, 6.0, 1.2), 24),
            (T, (4.0, -9.0, 3.4), (0.0, 9.0, 1.4), 24)]
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
