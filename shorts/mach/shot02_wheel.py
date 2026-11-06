"""場面2（0.000秒、1/500→1/1000スロー）：車輪のアップ。動き出した瞬間に火花とバラスト（砂利）が跳ねる。
参考の「足のアップ、石が跳ねる」にあたる。
usage: python3 shot02_wheel.py out_dir frame_start frame_end"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import world as W  # noqa: E402

out = sys.argv[1]
f0, f1 = int(sys.argv[2]), int(sys.argv[3])
N = 45                  # 1.5秒

W.reset()
bpy = W.bpy
W.ground()
W.track(0, -400, 6000)
W.platform(x_side=+1, y_from=-170, y_to=40, roof_to=-45)
W.buildings(seed=3, n=70, y_from=-200, y_to=900, x_min=30, x_max=500)
train = W.shinkansen(y0=0.0, cars=2)
W.sunset()

# 車輪（台車ごと2軸）
wheel_m = W.mat("wheel", (0.25, 0.24, 0.24), 0.35)
for y in (-16.4, -19.0):
    for sx in (-0.7175, 0.7175):
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.43, depth=0.14,
                                            location=(sx, y, 0.43 + 0.44), rotation=(0, math.radians(90), 0))
        o = bpy.context.object
        o.data.materials.append(wheel_m)
        o.parent = train

# 跳ねる砂利と火花（小さな箱。物理の代わりに放物線で動かす）
stone = W.mat("stone", (0.42, 0.38, 0.33), 1.0)
spark = W.mat("spark", (1, 0.6, 0.2), emit=(1.0, 0.55, 0.15), emit_strength=60)
r = random.Random(7)
for i in range(70):
    is_spark = i < 30
    s = r.uniform(0.02, 0.05) if is_spark else r.uniform(0.04, 0.12)
    sx = r.choice((-0.7175, 0.7175))
    p0 = (sx + r.uniform(-0.3, 0.3), -17.0 + r.uniform(-1.0, 1.0), 0.4)
    v = (r.uniform(-3.5, -0.5), r.uniform(-3, 1), r.uniform(1.5, 4.5))
    o = W.box(p0, (s, s * r.uniform(0.6, 1.4), s), spark if is_spark else stone, bevel=0)
    start = r.randint(3, 20)
    for f in range(1, N + 1):
        t = max(0, (f - start)) / 30 * 0.6        # スロー
        o.location = (p0[0] + v[0] * t, p0[1] + v[1] * t, max(0.32, p0[2] + v[2] * t - 4.9 * t * t))
        o.rotation_euler = (t * 9, t * 7, t * 5)
        o.scale = (1, 1, 1) if f >= start else (0, 0, 0)
        o.keyframe_insert("location", frame=f)
        o.keyframe_insert("rotation_euler", frame=f)
        o.keyframe_insert("scale", frame=f)

# 列車はほんの少しだけ前に出る（超スロー）
train.keyframe_insert("location", frame=1)
train.location.y += 0.25
train.keyframe_insert("location", frame=N)

cam = W.camera((-2.4, -19.6, 0.32), (-0.4, -10.0, 1.4), lens=17)
W.render_setup(os.path.join(out, "f_####.png"), f0, f1)
bpy.ops.render.render(animation=True)
