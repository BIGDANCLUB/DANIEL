"""場面1（0〜5秒）：夕日に向かってホームに止まる新幹線の後ろ姿。参考の「夕日に向かって立つメロスの後ろ姿」にあたる。
usage: python3 shot01_open.py out_dir [frame_start frame_end]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import world as W  # noqa: E402

out = sys.argv[1]
f0, f1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1, 150)

W.reset()
W.ground()
W.track(0, -400, 6000)
W.track(-5.0, -400, 6000)
W.platform(x_side=+1, y_from=-170, y_to=40, roof_to=-45)
W.platform(x_side=-1, y_from=-170, y_to=40, x_track=-5.0, roof_to=-45)
W.catenary(40, 4000, 50)
W.buildings(seed=3, n=70, y_from=-200, y_to=900, x_min=30, x_max=500)
W.houses(seed=4, n=120, y_from=900, y_to=3500, x_min=20, x_max=600)
W.shinkansen(y0=0.0, cars=4)
W.sunset()

cam = W.camera((1.6, -160, 3.6), (-0.3, 300, 4.8), lens=40)
# ゆっくり前へ押し込む（参考と同じ、ほぼ止まって見えるくらいの動き）
sc = W.bpy.context.scene
cam.keyframe_insert("location", frame=f0)
cam.location.y += 1.5
cam.keyframe_insert("location", frame=150)

W.render_setup(os.path.join(out, "f_####.png"), f0, f1)
W.bpy.ops.render.render(animation=True)
