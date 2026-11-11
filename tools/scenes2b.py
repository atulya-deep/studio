"""Batch 2 scenes, part B: rats, Parkinson, pomodoro, duck, two-minute rule."""
from kit2 import *

# ======================= 09 Hanoi rats =======================
def _office(cr):
    room(cr, C("E8DCC0"), C("D9C9A3"), C("9C7B55"))
    for x in (60, 900): rrect(cr, x - 12, 0, 24, 600, 0, C("CDB98C"))

def _official(cr, x, y, s, t, **kw):
    pose = dict(helmet=C("F6F1E4"), look=1, mouth="smile", blink=(t % 3) < .12); pose.update(kw)
    o = person(cr, x, y, s, shirt=C("F2EEE6"), pants=C("C9BFA6"), pose=pose); hx, hy = o["head"]; u = o["u"]
    line(cr, hx - 7 * u, hy + 5.5 * u, hx + 7 * u, hy + 5.5 * u, 2.6 * u, HAIR)
    return o

def r_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("3A2A1E"), C("6B4A2B")); rrect(cr, 0, 610, PW, 110, 0, C("2A1E15"))
    n = int(min(15, 1 + t * 2.2))
    for i in range(n):
        ell(cr, 130 + (i % 3) * 56, 600 - (i // 3) * 20, 34, 12, C("B8862B")); ell(cr, 130 + (i % 3) * 56, 596 - (i // 3) * 20, 34, 12, GOLD)
    polyline(cr, [(320, 430), (400, 430)], 10, CREAM); poly(cr, [(400, 408), (440, 430), (400, 452)], CREAM)
    nr = int(min(14, 1 + t * 2.4))
    for i in range(nr):
        x = 520 + (i * 97) % 380; y = 300 + (i * 67) % 330; k = back((t - i / 2.4) / .3)
        push(cr, x, y, k); rat(cr, 0, 0, 95, t + i, face=1 if i % 2 else -1, run=.5); cr.restore()

def r_office(cr, t, d, m):
    _office(cr)
    rrect(cr, 540, 110, 300, 230, 6, WHITE); rr_path(cr, 552, 122, 276, 206, 4); cr.set_line_width(4); src(cr, RED); cr.stroke()
    text(cr, "WANTED", 690, 180, 36, RED, anchor="c", face="Lora"); text(cr, "Rat tails", 690, 236, 32, DK, anchor="c"); text(cr, "1 cent each", 690, 300, 38, INK, anchor="c", face="Lora")
    _official(cr, 300, 640, 340, t, ra=105, ra2=-10)
    desk(cr, 130, 490, 340); rrect(cr, 180, 460, 90, 30, 4, WHITE); circle(cr, 400, 474, 16, GOLD)
    rat(cr, PW + 80 - (t * 210) % (PW + 220), 700, 95, t, face=-1)

def r_tails(cr, t, d, m):
    _office(cr)
    rrect(cr, 530, 80, 360, 190, 8, INK); text(cr, "Tails received", 550, 122, 24, CREAM)
    n = int(min(60, t * 9))
    for j in range(n):
        g = j // 5; gx = 556 + (g % 6) * 54 + (j % 5) * 7; gy = 150 + (g // 6) * 56
        if j % 5 == 4: line(cr, gx - 34, gy + 36, gx + 2, gy + 4, 3, ACC)
        else: line(cr, gx, gy, gx, gy + 40, 3, WHITE)
    late = t > d * .58
    o = _official(cr, 170, 640, 320, t, look=1, mouth="o" if late else "smile")
    desk(cr, 60, 490, 260)
    sh = (t * 45) % 150
    for i in range(3):
        x = 420 + i * 150 - sh
        o2 = person(cr, x, 640, 230, shirt=[C("4F7DD9"), C("3FA77A"), C("D9644A")][i], pose=dict(walk_pose(t + i, 6), look=-1, la=60, la2=-40, hairstyle=["short", "long", "bun"][i]))
        lx, ly = o2["lh"]; polyline(cr, [(lx, ly), (lx - 6, ly + 14), (lx + 4, ly + 26), (lx - 4, ly + 40)], 4, C("F2A7B5"))
    if late:
        rx = -80 + (t - d * .58) * 200
        rat(cr, min(rx, 620), 705, 125, t, tail=False, run=1 if rx < 620 else 0)
        hx, hy = o["head"]; text(cr, "?", hx + 50, hy - 40, 70, RED, face="Lora")

def r_loop(cr, t, d, m):
    vgrad(cr, PW, PH, C("2D2A4A"), C("C4643A")); rrect(cr, 0, 610, PW, 110, 0, C("3A2A1E"))
    k = appear(t, d * .5, .6)
    if k > 0:
        for i in range(7): rrect(cr, 560 + i * 50, 470, 12, 110, 3, BROWN, k)
        rrect(cr, 550, 490, 330, 12, 4, BROWN, k); rrect(cr, 550, 540, 330, 12, 4, BROWN, k)
        for i in range(4): rat(cr, 600 + i * 70, 470 - abs(math.sin(t * 5 + i)) * 14, 60, t + i, face=1 if i % 2 else -1, run=.3)
        bubble(cr, 715, 360, 220, 60, "Rat farm", 28, back((t - d * .5) / .4), tail=0)
    rrect(cr, 70, 520, 110, 100, 22, C("9C7B55")); text(cr, "1c", 125, 584, 34, CREAM, anchor="c", face="Lora")
    P = 2.6; ph = (t % P) / P
    rrect(cr, 205, 505, 90, 135, 8, C("6E5A3A"))
    o = person(cr, 250, 640, 300, shirt=C("4F7DD9"), pose=dict(sit=True, face=1, ra=60, ra2=20, la=30, la2=40, look=.6, mouth="smile", hairstyle="short"))
    if ph < .45:
        rat(cr, 430, 620, 110, t, run=0); scissors(cr, 355, 598, 50, t)
    else:
        q = (ph - .45) / .55
        rat(cr, 430 + q * 640, 620, 110, t, tail=False)
        ax = 350 - q * 230; ay = 600 - math.sin(min(1, q * 2) * math.pi) * 120
        if q < .5: polyline(cr, [(ax, ay), (ax - 18, ay - 8), (ax - 34, ay + 4)], 5, C("F2A7B5"))
        else: text(cr, "+1c", 125, 500 - (q - .5) * 80, 30, ACC, 1 - (q - .5) * 2, anchor="c")

def r_cobra(cr, t, d, m):
    vgrad(cr, PW, PH, C("1B2440"), C("27345E"))
    g = ease(t / (d * .45))
    line(cr, 80, 560, 420, 560, 4, CREAM, .6); line(cr, 80, 560, 80, 200, 4, CREAM, .6)
    for i in range(5): h = (60 + i * 62) * g; rrect(cr, 100 + i * 62, 560 - h, 46, h, 8, GREEN)
    text(cr, "Tails collected", 80, 610, 26, CREAM)
    k = back((t - d * .45) / .4)
    if k > 0:
        push(cr, 250, 170, k, -.08); rrect(cr, -130, -34, 260, 68, 12, GREEN); text(cr, "Target hit!", 0, 11, 30, INK, anchor="c"); cr.restore()
    line(cr, 520, 560, 880, 560, 4, CREAM, .6); line(cr, 520, 560, 520, 200, 4, CREAM, .6)
    g2 = ease((t - d * .3) / (d * .45)); pts = [(530 + i * 22, 530 - (i ** 1.7) * 3.6) for i in range(16)]
    nn = max(2, int(len(pts) * g2))
    if g2 > 0: polyline(cr, pts[:nn], 8, RED); rat(cr, pts[nn - 1][0], pts[nn - 1][1] - 6, 70, t, run=.5)
    text(cr, "Rats in the city", 520, 610, 26, CREAM)

# ======================= 10 Parkinson's law =======================
def p_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("1E2A4E"), C("2D4176"))
    ox, oy, cw = 100, 210, 108
    text(cr, "2 weeks", ox, 150, 40, CREAM, face="Lora")
    for r in range(2):
        for c in range(7):
            rrect(cr, ox + c * cw, oy + r * 170, cw - 8, 150, 12, C("F6F0E2"), .95); text(cr, str(r * 7 + c + 1), ox + c * cw + 12, oy + r * 170 + 34, 22, MUTED)
    n = 1 + 13 * ease((t - 1.2) / (d * .55))
    for r in range(2):
        cells = max(0, min(7, n - r * 7))
        if cells > 0: rrect(cr, ox + 6, oy + r * 170 + 62, cells * cw - 20, 60, 30, ACC)
    text(cr, "2-hour task", ox + 26, oy + 101, 24, INK)

def p_essay(cr, t, d, m):
    room(cr, C("D8C7A0"), C("C4AE80"), C("8A6B45"))
    rrect(cr, 640, 110, 190, 170, 6, WHITE); rrect(cr, 640, 110, 190, 46, 6, RED); text(cr, "1955", 735, 245, 56, DK, anchor="c", face="Lora")
    tap = math.sin(t * 14) * 8
    o = person(cr, 330, 640, 340, shirt=C("5A6B52"), pose=dict(la=-10, la2=-60 + tap, ra=42, ra2=62 - tap, look=.5, mouth="smile", blink=(t % 3) < .12)); glasses(cr, o)
    desk(cr, 150, 490, 500)
    ph = 50 + (t * 16) % 150
    rrect(cr, 440, 432 - ph, 120, ph + 10, 3, WHITE)
    for j in range(int(ph / 18)): line(cr, 452, 426 - j * 18, 548 - (j % 3) * 22, 426 - j * 18, 3, C("9AA3B5"))
    rrect(cr, 400, 424, 200, 68, 12, INK); rrect(cr, 392, 414, 216, 18, 8, C("3A3A44"))
    for j in range(8): circle(cr, 420 + j * 23, 462 + (tap > 4 and j % 3 == int(t * 7) % 3) * 4, 7, C("C7CFE0"))

def p_law(cr, t, d, m):
    vgrad(cr, PW, PH, C("2B2758"), C("4A3E8E"))
    for i, (x, w, lbl) in enumerate([(70, 130, "1 hour"), (250, 220, "1 day"), (520, 360, "1 week")]):
        t0 = .4 + i * d * .22; fill = ease((t - t0) / (d * .2))
        text(cr, lbl, x + w / 2, 190, 30, CREAM, anchor="c")
        rrect(cr, x + 8, 552 - fill * 300, w - 16, fill * 300, 12, ACC, .95)
        rr_path(cr, x, 240, w, 320, 16); cr.set_line_width(6); src(cr, WHITE, .85); cr.stroke()
        if fill > .85: text(cr, "same task", x + w / 2, 410, 20 if w < 200 else 26, INK, anchor="c")

def p_lady(cr, t, d, m):
    room(cr, C("F3E3EE"), C("E6CFE0"), C("B894AC")); f = min(1, t / d)
    rrect(cr, 70, 90, 250, 200, 10, BROWN); sky = lerpc(C("BFE0F7"), C("141B40"), ease((f - .45) / .4)); rrect(cr, 84, 104, 222, 172, 6, sky)
    cr.save(); rr_path(cr, 84, 104, 222, 172, 6); cr.clip(); sx = 84 + f * 222; sy = 250 - math.sin(f * math.pi) * 120
    circle(cr, sx, sy, 24, lerpc(C("FFB347"), C("FFF3C4"), f)); cr.restore()
    circle(cr, 780, 180, 78, INK); circle(cr, 780, 180, 68, WHITE)
    for i in range(12): a = i * math.pi / 6; line(cr, 780 + math.sin(a) * 56, 180 - math.cos(a) * 56, 780 + math.sin(a) * 63, 180 - math.cos(a) * 63, 3, INK)
    ah = f * 2 * math.pi * .75; am = f * 2 * math.pi * 9
    line(cr, 780, 180, 780 + math.sin(ah) * 34, 180 - math.cos(ah) * 34, 8, INK); line(cr, 780, 180, 780 + math.sin(am) * 54, 180 - math.cos(am) * 54, 5, RED)
    rrect(cr, 490, 500, 90, 140, 8, C("8A5F78")); rrect(cr, 560, 380, 20, 260, 8, C("8A5F78"))
    o = person(cr, 520, 640, 320, shirt=C("9B6BB3"), hair=C("C9CCD6"), pose=dict(sit=True, face=-1, hairstyle="bun", la=55, la2=50 + math.sin(t * 3) * 8, look=-.5, mouth="smile", blink=(t % 3.2) < .14)); glasses(cr, o)
    rrect(cr, 300, 500, 330, 22, 8, BROWN); rrect(cr, 330, 520, 22, 100, 4, DBROWN); rrect(cr, 380, 474, 96, 28, 3, WHITE); rrect(cr, 452, 478, 18, 14, 2, RED)
    for i, lbl in enumerate(["Find the card: 1 h", "Find glasses: 1 h", "Choose words: 1 h 15"]):
        bubble(cr, 200, 350 + i * 66, 300, 52, lbl, 22, back((t - 1 - i * (d - 2.5) / 3) / .4))

def p_use(cr, t, d, m):
    vgrad(cr, PW, PH, C("11394A"), C("1E5C68")); rrect(cr, 60, 560, 760, 14, 6, C("0D2B38"))
    sq = ease((t - .9) / (d * .4)); L = 110 + 190 * sq; R = 770 - 190 * sq
    rrect(cr, L - 26, 300, 26, 262, 8, CREAM); rrect(cr, R, 300, 26, 262, 8, CREAM)
    bw = R - L - 16; bh = 120 + sq * 60
    rrect(cr, L + 8, 560 - bh, bw, bh, 34, ACC)
    cx = (L + R) / 2; cy = 560 - bh / 2
    for sx in (-1, 1): circle(cr, cx + sx * 26, cy - 10, 8, INK)
    cr.new_path(); cr.arc(cx, cy + 4, 20, .4, math.pi - .4); cr.set_line_width(5); src(cr, INK); cr.stroke()
    polyline(cr, [(110, 250), (L - 40, 250)], 6, CREAM, .5); polyline(cr, [(770, 250), (R + 40, 250)], 6, CREAM, .5)
    text(cr, "Deadline", cx, 215, 32, CREAM, anchor="c")
    bubble(cr, 400, 110, 330, 66, "Done early", 32, back((t - d * .6) / .4)); check(cr, 610, 110, 44, GREEN, back((t - d * .6 - .3) / .4))

# ======================= 11 Pomodoro =======================
def m_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("3B1F2B"), C("7A2E3A")); glow(cr, 480, 370, 380, C("FFB15C"), .3)
    for i in range(8):
        a = t * .6 + i * math.pi / 4; k = .6 + .4 * math.sin(t * 3 + i)
        line(cr, 480 + math.cos(a) * 270, 380 + math.sin(a) * 270, 480 + math.cos(a) * (300 + 30 * k), 380 + math.sin(a) * (300 + 30 * k), 8, ACC, .8)
    sh = math.sin(t * 30) * 3 if (t % 3) > 2.5 else 0
    tomato(cr, 480 + sh, 390, 200 * back(t / .6), t, face=True)

