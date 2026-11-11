"""Story scenes. Each fn(cr, t, d, mouth) draws into a 960x720 panel."""
import math
from chars import *

PW, PH = 960, 720
ACC = C("F7B248"); CREAM = C("F6F0E2"); TEAL = C("3FC1B0"); PINK = C("F07A9A"); GREEN = C("5BD18B")

def walk_pose(t, speed=7):
    s = math.sin(t * speed)
    return dict(swing=s, la=12 - s * 18, ra=12 + s * 18)

# ======================= Reel 1: Zeigarnik =======================
def z_bed(cr, t, d, m):
    vgrad(cr, PW, PH, C("151C45"), C("2A3572"))
    for i, (sx, sy) in enumerate([(120, 80), (300, 50), (480, 120), (90, 220), (560, 40), (380, 200)]):
        circle(cr, sx, sy, 2.5, WHITE, 0.4 + 0.4 * math.sin(t * 3 + i))
    glow(cr, 110, 100, 80, C("FFF3C4"), 0.3); circle(cr, 110, 100, 30, C("FFF3C4"))
    # bed
    rrect(cr, 70, 330, 36, 300, 10, C("6B4A2B"))
    rrect(cr, 90, 470, 660, 110, 18, C("5C6BC7"))
    ell(cr, 185, 455, 80, 34, WHITE)
    # person lying: head on pillow
    circle(cr, 200, 420, 46, SKIN)
    cr.new_path(); cr.arc(200, 404, 46, math.pi, math.pi * 2); src(cr, HAIR); cr.fill()
    bl = (t % 2.6) < 0.15
    for ex in (184, 216):
        if bl: line(cr, ex - 6, 424, ex + 6, 424, 4, DARK)
        else: circle(cr, ex, 424, 6, DARK); circle(cr, ex + 1.5, 420, 2, WHITE)
    line(cr, 192, 448, 208, 448, 4, DARK)
    # blanket with breathing
    br = math.sin(t * 2) * 4
    rrect(cr, 250, 430 - br, 500, 90 + br, 30, ACC)
    line(cr, 270, 470 - br, 730, 470 - br, 3, C("E09A2F"), .6)
    # thought bubbles
    for i, (bx, by, r) in enumerate([(270, 360, 10), (320, 320, 16), (380, 280, 22)]):
        circle(cr, bx, by, r * appear(t, 0.2 + i * .15, .3), WHITE, .95)
    k = back((t - 0.6) / 0.6)
    if k > 0:
        cr.save(); cr.translate(600, 190); cr.scale(max(k, 1e-3), max(k, 1e-3)); cloud(cr, 0, 0, 560, 250, WHITE, .97); cr.restore()
    for i, lbl in enumerate(["Reply to email", "Finish report", "Call back"]):
        a = appear(t, 1.1 + i * 0.6, .35)
        if a <= 0: continue
        yy = 140 + i * 56
        rr_path(cr, 470, yy - 22, 28, 28, 5); cr.set_line_width(4); src(cr, C("3B4790"), a); cr.stroke()
        text(cr, lbl, 514, yy + 2, 30, C("2A3572"), a)
    if t > 3:
        p = 1 + 0.15 * math.sin(t * 8)
        circle(cr, 285, 395, 22 * p, C("E5484D")); text(cr, "!", 285, 406, 32, WHITE, anchor="c")

