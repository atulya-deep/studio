"""Film 34: the fresh start effect (Dai, Milkman & Riis 2014, Management Science 60(10)).
Google 'diet' searches vs baseline: +14.4% start of a week, +82.1% start of a new year (Study 1, Table 1).
Gym visits (Penn students) and stickK commitment contracts also rise after temporal landmarks (new week/month/year, birthdays, holidays)."""
import sys, math
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, pill
from film_bundle import treadmill, runner, couch
from film_peak import sheet

BLUE = C("3A86FF"); MINT = C("06D6A0")

def calendar(cr, x, y, w, top, big, col=RED, k=1.0, rot=0.0, circled=0.0, t=0.0):
    if k <= 0: return
    push(cr, x, y, k, rot); h = w * 1.05
    rrect(cr, -w / 2 + 10, -h / 2 + 14, w, h, 28, INK, .25)
    rrect(cr, -w / 2, -h / 2, w, h, 28, WHITE); rrect(cr, -w / 2, -h / 2, w, h * .28, 28, col); rrect(cr, -w / 2, -h / 2 + h * .18, w, h * .1, 0, col)
    for sx in (-1, 1): rrect(cr, sx * w * .25 - 10, -h / 2 - 26, 20, 52, 10, C("495057"))
    text(cr, top, 0, -h / 2 + h * .19, w * .13, WHITE, anchor="c")
    text(cr, big, 0, h * .3, w * .42, INK, anchor="c")
    if circled > 0:
        cr.new_path(); cr.arc(0, h * .14, w * .4, -1.4, -1.4 + 6.4 * min(1, circled)); cr.set_line_width(w * .04); src(cr, RED); cr.stroke()
    cr.restore()

def donut(cr, x, y, r):
    circle(cr, x, y, r, C("E9C46A")); circle(cr, x, y, r * .8, PINK); circle(cr, x, y, r * .3, C("FFF3D6"))
    for i in range(7): a = i * .9; line(cr, x + math.cos(a) * r * .55, y + math.sin(a) * r * .55, x + math.cos(a) * r * .55 + 10, y + math.sin(a) * r * .55 + 6, 6, [YEL, MINT, BLUE][i % 3])

def searchbar(cr, x, y, w, txt, cursor=True):
    rrect(cr, x - w / 2, y - 60, w, 120, 60, WHITE); ring(cr, x - w / 2 + 70, y - 8, 24, 8, MUTED); line(cr, x - w / 2 + 86, y + 10, x - w / 2 + 104, y + 28, 8, MUTED)
    text(cr, txt, x - w / 2 + 130, y + 22, 60, INK)
    if cursor:
        cr.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); cr.set_font_size(60); tw = cr.text_extents(txt).x_advance
        rrect(cr, x - w / 2 + 136 + tw, y - 30, 6, 60, 3, BLUE)

def chart(cr, x0, y0, w, h, prog, spikes, col=BLUE):
    """line chart of daily searches with spikes at fractions in `spikes` (pos, height)"""
    n = 90; pts = []
    for i in range(n):
        f = i / (n - 1)
        if f > prog: break
        v = .18 + .04 * math.sin(i * 1.7) + .03 * math.sin(i * .6)
        for p, hgt in spikes: v += hgt * math.exp(-((f - p) * 60) ** 2)
        pts.append((x0 + f * w, y0 - v * h))
    line(cr, x0, y0, x0 + w, y0, 5, INK, .4)
    if len(pts) > 1: polyline(cr, pts, 9, col)

def f_hook(cr, lt, d, t):
    bg(cr, C("FF006E"), C("8338EC")); rays(cr, 540, 640, t, WHITE, .1)
    sh = math.sin(t * 40) * 6 * max(0, 1 - lt / .6)
    calendar(cr, 540 + sh, 640, 520, "MONDAY", "1", RED, 1.0, -.05 + .02 * math.sin(t * 3), circled=min(1, (lt + .3) / .6))
    donut(cr, 230, 1040, 90); cross(cr, 230, 1040, 150, RED, back((lt - .2) / .2))
    o = person(cr, 820, 1220, 300, shirt=MINT, pants=INK, pose=dict(mouth="smile", ra=160, ra2=-10, la=30))
    pill(cr, 540, 270, "“FROM MONDAY!”", 66, YEL, INK, 1 + .05 * math.sin(t * 8), .04)

def f_search(cr, lt, d, t):
    bg(cr, C("E0FBFC"), C("98C1D9"))
    pill(cr, 540, 260, "WHARTON · 2014", 58, INK, WHITE, back((lt - .05) / .25), -.03)
    n = int(min(4, max(0, (lt - .3) / .18))); searchbar(cr, 540, 520, 820, "diet"[:n], cursor=(t % .8) < .5)
    for i in range(4):
        k = back((lt - .6 - i * .1) / .25)
        if k > 0: rrect(cr, 180, 630 + i * 70, 720 * (.9 - (i % 3) * .2), 40, 20, MUTED, .5 * k)
    person(cr, 540, 1240, 250, shirt=BLUE, pants=INK, pose=dict(mouth="o", look=0, la=40, la2=60, ra=40, ra2=60))

