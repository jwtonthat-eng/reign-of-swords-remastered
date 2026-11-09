#!/usr/bin/env python3
"""Draw the bonus-campaign unit art (Tilicia & Isoluccia) from scratch.

These six units are NOT from the original games: they are fan-made, drawn in code by this script (a small limb rig,
shaded shapes and hand-placed pixels). Nothing is copied from the original sprite sheets; only their palette,
proportions and frame layout were matched so the new units sit beside the old ones.

    python3 tools/ros/bonus/draw_units.py        (from the repo root; deterministic)

Writes, under public/games/reign-of-swords/:
    sprites/<key>.png         attack strip, 72x72 frames, facing right
    sprites/stand/<key>.png   one idle frame, cropped
    sprites/walk/<key>.png    4 walk frames, 64x72 each
    hud/skill_<name>.png      six 52x52 ability icons
and the preview sheet docs/images/bonus-units.png.

Cloth is painted in the game's two key ramps (greens = the army's first heraldry colour, blues = its second), which
the engine re-palettises per army (render.js _recolored) -- so those pixels must be exact.
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OUT = os.path.join(ROOT, "public", "games", "reign-of-swords")


def rgb(h, a=255):
    return ((h >> 16) & 255, (h >> 8) & 255, h & 255, a)


def ramp(*hs):
    return tuple(rgb(h) for h in hs)


BLACK = rgb(0x000000)
# (dark, mid, light)
GREEN = ramp(0x007800, 0x00A606, 0x00D40B)  # key ramp 1 -- exact
BLUE = ramp(0x00008C, 0x000BC6, 0x0015FF)  # key ramp 2 -- exact
SKIN = ramp(0x855236, 0xB6836A, 0xC59C7D)
STEEL = ramp(0x535353, 0x988E89, 0xD8D8D8)
DSTEEL = ramp(0x404040, 0x706663, 0xA1A1A1)
LEATHER = ramp(0x4F3128, 0x784A3C, 0xA67247)
BOOT = ramp(0x3A2630, 0x5D3A48, 0x855236)
WOOD = ramp(0x5B3A1E, 0x855236, 0xA67247)
GOLD = ramp(0xA26B3F, 0xCBA653, 0xF7E96D)
FUR = ramp(0x4A3A2A, 0x7D6648, 0xAB966C)
STONE = ramp(0x4B443C, 0x7A6F60, 0xA59A86)
DSTONE = ramp(0x37322C, 0x5C5348, 0x857A69)
TAN = ramp(0x6F6045, 0x92805A, 0xB6A67B)
LINEN = ramp(0x988E89, 0xC0B7AF, 0xE8DFD5)
RED = ramp(0x6E1414, 0xA32020, 0xD23A2E)
GLOW = ramp(0x1A878F, 0x5FE0EA, 0xD8FFFF)
DARK = ramp(0x1C1C24, 0x2A2A3E, 0x383852)


def vec(a, l=1.0):
    """Angle in degrees: 0 = down, 90 = forward (right), 180 = up."""
    r = math.radians(a)
    return (math.sin(r) * l, math.cos(r) * l)


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def shift(m, dx, dy):
    out = np.zeros_like(m)
    h, w = m.shape
    xs0, xs1 = max(0, -dx), min(w, w - dx)
    ys0, ys1 = max(0, -dy), min(h, h - dy)
    out[ys0 + dy : ys1 + dy, xs0 + dx : xs1 + dx] = m[ys0:ys1, xs0:xs1]
    return out


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.a = np.zeros((h, w, 4), np.uint8)

    # -- shape masks --------------------------------------------------
    def _m(self):
        im = Image.new("L", (self.w, self.h), 0)
        return im, ImageDraw.Draw(im)

    def capsule(self, p0, p1, r):
        im, d = self._m()
        d.line([p0, p1], fill=255, width=max(1, int(round(r * 2))))
        for p in (p0, p1):
            d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=255)
        return np.array(im) > 0

    def ellipse(self, c, rx, ry):
        im, d = self._m()
        d.ellipse([c[0] - rx, c[1] - ry, c[0] + rx, c[1] + ry], fill=255)
        return np.array(im) > 0

    def poly(self, pts):
        im, d = self._m()
        d.polygon([(round(x), round(y)) for x, y in pts], fill=255)
        return np.array(im) > 0

    def line(self, p0, p1, w=1):
        im, d = self._m()
        d.line([p0, p1], fill=255, width=w)
        return np.array(im) > 0

    def rect(self, x0, y0, x1, y1):
        im, d = self._m()
        d.rectangle([round(x0), round(y0), round(x1), round(y1)], fill=255)
        return np.array(im) > 0

    # -- painting -----------------------------------------------------
    def put(self, m, rp, outline=True, band=1):
        """Paint mask m with a 3-shade ramp: dark on the left / bottom rim, light on the right / top rim."""
        if not m.any():
            return
        if outline:
            o = (shift(m, 1, 0) | shift(m, -1, 0) | shift(m, 0, 1) | shift(m, 0, -1)) & ~m
            self.a[o] = BLACK
        self.a[m] = rp[1]
        dark = m & ~(shift(m, band, 0) & shift(m, 0, -1))
        light = m & ~(shift(m, -1, 0) & shift(m, 0, 1)) & ~dark
        self.a[dark] = rp[0]
        self.a[light] = rp[2]

    def flat(self, m, col):
        self.a[m] = col

    def px(self, x, y, col):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = col

    def fx(self, m, col):
        """Alpha-over an effect colour (weapon swoosh, lightning glow)."""
        a = col[3] / 255.0
        src = np.array(col[:3], float)
        dst = self.a[m].astype(float)
        da = dst[:, 3:4] / 255.0
        oa = a + da * (1 - a)
        orgb = (src * a + dst[:, :3] * da * (1 - a)) / np.maximum(oa, 1e-6)
        self.a[m] = np.concatenate([orgb, oa * 255], axis=1).round().astype(np.uint8)

    def image(self):
        return Image.fromarray(self.a, "RGBA")


# ---------------------------------------------------------------------------------------------------------------
# The rig
# ---------------------------------------------------------------------------------------------------------------
BODY = dict(thigh=13, shin=13, torso=19, ua=10, fa=10, limb=3.0, arm=2.5, tw=6.0, hip=5.0, head=(4.8, 5.6), foot=6)

BASE_POSE = dict(
    lean=4,  # torso lean, + = forward
    crouch=1,  # hip drop
    nf=(5, 0),  # near (front-drawn) foot: (x offset from hip, lift)
    ff=(-5, 0),  # far foot
    na=(20, 70),  # near arm: (upper angle, forearm angle)
    fa=(-10, 40),  # far arm
    wa=150,  # weapon angle
    dx=0,
)


def ik(h, f, a, b, fwd=1):
    dx, dy = f[0] - h[0], f[1] - h[1]
    d = max(0.01, min(math.hypot(dx, dy), a + b - 0.01))
    ux, uy = dx / math.hypot(dx, dy), dy / math.hypot(dx, dy)
    t = (a * a - b * b + d * d) / (2 * d)
    hh = math.sqrt(max(0.0, a * a - t * t))
    px, py = -uy, ux
    if px * fwd < 0:
        px, py = -px, -py
    return (h[0] + ux * t + px * hh, h[1] + uy * t + py * hh)


def joints(B, P, ox, ground):
    leg = (B["thigh"] + B["shin"]) * 0.98
    hip = (ox + P["dx"], ground - 3 - leg + P["crouch"])
    J = {"hip": hip, "ground": ground}
    for k, off in (("n", 1.5), ("f", -1.5)):
        h = (hip[0] + off, hip[1])
        fx_, lift = P[k + "f"]
        ank = (hip[0] + fx_, ground - 3 - lift)
        J[k + "hip"], J[k + "ank"] = h, ank
        J[k + "knee"] = ik(h, ank, B["thigh"], B["shin"])
    up = vec(180 - P["lean"], B["torso"])
    neck = add(hip, up)
    J["neck"] = neck
    hr = B["head"]
    J["head"] = add(neck, add(vec(180 - P["lean"], hr[1] + 0.5), (1, 0)))
    for k, off in (("n", 1.0), ("f", -1.0)):
        sh = (neck[0] + off - 0.5, neck[1] + 3)
        ua, fa = P[k + "a"]
        el = add(sh, vec(ua, B["ua"]))
        J[k + "sh"], J[k + "el"], J[k + "hand"] = sh, el, add(el, vec(fa, B["fa"]))
    return J


def draw_leg(cv, B, U, J, k):
    hipp, knee, ank = J[k + "hip"], J[k + "knee"], J[k + "ank"]
    cv.put(cv.capsule(hipp, knee, B["limb"] + 0.4), U["thigh"])
    cv.put(cv.capsule(knee, ank, B["limb"]), U["shin"])
    f = B["foot"]
    cv.put(cv.poly([(ank[0] - 2.5, ank[1] - 1), (ank[0] + f, ank[1] + 1), (ank[0] + f, ank[1] + 3), (ank[0] - 2.5, ank[1] + 3)]), U["boot"])


def draw_arm(cv, B, U, J, k):
    sh, el, hand = J[k + "sh"], J[k + "el"], J[k + "hand"]
    cv.put(cv.capsule(sh, el, B["arm"] + 0.4), U["sleeve"])
    cv.put(cv.capsule(el, hand, B["arm"]), U["forearm"])
    cv.put(cv.ellipse(hand, 2.2, 2.2), U.get("hand", SKIN))


def draw_torso(cv, B, U, J):
    hip, neck = J["hip"], J["neck"]
    tw, hw = B["tw"], B["hip"]
    cv.put(
        cv.poly([(neck[0] - tw, neck[1] + 1), (neck[0] + tw, neck[1] + 1), (hip[0] + hw, hip[1] + 2), (hip[0] - hw, hip[1] + 2)]),
        U["torso"],
        band=2,
    )


def shadow(cv, ox, ground, rx=17):
    m = cv.ellipse((ox, ground - 2), rx, 2.5)
    cv.flat(m, BLACK)


def figure(U, pose, w=72, ox=None, ground=71):
    B = dict(BODY, **U.get("body", {}))
    P = dict(BASE_POSE, **U.get("pose", {}))
    P.update(pose)
    cv = Canvas(w, 72)
    ox = (w // 2 - 2) if ox is None else ox
    J = joints(B, P, ox, ground)
    J["P"], J["B"] = P, B
    g = U["gear"]
    shadow(cv, ox + P["dx"], ground, U.get("shadow", 15))
    g("behind", cv, J)
    draw_arm(cv, B, U, J, "f")
    g("farhand", cv, J)
    draw_leg(cv, B, U, J, "f")
    draw_leg(cv, B, U, J, "n")
    draw_torso(cv, B, U, J)
    g("torso", cv, J)
    g("head", cv, J)
    g("mid", cv, J)
    if not P.get("hide_near"):
        g("weapon_under", cv, J)
        draw_arm(cv, B, U, J, "n")
    g("front", cv, J)
    return cv


# ---------------------------------------------------------------------------------------------------------------
# Shared gear pieces
# ---------------------------------------------------------------------------------------------------------------
def face(cv, J, rp=SKIN):
    c, (rx, ry) = J["head"], J["B"]["head"]
    cv.put(cv.ellipse(c, rx, ry), rp)
    cv.px(c[0] + 2, c[1] - 1, rgb(0x2A1A14))  # eye
    cv.px(c[0] + rx, c[1] + 1, rp[1])  # nose


def blade(cv, hand, ang, length, w=1.6, rp=STEEL, tip=True):
    d = vec(ang)
    n = (-d[1], d[0])
    base, end = hand, add(hand, (d[0] * length, d[1] * length))
    pts = [(base[0] + n[0] * w, base[1] + n[1] * w), (base[0] - n[0] * w, base[1] - n[1] * w)]
    if tip:
        pts += [(end[0] - n[0] * 0.3, end[1] - n[1] * 0.3), (end[0] + n[0] * 0.3, end[1] + n[1] * 0.3)]
    else:
        pts += [(end[0] - n[0] * w, end[1] - n[1] * w), (end[0] + n[0] * w, end[1] + n[1] * w)]
    cv.put(cv.poly(pts), rp)
    return end


def shaft(cv, p0, ang, back, fwd, rp=WOOD, w=2):
    a, b = add(p0, vec(ang, -back)), add(p0, vec(ang, fwd))
    cv.put(cv.line(a, b, w), rp)
    return a, b


def spearhead(cv, p, ang, l=6, rp=STEEL):
    d = vec(ang)
    n = (-d[1], d[0])
    cv.put(cv.poly([(p[0] + n[0] * 2, p[1] + n[1] * 2), (p[0] - n[0] * 2, p[1] - n[1] * 2), (p[0] + d[0] * l, p[1] + d[1] * l)]), rp)


def swoosh(cv, c, r0, r1, a0, a1, col=rgb(0xD8ECEE, 170)):
    """A weapon trail: an annulus slice around c from angle a0 to a1 (same angle convention as vec)."""
    pts = []
    steps = 14
    for i in range(steps + 1):
        a = a0 + (a1 - a0) * i / steps
        rr = r1 - (r1 - r0) * (i / steps) * 0.0
        pts.append(add(c, vec(a, rr)))
    for i in range(steps, -1, -1):
        a = a0 + (a1 - a0) * i / steps
        t = i / steps
        pts.append(add(c, vec(a, r0 + (r1 - r0) * (1 - t) * 0.15)))
    m = cv.poly(pts)
    cv.fx(m, col)
    edge = cv.poly(pts[: steps + 1] + [add(c, vec(a0 + (a1 - a0) * i / steps, r1 - 1.6)) for i in range(steps, -1, -1)])
    cv.fx(edge & m, rgb(0xFCFCFC, 230))


def bolt_zigzag(cv, p0, p1, seed=0, w=1, jit=3.0):
    """A lightning zigzag from p0 to p1 (deterministic jitter)."""
    n = max(3, int(math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / 5))
    pts = [p0]
    for i in range(1, n):
        t = i / n
        j = math.sin(seed * 12.9898 + i * 78.233) * jit
        pts.append((p0[0] + (p1[0] - p0[0]) * t - j * 0.5, p0[1] + (p1[1] - p0[1]) * t + j))
    pts.append(p1)
    for a, b in zip(pts, pts[1:]):
        cv.fx(cv.line(a, b, w + 2), rgb(0x5FE0EA, 150))
    for a, b in zip(pts, pts[1:]):
        cv.flat(cv.line(a, b, w), rgb(0xFCFFFF))


# ---------------------------------------------------------------------------------------------------------------
# The six units
# ---------------------------------------------------------------------------------------------------------------
def javelin(cv, p, ang, back=13, fwd=13):
    a, b = shaft(cv, p, ang, back, fwd)
    spearhead(cv, b, ang, 6)


def gear_cragsmen(stage, cv, J):
    P = J["P"]
    neck, head = J["neck"], J["head"]
    if stage == "behind":
        # the javelin bundle slung across the back
        for off in (-4, -1):
            s = (neck[0] - 5 + off, neck[1] + 8)
            a, b = shaft(cv, s, 172, 6, 20)
            spearhead(cv, b, 172, 5)
    elif stage == "torso":
        hip = J["hip"]
        cv.put(cv.rect(hip[0] - 5, hip[1] - 1, hip[0] + 5, hip[1] + 1), LEATHER)  # belt
        # green kilt flap under the belt
        cv.put(cv.poly([(hip[0] - 5, hip[1] + 2), (hip[0] + 5, hip[1] + 2), (hip[0] + 6, hip[1] + 8), (hip[0] - 6, hip[1] + 8)]), GREEN)
        # fur mantle over the shoulders
        m = cv.ellipse((neck[0] - 1, neck[1] + 3), 8.5, 4.5)
        cv.put(m, FUR, band=2)
        for i in range(-7, 8, 3):  # ragged fur fringe
            cv.put(cv.poly([(neck[0] - 1 + i - 1.5, neck[1] + 6), (neck[0] - 1 + i + 1.5, neck[1] + 6), (neck[0] - 1 + i, neck[1] + 9.5)]), FUR, outline=True)
    elif stage == "head":
        face(cv, J)
        # green hood, peaked at the back
        hd = cv.poly([(head[0] - 5.5, head[1] + 4), (head[0] - 7, head[1] - 3), (head[0] - 3, head[1] - 7), (head[0] + 3, head[1] - 6.5), (head[0] + 4.5, head[1] - 3), (head[0] + 0.5, head[1] - 3), (head[0] - 1, head[1] + 4)])
        cv.put(hd, GREEN)
    elif stage == "weapon_under":
        if P.get("jav", True):
            javelin(cv, J["nhand"], P["wa"])
    elif stage == "front":
        if P.get("fly") is not None:
            javelin(cv, (J["neck"][0] + P["fly"], J["neck"][1] - 2), 92, 10, 10)
            cv.fx(cv.line((J["neck"][0] + P["fly"] - 26, J["neck"][1] - 3), (J["neck"][0] + P["fly"] - 11, J["neck"][1] - 2), 2), rgb(0xD8ECEE, 150))


CRAGSMEN = dict(
    gear=gear_cragsmen,
    body=dict(limb=2.5, arm=2.1, tw=5.2, hip=4.5),
    torso=BLUE,
    sleeve=SKIN,
    forearm=LEATHER,
    thigh=TAN,
    shin=FUR,
    boot=BOOT,
    pose=dict(na=(35, 110), fa=(-25, 30), wa=118),
    attack=[
        dict(),
        dict(lean=-4, na=(-60, 170), wa=112, fa=(40, 70), nf=(3, 0), ff=(-7, 0)),
        dict(lean=-9, na=(-95, 185), wa=108, fa=(60, 80), nf=(2, 0), ff=(-8, 0), dx=-1),
        dict(lean=2, na=(-150, -200), wa=100, fa=(30, 60), nf=(6, 0), ff=(-7, 0)),
        dict(lean=16, na=(80, 95), jav=False, fly=22, fa=(-40, 10), nf=(9, 0), ff=(-7, 1), crouch=3, dx=2),
        dict(lean=13, na=(60, 80), jav=False, fa=(-35, 10), nf=(9, 0), ff=(-6, 0), crouch=3, dx=2),
        dict(lean=6, na=(-40, -160), jav=False, fa=(-20, 20), nf=(6, 0), ff=(-5, 0), crouch=1),
    ],
    hit=4,
)


def mace(cv, hand, ang, l=13):
    a, b = shaft(cv, hand, ang, 2, l, rp=WOOD)
    cv.put(cv.ellipse(b, 3.6, 3.6), DSTEEL, band=2)
    for da in (0, 90, 180, 270):  # flanges
        q = add(b, vec(ang + da + 45, 4.2))
        cv.put(cv.rect(q[0] - 0.6, q[1] - 0.6, q[0] + 0.6, q[1] + 0.6), STEEL)


def rune(cv, c, col):
    x, y = round(c[0]), round(c[1])
    for dx, dy in [(0, -5), (0, -4), (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, -3), (2, -2), (3, -1), (-1, -3), (-2, -2), (-3, -1), (1, 2), (2, 3), (-1, 2), (-2, 3)]:
        cv.px(x + dx, y + dy, col)


def gear_spellwardens(stage, cv, J):
    P = J["P"]
    neck, head, hip = J["neck"], J["head"], J["hip"]
    if stage == "torso":
        # blue tabard over the mail, steel pauldrons
        cv.put(cv.poly([(neck[0] - 4, neck[1] + 2), (neck[0] + 4.5, neck[1] + 2), (hip[0] + 5.5, hip[1] + 9), (hip[0] - 4.5, hip[1] + 9)]), BLUE, band=2)
        cv.put(cv.rect(hip[0] - 5, hip[1] - 1, hip[0] + 5.5, hip[1] + 1), GOLD)
        cv.put(cv.ellipse((neck[0] - 5, neck[1] + 3), 4, 3.3), STEEL)
        cv.put(cv.ellipse((neck[0] + 5, neck[1] + 3), 4, 3.3), STEEL)
    elif stage == "head":
        # a flat-topped great helm with an eye slit and a gold cross-bar
        hx, hy = head
        cv.put(cv.poly([(hx - 5, hy - 6), (hx + 5, hy - 6), (hx + 5.5, hy + 5), (hx - 5, hy + 5)]), STEEL, band=2)
        cv.flat(cv.rect(hx - 1, hy - 2, hx + 5, hy - 2), BLACK)
        cv.flat(cv.rect(hx + 2, hy - 5, hx + 2, hy + 4), GOLD[1])
        cv.flat(cv.rect(hx - 4, hy - 6, hx + 4, hy - 6), GOLD[2])
        for yy in (1, 3):
            cv.px(hx + 4, hy + yy, BLACK)
    elif stage == "mid":
        # the rune shield on the far arm, carried in front
        c = add(J["fhand"], (1, 2))
        sx, sy = c
        m = cv.poly([(sx - 8, sy - 13), (sx + 8, sy - 13), (sx + 9, sy + 2), (sx + 5, sy + 11), (sx, sy + 15), (sx - 5, sy + 11), (sx - 9, sy + 2)])
        cv.put(m, STEEL, band=1)
        inner = cv.poly([(sx - 6, sy - 11), (sx + 6, sy - 11), (sx + 7, sy + 2), (sx + 4, sy + 9), (sx, sy + 12), (sx - 4, sy + 9), (sx - 7, sy + 2)])
        cv.put(inner, GREEN, outline=False, band=2)
        rune(cv, (sx, sy - 1), BLUE[2])
        rune(cv, (sx + 1, sy - 1), BLUE[0])
    elif stage == "weapon_under":
        mace(cv, J["nhand"], P["wa"])
    elif stage == "front":
        if P.get("sw"):
            swoosh(cv, J["nsh"], 14, 24, *P["sw"])


SPELLWARDENS = dict(
    gear=gear_spellwardens,
    body=dict(limb=3.5, arm=3.0, tw=7.0, hip=6.0, foot=7),
    torso=DSTEEL,
    sleeve=STEEL,
    forearm=STEEL,
    hand=DSTEEL,
    thigh=DSTEEL,
    shin=STEEL,
    boot=DSTEEL,
    shadow=17,
    pose=dict(na=(-35, -140), fa=(60, 85), wa=160, nf=(5, 0), ff=(-5, 0)),
    attack=[
        dict(),
        dict(na=(-70, -165), wa=190, lean=-2),
        dict(na=(-120, -175), wa=215, lean=-6, dx=-1),
        dict(na=(-150, 170), wa=160, lean=4),
        dict(na=(100, 85), wa=70, lean=14, sw=(175, 80), nf=(8, 0), crouch=3, dx=2),
        dict(na=(60, 60), wa=40, lean=16, nf=(8, 0), crouch=4, dx=2),
        dict(na=(20, 30), wa=70, lean=8, nf=(6, 0), crouch=2),
    ],
    hit=4,
)


def gear_sentinel(stage, cv, J):
    P = J["P"]
    neck, head, hip = J["neck"], J["head"], J["hip"]
    if stage == "torso":
        # a slab chest far wider than the hips, stepped like stacked masonry
        cv.put(cv.poly([(neck[0] - 13, neck[1] + 2), (neck[0] + 13, neck[1] + 1), (neck[0] + 12, neck[1] + 15), (hip[0] + 8, hip[1] + 3), (hip[0] - 8, hip[1] + 3), (neck[0] - 12, neck[1] + 15)]), STONE, band=2)
        # shoulder blocks, square-cut
        cv.put(cv.poly([(neck[0] - 18, neck[1] + 1), (neck[0] - 8, neck[1] - 2), (neck[0] - 7, neck[1] + 8), (neck[0] - 17, neck[1] + 10)]), DSTONE, band=2)
        cv.put(cv.poly([(neck[0] + 7, neck[1] - 2), (neck[0] + 18, neck[1]), (neck[0] + 18, neck[1] + 9), (neck[0] + 8, neck[1] + 8)]), STONE, band=2)
        # masonry joints and cracks
        cv.flat(cv.line((neck[0] - 11, neck[1] + 15), (neck[0] + 11, neck[1] + 15)), DSTONE[0])
        for (x0, y0, x1, y1) in [(-9, 4, -6, 9), (-6, 9, -8, 14), (7, 5, 9, 11), (-3, 16, -4, 21), (5, 16, 6, 20)]:
            cv.flat(cv.line((neck[0] + x0, neck[1] + y0), (neck[0] + x1, neck[1] + y1)), DSTONE[0])
        # the army plate: a key-coloured band with a gem (so armies still read apart)
        cv.put(cv.rect(hip[0] - 8, hip[1] - 2, hip[0] + 8, hip[1] + 1), GREEN)
        cv.put(cv.rect(hip[0] - 2, hip[1] - 4, hip[0] + 2, hip[1] + 3), BLUE)
        # glowing chest rune
        g = P.get("glow", 1)
        col = GLOW[2] if g > 1 else GLOW[1]
        cx, cy = round(neck[0] + 1), round(neck[1] + 9)
        cv.fx(cv.ellipse((cx, cy), 7 if g > 1 else 5, 7 if g > 1 else 5), rgb(0x5FE0EA, 90 if g > 1 else 45))
        for dx, dy in [(0, -5), (0, -4), (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3), (-1, -4), (-2, -3), (-3, -2), (-4, -1), (1, -4), (2, -3), (3, -2), (4, -1), (-3, 2), (-2, 3), (-1, 4), (1, 4), (2, 3), (3, 2)]:
            cv.px(cx + dx, cy + dy, col)
    elif stage == "head":
        # a squat block sunk between the shoulders, a brow ridge and two burning eyes
        hx, hy = neck[0] + 2, neck[1] - 4
        cv.put(cv.poly([(hx - 6, hy - 6), (hx + 6, hy - 6), (hx + 7, hy + 6), (hx - 6, hy + 6)]), STONE, band=2)
        cv.put(cv.rect(hx - 6, hy - 3, hx + 7, hy - 2), DSTONE, outline=False)
        # a second army mark where no arm can cover it: a key-coloured circlet with a gem on the brow
        cv.put(cv.rect(hx - 6, hy - 6, hx + 6, hy - 5), GREEN, outline=False)
        cv.put(cv.rect(hx + 1, hy - 7, hx + 3, hy - 4), BLUE)
        cv.flat(cv.rect(hx - 1, hy - 1, hx + 6, hy + 1), BLACK)
        for ex in (1, 4):
            cv.flat(cv.rect(hx + ex, hy - 1, hx + ex + 1, hy), GLOW[2])
            cv.px(hx + ex, hy + 1, GLOW[1])
        cv.flat(cv.rect(hx, hy + 4, hx + 5, hy + 4), DSTONE[0])
    elif stage in ("farhand", "front"):
        k = "f" if stage == "farhand" else "n"
        h = J[k + "hand"]
        cv.put(cv.poly([(h[0] - 5, h[1] - 4), (h[0] + 5, h[1] - 5), (h[0] + 6, h[1] + 4), (h[0] - 4, h[1] + 5)]), DSTONE if k == "f" else STONE, band=2)
        cv.flat(cv.line((h[0] - 2, h[1] - 1), (h[0] + 4, h[1] - 1)), DSTONE[0])
        el = J[k + "el"]
        for i in range(-2, 3):
            cv.px(el[0] + i, el[1] + (i % 2), GLOW[1])
        if stage == "front" and P.get("slam"):
            gx, gy = h[0] + 2, J["ground"] - 2
            for i, (dx, dy) in enumerate([(-9, -3), (-5, -8), (1, -11), (7, -7), (11, -2), (-12, -8), (13, -9)]):
                cv.put(cv.rect(gx + dx, gy + dy, gx + dx + 1 + (i % 2), gy + dy + 1 + (i % 2)), DSTONE)
            cv.fx(cv.ellipse((gx, gy), 13, 3), rgb(0xC0B7AF, 150))
            bolt_zigzag(cv, (gx - 10, gy), (gx + 12, gy - 1), seed=3, jit=1.5)


SENTINEL = dict(
    gear=gear_sentinel,
    body=dict(thigh=11, shin=11, torso=25, ua=14, fa=12, limb=5.2, arm=5.0, tw=10, hip=8, head=(6, 6), foot=9),
    torso=STONE,
    sleeve=STONE,
    forearm=DSTONE,
    hand=DSTONE,
    thigh=DSTONE,
    shin=STONE,
    boot=DSTONE,
    shadow=20,
    pose=dict(na=(-16, 8), fa=(30, 45), nf=(7, 0), ff=(-7, 0), lean=6, crouch=1),
    attack=[
        dict(),
        dict(na=(-40, -120), lean=0, glow=2),
        dict(na=(-110, -170), lean=-6, glow=2, dx=-1),
        dict(na=(-160, -190), lean=-8, glow=2, dx=-1),
        dict(na=(110, 80), lean=14, nf=(10, 0), crouch=2, dx=2),
        dict(na=(55, 25), lean=24, nf=(10, 0), crouch=5, dx=3, slam=True, glow=2),
        dict(na=(45, 20), lean=20, nf=(10, 0), crouch=4, dx=3, slam=True),
        dict(na=(30, 25), lean=10, nf=(8, 0), crouch=2, dx=1),
    ],
    hit=5,
)


def cutlass(cv, hand, ang, l=20):
    """A broad curved blade: a fat arc that widens toward the tip."""
    d = vec(ang)
    n = (-d[1], d[0])
    pts, back = [], []
    for i in range(9):
        t = i / 8
        bow = math.sin(t * math.pi) * 2.6
        wdt = 1.3 + t * 1.6 if t < 0.85 else 0.4
        c = (hand[0] + d[0] * l * t + n[0] * bow, hand[1] + d[1] * l * t + n[1] * bow)
        pts.append((c[0] + n[0] * wdt, c[1] + n[1] * wdt))
        back.append((c[0] - n[0] * wdt, c[1] - n[1] * wdt))
    cv.put(cv.poly(pts + back[::-1]), STEEL)
    cv.put(cv.rect(hand[0] - 2, hand[1] - 2, hand[0] + 2, hand[1] + 2), GOLD)


def gear_marines(stage, cv, J):
    P = J["P"]
    neck, head, hip = J["neck"], J["head"], J["hip"]
    if stage == "torso":
        # open blue vest over a linen shirt, a wide green sash with a trailing end
        cv.put(cv.poly([(neck[0] - 1.5, neck[1] + 2), (neck[0] + 2.5, neck[1] + 2), (hip[0] + 2, hip[1] - 2), (hip[0] - 1, hip[1] - 2)]), LINEN, outline=False)
        cv.put(cv.rect(hip[0] - 5, hip[1] - 2, hip[0] + 5, hip[1] + 2), GREEN)
        cv.put(cv.poly([(hip[0] - 5, hip[1] + 2), (hip[0] - 2, hip[1] + 2), (hip[0] - 5, hip[1] + 10), (hip[0] - 8, hip[1] + 9)]), GREEN)
    elif stage == "head":
        face(cv, J)
        hx, hy = head
        # red-free bandana in the army's green, knotted at the back; a dark beard
        cv.put(cv.poly([(hx - 4.5, hy - 1.5), (hx - 4, hy - 5), (hx, hy - 6), (hx + 4, hy - 4.5), (hx + 4.5, hy - 2.5)]), GREEN)
        cv.put(cv.poly([(hx - 5, hy - 2), (hx - 10, hy), (hx - 9, hy + 3), (hx - 5, hy)]), GREEN)
        cv.flat(cv.poly([(hx - 1, hy + 2), (hx + 4, hy + 2), (hx + 3, hy + 5), (hx, hy + 5)]), rgb(0x3A2A20))
        cv.px(hx - 4, hy + 1, GOLD[2])  # earring
    elif stage == "mid":
        c = add(J["fhand"], (1, 0))
        cv.put(cv.ellipse(c, 6.5, 6.5), DSTEEL, band=2)
        cv.put(cv.ellipse(c, 4, 4), BLUE, outline=False)
        cv.put(cv.ellipse(c, 1.5, 1.5), STEEL, outline=False)
    elif stage == "weapon_under":
        cutlass(cv, J["nhand"], P["wa"])
    elif stage == "front":
        if P.get("sw"):
            swoosh(cv, J["nsh"], 12, 25, *P["sw"])


MARINES = dict(
    gear=gear_marines,
    body=dict(limb=2.9, arm=2.6, tw=5.6),
    torso=BLUE,
    sleeve=SKIN,
    forearm=SKIN,
    thigh=TAN,
    shin=TAN,
    boot=BOOT,
    pose=dict(na=(25, 115), fa=(60, 100), wa=165, nf=(6, 0), ff=(-5, 0), crouch=2, lean=6),
    attack=[
        dict(),
        dict(na=(-80, -150), wa=200, lean=0),
        dict(na=(-130, -170), wa=230, lean=-6, dx=-1),
        dict(na=(-170, 160), wa=150, lean=6, nf=(8, 0)),
        dict(na=(95, 80), wa=75, lean=16, sw=(170, 70), nf=(10, 0), crouch=4, dx=3),
        dict(na=(50, 45), wa=30, lean=18, nf=(10, 0), crouch=5, dx=3),
        dict(na=(10, -60), wa=110, lean=10, nf=(8, 0), crouch=3, dx=1),
    ],
    hit=4,
)


def crossbow(cv, hand, ang, loaded=True, flash=False):
    d = vec(ang)
    n = (-d[1], d[0])
    a = add(hand, (-d[0] * 6, -d[1] * 6))
    b = add(hand, (d[0] * 10, d[1] * 10))
    cv.put(cv.line(a, b, 3), WOOD)  # stock
    p0, p1 = add(b, (n[0] * 6.5 - d[0] * 2, n[1] * 6.5 - d[1] * 2)), add(b, (-n[0] * 6.5 - d[0] * 2, -n[1] * 6.5 - d[1] * 2))
    cv.put(cv.line(p0, b, 2), DSTEEL)  # the bow's two limbs, swept back
    cv.put(cv.line(p1, b, 2), DSTEEL)
    back = add(hand, (d[0] * (2 if loaded else 7), d[1] * (2 if loaded else 7)))
    cv.flat(cv.line(p0, back), rgb(0xE8DFD5))
    cv.flat(cv.line(p1, back), rgb(0xE8DFD5))
    if loaded:
        cv.flat(cv.line(back, add(b, (d[0] * 3, d[1] * 3))), rgb(0xFCFCFC))
    if flash:
        cv.fx(cv.line(add(b, (d[0] * 2, d[1] * 2)), add(b, (d[0] * 22, d[1] * 22)), 2), rgb(0xD8ECEE, 170))
        cv.flat(cv.line(add(b, (d[0] * 12, d[1] * 12)), add(b, (d[0] * 22, d[1] * 22))), rgb(0xFCFCFC))


def pavise(cv, x, ground, h=36, w=18):
    """A tall planted shield: steel rim, green face with a blue pale and a boss, propped on a spike."""
    y1 = ground - 3
    y0 = y1 - h
    cv.put(cv.poly([(x - w / 2 + 2, y0), (x + w / 2 - 2, y0), (x + w / 2, y0 + 3), (x + w / 2, y1), (x - w / 2, y1), (x - w / 2, y0 + 3)]), LINEN, band=1)
    cv.put(cv.rect(x - w / 2 + 2, y0 + 3, x + w / 2 - 2, y1 - 2), GREEN, outline=False, band=3)
    cv.put(cv.rect(x - 2, y0 + 3, x + 2, y1 - 2), BLUE, outline=False, band=1)
    cv.put(cv.ellipse((x, y0 + h * 0.42), 3, 3), GOLD)
    for yy in (y0 + 8, y1 - 8):
        cv.flat(cv.rect(x - w / 2 + 2, yy, x + w / 2 - 2, yy), GREEN[0])


def gear_pavisiers(stage, cv, J):
    P = J["P"]
    neck, head, hip = J["neck"], J["head"], J["hip"]
    if stage == "torso":
        # breastplate with a fauld, blue skirt below
        cv.put(cv.poly([(hip[0] - 5, hip[1] + 1), (hip[0] + 5.5, hip[1] + 1), (hip[0] + 6.5, hip[1] + 8), (hip[0] - 6, hip[1] + 8)]), BLUE)
        cv.flat(cv.line((neck[0] + 1, neck[1] + 3), (hip[0] + 1.5, hip[1] - 2)), STEEL[0])
        cv.put(cv.rect(hip[0] - 5, hip[1] - 1, hip[0] + 5.5, hip[1] + 1), LEATHER)
        # quiver of bolts at the hip
        q = (hip[0] - 6, hip[1] + 1)
        cv.put(cv.poly([(q[0] - 3, q[1] - 3), (q[0] + 1, q[1] - 4), (q[0] - 1, q[1] + 8), (q[0] - 5, q[1] + 7)]), LEATHER)
        for i in (0, 2):
            cv.px(q[0] - 2 + i, q[1] - 5, rgb(0xFCFCFC))
            cv.px(q[0] - 2 + i, q[1] - 6, rgb(0xFCFCFC))
    elif stage == "head":
        face(cv, J)
        hx, hy = head
        # kettle hat: a rounded crown and a wide flat brim
        cv.put(cv.ellipse((hx, hy - 4), 4.5, 3.6), STEEL)
        cv.put(cv.poly([(hx - 8, hy - 2), (hx + 8, hy - 2), (hx + 7, hy - 0.2), (hx - 7, hy - 0.2)]), DSTEEL)
        cv.flat(cv.rect(hx - 3, hy - 5, hx + 3, hy - 5), GREEN[1])
    elif stage == "weapon_under":
        crossbow(cv, J["nhand"], P["wa"], P.get("loaded", True), P.get("flash", False))
    elif stage == "mid":
        # the planted pavise stands in front of the body; the arms and crossbow reach over its top edge
        pavise(cv, J["hip"][0] - P["dx"] + P.get("pavx", 17), J["ground"])


PAVISIERS = dict(
    gear=gear_pavisiers,
    body=dict(limb=3.0, arm=2.6, tw=6.2),
    torso=STEEL,
    sleeve=BLUE,
    forearm=LEATHER,
    thigh=TAN,
    shin=DSTEEL,
    boot=BOOT,
    shadow=19,
    pose=dict(na=(78, 100), fa=(70, 100), wa=92, nf=(4, 0), ff=(-6, 0), lean=5, dx=-8, crouch=1),
    attack=[
        dict(),
        dict(na=(82, 98), wa=90, lean=8),
        dict(na=(84, 96), wa=90, lean=9, crouch=2),
        dict(na=(80, 96), wa=86, lean=5, crouch=2, loaded=False, flash=True),
        dict(na=(76, 94), wa=80, lean=2, crouch=1, loaded=False),
        dict(na=(45, 70), wa=35, lean=10, crouch=3, loaded=False),
        dict(na=(35, 60), wa=25, lean=14, crouch=4, loaded=False, fa=(30, 50)),
        dict(na=(70, 98), wa=88, lean=6, crouch=1),
    ],
    hit=3,
)


def runeblade(cv, hand, ang, l=24):
    end = blade(cv, hand, ang, l, 2.0, ramp(0x5FE0EA, 0xB4F4F8, 0xFCFFFF))
    d = vec(ang)
    n = (-d[1], d[0])
    cv.put(cv.line(add(hand, (n[0] * 4, n[1] * 4)), add(hand, (-n[0] * 4, -n[1] * 4)), 2), GOLD)
    cv.put(cv.line(hand, add(hand, (-d[0] * 4, -d[1] * 4)), 2), GOLD)
    for t in (0.3, 0.5, 0.7):
        cv.px(hand[0] + d[0] * l * t, hand[1] + d[1] * l * t, GLOW[0])
    return end


def gear_battlemage(stage, cv, J):
    P = J["P"]
    neck, head, hip = J["neck"], J["head"], J["hip"]
    if stage == "behind":
        # a long cloak, billowing behind
        b = P.get("billow", 0)
        g = J["ground"]
        cv.put(cv.poly([(neck[0] - 5, neck[1] + 1), (neck[0] + 3, neck[1] + 1), (hip[0] + 1, g - 5), (hip[0] - 15 - b, g - 3), (hip[0] - 13 - b, hip[1] + 4), (neck[0] - 9, neck[1] + 8)]), BLUE, band=3)
        cv.flat(cv.line((neck[0] - 6, neck[1] + 8), (hip[0] - 10 - b, g - 5)), BLUE[0])
    elif stage == "torso":
        # green tabard hanging from the belt, gold gorget and pauldrons
        cv.put(cv.poly([(hip[0] - 3, hip[1] + 1), (hip[0] + 4.5, hip[1] + 1), (hip[0] + 5, hip[1] + 15), (hip[0] + 1, hip[1] + 18), (hip[0] - 3, hip[1] + 15)]), GREEN, band=2)
        cv.px(hip[0] + 1, hip[1] + 7, GOLD[2])
        cv.px(hip[0] + 1, hip[1] + 10, GOLD[2])
        cv.put(cv.rect(hip[0] - 5.5, hip[1] - 1, hip[0] + 6, hip[1] + 1), DARK)
        cv.flat(cv.line((neck[0] - 3, neck[1] + 7), (neck[0] + 4, neck[1] + 7)), GOLD[0])
        cv.flat(cv.line((neck[0] + 1, neck[1] + 3), (neck[0] + 1, neck[1] + 12)), GOLD[0])
        cv.px(neck[0] + 1, neck[1] + 7, GLOW[1])
        for sx in (-6.5, 6.5):
            cv.put(cv.ellipse((neck[0] + sx, neck[1] + 2.5), 5, 4), GOLD, band=2)
            cv.put(cv.poly([(neck[0] + sx - 2, neck[1] - 1), (neck[0] + sx + 2, neck[1] - 1), (neck[0] + sx + (2 if sx > 0 else -2), neck[1] - 5)]), GOLD)
    elif stage == "head":
        hx, hy = head
        # a closed gold helm with a dark visor, two swept horns and a tall crest
        cv.put(cv.ellipse((hx, hy), 4.8, 5.6), GOLD, band=2)
        cv.flat(cv.poly([(hx, hy - 2), (hx + 5, hy - 2), (hx + 4, hy + 1), (hx + 1, hy + 1)]), BLACK)
        cv.px(hx + 3, hy - 1, GLOW[2])
        cv.put(cv.poly([(hx - 5, hy - 3), (hx + 5, hy - 3), (hx + 6, hy - 7), (hx + 3, hy - 5), (hx + 1, hy - 8), (hx - 1, hy - 5), (hx - 4, hy - 8)]), GOLD)
        cv.put(cv.poly([(hx - 3, hy - 6), (hx - 9, hy - 8), (hx - 11, hy - 3), (hx - 8, hy + 3), (hx - 5, hy - 1)]), GREEN)
        cv.put(cv.poly([(hx - 4.5, hy + 2), (hx + 3, hy + 3), (hx + 2, hy + 7), (hx - 4, hy + 6)]), GOLD)
    elif stage == "farhand":
        pass
    elif stage == "mid":
        # the casting hand: a ball of crackling light
        h = J["fhand"]
        c = P.get("charge", 1)
        cv.put(cv.ellipse(h, 2.4, 2.4), GOLD)
        if c:
            cv.fx(cv.ellipse(h, 3 + c * 2, 3 + c * 2), rgb(0x5FE0EA, 90))
            cv.flat(cv.ellipse(h, 1.2 + c * 0.6, 1.2 + c * 0.6), rgb(0xFCFFFF))
            for i in range(3 + c * 2):
                a = i * 360 / (3 + c * 2) + c * 25
                bolt_zigzag(cv, h, add(h, vec(a, 5 + c * 2.5)), seed=i + c, jit=1.5)
        if P.get("cast"):
            bolt_zigzag(cv, h, (h[0] + P["cast"], h[1] - 2), seed=5, w=2, jit=4)
            bolt_zigzag(cv, h, (h[0] + P["cast"] - 4, h[1] + 7), seed=9, jit=3)
            bolt_zigzag(cv, h, (h[0] + P["cast"] - 6, h[1] - 9), seed=2, jit=3)
    elif stage == "weapon_under":
        runeblade(cv, J["nhand"], P["wa"])


BATTLEMAGE = dict(
    gear=gear_battlemage,
    body=dict(thigh=14, shin=14, torso=20, ua=11, fa=10, limb=3.3, arm=2.8, tw=6.8, hip=5.6, head=(5.0, 5.8), foot=7),
    torso=GOLD,
    sleeve=GOLD,
    forearm=ramp(0x8A5C36, 0xB58546, 0xE1C760),
    hand=GOLD,
    thigh=ramp(0x8A5C36, 0xB58546, 0xE1C760),
    shin=GOLD,
    boot=ramp(0x8A5C36, 0xB58546, 0xE1C760),
    shadow=18,
    pose=dict(na=(-20, 10), wa=25, fa=(50, 120), nf=(4, 0), ff=(-5, 0), lean=2, crouch=0, dx=-2),
    attack=[
        dict(),
        dict(fa=(20, 150), charge=2, lean=-2, billow=1),
        dict(fa=(-30, 175), charge=3, lean=-5, billow=3, na=(-30, -10), wa=10),
        dict(fa=(-60, 185), charge=3, lean=-6, billow=4, na=(-35, -20), wa=5),
        dict(fa=(70, 92), charge=3, cast=24, lean=8, billow=5, nf=(7, 0), dx=0, na=(-40, -40), wa=-10),
        dict(fa=(75, 90), charge=2, cast=18, lean=9, billow=4, nf=(7, 0), dx=0, na=(-40, -40), wa=-10),
        dict(fa=(65, 100), charge=1, lean=6, billow=2, nf=(6, 0), dx=-1),
    ],
    hit=4,
)

UNITS = dict(cragsmen=CRAGSMEN, spellwardens=SPELLWARDENS, sentinel=SENTINEL, marines=MARINES, pavisiers=PAVISIERS, battlemage=BATTLEMAGE)

# A 4-frame walk: contact, passing, contact (legs swapped), passing.
WALK = [
    dict(nf=(8, 0), ff=(-7, 1), crouch=2),
    dict(nf=(1, 0), ff=(2, 5), crouch=0),
    dict(nf=(-7, 1), ff=(8, 0), crouch=2),
    dict(nf=(2, 5), ff=(1, 0), crouch=0),
]
WALK_ARMS = {
    "cragsmen": [dict(na=(30, 105), fa=(-30, 0)), dict(na=(32, 108), fa=(-5, 20)), dict(na=(34, 110), fa=(25, 45)), dict(na=(32, 108), fa=(5, 25))],
    "marines": [dict(na=(25, 60), fa=(50, 95)), dict(na=(5, 40), fa=(52, 95)), dict(na=(-15, 20), fa=(55, 95)), dict(na=(5, 40), fa=(52, 95))],
    "sentinel": [dict(na=(-28, -10), fa=(34, 45)), dict(na=(-18, 4), fa=(20, 32)), dict(na=(-8, 12), fa=(-10, 10)), dict(na=(-18, 4), fa=(15, 28))],
}


def crop(img):
    return img.crop(img.getbbox())


def build(key):
    U = UNITS[key]
    frames = [figure(U, p).image() for p in U["attack"]]
    strip = Image.new("RGBA", (72 * len(frames), 72))
    for i, f in enumerate(frames):
        strip.paste(f, (i * 72, 0))
    walk = Image.new("RGBA", (256, 72))
    for i, w in enumerate(WALK):
        p = dict(w)
        p.update(WALK_ARMS.get(key, [{}] * 4)[i])
        p["dx"] = 0 if key != "pavisiers" else -6
        if key == "pavisiers":
            p["pavx"] = 15  # the pavise is carried in front while marching
        if key == "battlemage":
            p["billow"] = (2, 4, 2, 0)[i]
        walk.paste(figure(U, p, w=64, ox=31).image(), (i * 64, 0))
    stand = crop(figure(U, {"dx": 0} if key not in ("pavisiers",) else {}).image())
    return strip, stand, walk


# ---------------------------------------------------------------------------------------------------------------
# Ability icons (52x52): a tan plate in a brown frame, one pictogram each
# ---------------------------------------------------------------------------------------------------------------
PLATE = ramp(0xA08663, 0xC9AE87, 0xDCC8A4)
FRAME = ramp(0x4F4137, 0x6E5B4C, 0x8A7461)
IGOLD = ramp(0xA87018, 0xE0A93A, 0xF8DC78)


def icon_base():
    cv = Canvas(52, 52)
    im, d = cv._m()
    d.rounded_rectangle([1, 1, 50, 50], 7, fill=255)
    cv.put(np.array(im) > 0, FRAME, outline=False, band=2)
    im, d = cv._m()
    d.rounded_rectangle([5, 5, 46, 46], 4, fill=255)
    cv.put(np.array(im) > 0, PLATE, outline=False, band=2)
    return cv


def icon_climb():
    cv = icon_base()
    cv.put(cv.poly([(7, 44), (16, 22), (22, 28), (30, 10), (38, 24), (44, 44)]), ramp(0x5C5348, 0x857A69, 0xB4A994), band=3)
    cv.put(cv.poly([(26, 18), (30, 10), (34, 17), (31, 20), (29, 17)]), ramp(0xC0B7AF, 0xE8DFD5, 0xFCFCFC), outline=False)
    # the climbing arrow
    cv.put(cv.line((14, 40), (27, 24), 3), IGOLD)
    cv.put(cv.poly([(22, 22), (31, 19), (29, 29)]), IGOLD)
    return cv


def icon_nullify():
    cv = icon_base()
    # a spell-star struck through by a ward ring
    c = (26, 26)
    for a in range(0, 360, 45):
        cv.put(cv.line(c, add(c, vec(a, 13)), 3), ramp(0x5C2B7A, 0x9B48CF, 0xD9A8F5), outline=False)
    cv.put(cv.ellipse(c, 5, 5), ramp(0x7C3AA5, 0xD9A8F5, 0xFCFCFC))
    ring = cv.ellipse(c, 17, 17) & ~cv.ellipse(c, 13.5, 13.5)
    cv.put(ring, IGOLD)
    cv.put(cv.line((14, 38), (38, 14), 4), IGOLD)
    return cv


def icon_unyielding():
    cv = icon_base()
    # a stone fist
    st = ramp(0x5C5348, 0x8C8273, 0xB9AE99)
    cv.put(cv.poly([(18, 30), (34, 30), (36, 46), (16, 46)]), st, band=3)
    cv.put(cv.poly([(12, 14), (38, 12), (41, 30), (13, 32)]), st, band=3)
    for x in (19, 26, 33):
        cv.flat(cv.line((x, 13), (x + 1, 24)), st[0])
    cv.put(cv.poly([(9, 22), (16, 20), (18, 31), (11, 33)]), st, band=2)
    for dx, dy in [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)]:
        cv.px(22 + dx, 37 + dy, GLOW[1])
        cv.px(22 + dx, 41 + dy, GLOW[1])
    return cv


def icon_amphibious():
    cv = icon_base()
    # a boot wading through waves
    cv.put(cv.poly([(20, 8), (30, 8), (30, 26), (39, 30), (39, 35), (19, 35)]), ramp(0x4F3128, 0x855236, 0xB6836A), band=3)
    cv.put(cv.rect(19, 8, 31, 12), IGOLD)
    w = ramp(0x1D3569, 0x2E74C6, 0xA3D8FF)
    for row, y in enumerate((30, 37)):
        pts = [(6, y + 8)]
        for i in range(0, 41, 5):
            pts.append((6 + i, y + (0 if (i // 5 + row) % 2 else 4)))
        pts.append((46, y + 8))
        cv.put(cv.poly(pts), w, band=1)
    cv.flat(cv.rect(6, 44, 45, 45), w[0])
    return cv


def icon_pavise():
    cv = icon_base()
    cv.put(cv.poly([(15, 9), (37, 9), (39, 13), (39, 43), (13, 43), (13, 13)]), ramp(0x988E89, 0xD8D8D8, 0xFCFCFC), band=2)
    cv.put(cv.rect(16, 13, 36, 40), IGOLD, outline=False, band=3)
    cv.put(cv.rect(24, 13, 28, 40), ramp(0x731F1F, 0xB91418, 0xFF5A4A), outline=False)
    cv.put(cv.rect(16, 23, 36, 27), ramp(0x731F1F, 0xB91418, 0xFF5A4A), outline=False)
    # arrows glancing off
    for (x0, y0) in ((6, 12), (5, 30)):
        cv.put(cv.line((x0, y0), (x0 + 8, y0 + 4), 2), ramp(0x5B3A1E, 0x855236, 0xA67247))
    return cv


def icon_chain():
    cv = icon_base()
    im, d = cv._m()
    d.rounded_rectangle([5, 5, 46, 46], 4, fill=255)
    cv.put(np.array(im) > 0, ramp(0x1E2A44, 0x33456B, 0x52688F), outline=False, band=2)
    pts = [(9, 12), (20, 22), (15, 27), (28, 30), (24, 36), (43, 41)]
    for a, b in zip(pts, pts[1:]):
        cv.fx(cv.line(a, b, 5), rgb(0x5FE0EA, 140))
    for a, b in zip(pts, pts[1:]):
        cv.flat(cv.line(a, b, 2), rgb(0xFCFFFF))
    # the two forks to the next targets
    for a, b in (((28, 30), (40, 20)), ((15, 27), (11, 40))):
        cv.fx(cv.line(a, b, 3), rgb(0x5FE0EA, 140))
        cv.flat(cv.line(a, b, 1), rgb(0xFCFFFF))
    for c in ((9, 12), (40, 20), (11, 40), (43, 41)):
        cv.put(cv.ellipse(c, 2.5, 2.5), IGOLD)
    return cv


ICONS = dict(climb=icon_climb, nullify=icon_nullify, unyielding=icon_unyielding, amphibious=icon_amphibious, pavise=icon_pavise, chain=icon_chain)


# ---------------------------------------------------------------------------------------------------------------
def preview(built, icons, path, scale=2):
    names = dict(cragsmen="Cragsmen", spellwardens="Spellwardens", sentinel="Stone Sentinel", marines="Marines", pavisiers="Pavisiers", battlemage="Battlemage")
    rowh = 72 + 14
    w = 80 + 4 * 64 + 12 + max(s.width for s, _, _ in built.values()) + 8
    h = rowh * len(built) + 64
    sheet = Image.new("RGBA", (w, h), (86, 122, 84, 255))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    y = 2
    for key, (strip, stand, walk) in built.items():
        d.text((4, y), names[key] + "  -  stand / walk / attack (hit frame %d)" % UNITS[key]["hit"], fill=(255, 255, 255, 255), font=font)
        sheet.paste(stand, (8 + (64 - stand.width) // 2, y + 12 + 72 - stand.height), stand)
        sheet.paste(walk, (80, y + 12), walk)
        sheet.paste(strip, (80 + 256 + 12, y + 12), strip)
        y += rowh
    d.text((4, y + 2), "Ability icons: " + " / ".join(icons), fill=(255, 255, 255, 255), font=font)
    for i, im in enumerate(icons.values()):
        sheet.paste(im, (8 + i * 60, y + 14), im)
    sheet.resize((w * scale, h * scale), Image.NEAREST).save(path)


def main():
    built = {}
    for key in UNITS:
        strip, stand, walk = build(key)
        strip.save(os.path.join(OUT, "sprites", key + ".png"))
        stand.save(os.path.join(OUT, "sprites", "stand", key + ".png"))
        walk.save(os.path.join(OUT, "sprites", "walk", key + ".png"))
        built[key] = (strip, stand, walk)
        print("%-13s attack %d frames (hit %d)  stand %dx%d" % (key, strip.width // 72, UNITS[key]["hit"], stand.width, stand.height))
    icons = {}
    for name, fn in ICONS.items():
        im = fn().image()
        im.save(os.path.join(OUT, "hud", "skill_" + name + ".png"))
        icons[name] = im
    os.makedirs(os.path.join(ROOT, "docs", "images"), exist_ok=True)
    preview(built, icons, os.path.join(ROOT, "docs", "images", "bonus-units.png"))


if __name__ == "__main__":
    main()
