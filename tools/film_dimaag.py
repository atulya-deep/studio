"""Film 20 (Hinglish roast, strong language): your brain is 2% of your body but burns 20% of its energy."""
import sys, math
from kit2 import *
from scenes4 import _phone
from motion import Film, W, H
from film_voice import bg, rays, face, pill, bars

BR = C("F4A6B8"); BR2 = C("E07A95")

def brain(cr, x, y, r, t, mood="smug", a=1.0):
    u = r / 100; wob = math.sin(t * 6) * 3 * u
    for dx, dy, rr in [(-55, -20, 52), (-20, -52, 55), (30, -50, 55), (62, -12, 50), (55, 35, 46), (10, 48, 50), (-45, 35, 48), (0, 0, 70)]:
        circle(cr, x + dx * u, y + dy * u + wob, rr * u, BR, a)
    for pts in ([(-70, -10), (-45, -30), (-25, -8), (-48, 14)], [(20, -80), (38, -50), (15, -32), (40, -10)], [(60, 20), (36, 34), (58, 56)], [(-30, 60), (-10, 40), (-34, 26)], [(0, -90), (-6, -50), (6, -10), (-4, 30), (4, 78)]):
        polyline(cr, [(x + px * u, y + py * u + wob) for px, py in pts], 7 * u, BR2, a)
    ey = y - 4 * u + wob
    for sx in (-1, 1):
        circle(cr, x + sx * 30 * u, ey, 17 * u, WHITE, a); circle(cr, x + sx * 30 * u + (4 * u if mood != "heart" else 0), ey + 2 * u, 9 * u, INK, a)
        if mood == "smug": line(cr, x + sx * 30 * u - 20 * u, ey - 24 * u, x + sx * 30 * u + 20 * u, ey - 30 * u + sx * 8 * u, 7 * u, INK, a)
        if mood == "heart": heart(cr, x + sx * 30 * u, ey + 2 * u, .3 * u * (1 + .15 * math.sin(t * 10)), RED, a)
    if mood == "eat": ell(cr, x, y + 42 * u + wob, 30 * u, (14 + 16 * abs(math.sin(t * 12))) * u, C("5A1F2B"), a)
    elif mood == "dead":
        line(cr, x - 22 * u, y + 44 * u + wob, x + 22 * u, y + 44 * u + wob, 7 * u, INK, a)
    else:
        cr.new_path(); cr.arc(x, y + 30 * u + wob, 30 * u, .3, math.pi - .3); cr.set_line_width(7 * u); cr.set_line_cap(cairo.LINE_CAP_ROUND); src(cr, INK, a); cr.stroke()

def bolt(cr, x, y, s, col=YEL, a=1.0, rot=0.0):
    push(cr, x, y, s, rot); poly(cr, [(10, -50), (-28, 8), (-4, 8), (-14, 50), (30, -12), (4, -12)], col, a); cr.restore()

def d_hook(cr, lt, d, t):
    bg(cr, C("D00000"), C("370617")); rays(cr, 540, 600, t, YEL, .1)
    sh = math.sin(t * 50) * 10 * max(0, 1 - lt * 1.2)
    rrect(cr, 240, 860, 600, 300, 50, C("E9ECEF")); rrect(cr, 200, 800, 680, 90, 40, C("ADB5BD"))
    rrect(cr, 360, 940, 360, 150, 24, INK); text(cr, "1.4 KG", 540, 1048, 104, C("70E000"), anchor="c", face="Lora")
    by = 560 + abs(math.sin(t * 5)) * -40
    ell(cr, 540, 800, 220 - (560 - by) * .6, 26, INK, .25)
    brain(cr, 540 + sh, by, 250, t, "smug")

