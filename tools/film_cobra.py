"""Film 27: the cobra effect (Delhi bounty legend), with the honest twist that it may never have happened; Hanoi rats as the documented case."""
import sys, math
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, pill

GREEN_S = C("2D6A4F"); GREEN_L = C("52B788"); HOOD = C("40916C"); BELLY_S = C("D8F3DC")

def cobra(cr, x, y, s, t, face=1, rise=1.0, a=1.0):
    """(x, y) = base of the coil on the ground; s = height of the raised body."""
    u = s / 100
    push(cr, x, y); cr.scale(face, 1)
    for i in range(3): ell(cr, (i - 1) * 18 * u, -6 * u - i * 4 * u, (46 - i * 8) * u, 12 * u, GREEN_S if i % 2 else HOOD, a)
    sway = math.sin(t * 2.2) * 8 * u
    top = (8 * u + sway, -100 * u * rise)
    cr.new_path(); cr.move_to(-10 * u, -10 * u); cr.curve_to(-30 * u, -40 * u * rise, 30 * u + sway, -60 * u * rise, top[0], top[1] + 20 * u)
    cr.set_line_width(20 * u); cr.set_line_cap(cairo.LINE_CAP_ROUND); src(cr, GREEN_S, a); cr.stroke()
    hx, hy = top
    ell(cr, hx, hy + 8 * u, 30 * u, 36 * u, HOOD, a); ell(cr, hx, hy + 12 * u, 16 * u, 26 * u, BELLY_S, a * .8)
    for sx in (-1, 1): ring(cr, hx + sx * 15 * u, hy + 2 * u, 5 * u, 2.5 * u, C("1B4332"), a)
    ell(cr, hx, hy - 16 * u, 14 * u, 11 * u, GREEN_S, a)
    for sx in (-1, 1): circle(cr, hx + sx * 6 * u, hy - 19 * u, 3 * u, YEL, a); circle(cr, hx + sx * 6 * u, hy - 19 * u, 1.3 * u, INK, a)
    if (t % 1.3) < .35:
        polyline(cr, [(hx, hy - 8 * u), (hx, hy + 2 * u), (hx - 4 * u, hy + 8 * u)], 2 * u, RED, a); polyline(cr, [(hx, hy + 2 * u), (hx + 4 * u, hy + 8 * u)], 2 * u, RED, a)
    cr.restore()

def coin(cr, x, y, r, a=1.0, spin=0.0):
    sx = max(.15, abs(math.cos(spin)))
    ell(cr, x, y, r * sx, r, C("B8862B"), a); ell(cr, x, y, r * .8 * sx, r * .8, GOLD, a)
    if sx > .5: text(cr, "1", x, y + r * .35, r * 1.0, C("8A5A00"), a, anchor="c", face="Lora")

def basket(cr, x, y, w, t, lid=0.0, snake=True):
    if snake and lid > .1: cobra(cr, x, y - w * .25, w * .9 * min(1, lid), t, rise=min(1, lid))
    rrect(cr, x - w / 2, y - w * .45, w, w * .5, w * .12, C("BC8A5F"))
    for i in range(4): line(cr, x - w / 2 + 6, y - w * .38 + i * w * .11, x + w / 2 - 6, y - w * .38 + i * w * .11, 3, C("8B5E34"), .7)
    if lid < .5: ell(cr, x, y - w * .45 - lid * 60, w * .52, w * .12, C("A47148"))

def city(cr, t, dusk=0.0):
    bg(cr, lerpc(C("FFB703"), C("3D2C8D"), dusk), lerpc(C("FB8500"), C("1B1B3A"), dusk))
    glow(cr, 820, 300, 180, C("FFF3C4"), .35 * (1 - dusk)); circle(cr, 820, 300, 70, C("FFE8A3"), 1 - dusk * .7)
    for i, (x, w, h) in enumerate([(40, 180, 380), (230, 140, 300), (380, 220, 450), (620, 160, 340), (790, 240, 420)]):
        col = lerpc(C("BC6C25"), C("2A2140"), dusk); rrect(cr, x, 1050 - h, w, h, 8, col)
        if i == 2:
            cr.new_path(); cr.arc(x + w / 2, 1050 - h, w * .38, math.pi, 2 * math.pi); src(cr, col); cr.fill(); rrect(cr, x + w / 2 - 6, 1050 - h - w * .52, 12, 40, 4, col)
        for j in range(3):
            for k in range(2): rrect(cr, x + 24 + k * (w - 72), 1050 - h + 40 + j * 90, 24, 40, 12, lerpc(C("FFE8A3"), C("FFD166"), dusk), .5 + .4 * dusk)
    rrect(cr, 0, 1050, W, 870, 0, lerpc(C("D4A373"), C("3B2F2F"), dusk))

def k_hook(cr, lt, d, t):
    city(cr, t, .2)
    for i in range(5):
        cobra(cr, 140 + i * 200, 1150 - (i % 2) * 60, 280 + (i % 3) * 40, t + i * .7, face=1 if i % 2 else -1)
    for i in range(8):
        ph = (t * .6 + i / 8) % 1; coin(cr, 100 + (i * 131) % 880, 200 + ph * 900, 34, 1 - ph * .6, t * 5 + i)
    pill(cr, 540, 330, "MORE COBRAS?!", 84, RED, WHITE, back((lt + .25) / .25) * (1 + .05 * math.sin(t * 7)), -.04)

