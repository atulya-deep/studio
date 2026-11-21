"""Film 23: temptation bundling (Milkman, Minson & Volpp, Management Science 2014). Motion style."""
import sys, math
from kit2 import *
from scenes import walk_pose
from motion import Film, W, H
from film_voice import bg, rays, face, pill
from film_peak import sheet

TEAL2 = C("06D6A0"); BLUE = C("3A86FF")

def headphones(cr, x, y, r, col=C("FF006E")):
    cr.new_path(); cr.arc(x, y - r * .05, r * 1.08, math.pi * 1.08, math.pi * 1.92); cr.set_line_width(r * .14); cr.set_line_cap(cairo.LINE_CAP_ROUND); src(cr, col); cr.stroke()
    for sx in (-1, 1): rrect(cr, x + sx * r * 1.02 - r * .2, y - r * .25, r * .4, r * .6, r * .16, col)

def notes(cr, x, y, t, col=YEL, n=4):
    for i in range(n):
        ph = (t * .7 + i / n) % 1; nx = x + math.sin(ph * 6 + i) * 60 + (i - n / 2) * 50; ny = y - ph * 300
        circle(cr, nx, ny, 16, col, 1 - ph); line(cr, nx + 14, ny, nx + 14, ny - 50, 6, col, 1 - ph); line(cr, nx + 14, ny - 50, nx + 34, ny - 40, 6, col, 1 - ph)

def book(cr, x, y, s, col, title="", rot=0.0, k=1.0):
    if k <= 0: return
    push(cr, x, y, k * s / 100, rot)
    rrect(cr, -70, -95, 140, 190, 10, col); rrect(cr, -70, -95, 20, 190, 6, INK, .25)
    rrect(cr, -40, -60, 90, 14, 4, WHITE, .8); rrect(cr, -40, -36, 60, 10, 4, WHITE, .6)
    if title: text(cr, title, 5, 60, 30, WHITE, anchor="c")
    cr.restore()

def treadmill(cr, x, y, w, t):
    """origin at belt centre"""
    rrect(cr, x - w / 2, y, w, 40, 20, INK);
    for i in range(8):
        bx = x - w / 2 + 20 + ((i * w / 8 - t * 260) % (w - 40)); line(cr, bx, y + 10, bx, y + 30, 5, WHITE, .25)
    line(cr, x + w * .42, y, x + w * .36, y - 260, 16, C("6C757D")); rrect(cr, x + w * .26, y - 300, 140, 60, 16, C("6C757D"))
    rrect(cr, x + w * .29, y - 288, 90, 34, 8, C("4CC9F0"))

def runner(cr, x, y, s, t, shirt=C("3A86FF"), mood="smile", phones=True):
    o = person(cr, x, y, s, shirt=shirt, pants=INK, pose=dict(walk_pose(t, 13), mouth=mood, look=.6, la2=60, ra2=60))
    if phones:
        hx, hy = o["head"]; u = o["u"]; headphones(cr, hx, hy, 13 * u)
    return o

def locker(cr, x, y, w, h, k_open=0.0, num="07"):
    rrect(cr, x, y, w, h, 14, C("ADB5BD"))
    for i in range(4): rrect(cr, x + w * .2, y + 40 + i * 22, w * .6, 8, 4, C("6C757D"))
    text(cr, num, x + w / 2, y + h * .42, 54, INK, anchor="c")
    # door swings open (drawn as a thinning panel)
    if k_open > 0:
        rrect(cr, x + 10, y + 10, w - 20, h - 20, 10, INK)
        dw = w * (1 - k_open * .8); rrect(cr, x + w - dw - (w * .9) * k_open, y, dw, h, 14, C("CED4DA"))
    circle(cr, x + w * .82, y + h * .55, 12, C("495057"))

def couch(cr, x, y, w):
    rrect(cr, x - w / 2, y - 120, w, 120, 30, C("8338EC")); rrect(cr, x - w / 2 - 30, y - 160, 70, 180, 30, C("6A2CC4")); rrect(cr, x + w / 2 - 40, y - 160, 70, 180, 30, C("6A2CC4"))
    rrect(cr, x - w / 2 + 20, y - 230, w - 40, 130, 30, C("9D5CF2"))

