"""Film 26: Hannibal escapes Fabius's trap with 2,000 oxen carrying burning torches (Ager Falernus, 217 BC)."""
import sys, math
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, pill

ROME = C("D62828"); CARTH = C("7B2CBF"); FIRE = C("FF9F1C")

def flame(cr, x, y, s, t, a=1.0):
    f = 1 + .25 * math.sin(t * 22 + x)
    glow(cr, x, y - s * .3, s * 1.6, FIRE, .45 * a)
    cr.new_path(); cr.move_to(x - s * .5, y); cr.curve_to(x - s * .6, y - s * .8 * f, x, y - s * 1.1 * f, x, y - s * 1.5 * f); cr.curve_to(x, y - s * 1.1 * f, x + s * .6, y - s * .8 * f, x + s * .5, y); cr.close_path(); src(cr, FIRE, a); cr.fill()
    ell(cr, x, y - s * .35, s * .25, s * .4, YEL, a)

def ox(cr, x, y, s, t, fire=True, face=1, run=1.0):
    u = s / 100
    push(cr, x, y); cr.scale(face, 1)
    for i, lx in enumerate((-40, -20, 22, 40)):
        sw = math.sin(t * 9 + i * 1.6) * 8 * u * run
        rrect(cr, lx * u - 6 * u + sw, -36 * u, 12 * u, 36 * u, 5 * u, C("5E3B22"))
    ell(cr, 0, -56 * u, 56 * u, 30 * u, C("7F5539"))
    ell(cr, 56 * u, -66 * u, 22 * u, 20 * u, C("7F5539")); ell(cr, 72 * u, -58 * u, 12 * u, 10 * u, C("B08968"))
    circle(cr, 60 * u, -72 * u, 3.5 * u, INK)
    for sx in (-1, 1):
        hx = 50 * u + sx * 6 * u
        polyline(cr, [(hx, -82 * u), (hx + sx * 10 * u, -98 * u), (hx + sx * 2 * u, -112 * u)], 5 * u, C("EDE0D4"))
        if fire: flame(cr, hx + sx * 2 * u, -112 * u, 14 * u, t + sx)
    line(cr, -56 * u, -60 * u, -66 * u, -36 * u + math.sin(t * 5) * 6 * u, 4 * u, C("5E3B22"))
    cr.restore()

def valley(cr, t, night=0.0):
    sky = lerpc(C("F4A261"), C("0B1026"), night)
    bg(cr, sky, lerpc(C("E76F51"), C("1B2A4A"), night))
    if night > .5:
        for i in range(30): circle(cr, (i * 173) % W, 80 + (i * 97) % 500, 3, WHITE, .3 + .3 * math.sin(t * 3 + i))
    hill = lerpc(C("6A994E"), C("1F3B2D"), night); hill2 = lerpc(C("386641"), C("142821"), night)
    poly(cr, [(-50, 1900), (-50, 700), (180, 520), (420, 760), (420, 1900)], hill2)
    poly(cr, [(1130, 1900), (1130, 680), (880, 500), (660, 760), (660, 1900)], hill2)
    poly(cr, [(-50, 1900), (-50, 980), (300, 880), (540, 1050), (780, 880), (1130, 980), (1130, 1900)], hill)
    rrect(cr, 455, 560, 170, 520, 60, lerpc(C("DDB892"), C("3D3428"), night))

def unit(cr, x, y, col, s=30, a=1.0):
    circle(cr, x, y - s * .8, s * .55, col, a); rrect(cr, x - s * .6, y - s * .3, s * 1.2, s * 1.2, s * .4, col, a)

def o_hook(cr, lt, d, t):
    valley(cr, t, 1.0)
    for i in range(7):
        x = 120 + i * 140 + math.sin(t * 2 + i) * 10; y = 1010 - (i % 2) * 70
        ox(cr, x, y, 160, t + i * .7, run=.8)
    pill(cr, 540, 330, "2,000 OXEN", 92, FIRE, INK, back((lt + .25) / .25) * (1 + .05 * math.sin(t * 7)), -.04)

