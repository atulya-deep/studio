"""Batch 2 scenes, part A: spotlight, IKEA, doorway, Wald, emu. fn(cr, t, d, mouth) on a 960x720 panel."""
from kit2 import *

# ======================= 04 Spotlight effect =======================
def s_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("14122B"), C("241F4A")); rrect(cr, 0, 600, PW, 120, 0, C("0F0D22"))
    for i, x in enumerate((110, 240, 730, 850)):
        f = -1 if x < 480 else 1
        o2 = person(cr, x, 650, 220, shirt=C("3B4790"), pants=C("23263A"), pose=dict(look=f, ra=35, ra2=-115, la=35, la2=-115, mouth="flat"))
        rx, ry = o2["rh"]; rrect(cr, rx - 16 + f * 4, ry - 26, 22, 34, 4, C("8FD3FF"))
    sx = 480 + math.sin(t * .8) * 14
    cr.new_path(); cr.move_to(sx - 30, 0); cr.line_to(sx + 30, 0); cr.line_to(650, 612); cr.line_to(310, 612); cr.close_path(); src(cr, C("FFF3C4"), .2 + .04 * math.sin(t * 3)); cr.fill()
    ell(cr, 480, 614, 170, 22, C("FFF3C4"), .35)
    o = person(cr, 480, 614, 320, shirt=C("D9644A"), pose=dict(mouth="o", la=30, la2=-80, ra=30, ra2=-80, blink=(t % 2.4) < .12))
    hx, hy = o["head"]; dr = (t * .9) % 1; ell(cr, hx + 52, hy - 10 + dr * 40, 7, 10, C("8FD3FF"), 1 - dr)
    bubble(cr, 480, 120, 400, 70, "Everyone saw that...", 30, back((t - 1) / .4), tail=0)

def s_shirt(cr, t, d, m):
    room(cr, C("E9EEF7"), C("CBD5E8"), C("9AA7C2"))
    rrect(cr, 40, 240, 150, 360, 6, BROWN); rrect(cr, 52, 252, 126, 336, 4, C("A87448")); circle(cr, 164, 430, 8, ACC)
    for i, x in enumerate((640, 800)):
        person(cr, x, 610, 250, shirt=[C("3FA77A"), C("6B5BD2")][i], pose=dict(sit=True, face=-1, look=-.2, la=45, la2=70, ra=45, ra2=70, hairstyle=["long", "short"][i], blink=((t + i) % 3) < .12))
    rrect(cr, 560, 480, 330, 22, 8, BROWN); rrect(cr, 600, 462, 70, 18, 3, WHITE); rrect(cr, 760, 462, 70, 18, 3, WHITE)
    arr = min(1, t / 2.2); wx = 150 + 250 * ease(arr)
    pose = walk_pose(t) if arr < 1 else dict(la=25, la2=-70, ra=25, ra2=-70)
    pose.update(mouth="flat", look=1, blink=(t % 2.8) < .12)
    o = person(cr, wx, 630, 340, shirt=YEL, pose=pose); u = o["u"]; hx, hy = o["head"]
    cy = 630 - 62 * u; circle(cr, wx, cy, 9 * u, WHITE); circle(cr, wx - 3 * u, cy - 2 * u, 1.3 * u, INK); circle(cr, wx + 3 * u, cy - 2 * u, 1.3 * u, INK)
    cr.new_path(); cr.arc(wx, cy + 1 * u, 4.5 * u, .3, math.pi - .3); cr.set_line_width(1.2 * u); src(cr, INK); cr.stroke()
    circle(cr, hx - 8 * u, hy + 5 * u, 3 * u, PINK, .7); circle(cr, hx + 8 * u, hy + 5 * u, 3 * u, PINK, .7)
    bubble(cr, wx + 30, 170, 330, 62, "The uncool T-shirt", 28, back((t - 2.4) / .4), tail=-1)

def s_stats(cr, t, d, m):
    vgrad(cr, PW, PH, C("14304A"), C("1E4870"))
    for r, (lbl, n, col, t0, big) in enumerate([("Wearers guessed", 4, ACC, .6, "about half"), ("Actually noticed", 2, TEAL, d * .45, "about 1 in 4")]):
        y = 210 + r * 240
        text(cr, lbl, 70, y - 70, 30, CREAM, appear(t, t0 - .3, .3))
        for i in range(8):
            x = 100 + i * 70; lit = i < n and t > t0 + i * .25
            c2 = col if lit else C("33507A")
            circle(cr, x, y - 14, 20, c2); rrect(cr, x - 24, y + 10, 48, 50, 16, c2)
        text(cr, big, 672, y + 36, 40, col, appear(t, t0 + n * .25, .4), face="Lora")

