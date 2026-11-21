"""Film 22: the peak-end rule (Kahneman et al. 1993, 'When More Pain Is Preferred to Less'). Motion style."""
import sys, math
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, face, pill
from film_tickle import hand

ICE = C("BDE6FF"); WATER = C("4CC9F0"); WATER2 = C("0077B6")

def bucket(cr, x, y, w, t, col=C("ADB5BD"), shiver=0.0):
    """origin = rim centre; w = rim width"""
    h = w * .9; sx = math.sin(t * 50) * shiver
    poly(cr, [(x - w / 2 + sx, y), (x + w / 2 + sx, y), (x + w * .38 + sx, y + h), (x - w * .38 + sx, y + h)], col)
    ell(cr, x + sx, y, w / 2, w * .09, C("6C757D"))
    ell(cr, x + sx, y + 4, w * .46, w * .075, WATER)
    for i in range(4):
        bx = x - w * .3 + i * w * .2 + sx; by = y + 2 + math.sin(t * 2 + i) * 3
        rrect(cr, bx - w * .05, by - w * .04, w * .1, w * .08, w * .02, ICE, .95)
    for i in range(3): line(cr, x - w * .3 + i * w * .3 + sx, y + h * .25, x - w * .26 + i * w * .3 + sx, y + h * .85, 5, WHITE, .25)

def submerge(cr, x, y, w, t):
    """redraw the bucket's front wall over whatever is in the water, so hands look submerged"""
    h = w * .9
    poly(cr, [(x - w / 2, y + w * .06), (x + w / 2, y + w * .06), (x + w * .38, y + h), (x - w * .38, y + h)], C("ADB5BD"))
    for i in range(3): line(cr, x - w * .3 + i * w * .3, y + h * .25, x - w * .26 + i * w * .3, y + h * .85, 5, WHITE, .25)
    cr.new_path(); cr.arc(x, y + w * .02, w / 2, 0, math.pi); cr.set_line_width(10); src(cr, C("6C757D")); cr.stroke()
    ell(cr, x, y + w * .04, w * .44, w * .035, WATER, .7)

def therm(cr, x, y, h, v, lbl, k=1.0):
    """v = 0..1 fill, lbl drawn beside"""
    if k <= 0: return
    push(cr, x, y, k)
    rrect(cr, -26, -h, 52, h, 26, WHITE); circle(cr, 0, 0, 44, WHITE)
    col = lerpc(C("3A86FF"), C("FF006E"), v)
    rrect(cr, -12, -h * (.15 + .7 * v), 24, h * (.15 + .7 * v), 12, col); circle(cr, 0, 0, 32, col)
    text(cr, lbl, 0, 100, 56, WHITE, anchor="c")
    cr.restore()

def stopwatch(cr, x, y, r, sec, total, lbl, col=YEL):
    circle(cr, x, y, r + 14, INK); circle(cr, x, y, r, WHITE)
    rrect(cr, x - 22, y - r - 46, 44, 34, 8, INK)
    p = min(1, sec / total) if total else 0
    cr.new_path(); cr.move_to(x, y); cr.arc(x, y, r * .86, -math.pi / 2, -math.pi / 2 + 2 * math.pi * max(.001, p)); cr.close_path(); src(cr, col, .55); cr.fill()
    text(cr, lbl, x, y + r * .2, r * .58, INK, anchor="c")

def chill(cr, x, y, t, n=3):
    for i in range(n):
        ph = (t * 1.2 + i / n) % 1
        a0 = -1.2 + i * .6
        line(cr, x + math.cos(a0) * (60 + ph * 50), y + math.sin(a0) * (60 + ph * 50), x + math.cos(a0) * (90 + ph * 50), y + math.sin(a0) * (90 + ph * 50), 8, ICE, 1 - ph)