# ---------- scenes ----------
def b_hook(cr, lt, d, t):
    bg(cr, C("FF006E"), C("3A0CA3")); rays(cr, 540, 640, t, WHITE, .1)
    couch(cr, 540, 1060, 640)
    o = person(cr, 540, 1000, 380, shirt=C("FFBE0B"), pants=INK, pose=dict(sit=True, la=25, la2=40, ra=25, ra2=40, mouth="frown", blink=(t % 2.5) < .15))
    # chained book above
    k = 1 + .05 * math.sin(t * 8)
    for sx in (-1, 1):
        for i in range(6): ring(cr, 540 + sx * (40 + i * 52), 440 - i * 30, 24, 9, C("CED4DA"))
    book(cr, 540, 430, 130, C("FB5607"), "", -.08 + math.sin(t * 5) * .05, k)
    rrect(cr, 505, 450, 70, 56, 12, C("495057")); ring(cr, 540, 450, 24, 9, C("495057"), 1, math.pi, 2 * math.pi)
    pill(cr, 540, 250, "HOSTAGE", 74, YEL, INK, k, .05)

def b_locker(cr, lt, d, t):
    bg(cr, C("0B132B"), C("1C2541"))
    for i in range(3): locker(cr, 120 + i * 290, 330, 250, 620, ease((lt - d * .25) / .4) if i == 1 else 0, ["06", "07", "08"][i])
    k = ease((lt - d * .3) / .4)
    if k > 0:
        # an MP3 player with audiobooks lights up inside locker 07
        push(cr, 535, 600, back((lt - d * .35) / .3))
        rrect(cr, -60, -90, 120, 180, 20, WHITE); circle(cr, 0, 30, 36, C("CED4DA")); rrect(cr, -40, -70, 80, 60, 8, C("4CC9F0"))
        cr.restore(); glow(cr, 535, 600, 200, YEL, .35 * k)
    book(cr, 260, 1130, 70, C("FB5607"), "", -.2, back((lt - .1) / .3))
    book(cr, 380, 1140, 70, C("06D6A0"), "", .1, back((lt - .25) / .3))
    book(cr, 500, 1130, 70, C("8338EC"), "", -.05, back((lt - .4) / .3))
    pill(cr, 800, 1120, "GYM ONLY", 52, YEL, INK, back((lt - d * .55) / .25), .06)
    pill(cr, 540, 230, "AUDIOBOOKS", 60, WHITE, INK, back((lt - .1) / .25), -.04)

def b_rule(cr, lt, d, t):
    bg(cr, C("06D6A0"), C("118AB2")); rays(cr, 540, 700, t, WHITE, .1)
    treadmill(cr, 520, 1040, 640, t)
    runner(cr, 480, 1040, 520, t, mood="smile")
    notes(cr, 360, 520, t, YEL)
    pill(cr, 300, 260, "PRESS PLAY", 58, YEL, INK, back((lt - .1) / .25), -.05)
    k = back((lt - d * .5) / .25)
    if k > 0:
        push(cr, 820, 380, k); circle(cr, 0, 0, 110, INK); text(cr, "ONLY", 0, -6, 44, WHITE, anchor="c"); text(cr, "HERE", 0, 44, 44, YEL, anchor="c"); cr.restore()

def b_stat(cr, lt, d, t):
    bg(cr, C("FFBE0B"), C("FB5607")); rays(cr, 540, 600, t, WHITE, .12)
    base, top = 1000, 380
    kc = ease((lt - .1) / .5); kt = ease((lt - .25) / (d * .5))
    hC = 300 * kc; hT = 453 * kt  # 151% of control
    rrect(cr, 210, base - hC, 240, hC, 24, WHITE, .9); rrect(cr, 630, base - hT, 240, hT, 24, INK)
    text(cr, "NORMAL", 330, base + 70, 46, WHITE, anchor="c"); text(cr, "BUNDLED", 750, base + 70, 46, WHITE, anchor="c")
    v = int(51 * kt)
    push(cr, 750, base - hT - 90, back((lt - .3) / .3) * (1 + .04 * math.sin(t * 8))); rrect(cr, -150, -62, 300, 124, 62, YEL); text(cr, f"+{v}%", 0, 30, 80, INK, anchor="c"); cr.restore()
    for i in range(4):
        ph = (t * .6 + i / 4) % 1; circle(cr, 600 + (i * 97) % 300, 1150 - ph * 800, 9, WHITE, .6 * (1 - ph))
    pill(cr, 330, 470, "GYM VISITS", 46, INK, WHITE, back((lt - .2) / .25), -.06)

