"""Film 33: the Ben Franklin effect. Franklin's Autobiography (clerk of the Pennsylvania Assembly, 1736; opposed 1737;
borrowed 'a certain very scarce and curious book') + Jecker & Landy (1969, Human Relations 22:371-378)."""
import sys, math
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, pill
from film_bundle import book
from film_peak import sheet

COAT = C("7F5539"); COAT2 = C("3D405B"); SILVER = C("D9D9D9")

def tricorn(cr, o, col=INK):
    hx, hy = o["head"]; u = o["u"]
    poly(cr, [(hx - 19 * u, hy - 8 * u), (hx + 19 * u, hy - 8 * u), (hx + 10 * u, hy - 20 * u), (hx, hy - 26 * u), (hx - 10 * u, hy - 20 * u)], col)
    line(cr, hx - 19 * u, hy - 8 * u, hx + 19 * u, hy - 8 * u, 2.5 * u, GOLD)

def franklin(cr, x, y, s, t, mood="smile", **kw):
    """Ben: long grey hair, bald crown, round specs, brown coat"""
    pose = dict(hairstyle="long", mouth=mood, blink=(t % 3.1) < .12); pose.update(kw)
    o = person(cr, x, y, s, shirt=COAT, pants=C("4A3020"), hair=SILVER, pose=pose)
    hx, hy = o["head"]; u = o["u"]
    cr.new_path(); cr.arc(hx, hy - 1 * u, 13.2 * u, math.pi * 1.22, math.pi * 1.78); cr.line_to(hx, hy - 4 * u); cr.close_path(); src(cr, SKIN); cr.fill()
    glasses(cr, o); return o

def rival(cr, x, y, s, t, mood="frown", hat=True, **kw):
    pose = dict(mouth=mood, blink=(t % 2.7) < .12, hairstyle="short"); pose.update(kw)
    o = person(cr, x, y, s, shirt=COAT2, pants=INK, hair=C("F1F1F1"), pose=pose)
    if hat: tricorn(cr, o)
    return o

def storm(cr, x, y, t, k=1.0):
    if k <= 0: return
    cloud(cr, x - 90, y - 40, 180, 80, C("495057"), .95 * k)
    if (t % .8) < .2: polyline(cr, [(x, y + 30), (x - 18, y + 70), (x + 8, y + 70), (x - 10, y + 115)], 8, YEL, k)

def note(cr, x, y, k=1.0, rot=0.0):
    if k <= 0: return
    push(cr, x, y, k, rot); rrect(cr, -86, -61, 172, 122, 14, C("6E4A2F")); rrect(cr, -80, -55, 160, 110, 10, C("FFF3D6"))
    for i in range(4): line(cr, -55, -25 + i * 18, 55 - (i == 3) * 40, -25 + i * 18, 5, C("A68A64"))
    cr.restore()

def hall(cr, t):
    bg(cr, C("F2E3C6"), C("D9B98A"))
    for i in range(4):
        x = 60 + i * 280; rrect(cr, x, 260, 150, 380, 75, C("FFF8E7")); rrect(cr, x + 10, 270, 130, 360, 65, C("BDE0FE"), .6)
        line(cr, x + 75, 270, x + 75, 630, 6, C("FFF8E7")); line(cr, x + 10, 450, x + 140, 450, 6, C("FFF8E7"))
    rrect(cr, -20, 1180, W + 40, 800, 0, C("8B5E3C"))

def f_hook(cr, lt, d, t):
    bg(cr, C("3A0CA3"), C("F72585")); rays(cr, 540, 640, t, WHITE, .1)
    o = rival(cr, 780, 1180, 420, t, "frown", la=150, la2=-40)
    storm(cr, 780, 560, t)
    franklin(cr, 300, 1180, 400, t, "smile", ra=110, ra2=-30)
    book(cr, 520, 760 + math.sin(t * 5) * 14, 110, C("D62828"), "?", .1 * math.sin(t * 3))
    pill(cr, 540, 300, "ASK YOUR RIVAL FOR A FAVOUR", 52, YEL, INK, 1 + .04 * math.sin(t * 8), -.03)

def f_speech(cr, lt, d, t):
    hall(cr, t)
    pill(cr, 540, 250, "1737 · PENNSYLVANIA", 56, INK, WHITE, back((lt - .05) / .25), -.03)
    rival(cr, 790, 1180, 360, t, "o", ra=150 + 15 * math.sin(t * 6), ra2=-20)
    rrect(cr, 640, 1000, 300, 190, 20, C("6E4A2F")); rrect(cr, 620, 990, 340, 30, 12, C("8B5E3C"))
    for i in range(3):
        k = back((lt - .3 - i * .35) / .2)
        if k > 0: bubble(cr, 640 - i * 60, 600 - i * 120, 300 if i == 1 else 160, 80, "NO!" if i != 1 else "NOT FRANKLIN!", 36 if i == 1 else 44, k, RED, WHITE)
    franklin(cr, 230, 1180, 340, t, "frown", sit=True, face=1)
    rrect(cr, 120, 1080, 300, 30, 10, C("6E4A2F"))