# ---------- scenes ----------
def p_hook(cr, lt, d, t):
    bg(cr, C("023E8A"), C("7209B7")); rays(cr, 540, 700, t, WHITE, .1)
    sh = math.sin(t * 44) * 8
    bucket(cr, 540, 760, 460, t, shiver=.3)
    hand(cr, 560 + sh, 800, 150, t, rot=math.pi / 2, wig=.4); submerge(cr, 540, 760, 460, t)
    face(cr, 540 + sh, 435, 140, t, "cringe")
    chill(cr, 540, 435, t, 4)
    pill(cr, 230, 1000, "60 SEC", 60, WHITE, INK, 1, -.08)
    pill(cr, 850, 1000, "90 SEC", 60, YEL, INK, 1 + .06 * math.sin(t * 9), .08)
    k = 1
    if k > 0: pill(cr, 540, 228, "MORE PAIN?", 76, C("FF006E"), WHITE, k * (1 + .04 * math.sin(t * 10)), -.04)

def p_short(cr, lt, d, t):
    bg(cr, C("0B132B"), C("1C2541"))
    sec = min(60, 60 * lt / (d * .85))
    stopwatch(cr, 300, 420, 150, sec, 60, f"{int(sec)}s")
    therm(cr, 820, 560, 300, .1, "14°C", back((lt - .1) / .3))
    bucket(cr, 540, 860, 380, t, shiver=.4)
    hand(cr, 560, 860, 130, t, rot=math.pi / 2, wig=.3); submerge(cr, 540, 860, 380, t)
    face(cr, 190, 1000, 110, t, "cringe")
    pill(cr, 880, 1010, "HAND 1", 50, WHITE, INK, back((lt - .2) / .25))

def p_long(cr, lt, d, t):
    bg(cr, C("0B132B"), C("3A0CA3"))
    sec = min(90, 90 * lt / (d * .85))
    stopwatch(cr, 300, 420, 150, sec, 90, f"{int(sec)}s", col=C("FF9F1C") if sec > 60 else YEL)
    v = .1 + .35 * ease((sec - 60) / 30) if sec > 60 else .1
    therm(cr, 820, 560, 300, v, "15°C" if sec > 75 else "14°C", back((lt - .1) / .3))
    k = ease((lt - d * .5) / .3)
    if k > 0: pill(cr, 820, 220, "+30s", 56, YEL, INK, back((lt - d * .5) / .25), .06)
    bucket(cr, 540, 860, 380, t, shiver=.4 * (1 - k))
    hand(cr, 560, 860, 130, t, rot=math.pi / 2, wig=.3); submerge(cr, 540, 860, 380, t)
    face(cr, 190, 1000, 110, t, "cringe" if k < .5 else "smile")
    pill(cr, 880, 1010, "HAND 2", 50, WHITE, INK, back((lt - .2) / .25))

def p_vote(cr, lt, d, t):
    bg(cr, C("FFBE0B"), C("FB5607")); rays(cr, 760, 640, t, WHITE, .12)
    bucket(cr, 300, 760, 300, t, C("ADB5BD"))
    bucket(cr, 780, 760, 300, t, C("ADB5BD"))
    text(cr, "60s", 300, 1110, 70, WHITE, anchor="c"); text(cr, "90s", 780, 1110, 70, WHITE, anchor="c")
    k = ease((lt - .15) / (d * .55)); pct = int(69 * k)
    push(cr, 780, 430, back((lt - .1) / .3) * (1 + .04 * math.sin(t * 8))); circle(cr, 0, 0, 170, INK); text(cr, f"{pct}%", 0, 34, 110, YEL, anchor="c"); cr.restore()
    push(cr, 300, 470, back((lt - .3) / .3)); circle(cr, 0, 0, 110, WHITE, .9); text(cr, f"{100 - pct}%", 0, 24, 70, INK, anchor="c"); cr.restore()
    check(cr, 780, 960, 120, GREEN, back((lt - d * .6) / .25))
    for i in range(5):
        ph = (t * .5 + i / 5) % 1; circle(cr, 640 + (i * 71) % 280, 1180 - ph * 900, 10, WHITE, .6 * (1 - ph))

