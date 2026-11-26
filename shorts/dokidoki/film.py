"""「もしも恋のドキドキが周りに聞こえるようになったら？」全場面の3D（Blender / bpy）。フェロモン版（PH-001）の部品と人を使う。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]
心臓の音は目に見えないので、胸から広がる赤い輪（音の波）で見せる。拍の時刻は beats.py（合成の音と同じ）。"""
import importlib.util
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timeline as TL  # noqa: E402  （フェロモン版より先に読み込む＝こちらの時間割を使わせる）
import beats as BT  # noqa: E402

_spec = importlib.util.spec_from_file_location("ph_film", os.path.join(HERE, "..", "pheromone", "film.py"))
PF = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PF)
FJ, C, W, F, SG, bpy = PF.FJ, PF.C, PF.W, PF.F, PF.SG, PF.bpy
from mathutils import Vector  # noqa: E402

FPS = TL.FPS
fr = C.frame_of
cut, fill = FJ.cut, PF.fill
L, actor, person, crowd_look, vis = PF.L, PF.actor, PF.person, PF.crowd_look, PF.vis
KACHO, WIFE, YOUNG_M, YOUNG_W = PF.KACHO, PF.WIFE, PF.YOUNG_M, PF.YOUNG_W
smooth, lerp3 = PF.smooth, PF.lerp3
RED = (1.0, 0.16, 0.24)
CHEST = 1.18


# ---------- 音の輪（胸から広がる） ----------
def ring_mat(name="ring", col=RED, strength=4.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    pw = nt.nodes.new("ShaderNodeMath")
    pw.operation = 'POWER'
    pw.inputs[1].default_value = 2.2
    nt.links.new(lw.outputs["Facing"], pw.inputs[0])
    oi = nt.nodes.new("ShaderNodeObjectInfo")
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = 'MULTIPLY'
    nt.links.new(pw.outputs[0], mul.inputs[0])
    nt.links.new(oi.outputs["Alpha"], mul.inputs[1])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*col, 1)
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(mul.outputs[0], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    try:
        m.blend_method = 'BLEND'
    except AttributeError:
        pass
    return m


_RME = {}


def ring_mesh():
    if "m" not in _RME:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0)
        o = bpy.context.object
        for p in o.data.polygons:
            p.use_smooth = True
        _RME["m"] = o.data
        o.data.use_fake_user = True
        bpy.data.objects.remove(o)
    return _RME["m"]


def heart_rings(src, times, nf, name="hr", size=1.0, speed=1.7, life=0.85, alpha=0.9, dub=True, mat=None, t_off=0.0):
    """拍の時刻（場面の中の秒）ごとに、胸から輪を出す。src＝(x,y,z) か 関数 f→(x,y,z)。dub＝「ドクン」の2つ目の小さい輪。"""
    me = ring_mesh()
    mat = mat or ring_mat()
    objs = []
    k = 0
    for t in times:
        for j, (dt, s_mul, a_mul) in enumerate(((0.0, 1.0, 1.0), (0.2, 0.75, 0.6)) if dub else ((0.0, 1.0, 1.0),)):
            fb = fr(t + dt + t_off)
            if fb >= nf:
                continue
            o = bpy.data.objects.new(f"{name}{k}", me)
            bpy.context.collection.objects.link(o)
            o.data.materials.clear() if False else None
            o.active_material = mat
            o.visible_shadow = False
            k += 1
            p = Vector(src(fb) if callable(src) else src)
            o.location = p
            o.keyframe_insert("location", frame=max(1, fb))
            Lf = int(life * FPS)
            o.scale = (1e-4,) * 3
            o.keyframe_insert("scale", frame=max(1, fb - 1))
            o.color = (1, 1, 1, 0)
            o.keyframe_insert("color", frame=max(1, fb - 1))
            for g in list(range(fb, min(nf, fb + Lf) + 1, 2)):
                u = (g - fb) / Lf
                r = (0.12 + speed * size * u * life) * s_mul
                o.scale = (r, r, r)
                o.keyframe_insert("scale", frame=g)
                o.color = (1, 1, 1, alpha * a_mul * (1 - u) ** 1.4 / (1 + 1.2 * r * r))
                o.keyframe_insert("color", frame=g)
            g = min(nf, fb + Lf) + 1
            o.scale = (1e-4,) * 3
            o.keyframe_insert("scale", frame=g)
            objs.append(o)
    return objs