def d_pct(cr, lt, d, t):
    bg(cr, C("03071E"), C("1B263B"))
    o = person(cr, 250, 1160, 760, shirt=C("4F7DD9"), pose=dict(mouth="flat", look=1, blink=(t % 2.6) < .12)); hx, hy = o["head"]
    ring(cr, hx, hy - 30, 120 + math.sin(t * 6) * 10, 12, YEL, .9, 0, 2 * math.pi)
    pill(cr, 250, 180, "2%", 96, YEL, INK, back((lt - .15) / .25), -.06, "Lora")
    brain(cr, 780, 520, 190, t, "eat")
    for i in range(6):
        ph = (t * 1.3 + i / 6) % 1; x = 260 + (760 - 260) * ph; y = 1000 - (1000 - 560) * ph - math.sin(ph * math.pi) * 120
        bolt(cr, x, y, 1.1 * (1 - ph * .5), YEL, 1, ph * 3)
    k = lt - d * .5
    if k > 0:
        s = 1 + 1.5 * (1 - ease(k / .2))
        push(cr, 780, 900, s, .06); rrect(cr, -200, -100, 400, 200, 40, RED); text(cr, "20%", 0, 52, 150, WHITE, anchor="c", face="Lora"); cr.restore()
        text(cr, "ENERGY", 780, 1070, 56, YEL, min(1, k * 4), anchor="c")

def d_bulb(cr, lt, d, t):
    bg(cr, C("240046"), C("10002B"))
    gl = .6 + .4 * math.sin(t * 7)
    glow(cr, 540, 420, 420, YEL, .45 * gl)
    line(cr, 540, 0, 540, 240, 8, C("ADB5BD")); rrect(cr, 490, 230, 100, 70, 14, C("6C757D"))
    circle(cr, 540, 420, 150, YEL); circle(cr, 500, 380, 40, WHITE, .5); text(cr, "20W", 540, 452, 84, INK, anchor="c", face="Lora")
    for i in range(10):
        a0 = i * math.pi / 5 + t * .6; line(cr, 540 + math.cos(a0) * 190, 420 + math.sin(a0) * 190, 540 + math.cos(a0) * (240 + 30 * gl), 420 + math.sin(a0) * (240 + 30 * gl), 12, YEL, .8)
    rrect(cr, 120, 900, 840, 220, 60, C("7B2CBF")); rrect(cr, 80, 820, 130, 300, 50, C("5A189A")); rrect(cr, 870, 820, 130, 300, 50, C("5A189A")); rrect(cr, 150, 1100, 780, 60, 20, C("3C096C"))
    push(cr, 600, 900, 1, -math.pi / 2 + .04 * math.sin(t * 2)); person(cr, 0, 0, 560, shirt=C("4F7DD9"), pose=dict(blink=True, mouth="smile", la=20, ra=20)); cr.restore()
    for i in range(3):
        ph = (t * .5 + i / 3) % 1; text(cr, "Z", 300 + ph * 120 + i * 20, 760 - ph * 200, 70 + i * 20, WHITE, 1 - ph, face="Lora")

def d_keys(cr, lt, d, t):
    bg(cr, C("005F73"), C("001219"))
    face(cr, 540, 860, 230, t, "shock", look=math.sin(t * 4))
    for i, (dx, s, ph) in enumerate([(0, 230, 0), (-260, 130, 1), (270, 150, 2)]):
        text(cr, "?", 540 + dx, 520 - (40 if i else 0) + math.sin(t * 5 + ph) * 16, s, YEL, min(1, max(0, (lt - i * .2) * 5)), face="Lora", anchor="c")
    q = (t * .45) % 1; kx = 200 + q * 760; ky = 330 - math.sin(q * math.pi) * 150; a = 1 - q * .6
    push(cr, kx, ky, 1.2, t * 3); ring(cr, 0, -40, 34, 14, GOLD, a); rrect(cr, -8, -10, 16, 90, 6, GOLD, a); rrect(cr, 8, 40, 26, 14, 4, GOLD, a); rrect(cr, 8, 62, 18, 14, 4, GOLD, a); cr.restore()
    for sx in (-1, 1): ell(cr, kx - 60 * sx, ky - 20, 34, 14, WHITE, a * .9, rot=sx * (.5 + .4 * math.sin(t * 25)))
    for i in range(4):
        ph = (t * .7 + i / 4) % 1; circle(cr, 540 + (i - 1.5) * 60, 620 - ph * 160, 26 + ph * 30, C("ADB5BD"), .5 * (1 - ph))

