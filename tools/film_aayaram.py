"""Film 28: Aaya Ram, Gaya Ram. Gaya Lal's 1967 party switches and the 1985 anti-defection law. Non-partisan: generic party colours, no symbols."""
import sys, math
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, pill

PA = C("2A9D8F"); PB = C("E76F51"); KURTA = C("F8F9FA"); CAP = C("FFFFFF")

def neta(cr, x, y, s, t, walk=0.0, face=1, mouth="smile", arms=None):
    pose = dict(mouth=mouth, look=face, blink=(t % 2.8) < .12)
    if walk: pose.update(swing=math.sin(t * 14), la=12 - math.sin(t * 14) * 30, ra=12 + math.sin(t * 14) * 30)
    if arms: pose.update(arms)
    o = person(cr, x, y, s, shirt=KURTA, pants=C("E9ECEF"), skin=SKIN2, pose=pose)
    hx, hy = o["head"]; u = o["u"]
    poly(cr, [(hx - 13 * u, hy - 8 * u), (hx + 13 * u, hy - 8 * u), (hx + 10 * u, hy - 17 * u), (hx - 10 * u, hy - 17 * u)], CAP)
    line(cr, hx - 13 * u, hy - 8 * u, hx + 13 * u, hy - 8 * u, 1.2 * u, C("CED4DA"))
    ell(cr, hx, hy + 5 * u, 7 * u, 2.2 * u, INK, .9)
    return o

def office(cr, x, y, col, lbl, k=1.0, glowk=0.0):
    if glowk > 0: glow(cr, x, y - 200, 300, col, .45 * glowk)
    rrect(cr, x - 190, y - 380, 380, 380, 16, col, k)
    poly(cr, [(x - 220, y - 380), (x + 220, y - 380), (x, y - 500)], lerpc(col, INK, .25), k)
    rrect(cr, x - 70, y - 220, 140, 220, 70, C("1B1B3A"), k)
    text(cr, lbl, x, y - 290, 60, WHITE, k, anchor="c", face="Lora")

def hop_x(t, a, b, period):
    ph = (t % period) / period
    if ph < .5: return a + (b - a) * ease(ph / .5), 1 if b > a else -1
    return b + (a - b) * ease((ph - .5) / .5), 1 if a > b else -1

def g_hook(cr, lt, d, t):
    bg(cr, C("FFD166"), C("EF476F")); rays(cr, 540, 760, t, WHITE, .1)
    office(cr, 200, 1150, PA, "A"); office(cr, 880, 1150, PB, "B")
    x, f = hop_x(t, 260, 820, 1.4)
    neta(cr, x, 1160, 420, t, walk=1, face=f)
    for i in range(3):
        ph = (t * 2 + i / 3) % 1; line(cr, x - f * (60 + ph * 80), 950 + i * 40, x - f * (110 + ph * 120), 950 + i * 40, 8, WHITE, 1 - ph)
    pill(cr, 540, 330, "1967", 96, INK, WHITE, back((lt + .25) / .25) * (1 + .04 * math.sin(t * 7)), -.04)

def g_count(cr, lt, d, t):
    bg(cr, C("14213D"), C("000814"))
    office(cr, 200, 1100, PA, "A", glowk=.6 + .4 * math.sin(t * 4)); office(cr, 880, 1100, PB, "B", glowk=.6 + .4 * math.cos(t * 4))
    n = min(3, int(lt / (d / 3.2)) + 1)
    xs = [260, 820, 260, 820]; ph = min(1, (lt % (d / 3.2)) / (d / 3.2) * 1.6)
    x = xs[n - 1] + (xs[n] - xs[n - 1]) * ease(ph)
    neta(cr, x, 1110, 360, t, walk=1 if ph < 1 else 0, face=1 if xs[n] > xs[n - 1] else -1)
    for i in range(3):
        k = back((lt - i * d / 3.2) / .25)
        if k > 0: push(cr, 360 + i * 180, 330, k, (i - 1) * .1); circle(cr, 0, 0, 70, YEL if i < n else C("3A506B")); text(cr, str(i + 1), 0, 30, 90, INK, anchor="c", face="Lora"); cr.restore()
    pill(cr, 540, 520, "HARYANA", 54, WHITE, INK, back((lt - .2) / .25), .03)

def g_seesaw(cr, lt, d, t):
    bg(cr, C("8ECAE6"), C("219EBC"))
    ang = math.sin(t * 2.4) * .22
    poly(cr, [(540, 1000), (480, 1150), (600, 1150)], C("023047"))
    push(cr, 540, 1000, 1, ang); rrect(cr, -440, -16, 880, 32, 16, C("FB8500"))
    for i in range(3): rrect(cr, -420 + i * 70, -110, 54, 94, 12, PA); rrect(cr, 236 + i * 70, -110, 54, 94, 12, PB)
    cr.restore()
    rrect(cr, 430, 420, 220, 200, 20, GOLD); rrect(cr, 440, 380, 200, 60, 16, C("D4A017")); rrect(cr, 450, 620, 30, 120, 8, C("B8860B")); rrect(cr, 600, 620, 30, 120, 8, C("B8860B"))
    text(cr, "POWER", 540, 540, 52, INK, anchor="c", face="Lora")
    side = -1 if ang > 0 else 1
    neta(cr, 540 + side * 300, 900, 260, t, face=-side, mouth="o")

