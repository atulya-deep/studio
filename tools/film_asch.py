"""Film 32: Asch conformity (1951). Most people went along with an obviously wrong group answer at least once; one ally broke it."""
import sys, math
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, face, pill

SH = [C("E76F51"), C("2A9D8F"), C("E9C46A"), C("8E7DBE"), C("F4A261"), C("457B9D")]

def card(cr, x, y, s, k=1.0, hl=None):
    """reference line + A/B/C; C matches."""
    if k <= 0: return
    push(cr, x, y, k); rrect(cr, -s, -s * .55, s * 2, s * 1.1, 24, WHITE)
    line(cr, -s * .8, s * .3, -s * .8, -s * .3, 14, INK); text(cr, "X", -s * .8, s * .46, 34, MUTED, anchor="c")
    line(cr, -s * .42, s * .3, -s * .42, -s * .3, 4, C("CED4DA"), 1)
    for i, (lab, L) in enumerate([("A", .38), ("B", .82), ("C", .6)]):
        xx = -s * .1 + i * s * .38
        if hl == lab: rrect(cr, xx - 40, -s * .42, 80, s * .92, 16, C("FFE066"))
        line(cr, xx, s * .3, xx, s * .3 - s * L, 14, INK); text(cr, lab, xx, s * .46, 34, INK, anchor="c")
    cr.restore()

def row(cr, t, lt, n=6, y=1180, s=300, says="A", k0=.2, gap=.35, ally=None):
    xs = [100 + i * 135 for i in range(n)]
    for i, x in enumerate(xs):
        person(cr, x, y, s, shirt=SH[i % 6], pose=dict(face=1, mouth="smile", blink=(t + i) % 3.3 < .12))
        lab = "C" if i == ally else says
        bubble(cr, x, y - s - 60, 90, 80, lab, 52, back((lt - k0 - i * gap) / .2), GREEN if i == ally else WHITE, WHITE if i == ally else INK, tail=0)
    return xs

def hero(cr, x, y, s, t, mood="flat", sweat=0):
    o = person(cr, x, y, s, shirt=C("1D3557"), pose=dict(face=-1, mouth=mood, look=-.6, blink=t % 2.7 < .12))
    if sweat:
        hx, hy = o["head"]
        for i in range(2):
            ph = (t * 1.4 + i * .5) % 1; ell(cr, hx + 30 + i * 14, hy - 20 + ph * 60, 8, 12, C("8ECAE6"), 1 - ph)
    return o

def s_hook(cr, lt, d, t):
    bg(cr, C("14213D"), C("3A0CA3")); rays(cr, 540, 700, t, YEL, .1)
    card(cr, 540, 450, 300, 1.0, hl="A" if (t % 1.4) < .7 else None)
    for i in range(5):
        x = 90 + i * 140; person(cr, x, 1180, 260, shirt=SH[i], pose=dict(face=1, mouth="smile", ra=150, ra2=-20))
        bubble(cr, x, 860, 80, 72, "A", 46, 1.0)
    hero(cr, 920, 1180, 300, t, "frown", sweat=1)
    pill(cr, 920, 820, "C...?", 52, YEL, INK, 1 + .05 * math.sin(t * 8), .05)

def s_setup(cr, lt, d, t):
    bg(cr, C("FFF8E7"), C("FFE8B6"))
    pill(cr, 540, 220, "1951 · SOLOMON ASCH", 60, INK, WHITE, back((lt - .05) / .25), -.03)
    card(cr, 540, 620, 330, back((lt - .3) / .3), hl="C" if lt > d * .6 else None)
    k = back((lt - d * .6) / .25)
    if k > 0: check(cr, 760, 860, 90, GREEN, k)
    text(cr, "WHICH LINE MATCHES X?", 540, 1060, 50, INK, anchor="c", face="Lora")

def s_actors(cr, lt, d, t):
    bg(cr, C("E0FBFC"), C("98C1D9"))
    xs = row(cr, t, lt, n=6, y=1180, s=280, says="A", k0=.15, gap=d * .1)
    hero(cr, 960, 1180, 300, t, "o", sweat=lt > d * .5)
    for i, x in enumerate(xs):
        k = back((lt - .1 - i * .08) / .2)
        if k > 0: pill(cr, x, 760 - (i % 2) * 50, "ACTOR", 30, RED, WHITE, k, (i % 2 - .5) * .2)
    pill(cr, 540, 300, "ALL WRONG. ON PURPOSE.", 54, INK, WHITE, back((lt - d * .55) / .25), .03)