def m_student(cr, t, d, m):
    room(cr, C("E3ECF7"), C("C9D8EC"), C("93A7C4")); t0 = d * .6; fade = 1 - ease((t - t0 - .3) / .6)
    o = person(cr, 340, 640, 340, shirt=C("4F7DD9"), pose=dict(la=30, la2=60, ra=150 if fade > .5 else 40, ra2=70, mouth="frown" if fade > .5 else "smile", look=math.sin(t * 2) * fade, blink=(t % 3) < .12))
    hx, hy = o["head"]
    desk(cr, 150, 490, 440)
    for j, (bw, col) in enumerate([(150, RED), (130, TEAL), (140, DK)]): rrect(cr, 180 + j * 6, 462 - j * 28, bw, 26, 4, col)
    for i in range(4):
        a = t * 1.3 + i * math.pi / 2; x = hx + math.cos(a) * 190; y = hy - 20 + math.sin(a) * 90
        if fade <= 0: break
        if i == 0: rrect(cr, x - 18, y - 30, 36, 60, 8, INK, fade); rrect(cr, x - 13, y - 22, 26, 40, 3, C("8FD3FF"), fade)
        elif i == 1: circle(cr, x - 8, y + 14, 12, PINK, fade); line(cr, x + 3, y + 14, x + 3, y - 26, 5, PINK, fade); line(cr, x + 3, y - 26, x + 22, y - 18, 5, PINK, fade)
        elif i == 2: rrect(cr, x - 30, y - 20, 60, 40, 14, WHITE, fade); [circle(cr, x - 14 + q * 14, y, 4, MUTED, fade) for q in range(3)]
        else: rrect(cr, x - 30, y - 16, 60, 32, 14, C("6B5BD2"), fade); circle(cr, x - 14, y, 6, WHITE, fade); circle(cr, x + 14, y, 6, ACC, fade)
    if t > t0:
        tt = t - t0; yb = 444 - 260 * abs(math.cos(tt * 5)) * math.exp(-tt * 2.5) * (tt < 2)
        tomato(cr, 500, yb, 46, t)