def f_note(cr, lt, d, t):
    bg(cr, C("90E0EF"), C("0077B6"))
    franklin(cr, 220, 1180, 360, t, "smile", ra=100, ra2=-20)
    rival(cr, 860, 1180, 360, t, "flat" if lt < d * .6 else "o")
    p = ease((lt - .3) / (d * .5)); x = 330 + p * 380; y = 920 - math.sin(p * math.pi) * 300
    note(cr, x, y, .8, .3 * math.sin(p * 6.28))
    k = back((lt - .1) / .25)
    if k > 0:
        push(cr, 540, 420, k); rrect(cr, -280, -110, 560, 220, 30, WHITE)
        text(cr, "“May I borrow", 0, -20, 50, INK, anchor="c", face="Lora")
        text(cr, "your rare book?”", 0, 50, 50, INK, anchor="c", face="Lora"); cr.restore()
    book(cr, 690, 950, 80, C("D62828"), "", -.1, back((lt - d * .7) / .25))

def f_friends(cr, lt, d, t):
    bg(cr, C("D8F3DC"), C("95D5B2")); rays(cr, 540, 720, t, WHITE, .12)
    sm = lt > d * .35
    o1 = franklin(cr, 380, 1180, 400, t, "smile", ra=70, ra2=-10)
    o2 = rival(cr, 700, 1180, 400, t, "smile" if sm else "flat", la=70, la2=-10)
    for i in range(3):
        k = back((lt - d * .4 - i * .15) / .25)
        heart(cr, 440 + i * 100, 640 - i * 40 + math.sin(t * 3 + i) * 12, .9 * k, PINK)
    pill(cr, 540, 300, "FRIENDS FOR LIFE", 70, INK, WHITE, back((lt - d * .45) / .25), .03)
    note(cr, 540, 470, back((lt - .05) / .25) * .9, -.08)
    text(cr, "THANK YOU", 540, 485, 30, C("6E4A2F"), back((lt - .05) / .25), anchor="c", face="Lora")

def coin(cr, x, y, r, a=1.0):
    circle(cr, x, y, r, C("F4A261"), a); circle(cr, x, y, r * .75, YEL, a); text(cr, "$", x, y + r * .35, r, C("B5651D"), a, anchor="c")

def meter(cr, x, y, h, v, lbl, col, k=1.0):
    if k <= 0: return
    rrect(cr, x - 50, y - h, 100, h, 30, WHITE, .9); rrect(cr, x - 38, y - 12 - (h - 24) * v, 76, (h - 24) * v, 24, col)
    text(cr, lbl, x, y + 60, 34, INK, anchor="c")

def f_study(cr, lt, d, t):
    bg(cr, C("E0FBFC"), C("98C1D9"))
    pill(cr, 540, 250, "1969 STUDY", 64, INK, WHITE, back((lt - .05) / .25), -.03)
    o = person(cr, 760, 1180, 380, shirt=WHITE, pants=INK, pose=dict(mouth="smile", la=60, la2=-20))
    glasses(cr, o)
    p = person(cr, 300, 1180, 360, shirt=C("F77F00"), pants=INK, pose=dict(mouth="smile", ra=70, ra2=-20, look=.6))
    for i in range(3):
        ph = ((lt * 1.1) + i / 3) % 1; coin(cr, 370 + ph * 310, 860 - math.sin(ph * math.pi) * 140, 30, 1 - ph * .3)
    k = ease((lt - d * .35) / (d * .45))
    meter(cr, 330, 560, 230, .35, "NOT ASKED", C("ADB5BD"), back((lt - d * .25) / .25))
    meter(cr, 700, 560, 230, .35 + .55 * k, "DID A FAVOUR", PINK, back((lt - d * .3) / .25))
    heart(cr, 700, 270 + 40, .6 * k, PINK)

def f_end(cr, lt, d, t):
    bg(cr, C("FFBE0B"), C("FB5607")); rays(cr, 540, 700, t * .6, WHITE, .14)
    book(cr, 540, 800, 260, C("D62828"), "", .06 * math.sin(t * 2))
    pill(cr, 540, 300, "WE LIKE WHO WE HELP", 64, INK, WHITE, back((lt - .1) / .25), -.03)
    pill(cr, 540, 1120, "ASK FOR SOMETHING SMALL", 50, WHITE, INK, back((lt - d * .3) / .25), .03)

BEATS = [
    dict(say="Want a rival to like you? Ask him for a favour.", cap="Want a rival to *like you?* Ask him for a *favour*.", scene=f_hook),
    dict(say="1737. A powerful new lawmaker makes a long speech against Ben Franklin.", cap="*1737.* A new lawmaker gives a speech *against* Ben Franklin.", scene=f_speech),
    dict(say="Franklin doesn't flatter him. He writes asking to borrow a rare book.", cap="Franklin doesn't flatter him. He asks to *borrow a rare book*.", scene=f_note),
    dict(say="He returns it a week later with a thank you note. The man starts talking to him, and they stay friends for life.", cap="A week later, a *thank-you note*. They stay *friends for life*.", scene=f_friends),
    dict(say="In 1969, a study found the same thing. People who did a researcher a personal favour liked him more.", cap="*1969 study:* people who did a researcher a *favour* liked him *more*.", scene=f_study),
    dict(say="We like the people we help. So ask for something small. Send this to someone with a rival.", cap="We like the people we *help*. Ask for something *small*. Send this to someone with a *rival*.", scene=f_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("33_franklin", BEATS, voice=("af_heart", 1.08, "en-us"))
    if "--stills" in sys.argv: sheet(f)
    else: f.render()