def z_cafe(cr, t, d, m):
    vgrad(cr, PW, PH, C("F6DDB6"), C("EEC892"))
    rrect(cr, 0, 520, PW, 200, 0, C("C08A58"))
    for i in range(8): line(cr, i * 130, 520, i * 130 - 60, 720, 3, C("A8764A"), .5)
    for lx in (200, 520, 840):
        sw = math.sin(t * 1.5 + lx) * 6
        line(cr, lx, 0, lx + sw, 90, 3, DARK); poly(cr, [(lx + sw - 30, 120), (lx + sw + 30, 120), (lx + sw + 14, 90), (lx + sw - 14, 90)], C("2F3B6B"))
        glow(cr, lx + sw, 125, 60, C("FFE7A8"), .5)
    rrect(cr, 330, 180, 130, 100, 8, C("8B5E3C")); rrect(cr, 340, 190, 110, 80, 4, C("7FB3D5"))
    # customers at table
    person(cr, 580, 560, 300, shirt=C("3FA77A"), pose=dict(sit=True, face=1, la=40, la2=60, mouth="smile", look=-1, hairstyle="long"))
    person(cr, 770, 560, 300, shirt=C("D9644A"), pose=dict(sit=True, face=-1, ra=40, ra2=60, look=-1, hairstyle="bun"))
    rrect(cr, 520, 470, 330, 22, 8, C("6E4A2F")); rrect(cr, 670, 490, 24, 80, 4, C("6E4A2F"))
    circle(cr, 610, 462, 14, WHITE); circle(cr, 740, 462, 14, WHITE)
    # waiter walks in
    wx = -80 + 420 * ease(t / 1.8)
    pose = walk_pose(t) if t < 1.8 else dict(ra=95, ra2=-40, la=10)
    pose.update(dict(apron=True, look=1, mouth="smile"))
    o = person(cr, wx, 600, 330, shirt=C("23263A"), pants=C("23263A"), pose=pose)
    if t >= 1.8:
        rx, ry = o["rh"]; rrect(cr, rx - 4, ry - 34, 30, 40, 3, WHITE); line(cr, rx + 2, ry - 24, rx + 20, ry - 24, 2, DARK, .5)
    pay = d * 0.62
    for i in range(3):
        a = appear(t, 2.0 + i * .45, .35)
        fly = ease((t - pay - i * .12) / .8)
        if a <= 0: continue
        sx, sy = 250 + i * 80, 130 - fly * 160 + math.sin(t * 2 + i) * 5
        cr.save(); cr.translate(sx, sy); cr.rotate(-.15 + i * .15)
        rrect(cr, -30, -40, 60, 80, 5, WHITE, a * (1 - fly))
        for j in range(4): line(cr, -18, -24 + j * 14, 18 - (j % 2) * 10, -24 + j * 14, 3, C("9AA3B5"), a * (1 - fly))
        cr.restore()
    if t > pay:
        k = back((t - pay) / .5)
        cr.save(); cr.translate(690, 400); cr.scale(max(k, 1e-3), max(k, 1e-3)); cr.rotate(-.12)
        rr_path(cr, -70, -26, 140, 52, 8); cr.set_line_width(6); src(cr, C("2E9E5B")); cr.stroke()
        text(cr, "PAID", 0, 14, 38, C("2E9E5B"), anchor="c"); cr.restore()

def _openring(cr, x, y, r, c, t, spd, gap=1.0, w=14):
    a0 = t * spd
    ring(cr, x, y, r, w, c, 1, a0, a0 + 2 * math.pi - gap)

def z_effect(cr, t, d, m):
    vgrad(cr, PW, PH, C("2B2758"), C("4A3E8E"))
    rrect(cr, 0, 600, PW, 120, 0, C("231F48"))
    o = person(cr, 230, 640, 430, shirt=C("4F7DD9"), pose=dict(mouth="flat", look=1, ra=150, ra2=40, blink=(t % 3.1) < .14))
    hx, hy = o["head"]
    drop = (t * 0.8) % 1
    ell(cr, hx + 50, hy - 20 + drop * 40, 7, 10, C("8FD3FF"), 1 - drop)
    for i, (bx, by, r) in enumerate([(310, 230, 12), (350, 190, 18)]):
        circle(cr, bx, by, r, WHITE, .9)
    k = back((t - .2) / .6)
    cr.save(); cr.translate(600, 190); cr.scale(max(k, 1e-3), max(k, 1e-3)); cloud(cr, 0, 0, 480, 230, WHITE, .95)
    for i, (c, spd) in enumerate([(ACC, 2.0), (TEAL, -1.4), (PINK, 1.1)]):
        p = 1 + 0.08 * math.sin(t * 5 + i * 2)
        _openring(cr, -120 + i * 120, 10, 40 * p, c, t, spd)
    cr.restore()
    for i in range(3):
        ph = ((t * 0.9 + i / 3) % 1)
        x = 470 - ph * 140; y = 300 + ph * 40
        line(cr, x, y, x - 30, y + 9, 6, ACC, 1 - ph); poly(cr, [(x - 40, y + 12), (x - 26, y), (x - 24, y + 16)], ACC, 1 - ph)

