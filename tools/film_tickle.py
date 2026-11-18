"""Film 21: why you can't tickle yourself. Full-screen motion style, English voice, challenge hook."""
import sys, math
from kit2 import *
from motion import Film, W, H
from film_voice import bg, rays, face, pill, bars

def hand(cr, x, y, s, t, rot=0.0, wig=1.0, col=SKIN):
    u = s / 100
    push(cr, x, y, 1, rot)
    rrect(cr, -150 * u, -46 * u, 160 * u, 92 * u, 30 * u, col)
    rrect(cr, -60 * u, -66 * u, 120 * u, 132 * u, 44 * u, col)
    for i, dy in enumerate((-48, -16, 16, 48)):
        a = math.sin(t * 16 + i * 1.3) * .35 * wig
        cr.save(); cr.translate(50 * u, dy * u); cr.rotate(a); rrect(cr, 0, -13 * u, 82 * u, 26 * u, 13 * u, col); circle(cr, 74 * u, 0, 9 * u, C("F5C9AE")); cr.restore()
    cr.save(); cr.translate(-10 * u, -64 * u); cr.rotate(-.9 + math.sin(t * 12) * .2 * wig); rrect(cr, 0, -12 * u, 62 * u, 24 * u, 12 * u, col); cr.restore()
    cr.restore()

def meter(cr, x, y, v, lbl="TICKLE"):
    rrect(cr, x - 300, y - 46, 600, 92, 46, INK, .85)
    col = lerpc(C("6C757D"), C("FF006E"), min(1, v))
    rrect(cr, x - 288, y - 34, max(68, 576 * min(1, v)), 68, 34, col)
    text(cr, f"{lbl} {int(v * 100)}%", x, y + 16, 44, WHITE, anchor="c")

def t_hook(cr, lt, d, t):
    bg(cr, C("FF006E"), C("FB5607")); rays(cr, 540, 760, t, WHITE, .12)
    for i in range(4):
        ph = (t * 1.5 + i / 4) % 1; ring(cr, 540, 760, 220 + ph * 520, 14 * (1 - ph) + 2, WHITE, .45 * (1 - ph))
    face(cr, 540, 760, 240, t, "smile", look=.8)
    hx = 980 - 230 * ease(lt / (d * .9)); hand(cr, hx, 900, 150, t, rot=math.pi + .2)
    pill(cr, 540, 330, "RIGHT NOW", 70, YEL, INK, back((lt - .1) / .25) * (1 + .05 * math.sin(t * 9)), -.05)

def t_fail(cr, lt, d, t):
    bg(cr, C("495057"), C("212529"))
    face(cr, 540, 660, 240, t, "smile" if lt < .3 else "flat")
    hand(cr, 800 + math.sin(t * 6) * 20, 760, 140, t, rot=math.pi + .3)
    meter(cr, 540, 1080, .03 + .02 * abs(math.sin(t * 3)))
    for i in range(3):
        ph = (t * .6 + i / 3) % 1; text(cr, ".", 300 + i * 40, 360 - ph * 10, 120, WHITE, .5, face="Lora")
    k = back((lt - d * .45) / .25)
    if k > 0: pill(cr, 540, 330, "NOTHING", 80, WHITE, INK, k, .06)

def _brain(cr, x, y, r, t, hot=0.0):
    u = r / 100
    for dx, dy, rr in [(-55, -20, 52), (-20, -52, 55), (30, -50, 55), (62, -12, 50), (-45, 30, 48), (5, 0, 66)]:
        circle(cr, x + dx * u, y + dy * u, rr * u, C("F4A6B8"))
    cx, cy = x + 52 * u, y + 52 * u
    glow(cr, cx, cy, 90 * u, YEL, .5 * hot)
    circle(cr, cx, cy, 40 * u, lerpc(C("E07A95"), YEL, hot))
    for i in range(4): line(cr, cx - 28 * u, cy - 18 * u + i * 12 * u, cx + 28 * u, cy - 18 * u + i * 12 * u, 4 * u, C("C9184A"), .6)

def t_predict(cr, lt, d, t):
    bg(cr, C("10002B"), C("3C096C"))
    hot = .6 + .4 * math.sin(t * 8)
    _brain(cr, 540, 470, 230, t, hot)
    pill(cr, 760, 230, "CEREBELLUM", 48, YEL, INK, back((lt - .2) / .25), .06)
    # predicted path (dashed) and the hand following it
    pts = [(160 + i * 26, 980 - math.sin(i / 3) * 70) for i in range(30)]
    polyline(cr, pts, 8, YEL, .5, dash=[16, 16])
    p = min(1, lt / (d * .8)); n = max(2, int(len(pts) * p)); hx, hy = pts[n - 1]
    hand(cr, hx, hy, 90, t, rot=0)
    # incoming signal wave being cancelled
    k = ease((lt - d * .45) / .3)
    wav = [(200 + i * 22, 1180 + math.sin(i * .8 + t * 8) * 60 * (1 - k)) for i in range(32)]
    polyline(cr, wav, 10, C("FF006E"))
    if k > 0:
        push(cr, 540, 1180, back((lt - d * .45) / .25)); circle(cr, 0, 0, 120, RED, .25); line(cr, -90, -90, 90, 90, 18, RED); line(cr, 90, -90, -90, 90, 18, RED); cr.restore()

