"""「もしも大谷翔平がホームランを年250本打ったら？」全場面の3D（Blender / bpy）。新幹線版（../mach）の部品を使う。
usage: python3 film.py 場面名 出力フォルダ [step] [最初 最後]
座標: ホームベースが原点、センター方向が +y（夕日も +y）。実在の人物なので顔や球団ロゴは作らない（背番号だけ）。"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, "..", "mach"))
import timeline as TL  # noqa: E402
import world as W  # noqa: E402
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("mach_film", os.path.join(HERE, "..", "mach", "film.py"))
F = importlib.util.module_from_spec(_spec)   # 新幹線版の部品（同じ名前の film.py なので別名で読む）
_spec.loader.exec_module(F)

bpy = W.bpy
from mathutils import Vector  # noqa: E402

FENCE_R = 122.0


def number_texture(path, text="17"):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (256, 256), (236, 236, 232))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(os.path.join(HERE, "..", "fonts", "NotoSansJP[wght].ttf"), 170)
    f.set_variation_by_name("Black")
    d.text((128, 140), text, font=f, fill=(20, 40, 110), anchor="mm")
    im.save(path)
    return path


def img_mat(name, path):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path)
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    return m


# ---------- 球場 ----------
def stadium(crowd=700, seed=1):
    grass = W.mat("grass", (0.10, 0.20, 0.06), 0.9)
    grass2 = W.mat("grass2", (0.12, 0.24, 0.07), 0.9)
    dirt = W.mat("dirt", (0.45, 0.30, 0.18), 1.0)
    white = W.mat("chalk", (0.95, 0.95, 0.92), 0.8)
    F.ground_y(-400, 600, x_half=600)
    # 外野の芝（しま模様）
    for i in range(14):
        W.box((0, 10 + i * 9, 0.01), (260, 9, 0.02), grass if i % 2 else grass2, bevel=0)
    # 内野の土（ダイヤモンド）
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 19.4, 0.03), rotation=(0, 0, math.radians(45)))
    o = bpy.context.object
    o.scale = (34, 34, 1)
    o.data.materials.append(dirt)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 19.4, 0.04), rotation=(0, 0, math.radians(45)))
    o = bpy.context.object
    o.scale = (22, 22, 1)
    o.data.materials.append(grass2)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=2.7, depth=0.3, location=(0, 18.4, 0.1))
    bpy.context.object.data.materials.append(dirt)
    for p in [(0, 0), (19.4, 19.4), (0, 38.8), (-19.4, 19.4)]:
        W.box((p[0], p[1], 0.06), (0.45, 0.45, 0.06), white, bevel=0)
    for s in (-1, 1):   # ファウルライン
        bpy.ops.mesh.primitive_plane_add(size=1, location=(s * 45, 45, 0.05), rotation=(0, 0, math.radians(-45 * s)))
        o = bpy.context.object
        o.scale = (0.12, 127, 1)
        o.data.materials.append(white)
    # 外野フェンスとスタンド
    wall = W.mat("fence", (0.08, 0.16, 0.12), 0.7)
    seat = [W.mat("seat_a", (0.15, 0.25, 0.45), 0.8), W.mat("seat_b", (0.55, 0.52, 0.48), 0.8)]
    r = random.Random(seed)
    crowd_m = [W.mat(f"crowd{k}", c, 0.9) for k, c in enumerate([(0.85, 0.85, 0.85), (0.15, 0.25, 0.6), (0.7, 0.15, 0.12),
                                                                 (0.2, 0.2, 0.22), (0.85, 0.7, 0.2)])]
    for k in range(-24, 25):
        a = math.radians(k * 1.85)
        x, y = FENCE_R * math.sin(a), FENCE_R * math.cos(a)
        W.box((x, y, 1.8), (5.2, 0.6, 3.6), wall, rot=(0, 0, -a), bevel=0)
        for tier in range(6):
            rr = FENCE_R + 4 + tier * 4.5
            W.box((rr * math.sin(a), rr * math.cos(a), 2.5 + tier * 2.6), (5.0, 4.4, 1.0), seat[tier % 2], rot=(0, 0, -a), bevel=0)
    # 内野スタンド（ホームの後ろ・一塁側・三塁側）
    for k in range(-20, 21):
        a = math.radians(180 + k * 4.5)
        for tier in range(8):
            rr = 30 + tier * 4.0
            W.box((rr * math.sin(a), rr * math.cos(a) + 10, 1.5 + tier * 2.2), (4.6, 4.0, 1.0), seat[tier % 2],
                  rot=(0, 0, -a), bevel=0)
    # 観客（小さな箱）
    for _ in range(crowd):
        if r.random() < 0.6:
            a = math.radians(r.uniform(-44, 44))
            tier = r.randrange(6)
            rr = FENCE_R + 4 + tier * 4.5 + r.uniform(-1.5, 1.5)
            z = 3.0 + tier * 2.6
        else:
            a = math.radians(180 + r.uniform(-88, 88))
            tier = r.randrange(8)
            rr = 30 + tier * 4.0 + r.uniform(-1.2, 1.2)
            z = 2.0 + tier * 2.2
        x, y = rr * math.sin(a), rr * math.cos(a) + (0 if abs(math.degrees(a)) < 60 else 10)
        if abs(math.degrees(a)) >= 60:
            y = rr * math.cos(a) + 10
        W.box((x, y, z + 0.5), (0.45, 0.35, 0.9), r.choice(crowd_m), bevel=0)
    # 照明塔とスコアボード
    pole = W.mat("light_pole", (0.25, 0.25, 0.27), 0.5)
    lamp = W.mat("lamp", (1, 1, 0.9), emit=(1.0, 0.95, 0.85), emit_strength=6)
    for x, y in [(-95, 95), (95, 95), (-60, -20), (60, -20)]:
        W.box((x, y, 22), (1.2, 1.2, 44), pole, bevel=0)
        W.box((x, y, 45), (8, 1.0, 4), lamp, bevel=0)
    board = W.mat("board", (0.05, 0.05, 0.06), 0.5)
    W.box((0, 160, 22), (40, 2, 18), board, bevel=0.2)
    W.box((0, 159, 22), (36, 0.2, 14), W.mat("board_lit", (0.2, 0.3, 0.5), emit=(0.2, 0.35, 0.6), emit_strength=2), bevel=0)


def player(loc, facing=0, seed=0, number=False, bat=None, helmet=True, color=(0.92, 0.92, 0.90), pose="stand"):
    """選手（ローポリ）。bat='ready'（構え）/'swing'（振り切り）/None。"""
    root, hat = F.person(loc, facing, seed=seed, pose=pose, hat=False)
    uni = W.mat(f"uniform_{color}", color, 0.8)
    pants = W.mat("pants", (0.88, 0.88, 0.86), 0.8)
    for c in root.children:
        n = c.data.materials[0].name if c.data.materials else ""
        if n.startswith("cloth"):
            c.data.materials[0] = uni if c.location.z > 0.9 else pants
    if helmet:
        hm = W.mat("helmet", (0.10, 0.18, 0.45), 0.3)
        h = W.box((0, 0, 1.88), (0.34, 0.36, 0.2), hm, bevel=0.06)
        h.parent = root
    if number:
        tex = number_texture(os.path.join(os.environ.get("TMPDIR", "/tmp"), "num17.png"))
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.135, 1.25), rotation=(math.radians(90), 0, math.radians(180)))
        p = bpy.context.object
        p.scale = (-0.32, 0.32, 1)      # 背中から見て正しい向き
        p.data.materials.append(img_mat("num17", tex))
        p.parent = root
    if bat:
        wood = W.mat("bat", (0.55, 0.40, 0.22), 0.5)
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.035, depth=0.9, location=(0, 0, 0))
        b = bpy.context.object
        b.data.materials.append(wood)
        b.parent = root
        if bat == "ready":
            b.location = (0.25, -0.05, 1.75)
            b.rotation_euler = (math.radians(-30), math.radians(25), 0)
        else:
            b.location = (-0.35, 0.35, 1.35)
            b.rotation_euler = (0, math.radians(80), math.radians(40))
    return root


def balls(flights, tm_video, glow=True):
    """ボール。flights = [(打った瞬間の動画秒, 方向(度), 距離m, 飛ぶ時間 動画秒)]。動画の時間で動かす。"""
    m = W.mat("ball", (1, 1, 1), 0.4, emit=(1.0, 0.9, 0.75) if glow else None, emit_strength=3.0 if glow else 0)
    out = []
    for (t0, ang, dist, dur) in flights:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.22 if glow else 0.04, location=(0, 0.6, 1.0))
        o = bpy.context.object
        o.data.materials.append(m)
        o.visible_shadow = False
        a = math.radians(ang)
        h = dist * 0.28
        for f, tv in enumerate(tm_video, start=1):
            u = (tv - t0) / dur
            if u < 0 or u > 1.15:
                o.scale = (0.001,) * 3
                o.location = (0, 0.6, 1.0)
            else:
                d = dist * min(u, 1.15)
                o.location = (d * math.sin(a), 0.6 + d * math.cos(a), 1.0 + 4 * h * u * (1 - u) + (0 if u <= 1 else -20 * (u - 1)))
                o.scale = (1, 1, 1)
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("scale", frame=f)
        out.append(o)
    return out


def video_time(n):
    return [i / TL.FPS for i in range(n)]


def random_flights(n, seed, t_from, t_to, dur=1.2):
    r = random.Random(seed)
    return [(r.uniform(t_from, t_to), r.uniform(-38, 38), r.uniform(125, 150), dur * r.uniform(0.9, 1.2)) for _ in range(n)]


def tmap_of(name):
    s = TL.shot(name)
    return [TL.t_of(s, i)[0] for i in range(s["frames"])]


# ---------- 場面 ----------
def o01_open(tm):
    stadium()
    W.sunset()
    player((0.9, -0.2, 0), 0, seed=1, number=True, bat="ready")
    player((0, -1.4, 0), 0, seed=4, helmet=False, color=(0.25, 0.25, 0.28), pose="sit")      # 捕手
    player((0, 18.4, 0.3), 180, seed=5, helmet=False, color=(0.85, 0.85, 0.82))              # 投手
    cam = W.camera((1.6, -6.5, 1.5), (0.2, 60, 3.0), lens=30)
    cam.keyframe_insert("location", frame=1)
    cam.location.y += 0.8
    cam.keyframe_insert("location", frame=len(tm))


def o02_swing(tm):
    stadium(crowd=300)
    W.sunset()
    player((0.9, -0.2, 0), 0, seed=1, number=True, bat="swing")
    balls([(-10, 0, 0.0, 1.0)], video_time(len(tm)))   # 当たる瞬間のボール（止まって見える）
    m = W.mat("ball2", (1, 1, 1), 0.4)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.037, location=(0.55, 0.45, 1.33))
    b = bpy.context.object
    b.data.materials.append(m)
    b.scale = (1.0, 0.8, 1.0)
    W.camera((1.6, 1.4, 1.35), (0.5, 0.4, 1.33), lens=40)


def o03a_fly(tm):
    stadium()
    W.sunset()
    player((0.9, -0.2, 0), 0, seed=1, number=True, bat="swing")
    balls(random_flights(40, 3, 0, 2.4), video_time(len(tm)))
    W.camera((2.2, -7.0, 2.2), (0, 60, 8.0), lens=26)
    F.motion_blur(True, 0.5)


def o03b_stands(tm):
    stadium()
    W.sunset()
    balls(random_flights(60, 4, -1.0, 3.0), video_time(len(tm)))
    W.camera((8, 95, 2.5), (0, 0, 12), lens=24)
    F.motion_blur(True, 0.5)


def o03c_board(tm):
    stadium()
    W.sunset()
    balls(random_flights(50, 5, -1.0, 2.5), video_time(len(tm)))
    W.camera((30, 60, 3), (0, 160, 25), lens=24)
    F.motion_blur(True, 0.5)


def o03d_last(tm):
    stadium()
    W.sunset()
    player((0.9, -0.2, 0), 0, seed=1, number=True, bat="swing")
    balls(random_flights(30, 6, -1.0, 1.4), video_time(len(tm)))
    cam = W.camera((60, -90, 70), (0, 50, 0), lens=24)
    F.motion_blur(True, 0.5)


def o06_pergame(tm):
    stadium()
    W.sunset()
    player((0.9, -0.2, 0), 0, seed=1, number=True, bat="swing")
    b = balls([(0.0, 8, 140, 4.4 * 5)], video_time(len(tm)), glow=False)[0]
    b.scale = (1, 1, 1)
    trail = W.box((0, 0, 0), (0.06, 6.0, 0.06), W.mat("ball_trail", (1, 1, 1), emit=(1, 0.95, 0.85), emit_strength=8), bevel=0)
    trail.parent = b
    trail.location = (0, -3.0, 0)
    W.camera((-12, 8, 4), (2, 20, 6), lens=24)


def o07_bonds(tm):
    stadium(crowd=400)
    W.sunset()
    player((0.9, -0.2, 0), 0, seed=1, number=True, bat="swing")
    W.camera((3.2, 2.4, 1.6), (0.6, -0.2, 1.4), lens=30)


def o08_rain(tm):
    stadium()
    W.sunset()
    r8 = random.Random(8)      # カメラのいる外野席の近くに落ちるボール
    fl = [(r8.uniform(-2.0, 4.0), r8.uniform(-4, 10), r8.uniform(124, 134), 3.0 * r8.uniform(0.9, 1.1)) for _ in range(30)]
    balls(fl, video_time(len(tm)))
    W.camera((8, 128, 6.5), (-6, 100, 8), lens=24)


def o09_lap(tm):
    stadium()
    W.sunset()
    runner = player((0, 0, 0), 45, seed=1, number=True, helmet=True)
    pts = [(0, 0), (19.4, 19.4), (0, 38.8), (-19.4, 19.4), (0, 0)]
    n = len(tm)
    for f in range(1, n + 1):
        u = 0.35 + 0.25 * f / n            # 1塁を回ったあたりから2塁へ
        seg = min(3, int(u * 4))
        k = u * 4 - seg
        p0, p1 = Vector((*pts[seg], 0)), Vector((*pts[seg + 1], 0))
        runner.location = p0.lerp(p1, k)
        d = p1 - p0
        runner.rotation_euler.z = math.atan2(-d.x, d.y)
        runner.keyframe_insert("location", frame=f)
        runner.keyframe_insert("rotation_euler", frame=f)
    W.camera((17, 23, 1.8), (8, 30, 1.2), lens=32)


def o10_distance(tm):
    stadium()
    W.sunset()
    m = W.mat("arc", (1, 0.9, 0.75), emit=(1.0, 0.85, 0.6), emit_strength=6)
    r = random.Random(10)
    for _ in range(60):          # ボールの通り道（光る線）
        a = math.radians(r.uniform(-40, 40))
        d = r.uniform(125, 150)
        pts = []
        for k in range(13):
            u = k / 12
            dd = d * u
            pts.append(Vector((dd * math.sin(a), dd * math.cos(a), 1 + 4 * d * 0.28 * u * (1 - u))))
        for p0, p1 in zip(pts, pts[1:]):
            mid = (p0 + p1) / 2
            seg = W.box(tuple(mid), (0.25, (p1 - p0).length, 0.25), m, bevel=0)
            seg.rotation_euler = (p1 - p0).to_track_quat('Y', 'Z').to_euler()
            seg.visible_shadow = False
    W.camera((0, -120, 140), (0, 60, 0), lens=26)


def o11_walk(tm):
    stadium()
    W.sunset()
    player((0.9, -0.2, 0), 0, seed=1, number=True, bat="ready")
    c = player((-1.4, -1.2, 0), 0, seed=4, helmet=False, color=(0.25, 0.25, 0.28))   # 立ち上がって外に構える捕手
    player((0, 18.4, 0.3), 180, seed=5, helmet=False, color=(0.85, 0.85, 0.82))
    b = balls([(0.0, -175, 18.0, 4.4 * 6 / 6)], video_time(len(tm)), glow=False)[0]
    b.location = (0, 18.4, 2.0)
    W.camera((5.5, -6.0, 2.0), (-0.5, 10, 1.6), lens=26)


def o12_fans(tm):
    stadium()
    W.sunset()
    for i, x in enumerate([-3, -1.5, 0, 1.5, 3, 4.5]):
        player((x, 130.5, 5.6), 180, seed=10 + i, helmet=False, color=[(0.15, 0.25, 0.6), (0.85, 0.85, 0.85)][i % 2])
    r12 = random.Random(12)
    fl = [(r12.uniform(-1.0, 4.0), r12.uniform(-3, 4), r12.uniform(126, 132), 3.0) for _ in range(14)]
    balls(fl, video_time(len(tm)))
    W.camera((2, 142, 12.0), (0, 100, 6), lens=24)


def o15_end(tm):
    o01_open(tm)


if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    first = int(sys.argv[4]) if len(sys.argv) > 4 else None
    last = int(sys.argv[5]) if len(sys.argv) > 5 else None
    W.reset()
    random.seed(1)
    s = TL.shot(name)
    tm = tmap_of(name) if "segs" in s else [0.0] * s["frames"]
    globals()[name](tm)
    F.render(out, s["frames"], step, first, last)
    print("rendered", name)