def s_movie(cr, t, d, m):
    vgrad(cr, PW, PH, C("2B2758"), C("4A3E8E")); rrect(cr, 0, 610, PW, 110, 0, C("231F48"))
    data = [(170, C("4F7DD9"), "Is my hair ok?", "short", -1), (460, C("3FA77A"), "Did I lock the door?", "long", 1), (720, C("D9644A"), "What's for lunch?", "bun", -1)]
    for i, (x, col, txt, hs, lk) in enumerate(data):
        ell(cr, x, 632, 100, 16, C("FFF3C4"), .25)
        person(cr, x, 630, 290, shirt=col, pose=dict(look=lk * math.sin(t * .8 + i), hairstyle=hs, mouth="flat", blink=((t + i * .7) % 3) < .12, ra=150 if i == 0 else 12, ra2=60 if i == 0 else 8))
        k = back((t - .5 - i * .9) / .5)
        if k > 0:
            push(cr, x + 10, 200 - (i % 2) * 50, k); cloud(cr, 0, 0, 300, 120, WHITE, .97); text(cr, txt, 0, 12, 22, DK, anchor="c"); cr.restore()
            circle(cr, x + 20, 300 - (i % 2) * 40, 9 * min(1, k), WHITE, .9)

def s_use(cr, t, d, m):
    room(cr, C("E9F3EC"), C("CFE5D6"), C("9DBFA8"))
    for i in range(4): rrect(cr, 500 + i * 80, 560 - i * 42, 500, 200, 0, lerpc(C("B9C7BE"), C("8FA398"), i / 3))
    for i in range(2):
        x = PW + 120 - ((t * 85 + i * 480) % (PW + 300))
        o2 = person(cr, x, 600, 200, shirt=[C("6B5BD2"), C("D9644A")][i], pose=dict(walk_pose(t + i, 6), look=-1, ra=35, ra2=-115, hairstyle=["long", "short"][i]))
        rx, ry = o2["rh"]; rrect(cr, rx - 22, ry - 26, 20, 30, 4, C("8FD3FF"))
    trip = ease((t - 1) / .3) - ease((t - 2.3) / .5); ok = t > 2.9
    push(cr, 320, 640, 1, rot=trip * .55)
    o = person(cr, 0, 0, 320, shirt=TEAL, pose=dict(mouth="o" if trip > .3 else "smile", ra=165 if ok else 20 + trip * 110, la=20 + trip * 90, blink=ok and (t % 2.5) < .12, look=1))
    cr.restore()
    if trip > .3: text(cr, "!", 400, 250, 90, RED, face="Lora")
    bubble(cr, 330, 150, 440, 70, "Noticed by: almost nobody", 28, back((t - 3) / .4))
    check(cr, 600, 150, 40, GREEN, back((t - 3.4) / .4))

# ======================= 05 IKEA effect =======================
def _shelf(cr, x, y, k, rot):
    push(cr, x, y, k, rot)
    rrect(cr, -130, -380, 18, 380, 4, C("D9A066")); rrect(cr, 112, -380, 18, 380, 4, C("D9A066"))
    for yy in (-372, -252, -132, -20): rrect(cr, -130, yy, 260, 16, 4, C("C68A4E"))
    for bx, bw, bh, col in [(-104, 26, 90, RED), (-74, 22, 78, TEAL), (-48, 30, 96, DK), (22, 24, 84, ACC)]: rrect(cr, bx, -252 - bh, bw, bh, 3, col)
    rrect(cr, 24, -160, 44, 28, 4, C("C2603C")); circle(cr, 46, -182, 24, C("3FA77A"))
    cr.restore()

def k_hook(cr, t, d, m):
    room(cr, C("F3E9DC"), C("E6D3BC"), C("B98F65"))
    _shelf(cr, 610, 602, 1, .06 + math.sin(t * 2.2) * .03)
    person(cr, 300, 625, 350, shirt=C("4F7DD9"), pose=dict(ra=95, ra2=-25, la=25, la2=-95, look=1, mouth="smile", blink=(t % 3) < .12))
    for i in range(3):
        ph = (t * .5 + i / 3) % 1
        heart(cr, 400 + i * 40, 240 - ph * 120, .35 * (1 - ph) + .1, PINK, 1 - ph)

