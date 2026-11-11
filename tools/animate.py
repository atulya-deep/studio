"""Animated, narrated microlearning reels. Usage: python3 animate.py [reel_key ...] [--still KEY IDX T]"""
import os, sys, re, math, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import soundfile as sf

W, H, FPS = 1080, 1920, 30
BG = (14, 18, 33)
CREAM = (246, 240, 226)
BODY = (220, 217, 210)
MUTED = (150, 158, 180)
ACCENT = (247, 178, 72)
BLOBS = [((92, 70, 200), 0.0), ((230, 120, 60), 2.1), ((40, 140, 170), 4.2)]
SERIF = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
SANS_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
SANS = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
if not os.path.exists(SANS): SANS = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
TTS = "/home/claude/tts"
VOICE, SPEED = "af_heart", 1.0
ROOT = "/home/claude/reels/v2"

_fc = {}
def font(p, s, bold=False):
    k = (p, s, bold)
    if k not in _fc:
        f = ImageFont.truetype(p, s)
        if bold and "Variable" in p:
            try: f.set_variation_by_name("Bold")
            except Exception: pass
        _fc[k] = f
    return _fc[k]

def ease(x):  # easeOutCubic, clamped
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

# ---------- layout ----------
def tokens(text):
    """split into words; *phrase* -> accent. returns [word, accent, newline_before]"""
    out, acc = [], False
    for pi, para in enumerate(text.split("\n")):
        for j, w in enumerate(para.split()):
            if w.startswith("*"): acc = True; w = w[1:]
            a = acc
            if "*" in w: acc = False; w = w.replace("*", "")
            out.append([w, a, pi > 0 and j == 0])
    return out

def layout(words, f, x0, y0, maxw, lh):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    sp = d.textlength(" ", font=f)
    x, y, placed = x0, y0, []
    for w, a, nl in words:
        if nl: x = x0; y += int(lh * 1.6)
        wl = d.textlength(w, font=f)
        if x > x0 and x + wl > x0 + maxw: x = x0; y += lh
        placed.append((w, a, x, y)); x += wl + sp
    return placed, y + lh

# ---------- background ----------
def background(t):
    small = Image.new("RGB", (216, 384), BG)
    d = ImageDraw.Draw(small)
    for i, (col, ph) in enumerate(BLOBS):
        cx = 108 + 85 * math.sin(t * 0.23 + ph)
        cy = 192 + 140 * math.sin(t * 0.17 + ph * 1.7) + (i - 1) * 60
        r = 95 + 15 * math.sin(t * 0.4 + ph)
        c = tuple(int(BG[k] + (col[k] - BG[k]) * 0.42) for k in range(3))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
    small = small.filter(ImageFilter.GaussianBlur(38))
    return small.resize((W, H), Image.BILINEAR)

# ---------- scene ----------
class Scene:
    def __init__(self, tag, idx, total, card, dur, words_t, t0_global, total_dur):
        self.tag, self.idx, self.total, self.c = tag, idx, total, card
        self.dur, self.t0g, self.T = dur, t0_global, total_dur
        big = card.get("big", False)
        self.ft = font(SERIF, 112 if big else 80, True)
        self.fb = font(SANS, 52)
        y = 640 if big else 560
        self.title, self.body = [], []
        if card.get("title"):
            self.title, y = layout(tokens(card["title"]), self.ft, 90, y, W - 180, int(self.ft.size * 1.2))
            y += 60
        self.title_bottom = y - 60
        if card.get("body"):
            self.body, y = layout(tokens(card["body"]), self.fb, 90, y, W - 180, 76)
        allw = self.title + self.body
        # reveal times: proportional to character position across spoken span
        chars = [len(w[0]) + 1 for w in allw]
        tot = sum(chars) or 1
        s0, s1 = words_t
        acc, self.times = 0, []
        for n in chars:
            self.times.append(s0 + (s1 - s0) * acc / tot - 0.08); acc += n

    def draw_words(self, layer, placed, times, f, base_col, t, rise=26, pop=False):
        d = ImageDraw.Draw(layer)
        for (w, a, x, y), wt in zip(placed, times):
            p = ease((t - wt) / 0.35)
            if p <= 0: continue
            col = ACCENT if a else base_col
            alpha = int(255 * p)
            if pop:
                dy = int((1 - p) * 60)
            else:
                dy = int((1 - p) * rise)
            d.text((x, y + dy), w, font=f, fill=col + (alpha,))

    def frame(self, t):
        tg = self.t0g + t
        im = background(tg).convert("RGBA")
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        # header (persistent)
        d.text((90, 150), self.tag.upper(), font=font(SANS_B, 34), fill=ACCENT + (255,))
        # global progress bar
        d.rounded_rectangle((90, 222, W - 90, 230), 4, fill=(60, 66, 92, 255))
        px = 90 + (W - 180) * min(1, tg / self.T)
        d.rounded_rectangle((90, 222, max(98, px), 230), 4, fill=ACCENT + (255,))
        # slide counter
        d.text((W - 90, 150), f"{self.idx + 1}/{self.total}", font=font(SANS_B, 34), fill=MUTED + (255,), anchor="ra")
        nt = len(self.title)
        self.draw_words(layer, self.title, self.times[:nt], self.ft, CREAM, t, pop=self.c.get("big", False))
        # accent underline grows under title
        if self.title:
            u = ease((t - self.times[0] - 0.2) / 0.8)
            if u > 0:
                d.rounded_rectangle((90, self.title_bottom + 18, 90 + int(160 * u), self.title_bottom + 28), 5, fill=ACCENT + (255,))
        self.draw_words(layer, self.body, self.times[nt:], self.fb, BODY if self.title else CREAM, t)
        if self.c.get("footer"):
            fa = int(255 * ease((t - 0.8) / 0.6))
            d.text((90, 1440), self.c["footer"], font=font(SANS, 38), fill=MUTED + (fa,))
        im = Image.alpha_composite(im, layer)
        # scene transition: fade in from bg / slide
        fin = ease(t / 0.3); fout = ease((self.dur - t) / 0.3)
        k = min(fin, fout)
        if k < 1:
            bg = background(tg).convert("RGBA")
            im = Image.blend(bg, im, k)
        return im.convert("RGB")