def chest_of(root, dz=CHEST):
    """人（actor の root）の胸の位置を、コマごとに返す関数。"""
    def f(fr_):
        sc = bpy.context.scene
        sc.frame_set(max(1, fr_))
        p = root.matrix_world.translation.copy()
        sc.frame_set(1)
        return (p.x, p.y, p.z + dz)
    return f


def crowd_rings(roots, t0, t1, nf, seed=1, bpm=(68, 92), size=0.7, alpha=0.5, every=1):
    r = random.Random(seed)
    for k, o in enumerate(roots[::every]):
        b = r.uniform(*bpm)
        ts = BT.beats(t0, t1, lambda t, b=b: b, r.uniform(0, 60 / b))
        p = chest_of(o)(fr(t0) + 1)
        heart_rings(p, ts, nf, f"cr{seed}_{k}_", size=size, alpha=alpha, dub=False)


def main_rings(scene, src, nf, size=1.3, alpha=1.0, name="mr"):
    return heart_rings(src, BT.main_beats(scene), nf, name, size=size, alpha=alpha)


# ============================ 冒頭：朝の交差点 → 5.6秒で全員の胸から輪 ============================
F_ON = fr(TL.T_VANISH)


def cp(f):
    if f <= F_ON:
        return lerp3((-0.6, -20.0, 1.3), (-0.25, -5.6, 1.6), smooth((f - 1) / (F_ON - 1)) * 0.8 + 0.2 * (f - 1) / (F_ON - 1))
    return lerp3((-0.25, -5.6, 1.6), (-0.6, -6.6, 2.1), smooth((f - F_ON) / 40))


def ca(f):
    if f <= F_ON:
        return lerp3((0.4, -0.5, 1.5), (0.2, -3.0, 1.45), smooth((f - 1) / (F_ON - 1)))
    return lerp3((0.2, -3.0, 1.45), (0.1, -2.6, 1.8), smooth((f - F_ON) / 40))


def d00_open(nf):
    FJ.morning()
    PF.crossing_set()
    r = random.Random(31)
    kacho = actor(1, L(KACHO, face="neutral"), [(1, 0.4, 4.5, 180), (F_ON, 0.2, -3.0, 180), (nf, 0.2, -3.0, 180)], nf,
                  face_at=(F_ON + 3, "surprised", "cheek"))
    roots = PF.crossing_crowd(r, nf, F_ON, n=70, avoid=[(0.3, 0.0, 1.2), (0.2, -3.0, 1.3), (-0.4, -6.0, 1.6)])
    for k in range(20):                       # カメラのすぐ前を横切る人（最初の5秒を強く動かす）
        tk = 0.12 + k * 0.27 + r.uniform(-0.05, 0.05)
        fk = 1 + tk * FPS
        cy = cp(min(fk, F_ON))[1]
        y = cy + r.uniform(1.6, 3.8)
        if y > -4.5:
            continue
        sx = 1 if k % 2 else -1
        sp = r.uniform(1.5, 1.9)
        way = [(1, -0.5 + sx * sp * (1 - fk) / FPS, y), (nf, -0.5 + sx * sp * (nf - fk) / FPS, y)]
        actor(200 + k, crowd_look(r), way, nf, period=7)
    t_on = TL.T_VANISH
    crowd_rings(roots, t_on, nf / FPS, nf, seed=3, alpha=0.55)
    main_rings("d00_open", chest_of(kacho), nf, size=1.2)
    c = PF.track_cam(cp, ca, 1, nf, 24)
    PF.shake(c, 1, F_ON + 10, 1.1, seed=5)
    fill((-1.5, -7.0, 2.4), (0.2, -3.0, 1.5), power=70)
    return nf


