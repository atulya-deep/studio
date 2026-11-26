"""Film 30: 'Jeete toh janta mahaan, haare toh EVM beimaan' — both sides blame the system when they lose (BJP 2009-10, opposition 2026). Self-serving bias. Roasts both."""
import sys, math
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, pill
from film_aayaram import neta

SAFF = C("F97316"); TRI = C("2563EB")

def sash(o, cr, col):
    hx, hy = o["head"]; u = o["u"]
    line(cr, hx - 13 * u, hy + 16 * u, hx + 13 * u, hy + 50 * u, 7 * u, col)
    return o

def evm(cr, x, y, s, t, mood="calm", sweat=0.0):
    u = s / 100
    rrect(cr, x - 60 * u, y - 90 * u, 120 * u, 180 * u, 14 * u, C("CBD5E1")); rrect(cr, x - 52 * u, y - 82 * u, 104 * u, 164 * u, 10 * u, C("E2E8F0"))
    for i in range(5):
        yy = y - 30 * u + i * 22 * u
        rrect(cr, x - 44 * u, yy - 8 * u, 58 * u, 16 * u, 4 * u, WHITE); circle(cr, x + 30 * u, yy, 7 * u, C("1D4ED8"))
        circle(cr, x + 30 * u, yy, 3 * u, RED if (int(t * 3) % 5 == i) else C("1D4ED8"))
    ey = y - 60 * u; lk = math.sin(t * 3) * 3 * u
    for sx in (-1, 1):
        circle(cr, x + sx * 18 * u, ey, 9 * u, WHITE); circle(cr, x + sx * 18 * u + lk, ey + 1 * u, 4.5 * u, INK)
        if mood == "worried": line(cr, x + sx * 18 * u - 10 * u, ey - 14 * u + sx * 3 * u, x + sx * 18 * u + 10 * u, ey - 12 * u - sx * 3 * u, 3 * u, INK)
    if mood == "worried": ell(cr, x, ey + 18 * u, 8 * u, 6 * u, C("5A1F2B"))
    else:
        cr.new_path(); cr.arc(x, ey + 10 * u, 10 * u, .3, math.pi - .3); cr.set_line_width(3 * u); src(cr, INK); cr.stroke()
    for sx in (-1, 1):
        line(cr, x + sx * 60 * u, y - 10 * u, x + sx * 85 * u, y + 20 * u + math.sin(t * 6 + sx) * 6 * u, 6 * u, C("94A3B8"))
    for i in range(int(3 * sweat)):
        ph = (t * 1.2 + i / 3) % 1; ell(cr, x + 50 * u + i * 8 * u, y - 80 * u + ph * 60 * u, 4 * u, 7 * u, C("60A5FA"), 1 - ph)

def catch(cr, lt, k0=0.0):
    k1 = back((lt - k0) / .25); k2 = back((lt - k0 - .35) / .25)
    if k1 > 0: push(cr, 540, 240, k1, -.03); rrect(cr, -420, -64, 840, 128, 26, GREEN); text(cr, "JEETE TOH JANTA MAHAAN", 0, 22, 56, INK, anchor="c", face="Lora"); cr.restore()
    if k2 > 0: push(cr, 540, 390, k2, .03); rrect(cr, -420, -64, 840, 128, 26, RED); text(cr, "HAARE TOH EVM BEIMAAN", 0, 22, 56, WHITE, anchor="c", face="Lora"); cr.restore()

def e_hook(cr, lt, d, t):
    bg(cr, C("1E1B4B"), C("4C1D95")); rays(cr, 540, 860, t, YEL, .1)
    catch(cr, lt, -0.4)
    P = 2.0; ph = (t % P) / P; won = ph < .5
    o = neta(cr, 300, 1180, 430, t, mouth="smile" if won else "frown", arms=dict(ra=165, la=165) if won else dict(ra=60, ra2=-80)); sash(o, cr, SAFF if int(t / P) % 2 == 0 else TRI)
    if won:
        for i in range(5): heart(cr, 200 + i * 60, 600 - ((t * 120 + i * 40) % 160), .25, PINK)
    else:
        line(cr, 420, 760, 640, 820, 8, RED); poly(cr, [(640, 820), (610, 795), (615, 835)], RED)
    evm(cr, 790, 920, 330, t, "calm" if won else "worried", sweat=0 if won else 1)

def e_2009(cr, lt, d, t):
    bg(cr, C("FFF7ED"), C("FED7AA"))
    pill(cr, 540, 240, "2009", 90, INK, WHITE, back((lt - .05) / .25), -.04)
    o = sash(neta(cr, 320, 1150, 420, t, mouth="frown", face=1), cr, SAFF)
    hx, hy = o["head"]
    for i in range(3):
        ph = (t * .9 + i / 3) % 1; text(cr, "?", hx + 60 + i * 50, hy - 80 - ph * 80, 80 + i * 20, SAFF, 1 - ph, face="Lora")
    evm(cr, 780, 900, 300, t, "worried", sweat=1)
    k = back((lt - d * .5) / .25)
    if k > 0:
        push(cr, 760, 520, k, .06); rrect(cr, -150, -190, 300, 380, 14, SAFF); rrect(cr, -150, -190, 34, 380, 10, C("C2410C"))
        text(cr, "DEMOCRACY", 15, -80, 36, WHITE, anchor="c", face="Lora"); text(cr, "AT RISK!", 15, -30, 44, WHITE, anchor="c", face="Lora")
        evm(cr, 15, 90, 110, t, "worried"); cr.restore()