def k_screws(cr, t, d, m):
    room(cr, C("F3E9DC"), C("E6D3BC"), C("B98F65"))
    _shelf(cr, 730, 600, .62, .1)
    person(cr, 250, 625, 340, shirt=C("4F7DD9"), pose=dict(ra=165 + math.sin(t * 8) * 5, ra2=65, look=.6, mouth="flat", blink=(t % 3) < .12))
    push(cr, 500, 655, 1, -.08); rrect(cr, -90, -55, 180, 110, 4, WHITE)
    for j in range(4): line(cr, -70, -32 + j * 22, 70 - (j % 2) * 40, -32 + j * 22, 4, C("B5C2CF"))
    cr.restore()
    for i in range(3):
        t0 = .8 + i * .5
        if t < t0: continue
        tt = t - t0; yb = 596 - 150 * abs(math.cos(tt * 5)) * math.exp(-tt * 2.2)
        x = 400 + i * 50
        line(cr, x, yb - 26, x, yb, 6, C("9AA3B5")); rrect(cr, x - 10, yb - 34, 20, 9, 3, C("7C8798"))
    bubble(cr, 480, 190, 380, 70, "Left over: 3 screws", 30, back((t - 2.4) / .4))

def k_study(cr, t, d, m):
    vgrad(cr, PW, PH, C("11394A"), C("1E5C68")); rrect(cr, 60, 520, 760, 22, 8, BROWN)
    for i, (lbl, price, x, t0) in enumerate([("Built it myself", "$0.78", 250, .6), ("Ready-made", "$0.48", 620, 1.5)]):
        rrect(cr, x - 95, 380, 190, 140, 8, C("C9A26B")); rrect(cr, x - 100, 372, 200, 34, 8, C("B58A52")); rrect(cr, x - 22, 440, 44, 12, 6, C("8B6A3C"))
        text(cr, lbl, x, 590, 26, CREAM, anchor="c")
        k = back((t - t0) / .4)
        if k > 0:
            push(cr, x, 290, k); rrect(cr, -80, -40, 160, 80, 14, WHITE); text(cr, price, 0, 16, 44, DK, anchor="c", face="Lora"); cr.restore()
    k = back((t - 2.6) / .5) * (1 + .04 * math.sin(t * 5))
    if k > 0:
        push(cr, 435, 160, k); rrect(cr, -115, -50, 230, 100, 50, ACC); text(cr, "+63%", 0, 20, 56, INK, anchor="c", face="Lora"); cr.restore()
    text(cr, "Same box. Same wood.", 70, 670, 26, MUTED, appear(t, 3.4, .5), bold=False)

def k_love(cr, t, d, m):
    vgrad(cr, PW, PH, C("2B2758"), C("4A3E8E"))
    poly(cr, [(0, 650), (960, 340), (960, 720), (0, 720)], C("231F48"))
    sl = lambda x: 650 - (x / 960) * 310
    p = min(1, t / d) * .62 + .06; rx = 140 + p * 640; ry = sl(rx) - 72
    px = rx - 125
    person(cr, px, sl(px), 230, shirt=ACC, pose=dict(ra=88, ra2=-8, la=-30, la2=0, look=1, mouth="smile", swing=math.sin(t * 6)))
    circle(cr, rx, ry, 74, C("7A7F99"))
    push(cr, rx, ry, 1, rx / 74); polyline(cr, [(-50, -20), (-20, 5), (-35, 40)], 4, C("5D6280")); polyline(cr, [(30, -52), (18, -18), (48, 6)], 4, C("5D6280")); cr.restore()
    text(cr, "my idea", rx, ry + 9, 24, WHITE, anchor="c")
    heart(cr, rx + 10, ry - 120, .5 * (1 + .12 * math.sin(t * 6)))
    line(cr, 890, 362, 890, 250, 6, CREAM); poly(cr, [(890, 250), (830, 268), (890, 290)], RED)
    bubble(cr, 760, 190, 190, 54, "Week 6", 26, back((t - 1.5) / .4))