# ============================ 同じ瞬間：交差点の全員から ============================
def d01_burst(nf):
    FJ.morning()
    PF.crossing_set()
    r = random.Random(32)
    roots = []
    for k in range(70):
        x, y = r.uniform(-10, 10), r.uniform(-10, 10)
        way = PF.look_around(r, (x, y), r.randint(1, 20), nf, r.uniform(0, 360), n=3)
        roots.append(actor(40 + k, crowd_look(r, "surprised"), way, nf, arms=r.choice(["cheek", "down", "head"])))
    k_root = actor(1, L(KACHO, face="surprised"), PF.look_around(r, (0.2, -3.0), 10, nf, 180, n=2), nf, arms="cheek")
    crowd_rings(roots, 0.0, nf / FPS, nf, seed=4, alpha=0.6, size=0.9)
    main_rings("d01_burst", chest_of(k_root), nf, size=1.1)
    W.camera((-13.0, -17.0, 6.5), (0.0, -1.0, 1.0), lens=26)
    fill((-6.0, -12.0, 5.0), (0, 0, 1.2), power=200, size=4)
    return nf


# ============================ 満員電車：若い2人。青年の輪だけ速く大きい ============================
def d02_train(nf):
    FJ.room((0.95, 0.95, 0.95), 0.9)
    PF.train_car(nf=nf)
    r = random.Random(33)
    pm, pw = (0.55, -5.0), (0.55, -4.25)
    yman = actor(2, L(YOUNG_M, face="neutral"), [(1, *pm, 0), (nf, *pm, 0)], nf, arms=("down", "up"), face_at=(fr(1.6), "blush", ("down", "up")))
    actor(3, L(YOUNG_W, face="neutral"), [(1, *pw, 180), (nf, *pw, 180)], nf, arms=("up", "down"), face_at=(fr(3.0), "blush", ("up", "down")))
    others = []
    for k, (x, y, f0) in enumerate([(-0.6, -5.6, 120), (-0.5, -4.2, 60), (-0.7, -3.4, 150), (0.75, -3.4, 200), (0.0, -6.4, 30), (-0.1, -2.6, 170)]):
        to_m = math.degrees(math.atan2(pm[0] - x, pm[1] - y))
        way = [(1, x, y, f0), (fr(2.4) + 2 * k, x, y, f0), (nf, x, y, to_m)]
        others.append(actor(80 + k, crowd_look(r, "surprised"), way, nf, arms=("hold", "up") if k % 2 else ("up", "down")))
    for k in range(8):
        sx = -1 if k % 2 else 1
        PF.person((sx * (PF.CAR_W / 2 - 0.42), -8.0 + 1.6 * k, 0.28), 90 * sx + 180, seed=60 + k, pose="sit", look=crowd_look(r, "neutral"))
    crowd_rings(others, 0.0, nf / FPS, nf, seed=5, alpha=0.35, size=0.5)
    main_rings("d02_train", chest_of(yman), nf, size=1.2)
    W.camera((1.0, -7.4, 1.6), (0.45, -4.6, 1.45), lens=26)
    cut(fr(2.6), (-0.6, -4.0, 1.55), (0.55, -5.0, 1.55), lens=32, orbit=3, push=0.1)
    fill((0.6, -6.8, 2.0), (0.5, -4.6, 1.4), power=60)
    return nf


