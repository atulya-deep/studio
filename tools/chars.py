"""Vector drawing kit: shapes, characters, owl mascot (pycairo)."""
import math, cairo

def C(h, a=None):
    h = h.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return (r, g, b)

def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

def back(x):  # easeOutBack
    x = max(0.0, min(1.0, x)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def appear(t, t0, d=0.5): return ease((t - t0) / d)

def src(cr, c, a=1.0): cr.set_source_rgba(c[0], c[1], c[2], a)

def circle(cr, x, y, r, c, a=1.0):
    cr.new_path(); cr.arc(x, y, max(0.01, r), 0, 2 * math.pi); src(cr, c, a); cr.fill()

def ring(cr, x, y, r, w, c, a=1.0, a0=0, a1=2 * math.pi):
    cr.new_path(); cr.arc(x, y, r, a0, a1); cr.set_line_width(w); cr.set_line_cap(cairo.LINE_CAP_ROUND); src(cr, c, a); cr.stroke()

def ell(cr, x, y, rx, ry, c, a=1.0, rot=0):
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(max(rx, .01), max(ry, .01)); cr.new_path(); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); src(cr, c, a); cr.fill()

def rr_path(cr, x, y, w, h, r):
    r = min(r, w / 2, h / 2); cr.new_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0); cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi); cr.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); cr.close_path()

def rrect(cr, x, y, w, h, r, c, a=1.0):
    rr_path(cr, x, y, w, h, r); src(cr, c, a); cr.fill()

def line(cr, x1, y1, x2, y2, w, c, a=1.0, dash=None):
    cr.new_path(); cr.move_to(x1, y1); cr.line_to(x2, y2); cr.set_line_width(w); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    if dash: cr.set_dash(dash)
    src(cr, c, a); cr.stroke(); cr.set_dash([])

def poly(cr, pts, c, a=1.0):
    cr.new_path(); cr.move_to(*pts[0])
    for p in pts[1:]: cr.line_to(*p)
    cr.close_path(); src(cr, c, a); cr.fill()

def polyline(cr, pts, w, c, a=1.0, dash=None):
    cr.new_path(); cr.move_to(*pts[0])
    for p in pts[1:]: cr.line_to(*p)
    cr.set_line_width(w); cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_join(cairo.LINE_JOIN_ROUND)
    if dash: cr.set_dash(dash)
    src(cr, c, a); cr.stroke(); cr.set_dash([])

def text(cr, s, x, y, size, c, a=1.0, face="Inter", bold=True, anchor="l"):
    cr.select_font_face(face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size); e = cr.text_extents(s)
    if anchor == "c": x -= e.x_advance / 2
    elif anchor == "r": x -= e.x_advance
    cr.move_to(x, y); src(cr, c, a); cr.show_text(s)

def vgrad(cr, w, h, c1, c2):
    g = cairo.LinearGradient(0, 0, 0, h); g.add_color_stop_rgb(0, *c1); g.add_color_stop_rgb(1, *c2)
    cr.rectangle(0, 0, w, h); cr.set_source(g); cr.fill()

def glow(cr, x, y, r, c, a=0.5):
    g = cairo.RadialGradient(x, y, 0, x, y, r); g.add_color_stop_rgba(0, *c, a); g.add_color_stop_rgba(1, *c, 0)
    cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source(g); cr.fill()

def cloud(cr, x, y, w, h, c, a=1.0):
    ell(cr, x, y + h * .05, w * .42, h * .42, c, a)
    for dx, dy, r in [(-.32, .1, .3), (-.1, -.15, .36), (.18, -.08, .33), (.36, .12, .27), (0, .18, .32)]:
        circle(cr, x + dx * w, y + dy * h * 1.2, r * h * 1.05, c, a)

def lerpc(c1, c2, k): return tuple(c1[i] + (c2[i] - c1[i]) * k for i in range(3))

# ---------------- people ----------------
SKIN = C("E9B48C"); SKIN2 = C("B97A50"); HAIR = C("2A2633"); WHITE = C("FFFFFF"); DARK = C("1C1C28")
ROMAN_RED = C("C23B33"); GOLD = C("E8B54A"); STEEL = C("9AA3B5"); PURPLE = C("6B3FA0"); BRONZE = C("B9853D")