def s_result(cr, lt, d, t):
    bg(cr, C("FF006E"), C("8338EC")); rays(cr, 540, 600, t, WHITE, .08)
    n = min(3, int(4 * ease((lt - .3) / (d * .5))))
    for i in range(4):
        x = 180 + i * 240; lit = i < n
        o = person(cr, x, 1100, 360, shirt=YEL if lit else C("C77DFF"), pose=dict(face=1, mouth="frown" if lit else "smile"))
        bubble(cr, x, 640, 110, 90, "A" if lit else "?", 56, back((lt - .3 - i * .25) / .2), WHITE if lit else C("E0AAFF"), INK)
    k = back((lt - d * .55) / .25)
    if k > 0: push(cr, 540, 330, k * (1 + .03 * math.sin(t * 8))); rrect(cr, -330, -85, 660, 170, 40, WHITE); text(cr, "3 OUT OF 4", 0, 34, 96, INK, anchor="c", face="Lora"); cr.restore()
    text(cr, "went along at least once", 540, 1220, 44, WHITE, anchor="c")

def s_ally(cr, lt, d, t):
    bg(cr, C("D8F3DC"), C("95D5B2")); rays(cr, 540, 700, t, WHITE, .12)
    row(cr, t, lt, n=6, y=1180, s=280, says="A", k0=-1, gap=0, ally=5)
    calm = lt > d * .45
    hero(cr, 960, 1180, 300, t, "smile" if calm else "o")
    bubble(cr, 960, 800, 100, 84, "C", 56, back((lt - d * .45) / .2), GREEN, WHITE)
    pill(cr, 540, 300, "JUST ONE ALLY", 64, INK, WHITE, back((lt - .1) / .25), -.03)
    k = back((lt - d * .6) / .25)
    if k > 0: pill(cr, 540, 450, "CONFORMITY CRASHED", 54, RED, WHITE, k, .04)

def s_end(cr, lt, d, t):
    bg(cr, C("0B132B"), C("1C2541")); rays(cr, 540, 700, t * .6, YEL, .12)
    for i in range(5):
        x = 120 + i * 120; person(cr, x, 1180, 240, shirt=C("3A506B"), pose=dict(face=1, mouth="flat"))
    o = person(cr, 860, 1180, 340, shirt=YEL, pose=dict(face=-1, mouth="smile", ra=165, ra2=0))
    rx, ry = o["rh"]; glow(cr, rx, ry - 40, 120, YEL, .4)
    pill(cr, 540, 360, "BE THE ONE", 90, YEL, INK, back((lt - .1) / .25) * (1 + .03 * math.sin(t * 6)), -.04)

BEATS = [
    dict(say="Would you give an answer you know is wrong, just because everyone else did?", cap="Would you say an answer you *know is wrong*, just because *everyone else* did?", scene=s_hook),
    dict(say="1951. Psychologist Solomon Asch asks a simple question. Which line matches?", cap="*1951.* Solomon Asch asks a simple question: *which line matches?*", scene=s_setup),
    dict(say="But everyone else in the room is an actor. And one by one, they all pick the wrong line.", cap="But everyone else is an *actor*. One by one, they all pick the *wrong line*.", scene=s_actors),
    dict(say="Three out of four real people went along with them at least once.", cap="*3 out of 4* real people went along *at least once*.", scene=s_result),
    dict(say="But add just one person who tells the truth, and conformity crashes.", cap="Add *just one* person who tells the truth, and conformity *crashes*.", scene=s_ally),
    dict(say="Be that one person. Send this to the friend who always says it out loud.", cap="Be *that one person*. Send this to the friend who *says it out loud*.", scene=s_end, hold=0.4),
]

if __name__ == "__main__":
    f = Film("32_asch_lines", BEATS, voice=("af_heart", 1.08, "en-us"))
    if "--stills" in sys.argv:
        from PIL import Image
        ts = [0.0, 1.5]
        for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
        ims = []
        for n, tt in enumerate(ts):
            p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
        s = Image.new("RGB", (270 * len(ims), 480)); [s.paste(im, (n * 270, 0)) for n, im in enumerate(ims)]; s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])
    else: f.render()
