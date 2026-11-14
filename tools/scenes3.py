"""Batch 3 scenes: pratfall effect, Ivy Lee method, Operation Mincemeat. fn(cr, t, d, mouth) on a 960x720 panel."""
from kit2 import *

COFFEE = C("6B3E1F"); NAVY = C("2E3A6B"); CHARC = C("3A3F4E"); PAPER = C("FBF6E9"); LINE_C = C("C9D2E3")
SEA1 = C("0F2A4A"); SEA2 = C("1C4E7A"); KHAKI = C("8A7B4F"); LIFE = C("F2A93B")

def tie(cr, o, col=RED):
    u = o["u"]; hx, hy = o["head"]; x = hx; y0 = hy + 14 * u
    poly(cr, [(x - 3 * u, y0), (x + 3 * u, y0), (x + 4 * u, y0 + 22 * u), (x, y0 + 27 * u), (x - 4 * u, y0 + 22 * u)], col)

def mustache(cr, o, col=C("5A4632")):
    u = o["u"]; hx, hy = o["head"]
    ell(cr, hx - 3.5 * u, hy + 5 * u, 4 * u, 1.8 * u, col, rot=.2); ell(cr, hx + 3.5 * u, hy + 5 * u, 4 * u, 1.8 * u, col, rot=-.2)

def mug(cr, x, y, s, rot=0.0, col=WHITE):
    push(cr, x, y, 1, rot)
    rrect(cr, -s * .5, -s * .6, s, s * 1.1, s * .15, col); ring(cr, s * .55, -s * .1, s * .25, s * .1, col)
    rrect(cr, -s * .42, -s * .58, s * .84, s * .14, s * .06, COFFEE)
    cr.restore()

def splash(cr, x, y, k, s=1.0):
    if k <= 0: return
    for i in range(9):
        a = -math.pi / 2 + (i - 4) * .32; r = (40 + (i % 3) * 22) * k * s
        ell(cr, x + math.cos(a) * r, y + math.sin(a) * r + 30 * k * k * s, (9 - i % 3 * 2) * s, (12 - i % 3 * 2) * s, COFFEE, max(0, 1 - k * .3))

def stains(cr, o, k):
    if k <= 0: return
    u = o["u"]; hx, hy = o["head"]
    for dx, dy, r in [(-6, 22, 6), (4, 30, 7.5), (-2, 40, 5), (8, 20, 4)]:
        circle(cr, hx + dx * u, hy + dy * u, r * u * k, COFFEE, .9)

def audience(cr, n, y, t, cols=None, hearts=0.0, s=1.0):
    cols = cols or [C("232849"), C("2B3159"), C("1E2340")]
    for i in range(n):
        x = (i + .5) * PW / n
        circle(cr, x, y - 70 * s, 38 * s, cols[i % 3]); ell(cr, x, y + 10 * s, 70 * s, 60 * s, cols[i % 3])
        if hearts > 0:
            ph = (t * .6 + i * .37) % 1
            heart(cr, x + 20, y - 130 * s - ph * 110, .3 * hearts * (1 - ph * .5), PINK, (1 - ph) * hearts)

def scoreboard(cr, x, y, w, h, val, lbl):
    rrect(cr, x, y, w, h, 14, C("12162B")); rrect(cr, x + 8, y + 8, w - 16, h - 16, 10, C("1E2547"))
    text(cr, lbl, x + w / 2, y + 44, 24, MUTED, anchor="c")
    text(cr, val, x + w / 2, y + h - 30, 68, ACC, anchor="c", face="Lora")

def podium(cr, x, y, w=170, h=150, col=C("2A3572")):
    poly(cr, [(x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2 - 14, y), (x - w / 2 + 14, y)], col)
    rrect(cr, x - w / 2 - 10, y - h - 14, w + 20, 18, 6, lerpc(col, WHITE, .2))
    circle(cr, x + w / 2 - 34, y - h - 18, 13, RED)

def taperec(cr, x, y, t, spin=True):
    rrect(cr, x, y, 260, 150, 16, C("4A4F63")); rrect(cr, x + 14, y + 112, 232, 24, 6, C("2E3242"))
    for cx in (x + 70, x + 190):
        circle(cr, cx, y + 58, 42, C("1C1F2B")); circle(cr, cx, y + 58, 12, C("B5BCCC"))
        for k in range(3):
            a = (t * 4 if spin else 0) + k * 2 * math.pi / 3
            line(cr, cx, y + 58, cx + math.cos(a) * 32, y + 58 + math.sin(a) * 32, 5, C("8C93A6"))
    line(cr, x + 70, y + 100, x + 190, y + 100, 3, C("6B3E1F"))
    for i in range(4): rrect(cr, x + 34 + i * 54, y + 117, 34, 14, 4, [RED, C("B5BCCC"), C("B5BCCC"), C("B5BCCC")][i])

