#!/usr/bin/env python3
"""
体位クイズ SVG 生成エンジン v3
- HEADR を大きく / torso を長く / 四肢を太くして「棒人間らしさ」を強調
- 側位は「枕」（横向き胴体を明確なL字）で区別
- 全プリミティブを再設計（明示座標）
"""
import cairosvg, json, sys

SW   = '2.8'   # main stroke width
SWH  = '2.2'   # hair stroke width
HEADR = 13

SA = f'stroke="#111" stroke-width="{SW}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
HA = f'stroke="#111" stroke-width="{SWH}" fill="none" stroke-linecap="round" stroke-linejoin="round"'

# ─── 基本描画ヘルパー ─────────────────────────────
class Figure:
    def __init__(self, long=False):
        self.long = long
        self.head = None      # (lx, ly) local coords
        self.segs = []        # list of [(lx,ly), ...]

    def S(self, *pts):
        self.segs.append(list(pts))

def emit(fig, ox, oy, flip):
    """ローカル座標 → SVG 文字列。flip=1 で右向き、flip=-1 で左右反転。"""
    def T(p): return (ox + flip * p[0], oy + p[1])
    out = []
    for seg in fig.segs:
        pts = " L ".join(f"{T(p)[0]:.1f},{T(p)[1]:.1f}" for p in seg)
        out.append(f'<path d="M {pts}" {SA}/>')
    if fig.head:
        hx, hy = T(fig.head)
        r = HEADR
        out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{r}" {SA}/>')
        if fig.long:
            # 女性：両サイドに長く垂れる髪（センター分け）＝「長髪」を強調
            out.append(f'<path d="M{hx:.1f},{hy-r-1:.1f} L{hx:.1f},{hy-r+4:.1f}" {HA}/>')                                       # センター分け目
            out.append(f'<path d="M{hx-r+1:.1f},{hy-4:.1f} Q{hx-r-5:.1f},{hy+12:.1f} {hx-r-3:.1f},{hy+26:.1f}" {HA}/>')        # 左に長く垂れる髪
            out.append(f'<path d="M{hx+r-1:.1f},{hy-4:.1f} Q{hx+r+5:.1f},{hy+12:.1f} {hx+r+3:.1f},{hy+26:.1f}" {HA}/>')        # 右に長く垂れる髪
            out.append(f'<path d="M{hx-r+1:.1f},{hy-4:.1f} Q{hx:.1f},{hy-r-3:.1f} {hx+r-1:.1f},{hy-4:.1f}" {HA}/>')            # 生え際
        else:
            # 男性：頭頂だけの短髪（クルーカット）＝サイドに髪なし
            out.append(f'<path d="M{hx-r+1:.1f},{hy-3:.1f} Q{hx:.1f},{hy-r-9:.1f} {hx+r-1:.1f},{hy-3:.1f}" {HA}/>')            # 短髪トップ（頭頂のみ盛り上げ）
    return "".join(out)

def mir(placements):
    """全シーンを左右反転（ox=200-ox で折り返し）。"""
    return [[p, l, a, 200 - x, y, -f] for p, l, a, x, y, f in placements]

# ─── プリミティブ定義 ─────────────────────────────
# 座標系：ローカル。pelvis/floor など各プリミティブで基準を定義。
# x 正方向 = flip=1 のとき右方向（頭は -x 側が多い）

# ── 直立（STAND）
def STAND(long=False, legs='together', arms='down'):
    """直立。pelvis (0,0)。頭上方(-y)。"""
    f = Figure(long)
    f.head = (0, -53)
    f.S((0, 0), (0, -42))          # 胴
    sh = (0, -36)
    {
        'down':  lambda: f.S(sh, (14, -22), (20, -4)),
        'reach': lambda: f.S(sh, (20, -32), (36, -32)),
        'hold':  lambda: f.S(sh, (18, -26), (32, -22)),
        'hug':   lambda: f.S(sh, (16, -30), (30, -34)),
        'up':    lambda: f.S(sh, (10, -54), (16, -68)),
        'back':  lambda: f.S(sh, (-14, -22), (-22, -12)),
    }[arms]()
    f.S(sh, (-12, -22), (-18, -4))  # 反対腕（常に下）
    {
        'together': lambda: [f.S((0,0), (4,26),  (4,52)),  f.S((0,0), (-4,26), (-4,52))],
        'spread':   lambda: [f.S((0,0), (16,24), (20,50)), f.S((0,0), (-16,24),(-20,50))],
        'stride':   lambda: [f.S((0,0), (18,22), (24,48)), f.S((0,0), (-14,26),(-16,50))],
        'wide':     lambda: [f.S((0,0), (20,20), (26,48)), f.S((0,0), (-20,20),(-26,48))],
        'oneup':    lambda: [f.S((0,0), (4,26),  (4,52)),  f.S((0,0), (22,6),  (38,14))],
    }[legs]()
    return f

