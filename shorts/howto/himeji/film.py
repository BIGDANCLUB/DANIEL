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
    for i, (x, htop) in enumerate([(-10.6, 7.2), (-8.6, 8.4), (-6.6, 6.6), (-4.6, 7.8)]):
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
    keys = [(0.0, (-21.0, -22.0, 3.6), (-7.0, -16.4, 4.2), 32),
            (a + 1.6, (-20.5, -23.0, 5.4), (-7.0, -16.0, 5.8), 32),
            (T, (-20.0, -25.5, 3.6), (-7.0, -17.5, 3.0), 30)]
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


# ============================ 6) せまい門と上の櫓からの一斉攻撃 ============================
def orange_cover(o_size, loc, parent, f_on, f_off, name):
    """動かす部分をオレンジでぬって目立たせる（参考元2の「切る部分はオレンジ」）。"""
    m = K.fade_mat(K.glow("orange_cover", ORANGE, 2.0, 0.45), f_on, f_on + 4, f_off, f_off + 6, name=f"{name}_m")
    return K.obj(K.box_mesh(*o_size), m, parent, loc, name=name, shadow=False)


def h06_gate(nf):
    world(az=200)
    T = SC["dur"]
    a, _ = line_t(17)
    b, _ = line_t(18)
    c, _ = line_t(19)
    d, _ = line_t(20)
    HB = 5.0
    blocks = []
    for s in (-1, 1):
        root = K.empty((0, 0, 0), None, f"blk{s}")
        CS.Ishigaki(s * 9.0, 2.0, 12.0, 9.0, HB, 0.9, seed=20 + s, name=f"gb{s}", parent=root, course=0.72)
        CS.slab(s * 9.0, 2.0, HB, 12.0, 9.0, th=0.4, parent=root)
        CS.dobei([(s * 14.8, -2.2), (s * 3.6, -2.2)], z=HB, closed=False, parent=root, name=f"gbw{s}")
        blocks.append((s, root))
        # 門をせまくする：左右の石垣が内へ寄る
        K.key_loc(root, fr(b + 0.05), (0, 0, 0))
        K.key_loc(root, fr(b + 0.85), (-s * 1.9, 0, 0))
        orange_cover((12.4, 9.4, HB + 0.3), (s * 9.0, 2.0, HB / 2), root, fr(b), fr(b + 1.1), f"oc{s}")
    # 門の扉
    for s in (-1, 1):
        hinge = K.empty((s * 1.1, 4.5, 0), None, f"door{s}")
        hinge.rotation_euler = (0, 0, s * 70 * D2R)
        K.obj(K.box_mesh(1.1, 0.15, 3.6), K.noisy("door_wood", (0.13, 0.08, 0.05), 3.0, 0.3, 0.2), hinge, (-s * 0.55, 0, 1.8), name=f"door{s}_m")
    # 櫓門：せまくなった門の上にかかる（下から組み上がる）
    ya = CS.yagura(0.0, 2.0, HB, 10.0, 7.0, 3.4, 2.6, ishiotoshi=False, name="yamon")
    CS.rise_parts(ya["parts"], fr(c - 0.2), fr(c + 0.6), drop=5.0)
    # 敵の群れ（門へ向かって走り、せまい門の前でつかえる）
    ym = K.glow("yellow_arrow", YELLOW, 4.0)
    K.flow_arrow([(0, -40.0, 0.2), (0, -9.5, 0.2)], ym, fr(a + 0.05), fr(b + 0.6), width=0.7, dash=2.0, gap=1.2, speed=12.0, head=2.0,
                 name="gate_ar")
    r = random.Random(12)
    enemies = []
    for i in range(22):
        sx, sy = r.uniform(-13, 13), r.uniform(-44, -30)
        e = K.Person((sx, sy, 0), 0, K.ENEMY, name=f"g{i}", seed=100 + i)
        if i < 2:
            q = ((-0.45 if i == 0 else 0.45), -5.0, 0.0)
        else:
            row, col = divmod(i - 2, 5)
            q = ((col - 2) * 1.0 + r.uniform(-0.2, 0.2), -7.0 - row * 1.0 + r.uniform(-0.2, 0.2), 0.0)
        t_arr = c - 0.1 + r.uniform(-0.3, 0.2)
        e.walk(fr(0.05), fr(t_arr), [(sx, sy, 0), (q[0] * 0.6, -14.0, 0), q], run=True)
        if i < 2:          # 2人だけ門をくぐる
            e.walk(fr(t_arr) + 1, fr(d + 0.4), [q, (q[0], 7.0, 0)], run=False)
        else:              # 残りはつかえて足ぶみ
            for f in range(fr(t_arr) + 1, nf + 1, 4):
                w = math.sin(f * 0.7 + i)
                e.pose(f, shL=(20 + 20 * w, 15), shR=(20 - 20 * w, 15), hipL=10 * w, hipR=-10 * w, kneeL=-10, kneeR=-10, spine=-4)
        enemies.append((e, q, i))
    # 味方（赤・青）が櫓の窓と石垣の上から一斉攻撃
    allies = []
    for k, (x, y) in enumerate([(-9.5, -1.4), (-6.5, -1.4), (6.5, -1.4), (9.5, -1.4)]):
        al = K.Person((x - (1.9 if x < 0 else -1.9), y, HB), 180, K.ALLY_R if k % 2 == 0 else K.ALLY_B, name=f"al{k}", seed=200 + k)
        al.stand(1)
        K.key_scale(al.root, fr(c), 1e-4)
        K.key_scale(al.root, fr(c) + 4, 1.0)
        al.pose(fr(d), shL=(160, 10), shR=(160, 10), elL=40, elR=40)
        al.pose(fr(d) + 5, shL=(100, 10), shR=(100, 10), elL=10, elR=10, spine=-12)
        al.pose(fr(d) + 12, shL=(160, 10), shR=(160, 10), elL=40, elR=40, spine=0)
        al.pose(fr(d) + 17, shL=(100, 10), shR=(100, 10), elL=10, elR=10, spine=-12)
        allies.append(al)
    # 矢と石が雨のように降る
    am = None
    for k in range(26):
        ar = K.arrow_obj(False, f"arw{k}")
        t0 = d + 0.05 + 0.06 * k
        src = (r.uniform(-4, 4), -1.6, HB + r.uniform(2.0, 4.0))
        tgt = (r.uniform(-4.5, 4.5), r.uniform(-12, -6), 0.1)
        K.key_scale(ar, fr(t0) - 1, 1e-4)
        K.key_scale(ar, fr(t0), 1.0)
        K.projectile(ar, fr(t0), fr(t0 + 0.45), src, tgt, arc=1.2)
        _ = am
    for (e, q, i) in enemies:
        if i < 2:
            continue
        th = d + 0.35 + 0.07 * (i % 9) + r.uniform(0, 0.2)
        if th < T - 0.15:
            e.fall(fr(th), nf, (q[0], q[1], 0.0), (r.uniform(-1, 1), r.uniform(-1.5, -0.5), 2.0), spin=(-200, r.uniform(-90, 90)), ground=0.0)
    K.marker("gate", (0, -3.0, 1.5))
    K.marker("two", (0, -5.0, 1.8))
    keys = [(0.0, (0.0, -52.0, 30.0), (0, -12.0, 0.0), 26),
            (b, (0.0, -38.0, 24.0), (0, -6.0, 1.0), 26),
            (c, (5.0, -24.0, 12.0), (0, -5.0, 2.0), 26),
            (d - 0.02, (6.0, -21.0, 9.0), (0, -4.5, 2.5), 26),
            (d, (-13.0, -22.0, 3.0), (0, -3.0, 5.5), 24),
            (T, (-14.5, -24.0, 2.4), (0, -3.0, 5.0), 24)]
    K.campath(keys, nf, shake=0.03, cuts=[d])


