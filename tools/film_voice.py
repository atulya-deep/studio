"""Film 19: why you hate your own voice in recordings. Full-screen motion style."""
import sys, math
from kit2 import *
from scenes4 import _phone
from motion import Film, W, H

def bg(cr, c1, c2):
    g = cairo.LinearGradient(0, 0, W * .4, H); g.add_color_stop_rgb(0, *c1); g.add_color_stop_rgb(1, *c2); cr.rectangle(-200, -200, W + 400, H + 400); cr.set_source(g); cr.fill()

def rays(cr, x, y, t, col, a=.14, n=14):
    for i in range(n):
        a0 = t * .5 + i * 2 * math.pi / n
        cr.new_path(); cr.move_to(x, y); cr.line_to(x + math.cos(a0) * 2400, y + math.sin(a0) * 2400); cr.line_to(x + math.cos(a0 + .22) * 2400, y + math.sin(a0 + .22) * 2400); cr.close_path(); src(cr, col, a); cr.fill()

def bars(cr, x, y, w, h, n, t, col, amp=None, a=1.0, seed=0.0):
    bw = w / n
    for i in range(n):
        k = amp(i) if amp else 1.0
        v = (.25 + .75 * abs(math.sin(t * (7 + (i * 1.7) % 5) + i * 1.3 + seed))) * k
        rrect(cr, x + i * bw + bw * .18, y - h * v / 2, bw * .64, max(6, h * v), bw * .3, col, a)

def face(cr, x, y, r, t, mood="smile", skin=SKIN, hair=HAIR, hs="short", look=0.0, talk=0.0):
    u = r / 100
    circle(cr, x - 98 * u, y + 5 * u, 20 * u, skin); circle(cr, x + 98 * u, y + 5 * u, 20 * u, skin)
    if hs == "long": rrect(cr, x - 112 * u, y - 60 * u, 224 * u, 190 * u, 60 * u, hair)
    circle(cr, x, y, r, skin)
    cr.new_path(); cr.arc(x, y - 12 * u, 104 * u, math.pi * 1.02, math.pi * 1.98); cr.close_path(); src(cr, hair); cr.fill()
    if hs == "bun": circle(cr, x, y - 118 * u, 40 * u, hair)
    ex, ey = 38 * u, -8 * u; lk = look * 8 * u
    blink = (t % 2.9) < .12
    if mood == "cringe":
        for sx in (-1, 1):
            polyline(cr, [(x + sx * (ex + 16 * u), y + ey - 14 * u), (x + sx * (ex - 12 * u), y + ey), (x + sx * (ex + 16 * u), y + ey + 14 * u)], 9 * u, INK)
        pts = [(x - 36 * u + i * 12 * u, y + 46 * u + (8 * u if i % 2 else -8 * u)) for i in range(7)]; polyline(cr, pts, 8 * u, INK)
        for sx in (-1, 1): ell(cr, x + sx * 62 * u, y + 30 * u, 20 * u, 12 * u, PINK, .55)
    else:
        for sx in (-1, 1):
            if blink and mood != "shock": line(cr, x + sx * ex - 14 * u, y + ey, x + sx * ex + 14 * u, y + ey, 8 * u, INK)
            else:
                rr = 22 * u if mood == "shock" else 15 * u
                if mood == "shock": circle(cr, x + sx * ex, y + ey, rr, WHITE); circle(cr, x + sx * ex + lk, y + ey, 10 * u, INK)
                else: circle(cr, x + sx * ex + lk, y + ey, rr, INK); circle(cr, x + sx * ex + lk + 5 * u, y + ey - 5 * u, 5 * u, WHITE)
            if mood == "smug": line(cr, x + sx * ex - 18 * u, y + ey - 30 * u, x + sx * ex + 18 * u, y + ey - 36 * u + sx * 6 * u, 7 * u, INK)
        if mood == "shock" or talk > .5: ell(cr, x, y + 50 * u, 20 * u, (26 if mood == "shock" else 12 + 14 * talk) * u, C("5A1F2B"))
        else:
            cr.new_path(); cr.arc(x, y + 30 * u, 40 * u, .25, math.pi - .25); cr.set_line_width(9 * u); cr.set_line_cap(cairo.LINE_CAP_ROUND); src(cr, INK); cr.stroke()
        if mood in ("smile", "smug"):
            for sx in (-1, 1): ell(cr, x + sx * 64 * u, y + 34 * u, 18 * u, 11 * u, PINK, .45)

def pill(cr, x, y, txt, size, col, tcol=INK, k=1.0, rot=0.0, face_="Inter"):
    if k <= 0: return
    cr.select_font_face(face_, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); cr.set_font_size(size); w = cr.text_extents(txt).x_advance + size * 1.1
    push(cr, x, y, k, rot); rrect(cr, -w / 2, -size * .85, w, size * 1.7, size * .85, col); text(cr, txt, 0, size * .36, size, tcol, anchor="c", face=face_); cr.restore()