# ---------- narration ----------
_kok = None
def speak(text, path):
    global _kok
    if os.path.exists(path):
        a, sr = sf.read(path); return len(a) / sr
    if _kok is None:
        from kokoro_onnx import Kokoro
        _kok = Kokoro(f"{TTS}/kokoro-v1.0.onnx", f"{TTS}/voices-v1.0.bin")
    s, sr = _kok.create(text, voice=VOICE, speed=SPEED, lang="en-us")
    # trim leading/trailing silence
    nz = np.where(np.abs(s) > 0.01)[0]
    if len(nz): s = s[max(0, nz[0] - 600): nz[-1] + 1200]
    sf.write(path, s, sr)
    return len(s) / sr

def plain(t): return t.replace("*", "").replace("\n", " ")

def build(key, only_still=None):
    tag, cards = REELS[key]
    out = f"{ROOT}/{key}"; os.makedirs(out, exist_ok=True)
    LEAD, TAIL = 0.45, 0.75
    plan = []
    for i, c in enumerate(cards):
        say = c.get("say") or " ".join(x for x in [plain(c.get("title", "")), plain(c.get("body", ""))] if x)
        sd = speak(say, f"{out}/n{i}.wav")
        plan.append((c, sd, LEAD + sd + TAIL))
    T = sum(p[2] for p in plan)
    scenes, t0 = [], 0
    for i, (c, sd, dur) in enumerate(plan):
        scenes.append(Scene(tag, i, len(cards), c, dur, (LEAD, LEAD + sd), t0, T)); t0 += dur
    if only_still:
        i, t = only_still
        scenes[i].frame(t).save(f"{ROOT}/still_{key}_{i}.png"); return
    parts = []
    for i, sc in enumerate(scenes):
        tmp, fin = f"{out}/s{i}.tmp.mp4", f"{out}/s{i}.mp4"
        n = int(round(sc.dur * FPS))
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                              "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for fi in range(n):
            p.stdin.write(sc.frame(fi / FPS).tobytes())
        p.stdin.close(); assert p.wait() == 0
        os.rename(tmp, fin); parts.append(fin)
        print(key, "scene", i, "done", flush=True)
    with open(f"{out}/list.txt", "w") as f:
        for q in parts: f.write(f"file '{q}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt", "-c", "copy", f"{out}/video.mp4"], check=True)
    # narration track with real scene offsets
    sr = 24000
    track = np.zeros(int((T + 1) * sr))
    t0 = 0
    for i, (c, sd, dur) in enumerate(plan):
        a, _ = sf.read(f"{out}/n{i}.wav")
        st = int((t0 + LEAD) * sr); track[st:st + len(a)] += a; t0 += dur
    sf.write(f"{out}/voice.wav", track, sr)
    expr = "0.05*(sin(2*PI*110*t)+0.7*sin(2*PI*164.81*t)+0.6*sin(2*PI*220*t)+0.4*sin(2*PI*261.63*t))*(0.75+0.25*sin(2*PI*0.2*t))"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{out}/video.mp4", "-i", f"{out}/voice.wav",
                    "-f", "lavfi", "-i", f"aevalsrc={expr}:s=44100:d={T}",
                    "-filter_complex",
                    f"[1:a]aresample=44100,volume=1.6,acompressor=threshold=-18dB:ratio=3[v];"
                    f"[2:a]lowpass=f=900,volume=0.45,afade=t=in:d=1.5,afade=t=out:st={T-2}:d=2[m];"
                    f"[v][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", f"{T}",
                    f"{ROOT}/{key}.mp4"], check=True)
    print(key, "total", round(T, 1), "s")