# ============================ 駅のホーム：音は、はなれると小さくなる ============================
def d03_distance(nf):
    FJ.day(elev=40, az=200)
    plat = W.mat("platform2", (0.70, 0.68, 0.62), 0.8)
    W.box((0, 4.0, -0.1), (8.0, 30.0, 0.2), plat, bevel=0)
    W.box((-2.4, 4.0, 0.004), (0.3, 30.0, 0.01), W.mat("tactile2", (0.95, 0.80, 0.15), 0.7), bevel=0)
    W.box((3.8, 4.0, 1.5), (0.3, 30.0, 3.0), W.mat("plat_wall", (0.85, 0.85, 0.82), 0.8), bevel=0)
    W.box((0, 4.0, 3.4), (8.0, 30.0, 0.15), W.mat("plat_roof", (0.55, 0.57, 0.60), 0.6), bevel=0)
    r = random.Random(34)
    # 青年（ドキドキ）と、1倍・2倍のきょりの人
    yman = actor(2, L(YOUNG_M, face="blush"), [(1, 0.0, 0.0, 0), (nf, 0.0, 0.0, 0)], nf, arms="cheek")
    near = actor(81, crowd_look(r, "surprised"), [(1, 0.0, 2.0, 180), (nf, 0.0, 2.0, 180)], nf, arms="cheek")
    far = actor(82, crowd_look(r, "neutral"), [(1, 0.0, 4.0, 180), (nf, 0.0, 4.0, 180)], nf, arms="down")
    _ = (near, far)
    main_rings("d03_distance", chest_of(yman), nf, size=2.4, alpha=1.0)
    wm = W.mat("dim_w", (1, 1, 1), 0.5, emit=(1, 1, 1), emit_strength=2.0)
    for k, (y0, y1) in enumerate(((0.0, 2.0), (0.0, 4.0))):
        x = -1.0 - 0.5 * k
        W.box((x, (y0 + y1) / 2, 0.02), (0.05, y1 - y0, 0.02), wm, bevel=0)
        for y in (y0, y1):
            W.box((x, y, 0.02), (0.3, 0.05, 0.02), wm, bevel=0)
    PF.sign((-1.0, 1.0, 0.03), 0.55, 0.3, PF.text_texture("dist1.png", [("1倍", 150)], size=(400, 220), bg=(30, 30, 30)), "dist1", rot_x=0)
    PF.sign((-1.5, 3.0, 0.03), 0.55, 0.3, PF.text_texture("dist2.png", [("2倍", 150)], size=(400, 220), bg=(30, 30, 30)), "dist2", rot_x=0)
    W.camera((-5.5, 2.0, 3.2), (0.0, 2.0, 0.9), lens=26)
    fill((-3.0, 2.0, 3.0), (0, 2, 1.0), power=80)
    return nf


# ============================ 会議室：課長のポーカーフェイスが通じない ============================
def d04_meeting(nf):
    FJ.room((0.95, 0.93, 0.90), 1.0)
    FJ.window_sun(30, 200, 2.6)
    W.box((0, 2, -0.05), (12, 12, 0.1), W.mat("carpet2", (0.36, 0.40, 0.46), 1.0), bevel=0)
    W.box((0, 5.5, 1.5), (12, 0.2, 3.0), W.mat("mtg_wall", (0.90, 0.89, 0.86), 0.9), bevel=0)
    W.box((0, 2.0, 0.74), (1.4, 4.0, 0.06), W.mat("mtg_table", (0.55, 0.40, 0.28), 0.5), bevel=0.01)
    scr = W.box((0, 5.35, 1.7), (2.6, 0.05, 1.4), W.mat("screen_w", (0.95, 0.95, 0.95), 0.5, emit=(0.9, 0.95, 1.0), emit_strength=1.0),
                bevel=0)
    _ = scr
    PF.sign((0, 5.32, 1.75), 2.4, 1.2, PF.text_texture("sales.png", [("売上報告", 130), ("前年比 98%", 90)], size=(1024, 512),
                                                        bg=(245, 245, 245), fg=(40, 40, 60)), "sales")
    r = random.Random(35)
    seats = [(-1.1, 1.0), (-1.1, 2.0), (-1.1, 3.0), (1.1, 1.0), (1.1, 2.0), (1.1, 3.0)]
    for k, (x, y) in enumerate(seats):
        fc = 90 if x < 0 else 270
        o = PF.person((x, y, 0.3), fc, seed=90 + k, pose="sit", look=crowd_look(r, "neutral"))
        o2 = PF.person((x, y, 0.3), math.degrees(math.atan2(0.0 - x, 4.4 - y)), seed=90 + k, pose="sit", look=crowd_look(r, "surprised"))
        vis(o, [(1, True), (fr(2.4) + 3 * k, False)])
        vis(o2, [(1, False), (fr(2.4) + 3 * k, True)])
    kacho = actor(1, L(KACHO, face="neutral"), [(1, 0.9, 4.4, 200), (nf, 0.9, 4.4, 200)], nf, arms="hold",
                  face_at=(fr(2.0), "worried", "brow"))
    main_rings("d04_meeting", chest_of(kacho), nf, size=1.5)
    W.camera((0.2, -1.6, 1.9), (0.4, 3.8, 1.3), lens=26)
    fill((0.5, 0.0, 2.4), (0.8, 4.2, 1.4), power=90)
    return nf


