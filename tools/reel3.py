"""v3: character scenes + owl mascot + narration, HD. usage: python3 reel3.py KEY [--still IDX T]"""
import os, sys, math, subprocess, shutil
import numpy as np, soundfile as sf, cairo
from chars import *
from scenes import SCENES, PW, PH
import animate  # reuse REELS text + narration helpers
import lessons2  # registers batch 2
import lessons3  # registers batch 3

W, H, FPS = 1080, 1920, 30
BG = C("0E1221"); CREAM = C("F6F0E2"); BODY = C("DCD9D2"); MUTED = C("969EB4"); ACC = C("F7B248")
PX, PY = 60, 280
ROOT = "/home/claude/reels/v3"
LEAD, TAIL = 0.45, 0.75

def toks(text): return animate.tokens(text)

def layout(cr, words, face, size, x0, y0, maxw, lh):
    cr.select_font_face(face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if face == "Lora" else cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size); sp = cr.text_extents(" ").x_advance
    x, y, out = x0, y0 + size, []
    for w, a, nl in words:
        if nl: x = x0; y += int(lh * 1.45)
        wl = cr.text_extents(w).x_advance
        if x > x0 and x + wl > x0 + maxw: x = x0; y += lh
        out.append((w, a, x, y)); x += wl + sp
    return out, y

class Scene:
    def __init__(self, key, idx, total, card, dur, span, t0, T, fn):
        self.idx, self.total, self.c, self.dur, self.t0, self.T, self.fn = idx, total, card, dur, t0, T, fn
        tmp = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 10, 10))
        big = card.get("big", False)
        self.tsize = 84 if big else 70; self.bsize = 48
        y = 1080
        self.title, self.body = [], []
        if card.get("title"):
            self.title, yb = layout(tmp, toks(card["title"]), "Lora", self.tsize, 90, y, W - 180, int(self.tsize * 1.18))
            self.tb = yb; y = yb + 38
        if card.get("body"):
            self.body, _ = layout(tmp, toks(card["body"]), "Inter", self.bsize, 90, y, W - 180, 70)
        allw = self.title + self.body
        ch = [len(w[0]) + 1 for w in allw]; tot = sum(ch) or 1
        s0, s1 = span; acc = 0; self.times = []
        for n in ch: self.times.append(s0 + (s1 - s0) * acc / tot - 0.08); acc += n

