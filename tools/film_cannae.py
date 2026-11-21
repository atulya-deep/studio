"""Film 24: Hannibal's trap at Cannae, 216 BC (Polybius, Livy; Britannica). Motion style."""
import sys, math
from kit2 import *
from scenes import walk_pose
from motion import Film, W, H
from film_voice import bg, rays, pill
from film_peak import sheet

GAUL = C("FF9F1C"); AFR = C("5A189A"); CAV = C("FFD23F"); ROM = C("D62828"); FIELD1 = C("A7C957"); FIELD2 = C("6A994E")

def lerp(a, b, k): return a + (b - a) * k

def field(cr, t):
    bg(cr, FIELD1, FIELD2)
    for i in range(14):
        x = (i * 173) % 1080; y = 260 + (i * 311) % 1000
        line(cr, x, y, x + 10, y - 22, 5, C("386641"), .35); line(cr, x + 14, y, x + 18, y - 18, 5, C("386641"), .35)
    # river Aufidus along the left edge
    pts = [(40 + 30 * math.sin(i * .5 + t * .4), 200 + i * 60) for i in range(18)]
    polyline(cr, pts, 46, C("4CC9F0"), .7)

def unit(cr, x, y, col, s=34):
    rrect(cr, x - s / 2, y - s / 2, s, s, 8, col); rrect(cr, x - s / 2, y - s / 2, s, s * .3, 6, WHITE, .25)

def roman_block(cr, cx, cy, squeeze=0.0, t=0, shake=0.0):
    cols, rows = 13, 6
    w = lerp(560, 400, squeeze); h = lerp(230, 300, squeeze)
    for r in range(rows):
        for c in range(cols):
            x = cx - w / 2 + c * w / (cols - 1) + math.sin(t * 30 + r + c) * shake
            y = cy - h / 2 + r * h / (rows - 1) + math.cos(t * 27 + r * c) * shake
            unit(cr, x, y, ROM, 30)

def centre(cr, cx, cy, bulge, n=11, span=440):
    """bulge > 0 = convex toward the Romans (up)."""
    for i in range(n):
        u = i / (n - 1) * 2 - 1; x = cx + u * span / 2; y = cy - bulge * (1 - u * u)
        for r in range(2): unit(cr, x, y + r * 40, GAUL, 34)

def africans(cr, side, x, y, k_turn=0.0):
    for r in range(5):
        for c in range(2):
            unit(cr, x + side * c * 40, y + r * 44 - 80, AFR, 34)
    if k_turn > 0:  # arrow showing the inward turn
        push(cr, x + side * 20, y - 150, k_turn); poly(cr, [(-side * 60, 0), (0, -26), (0, 26)], WHITE, .9); cr.restore()

def cavalry(cr, x, y, ang, n=4):
    for i in range(n):
        push(cr, x + math.cos(ang + math.pi / 2) * (i - n / 2) * 46, y + math.sin(ang + math.pi / 2) * (i - n / 2) * 46, 1, ang)
        poly(cr, [(24, 0), (-18, -18), (-18, 18)], CAV); cr.restore()

def legend(cr, k):
    if k <= 0: return
    push(cr, 540, 1165, k)
    rrect(cr, -420, -40, 840, 80, 40, INK, .75)
    for i, (c, s) in enumerate([(ROM, "ROME"), (GAUL, "CENTRE"), (AFR, "VETERANS"), (CAV, "CAVALRY")]):
        x = -380 + i * 205; rrect(cr, x, -14, 28, 28, 6, c); text(cr, s, x + 40, 12, 28, WHITE)
    cr.restore()