# ============================ 【実話】1974年 カナダ：ゆれるつり橋 ============================
def d05_bridge(nf):
    FJ.day(elev=35, az=210)
    rock = W.mat("canyon_rock", (0.42, 0.38, 0.32), 0.95)
    for sx in (-1, 1):
        W.box((sx * 18.0, 10.0, -20.0), (20.0, 60.0, 40.0), rock, bevel=0)
    W.box((0, 10.0, -68.0), (60, 60, 2), W.mat("river", (0.20, 0.35, 0.40), 0.3), bevel=0)
    r = random.Random(36)
    for k in range(40):
        C.tree((r.choice([-1, 1]) * r.uniform(9, 26), r.uniform(-10, 40), 0), h=r.uniform(8, 16), seed=360 + k)
    # つり橋（左右にゆれる）
    br = bpy.data.objects.new("bridge", None)
    bpy.context.collection.objects.link(br)
    plank = W.mat("plank2", (0.50, 0.36, 0.22), 0.8)
    rope = W.mat("rope2", (0.55, 0.45, 0.30), 0.9)
    for k in range(60):
        x = -15.0 + 0.5 * k
        sag = -0.8 * (1 - (x / 15.0) ** 2)
        o = W.box((x, 0, sag), (0.42, 1.4, 0.06), plank, bevel=0)
        o.parent = br
    for sy in (-1, 1):
        for k in range(30):
            x0, x1 = -15.0 + k, -14.0 + k
            s0, s1 = -0.8 * (1 - (x0 / 15) ** 2), -0.8 * (1 - (x1 / 15) ** 2)
            o = W.box(((x0 + x1) / 2, sy * 0.7, (s0 + s1) / 2 + 1.0), (1.02, 0.04, 0.04), rope, bevel=0)
            o.parent = br
    for f in range(1, nf + 1, 2):
        t = f / FPS
        br.rotation_euler = (6 * math.pi / 180 * math.sin(2 * math.pi * 0.7 * t), 0, 0)
        br.location = (0, 0.15 * math.sin(2 * math.pi * 0.7 * t), 0.05 * math.sin(2 * math.pi * 1.4 * t))
        br.keyframe_insert("rotation_euler", frame=f)
        br.keyframe_insert("location", frame=f)
    man = actor(2, {"hair": (0.25, 0.18, 0.12), "top": (0.55, 0.45, 0.35), "bottom": (0.30, 0.28, 0.25), "face": "surprised"},
                [(1, -6.0, 0.0), (fr(1.6), -1.0, 0.0, 90), (nf, -1.0, 0.0, 90)], nf, face_at=(fr(2.2), "blush", "hold"))
    woman = actor(3, {"hair": (0.15, 0.10, 0.06), "top": (0.70, 0.30, 0.30), "bottom": (0.25, 0.25, 0.30), "long": True, "face": "happy"},
                  [(1, 0.0, 0.0, 270), (nf, 0.0, 0.0, 270)], nf, arms="hold")
    for o in (man, woman):
        o.parent = br
    main_rings("d05_bridge", chest_of(man, CHEST - 0.6), nf, size=1.3)
    W.camera((-2.0, -5.5, 1.6), (-0.5, 0.0, 0.6), lens=24)
    fill((-2.0, -4.0, 2.0), (-0.5, 0, 0.6), power=120)
    return nf


