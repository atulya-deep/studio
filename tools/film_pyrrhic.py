"""Film 35: the Pyrrhic victory. Plutarch, Life of Pyrrhus 21 (Perrin): Asculum 279 BC, Romans lost 6,000 (Hieronymus),
Pyrrhus 3,505 dead 'according to the king's own commentaries'; 'If we are victorious in one more battle with the Romans,
we shall be utterly ruined.' Rome refilled its army 'as from a fountain'; he had lost most of his friends and generals.
Heraclea 280 BC was his first win; he used war elephants."""
import sys, math
from kit2 import *
from scenes import walk_pose
from motion import Film, W, H
from film_voice import bg, rays, pill
from film_peak import sheet

EPI = C("1D4E89"); EPI2 = C("0D2C54"); ROM = C("D62828")

def king(cr, x, y, s, t, mood="smile", **kw):
    pose = dict(helmet=GOLD, crest=EPI, shield=EPI, beard=C("5C4033"), cloak=C("7B2CBF"), la=20, la2=-30, mouth=mood, blink=(t % 3.3) < .12)
    pose.update(kw)
    o = person(cr, x, y, s, shirt=EPI, pants=EPI2, pose=pose)
    hx, hy = o["head"]; u = o["u"]
    poly(cr, [(hx - 12 * u, hy - 14 * u), (hx - 8 * u, hy - 26 * u), (hx - 3 * u, hy - 17 * u), (hx, hy - 28 * u), (hx + 3 * u, hy - 17 * u), (hx + 8 * u, hy - 26 * u), (hx + 12 * u, hy - 14 * u)], YEL)
    return o

def hoplite(cr, x, y, s, t, **kw):
    pose = dict(helmet=BRONZE, crest=EPI, shield=EPI, la=20, la2=-30, spear=True, mouth="flat"); pose.update(kw)
    return person(cr, x, y, s, shirt=EPI, pants=EPI2, pose=pose)

def trophy(cr, x, y, s, crack=0.0, a=1.0):
    u = s / 100
    poly(cr, [(x - 40 * u, y - 100 * u), (x + 40 * u, y - 100 * u), (x + 28 * u, y - 50 * u), (x - 28 * u, y - 50 * u)], GOLD, a)
    for sx in (-1, 1): ring(cr, x + sx * 44 * u, y - 82 * u, 16 * u, 7 * u, GOLD, a)
    rrect(cr, x - 8 * u, y - 52 * u, 16 * u, 32 * u, 4 * u, GOLD, a); rrect(cr, x - 30 * u, y - 22 * u, 60 * u, 22 * u, 6 * u, C("B5852D"), a)
    if crack > 0:
        pts = [(x - 6 * u, y - 100 * u), (x + 6 * u, y - 88 * u), (x - 4 * u, y - 76 * u), (x + 8 * u, y - 62 * u), (x, y - 50 * u)]
        n = max(2, int(len(pts) * min(1, crack))); polyline(cr, pts[:n], 4 * u, INK, a)

def battlefield(cr, t, dusk=0.0):
    bg(cr, lerpc(C("FFB703"), C("6A040F"), dusk), lerpc(C("FB8500"), C("370617"), dusk))
    poly(cr, [(-50, 1900), (-50, 1000), (300, 930), (700, 1010), (1130, 940), (1130, 1900)], lerpc(C("BC6C25"), C("3D1308"), dusk))

def flag(cr, x, y, col, t, a=1.0):
    line(cr, x, y, x, y - 200, 8, C("6E4A2F"), a)
    pts = [(x, y - 200), (x + 90, y - 190 + 10 * math.sin(t * 6)), (x + 90, y - 130 + 10 * math.sin(t * 6 + 1)), (x, y - 140)]
    poly(cr, pts, col, a)

def helmet_down(cr, x, y, s, col=BRONZE):
    cr.new_path(); cr.arc(x, y, s, math.pi, 2 * math.pi); src(cr, col); cr.fill(); rrect(cr, x - s * 1.1, y - 2, s * 2.2, s * .25, 4, col)