def e_2026(cr, lt, d, t):
    bg(cr, C("EFF6FF"), C("BFDBFE"))
    pill(cr, 540, 240, "2026", 90, INK, WHITE, back((lt - .05) / .25), .04)
    sash(neta(cr, 760, 1150, 400, t, mouth="smile", arms=dict(ra=165, la=165)), cr, SAFF)
    o = sash(neta(cr, 300, 1150, 420, t + 1, mouth="o", arms=dict(ra=150 + math.sin(t * 9) * 20, ra2=10)), cr, TRI)
    k = back((lt - .3) / .25)
    if k > 0:
        push(cr, 330, 520, k * (1 + .06 * math.sin(t * 10)), -.06); rrect(cr, -230, -70, 460, 140, 70, TRI); text(cr, "VOTE CHORI!", 0, 24, 66, WHITE, anchor="c", face="Lora"); cr.restore()
    for i in range(3):
        ph = (t * 1.1 + i / 3) % 1; text(cr, "♪", 820 + i * 40, 720 - ph * 120, 60, C("16A34A"), 1 - ph)

def e_script(cr, lt, d, t):
    bg(cr, C("111827"), C("1F2937"))
    rrect(cr, 290, 300, 500, 640, 20, C("FEF3C7")); rrect(cr, 290, 300, 500, 110, 20, C("B45309"))
    text(cr, "SCRIPT", 540, 375, 60, WHITE, anchor="c", face="Lora")
    lines = ["1. Lose", "2. Blame machine", "3. Win", "4. Machine is great"]
    for i, s in enumerate(lines):
        text(cr, s, 330, 490 + i * 100, 46, INK, appear(t, .1 + i * .4, .2) if False else min(1, max(0, (lt - .2 - i * .35) * 4)))
    sw = (t % 2.4) < 1.2
    sash(neta(cr, 180, 1180, 300, t, mouth="frown" if sw else "smile"), cr, SAFF)
    sash(neta(cr, 900, 1180, 300, t + 1, mouth="smile" if sw else "frown"), cr, TRI)
    for i, x in enumerate((180, 900)):
        col = SAFF if i == 0 else TRI
        ring(cr, x, 760, 40, 10, col)

def e_bias(cr, lt, d, t):
    bg(cr, C("0F766E"), C("042F2E")); rays(cr, 540, 720, t, C("5EEAD4"), .08)
    pill(cr, 540, 240, "SELF-SERVING BIAS", 66, YEL, INK, back((lt - .05) / .25), -.03)
    for i, (x, lbl, col, sym) in enumerate([(300, "WIN", GREEN, "ME!"), (780, "LOSE", RED, "THEM!")]):
        k = back((lt - .4 - i * .4) / .25)
        if k > 0:
            push(cr, x, 660, k); rrect(cr, -200, -220, 400, 440, 40, WHITE)
            text(cr, lbl, 0, -120, 56, col, anchor="c", face="Lora")
            if i == 0: o = neta(cr, 0, 160, 230, t, mouth="smile", arms=dict(la=30, la2=-120))
            else: evm(cr, 0, 70, 150, t, "worried", sweat=1)
            text(cr, sym, 0, 200, 40, INK, anchor="c"); cr.restore()

def e_end(cr, lt, d, t):
    bg(cr, C("F59E0B"), C("B91C1C")); rays(cr, 540, 800, t, WHITE, .12)
    catch(cr, lt, 0.0)
    evm(cr, 540, 910, 380, t, "calm")
    for sx in (-1, 1): text(cr, "?", 540 + sx * 260, 760 + math.sin(t * 4 + sx) * 20, 120, WHITE, .9, face="Lora", anchor="c")

BEATS = [
    dict(say="Win, and the people are geniuses. Lose, and the machine cheated.", cap="Win? *People are geniuses.* Lose? *The machine cheated.*", scene=e_hook),
    dict(say="2009. The BJP loses, and Advani starts doubting voting machines. A BJP leader even writes a book on it.", cap="*2009.* BJP loses. Advani starts *doubting the machines*. A BJP leader writes *a whole book*.", scene=e_2009),
    dict(say="2026. The BJP is winning, and now the opposition is shouting vote chori.", cap="*2026.* BJP is winning, and now the opposition shouts *vote chori*.", scene=e_2026),
    dict(say="Different decade, same script. Only the loser changed.", cap="Different decade, *same script*. Only *the loser* changed.", scene=e_script, hold=0.7),
    dict(say="Psychologists call it self-serving bias. My win? Skill. My loss? Someone else's fault.", cap="It's *self-serving bias*. My win? *Skill.* My loss? *Someone else's fault.*", scene=e_bias),
    dict(say="So remember. Jeete toh janta mahaan. Haare toh E V M beimaan. Tag a friend who always blames the referee.", cap="Tag a friend who *always blames the referee*.", scene=e_end, hold=0.6),
]

if __name__ == "__main__":
    f = Film("30_evm_beimaan", BEATS, voice=("af_heart", 1.1, "en-us"))
    if "--stills" in sys.argv:
        from PIL import Image
        ts = [0.0, 1.5]
        for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
        ims = []
        for n, tt in enumerate(ts):
            p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
        s = Image.new("RGB", (270 * len(ims), 480)); [s.paste(im, (n * 270, 0)) for n, im in enumerate(ims)]; s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])
    else: f.render()
