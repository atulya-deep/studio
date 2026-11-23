"""Film 25: people would rather shock themselves than sit alone with their thoughts (Wilson et al., Science 2014)."""
import sys, math
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, face, pill

def zap(cr, x, y, s, t, a=1.0):
    pts = [(x, y)]
    for i in range(1, 7): pts.append((x + (i % 2 * 2 - 1) * s * .25 + math.sin(t * 40 + i) * 6, y + i * s / 6))
    polyline(cr, pts, 14, YEL, a); polyline(cr, pts, 5, WHITE, a)

def button(cr, x, y, r, pressed=False, glowk=1.0):
    glow(cr, x, y, r * 2.2, RED, .35 * glowk)
    rrect(cr, x - r * 1.3, y - r * .1, r * 2.6, r * .9, r * .3, C("343A40"))
    ell(cr, x, y - (0 if pressed else r * .18), r, r * .45, C("C1121F")); ell(cr, x, y - (r * .1 if pressed else r * .32), r * .92, r * .38, RED)

def room(cr, t):
    bg(cr, C("E9ECEF"), C("ADB5BD"))
    rrect(cr, 0, 1000, W, 920, 0, C("CED4DA"))
    rrect(cr, 380, 220, 320, 360, 12, C("DEE2E6")); line(cr, 540, 220, 540, 580, 6, C("ADB5BD"))
    circle(cr, 860, 320, 70, WHITE); ring(cr, 860, 320, 70, 8, C("495057"))
    a = t * .2; line(cr, 860, 320, 860 + math.sin(a) * 50, 320 - math.cos(a) * 50, 6, INK); line(cr, 860, 320, 860 + math.sin(a / 12) * 34, 320 - math.cos(a / 12) * 34, 8, INK)

def chair_person(cr, x, y, t, mood="flat", look=0.0, reach=0.0):
    rrect(cr, x - 150, y - 40, 300, 40, 12, C("6C757D")); rrect(cr, x - 140, y, 20, 200, 6, C("495057")); rrect(cr, x + 120, y, 20, 200, 6, C("495057"))
    rrect(cr, x - 150, y - 300, 30, 270, 10, C("6C757D"))
    o = person(cr, x - 10, y + 30, 520, shirt=C("4F7DD9"), pose=dict(sit=True, face=1, mouth=mood, look=look, la=40, la2=60, ra=40 + reach * 60, ra2=60 - reach * 70, blink=(t % 3.1) < .12))
    return o

def s_hook(cr, lt, d, t):
    bg(cr, C("1B0033"), C("5A0FC8")); rays(cr, 540, 720, t, YEL, .1)
    k = .5 + .5 * math.sin(t * 6)
    button(cr, 540, 760, 200, pressed=(t % 1.2) < .15, glowk=k)
    for i in range(3): zap(cr, 200 + i * 340, 260 + (i % 2) * 60, 360, t + i, .5 + .5 * k)
    pill(cr, 540, 360, "OR", 90, WHITE, INK, back((lt + .25) / .25) * (1 + .05 * math.sin(t * 8)), -.04)
    pill(cr, 540, 1080, "15 MIN OF NOTHING", 64, YEL, INK, back((lt + .25) / .25), .03)

def s_room(cr, lt, d, t):
    room(cr, t)
    chair_person(cr, 470, 1000, t, "flat", look=math.sin(t * 1.3))
    for i, (x, y) in enumerate([(820, 620), (900, 760)]):
        k = back((lt - .3 - i * .3) / .25)
        if k > 0:
            push(cr, x, y, k, .1 * (i - .5)); rrect(cr, -60, -100, 120, 200, 18, INK, .9); cross(cr, 0, 0, 110, RED); cr.restore()
    pill(cr, 230, 300, "NO PHONE", 56, INK, WHITE, back((lt - .2) / .25), -.06)

def s_button(cr, lt, d, t):
    room(cr, t)
    rrect(cr, 640, 900, 260, 40, 10, C("6C757D")); rrect(cr, 700, 940, 140, 120, 8, C("495057"))
    button(cr, 770, 880, 70, glowk=.6 + .4 * math.sin(t * 5))
    chair_person(cr, 380, 1000, t, "flat", look=1)
    for i in range(3):
        ph = (t * .8 + i / 3) % 1; text(cr, "?", 780 + (i - 1) * 60, 720 - ph * 120, 70, RED, 1 - ph, face="Lora", anchor="c")
    pill(cr, 760, 560, "MILD SHOCK", 52, RED, WHITE, back((lt - .3) / .25), .05)

