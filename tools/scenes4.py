"""Short-format (30s) scenes: phantom vibration."""
from kit2 import *

def _phone(cr, x, y, s, a=1.0, screen=None):
    w, h = s * .52, s
    rrect(cr, x - w / 2, y - h / 2, w, h, s * .09, INK, a); rrect(cr, x - w / 2 + s * .03, y - h / 2 + s * .05, w - s * .06, h - s * .1, s * .06, screen or C("1E2A4E"), a)
    rrect(cr, x - s * .07, y - h / 2 + s * .02, s * .14, s * .02, s * .01, C("3A3A44"), a)

def ph_hook(cr, t, d, m):
    f = t / d; buzz = f < .55
    vgrad(cr, PW, PH, C("2A0F2E"), C("7A1F3D")) if buzz else vgrad(cr, PW, PH, C("14122B"), C("241F4A"))
    jx = math.sin(t * 95) * 14 if buzz else 0; jy = math.cos(t * 83) * 6 if buzz else 0
    if buzz:
        for i in range(4):
            ph = (t * 2.2 + i / 4) % 1
            ring(cr, 480, 370, 150 + ph * 330, 14 * (1 - ph) + 2, ACC, .9 * (1 - ph))
        for i, (x, y, r) in enumerate([(165, 190, -.25), (800, 250, .2), (190, 560, .15), (770, 560, -.2)]):
            if int(t * 9 + i) % 2 == 0:
                push(cr, x, y, 1 + .15 * math.sin(t * 30), r); text(cr, "BZZT", 0, 0, 74, WHITE, anchor="c", face="Lora"); cr.restore()
    push(cr, 480 + jx, 370 + jy, 1, math.sin(t * 70) * .05 if buzz else 0)
    _phone(cr, 0, 0, 480, screen=C("FFF3C4") if buzz and int(t * 12) % 2 else C("1E2A4E"))
    if not buzz:
        text(cr, "No new", 0, -20, 34, CREAM, anchor="c"); text(cr, "notifications", 0, 24, 34, CREAM, anchor="c")
    cr.restore()
    if not buzz:
        k = back((f - .55) * d / .3)
        text(cr, "?", 760, 250, 200 * min(1.2, k), ACC, face="Lora", anchor="c"); text(cr, "?", 190, 300, 120 * min(1.2, k), RED, face="Lora", anchor="c")

def ph_stat(cr, t, d, m):
    vgrad(cr, PW, PH, C("14304A"), C("1E4870"))
    for i in range(10):
        x = 130 + (i % 5) * 150; y = 170 + (i // 5) * 190; lit = i < 9 and t > .3 + i * .16
        col = ACC if lit else C("33507A"); k = 1 + .25 * max(0, 1 - abs(t - (.3 + i * .16)) * 6) if i < 9 else 1
        push(cr, x, y, k); circle(cr, 0, -30, 34, col); rrect(cr, -40, 12, 80, 84, 26, col)
        if lit: rrect(cr, 14, 30, 22, 36, 5, INK); rrect(cr, 17, 34, 16, 26, 3, C("8FD3FF"))
        cr.restore()
    k = back((t - 2.0) / .4) * (1 + .04 * math.sin(t * 6))
    if k > 0:
        push(cr, 400, 610, k); rrect(cr, -210, -62, 420, 124, 62, WHITE); text(cr, "9 in 10", 0, 28, 84, DK, anchor="c", face="Lora"); cr.restore()

def ph_why(cr, t, d, m):
    vgrad(cr, PW, PH, C("2B2758"), C("4A3E8E")); rrect(cr, 0, 610, PW, 110, 0, C("231F48"))
    fl = int(t * 5) % 2
    o = person(cr, 440, 640, 380, shirt=C("4F7DD9"), pose=dict(mouth="o", look=math.sin(t * 3) * .8, la=20 + math.sin(t * 25) * 4, ra=40, ra2=-60, blink=(t % 2.2) < .1)); hx, hy = o["head"]; u = o["u"]
    glow(cr, hx, hy - 16 * u, 120, RED, .55 if fl else .2)
    rrect(cr, hx - 22, hy - 30 * u, 44, 26, 10, RED if fl else C("8A1F1F")); rrect(cr, hx - 30, hy - 30 * u + 22, 60, 10, 4, INK)
    px, py = 440 + 9 * u, 640 - 40 * u
    _phone(cr, px, py, 70)
    for i in range(3):
        ph = (t * 3 + i / 3) % 1; ring(cr, px, py, 30 + ph * 50, 5, ACC, .8 * (1 - ph), -.8, .8); ring(cr, px, py, 30 + ph * 50, 5, ACC, .8 * (1 - ph), math.pi - .8, math.pi + .8)
    for i, (x, y, lbl, tl) in enumerate([(175, 430, "muscle twitch", 1), (740, 330, "sleeve moves", -1)]):
        bubble(cr, x, y, 260, 60, lbl, 26, back((t - .8 - i * 1.6) / .35), tail=tl)
    k = back((t - d * .55) / .35) * (1 + .08 * math.sin(t * 14))
    if k > 0:
        push(cr, 250, 150, k, -.08); rrect(cr, -170, -52, 340, 104, 18, RED); text(cr, "PHONE?!", 0, 22, 62, WHITE, anchor="c", face="Lora"); cr.restore()

def ph_fix(cr, t, d, m):
    room(cr, C("E9F3EC"), C("CFE5D6"), C("9DBFA8")); f = t / d
    o = person(cr, 420, 640, 380, shirt=C("4F7DD9"), pose=dict(mouth="smile", look=.3, ra=165 if f > .6 else 30, ra2=0 if f > .6 else -40, blink=(t % 2.5) < .12)); u = o["u"]
    mv = ease((t - .5) / 1.1)
    x0, x1, yy = 420 + 9 * u, 420 - 9 * u, 640 - 40 * u
    px = x0 + (x1 - x0) * mv; py = yy - math.sin(mv * math.pi) * 150
    _phone(cr, px, py, 76)
    if 0 < mv < 1: polyline(cr, [(x0, yy - 60), (420, yy - 190), (x1, yy - 60)], 5, ACC, .7, dash=[14, 10])
    g = ease((t - 1.4) / 2.2)
    if 0 < g < 1:
        gx, gy = 690 + math.sin(t * 3) * 20, 430 - g * 330
        _phone(cr, gx, gy, 120, a=.45 * (1 - g))
        for sx in (-1, 1): circle(cr, gx + sx * 12, gy - 14, 6, WHITE, .7 * (1 - g))
        text(cr, "bzzt...", gx, gy + 100, 30, MUTED, 1 - g, anchor="c")
    check(cr, 200, 220, 110, GREEN, back((t - d * .6) / .4))