# ============================ 遊園地：ジェットコースター ============================
def coaster_track(pts, m, name="track"):
    for k in range(len(pts) - 1):
        a, b = Vector(pts[k]), Vector(pts[k + 1])
        d = b - a
        o = W.box(tuple((a + b) / 2), (0.9, d.length + 0.05, 0.08), m, bevel=0)
        o.rotation_euler = d.to_track_quat('Y', 'Z').to_euler()
        if k % 3 == 0 and a.z > 0.5:
            W.box((a.x, a.y, a.z / 2), (0.12, 0.12, a.z), m, bevel=0)


def d06_coaster(nf):
    FJ.day(elev=45, az=200)
    C.grass_ground(col=(0.30, 0.46, 0.17), name="grass_park2", tufts=600, area=(-20, 20, -10, 30), seed=37)
    m = W.mat("track_red", (0.80, 0.12, 0.10), 0.4)
    pts = []
    for k in range(80):
        y = -10.0 + 0.5 * k
        z = 14.0 if y < 2 else max(1.0, 14.0 - 13.0 * smooth((y - 2.0) / 9.0))
        if y > 13:
            z = 1.0 + 4.0 * math.sin((y - 13.0) / 12.0 * math.pi)
        pts.append((0.0, y, z))
    coaster_track(pts, m)
    # 車両（2人が乗る）：落ちる
    car = bpy.data.objects.new("cart", None)
    bpy.context.collection.objects.link(car)
    W.box((0, 0, 0.35), (1.1, 2.0, 0.5), W.mat("cart_y", (0.95, 0.75, 0.10), 0.4), bevel=0.05).parent = car
    pm = actor(2, L(YOUNG_M, face="surprised"), [(1, -0.25, 0.1, 0), (nf, -0.25, 0.1, 0)], nf, arms="up", face_at=(fr(3.2), "love", "down"))
    pw = actor(3, L(YOUNG_W, face="surprised"), [(1, 0.25, 0.1, 0), (nf, 0.25, 0.1, 0)], nf, arms="up", face_at=(fr(3.2), "love", "down"))
    for o in (pm, pw):
        o.parent = car
        o.scale = (0.9, 0.9, 0.9)

    def pos(t):
        if t < 1.0:
            y = -2.0 + 2.0 * t
        else:
            y = 0.0 + 9.0 * (t - 1.0) ** 1.6
        y = min(y, 28.0)
        for k in range(len(pts) - 1):
            if pts[k][1] <= y <= pts[k + 1][1]:
                u = (y - pts[k][1]) / (pts[k + 1][1] - pts[k][1])
                z = pts[k][2] + (pts[k + 1][2] - pts[k][2]) * u
                ang = math.atan2(pts[k + 1][2] - pts[k][2], pts[k + 1][1] - pts[k][1])
                return (0.0, y, z + 0.1), ang
        return (0.0, y, pts[-1][2]), 0.0
    for f in range(1, nf + 1):
        p, ang = pos(f / FPS)
        car.location = p
        car.rotation_euler = (ang, 0, 0)
        car.keyframe_insert("location", frame=f)
        car.keyframe_insert("rotation_euler", frame=f)
    for k, o in enumerate((pm, pw)):
        main_rings("d06_coaster", chest_of(o, CHEST - 0.15), nf, size=1.3, name=f"cr{k}_")
    c = W.camera((5.5, -6.0, 15.5), (0.0, 0.0, 14.5), lens=26)
    c["keep"] = 1
    for f in range(1, nf + 1, 2):
        p, _a = pos(f / FPS)
        c.location = (5.0, p[1] - 5.0, p[2] + 1.6)
        W.aim(c, Vector((0.0, p[1] + 0.5, p[2] + 0.6)))
        c.keyframe_insert("location", frame=f)
        c.keyframe_insert("rotation_euler", frame=f)
    fill((4.0, 0.0, 10.0), (0, 6, 6), power=200, size=6)
    return nf


