"""「立体駐車場の作り方」全場面の3D（Blender / bpy）。主人公はレッサーパンダ（黄色いヘルメット・オレンジのベスト・電動ドリル）。
駅前の空き地（x -8〜8、y 0〜20）。手前（-y）が道路。カメラはおおむね道路の側から奥（+y）を見る。
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
ORANGE = (1.0, 0.38, 0.02)
YELLOW = (1.0, 0.82, 0.05)
BLUE = (0.15, 0.55, 1.0)
fr = K.fr
campath = K.campath

LOT_X, LOT_Y = 8.0, 20.0          # 空き地：x -8〜8、y 0〜20
FLOOR_H = 3.0                     # 1階の高さ
COLS_X = (-7.6, -2.55, 2.55, 7.6)
COLS_Y = (0.4, 6.8, 13.2, 19.6)
# タワーパーキング：x -3.6〜3.6、y 8〜15、高さ 2.2m ごとの段
TW_X, TW_Y0, TW_Y1, TW_LV, TW_N = 3.6, 8.0, 15.0, 2.2, 25


def lt(i):
    L = SC["lines"][i]
    return L["t"], L["t_end"]


# ---------- 材質 ----------
def M(key):
    tab = {
        "asphalt": lambda: K.noisy("asphalt", (0.16, 0.16, 0.17), 30.0, 0.12, 0.3, 0.9),
        "road": lambda: K.noisy("road", (0.12, 0.12, 0.13), 30.0, 0.10, 0.3, 0.9),
        "walk": lambda: K.noisy("sidewalk", (0.55, 0.53, 0.50), 8.0, 0.10, 0.2, 0.9),
        "line": lambda: K.mat("white_line", (0.92, 0.92, 0.90), 0.6),
        "yline": lambda: K.mat("yellow_line", (0.95, 0.72, 0.08), 0.6),
        "steel": lambda: K.noisy("steel_frame", (0.56, 0.62, 0.68), 6.0, 0.06, 0.1, 0.45),
        "deck": lambda: K.noisy("deck", (0.58, 0.58, 0.56), 3.0, 0.08, 0.2, 0.9),
        "ramp": lambda: K.noisy("ramp", (0.50, 0.50, 0.49), 3.0, 0.08, 0.2, 0.9),
        "rail": lambda: K.mat("rail", (0.85, 0.86, 0.86), 0.4),
        "glass": lambda: K.mat("glass_dark", (0.05, 0.07, 0.10), 0.15),
        "tire": lambda: K.mat("tire", (0.03, 0.03, 0.03), 0.8),
        "light": lambda: K.glow("car_light", (1.0, 0.95, 0.8), 3.0),
        "tail": lambda: K.glow("tail_light", (1.0, 0.1, 0.05), 3.0),
        "red": lambda: K.glow("sign_red", (1.0, 0.08, 0.05), 6.0),
        "green": lambda: K.glow("sign_green", (0.1, 1.0, 0.3), 6.0),
        "blue_sign": lambda: K.mat("p_blue", (0.05, 0.22, 0.75), 0.4),
        "pole": lambda: K.mat("pole", (0.55, 0.56, 0.58), 0.4),
        "booth": lambda: K.mat("booth", (0.90, 0.90, 0.88), 0.5),
        "bar": lambda: K.mat("bar_red", (0.85, 0.10, 0.08), 0.5),
        "plate": lambda: K.mat("base_plate", (0.35, 0.36, 0.38), 0.35),
        "wall": lambda: K.noisy("tower_wall", (0.80, 0.80, 0.78), 3.0, 0.06, 0.1, 0.8),
        "turn": lambda: K.noisy("turntable", (0.45, 0.47, 0.50), 10.0, 0.08, 0.3, 0.5),
        "laser": lambda: K.glow("laser", (1.0, 0.05, 0.05), 12.0),
    }
    return tab[key]()


CAR_COLS = [(0.85, 0.86, 0.86), (0.08, 0.08, 0.09), (0.55, 0.06, 0.05), (0.10, 0.22, 0.48), (0.60, 0.62, 0.64), (0.92, 0.92, 0.90),
            (0.35, 0.40, 0.30), (0.75, 0.55, 0.12)]


def hl(name, f_on, f_full, f_off=None, f_gone=None, col=ORANGE, alpha=0.6, strength=2.2):
    alpha = min(alpha, 0.97)
    return K.fade_mat(K.glow(f"hl_{name}", col, strength, alpha), f_on, f_full, f_off, f_gone, f"hl_{name}_{f_on}")


def box(size, loc, m, name="b", parent=None, rot=(0, 0, 0), shadow=True):
    return K.obj(K.box_mesh(*size), m, parent, loc, rot=rot, name=name, shadow=shadow)


def boxes(items, m, name="bx", parent=None):
    """たくさんの箱を1つのメッシュに。items = [(中心, 大きさ)]。"""
    bm = bmesh.new()
    for c, s in items:
        r = bmesh.ops.create_cube(bm, size=1.0)
        for v in r["verts"]:
            v.co = Vector((v.co.x * s[0] + c[0], v.co.y * s[1] + c[1], v.co.z * s[2] + c[2]))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(None)
    return K.obj(me, m, parent, (0, 0, 0), name=name)


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


# ---------- 町（駅前） ----------
def city(seed=4, skip=()):
    r = random.Random(seed)
    facade = [K.noisy(f"facade{k}", c, 4.0, 0.06, 0.1, 0.85) for k, c in
              enumerate([(0.78, 0.74, 0.66), (0.62, 0.62, 0.62), (0.70, 0.66, 0.60), (0.84, 0.82, 0.78), (0.55, 0.52, 0.48)])]
    win = K.mat("windows", (0.10, 0.14, 0.20), 0.15)
    blds = []
    for side, (x0, x1, y0, y1) in zip(("left", "right", "back"), ((-34, -9.5, -2, 44), (9.5, 34, -2, 44), (-9.5, 9.5, 21.5, 44))):
        if side in skip:
            continue
        y = y0
        while y < y1:
            dy = r.uniform(7, 12)
            x = x0
            while x < x1:
                dx = r.uniform(7, 11)
                h = r.uniform(10, 30)
                bx, by = min(x + dx, x1), min(y + dy, y1)
                blds.append((x, bx, y, by, h))
                x = bx + 0.6
            y += dy + 0.6
    wins = []
    for k, (x0, x1, y0, y1, h) in enumerate(blds):
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        box((x1 - x0, y1 - y0, h), (cx, cy, h / 2), facade[k % len(facade)], f"bld{k}")
        # 窓（道路と空き地に向く面だけ）
        faces = []
        if y0 < 1:
            faces.append(("y", y0 - 0.03, x0, x1))
        if x1 < -9 and abs(cx) < 30:
            faces.append(("x", x1 + 0.03, y0, y1))
        if x0 > 9 and abs(cx) < 30:
            faces.append(("x", x0 - 0.03, y0, y1))
        if y0 > 21:
            faces.append(("y", y0 - 0.03, x0, x1))
        for ax, p, a0, a1 in faces:
            for z in [3.0 + 3.2 * j for j in range(int((h - 3) / 3.2))]:
                n = max(1, int((a1 - a0 - 1.2) / 2.2))
                for i in range(n):
                    a = a0 + 0.9 + i * (a1 - a0 - 1.8) / max(1, n - 1) if n > 1 else (a0 + a1) / 2
                    if ax == "y":
                        wins.append(((a, p, z), (1.4, 0.06, 1.6)))
                    else:
                        wins.append(((p, a, z), (0.06, 1.4, 1.6)))
    boxes(wins, win, "windows")
    # 駅（左手前）の看板
    text3d("駅", (-12.0, -2.15, 9.0), 4.0, K.glow("eki_sign", (1.0, 1.0, 1.0), 2.5), "eki", rot=(90, 0, 0))
    box((5.0, 0.2, 5.0), (-12.0, -2.08, 9.2), K.mat("eki_board", (0.05, 0.25, 0.60), 0.4), "eki_board")


def world(seed=4, clouds=True, skip=()):
    K.daylight(elev=52, az=215)
    if clouds:
        K.clouds(seed=seed)
    K.ground(3000, (0.30, 0.32, 0.22), "far_ground")
    box((90, 120, 0.1), (0, 10, -0.04), M("road"), "city_floor")
    city(seed, skip)
    # 空き地（アスファルト）と歩道と道路の線
    box((2 * LOT_X, LOT_Y, 0.04), (0, LOT_Y / 2, 0.0), M("asphalt"), "lot")
    box((90, 0.8, 0.12), (0, -0.4, 0.04), M("walk"), "sidewalk")
    dash = [((x, -4.2, 0.03), (2.0, 0.15, 0.02)) for x in range(-40, 41, 4)]
    boxes(dash, M("line"), "lane")
    boxes([((0, -7.6, 0.03), (90, 0.15, 0.02)), ((0, -0.95, 0.03), (90, 0.15, 0.02))], M("line"), "road_edge")


# ---------- 車 ----------
_CAR = {}


def car(col, name="car", parent=None):
    """長さ 4.4m・幅 1.75m。+y が前。"""
    if not _CAR:
        _CAR["body"] = K.box_mesh(1.75, 4.4, 0.62, 0.08)
        _CAR["cabin"] = K.box_mesh(1.55, 2.3, 0.58, 0.12)
        _CAR["win"] = K.box_mesh(1.58, 2.0, 0.42, 0.06)
        _CAR["wheel"] = K.cyl_mesh(0.33, 0.33, 0.24, 16)
        _CAR["lamp"] = K.box_mesh(0.3, 0.05, 0.12)
    c = K.empty((0, 0, 0), parent, name)
    m = K.mat(f"carpaint_{col}", col, 0.25)
    K.obj(_CAR["body"], m, c, (0, 0, 0.62), name=f"{name}_body")
    K.obj(_CAR["cabin"], m, c, (0, -0.25, 1.16), name=f"{name}_cabin")
    K.obj(_CAR["win"], M("glass"), c, (0, -0.25, 1.18), name=f"{name}_win")
    for sx in (-1, 1):
        for sy in (-1, 1):
            K.obj(_CAR["wheel"], M("tire"), c, (sx * 0.8, sy * 1.35, 0.33), rot=(0, 90 * D2R, 0), name=f"{name}_wheel")
        K.obj(_CAR["lamp"], M("light"), c, (sx * 0.6, 2.21, 0.72), name=f"{name}_head", shadow=False)
        K.obj(_CAR["lamp"], M("tail"), c, (sx * 0.6, -2.21, 0.72), name=f"{name}_tl", shadow=False)
    return c


def drive(c, f0, f1, pts, step=2, ease=True, back=False):
    """車を pts の点の列に沿って走らせる（向きは進む方向。back=True はバック）。"""
    pts = [Vector(p) for p in pts]
    seg = [(pts[i + 1] - pts[i]).length for i in range(len(pts) - 1)]
    total = sum(seg) or 1e-6
    for f in list(range(f0, f1 + 1, step)) + [f1]:
        u = (f - f0) / max(1, f1 - f0)
        if ease:
            u = K.smooth(u)
        d = u * total
        i = 0
        while i < len(seg) - 1 and d > seg[i]:
            d -= seg[i]
            i += 1
        p = pts[i] + (pts[i + 1] - pts[i]) * (d / max(1e-6, seg[i]))
        dv = pts[i + 1] - pts[i]
        if back:
            dv = -dv
        c.location = p
        c.keyframe_insert("location", frame=f)
        if dv.xy.length > 1e-6:
            c.rotation_euler = (c.rotation_euler.x, c.rotation_euler.y, math.atan2(-dv.x, dv.y))
            c.keyframe_insert("rotation_euler", frame=f)


def park(c, loc, face, f=1):
    c.location = loc
    c.rotation_euler = (0, 0, face * D2R)
    c.keyframe_insert("location", frame=f)
    c.keyframe_insert("rotation_euler", frame=f)


SPOTS = [((-5.0 + 2.5 * i, 4.2), 0) for i in range(5)] + [((-5.0 + 2.5 * i, 15.8), 0) for i in range(5)]   # 10台分（頭から入れる）


def spot_lines(z=0.03, name="spots"):
    items = []
    for yrow, y0, y1 in ((4.2, 1.6, 6.8), (15.8, 13.2, 18.4)):
        for i in range(6):
            x = -6.25 + 2.5 * i
            items.append(((x, (y0 + y1) / 2, z), (0.12, y1 - y0, 0.02)))
        items.append(((0, y1 if yrow < 10 else y0, z), (12.6, 0.12, 0.02)))
    return items


# ---------- 主人公 ----------
def panda(loc, face, name="hero", drill_on=True):
    h = K.Person(loc, face, K.PANDA, name=name)
    d = None
    if drill_on:
        d = K.drill(1.6, f"{name}_drill")
        h.hold(d, "R", (0, 0.03, -0.02), (-90, 0, 0))
    h.stand(1)
    return h, d


def tip_at(d, f):
    sc = bpy.context.scene
    sc.frame_set(f)
    p = bpy.data.objects[d["tip"]].matrix_world.translation.copy()
    sc.frame_set(1)
    return (p.x, p.y, max(0.03, p.z))


DRILL_DOWN = dict(spine=-32, neck=18, shR=(6, -10), elR=6, shL=(14, -22), elL=18, hipL=22, hipR=22, kneeL=-28, kneeR=-28, hz=-0.10)


# ============================ 1) ドリルで穴 → 白い線 → 駐車場 → せまい ============================
def s01_drill(nf):
    world()
    T = SC["dur"]
    a1, _ = lt(1)
    a2, _ = lt(2)
    a3, _ = lt(3)
    a4, _ = lt(4)
    # レッサーパンダが地面にドリル（最初の 1.7秒：強く動かす）
    hero, dr = panda((0.0, 1.3, 0.0), 180)
    hero.stand(1, **DRILL_DOWN)
    for k in range(6):                       # ドリルの反動で体がふるえる
        f = 2 + 4 * k
        hero.pose(f, **dict(DRILL_DOWN, spine=-28 + (3 if k % 2 else -3), hz=-0.05 - (0.015 if k % 2 else 0)))
    K.spin(dr, 1, fr(a1 - 0.1), 80)
    tip = tip_at(dr, 10)
    print("tip", tip)
    K.drill_fx(tip, 1, fr(a1 - 0.1), "dust", seed=3, n=50, up=(0, -0.3, 1))
    K.drill_fx(tip, 1, fr(a1 - 0.1), "sparks", seed=4, n=40, up=(0, -0.3, 1))
    hole = K.obj(K.cyl_mesh(0.05, 0.05, 0.02, 12), K.mat("hole_dark", (0.02, 0.02, 0.02), 0.9), None, (tip[0], tip[1], 0.025),
                 name="anchor_hole")
    K.show(hole, fr(0.8))
    hero.pose(fr(a1 - 0.05), **DRILL_DOWN)
    hero.pose(fr(a1 + 0.3), spine=0, neck=-5, shR=(25, 8), elR=40, shL=(15, -8), elL=20, hipL=0, hipR=0, kneeL=0, kneeR=0, hz=0)
    hero.wag(1, nf)
    # 白い線がのびる
    for k, (c, s) in enumerate(spot_lines()):
        ln = box(s, c, M("line"), f"spot{k}", shadow=False)
        f_on = fr(a1 + 0.04 * k)
        K.key_scale(ln, max(1, f_on - 1), (1e-4, 1e-4, 1))
        K.key_scale(ln, f_on, (1, 0.05, 1))
        K.key_scale(ln, f_on + 6, (1, 1, 1))
    # 10台の車が入ってくる（道路から。奥の列が先）
    order = list(range(5, 10)) + list(range(5))
    for j, k in enumerate(order):
        (x, y), face = SPOTS[k]
        c = car(CAR_COLS[k % len(CAR_COLS)], f"car{k}")
        f0 = fr(a2 - 0.2 + 0.1 * j)
        side = -1 if k % 2 else 1
        start = (side * 26.0, -2.4 if side < 0 else -5.8, 0)
        if k >= 5:
            path = [start, (side * 3.0, -2.0, 0), (0.0, 1.0, 0), (0.0, 10.0, 0), (x, 12.0, 0), (x, y, 0)]
        else:
            path = [start, (side * 3.0, -2.0, 0), (x, 0.5, 0), (x, y, 0)]
        park(c, start, -90 * side, 1)
        drive(c, f0, f0 + 26, path)
    # 道路に並ぶ車（満車で入れない）と、満車の看板
    for k in range(6):
        c = car(CAR_COLS[(k + 3) % len(CAR_COLS)], f"wait{k}")
        x_end = 2.5 + 5.2 * k
        park(c, (40 + 6 * k, -2.4, 0), 90, 1)
        drive(c, fr(a3 + 0.2 + 0.15 * k), fr(a4 + 0.6 + 0.15 * k), [(40 + 6 * k, -2.4, 0), (x_end, -2.4, 0)])
    sign = K.empty((-2.6, -0.3, 0), None, "full_sign")
    box((0.1, 0.1, 2.4), (0, 0, 1.2), M("pole"), "fs_pole", sign)
    box((1.3, 0.12, 0.8), (0, 0, 2.6), K.mat("fs_board", (0.05, 0.05, 0.06), 0.4), "fs_board", sign)
    full = text3d("満車", (0, -0.08, 2.6), 0.42, M("red"), "fs_text")
    full.parent = sign
    full.location = (0, -0.08, 2.6)
    K.show(full, fr(a4))
    vac = text3d("空車", (0, -0.08, 2.6), 0.42, M("green"), "fs_vac")
    vac.parent = sign
    vac.location = (0, -0.08, 2.6)
    K.show(vac, 1, fr(a4))
    hero.place(1, face=180)
    hero.place(fr(a3 - 0.5) - 1, face=180)
    hero.walk(fr(a3 - 0.5), fr(a3 + 0.6), [(0.0, 1.3, 0), (-1.2, 0.2, 0), (-1.2, -0.6, 0)])
    hero.place(fr(a3 + 0.7), (-1.2, -0.6, 0), 200)
    hero.pose(fr(a4 - 0.2), shL=(10, 8), shR=(10, 8), elL=12, elR=12, neck=-8)
    hero.pose(fr(a4 + 0.3), shL=(150, 30), shR=(30, 8), elL=110, elR=30, neck=5)          # 頭をかかえる
    K.marker("hero", (0, 0, 0.18), hero.j["neck"])
    K.marker("full", (0, -0.1, 2.6), sign)
    fill_light((2.0, -10.0, 4.0), (0, 2, 0.8), 1800, 10.0)
    keys = [(0.0, (1.3, -1.1, 0.9), (-0.05, 1.1, 0.6), 24),
            (0.7, (-1.1, -1.0, 1.0), (-0.05, 1.1, 0.65), 24),
            (a1 - 0.15, (-1.3, -1.6, 1.35), (0.0, 1.1, 0.75), 24),
            (a1 + 0.5, (0.0, -12.0, 9.0), (0.0, 8.0, 0.0), 24),
            (a2 + 1.2, (0.5, -15.0, 7.5), (0.0, 9.0, 0.5), 24),
            (a3 + 0.8, (-3.0, -24.0, 16.0), (0.0, 8.0, 3.0), 24),
            (a4 + 0.3, (-4.0, -8.5, 2.6), (-1.5, -0.5, 1.5), 26),
            (T, (-4.6, -9.2, 2.9), (-1.6, -0.6, 1.7), 26)]
    campath(keys, nf, shake=0.02)


# ============================ 2) 鉄骨の柱 → 床を重ねる ============================
def structure(levels=3, f_cols=None, f_floor=None, ramp_gap=False, name="st"):
    """鉄骨の柱と床（levels 段）。f_cols＝柱がのびるコマ (f0, f1)、f_floor＝床ごとに落ちてくるコマ [f, ...]。"""
    root = K.empty((0, 0, 0), None, name)
    H = FLOOR_H * levels + 1.1
    cols = []
    for x in COLS_X:
        for y in COLS_Y:
            c = box((0.36, 0.36, H), (x, y, H / 2), M("steel"), f"{name}_col", root)
            cols.append(c)
            if f_cols:
                K.key_scale(c, 1, (1, 1, 1e-3))
                K.key_loc(c, 1, (x, y, 0))
                K.key_scale(c, f_cols[0], (1, 1, 1e-3))
                K.key_loc(c, f_cols[0], (x, y, 0))
                K.key_scale(c, f_cols[1], (1, 1, 1))
                K.key_loc(c, f_cols[1], (x, y, H / 2))
    floors = []
    for k in range(levels):
        z = FLOOR_H * (k + 1)
        fl = K.empty((0, 0, z), root, f"{name}_fl{k}")
        if ramp_gap and k == 0:          # 坂道の上だけ床をあける（坂：x 2.9〜7.25、y 0〜17.3）
            box((11.15, LOT_Y + 0.6, 0.3), (-2.725, LOT_Y / 2, 0), M("deck"), f"{name}_deck", fl)
            box((1.0, LOT_Y + 0.6, 0.3), (7.8, LOT_Y / 2, 0), M("deck"), f"{name}_deck3", fl)
            box((4.45, 3.0, 0.3), (5.075, 18.8, 0), M("deck"), f"{name}_deck2", fl)
        else:
            box((2 * LOT_X + 0.6, LOT_Y + 0.6, 0.3), (0, LOT_Y / 2, 0), M("deck"), f"{name}_deck", fl)
        rails = [((0, -0.1, 0.55), (2 * LOT_X + 0.6, 0.08, 0.8)), ((0, LOT_Y + 0.2, 0.55), (2 * LOT_X + 0.6, 0.08, 0.8)),
                 ((-LOT_X - 0.25, LOT_Y / 2, 0.55), (0.08, LOT_Y + 0.6, 0.8)), ((LOT_X + 0.25, LOT_Y / 2, 0.55), (0.08, LOT_Y + 0.6, 0.8))]
        boxes(rails, M("rail"), f"{name}_rail{k}", fl)
        boxes(spot_lines(0.17), M("line"), f"{name}_lines{k}", fl)
        floors.append(fl)
        if f_floor:
            f = f_floor[k]
            K.key_loc(fl, 1, (0, 0, z + 40))
            K.key_loc(fl, f, (0, 0, z + 40))
            K.key_loc(fl, f + 6, (0, 0, z - 0.15))
            K.key_loc(fl, f + 8, (0, 0, z + 0.05))
            K.key_loc(fl, f + 10, (0, 0, z))
    return root, floors


def ground_cars(prefix="g", skip=()):
    out = []
    for k, ((x, y), face) in enumerate(SPOTS):
        if k in skip:
            continue
        c = car(CAR_COLS[k % len(CAR_COLS)], f"{prefix}{k}")
        park(c, (x, y, 0), face)
        out.append(c)
    return out


def boxes_lines():
    boxes(spot_lines(), M("line"), "lines0")


def s02_floors(nf):
    world()
    T = SC["dur"]
    a5, _ = lt(5)
    a6, _ = lt(6)
    a7, _ = lt(7)
    boxes_lines()
    ground_cars()
    f_drop = [fr(a6 + 0.05), fr(a6 + 0.4), fr(a6 + 0.75)]
    root, floors = structure(3, (fr(a5 + 0.1), fr(a5 + 1.2)), f_drop)
    # 床ごとに車がポンと出る
    r = random.Random(6)
    for k, fl in enumerate(floors):
        for j, ((x, y), face) in enumerate(SPOTS):
            if r.random() < 0.25:
                continue
            c = car(CAR_COLS[(j + 2 * k) % len(CAR_COLS)], f"f{k}car{j}", fl)
            c.location = (x, y, 0.15)
            c.rotation_euler = (0, 0, face * D2R)
            K.show(c, f_drop[k] + 10 + 2 * j, pop=4)
    hero, dr = panda((-9.0, -1.2, 0), 160)
    hero.pose(fr(a5 + 0.2), shR=(150, 20), elR=20, shL=(20, -8), elL=20)
    hero.pose(fr(a7), shL=(160, 40), shR=(160, 40), elL=15, elR=15)
    hero.wag(1, nf)
    fill_light((2.0, -14.0, 6.0), (0, 8, 4), 2200, 14.0)
    keys = [(0.0, (-4.0, -16.0, 4.0), (0.0, 8.0, 3.5), 24),
            (a6, (-2.0, -22.0, 9.0), (0.0, 9.0, 5.0), 24),
            (a7, (12.0, -20.0, 12.0), (0.0, 9.0, 4.5), 24),
            (T, (14.5, -17.0, 13.0), (0.0, 9.0, 4.5), 24)]
    campath(keys, nf, shake=0.02)


# ============================ 3) 坂道（急すぎ → 17%・約18m）→ 自走式 ============================
RX0, RX1, RY0, RY1 = 2.9, 7.25, 0.0, 17.3          # 坂道（x、y）。2階の高さまで 17.3m（約17%）


def ramp(y0, y1, name="ramp", m=None):
    """y0（地面）から y1（2階の床）までの坂。上の端（y1）を原点にした空オブジェクトの子。"""
    piv = K.empty((0, y1, 0), None, f"{name}_piv")
    L = math.hypot(y1 - y0, FLOOR_H)
    ang = math.atan2(FLOOR_H, y1 - y0)
    r = K.empty((0, 0, FLOOR_H), piv, f"{name}_rot")
    r.rotation_euler = (ang, 0, 0)
    box((RX1 - RX0, L, 0.25), ((RX0 + RX1) / 2, -L / 2, -0.06), m or M("ramp"), f"{name}_slab", r)
    boxes([(((RX0 + RX1) / 2 + s * (RX1 - RX0) / 2, -L / 2, 0.45), (0.08, L, 0.7)) for s in (-1, 1)], M("rail"), f"{name}_rails", r)
    return piv, ang


def car_on_ramp_path(y0, y1, n=12):
    pts = []
    for k in range(n + 1):
        u = k / n
        y = y0 + (y1 - y0) * u
        pts.append(((RX0 + RX1) / 2, y, FLOOR_H * u))
    return pts


def s03_ramp(nf):
    world(skip=("right",))
    T = SC["dur"]
    a8, _ = lt(8)
    a9, _ = lt(9)
    a10, _ = lt(10)
    a11, _ = lt(11)
    a12, _ = lt(12)
    a13, _ = lt(13)
    a14, _ = lt(14)
    boxes_lines()
    ground_cars(skip=(3, 4, 8, 9))
    structure(3, ramp_gap=True)
    # 2階へ上がれない車（柱の前で止まる）
    c = car((0.85, 0.15, 0.10), "hero_car")
    park(c, (5.1, -6.0, 0), 0)
    drive(c, fr(a8), fr(a8 + 1.2), [(5.1, -6.0, 0), (5.1, -1.0, 0), (5.1, 9.5, 0)])
    K.marker("car", (0, 0, 1.4), c)
    # 急な坂（6m で 3m 上がる）→ 車がこする（火花）
    st_piv, st_ang = ramp(11.3, 17.3, "steep")
    K.key_scale(st_piv, 1, (1, 1e-3, 1e-3))
    K.key_scale(st_piv, fr(a9 + 0.1), (1, 1e-3, 1e-3))
    K.key_scale(st_piv, fr(a9 + 0.6), (1, 1, 1))
    K.key_scale(st_piv, fr(a12 - 0.05), (1, 1, 1))
    K.key_scale(st_piv, fr(a12 + 0.1), (1, 1e-3, 1e-3))
    # 車が急な坂へ：前が上がって、おなかをこする
    f_up = fr(a10 + 0.2)
    drive(c, f_up, f_up + 22, [(5.1, 9.5, 0), (5.1, 11.6, 0.15)], ease=False)
    for f, rx, z in ((f_up + 22, 0.0, 0.15), (f_up + 30, 16 * D2R, 0.55), (fr(a11 + 0.3), 14 * D2R, 0.5), (fr(a11 + 0.5), 16 * D2R, 0.55),
                     (fr(a12 - 0.1), 16 * D2R, 0.55), (fr(a12), 0.0, 0.0)):
        c.rotation_euler = (rx, 0, 0)
        c.keyframe_insert("rotation_euler", frame=f)
        c.location = (5.1, 11.6 if rx else 9.5, z)
        c.keyframe_insert("location", frame=f)
    K.drill_fx((5.1, 11.9, 0.15), f_up + 26, fr(a11 + 1.3), "sparks", seed=31, n=70, up=(0, -0.6, 1))
    # 17% の長い坂（上からのびる）
    lp_piv, ang = ramp(RY0, RY1, "long")
    K.key_scale(lp_piv, 1, (1, 1e-3, 1e-3))
    K.key_scale(lp_piv, fr(a12), (1, 1e-3, 1e-3))
    K.key_scale(lp_piv, fr(a12 + 0.6), (1, 1, 1))
    # 坂の角度の黄色い三角と、約18m の白い寸法線
    ym = K.glow("slope_yellow", YELLOW, 6.0)
    tri = K.poly_curve([(RX1 + 0.4, RY0, 0.05), (RX1 + 0.4, RY1, 0.05), (RX1 + 0.4, RY1, FLOOR_H), (RX1 + 0.4, RY0, 0.05)], 0.07, ym, "slope_tri")
    K.grow_line(tri, fr(a12 + 0.4), fr(a12 + 1.3), fr(a14))
    wm = K.glow("dim_white", (1, 1, 1), 5.0)
    dim = K.poly_curve([(RX0 - 0.6, RY0, 0.4), (RX0 - 0.6, RY1, 0.4)], 0.06, wm, "dim18")
    K.grow_line(dim, fr(a13 + 0.2), fr(a13 + 1.4), fr(a14 + 0.4))
    for y in (RY0, RY1):
        tk = K.poly_curve([(RX0 - 0.6, y, 0.0), (RX0 - 0.6, y, 0.8)], 0.05, wm, "dim_tick")
        K.grow_line(tk, fr(a13 + 0.2), fr(a13 + 0.4), fr(a14 + 0.4))
    # 自走式：車がゆっくり坂を上がって2階へ
    c2 = car((0.10, 0.22, 0.48), "up_car")
    park(c2, (5.1, -6.0, 0), 0)
    path = [(5.1, -6.0, 0), (5.1, -1.5, 0)] + car_on_ramp_path(RY0, RY1) + [(5.1, 19.0, FLOOR_H)]
    drive(c2, fr(a14 - 0.6), fr(T), path, ease=False)
    for f in range(fr(a14 - 0.6), fr(T) + 1, 2):        # 坂の上では車も傾く
        sc = bpy.context.scene
        sc.frame_set(f)
        y = c2.location.y
        c2.rotation_euler = (ang if RY0 + 0.5 < y < RY1 - 0.3 else 0.0, 0, 0)
        c2.keyframe_insert("rotation_euler", frame=f)
    bpy.context.scene.frame_set(1)
    hero, dr = panda((-0.6, -1.0, 0), 150)
    hero.pose(fr(a9), shR=(150, 20), elR=20)
    hero.pose(fr(a11), shL=(150, 30), shR=(150, 30), elL=110, elR=110)       # あわてる
    hero.pose(fr(a12 + 0.3), shL=(10, 8), shR=(110, 10), elL=12, elR=20)     # 指さす
    hero.wag(1, nf)
    fill_light((14.0, -6.0, 6.0), (5, 9, 1.5), 2200, 12.0)
    keys = [(0.0, (9.0, -4.5, 1.2), (5.0, 8.0, 2.4), 24),
            (a9, (11.0, 3.0, 3.0), (5.0, 12.0, 1.5), 24),
            (a10 + 0.4, (10.5, 7.5, 1.4), (5.1, 11.6, 0.6), 26),
            (a11 + 0.8, (9.5, 8.5, 0.9), (5.1, 11.8, 0.4), 28),
            (a12 + 0.2, (24.0, 8.6, 4.0), (5.0, 8.6, 1.4), 24),
            (a13 + 1.0, (25.0, 8.6, 3.5), (5.0, 8.6, 1.3), 24),
            (a14, (17.0, -2.0, 4.0), (5.0, 9.0, 1.6), 24),
            (T, (15.0, 4.0, 5.0), (5.0, 16.0, 2.6), 24)]
    campath(keys, nf, shake=0.02)


# ============================ 4) 坂をやめて、エレベーター → タワーパーキング ============================
def tower(name="tw", braces=False, cars=True, f_rise=None, seed=8, lean=None):
    """タワーパーキング（x ±3.6、y 8〜15、25段）。中央がエレベーター、左右に車の段。"""
    root = K.empty((0, (TW_Y0 + TW_Y1) / 2, 0), None, name)
    body = K.empty((0, 0, 0), root, f"{name}_body")
    H = TW_LV * TW_N + 0.6
    cy0, cy1 = TW_Y0 - (TW_Y0 + TW_Y1) / 2, TW_Y1 - (TW_Y0 + TW_Y1) / 2
    cols = [((x, y, H / 2), (0.32, 0.32, H)) for x in (-TW_X, -1.3, 1.3, TW_X) for y in (cy0, cy1)]
    boxes(cols, M("steel"), f"{name}_cols", body)
    beams = []
    for k in range(1, TW_N + 1):
        z = TW_LV * k
        for y in (cy0, cy1):
            beams.append(((0, y, z), (2 * TW_X + 0.3, 0.22, 0.22)))
        for x in (-TW_X, TW_X):
            beams.append(((x, 0, z), (0.22, cy1 - cy0, 0.22)))
    boxes(beams, M("steel"), f"{name}_beams", body)
    decks = []
    for k in range(TW_N):
        z = TW_LV * k + 0.12
        for sx in (-1, 1):
            decks.append(((sx * (TW_X + 1.3) / 2, 0, z), (TW_X - 1.3 - 0.1, cy1 - cy0 - 0.3, 0.08)))
    boxes(decks, K.mat("tw_deck", (0.40, 0.42, 0.45), 0.5), f"{name}_decks", body)
    # 屋根と、入口の壁（1階の前）
    box((2 * TW_X + 0.6, cy1 - cy0 + 0.6, 0.5), (0, 0, H + 0.25), M("wall"), f"{name}_roof", body)
    for sx in (-1, 1):
        box((TW_X - 1.6, 0.25, 2.2), (sx * (TW_X + 1.6) / 2, cy0 - 0.15, 1.1), M("wall"), f"{name}_front", body)
    box((2 * TW_X, 0.25, 0.6), (0, cy0 - 0.15, 2.5), M("wall"), f"{name}_lintel", body)
    signb = box((3.0, 0.15, 0.9), (0, cy0 - 0.3, 3.4), M("blue_sign"), f"{name}_sign", body)
    _ = signb
    txt = text3d("P", (0, cy0 - 0.4, 3.4), 0.75, K.glow("p_white", (1, 1, 1), 3.0), f"{name}_p")
    txt.parent = body
    txt.location = (0, cy0 - 0.4, 3.4)
    r = random.Random(seed)
    parked = []
    if cars:
        for k in range(1, TW_N):
            for sx in (-1, 1):
                if r.random() < 0.15:
                    continue
                c = car(CAR_COLS[r.randrange(len(CAR_COLS))], f"{name}_c{k}{sx}", body)
                c.location = (sx * (TW_X + 1.3) / 2, 0, TW_LV * k + 0.16)
                parked.append(c)
    if braces:
        add_braces(body, name)
    if f_rise:
        K.key_scale(root, 1, (1, 1, 1e-3))
        K.key_scale(root, f_rise[0], (1, 1, 1e-3))
        K.key_scale(root, f_rise[1], (1, 1, 1))
    if lean:
        for f, a in lean:
            body.rotation_euler = (0, a * D2R, 0)
            body.keyframe_insert("rotation_euler", frame=f)
    return root, body, parked


def add_braces(body, name="tw", m=None, f_on=None):
    """横の面に、三角になるななめの鉄骨（ジグザグ）。"""
    cy0, cy1 = TW_Y0 - (TW_Y0 + TW_Y1) / 2, TW_Y1 - (TW_Y0 + TW_Y1) / 2
    objs = []
    m = m or M("steel")
    for x in (-TW_X - 0.05, TW_X + 0.05):
        for k in range(TW_N):
            z0, z1 = TW_LV * k, TW_LV * (k + 1)
            ya, yb = (cy0, cy1) if k % 2 == 0 else (cy1, cy0)
            L = math.hypot(yb - ya, z1 - z0)
            ang = math.atan2(z1 - z0, yb - ya)
            b = box((0.16, L, 0.16), (x, (ya + yb) / 2, (z0 + z1) / 2), m, f"{name}_brace", body, rot=(ang, 0, 0))
            objs.append(b)
            if f_on:
                K.show(b, f_on + k // 2, pop=3)
    for y in (cy0 - 0.05, cy1 + 0.05):
        for k in range(TW_N):
            z0, z1 = TW_LV * k, TW_LV * (k + 1)
            xa, xb = (-TW_X, TW_X) if k % 2 == 0 else (TW_X, -TW_X)
            L = math.hypot(xb - xa, z1 - z0)
            ang = math.atan2(z1 - z0, xb - xa)
            b = box((L, 0.16, 0.16), ((xa + xb) / 2, y, (z0 + z1) / 2), m, f"{name}_brace", body, rot=(0, -ang, 0))
            objs.append(b)
            if f_on:
                K.show(b, f_on + k // 2, pop=3)
    return objs


def s04_tower(nf):
    world()
    T = SC["dur"]
    a15, _ = lt(15)
    a16, _ = lt(16)
    a17, _ = lt(17)
    a18, _ = lt(18)
    lines = boxes(spot_lines(), M("line"), "lines0")
    gc = ground_cars(skip=(3, 4, 8, 9))
    st, _fl = structure(3, ramp_gap=True)
    lp, _a = ramp(RY0, RY1, "long")
    # 坂が土地の半分を使う（オレンジ）
    half = box((LOT_X, LOT_Y, 3.0), (LOT_X / 2, LOT_Y / 2, 1.5), hl("half", fr(a15 + 0.4), fr(a15 + 0.8), fr(a16 + 0.2), fr(a16 + 0.5)),
               "half_hl", shadow=False)
    _ = half
    # 坂をやめる：坂がちぢんで消え、立体駐車場ごと片づく
    K.key_scale(lp, fr(a16), (1, 1, 1))
    K.key_scale(lp, fr(a16 + 0.4), (1, 1e-3, 1e-3))
    for o in [st, lines] + gc:
        K.key_scale(o, fr(a16 + 0.5), tuple(o.scale))
        K.key_scale(o, fr(a16 + 0.8), (1e-3, 1e-3, 1e-3) if o is not lines else (1, 1, 1))
    # タワーが地面から立ち上がる
    root, body, parked = tower("tw", f_rise=(fr(a17 - 0.4), fr(a17 + 0.5)))
    _ = parked
    # エレベーター：車ごと持ち上げる
    lift = K.empty((0, (TW_Y0 + TW_Y1) / 2, 0.1), None, "lift")
    box((2.4, 6.2, 0.15), (0, 0, 0), K.mat("lift_plate", (0.30, 0.32, 0.35), 0.4), "lift_plate", lift)
    lc = car((0.92, 0.92, 0.90), "lift_car", lift)
    lc.location = (0, 0, 0.1)
    K.key_loc(lift, 1, (0, (TW_Y0 + TW_Y1) / 2, -30))
    K.key_loc(lift, fr(a17 + 0.4), (0, (TW_Y0 + TW_Y1) / 2, -30))
    K.key_loc(lift, fr(a17 + 0.45), (0, (TW_Y0 + TW_Y1) / 2, 0.1))
    K.key_loc(lift, fr(a17 + 0.8), (0, (TW_Y0 + TW_Y1) / 2, 0.1))
    K.key_loc(lift, fr(T), (0, (TW_Y0 + TW_Y1) / 2, 0.1 + TW_LV * 14))
    hero, dr = panda((-6.0, -0.8, 0), 160)
    hero.pose(fr(a15 + 0.3), shL=(150, 30), shR=(150, 30), elL=110, elR=110)
    hero.pose(fr(a17), shL=(10, 8), shR=(160, 20), elL=12, elR=10, neck=-25)
    hero.pose(fr(a18), shL=(160, 40), shR=(160, 40), elL=15, elR=15, neck=-30)
    hero.wag(1, nf)
    fill_light((4.0, -16.0, 10.0), (0, 11, 12), 3000, 16.0)
    keys = [(0.0, (-3.0, -24.0, 16.0), (2.0, 9.0, 1.5), 24),
            (a16, (-3.0, -22.0, 14.0), (1.0, 9.0, 2.0), 24),
            (a17, (-6.0, -20.0, 6.0), (0.0, 11.0, 10.0), 24),
            (a18, (-9.0, -12.0, 1.4), (0.0, 11.0, 26.0), 20),
            (T, (-10.0, -11.0, 1.2), (0.0, 11.0, 30.0), 20)]
    campath(keys, nf, shake=0.02)


# ============================ 5) ターンテーブル ============================
TT_C = (0.0, 11.5)


def s05_turn(nf):
    world()
    T = SC["dur"]
    a19, _ = lt(19)
    a20, _ = lt(20)
    a21, _ = lt(21)
    a22, _ = lt(22)
    root, body, _p = tower("tw", cars=True)
    # 前の壁と看板は切りとって中を見せる（断面）
    for o in list(body.children):
        if o.name.startswith("tw_front") or o.name.startswith("tw_lintel") or o.name.startswith("tw_sign") or o.name.startswith("tw_p"):
            o.scale = (1e-3, 1e-3, 1e-3)
    tt = K.empty((TT_C[0], TT_C[1], 0.0), None, "turntable")
    K.obj(K.cyl_mesh(2.7, 2.7, 0.08, 48), M("turn"), tt, (0, 0, 0.04), name="tt_disc")
    boxes([((0, 0, 0.09), (0.12, 5.2, 0.01)), ((0, 0, 0.09), (5.2, 0.12, 0.01))], M("yline"), "tt_marks", tt)
    c = car((0.55, 0.06, 0.05), "turn_car")
    park(c, (0.0, -6.0, 0), 0)
    drive(c, fr(a19), fr(a19 + 1.3), [(0.0, -6.0, 0), (0.0, 4.0, 0), (TT_C[0], TT_C[1], 0.1)])
    # バックで出ようとする（後ろに道路、車が通る）
    drive(c, fr(a20 + 0.2), fr(a20 + 1.0), [(TT_C[0], TT_C[1], 0.1), (TT_C[0], TT_C[1] - 1.6, 0.1)], back=True)
    drive(c, fr(a20 + 1.1), fr(a21 - 0.05), [(TT_C[0], TT_C[1] - 1.6, 0.1), (TT_C[0], TT_C[1], 0.1)], back=True)
    om = K.glow("arrow_orange", ORANGE, 6.0)
    K.flow_arrow([(0.0, TT_C[1] - 2.6, 0.5), (0.0, 2.0, 0.5), (0.0, -2.5, 0.5)], om, fr(a20), fr(a21), width=0.18, name="back_arrow")
    tr = car((0.85, 0.86, 0.86), "road_car")
    park(tr, (30.0, -2.4, 0), 90)
    drive(tr, fr(a20 + 0.3), fr(a20 + 1.5), [(30.0, -2.4, 0), (-30.0, -2.4, 0)], ease=False)
    # 床ごと回す
    f0, f1 = fr(a21 + 0.2), fr(a21 + 1.6)
    c.parent = None
    K.key_rot(tt, 1, (0, 0, 0))
    K.key_rot(tt, f0, (0, 0, 0))
    K.key_rot(tt, f1, (0, 0, math.pi))
    for f in range(f0, f1 + 1):                      # 車も床といっしょに回る
        u = K.smooth((f - f0) / (f1 - f0))
        c.location = (TT_C[0], TT_C[1], 0.1)
        c.rotation_euler = (0, 0, math.pi * u)
        c.keyframe_insert("location", frame=f)
        c.keyframe_insert("rotation_euler", frame=f)
    bm = K.glow("arrow_blue", BLUE, 6.0)
    ring = K.poly_curve([(TT_C[0] + 3.0 * math.cos(a), TT_C[1] + 3.0 * math.sin(a), 0.3) for a in [i * 0.1 for i in range(0, 50)]], 0.12, bm,
                        "turn_arrow")
    K.grow_line(ring, f0, f1, fr(a22 + 1.0))
    # 前向きで出ていく
    drive(c, fr(a22 + 0.2), fr(T), [(TT_C[0], TT_C[1], 0.1), (0.0, 4.0, 0), (0.0, -2.0, 0), (-8.0, -2.4, 0)])
    K.marker("car", (0, 0, 1.5), c)
    fill_light((-3.0, 2.0, 6.0), (0, 11.5, 0.5), 2500, 8.0)
    keys = [(0.0, (-3.0, -4.0, 1.9), (0.0, 8.0, 0.8), 26),
            (a20, (-2.2, 3.6, 1.9), (0.0, 11.0, 0.5), 24),
            (a21, (-1.5, 5.2, 1.9), (0.0, 11.5, 0.3), 24),
            (a22, (-1.4, 5.4, 1.9), (0.0, 11.3, 0.3), 24),
            (T, (-2.5, 1.5, 1.9), (0.0, 7.0, 0.5), 24)]
    campath(keys, nf, shake=0.02)


# ============================ 6) 重さ → 三角に組む ============================
def frame2d(name, kind, loc, m, f_push=None, push=0.0):
    """押される四角／三角のわく（見本）。kind="square" は押されると平行四辺形にくずれる。"""
    root = K.empty(loc, None, name)
    s = 1.6
    bars = []
    pts = [(-s / 2, 0), (s / 2, 0), (s / 2, s), (-s / 2, s)] if kind == "square" else [(-s / 2, 0), (s / 2, 0), (0, s)]
    for i in range(len(pts)):
        bars.append(K.obj(K.box_mesh(1.0, 0.12, 0.12), m, root, (0, 0, 0), name=f"{name}_bar{i}"))

    def place(f, sh):
        q = [(x + (sh * y / s if y > 0 else 0), y) for x, y in pts]
        for i, b in enumerate(bars):
            (x0, y0), (x1, y1) = q[i], q[(i + 1) % len(q)]
            b.location = ((x0 + x1) / 2, 0, (y0 + y1) / 2)
            b.rotation_euler = (0, -math.atan2(y1 - y0, x1 - x0), 0)
            b.scale = (math.hypot(x1 - x0, y1 - y0) + 0.12, 1, 1)
            b.keyframe_insert("location", frame=f)
            b.keyframe_insert("rotation_euler", frame=f)
            b.keyframe_insert("scale", frame=f)
    place(1, 0.0)
    if f_push:
        place(f_push[0], 0.0)
        place(f_push[1], push if kind == "square" else 0.0)
    return root


def s06_truss(nf):
    world()
    T = SC["dur"]
    a23, _ = lt(23)
    a24, _ = lt(24)
    a25, _ = lt(25)
    a26, _ = lt(26)
    # たくさんの車でタワーがゆれる → ななめの鉄骨で止まる
    lean = [(1, 0.0), (fr(a24 + 0.4), 0.0), (fr(a24 + 0.9), 2.2), (fr(a24 + 1.3), -1.6), (fr(a25 - 0.3), 2.4), (fr(a25 + 0.5), 1.6),
            (fr(a25 + 1.0), 0.0)]
    root, body, parked = tower("tw", lean=lean)
    for k, c in enumerate(parked):          # 車がどんどん入る
        K.show(c, fr(a24 - 0.2) + k // 3, pop=3)
    f_br = fr(a25 + 0.1)
    add_braces(body, "tw", hl("brace", f_br, f_br + 4, f_br + 40, f_br + 50, col=YELLOW, alpha=0.95, strength=4.0), f_on=f_br)
    add_braces(body, "twb", None, f_on=f_br + 40)
    hl_cols = box((2 * TW_X + 0.5, TW_Y1 - TW_Y0 + 0.5, TW_LV * TW_N), (0, 0, TW_LV * TW_N / 2),
                  hl("sway", fr(a24 + 0.4), fr(a24 + 0.7), fr(a25), fr(a25 + 0.3), alpha=0.35), "sway_hl", body, shadow=False)
    _ = hl_cols
    # 1台の車がドスンとのる（1.5トン）
    c1 = car((0.55, 0.06, 0.05), "heavy_car")
    park(c1, (-(TW_X + 1.3) / 2, (TW_Y0 + TW_Y1) / 2, TW_LV * 1 + 3.0), 0)
    K.key_loc(c1, fr(a23 + 0.3), (-(TW_X + 1.3) / 2, (TW_Y0 + TW_Y1) / 2, TW_LV * 1 + 3.0))
    K.key_loc(c1, fr(a23 + 0.6), (-(TW_X + 1.3) / 2, (TW_Y0 + TW_Y1) / 2, TW_LV * 1 + 0.16))
    # 四角と三角の見本（押す青い矢印）
    sm = K.mat("demo_steel", (0.85, 0.70, 0.10), 0.4)
    fp = (fr(a26 + 0.2), fr(a26 + 1.2))
    frame2d("sq", "square", (-1.6, 2.0, 0.3), sm, fp, push=0.9)
    frame2d("tri", "tri", (1.4, 2.0, 0.3), sm, fp)
    bm = K.glow("push_blue", BLUE, 6.0)
    for x0 in (-3.4, -0.4):
        ar = K.flow_arrow([(x0 - 0.8, 1.9, 1.7), (x0, 1.9, 1.7)], bm, fp[0] - 6, fp[1], width=0.1, head=0.5, name=f"push{x0}")
        _ = ar
    hero, dr = panda((4.2, 1.0, 0), 200)
    hero.pose(fr(a24 + 0.5), shL=(150, 30), shR=(150, 30), elL=110, elR=110, neck=-25)
    hero.pose(fr(a26), shL=(10, 8), shR=(110, 10), elL=12, elR=20, neck=5)
    hero.wag(1, nf)
    fill_light((2.0, -14.0, 12.0), (0, 11, 14), 3000, 16.0)
    keys = [(0.0, (-7.0, 2.0, 3.5), (-2.0, 11.5, 2.8), 24),
            (a23 + 1.2, (-7.5, 1.5, 4.0), (-2.0, 11.5, 2.8), 24),
            (a24 + 0.3, (-8.0, -26.0, 8.0), (0.0, 11.0, 24.0), 22),
            (a25 + 1.2, (-10.0, -30.0, 10.0), (0.0, 11.0, 26.0), 22),
            (a26 - 0.1, (0.0, -6.0, 2.2), (0.0, 2.0, 1.2), 26),
            (T, (0.0, -5.4, 2.0), (0.0, 2.0, 1.1), 26)]
    campath(keys, nf, shake=0.02, cuts=[a26 - 0.1])


# ============================ 7) 光のセンサー ============================
def s07_sensor(nf):
    world()
    T = SC["dur"]
    a27, _ = lt(27)
    a28, _ = lt(28)
    a29, _ = lt(29)
    a30, _ = lt(30)
    root, body, _p = tower("tw", cars=True, braces=True)
    for o in list(body.children):
        if o.name.startswith("tw_front") or o.name.startswith("tw_lintel") or o.name.startswith("tw_sign") or o.name.startswith("tw_p"):
            o.scale = (1e-3, 1e-3, 1e-3)
        if o.name.startswith("tw_brace") and o.location.z < 4.5 and abs(o.location.y) > 3.0:     # 前の面の下のななめ材はどける
            o.scale = (1e-3, 1e-3, 1e-3)
    tt = K.empty((TT_C[0], TT_C[1], 0.0), None, "turntable")
    K.obj(K.cyl_mesh(2.7, 2.7, 0.08, 48), M("turn"), tt, (0, 0, 0.04), name="tt_disc")
    boxes([((0, 0, 0.09), (0.12, 5.2, 0.01)), ((0, 0, 0.09), (5.2, 0.12, 0.01))], M("yline"), "tt_marks", tt)
    c = car((0.10, 0.22, 0.48), "sensor_car", tt)
    c.location = (0, 0, 0.1)
    # 床が回りはじめる → 人を見つけて止まる
    f_go, f_stop = fr(a27 + 0.6), fr(a29 + 1.1)
    K.key_rot(tt, 1, (0, 0, 0))
    K.key_rot(tt, f_go, (0, 0, 0))
    K.key_rot(tt, f_stop, (0, 0, 0.35 * (f_stop - f_go) / 30))      # 車のかどが、パンダの直前で止まる
    K.key_rot(tt, nf, (0, 0, 0.35 * (f_stop - f_go) / 30))
    # 回転灯（黄色く点滅）
    lamp = K.obj(K.ellip_mesh(0.14, 0.14, 0.18), K.glow("warn_lamp", (1.0, 0.65, 0.05), 10.0), None, (-TW_X + 0.4, TW_Y0 + 0.5, 2.3),
                 name="warn_lamp", shadow=False)
    for f in range(f_go, f_stop + 1, 6):
        K.key_scale(lamp, f, 1.0)
        K.key_scale(lamp, f + 3, 0.4)
    # レッサーパンダが車の横（壁とのすき間）に残っている
    hero, dr = panda((2.45, 13.5, 0.16), 200, drill_on=False)
    hero.walk(1, fr(a27 + 0.5), [(2.45, 14.4, 0.16), (2.45, 12.0, 0.16)])
    hero.place(fr(a27 + 0.6), (2.45, 12.0, 0.16), 230)
    hero.pose(fr(a28), shL=(150, 40), shR=(150, 40), elL=30, elR=30, spine=-5, neck=10)        # はさまれる！
    hero.pose(fr(a30), shL=(10, 8), shR=(160, 20), elL=12, elR=10, neck=-5)
    hero.wag(1, nf)
    K.marker("hero", (0, 0, 0.18), hero.j["neck"])
    # 光のセンサー（赤い光のすじ）：人をさえぎると、強く光って止まる
    lm = K.glow("laser_beam", (1.0, 0.05, 0.05), 6.0)
    for k, z in enumerate((0.5, 0.95, 1.4)):
        b = K.obj(K.cyl_mesh(0.018, 0.018, 6.0, 8), lm, None, (2.3, 11.5, z), rot=(90 * D2R, 0, 0), name=f"beam{k}", shadow=False)
        K.show(b, fr(a29 + 0.2 + 0.1 * k))
        K.key_scale(b, fr(a29 + 1.0), (1, 1, 1))
        K.key_scale(b, fr(a29 + 1.1), (2.6, 2.6, 1))
        K.key_scale(b, fr(a29 + 1.4), (1.6, 1.6, 1))
    for sy in (-1, 1):
        box((0.25, 0.12, 1.6), (2.3, 11.5 + sy * 3.05, 0.9), K.mat("sensor_box", (0.15, 0.15, 0.17), 0.4), "sensor_post")
    stop = text3d("STOP", (0.0, TW_Y1 - 0.3, 1.5), 0.8, M("red"), "stop_txt")
    K.show(stop, fr(a29 + 1.1), pop=3)
    fill_light((-3.0, 6.0, 6.0), (1.0, 13.0, 0.8), 2500, 8.0)
    keys = [(0.0, (-1.2, 4.8, 1.5), (1.4, 12.5, 0.8), 24),
            (a28, (0.2, 6.6, 1.3), (2.2, 12.0, 0.9), 28),
            (a29, (-1.0, 5.2, 1.6), (1.6, 12.0, 0.8), 24),
            (T, (-0.6, 5.8, 1.5), (2.0, 12.0, 0.9), 26)]
    campath(keys, nf, shake=0.02)


# ============================ 8) 料金所と看板 → 最後のボルトもドリルで → 完成 ============================
def s08_final(nf):
    world()
    T = SC["dur"]
    a31, _ = lt(31)
    a32, _ = lt(32)
    a33, _ = lt(33)
    root, body, _p = tower("tw", cars=True, braces=True)
    # 料金所（ブースとバー）
    booth = K.empty((-2.6, 5.2, 0), None, "booth")
    box((1.4, 1.4, 2.3), (0, 0, 1.15), M("booth"), "booth_b", booth)
    box((1.2, 0.05, 0.8), (0, -0.72, 1.4), M("glass"), "booth_win", booth)
    box((1.6, 1.6, 0.15), (0, 0, 2.38), K.mat("booth_roof", (0.10, 0.30, 0.65), 0.4), "booth_roof", booth)
    bar = K.empty((-1.6, 5.2, 0.95), None, "bar")
    for k in range(6):
        box((0.5, 0.08, 0.08), (0.25 + 0.5 * k, 0, 0), M("bar") if k % 2 == 0 else M("booth"), "bar_seg", bar)
    K.show(booth, fr(a31 + 0.3), pop=5)
    K.show(bar, fr(a31 + 0.4), pop=5)
    # P の看板（柱の根もとのボルトを、ドリルで締める）
    pole = K.empty((4.6, 4.2, 0), None, "p_pole")
    box((0.7, 0.7, 0.05), (0, 0, 0.025), M("plate"), "p_plate", pole)
    box((0.16, 0.16, 5.0), (0, 0, 2.5), M("pole"), "p_post", pole)
    box((1.8, 0.15, 1.8), (0, 0, 5.6), M("blue_sign"), "p_board", pole)
    pt = text3d("P", (0, -0.1, 5.6), 1.4, K.glow("p_white2", (1, 1, 1), 3.0), "p_txt")
    pt.parent = pole
    pt.location = (0, -0.1, 5.6)
    K.show(pole, fr(a31 + 0.8), pop=5)
    bolts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            b = K.obj(K.cyl_mesh(0.035, 0.035, 0.06, 6), M("pole"), pole, (sx * 0.25, sy * 0.25, 0.08), name="bolt")
            bolts.append(b)
    hero, dr = panda((4.995, 4.63, 0), 180)
    tip0 = tip_at(dr, 1)
    _ = tip0
    hero.stand(1, shR=(20, 8), elR=30)
    hero.pose(fr(a32 - 0.2), **DRILL_DOWN)
    hero.pose(fr(a33 - 0.15), **DRILL_DOWN)
    for k in range(6):
        f = fr(a32) + 4 * k
        hero.pose(f, **dict(DRILL_DOWN, spine=-32 + (3 if k % 2 else -3)))
    hero.pose(fr(a33 + 0.2), spine=0, neck=-10, shR=(165, 20), elR=10, shL=(20, -8), elL=20, hipL=0, hipR=0, kneeL=0, kneeR=0, hz=0)
    hero.wag(1, nf)
    K.spin(dr, fr(a32), fr(a33 - 0.15), 80)
    tip = tip_at(dr, fr(a32) + 4)
    K.drill_fx(tip, fr(a32), fr(a33 - 0.15), "sparks", seed=81, n=40)
    bb = bolts[3]
    K.key_rot(bb, fr(a32), (0, 0, 0))
    K.key_rot(bb, fr(a33 - 0.15), (0, 0, 12.0))
    # 完成：車が入っていく
    for k in range(3):
        c = car(CAR_COLS[k + 2], f"in_car{k}")
        park(c, (-30.0 - 7 * k, -2.4, 0), -90)
        drive(c, fr(a33), fr(T) + 20, [(-30.0 - 7 * k, -2.4, 0), (-6.0 - 7 * k, -2.4, 0), (0.0, 2.0, 0), (0.0, 9.0, 0)])
    fill_light((6.0, -2.0, 4.0), (4.5, 4.0, 0.8), 1800, 6.0)
    keys = [(0.0, (-3.0, -12.0, 3.0), (-1.0, 6.0, 2.0), 24),
            (a31 + 1.4, (2.0, -6.0, 4.5), (3.0, 5.0, 3.5), 24),
            (a32 - 0.05, (6.3, 2.2, 1.4), (4.9, 4.5, 0.85), 24),
            (a33 - 0.1, (5.9, 2.4, 1.2), (4.9, 4.5, 0.8), 24),
            (a33 + 0.6, (2.0, -10.0, 6.0), (0.0, 9.0, 14.0), 22),
            (T, (1.0, -26.0, 9.0), (0.0, 10.0, 20.0), 22)]
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