def p_hook(cr, lt, d, t):
    bg(cr, C("6A040F"), C("03071E")); rays(cr, 540, 700, t, YEL, .1)
    elephant(cr, 820, 1220, 380, t, walk=.2)
    o = king(cr, 380, 1220, 420, t, "frown", ra=150, ra2=-20)
    rx, ry = o["rh"]
    sh = math.sin(t * 50) * 5
    trophy(cr, rx + sh, ry + 20, 120, crack=min(1, (lt + .3) / .8))
    pill(cr, 540, 280, "HE WON. IT RUINED HIM.", 60, YEL, INK, 1 + .04 * math.sin(t * 8), -.03)

def p_heraclea(cr, lt, d, t):
    battlefield(cr, t)
    pill(cr, 540, 260, "280 BC · HERACLEA", 58, INK, WHITE, back((lt - .05) / .25), -.03)
    p = ease(lt / d)
    for i in range(2):
        elephant(cr, 120 + p * 260 + i * 200, 1150 + i * 70, 300 - i * 30, t + i, walk=1.0)
    for i in range(4):
        x = 760 + i * 80 + p * 160; roman(cr, x, 1180 + (i % 2) * 40, 230, t, face=-1, mouth="o", **walk_pose(t + i, 14))
    for i in range(3):
        ph = (t * 1.3 + i / 3) % 1; circle(cr, 140 + p * 260 + i * 60, 1200 - ph * 120, 18 + ph * 20, C("DDB892"), .6 * (1 - ph))
    pill(cr, 300, 520, "WAR ELEPHANTS", 44, YEL, INK, back((lt - .4) / .25), .04)

def p_asculum(cr, lt, d, t):
    battlefield(cr, t, .5)
    pill(cr, 540, 260, "279 BC · ASCULUM", 58, INK, WHITE, back((lt - .05) / .25), -.03)
    flag(cr, 200, 1150, EPI, t)
    king(cr, 360, 1180, 300, t, "smile" if lt < d * .5 else "frown", ra=160, ra2=-10)
    k = back((lt - .3) / .25)
    if k > 0:
        push(cr, 760, 640, k); rrect(cr, -250, -170, 500, 340, 30, INK, .9)
        text(cr, "DEAD", 0, -105, 36, MUTED, anchor="c")
        cr.restore()
        push(cr, 760, 640, k)
        cr.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        for i, (lb, n, c) in enumerate([("ROME", "6,000", C("FF6B6B")), ("PYRRHUS", "3,505", C("74C0FC"))]):
            kk = back((lt - .6 - i * .5) / .25)
            if kk > 0:
                text(cr, lb, -215, -10 + i * 100, 42, c, kk)
                cr.set_font_size(58); tw = cr.text_extents(n).x_advance; text(cr, n, 215 - tw, -10 + i * 100, 58, WHITE, kk)
        cr.restore()
    for i in range(6):
        kk = back((lt - d * .5 - i * .08) / .2)
        if kk > 0: push(cr, 560 + i * 80, 1170 + (i % 2) * 20, kk); helmet_down(cr, 0, 0, 28); cr.restore()