# ── 前傾立位（STANDBEND）― 立ちバックの受け手
def STANDBEND(long=False, arms='hang'):
    """腰から前傾。pelvis (0,0)。"""
    f = Figure(long)
    f.head = (48, -34)
    f.S((0,0), (38, -28))             # 胴（前傾）
    if arms == 'hang':
        f.S((36, -26), (42, 0)); f.S((30, -22), (36, 0))
    else:
        f.S((36, -26), (52, -20))
    f.S((0,0), (2, 26), (0, 52))      # 脚
    f.S((0,0), (-6, 26), (-8, 52))
    return f

# ── 仰向け（SUPINE）― 頭は -x 側、脚は +x 側
def SUPINE(long=False, legs='bent', arms='rest'):
    """仰向け。床 y=0。pelvis (0,0)。頭左・脚右。"""
    f = Figure(long)
    f.head = (-56, -12)
    f.S((-44, -10), (0, 0))           # 脊柱
    {
        'rest': lambda: f.S((-32, -10), (-48, 2)),
        'up':   lambda: f.S((-32, -10), (-42, -24)),
        'hold': lambda: f.S((-30, -10), (-14, -18)),
    }[arms]()
    {
        'bent':     lambda: [f.S((0,0),(30,-26),(44,0)),   f.S((0,0),(32,-6),(50,0))],
        'straight': lambda: [f.S((0,0),(52,-2)),           f.S((0,0),(50,6))],
        'raised':   lambda: [f.S((0,0),(24,-34),(32,-60)), f.S((0,0),(30,-26),(42,-48))],
        'spread':   lambda: [f.S((0,0),(30,-18),(44,-32)), f.S((0,0),(30,10), (44,20))],
        'overhead': lambda: [f.S((0,0),(10,-32),(4,-60)),  f.S((0,0),(18,-30),(16,-58))],
    }[legs]()
    return f

# ── 四つん這い（ALLFOURS）― 頭左・尻右
def ALLFOURS(long=False):
    """四つん這い。床 y=0。"""
    f = Figure(long)
    f.head = (-64, -34)
    f.S((-50, -36), (0, -36))         # 背中（水平）
    f.S((-50, -36), (-50, 0))         # 前腕
    f.S((-46, -36), (-48, 0))         # 前腕（もう片方）
    f.S((0, -36), (0, 0))             # 後大腿
    f.S((0, 0), (16, 0))              # すね（床に沿う）
    return f

# ── 膝立ち（KNEEL）― 膝床、上体ほぼ直立
def KNEEL(long=False, arms='reach', lean=0):
    """膝立ち。膝床 y=0。"""
    f = Figure(long)
    dx = lean
    f.S((0, 0), (0, -28))             # 太もも（膝→腰）
    f.S((0, -28), (dx, -64))          # 胴（腰→肩）
    f.head = (dx, -76)
    sh = (dx * 0.8, -57)
    {
        'reach': lambda: f.S(sh, (18,  2), (34,  4)),
        'hold':  lambda: f.S(sh, (16, -4), (30, -8)),
        'hug':   lambda: f.S(sh, (16, -8), (30,-12)),
        'down':  lambda: [f.S(sh, (10, 8), (14, 26)), f.S(sh, (-12,-6), (-18, 8))],
        'back':  lambda: f.S(sh, (-14, -4), (-26, -12)),
    }[arms]()
    if arms not in ('down',):
        f.S(sh, (-12, -6), (-18, 8))   # 反対腕
    f.S((0, 0), (-14, 2))              # 脛
    return f

# ── 座位（SIT）― 尻床、上体直立
def SIT(long=False, legs='forward', arms='hold'):
    """座位。尻床 y=0。"""
    f = Figure(long)
    f.S((0, 0), (0, -42))
    f.head = (0, -54)
    sh = (0, -38)
    {
        'hold':  lambda: f.S(sh, (16, -24), (30, -22)),
        'hug':   lambda: f.S(sh, (16, -28), (30, -30)),
        'back':  lambda: f.S(sh, (-14, -24), (-24, -14)),
        'knee':  lambda: f.S(sh, (18, -14), (30,  -6)),
        'reach': lambda: f.S(sh, (22, -30), (38, -28)),
    }[arms]()
    f.S(sh, (-12, -22), (-18, -6))    # 反対腕
    {
        'forward':  lambda: [f.S((0,0),(28,-16),(44,4)),   f.S((0,0),(28,-8),(46,8))],
        'cross':    lambda: [f.S((0,0),(24, 4),(42,-4)),   f.S((0,0),(22,10),(40, 4))],
        'wide':     lambda: [f.S((0,0),(30,-14),(48,2)),   f.S((0,0),(30,12),(48,22))],
        'bentknee': lambda: [f.S((0,0),(22,-20),(36, 0)),  f.S((0,0),(26,-12),(42, 4))],
        'folded':   lambda: [f.S((0,0),(20,-22),(10, 0)),  f.S((0,0),(22,-18),(14, 2))],
    }[legs]()
    return f

