"""Film 31 (opposition-leaning satire, at owner's request): 'Haare toh sawaal, jeete toh bawaal'.
BJP questioned EVMs out of power (2010 book, Gadkari quote); in 2026 questions about Bengal's ~91 lakh deletions get called anarchy.
Every claim sourced; no invented quotes."""
import sys, math
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, pill
from film_aayaram import neta
from film_evm import evm, sash, SAFF, TRI

def catch(cr, lt, k0=0.0):
    k1 = back((lt - k0) / .25); k2 = back((lt - k0 - .35) / .25)
    if k1 > 0: push(cr, 540, 240, k1, -.03); rrect(cr, -380, -64, 760, 128, 26, C("60A5FA")); text(cr, "HAARE TOH SAWAAL", 0, 22, 60, INK, anchor="c", face="Lora"); cr.restore()
    if k2 > 0: push(cr, 540, 390, k2, .03); rrect(cr, -380, -64, 760, 128, 26, RED); text(cr, "JEETE TOH BAWAAL", 0, 22, 60, WHITE, anchor="c", face="Lora"); cr.restore()

def qsign(cr, x, y, s, col=TRI, a=1.0):
    line(cr, x, y, x, y + s * 1.2, s * .08, C("7F5539"), a); rrect(cr, x - s * .55, y - s * .55, s * 1.1, s * .9, s * .12, WHITE, a)
    text(cr, "?", x, y + s * .2, s * .8, col, a, anchor="c", face="Lora")

def s_hook(cr, lt, d, t):
    bg(cr, C("1E1B4B"), C("4C1D95")); rays(cr, 540, 860, t, YEL, .1)
    catch(cr, lt, -0.4)
    P = 2.2; ph = (t % P) / P; lost = ph < .5
    if lost:
        o = sash(neta(cr, 380, 1180, 430, t, mouth="o", arms=dict(ra=150, ra2=10)), cr, SAFF); rx, ry = o["rh"]; qsign(cr, rx + 10, ry - 170, 150, SAFF)
        evm(cr, 800, 930, 300, t, "worried", sweat=1)
    else:
        sash(neta(cr, 760, 1180, 430, t, mouth="frown", arms=dict(la=90, la2=-20)), cr, SAFF)
        o = sash(neta(cr, 250, 1180, 360, t + 1, mouth="o", arms=dict(ra=150, ra2=10)), cr, TRI); rx, ry = o["rh"]; qsign(cr, rx + 10, ry - 150, 130, TRI)
        pill(cr, 600, 720, "ANARCHY!", 60, RED, WHITE, 1.0, .08)

def s_2010(cr, lt, d, t):
    bg(cr, C("FFF7ED"), C("FED7AA"))
    pill(cr, 540, 230, "2010", 90, INK, WHITE, back((lt - .05) / .25), -.04)
    push(cr, 330, 720, back((lt - .2) / .3), -.06)
    rrect(cr, -190, -260, 380, 520, 16, SAFF); rrect(cr, -190, -260, 40, 520, 12, C("C2410C"))
    text(cr, "DEMOCRACY", 20, -150, 48, WHITE, anchor="c", face="Lora"); text(cr, "AT RISK!", 20, -90, 56, WHITE, anchor="c", face="Lora")
    evm(cr, 20, 90, 150, t, "worried", sweat=1); cr.restore()
    sash(neta(cr, 790, 1180, 380, t, mouth="o", arms=dict(la=60, la2=-90)), cr, SAFF)
    k = back((lt - d * .45) / .25)
    if k > 0:
        push(cr, 700, 470, k, .04); rrect(cr, -320, -110, 640, 220, 30, WHITE)
        text(cr, "“CANNOT BE", 0, -25, 54, INK, anchor="c", face="Lora"); text(cr, "TRUSTED FULLY”", 0, 40, 54, RED, anchor="c", face="Lora")
        text(cr, "BJP president, 2010", 0, 92, 26, MUTED, anchor="c"); cr.restore()

def s_quiet(cr, lt, d, t):
    bg(cr, C("ECFDF5"), C("A7F3D0"))
    o = sash(neta(cr, 540, 1180, 460, t, mouth="smile", arms=dict(ra=165, la=165)), cr, SAFF)
    hx, hy = o["head"]
    for i in range(6):
        ph = (t * .7 + i / 6) % 1; circle(cr, 140 + (i * 151) % 800, 300 + ph * 700, 10, [SAFF, GREEN, YEL][i % 3], 1 - ph)
    rrect(cr, hx - 34, hy + 16, 68, 14, 7, INK)
    for i in range(5): line(cr, hx - 28 + i * 14, hy + 12, hx - 28 + i * 14, hy + 34, 3, C("94A3B8"))
    bx = 880; rrect(cr, bx - 70, 1000, 140, 180, 14, C("64748B")); rrect(cr, bx - 80, 985, 160, 26, 10, C("475569"))
    k = ease((lt - .3) / .8); y = 600 + 420 * k
    push(cr, bx - 140 * (1 - k), y, 1, k * 2.5); rrect(cr, -50, -70, 100, 140, 8, SAFF); cr.restore()
    pill(cr, 540, 300, "2014+: WIN, WIN, WIN", 56, INK, WHITE, back((lt - .1) / .25), -.03)
    pill(cr, 300, 520, "QUESTIONS?", 50, WHITE, INK, back((lt - d * .5) / .25), .05)