def m_cycle(cr, t, d, m):
    vgrad(cr, PW, PH, C("1B2440"), C("27345E"))
    p = min(1, t / (d * .85)); mx = 70 + p * 820
    line(cr, 70, 440, 890, 440, 6, C("3C4670"))
    for i in range(4):
        x = 130 + i * 160
        if mx > x - 50: tomato(cr, x, 370, 50, t)
        else: ring(cr, x, 370, 50, 5, C("5D6B9A"))
        text(cr, "25", x, 500, 34, CREAM if mx > x - 50 else MUTED, anchor="c", face="Lora")
        if i < 3:
            on = mx > x + 60; rrect(cr, x + 62, 356, 36, 28, 14, GREEN if on else C("3C4670")); text(cr, "5", x + 80, 500, 26, GREEN if on else MUTED, anchor="c")
    on = mx > 700; rrect(cr, 690, 340, 200, 60, 30, GREEN if on else C("3C4670")); text(cr, "long break", 790, 379, 26, INK if on else MUTED, anchor="c")
    poly(cr, [(mx - 16, 240), (mx + 16, 240), (mx, 272)], ACC); line(cr, mx, 272, mx, 440, 3, ACC, .5)
    text(cr, "minutes", 70, 160, 28, MUTED, bold=False)

def m_small(cr, t, d, m):
    vgrad(cr, PW, PH, C("23304F"), C("34497A")); rrect(cr, 0, 600, PW, 120, 0, C("1A2440"))
    poly(cr, [(240, 600), (580, 130), (920, 600)], C("6E7B96")); poly(cr, [(520, 213), (580, 130), (640, 213), (600, 240), (570, 215), (545, 240)], WHITE)
    text(cr, "Write the report", 585, 420, 30, CREAM, anchor="c")
    f = t / d; go = ease((f - .5) / .12)
    k = back((f - .42) / .08)
    if k > 0:
        rrect(cr, 200, 600 - 62 * min(1, k), 170, 62 * min(1, k), 8, ACC); text(cr, "25 min", 285, 580, 26, INK, min(1, k), anchor="c")
    hopy = math.sin(go * math.pi) * 60 if 0 < go < 1 else 0
    person(cr, 110 + go * 150, 600 - go * 62 - hopy, 180, shirt=C("3FA77A"), pose=dict(mouth="o" if go < .5 else "smile", look=1, ra=165 if go >= 1 else 12, blink=(t % 3) < .12))
    if k > 0: tomato(cr, 345, 600 - 62 - 26, 26 * min(1, k), t)