def k_use(cr, t, d, m):
    room(cr, C("E9EEF7"), C("CBD5E8"), C("9AA7C2")); rrect(cr, 410, 600, 300, 14, 6, C("6E7B96"))
    cols = [ACC, TEAL, PINK]; ppl = [(130, ACC, "short"), (290, TEAL, "long"), (810, PINK, "bun")]
    for i in range(6):
        t0 = .5 + i * .7
        if t < t0: continue
        k = ease((t - t0) / .5); bx = 425 + (i % 3) * 92; by = 514 - (i // 3) * 90
        rrect(cr, bx, by - (1 - k) * 420, 86, 86, 10, cols[i % 3])
    for j, (x, col, hs) in enumerate(ppl):
        act = any(0 < t - (.5 + i * .7) < .7 for i in range(6) if i % 3 == j)
        person(cr, x, 630 if j < 2 else 600, 300 if j < 2 else 250, shirt=col, pose=dict(look=1 if j < 2 else -1, hairstyle=hs, ra=150 if act else 20, la=150 if act and j == 2 else 12, mouth="smile", blink=((t + j) % 3) < .12))
        heart(cr, x, 250 if j < 2 else 290, .3 * back((t - 1.2 - j * .7) / .4))

# ======================= 06 Doorway effect =======================
def d_hook(cr, t, d, m):
    kitchen(cr)
    o = person(cr, 480, 630, 340, shirt=C("3FA77A"), pose=dict(look=math.sin(t * 1.5), mouth="flat", ra=150, ra2=70, blink=(t % 2.6) < .12))
    hx, hy = o["head"]
    for i, (dx, s, ph) in enumerate([(0, 96, 0), (-80, 50, 1), (85, 60, 2)]):
        text(cr, "?", hx + dx, hy - 80 - s * .2 + math.sin(t * 3 + ph) * 10, s, RED, appear(t, .4 + i * .4, .3), face="Lora", anchor="c")

def d_robot(cr, t, d, m):
    kitchen(cr)
    arr = min(1, t / 2.4); x = -60 + 520 * ease(arr); here = arr >= 1
    pose = dict(walk_pose(t, 8), mouth="smile", look=1) if not here else dict(ra=90, ra2=-90, la=90, la2=-90, mouth="flat", look=math.sin(t * 2) * .6)
    o = person(cr, x, 630, 340, shirt=C("3FA77A"), pose=pose); hx, hy = o["head"]
    if not here:
        push(cr, hx + 30, hy - 120, 1); cloud(cr, 0, 0, 190, 100, WHITE, .97); cr.restore(); scissors(cr, hx + 30, hy - 118, 50, 0)
    else:
        push(cr, hx + 30, hy - 120, 1 - .5 * ease((t - 2.4) / .3)); cloud(cr, 0, 0, 190, 100, WHITE, .5); cr.restore()
        bl = .55 + .45 * (math.sin(t * 6) > 0)
        k = back((t - 2.9) / .4)
        if k > 0:
            push(cr, 400, 120, k); rrect(cr, -290, -42, 580, 84, 12, INK); text(cr, "ERROR 404: purpose not found", 0, 11, 30, GREEN, bl, anchor="c"); cr.restore()

def d_study(cr, t, d, m):
    vgrad(cr, PW, PH, C("1B2440"), C("27345E"))
    p = (t % 5) / 5; x = 110 + p * 600
    for r, (lbl, fy) in enumerate([("Same room", 300), ("Through a doorway", 610)]):
        rrect(cr, 40, fy, 880 if r == 0 else 700, 8, 4, C("3C4670")); text(cr, lbl, 60, fy - 215, 28, CREAM)
        if r == 1:
            rrect(cr, 400, fy - 190, 14, 190, 4, BROWN); rrect(cr, 400, fy - 200, 100, 14, 4, BROWN); rrect(cr, 486, fy - 190, 14, 190, 4, BROWN)
        o = person(cr, x, fy, 165, shirt=[TEAL, ACC][r], pose=dict(walk_pose(t, 8), look=1, ra=60, ra2=-60))
        rx, ry = o["rh"]; rrect(cr, rx - 12, ry - 16, 26, 24, 4, C("C9A26B"))
        lvl = 1.0 if r == 0 else 1 - .5 * ease((x - 450) / 60)
        text(cr, "memory", 640, fy - 232, 20, MUTED, bold=False)
        rrect(cr, 640, fy - 218, 220, 22, 11, C("3C4670")); rrect(cr, 640, fy - 218, 220 * lvl, 22, 11, GREEN if lvl > .8 else RED)

def d_file(cr, t, d, m):
    vgrad(cr, PW, PH, C("23304F"), C("34497A"))
    rrect(cr, 560, 130, 290, 430, 12, C("5D6680"))
    t1 = d * .5; op = ease((t - .4) / .5) - ease((t - t1 - .3) / .5)
    for i, y in enumerate((150, 285, 420)):
        ox = -op * 70 if i == 1 else 0
        rrect(cr, 575 + ox, y, 260, 122, 8, C("8E9BBD") if i == 1 else C("7A86A6")); rrect(cr, 675 + ox, y + 52, 60, 12, 6, C("C7CFE0"))
    f = ease((t - .9) / max(.5, t1 - .9)); fx = 150 + 440 * f; fa = 1 - ease((t - t1) / .3)
    rrect(cr, fx - 75, 300, 150, 92, 6, ACC, fa); rrect(cr, fx - 75, 286, 64, 22, 6, ACC, fa); text(cr, "Scene 1", fx, 356, 22, INK, fa, anchor="c")
    f2 = ease((t - 1.5) / max(.5, t1 - .9)); bx = 150 + 440 * f2
    bubble(cr, bx, 210, 230, 54, "get scissors", 24, (1 - ease((t - t1 - .2) / .3)) * min(1, t * 3))
    k = back((t - t1 - .8) / .4)
    if k > 0:
        push(cr, 290, 500, k, -.1); rr_path(cr, -110, -40, 220, 80, 10); cr.set_line_width(7); src(cr, RED); cr.stroke(); text(cr, "FILED", 0, 18, 50, RED, anchor="c", face="Lora"); cr.restore()

def d_fix(cr, t, d, m):
    room(cr, C("E9F3EC"), C("CFE5D6"), C("9DBFA8"))
    rrect(cr, 390, 230, 16, 372, 4, BROWN); rrect(cr, 390, 216, 150, 16, 4, BROWN); rrect(cr, 524, 230, 16, 372, 4, BROWN)
    f = t / d
    if f < .5:
        x = 110 + 520 * (f / .5)
        o = person(cr, x, 630, 320, shirt=C("3FA77A"), pose=dict(walk_pose(t, 8), look=1, mouth="o" if int(t * 5) % 2 else "smile")); hx, hy = o["head"]
        bubble(cr, min(max(hx + 40, 190), 700), hy - 110, 320, 60, "Scissors. Scissors.", 26, 1, tail=-1)
    else:
        o = person(cr, 630, 630, 320, shirt=C("3FA77A"), pose=dict(ra=165, ra2=5, look=-.3, mouth="smile", blink=(t % 2.5) < .12))
        rx, ry = o["rh"]; scissors(cr, rx + 6, ry - 34, 70, t)
        for i in range(6):
            a = t * 1.5 + i * math.pi / 3; line(cr, rx + 6 + math.cos(a) * 70, ry - 34 + math.sin(a) * 70, rx + 6 + math.cos(a) * 92, ry - 34 + math.sin(a) * 92, 5, ACC)
        check(cr, 250, 200, 80, GREEN, back((t - d * .5 - .3) / .4))

# ======================= 07 Wald / survivorship bias =======================
def _blueprint(cr):
    vgrad(cr, PW, PH, C("123A66"), C("0E2F55"))
    for x in range(0, PW, 48): line(cr, x, 0, x, PH, 1.5, WHITE, .08)
    for y in range(0, PH, 48): line(cr, 0, y, PW, y, 1.5, WHITE, .08)

def w_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("6FA8DC"), C("BFE0F7"))
    for i in range(5): cloud(cr, 120 + (i * 233) % 760, (i * 190 + t * 70) % 900 - 100, 200, 80, WHITE, .85)
    y = 380 + math.sin(t * 1.3) * 12; x = 480 + math.sin(t * .7) * 10
    plane(cr, x + 14, y + 22, 560, INK, .12); plane(cr, x, y, 560, C("6B7A62"))
    holes(cr, x, y, 560, int((t - .5) / .3))