def z_plan(cr, t, d, m):
    vgrad(cr, PW, PH, C("11394A"), C("1E5C68"))
    rrect(cr, 0, 600, PW, 120, 0, C("0D2B38"))
    wr = math.sin(t * 9) * 8 if t < d - 1 else 0
    person(cr, 250, 640, 400, shirt=C("F2A93B"), pose=dict(sit=True, face=1, ra=75 + wr * .4, ra2=30, la=40, la2=50, look=1, blink=(t % 3.3) < .14))
    rrect(cr, 180, 500, 420, 26, 8, C("8B5E3C")); rrect(cr, 520, 520, 26, 120, 4, C("6E4A2F"))
    cr.save(); cr.translate(390, 486); cr.rotate(-.06); rrect(cr, -70, -24, 140, 40, 4, WHITE)
    for j in range(3):
        L = 110 * min(1, max(0, (t - .5 - j * 1.2) / 1.0))
        if L > 0: line(cr, -58, -14 + j * 11, -58 + L, -14 + j * 11, 3, C("2A3572"))
    cr.restore()
    for i, c in enumerate([ACC, TEAL, PINK]):
        x, y = 470 + i * 150, 190
        cl = ease((t - 1.0 - i * 1.1) / .6)
        gap = 1.0 * (1 - cl)
        a0 = (t * 1.6 * (1 - cl)) + i
        ring(cr, x, y, 50, 14, c, 1, a0, a0 + 2 * math.pi - gap)
        if cl >= 1:
            k = back((t - 1.6 - i * 1.1) / .4)
            cr.save(); cr.translate(x, y); cr.scale(max(k, 1e-3), max(k, 1e-3)); polyline(cr, [(-20, 2), (-5, 18), (24, -16)], 10, GREEN); cr.restore()

def z_tonight(cr, t, d, m):
    k = ease((t - 1.2) / 2.0)
    vgrad(cr, PW, PH, lerpc(C("6FA8DC"), C("141B40"), k), lerpc(C("A9CCE8"), C("2A3572"), k))
    rrect(cr, 600, 60, 260, 200, 10, C("3B4790")); rrect(cr, 612, 72, 236, 176, 6, lerpc(C("BFE0F7"), C("0B1030"), k))
    my = 260 - 140 * k
    cr.save(); rr_path(cr, 612, 72, 236, 176, 6); cr.clip(); glow(cr, 730, my, 80, C("FFF3C4"), .4 * k); circle(cr, 730, my, 30, C("FFF3C4"), k); cr.restore()
    rrect(cr, 0, 600, PW, 120, 0, lerpc(C("5E7FA6"), C("0F1533"), k))
    st = ease((t - 2.4) / 1.0)
    person(cr, 250, 640, 400, shirt=C("3FA77A"), pose=dict(sit=True, face=1, ra=60 + 110 * st, ra2=10 * st, la=40 + 120 * st, la2=10 * st, mouth="smile", blink=st > .5, look=1))
    rrect(cr, 180, 500, 460, 26, 8, C("8B5E3C")); rrect(cr, 560, 520, 26, 120, 4, C("6E4A2F"))
    # laptop closing
    lid = 1 - ease((t - 0.6) / 0.7)
    rrect(cr, 380, 488, 170, 14, 4, C("9AA3B5"))
    if lid > 0.02:
        hgt = 110 * lid
        poly(cr, [(390, 490), (540, 490), (548, 490 - hgt), (398, 490 - hgt)], C("5D6680"))
        poly(cr, [(398, 486), (532, 486), (538, 494 - hgt), (404, 494 - hgt)], C("9ED8FF"), .9 * lid)
    rrect(cr, 255, 470, 110, 30, 4, WHITE); text(cr, "Next step →", 262, 492, 18, C("2A3572"))
    if t > 3.5:
        for i in range(3):
            ph = ((t - 3.5) * 0.5 + i / 3) % 1
            text(cr, "z", 330 + ph * 60 + i * 10, 260 - ph * 120, 30 + i * 8, CREAM, 1 - ph)