def _arm(cr, sx, sy, a1, a2, L, w, side, sleeve, skin):
    r1 = math.radians(a1); ex = sx + side * math.sin(r1) * L; ey = sy + math.cos(r1) * L
    r2 = math.radians(a1 + a2); hx = ex + side * math.sin(r2) * L; hy = ey + math.cos(r2) * L
    line(cr, sx, sy, ex, ey, w, sleeve); line(cr, ex, ey, hx, hy, w * .9, sleeve)
    circle(cr, hx, hy, w * .55, skin)
    return hx, hy

def person(cr, x, y, s, shirt=C("4F7DD9"), pants=C("2E3550"), skin=SKIN, hair=HAIR, pose=None):
    """origin at feet; s = height in px. pose keys: la, la2, ra, ra2 (deg), swing, sit, look, blink, mouth, tilt,
       hairstyle, helmet, beard, crest, shield, cloak, apron, spear, sword"""
    p = dict(la=12, la2=8, ra=12, ra2=8, swing=0, sit=False, look=0, blink=False, mouth="smile", tilt=0, hairstyle="short")
    p.update(pose or {})
    u = s / 100.0
    hipy = y - 45 * u
    if p.get("cloak"):
        poly(cr, [(x - 13 * u, y - 80 * u), (x + 13 * u, y - 80 * u), (x + 22 * u, y - 30 * u), (x - 22 * u, y - 30 * u)], p["cloak"])
    if p["sit"]:
        kx = x + 22 * u * (1 if p.get("face", 1) > 0 else -1)
        line(cr, x - 5 * u, hipy, kx, hipy, 10 * u, pants); line(cr, kx, hipy, kx, y, 9 * u, pants)
        line(cr, x + 5 * u, hipy, kx + 3 * u, hipy, 10 * u, pants); line(cr, kx + 3 * u, hipy, kx + 3 * u, y, 9 * u, pants)
        ell(cr, kx + 4 * u, y, 7 * u, 3 * u, DARK)
    else:
        sw = p["swing"]
        for side, k in ((-1, 1), (1, -1)):
            fx = x + side * 6 * u + k * sw * 14 * u
            line(cr, x + side * 5 * u, hipy, fx, y - 3 * u, 9 * u, pants)
            ell(cr, fx + 3 * u, y - 1 * u, 7 * u, 3.5 * u, DARK)
    # torso
    rrect(cr, x - 15 * u, y - 82 * u, 30 * u, 42 * u, 9 * u, shirt)
    if p.get("apron"): rrect(cr, x - 11 * u, y - 66 * u, 22 * u, 30 * u, 4 * u, WHITE, .95)
    if p.get("roman"):
        rrect(cr, x - 15 * u, y - 82 * u, 30 * u, 14 * u, 6 * u, STEEL)  # armor
        for i in range(4): rrect(cr, x - 14 * u + i * 7.3 * u, y - 46 * u, 6 * u, 10 * u, 2 * u, BRONZE)
    # arms
    lh = _arm(cr, x - 14 * u, y - 77 * u, p["la"], p["la2"], 18 * u, 7 * u, -1, shirt, skin)
    if p.get("spear"): line(cr, lh[0], lh[1] - 55 * u, lh[0], lh[1] + 30 * u, 2.6 * u, C("6B4A2B")); poly(cr, [(lh[0], lh[1] - 66 * u), (lh[0] - 3.5 * u, lh[1] - 54 * u), (lh[0] + 3.5 * u, lh[1] - 54 * u)], STEEL)
    rh = _arm(cr, x + 14 * u, y - 77 * u, p["ra"], p["ra2"], 18 * u, 7 * u, 1, shirt, skin)
    if p.get("sword"):
        ang = math.radians(p["ra"] + p["ra2"]); dx, dy = math.sin(ang), math.cos(ang)
        line(cr, rh[0], rh[1], rh[0] + dx * 32 * u, rh[1] + dy * 32 * u, 3 * u, STEEL); line(cr, rh[0] - dy * 5 * u, rh[1] + dx * 5 * u, rh[0] + dy * 5 * u, rh[1] - dx * 5 * u, 2.5 * u, GOLD)
    if p.get("shield"):
        rrect(cr, lh[0] - 13 * u, lh[1] - 22 * u, 26 * u, 36 * u, 5 * u, p["shield"]); circle(cr, lh[0], lh[1] - 4 * u, 4 * u, GOLD)
    # head
    hx, hy = x + p["tilt"] * u, y - 95 * u
    rrect(cr, x - 3.5 * u, y - 87 * u, 7 * u, 6 * u, 2 * u, skin)
    circle(cr, hx, hy, 12.5 * u, skin)
    if p.get("beard"):
        cr.new_path(); cr.arc(hx, hy + 1 * u, 12.5 * u, 0.1, math.pi - 0.1); src(cr, p["beard"]); cr.fill()
    if not p.get("helmet"):
        hs = p["hairstyle"]
        cr.new_path(); cr.arc(hx, hy - 1 * u, 13 * u, math.pi * 1.0, math.pi * 2.0); src(cr, hair); cr.fill()
        if hs == "long": rrect(cr, hx - 14 * u, hy - 4 * u, 6 * u, 22 * u, 3 * u, hair); rrect(cr, hx + 8 * u, hy - 4 * u, 6 * u, 22 * u, 3 * u, hair)
        if hs == "bun": circle(cr, hx, hy - 15 * u, 6 * u, hair)
    lk = p["look"] * 2.5 * u
    if p["blink"]:
        line(cr, hx - 6 * u + lk, hy + 1 * u, hx - 2 * u + lk, hy + 1 * u, 1.6 * u, DARK); line(cr, hx + 2 * u + lk, hy + 1 * u, hx + 6 * u + lk, hy + 1 * u, 1.6 * u, DARK)
    else:
        circle(cr, hx - 4.5 * u + lk, hy + 1 * u, 1.9 * u, DARK); circle(cr, hx + 4.5 * u + lk, hy + 1 * u, 1.9 * u, DARK)
    m = p["mouth"]
    if m == "smile":
        cr.new_path(); cr.arc(hx + lk, hy + 5 * u, 4 * u, 0.3, math.pi - 0.3); cr.set_line_width(1.6 * u); src(cr, DARK); cr.stroke()
    elif m == "o": circle(cr, hx + lk, hy + 7 * u, 2.2 * u, DARK)
    elif m == "flat": line(cr, hx - 3 * u + lk, hy + 7.5 * u, hx + 3 * u + lk, hy + 7.5 * u, 1.6 * u, DARK)
    elif m == "frown":
        cr.new_path(); cr.arc(hx + lk, hy + 11 * u, 4 * u, math.pi + 0.5, 2 * math.pi - 0.5); cr.set_line_width(1.6 * u); src(cr, DARK); cr.stroke()
    if p.get("helmet"):
        cr.new_path(); cr.arc(hx, hy - 1 * u, 14 * u, math.pi, 2 * math.pi); src(cr, p["helmet"]); cr.fill()
        rrect(cr, hx - 15 * u, hy - 2 * u, 30 * u, 3.5 * u, 1.5 * u, p["helmet"])
        if p.get("crest"):
            cr.new_path(); cr.arc(hx, hy - 10 * u, 10 * u, math.pi * 1.05, math.pi * 1.95); cr.set_line_width(6 * u); src(cr, p["crest"]); cr.stroke()
    return dict(lh=lh, rh=rh, head=(hx, hy), u=u)

