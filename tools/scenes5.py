"""Hinglish short: revenge bedtime procrastination (2 a.m. scrolling)."""
from kit2 import *
from scenes4 import _phone

def _bed(cr, t, awake=True, glowk=1.0):
    rrect(cr, 90, 400, 40, 230, 10, C("4A3526")); rrect(cr, 110, 500, 640, 120, 18, C("3B4790")); ell(cr, 215, 488, 85, 34, C("E3E8F2"))
    circle(cr, 230, 452, 50, SKIN); cr.new_path(); cr.arc(230, 436, 50, math.pi, 2 * math.pi); src(cr, HAIR); cr.fill()
    if awake:
        if glowk > 0: glow(cr, 330, 400, 190, C("8FD3FF"), .5 * glowk)
        dr = .45 + .4 * abs(math.sin(t * .9))
        for ex in (214, 248):
            circle(cr, ex, 456, 8, WHITE); circle(cr, ex + 3, 456, 4.5, INK); rrect(cr, ex - 9, 446, 18, 16 * dr, 3, SKIN)
            ell(cr, ex, 470, 9, 4, C("B98A7A"), .8)
        line(cr, 222, 482, 240, 482, 4, INK)
    else:
        for ex in (214, 248): line(cr, ex - 7, 458, ex + 7, 458, 4, INK)
        cr.new_path(); cr.arc(231, 474, 9, .3, math.pi - .3); cr.set_line_width(3.5); src(cr, INK); cr.stroke()
    br = math.sin(t * 2) * 4
    rrect(cr, 280, 466 - br, 470, 100 + br, 34, ACC)

def n_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("070A1C"), C("151C45"))
    for i in range(14): circle(cr, (i * 173) % PW, 40 + (i * 97) % 260, 2.5, WHITE, .3 + .3 * math.sin(t * 3 + i))
    _bed(cr, t)
    sx = math.sin(t * 60) * 12 * max(0, 1 - t * 1.6)
    k = back(t / .35)
    push(cr, 600 + sx, 180, k, -.06); rrect(cr, -250, -95, 500, 190, 24, INK); rr_path(cr, -250, -95, 500, 190, 24); cr.set_line_width(6); src(cr, RED); cr.stroke()
    text(cr, "2:00", -30, 44, 150, RED if int(t * 3) % 2 == 0 else C("FF8A8E"), anchor="c", face="Lora"); text(cr, "AM", 190, 44, 44, RED, anchor="c"); cr.restore()
    push(cr, 345, 395, 1, -.25); _phone(cr, 0, 0, 170, screen=C("DCEBFF"))
    cr.save(); rr_path(cr, -38, -74, 76, 148, 8); cr.clip()
    for j in range(5):
        y = -90 + ((j * 52 - t * 150) % 260); rrect(cr, -32, y, 64, 44, 6, [PINK, TEAL, ACC, C("6B5BD2"), GREEN][j])
    cr.restore(); cr.restore()
    line(cr, 300, 470, 335, 440, 16, SKIN)

def n_name(cr, t, d, m):
    vgrad(cr, PW, PH, C("1B1038"), C("4A1F5E"))
    glow(cr, 760, 150, 170, C("FFF3C4"), .4); circle(cr, 760, 150, 62, C("FFF3C4")); circle(cr, 786, 132, 56, C("2D1548"))
    _bed(cr, t)
    push(cr, 350, 360 + math.sin(t * 5) * 8, 1, -.15); _phone(cr, 0, 0, 150, screen=C("DCEBFF")); cr.restore(); line(cr, 300, 470, 340, 420, 16, SKIN)
    for i, (lbl, col, tc, t0) in enumerate([("Din: boss ka", C("5D6680"), CREAM, .4), ("Raat: MERI", ACC, INK, 1.3)]):
        k = back((t - t0) / .35)
        if k > 0:
            push(cr, 300 + i * 50, 110 + i * 110, k, -.05 + i * .08); rrect(cr, -190, -44, 380, 88, 44, col); text(cr, lbl, 0, 15, 44, tc, anchor="c", face="Lora"); cr.restore()
    k = back((t - d * .6) / .35) * (1 + .06 * math.sin(t * 12))
    if k > 0:
        push(cr, 640, 400, k, .1); rrect(cr, -150, -50, 300, 100, 18, RED); text(cr, "BADLA!", 0, 22, 62, WHITE, anchor="c", face="Lora"); cr.restore()