def m_try(cr, t, d, m):
    room(cr, C("E3ECF7"), C("C9D8EC"), C("93A7C4")); f = min(1, t / d)
    tap = math.sin(t * 12) * 6
    person(cr, 330, 640, 340, shirt=C("4F7DD9"), pose=dict(la=-8, la2=-60 + tap, ra=42, ra2=60 - tap, look=.4, mouth="smile", blink=(t % 3.4) < .12))
    desk(cr, 150, 490, 480)
    rrect(cr, 380, 478, 170, 12, 4, C("9AA3B5")); poly(cr, [(392, 478), (538, 478), (552, 380), (406, 380)], C("5D6680")); poly(cr, [(402, 472), (530, 472), (542, 388), (414, 388)], C("9ED8FF"))
    ring_ = f > .92; sh = math.sin(t * 40) * 4 if ring_ else 0
    tomato(cr, 590 + sh, 440, 44, t, prog=f)
    if ring_:
        for i in range(5): a = -math.pi / 2 + (i - 2) * .5; line(cr, 590 + math.cos(a) * 74, 440 + math.sin(a) * 74, 590 + math.cos(a) * 96, 440 + math.sin(a) * 96, 5, ACC)
    q = ease((t - .8) / 1.6)
    if q < 1:
        px = 250 + q * 800; py = 430 - q * 330 - math.sin(q * math.pi) * 60; fl = math.sin(t * 22) * .5
        ell(cr, px - 26, py - 6, 22, 9, WHITE, .9, rot=-.4 + fl); ell(cr, px + 26, py - 6, 22, 9, WHITE, .9, rot=.4 - fl)
        rrect(cr, px - 18, py - 30, 36, 60, 8, INK); rrect(cr, px - 13, py - 22, 26, 40, 3, C("8FD3FF"))

