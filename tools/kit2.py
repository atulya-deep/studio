"""Shared props for batch-2 scenes."""
import math
from chars import *
from scenes import PW, PH, ACC, CREAM, TEAL, PINK, GREEN, walk_pose

DK = C("2A3572"); RED = C("E5484D"); YEL = C("FFD23F"); GREY = C("8C8FA3"); BROWN = C("8B5E3C"); DBROWN = C("6E4A2F")
INK = C("1C1C28"); MUTED = C("969EB4"); ORANGE = C("F28C28")
_rr = rrect
def rrect(cr, x, y, w, h, r, c, a=1.0):
    if w < 1 or h < 1: return
    _rr(cr, x, y, w, h, r, c, a)

def push(cr, x, y, k=1.0, rot=0.0):
    cr.save(); cr.translate(x, y); cr.rotate(rot); k = max(k, 1e-3); cr.scale(k, k)

def check(cr, x, y, s, col=GREEN, k=1.0):
    if k <= 0: return
    push(cr, x, y, k); polyline(cr, [(-.5 * s, 0), (-.15 * s, .38 * s), (.55 * s, -.4 * s)], .22 * s, col); cr.restore()

def cross(cr, x, y, s, col=RED, k=1.0):
    if k <= 0: return
    push(cr, x, y, k); line(cr, -.4 * s, -.4 * s, .4 * s, .4 * s, .2 * s, col); line(cr, .4 * s, -.4 * s, -.4 * s, .4 * s, .2 * s, col); cr.restore()

def bubble(cr, x, y, w, h, txt, size=28, k=1.0, col=WHITE, tcol=DK, tail=0, face="Inter"):
    if k <= 0: return
    push(cr, x, y, k); rrect(cr, -w / 2, -h / 2, w, h, min(24, h / 2), col)
    if tail: poly(cr, [(tail * w * .2 - 14, h / 2 - 2), (tail * w * .2 + 14, h / 2 - 2), (tail * w * .3, h / 2 + 26)], col)
    text(cr, txt, 0, size * .35, size, tcol, anchor="c", face=face); cr.restore()

def room(cr, w1, w2, fl, fy=600):
    vgrad(cr, PW, PH, w1, w2); rrect(cr, 0, fy, PW, PH - fy, 0, fl)

def desk(cr, x, y, w, col=BROWN, legs=120):
    rrect(cr, x + 26, y + 16, 22, legs, 4, DBROWN); rrect(cr, x + w - 48, y + 16, 22, legs, 4, DBROWN); rrect(cr, x, y, w, 24, 8, col)

def heart(cr, x, y, k, col=PINK, a=1.0):
    if k <= 0: return
    push(cr, x, y, k); cr.new_path(); cr.move_to(0, 30); cr.curve_to(-70, -20, -30, -75, 0, -40); cr.curve_to(30, -75, 70, -20, 0, 30); src(cr, col, a); cr.fill(); cr.restore()

def glasses(cr, o):
    hx, hy = o["head"]; u = o["u"]
    ring(cr, hx - 5 * u, hy + 1 * u, 4.2 * u, 1.2 * u, INK); ring(cr, hx + 5 * u, hy + 1 * u, 4.2 * u, 1.2 * u, INK); line(cr, hx - 1 * u, hy + 1 * u, hx + 1 * u, hy + 1 * u, 1.2 * u, INK)

def duck(cr, x, y, s, t=0, face=1):
    u = s / 100; b = math.sin(t * 3) * 2 * u
    push(cr, x, y + b); cr.scale(face, 1)
    poly(cr, [(-36 * u, -40 * u), (-60 * u, -64 * u), (-28 * u, -58 * u)], YEL)
    ell(cr, 0, -32 * u, 42 * u, 30 * u, YEL); circle(cr, 26 * u, -70 * u, 24 * u, YEL)
    ell(cr, 52 * u, -66 * u, 14 * u, 7 * u, ORANGE)
    circle(cr, 32 * u, -76 * u, 4 * u, INK); circle(cr, 33.5 * u, -77.5 * u, 1.3 * u, WHITE)
    ell(cr, -6 * u, -34 * u, 20 * u, 13 * u, C("F2B90F"), rot=-.2)
    cr.restore()