# ======================= 14 Pratfall effect =======================
def pf_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("1B1A3A"), C("2E2A5C")); rrect(cr, 0, 560, PW, 160, 0, C("151431"))
    poly(cr, [(430, 0), (530, 0), (680, 560), (280, 560)], C("FFF3C4"), .14)
    ell(cr, 480, 562, 200, 24, C("FFF3C4"), .3)
    trip = ease((t - 1.0) / .35); rec = ease((t - 2.2) / .5)
    tilt = trip * .22 - rec * .22
    push(cr, 480, 560, 1, tilt)
    o = person(cr, 0, 0, 330, shirt=NAVY, pants=C("23263A"), pose=dict(ra=30 + trip * 120 - rec * 70, ra2=-90 + trip * 70, la=20 + trip * 60, la2=10,
               mouth="o" if 1 < t < 2.6 else "smile", blink=(t % 2.7) < .12, look=.6))
    tie(cr, o); stains(cr, o, ease((t - 1.3) / .3))
    if t < 1.05:
        rx, ry = o["rh"]; mug(cr, rx + 6, ry - 6, 26)
    cr.restore()
    if t >= 1.05:
        f = min(1, (t - 1.05) / .7)
        cx = 560 + f * 90; cy = 330 - 140 * f + 260 * f * f
        mug(cr, cx, cy, 26, f * 5)
        splash(cr, 545, 380, ease((t - 1.1) / .5))
    audience(cr, 5, 735, t, hearts=ease((t - 2.6) / .6), s=.9)
    bubble(cr, 250, 110, 230, 66, "Oops!", 34, back((t - 1.2) / .4), tail=1)

def pf_tape(cr, t, d, m):
    vgrad(cr, PW, PH, C("17345A"), C("24507F")); rrect(cr, 0, 590, PW, 130, 0, C("13294A"))
    for i in range(5): rrect(cr, 40 + i * 200, 40, 140, 26, 8, ACC if (int(t * 3) + i) % 2 else C("F07A9A"), .5)
    pct = int(92 * ease((t - .6) / 2.2))
    scoreboard(cr, 620, 110, 280, 180, f"{pct}%", "QUESTIONS RIGHT")
    o = person(cr, 470, 600, 300, shirt=C("3FA77A"), pose=dict(ra=95, ra2=-40, la=20, la2=0, mouth="smile", look=.4, blink=(t % 3.1) < .12))
    podium(cr, 470, 600)
    if pct >= 92: text(cr, "★", 470, 170, 70, ACC, appear(t, 2.8, .4), anchor="c")
    taperec(cr, 50, 420, t)
    text(cr, "1966", 60, 120, 58, CREAM, face="Lora")
    cr_t = d * .72
    if t > cr_t:
        k = back((t - cr_t) / .35); push(cr, 300, 300, k, -.12)
        poly(cr, [(-120, -10), (-70, -60), (-30, -30), (10, -80), (40, -30), (110, -55), (80, 0), (130, 40), (60, 40), (40, 90), (0, 45), (-60, 80), (-50, 30), (-130, 40)], RED)
        text(cr, "CRASH!", 0, 14, 40, WHITE, anchor="c"); cr.restore()

def pf_result(cr, t, d, m):
    vgrad(cr, PW, PH, C("EEF1F8"), C("D3DAEA")); rrect(cr, 0, 600, PW, 120, 0, C("A9B4CC"))
    line(cr, 480, 40, 480, 600, 3, C("A9B4CC"), dash=[10, 10])
    for side, (x, shirt, lbl, up) in enumerate([(200, NAVY, "The star", True), (630, C("8C8FA3"), "Average", False)]):
        text(cr, lbl, x, 80, 38, DK, anchor="c", face="Lora")
        o = person(cr, x + 50, 610, 300, shirt=shirt, pants=C("23263A"), pose=dict(mouth="o" if t < 1.5 else ("smile" if up else "frown"), la=25, la2=-60, ra=25, ra2=-60, look=1, blink=((t + side) % 3) < .12))
        if up: tie(cr, o)
        stains(cr, o, 1)
        k = ease((t - 1.2 - side * .9) / 1.0)
        base = 560; h0 = 220
        h = h0 + (110 if up else -150) * k
        col = GREEN if up else RED
        rrect(cr, x - 130, base - h, 70, h, 10, col)
        text(cr, "liking", x - 95, base + 30, 22, DK, anchor="c")
        if k > .5:
            ax = x - 95; ay = base - h - 40
            if up: poly(cr, [(ax - 24, ay + 10), (ax + 24, ay + 10), (ax, ay - 26)], GREEN, appear(t, 1.8 + side * .9, .3))
            else: poly(cr, [(ax - 24, ay - 10), (ax + 24, ay - 10), (ax, ay + 26)], RED, appear(t, 1.8 + side * .9, .3))
        if up: text(cr, "★", x + 50, 260, 46, ACC, anchor="c")