# ── 側位（SIDELIE）― 頭左・胴右・膝前（Y 方向に高さを出す）
def SIDELIE(long=False, knees='bent'):
    """横向き寝。床 y=0。頭は -x 側で枕の上に乗る感じ。"""
    f = Figure(long)
    # 頭を少し持ち上げ（枕代わりの腕）
    f.head = (-56, -28)
    f.S((-44, -25), (0, -14))                  # 脊柱（少し起き上がる）
    f.S((-42, -23), (-28, -8))                 # 下になる腕（前へ）
    # 脚
    if knees == 'bent':
        f.S((0,-14),(26,-22),(36, 2))           # 上の脚
        f.S((0,-14),(24,-14),(36, 6))           # 下の脚
    elif knees == 'straight':
        f.S((0,-14),(48,-6))
        f.S((0,-14),(48, 2))
    elif knees == 'curl':
        f.S((0,-14),(20,-26),(14, 2))
        f.S((0,-14),(22,-20),(18, 4))
    elif knees == 'wide':
        f.S((0,-14),(28,-30),(38,-6))
        f.S((0,-14),(24,  4),(36,14))
    return f

# ── 覆いかぶさり（OVER）― 正常位の上になる側
def OVER(long=False, arms='straight', legs='kneel'):
    """覆いかぶさり。pelvis (0,0) を SUPINE の腰に合わせる。"""
    f = Figure(long)
    f.head = (-48, -34)
    f.S((-36, -30), (0, 0))            # 斜め胴
    if arms == 'straight':
        f.S((-32, -28), (-28,  2))
        f.S((-24, -22), (-20,  2))
    elif arms == 'elbow':
        f.S((-32, -28), (-18, -12))
        f.S((-24, -22), (-12, -10))
    {
        'kneel': lambda: [f.S((0,0),(14,20),(28,20)), f.S((0,0),(18,18),(32,22))],
        'ext':   lambda: [f.S((0,0),(26,10),(50,14)), f.S((0,0),(26,16),(50,22))],
    }[legs]()
    return f

# ── 抱えられ（CARRY）― 抱き上げられる側
def CARRY(long=False):
    """抱えられ。宙に浮く。pelvis (0,0)。"""
    f = Figure(long)
    f.S((0, 0), (-4, -40))
    f.head = (-6, -52)
    f.S((-2, -36), (-22, -24))         # しがみつく腕
    f.S((0,  0),  (22, -8),  (36,-20))  # 巻きつく脚
    f.S((0,  0),  (20, 8),   (32, -2))
    return f

# ── 倒立（INVERT）― 肩立ち、頭下
def INVERT(long=False):
    """肩立ち。床 y=0。"""
    f = Figure(long)
    f.head = (-2, -8)
    f.S((-2, -14), (2, -48))           # 胴（逆立ち）
    f.S((0, -14), (-18, -6))           # 支え腕
    f.S((0, -14), ( 14, -6))
    f.S((2, -48), (-10, -70))          # 上に伸びる脚
    f.S((2, -48), ( 12, -70))
    return f

# ── 前傾後背（OVER_BACK）― 立ちバックの攻め手
def OVER_BACK(long=False, arms='hold'):
    """立ったまま前傾してもたれかかる。pelvis (0,0)。"""
    f = Figure(long)
    f.head = (-44, -36)
    f.S((-34, -32), (0, 0))
    f.S((-30, -28), (-12, -18))        # 相手を押さえる腕
    f.S((-30, -28), (-36,  2))         # 逆腕（床支え）
    f.S((0, 0), (2, 26), (0, 52))
    f.S((0, 0), (-6, 26), (-8, 52))
    return f

PRIMS = {
    'STAND': STAND, 'STANDBEND': STANDBEND, 'SUPINE': SUPINE,
    'ALLFOURS': ALLFOURS, 'KNEEL': KNEEL, 'SIT': SIT,
    'SIDELIE': SIDELIE, 'OVER': OVER, 'CARRY': CARRY,
    'INVERT': INVERT, 'OVER_BACK': OVER_BACK,
}

# ─── シーン合成 ──────────────────────────────────
def build_svg(placements):
    """
    placements = list of [prim_name, long(0/1), args(list), ox, oy, flip]
    → SVG の <rect>+パーツを返す（viewBox="0 0 200 200" 用）
    """
    parts = ['<rect x="0" y="0" width="200" height="200" fill="#fff"/>']
    for pl in placements:
        prim, long, args, ox, oy, flip = pl
        fig = PRIMS[prim](bool(long), *args)
        parts.append(emit(fig, ox, oy, flip))
    return "".join(parts)

# ─── レシピ短縮ヘルパー ──────────────────────────
def _pl(prim, long, args, x, y, f=1):
    return [prim, long, args, x, y, f]

def mission(legs='bent', oa='straight', ol='kneel'):
    return [_pl('SUPINE',1,[legs,'rest'],56,152), _pl('OVER',0,[oa,ol],118,128)]

def rear_af(arms='hold', lean=0):
    return [_pl('ALLFOURS',1,[],68,152), _pl('KNEEL',0,[arms,lean],130,152,-1)]