def tomato(cr, x, y, r, t=0, prog=None, face=False):
    if prog is not None:
        ring(cr, x, y, r * 1.28, r * .1, C("3C4260")); ring(cr, x, y, r * 1.28, r * .1, ACC, 1, -math.pi / 2, -math.pi / 2 + 2 * math.pi * max(.001, min(1, prog)))
    circle(cr, x, y, r, C("E5383B")); ell(cr, x - r * .4, y - r * .42, r * .26, r * .14, WHITE, .25, rot=-.6)
    rrect(cr, x - r * .97, y + r * .12, r * 1.94, r * .16, r * .06, WHITE, .9)
    for i in range(9): line(cr, x - r * .8 + i * r * .2, y + r * .14, x - r * .8 + i * r * .2, y + r * .26, r * .025, C("B02A2D"))
    line(cr, x, y - r * .95, x, y - r * 1.16, r * .1, C("2E7D4F"))
    for i in range(5): ell(cr, x + (i - 2) * r * .2, y - r * .9 + abs(i - 2) * r * .06, r * .2, r * .075, C("3FA75F"), rot=(i - 2) * .5)
    if face:
        for sx in (-1, 1): circle(cr, x + sx * r * .28, y - r * .18, r * .09, INK); circle(cr, x + sx * r * .28 + r * .03, y - r * .21, r * .03, WHITE)
        cr.new_path(); cr.arc(x, y - r * .1, r * .22, .5, math.pi - .5); cr.set_line_width(r * .05); src(cr, INK); cr.stroke()

def emu(cr, x, y, s, t=0, run=1.0, face=1, hat=False):
    u = s / 100; LEG = C("5A4632")
    push(cr, x, y); cr.scale(face, 1)
    for i, ph in enumerate((0, math.pi)):
        sw = math.sin(t * 10 + ph) * run
        hx = -5 * u + i * 9 * u; kx = hx + sw * 13 * u; fx = kx + sw * 9 * u + 3 * u
        line(cr, hx, -44 * u, kx, -22 * u, 4 * u, LEG); line(cr, kx, -22 * u, fx, -1 * u, 3.4 * u, LEG); line(cr, fx, -1 * u, fx + 10 * u, -1 * u, 3.4 * u, LEG)
    ell(cr, 0, -56 * u, 31 * u, 20 * u, C("6B5744")); ell(cr, -9 * u, -59 * u, 22 * u, 14 * u, C("59483A"))
    nb = math.sin(t * 10) * 3 * u * run + math.sin(t * 2) * 1.5 * u
    cr.new_path(); cr.move_to(22 * u, -62 * u); cr.curve_to(36 * u, -74 * u, 26 * u, -92 * u, 34 * u + nb, -104 * u)
    cr.set_line_width(7 * u); cr.set_line_cap(cairo.LINE_CAP_ROUND); src(cr, C("7C8FA6")); cr.stroke()
    circle(cr, 36 * u + nb, -108 * u, 8 * u, C("59483A"))
    poly(cr, [(42 * u + nb, -111 * u), (57 * u + nb, -106 * u), (42 * u + nb, -103 * u)], C("2B2B2B"))
    circle(cr, 38 * u + nb, -110 * u, 2.4 * u, ORANGE); circle(cr, 38.5 * u + nb, -110 * u, 1.1 * u, INK)
    if hat:
        rrect(cr, 25 * u + nb, -123 * u, 21 * u, 8 * u, 2 * u, C("3E5C3A")); rrect(cr, 40 * u + nb, -117 * u, 13 * u, 3 * u, 1 * u, C("2E4429")); circle(cr, 35 * u + nb, -119 * u, 1.8 * u, ACC)
    cr.restore()

def rat(cr, x, y, s, t=0, tail=True, face=1, run=1.0):
    u = s / 100; hop = abs(math.sin(t * 12)) * 3 * u * run
    push(cr, x, y); cr.scale(face, 1)
    if tail:
        cr.new_path(); cr.move_to(-34 * u, -14 * u); cr.curve_to(-56 * u, -4 * u, -62 * u, -34 * u + math.sin(t * 5) * 6 * u, -84 * u, -24 * u)
        cr.set_line_width(4 * u); cr.set_line_cap(cairo.LINE_CAP_ROUND); src(cr, C("F2A7B5")); cr.stroke()
    for i in (-1, 1): ell(cr, i * 18 * u + math.sin(t * 12 + i) * 5 * u * run, -2 * u, 7 * u, 3 * u, C("74778C"))
    ell(cr, 0, -19 * u - hop, 38 * u, 20 * u, GREY); ell(cr, 34 * u, -17 * u - hop, 19 * u, 13 * u, GREY)
    circle(cr, 27 * u, -33 * u - hop, 8 * u, C("F2A7B5")); circle(cr, 42 * u, -21 * u - hop, 2.6 * u, INK); circle(cr, 53 * u, -15 * u - hop, 3 * u, C("F2A7B5"))
    cr.restore()