def w_holes(cr, t, d, m):
    _blueprint(cr); x, y, s = 440, 360, 600
    plane(cr, x, y, s, C("DCE6F2"), .92, C("AEBBD0")); holes(cr, x, y, s, int(t / .15))
    t0 = d * .5
    for i, (ax, ay, w, h) in enumerate([(-46, 0, 26, 16), (20, 0, 26, 16), (-7, 14, 14, 26)]):
        k = ease((t - t0 - i * .3) / .4)
        if t > t0 + i * .3: rrect(cr, x + ax * 6, y + ay * 6 - (1 - k) * 300, w * 6, h * 6, 8, STEEL, .85)
    bubble(cr, 250, 640, 330, 62, "Add armour here?", 28, back((t - t0 - 1) / .4))

def w_wald(cr, t, d, m):
    room(cr, C("E8DCC0"), C("D9C9A3"), C("9C7B55"))
    rrect(cr, 370, 100, 500, 360, 10, BROWN); rrect(cr, 384, 114, 472, 332, 6, C("2F4F3E"))
    px, py, s = 620, 250, 300
    plane(cr, px, py, s, C("E8EEF0"), .85, C("B9C4C0")); holes(cr, px, py, s, 14, .9)
    o = person(cr, 210, 630, 350, shirt=C("5A6B52"), pants=C("3A3A44"), pose=dict(ra=100, ra2=-12, look=1, mouth="o" if int(t * 4) % 2 else "smile", blink=(t % 3) < .12)); glasses(cr, o)
    t0 = d * .4; pr = ease((t - t0) / 1.2)
    if pr > 0:
        for ex in ENG: ring(cr, px + ex * 3, py - 15, 20, 5, ACC, 1, 0, 2 * math.pi * pr)
    text(cr, "These ones came back.", 620, 425, 26, C("E8EEF0"), appear(t, t0 + 1.2, .5), anchor="c", bold=False)