def words(cr, placed, times, face, size, col, t):
    cr.select_font_face(face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if face == "Lora" else cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    for (w, a, x, y), wt in zip(placed, times):
        p = ease((t - wt) / 0.35)
        if p <= 0: continue
        c = ACC if a else col
        cr.move_to(x, y + (1 - p) * 22); src(cr, c, p); cr.show_text(w)

def frame_bg(cr, tg):
    src(cr, BG); cr.paint()
    for i, (c, ph) in enumerate([(C("3E3480"), 0), (C("7A3E2A"), 2.1), (C("1E5A6A"), 4.2)]):
        x = W / 2 + 380 * math.sin(tg * .23 + ph); y = H / 2 + 650 * math.sin(tg * .17 + ph * 1.7)
        glow(cr, x, y, 620, c, .55)

def draw(cr, sc, t, mouth):
    tg = sc.t0 + t
    frame_bg(cr, tg)
    k = min(ease(t / .3), ease((sc.dur - t) / .3))
    cr.push_group()
    # panel
    cr.save(); rr_path(cr, PX, PY, PW, PH, 40); cr.clip(); cr.translate(PX, PY)
    z = 1 + 0.035 * (t / sc.dur)
    cr.translate(PW / 2, PH / 2); cr.scale(z, z); cr.translate(-PW / 2, -PH / 2)
    sc.fn(cr, t, sc.dur, mouth)
    cr.restore()
    rr_path(cr, PX, PY, PW, PH, 40); cr.set_line_width(3); src(cr, WHITE, .12); cr.stroke()
    nt = len(sc.title)
    words(cr, sc.title, sc.times[:nt], "Lora", sc.tsize, CREAM, t)
    if sc.title:
        u = ease((t - sc.times[0] - .2) / .8)
        if u > 0: rrect(cr, 90, sc.tb + 14, 150 * u, 9, 4, ACC)
    words(cr, sc.body, sc.times[nt:], "Inter", sc.bsize, BODY if sc.title else CREAM, t)
    if sc.c.get("footer"):
        text(cr, sc.c["footer"], 90, 1560, 36, MUTED, ease((t - .8) / .6), bold=False)
    cr.pop_group_to_source(); cr.paint_with_alpha(k)
    # persistent chrome
    text(cr, animate.REELS_TAG, 90, 190, 34, ACC)
    text(cr, f"{sc.idx + 1}/{sc.total}", W - 90, 190, 34, MUTED, anchor="r")
    rrect(cr, 90, 222, W - 180, 8, 4, C("3C4260"))
    rrect(cr, 90, 222, max(8, (W - 180) * min(1, tg / sc.T)), 8, 4, ACC)
    if sc.fn.__name__ != "end_card":
        owl(cr, 910, PY + PH + 40, 190, tg, mouth, look=(-.6, .5))

def build(key, still=None):
    tag, cards = animate.REELS[key]
    animate.REELS_TAG = tag.upper()
    out = f"{ROOT}/{key}"; os.makedirs(out, exist_ok=True)
    plan = []
    for i, c in enumerate(cards):
        say = c.get("say") or " ".join(x for x in [animate.plain(c.get("title", "")), animate.plain(c.get("body", ""))] if x)
        src_wav = f"/home/claude/reels/v2/{key}/n{i}.wav"
        dst = f"{out}/n{i}.wav"
        if not os.path.exists(dst) and os.path.exists(src_wav): shutil.copy(src_wav, dst)
        sd = animate.speak(say, dst)
        plan.append((c, sd, LEAD + sd + TAIL))
    T = sum(p[2] for p in plan)
    sr = 24000; track = np.zeros(int((T + 1) * sr)); t0 = 0
    for i, (c, sd, dur) in enumerate(plan):
        a, _ = sf.read(f"{out}/n{i}.wav"); st = int((t0 + LEAD) * sr); track[st:st + len(a)] += a; t0 += dur
    sf.write(f"{out}/voice.wav", track, sr)
    # mouth envelope per frame
    hop = sr // FPS; nfr = int(T * FPS) + 2
    env = np.array([np.sqrt(np.mean(track[i * hop:(i + 1) * hop] ** 2)) for i in range(nfr)])
    env = env / (np.percentile(env[env > 1e-4], 95) + 1e-9)
    env = np.clip(env, 0, 1); env = np.convolve(env, [.25, .5, .25], "same")
    mouth = lambda tg: float(env[min(len(env) - 1, int(tg * FPS))]) * (0.4 + 0.6 * abs(math.sin(tg * 22)))
    scenes = []; t0 = 0
    for i, (c, sd, dur) in enumerate(plan):
        scenes.append(Scene(key, i, len(cards), c, dur, (LEAD, LEAD + sd), t0, T, SCENES[key][i])); t0 += dur
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); cr = cairo.Context(surf)
    cr.set_antialias(cairo.ANTIALIAS_BEST)
    if still:
        i, t = still[0], still[1]; sc = scenes[i]; t = -t * sc.dur if t < 0 else t; draw(cr, sc, t, mouth(sc.t0 + t)); surf.write_to_png(f"{ROOT}/still_{key}_{i}{still[2] if len(still) > 2 else ''}.png"); return
    parts = []
    for i, sc in enumerate(scenes):
        tmp, fin = f"{out}/s{i}.tmp.mp4", f"{out}/s{i}.mp4"
        n = int(round(sc.dur * FPS))
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr0", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-tune", "animation", "-profile:v", "high",
                              "-pix_fmt", "yuv420p", "-g", "60", tmp], stdin=subprocess.PIPE)
        for fi in range(n):
            t = fi / FPS; draw(cr, sc, t, mouth(sc.t0 + t)); surf.flush(); p.stdin.write(bytes(surf.get_data()))
        p.stdin.close(); assert p.wait() == 0
        os.rename(tmp, fin); parts.append(fin); print(key, "scene", i, flush=True)
    with open(f"{out}/list.txt", "w") as f:
        for q in parts: f.write(f"file '{q}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt", "-c", "copy", f"{out}/video.mp4"], check=True)
    expr = "0.05*(sin(2*PI*110*t)+0.7*sin(2*PI*164.81*t)+0.6*sin(2*PI*220*t)+0.4*sin(2*PI*261.63*t))*(0.75+0.25*sin(2*PI*0.2*t))"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{out}/video.mp4", "-i", f"{out}/voice.wav",
                    "-f", "lavfi", "-i", f"aevalsrc={expr}:s=44100:d={T}",
                    "-filter_complex",
                    f"[1:a]aresample=44100,acompressor=threshold=-18dB:ratio=3[v];"
                    f"[2:a]lowpass=f=900,volume=0.3,afade=t=in:d=1.5,afade=t=out:st={T-2}:d=2[m];"
                    f"[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", f"{T}",
                    "-movflags", "+faststart", f"{ROOT}/{key}.tmp.mp4"], check=True)
    os.rename(f"{ROOT}/{key}.tmp.mp4", f"{ROOT}/{key}.mp4"); print(key, "done", round(T, 1))

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--still" in a:
        k = a[0]; i = a.index("--still"); build(k, (int(a[i + 1]), float(a[i + 2])))
    else:
        for k in a: build(k)