def pf_why(cr, t, d, m):
    vgrad(cr, PW, PH, C("2B2758"), C("4A3E8E")); rrect(cr, 0, 620, PW, 100, 0, C("231F48"))
    k = ease((t - d * .45) / 1.2)
    h = 300 - 250 * k
    glow(cr, 480, 620 - h - 150, 180 * (1 - k * .6), C("FFE3A3"), .5)
    rrect(cr, 400, 620 - h, 160, h, 8, C("B5BCCC")); rrect(cr, 385, 620 - h, 190, 22, 6, C("D6DBE6"))
    o = person(cr, 480, 620 - h, 230 + 60 * k, shirt=NAVY, pants=C("23263A"),
               pose=dict(mouth="smile", la=10 + 20 * (1 - k), ra=10 + 150 * k, ra2=40 * k, blink=(t % 3) < .12))
    tie(cr, o)
    if k > .3: stains(cr, o, ease((k - .3) / .4))
    if k < .2: ring(cr, o["head"][0], o["head"][1] - 52, 30, 6, ACC, 1 - k * 5, 0, 2 * math.pi)
    gap = 360 * (1 - k)
    for i, x in enumerate((130, 230, 730, 830)):
        xx = x + (gap * .4 if x < 480 else -gap * .4) * 0 + ((1 if x < 480 else -1) * 100 * k)
        person(cr, xx, 640, 200, shirt=[C("3FA77A"), C("D9644A"), C("6B5BD2"), C("4F7DD9")][i],
               pose=dict(look=1 if x < 480 else -1, mouth="smile" if k > .5 else "flat", hairstyle=["long", "short", "bun", "short"][i], blink=((t + i) % 3) < .12))
    bubble(cr, 220, 220, 330, 62, "Too perfect = distant", 26, back((t - .5) / .4) * (1 - ease((t - d * .45) / .3)))
    bubble(cr, 480, 120, 260, 62, "Human = likeable", 26, back((t - d * .45 - 1.0) / .4))
    if k > .6:
        for i in range(3):
            ph = (t * .5 + i / 3) % 1; heart(cr, 330 + i * 150, 330 - ph * 120, .3 * (1 - ph) + .1, PINK, 1 - ph)

def pf_use(cr, t, d, m):
    room(cr, C("EAF2F6"), C("D2E2EC"), C("9DB4C4"), fy=590)
    rrect(cr, 380, 90, 500, 300, 12, WHITE); rrect(cr, 380, 90, 500, 300, 12, C("C9D2E3"), .25)
    pts = [(420, 340), (520, 300), (610, 310), (700, 220), (820, 150)]
    pr = ease(t / 1.5); n = int(pr * 4)
    polyline(cr, pts[:n + 1] if n >= 1 else pts[:2], 8, GREEN)
    spill = ease((t - 1.6) / .3)
    o = person(cr, 300, 600, 330, shirt=TEAL, pants=C("23263A"), pose=dict(ra=95 - spill * 40, ra2=-60, la=20 + spill * 30, la2=-30, look=1 - spill,
               mouth="o" if 1.6 < t < 2.4 else "smile", blink=(t % 2.6) < .12))
    stains(cr, o, spill)
    if spill > 0: splash(cr, 260, 400, ease((t - 1.6) / .5), .7)
    else:
        lx, ly = o["lh"]; mug(cr, lx - 6, ly - 6, 22)
    for i, x in enumerate((620, 800)):
        laugh = t > 2.4
        person(cr, x, 650, 230, shirt=[C("6B5BD2"), C("D9644A")][i], pose=dict(sit=True, face=-1, look=-1, mouth="o" if laugh and (int(t * 6) + i) % 2 else "smile",
               hairstyle=["long", "short"][i], la=40, la2=60, ra=40, ra2=60))
    desk(cr, 540, 520, 380, legs=70)
    bubble(cr, 250, 110, 300, 64, "Ha! Classic me.", 28, back((t - 2.5) / .4), tail=0)
    if t > 2.9:
        for i in range(2): text(cr, "ha", 640 + i * 180, 380 - (t * 20 % 30), 30, DK, appear(t, 2.9 + i * .3, .3))
    check(cr, 450, 110, 44, GREEN, back((t - 3.4) / .4))

# ======================= 15 Ivy Lee method =======================
def notepad(cr, x, y, w, h, n=6, prog=1.0, done=0.0, nums=True, rot=0.0):
    push(cr, x, y, 1, rot)
    rrect(cr, 0, 0, w, h, 12, PAPER); rrect(cr, 0, 0, w, 40, 12, C("E5484D")); rrect(cr, 0, 26, w, 14, 0, C("E5484D"))
    for i in range(7): circle(cr, 30 + i * (w - 60) / 6, 14, 6, C("8A2B2E"))
    lh = (h - 70) / n; ws = [.7, .55, .8, .5, .65, .6, .5, .7, .45, .6]
    for i in range(n):
        yy = 60 + i * lh + lh * .5
        line(cr, 24, yy + lh * .32, w - 24, yy + lh * .32, 1.5, LINE_C)
        k = max(0, min(1, prog * n - i))
        if k <= 0: continue
        if nums: text(cr, str(i + 1), 34, yy + 10, min(30, lh * .55), DK, k)
        rrect(cr, 74, yy - 4, (w - 110) * ws[i % 10] * k, min(10, lh * .2), 4, C("3B4790"), .85)
        dk = max(0, min(1, done * n - i))
        if dk > 0: check(cr, w - 34, yy - 2, min(28, lh * .5), GREEN, dk)
    cr.restore()