def t_other(cr, lt, d, t):
    bg(cr, C("FFBE0B"), C("FF006E")); rays(cr, 540, 700, t * 1.5, WHITE, .14)
    sh = math.sin(t * 40) * 10
    face(cr, 540 + sh, 700, 250, t, "shock" if lt < d * .3 else "smile", talk=abs(math.sin(t * 14)))
    hand(cr, 140 + math.sin(t * 9) * 30, 860, 150, t, rot=-.2, wig=1.8, col=SKIN2)
    hand(cr, 960 - math.sin(t * 8) * 30, 820, 150, t + .5, rot=math.pi + .2, wig=1.8, col=SKIN2)
    v = min(1, ease((lt - .2) / (d * .5)))
    meter(cr, 540, 1080, v)
    for i, (x, y, w) in enumerate([(220, 340, "HA"), (800, 300, "HAHA"), (540, 220, "HA")]):
        k = back((lt - d * .35 - i * .15) / .2)
        if k > 0: push(cr, x, y + math.sin(t * 7 + i) * 12, k, (i - 1) * .15); text(cr, w, 0, 0, 100, WHITE, anchor="c", face="Lora"); cr.restore()

def t_robot(cr, lt, d, t):
    bg(cr, C("023E8A"), C("03045E"))
    rrect(cr, 380, 230, 320, 260, 50, C("ADB5BD")); rrect(cr, 420, 280, 240, 120, 30, INK)
    for sx in (-1, 1): circle(cr, 540 + sx * 60, 340, 26, C("4CC9F0") if int(t * 3) % 4 else INK)
    line(cr, 540, 230, 540, 170, 10, C("ADB5BD")); circle(cr, 540, 160, 18, RED, .5 + .5 * (math.sin(t * 8) > 0))
    rrect(cr, 450, 430, 180, 30, 10, C("6C757D"))
    line(cr, 700, 380, 860, 560, 26, C("ADB5BD")); line(cr, 860, 560, 780, 760, 26, C("ADB5BD"))
    hand(cr, 760, 820, 110, t, rot=math.pi * .6, col=C("ADB5BD"))
    pill(cr, 270, 600, "+0.2 sec", 58, YEL, INK, back((lt - .3) / .25), -.06)
    face(cr, 470, 930, 160, t, "smile" if lt > d * .5 else "flat", talk=abs(math.sin(t * 12)) if lt > d * .5 else 0, look=.8)
    meter(cr, 540, 1140, min(.55, .05 + .5 * ease((lt - d * .45) / .4)))

def t_end(cr, lt, d, t):
    bg(cr, C("8338EC"), C("3A0CA3")); rays(cr, 540, 650, t, WHITE, .1)
    face(cr, 330, 650, 170, t, "smile", look=.8)
    face(cr, 760, 650, 170, t + 1, "shock", SKIN2, C("3B2314"), "long")
    hand(cr, 560, 820, 110, t, rot=0, wig=1.5)
    for i in range(6):
        ph = (t * .45 + i / 6) % 1; heart(cr, 150 + (i * 167) % 800, 1200 - ph * 1000, .6 * (1 - ph * .4), WHITE if i % 2 else PINK, .9 * (1 - ph))
    pill(cr, 540, 330, "TRY IT", 80, YEL, INK, back((lt - .2) / .25) * (1 + .06 * math.sin(t * 8)), .05)

BEATS = [
    dict(say="Try to tickle yourself. Right now.", cap="*Try to tickle yourself.* Right now.", scene=t_hook),
    dict(say="Nothing, right?", cap="*Nothing*, right?", scene=t_fail, hold=0.4),
    dict(say="Your cerebellum predicts your own touch, and cancels the feeling before it lands.", cap="Your *cerebellum* predicts your own touch, and *cancels* the feeling before it lands.", scene=t_predict),
    dict(say="Someone else's hand? Your brain can't predict it. So you lose it.", cap="Someone else's hand? Your brain *can't predict it*. So you *lose it*.", scene=t_other),
    dict(say="Scientists added a tiny robot delay to people's own touch, and it got more ticklish.", cap="Scientists added a tiny *robot delay* to people's own touch, and it got *more ticklish*.", scene=t_robot),
    dict(say="Send this to someone and watch them try.", cap="Send this to someone and *watch them try*.", scene=t_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("21_tickle", BEATS, voice=("af_heart", 1.1, "en-us"))
    if "--stills" in sys.argv:
        from PIL import Image
        ts = [0.0, 1.0]
        for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
        ims = []
        for n, tt in enumerate(ts):
            p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
        s = Image.new("RGB", (270 * len(ims), 480)); [s.paste(im, (n * 270, 0)) for n, im in enumerate(ims)]; s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])
    else: f.render()