def rear_stand():
    return [_pl('STANDBEND',1,['hang'],74,98), _pl('STAND',0,['stride','hold'],120,80,-1)]

def cowgirl(la='hold', face=1, sl='wide'):
    return [_pl('SUPINE',0,['bent','rest'],56,154), _pl('SIT',1,[sl,la],102,96,face)]

def face_sit(la='cross', lb='cross'):
    return [_pl('SIT',1,[la,'hug'],80,120), _pl('SIT',0,[lb,'hug'],122,120,-1)]

def side(kn='bent', flip2=1):
    return [_pl('SIDELIE',1,[kn],56,152), _pl('SIDELIE',0,[kn],102,152,flip2)]

def standing(la='hug', lb='hug'):
    return [_pl('STAND',1,['together',la],84,72), _pl('STAND',0,['spread',lb],116,66,-1)]

def carry_pl():
    return [_pl('STAND',0,['wide','reach'],124,74,-1), _pl('CARRY',1,[],98,112)]

def sixtynine():
    return [_pl('SUPINE',1,['straight','rest'],50,84), _pl('SUPINE',0,['straight','rest'],152,120,-1)]

def matsuba(lean=8):
    return [_pl('SUPINE',1,['spread','rest'],58,152), _pl('KNEEL',0,['hold',lean],122,152,-1)]

def lotus_carry():
    return [_pl('SIT',0,['cross','back'],118,128), _pl('CARRY',1,[],94,110)]

def invert_pair():
    return [_pl('INVERT',1,[],76,152), _pl('KNEEL',0,['hold'],118,152,-1)]

def prone():
    return [_pl('SUPINE',1,['straight','rest'],58,154), _pl('OVER',0,['ext','ext'],122,136)]

# ─── データセット ─────────────────────────────────
FM  = '対面・正常位系'
RR  = '後背位系'
CW  = '騎乗位系'
SI  = '座位系'
SD  = '側位系'
ST  = '立位系'
OR  = '口唇系'
AC  = 'アクロバット系'

FAM_DESC = {
    FM: '向かい合う対面型。仰向けの相手に上から重なる、正常位を基本とする体位です。',
    RR: '後ろから重なる後背位型。四つん這いや前傾姿勢が特徴で、世界各地で古くから知られています。',
    CW: '仰向けの相手に上からまたがる騎乗位型。上になる側が動きを主導する体位です。',
    SI: '向かい合って、または重なって座る座位型。密着しやすくゆったり行える体位です。',
    SD: '二人とも横向きに寝そべる側位型。体への負担が少なくリラックスして行えます。',
    ST: '立った姿勢で行う立位型。支え合ったり抱え上げたりするダイナミックな体位です。',
    OR: '頭と足の向きを工夫して向き合う体位。互いの配置が特徴的です。',
    AC: '逆さや反り、ねじりを伴うアクロバティックな体位。柔軟性を要する上級型です。',
}