def end_card(cr, t, d, m):
    vgrad(cr, PW, PH, C("2A2F6A"), C("4B3F8F"))
    for i in range(14):
        ph = (t * .25 + i * .071) % 1
        circle(cr, (i * 151) % PW, PH - ph * PH, 4 + i % 3 * 2, ACC, .35 * (1 - ph))
    k = back(t / .6)
    cr.save(); cr.translate(480, 640); cr.scale(max(k, 1e-3), max(k, 1e-3)); owl(cr, 0, 0, 470, t, m, look=(0, .2), wave=1); cr.restore()
    b = math.sin(t * 4) * 8
    cr.save(); cr.translate(150, 230 + b); s = appear(t, .5, .4)
    poly(cr, [(-40, -60), (40, -60), (40, 60), (0, 30), (-40, 60)], ACC, s); cr.restore()
    cr.save(); cr.translate(810, 230 - b); p = (1 + .1 * math.sin(t * 6)) * appear(t, .8, .4); cr.scale(max(p, 1e-3), max(p, 1e-3))
    cr.new_path(); cr.move_to(0, 30); cr.curve_to(-70, -20, -30, -75, 0, -40); cr.curve_to(30, -75, 70, -20, 0, 30); src(cr, PINK); cr.fill(); cr.restore()

# ======================= Reel 2: If-then =======================
def i_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("1E2A4E"), C("2D4176"))
    rrect(cr, 0, 610, PW, 110, 0, C("172040"))
    ox, oy = 470, 560
    line(cr, ox, oy, 900, oy, 4, CREAM, .6); line(cr, ox, oy, ox, 120, 4, CREAM, .6)
    pts = [(ox + 10, 500), (ox + 120, 470), (ox + 230, 380), (ox + 330, 250), (ox + 410, 150)]
    pr = ease((t - .5) / 2.2)
    n = pr * (len(pts) - 1); i0 = int(n)
    seg = pts[:i0 + 1]
    if i0 < len(pts) - 1:
        f = n - i0; a, b = pts[i0], pts[i0 + 1]; seg = seg + [(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)]
    if len(seg) > 1: polyline(cr, seg, 10, ACC)
    circle(cr, seg[-1][0], seg[-1][1], 12, ACC)
    if pr > .98:
        k = back((t - 2.7) / .5); cr.save(); cr.translate(820, 120); cr.scale(max(k, 1e-3), max(k, 1e-3)); text(cr, "≈3×", 0, 0, 56, ACC, anchor="c", face="Lora"); cr.restore()
    text(cr, "1×", ox + 10, 540, 28, CREAM, .7)
    o = person(cr, 220, 640, 420, shirt=C("D9644A"), pose=dict(ra=165, ra2=0, mouth="smile", look=1))
    hx, hy = o["rh"]
    k = back((t - .2) / .5)
    cr.save(); cr.translate(hx + 40, hy - 50); cr.scale(max(k, 1e-3), max(k, 1e-3)); cr.rotate(math.sin(t * 2) * .05)
    rrect(cr, -110, -50, 220, 100, 12, WHITE); text(cr, "If…  then…", 0, 14, 38, C("2A3572"), anchor="c", face="Lora"); cr.restore()

def i_gap(cr, t, d, m):
    vgrad(cr, PW, PH, C("8EC5E8"), C("D6ECF7"))
    for i, cx in enumerate((150, 520, 800)):
        cloud(cr, (cx + t * 12) % 1100 - 70, 90 + i * 25, 160, 70, WHITE, .9)
    poly(cr, [(0, 430), (330, 430), (360, 720), (0, 720)], C("6A9A55"))
    poly(cr, [(630, 430), (960, 430), (960, 720), (600, 720)], C("6A9A55"))
    rrect(cr, 0, 430, 340, 30, 0, C("85B86A")); rrect(cr, 625, 430, 340, 30, 0, C("85B86A"))
    g = cairo.LinearGradient(0, 430, 0, 720); g.add_color_stop_rgb(0, .1, .14, .25); g.add_color_stop_rgb(1, .02, .03, .08)
    cr.move_to(330, 430); cr.line_to(630, 430); cr.line_to(600, 720); cr.line_to(360, 720); cr.close_path(); cr.set_source(g); cr.fill()
    scratch = math.sin(t * 8) * 10
    person(cr, 210, 432, 330, shirt=C("4F7DD9"), pose=dict(ra=165 + scratch * .3, ra2=60, look=1, mouth="flat"))
    line(cr, 800, 432, 800, 250, 6, C("5A4632"))
    wv = math.sin(t * 4) * 12
    poly(cr, [(803, 255), (900, 275 + wv * .5), (803, 320)], ACC)
    text(cr, "GOAL", 815, 296, 22, C("2A3572"))
    for i, (lbl, x0) in enumerate([("When?", 410), ("Where?", 520)]):
        a = appear(t, 1.4 + i * 1.0, .4)
        y = 360 + math.sin(t * 2.5 + i) * 14
        text(cr, "?", x0 + 20, y - 40, 80, C("E5484D"), a, face="Lora", anchor="c")
        text(cr, lbl, x0 + 20, y + 10, 26, C("2A3572"), a, anchor="c")