def battle(cr, lt, d, t, p0, p1, hi=None):
    """interpolate the whole battle state between phases p0 -> p1 over the beat"""
    p = lerp(p0, p1, ease(lt / (d * .85)))
    field(cr, t)
    # 0->1: Romans advance, centre flattens; 1->2: Romans push in, centre bends back into a cup; 2->3: flanks + cavalry close
    k1 = min(1, max(0, p)); k2 = min(1, max(0, p - 1)); k3 = min(1, max(0, p - 2))
    ry = 430 + 100 * k1 + 120 * k2 + 40 * k3
    bulge = 120 - 120 * k1 - 150 * k2
    cy = 930
    roman_block(cr, 540, ry, squeeze=min(1, max(0, p - 2)), t=t, shake=4 * min(1, max(0, p - 2)))
    centre(cr, 540, cy, bulge)
    ax = lerp(170, 290, k3); ay = lerp(900, 700, k3)
    africans(cr, 1, ax, ay); africans(cr, -1, 1080 - ax, ay)
    # cavalry: starts on the wings, ends sweeping behind (above) the Roman block
    cx0 = lerp(140, 540, k3); cyv = lerp(1050, 420, k3)
    cavalry(cr, 1080 - cx0 if k3 < 1 else 400, cyv, lerp(-math.pi / 2, math.pi / 2, k3), 3)
    cavalry(cr, cx0 if k3 < 1 else 680, cyv, lerp(-math.pi / 2, math.pi / 2, k3), 3)
    legend(cr, 1)
    return p

# ---------- scenes ----------
def c_hook(cr, lt, d, t):
    bg(cr, C("E85D04"), C("6A040F")); rays(cr, 540, 760, t, WHITE, .1)
    rrect(cr, -50, 1100, 1180, 400, 0, C("9C6644"))
    back_x = -60 * lt
    for i in range(3):
        carthage(cr, 300 + back_x - i * 120 + (i % 2) * 30, 1100 - (i % 2) * 20, 330, **dict(walk_pose(t + i, 9), look=1, sword=True, ra=120, ra2=20, mouth="smile"))
    for i in range(3):
        roman(cr, 760 + back_x * 1.3 + i * 120 - (i % 2) * 30, 1100 - (i % 2) * 20, 330, **dict(walk_pose(t + i * .6, 11), look=-1, spear=False, sword=True, ra=110, ra2=30, mouth="o"))
    for i in range(3):
        ph = (t * 1.2 + i / 3) % 1; ell(cr, 600 + i * 120 - ph * 80, 1100 - ph * 30, 40 * (1 - ph) + 10, 14, C("D9B38C"), .6 * (1 - ph))
    pill(cr, 300, 380, "RETREAT?", 66, WHITE, INK, 1 + .05 * math.sin(t * 9), -.06)
    pill(cr, 760, 270, "TRAP", 80, YEL, INK, 1 + .06 * math.sin(t * 8 + 1), .06)
    for i in range(3): poly(cr, [(180 - i * 60 + (t * 120) % 60 * 0, 560), (230 - i * 60, 530), (230 - i * 60, 590)], WHITE, .5)