def b_name(cr, lt, d, t):
    bg(cr, C("10002B"), C("3C096C"))
    # WANT + SHOULD = bundle
    k1 = back((lt - .05) / .3); k2 = back((lt - d * .3) / .3); k3 = back((lt - d * .6) / .3)
    if k1 > 0:
        push(cr, 260, 560, k1); circle(cr, 0, 0, 170, C("FF006E")); headphones(cr, 0, 10, 80, WHITE); cr.restore()
        pill(cr, 260, 800, "WANT", 56, C("FF006E"), WHITE, k1)
    text(cr, "+", 540, 610, 140, WHITE, .9 * min(1, k2), anchor="c")
    if k2 > 0:
        push(cr, 820, 560, k2); circle(cr, 0, 0, 170, TEAL2); rrect(cr, -110, -18, 220, 36, 14, INK); rrect(cr, -120, -55, 34, 110, 12, INK); rrect(cr, 86, -55, 34, 110, 12, INK); cr.restore()
        pill(cr, 820, 800, "SHOULD", 56, TEAL2, INK, k2)
    if k3 > 0:
        push(cr, 540, 1030, k3 * (1 + .04 * math.sin(t * 8))); rrect(cr, -380, -80, 760, 160, 80, YEL); text(cr, "TEMPTATION BUNDLE", 0, 22, 56, INK, anchor="c"); cr.restore()
    glow(cr, 540, 600, 300, C("9D4EDD"), .25)

def b_end(cr, lt, d, t):
    bg(cr, C("3A86FF"), C("8338EC")); rays(cr, 540, 660, t, WHITE, .1)
    # person doing dishes with headphones, notes flying
    rrect(cr, 160, 860, 760, 60, 20, C("ADB5BD")); rrect(cr, 380, 860, 320, 50, 12, C("4CC9F0"))
    o = person(cr, 540, 1180, 520, shirt=C("FB5607"), pants=INK, pose=dict(la=60 + math.sin(t * 8) * 12, la2=80, ra=60 - math.sin(t * 8) * 12, ra2=80, mouth="smile", look=.3))
    headphones(cr, *o["head"], 13 * o["u"])
    rrect(cr, 330, 830, 380, 90, 20, C("ADB5BD"))
    for i in range(4):
        ph = (t * .8 + i / 4) % 1; circle(cr, 440 + i * 60, 820 - ph * 120, 14 + i * 3, WHITE, .7 * (1 - ph))
    notes(cr, 820, 560, t, YEL)
    pill(cr, 540, 260, "SHOWS = CHORES", 66, YEL, INK, back((lt - .1) / .25) * (1 + .05 * math.sin(t * 8)), .04)

BEATS = [
    dict(say="Can't make yourself work out? Hold your favourite story hostage.", cap="Can't make yourself work out? *Hold your favourite story hostage.*", scene=b_hook),
    dict(say="Researchers at Wharton locked gripping audiobooks, like The Hunger Games, in gym lockers.", cap="Researchers locked gripping *audiobooks*, like The Hunger Games, in *gym lockers*.", scene=b_locker),
    dict(say="The rule: you can only listen while you exercise.", cap="The rule: you can *only listen* while you exercise.", scene=b_rule),
    dict(say="Those people went to the gym fifty one percent more often, at least at first.", cap="They went to the gym *51% more* often, at least at first.", scene=b_stat, hold=0.2),
    dict(say="It's called temptation bundling. Pair something you want with something you should do.", cap="It's called *temptation bundling*. Pair a *want* with a *should*.", scene=b_name),
    dict(say="Pick one show you only watch while doing chores. Send this to your gym buddy.", cap="Pick one show you *only watch* during chores. Send this to your *gym buddy*.", scene=b_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("23_temptation_bundling", BEATS, voice=("af_heart", 1.08, "en-us"))
    if "--stills" in sys.argv: sheet(f)
    else: f.render()