def s_press(cr, lt, d, t):
    bg(cr, C("FFD60A"), C("FF7B00")); rays(cr, 540, 700, t * 1.5, WHITE, .14)
    P = 1.6; ph = (t % P) / P; hit = ph < .2
    sh = math.sin(t * 70) * 14 if hit else 0
    face(cr, 540 + sh, 560, 220, t, "shock" if hit else "smile")
    if hit:
        for i in range(4): zap(cr, 260 + i * 180, 260, 260, t + i)
    tot = 18; done = min(12, int(12 * ease((lt - .3) / (d * .6))))
    for i in range(tot):
        x = 160 + (i % 9) * 95; y = 950 + (i // 9) * 120; lit = i < done
        circle(cr, x, y - 26, 24, INK if lit else C("FFE5A3")); rrect(cr, x - 28, y, 56, 52, 18, INK if lit else C("FFE5A3"))
        if lit: zap(cr, x + 20, y - 70, 60, t + i, .9)
    text(cr, f"{done} of 18 men", 540, 1230 - 20, 58, INK, anchor="c", face="Lora")

def s_women(cr, lt, d, t):
    bg(cr, C("FF006E"), C("8338EC"))
    tot = 24; done = min(6, int(6 * ease((lt - .2) / (d * .5))))
    for i in range(tot):
        x = 150 + (i % 8) * 110; y = 520 + (i // 8) * 150; lit = i < done
        col = YEL if lit else C("C77DFF")
        circle(cr, x, y - 30, 28, col); rrect(cr, x - 32, y, 64, 60, 22, col)
        if lit: zap(cr, x + 24, y - 90, 70, t + i, .9)
    text(cr, f"{done} of 24 women", 540, 1060, 64, WHITE, anchor="c", face="Lora")
    pill(cr, 540, 280, "WOMEN", 70, WHITE, INK, back((lt - .1) / .25), -.04)

def s_end(cr, lt, d, t):
    bg(cr, C("0B132B"), C("1C2541")); rays(cr, 540, 620, t * .6, C("5BC0BE"), .1)
    f = min(1, lt / (d * .9)); a = -math.pi / 2 + f * 2 * math.pi
    circle(cr, 540, 620, 260, C("3A506B")); ring(cr, 540, 620, 260, 22, C("5BC0BE"), 1, -math.pi / 2, a)
    face(cr, 540, 620, 160, t, "smile" if f > .5 else "flat", look=0)
    text(cr, "5:00", 540, 980, 110, WHITE, anchor="c", face="Lora")
    pill(cr, 540, 230, "NO PHONE. TRY IT.", 60, YEL, INK, back((lt - .2) / .25), -.03)

BEATS = [
    dict(say="Would you give yourself an electric shock, just to escape fifteen minutes of doing nothing?", cap="Would you *shock yourself* just to escape *15 minutes* of doing nothing?", scene=s_hook),
    dict(say="In a 2014 study, people sat alone in an empty room. No phone. Nothing to do.", cap="In a 2014 study, people sat alone in an empty room. *No phone.* Nothing to do.", scene=s_room),
    dict(say="Next to them, a button that gave a mild shock.", cap="Next to them: a button that gave a *mild shock*.", scene=s_button),
    dict(say="Twelve of eighteen men pressed it at least once.", cap="*12 of 18 men* pressed it at least once.", scene=s_press),
    dict(say="So did six of twenty four women. Pain beat boredom.", cap="So did *6 of 24 women*. Pain *beat boredom*.", scene=s_women),
    dict(say="Try five minutes with no phone today. Send this to someone who can't sit still.", cap="Try *5 minutes* with no phone today. Send this to someone who *can't sit still*.", scene=s_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("25_shock", BEATS, voice=("af_heart", 1.08, "en-us"))
    if "--stills" in sys.argv:
        from PIL import Image
        ts = [0.0, 1.5]
        for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
        ims = []
        for n, tt in enumerate(ts):
            p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
        s = Image.new("RGB", (270 * len(ims), 480)); [s.paste(im, (n * 270, 0)) for n, im in enumerate(ims)]; s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])
    else: f.render()