def f_spikes(cr, lt, d, t):
    bg(cr, C("0B132B"), C("1C2541"))
    prog = ease(lt / (d * .75))
    chart(cr, 90, 1080, 900, 900, prog, [(.08, .2), (.31, .2), (.54, .2), (.77, .7), (.92, .2)], YEL)
    for i, f in enumerate((.08, .31, .54, .92)):
        k = back((lt - d * .75 * f - .1) / .2)
        if k > 0: pill(cr, 90 + f * 900, 760 - (i % 2) * 70, "+14%", 40, MINT, INK, k)
    k = back((lt - d * .75 * .77 - .1) / .25)
    if k > 0:
        pill(cr, 90 + .77 * 900 - 60, 300, "+82% NEW YEAR", 56, YEL, INK, k * (1 + .04 * math.sin(t * 8)), -.03)
    text(cr, "MONDAYS", 90 + .08 * 900, 1140, 30, WHITE, .7, anchor="c"); text(cr, "JAN 1", 90 + .77 * 900, 1140, 30, YEL, anchor="c")

def f_gym(cr, lt, d, t):
    bg(cr, C("FFBE0B"), C("FB5607")); rays(cr, 540, 600, t, WHITE, .1)
    treadmill(cr, 380, 1180, 480, t); runner(cr, 380, 1180, 330, t, shirt=BLUE)
    labels = [("NEW MONTH", MINT), ("BIRTHDAY", PINK), ("HOLIDAY", WHITE)]
    for i, (lb, c) in enumerate(labels):
        calendar(cr, 230 + i * 310, 420 + (i % 2) * 40, 230, lb, ["1", "★", "✓"][i], [BLUE, PINK, C("2A9D8F")][i], back((lt - .2 - i * .4) / .25), (i - 1) * .08)
    for i in range(3):
        k = back((lt - .4 - i * .4) / .25)
        if k > 0: push(cr, 860, 1000 - i * 90, k); poly(cr, [(-30, 20), (0, -25), (30, 20)], C("70E000")); cr.restore()
    pill(cr, 860, 1120, "GYM VISITS", 40, INK, WHITE, back((lt - .3) / .25))

def f_selves(cr, lt, d, t):
    bg(cr, C("2B2D42"), C("8D99AE"))
    k = ease((lt - .2) / (d * .5))
    o = person(cr, 290, 1220, 320, shirt=C("8D99AE"), pants=C("6C757D"), pose=dict(mouth="frown", look=-.5))
    pill(cr, 290, 760, "OLD YOU", 48, C("6C757D"), WHITE, 1.0, -.04)
    calendar(cr, 540, 450, 260, "NEW WEEK", "1", MINT, back((lt - .1) / .3), .04)
    glow(cr, 790, 980, 260 * k, YEL, .5 * k)
    person(cr, 790, 1220, 360, shirt=YEL, pants=INK, pose=dict(mouth="smile", ra=160, ra2=-10, la=160, la2=-10, blink=(t % 2.5) < .1))
    pill(cr, 790, 720, "NEW YOU", 52, YEL, INK, back((lt - .4) / .25), .04)
    line(cr, 540, 640, 540, 1240, 6, WHITE, .4, dash=[18, 14])

def f_end(cr, lt, d, t):
    bg(cr, C("06D6A0"), C("118AB2")); rays(cr, 540, 640, t * .6, WHITE, .14)
    calendar(cr, 330, 620, 300, "JANUARY", "1", C("6C757D"), 1.0, -.08)
    cross(cr, 330, 640, 300, RED, back((lt - .2) / .25))
    calendar(cr, 760, 660, 340, "NEXT MONDAY", "→", RED, back((lt - .5) / .3), .06, circled=ease((lt - .8) / .5))
    pill(cr, 540, 270, "DON'T WAIT FOR JANUARY", 58, INK, WHITE, back((lt - .05) / .25), -.03)

BEATS = [
    dict(say="Why does every diet start on a Monday?", cap="Why does every diet start on a *Monday?*", scene=f_hook),
    dict(say="Researchers at Wharton tracked eight years of Google searches for the word diet.", cap="Wharton researchers tracked 8 years of Google searches for *“diet”*.", scene=f_search),
    dict(say="Searches jump fourteen percent at the start of every week, and eighty two percent at the start of a new year.", cap="*+14%* at the start of every week. *+82%* at the start of a *new year*.", scene=f_spikes),
    dict(say="Gym visits and goal pledges spike the same way: after new months, birthdays and holidays.", cap="Gym visits and goal pledges spike too: new *months*, *birthdays*, *holidays*.", scene=f_gym),
    dict(say="A new date feels like a clean page. Your old mistakes belong to the old you.", cap="A new date is a *clean page*. Old mistakes belong to the *old you*.", scene=f_selves),
    dict(say="So don't wait for January. Next Monday counts. Send this to your from Monday friend.", cap="Don't wait for January. *Next Monday* counts. Send this to your *“from Monday”* friend.", scene=f_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("34_fresh_start", BEATS, voice=("af_heart", 1.08, "en-us"))
    if "--stills" in sys.argv: sheet(f)
    else: f.render()