HOLES = [(-40, 6), (27, 3), (0, 10), (-24, 4), (38, 7), (2, 22), (-33, 2), (44, 8), (-3, 30), (-12, 42), (10, 43), (-45, 9), (21, 1), (1, -2)]
ENG = (-30, -17, 17, 30)
def plane(cr, x, y, s, col, a=1.0, col2=None):
    u = s / 100; col2 = col2 or lerpc(col, INK, .3)
    poly(cr, [(x - 50 * u, y + 4 * u), (x - 8 * u, y - 12 * u), (x + 8 * u, y - 12 * u), (x + 50 * u, y + 4 * u), (x + 50 * u, y + 12 * u), (x + 8 * u, y + 7 * u), (x - 8 * u, y + 7 * u), (x - 50 * u, y + 12 * u)], col, a)
    poly(cr, [(x - 18 * u, y + 40 * u), (x, y + 32 * u), (x + 18 * u, y + 40 * u), (x + 18 * u, y + 46 * u), (x - 18 * u, y + 46 * u)], col, a)
    for ex in ENG: ell(cr, x + ex * u, y - 5 * u, 3.6 * u, 8 * u, col2, a)
    ell(cr, x, y, 7 * u, 48 * u, col, a); ell(cr, x, y - 34 * u, 4 * u, 7 * u, C("BFE0F7"), a)

def holes(cr, x, y, s, n, a=1.0):
    u = s / 100
    for i, (hx, hy) in enumerate(HOLES[:max(0, n)]):
        circle(cr, x + hx * u, y + hy * u, 2.6 * u, RED, a); circle(cr, x + hx * u, y + hy * u, 1.1 * u, INK, a)

def scissors(cr, x, y, s, t=0, col=None):
    col = col or C("C7CFE0"); a = .35 + .25 * math.sin(t * 9)
    for sg in (-1, 1):
        dx, dy = math.cos(sg * a) * s, math.sin(sg * a) * s
        line(cr, x - dx * .2, y - dy * .2, x + dx * .6, y + dy * .6, s * .09, col); ring(cr, x - dx * .36, y - dy * .36, s * .16, s * .07, RED)

def monitor(cr, x, y, w, h, hl=None, bug=None):
    rrect(cr, x + w / 2 - 22, y + h, 44, 40, 4, C("5D6680")); rrect(cr, x + w / 2 - 80, y + h + 36, 160, 14, 7, C("5D6680"))
    rrect(cr, x, y, w, h, 16, C("2B2F45")); rrect(cr, x + 12, y + 12, w - 24, h - 24, 8, C("12162B"))
    n = 6; lh = (h - 60) / n; cols = [TEAL, ACC, PINK, C("8FD3FF"), ACC, TEAL]; ws = [.55, .8, .4, .7, .5, .62]
    for i in range(n):
        yy = y + 30 + i * lh
        if hl == i: rrect(cr, x + 18, yy - 6, w - 36, lh - 4, 6, WHITE, .14)
        c = RED if bug == i else cols[i]
        rrect(cr, x + 34 + (i % 3 == 1) * 26, yy + lh * .2, (w - 90) * ws[i], lh * .32, lh * .16, c)
        circle(cr, x + 24, yy + lh * .36, 3, MUTED)
    if bug is not None:
        bx, by = x + w - 60, y + 30 + bug * lh + lh * .36
        for i in range(3): line(cr, bx - 14, by - 8 + i * 8, bx + 14, by - 8 + i * 8, 2.5, INK)
        ell(cr, bx, by, 10, 13, RED)

def envelope(cr, x, y, w, a=1.0):
    h = w * .66; rrect(cr, x - w / 2, y - h / 2, w, h, 6, WHITE, a)
    polyline(cr, [(x - w / 2 + 4, y - h / 2 + 4), (x, y + h * .08), (x + w / 2 - 4, y - h / 2 + 4)], 3, C("9AA3B5"), a)

def kitchen(cr):
    room(cr, C("FBEFD5"), C("F3DDB0"), C("C9A27A"))
    rrect(cr, 650, 190, 190, 410, 14, C("DDE6EE")); line(cr, 650, 340, 840, 340, 4, C("B5C2CF"))
    rrect(cr, 666, 250, 10, 60, 4, C("9AA7B5")); rrect(cr, 666, 370, 10, 90, 4, C("9AA7B5"))
    rrect(cr, 50, 470, 310, 130, 6, C("B98F65")); rrect(cr, 40, 455, 330, 22, 6, BROWN)
    rrect(cr, 110, 400, 76, 56, 8, C("9AA3B5")); rrect(cr, 100, 392, 96, 12, 6, C("7C8798"))
    rrect(cr, 230, 150, 120, 130, 8, WHITE); rrect(cr, 240, 160, 100, 110, 4, C("BFE0F7"))

def outback(cr, t=0):
    vgrad(cr, PW, PH, C("8ED1F0"), C("FCE3B0")); glow(cr, 800, 120, 150, C("FFE3A3"), .6); circle(cr, 800, 120, 52, C("FFE9B0"))
    poly(cr, [(0, 480), (220, 420), (480, 470), (720, 410), (960, 460), (960, 720), (0, 720)], C("D98B4E"))
    rrect(cr, 0, 560, PW, 160, 0, C("E0A45C"))
    for i in range(6): ell(cr, 90 + i * 170, 590 + (i % 2) * 60, 40, 8, C("C98A45"), .6)