def i_domino(cr, t, d, m):
    vgrad(cr, PW, PH, C("1B2440"), C("27345E"))
    rrect(cr, 0, 560, PW, 160, 0, C("141B33"))
    person(cr, 120, 560, 300, shirt=C("3FA77A"), pose=dict(ra=95, ra2=-10, look=1, mouth="o" if (t % 4.5) > 1.6 else "smile"))
    P = 4.5; ph = t % P
    a1 = ease((ph - .6) / .5) * 0.52
    a2 = ease((ph - 1.0) / .7) * (math.pi / 2)
    fade = 1 - ease((ph - 3.9) / .5)
    def tile(x, ang, lbl, sub, c):
        cr.save(); cr.translate(x + 50, 560); cr.rotate(ang)
        rrect(cr, -100, -230, 100, 230, 14, c, fade)
        rr_path(cr, -100, -230, 100, 230, 14); cr.set_line_width(4); src(cr, WHITE, .5 * fade); cr.stroke()
        cr.save(); cr.translate(-50, -115); cr.rotate(-math.pi / 2)
        text(cr, lbl, 0, 12, 38, WHITE, fade, anchor="c"); cr.restore()
        cr.restore()
        text(cr, sub, x, 610, 24, CREAM, fade * (1 - min(1, ang)), anchor="c")
    tile(370, a2, "THEN", "", TEAL)
    tile(270, a1, "IF", "", ACC)
    text(cr, "cue", 320, 640, 26, ACC, .9, anchor="c"); text(cr, "action", 420, 640, 26, TEAL, .9, anchor="c")
    if ph > 1.6:
        k = back((ph - 1.6) / .4) * fade
        cr.save(); cr.translate(700, 200); cr.scale(max(k, 1e-3), max(k, 1e-3))
        rrect(cr, -150, -50, 300, 100, 20, WHITE); text(cr, "Automatic ✓", 0, 14, 36, C("2E9E5B"), anchor="c"); cr.restore()

def i_evidence(cr, t, d, m):
    vgrad(cr, PW, PH, C("14304A"), C("1E4870"))
    base = 580
    line(cr, 330, base, 820, base, 4, CREAM, .6)
    gr = ease((t - .8) / 1.4)
    for x, v, c, lbl, num in [(370, .91, ACC, "Made a plan", "91%"), (590, .34, C("7A8BB8"), "Others", "~1/3")]:
        h = 420 * v * gr
        rrect(cr, x, base - h, 150, h + 8, 10, c)
        if gr > 0.05:
            val = num if gr >= 1 else (f"{int(91 * gr)}%" if num == "91%" else f"{int(34 * gr)}%")
            text(cr, val, x + 75, base - h - 18, 46, c, face="Lora", anchor="c")
        text(cr, lbl, x + 75, base + 44, 26, CREAM, anchor="c")
    person(cr, 170, 640, 400, shirt=C("D9644A"), pose=dict(ra=100, ra2=-20, look=1, mouth="smile", blink=(t % 3) < .13))

