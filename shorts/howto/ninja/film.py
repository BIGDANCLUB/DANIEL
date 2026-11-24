"""「忍者屋敷の作り方」全場面の3D（Blender / bpy）。姫路城と同じ作り（参考元＝0秒博士の型・絵づくり）。
家は 断面（前の壁をはずした「ドールハウス」）で中のしかけを見せる。主人公は赤いT・ジーンズの半ズボンに忍者の頭巾、敵は黒装束の忍者。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "himeji"))
import kit as K  # noqa: E402
import castle as CS  # noqa: E402
from htimeline import Timeline  # noqa: E402

bpy = K.bpy
import bmesh  # noqa: E402
from mathutils import Vector  # noqa: E402

D2R = K.D2R
TL = Timeline(HERE)
SC = None
YELLOW = (1.0, 0.82, 0.05)
ORANGE = (1.0, 0.38, 0.02)
fr = K.fr
campath = K.campath

# 家の大きさ（m）：横 12 × 奥行 8。床の高さ：1階 0.5、2階（隠し部屋）2.8、3階（屋根裏）4.8、軒 6.0
X0, X1, Y0, Y1 = -6.0, 6.0, -4.0, 4.0
Z1, Z2, Z3, EAVE = 0.5, 2.8, 4.8, 6.0
WT = 0.18


def lt(i):
    """i 行目の、この場面の頭からの (はじまり, おわり) 秒。"""
    L = SC["lines"][i]
    return L["t"], L["t_end"]


# ---------- 材質 ----------
def M(key):
    tab = {
        "ext": lambda: K.noisy("tsuchikabe", (0.66, 0.57, 0.42), 2.0, 0.08, 0.06, 0.92),
        "inw": lambda: K.noisy("inner_wall", (0.80, 0.74, 0.60), 2.0, 0.05, 0.04, 0.9),
        "wood": CS.wood_mat,
        "board": lambda: K.noisy("floor_board", (0.42, 0.27, 0.13), 3.0, 0.22, 0.15, 0.6),
        "line": lambda: K.mat("board_line", (0.10, 0.06, 0.03), 0.8),
        "tatami": lambda: K.noisy("tatami", (0.60, 0.56, 0.28), 30.0, 0.12, 0.25, 0.8),
        "heri": lambda: K.mat("heri", (0.07, 0.09, 0.08), 0.7),
        "shoji": lambda: K.mat("shoji", (0.93, 0.91, 0.85), 0.9),
        "door": lambda: K.noisy("itado", (0.30, 0.19, 0.10), 3.0, 0.25, 0.2, 0.7),
        "soil": lambda: K.noisy("soil_sec", (0.26, 0.17, 0.09), 0.8, 0.25, 0.3, 0.95),
        "dark": lambda: K.mat("pit_dark", (0.05, 0.04, 0.035), 0.95),
        "tile": lambda: CS.tile_mat("tile_n", (0.17, 0.18, 0.19), (0.24, 0.24, 0.25)),
        "futon": lambda: K.noisy("futon", (0.80, 0.80, 0.86), 6.0, 0.05, 0.1, 0.9),
        "futon2": lambda: K.noisy("kakebuton", (0.55, 0.15, 0.12), 6.0, 0.08, 0.1, 0.9),
        "rope": lambda: K.noisy("rope", (0.62, 0.52, 0.34), 20.0, 0.2, 0.3, 0.9),
    }
    return tab[key]()


def hl(name, f_on, f_full, f_off=None, f_gone=None, col=ORANGE, alpha=0.6, strength=2.2):
    """参考元の「直す部分をオレンジでぬる」：光る半透明の材質（出たり消えたり）。"""
    alpha = min(alpha, 0.97)          # 1 だと fade_mat が半分の濃さにしてしまう
    return K.fade_mat(K.glow(f"hl_{name}", col, strength, alpha), f_on, f_full, f_off, f_gone, f"hl_{name}_{f_on}")


def box(size, loc, m, name="b", parent=None, rot=(0, 0, 0), shadow=True):
    return K.obj(K.box_mesh(*size), m, parent, loc, rot=rot, name=name, shadow=shadow)


def prism(poly, z0, z1, m, name="prism"):
    """上から見た多角形（反時計回り）を z0〜z1 に立ち上げた柱。"""
    bm = bmesh.new()
    lo = [bm.verts.new((x, y, z0)) for x, y in poly]
    hi = [bm.verts.new((x, y, z1)) for x, y in poly]
    bm.faces.new(hi)
    bm.faces.new(lo[::-1])
    n = len(poly)
    for k in range(n):
        bm.faces.new((lo[k], lo[(k + 1) % n], hi[(k + 1) % n], hi[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m)
    return K.obj(me, m, None, (0, 0, 0), name=name)


def cut_mesh(o, keep_y_above=0.0):
    """メッシュを y = keep_y_above の面で切って、手前（y が小さい側）を捨てる（屋根の断面）。"""
    me = o.data.copy()
    o.data = me
    bm = bmesh.new()
    bm.from_mesh(me)
    geom = list(bm.verts) + list(bm.edges) + list(bm.faces)
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, keep_y_above - o.location.y, 0), plane_no=(0, 1, 0), clear_inner=True)
    bm.to_mesh(me)
    bm.free()


def world(elev=52, az=215, fields=True, seed=3, trees=300, ground_cut=None):
    """ground_cut＝その y より手前（-y）には地面を作らない（地面の断面を見せる場面）。"""
    K.daylight(elev=elev, az=az)
    K.clouds(seed=seed)
    if ground_cut is None:
        K.ground()
    else:
        box((6000, 3000, 0.2), (0, ground_cut + 1500, -0.1), K.grass_mat(), "ground_cut")
    if fields:
        K.countryside(seed=seed, keep_out=45, r_max=700, n_fields=110, n_trees=trees)


def fill_light(loc, at, energy=2500, size=8.0, col=(1.0, 0.95, 0.88), name="fill"):
    """断面の中を明るくする面の光（前から当てる）。"""
    lt_ = bpy.data.lights.new(name, 'AREA')
    lt_.energy = energy
    lt_.size = size
    lt_.color = col
    o = bpy.data.objects.new(name, lt_)
    bpy.context.collection.objects.link(o)
    o.location = loc
    K.W.aim(o, at)
    return o


# ---------- 家の部品 ----------
def tatami_floor(x0, x1, y0, y1, z, name="tt"):
    nx = max(1, round((x1 - x0) / 1.8))
    ny = max(1, round((y1 - y0) / 0.9))
    w, d = (x1 - x0) / nx, (y1 - y0) / ny
    box((x1 - x0, y1 - y0, 0.1), ((x0 + x1) / 2, (y0 + y1) / 2, z - 0.05), M("board"), f"{name}_base")
    for i in range(nx):
        for j in range(ny):
            cx, cy = x0 + w * (i + 0.5), y0 + d * (j + 0.5)
            box((w - 0.02, d - 0.02, 0.06), (cx, cy, z + 0.03), M("tatami"), f"{name}_m")
            for s in (-1, 1):
                box((w - 0.02, 0.04, 0.066), (cx, cy + s * (d / 2 - 0.03), z + 0.033), M("heri"), f"{name}_h")


def board_floor(x0, x1, y0, y1, z, name="bf", skip=None):
    """板の床（板のすじつき）。skip=(x0, x1, y0, y1) の四角はあけておく（落とし穴・はしごの口）。"""
    def rect(a0, a1, b0, b1):
        if a1 - a0 > 0.01 and b1 - b0 > 0.01:
            box((a1 - a0, b1 - b0, 0.08), ((a0 + a1) / 2, (b0 + b1) / 2, z - 0.04), M("board"), f"{name}_p")
    if skip:
        sx0, sx1, sy0, sy1 = skip
        rect(x0, sx0, y0, y1)
        rect(sx1, x1, y0, y1)
        rect(sx0, sx1, y0, sy0)
        rect(sx0, sx1, sy1, y1)
    else:
        rect(x0, x1, y0, y1)
    n = int((y1 - y0) / 0.3)
    for k in range(1, n):
        y = y0 + k * (y1 - y0) / n
        if skip and skip[2] < y < skip[3]:
            box((skip[0] - x0, 0.012, 0.005), ((x0 + skip[0]) / 2, y, z + 0.001), M("line"), f"{name}_l", shadow=False)
            box((x1 - skip[1], 0.012, 0.005), ((skip[1] + x1) / 2, y, z + 0.001), M("line"), f"{name}_l", shadow=False)
        else:
            box((x1 - x0, 0.012, 0.005), ((x0 + x1) / 2, y, z + 0.001), M("line"), f"{name}_l", shadow=False)


def lattice_window(cx, y, z0, w, h, name="mado", parent=None, face_y=-1):
    """格子窓（黒い口＋木の縦格子）。face_y=-1 で手前（-y）向きの壁。"""
    root = K.empty((cx, y, z0), parent, name)
    box((w, 0.06, h), (0, face_y * 0.03, h / 2), K.mat("window_dark", (0.03, 0.03, 0.035), 0.5), f"{name}_hole", root)
    n = max(3, int(w / 0.13))
    for k in range(n + 1):
        box((0.045, 0.07, h), (-w / 2 + w * k / n, face_y * 0.07, h / 2), M("wood"), f"{name}_bar", root)
    for z in (0.0, h):
        box((w + 0.12, 0.09, 0.07), (0, face_y * 0.07, z), M("wood"), f"{name}_frame", root)
    return root


def shell(front=True, z_top=EAVE, roof=True, cut_roof=False, windows=True, back=True, sides=True, name="house", z0=0.0, band=True):
    """家の外まわり（壁は z0〜z_top）。戻り値 dict(sides={front/back/left/right: [オブジェクト]}, roof=屋根, band=[庇])。"""
    ext, wood = M("ext"), M("wood")
    out = dict(sides={"front": [], "back": [], "left": [], "right": []}, roof=None, band=[])
    walls = []
    if front:
        walls.append(("front", (X0, Y0), (X1, Y0), (0, -1)))
    if back:
        walls.append(("back", (X0, Y1), (X1, Y1), (0, 1)))
    if sides:
        walls += [("left", (X0, Y0), (X0, Y1), (-1, 0)), ("right", (X1, Y0), (X1, Y1), (1, 0))]
    for side, p0, p1, nv in walls:
        root = K.empty((0, 0, 0), None, f"{name}_{side}")
        CS.wall_box(p0, p1, z0, z_top - z0, WT, ext, f"{name}_{side}_w", root)
        a_, b_ = Vector((p0[0], p0[1], 0)), Vector((p1[0], p1[1], 0))
        L = (b_ - a_).length
        dv = (b_ - a_).normalized()
        nrm = Vector((nv[0], nv[1], 0))
        c = (a_ + b_) / 2 + nrm * (WT / 2 + 0.02)
        ang = math.atan2(dv.y, dv.x)
        if z0 < 0.9:
            box((L, 0.05, 0.9 - z0), (c.x, c.y, (z0 + 0.9) / 2), M("door"), f"{name}_{side}_koshi", root, rot=(0, 0, ang))
        n = int(L / 2.0)
        for k in range(n + 1):
            p = a_ + dv * (L * k / n) + nrm * (WT / 2 + 0.04)
            box((0.2, 0.08, z_top - z0), (p.x, p.y, (z0 + z_top) / 2), wood, f"{name}_{side}_post", root, rot=(0, 0, ang))
        for zb in (Z2 - 0.05, z_top - 0.1):
            if z0 < zb < z_top + 0.01:
                box((L + 0.2, 0.1, 0.18), (c.x + nrm.x * 0.03, c.y + nrm.y * 0.03, zb), wood, f"{name}_{side}_beam", root, rot=(0, 0, ang))
        if windows and side in ("front", "back"):
            for x in (-3.6, 3.6):
                lattice_window(x, c.y + nrm.y * 0.02, 1.25, 1.6, 0.95, f"{name}_{side}_w1", root, face_y=nrm.y)
            if z_top >= EAVE - 0.01:
                for x in (-3.0, 0.0, 3.0):
                    lattice_window(x, c.y + nrm.y * 0.02, 5.0, 1.1, 0.6, f"{name}_{side}_w3", root, face_y=nrm.y)
        if windows and side == "front":
            box((2.0, 0.08, 2.05), (0, c.y - 0.02, Z1 + 1.0), M("door"), f"{name}_door", root)
            for k in range(5):
                box((0.04, 0.1, 2.05), (-0.8 + 0.4 * k, c.y - 0.05, Z1 + 1.0), M("wood"), f"{name}_doorbar", root)
        if band and z0 < Z2 < z_top:
            # 庇（1階の上の小さな瓦屋根）：外へ向かって下がる
            tilt = 22 * D2R
            pb = (a_ + b_) / 2 + nrm * (WT / 2 + 0.5)
            if nv[1]:
                bd = box((L + 1.0, 0.95, 0.1), (pb.x, pb.y, Z2 + 0.25), M("tile"), f"{name}_{side}_hisashi", root, rot=(-tilt * nv[1], 0, 0))
            else:
                bd = box((0.95, L + 1.0, 0.1), (pb.x, pb.y, Z2 + 0.25), M("tile"), f"{name}_{side}_hisashi", root, rot=(0, tilt * nv[0], 0))
            out["band"].append(bd)
        out["sides"][side].append(root)
    if roof:
        r = CS.hip_roof(0, 0, z_top, X1 - X0, Y1 - Y0, 3.4, over=1.0, sori=0.1, m=M("tile"), name=f"{name}_roof", gable=True)
        if cut_roof:
            cut_mesh(r, 0.0)
            for ch in r.children_recursive:
                if "hafu" in ch.name:
                    ch.hide_render = True
        out["roof"] = r
    return out


def levels(which=(1, 2, 3), x0=X0 + WT / 2, x1=X1 - WT / 2, y0=Y0, y1=Y1 - WT / 2, hole=None, name="lv"):
    """中の床：1階（畳）、2階＝隠し部屋（板）、3階＝屋根裏（板）。hole=(x0,x1,y0,y1) は 2・3階の床にあける口（縄ばしご）。"""
    if 1 in which:
        tatami_floor(x0, x1, y0, y1, Z1, f"{name}1")
        box((x1 - x0, y1 - y0, Z1), ((x0 + x1) / 2, (y0 + y1) / 2, Z1 / 2), M("dark"), f"{name}_under")
    if 2 in which:
        board_floor(x0, x1, y0, y1, Z2, f"{name}2", skip=hole)
        box((x1 - x0, 0.12, 0.18), ((x0 + x1) / 2, y0 + 0.06, Z2 - 0.12), M("wood"), f"{name}2_edge")
    if 3 in which:
        board_floor(x0, x1, y0, y1, Z3, f"{name}3", skip=hole)
        box((x1 - x0, 0.12, 0.18), ((x0 + x1) / 2, y0 + 0.06, Z3 - 0.12), M("wood"), f"{name}3_edge")


def katana(name="katana"):
    """刀（+y が切っ先、原点は手）。"""
    root = K.empty(name=name)
    box((0.03, 0.78, 0.012), (0, 0.5, 0), K.mat("blade", (0.82, 0.84, 0.88), 0.18), f"{name}_blade", root)
    K.obj(K.cyl_mesh(0.05, 0.05, 0.014, 16), K.mat("tsuba", (0.15, 0.12, 0.08), 0.4), root, (0, 0.1, 0), rot=(90 * D2R, 0, 0), name=f"{name}_tsuba")
    box((0.036, 0.24, 0.03), (0, -0.02, 0), K.mat("tsuka", (0.05, 0.05, 0.06), 0.7), f"{name}_tsuka", root)
    return root


def rope_ladder(length, name="nawa"):
    """縄ばしご（原点は上の端。-z へ垂れる）。"""
    root = K.empty(name=name)
    for sx in (-1, 1):
        K.obj(K.cyl_mesh(0.022, 0.022, length, 8), M("rope"), root, (sx * 0.22, 0, -length), name=f"{name}_r")
    n = int(length / 0.32)
    for k in range(1, n + 1):
        box((0.48, 0.05, 0.04), (0, 0, -k * length / n), M("board"), f"{name}_s", root)
    return root


def jump(p, f0, f1, a, b, h, face=None):
    """人が a から b へ跳ぶ（ちぢこまった姿勢で弧をえがく）。"""
    a, b = Vector(a), Vector(b)
    for f in list(range(f0, f1 + 1, 2)) + [f1]:
        u = (f - f0) / max(1, f1 - f0)
        q = a + (b - a) * u + Vector((0, 0, 4 * h * u * (1 - u)))
        p.place(f, tuple(q), face)
        p.pose(f, shL=(120, 30), shR=(120, 30), elL=40, elR=40, hipL=90, hipR=70, kneeL=-110, kneeR=-100, spine=-20, neck=10, hz=-0.1)


def seal(p, f):
    """忍者の「印」：胸の前で手を合わせる。"""
    p.pose(f, shL=(70, -25), shR=(70, -25), elL=95, elR=95, neck=0, spine=0)


def spin_with(p, f0, f1, pivot, ang, p0, face0, step=1):
    """人を pivot のまわりで ang 度回す（どんでん返しに乗って回る）。"""
    pv = Vector(pivot)
    r = Vector(p0) - pv
    for f in list(range(f0, f1 + 1, step)) + [f1]:
        u = K.smooth((f - f0) / max(1, f1 - f0))
        a = ang * u * D2R
        q = Vector((r.x * math.cos(a) - r.y * math.sin(a), r.x * math.sin(a) + r.y * math.cos(a), r.z)) + pv
        p.place(f, tuple(q), face0 + ang * u)


# ============================ 1) 家と忍者 ============================
def n01_house(nf):
    world()
    T = SC["dur"]
    a0, _ = lt(0)
    a1, _ = lt(1)
    a2, _ = lt(2)
    a3, _ = lt(3)
    H = shell(name="h")
    r = random.Random(1)
    # 家がいっきに建つ：土台 → 壁が地面から飛び出す（左右 → 奥 → 手前）→ 庇 → 屋根が落ちてくる
    base = box((X1 - X0 + 0.6, Y1 - Y0 + 0.6, 0.45), (0, 0, 0.2), K.noisy("foundation", (0.35, 0.34, 0.32), 1.5, 0.2, 0.3), "base")
    K.key_loc(base, 1, (0, 0, -0.5))
    K.key_loc(base, fr(0.12), (0, 0, 0.2))
    order = [("left", 0.18), ("right", 0.18), ("back", 0.36), ("front", 0.55)]
    for side, ts in order:
        for piece in H["sides"][side]:
            f = fr(ts)
            K.key_loc(piece, max(1, f - 1), (0, 0, -6.2))
            K.key_loc(piece, f + 5, (0, 0, 0.3))
            K.key_loc(piece, f + 8, (0, 0, -0.05))
            K.key_loc(piece, f + 10, (0, 0, 0))
        for u in (0.2, 0.5, 0.8):
            p = {"left": (X0, Y0 + 8 * u), "right": (X1, Y0 + 8 * u), "back": (X0 + 12 * u, Y1), "front": (X0 + 12 * u, Y0)}[side]
            K.smoke_puffs((p[0], p[1], 0.2), fr(ts) + 2, n=4, seed=r.randint(0, 999), col=(0.60, 0.52, 0.40), size=1.6, rise=1.5,
                          life=20, spread=1.6, alpha=0.9, name=f"dust{side}{u}")
    roof = H["roof"]
    rz = roof.location.z                                  # 屋根の元の高さ（軒の高さ）
    K.key_loc(roof, 1, (0, 0, rz + 40))
    K.key_loc(roof, fr(0.95), (0, 0, rz + 22))
    K.key_loc(roof, fr(1.2), (0, 0, rz - 0.25))
    K.key_loc(roof, fr(1.28), (0, 0, rz + 0.08))
    K.key_loc(roof, fr(1.34), (0, 0, rz))
    for k in range(8):
        a = k / 8 * 2 * math.pi
        K.smoke_puffs((7.5 * math.cos(a), 5.5 * math.sin(a), 6.0), fr(1.2), n=3, seed=40 + k, col=(0.62, 0.56, 0.46), size=1.8, rise=0.8,
                      life=18, spread=1.0, alpha=0.8, name=f"rdust{k}")
    # 主人公：頭巾をかぶって印を結ぶ → 両手を広げて家を見せる → ガッツポーズ → 敵に気づいて驚く
    hero = K.Person((0.6, -8.2, 0), 180, K.HERO_NINJA, name="hero")
    hero.stand(1)
    seal(hero, fr(0.1))
    seal(hero, fr(0.7))
    hero.pose(fr(1.0), shL=(100, 70), shR=(100, 70), elL=5, elR=5, neck=5)
    hero.pose(fr(a1 + 0.1), shL=(100, 70), shR=(100, 70), elL=5, elR=5)
    hero.pose(fr(a1 + 0.4), shL=(15, 10), shR=(150, 20), elR=95)
    hero.pose(fr(a1 + 0.8), shR=(165, 15), elR=70)
    hero.place(fr(a2 - 0.1), face=180)
    hero.place(fr(a2 + 0.3), face=230)
    hero.pose(fr(a2 + 0.25), shL=(10, 8), shR=(10, 8), elL=12, elR=12, neck=8)
    hero.pose(fr(a2 + 0.5), shL=(135, 45), shR=(135, 45), elL=120, elR=120, neck=12, spine=6)      # 頭をかかえる
    hero.pose(nf, shL=(140, 45), shR=(140, 45), elL=125, elR=125, neck=14, spine=8)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    # 敵の忍者：左の奥から走ってきて、屋根へ跳び上がり、屋根をつたって忍び込む
    xs = [-17.0, -19.0, -15.5, -21.0]
    for i, x in enumerate(xs):
        y = -10.0 + i * 2.2
        e = K.Person((x, y, 0), -90, K.NINJA, name=f"en{i}", seed=10 + i)
        e.stand(1)
        t0 = a2 - 0.5 + 0.12 * i
        K.show(e.root, fr(t0 - 0.05))                       # ドロンとけむりの中から現れる
        K.smoke_puffs((x, y, 0.8), fr(t0 - 0.1), n=5, seed=70 + i, col=(0.75, 0.74, 0.72), size=1.0, rise=1.0, life=14, spread=0.5,
                      alpha=0.9, name=f"doron{i}")
        tx = X0 - 1.2
        ty = -2.4 + 1.6 * i
        e.walk(fr(t0), fr(t0 + 1.0), [(x, y, 0), (tx, ty, 0)], run=True)
        t1 = t0 + 1.0
        jump(e, fr(t1), fr(t1 + 0.55), (tx, ty, 0), (X0 + 1.2, ty * 0.6, EAVE + 1.1), 3.0, -90)
        t2 = t1 + 0.55
        e.place(fr(t2), face=-90)
        e.pose(fr(t2) + 2, shL=(60, 20), shR=(60, 20), elL=60, elR=60, hipL=70, hipR=40, kneeL=-100, kneeR=-80, spine=-35, hz=-0.3)
        e.walk(fr(t2) + 3, nf, [(X0 + 1.2, ty * 0.6, EAVE + 1.1), (X0 + 4.5, ty * 0.3, EAVE + 2.6)], run=False,
               arms=dict(shL=(50, 20), shR=(50, 20), elL=70, elR=70))
        if i == 1:
            K.marker("enemy", (0, 0, 0.2), e.j["neck"])
    keys = [(0.0, (0.95, -10.1, 1.65), (0.6, -8.2, 1.5), 40),
            (0.3, (1.5, -12.5, 2.6), (0.4, -7.0, 1.8), 34),
            (1.15, (-6.0, -27.0, 9.0), (0, -1.0, 3.2), 28),
            (a1 + 0.6, (-12.0, -30.0, 12.0), (0, -1.0, 3.0), 28),
            (a2 + 0.2, (-20.0, -24.0, 8.0), (-6.0, -3.0, 3.5), 28),
            (a3 + 0.4, (-17.0, -14.0, 11.0), (-3.0, 0.0, 6.0), 26),
            (T, (-13.0, -11.0, 12.5), (-1.0, 0.5, 6.5), 26)]
    campath(keys, nf, shake=0.03)


# ============================ 2) どんでん返し ============================
PANEL = (0.0, 0.0)      # どんでん返しの軸（x=0 の仕切り壁のまん中）
PW, PH = 1.0, 2.15      # 板の幅と高さ


def two_rooms(ceiling=False, name="r"):
    """1階の2つの部屋（左 x<0、右 x>0）。間の壁（x=0）に どんでん返しの板。前（-y）の壁はなし（断面）。戻り値：板の回る軸（empty）。"""
    shell(front=False, z_top=2.75, roof=False, windows=False, name=f"{name}s", band=False)
    levels((1,), name=f"{name}l")
    inw = M("inw")
    # 仕切り壁：板の口（y = -0.5〜0.5、高さ Z1〜Z1+PH）をあける
    prism([(-0.09, Y0), (0.09, Y0), (0.09, -PW / 2), (-0.09, -PW / 2)], Z1, 2.75, inw, f"{name}_pw1")
    prism([(-0.09, PW / 2), (0.09, PW / 2), (0.09, Y1), (-0.09, Y1)], Z1, 2.75, inw, f"{name}_pw2")
    box((0.18, PW, 2.75 - Z1 - PH), (0, 0, Z1 + PH + (2.75 - Z1 - PH) / 2), inw, f"{name}_lintel")
    for y in (-PW / 2 - 0.05, PW / 2 + 0.05):
        box((0.24, 0.1, 2.75 - Z1), (0, y, (Z1 + 2.75) / 2), M("wood"), f"{name}_jamb")
    box((0.24, Y1 - Y0, 0.12), (0, 0, 2.75 - 0.06), M("wood"), f"{name}_kamoi")
    pivot = K.empty((PANEL[0], PANEL[1], Z1), None, "donden")
    box((0.08, PW - 0.04, PH - 0.02), (0, 0, PH / 2), inw, "donden_board", pivot)
    for s in (-1, 1):
        box((0.1, 0.06, PH), (0, s * (PW / 2 - 0.05), PH / 2), M("wood"), "donden_frame", pivot)
    # ふすま・障子・掛け軸で部屋らしく
    for x in (-4.6, -2.2):
        box((1.15, 0.05, 1.9), (x, Y1 - 0.12, Z1 + 0.95), M("shoji"), f"{name}_fusuma")
    box((0.6, 0.03, 1.2), (3.0, Y1 - 0.12, Z1 + 1.2), K.mat("kakejiku", (0.85, 0.80, 0.66), 0.8), f"{name}_jiku")
    box((0.5, 0.04, 0.8), (3.0, Y1 - 0.13, Z1 + 1.2), K.mat("kakejiku_e", (0.25, 0.28, 0.22), 0.8), f"{name}_jiku_e")
    box((1.2, 0.8, 0.35), (-4.0, 1.5, Z1 + 0.18), M("door"), f"{name}_tansu")
    if ceiling:
        board_floor(0.09, X1 - WT / 2, Y0, Y1 - WT / 2, 2.75 + 0.1, f"{name}_ceil", skip=(3.4, 4.4, 0.5, 1.5))
    return pivot


def n02_donden(nf):
    world(fields=True, trees=200)
    T = SC["dur"]
    a5, e5 = lt(5)
    a6, e6 = lt(6)
    a7, e7 = lt(7)
    a8, e8 = lt(8)
    a9, _ = lt(9)
    pivot = two_rooms(name="r")
    fill_light((-2.0, -14.0, 7.0), (0, 0, 1.2), 3500, 10.0)
    # 軸（黄色い縦の線）と、板をオレンジでぬる
    ax = K.poly_curve([(0, 0, Z1 - 0.2), (0, 0, Z1 + PH + 0.35)], 0.035, hl("axis", fr(a5 + 0.9), fr(a5 + 1.1), fr(e6 + 0.3), fr(e6 + 0.6), YELLOW, 1.0, 6.0),
                      "axis")
    K.grow_line(ax, fr(a5 + 0.9), fr(a5 + 1.5))
    ov = box((0.12, PW, PH), (0, 0, PH / 2), hl("panel", fr(a5 + 0.2), fr(a5 + 0.45), fr(a9 + 0.6), fr(a9 + 0.9)), "panel_hl", pivot, shadow=False)
    _ = ov
    # 試しに回る（主人公は横で見ている）
    K.key_rot(pivot, fr(a6 + 0.1), (0, 0, 0))
    K.key_rot(pivot, fr(a6 + 0.9), (0, 0, 360 * D2R))
    # 敵が来たら、主人公は板に背をつけて押す → 板ごと半回転して右の部屋へ
    hero = K.Person((-1.6, -1.2, Z1), -60, K.HERO_NINJA, name="hero")
    hero.stand(1)
    seal(hero, fr(0.3))
    hero.pose(fr(a5 + 0.6), shL=(20, 10), shR=(120, 10), elR=20, neck=0)                       # 板を指さす
    hero.pose(fr(a6 + 0.1), shL=(10, 10), shR=(10, 10), elL=10, elR=10)
    p0 = (-0.34, 0.18, Z1)
    hero.walk(fr(a7 - 0.4), fr(a7 + 0.2), [(-1.6, -1.2, Z1), p0], run=True)
    hero.place(fr(a7 + 0.25), p0, -90)
    hero.pose(fr(a7 + 0.25), shL=(60, 20), shR=(60, 20), elL=30, elR=30, spine=-8, neck=-5)
    t_push = a7 + 1.0
    hero.pose(fr(t_push), shL=(85, 10), shR=(85, 10), elL=10, elR=10, spine=-12)              # 板を押す
    spin_with(hero, fr(t_push), fr(t_push + 0.35), (PANEL[0], PANEL[1], Z1), 180, p0, -90)
    K.key_rot(pivot, fr(t_push), (0, 0, 360 * D2R))
    K.key_rot(pivot, fr(t_push + 0.35), (0, 0, 540 * D2R))
    hero.pose(fr(t_push + 0.45), shL=(15, 10), shR=(150, 20), elR=95)                         # 右の部屋でガッツポーズ
    hero.pose(fr(a9 + 0.3), shR=(165, 15), elR=70)
    hero.pose(nf, shR=(160, 15), elR=60)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    # 敵：左の部屋の入口（左の奥）から走ってくる → 板の前で止まって、きょろきょろ
    en = K.Person((-5.6, -7.0, 0.0), 0, K.NINJA, name="en", seed=21)
    en.stand(1)
    K.show(en.root, fr(a7 - 0.25))
    en.walk(fr(a7 - 0.2), fr(t_push + 0.4), [(-5.6, -7.0, 0.0), (-4.8, -4.6, 0.0), (-4.3, -3.4, Z1), (-2.0, -0.8, Z1), (-0.7, 0.0, Z1)],
            run=True)
    tl = t_push + 0.45
    for k, (fc, nk) in enumerate([(-90, 0), (-40, 30), (-140, -30), (-90, 0)]):
        en.place(fr(tl + 0.45 * k), (-0.7, 0.0, Z1), fc)
        en.pose(fr(tl + 0.45 * k), shL=(30, 30), shR=(30, 30), elL=40, elR=40, neck=10, spine=-5)
    en.pose(fr(a9 + 0.2), shL=(150, 30), shR=(20, 10), elL=110, elR=10, neck=15)              # 頭をかく
    en.pose(nf, shL=(155, 30), elL=120)
    K.marker("enemy", (0, 0, 0.2), en.j["neck"])
    keys = [(0.0, (-7.0, -12.0, 9.0), (0.0, 0.0, 1.0), 26),
            (a5 + 0.1, (-4.5, -7.0, 4.2), (-0.2, 0.0, 1.5), 28),
            (e6, (-3.8, -6.4, 3.8), (0.0, 0.0, 1.5), 30),
            (a7 + 0.4, (-5.2, -8.5, 5.0), (-1.0, -0.4, 1.2), 28),
            (t_push + 0.5, (0.8, -8.0, 6.8), (0.0, 0.0, 1.0), 28),
            (a9, (1.8, -8.6, 7.2), (0.2, 0.2, 1.0), 28),
            (T, (2.4, -9.0, 7.6), (0.3, 0.3, 1.0), 27)]
    campath(keys, nf, shake=0.02)


# ============================ 3) 隠し梯子と隠し部屋 ============================
def n03_ladder(nf):
    world(fields=True, trees=200)
    T = SC["dur"]
    a10, _ = lt(10)
    a11, _ = lt(11)
    a12, _ = lt(12)
    a13, _ = lt(13)
    a14, _ = lt(14)
    a15, _ = lt(15)
    a16, _ = lt(16)
    pivot = two_rooms(ceiling=False, name="r")
    # 天井（＝隠し部屋の床）に口。口のふたの板（横へすべる）
    HX0, HX1, HY0, HY1 = 3.4, 4.4, 0.5, 1.5
    board_floor(0.09, X1 - WT / 2, Y0, Y1 - WT / 2, Z2, "ceil", skip=(HX0, HX1, HY0, HY1))
    box((X1 - 0.09, 0.14, 0.2), ((0.09 + X1) / 2, Y0 + 0.07, Z2 - 0.12), M("wood"), "ceil_edge")
    lid = box((HX1 - HX0, HY1 - HY0, 0.06), ((HX0 + HX1) / 2, (HY0 + HY1) / 2, Z2 - 0.1), M("board"), "lid")
    lid_hl = box((HX1 - HX0 + 0.04, HY1 - HY0 + 0.04, 0.08), (0, 0, 0), hl("lid", fr(a12 + 0.1), fr(a12 + 0.3), fr(a15 + 0.7), fr(a15 + 1.0)),
                 "lid_hl", lid, shadow=False)
    _ = lid_hl
    cx = (HX0 + HX1) / 2
    K.key_loc(lid, fr(a12 + 0.55), (cx, (HY0 + HY1) / 2, Z2 - 0.1))
    K.key_loc(lid, fr(a12 + 0.95), (cx - 1.05, (HY0 + HY1) / 2, Z2 - 0.1))
    K.key_loc(lid, fr(a15 + 0.05), (cx - 1.05, (HY0 + HY1) / 2, Z2 - 0.1))
    K.key_loc(lid, fr(a15 + 0.45), (cx, (HY0 + HY1) / 2, Z2 - 0.1))
    # 隠し部屋（2階）：壁、座布団、行灯
    shell(front=False, z_top=Z3 - 0.1, roof=False, windows=False, name="up", z0=Z2, band=False)
    box((0.6, 0.6, 0.08), (1.6, 2.4, Z2 + 0.04), M("futon2"), "zabuton")
    K.obj(K.cyl_mesh(0.18, 0.18, 0.55, 12), K.glow("andon", (1.0, 0.82, 0.5), 2.5), None, (5.0, 2.8, Z2), name="andon")
    # 梯子：口の手前のふちを軸にして、上の部屋の床に寝かせてある → 下へ回って下りる → 登ったら引き上げる
    LL = 2.4
    lh = K.empty((cx, HY0, Z2 + 0.06), None, "lad_hinge")
    lad = K.ladder(LL, 0.5, "lad")
    lad.parent = lh
    lad.location = (0, 0, -LL)
    K.obj(K.box_mesh(0.62, 0.1, LL), hl("lad", fr(a13 + 0.05), fr(a13 + 0.25), fr(a14 + 0.4), fr(a14 + 0.7)), lad, (0, 0, LL / 2),
          name="lad_hl", shadow=False)
    down = -math.degrees(math.acos((Z2 + 0.06 - Z1) / LL))
    t_up = a14 + 1.1
    K.key_rot(lh, 1, (90 * D2R, 0, 0))
    K.key_rot(lh, fr(a13 + 0.1), (90 * D2R, 0, 0))
    K.key_rot(lh, fr(a13 + 0.55), (down * D2R, 0, 0))
    K.key_rot(lh, fr(t_up), (down * D2R, 0, 0))
    K.key_rot(lh, fr(t_up + 0.35), (90 * D2R, 0, 0))
    foot = HY0 + LL * math.sin(down * D2R)
    # 主人公
    hero = K.Person((0.34, -0.18, Z1), 90, K.HERO_NINJA, name="hero")
    hero.stand(1, shL=(15, 10), shR=(150, 20), elR=95)
    hero.place(fr(a10 + 0.3), face=90)
    hero.pose(fr(a10 + 0.4), shL=(30, 30), shR=(30, 30), elL=20, elR=20, neck=10)            # 板が回り始めて驚く
    hero.walk(fr(a11 - 0.2), fr(a12), [(0.34, -0.18, Z1), (2.5, -0.6, Z1), (cx, HY0 - 0.25, Z1)], run=True)
    hero.place(fr(a12 + 0.05), (cx, HY0 - 0.25, Z1), 0)
    hero.pose(fr(a12 + 0.2), shL=(170, 20), shR=(170, 20), elL=10, elR=10, neck=-25)          # 天井の板を押し上げてずらす
    hero.pose(fr(a12 + 0.95), shL=(170, 20), shR=(170, 20), elL=10, elR=10, neck=-25)
    hero.pose(fr(a13 + 0.3), shL=(20, 10), shR=(20, 10), elL=10, elR=10, neck=-15)
    hero.place(fr(a14), (cx, foot - 0.3, Z1), 0)
    hero.climb(fr(a14 + 0.05), fr(a14 + 0.85), (cx, foot - 0.3, Z1 + 0.05), (cx, HY0 - 0.25, Z2 - 0.25), 0, tilt=-12)
    hero.place(fr(a14 + 0.95), (cx + 1.1, HY1 + 0.3, Z2), 200)
    hero.stand(fr(a14 + 0.95))
    hero.pose(fr(t_up), shL=(60, 10), shR=(60, 10), elL=60, elR=60, spine=-35, hz=-0.25)     # 梯子を引き上げる
    hero.pose(fr(t_up + 0.3), shL=(140, 10), shR=(140, 10), elL=40, elR=40, spine=-10, hz=-0.1)
    hero.stand(fr(a15 + 0.6))
    hero.place(fr(a16), (cx - 1.4, 2.2, Z2), 180)
    hero.pose(fr(a16), hipL=90, hipR=90, kneeL=-150, kneeR=-150, hz=-0.62, shL=(20, 10), shR=(20, 10), elL=60, elR=60)   # すわってひと息
    hero.pose(nf, hipL=90, hipR=90, kneeL=-150, kneeR=-150, hz=-0.62, shL=(165, 25), shR=(20, 10), elL=20, elR=60)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    # 敵：どんでん返しで回ってきて追う → 梯子の下で上を見てきょろきょろ
    K.key_rot(pivot, fr(a10 + 0.25), (0, 0, 0))
    K.key_rot(pivot, fr(a10 + 0.6), (0, 0, 180 * D2R))
    en = K.Person((-0.34, 0.18, Z1), -90, K.NINJA, name="en", seed=31)
    en.stand(1, shL=(60, 20), shR=(60, 20), elL=30, elR=30)
    spin_with(en, fr(a10 + 0.25), fr(a10 + 0.6), (0, 0, Z1), 180, (-0.34, 0.18, Z1), -90)
    en.walk(fr(a11), fr(t_up + 0.1), [(0.34, -0.18, Z1), (2.2, -0.9, Z1), (cx - 0.3, foot - 0.5, Z1)], run=True)
    en.place(fr(t_up + 0.15), (cx - 0.3, foot - 0.5, Z1), 10)
    en.pose(fr(t_up + 0.15), shL=(170, 20), shR=(170, 20), elL=10, elR=10, neck=-30)          # つかみそこねる
    for k, fc in enumerate([40, -30, 60, 0]):
        en.place(fr(a15 + 0.3 + 0.5 * k), face=fc)
        en.pose(fr(a15 + 0.3 + 0.5 * k), shL=(30, 30), shR=(30, 30), elL=40, elR=40, neck=-20 if k % 2 else 15)
    en.pose(nf, shL=(150, 30), elL=110, neck=10)
    K.marker("enemy", (0, 0, 0.2), en.j["neck"])
    fill_light((3.0, -14.0, 3.5), (3.0, 0.0, 2.0), 3500, 10.0)
    keys = [(0.0, (-1.6, -8.5, 2.6), (1.2, 0.0, 1.4), 28),
            (a11, (0.5, -9.0, 2.4), (2.5, 0.0, 1.6), 28),
            (a12 + 0.2, (2.6, -7.2, 1.9), (cx, 0.6, 2.4), 28),
            (a13 + 0.5, (2.4, -7.6, 2.0), (cx, 0.6, 2.0), 28),
            (a14 + 0.8, (2.8, -8.6, 2.8), (cx, 0.6, 2.6), 28),
            (a15 + 0.5, (2.6, -9.6, 3.2), (cx - 0.4, 0.8, 2.8), 28),
            (T, (2.2, -10.4, 3.8), (cx - 0.6, 0.8, 2.9), 28)]
    campath(keys, nf, shake=0.02)


# ============================ 4) 外から見るとふつうの家、中は3階 ============================
def n04_floors(nf):
    world()
    T = SC["dur"]
    a17, _ = lt(17)
    a18, _ = lt(18)
    H = shell(name="h")
    levels((1, 2, 3), name="lv")
    box((0.6, 0.6, 0.08), (-2.0, 1.5, Z2 + 0.04), M("futon2"), "zabuton")
    K.obj(K.cyl_mesh(0.18, 0.18, 0.55, 12), K.glow("andon", (1.0, 0.82, 0.5), 2.5), None, (-3.2, 2.4, Z2), name="andon")
    for k, x in enumerate((-4.5, -3.6, 4.8)):
        box((0.8, 0.6, 0.6), (x, 2.8, Z3 + 0.3), M("door"), f"kura{k}")
    fill_light((0.0, -16.0, 5.0), (0, 0, 3.0), 4000, 12.0)
    # 「でも中は3階建て」：前の壁が地面へ沈み、屋根が上へ飛んで、3つの階が見える
    t = a18 + 0.1
    for piece in H["sides"]["front"]:
        K.key_loc(piece, fr(t), (0, 0, 0))
        K.key_loc(piece, fr(t + 0.3), (0, 0, -6.3))
    r = H["roof"]
    rz = r.location.z
    K.key_loc(r, fr(t + 0.05), (0, 0, rz))
    K.key_loc(r, fr(t + 0.45), (0, 4.0, rz + 18.0))
    K.key_scale(r, fr(t + 0.4), 1.0)
    K.key_scale(r, fr(t + 0.45), 1e-4)
    for k, x in enumerate((-4.0, 0.0, 4.0)):
        K.smoke_puffs((x, Y0 - 0.5, 0.3), fr(t + 0.2), n=4, seed=60 + k, col=(0.60, 0.52, 0.40), size=1.8, rise=1.2, life=18, spread=1.6,
                      alpha=0.85, name=f"fd{k}")
    # 階ごとに黄色い線が光る（1階 → 2階 → 3階）
    for k, z in enumerate((Z1, Z2, Z3)):
        f0 = fr(t + 0.45 + 0.28 * k)
        ln = K.poly_curve([(X0 + 0.1, Y0 + 0.05, z + 0.02), (X1 - 0.1, Y0 + 0.05, z + 0.02)], 0.06,
                          hl(f"floor{k}", f0, f0 + 3, None, None, YELLOW, 1.0, 6.0), f"fl{k}")
        K.grow_line(ln, f0, f0 + 6)
    # 3階に主人公が立って手をふる
    hero = K.Person((3.5, 1.0, Z3), 0, K.HERO_NINJA, name="hero")
    hero.stand(1)
    hero.wave(fr(t + 1.0), nf, "R")
    keys = [(0.0, (-14.0, -22.0, 6.0), (0, 0, 3.6), 30),
            (a18, (-9.0, -24.0, 5.5), (0, 0, 3.6), 30),
            (t + 0.5, (-4.0, -23.0, 4.6), (0, 0, 3.6), 30),
            (T, (-1.5, -22.0, 4.4), (0, 0, 3.7), 31)]
    campath(keys, nf, shake=0.02)


# ============================ 5) 落とし穴 ============================
PIT = (1.2, 2.8, -4.0, -2.2, -2.6)     # 穴：x0, x1, y0, y1, 底の高さ


def n05_pit(nf):
    world(fields=False, ground_cut=Y0)
    T = SC["dur"]
    a19, _ = lt(19)
    a20, _ = lt(20)
    a21, _ = lt(21)
    a22, _ = lt(22)
    a23, _ = lt(23)
    px0, px1, py0, py1, pz = PIT
    shell(front=False, z_top=2.75, roof=False, windows=False, name="s")
    # 床：落とし穴の上だけ、2枚の板（外側のふちを軸に下へ開く）
    board_floor(X0 + WT / 2, X1 - WT / 2, Y0, Y1 - WT / 2, Z1, "fl", skip=(px0, px1, py0, py1))
    hinges = []
    for k, (hx, sgn) in enumerate(((px0, 1), (px1, -1))):
        h = K.empty((hx, (py0 + py1) / 2, Z1 - 0.04), None, f"trap{k}")
        box(((px1 - px0) / 2 - 0.02, py1 - py0, 0.08), (sgn * (px1 - px0) / 4, 0, 0), M("board"), f"trapb{k}", h)
        box(((px1 - px0) / 2, py1 - py0 + 0.02, 0.1), (sgn * (px1 - px0) / 4, 0, 0), hl(f"trap{k}", fr(a21 - 0.1), fr(a21 + 0.05), fr(a23 + 0.6),
                                                                                         fr(a23 + 0.9)), f"traph{k}", h, shadow=False)
        hinges.append((h, sgn))
    for h, sgn in hinges:
        K.key_rot(h, fr(a21 + 0.05), (0, 0, 0))
        K.key_rot(h, fr(a21 + 0.22), (0, sgn * 85 * D2R, 0))
        K.key_rot(h, fr(a23 + 0.2), (0, sgn * 85 * D2R, 0))
        K.key_rot(h, fr(a23 + 0.5), (0, 0, 0))
    # 床下と地面の断面（茶色い土）。穴だけ深く掘ってある
    soil, dark = M("soil"), M("dark")
    G = -6.0
    prism([(-30, Y0), (px0, Y0), (px0, py1), (px1, py1), (px1, Y0), (30, Y0), (30, 20), (-30, 20)], G, -0.01, soil, "soil_main")
    box((px1 - px0, py1 - Y0, pz - G), ((px0 + px1) / 2, (Y0 + py1) / 2, (G + pz) / 2), soil, "soil_bottom")
    box((px1 - px0 - 0.02, 0.02, -pz - 0.1), ((px0 + px1) / 2, py1 - 0.01, (pz - 0.1) / 2), dark, "pit_back")
    for x in (X0 + 0.5, -2.0, 0.6, 3.6, X1 - 0.5):
        if not (px0 - 0.2 < x < px1 + 0.2):
            box((0.16, 0.16, Z1), (x, Y0 + 0.4, Z1 / 2), M("wood"), "tsuka")
    box((X1 - X0, 0.12, 0.12), (0, Y0 + 0.06, Z1 - 0.06), M("wood"), "fl_edge")
    # 敵：入ってきて、きょろきょろしながら歩く → 板の上で落ちる
    en = K.Person((X0 + 0.6, -3.0, Z1), -90, K.NINJA, name="en", seed=41)
    en.stand(1)
    sneak = dict(shL=(40, 15), shR=(40, 15), elL=70, elR=70)
    en.walk(fr(0.1), fr(a19 + 1.2), [(X0 + 0.6, -3.0, Z1), (-2.8, -2.6, Z1)], arms=sneak)
    for k, fc in enumerate([-30, -150, -90]):
        en.place(fr(a19 + 1.35 + 0.3 * k), face=fc)
        en.pose(fr(a19 + 1.35 + 0.3 * k), neck=10 if k % 2 else -5, **sneak)
    en.walk(fr(a20), fr(a21 + 0.05), [(-2.8, -2.6, Z1), (0.0, -3.0, Z1), ((px0 + px1) / 2, -3.1, Z1)], arms=sneak)
    en.pose(fr(a21 + 0.08), shL=(160, 40), shR=(160, 40), elL=10, elR=10, neck=15)
    en.fall(fr(a21 + 0.12), fr(a22 + 0.2), ((px0 + px1) / 2, -3.1, Z1), (0, 0.15, 0.6), spin=(-80, 0), ground=pz)
    en.place(fr(a23), ((px0 + px1) / 2, -3.1, pz), -90, (-90, 0))
    K.smoke_puffs(((px0 + px1) / 2, -3.1, pz + 0.1), fr(a22 + 0.05), n=5, seed=44, col=(0.50, 0.40, 0.28), size=0.6, rise=0.8, life=18,
                  spread=0.5, alpha=0.85, name="pitdust")
    K.marker("enemy", (0, 0, 0.2), en.j["neck"])
    fill_light((0.0, -14.0, 1.0), (0, 0, 0.0), 1800, 12.0)
    keys = [(0.0, (-6.5, -11.0, 3.8), (-3.5, -1.0, 1.0), 28),
            (a20, (-3.5, -11.5, 3.0), (-0.8, -1.5, 0.6), 28),
            (a21, (-0.5, -11.0, 2.2), (1.6, -2.0, 0.2), 28),
            (a22 + 0.3, (1.0, -10.5, 0.2), (2.0, -2.5, -1.4), 28),
            (a23 + 0.2, (1.4, -10.0, 0.0), (2.0, -2.5, -1.4), 30),
            (T, (1.0, -11.5, 1.2), (1.8, -2.0, -0.8), 28)]
    campath(keys, nf, shake=0.02)


# ============================ 6) 刀隠し ============================
def n06_katana(nf):
    world(fields=False, ground_cut=Y0)
    T = SC["dur"]
    a24, _ = lt(24)
    a25, _ = lt(25)
    a26, _ = lt(26)
    a27, _ = lt(27)
    a28, _ = lt(28)
    shell(front=False, z_top=2.75, roof=False, windows=False, name="s")
    # 畳の部屋。ふとんの横の床板が1枚だけはずれて、下に刀がある
    KX0, KX1, KY0, KY1 = 1.15, 1.55, -1.6, -0.2
    board_floor(X0 + WT / 2, X1 - WT / 2, Y0, Y1 - WT / 2, Z1, "fl", skip=(KX0, KX1, KY0, KY1))
    box((X1 - X0, Y1 - Y0, 2.0), (0, 0, -1.0), M("soil"), "soil_block")
    for x in (-4.0, -1.0, 3.0, 5.0):
        box((0.16, 0.16, Z1), (x, 0.8, Z1 / 2), M("wood"), "tsuka")
    lid = K.empty((KX1, (KY0 + KY1) / 2, Z1 - 0.04), None, "klid")
    box((KX1 - KX0 - 0.02, KY1 - KY0, 0.08), (-(KX1 - KX0) / 2, 0, 0), M("board"), "klid_b", lid)
    box((KX1 - KX0 + 0.02, KY1 - KY0 + 0.04, 0.1), (-(KX1 - KX0) / 2, 0, 0), hl("klid", fr(a26 + 0.1), fr(a26 + 0.3), fr(a28 + 0.5), fr(a28 + 0.8)),
        "klid_h", lid, shadow=False)
    K.key_rot(lid, fr(a27 + 0.05), (0, 0, 0))
    K.key_rot(lid, fr(a27 + 0.25), (0, -110 * D2R, 0))
    # ふとん
    box((1.1, 2.1, 0.12), (0.4, -0.9, Z1 + 0.06), M("futon"), "shikibuton")
    kake = box((1.15, 1.45, 0.12), (0.4, -0.45, Z1 + 0.2), M("futon2"), "kakebuton")
    box((0.45, 0.28, 0.07), (0.4, -1.62, Z1 + 0.155), M("futon"), "makura")
    K.key_loc(kake, fr(a27 + 0.15), (0.4, -0.45, Z1 + 0.2))
    K.key_loc(kake, fr(a27 + 0.4), (-0.6, -0.2, Z1 + 0.1))
    # 刀：床下 → 手へ
    kt = katana("kt")
    K.key_loc(kt, 1, (1.35, -1.3, 0.12))
    K.key_rot(kt, 1, (0, 0, 0))
    K.key_loc(kt, fr(a27 + 0.2), (1.35, -1.3, 0.12))
    K.key_loc(kt, fr(a27 + 0.45), (1.35, -1.3, Z1 + 0.5))
    kt_hl = box((0.1, 1.1, 0.06), (0, 0.35, 0), hl("kt", fr(a26 + 0.5), fr(a26 + 0.7), fr(a28 + 0.5), fr(a28 + 0.8), YELLOW, 0.55, 3.0), "kt_hl", kt,
                shadow=False)
    _ = kt_hl
    K.marker("katana", (0, 0.4, 0), kt)
    # 主人公：あおむけに寝ている → 床から刀をとって、はね起きる
    HL = (0.4, 0.3, Z1 + 0.27)                  # 寝ている主人公の足もと（頭は -y の枕の上）
    hero = K.Person(HL, 0, K.HERO_NINJA, name="hero")
    hero.place(1, HL, 0, (90, 0))
    hero.stand(1, shL=(10, 10), shR=(10, 10))
    hero.place(fr(a27 + 0.15), HL, 0, (90, 0))
    hero.pose(fr(a27 + 0.15), shR=(60, 70), elR=20)
    hero.place(fr(a27 + 0.55), (0.9, -0.6, Z1), -110, (0, 0))
    hero.pose(fr(a27 + 0.55), shL=(30, 20), shR=(80, 10), elR=30, hipL=40, hipR=20, kneeL=-60, kneeR=-40, hz=-0.2)
    hero.pose(fr(a28), shL=(80, 10), shR=(85, 5), elL=60, elR=10, hipL=20, hipR=-10, kneeL=-30, kneeR=-10, hz=-0.1, spine=-8)
    hero.pose(nf, shL=(80, 10), shR=(88, 5), elL=60, elR=10, hipL=20, hipR=-10, kneeL=-30, kneeR=-10, hz=-0.1, spine=-8)
    # 刀は起き上がるときに手へ
    kt2 = katana("kt2")
    hero.hold(kt2, "R", (0, 0.02, 0), (90, 0, 0))
    K.show(kt2, fr(a27 + 0.45))
    K.key_scale(kt, fr(a27 + 0.44), 1.0)
    K.key_scale(kt, fr(a27 + 0.45), 1e-4)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    # 敵：刀をふりかぶって忍び寄る → 刀を向けられて、しりもち
    en = K.Person((-5.2, -2.6, Z1), -90, K.NINJA, name="en", seed=51)
    ekt = katana("ekt")
    en.hold(ekt, "R", (0, 0.02, 0), (90, 0, 0))
    en.stand(1)
    sneak = dict(shL=(40, 15), shR=(40, 15), elL=70, elR=70)
    en.walk(fr(0.0), fr(a25 + 0.3), [(-5.2, -2.6, Z1), (-1.0, -1.5, Z1)], arms=sneak)
    en.place(fr(a25 + 0.35), (-1.0, -1.5, Z1), -70)
    en.pose(fr(a25 + 0.45), shR=(175, 10), elR=40, shL=(160, 20), elL=30, spine=5)            # ふりかぶる
    en.pose(fr(a27 + 0.4), shR=(175, 10), elR=40, shL=(160, 20), elL=30, spine=5)
    en.place(fr(a27 + 0.6), (-1.0, -1.5, Z1), -70)
    en.place(fr(a28 - 0.1), (-1.9, -1.7, Z1), -70, (-20, 0))
    en.pose(fr(a28 - 0.1), shL=(60, 50), shR=(60, 50), elL=20, elR=20, hipL=90, hipR=90, kneeL=-60, kneeR=-60, hz=-0.6, spine=-20, neck=15)
    en.pose(nf, shL=(70, 50), shR=(70, 50), elL=20, elR=20, hipL=90, hipR=90, kneeL=-60, kneeR=-60, hz=-0.6, spine=-20, neck=15)
    K.marker("enemy", (0, 0, 0.2), en.j["neck"])
    fill_light((0.0, -14.0, 2.5), (0, 0, 0.6), 4000, 12.0)
    fill_light((1.6, -3.4, 0.25), (1.3, -1.0, 0.15), 260, 1.2, name="under")          # 床下を照らす
    cut = a26
    keys = [(0.0, (-4.0, -9.0, 4.2), (-0.5, -0.6, 0.6), 28),
            (cut - 0.02, (-2.5, -8.6, 3.2), (-0.2, -0.8, 0.8), 30),
            (cut, (2.6, -4.9, 0.25), (1.3, -0.9, 0.2), 30),
            (a27, (2.7, -5.2, 0.45), (1.3, -0.9, 0.5), 30),
            (a27 + 0.6, (1.5, -7.0, 2.2), (0.2, -0.8, 1.0), 28),
            (T, (1.0, -8.0, 2.6), (-0.2, -0.9, 1.0), 28)]
    campath(keys, nf, shake=0.02, cuts=[cut])


# ============================ 7) からくり窓 ============================
def n07_window(nf):
    world()
    T = SC["dur"]
    a29, _ = lt(29)
    a30, _ = lt(30)
    a31, _ = lt(31)
    a32, _ = lt(32)
    # 家の前の壁と、引き戸の格子窓（中に隠したかんぬき＝オレンジ）
    shell(front=False, windows=False, name="h")
    levels((1,), name="lv")
    WX, WZ, WW, WH = 0.0, 1.3, 1.6, 1.1
    ext = M("ext")
    box((WX - WW / 2 - X0, WT, EAVE), ((X0 + WX - WW / 2) / 2, Y0, EAVE / 2), ext, "fw_l")
    box((X1 - WX - WW / 2, WT, EAVE), ((X1 + WX + WW / 2) / 2, Y0, EAVE / 2), ext, "fw_r")
    box((WW, WT, WZ), (WX, Y0, WZ / 2), ext, "fw_b")
    box((WW, WT, EAVE - WZ - WH), (WX, Y0, (WZ + WH + EAVE) / 2), ext, "fw_t")
    for x in (X0, -3.0, WX - WW / 2 - 0.1, WX + WW / 2 + 0.1, 3.0, X1):
        box((0.2, 0.08, EAVE), (x, Y0 - WT / 2 - 0.04, EAVE / 2), M("wood"), "fpost")
    box((X1 - X0, 0.05, 0.9), (0, Y0 - WT / 2 - 0.03, 0.45), M("door"), "fkoshi")
    sash = K.empty((WX, Y0 - WT / 2 - 0.08, WZ), None, "sash")
    n = 11
    for k in range(n + 1):
        box((0.045, 0.06, WH), (-WW / 2 + WW * k / n, 0, WH / 2), M("wood"), "sash_bar", sash)
    for z in (0.0, WH):
        box((WW + 0.06, 0.07, 0.06), (0, 0, z), M("wood"), "sash_frame", sash)
    for s in (-1, 1):
        box((0.06, 0.07, WH), (s * WW / 2, 0, WH / 2), M("wood"), "sash_side", sash)
    box((WW + 0.4, 0.12, 0.08), (WX, Y0 - WT / 2 - 0.12, WZ - 0.06), M("wood"), "sill")
    box((WW + 0.4, 0.12, 0.08), (WX, Y0 - WT / 2 - 0.12, WZ + WH + 0.06), M("wood"), "head")
    # 中のかんぬき（窓枠を縦につらぬく木の棒）。主人公が抜くと窓が開く
    pin = box((0.05, 0.05, 0.5), (WX + WW / 2 - 0.12, Y0 + WT / 2 + 0.06, WZ + WH - 0.1), M("board"), "pin")
    box((0.09, 0.09, 0.54), (0, 0, 0), hl("pin", fr(a30 + 0.6), fr(a30 + 0.8), fr(a32 + 0.9), fr(a32 + 1.2)), "pin_hl", pin, shadow=False)
    K.marker("pin", (0, 0, 0), pin)
    t_open = a32 + 0.25
    K.key_loc(pin, fr(t_open - 0.3), tuple(pin.location))
    K.key_loc(pin, fr(t_open - 0.05), (pin.location.x, pin.location.y, pin.location.z + 0.45))
    # 敵が外から格子をつかんで、横に引いても引いても動かない（ガタガタふるえるだけ）
    en = K.Person((WX + 0.3, Y0 - 1.0, 0.0), 0, K.NINJA, name="en", seed=61)
    en.stand(1)
    en.walk(fr(0.0), fr(a29 + 0.6), [(WX - 3.0, Y0 - 2.6, 0.0), (WX + 0.3, Y0 - 0.85, 0.0)], arms=dict(shL=(40, 15), shR=(40, 15), elL=70, elR=70))
    en.place(fr(a29 + 0.65), (WX + 0.3, Y0 - 0.85, 0.0), 0)
    r = random.Random(7)
    for f in range(fr(a29 + 0.7), fr(t_open), 2):
        w = math.sin(f * 1.7)
        en.pose(f, shL=(100 + 6 * w, -10), shR=(100 - 6 * w, 10), elL=30 + 10 * w, elR=30 - 10 * w, spine=-5 - 6 * abs(w), hipL=-10, hipR=15,
                kneeL=-15, kneeR=-5)
        en.place(f, (WX + 0.3 + 0.06 * w, Y0 - 0.85 - 0.04 * abs(w), 0.0))
        sash.location = (WX + r.uniform(-0.006, 0.006), Y0 - WT / 2 - 0.08, WZ + r.uniform(-0.004, 0.004))
        sash.keyframe_insert("location", frame=f)
    # かんぬきを抜くと、窓がスッと開く → 引っぱっていた敵は、うしろへ転ぶ
    K.key_loc(sash, fr(t_open), (WX, Y0 - WT / 2 - 0.08, WZ))
    K.key_loc(sash, fr(t_open + 0.3), (WX - WW + 0.1, Y0 - WT / 2 - 0.08, WZ))
    en.fall(fr(t_open + 0.05), fr(t_open + 0.6), (WX + 0.3, Y0 - 0.85, 0.0), (-0.6, -1.6, 1.5), spin=(60, 0), ground=0.0)
    en.place(nf, face=0)
    K.marker("enemy", (0, 0, 0.2), en.j["neck"])
    # 主人公（中）：かんぬきを抜いて、窓から顔を出す
    hero = K.Person((WX + 0.5, Y0 + 0.8, Z1), 180, K.HERO_NINJA, name="hero")
    hero.stand(1)
    hero.pose(fr(t_open - 0.35), shR=(150, -10), elR=60)
    hero.pose(fr(t_open - 0.05), shR=(170, -10), elR=20)
    hero.place(fr(t_open + 0.2), (WX + 0.5, Y0 + 0.8, Z1), 180)
    hero.place(fr(t_open + 0.55), (WX - 0.3, Y0 + 0.4, Z1), 180)
    hero.pose(fr(t_open + 0.6), shL=(15, 10), shR=(150, 20), elR=95)
    fill_light((WX + 1.2, Y0 + 3.2, 2.6), (WX, Y0, 1.6), 900, 3.0, name="inner")
    fill_light((WX - 2.5, Y0 + 2.0, 2.2), (WX, Y0 + 0.6, 1.4), 400, 2.0, name="inner2")
    cut = a30 + 0.4
    keys = [(0.0, (-4.5, -11.0, 2.6), (0.0, Y0, 1.6), 30),
            (a29 + 0.6, (-1.8, -8.6, 2.0), (WX, Y0, 1.8), 30),
            (cut - 0.02, (-0.9, -7.4, 2.0), (WX, Y0, 1.8), 32),
            (cut, (WX + 1.5, Y0 + 2.6, 2.1), (WX, Y0 - 0.5, 1.8), 30),            # 中から：かんぬきが見える
            (a31 + 0.4, (WX + 1.2, Y0 + 2.3, 2.0), (WX, Y0 - 0.5, 1.8), 30),
            (a32, (WX + 1.0, Y0 + 2.6, 2.1), (WX, Y0 - 0.5, 1.7), 28),
            (T, (WX + 0.9, Y0 + 3.0, 2.2), (WX - 0.3, Y0 - 1.0, 1.3), 28)]
    campath(keys, nf, shake=0.02, cuts=[cut])


# ============================ 8) 縄ばしご ============================
def n08_rope(nf):
    world()
    T = SC["dur"]
    a33, _ = lt(33)
    a34, _ = lt(34)
    a35, _ = lt(35)
    HX0, HX1, HY0, HY1 = 4.2, 5.0, 2.4, 3.2
    H = shell(front=False, cut_roof=True, windows=True, name="h")
    _ = H
    levels((1, 2, 3), hole=(HX0, HX1, HY0, HY1), name="lv")
    box((X1 - X0, 0.15, 0.12), (0, Y0 + 0.1, Z3 - 0.05), M("wood"), "lv_edge")
    fill_light((0.0, -18.0, 5.0), (0, 0, 3.0), 5000, 14.0)
    # 口のふちを黄色く
    for k, z in enumerate((Z2, Z3)):
        K.poly_curve([(HX0, HY0, z + 0.03), (HX1, HY0, z + 0.03), (HX1, HY1, z + 0.03), (HX0, HY1, z + 0.03)], 0.03,
                     hl(f"hole{k}", fr(a34), fr(a34 + 0.2), fr(a35 + 1.0), fr(a35 + 1.3), YELLOW, 1.0, 5.0), f"holeline{k}", cyclic=True)
    # 縄ばしご：3階の口から1階まで、上から下へほどけて垂れる
    nl = rope_ladder(Z3 - Z1 + 0.1, "nawa")
    nl.location = ((HX0 + HX1) / 2, HY1 - 0.1, Z3 + 0.05)
    K.key_scale(nl, fr(a34 + 0.35), (1, 1, 0.02))
    K.key_scale(nl, fr(a34 + 0.85), (1, 1, 1.0))
    K.obj(K.box_mesh(0.7, 0.12, Z3 - Z1), hl("nawa", fr(a34 + 0.4), fr(a34 + 0.6), fr(a35 + 1.0), fr(a35 + 1.3)), nl, (0, 0, -(Z3 - Z1) / 2),
          name="nawa_hl", shadow=False)
    # 主人公：3階 → 縄ばしごを投げる → 一気にすべり下りて、裏口から外へ
    cx = (HX0 + HX1) / 2
    hero = K.Person((2.0, 2.0, Z3), 90, K.HERO_NINJA, name="hero")
    hero.stand(1)
    hero.pose(fr(a33 + 0.4), shL=(30, 30), shR=(30, 30), elL=20, elR=20, neck=-15)            # 下の敵を見て驚く
    hero.walk(fr(a34 - 0.2), fr(a34 + 0.25), [(2.0, 2.0, Z3), (cx, HY0 - 0.35, Z3)], run=True)
    hero.place(fr(a34 + 0.3), (cx, HY0 - 0.35, Z3), 0)
    hero.pose(fr(a34 + 0.3), shL=(40, 10), shR=(40, 10), elL=20, elR=20, spine=-30)           # 投げる
    hero.pose(fr(a34 + 0.5), shL=(110, 10), shR=(110, 10), elL=10, elR=10, spine=-15)
    t_dn = a35 + 0.05
    hero.place(fr(t_dn - 0.05), (cx, HY1 - 0.4, Z3), 0)
    for f in list(range(fr(t_dn), fr(t_dn + 0.55) + 1, 2)) + [fr(t_dn + 0.55)]:
        u = (f - fr(t_dn)) / max(1, fr(t_dn + 0.55) - fr(t_dn))
        hero.place(f, (cx, HY1 - 0.4, Z3 - 1.05 + (Z1 - Z3 + 1.05) * u * u), 0)
        hero.pose(f, shL=(160, 10), shR=(160, 10), elL=30, elR=30, hipL=40, hipR=40, kneeL=-50, kneeR=-50)
    hero.walk(fr(t_dn + 0.6), nf, [(cx, HY1 - 0.4, Z1), (cx + 0.2, Y1 + 0.6, Z1 - 0.3), (cx + 0.6, Y1 + 5.0, 0.0)], run=True)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    # 敵：まわりから家へかけこみ、3階へ上がってくる（間に合わない）
    r = random.Random(81)
    for i in range(8):
        a = -150 + i * 17
        p0 = (10 * math.cos(a * D2R) * 1.6, -10 + 6 * math.sin(a * D2R) - 4, 0.0)
        e = K.Person(p0, 0, K.NINJA, name=f"en{i}", seed=80 + i)
        e.stand(1)
        tgt = (r.uniform(-4.5, 3.0), r.uniform(-3.0, 0.5), Z1)
        e.walk(fr(0.05 + 0.05 * i), fr(a34 + 0.3), [p0, (tgt[0], Y0 - 0.6, 0.0), tgt], run=True)
        e.pose(fr(a34 + 0.4), shL=(30, 30), shR=(30, 30), elL=40, elR=40, neck=-25)
    keys = [(0.0, (-9.0, -26.0, 9.0), (0, 0, 2.6), 26),
            (a34 - 0.1, (-4.0, -22.0, 7.5), (1.5, 0.5, 3.2), 28),
            (a34 + 0.6, (1.5, -15.0, 6.0), (cx, 1.5, 3.6), 30),
            (a35 + 0.3, (2.5, -14.5, 3.6), (cx, 2.0, 2.0), 30),
            (T, (1.0, -18.0, 4.5), (cx - 0.5, 1.5, 2.0), 28)]
    campath(keys, nf, shake=0.02)


# ============================ 9) 完成 ============================
def n09_final(nf):
    world(trees=420)
    T = SC["dur"]
    a36, _ = lt(36)
    a37, _ = lt(37)
    a38, _ = lt(38)
    a39, _ = lt(39)
    shell(name="h")
    box((X1 - X0 + 0.6, Y1 - Y0 + 0.6, 0.45), (0, 0, 0.2), K.noisy("foundation", (0.35, 0.34, 0.32), 1.5, 0.2, 0.3), "base")
    # 生け垣と庭の木
    for k in range(14):
        x = -11 + k * 1.7
        if abs(x) > 1.6:
            K.obj(K.ellip_mesh(0.9, 0.6, 0.7, 10, 8), K.noisy("ikegaki", (0.10, 0.22, 0.06), 3.0, 0.2, 0.3), None, (x, -12.0, 0.6), name="hedge")
    for k, (x, y, kind) in enumerate([(-9.0, -6.0, 1), (9.5, -5.0, 5), (-10.5, 4.0, 2), (10.0, 5.0, 0), (-4.0, 9.0, 6)]):
        K.tree(x, y, kind, 1.0, k * 40 * D2R, name=f"tr{k}")
    hero = K.Person((0.6, -8.2, 0), 180, K.HERO_NINJA, name="hero")
    hero.stand(1)
    seal(hero, fr(a36))
    hero.pose(fr(a38 - 0.2), shL=(10, 8), shR=(10, 8), elL=12, elR=12)
    hero.wave(fr(a38), fr(a39 + 0.5), "R")
    hero.pose(fr(a39 + 0.6), shL=(150, 40), shR=(150, 40), elL=15, elR=15)
    hero.pose(nf, shL=(160, 45), shR=(160, 45), elL=10, elR=10)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    keys = [(0.0, (-60.0, -90.0, 45.0), (0, 0, 3.0), 30),
            (a37, (-30.0, -50.0, 18.0), (0, 0, 3.0), 30),
            (a38 - 0.05, (-12.0, -30.0, 9.0), (0, -2.0, 3.0), 30),
            (a38 + 0.1, (0.9, -10.6, 1.7), (0.6, -8.2, 1.5), 36),
            (a39 + 0.3, (1.2, -11.8, 2.0), (0.5, -8.0, 1.6), 34),
            (T, (-12.0, -30.0, 12.0), (0, -1.0, 3.0), 28)]
    campath(keys, nf, shake=0.03, cuts=[a38 + 0.1])


SCENES = {k: v for k, v in globals().items() if callable(v) and k[:1] == "n" and k[1:3].isdigit()}

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