DATASET = [
    # ── 対面・正常位系 ──
    ("正常位",       "ミッショナリー",       FM, mission('bent')),
    ("屈曲位",       "ベンディング",          FM, mission('raised')),
    ("開脚位",       "スプレッド・イーグル",  FM, mission('spread')),
    ("伸長位",       "ストレッチ",            FM, mission('straight','elbow','ext')),
    ("種付けプレス", "メイティング・プレス",  FM, mission('overhead')),
    ("抱擁位",       "コイタル・アライメント",FM, mission('bent','elbow')),
    ("M字開脚位",    "Mレッグ",               FM, mission('spread','elbow','kneel')),
    ("深屈曲位",     "ディープ・ベンディング",FM, mission('overhead','elbow')),
    ("バタフライ",   "蝶々",                  FM, mir(mission('raised','elbow','ext'))),
    ("仏壇返し",     "ぶつだんがえし",        FM, mission('overhead','straight','ext')),
    ("揚羽返し",     "あげはがえし",          FM, mir(mission('overhead','elbow','kneel'))),
    ("だるま返し",   "だるまがえし",          FM, mission('overhead','elbow','ext')),
    ("理非知らず",   "りひしらず",            FM, mir(mission('spread','straight','ext'))),
    ("乱れ牡丹",     "みだれぼたん",          FM, mir(mission('spread','elbow','kneel'))),
    ("百閉",         "ひゃくとじ",            FM, mission('straight','elbow','kneel')),
    ("正常位（逆）", "ミラー・ミッショナリー",FM, mir(mission('bent'))),
    ("本手",         "ほんて",                FM, mission('bent','straight','ext')),
    ("クレイドル",   "ゆりかご位",            FM, mission('bent','straight','kneel')),
    ("浮き橋",       "うきはし",              FM, mir(mission('raised','straight','kneel'))),
    ("交差位",       "クロスド",              FM, mir(mission('spread','straight','kneel'))),
    ("本駒掛け",     "ほんこまがけ",          FM, mir(mission('bent','elbow','kneel'))),
    ("燕返し",       "つばめがえし",          FM, mission('overhead','straight','kneel')),
    ("松葉崩し",     "まつばくずし",          FM, matsuba(8)),
    ("松葉崩し（逆）","まつばくずし逆",       FM, mir(matsuba(8))),
    ("ランジ",       "ザ・ランジ",            FM, mission('raised','straight','ext')),
    ("コアラ",       "抱きつき正常位",        FM, mission('bent','elbow','kneel')),
    ("撞木反り",     "しゅもくぞり",          FM, mir(mission('raised','elbow','kneel'))),
    ("コンパス",     "コンパス位",            FM, [_pl('SUPINE',1,['raised','rest'],56,152),
                                                    _pl('KNEEL',0,['hold',12],122,152,-1)]),

    # ── 後背位系 ──
    ("後背位",       "ドギースタイル",        RR, rear_af('hold')),
    ("後背位（逆）", "ドギー逆向き",          RR, mir(rear_af('hold'))),
    ("寝バック",     "プローン・バック",       RR, prone()),
    ("寝バック（逆）","プローン逆向き",        RR, mir(prone())),
    ("立ちバック",   "スタンディング・リア",  RR, rear_stand()),
    ("立ちバック（逆）","スタンディング逆",   RR, mir(rear_stand())),
    ("帆掛茶臼",     "ほかけちゃうす",        RR, mir(rear_af('reach'))),
    ("流鏑馬",       "やぶさめ",              RR, [_pl('ALLFOURS',1,[],68,152), _pl('KNEEL',0,['down',6],130,152,-1)]),
    ("尻上げ後背位", "レイズド・ドギー",      RR, [_pl('ALLFOURS',1,[],68,152), _pl('KNEEL',0,['hold',10],130,152,-1)]),
    ("押し車",       "ウィールバロー",        RR, [_pl('OVER',1,['straight','ext'],64,152), _pl('STAND',0,['stride','hold'],128,98,-1)]),
    ("側面後背位",   "スプーン・バック",      RR, [_pl('SIDELIE',1,['straight'],58,152), _pl('SIDELIE',0,['straight'],106,152)]),

    # ── 騎乗位系 ──
    ("騎乗位",       "カウガール",            CW, cowgirl('hold',1)),
    ("騎乗位（前傾）","リーニング・カウガール",CW, cowgirl('knee',1)),
    ("背面騎乗位",   "リバース・カウガール",  CW, cowgirl('back',-1,'wide')),
    ("背面騎乗位（前傾）","リバース・リーニング",CW, cowgirl('knee',-1,'forward')),
    ("しゃがみ騎乗位","スクワット・ライド",   CW, [_pl('SUPINE',0,['bent','rest'],56,154), _pl('SIT',1,['bentknee','knee'],102,98)]),
    ("しゃがみ騎乗位（逆）","スクワット逆",   CW, mir([_pl('SUPINE',0,['bent','rest'],56,154), _pl('SIT',1,['bentknee','knee'],102,98)])),
    ("茶臼",         "ちゃうす",              CW, cowgirl('hold',1,'forward')),
    ("時雨茶臼",     "しぐれちゃうす",        CW, cowgirl('back',-1,'forward')),
    ("御所車",       "ごしょぐるま",          CW, cowgirl('hold',-1,'wide')),
    ("月見茶臼",     "つきみちゃうす",        CW, mir(cowgirl('back',-1,'wide'))),
    ("鵯越え",       "ひよどりごえ",          CW, mir(cowgirl('knee',1,'wide'))),
    ("帆掛け騎乗",   "セイルライド",          CW, cowgirl('knee',1,'forward')),
    ("含み茶臼",     "ふくみちゃうす",        CW, cowgirl('back',1,'forward')),
    ("ワイルドライド","奔馬",                  CW, cowgirl('knee',-1,'wide')),
    ("撞木茶臼",     "しゅもくちゃうす",      CW, mir(cowgirl('back',1,'wide'))),
    ("唐草居茶臼",   "からくさいちゃうす",    CW, mir(cowgirl('hold',1,'forward'))),

    # ── 座位系 ──
    ("対面座位",     "ロータス",              SI, face_sit()),
    ("蓮華座",       "パドマーサナ",          SI, face_sit('folded','folded')),
    ("対面座位（脚絡み）","エンタングル",     SI, [_pl('SIT',1,['forward','hug'],82,120), _pl('SIT',0,['forward','hug'],122,120,-1)]),
    ("背面座位",     "リバース・シーテッド",  SI, lotus_carry()),
    ("背面座位（逆）","リバース逆",           SI, mir(lotus_carry())),
    ("抱き地蔵",     "だきじぞう",            SI, [_pl('SIT',0,['cross','back'],112,128), _pl('CARRY',1,[],92,112)]),
    ("宝船",         "たからぶね",            SI, [_pl('SIT',1,['forward','back'],80,122), _pl('SIT',0,['forward','hold'],122,122,-1)]),
    ("椅子対面位",   "チェア・フェイシング",  SI, [_pl('SIT',1,['bentknee','hug'],82,120), _pl('SIT',0,['bentknee','hug'],122,120,-1)]),
    ("二つ巴",       "ふたつどもえ",          SI, mir(face_sit())),
    ("火燵隠れ",     "こたつがくれ",          SI, [_pl('SIT',1,['cross','hug'],84,122), _pl('SIT',0,['cross','hug'],120,122,-1)]),

    # ── 側位系 ──
    ("側位",         "スプーン",              SD, side('bent')),
    ("側位（逆向き）","スプーン逆",           SD, mir(side('bent'))),
    ("シザーズ",     "はさみ",               SD, side('straight')),
    ("シザーズ（逆）","はさみ逆",             SD, mir(side('straight'))),
    ("抱き合い側位", "フェイシング・スプーン",SD, side('bent', -1)),
    ("鴛鴦",         "えんおう",              SD, side('curl')),
    ("千鳥",         "ちどり",               SD, mir(side('curl'))),
    ("鳴門",         "なると",               SD, [_pl('SIDELIE',1,['curl'],58,152), _pl('SIDELIE',0,['bent'],104,152,-1)]),
    ("椋鳥",         "むくどり",             SD, [_pl('SIDELIE',1,['curl'],58,152), _pl('SIDELIE',0,['straight'],104,152)]),
    ("千鳥の曲",     "ちどりのきょく",        SD, mir([_pl('SIDELIE',1,['bent'],58,152), _pl('SIDELIE',0,['curl'],104,152,-1)])),
    ("鶺鴒",         "せきれい",             SD, [_pl('SIDELIE',1,['wide'],58,152), _pl('SIDELIE',0,['bent'],106,152)]),
    ("ランプ",       "横たわり位",           SD, [_pl('SIDELIE',1,['bent'],58,152), _pl('SIDELIE',0,['straight'],106,152,-1)]),

    # ── 立位系 ──
    ("立位",         "スタンディング",        ST, standing()),
    ("立位（逆）",   "スタンディング逆",      ST, mir(standing())),
    ("立ち花菱",     "たちはなびし",          ST, standing('up','hug')),
    ("壁面立位",     "ウォール・フェイス",    ST, standing('reach','reach')),
    ("帆柱",         "ほばしら",              ST, mir(standing('up','hug'))),
    ("駅弁",         "ピックアップ",          ST, carry_pl()),
    ("駅弁（逆）",   "ピックアップ逆",        ST, mir(carry_pl())),
    ("立ち松葉",     "スタンド・スプリット",  ST, [_pl('STAND',1,['oneup','hold'],86,74), _pl('STAND',0,['spread','hold'],118,70,-1)]),
    ("背面立位",     "リア・スタンド",        ST, [_pl('STAND',1,['stride','reach'],82,74), _pl('STAND',0,['stride','hold'],118,70)]),
    ("抱え上げ対面", "リフト・フェイシング",  ST, [_pl('STAND',0,['wide','reach'],122,72), _pl('CARRY',1,[],98,112)]),
    ("リバースリフト","背面抱え",             ST, mir([_pl('STAND',0,['wide','reach'],122,72), _pl('CARRY',1,[],98,112)])),

    # ── 口唇系 ──
    ("シックスナイン","69",                   OR, sixtynine()),
    ("シックスナイン（逆）","69逆",           OR, mir(sixtynine())),
    ("対面口唇",     "フェイス・シット",      OR, [_pl('SUPINE',1,['bent','rest'],56,152), _pl('KNEEL',0,['hold',6],120,152,-1)]),
    ("対面口唇（逆）","フェイス・シット逆",   OR, mir([_pl('SUPINE',1,['bent','rest'],56,152), _pl('KNEEL',0,['hold',6],120,152,-1)])),
    ("スタンディング69","立ち69",             OR, [_pl('STAND',1,['together','reach'],90,82), _pl('INVERT',0,[],110,152,-1)]),

    # ── アクロバット系 ──
    ("逆さ位",       "インバーテッド",        AC, invert_pair()),
    ("逆さ位（逆）", "インバーテッド逆",      AC, mir(invert_pair())),
    ("肩立ち位",     "ショルダースタンド",    AC, [_pl('INVERT',1,[],74,152), _pl('STAND',0,['stride','down'],124,98,-1)]),
    ("ブリッジ位",   "ブリッジ",              AC, [_pl('SUPINE',1,['overhead','up'],60,152), _pl('KNEEL',0,['hold',4],120,152,-1)]),
    ("プレッツェル", "ねじり位",              AC, [_pl('SIDELIE',1,['bent'],60,152), _pl('KNEEL',0,['hold',8],118,152,-1)]),
    ("ゴールデンアーチ","アーチ位",           AC, [_pl('SUPINE',1,['overhead','up'],60,152), _pl('STAND',0,['stride','down'],130,98,-1)]),
    ("アコーディオン","折り畳み位",           AC, cowgirl('knee',-1,'forward')),
    ("スプリットレベル","段差位",             AC, mir(cowgirl('hold',-1,'forward'))),

    # ── 追加分（150体位化） ──
    # 対面・正常位系
    ("正常位（深め）",   "ディープ・ミッショナリー", FM, mission('overhead','straight','kneel')),
    ("足上げ抱え",       "レッグ・ホールド",     FM, mir(mission('raised','elbow','kneel'))),
    ("水入らず",         "みずいらず",           FM, mission('bent','elbow','ext')),
    ("時計仕掛け",       "クロックワーク",       FM, mir(mission('straight','straight','kneel'))),
    ("抱え込み正常位",   "ニーフック",           FM, mission('raised','elbow','kneel')),
    ("流し込み",         "ながしこみ",           FM, mir(mission('overhead','straight','kneel'))),
    ("満月",             "フルムーン",           FM, mir(mission('spread','elbow','ext'))),
    ("乱れ松葉",         "みだれまつば",         FM, mir(matsuba(14))),
    ("深押し松葉",       "ディープ松葉",         FM, matsuba(16)),
    ("抱き柏",           "だきかしわ",           FM, mission('bent','straight','kneel')),

    # 後背位系
    ("立ちバック（深）", "ディープ・リア",       RR, [_pl('STANDBEND',1,['flat'],74,98), _pl('STAND',0,['wide','hold'],120,80,-1)]),
    ("寝バック（深）",   "プローン・ディープ",    RR, [_pl('SUPINE',1,['straight','rest'],58,154), _pl('OVER',0,['elbow','ext'],122,138)]),
    ("後ろ抱え",         "リア・ホールド",       RR, mir([_pl('ALLFOURS',1,[],68,152), _pl('KNEEL',0,['hug',8],130,152,-1)])),
    ("逆さ後背位",       "リバース・ドギー",      RR, [_pl('ALLFOURS',1,[],70,152), _pl('STANDBEND',0,['hang'],128,98,-1)]),
    ("飛び込み後背位",   "ダイブ・バック",       RR, mir([_pl('OVER',1,['straight','ext'],64,152), _pl('STAND',0,['wide','hold'],128,98,-1)])),
    ("膝つき立ちバック", "ハーフ・スタンド・リア", RR, mir(rear_af('hug', 6))),
    ("猫のポーズ",       "キャット",             RR, rear_af('reach')),

    # 騎乗位系
    ("逆さ茶臼",         "リバース茶臼",          CW, mir(cowgirl('back',1,'forward'))),
    ("立て膝騎乗",       "ニーリング・ライド",    CW, [_pl('SUPINE',0,['bent','rest'],56,154), _pl('SIT',1,['bentknee','back'],102,98,-1)]),
    ("深座り騎乗",       "ディープ・スクワット",  CW, [_pl('SUPINE',0,['bent','rest'],56,154), _pl('SIT',1,['folded','knee'],102,98)]),
    ("船遊び",           "ふなあそび",            CW, cowgirl('back',1,'wide')),
    ("帆上げ茶臼",       "ほあげちゃうす",        CW, mir(cowgirl('knee',1,'forward'))),
    ("鶯茶臼",           "うぐいすちゃうす",      CW, cowgirl('hold',-1,'forward')),
    ("乱れ茶臼",         "みだれちゃうす",        CW, mir(cowgirl('knee',-1,'wide'))),
    ("立ち茶臼",         "たちちゃうす",          CW, cowgirl('hold',1,'wide')),

    # 座位系
    ("対面抱え座位",     "ラップ・シット",        SI, [_pl('SIT',0,['cross','back'],116,128), _pl('CARRY',1,[],94,108)]),
    ("胡座対面",         "あぐらたいめん",        SI, face_sit('cross','folded')),
    ("膝乗せ座位",       "ニー・ラップ",          SI, [_pl('SIT',1,['bentknee','hug'],82,122), _pl('SIT',0,['folded','hug'],122,122,-1)]),
    ("背中合わせ座位",   "バック・トゥ・バック",  SI, [_pl('SIT',1,['forward','back'],82,122), _pl('SIT',0,['forward','back'],122,122)]),
    ("揺り椅子",         "ロッキング・チェア",    SI, mir(lotus_carry())),
    ("蓮の戯れ",         "ロータス・プレイ",      SI, face_sit('folded','cross')),
    ("抱き合い座位",     "エンブレース・シット",  SI, [_pl('SIT',1,['cross','hug'],84,122), _pl('SIT',0,['folded','hug'],120,122,-1)]),

    # 側位系
    ("深スプーン",       "ディープ・スプーン",    SD, [_pl('SIDELIE',1,['curl'],56,152), _pl('SIDELIE',0,['bent'],100,152)]),
    ("抱き枕側位",       "ボルスター",            SD, side('wide')),
    ("交差側位",         "クロス・スプーン",      SD, [_pl('SIDELIE',1,['bent'],58,152), _pl('SIDELIE',0,['wide'],104,152,-1)]),
    ("半身側位",         "ハーフ・サイド",        SD, mir([_pl('SIDELIE',1,['straight'],58,152), _pl('SIDELIE',0,['curl'],104,152)])),
    ("浮舟",             "うきふね",              SD, [_pl('SIDELIE',1,['wide'],58,152), _pl('SIDELIE',0,['straight'],106,152,-1)]),

    # 立位系
    ("立位（抱き上げ）", "スタンディング・リフト", ST, mir(carry_pl())),
    ("壁立ちバック",     "ウォール・リア",        ST, [_pl('STANDBEND',1,['hang'],84,98), _pl('STAND',0,['together','hold'],116,80,-1)]),
    ("片足立位",         "ワンレッグ・スタンド",  ST, mir([_pl('STAND',1,['oneup','hold'],84,74), _pl('STAND',0,['stride','hug'],118,70,-1)])),
    ("抱き合い立位",     "エンブレース・スタンド", ST, standing('hug','reach')),
    ("背面立ち抱え",     "リア・リフト",          ST, [_pl('STANDBEND',1,['flat'],84,98), _pl('STAND',0,['wide','reach'],118,80,-1)]),

    # 口唇系
    ("立ち対面口唇",     "スタンド・オーラル",    OR, [_pl('STAND',1,['together','down'],86,82), _pl('KNEEL',0,['hug'],116,152,-1)]),
    ("膝つき口唇",       "ニール・オーラル",      OR, mir([_pl('STAND',1,['together','down'],86,82), _pl('KNEEL',0,['hug'],116,152,-1)])),
    ("横向き69",         "サイド69",             OR, [_pl('SIDELIE',1,['straight'],56,150), _pl('SIDELIE',0,['straight'],104,150,-1)]),

    # アクロバット系
    ("立ち逆さ",         "スタンド・インバート",  AC, mir([_pl('INVERT',1,[],74,152), _pl('STAND',0,['stride','down'],124,98,-1)])),
    ("車輪",             "ホイール",              AC, [_pl('SUPINE',1,['overhead','up'],58,152), _pl('OVER',0,['straight','ext'],122,118)]),
    ("ねじり後背",       "ツイスト・リア",        AC, mir([_pl('SIDELIE',1,['wide'],60,152), _pl('KNEEL',0,['hold',8],118,152,-1)])),
    ("空中ブランコ",     "トラピーズ",            AC, [_pl('STAND',0,['wide','reach'],126,74), _pl('INVERT',1,[],96,150)]),
]

