"""Full-screen motion renderer (no cards). A film is a list of beats:
   dict(say="narration", cap="CAPTION with *accent* words", scene=fn(cr, lt, d, t), hold=0.0)
Scenes paint the whole 1080x1920 frame. Captions are big kinetic words in the lower-middle safe zone."""
import os, sys, math, subprocess
import numpy as np, soundfile as sf, cairo
from chars import *
import animate

W, H, FPS = 1080, 1920, 30
ROOT = "/home/claude/reels/v4"
GAP, TR, LEAD0 = 0.10, 0.20, 0.12
CAP_Y, CAP_SIZE = 1340, 96
AMBER = C("FFC83D"); INKC = C("12121C")

def chunks(text, maxc=14, maxw=3):
    out, cur, n = [], [], 0
    for i, (w, acc, nl) in enumerate(animate.tokens(text)):
        if cur and (n + len(w) > maxc or len(cur) >= maxw or nl): out.append(cur); cur, n = [], 0
        cur.append((w.upper(), acc, i)); n += len(w) + 1
    if cur: out.append(cur)
    return out

def word_times(text, s0, s1):
    ws = animate.tokens(text); ch = [len(w[0]) + 1 for w in ws]; tot = sum(ch) or 1; acc = 0; out = []
    for n in ch: out.append(s0 + (s1 - s0) * acc / tot - 0.05); acc += n
    return out

def caption(cr, chs, wt, lt):
    cur = chs[0]
    for c in chs:
        if wt[c[0][2]] <= lt: cur = c
    cr.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    size = CAP_SIZE; cr.set_font_size(size); sp = size * .28
    wd = [cr.text_extents(w).x_advance for w, _, _ in cur]; tot = sum(wd) + sp * (len(cur) - 1)
    if tot > 960: size *= 960 / tot; cr.set_font_size(size); sp = size * .28; wd = [cr.text_extents(w).x_advance for w, _, _ in cur]; tot = sum(wd) + sp * (len(cur) - 1)
    x = (W - tot) / 2; last = max([i for _, _, i in cur if wt[i] <= lt], default=-1)
    for (w, acc, i), wl in zip(cur, wd):
        k = back((lt - wt[i]) / .16)
        if k > 0:
            cr.save(); cr.translate(x + wl / 2, CAP_Y - size * .35); cr.scale(k, k); cr.translate(-wl / 2, size * .35)
            cr.new_path(); cr.move_to(0, 0); cr.text_path(w); cr.set_line_join(cairo.LINE_JOIN_ROUND); cr.set_line_width(size * .2)
            src(cr, INKC); cr.stroke_preserve(); src(cr, AMBER if (acc or i == last) else WHITE); cr.fill(); cr.restore()
        x += wl + sp

class Film:
    def __init__(self, key, beats, voice=("af_heart", 1.08, "en-us"), handle="@mind_shap"):
        self.key, self.handle = key, handle; self.out = f"{ROOT}/{key}"; os.makedirs(self.out, exist_ok=True)
        animate.VOICE, animate.SPEED, animate.LANG = voice
        self.b = []; t0 = 0.0
        for i, b in enumerate(beats):
            p = f"{self.out}/n{i}.wav"; animate.speak(b["say"], p); a, sr = sf.read(p)
            a = np.asarray(a, dtype=np.float32)
            if not voice[0].startswith("piper:"): a = animate._tighten(a, sr, keep=.13)  # piper audio is already smoothed in animate._piper
            off = LEAD0 if i == 0 else 0.0; sd = len(a) / sr; d = off + sd + GAP + b.get("hold", 0.0)
            chs = chunks(b["cap"]); wt = word_times(b["cap"], off, off + sd)
            if i == 0:  # the hook's first words are on screen from frame 0
                for _, _, wi in chs[0]: wt[wi] = -1.0
            self.b.append(dict(a=a, t0=t0, d=d, off=off, sd=sd, fn=b["scene"], chs=chs, wt=wt))
            t0 += d
        self.T = t0
        self.surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); self.cr = cairo.Context(self.surf)

    def _scene(self, b, lt, t, dx=0.0):
        cr = self.cr; cr.save(); cr.translate(dx, 0); cr.rectangle(0, 0, W, H); cr.clip()
        z = 1.0 + 0.05 * min(1, lt / b["d"]); cr.translate(W / 2, H * .42); cr.scale(z, z); cr.translate(-W / 2, -H * .42)
        b["fn"](cr, lt, b["d"], t); cr.restore()

    def frame(self, t):
        cr = self.cr; i = len(self.b) - 1
        for j, b in enumerate(self.b):
            if t < b["t0"] + b["d"]: i = j; break
        b = self.b[i]; lt = t - b["t0"]
        if i > 0 and lt < TR:
            e = ease(lt / TR); sg = 1 if i % 2 else -1; p = self.b[i - 1]
            self._scene(p, p["d"] + lt, t, -sg * e * W); self._scene(b, lt, t, sg * (1 - e) * W)
        else: self._scene(b, lt, t)
        g = cairo.LinearGradient(0, 1100, 0, 1560); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(.5, 0, 0, 0, .38); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        cr.rectangle(0, 1100, W, 460); cr.set_source(g); cr.fill()
        caption(cr, b["chs"], b["wt"], lt)
        text(cr, self.handle, W / 2, 150, 34, WHITE, .55, anchor="c")
        return self.surf

    def still(self, t, path): self.frame(t).write_to_png(path)

    def render(self):
        out, T = self.out, self.T; n = int(round(T * FPS)); tmp = f"{out}/video.tmp.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr0", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-tune", "animation", "-profile:v", "high", "-pix_fmt", "yuv420p", "-g", "60", tmp], stdin=subprocess.PIPE)
        for fi in range(n):
            s = self.frame(fi / FPS); s.flush(); p.stdin.write(bytes(s.get_data()))
        p.stdin.close(); assert p.wait() == 0; os.rename(tmp, f"{out}/video.mp4")
        sr = 24000; track = np.zeros(int((T + 1) * sr), dtype=np.float32)
        for b in self.b:
            st = int((b["t0"] + b["off"]) * sr); track[st:st + len(b["a"])] += b["a"]
        sf.write(f"{out}/voice.wav", track, sr)
        expr = "0.05*(sin(2*PI*110*t)+0.7*sin(2*PI*164.81*t)+0.6*sin(2*PI*220*t)+0.4*sin(2*PI*261.63*t))*(0.7+0.3*sin(2*PI*2*t))"
        fin = f"{ROOT}/{self.key}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{out}/video.mp4", "-i", f"{out}/voice.wav", "-f", "lavfi", "-i", f"aevalsrc={expr}:s=44100:d={T}",
                        "-filter_complex", f"[1:a]aresample=44100,acompressor=threshold=-18dB:ratio=3[v];[2:a]lowpass=f=900,volume=0.3,afade=t=in:d=0.4,afade=t=out:st={T-0.6}:d=0.6[m];"
                        f"[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", f"{T}", "-movflags", "+faststart", fin + ".tmp.mp4"], check=True)
        os.rename(fin + ".tmp.mp4", fin); print(self.key, "done", round(T, 1), "s")
        return fin