# ======================= 12 Rubber duck =======================
def _office2(cr): room(cr, C("26315A"), C("34447A"), C("1C2445"))

def u_hook(cr, t, d, m):
    _office2(cr)
    person(cr, 300, 640, 340, shirt=C("3FA77A"), pose=dict(look=1, mouth="o" if int(t * 5) % 2 else "smile", ra=75 + math.sin(t * 4) * 14, ra2=-25, la=20, la2=40, hairstyle="long", blink=(t % 3) < .12))
    desk(cr, 170, 500, 600)
    duck(cr, 620, 500, 190, t, face=-1)
    for i in range(3):
        ph = (t * 1.2 + i / 3) % 1
        ring(cr, 420, 300, 30 + ph * 70, 6, CREAM, .8 * (1 - ph), -.5, .5)

def u_secret(cr, t, d, m):
    vgrad(cr, PW, PH, C("14122B"), C("241F4A")); rrect(cr, 0, 600, PW, 120, 0, C("0F0D22"))
    cr.new_path(); cr.move_to(450, 0); cr.line_to(510, 0); cr.line_to(680, 600); cr.line_to(280, 600); cr.close_path(); src(cr, C("FFF3C4"), .2); cr.fill()
    rrect(cr, 390, 470, 180, 130, 8, C("C7CFE0")); rrect(cr, 376, 456, 208, 22, 6, C("E3E8F2"))
    duck(cr, 475, 456, 210, t)
    for i, (x, y, w, lbl) in enumerate([(170, 250, 210, "Yellow"), (790, 300, 230, "Squeaks")]):
        k = back((t - .8 - i * .9) / .4); bubble(cr, x, y, w, 62, lbl, 30, k); check(cr, x + w / 2 - 6, y - 34, 34, GREEN, k)
    bubble(cr, 480, 90, 500, 70, "Lines of code written: 0", 30, back((t - 2.8) / .4))