def g_paper(cr, lt, d, t):
    bg(cr, C("F1FAEE"), C("A8DADC"))
    push(cr, 540, 700, 1 + .02 * math.sin(t * 2), -.04)
    rrect(cr, -420, -520, 840, 1040, 10, C("FEFAE0")); rrect(cr, -420, -520, 840, 130, 10, INK)
    text(cr, "THE DAILY", 0, -440, 64, WHITE, anchor="c", face="Lora")
    k = back((lt - .2) / .3)
    if k > 0:
        push(cr, 0, -260, k); text(cr, "AAYA RAM,", 0, 0, 100, RED, anchor="c", face="Lora"); text(cr, "GAYA RAM!", 0, 110, 100, RED, anchor="c", face="Lora"); cr.restore()
    for j in range(5): rrect(cr, -360, 0 + j * 46, 330 - (j % 2) * 60, 18, 9, C("CED4DA"))
    rrect(cr, 30, -10, 330, 260, 8, C("E9ECEF"))
    x, f = hop_x(t, 90, 300, 1.2); neta(cr, x, 230, 200, t, walk=1, face=f)
    cr.restore()

def g_law(cr, lt, d, t):
    bg(cr, C("3D405B"), C("1B1B3A")); rays(cr, 540, 600, t * .5, GOLD, .08)
    push(cr, 540, 560, back((lt - .05) / .3)); rrect(cr, -300, -220, 600, 440, 24, C("6D2E46")); rrect(cr, -280, -200, 560, 400, 18, C("8E3B5E"))
    text(cr, "TENTH", 0, -40, 92, GOLD, anchor="c", face="Lora"); text(cr, "SCHEDULE", 0, 70, 80, GOLD, anchor="c", face="Lora"); cr.restore()
    pill(cr, 540, 230, "1985", 90, GOLD, INK, back((lt - .1) / .25), -.05)
    k = ease((lt - d * .45) / .25); sw = math.sin(min(1, k) * math.pi) * .6
    push(cr, 860, 300, 1, -.6 + sw); rrect(cr, -30, 0, 60, 260, 20, C("7F5539")); rrect(cr, -110, -60, 220, 120, 30, C("9C6644")); cr.restore()
    if lt > d * .55:
        neta(cr, 540, 1110, 300, t, mouth="o")
        pill(cr, 540, 860, "SEAT LOST", 56, RED, WHITE, back((lt - d * .55) / .25), .04)

def g_loophole(cr, lt, d, t):
    bg(cr, C("2EC4B6"), C("011627"))
    office(cr, 880, 1150, PB, "B")
    p = (t * .22) % 1
    for i in range(6):
        x = 120 + p * 600 + (i % 3) * 70 - (i // 3) * 40; y = 1160 - (i // 3) * 40
        neta(cr, x, y, 230, t + i * .3, walk=1, face=1)
    k = back((lt - .2) / .25)
    if k > 0:
        push(cr, 300, 420, k, -.05); rrect(cr, -210, -90, 420, 180, 30, YEL); text(cr, "2/3", 0, 30, 110, INK, anchor="c", face="Lora"); cr.restore()
    pill(cr, 760, 520, "= MERGER", 64, WHITE, INK, back((lt - .6) / .25), .05)

BEATS = [
    dict(say="In 1967, an Indian MLA switched parties twice in a few hours.", cap="In 1967, an Indian MLA switched parties *twice in a few hours*.", scene=g_hook),
    dict(say="Gaya Lal, from Haryana. Three switches in about two weeks.", cap="*Gaya Lal*, from Haryana. *Three switches* in about two weeks.", scene=g_count),
    dict(say="Back then, one MLA hopping sides could decide who ran the state.", cap="Back then, one MLA hopping sides could decide *who ran the state*.", scene=g_seesaw),
    dict(say="The joke stuck forever. Aaya Ram, Gaya Ram.", cap="The joke stuck forever. *Aaya Ram, Gaya Ram.*", scene=g_paper),
    dict(say="In 1985, India finally passed the anti-defection law. Switch sides, and you can lose your seat.", cap="In 1985, India passed the *anti-defection law*. Switch sides, and you can *lose your seat*.", scene=g_law),
    dict(say="But if two-thirds of a party's legislators move together, it counts as a merger. Send this to someone who follows politics.", cap="But if *two-thirds* move together, it counts as a *merger*. Send this to someone who *follows politics*.", scene=g_loophole, hold=0.3),
]

if __name__ == "__main__":
    f = Film("28_aaya_ram", BEATS, voice=("af_heart", 1.08, "en-us"))
    if "--stills" in sys.argv:
        from PIL import Image
        ts = [0.0, 1.5]
        for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
        ims = []
        for n, tt in enumerate(ts):
            p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
        s = Image.new("RGB", (270 * len(ims), 480)); [s.paste(im, (n * 270, 0)) for n, im in enumerate(ims)]; s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])
    else: f.render()