END = dict(title="Save this.", body="Follow for a new lesson from books, research and history.",
           footer="New lesson every Mon · Wed · Fri",
           say="Save this. And follow for a new lesson every Monday, Wednesday and Friday.")

REELS = {
 "01_zeigarnik": ("Psychology · Mindset", [
   dict(title="Why your brain *won't let go* of unfinished tasks", big=True, footer="A 60-second lesson"),
   dict(body="In the 1920s, psychologist Bluma Zeigarnik noticed something odd. Waiters remembered open orders *perfectly*, then forgot them the moment the bill was paid.",
        say="In the nineteen-twenties, psychologist Bluma Zeigarnik noticed something odd. Waiters remembered open orders perfectly, then forgot them the moment the bill was paid."),
   dict(title="The Zeigarnik Effect", body="Unfinished tasks stay active in memory. Your mind keeps *nudging* you about them, which is why open loops feel so draining."),
   dict(title="You don't have to finish everything", body="A 2011 study by Masicampo and Baumeister found that simply making a *concrete plan* for an unfinished goal reduced intrusive thoughts about it."),
   dict(title="Try this tonight", body="Before you stop work, write down the *very next step* for each open task. Your brain treats the plan as a closed loop, and lets you *rest*."),
   END]),
 "02_if_then": ("Productivity · Habits", [
   dict(title="The one-sentence trick that *nearly triples* follow-through", big=True, footer="A 60-second lesson"),
   dict(body="Motivation tells you *what* you want. It doesn't tell you *when*, or *where*, you'll actually do it. That gap is where most habits die."),
   dict(title="Implementation intentions", body="Psychologist Peter Gollwitzer's research shows that plans written as \"if X, then I'll do Y\" make action far more *automatic*."),
   dict(title="The evidence", body="In a 2002 exercise study, *91%* of people who wrote down when and where they'd work out actually did it. In the other groups, only about *a third* did.",
        say="The evidence. In a two thousand two exercise study, ninety-one percent of people who wrote down when and where they'd work out actually did it. In the other groups, only about a third did."),
   dict(title="Write yours now", body="\"If it's 7 a.m. and I've poured my coffee, then I'll read ten pages.\"\nSpecific cue. Specific action. *No debating.*",
        say="Write yours now. If it's seven A M and I've poured my coffee, then I'll read ten pages. Specific cue. Specific action. No debating."),
   END]),
 "03_fabian": ("History · Strategy", [
   dict(title="How Rome beat an unbeatable general by *refusing to fight*", big=True, footer="A 60-second lesson"),
   dict(body="217 BC. Hannibal has crushed Roman armies again and again in Italy. Rome is in *panic*.",
        say="Two seventeen B C. Hannibal has crushed Roman armies again and again in Italy. Rome is in panic."),
   dict(title="Enter Fabius Maximus", body="Instead of a big battle, he shadowed Hannibal from the hills, cut off his supplies, and struck only small, safe blows. Romans mocked him as *\"the Delayer.\"*"),
   dict(title="Then Rome got impatient", body="In 216 BC, they abandoned his approach and met Hannibal head-on at Cannae. It became one of the *worst defeats* in Roman history. Afterwards, Rome went back to Fabius's way.",
        say="Then Rome got impatient. In two sixteen B C, they abandoned his approach and met Hannibal head-on at Cannae. It became one of the worst defeats in Roman history. Afterwards, Rome went back to Fabius's way."),
   dict(title="The lesson", body="You don't have to win the fight your opponent *chooses*. Sometimes the strongest move is to control the tempo, and let *time* work for you."),
   END]),
}

if __name__ == "__main__":
    if "--still" in sys.argv:
        i = sys.argv.index("--still"); build(sys.argv[i + 1], (int(sys.argv[i + 2]), float(sys.argv[i + 3])))
    else:
        for k in (sys.argv[1:] or list(REELS)): build(k)