def u_book(cr, t, d, m):
    _office2(cr)
    person(cr, 150, 640, 330, shirt=C("3FA77A"), pose=dict(look=1, ra=98, ra2=-20, mouth="o" if int(t * 5) % 2 else "smile", hairstyle="long", blink=(t % 3) < .12))
    desk(cr, 230, 500, 600)
    monitor(cr, 300, 190, 360, 256, hl=int(t * 1.1) % 6)
    duck(cr, 750, 500, 150, t, face=-1)
    bubble(cr, 810, 120, 170, 60, "1999", 32, back((t - .6) / .4))

def u_why(cr, t, d, m):
    _office2(cr); t0 = d * .5; found = t > t0
    hl = min(3, int(t / (t0 / 4)))
    monitor(cr, 300, 150, 420, 300, hl=hl, bug=3 if found else None)
    rrect(cr, 260, 506, 520, 20, 8, BROWN)
    person(cr, 150, 640, 330, shirt=C("3FA77A"), pose=dict(look=1, ra=165 if found else 98, ra2=0 if found else -20, la=165 if found else 12, mouth="smile" if found else "flat", hairstyle="long", blink=(t % 3) < .12))
    duck(cr, 830, 506, 140, t, face=-1)
    bubble(cr, 500, 80, 200, 70, "Aha!", 38, back((t - t0) / .4), col=ACC, tcol=INK)