def cheque(cr, x, y, w, k=1.0, rot=0.0, amt="$25,000"):
    if k <= 0: return
    h = w * .42; push(cr, x, y, k, rot)
    rrect(cr, -w / 2, -h / 2, w, h, 12, C("EAF4E4")); rrect(cr, -w / 2 + 10, -h / 2 + 10, w - 20, h - 20, 8, C("CFE5C6"), .35)
    text(cr, "PAY TO: IVY LEE", -w / 2 + 30, -h / 2 + 52, w * .045, C("2E5A3A"))
    rrect(cr, w / 2 - w * .44, -h * .12, w * .38, h * .3, 8, WHITE)
    text(cr, amt, w / 2 - w * .25, h * .1, w * .07, C("1E5A2E"), anchor="c", face="Lora")
    line(cr, -w / 2 + 30, h * .3, -w * .05, h * .3, 2, C("2E5A3A"))
    polyline(cr, [(-w / 2 + 40, h * .27), (-w / 2 + 70, h * .18), (-w / 2 + 90, h * .28), (-w / 2 + 120, h * .16), (-w / 2 + 150, h * .26)], 3, INK)
    text(cr, "C. M. SCHWAB", -w / 2 + 30, h * .42, w * .032, C("2E5A3A"), bold=False)
    cr.restore()

def iv_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("1D3B2C"), C("2E5A42"))
    for i in range(14):
        ph = (t * .3 + i * .071) % 1
        text(cr, "$", (i * 137) % PW, PH - ph * PH, 30 + i % 3 * 10, ACC, .3 * (1 - ph))
    notepad(cr, 90, 120, 300, 440, prog=ease((t - .2) / 1.2), rot=-.06)
    cheque(cr, 610, 360, 520, back((t - 1.2) / .6), rot=.08 + math.sin(t * 1.5) * .02)
    if t > 2: text(cr, "= a to-do list?", 610, 600, 40, CREAM, appear(t, 2, .4), anchor="c", face="Lora")

def mill_window(cr, x, y, w, h, t):
    rrect(cr, x - 10, y - 10, w + 20, h + 20, 8, C("5A4632"))
    rrect(cr, x, y, w, h, 4, C("F2A65E"))
    glow(cr, x + w * .6, y + h, w * .6, C("FFD27A"), .6)
    for i, (cx, ch) in enumerate([(.2, .7), (.45, .85), (.7, .6)]):
        rrect(cr, x + w * cx, y + h * (1 - ch), w * .08, h * ch, 2, C("3A2E2A"))
        for j in range(3):
            ph = (t * .4 + j / 3 + i * .2) % 1
            circle(cr, x + w * cx + w * .04 + ph * 30, y + h * (1 - ch) - ph * 60, 10 + ph * 16, C("8C8FA3"), .6 * (1 - ph))
    rrect(cr, x, y + h * .72, w, h * .28, 0, C("4A3A33"))
    line(cr, x + w / 2, y, x + w / 2, y + h, 6, C("5A4632")); line(cr, x, y + h / 2, x + w, y + h / 2, 6, C("5A4632"))

def clock(cr, x, y, r, frac, col=WHITE):
    circle(cr, x, y, r, col); ring(cr, x, y, r, r * .1, DK)
    cr.new_path(); cr.move_to(x, y); cr.arc(x, y, r * .8, -math.pi / 2, -math.pi / 2 + 2 * math.pi * max(.001, frac)); cr.close_path(); src(cr, ACC, .8); cr.fill()
    line(cr, x, y, x, y - r * .7, r * .08, DK); circle(cr, x, y, r * .08, DK)

def iv_office(cr, t, d, m):
    room(cr, C("E8DCC4"), C("D6C3A2"), C("8B6A4A"), fy=600)
    mill_window(cr, 90, 80, 330, 240, t)
    o = person(cr, 300, 600, 330, shirt=CHARC, pants=C("23263A"), hair=C("8C8FA3"), pose=dict(la=60, la2=40, ra=60, ra2=40, mouth="flat", look=1, blink=(t % 3.3) < .12))
    mustache(cr, o, C("8C8FA3")); tie(cr, o, C("6B3E1F"))
    desk(cr, 80, 470, 420, legs=110)
    rrect(cr, 140, 440, 90, 30, 4, PAPER); rrect(cr, 380, 430, 26, 40, 4, C("2B2B38"))
    text(cr, "Charles Schwab", 290, 650, 26, DK, anchor="c")
    wx = 900 - 200 * ease(t / 1.6)
    pose = walk_pose(t) if t < 1.6 else dict(ra=150, ra2=10, la=15)
    pose.update(look=-1, mouth="smile", blink=(t % 2.9) < .12)
    o2 = person(cr, wx, 620, 360, shirt=C("3B5998"), pants=C("2E3550"), pose=pose); tie(cr, o2, ACC); glasses(cr, o2)
    text(cr, "Ivy Lee", wx - 120, 680, 26, DK, anchor="c")
    k = back((t - 1.8) / .5)
    if k > 0:
        push(cr, 690, 150, k); cloud(cr, 0, 0, 340, 170, WHITE, .97); clock(cr, -70, 0, 44, min(1, (t - 1.8) / 2) * .25)
        text(cr, "15 min", 50, 12, 34, DK, anchor="c"); cr.restore()
    text(cr, "1918", 840, 60, 50, DK, appear(t, .3, .4), face="Lora", anchor="c")