def i_morning(cr, t, d, m):
    vgrad(cr, PW, PH, C("FFDDA0"), C("F7B267"))
    rrect(cr, 600, 50, 260, 210, 10, C("C47A3A")); rrect(cr, 612, 62, 236, 186, 6, C("FFE9B8"))
    sy = 220 - 60 * ease(t / 3); glow(cr, 730, sy, 110, C("FF9D3C"), .5); circle(cr, 730, sy, 40, C("FFB347"))
    circle(cr, 200, 160, 92, C("7A4A2A")); circle(cr, 200, 160, 80, WHITE)
    for i in range(12):
        a = i * math.pi / 6; line(cr, 200 + math.sin(a) * 66, 160 - math.cos(a) * 66, 200 + math.sin(a) * 74, 160 - math.cos(a) * 74, 4, DARK)
    ha = 7 / 12 * 2 * math.pi
    line(cr, 200, 160, 200 + math.sin(ha) * 38, 160 - math.cos(ha) * 38, 9, DARK); line(cr, 200, 160, 200, 102, 6, DARK)
    sa = t * 2 * math.pi / 6; line(cr, 200, 160, 200 + math.sin(sa) * 62, 160 - math.cos(sa) * 62, 2.5, C("E5484D"))
    text(cr, "7:00", 200, 290, 34, C("7A4A2A"), anchor="c")
    rrect(cr, 0, 600, PW, 120, 0, C("C98F5A"))
    person(cr, 560, 640, 400, shirt=C("4F7DD9"), pose=dict(sit=True, face=-1, ra=55, ra2=60, la=55, la2=60, look=-1, mouth="smile", blink=(t % 3.4) < .14, hairstyle="long"))
    rrect(cr, 260, 520, 460, 24, 8, C("8B5E3C")); rrect(cr, 300, 540, 24, 100, 4, C("6E4A2F"))
    # book
    rrect(cr, 470, 420, 160, 100, 6, C("2E9E5B")); rrect(cr, 480, 428, 140, 84, 4, WHITE)
    f = (t * 0.8) % 1; pw = 70 * math.cos(f * math.pi)
    poly(cr, [(550, 428), (550 + pw, 432), (550 + pw, 508), (550, 512)], C("F2EEE6"))
    pg = min(10, 1 + int(t * 0.8 * 1.3)); text(cr, f"page {pg}/10", 550, 400, 24, C("7A4A2A"), anchor="c")
    # mug + steam
    rrect(cr, 330, 450, 70, 74, 10, WHITE); ring(cr, 404, 486, 16, 8, WHITE, 1, -1.4, 1.4)
    for i in range(3):
        pts = [(345 + i * 20 + math.sin(t * 3 + i + k * .6) * 8, 440 - k * 14) for k in range(9)]
        polyline(cr, pts, 5, WHITE, .6)

# ======================= Reel 3: Fabius =======================
def f_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("3A1C3F"), C("C4643A"))
    glow(cr, 480, 420, 300, C("FFB15C"), .35)
    for i, x in enumerate((60, 260, 700, 900)):
        poly(cr, [(x - 120, 600), (x, 470 - i % 2 * 40), (x + 140, 600)], C("2A1530"), .7)
    rrect(cr, 0, 600, PW, 120, 0, C("1E0F22"))
    elephant(cr, 790, 600, 230, t)
    sw = math.sin(t * 3) * 8
    carthage(cr, 620, 610, 400, ra=150 + sw, ra2=10, sword=True, look=-1, mouth="frown")
    roman(cr, 250, 610, 400, ra=60, ra2=70, la=60, la2=70, shield=None, look=1, mouth="smile")
    k = back((t - .5) / .5) * (1 + .06 * math.sin(t * 5))
    cr.save(); cr.translate(440, 260); cr.scale(max(k, 1e-3), max(k, 1e-3)); text(cr, "VS", 0, 20, 90, ACC, anchor="c", face="Lora"); cr.restore()

ITALY = [(250, 120), (420, 90), (560, 110), (620, 170), (600, 230), (650, 330), (720, 400), (800, 450), (790, 480),
         (860, 540), (900, 600), (870, 610), (800, 560), (760, 560), (760, 620), (720, 700), (690, 690), (700, 600),
         (650, 520), (560, 450), (480, 380), (400, 300), (330, 240), (260, 200)]
def _it(p): return (40 + p[0] * 0.82, 30 + p[1] * 0.9)