def n_why(cr, t, d, m):
    vgrad(cr, PW, PH, C("3A2A1E"), C("7A4A2B"))
    text(cr, "Tera din", 70, 110, 40, CREAM, face="Lora")
    rrect(cr, 70, 150, 820, 90, 20, C("2A1E15"))
    blocks = [("Office", C("5D6680"), 250), ("Boss", RED, 170), ("Kaam", C("6B5BD2"), 210), ("Traffic", C("8C8FA3"), 174)]
    x = 78
    for i, (lbl, col, w) in enumerate(blocks):
        k = ease((t - .3 - i * .55) / .35)
        if k > 0: rrect(cr, x, 158, w * k, 74, 14, col); text(cr, lbl, x + w / 2, 206, 30, WHITE, k, anchor="c")
        x += w + 4
    tap = math.sin(t * 16) * 8
    o = person(cr, 300, 660, 330, shirt=C("4F7DD9"), pose=dict(mouth="frown", look=.4, la=-8, la2=-60 + tap, ra=42, ra2=60 - tap, blink=(t % 2.4) < .12)); hx, hy = o["head"]
    dr = (t * 1.1) % 1; ell(cr, hx + 50, hy - 10 + dr * 40, 7, 10, C("8FD3FF"), 1 - dr)
    desk(cr, 130, 510, 420); rrect(cr, 380, 400, 130, 110, 8, INK); rrect(cr, 388, 408, 114, 86, 4, C("9ED8FF"))
    for j in range(3): rrect(cr, 160 + j * 5, 484 - j * 26, 120, 24, 4, [RED, ACC, TEAL][j])
    k = back((t - d * .55) / .35) * (1 + .05 * math.sin(t * 10))
    if k > 0:
        push(cr, 690, 400, k, .05); rrect(cr, -200, -80, 400, 160, 22, INK); text(cr, "Apna time", 0, -22, 34, CREAM, anchor="c"); text(cr, "0 min", 0, 52, 70, RED, anchor="c", face="Lora"); cr.restore()

def n_fix(cr, t, d, m):
    vgrad(cr, PW, PH, C("0F1838"), C("23346E"))
    for i in range(12): circle(cr, (i * 173) % PW, 260 + (i * 61) % 120, 2.5, WHITE, .3 + .3 * math.sin(t * 3 + i))
    rrect(cr, 70, 90, 820, 80, 20, C("0A1026")); x = 78
    for i, (col, w) in enumerate([(C("5D6680"), 230), (GREEN, 150), (C("6B5BD2"), 250), (C("8C8FA3"), 178)]):
        k = 1 if i != 1 else back((t - .5) / .4)
        if k > 0:
            rrect(cr, x, 98, w, 64, 12, col, min(1, k))
            if i == 1: text(cr, "20 min", x + w / 2, 142, 30, INK, min(1, k), anchor="c")
        x += w + 4
    k = back((t - 1.1) / .35)
    if k > 0:
        push(cr, 383, 220, k); poly(cr, [(-16, 0), (16, 0), (0, -30)], GREEN); rrect(cr, -130, 0, 260, 60, 30, GREEN); text(cr, "sirf tera", 0, 42, 32, INK, anchor="c"); cr.restore()
    _bed(cr, t, awake=False)
    rrect(cr, 780, 520, 110, 110, 8, C("4A3526")); push(cr, 835, 505, 1, math.pi / 2); _phone(cr, 0, 0, 90, screen=C("0A1026")); cr.restore()
    for i in range(3):
        ph = (t * .5 + i / 3) % 1; text(cr, "z", 300 + ph * 90 + i * 14, 420 - ph * 150, 40 + i * 12, CREAM, 1 - ph, face="Lora")
