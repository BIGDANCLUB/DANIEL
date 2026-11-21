"""ブロック体の人（参考元＝よねあぷ のような四角い頭・ドットの顔。デザインはオリジナル）。
富士山版の person() が使う person_mesh / hat_mesh を差しかえて、すべての場面の人をこの形にする。
使い方：  import people as VP;  VP.install(FJ)   →  以後 FJ.person(...) がブロック体になる。
寸法（立ち）：脚 0.72m、胴 0.56m、頭 0.35m の立方体 → 身長 約1.67m。頭の中心の高さ：立ち 1.495m、すわり 0.975m。"""
import math
import os

from PIL import Image

HC_STAND, HC_SIT = 1.495, 0.975
HEAD = 0.35
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

SKIN = [(0.80, 0.58, 0.42), (0.72, 0.50, 0.35), (0.85, 0.66, 0.52)]
CLOTH = [(0.40, 0.50, 0.65), (0.72, 0.62, 0.42), (0.85, 0.84, 0.80), (0.42, 0.30, 0.20), (0.25, 0.27, 0.32), (0.55, 0.45, 0.35)]


def srgb(c):
    """Blender の色（リニア）→ 画像の色（sRGB 0〜255）。顔の画像と頭の色をそろえるため。"""
    out = []
    for v in c:
        v = max(0.0, min(1.0, v))
        s = 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
        out.append(int(s * 255 + 0.5))
    return tuple(out)


def face_image(skin, hair, face="neutral", brows=None, kid=False, beard=False, glasses=False):
    """16×16 ドットの顔（前から見た頭の正面）。上の2〜3列は前髪。"""
    key = f"face_{skin}_{hair}_{face}_{brows}_{kid}_{beard}_{glasses}".replace(" ", "")
    p = os.path.join(ASSETS, f"{abs(hash(key)) % 10**10}.png")
    if os.path.exists(p):
        return p
    os.makedirs(ASSETS, exist_ok=True)
    S, Hc = srgb(skin), srgb(hair)
    B = srgb(brows or tuple(h * 0.8 for h in hair))
    eye, mouth = (40, 28, 24), (120, 50, 45)
    im = Image.new("RGB", (16, 16), S)
    px = im.load()

    def put(x, y, c):
        if 0 <= x < 16 and 0 <= y < 16:
            px[x, y] = c
    for x in range(16):                     # 前髪（段々）
        for y in range(3 if x % 5 else 4):
            put(x, y, Hc)
    for y in range(3, 9):                   # もみあげ
        put(0, y, Hc)
        put(15, y, Hc)
    ey = 8
    for ex in (4, 10):                      # 目（2×2）
        for dx in (0, 1):
            for dy in (0, 1):
                put(ex + dx, ey + dy, eye)
    if face == "worried":                   # まゆ：困り顔は内側が上がる
        for k, (x, y) in enumerate(((3, 6), (4, 6), (5, 5), (10, 5), (11, 6), (12, 6))):
            put(x, y, B)
    elif face == "surprised":
        for x, y in ((3, 5), (4, 5), (5, 5), (10, 5), (11, 5), (12, 5)):
            put(x, y, B)
    else:
        for x, y in ((3, 6), (4, 6), (5, 6), (10, 6), (11, 6), (12, 6)):
            put(x, y, B)
    if face == "happy":                     # 口：笑顔は U の形
        for x, y in ((6, 12), (7, 13), (8, 13), (9, 12)):
            put(x, y, mouth)
    elif face == "worried":
        for x, y in ((6, 13), (7, 12), (8, 12), (9, 13)):
            put(x, y, mouth)
    elif face == "surprised":
        for x, y in ((7, 12), (8, 12), (7, 13), (8, 13)):
            put(x, y, mouth)
    else:
        for x in (7, 8):
            put(x, 12, mouth)
    if kid:                                 # ほっぺ
        for x in (3, 12):
            put(x, 11, (235, 150, 140))
    if beard:                               # 白いひげ
        for x in range(5, 11):
            put(x, 11, B)
    if glasses:
        for x in range(3, 13):
            put(x, 7, (30, 30, 30))
    im.save(p)
    return p