def f_map(cr, t, d, m):
    vgrad(cr, PW, PH, C("1F4E7A"), C("2B6A9A"))
    for i in range(6):
        y = 80 + i * 110 + math.sin(t + i) * 4
        polyline(cr, [(x, y + math.sin(x / 40 + t * 2) * 4) for x in range(0, PW + 40, 40)], 2, WHITE, .1)
    poly(cr, [_it(p) for p in ITALY], C("E8D5A6"))
    poly(cr, [_it(p) for p in [(220, 60), (600, 40), (640, 120), (260, 130)]], C("B9BFC9"))
    for x in range(260, 620, 60):
        poly(cr, [_it((x, 110)), _it((x + 30, 50)), _it((x + 60, 110))], WHITE, .8)
    rx, ry = _it((480, 380))
    p = 1 + .25 * math.sin(t * 6)
    glow(cr, rx, ry, 40 * p, C("E5484D"), .6); circle(cr, rx, ry, 10, C("E5484D"))
    text(cr, "ROME", rx - 16, ry + 8, 26, C("8A1F1F"), anchor="r")
    path = [_it(q) for q in [(300, 40), (320, 150), (360, 200), (440, 250), (520, 300), (580, 360), (640, 430)]]
    pr = ease((t - .4) / 3.2); n = pr * (len(path) - 1); i0 = int(n)
    seg = path[:i0 + 1]
    if i0 < len(path) - 1:
        f = n - i0; a, b = path[i0], path[i0 + 1]; seg = seg + [(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)]
    if len(seg) > 1: polyline(cr, seg, 7, C("C23B33"), dash=[18, 12])
    hx, hy = seg[-1]
    cr.save(); cr.translate(hx, hy); elephant(cr, -30, 20, 70, t, walk=1); cr.restore()
    for i, (q, tt) in enumerate([((340, 180), 1.1), ((460, 260), 2.2)]):
        k = back((t - tt) / .4)
        if k <= 0: continue
        bx, by = _it(q); cr.save(); cr.translate(bx + 40, by); cr.scale(max(k, 1e-3), max(k, 1e-3))
        circle(cr, 0, 0, 26, C("C23B33")); line(cr, -12, -12, 12, 12, 5, WHITE); line(cr, 12, -12, -12, 12, 5, WHITE); cr.restore()
    text(cr, "217 BC", 40, 680, 58, CREAM, face="Lora")

def f_hills(cr, t, d, m):
    vgrad(cr, PW, PH, C("F6C77F"), C("EC9A5C"))
    circle(cr, 820, 110, 50, C("FFE3A3"))
    poly(cr, [(0, 330), (200, 250), (420, 280), (650, 230), (960, 290), (960, 720), (0, 720)], C("9A6B4C"))
    poly(cr, [(0, 420), (300, 380), (600, 420), (960, 390), (960, 720), (0, 720)], C("C9925D"))
    rrect(cr, 0, 560, PW, 160, 0, C("D8A86A")); rrect(cr, 0, 600, PW, 26, 0, C("E8C38A"))
    off = (t * 28) % 300
    rx = 120 + t * 26
    for i in range(3):
        k = i * 70
        roman(cr, rx + k, 290 - (i == 0) * 6, 130 + (i == 0) * 20, **dict(walk_pose(t + i), spear=(i > 0), look=1, shield=ROMAN_RED, la=20))
    ax = 340 + t * 26
    elephant(cr, ax + 220, 640, 150, t, walk=1)
    for i in range(3):
        carthage(cr, ax + i * 70, 640, 150, **dict(walk_pose(t + i * .7), look=1))
    # supply wagon cut
    wx = 90
    rrect(cr, wx - 60, 560, 120, 50, 6, C("8B5E3C")); circle(cr, wx - 35, 615, 16, DARK); circle(cr, wx + 35, 615, 16, DARK)
    for j in range(3): rrect(cr, wx - 50 + j * 34, 530, 30, 30, 4, C("D9B98A"))
    k = back((t - 2.2) / .4)
    if k > 0:
        cr.save(); cr.translate(wx, 560); cr.scale(max(k, 1e-3), max(k, 1e-3)); line(cr, -46, -46, 46, 46, 14, C("E5484D")); line(cr, 46, -46, -46, 46, 14, C("E5484D")); cr.restore()
    if t > 3.5:
        for i in range(3):
            ph = ((t - 3.5) * 0.9 + i / 3) % 1
            x0, y0 = rx + 100 + i * 40, 300
            x1, y1 = ax + 60 + i * 50, 560
            x = x0 + (x1 - x0) * ph; y = y0 + (y1 - y0) * ph - math.sin(ph * math.pi) * 60
            line(cr, x, y, x - 14, y - 10, 4, DARK, 1 - ph * .5)