def c_armies(cr, lt, d, t):
    bg(cr, C("1B263B"), C("0D1B2A"))
    pill(cr, 540, 250, "CANNAE · 216 BC", 60, YEL, INK, back((lt - .05) / .25))
    k1 = ease((lt - .1) / (d * .45)); k2 = ease((lt - d * .45) / (d * .4))
    # Roman crowd: 16 icons, Carthage: 10 icons (each ~5,000 men)
    for i in range(16):
        if i / 16 <= k1: roman(cr, 150 + (i % 8) * 110, 620 + (i // 8) * 120, 130, look=1, mouth="smile", blink=(t + i) % 3 < .1)
    v1 = int(80000 * k1)
    if k1 > 0: text(cr, f"ROME ~{v1:,}", 540, 790, 64, C("FF6B6B"), anchor="c")
    for i in range(10):
        if i / 10 <= k2: carthage(cr, 260 + (i % 5) * 140, 990 + (i // 5) * 110, 120, look=-1, mouth="smile")
    v2 = int(50000 * k2)
    if k2 > 0: text(cr, f"HANNIBAL ~{v2:,}", 540, 1150, 64, C("C77DFF"), anchor="c")

def c_bulge(cr, lt, d, t):
    battle(cr, lt, d, t, 0.0, 0.45)
    pill(cr, 540, 250, "BULGE OUT", 60, YEL, INK, back((lt - .1) / .25), -.04)

def c_push(cr, lt, d, t):
    battle(cr, lt, d, t, 0.45, 2.0)
    k = ease((lt - .1) / .4)
    for i in range(3):
        y0 = 560 + 120 * ease(lt / (d * .85))
        polyline(cr, [(420 + i * 120, y0 - 100), (420 + i * 120, y0 - 100 + 120 * k)], 14, WHITE, .8)
        if k > .3: poly(cr, [(400 + i * 120, y0 - 100 + 120 * k), (440 + i * 120, y0 - 100 + 120 * k), (420 + i * 120, y0 - 70 + 120 * k)], WHITE, .8)
    pill(cr, 540, 250, "\"WE'RE WINNING!\"", 56, WHITE, ROM, back((lt - d * .4) / .25), .05)

def c_close(cr, lt, d, t):
    p = battle(cr, lt, d, t, 2.0, 3.0)
    k = ease((lt - d * .55) / .3)
    if k > 0:
        ring(cr, 540, 700, 360, 14, YEL, .8 * k)
        push(cr, 540, 250, back((lt - d * .55) / .3)); rrect(cr, -330, -62, 660, 124, 62, INK); text(cr, "50,000+ DEAD", 0, 26, 74, YEL, anchor="c"); cr.restore()
    else: pill(cr, 540, 250, "SURROUNDED", 60, YEL, INK, back((lt - .1) / .25), -.04)

def c_end(cr, lt, d, t):
    bg(cr, C("3A0CA3"), C("7209B7")); rays(cr, 540, 700, t, WHITE, .1)
    carthage(cr, 360, 1100, 520, look=1, mouth="smile", ra=150 + math.sin(t * 4) * 10, ra2=10, sword=True, blink=(t % 3) < .12)
    roman(cr, 760, 1100, 440, look=-1, mouth="o", la=60, la2=90, ra=150, ra2=20, shield=None)
    for i in range(3):
        ph = (t * 1.1 + i / 3) % 1; ell(cr, 860 + i * 20, 560 + ph * 60, 10, 16, C("8FD3FF"), 1 - ph)
    pill(cr, 540, 300, "GIVE GROUND, THEN CLOSE IN", 52, YEL, INK, back((lt - .1) / .25) * (1 + .04 * math.sin(t * 8)), .03)

BEATS = [
    dict(say="Hannibal's greatest win began with his army going backwards.", cap="Hannibal's greatest win began with his army *going backwards*.", scene=c_hook),
    dict(say="Cannae, two sixteen B C. Rome had about eighty thousand men. Hannibal, about fifty thousand.", cap="Cannae, 216 BC. Rome had about *80,000* men. Hannibal, about *50,000*.", scene=c_armies),
    dict(say="He bowed his centre out toward the Romans, then let it slowly give way.", cap="He bowed his centre out toward the Romans, then let it *slowly give way*.", scene=c_bulge),
    dict(say="The Romans pushed deeper, sure they were winning, while his veterans waited on both sides.", cap="The Romans pushed deeper, *sure they were winning*, while his veterans waited on both sides.", scene=c_push),
    dict(say="Then the sides closed in, and his cavalry hit from behind. Over fifty thousand Romans died in one day.", cap="Then the sides *closed in*, and his cavalry hit from behind. Over *50,000* Romans died in one day.", scene=c_close, hold=0.2),
    dict(say="When someone charges at you, giving ground can be the trap. Send this to a strategy nerd.", cap="When someone charges at you, *giving ground* can be the trap. Send this to a *strategy nerd*.", scene=c_end, hold=0.3),
]

if __name__ == "__main__":
    f = Film("24_cannae", BEATS, voice=("af_heart", 1.08, "en-us"))
    if "--stills" in sys.argv: sheet(f)
    else: f.render()