def iv_list(cr, t, d, m):
    vgrad(cr, PW, PH, C("17345A"), C("24507F"))
    wr = ease((t - .3) / 2.0); dn = ease((t - 2.8) / (d - 4.2)) * (5 / 6)
    notepad(cr, 230, 50, 400, 600, prog=wr, done=dn)
    # pencil writing
    if wr < 1:
        i = int(wr * 6); yy = 50 + 60 + i * (530 / 6) + 30
        push(cr, 560 + math.sin(t * 14) * 10, yy, 1, .6)
        rrect(cr, -6, -90, 14, 90, 3, YEL); poly(cr, [(-6, 0), (8, 0), (1, 16)], C("E9C79A")); cr.restore()
    k = appear(t, d - 1.6, .5)
    if k > 0:
        polyline(cr, [(220, 560), (130, 560), (130, 610)], 6, ACC, k)
        poly(cr, [(115, 600), (145, 600), (130, 625)], ACC, k)
        text(cr, "tomorrow", 130, 670, 34, ACC, k, anchor="c", face="Lora")
    text(cr, "Rank", 110, 200, 34, CREAM, appear(t, 2.2, .4), anchor="c"); text(cr, "1 → 6", 110, 250, 34, ACC, appear(t, 2.4, .4), anchor="c")
    text(cr, "One", 800, 200, 34, CREAM, appear(t, 3.0, .4), anchor="c"); text(cr, "at a time", 800, 250, 30, ACC, appear(t, 3.2, .4), anchor="c")

def iv_cheque(cr, t, d, m):
    vgrad(cr, PW, PH, C("2B2758"), C("4A3E8E"))
    # calendar flip
    pages = int(min(3, t / .5))
    push(cr, 160, 170, 1)
    rrect(cr, -90, -90, 180, 190, 14, WHITE); rrect(cr, -90, -90, 180, 50, 14, RED); rrect(cr, -90, -54, 180, 14, 0, RED)
    text(cr, ["JAN", "FEB", "MAR", "APR"][pages], 0, -52, 30, WHITE, anchor="c")
    text(cr, f"+{pages}", 0, 50, 64, DK, anchor="c", face="Lora")
    cr.restore()
    text(cr, "months", 160, 320, 30, CREAM, anchor="c")
    k = ease((t - .6) / .8)
    ex = 1100 - 520 * k
    if t < 2.2: envelope(cr, ex, 380, 300)
    ck = back((t - 2.0) / .6)
    cheque(cr, 560, 360, 600, ck, rot=-.04)
    for i in range(10):
        if t < 2.4: break
        ph = (t * .7 + i * .1) % 1
        circle(cr, 200 + i * 60, 650 + 20 * math.sin(i * 2), 6 * (1 - ph) + 2, ACC, 1 - ph)
    text(cr, "≈ hundreds of thousands today", 480, 580, 32, ACC, appear(t, 3.0, .5), anchor="c", face="Lora")

def iv_tonight(cr, t, d, m):
    vgrad(cr, PW, PH, C("101433"), C("1E2550")); rrect(cr, 0, 560, PW, 160, 0, C("2E2A3A"))
    rrect(cr, 600, 60, 300, 230, 8, C("5A4632")); rrect(cr, 612, 72, 276, 206, 4, C("17204A"))
    circle(cr, 820, 130, 30, C("FFF3C4"))
    for i, (sx, sy) in enumerate([(660, 110), (720, 200), (700, 140), (860, 230)]): circle(cr, sx, sy, 2.5, WHITE, .5 + .4 * math.sin(t * 3 + i))
    desk(cr, 60, 520, 840, legs=200)
    glow(cr, 220, 460, 260, C("FFD27A"), .35)
    polyline(cr, [(150, 518), (150, 420), (220, 360)], 8, C("4A4F63")); poly(cr, [(190, 340), (270, 360), (240, 400)], ACC)
    o = person(cr, 760, 640, 300, shirt=C("D9644A"), pose=dict(sit=True, face=-1, look=-1, la=70, la2=50, ra=70, ra2=50, mouth="smile", blink=(t % 3) < .12, hairstyle="bun"))
    # list of 10 lines, 7-10 crossed out
    push(cr, 330, 130, 1, -.03)
    rrect(cr, 0, 0, 260, 390, 10, PAPER)
    for i in range(10):
        yy = 30 + i * 35; k = ease((t - .2 - i * .12) / .3)
        text(cr, str(i + 1), 18, yy + 10, 20, DK, k)
        rrect(cr, 50, yy, 170 * [.9, .7, .8, .6, .75, .65, .8, .55, .7, .6][i] * k, 8, 4, C("3B4790"), .85 * (1 - (i >= 6) * .6 * ease((t - 2.2) / .4)))
        if i >= 6: line(cr, 40, yy + 4, 40 + 190 * ease((t - 2 - (i - 6) * .15) / .3), yy + 4, 4, RED)
    cr.restore()
    text(cr, "Six.", 470, 640, 54, ACC, appear(t, 2.8, .4), anchor="c", face="Lora")
    ring(cr, 357, 164, 22, 4, GREEN, appear(t, 3.4, .4), 0, 2 * math.pi * ease((t - 3.4) / .5) + .001)