# ---------- scenes ----------
def v_hook(cr, lt, d, t):
    bg(cr, C("FF4D6D"), C("7209B7")); rays(cr, 540, 520, t, WHITE, .1)
    sh = math.sin(t * 46) * 9
    for i in range(4):
        ph = (t * 1.6 + i / 4) % 1; ring(cr, 540, 480, 200 + ph * 480, 16 * (1 - ph) + 2, WHITE, .5 * (1 - ph))
    push(cr, 540 + sh * .6, 470, 1, math.sin(t * 5) * .07)
    _phone(cr, 0, 0, 560, screen=C("F6F0E2"))
    circle(cr, -78, -150, 34, C("25D366")); poly(cr, [(-88, -168), (-88, -132), (-58, -150)], WHITE)
    bars(cr, -110, 0, 220, 190, 9, t, C("7209B7"))
    text(cr, "0:07", 0, 190, 40, INK, anchor="c")
    cr.restore()
    fx, fy = 540 + sh, 990
    face(cr, fx, fy, 190, t, "cringe")
    for sx in (-1, 1): circle(cr, fx + sx * 196, fy + 6, 62, SKIN); circle(cr, fx + sx * 196, fy + 6, 62, C("D99A70"), .25)
    for i in range(3):
        dr = (t * 1.3 + i / 3) % 1; ell(cr, fx + 150 + i * 30, fy - 170 + dr * 70, 10, 16, C("8FD3FF"), 1 - dr)

def v_truth(cr, lt, d, t):
    bg(cr, C("10002B"), C("3C096C")); rays(cr, 540, 560, -t, C("9D4EDD"), .12)
    rrect(cr, 110, 330, 860, 380, 40, WHITE); text(cr, "YOUR VOICE", 160, 410, 40, MUTED)
    bars(cr, 160, 560, 760, 220, 22, t, C("7209B7"))
    ts = d * .5; k = lt - ts
    face(cr, 540 + (math.sin(t * 50) * 8 if 0 < k < .4 else 0), 990, 180, t, "shock" if k > 0 else "cringe")
    if k > 0:
        s = 1 + 2.2 * (1 - ease(k / .18)); sh = math.sin(t * 60) * 10 * max(0, 1 - k * 3)
        push(cr, 540 + sh, 520, s, -.2); rr_path(cr, -330, -105, 660, 210, 26); src(cr, WHITE, .92); cr.fill_preserve(); cr.set_line_width(16); src(cr, RED); cr.stroke()
        text(cr, "100% REAL", 0, 40, 112, RED, anchor="c", face="Lora"); cr.restore()

def _bez(p0, p1, p2, p3, s):
    m = 1 - s
    return (m ** 3 * p0[0] + 3 * m * m * s * p1[0] + 3 * m * s * s * p2[0] + s ** 3 * p3[0], m ** 3 * p0[1] + 3 * m * m * s * p1[1] + 3 * m * s * s * p2[1] + s ** 3 * p3[1])

def v_two(cr, lt, d, t):
    bg(cr, C("006D77"), C("001219"))
    fx, fy, r = 470, 640, 280
    face(cr, fx, fy, r, t, "smile", talk=abs(math.sin(t * 9)), look=.4)
    A = [(fx + 30, fy + 150), (fx + 520, fy + 420), (fx + 620, fy - 260), (fx + 300, fy + 10)]
    pts = [_bez(*A, i / 40) for i in range(41)]; polyline(cr, pts, 12, C("8FD3FF"), .35, dash=[4, 26])
    for i in range(7):
        s = (t * .55 + i / 7) % 1; x, y = _bez(*A, s); circle(cr, x, y, 17, C("8FD3FF"))
    pill(cr, 880, 330, "AIR", 64, C("8FD3FF"), INK, back((lt - .25 * d) / .25), .08)
    k = ease((lt - .55 * d) / .35)
    if k > 0:
        zz = [(fx + 20, fy + 130)] + [(fx + 40 + i * 34, fy + 110 - i * 14 + (24 if i % 2 else -24)) for i in range(1, 7)] + [(fx + 268, fy + 14)]
        n = max(2, int(len(zz) * k)); glow(cr, fx + 150, fy + 70, 190, ACC, .4 * k)
        polyline(cr, zz[:n], 20, ACC); polyline(cr, zz[:n], 7, WHITE, .8)
        pill(cr, 250, 250, "BONE", 64, ACC, INK, back((lt - .6 * d) / .25), -.08)
        for i in range(3):
            ph = (t * 2 + i / 3) % 1; ring(cr, fx, fy, r + 20 + ph * 70, 8, ACC, .6 * (1 - ph) * k)

def v_bass(cr, lt, d, t):
    bg(cr, C("240046"), C("03071E")); th = abs(math.sin(t * 9.5)) ** 2
    for i in range(5): ring(cr, 540, 640, 250 + i * 95 + th * 40, 26 - i * 4, lerpc(ACC, C("9D4EDD"), i / 4), .9 - i * .15)
    glow(cr, 540, 640, 420, ACC, .25 + .2 * th)
    fy = 640 - th * 26
    face(cr, 540, fy, 200, t, "smug")
    ring(cr, 540, fy - 20, 222, 30, INK, 1, math.pi * 1.08, math.pi * 1.92)
    for sx in (-1, 1): rrect(cr, 540 + sx * 215 - 42, fy - 60, 84, 150, 36, INK); rrect(cr, 540 + sx * 215 - 26, fy - 40, 52, 110, 22, C("9D4EDD"))
    bars(cr, 120, 1080, 840, 240, 12, t, ACC, amp=lambda i: 1.0 if i < 5 else .22)
    k = back((lt - .2) / .25) * (1 + .1 * th)
    if k > 0:
        push(cr, 540, 300, k, -.06); text(cr, "+BASS", 0, 40, 170, ACC, anchor="c", face="Lora"); cr.restore()