def u_use(cr, t, d, m):
    room(cr, C("E9F3EC"), C("CFE5D6"), C("9DBFA8"))
    person(cr, 160, 640, 330, shirt=C("3FA77A"), pose=dict(look=1, ra=80 + math.sin(t * 4) * 14, ra2=-25, mouth="o" if int(t * 5) % 2 else "smile", hairstyle="long", blink=(t % 3) < .12))
    rrect(cr, 330, 560, 440, 22, 8, BROWN); rrect(cr, 360, 580, 20, 60, 4, DBROWN); rrect(cr, 720, 580, 20, 60, 4, DBROWN)
    duck(cr, 410, 560, 150, t, face=-1)
    rrect(cr, 530, 500, 70, 60, 8, C("C2603C"))
    for i in range(5): ell(cr, 565 + (i - 2) * 16, 470 - abs(i - 2) * -8 - 30, 12, 34, C("3FA77A"), rot=(i - 2) * .35 + math.sin(t * 2 + i) * .04)
    cx = 700; ell(cr, cx, 520, 44, 40, C("F2A65A")); circle(cr, cx, 455, 34, C("F2A65A"))
    poly(cr, [(cx - 30, 440), (cx - 24, 404), (cx - 6, 428)], C("F2A65A")); poly(cr, [(cx + 30, 440), (cx + 24, 404), (cx + 6, 428)], C("F2A65A"))
    bl = (t % 3.3) < .14
    for sx in (-1, 1):
        if bl: line(cr, cx + sx * 13 - 5, 452, cx + sx * 13 + 5, 452, 3, INK)
        else: circle(cr, cx + sx * 13, 452, 5, INK)
    poly(cr, [(cx - 5, 464), (cx + 5, 464), (cx, 470)], PINK)
    cr.new_path(); cr.move_to(cx + 40, 540); cr.curve_to(cx + 90, 540, cx + 80, 480 + math.sin(t * 3) * 10, cx + 70, 470); cr.set_line_width(12); cr.set_line_cap(cairo.LINE_CAP_ROUND); src(cr, C("F2A65A")); cr.stroke()
    k = back((t - d * .6) / .4)
    if k > 0:
        push(cr, 380, 420, k); poly(cr, [(-30, 0), (-30, -34), (-14, -16), (0, -40), (14, -16), (30, -34), (30, 0)], GOLD); cr.restore()
    bubble(cr, 400, 300, 120, 56, "...", 34, back((t - 1.2) / .4), tail=0)

# ======================= 13 Two-minute rule =======================
def t_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("1E2A4E"), C("2D4176"))
    rrect(cr, 270, 50, 460, 640, 14, WHITE); text(cr, "To do", 310, 122, 42, DK, face="Lora")
    ws = [.8, .55, .7, .45, .75, .6, .5, .66]; done = 0
    for i in range(8):
        y = 180 + i * 60; t0 = .6 + i * .3; dn = t > t0; done += dn
        rr_path(cr, 310, y - 16, 32, 32, 6); cr.set_line_width(4); src(cr, C("9AA3B5")); cr.stroke()
        rrect(cr, 362, y - 7, 320 * ws[i], 14, 7, C("9AA3B5"), .35 if dn else 1)
        if dn: check(cr, 326, y, 30, GREEN, back((t - t0) / .3)); line(cr, 358, y, 366 + 320 * ws[i], y, 3, GREEN, .8)
    person(cr, 130, 650, 250, shirt=ACC, pose=dict(look=1, ra=165 if done == 8 else 20, la=165 if done == 8 else 12, mouth="smile", blink=(t % 3) < .12))

def t_tiny(cr, t, d, m):
    room(cr, C("E3ECF7"), C("C9D8EC"), C("93A7C4"))
    o = person(cr, 460, 640, 340, shirt=C("D9644A"), pose=dict(mouth="frown", look=math.sin(t * 1.8), la=30, la2=-80, ra=30, ra2=-80, blink=(t % 2.6) < .12)); hx, hy = o["head"]
    dr = (t * .9) % 1; ell(cr, hx + 54, hy - 10 + dr * 40, 7, 10, C("5AA9E6"), 1 - dr)
    for i, lbl in enumerate(["Reply", "Dentist", "Bill", "Call", "Form", "RSVP", "Renew"]):
        a = t * .8 + i * 2 * math.pi / 7; x = 460 + math.cos(a) * 330; y = 250 + math.sin(a) * 130; k = back((t - i * .2) / .3)
        push(cr, x, y, k * (.85 + .15 * math.sin(a)), math.sin(a + i) * .15); rrect(cr, -44, -40, 88, 80, 6, YEL); rrect(cr, -44, -40, 88, 16, 6, C("F2B90F")); text(cr, lbl, 0, 16, 20, INK, anchor="c"); cr.restore()