# ============================ 図書館：静かな場所がうるさい ============================
def d07_library(nf):
    FJ.room((0.95, 0.90, 0.80), 0.9)
    FJ.window_sun(30, 220, 2.4)
    W.box((0, 3, -0.05), (14, 14, 0.1), W.mat("lib_floor", (0.55, 0.42, 0.30), 0.6), bevel=0)
    W.box((0, 8.0, 1.6), (14, 0.2, 3.2), W.mat("lib_wall", (0.88, 0.85, 0.78), 0.9), bevel=0)
    r = random.Random(38)
    book_cols = [(0.6, 0.15, 0.12), (0.15, 0.3, 0.55), (0.2, 0.45, 0.25), (0.8, 0.65, 0.2), (0.4, 0.3, 0.5)]
    for sx in (-1, 1):
        for k in range(3):
            x = sx * (2.5 + 1.8 * k)
            W.box((x, 7.4, 1.1), (1.4, 0.4, 2.2), W.mat("shelf_w", (0.45, 0.32, 0.20), 0.7), bevel=0)
            for z in (0.4, 0.9, 1.4, 1.9):
                for j in range(8):
                    W.box((x - 0.6 + 0.15 * j, 7.2, z + 0.12), (0.1, 0.05, 0.3), W.mat(f"book{j % 5}", book_cols[j % 5], 0.7), bevel=0)
    roots = []
    for row in range(2):
        W.box((0, 1.6 + 2.4 * row, 0.74), (6.0, 1.0, 0.06), W.mat("lib_table", (0.55, 0.40, 0.28), 0.5), bevel=0.01)
        for k in range(5):
            for sy in (-1, 1):
                x = -2.4 + 1.2 * k
                y = 1.6 + 2.4 * row + sy * 0.75
                o = PF.person((x, y, 0.3), 0 if sy < 0 else 180, seed=100 + k + 10 * row + (sy > 0), pose="sit",
                              look=crowd_look(r, "worried"))
                roots.append(o)
    lib = actor(1, {"hair": (0.12, 0.10, 0.09), "top": (0.85, 0.85, 0.80), "bottom": (0.30, 0.30, 0.32), "long": True, "glasses": True,
                    "face": "worried"}, [(1, 3.6, -0.6, 300), (nf, 3.6, -0.6, 300)], nf, arms="down", face_at=(fr(1.8), "worried", "brow"))
    _ = lib
    for k, o in enumerate(roots):
        b = r.uniform(70, 90)
        ts = BT.beats(0.0, nf / FPS, lambda t, b=b: b, r.uniform(0, 60 / b))
        heart_rings((o.location.x, o.location.y, 1.05), ts, nf, f"lb{k}_", size=0.9, alpha=0.6, dub=True)
    W.camera((-4.5, -2.6, 2.8), (0.0, 2.8, 0.9), lens=24)
    fill((-3.0, -1.0, 3.0), (0, 2.5, 1.0), power=120)
    return nf