# ======================= 16 Operation Mincemeat =======================
def mm_map_draw(cr, t, sic=0.0, greece=0.0, sard=0.0):
    vgrad(cr, PW, PH, C("1F4E7A"), C("2B6A9A"))
    for i in range(6):
        y = 60 + i * 120 + math.sin(t + i) * 4
        polyline(cr, [(x, y + math.sin(x / 40 + t * 2) * 4) for x in range(0, PW + 40, 40)], 2, WHITE, .08)
    sand = C("E8D5A6")
    f = lambda p: (110 + p[0] * .5, 10 + p[1] * .5)
    from scenes import ITALY
    poly(cr, [f(p) for p in ITALY], sand)
    poly(cr, [(0, 0), (360, 0), (330, 60), (230, 80), (0, 120)], sand)              # France/Alps
    poly(cr, [(560, 0), (960, 0), (960, 200), (800, 250), (700, 190), (620, 90)], sand)  # Balkans
    G = [(700, 250), (790, 240), (820, 300), (780, 330), (800, 380), (760, 420), (740, 380), (700, 400), (690, 330)]
    poly(cr, G, lerpc(sand, RED, greece * .5))                                       # Greece
    S = [(230, 250), (270, 245), (275, 320), (240, 340), (225, 300)]
    poly(cr, S, lerpc(sand, RED, sard * .5))                                         # Sardinia
    SI = [(480, 360), (560, 350), (540, 410)]
    poly(cr, SI, lerpc(sand, GREEN, sic * .6))                                      # Sicily
    poly(cr, [(0, 520), (180, 500), (330, 470), (420, 420), (470, 440), (520, 520), (700, 560), (960, 560), (960, 720), (0, 720)], C("E0C08A"))  # N. Africa
    text(cr, "SICILY", 520, 455, 22, DK, anchor="c"); text(cr, "SARDINIA", 250, 380, 22, DK, anchor="c"); text(cr, "GREECE", 760, 470, 22, DK, anchor="c")
    text(cr, "NORTH AFRICA", 230, 640, 26, C("8A6A3A"), anchor="c")
    return dict(sic=(515, 375), gr=(760, 330), sa=(250, 295), af=(440, 470))

def arrow(cr, a, b, k, col, w=10):
    if k <= 0: return
    x = a[0] + (b[0] - a[0]) * k; y = a[1] + (b[1] - a[1]) * k
    line(cr, a[0], a[1], x, y, w, col)
    ang = math.atan2(y - a[1], x - a[0])
    poly(cr, [(x + math.cos(ang) * 22, y + math.sin(ang) * 22), (x + math.cos(ang + 2.4) * 22, y + math.sin(ang + 2.4) * 22), (x + math.cos(ang - 2.4) * 22, y + math.sin(ang - 2.4) * 22)], col)

def briefcase(cr, x, y, s, k=1.0, rot=0.0, stamp=True):
    if k <= 0: return
    push(cr, x, y, k, rot)
    rrect(cr, -s * .22, -s * .52, s * .44, s * .16, s * .06, C("3A2A1E"))
    rrect(cr, -s * .16, -s * .46, s * .32, s * .1, s * .04, C("1B2140"))
    rrect(cr, -s * .5, -s * .4, s, s * .7, s * .06, C("6B4A2B")); rrect(cr, -s * .5, -s * .4, s, s * .14, s * .06, C("5A3E24"))
    rrect(cr, -s * .06, -s * .3, s * .12, s * .08, 3, GOLD)
    if stamp:
        push(cr, 0, s * .02, 1, -.15); rr_path(cr, -s * .36, -s * .1, s * .72, s * .18, 6); cr.set_line_width(4); src(cr, RED); cr.stroke()
        text(cr, "TOP SECRET", 0, s * .04, s * .1, RED, anchor="c"); cr.restore()
    cr.restore()