# ─── 重複チェック ─────────────────────────────────
def check_dupes():
    names = [d[0] for d in DATASET]
    dupes = [n for n in names if names.count(n) > 1]
    if dupes:
        print("WARNING: duplicate names:", set(dupes), file=sys.stderr)
check_dupes()

# ─── シート生成（検証用） ────────────────────────
def make_sheet(items, path, cols=4):
    rows = (len(items) + cols - 1) // cols
    cell = 200
    tiles = ''
    for i, (nm, aka, fam, pl) in enumerate(items):
        x = (i % cols) * cell
        y = (i // cols) * cell
        body = build_svg(pl)
        tiles += (
            f'<g transform="translate({x},{y})"><rect width="200" height="200"'
            f' fill="#fff" stroke="#ddd"/>{body}'
            f'<text x="100" y="194" font-size="11" text-anchor="middle"'
            f' font-family="sans-serif" fill="#333">{nm}</text></g>'
        )
    sheet = (f'<svg viewBox="0 0 {cols*cell} {rows*cell}"'
             f' xmlns="http://www.w3.org/2000/svg">{tiles}</svg>')
    cairosvg.svg2png(
        bytestring=sheet.encode(), write_to=path,
        output_width=cols*cell*2, output_height=rows*cell*2,
        background_color='white'
    )

# ─── positions.js 生成 ───────────────────────────
def build_positions_js():
    def esc(s):
        return s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    out = 'const POSITIONS = [\n'
    for nm, aka, fam, pl in DATASET:
        body = build_svg(pl)
        desc = FAM_DESC[fam]
        out += '  {\n'
        out += f'    name: `{esc(nm)}`,\n'
        out += f'    aka: `{esc(aka)}`,\n'
        out += f'    family: `{esc(fam)}`,\n'
        out += f'    desc: `{esc(desc)}`,\n'
        out += f'    svg: `{body}`\n'
        out += '  },\n'
    out += '];\n'
    return out

if __name__ == '__main__':
    import os
    # 検証シート
    os.makedirs('/tmp/sheets', exist_ok=True)
    for bi in range(0, len(DATASET), 16):
        make_sheet(DATASET[bi:bi+16], f'/tmp/sheets/s{bi//16:02d}.png')
    print(f"Generated {len(DATASET)} positions across {(len(DATASET)+15)//16} sheets.")
    # positions.js
    js = build_positions_js()
    open('/tmp/positions.js', 'w').write(js)
    print(f"positions.js: {len(js)} chars")