def v_rec(cr, lt, d, t):
    bg(cr, C("023E8A"), C("03045E"))
    rrect(cr, 470, 190, 140, 250, 70, C("CAD2E0")); rrect(cr, 492, 214, 96, 150, 48, C("8E9BBD"))
    for j in range(4): line(cr, 500, 250 + j * 30, 580, 250 + j * 30, 5, C("5D6680"))
    ring(cr, 540, 390, 110, 12, C("CAD2E0"), 1, .15, math.pi - .15); rrect(cr, 532, 500, 16, 70, 6, C("CAD2E0")); rrect(cr, 470, 566, 140, 18, 9, C("CAD2E0"))
    circle(cr, 690, 220, 18, RED, .5 + .5 * (math.sin(t * 6) > 0)); text(cr, "REC", 720, 234, 40, WHITE)
    drop = ease((lt - .3) / .7)
    bars(cr, 160, 760, 760, 230, 12, t, C("8FD3FF"), amp=lambda i: (1.0 - .8 * drop) if i < 5 else .55)
    if drop > .2:
        for i in range(3):
            x = 220 + i * 110; y = 640 + ((t * 120 + i * 30) % 70); poly(cr, [(x - 22, y), (x + 22, y), (x, y + 34)], RED, min(1, drop))
    ppl = [(SKIN, HAIR, "short"), (SKIN2, C("3B2314"), "long"), (C("F3C9A5"), C("A0522D"), "bun"), (C("8D5524"), INK, "short")]
    for i, (sk, hr, hs) in enumerate(ppl):
        k = back((lt - .5 * d - i * .14) / .25)
        if k > 0:
            x = 165 + i * 250; push(cr, x, 1060 + math.sin(t * 5 + i) * 8, k); face(cr, 0, 0, 96, t + i, "smile", sk, hr, hs); cr.restore()

def v_end(cr, lt, d, t):
    bg(cr, C("FFB703"), C("FB5607")); rays(cr, 540, 600, t, WHITE, .12)
    face(cr, 330, 760, 200, t, "smile", look=.6)
    face(cr, 820, 400, 130, t + 1, "smile", SKIN2, C("3B2314"), "long", look=-.6); face(cr, 850, 900, 130, t + 2, "smile", C("F3C9A5"), C("A0522D"), "bun", look=-.6)
    for i, (x1, y1) in enumerate(((760, 420), (790, 880))):
        ph = (t * .9 + i * .5) % 1; x = 470 + (x1 - 470) * ph - 60; y = 700 + (y1 - 700) * ph - math.sin(ph * math.pi) * 90
        push(cr, x, y, .5 + .5 * math.sin(ph * math.pi)); rrect(cr, -110, -42, 220, 84, 42, C("25D366")); bars(cr, -80, 0, 160, 50, 8, t, WHITE, seed=i); cr.restore()
    for i in range(6):
        ph = (t * .45 + i / 6) % 1; heart(cr, 150 + (i * 167) % 800, 1150 - ph * 1000, (.5 + (i % 3) * .2) * (1 - ph * .4), WHITE if i % 2 else PINK, .9 * (1 - ph))

BEATS = [
    dict(say="You hate your voice in recordings.", cap="You *hate* your voice in recordings.", scene=v_hook),
    dict(say="Here's the awful truth. That is your real voice.", cap="Here's the awful truth. That *is* your *real* voice.", scene=v_truth),
    dict(say="When you speak, you hear yourself two ways. Through the air, and through the bones of your skull.", cap="When you speak, you hear yourself *two ways*. Through the *air*, and through the *bones* of your skull.", scene=v_two),
    dict(say="Your skull adds bass. So in your head, you sound deeper and richer.", cap="Your skull adds *bass*. So in your head, you sound *deeper* and richer.", scene=v_bass),
    dict(say="A recording has no skull. That's the voice everyone else has always heard.", cap="A recording has *no skull*. That's the voice *everyone else* has always heard.", scene=v_rec),
    dict(say="And they still like you. Send this to someone who hates voice notes.", cap="And they *still like you*. Send this to someone who hates *voice notes*.", scene=v_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("19_voice", BEATS)
    if "--stills" in sys.argv:
        from PIL import Image
        ts = [0.0, 1.2]
        for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
        ims = []
        for n, tt in enumerate(ts):
            p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
        s = Image.new("RGB", (270 * len(ims), 480)); [s.paste(im, (n * 270, 0)) for n, im in enumerate(ims)]; s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])
    else: f.render()