def p_refill(cr, lt, d, t):
    bg(cr, C("E0FBFC"), C("98C1D9"))
    line(cr, 540, 300, 540, 1240, 6, INK, .3, dash=[18, 14])
    # Rome: a fountain pouring out fresh soldiers
    rrect(cr, 60, 520, 400, 320, 0, C("CDB4A0"))
    for i in range(5): rrect(cr, 60 + i * 84, 480, 50, 50, 0, C("CDB4A0"))
    cr.new_path(); cr.move_to(170, 840); cr.line_to(170, 690); cr.arc(260, 690, 90, math.pi, 2 * math.pi); cr.line_to(350, 840); cr.close_path(); src(cr, C("3D2B1F")); cr.fill()
    text(cr, "ROMA", 260, 580, 40, C("6E4A2F"), anchor="c", face="Lora")
    for i in range(6):
        ph = (lt * .6 + i / 6) % 1; x = 260 + (i % 2 - .5) * 120 * ph; y = 800 + ph * 420
        roman(cr, x, y, 200, t, mouth="smile", **walk_pose(t + i, 10))
    pill(cr, 260, 400, "ROME: REFILLED", 40, ROM, WHITE, back((lt - .1) / .25), -.04)
    # Pyrrhus: gaps that stay empty
    for i in range(6):
        x = 640 + (i % 3) * 150; y = 1000 + (i // 3) * 220
        if i in (0, 4): hoplite(cr, x, y, 200, t, mouth="frown")
        else:
            a = max(.25, 1 - ease((lt - .3 - i * .15) / .4))
            if a > .3: hoplite(cr, x, y, 200, t)
            else: rrect(cr, x - 35, y - 200, 70, 200, 30, INK, .12)
    pill(cr, 800, 400, "PYRRHUS: GONE", 40, EPI, WHITE, back((lt - .5) / .25), .04)

def p_quote(cr, lt, d, t):
    bg(cr, C("240046"), C("5A189A")); rays(cr, 540, 700, t, WHITE, .06)
    person(cr, 820, 1220, 330, shirt=C("2A9D8F"), pants=INK, pose=dict(mouth="smile", face=-1, ra=40, la=150, la2=-20, look=-.5))
    bubble(cr, 810, 780, 300, 90, "WELL DONE!", 40, back((lt - .05) / .2), WHITE, INK)
    king(cr, 330, 1220, 400, t, "flat", tilt=-3)
    k = back((lt - d * .3) / .3)
    if k > 0:
        push(cr, 540, 420, k); rrect(cr, -460, -170, 920, 340, 40, YEL)
        poly(cr, [(-260, 166), (-200, 166), (-280, 240)], YEL)
        for i, ln in enumerate(["“If we are victorious in one", "more battle with the Romans,", "we shall be utterly ruined.”"]):
            text(cr, ln, 0, -65 + i * 80, 50, INK, anchor="c", face="Lora")
        cr.restore()
    text(cr, "Plutarch, Life of Pyrrhus", 540, 650, 30, WHITE, .6 * min(1, k), anchor="c")

def p_end(cr, lt, d, t):
    bg(cr, C("FFBE0B"), C("FB5607")); rays(cr, 540, 700, t * .6, WHITE, .14)
    # one person 'wins' the argument and is left alone
    p = ease((lt - .4) / (d * .5))
    person(cr, 360, 1220, 360, shirt=EPI, pants=INK, pose=dict(mouth="smile", ra=165, ra2=0, la=165, la2=0))
    trophy(cr, 380, 680, 130)
    for i in range(3):
        person(cr, 700 + i * 110 + p * 600, 1220, 300, shirt=[C("2A9D8F"), PINK, C("8338EC")][i], pants=INK, pose=dict(walk_pose(t + i, 9), face=1, mouth="frown"))
    pill(cr, 540, 290, "COUNT THE COST", 76, INK, WHITE, back((lt - .1) / .25), -.03)
    pill(cr, 540, 420, "BEFORE YOU WIN", 60, WHITE, INK, back((lt - .35) / .25), .03)

BEATS = [
    dict(say="He won the battle. And it ruined him.", cap="He *won* the battle. And it *ruined him*.", scene=p_hook),
    dict(say="280 B C. King Pyrrhus brings war elephants to Italy, and beats Rome.", cap="*280 BC.* King Pyrrhus brings *war elephants* to Italy, and beats Rome.", scene=p_heraclea),
    dict(say="A year later, at Asculum, he wins again. But by his own count, thirty five hundred of his men are dead.", cap="A year later he *wins again*. But by his own count, *3,505* of his men are dead.", scene=p_asculum),
    dict(say="Rome refills its army. Pyrrhus can't replace his veterans or his generals.", cap="Rome *refills* its army. Pyrrhus *can't replace* his veterans or generals.", scene=p_refill),
    dict(say="When a man congratulated him, he said: If we are victorious in one more battle with the Romans, we shall be utterly ruined.", cap="Congratulated, he said: *one more* win like this and we're *utterly ruined*.", scene=p_quote),
    dict(say="That's a Pyrrhic victory. Count the cost before you win. Send this to someone who wins every argument.", cap="That's a *Pyrrhic victory*. Count the cost. Send this to someone who *wins every argument*.", scene=p_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("35_pyrrhic", BEATS, voice=("af_heart", 1.08, "en-us"))
    if "--stills" in sys.argv: sheet(f)
    else: f.render()