def mm_hook(cr, t, d, m):
    vgrad(cr, PW, PH, C("12182E"), C("22304F"))
    for i in range(8):
        ph = (t * .2 + i / 8) % 1
        text(cr, "?", 60 + i * 120, PH - ph * PH, 50, ACC, .25 * (1 - ph), face="Lora")
    briefcase(cr, 480, 400, 420, back((t - .2) / .6), rot=math.sin(t * 1.3) * .03)
    a = t * 1.2
    gx, gy = 480 + math.cos(a) * 150, 360 + math.sin(a * 1.3) * 70
    ring(cr, gx, gy, 70, 12, C("C7CFE0"), appear(t, .9, .4)); circle(cr, gx, gy, 64, C("BFE0F7"), .18 * appear(t, .9, .4))
    line(cr, gx + 50, gy + 50, gx + 110, gy + 110, 18, C("5A3E24"), appear(t, .9, .4))
    text(cr, "1943", 70, 100, 58, CREAM, face="Lora")

def mm_map(cr, t, d, m):
    P = mm_map_draw(cr, t, sic=.5 + .5 * math.sin(t * 4))
    arrow(cr, (440, 500), P["sic"], ease((t - .6) / 1.0), C("4F7DD9"), 12)
    k = back((t - 2.0) / .5)
    bubble(cr, 700, 120, 330, 70, "Too obvious!", 34, k, tail=-1)
    if t > 3.2:
        push(cr, 520, 260, back((t - 3.2) / .4)); cloud(cr, 0, 0, 360, 130, WHITE, .95); text(cr, "So... a lie.", 0, 10, 32, DK, anchor="c", face="Lora"); cr.restore()

def waves(cr, t, y0, col, a=1.0, amp=10):
    pts = [(x, y0 + math.sin(x / 50 + t * 2) * amp) for x in range(-40, PW + 41, 20)]
    poly(cr, pts + [(PW + 40, PH + 10), (-40, PH + 10)], col, a)

def submarine(cr, x, y, s):
    u = s / 100
    ell(cr, x, y, 100 * u, 20 * u, C("3A4152")); rrect(cr, x - 22 * u, y - 46 * u, 44 * u, 34 * u, 6 * u, C("4A5266"))
    line(cr, x + 6 * u, y - 46 * u, x + 6 * u, y - 70 * u, 3 * u, C("4A5266")); line(cr, x + 6 * u, y - 70 * u, x + 16 * u, y - 70 * u, 3 * u, C("4A5266"))
    text(cr, "SERAPH", x - 70 * u, y + 6 * u, 10 * u, C("8C93A6"))

def mm_sub(cr, t, d, m):
    vgrad(cr, PW, PH, C("0B1430"), C("1A2A55"))
    circle(cr, 160, 110, 42, C("FFF3C4")); glow(cr, 160, 110, 120, C("FFF3C4"), .25)
    for i, (sx, sy) in enumerate([(320, 70), (450, 130), (600, 60), (520, 200), (380, 220)]): circle(cr, sx, sy, 2.5, WHITE, .5 + .4 * math.sin(t * 3 + i))
    # Spanish coast + lighthouse
    poly(cr, [(720, 360), (800, 330), (960, 300), (960, 470), (700, 470)], C("3B3A3F"))
    rrect(cr, 860, 230, 26, 90, 3, WHITE); rrect(cr, 856, 220, 34, 14, 3, RED); circle(cr, 873, 215, 9, C("FFE9B0"))
    ba = math.sin(t * 1.2) * .6 + math.pi
    poly(cr, [(873, 215), (873 + math.cos(ba - .08) * 600, 215 + math.sin(ba - .08) * 600), (873 + math.cos(ba + .08) * 600, 215 + math.sin(ba + .08) * 600)], C("FFF3C4"), .12)
    text(cr, "SPAIN", 830, 420, 26, MUTED, anchor="c")
    waves(cr, t * .7, 440, SEA1, .9, 6)
    submarine(cr, 220, 470, 200)
    for i, x in enumerate((185, 215)):
        person(cr, x, 422 - (i == 0) * 2, 70, shirt=C("2B3159"), pants=C("1E2340"), pose=dict(look=1, mouth="flat", helmet=C("1E2340")))
    # floating officer drifting to coast
    k = ease((t - .8) / (d - 1.5))
    fx = 420 + 320 * k; fy = 505 + math.sin(t * 2) * 6
    push(cr, fx, fy, 1, math.pi / 2 - .1)
    o = person(cr, 0, 0, 130, shirt=KHAKI, pants=C("5A5236"), pose=dict(blink=True, mouth="flat", la=10, ra=10))
    u = o["u"]; rrect(cr, -17 * u, -80 * u, 34 * u, 26 * u, 8 * u, LIFE)
    cr.restore()
    briefcase(cr, fx - 30, fy + 40, 70, 1, .2, stamp=False)
    waves(cr, t, 520, SEA2, .85, 10)
    text(cr, "30 April 1943", 40, 680, 44, CREAM, face="Lora")