def f_cannae(cr, t, d, m):
    vgrad(cr, PW, PH, C("6E3A30"), C("C47A4C"))
    rrect(cr, 0, 300, PW, 420, 0, C("A86B42"))
    for i in range(10): circle(cr, (i * 137 + t * 30) % PW, 320 + (i * 53) % 340, 30, C("D9A070"), .15)
    # roman block in centre
    for r in range(4):
        for c in range(7):
            x = 300 + c * 50 + math.sin(t * 6 + r + c) * 2; y = 380 + r * 52
            shake = 3 * math.sin(t * 20 + c) if t > 2.6 else 0
            circle(cr, x + shake, y - 18, 11, SKIN); cr.new_path(); cr.arc(x + shake, y - 20, 12, math.pi, 2 * math.pi); src(cr, STEEL); cr.fill()
            rrect(cr, x - 14 + shake, y - 6, 28, 30, 5, ROMAN_RED)
    # carthaginian pincer: two wings sweep around the roman block
    wr = ease((t - .6) / 2.4)
    cx, cy = 450, 440
    for side in (0, math.pi):
        spread = 0.25 + wr * 1.15
        R = 330 - wr * 60
        for i in range(9):
            ang = side + (i / 8 - .5) * 2 * spread
            x = cx + math.cos(ang) * R; y = cy + math.sin(ang) * R * 0.55
            circle(cr, x, y - 18, 11, SKIN2); cr.new_path(); cr.arc(x, y - 20, 12, math.pi, 2 * math.pi); src(cr, BRONZE); cr.fill()
            rrect(cr, x - 14, y - 6, 28, 30, 5, PURPLE)
    for i in range(3):
        ph = (t * 1.2 + i / 3) % 1
        if wr > .3:
            for side in (-1, 1):
                line(cr, cx + side * (260 - ph * 80), cy - 10, cx + side * (240 - ph * 80), cy - 10, 5, ACC, .6 * (1 - ph))
    # banner falls
    fall = ease((t - 3.2) / .9)
    cr.save(); cr.translate(475, 560); cr.rotate(fall * 1.3)
    line(cr, 0, 0, 0, -330, 6, C("5A4632")); poly(cr, [(0, -330), (80, -310), (0, -280)], ROMAN_RED)
    cr.restore()
    if t > 2.6:
        a = .35 * (0.5 + 0.5 * math.sin(t * 9))
        cr.rectangle(0, 0, PW, PH); src(cr, C("E5484D"), a * (1 - ease((t - 4.5) / 1))); cr.fill()
    text(cr, "Cannae, 216 BC", 40, 70, 44, CREAM, face="Lora")

def f_lesson(cr, t, d, m):
    vgrad(cr, PW, PH, C("1A2142"), C("2D3B6E"))
    rrect(cr, 0, 610, PW, 110, 0, C("141A36"))
    roman(cr, 230, 620, 420, ra=60, ra2=70, la=60, la2=70, shield=None, look=1, mouth="smile", blink=(t % 3.6) < .14)
    cx, cy = 600, 330
    pr = min(1, t / d)
    ring(cr, cx, cy, 230, 10, C("3B4790"))
    ring(cr, cx, cy, 230, 10, ACC, 1, -math.pi / 2, -math.pi / 2 + 2 * math.pi * pr)
    top = 1 - pr; bot = pr
    poly(cr, [(cx - 110, cy - 170), (cx + 110, cy - 170), (cx + 8, cy - 4), (cx - 8, cy - 4)], WHITE, .15)
    poly(cr, [(cx - 8, cy + 4), (cx + 8, cy + 4), (cx + 110, cy + 170), (cx - 110, cy + 170)], WHITE, .15)
    h1 = 140 * top
    if h1 > 2:
        w = 8 + (110 - 8) * (h1 / 166)
        poly(cr, [(cx - w, cy - 4 - h1), (cx + w, cy - 4 - h1), (cx + 8, cy - 4), (cx - 8, cy - 4)], ACC)
    h2 = 140 * bot
    if h2 > 2:
        poly(cr, [(cx - 110, cy + 170), (cx + 110, cy + 170), (cx + 110 - h2 * .6, cy + 170 - h2), (cx - 110 + h2 * .6, cy + 170 - h2)], ACC)
    line(cr, cx, cy, cx, cy + 170 - h2, 4, ACC, .9)
    rrect(cr, cx - 130, cy - 186, 260, 18, 6, C("8B5E3C")); rrect(cr, cx - 130, cy + 168, 260, 18, 6, C("8B5E3C"))
    polyline(cr, [(cx - 110, cy - 170), (cx - 8, cy - 4), (cx - 110, cy + 170)], 5, WHITE, .7)
    polyline(cr, [(cx + 110, cy - 170), (cx + 8, cy - 4), (cx + 110, cy + 170)], 5, WHITE, .7)

SCENES = {
    "01_zeigarnik": [z_bed, z_cafe, z_effect, z_plan, z_tonight, end_card],
    "02_if_then": [i_hook, i_gap, i_domino, i_evidence, i_morning, end_card],
    "03_fabian": [f_hook, f_map, f_hills, f_cannae, f_lesson, end_card],
}