def install(FJ):
    """FJ（富士山版 film モジュール）の人の形を、ブロック体に差しかえる。"""
    W, F, bpy = FJ.W, FJ.F, FJ.bpy
    C = FJ.C
    _PM = {}

    def flat(name, col):
        return W.mat(name, col, 0.85)

    def box(c, s, m, rot=(0, 0, 0)):
        return W.box(c, s, m, rot=rot, bevel=0)

    def face_mat(path):
        m = bpy.data.materials.get(path)
        if m:
            return m
        m = bpy.data.materials.new(path)
        m.use_nodes = True
        nt = m.node_tree
        b = nt.nodes["Principled BSDF"]
        b.inputs["Roughness"].default_value = 0.85
        tx = nt.nodes.new("ShaderNodeTexImage")
        tx.image = bpy.data.images.load(path)
        tx.interpolation = 'Closest'          # ドットをくっきり
        nt.links.new(tx.outputs["Color"], b.inputs["Base Color"])
        return m

    def face_plane(cx, y, cz, w, h, m):
        """頭の正面（+y 向き）に貼る顔の板。左右・上下が正しくなるよう UV を指定。"""
        me = bpy.data.meshes.new("faceplane")
        verts = [(cx - w / 2, y, cz - h / 2), (cx + w / 2, y, cz - h / 2), (cx + w / 2, y, cz + h / 2), (cx - w / 2, y, cz + h / 2)]
        me.from_pydata(verts, [], [(0, 3, 2, 1)])
        uv = me.uv_layers.new()
        for li, vi in enumerate(me.polygons[0].vertices):
            x, _, z = verts[vi]
            uv.data[li].uv = ((1.0 if x < cx else 0.0), (1.0 if z > cz else 0.0))
        me.materials.append(m)
        o = bpy.data.objects.new("faceplane", me)
        bpy.context.collection.objects.link(o)
        return o

    def limb(p0, p1, t, m):
        from mathutils import Vector
        p0, p1 = Vector(p0), Vector(p1)
        d = p1 - p0
        rot = d.to_track_quat('Z', 'Y').to_euler()
        return box(tuple((p0 + p1) / 2), (t, t, d.length), m, rot=tuple(rot))

    def person_mesh(variant, pose="stand", arms="down", look=None):
        look = look or {}
        key = (variant, pose, arms, tuple(sorted(look.items())))
        if key in _PM:
            return _PM[key]
        sk = look.get("skin", SKIN[variant % 3])
        skin = flat(f"vskin_{sk}", sk)
        tc = look.get("top", CLOTH[variant % 6])
        top = flat(f"vtop_{tc}", tc)
        bc = look.get("bottom", CLOTH[(variant + 3) % 6])
        bottom = flat(f"vbot_{bc}", bc)
        hc_col = look.get("hair", (0.06, 0.045, 0.035))
        hair = flat(f"vhair_{hc_col}", hc_col)
        shoe = flat("vshoe", (0.10, 0.08, 0.07))
        p = []
        if pose == "sit":
            hip = 0.2
            for sx in (-1, 1):
                p.append(box((sx * 0.1, 0.2, hip), (0.17, 0.46, 0.17), bottom))
                p.append(box((sx * 0.1, 0.42, hip - 0.24), (0.16, 0.16, 0.44), bottom))
                p.append(box((sx * 0.1, 0.47, hip - 0.47), (0.17, 0.26, 0.08), shoe))
        else:
            hip = 0.72
            for sx in (-1, 1):
                p.append(box((sx * 0.1, 0, 0.40), (0.17, 0.18, 0.64), bottom))
                p.append(box((sx * 0.1, 0.03, 0.04), (0.18, 0.26, 0.08), shoe))
        p.append(box((0, 0, hip + 0.04), (0.38, 0.21, 0.1), bottom))
        p.append(box((0, 0, hip + 0.33), (0.40, 0.22, 0.50), top))
        sh = hip + 0.56
        hc = sh + 0.04 + HEAD / 2
        for sx in (-1, 1):
            s0 = (sx * 0.27, 0, sh - 0.06)
            a = arms if isinstance(arms, str) else arms[0 if sx < 0 else 1]
            if a == "pray":
                h = (sx * 0.04, 0.24, sh - 0.12)
            elif a == "up":
                h = (sx * 0.42, 0.04, sh + 0.52)
            elif a == "head":
                h = (sx * 0.2, 0.05, hc + 0.12)
            elif a == "brow":
                h = (sx * 0.08, 0.26, hc + 0.05)
            elif a == "wave":
                h = (sx * 0.5, 0.0, sh + 0.42)
            elif a == "hold":
                h = (sx * 0.12, 0.36, sh - 0.3)
            else:
                h = (sx * 0.285, 0.01, sh - 0.6)
            from mathutils import Vector
            v = Vector(h) - Vector(s0)
            tip = Vector(s0) + v.normalized() * (v.length - 0.06)
            p.append(limb(s0, tuple(tip), 0.13, top))           # 腕（四角い棒）
            p.append(box(h, (0.13, 0.13, 0.13), skin, rot=tuple(v.to_track_quat('Z', 'Y').to_euler())))   # 手
        # 頭（立方体）と髪の箱
        p.append(box((0, 0, hc), (HEAD, HEAD * 0.95, HEAD), skin))
        p.append(box((0, -0.012, hc + HEAD / 2 + 0.03), (HEAD + 0.03, HEAD * 0.95 + 0.04, 0.07), hair))        # 頭の上
        p.append(box((0, -HEAD * 0.475 - 0.012, hc + 0.05), (HEAD + 0.03, 0.04, HEAD * 0.82), hair))          # うしろ
        for sx in (-1, 1):
            p.append(box((sx * (HEAD / 2 + 0.012), -0.03, hc + 0.09), (0.03, HEAD * 0.95 - 0.04, HEAD * 0.55), hair))
        if look.get("long"):
            p.append(box((0, -HEAD * 0.48 - 0.02, hc - 0.15), (HEAD + 0.03, 0.05, HEAD * 0.9), hair))
        img = face_image(sk, hc_col, look.get("face", "neutral"), look.get("brows"), look.get("kid", False),
                         look.get("beard", False), look.get("glasses", False))
        p.append(face_plane(0, HEAD * 0.475 + 0.002, hc, HEAD, HEAD, face_mat(img)))
        me = F._join(p, f"vp_{variant}_{pose}_{arms}_{len(_PM)}")
        _PM[key] = me
        return me

    def hat_mesh(kind):
        key = ("hat", kind)
        if key in _PM:
            return _PM[key]
        top = HC_STAND + HEAD / 2
        m = W.mat("vcap_white", (0.92, 0.92, 0.90), 0.6) if kind == "white" else W.mat("vcap", (0.15, 0.25, 0.45), 0.8)
        parts = [box((0, -0.01, top + 0.06), (HEAD + 0.05, HEAD + 0.03, 0.12), m),
                 box((0, HEAD / 2 + 0.07, top + 0.01), (HEAD * 0.8, 0.16, 0.025), m)]
        _PM[key] = F._join(parts, f"vhat_{kind}")
        return _PM[key]

    FJ.person_mesh = person_mesh
    FJ.hat_mesh = hat_mesh
    _ = C, math
    return person_mesh