def photo(cr, x, y, w, k, rot):
    if k <= 0: return
    push(cr, x, y, k, rot); rrect(cr, -w / 2, -w * .6, w, w * 1.2, 6, WHITE); rrect(cr, -w * .42, -w * .52, w * .84, w * .84, 4, C("BFD3E6"))
    circle(cr, 0, -w * .18, w * .17, SKIN); cr.new_path(); cr.arc(0, -w * .2, w * .19, math.pi, 2 * math.pi); src(cr, HAIR); cr.fill()
    rrect(cr, -w * .2, -w * .14 + w * .14, w * .4, w * .2, 6, PINK); heart(cr, w * .3, w * .45, .25, RED); cr.restore()

def ticket(cr, x, y, w, k, rot):
    if k <= 0: return
    push(cr, x, y, k, rot); rrect(cr, -w / 2, -w * .22, w, w * .44, 6, ACC)
    line(cr, w * .2, -w * .2, w * .2, w * .2, 3, C("B07A1E"), dash=[6, 6]); text(cr, "THEATRE", -w * .12, w * .06, w * .12, C("5A3E24"), anchor="c"); cr.restore()

def receipt(cr, x, y, w, k, rot):
    if k <= 0: return
    push(cr, x, y, k, rot); rrect(cr, -w / 2, -w * .7, w, w * 1.4, 4, WHITE)
    text(cr, "RECEIPT", 0, -w * .45, w * .15, DK, anchor="c")
    for i in range(4): rrect(cr, -w * .38, -w * .25 + i * w * .2, w * .5, w * .06, 3, C("9AA3B5"))
    ring(cr, w * .2, w * .48, w * .12, w * .04, GOLD); circle(cr, w * .2, w * .34, w * .05, C("BFE0F7"))
    cr.restore()

def mm_pockets(cr, t, d, m):
    split = d * .5
    if t < split:
        vgrad(cr, PW, PH, C("3A2E2A"), C("5A4632"))
        rrect(cr, 300, 470, 360, 200, 20, C("2A1E18")); rrect(cr, 300, 470, 360, 60, 20, C("3A2A1E"))
        items = [(photo, 200, 260, 170, -.15, .3), (ticket, 480, 160, 220, .1, .9), (envelope, 760, 250, 200, 0, 1.5), (receipt, 520, 370, 150, -.05, 2.1)]
        for fn, x, y, w, rot, t0 in items:
            k = back((t - t0) / .45)
            if fn is envelope:
                if k > 0: push(cr, x, y, k, .08); envelope(cr, 0, 0, w); heart(cr, 0, 6, .25, RED); cr.restore()
            else: fn(cr, x, y, w, k, rot)
        bubble(cr, 480, 630, 340, 56, "Pocket litter", 28, back((t - 2.6) / .4))
    else:
        tt = t - split
        P = mm_map_draw(cr, t, sic=ease((tt - 2.2) / .5), greece=ease((tt - .3) / .6), sard=ease((tt - .3) / .6))
        for i in range(3):
            arrow(cr, (520 + i * 40, 60), (P["gr"][0] - 30 + i * 20, P["gr"][1] - 40), ease((tt - .4 - i * .15) / 1.0), C("8C8FA3"), 7)
        arrow(cr, (330, 60), (P["sa"][0] + 10, P["sa"][1] - 50), ease((tt - .6) / 1.0), C("8C8FA3"), 7)
        arrow(cr, (440, 500), P["sic"], ease((tt - 1.9) / .7), C("4F7DD9"), 12)
        if tt > 2.4:
            k = back((tt - 2.4) / .4); push(cr, P["sic"][0], P["sic"][1] - 70, k); text(cr, "July 1943", 0, 0, 34, WHITE, anchor="c", face="Lora"); cr.restore()

def mm_lesson(cr, t, d, m):
    room(cr, C("EEF1F8"), C("D3DAEA"), C("A9B4CC"), fy=600)
    o = person(cr, 250, 610, 340, shirt=C("3B5998"), pants=C("23263A"), pose=dict(ra=100, ra2=-30, la=20, mouth="smile", look=1, blink=(t % 2.8) < .12))
    tie(cr, o, ACC)
    # left: vague claim crossed, right: specifics checked
    bubble(cr, 250, 110, 280, 62, "\"Trust me.\"", 30, back((t - .3) / .4), tail=0)
    cross(cr, 400, 110, 50, RED, back((t - 1.1) / .4))
    items = [(receipt, 560, 330, 120, -.1, 1.6), (ticket, 760, 260, 170, .12, 1.9), (photo, 760, 450, 130, .08, 2.2)]
    for fn, x, y, w, rot, t0 in items: fn(cr, x, y, w, back((t - t0) / .4), rot)
    check(cr, 860, 120, 56, GREEN, back((t - 2.8) / .4))
    text(cr, "Show the receipts", 600, 560, 38, DK, appear(t, 3.1, .4), anchor="c", face="Lora")