# ============================ 1年後：夫婦の心拍がそろう ============================
def d08_home(nf):
    FJ.room((0.95, 0.80, 0.60), 0.45)
    W.box((0, 2, -0.05), (10, 10, 0.1), W.mat("living_floor", (0.50, 0.36, 0.22), 0.6), bevel=0)
    W.box((0, 4.6, 1.4), (10, 0.15, 2.8), W.mat("living_wall", (0.88, 0.84, 0.74), 0.9), bevel=0)
    W.box((-3.5, 2, 1.4), (0.15, 10, 2.8), W.mat("living_wall", (0.88, 0.84, 0.74), 0.9), bevel=0)
    sofa = W.mat("sofa", (0.35, 0.40, 0.50), 0.9)
    W.box((0, 2.6, 0.22), (2.2, 0.85, 0.44), sofa, bevel=0.05)
    W.box((0, 3.0, 0.62), (2.2, 0.25, 0.75), sofa, bevel=0.05)
    for sx in (-1, 1):
        W.box((sx * 1.15, 2.6, 0.45), (0.2, 0.85, 0.5), sofa, bevel=0.05)
    W.box((0, -0.8, 0.5), (1.6, 0.4, 1.0), W.mat("tv_stand", (0.30, 0.22, 0.15), 0.6), bevel=0.01)
    W.box((0, -0.85, 1.35), (1.5, 0.06, 0.85), W.mat("tv_screen", (0.2, 0.3, 0.45), 0.3, emit=(0.35, 0.45, 0.65), emit_strength=1.6),
          bevel=0)
    C.point_light((-2.4, 3.6, 1.8), 50, (1.0, 0.78, 0.5), 0.3)
    W.box((-2.4, 3.6, 0.8), (0.08, 0.08, 1.6), W.mat("lamp_pole", (0.3, 0.3, 0.3), 0.4), bevel=0)
    W.box((-2.4, 3.6, 1.75), (0.45, 0.45, 0.35), W.mat("lamp_shade", (1.0, 0.9, 0.7), 0.6, emit=(1.0, 0.85, 0.6), emit_strength=2.0),
          bevel=0)
    kacho = PF.person((0.45, 2.55, 0.3), 180, seed=1, pose="sit", look=L(KACHO, face="happy"))
    wife = PF.person((-0.45, 2.55, 0.3), 180, seed=2, pose="sit", look=L(WIFE, face="happy"))
    ts = BT.main_beats("d08_home")
    m2 = ring_mat("ring_soft", (1.0, 0.35, 0.40), 3.0)
    heart_rings((0.45, 2.55, 0.95), ts, nf, "kr", size=1.1, alpha=0.8, mat=m2)
    heart_rings((-0.45, 2.55, 0.95), ts, nf, "wr", size=1.1, alpha=0.8, mat=m2)
    _ = (kacho, wife)
    W.camera((1.6, -0.2, 1.4), (0.0, 2.6, 0.95), lens=24)
    cut(fr(4.4), (0.0, 0.4, 1.2), (0.0, 2.6, 1.05), lens=30, orbit=3, push=0.12)
    fill((1.0, 0.0, 2.0), (0, 2.6, 1.0), power=60, col=(1.0, 0.85, 0.7))
    return nf


SCENES = {k: v for k, v in globals().items() if callable(v) and k[:1] == "d" and k[1:3].isdigit() and "_" in k}

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    first = int(sys.argv[4]) if len(sys.argv) > 4 else None
    last = int(sys.argv[5]) if len(sys.argv) > 5 else None
    W.reset()
    nf = TL.shot(name)["frames"]
    SCENES[name](nf)
    for cam in FJ.cams():
        cam["orbit"] = min(cam.get("orbit", 13.0) * 0.55, 8.0)
        cam["push"] = min(cam.get("push", 0.3), 0.18)
    if os.environ.get("DRY"):
        print("built", name, len(bpy.data.objects), "objects", flush=True)
        sys.exit(0)
    FJ.render(out, nf, step, first, last)
    print("rendered", name, flush=True)