def w_engines(cr, t, d, m):
    _blueprint(cr); x, y, s = 440, 340, 600; u = 6
    for i, gx in enumerate((70, 870)):
        ph = (t * .25 + i * .5) % 1
        push(cr, gx, -80 + ph * 900, 1, .6 + ph * 2); plane(cr, 0, 0, 150, WHITE, .16 * (1 - ph)); cr.restore()
    plane(cr, x, y, s, C("DCE6F2"), .92, C("AEBBD0")); holes(cr, x, y, s, 14, .3)
    p = .5 + .5 * math.sin(t * 4); k = appear(t, .5, .6)
    for ex in ENG: glow(cr, x + ex * u, y - 5 * u, 60 + 14 * p, ACC, .75 * k); ring(cr, x + ex * u, y - 5 * u, 34, 5, ACC, k)
    glow(cr, x, y - 34 * u, 60 + 14 * p, ACC, .6 * k)
    bubble(cr, 300, 620, 480, 62, "No holes here = never came home", 26, back((t - 1.6) / .4))

def w_use(cr, t, d, m):
    vgrad(cr, PW, PH, C("1A2142"), C("2D3B6E")); rrect(cr, 0, 610, PW, 110, 0, C("141A36"))
    n = int(max(0, (t - 1.2) * 4))
    for i in range(min(n, 16)):
        x = 70 + (i * 131) % 700 + (i % 2) * 30; y = 520 + (i * 53) % 130
        if 360 < x < 600: x += 250 if i % 2 else -250
        circle(cr, x, y - 62, 18, GREY, .4); rrect(cr, x - 22, y - 42, 44, 60, 16, GREY, .4)
    glow(cr, 480, 300, 240, ACC, .3)
    rrect(cr, 385, 480, 190, 130, 8, GOLD); text(cr, "1", 480, 570, 64, INK, anchor="c", face="Lora")
    person(cr, 480, 480, 250, shirt=ACC, pose=dict(ra=165, la=165, mouth="smile", blink=(t % 3) < .12))
    bubble(cr, 480, 110, 330, 70, "Who's missing?", 32, back((t - d * .5) / .4))

# ======================= 08 Emu war =======================
def e_hook(cr, t, d, m):
    outback(cr, t)
    emu(cr, 400, 660, 340, t, run=0, hat=True)
    k = back((t - 1.6) / .5)
    if k > 0:
        push(cr, 480, 100, k); rrect(cr, -290, -52, 580, 104, 14, INK); text(cr, "EMUS  1 : 0  ARMY", 0, 17, 46, ACC, anchor="c", face="Lora"); cr.restore()