def s_2026(cr, lt, d, t):
    bg(cr, C("0F172A"), C("1E293B"))
    pill(cr, 540, 230, "BENGAL, 2026", 70, WHITE, INK, back((lt - .05) / .25), .03)
    v = int(9100000 * ease((lt - .2) / (d * .55)))
    lakh = v / 100000
    push(cr, 540, 440, 1 + .03 * math.sin(t * 8)); rrect(cr, -360, -90, 720, 180, 40, RED); text(cr, f"{lakh:,.0f} LAKH", 0, 40, 110, WHITE, anchor="c", face="Lora"); cr.restore()
    text(cr, "NAMES REMOVED", 540, 600, 50, WHITE, anchor="c")
    for r in range(4):
        for c in range(10):
            x = 140 + c * 90; y = 720 + r * 90; gone = (r * 10 + c) % 9 == 0 or (r * 10 + c) < int(40 * min(1, lt / d) * .12)
            circle(cr, x, y - 18, 16, C("475569") if gone else SKIN2, .4 if gone else 1)
            rrect(cr, x - 20, y, 40, 34, 12, C("475569") if gone else C("60A5FA"), .4 if gone else 1)
            if gone: cross(cr, x, y, 40, RED, 1)

def s_label(cr, lt, d, t):
    bg(cr, C("FEF3C7"), C("FCD34D")); rays(cr, 540, 720, t, WHITE, .1)
    o = sash(neta(cr, 230, 1180, 380, t, mouth="o", arms=dict(ra=150, ra2=10)), cr, TRI); rx, ry = o["rh"]; qsign(cr, rx + 10, ry - 160, 140, TRI)
    sash(neta(cr, 820, 1180, 400, t + 1, mouth="frown", arms=dict(la=165, ra=165)), cr, SAFF)
    k = back((lt - .2) / .25)
    if k > 0:
        push(cr, 820, 560, k, .05); line(cr, -170, 140, -170, 260, 8, C("7F5539")); line(cr, 170, 140, 170, 260, 8, C("7F5539"))
        rrect(cr, -260, -150, 520, 300, 18, WHITE); rr_path(cr, -260, -150, 520, 300, 18); cr.set_line_width(8); src(cr, SAFF); cr.stroke()
        text(cr, "LOKTANTRA BACHAO", 0, -40, 40, INK, anchor="c", face="Lora"); text(cr, "ARAJAKTA HATAO", 0, 40, 48, RED, anchor="c", face="Lora"); cr.restore()
    k2 = back((lt - d * .55) / .25)
    if k2 > 0: pill(cr, 540, 260, "SAME QUESTION. NEW LABEL.", 52, INK, WHITE, k2, -.03)

def s_end(cr, lt, d, t):
    bg(cr, C("B91C1C"), C("450A0A")); rays(cr, 540, 800, t, YEL, .12)
    catch(cr, lt, 0.0)
    for i, (x, lbl, col) in enumerate([(300, "2010", C("22C55E")), (780, "2026", RED)]):
        k = back((lt - .5 - i * .3) / .25)
        if k > 0:
            push(cr, x, 820, k); qsign(cr, 0, -120, 200, SAFF if i == 0 else TRI)
            pill(cr, 0, 200, "PATRIOTIC" if i == 0 else "ANARCHY", 48, col, WHITE, 1.0, 0); text(cr, lbl, 0, 300, 40, WHITE, anchor="c"); cr.restore()

BEATS = [
    dict(say="Lose, and asking questions is patriotic. Win, and asking questions is anarchy.", cap="Lose? Questions are *patriotic*. Win? Questions are *anarchy*.", scene=s_hook),
    dict(say="2010. Out of power, the BJP releases a whole book doubting voting machines. Its own party president said they cannot be trusted fully.", cap="*2010.* Out of power, BJP releases a book *doubting voting machines*. Its president: *“cannot be trusted fully.”*", scene=s_2010),
    dict(say="Then they started winning. And the questions went very, very quiet.", cap="Then they started *winning*. And the questions went *very quiet*.", scene=s_quiet),
    dict(say="2026. Bengal's voter list loses nearly ninety one lakh names.", cap="*2026.* Bengal's voter list loses *nearly 91 lakh names*.", scene=s_2026),
    dict(say="The opposition asks questions. The BJP marches against anarchy. Same question. New label.", cap="The opposition asks. BJP marches against *“anarchy.”* Same question, *new label*.", scene=s_label),
    dict(say="Haare toh sawaal. Jeete toh bawaal. Comment below: sawaal, ya bawaal?", cap="Comment below: *sawaal* ya *bawaal*?", scene=s_end, hold=0.6),
]

if __name__ == "__main__":
    f = Film("31_sawaal_bawaal", BEATS, voice=("af_heart", 1.1, "en-us"))
    if "--stills" in sys.argv:
        from PIL import Image
        ts = [0.0, 1.5]
        for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
        ims = []
        for n, tt in enumerate(ts):
            p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
        s = Image.new("RGB", (270 * len(ims), 480)); [s.paste(im, (n * 270, 0)) for n, im in enumerate(ims)]; s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])
    else: f.render()