# ============================ 7) 鉄砲で撃たれる → 壁に小さな穴 ============================
def sama_cutter(kind, x, z, y0=-0.5, y1=0.5, name="cut"):
    """狭間の穴を開ける形（外 -y がせまく、内 +y が広い）。kind：tri / circle / square。"""
    import bmesh
    bm = bmesh.new()
    so, si = 0.16, 0.34
    if kind == "circle":
        n = 16
        shp = [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)) for k in range(n)]
    elif kind == "tri":
        shp = [(-1, -0.75), (1, -0.75), (0, 1.0)]
    else:
        shp = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    vo = [bm.verts.new((x + px * so, y0 - 0.05, z + pz * so)) for px, pz in shp]
    vi = [bm.verts.new((x + px * si, y1 + 0.05, z + pz * si)) for px, pz in shp]
    bm.faces.new(vo[::-1])
    bm.faces.new(vi)
    n = len(shp)
    for k in range(n):
        bm.faces.new((vo[k], vo[(k + 1) % n], vi[(k + 1) % n], vi[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.hide_render = True
    return o


def sama_wall(x0, x1, z, h, t, holes, name="swall"):
    """穴（狭間）のある白い塀。holes = [(kind, x, z, 開くコマ)]。開くコマまでは穴の形を小さくしておく。"""
    pm = CS.plaster_mat()
    w = CS.wall_box((x0, 0), (x1, 0), z, h, t, pm, name)
    K.obj(K.box_mesh(x1 - x0, t + 0.04, 0.8), K.noisy("koshi", (0.07, 0.065, 0.06), 4.0, 0.2, 0.1, 0.7), None, ((x0 + x1) / 2, 0, z + 0.4),
          name=name + "_k")
    CS.coping((x0, 0), (x1, 0), z + h, t, name + "_c")
    for k, (kind, x, zz, f_open) in enumerate(holes):
        ct = sama_cutter(kind, x, zz, -t / 2, t / 2, f"{name}_cut{k}")
        md = w.modifiers.new(f"b{k}", 'BOOLEAN')
        md.operation = 'DIFFERENCE'
        md.object = ct
        md.solver = 'EXACT'
        if f_open is not None:
            ct.scale = (1, 1, 1)
            piv = Vector((x, 0, zz))
            ct.location = (0, 0, 0)
            # 中心から大きくする：原点を穴の中心へ
            me = ct.data
            for v in me.vertices:
                v.co = v.co - piv
            ct.location = piv
            K.key_scale(ct, max(0, f_open - 1), 1e-3)
            K.key_scale(ct, f_open + 3, 1.15)
            K.key_scale(ct, f_open + 5, 1.0)
    return w


def gunner(loc, face, look, name, seed, kneel=True):
    g = K.Person(loc, face, look, name=name, seed=seed)
    gn = K.gun()
    g.hold(gn, "R", (0, 0.02, 0), (90, 0, 0))
    aim = dict(shL=(85, -10), shR=(70, 10), elL=10, elR=70, neck=-4)
    if kneel:
        aim.update(hipL=85, kneeL=-90, hipR=-10, kneeR=-110, hz=-0.42)
    g.stand(1, **aim)
    return g, aim


def muzzle(gun_root, f, name):
    """銃口の火花とけむり。"""
    fl = K.obj(K.ellip_mesh(0.12, 0.35, 0.12, 10, 6), K.glow("muzzle", (1.0, 0.75, 0.3), 25.0), gun_root, (0, 0.62, 0.02), name=name,
               shadow=False)
    K.key_scale(fl, f - 1, 1e-4)
    K.key_scale(fl, f, 1.0)
    K.key_scale(fl, f + 2, 1e-4)
    return fl


def h07_sama(nf):
    world(elev=66, az=110)
    T = SC["dur"]
    a, _ = line_t(21)
    b, _ = line_t(22)
    c, _ = line_t(23)
    Z = 3.0
    CS.Ishigaki(0, 3.0, 40.0, 6.0, Z, 0.6, seed=31, name="lowig", course=0.75)
    CS.slab(0, 5.0, Z, 40, 10, th=0.3)
    K.obj(K.box_mesh(40, 2.4, 1.2), CS.soil_mat(), None, (0, 1.5, Z + 0.6), name="walkway")   # 壁の内側の足場
    K.obj(K.box_mesh(40, 0.9, 0.6), CS.soil_mat(), None, (0, 0.75, Z + 1.5), name="step")      # 上から撃つための段
    f_h = [fr(c + 0.25), fr(c + 0.75), fr(c + 1.25)]
    HZ = Z + 2.3
    holes = [("tri", -1.6, HZ, f_h[0]), ("circle", 0.0, HZ, f_h[1]), ("square", 1.6, HZ, f_h[2])]
    sama_wall(-20, 20, Z, 3.4, 0.42, holes)
    # 田んぼ（外）
    K.obj(K.box_mesh(60, 30, 0.05), K.noisy("paddy", (0.30, 0.36, 0.12), 0.6, 0.3, 0.2), None, (0, -22, 0.03), name="paddy")
    # 壁の上の味方（撃たれて落ちる）
    r = random.Random(7)
    for k, x in enumerate([-5.5, -2.8, 2.6, 5.4]):
        al = K.Person((x, 0.75, Z + 1.8), 180, K.ALLY_R if k % 2 else K.ALLY_B, name=f"wal{k}", seed=300 + k)
        al.stand(1, shL=(60, 10), shR=(60, 10), elL=60, elR=60)
        th = b + 0.35 + 0.22 * k
        al.fall(fr(th), fr(c - 0.1), (x, 0.75, Z + 1.8), (r.uniform(-0.5, 0.5), 2.2, 2.0), spin=(-150, 0), ground=Z + 1.2)
        K.key_scale(al.root, fr(c) - 1, 1.0)
        K.key_scale(al.root, fr(c), 1e-4)
    # 外の鉄砲隊
    gunners = []
    for k, x in enumerate([-7.5, -4.5, -1.5, 1.5, 4.5, 7.5]):
        g, aim = gunner((x, -22.0 - (k % 2) * 1.2, 0), 0, K.ENEMY, f"gun{k}", 400 + k)
        gunners.append(g)
        gn = [o for o in g.j["handR"].children][0]
        for j in range(2):
            ff = fr(b + 0.15 + 0.22 * k + 0.9 * j)
            if ff < fr(c):
                muzzle(gn, ff, f"mz{k}{j}")
                p = g.root.location
                K.smoke_puffs((p.x, p.y + 1.2, 1.1), ff, n=3, seed=k * 3 + j, col=(0.75, 0.74, 0.72), size=0.7, rise=0.8, life=26,
                              spread=0.3, alpha=0.8, name=f"gsm{k}{j}")
        K.key_scale(g.root, fr(c) - 1, 1.0)
        K.key_scale(g.root, fr(c), 1e-4)
    # 内側：職人が大きな木づちで壁をたたき、穴が開く。味方が鉄砲をかまえる
    wk = K.Person((-3.8, 2.4, Z + 1.2), 160, K.WORKER, name="wk", seed=500)
    mallet = K.empty(name="mallet")
    K.obj(K.cyl_mesh(0.07, 0.07, 2.2, 10), K.noisy("handle", (0.35, 0.22, 0.10), 4.0, 0.2, 0.1), mallet, (0, 0, -0.3))
    K.obj(K.cyl_mesh(0.45, 0.45, 1.3, 16), K.noisy("mallet_head", (0.42, 0.28, 0.14), 2.0, 0.3, 0.2), mallet, (-0.65, 0, 1.8),
          rot=(0, 90 * D2R, 0))
    wk.hold(mallet, "R", (0, 0, 0), (0, 0, 0))
    K.key_scale(wk.root, fr(c) - 1, 1e-4)
    K.key_scale(wk.root, fr(c), 1.0)
    for k, fh in enumerate(f_h):
        wk.place(fh - 8, (-1.6 + 1.6 * k - 1.4, 1.9, Z + 1.2), 200)
        wk.pose(fh - 8, shR=(200, -10), elR=30, shL=(160, 10), elL=40, spine=12)
        wk.pose(fh, shR=(95, -10), elR=5, shL=(80, 10), elL=10, spine=-20)
        wk.pose(fh + 5, shR=(150, -10), elR=20, shL=(130, 10), elL=30, spine=0)
        ring = K.obj(K.cyl_mesh(0.6, 0.6, 0.02, 24), K.fade_mat(K.glow("orange_ring", ORANGE, 4.0, 0.8), fh, fh + 1, fh + 8, fh + 12,
                     name=f"ring{k}"), None, (-1.6 + 1.6 * k, 0.24, HZ), rot=(90 * D2R, 0, 0), name=f"ring{k}", shadow=False)
        K.key_scale(ring, fh, 0.3)
        K.key_scale(ring, fh + 10, 1.4)
    for k, x in enumerate([-1.6, 0.0, 1.6]):
        g, aim = gunner((x, 0.75, Z + 1.2), 180, K.ALLY_R if k % 2 == 0 else K.ALLY_B, f"in{k}", 600 + k)
        K.key_scale(g.root, f_h[k] + 4, 1e-4)
        K.key_scale(g.root, f_h[k] + 8, 1.0)
    K.marker("holes", (0, 0, HZ))
    keys = [(0.0, (1.5, 6.5, 7.6), (0.0, -20.0, 3.0), 26),
            (a + 1.1, (0.5, -9.0, 10.0), (0.0, -24.0, 1.0), 26),
            (b - 0.02, (0.0, -12.0, 8.0), (0.0, -24.0, 1.2), 28),
            (b, (4.0, -27.0, 1.7), (0.0, 0.0, 5.6), 30),
            (c - 0.02, (3.4, -26.0, 1.9), (0.0, 0.0, 5.8), 32),
            (c, (3.4, 7.4, 6.4), (0.0, 0.0, 5.0), 28),
            (T, (2.6, 6.2, 6.1), (0.0, 0.0, 5.1), 28)]
    K.campath(keys, nf, shake=0.03, cuts=[b, c])


# ============================ 8) 狭間の図解（外からは当たらず、中からは広く） ============================
def h08_cone(nf):
    world(az=200)
    T = SC["dur"]
    a, _ = line_t(24)
    b, _ = line_t(25)
    c, _ = line_t(26)
    # --- 図解の場所（遠くに置く）：壁を真上から見る（穴の高さで切った断面）
    OX = 400.0
    sec = CS.wall_box((OX - 7, 0), (OX + 7, 0), 0.0, 1.2, 1.0, K.mat("section", (0.70, 0.69, 0.66), 0.8), "sec")
    ct = sama_cutter("square", OX, 0.6, -0.5, 0.5, "seccut")
    ct.scale = (1, 1, 6)
    md = sec.modifiers.new("b", 'BOOLEAN')
    md.operation = 'DIFFERENCE'
    md.object = ct
    md.solver = 'EXACT'
    K.obj(K.box_mesh(30, 30, 0.05), K.noisy("sec_ground", (0.36, 0.33, 0.27), 0.5, 0.2, 0.1), None, (OX, 0, -0.03), name="secg")
    ally = K.Person((OX, 1.2, -0.9), 180, K.ALLY_B, name="sec_al", seed=700)
    gn = K.gun()
    ally.hold(gn, "R", (0, 0.02, 0), (90, 0, 0))
    ally.stand(1, shL=(85, -10), shR=(70, 10), elL=10, elR=70)
    for f in range(fr(b), fr(c) + 1, 3):                 # 鉄砲の向きを左右に振る
        sw = math.sin((f - fr(b)) / K.FPS * 2.4) * 30
        ally.place(f, face=180 + sw)
    for k, x in enumerate([-3.5, 0.6, 3.8]):
        e = K.Person((OX + x, -11.0 - abs(x) * 0.3, 0), -math.degrees(math.atan2(x, 11)) * -1, K.ENEMY, name=f"sec_en{k}", seed=710 + k)
        g2 = K.gun()
        e.hold(g2, "R", (0, 0.02, 0), (90, 0, 0))
        e.stand(1, shL=(85, -10), shR=(70, 10), elL=10, elR=70)
    om = K.fade_mat(K.glow("orange_fan", ORANGE, 2.5, 0.55), fr(a + 0.1), fr(a + 0.3), fr(b), fr(b + 0.2), "ofan")
    K.fan((OX, 0.4, 1.25), (0, -1, 0), 7.0, 13.0, om, "ofan", width_at_apex=0.5)
    yfm = K.fade_mat(K.glow("yellow_fan", YELLOW, 2.5, 0.5), fr(b + 0.1), fr(b + 0.3), fr(c), fr(c + 0.2), "yfan")
    K.fan((OX, -0.5, 1.26), (0, -1, 0), 40.0, 13.0, yfm, "yfan", width_at_apex=0.3)
    # 外からの弾：ほとんど壁に当たって止まる
    r = random.Random(3)
    bm_ = K.glow("bullet", (1.0, 0.9, 0.5), 15.0)
    for k in range(6):
        bl = K.obj(K.ellip_mesh(0.07, 0.25, 0.07, 8, 6), bm_, None, (0, 0, 0), name=f"bul{k}", shadow=False)
        t0 = a + 0.15 + 0.22 * k
        x0 = r.choice([-3.5, 0.6, 3.8])
        x1 = OX + r.uniform(-4, 4) if k % 3 else OX + 0.05
        K.key_scale(bl, fr(t0) - 1, 1e-4)
        K.key_scale(bl, fr(t0), 1.0)
        K.projectile(bl, fr(t0), fr(t0 + 0.3), (OX + x0, -10.5, 1.2), (x1, -0.55, 1.2), arc=0.0)
        K.key_scale(bl, fr(t0 + 0.3), 1.0)
        K.key_scale(bl, fr(t0 + 0.3) + 1, 1e-4)
        K.smoke_puffs((x1, -0.7, 1.2), fr(t0 + 0.3), n=2, seed=k, col=(0.8, 0.78, 0.72), size=0.35, rise=0.3, life=12, spread=0.1,
                      alpha=0.9, name=f"hit{k}")
    # --- 城の全体：塀にならぶ狭間（暗い形）が、黄色く光って次々に数えられる
    ig, root = castle_on_ishigaki()
    dark = K.mat("sama_dark", (0.015, 0.015, 0.015), 0.9)
    lit = K.glow("sama_lit", YELLOW, 6.0)
    pts = WALL + [WALL[0]]
    k = 0
    holes = []
    for i in range(4):
        p0, p1 = Vector(pts[i]), Vector(pts[i + 1])
        L = (p1 - p0).length
        n = int(L / 1.5)
        dv = (p1 - p0).normalized()
        nrm = Vector((dv.y, -dv.x, 0))           # 外向き
        for j in range(1, n):
            p = p0 + dv * (L * j / n)
            if i == 0 and abs(p.x) < 2.6:
                continue
            kind = ("tri", "circle", "square")[k % 3]
            if kind == "circle":
                me = K.cyl_mesh(0.17, 0.17, 0.02, 12)
            elif kind == "tri":
                me = K.cyl_mesh(0.2, 0.2, 0.02, 3)
            else:
                me = K.box_mesh(0.3, 0.3, 0.02)
            ang = math.atan2(nrm.y, nrm.x)
            pos = (p.x + nrm.x * 0.22, p.y + nrm.y * 0.22, HI + 1.6)
            rot = (90 * D2R, 0, ang + 90 * D2R) if kind != "tri" else (90 * D2R, 0, ang + 90 * D2R)
            o = K.obj(me, dark, None, pos, rot=rot, name=f"sama{k}", shadow=False)
            g = K.obj(me, lit, None, (pos[0] + nrm.x * 0.01, pos[1] + nrm.y * 0.01, pos[2]), rot=rot, name=f"samalit{k}", shadow=False)
            holes.append(g)
            k += 1
    order = sorted(range(len(holes)), key=lambda q: (holes[q].location.x + holes[q].location.y * 0.3))
    for n_, q in enumerate(order):
        f_on = fr(c + 0.3) + int(n_ * 0.35)
        g = holes[q]
        K.key_scale(g, f_on - 1, 1e-4)
        K.key_scale(g, f_on, 1.6)
        K.key_scale(g, f_on + 4, 1.0)
    K.marker("sama", (OX, -0.5, 1.2))
    keys = [(0.0, (OX + 0.01, -0.6, 9.0), (OX, -0.9, 0.0), 30),
            (a + 0.6, (OX + 0.01, -3.2, 17.0), (OX, -4.0, 0.0), 30),
            (b, (OX + 0.01, -3.8, 21.0), (OX, -4.6, 0.0), 30),
            (c - 0.02, (OX + 0.01, -4.0, 22.0), (OX, -4.6, 0.0), 30),
            (c, (-14.0, -36.0, 19.0), (-2.0, -10.0, 12.5), 28),
            (T, (-24.0, -44.0, 24.0), (0.0, -4.0, 11.0), 28)]
    K.campath(keys, nf, shake=0.02, cuts=[c])


# ============================ 9) 火矢と白い漆喰 ============================
def h09_fire(nf):
    world(az=200)
    T = SC["dur"]
    a, _ = line_t(27)
    b, _ = line_t(28)
    c, _ = line_t(29)
    Z = 3.0
    CS.Ishigaki(0, 2.0, 16.0, 10.0, Z, 0.7, seed=41, name="fig", course=0.75)
    CS.slab(0, 2.0, Z, 16, 10, th=0.3)
    wood = CS.wood_raw_mat()
    pm = CS.plaster_mat()
    floors = [(-6.0, 6.0, Z, 4.0, 7.0), (-4.2, 4.2, Z + 4.0 + 1.0, 3.2, 5.0)]
    plaster = []
    for k, (x0, x1, z0, h, d) in enumerate(floors):
        K.obj(K.box_mesh(x1 - x0, d, h), wood, None, ((x0 + x1) / 2, 2.0, z0 + h / 2), name=f"fl{k}")
        # 板のすじ
        for j in range(int((x1 - x0) / 0.45)):
            K.obj(K.box_mesh(0.04, 0.03, h), K.mat("board_line", (0.12, 0.07, 0.035), 0.8), None, (x0 + 0.45 * (j + 0.5), 2.0 - d / 2 - 0.01, z0 + h / 2),
                  name="bl")
        CS.hip_roof((x0 + x1) / 2, 2.0, z0 + h, x1 - x0, d, 1.4 if k == 0 else 2.4, over=1.0, sori=0.3, name=f"fr{k}", gable=(k == 1))
        piv = K.empty((x0, 2.0 - d / 2 - 0.04, z0), None, f"pl{k}")
        K.obj(K.box_mesh(x1 - x0, 0.05, h), pm, piv, ((x1 - x0) / 2, 0, h / 2), name=f"plm{k}")
        plaster.append((piv, x0, x1, z0, h, d))
    # こて（巨大）と職人：1階、2階の順に左から右へぬる
    trowel = K.empty(name="trowel")
    K.obj(K.box_mesh(1.6, 0.06, 2.6), K.mat("trowel_steel", (0.22, 0.24, 0.27), 0.3), trowel, (0, -0.1, 0))
    K.obj(K.cyl_mesh(0.09, 0.09, 1.2, 10), K.noisy("handle", (0.35, 0.22, 0.10), 4.0, 0.2, 0.1), trowel, (0, -0.7, 0), rot=(90 * D2R, 0, 0))
    wk = K.Person((0, -1.5, -1.0), 0, K.WORKER, name="wk", seed=800)
    wk.root.parent = trowel
    wk.stand(1, shL=(80, 0), shR=(80, 0), elL=20, elR=20, spine=-10)
    passes = [(b + 0.05, b + 1.15, 0), (b + 1.2, b + 2.15, 1)]
    K.key_scale(trowel, fr(b) - 1, 1e-4)
    K.key_scale(trowel, fr(b), 1.0)
    for (t0, t1, k) in passes:
        piv, x0, x1, z0, h, d = plaster[k]
        y = 2.0 - d / 2 - 0.12
        K.key_loc(trowel, fr(t0), (x0 - 0.5, y, z0 + h / 2))
        K.key_loc(trowel, fr(t1), (x1 + 0.4, y, z0 + h / 2))
        K.key_scale(piv, fr(t0) - 1, (1e-4, 1, 1))
        K.key_scale(piv, fr(t0), (1e-3, 1, 1))
        K.key_scale(piv, fr(t1), (1.0, 1, 1))
        for f in range(fr(t0), fr(t1) + 1, 3):
            wobble = math.sin((f - fr(t0)) * 0.9) * 0.6
            K.key_loc(trowel, f, (x0 - 0.5 + (x1 - x0 + 0.9) * (f - fr(t0)) / (fr(t1) - fr(t0)), y, z0 + h / 2 + wobble))
    K.key_scale(trowel, fr(b + 2.2), 1.0)
    K.key_scale(trowel, fr(b + 2.3), 1e-4)
    # 火矢：射手から放物線で、板壁に刺さって燃える
    r = random.Random(21)
    archers = []
    for k, x in enumerate([-6.0, -2.0, 2.0, 6.0]):
        e = K.Person((x, -24.0, 0), 0, K.ENEMY, name=f"arch{k}", seed=900 + k)
        e.stand(1, shL=(95, -15), shR=(95, 35), elL=5, elR=120, spine=4, neck=6)
        bw_ = K.bow()
        e.hold(bw_, "L", (0, 0, 0), (0, 0, 90))
        archers.append(e)
    fires = []
    for k in range(7):
        ar = K.arrow_obj(True, f"farw{k}")
        t0 = a + 0.1 + 0.2 * k
        fl = k % 2
        piv, x0, x1, z0, h, d = plaster[fl if k < 6 else 0]
        tx = r.uniform(x0 + 0.8, x1 - 0.8)
        tz = z0 + r.uniform(0.8, h - 0.8)
        src = archers[k % 4].root.location
        K.key_scale(ar, fr(t0) - 1, 1e-4)
        K.key_scale(ar, fr(t0), 1.0)
        K.projectile(ar, fr(t0), fr(t0 + 0.55), (src.x, src.y + 0.6, 1.6), (tx, 2.0 - d / 2 - 0.3, tz), arc=5.0)
        hit = fr(t0 + 0.55)
        fire_end = None
        t_pass = None
        for (pt0, pt1, kk) in passes:
            if kk == fl:
                t_pass = pt0 + (pt1 - pt0) * (tx - x0 + 0.5) / (x1 - x0 + 0.9)
        if t_pass:
            fire_end = fr(t_pass)
        flame = K.flame((tx, 2.0 - d / 2 - 0.25, tz - 0.2), 0.9, seed=k, f0=hit, f1=fire_end, name=f"fire{k}")
        fires.append(flame)
        if fire_end:
            K.key_scale(ar, fire_end - 1, 1.0)
            K.key_scale(ar, fire_end, 1e-4)
            K.smoke_puffs((tx, 2.0 - d / 2 - 0.4, tz), fire_end, n=4, seed=50 + k, col=(0.85, 0.85, 0.85), size=0.9, rise=2.5, life=30,
                          spread=0.5, alpha=0.8, name=f"steam{k}")
    # 白い壁に当たった火矢は、はね返って落ちる
    for k in range(3):
        ar = K.arrow_obj(True, f"barw{k}")
        t0 = c - 0.45 + 0.2 * k
        piv, x0, x1, z0, h, d = plaster[k % 2]
        tx = r.uniform(x0 + 1, x1 - 1)
        tz = z0 + r.uniform(1, h - 1)
        src = archers[k].root.location
        K.key_scale(ar, fr(t0) - 1, 1e-4)
        K.key_scale(ar, fr(t0), 1.0)
        K.projectile(ar, fr(t0), fr(t0 + 0.5), (src.x, src.y + 0.6, 1.6), (tx, 2.0 - d / 2 - 0.35, tz), arc=5.0)
        K.projectile(ar, fr(t0 + 0.5), fr(t0 + 0.9), (tx, 2.0 - d / 2 - 0.35, tz), (tx + r.uniform(-1, 1), 2.0 - d / 2 - 2.5, Z), arc=0.8)
        K.smoke_puffs((tx, 2.0 - d / 2 - 0.4, tz), fr(t0 + 0.5), n=3, seed=80 + k, col=(0.6, 0.6, 0.6), size=0.5, rise=1.2, life=20,
                      spread=0.2, alpha=0.7, name=f"puff{k}")
    for k, e in enumerate(archers):
        for j in range(3):
            ff = fr(a + 0.05 + 0.2 * k + 0.8 * j)
            e.pose(ff, shR=(95, 35), elR=120)
            e.pose(ff + 3, shR=(90, 15), elR=20)
            e.pose(ff + 9, shR=(95, 35), elR=120)
    K.marker("wall", (0, 2.0 - 3.5, Z + 2.0))
    keys = [(0.0, (-9.0, -33.0, 2.2), (0.0, -2.0, 5.5), 28),
            (b - 0.4, (-6.0, -27.0, 3.5), (0.0, -1.0, 6.0), 28),
            (b + 0.2, (3.5, -15.0, 6.0), (0.0, 0.0, 5.8), 26),
            (T, (2.5, -16.5, 5.5), (0.0, 0.0, 5.8), 26)]
    K.campath(keys, nf, shake=0.03)


# ============================ 10) 完成した姫路城（1609年 → 1945年 → 2026年） ============================
KEEP = (4.0, 8.0)


def himeji_castle(trees=True, sakura=False):
    """完成した姫路城：大きな石垣の台 → 天守台 → 大天守・小天守3つ・渡櫓、まわりの塀と隅櫓、松（や桜）。"""
    big = CS.Ishigaki(0, 0, 70, 52, 9.0, 3.2, seed=51, name="big", course=0.9)
    CS.slab(0, 0, 9.0, 70, 52, th=0.4)
    top = CS.Ishigaki(KEEP[0] - 4, KEEP[1] + 2, 44, 30, 7.0, 2.2, z0=9.0, seed=52, name="tdai", course=0.8)
    CS.slab(KEEP[0] - 4, KEEP[1] + 2, 16.0, 44, 30, th=0.4)
    keep = CS.tenshu(KEEP[0], KEEP[1], 16.0, 1.0, name="keep")
    smalls = []
    for k, (x, y) in enumerate([(-15.0, 16.0), (-13.0, 0.5), (-1.0, 19.5)]):
        smalls.append(CS.tenshu(x, y, 16.0, 0.5, name=f"sk{k}", n_tiers=3))
    CS.watari((KEEP[0] - 9, KEEP[1] + 4), (-15.0, 16.0), 16.0, name="wa0")
    CS.watari((-15.0, 16.0), (-13.0, 0.5), 16.0, name="wa1")
    CS.watari((-15.0, 16.0), (-1.0, 19.5), 16.0, name="wa2")
    W2, D2 = 34.5, 25.5
    CS.dobei([(-W2, -D2), (W2, -D2), (W2, D2), (-W2, D2)], z=9.0, gap=(0, W2 - 8.0, 4.0))
    for (x, y, fc) in [(-W2 + 3.5, -D2 + 3.0, 0), (W2 - 3.5, -D2 + 3.0, 0), (W2 - 3.5, D2 - 3.0, 180), (-W2 + 3.5, D2 - 3.0, 180)]:
        CS.yagura(x, y, 9.0, 7.0, 6.0, ishiotoshi=False, face=fc, name=f"sumi{x}{y}")
    if trees:
        r = random.Random(61)
        pine = K.noisy("pine", (0.05, 0.12, 0.05), 0.8, 0.3, 0.4, 0.9)
        pink = K.noisy("sakura", (0.95, 0.62, 0.72), 0.9, 0.12, 0.4, 0.9)
        trunk = K.noisy("trunk", (0.12, 0.08, 0.05), 3.0, 0.3, 0.2)
        spots = [(r.uniform(-32, 32), r.uniform(-23, -16)) for _ in range(10)] + [(r.uniform(28, 33), r.uniform(-20, 20)) for _ in range(5)]
        spots += [(r.uniform(-55, 55), r.uniform(-48, -36)) for _ in range(18)]
        for k, (x, y) in enumerate(spots):
            z = 9.0 if abs(x) < 34 and abs(y) < 25 else 0.0
            m = pink if (sakura and k % 2 == 0) else pine
            K.obj(K.cyl_mesh(0.25, 0.18, 3.0, 8), trunk, None, (x, y, z), name="trunk")
            for j in range(3):
                s_ = r.uniform(1.8, 2.8)
                K.obj(K.ellip_mesh(s_, s_, s_ * 0.75, 10, 6), m, None, (x + r.uniform(-1.2, 1.2), y + r.uniform(-1.2, 1.2), z + 3.2 + j * 0.6),
                      name="crown")
    return keep, smalls, big


def h10a_1609(nf):
    world(az=200, fields=False)
    K.countryside(seed=7, keep_out=300, r_max=1200, n_fields=150, n_trees=200)
    keep, smalls, big = himeji_castle()
    CS.town(0, 0, 70, 280, n=230, seed=4)
    T = SC["dur"]
    a, _ = line_t(30)
    CS.rise_parts(keep["tiers"], fr(0.05), fr(1.3), drop=8.0)
    for k, sk in enumerate(smalls):
        CS.rise_parts(sk["tiers"], fr(0.1 + 0.1 * k), fr(0.9 + 0.1 * k), drop=6.0)
    for f in (fr(0.3), fr(0.65), fr(1.0), fr(1.35)):
        K.smoke_puffs((KEEP[0], KEEP[1] - 10, 16.5), f, n=4, seed=f, col=(0.85, 0.82, 0.76), size=3.0, rise=3.0, life=22, spread=6.0,
                      alpha=0.6, name=f"bdust{f}")
    # 時の流れ：太陽が回って影が動き、雲が流れる
    sun = [o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'SUN'][0]
    cl = bpy.data.objects["clouds"]
    r0 = tuple(sun.rotation_euler)
    K.key_rot(sun, fr(1.5), r0)
    K.key_rot(sun, nf, (r0[0], r0[1], r0[2] + 1.4))
    K.key_rot(cl, fr(1.5), (0, 0, 0))
    K.key_rot(cl, nf, (0, 0, 0.35))
    K.marker("keep", (KEEP[0], KEEP[1], 40.0))
    keys = [(0.0, (-30.0, -95.0, 7.0), (KEEP[0], KEEP[1], 18.0), 30),
            (1.4, (-48.0, -112.0, 24.0), (KEEP[0], KEEP[1], 24.0), 34),
            (T, (-54.0, -118.0, 30.0), (KEEP[0], KEEP[1], 24.0), 36)]
    K.campath(keys, nf, shake=0.04)


def bomber(name):
    root = K.empty(name=name)
    m = K.mat("bomber", (0.03, 0.03, 0.035), 0.5)
    K.obj(K.cyl_mesh(1.4, 1.0, 30.0, 12), m, root, (0, -15, 0), rot=(-90 * D2R, 0, 0))
    K.obj(K.box_mesh(43.0, 5.0, 0.5), m, root, (0, 1.0, 0))
    K.obj(K.box_mesh(14.0, 3.0, 0.4), m, root, (0, -13.0, 0.5))
    K.obj(K.box_mesh(0.4, 3.5, 6.0), m, root, (0, -13.5, 3.0))
    return root


def h10b_1945(nf):
    world(az=200, fields=False)
    K.countryside(seed=7, keep_out=300, r_max=1200, n_fields=120, n_trees=150)
    keep, smalls, big = himeji_castle()
    houses = CS.town(0, 0, 70, 280, n=230, seed=4)
    T = SC["dur"]
    # 夜：空は暗い赤、月の弱い光
    K.flat_sky(top=(0.004, 0.006, 0.018), horizon=(0.22, 0.05, 0.015), strength=1.0)
    sun = [o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'SUN'][0]
    sun.data.energy = 0.25
    sun.data.color = (0.55, 0.65, 1.0)
    cl = bpy.data.objects["clouds"]
    cl.hide_render = True
    r = random.Random(45)
    burning = r.sample(houses, 60)
    for k, h in enumerate(burning):
        p = h.location
        f0 = fr(r.uniform(0.0, 1.6))
        K.flame((p.x, p.y, 4.5), r.uniform(2.0, 3.2), seed=k, f0=f0, name=f"tf{k}")
        if k % 3 == 0:
            K.smoke_puffs((p.x, p.y, 8.0), f0, n=5, seed=k, col=(0.08, 0.06, 0.05), size=6.0, rise=25.0, life=70, spread=3.0, alpha=0.7,
                          name=f"ts{k}")
    # 爆撃機と焼夷弾
    for k in range(4):
        bmr = bomber(f"b29_{k}")
        y = 60 + k * 40
        K.key_loc(bmr, 1, (-500 + k * 60, y, 320 + k * 15))
        K.key_loc(bmr, nf, (300 + k * 60, y + 40, 320 + k * 15))
        bmr.rotation_euler = (0, 0, -80 * D2R)
    im = K.glow("incend", (1.0, 0.55, 0.15), 12.0)
    for k in range(40):
        st = K.obj(K.ellip_mesh(0.3, 0.3, 4.0, 6, 4), im, None, (0, 0, 0), name=f"inc{k}", shadow=False)
        t0 = r.uniform(0.0, T - 0.6)
        x, y = r.uniform(-250, 250), r.uniform(-250, 250)
        if abs(x) < 50 and abs(y) < 40:
            x += 120
        K.key_scale(st, fr(t0) - 1, 1e-4)
        K.key_scale(st, fr(t0), 1.0)
        K.key_loc(st, fr(t0), (x, y, 260))
        K.key_loc(st, fr(t0 + 0.6), (x + 8, y, 5))
        K.key_scale(st, fr(t0 + 0.6), 1e-4)
    # 城は白く浮かぶ（下からの火の照り返し）
    for k, (x, y) in enumerate([(-60, -70), (70, -60), (0, -90)]):
        lt = bpy.data.lights.new(f"glow{k}", 'AREA')
        lt.energy = 300000
        lt.size = 60
        lt.color = (1.0, 0.45, 0.15)
        lo = bpy.data.objects.new(f"glow{k}", lt)
        bpy.context.collection.objects.link(lo)
        lo.location = (x, y, 15)
        W_ = K.W
        W_.aim(lo, (KEEP[0], KEEP[1], 25))
    K.marker("keep", (KEEP[0], KEEP[1], 40.0))
    keys = [(0.0, (-70.0, -150.0, 22.0), (KEEP[0], KEEP[1], 24.0), 34),
            (T, (-60.0, -132.0, 20.0), (KEEP[0], KEEP[1], 25.0), 36)]
    K.campath(keys, nf, shake=0.03)


def h10c_final(nf):
    world(az=205, fields=False)
    K.countryside(seed=7, keep_out=300, r_max=1200, n_fields=150, n_trees=200)
    keep, smalls, big = himeji_castle(sakura=True)
    CS.town(0, 0, 70, 280, n=230, seed=4)
    T = SC["dur"]
    a, _ = line_t(32)
    b, _ = line_t(33)
    c, _ = line_t(34)
    # 主人公（最初と同じ）が城の前で手をふる
    hero = K.Person((-6.0, -60.0, 0), 160, K.HERO, name="hero")
    hero.stand(1)
    hero.wave(fr(b - 0.05), fr(c + 0.6), "R")
    hero.pose(fr(c + 0.7), shL=(150, 40), shR=(150, 40), elL=15, elR=15)
    hero.pose(nf, shL=(160, 45), shR=(160, 45), elL=10, elR=10)
    K.marker("hero", (0, 0, 0.15), hero.j["neck"])
    cut = b - 0.03
    keys = [(0.0, (60.0, -120.0, 14.0), (KEEP[0], KEEP[1], 22.0), 40),
            (cut - 0.02, (50.0, -116.0, 16.0), (KEEP[0], KEEP[1], 22.0), 42),
            (cut, (-4.6, -64.2, 1.5), (-6.0, -59.0, 4.5), 30),
            (c, (-4.8, -65.5, 1.7), (-5.5, -58.0, 6.0), 30),
            (c + 1.6, (-12.0, -100.0, 12.0), (KEEP[0], KEEP[1], 20.0), 32),
            (T, (-14.0, -110.0, 15.0), (KEEP[0], KEEP[1], 21.0), 34)]
    K.campath(keys, nf, shake=0.03, cuts=[cut])


SCENES = {k: v for k, v in globals().items() if callable(v) and k[:1] == "h" and k[1:3].isdigit()}
EXPOSURE = {"h10b_1945": 0.4}

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    first = int(sys.argv[4]) if len(sys.argv) > 4 else None
    last = int(sys.argv[5]) if len(sys.argv) > 5 else None
    K.W.reset()
    SC = TL.scene(name)
    SCENES[name](SC["nf"])
    K.render(out, SC["nf"], step, first, last, exposure=-0.8 + EXPOSURE.get(name, 0.0))
    print("rendered", name, flush=True)
