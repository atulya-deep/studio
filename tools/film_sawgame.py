"""Film 29: one Delhi rally, two realities (Nov 1, 2026) + Hastorf & Cantril 'They Saw a Game' (1951/1954). Neutral: both claims shown, no verdict."""
import sys, math, random
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, face, pill

SIDE_A = C("1D4ED8"); SIDE_B = C("F97316"); GRASS = C("8AB17D")
rnd = random.Random(7)
HEADS = [(rnd.uniform(60, 1020), rnd.uniform(560, 1180), rnd.choice([SKIN, SKIN2, C("C68642"), C("8D5524")])) for _ in range(420)]

def ground(cr):
    rrect(cr, 0, 520, W, 720, 0, C("C9B79C"))
    for i in range(6): line(cr, 0, 560 + i * 120, W, 560 + i * 120, 2, WHITE, .15)
    rrect(cr, 340, 470, 400, 90, 10, C("3D405B")); text(cr, "STAGE", 540, 530, 40, WHITE, anchor="c")

def crowd(cr, t, x0, x1, dens=1.0, col=SIDE_A):
    for i, (x, y, sk) in enumerate(HEADS):
        if not (x0 <= x <= x1) or (i % 100) / 100 > dens: continue
        b = math.sin(t * 6 + i) * 4
        rrect(cr, x - 14, y + 6 + b, 28, 26, 10, col); circle(cr, x, y + b, 12, sk)
        if i % 9 == 0: line(cr, x + 10, y + b, x + 22, y - 40 + b, 4, WHITE); rrect(cr, x + 12, y - 70 + b, 40, 30, 4, WHITE)

def chairs(cr, t, x0, x1, empty_frac=0.25, hi=0.0):
    rnd2 = random.Random(3)
    for r in range(11):
        for c in range(int((x1 - x0) / 60)):
            x = x0 + 30 + c * 60; y = 600 + r * 54
            emp = rnd2.random() < empty_frac
            col = C("ADB5BD") if emp else C("6C757D")
            rrect(cr, x - 18, y - 16, 36, 30, 6, col)
            if emp and hi > 0: ring(cr, x, y, 26, 4, RED, hi)
            if not emp: circle(cr, x, y - 26, 11, SKIN2)

def g_hook(cr, lt, d, t):
    bg(cr, C("0F172A"), C("1E293B"))
    ground(cr)
    crowd(cr, t, 0, 540, 1.0, SIDE_A)
    chairs(cr, t, 540, 1080, .55)
    line(cr, 540, 440, 540, 1240, 8, WHITE, .9)
    pill(cr, 270, 330, "PACKED", 64, SIDE_A, WHITE, back((lt + .25) / .25), -.05)
    pill(cr, 810, 330, "EMPTY", 64, SIDE_B, WHITE, back((lt + .25) / .25), .05)
    pill(cr, 540, 1300 - 120, "SAME RALLY", 56, WHITE, INK, back((lt - .5) / .25), 0)

def g_claimA(cr, lt, d, t):
    bg(cr, C("1E3A8A"), C("0F172A")); rays(cr, 540, 760, t, C("60A5FA"), .1)
    ground(cr); crowd(cr, t, 0, 1080, 1.0, SIDE_A)
    v = int(1000000 * ease((lt - .2) / (d * .7)))
    s = f"{v:,}".replace(",", "")
    s = (lambda n: (n[:-5] + "," + n[-5:-3] + "," + n[-3:]) if len(n) > 5 else n)(s) if v >= 100000 else f"{v:,}"
    push(cr, 540, 300, 1 + .03 * math.sin(t * 8)); rrect(cr, -380, -90, 760, 180, 40, WHITE); text(cr, s, 0, 40, 120, SIDE_A, anchor="c", face="Lora"); cr.restore()

def g_claimB(cr, lt, d, t):
    bg(cr, C("7C2D12"), C("1C1917"))
    ground(cr); chairs(cr, t, 0, 1080, .22, hi=ease((lt - .6) / .4))
    pill(cr, 540, 250, "28,000 CHAIRS", 66, WHITE, INK, back((lt - .1) / .25), -.03)
    pill(cr, 540, 380, "5,000-7,000 EMPTY?", 62, SIDE_B, WHITE, back((lt - .7) / .25), .03)

def tv(cr, x, y, w, t):
    h = w * .62
    rrect(cr, x - w / 2 - 20, y - h / 2 - 20, w + 40, h + 40, 24, C("212529")); rrect(cr, x - w / 2, y - h / 2, w, h, 12, GRASS)
    for i in range(5): line(cr, x - w / 2 + i * w / 4, y - h / 2, x - w / 2 + i * w / 4, y + h / 2, 3, WHITE, .5)
    bx = x + math.sin(t * 2.5) * w * .3; by = y + math.cos(t * 3.1) * h * .25
    ell(cr, bx, by, 22, 14, C("7F5539"), rot=t * 3)
    for i in range(4):
        px = x + math.sin(t * 2.5 + i) * w * .35; py = y + math.cos(t * 2 + i * 1.3) * h * .3
        circle(cr, px, py, 16, C("F97316") if i % 2 else C("15803D")); circle(cr, px, py, 7, INK)