def k_bounty(cr, lt, d, t):
    city(cr, t, 0)
    rrect(cr, 160, 1050, 760, 40, 10, C("6F4518")); rrect(cr, 200, 1090, 26, 180, 6, C("5A3A14")); rrect(cr, 850, 1090, 26, 180, 6, C("5A3A14"))
    o = person(cr, 640, 1060, 420, shirt=C("B91C1C"), pants=C("F5F0E1"), pose=dict(helmet=C("F5F0E1"), ra=110, ra2=-30, look=-1, mouth="smile", blink=(t % 3) < .12))
    for i in range(int(min(6, lt * 3))): coin(cr, 360 + (i % 3) * 70, 1010 - (i // 3) * 22, 30, spin=.3)
    for i in range(int(min(5, lt * 2.5))):
        y = 1030 - i * 14; polyline(cr, [(200 + i * 10, y), (300, y - 10), (400, y), (480 - i * 10, y - 6)], 14, GREEN_S)
    pill(cr, 300, 380, "1 COBRA = CASH", 62, GOLD, INK, back((lt - .2) / .25), -.05)

def k_farm(cr, lt, d, t):
    bg(cr, C("606C38"), C("283618"))
    rrect(cr, 0, 1150, W, 770, 0, C("4F3B24"))
    for i in range(6):
        x = 180 + (i % 3) * 360; y = 820 + (i // 3) * 300
        basket(cr, x, y, 230, t + i, lid=.5 + .5 * abs(math.sin(t * 1.5 + i)))
    pill(cr, 540, 330, "COBRA FARM", 84, YEL, INK, back((lt - .1) / .25), .04)
    for i in range(3):
        ph = (t * .5 + i / 3) % 1; coin(cr, 900, 520 - ph * 200, 30, 1 - ph, t * 6)

def k_release(cr, lt, d, t):
    city(cr, t, .85)
    k = back((lt - .1) / .25)
    if k > 0:
        push(cr, 520, 400, k, -.12); rr_path(cr, -300, -80, 600, 160, 20); cr.set_line_width(14); src(cr, RED); cr.stroke()
        text(cr, "CANCELLED", 0, 32, 100, RED, anchor="c", face="Lora"); cr.restore()
    p = ease((lt - d * .3) / (d * .6))
    for i in range(7):
        bx = 160 + (i % 4) * 250; by = 1000 + (i // 4) * 150
        basket(cr, bx, by + 100, 160, t + i, lid=1.0, snake=False)
        cobra(cr, bx + p * (220 + i * 30) * (1 if i % 2 else -1), by + 40, 200, t + i, face=1 if i % 2 else -1, rise=.8)

def k_twist(cr, lt, d, t):
    bg(cr, C("14213D"), C("000814")); rays(cr, 540, 640, t, C("FCA311"), .08)
    k1 = back((lt - .05) / .25)
    if k1 > 0:
        push(cr, 540, 520, k1, .08); cobra(cr, 0, 260, 380, t, a=.35); rr_path(cr, -260, -80, 520, 160, 20); src(cr, WHITE); cr.fill(); text(cr, "MYTH?", 0, 34, 110, INK, anchor="c", face="Lora"); cr.restore()
    k2 = ease((lt - d * .5) / .3)
    if k2 > 0:
        pill(cr, 540, 960, "HANOI, 1902: REAL", 60, YEL, INK, back((lt - d * .5) / .25), -.03)
        for i in range(4):
            x = -100 + ((t * 220 + i * 300) % 1300); rat(cr, x, 1140 + (i % 2) * 40, 150, t + i, tail=i % 2 == 0)

def k_end(cr, lt, d, t):
    bg(cr, C("FF006E"), C("3A0CA3")); rays(cr, 540, 640, t, WHITE, .1)
    line(cr, 160, 1100, 920, 1100, 8, WHITE, .8); line(cr, 160, 1100, 160, 420, 8, WHITE, .8)
    g = ease(lt / (d * .5))
    for i in range(5):
        h = (100 + i * 110) * g; rrect(cr, 200 + i * 140, 1100 - h, 100, h, 16, GREEN_L)
    pts = [(200 + i * 38, 1060 - (i ** 1.6) * 5.2 * g) for i in range(19)]
    polyline(cr, pts, 26, GREEN_S); cobra(cr, pts[-1][0] + 20, pts[-1][1] + 30, 220, t)
    pill(cr, 540, 300, "TARGET HIT!", 72, WHITE, INK, back((lt - .2) / .25), -.05)

BEATS = [
    dict(say="The British paid people in Delhi to kill cobras. The city ended up with more cobras.", cap="The British paid Delhi to *kill cobras*. The city ended up with *more cobras*.", scene=k_hook),
    dict(say="The story goes: every dead cobra earned a cash reward.", cap="The story goes: every *dead cobra* earned a *cash reward*.", scene=k_bounty),
    dict(say="So people started breeding cobras, just to kill them for money.", cap="So people started *breeding cobras*, just to kill them for money.", scene=k_farm),
    dict(say="Officials found out and cancelled the reward. The breeders set their worthless snakes free.", cap="Officials *cancelled the reward*. The breeders set their worthless snakes *free*.", scene=k_release),
    dict(say="Plot twist: historians can't prove it ever happened. But Hanoi in 1902 did the same with rats, and it really backfired.", cap="Plot twist: historians *can't prove it happened*. But *Hanoi, 1902* did it with rats, and it *really* backfired.", scene=k_twist),
    dict(say="Reward a number, and people will deliver the number. Send this to someone who sets targets.", cap="Reward a number, and people deliver *the number*. Send this to someone who *sets targets*.", scene=k_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("27_cobra", BEATS, voice=("af_heart", 1.08, "en-us"))
    if "--stills" in sys.argv:
        from PIL import Image
        ts = [0.0, 1.5]
        for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
        ims = []
        for n, tt in enumerate(ts):
            p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
        s = Image.new("RGB", (270 * len(ims), 480)); [s.paste(im, (n * 270, 0)) for n, im in enumerate(ims)]; s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])
    else: f.render()