def p_memory(cr, lt, d, t):
    bg(cr, C("10002B"), C("3C096C"))
    x0, x1, y0 = 120, 960, 1000
    line(cr, x0, y0, x1, y0, 6, WHITE, .4); line(cr, x0, 300, x0, y0, 6, WHITE, .4)
    text(cr, "PAIN", x0 + 20, 300, 40, WHITE, .5)
    pts = []
    for i in range(61):
        u = i / 60
        yv = 520 - 300 * math.exp(-((u - .32) / .14) ** 2) - 60 * math.sin(u * 9) * .3
        yv = yv + (u > .75) * (u - .75) * 900
        pts.append((x0 + 20 + u * (x1 - x0 - 40), min(y0 - 30, yv + 220)))
    p = min(1, lt / (d * .5)); n = max(2, int(len(pts) * p))
    polyline(cr, pts[:n], 12, C("FF006E"))
    # middle fades out (memory drops the duration)
    k = ease((lt - d * .5) / .4)
    if k > 0:
        mid = pts[24:46]; polyline(cr, mid, 30, C("10002B"), .85 * k)
        px, py = pts[19]; ex, ey = pts[-1]
        push(cr, px, py, back((lt - d * .5) / .3)); circle(cr, 0, 0, 36, YEL); cr.restore()
        push(cr, ex, ey, back((lt - d * .6) / .3)); circle(cr, 0, 0, 36, YEL); cr.restore()
        pill(cr, px, py - 110, "WORST", 48, YEL, INK, back((lt - d * .55) / .25), -.06)
        pill(cr, ex - 40, ey - 110, "END", 48, YEL, INK, back((lt - d * .65) / .25), .06)

def p_end(cr, lt, d, t):
    bg(cr, C("FF006E"), C("8338EC")); rays(cr, 540, 640, t, WHITE, .12)
    face(cr, 540, 660, 220, t, "smile", look=.4)
    for i in range(3):
        k = back((lt - .1 - i * .15) / .25)
        if k > 0:
            x = 220 + i * 320
            push(cr, x, 1000, k); rrect(cr, -130, -55, 260, 110, 55, WHITE); text(cr, ["MEETINGS", "TRIPS", "WORKOUTS"][i], 0, 16, 40, INK, anchor="c"); cr.restore()
    for i in range(6):
        ph = (t * .45 + i / 6) % 1; heart(cr, 150 + (i * 167) % 800, 1200 - ph * 1000, .6 * (1 - ph * .4), WHITE if i % 2 else YEL, .8 * (1 - ph))
    pill(cr, 540, 300, "END ON A HIGH", 76, YEL, INK, back((lt - .2) / .25) * (1 + .05 * math.sin(t * 8)), .04)

BEATS = [
    dict(say="Would you choose more pain? In one famous study, most people did.", cap="Would you choose *more pain*? In one famous study, most people *did*.", scene=p_hook),
    dict(say="One hand in icy water, fourteen degrees, for sixty seconds.", cap="One hand in *icy water*, 14°C, for *60 seconds*.", scene=p_short),
    dict(say="The other hand: the same sixty seconds, plus thirty more, as it warmed to fifteen.", cap="The other hand: the same 60 seconds, *plus 30 more*, as it warmed to 15°C.", scene=p_long),
    dict(say="Asked which one to repeat, sixty nine percent picked the longer one.", cap="Asked which to repeat, *69%* picked the *longer one*.", scene=p_vote, hold=0.2),
    dict(say="Memory ignores how long something lasts. It keeps the worst moment, and the end.", cap="Memory ignores how long it lasts. It keeps the *worst moment*, and the *end*.", scene=p_memory),
    dict(say="So end your meetings, trips and workouts on a high. Send this to someone.", cap="So end meetings, trips and workouts *on a high*. Send this to someone.", scene=p_end, hold=0.3),
]

def sheet(f):
    from PIL import Image
    ts = [0.0, 1.0]
    for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
    ims = []
    for n, tt in enumerate(ts):
        p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
    s = Image.new("RGB", (270 * 6, 480 * 2))
    for n, im in enumerate(ims): s.paste(im, ((n % 6) * 270, (n // 6) * 480))
    s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])

if __name__ == "__main__":
    f = Film("22_peak_end", BEATS, voice=("af_heart", 1.08, "en-us"))
    if "--stills" in sys.argv: sheet(f)
    else: f.render()