def o_trap(cr, lt, d, t):
    valley(cr, t, 0.0)
    for i in range(12): unit(cr, 470 + (i % 4) * 46, 1260 + (i // 4) * 60, CARTH, 26)
    k = ease((lt - .3) / (d * .5))
    for i in range(6): unit(cr, 480 + (i % 3) * 60, 640 + (i // 3) * 60 - (1 - k) * 300, ROME, 28, min(1, k * 2))
    for i in range(5): unit(cr, 120 + i * 50, 700 + i * 30, ROME, 24); unit(cr, 960 - i * 50, 700 + i * 30, ROME, 24)
    pill(cr, 540, 470, "PASS: BLOCKED", 54, ROME, WHITE, back((lt - d * .45) / .25), .03)
    pill(cr, 540, 230, "217 BC", 64, WHITE, INK, back((lt - .1) / .25), -.03)

def o_torches(cr, lt, d, t):
    valley(cr, t, .9)
    o = lt / d
    for i in range(3):
        x = 260 + i * 260
        ox(cr, x, 1150 - (i % 2) * 60, 200, t + i, fire=o > (.25 + i * .12), run=.3)
    for i in range(4):
        ph = (t * .9 + i / 4) % 1; circle(cr, 260 + (i * 211) % 600, 900 - ph * 260, 10, FIRE, 1 - ph)
    pill(cr, 540, 300, "TORCHES ON HORNS", 62, FIRE, INK, back((lt - .2) / .25), .04)

def o_hills(cr, lt, d, t):
    valley(cr, t, 1.0)
    p = ease(lt / (d * .9))
    for i in range(18):
        s0 = i / 18; x = 140 + 200 * s0 + 240 * p * (i % 3) / 2; y = 1200 - 520 * p - s0 * 120 + (i % 4) * 30
        flame(cr, x, y, 20, t + i)
    for i in range(6):
        k = ease((lt - .4 - i * .1) / .5); x = 510 + (i % 3) * 60 - k * 320; y = 640 + (i // 3) * 60 + k * 160
        unit(cr, x, y, ROME, 28)
    if lt > d * .4:
        polyline(cr, [(560, 600), (420, 700), (300, 800)], 8, WHITE, .5, dash=[20, 16]); poly(cr, [(280, 815), (300, 780), (320, 815)], WHITE, .6)
    pill(cr, 760, 300, "THE ARMY?!", 66, WHITE, INK, back((lt - .3) / .25), .05)

def o_escape(cr, lt, d, t):
    valley(cr, t, 1.0)
    for i in range(10): flame(cr, 120 + (i * 37) % 260, 760 + (i * 53) % 220, 20, t + i)
    for i in range(6): unit(cr, 180 + (i % 3) * 50, 900 + (i // 3) * 50, ROME, 24)
    p = ease(lt / (d * .9))
    for i in range(16):
        y = 1150 - p * 650 - (i // 4) * 60; x = 490 + (i % 4) * 34
        if y > 380: unit(cr, x, y, CARTH, 24)
    pill(cr, 760, 330, "PASS: EMPTY", 60, C("70E000"), INK, back((lt - .2) / .25), -.04)

def o_end(cr, lt, d, t):
    bg(cr, C("FF9F1C"), C("9D0208")); rays(cr, 540, 640, t, YEL, .14)
    ox(cr, 540, 1000, 420, t, run=.2)
    pill(cr, 540, 300, "GIVE THEM SOMETHING", 58, WHITE, INK, back((lt - .1) / .25), -.03)
    pill(cr, 540, 400, "BIGGER TO CHASE", 58, YEL, INK, back((lt - .35) / .25), .03)

BEATS = [
    dict(say="Hannibal escaped a deadly trap using two thousand cows.", cap="Hannibal escaped a deadly trap using *2,000 cows*.", scene=o_hook),
    dict(say="217 B C. Rome trapped his army in a valley and blocked the only pass out.", cap="217 BC. Rome trapped his army in a valley and *blocked the only pass*.", scene=o_trap),
    dict(say="That night, he tied burning sticks to the horns of the oxen.", cap="That night, he tied *burning sticks* to the horns of the oxen.", scene=o_torches),
    dict(say="Then drove them up the hills. The guards saw the lights and thought his whole army was escaping.", cap="Then drove them *up the hills*. The guards thought his *whole army* was escaping.", scene=o_hills),
    dict(say="They left the pass to chase them. Hannibal just walked out.", cap="They *left the pass* to chase them. Hannibal just *walked out*.", scene=o_escape),
    dict(say="Trapped? Give them something bigger to chase. Send this to a strategy nerd.", cap="Trapped? Give them something *bigger to chase*. Send this to a *strategy nerd*.", scene=o_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("26_oxen", BEATS, voice=("af_heart", 1.08, "en-us"))
    if "--stills" in sys.argv:
        from PIL import Image
        ts = [0.0, 1.5]
        for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
        ims = []
        for n, tt in enumerate(ts):
            p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
        s = Image.new("RGB", (270 * len(ims), 480)); [s.paste(im, (n * 270, 0)) for n, im in enumerate(ims)]; s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])
    else: f.render()
