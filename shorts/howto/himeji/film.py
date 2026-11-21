"""「姫路城の作り方」全場面の3D（Blender / bpy）。参考元（0秒博士「城の作り方」）の型・絵づくりに合わせる。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import kit as K  # noqa: E402
import castle as CS  # noqa: E402
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("hj_timeline", os.path.join(HERE, "timeline.py"))   # mach/timeline.py と名前がかぶるため
TL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(TL)

bpy = K.bpy
from mathutils import Vector  # noqa: E402

D2R = K.D2R
fr = K.fr
SC = None          # 今の場面（timeline.scene）

# 本丸（石垣の上の四角い敷地）の大きさ
WT, DT, HI, DI = 32.0, 26.0, 12.0, 4.5
WALL = [(-15.5, -12.5), (15.5, -12.5), (15.5, 12.5), (-15.5, 12.5)]
YELLOW = (1.0, 0.82, 0.05)
ORANGE = (1.0, 0.38, 0.02)
BLUE = (0.15, 0.55, 1.0)


def line_t(i):
    """台本の i 行目の、この場面の頭からの (はじまり, おわり) 秒。"""
    L = SC["lines"][i]
    return L["t"], L["t_end"]


def white_attr(me, col=(1, 1, 1, 1)):
    """石の材質は頂点の色 "col" を掛けるので、石垣以外の石（共有メッシュ）にも色を入れておく。"""
    if "col" not in me.color_attributes:
        me.color_attributes.new("col", 'FLOAT_COLOR', 'POINT')
        for d in me.color_attributes["col"].data:
            d.color = col


def world(elev=50, az=215, fields=True, seed=3):
    K.daylight(elev=elev, az=az)
    K.clouds(seed=seed)
    K.ground()
    if fields:
        K.countryside(seed=seed, keep_out=70, r_max=700, n_fields=110, n_trees=140)


def gate_small(x, y, z, w=3.2, parent=None, name="gate"):
    """塀の口の門（黒い柱・冠木・小さな瓦屋根・開いた扉）。"""
    root = K.empty((x, y, z), parent, name)
    wm = CS.wood_mat()
    for sx in (-1, 1):
        K.obj(K.box_mesh(0.32, 0.32, 3.0), wm, root, (sx * w / 2, 0, 1.5), name=f"{name}_post")
        door = K.empty((sx * w / 2, 0, 0), root, f"{name}_hinge")
        door.rotation_euler = (0, 0, -sx * 80 * D2R)
        K.obj(K.box_mesh(w / 2 - 0.1, 0.12, 2.5), K.noisy("door_wood", (0.13, 0.08, 0.05), 3.0, 0.3, 0.2), door,
              (-sx * (w / 4), 0, 1.3), name=f"{name}_door")
    K.obj(K.box_mesh(w + 1.2, 0.36, 0.34), wm, root, (0, 0, 2.85), name=f"{name}_beam")
    CS.coping((-w / 2 - 0.8, 0), (w / 2 + 0.8, 0), 3.05, 1.0, f"{name}_roof", root, over=0.45, h=0.55)
    return root


def compound(z=0.0, slab=True, gate=True, parent=None):
    """本丸：家・塀・門。戻り値 (root, 塀の辺ごとの部品, 家)。"""
    root = K.empty((0, 0, z), parent, "compound")
    if slab:
        CS.slab(0, 0, 0.0, WT - 0.1, DT - 0.1, th=0.6, parent=root)
    segs = CS.dobei(WALL, z=0.0, gap=(0, 15.5, 3.4) if gate else None, parent=root)
    if gate:
        gate_small(0, -12.5, 0, 3.4, root)
    hs = CS.house(0, 3.0, 0.0, parent=root)
    return root, segs, hs


# ============================ 1) 家と塀（最初の5秒は強く動かす） ============================
def h01_house(nf):
    world()
    root, segs, hs = compound(0.0, slab=False)
    t0, _ = line_t(0)
    # 塀が地面から次々に飛び出す（奥 → 左右 → 手前の順。カメラが手前の塀をこえたあとで手前が立つ）
    order = [(2, 0.10), (1, 0.30), (3, 0.30), (0, 0.95)]
    r = random.Random(4)
    for side, ts in order:
        for k, piece in enumerate(segs[side]):
            tt = ts + 0.12 * k
            f = fr(tt)
            K.key_loc(piece, max(0, f - 1), (0, 0, -2.9))
            K.key_loc(piece, f + 5, (0, 0, 0.35))
            K.key_loc(piece, f + 8, (0, 0, -0.06))
            K.key_loc(piece, f + 10, (0, 0, 0))
            pts = CS.WALL if False else None
            _ = pts
            a, b = Vector(WALL[side]), Vector(WALL[(side + 1) % 4])
            for u in (0.15, 0.5, 0.85):
                p = a + (b - a) * u
                K.smoke_puffs((p.x, p.y, 0.2), f + 2, n=4, seed=r.randint(0, 999), col=(0.60, 0.52, 0.40), size=1.5, rise=1.5,
                              life=20, spread=1.6, alpha=0.9, name=f"dust{side}{k}{u}")
    gate = [o for o in bpy.data.objects if o.name == "gate"][0]
    K.key_loc(gate, fr(1.0), (0, -12.5, -3.4))
    K.key_loc(gate, fr(1.25), (0, -12.5, 0.3))
    K.key_loc(gate, fr(1.35), (0, -12.5, 0))
    # 主人公（赤いTシャツ・ジーンズの半ズボン・麦わら帽子）
    hero = K.Person((0, -5.2, 0), 180, K.HERO, name="hero")
    hero.stand(1, shL=(10, 10), shR=(10, 10))
    hero.pose(fr(0.25), shL=(170, 35), shR=(170, 35), elL=10, elR=10, neck=10, hz=-0.08)      # ばんざい
    hero.pose(fr(0.55), shL=(100, 70), shR=(100, 70), elL=5, elR=5, neck=5, hz=0)              # 両手を広げて見せる
    hero.pose(fr(1.6), shL=(95, 75), shR=(95, 75), elL=8, elR=8, neck=0)
    hero.pose(fr(2.05), shL=(15, 10), shR=(150, 20), elR=95, neck=-5)                         # ガッツポーズ
    hero.pose(fr(2.4), shR=(165, 15), elR=70)
    hero.pose(fr(3.1), shL=(10, 8), shR=(10, 8), elR=15, neck=0)
    hero.place(fr(3.1), face=180)
    hero.place(fr(3.6), face=200)
    hero.pose(fr(4.7), shL=(10, 8), shR=(10, 8), elL=12, elR=12)
    hero.pose(fr(5.0), shL=(135, 45), shR=(135, 45), elL=120, elR=120, neck=12, spine=6)        # 頭をかかえる
    hero.pose(fr(6.2), shL=(140, 45), shR=(140, 45), elL=125, elR=125, neck=14, spine=8)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    # 敵：左手前から走ってきて、梯子をかけて登り、塀を乗りこえる
    xs = [-12.5, -9.5, -6.5, -3.8, 4.0, 6.8, 9.6, 12.4]
    for i, x in enumerate(xs):
        e = K.Person((x - 10 + i * 0.6, -27 - (i % 3) * 1.5, 0), 20, K.ENEMY, name=f"en{i}", seed=i)
        lad = K.ladder(3.3, 0.5, f"lad{i}")
        lad.location = (x, -14.0, 0)
        ts = 3.3 + 0.08 * i
        K.key_rot(lad, max(0, fr(ts) - 1), (88 * D2R, 0, 0))
        lad.scale = (1e-4,) * 3
        K.key_scale(lad, max(0, fr(ts) - 1))
        K.key_scale(lad, fr(ts), 1.0)
        K.key_rot(lad, fr(ts + 0.22), (-30 * D2R, 0, 0))
        K.key_rot(lad, fr(ts + 0.28), (-25 * D2R, 0, 0))
        e.stand(1)
        run0, run1 = 2.3 + 0.07 * i, 4.25 + 0.08 * i
        e.walk(fr(run0), fr(run1), [tuple(e.root.location), (x, -14.6, 0)], run=True)
        c0, c1 = run1 + 0.05, run1 + 1.0
        e.climb(fr(c0), fr(c1), (x, -14.35, 0.1), (x, -13.25, 2.25), 0, tilt=-18)
        top = fr(c1)
        e.pose(top + 2, shL=(120, 40), shR=(120, 40), elL=20, elR=20, hipL=80, hipR=20, kneeL=-90, kneeR=-30, spine=-20)
        e.place(top + 4, (x, -12.75, 3.05), 0, (0, 0))
        e.place(top + 9, (x, -11.6, 1.2), 0, (0, 0))
        e.place(top + 12, (x, -11.0, 0.0), 0, (0, 0))
        e.pose(top + 12, shL=(40, 30), shR=(40, 30), elL=40, elR=40, hipL=60, hipR=60, kneeL=-100, kneeR=-100, spine=-25, hz=-0.35)
        if top + 14 < nf:
            e.walk(top + 15, nf, [(x, -11.0, 0), (x * 0.4, -7.5, 0)], run=True)
        if i == 2:
            K.marker("climb", (0, 0, 0.2), e.j["neck"])
    keys = [(0.0, (0.9, -8.0, 1.55), (0, -5.2, 1.35), 38),
            (0.35, (1.2, -10.0, 2.4), (0, -5.0, 1.5), 34),
            (1.25, (-7.5, -27.0, 10.0), (0, -1.5, 2.0), 28),
            (2.6, (-20.0, -36.0, 17.0), (0, -2.0, 1.5), 28),
            (3.3, (-17.0, -29.0, 8.0), (-3.0, -12.5, 2.0), 28),
            (SC["dur"], (-12.0, -24.5, 5.2), (-2.0, -11.5, 2.2), 30)]
    K.campath(keys, nf, shake=0.05)


# ============================ 2) 石垣を積む ============================
def h02_stone(nf):
    world()
    ig = CS.Ishigaki(0, 0, WT, DT, HI, DI, seed=2)
    root, segs, hs = compound(0.0)
    T = SC["dur"]
    ta, tb = 0.40, 2.30                           # 持ち上げる時間
    n = len(ig.courses)
    ch = HI / n

    def zc(t):
        return HI * K.smooth((t - ta) / (tb - ta))
    for f in range(1, nf + 1, 2):
        t = (f - 1) / K.FPS
        K.key_loc(root, f, (0, 0, zc(t)))
        K.key_scale(ig.core, f, (1, 1, max(1e-3, zc(t) / HI)))
    for k, ob in enumerate(ig.courses):
        # 本丸がこの段の上まで上がった瞬間に、段が外からはまりこむ
        tk = ta
        while tk < tb and zc(tk) < (k + 1) * ch:
            tk += 1 / K.FPS
        f = fr(tk)
        K.key_scale(ob, max(0, f - 7), (1e-4, 1e-4, 1e-4))
        K.key_scale(ob, max(0, f - 6), (1.45, 1.45, 0.3))
        K.key_scale(ob, f - 4, (1.32, 1.32, 1.0))
        K.key_scale(ob, f, (0.995, 0.995, 1.0))
        K.key_scale(ob, f + 2, (1.0, 1.0, 1.0))
    # 職人（オレンジの服）が石をかついで走りこむ
    r = random.Random(8)
    for i, (x, y) in enumerate([(-9, -24), (-3, -26), (3, -25), (9, -24), (-14, -21)]):
        w = K.Person((x, y, 0), 0, K.WORKER, name=f"wk{i}", seed=40 + i)
        st = K.obj(K.box_mesh(0.9, 0.7, 0.55, 0.08), CS.stone_mat(), w.j["spine"], (0, 0.05, 1.0), name=f"wkstone{i}")
        white_attr(st.data, (1.0, 0.95, 0.88, 1))
        w.root.scale = (1e-4,) * 3
        K.key_scale(w.root, 1)
        fp = fr(0.05 + 0.05 * i)
        K.key_scale(w.root, fp, 0.3)
        K.key_scale(w.root, fp + 5, 1.12)
        K.key_scale(w.root, fp + 8, 1.0)
        arms = dict(shL=(170, 20), shR=(170, 20), elL=40, elR=40)
        w.stand(1, **arms)
        w.walk(fp + 6, fr(1.6), [(x, y, 0), (x * 1.05, -19.0 - r.uniform(0, 1), 0)], run=True, arms=arms)
        w.pose(fr(1.75), shL=(120, 20), shR=(120, 20), elL=10, elR=10, spine=-15)    # 投げこむ
        K.key_scale(st, fr(1.7), 1.0)
        K.key_scale(st, fr(1.8), 1e-4)
        w.pose(fr(2.4), shL=(160, 40), shR=(160, 40), elL=15, elR=15, spine=4, hz=0.05)   # ばんざい
        w.pose(fr(T), shL=(165, 45), shR=(165, 45), elL=10, elR=10, spine=4)
    # 着地の土けむり
    fland = fr(tb)
    for side in range(4):
        for u in (0.1, 0.35, 0.65, 0.9):
            p = Vector(ig.face_point(side, (u - 0.5) * (WT + 2 * DI if side % 2 == 0 else DT + 2 * DI), 0.0))
            K.smoke_puffs((p.x, p.y, 0.3), fland - 2, n=4, seed=side * 10 + int(u * 10), col=(0.60, 0.52, 0.40), size=2.6, rise=2.5,
                          life=24, spread=3.0, alpha=0.9, name=f"land{side}{u}")
    K.marker("ishigaki", (0, -DT / 2 - DI * 0.6, 4.0))
    keys = [(0.0, (-11.0, -30.0, 1.2), (-1.0, -10.0, 2.6), 24),
            (1.4, (-14.0, -34.0, 2.2), (0, -6.0, 7.5), 24),
            (2.3, (-16.5, -37.5, 3.2), (0, -4.0, 9.6), 24),
            (T, (-17.5, -39.0, 3.6), (0, -4.0, 9.8), 24)]
    cam = K.campath(keys, nf, shake=0.04)
    # 着地でカメラが一瞬ゆれる
    for f, dz in ((fland, 0.0), (fland + 2, -0.35), (fland + 4, 0.22), (fland + 6, -0.1), (fland + 8, 0.0)):
        if f <= nf:
            cam.location.z = cam.location.z
    _ = cam


# ============================ 3) 扇の勾配（黄色い線） ============================
def castle_on_ishigaki(seed=2):
    ig = CS.Ishigaki(0, 0, WT, DT, HI, DI, seed=seed)
    root, segs, hs = compound(HI)
    return ig, root


def profile_line(ig, sx, sy, h0, h1, m, name, out=0.18):
    pts = []
    n = max(2, int((h1 - h0) / 0.2))
    for i in range(n + 1):
        h = h0 + (h1 - h0) * i / n
        p = ig.corner_point(sx, sy, h)
        pts.append((p[0] + sx * out, p[1] + sy * out, p[2]))
    return K.poly_curve(pts, 0.13, m, name)


def h03_curve(nf):
    world()
    ig, root = castle_on_ishigaki()
    T = SC["dur"]
    ym = K.glow("yellow_line", YELLOW, 4.0)
    a, _ = line_t(7)
    b, _ = line_t(8)
    c, _ = line_t(9)
    d, _ = line_t(10)
    parts = [(0.0, 4.0, a + 0.1, b - 0.1), (4.0, 9.0, b + 0.05, c - 0.1), (9.0, HI + 0.05, c + 0.05, c + 1.0)]
    for k, (h0, h1, t0, t1) in enumerate(parts):
        ln = profile_line(ig, 1, -1, h0, h1, ym, f"prof{k}")
        K.grow_line(ln, fr(t0), fr(t1))
    # てっぺんの横に白い縦線（垂直の目安）
    wm = K.glow("white_line", (1, 1, 1), 3.0)
    p = ig.corner_point(1, -1, HI)
    vl = K.poly_curve([(p[0] + 0.5, p[1] - 0.9, 7.5), (p[0] + 0.5, p[1] - 0.9, HI + 1.2)], 0.05, wm, "vertical")
    K.grow_line(vl, fr(c + 0.3), fr(c + 0.9), fr(d + 0.2))
    # 「これが扇の勾配です」：もう一方の角にも線
    ln2 = profile_line(ig, -1, -1, 0.0, HI + 0.05, ym, "prof_b")
    K.grow_line(ln2, fr(d + 0.3), fr(d + 1.1))
    K.marker("curve_mid", ig.corner_point(1, -1, 6.0))
    keys = [(0.0, (62.0, -16.6, 2.6), (17.0, -16.6, 2.4), 105),
            (b, (62.0, -15.6, 5.2), (17.0, -15.6, 5.4), 100),
            (c, (62.0, -14.6, 8.6), (17.0, -14.6, 8.8), 95),
            (d, (62.0, -15.2, 6.4), (17.0, -15.2, 6.2), 62),
            (d + 0.5, (58.0, -22.0, 7.5), (14.0, -14.0, 6.2), 45),
            (T, (40.0, -48.0, 12.0), (0.0, -10.0, 6.5), 30)]
    K.campath(keys, nf, shake=0.015)


# ============================ 4) 登るほど体が外へ反り、落ちる ============================
def h04_fall(nf):
    world()
    ig, root = castle_on_ishigaki()
    T = SC["dur"]
    a, _ = line_t(11)
    b, _ = line_t(12)
    r = random.Random(5)
    for i, (x, htop) in enumerate([(-11.0, 7.0), (-8.6, 8.2), (-6.0, 6.4), (-3.8, 7.6), (-1.5, 8.6)]):
        e = K.Person((x, -18.5, 0), 0, K.ENEMY, name=f"cl{i}", seed=60 + i)
        t_climb0 = 0.0
        t_top = 1.55 + 0.1 * i
        f0, f1 = fr(t_climb0), fr(t_top)
        for f in range(f0, f1 + 1, 2):
            u = (f - f0) / max(1, f1 - f0)
            h = 0.6 + (htop - 0.6) * (1 - (1 - u) ** 1.4)
            p = ig.face_point(0, x, h)
            incl = math.degrees(math.atan(ig.slope(h)))           # 壁の面の傾き（垂直から）
            ph = 2 * math.pi * 1.5 * (f - f0) / K.FPS + i
            s = math.sin(ph)
            arch = max(0.0, (u - 0.7) / 0.3) * 30                 # 上のほうで体が外へ反る
            e.pose(f, shL=(150 + 20 * s, 10), shR=(150 - 20 * s, 10), elL=25, elR=25, hipL=40 + 25 * s, hipR=40 - 25 * s,
                   kneeL=-(55 + 25 * s), kneeR=-(55 - 25 * s), spine=-6 + arch, neck=-20 + arch * 0.6, hz=-0.06)
            e.place(f, (p[0], p[1] - 0.32, p[2] - 0.1), 0, (-incl + arch * 0.5, 0))
        tf = b + 0.05 + 0.12 * i
        e.pose(fr(tf), shL=(170, 50), shR=(170, 50), elL=15, elR=15, spine=28, neck=25)
        ptop = ig.face_point(0, x, htop)
        e.fall(fr(tf) + 1, nf, (ptop[0], ptop[1] - 0.5, ptop[2]), (r.uniform(-0.5, 0.5), -3.2, 1.2), spin=(260, r.uniform(-60, 60)),
               ground=0.0)
        if i == 1:
            K.marker("climber", (0, 0, 0.1), e.j["neck"])
    keys = [(0.0, (-34.0, -24.5, 4.0), (-5.0, -16.5, 4.6), 40),
            (a + 1.6, (-33.0, -26.0, 5.6), (-5.0, -16.0, 5.6), 40),
            (T, (-31.0, -29.0, 4.2), (-5.0, -17.0, 3.6), 36)]
    K.campath(keys, nf, shake=0.03)


# ============================ 5) 角に集まる敵と石落とし ============================
def h05_corner(nf):
    world()
    ig, root = castle_on_ishigaki()
    T = SC["dur"]
    a, _ = line_t(13)
    b, _ = line_t(14)
    c, _ = line_t(15)
    d, _ = line_t(16)
    # 角の塀は櫓に置きかえる（櫓が組み上がる）
    ya = CS.yagura(-12.5, -10.0, HI, 7.0, 6.0, so_x=-7.0 / 2 + 1.7)
    CS.rise_parts(ya["parts"], fr(b + 0.1), fr(b + 1.3), drop=5.0)
    # 敵：2つの辺のふもとを走って角へ集まり、角の近くを登る
    ym = K.glow("yellow_arrow", YELLOW, 4.0)
    K.flow_arrow([(-4.0, -18.6, 0.2), (-19.2, -18.6, 0.2)], ym, fr(a + 0.1), fr(b + 0.2), width=0.45, dash=1.3, gap=0.9, speed=8.0, head=1.3,
                 name="ar1")
    K.flow_arrow([(-21.6, -4.0, 0.2), (-21.6, -16.6, 0.2)], ym, fr(a + 0.3), fr(b + 0.2), width=0.45, dash=1.3, gap=0.9, speed=8.0, head=1.3,
                 name="ar2")
    so = ya["so_world"]
    drop_x = -12.5 + so[0]
    climbers = []
    r = random.Random(9)
    starts = [(-6, -19.5), (-8, -20.0), (-10, -19.4), (-22.5, -6), (-22.0, -8.5), (-23.0, -10.5), (-5.0, -20.5), (-22.5, -4.5)]
    targets = [(drop_x - 0.6, 7.6), (drop_x + 0.5, 6.2), (drop_x - 1.4, 5.0), ("c", 7.0), ("c", 5.2), (drop_x + 1.2, 4.0), (drop_x - 0.2, 3.0),
               ("c", 3.2)]
    for i, ((sx, sy), (tx, htop)) in enumerate(zip(starts, targets)):
        e = K.Person((sx, sy, 0), 0, K.ENEMY, name=f"en{i}", seed=80 + i)
        corner = tx == "c"
        if corner:
            base = ig.corner_point(-1, -1, 0.0)
            foot = (base[0] - 0.4, base[1] - 0.4, 0)
        else:
            base = ig.face_point(0, tx, 0.0)
            foot = (base[0], base[1] - 0.6, 0)
        t_run1 = 1.3 + 0.08 * i
        e.walk(fr(0.05), fr(t_run1), [(sx, sy, 0), foot], run=True)
        f0, f1 = fr(t_run1) + 1, fr(min(c + 0.6, t_run1 + 2.6))
        for f in range(f0, nf + 1, 2):
            u = min(1.0, (f - f0) / max(1, f1 - f0))
            h = 0.4 + (htop - 0.4) * (1 - (1 - u) ** 1.3)
            if corner:
                p = ig.corner_point(-1, -1, h)
                p = (p[0] - 0.3, p[1] - 0.3, p[2])
                incl = math.degrees(math.atan(ig.slope(h) * 1.414))
                face = -45
            else:
                p = ig.face_point(0, tx, h)
                p = (p[0], p[1] - 0.32, p[2])
                incl = math.degrees(math.atan(ig.slope(h)))
                face = 0
            ph = 2 * math.pi * 1.4 * (f - f0) / K.FPS + i
            s_ = math.sin(ph) if u < 1 else 0.3 * math.sin(ph * 0.5)
            e.pose(f, shL=(150 + 20 * s_, 10), shR=(150 - 20 * s_, 10), elL=25, elR=25, hipL=40 + 25 * s_, hipR=40 - 25 * s_,
                   kneeL=-(55 + 25 * s_), kneeR=-(55 - 25 * s_), spine=-6, neck=-20, hz=-0.06)
            e.place(f, (p[0], p[1], p[2] - 0.1), face, (-incl, 0))
            if f > fr(d + 0.25):
                break
        climbers.append((e, corner, tx, htop))
    # 床の蓋が下へ開き、石が落ちる
    hinge = ya["hinge"]
    rest = ya["hinge_rest"]
    K.key_rot(hinge, fr(c + 0.2), (rest, 0, 0))
    K.key_rot(hinge, fr(c + 0.55), (rest + 115 * D2R, 0, 0))
    K.key_rot(hinge, fr(c + 0.65), (rest + 100 * D2R, 0, 0))
    hole = Vector((drop_x, -10.0 + so[1], HI + so[2]))
    sm = CS.stone_mat()
    hit_t = []
    for k in range(5):
        rk = K.obj(K.ellip_mesh(0.38, 0.34, 0.32, 12, 8), sm, None, tuple(hole), name=f"rock{k}")
        white_attr(rk.data)
        t0 = d - 0.05 + 0.18 * k
        f0 = fr(t0)
        K.key_scale(rk, f0 - 1, 1e-4)
        K.key_scale(rk, f0, 1.0)
        xk = drop_x + (k - 2) * 0.45
        mid = ig.face_point(0, xk, 7.5)
        bot = ig.face_point(0, xk, 0.3)
        K.key_loc(rk, f0, (xk, hole.y, hole.z))
        K.key_loc(rk, f0 + 6, (xk, mid[1] - 0.4, 7.9))
        K.key_loc(rk, f0 + 13, (xk, bot[1] - 1.5, 0.4))
        K.key_loc(rk, f0 + 20, (xk + r.uniform(-1, 1), bot[1] - 3.5, 0.35))
        K.key_rot(rk, f0, (0, 0, 0))
        K.key_rot(rk, f0 + 20, (r.uniform(-12, 12), r.uniform(-12, 12), 0))
        hit_t.append(t0 + 0.2)
    # 当たった敵は落ちる
    for i, (e, corner, tx, htop) in enumerate(climbers):
        tf = d + 0.15 + 0.06 * i
        p = ig.corner_point(-1, -1, htop) if corner else ig.face_point(0, tx, htop)
        out = (-2.2, -2.2, 0.5) if corner else (r.uniform(-0.6, 0.6), -3.0, 0.8)
        e.fall(fr(tf), nf, (p[0] - (0.3 if corner else 0), p[1] - 0.35, p[2]), out, spin=(240, r.uniform(-90, 90)), ground=0.0)
        if i == 0:
            K.marker("target", (0, 0, 0.1), e.j["neck"])
    K.marker("ishiotoshi", tuple(hole))
    cut = c - 0.03
    keys = [(0.0, (-40.0, -40.0, 15.0), (-17.0, -14.0, 3.0), 30),
            (b, (-38.0, -41.0, 15.5), (-16.0, -13.5, 6.0), 30),
            (cut - 0.01, (-34.0, -40.0, 17.0), (-14.0, -11.0, 12.5), 30),
            (cut, (-11.2, -22.5, 4.0), (drop_x, hole.y, hole.z - 0.6), 28),
            (d, (-11.5, -23.5, 3.2), (drop_x, hole.y - 0.6, hole.z - 2.5), 26),
            (T, (-11.8, -25.0, 2.6), (drop_x, -15.0, 6.0), 26)]
    K.campath(keys, nf, shake=0.03, cuts=[cut])


SCENES = {k: v for k, v in globals().items() if callable(v) and k[:1] == "h" and k[1:3].isdigit()}

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    first = int(sys.argv[4]) if len(sys.argv) > 4 else None
    last = int(sys.argv[5]) if len(sys.argv) > 5 else None
    K.W.reset()
    SC = TL.scene(name)
    SCENES[name](SC["nf"])
    K.render(out, SC["nf"], step, first, last)
    print("rendered", name, flush=True)