def fan(cr, x, y, s, t, col, mood):
    o = person(cr, x, y, s, shirt=col, pose=dict(mouth=mood, ra=150 + math.sin(t * 9) * 12, ra2=20, la=12, blink=(t % 2.7) < .12))
    return o

def g_1951(cr, lt, d, t):
    bg(cr, C("FEF3C7"), C("FDE68A"))
    pill(cr, 540, 260, "1951", 92, INK, WHITE, back((lt - .05) / .25), -.04)
    tv(cr, 540, 640, 640, t)
    fan(cr, 230, 1150, 330, t, C("F97316"), "o"); fan(cr, 850, 1150, 330, t + 1, C("15803D"), "o")
    pill(cr, 230, 900, "PRINCETON", 38, C("F97316"), WHITE, back((lt - .3) / .25)); pill(cr, 850, 900, "DARTMOUTH", 38, C("15803D"), WHITE, back((lt - .5) / .25))

def counter(cr, x, y, n, col, lbl, k):
    n = f"{n:.1f}"
    if k <= 0: return
    push(cr, x, y, k); rrect(cr, -210, -150, 420, 300, 30, WHITE); text(cr, lbl, 0, -80, 34, INK, anchor="c")
    text(cr, n, 0, 70, 140, col, anchor="c", face="Lora"); cr.restore()

def g_counts(cr, lt, d, t):
    bg(cr, C("111827"), C("374151"))
    tv(cr, 540, 360, 460, t)
    p = ease((lt - .2) / (d * .6))
    counter(cr, 280, 860, 9.8 * p, C("F97316"), "PRINCETON FANS", back((lt - .1) / .25))
    counter(cr, 800, 860, 4.3 * p, C("15803D"), "DARTMOUTH FANS", back((lt - .4) / .25))
    pill(cr, 540, 1110, "DARTMOUTH FOULS SEEN", 46, YEL, INK, back((lt - .8) / .25), 0)

def g_end(cr, lt, d, t):
    bg(cr, C("7C3AED"), C("1E1B4B")); rays(cr, 540, 640, t, WHITE, .08)
    for i, (sx, col) in enumerate(((-1, SIDE_A), (1, SIDE_B))):
        x = 540 + sx * 230
        face(cr, x, 680, 170, t + i, "smug", look=-sx * .8)
        for j in range(2): ring(cr, x - 60 + j * 120, 672, 52, 14, col)
        line(cr, x - 8, 672, x + 8, 672, 10, col)
    pill(cr, 540, 320, "WHAT WOULD I THINK", 54, WHITE, INK, back((lt - .3) / .25), -.03)
    pill(cr, 540, 420, "IF THE OTHER SIDE SAID IT?", 54, YEL, INK, back((lt - .55) / .25), .03)

BEATS = [
    dict(say="One rally in Delhi. Two completely different crowds.", cap="One rally in Delhi. *Two completely different* crowds.", scene=g_hook),
    dict(say="November first. The opposition talked of ten lakh people, protesting vote chori.", cap="November 1. The opposition talked of *10 lakh people*, protesting *vote chori*.", scene=g_claimA),
    dict(say="The B J P said five to seven thousand of the twenty eight thousand chairs were empty.", cap="The BJP said *5,000 to 7,000* of the *28,000 chairs* were empty.", scene=g_claimB),
    dict(say="Psychologists caught this back in 1951. Rival college fans watched the same film of a rough football game.", cap="Psychologists caught this in *1951*. Rival fans watched the *same film* of a rough game.", scene=g_1951),
    dict(say="Princeton fans saw Dartmouth commit almost ten fouls. Dartmouth fans saw about four.", cap="Princeton fans saw *almost 10* Dartmouth fouls. Dartmouth fans saw *about 4*.", scene=g_counts),
    dict(say="We don't just watch. We watch for our side. So ask: what would I think if the other side said this? Send this to someone who argues politics.", cap="We don't just watch. We watch *for our side*. Send this to someone who *argues politics*.", scene=g_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("29_saw_a_rally", BEATS, voice=("af_heart", 1.1, "en-us"))
    if "--stills" in sys.argv:
        from PIL import Image
        ts = [0.0, 1.5]
        for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
        ims = []
        for n, tt in enumerate(ts):
            p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
        s = Image.new("RGB", (270 * len(ims), 480)); [s.paste(im, (n * 270, 0)) for n, im in enumerate(ims)]; s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])
    else: f.render()