def d_ex(cr, lt, d, t):
    bg(cr, C("FF006E"), C("8338EC")); rays(cr, 540, 600, t, WHITE, .08)
    push(cr, 400, 640, 1, -.08 + math.sin(t * 3) * .03); _phone(cr, 0, 0, 800, screen=C("12121C"))
    circle(cr, 0, -220, 70, C("FF006E")); text(cr, "EX", 0, -196, 64, WHITE, anchor="c")
    n = int(max(0, lt - .2) * 9); num = "98765 43210"[:max(0, min(11, n))]
    text(cr, num, 0, -60, 54, C("70E000"), anchor="c")
    for r in range(3):
        for c in range(3):
            on = (r * 3 + c) == int(t * 9) % 9; circle(cr, -100 + c * 100, 60 + r * 95, 36, WHITE if on else C("3A3A4A"))
    cr.restore()
    brain(cr, 830, 420, 170, t, "heart")
    for i in range(5):
        ph = (t * .6 + i / 5) % 1; heart(cr, 720 + (i * 97) % 300, 1100 - ph * 700, .7 * (1 - ph * .4), WHITE, 1 - ph)

def d_end(cr, lt, d, t):
    bg(cr, C("FFBA08"), C("E85D04")); rays(cr, 540, 600, t, WHITE, .12)
    push(cr, 330, 620, 1, -.06 + math.sin(t * 2) * .02); rrect(cr, -230, -330, 460, 660, 24, WHITE)
    text(cr, "BIJLI KA BILL", 0, -250, 46, INK, anchor="c")
    for j in range(4): rrect(cr, -180, -190 + j * 60, 360 - (j % 2) * 90, 22, 11, C("CED4DA"))
    amt = int(20000 * min(1, lt / (d * .6)) ** 2); text(cr, f"Rs {amt:,}", 0, 150, 84, RED, anchor="c", face="Lora")
    bolt(cr, 150, -270, 1.2, YEL); cr.restore()
    brain(cr, 800, 430, 160, t, "dead")
    for i in range(4):
        ph = (t * .8 + i / 4) % 1; circle(cr, 800 + (i - 1.5) * 50, 290 - ph * 170, 24 + ph * 30, C("495057"), .6 * (1 - ph))
    face(cr, 800, 930, 150, t, "smile", SKIN2, C("3B2314"), "short", look=-.6, talk=abs(math.sin(t * 10)))

BEATS = [
    dict(say="अबे चूतिये, तेरा दिमाग डेढ़ किलो का भी नहीं है।", cap="Abe *chutiye*, tera dimaag *dedh kilo* ka bhi nahi hai.", scene=d_hook),
    dict(say="बॉडी का सिर्फ़ दो परसेंट। फिर भी साला बीस परसेंट एनर्जी खा जाता है।", cap="Body ka sirf *2%*. Phir bhi saala *20% energy* kha jaata hai.", scene=d_pct),
    dict(say="तू सोफ़े पे पड़ा रहे, तब भी ये बीस वॉट का बल्ब जलता रहता है।", cap="Tu sofe pe pada rahe, tab bhi ye *20 watt* ka bulb jalta rehta hai.", scene=d_bulb),
    dict(say="इतनी बिजली फूँक के भी, तू चाबी कहाँ रखी भूल जाता है, गधे।", cap="Itni bijli phoonk ke bhi tu *chaabi* kahan rakhi bhool jaata hai, *gadhe*.", scene=d_keys),
    dict(say="और एक्स का नंबर? वो साला आज भी याद है।", cap="Aur *ex ka number*? Wo saala aaj bhi *yaad* hai.", scene=d_ex),
    dict(say="उस बकचोद दोस्त को भेज, जिसका दिमाग बस बिजली का बिल बढ़ाता है।", cap="Us *bakchod* dost ko bhej jiska dimaag bas *bijli ka bill* badhata hai.", scene=d_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("20_dimaag", BEATS, voice=("piper:rohan", 1.08, "hi"))
    if "--stills" in sys.argv:
        from PIL import Image
        ts = [0.0, 1.5]
        for b in f.b[1:]: ts += [b["t0"] + b["d"] * .45, b["t0"] + b["d"] * .92]
        ims = []
        for n, tt in enumerate(ts):
            p = f"{f.out}/st{n}.png"; f.still(tt, p); ims.append(Image.open(p).resize((270, 480)))
        s = Image.new("RGB", (270 * len(ims), 480)); [s.paste(im, (n * 270, 0)) for n, im in enumerate(ims)]; s.save(f"{f.out}/sheet.png"); print(round(f.T, 1), [round(b["d"], 1) for b in f.b])
    else: f.render()