def roman(cr, x, y, s, t=0, **kw):
    pose = dict(helmet=STEEL, crest=ROMAN_RED, roman=True, shield=ROMAN_RED, la=20, la2=-30)
    pose.update(kw)
    return person(cr, x, y, s, shirt=ROMAN_RED, pants=C("5A2A24"), pose=pose)

def carthage(cr, x, y, s, t=0, **kw):
    pose = dict(helmet=BRONZE, shield=PURPLE, la=20, la2=-30, beard=C("2A1E18"), cloak=C("4A2A70"))
    pose.update(kw)
    return person(cr, x, y, s, shirt=PURPLE, pants=C("3A2550"), skin=SKIN2, pose=pose)

def elephant(cr, x, y, s, t=0, walk=0.0):
    """origin at ground center, s = height"""
    u = s / 100.0; g = C("8C8FA3"); g2 = C("74778C")
    for i, lx in enumerate((-28, -12, 14, 28)):
        sw = math.sin(t * 6 + i * 1.7) * 5 * u * walk
        rrect(cr, x + lx * u - 6 * u + sw, y - 38 * u, 12 * u, 38 * u, 4 * u, g2 if i % 2 else g)
    ell(cr, x, y - 55 * u, 44 * u, 30 * u, g)
    circle(cr, x + 40 * u, y - 70 * u, 22 * u, g)
    ell(cr, x + 30 * u, y - 68 * u, 13 * u, 20 * u, g2)  # ear
    tw = math.sin(t * 2.2) * 6 * u
    cr.new_path(); cr.move_to(x + 56 * u, y - 70 * u)
    cr.curve_to(x + 70 * u, y - 50 * u, x + 64 * u + tw, y - 25 * u, x + 72 * u + tw, y - 12 * u)
    cr.set_line_width(9 * u); cr.set_line_cap(cairo.LINE_CAP_ROUND); src(cr, g); cr.stroke()
    line(cr, x + 52 * u, y - 60 * u, x + 64 * u, y - 52 * u, 3 * u, C("F2EBDD"))  # tusk
    circle(cr, x + 46 * u, y - 76 * u, 2.2 * u, DARK)
    line(cr, x - 44 * u, y - 60 * u, x - 52 * u, y - 40 * u + math.sin(t * 3) * 3 * u, 2.5 * u, g2)
    rrect(cr, x - 20 * u, y - 92 * u, 36 * u, 14 * u, 4 * u, PURPLE)  # saddle cloth