def e_farm(cr, t, d, m):
    outback(cr, t); wave = t * 230 - 150
    for x in range(20, 960, 24):
        fl = ease((wave - x) / 120); h = 80 * (1 - fl * .85)
        line(cr, x, 610, x + 8 + fl * 40, 610 - h, 5, C("E8B923")); ell(cr, x + 8 + fl * 40, 606 - h, 5, 11, C("D9A514"))
    for i in range(5):
        ex = (t * 230 + i * 215) % (PW + 300) - 150
        emu(cr, ex, 612 - (i % 2) * 34, 170 + (i % 3) * 14, t + i, run=1)
    person(cr, 110, 650, 240, shirt=C("B5533C"), pants=C("4F5D7A"), pose=dict(helmet=C("C68A4E"), ra=160 + math.sin(t * 9) * 12, la=160 - math.sin(t * 9) * 12, mouth="frown", look=1))

def e_guns(cr, t, d, m):
    outback(cr, t)
    for i in range(8):
        a = i * math.pi / 4 + .3; dist = 50 + (t * 150 + i * 47) % 430
        ex, ey = 640 + math.cos(a) * dist, 470 + math.sin(a) * dist * .45
        emu(cr, ex, ey + 60, 105, t + i, run=1, face=1 if math.cos(a) >= 0 else -1)
    for i, (x, y) in enumerate(((95, 655), (200, 665))):
        person(cr, x, y, 215, shirt=C("7A8452"), pants=C("5A6140"), pose=dict(helmet=C("4E5B35"), look=1, ra=70, ra2=-10, la=10, mouth="flat"))
    line(cr, 290, 590, 262, 660, 6, INK); line(cr, 290, 590, 318, 660, 6, INK)
    rrect(cr, 250, 572, 130, 20, 6, C("3A3A44")); rrect(cr, 372, 577, 46, 9, 4, C("3A3A44")); circle(cr, 310, 566, 14, C("4A4A55"))
    if int(t * 14) % 2:
        poly(cr, [(420, 581), (460, 566), (450, 581), (460, 596)], ACC)
        for j in range(3): line(cr, 470 + j * 130 + (t * 500) % 130, 578 - j * 14, 510 + j * 130 + (t * 500) % 130, 575 - j * 14, 3, WHITE, .7)
    rrect(cr, 330, 640, 150, 62, 6, C("6E5A3A")); text(cr, "10,000", 405, 681, 26, CREAM, anchor="c")

def e_score(cr, t, d, m):
    vgrad(cr, PW, PH, C("1B2440"), C("27345E"))
    emu(cr, 700, 800, 330, t, run=0, face=-1, hat=True)
    g = ease(t / (d * .5))
    for i, (lbl, val, col) in enumerate([("Bullets fired", 9860, ACC), ("Emus", 986, TEAL)]):
        y = 150 + i * 210
        text(cr, lbl, 80, y, 30, CREAM); text(cr, f"{int(val * g):,}", 80, y + 100, 100, col, face="Lora")
    k = back((t - d * .58) / .4)
    if k > 0:
        push(cr, 330, 600, k); rrect(cr, -250, -44, 500, 88, 44, WHITE); text(cr, "= 10 bullets per bird", 0, 12, 32, DK, anchor="c"); cr.restore()

def e_lesson(cr, t, d, m):
    outback(cr, t); P = 2.2; ph = (t % P) / P
    a = -0.5 + 1.95 * ease(ph / .35) - 1.95 * ease((ph - .6) / .4); hit = .32 < ph < .6
    for i in range(6):
        ex = 520 + i * 70; jump = math.sin(min(1, max(0, (ph - .3) / .3)) * math.pi) * (50 + i % 3 * 20)
        emu(cr, ex + (i % 2) * 14, 650 - (i % 3) * 22 - jump, 80, t + i, run=.4, face=1 if i % 2 else -1)
    push(cr, 250, 640, 1, a); rrect(cr, -12, -330, 24, 330, 8, BROWN); rrect(cr, -80, -400, 160, 90, 14, C("7A7F99")); rrect(cr, -80, -400, 160, 22, 10, C("9AA0B8")); cr.restore()
    if hit:
        q = (ph - .32) / .28
        for j in range(5): circle(cr, 560 + j * 34 - 68, 640 - q * 40 - (j % 2) * 16, 22 + q * 22, C("F6E2C0"), .7 * (1 - q))
    bubble(cr, 260, 110, 330, 66, "Bigger hammer?", 30, back((t - .8) / .4))