def t_rule(cr, t, d, m):
    vgrad(cr, PW, PH, C("14304A"), C("1E4870"))
    rrect(cr, 310, 148, 40, 50, 8, C("C7CFE0")); circle(cr, 330, 400, 190, INK); circle(cr, 330, 400, 172, CREAM)
    for i in range(12): a = i * math.pi / 6; line(cr, 330 + math.sin(a) * 148, 400 - math.cos(a) * 148, 330 + math.sin(a) * 162, 400 - math.cos(a) * 162, 5, INK)
    a = t * 2.4; line(cr, 330, 400, 330 + math.sin(a) * 130, 400 - math.cos(a) * 130, 6, RED); circle(cr, 330, 400, 12, RED)
    text(cr, "2:00", 330, 500, 54, DK, anchor="c", face="Lora")
    rrect(cr, 640, 200, 220, 300, 10, C("2E6FB0")); rrect(cr, 640, 200, 24, 300, 10, C("245A90"))
    for j, w in enumerate(["Getting", "Things", "Done"]): text(cr, w, 760, 290 + j * 46, 34, WHITE, anchor="c", face="Lora")
    text(cr, "David Allen", 760, 460, 20, CREAM, anchor="c", bold=False)
    P = 2.4; ph = (t % P) / P; ex = -80 + ph * 1100
    envelope(cr, ex, 90, 90); check(cr, ex + 40, 60, 30, GREEN, 1 if ph > .4 else 0)

def t_math(cr, t, d, m):
    vgrad(cr, PW, PH, C("2B2758"), C("4A3E8E"))
    a = -.2 * ease((t - 1.0) / (d * .45))
    rrect(cr, 468, 250, 24, 350, 6, C("C7CFE0")); rrect(cr, 380, 590, 200, 22, 8, C("C7CFE0"))
    push(cr, 480, 250, 1, a); rrect(cr, -300, -9, 600, 18, 9, CREAM); cr.restore(); circle(cr, 480, 250, 18, ACC)
    lx, ly = 480 - 300 * math.cos(a), 250 - 300 * math.sin(a); rx, ry = 480 + 300 * math.cos(a), 250 + 300 * math.sin(a)
    for px, py in ((lx, ly), (rx, ry)):
        line(cr, px, py, px - 100, py + 130, 3, CREAM, .7); line(cr, px, py, px + 100, py + 130, 3, CREAM, .7); rrect(cr, px - 120, py + 128, 240, 14, 7, CREAM)
    for i, (lbl, col) in enumerate([("write it down", ACC), ("re-read it", PINK), ("feel guilty", TEAL)]):
        k = back((t - .6 - i * .8) / .35)
        if k > 0:
            push(cr, lx, ly + 128 - 54 * i - 27, k); rrect(cr, -100, -25, 200, 50, 8, col); text(cr, lbl, 0, 8, 22, INK, anchor="c"); cr.restore()
    k = back((t - .6) / .35)
    if k > 0:
        push(cr, rx, ry + 128 - 27, k); rrect(cr, -80, -25, 160, 50, 8, GREEN); text(cr, "just do it", 0, 8, 22, INK, anchor="c"); cr.restore()
    text(cr, "Tracking it", 190, 660, 28, CREAM, anchor="c"); text(cr, "Doing it", 660, 660, 28, CREAM, anchor="c")

def t_today(cr, t, d, m):
    room(cr, C("E9EEF7"), C("CBD5E8"), C("9AA7C2"))
    rrect(cr, 0, 500, 600, 28, 14, C("5D6680"))
    for i in range(7): circle(cr, 40 + i * 90, 514, 9, C("8E9BBD")); line(cr, 40 + i * 90, 514, 40 + i * 90 + math.cos(t * 6) * 8, 514 + math.sin(t * 6) * 8, 3, INK)
    sp = 150; gap = 260; n = int((t * sp + 80) / gap)
    for i in range(4):
        x = (t * sp + i * gap) % (4 * gap) - 80
        if x < 520: envelope(cr, x, 470, 84)
        elif x < 620:
            q = (x - 520) / 100; check(cr, 560, 440 - q * 60, 44, GREEN, 1 - q * .5)
            for j in range(6): a = j * math.pi / 3; line(cr, 560 + math.cos(a) * (30 + q * 30), 450 + math.sin(a) * (30 + q * 30), 560 + math.cos(a) * (44 + q * 40), 450 + math.sin(a) * (44 + q * 40), 4, ACC, 1 - q)
    st = abs(math.sin((t * sp / gap) * math.pi))
    person(cr, 660, 650, 320, shirt=TEAL, pose=dict(look=-1, la=70 + st * 40, la2=-20, mouth="smile", blink=(t % 3) < .12))
    rrect(cr, 60, 80, 330, 120, 12, INK); text(cr, "Done today", 80, 122, 24, CREAM); text(cr, str(max(0, n)), 80, 184, 56, GREEN, face="Lora")
    text(cr, "To-do list: 0", 215, 180, 22, ACC)