# ---------------- owl mascot ----------------
OWL = C("8B5E3C"); OWL2 = C("6E4A2F"); BELLY = C("F3DDB8"); BEAK = C("F2A93B")

def owl(cr, x, y, s, t=0, mouth=0.0, look=(0, 0), wave=0.0):
    """(x,y) = feet center; s = height in px"""
    u = s / 100.0
    bob = math.sin(t * 2.4) * 1.2 * u
    y = y + bob
    cx, cy = x, y - 50 * u
    # wings
    wa = 0.25 + mouth * 0.15
    ell(cr, cx - 36 * u, cy + 6 * u, 13 * u, 30 * u, OWL2, rot=wa)
    if wave > 0:
        ang = -1.9 + math.sin(t * 9) * 0.35
        ell(cr, cx + 44 * u, cy - 22 * u, 13 * u, 30 * u, OWL2, rot=ang)
    else:
        ell(cr, cx + 36 * u, cy + 6 * u, 13 * u, 30 * u, OWL2, rot=-wa)
    ell(cr, cx, cy + 2 * u, 38 * u, 46 * u, OWL)
    ell(cr, cx, cy + 14 * u, 25 * u, 30 * u, BELLY)
    for i in range(3):
        for j in range(2):
            cr.new_path(); cr.arc(cx - 10 * u + i * 10 * u + j * 5 * u, cy + 8 * u + j * 9 * u, 3.5 * u, 0.2, math.pi - 0.2)
            cr.set_line_width(1.3 * u); src(cr, C("D9B98A")); cr.stroke()
    # ear tufts
    poly(cr, [(cx - 30 * u, cy - 30 * u), (cx - 26 * u, cy - 52 * u), (cx - 12 * u, cy - 38 * u)], OWL)
    poly(cr, [(cx + 30 * u, cy - 30 * u), (cx + 26 * u, cy - 52 * u), (cx + 12 * u, cy - 38 * u)], OWL)
    # face disc + eyes
    ell(cr, cx - 14 * u, cy - 18 * u, 16 * u, 15 * u, BELLY); ell(cr, cx + 14 * u, cy - 18 * u, 16 * u, 15 * u, BELLY)
    blink = (t % 3.9) < 0.13
    for sx in (-1, 1):
        ex, ey = cx + sx * 14 * u, cy - 18 * u
        if blink:
            line(cr, ex - 7 * u, ey, ex + 7 * u, ey, 2.2 * u, DARK)
        else:
            circle(cr, ex, ey, 10 * u, WHITE)
            circle(cr, ex + look[0] * 3.5 * u, ey + look[1] * 3.5 * u, 5.5 * u, DARK)
            circle(cr, ex + look[0] * 3.5 * u + 2 * u, ey + look[1] * 3.5 * u - 2 * u, 1.6 * u, WHITE)
        ring(cr, ex, ey, 12.5 * u, 2.4 * u, C("2B2B38"))
    line(cr, cx - 2 * u, cy - 20 * u, cx + 2 * u, cy - 20 * u, 2.4 * u, C("2B2B38"))
    # beak (opens with mouth)
    op = mouth * 6 * u
    poly(cr, [(cx - 6 * u, cy - 6 * u), (cx + 6 * u, cy - 6 * u), (cx, cy + 3 * u)], BEAK)
    if op > 0.3 * u:
        poly(cr, [(cx - 4.5 * u, cy - 1 * u + op * .4), (cx + 4.5 * u, cy - 1 * u + op * .4), (cx, cy + 4 * u + op)], C("D98A1F"))
    # feet
    for sx in (-1, 1):
        ell(cr, cx + sx * 12 * u, y - 2 * u, 7 * u, 3.5 * u, BEAK)
