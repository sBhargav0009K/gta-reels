"""Reel engine v2 ("full-bleed"): official GTA VI screenshots full screen with slow push-ins,
hook text on frame 0, voice from 0.05 s, word-synced punchy captions, cut on every line,
CTA as the last beat, no separate end card. 1080x1920, 30 fps.

Usage: python3 fb.py <REEL_ID> [preview]      (specs live in reels_v2.py)
Needs: shots in $SHOTS (default /home/claude/shots_dl/x), edge-tts, ffmpeg."""
import asyncio, json, os, subprocess, sys, wave, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tts
from reels_v2 import REELS

W, H, FPS = 1080, 1920, 30
SHOTS = os.environ.get("SHOTS", "/home/claude/shots_dl/x")
VOICE, RATE = "en-US-BrianNeural", "+8%"
LEAD, GAP, TAIL = 0.05, 0.16, 0.9
SR = 44100

GF = "/usr/share/fonts/truetype/google-fonts/ofl/"
INTER = "/usr/share/fonts/opentype/inter/"
PINK, YEL, WHITE, INK = (255, 46, 136), (255, 214, 60), (255, 255, 255), (8, 6, 12)
TEAL = (46, 230, 214)

_fc = {}
def anton(s):
    return _fc.setdefault(("a", s), ImageFont.truetype(GF + "anton/Anton-Regular.ttf", s))
def inter(s, w="ExtraBold"):
    return _fc.setdefault(("i", s, w), ImageFont.truetype(INTER + f"Inter-{w}.otf", s))


def find_shot(name):
    m = glob.glob(os.path.join(SHOTS, "**", name + ".jpg"), recursive=True)
    if not m:
        raise SystemExit(f"missing shot {name}")
    return m[0]


def prep_image(name, fx, fy):
    """9:16 crop of the screenshot at 1.2x output size, so frames can push in / pan."""
    im = Image.open(find_shot(name)).convert("RGB")
    BW, BH = int(W * 1.2), int(H * 1.2)
    s = max(BW / im.width, BH / im.height)
    im = im.resize((int(im.width * s + 0.5), int(im.height * s + 0.5)), Image.LANCZOS)
    x = int((im.width - BW) * fx); y = int((im.height - BH) * fy)
    im = im.crop((x, y, x + BW, y + BH))
    # gentle grade: a touch of contrast + warm/pink bias, so all shots feel like one reel
    a = np.asarray(im).astype(np.float32)
    a = (a - 128) * 1.08 + 128
    a[..., 0] *= 1.03; a[..., 2] *= 1.02
    return np.clip(a, 0, 255).astype(np.uint8)


def frame_bg(arr, p, mode, punch):
    """p: 0..1 progress through the scene. mode: 'in' push-in, 'out' pull-out, 'l'/'r' pan."""
    BH, BW = arr.shape[:2]
    if mode == "in":
        z = 1.2 - 0.12 * p; cx, cy = 0.5, 0.5
    elif mode == "out":
        z = 1.08 + 0.12 * p; cx, cy = 0.5, 0.5
    elif mode == "l":
        z = 1.1; cx, cy = 0.62 - 0.24 * p, 0.5
    else:
        z = 1.1; cx, cy = 0.38 + 0.24 * p, 0.5
    z = z / (1 + 0.10 * punch)  # cut punch: start slightly tighter
    cw, ch = W * z, H * z
    x0 = (BW - cw) * cx; y0 = (BH - ch) * cy
    im = Image.fromarray(arr).resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
    return im


# ---------- static overlay (gradients) ----------
def make_shade():
    a = np.zeros((H, 1), np.float32)
    y = np.arange(H)[:, None]
    a += np.clip(1 - y / 360, 0, 1) * 0.62                      # top
    a += np.exp(-((y - 1160) / 330) ** 2) * 0.38                 # caption band
    a += np.clip((y - 1500) / 420, 0, 1) * 0.55                  # bottom (IG UI)
    a = np.clip(a, 0, 0.85)
    al = (np.repeat(a, W, 1) * 255).astype(np.uint8)
    lay = Image.new("RGBA", (W, H), INK + (0,)); lay.putalpha(Image.fromarray(al))
    return lay
SHADE = None


def text_w(d, s, f, sw=0):
    b = d.textbbox((0, 0), s, font=f, stroke_width=sw); return b[2] - b[0]


def draw_header(img, R, t, total):
    d = ImageDraw.Draw(img)
    # progress bar
    d.rectangle([0, 0, int(W * min(1, t / total)), 9], fill=PINK)
    f = anton(40)
    lbl = "TRY THIS IN GTA 6"
    tw = text_w(d, lbl, f)
    d.rounded_rectangle([64, 112, 64 + tw + 44, 176], 14, fill=PINK)
    d.text((86, 144), lbl, font=f, fill=WHITE, anchor="lm")
    st = R["status"]
    f2 = inter(24, "ExtraBold")
    sw = text_w(d, st, f2)
    x = 64 + tw + 64
    col = TEAL if st.startswith("CONFIRMED") else YEL
    d.rounded_rectangle([x, 118, x + sw + 36, 170], 26, outline=col, width=3)
    d.text((x + 18, 144), st, font=f2, fill=col, anchor="lm")
    d.text((66, 198), "Gameplay screenshots: Rockstar Games", font=inter(21, "SemiBold"), fill=(235, 230, 240))


def wrap_lines(d, text, f, maxw, sw):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split():
            tt = (line + " " + w).strip()
            if text_w(d, tt, f, sw) <= maxw or not line:
                line = tt
            else:
                out.append(line); line = w
        out.append(line)
    return out


def big_text(img, text, cy, size, colors, k, maxw=900):
    """Hook / CTA: huge centred Anton, white with yellow keyword lines, thick outline, scale pop."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    paras = text.upper().split("\n")
    while size > 70 and max(text_w(d, ln, anton(size), max(6, size // 13)) for ln in paras) > maxw:
        size -= 6
    f = anton(size); sw = max(6, size // 13)
    lines = wrap_lines(d, text.upper(), f, maxw, sw)
    lh = int(size * 1.06)
    y = cy - lh * len(lines) / 2
    for i, ln in enumerate(lines):
        col = colors[i % len(colors)]
        d.text((W / 2 - 20 + 8, y + 10), ln, font=f, fill=(0, 0, 0, 150), anchor="ma", stroke_width=sw, stroke_fill=(0, 0, 0, 150))
        d.text((W / 2 - 20, y), ln, font=f, fill=col, anchor="ma", stroke_width=sw, stroke_fill=INK)
        y += lh
    sc = 1 + 0.10 * (1 - k)
    if sc != 1:
        lay = lay.resize((int(W * sc), int(H * sc)), Image.BILINEAR)
        ox = (lay.width - W) // 2; oy = int((lay.height - H) * cy / H)
        lay = lay.crop((ox, oy, ox + W, oy + H))
    img.alpha_composite(lay)


def chunks_for(words, key, say=""):
    """Group voiced words into caption chunks of <=3 words / <=15 chars, breaking after punctuation
    (edge-tts drops punctuation, so look it up in the spoken text)."""
    out, cur, pos = [], [], 0
    for w in words:
        cur.append(w)
        j = say.find(w[0], pos)
        punct = False
        if j >= 0:
            pos = j + len(w[0])
            punct = pos < len(say) and say[pos] in ".,?!:;"
            if punct:
                w = (w[0] + say[pos], w[1], w[2]); cur[-1] = w
        txt = " ".join(x[0] for x in cur)
        if w[0].upper() in ("GTA", "A", "THE", "VICE") and not punct:
            continue  # never strand "GTA" from "6" or an article from its noun
        if len(cur) >= 3 or len(txt) >= 15 or punct:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def caption(img, chunk, key, k):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    size = 104
    f = anton(size); sw = 9
    words = [w[0] for w in chunk]
    txt = " ".join(words).upper()
    while text_w(d, txt, f, sw) > 880 and size > 60:
        size -= 6; f = anton(size)
    total_w = text_w(d, txt, f, sw)
    x = W / 2 - 20 - total_w / 2; y = 1110
    kw = (key or "").upper().strip(".,?!")
    for w in words:
        u = w.upper()
        col = YEL if kw and u.strip(".,?!'’") == kw else WHITE
        d.text((x + 6, y + 8), u, font=f, fill=(0, 0, 0, 140), stroke_width=sw, stroke_fill=(0, 0, 0, 140))
        d.text((x, y), u, font=f, fill=col, stroke_width=sw, stroke_fill=INK)
        x += text_w(d, u + " ", f, 0)
    sc = 1 + 0.14 * (1 - k)
    if sc != 1:
        lay = lay.resize((int(W * sc), int(H * sc)), Image.BILINEAR)
        ox = (lay.width - W) // 2; oy = int((lay.height - H) * (1150 / H))
        lay = lay.crop((ox, oy, ox + W, oy + H))
    img.alpha_composite(lay)


def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


# ---------- audio ----------
def mp3_to_np(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def build(rid, preview=False):
    global SHADE
    R = REELS[rid]
    out = os.path.join(HERE, "out", rid); os.makedirs(out, exist_ok=True)
    # 1) voice each line, collect word timings
    lines = R["lines"]
    timeline, voice_parts, t = [], [], LEAD
    for i, L in enumerate(lines):
        mp3 = os.path.join(out, f"l{i}.mp3")
        words = asyncio.run(tts.say_words(VOICE, R.get("rate", RATE), L["say"], mp3))
        a = mp3_to_np(mp3)
        # trim leading/trailing silence edge-tts adds
        nz = np.where(np.abs(a) > 0.01)[0]
        s0 = nz[0] / SR if len(nz) else 0; s1 = nz[-1] / SR if len(nz) else len(a) / SR
        a = a[int(max(0, s0 - 0.02) * SR): int((s1 + 0.06) * SR)]
        shift = max(0, s0 - 0.02)
        words = [(w, ws - shift + t, we - shift + t) for (w, ws, we) in words]
        dur = len(a) / SR
        timeline.append(dict(start=t, end=t + dur, words=words, **L))
        voice_parts.append((t, a))
        t += dur + (L.get("gap", GAP))
    main_end = t - GAP
    total = round(main_end + TAIL, 2)
    # scene windows: each scene starts 0.08 s before its line (cut lands just before the word)
    for i, sc in enumerate(timeline):
        sc["s0"] = 0.0 if i == 0 else sc["start"] - 0.08
        sc["s1"] = timeline[i + 1]["start"] - 0.08 if i + 1 < len(timeline) else total
    json.dump(dict(total=total, scenes=[{k: v for k, v in s.items()} for s in timeline]), open(os.path.join(out, "timing.json"), "w"), indent=1)
    cuts = [s["s0"] for s in timeline[1:]]
    # 2) audio mix
    n = int(total * SR)
    v = np.zeros(n, np.float32)
    for (st, a) in voice_parts:
        i0 = int(st * SR); v[i0:i0 + len(a)] += a[: max(0, n - i0)]
    mus_wav = os.path.join(out, "music.wav")
    env = dict(os.environ, BPM=str(R.get("bpm", 100)), MOOD=R.get("mood", "drive"))
    subprocess.run([sys.executable, os.path.join(HERE, "music.py"), mus_wav, str(total), ",".join(f"{c:.2f}" for c in cuts)], check=True, env=env)
    with wave.open(mus_wav) as w:
        m = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2)[:, 0] / 32768
    m = np.pad(m, (0, max(0, n - len(m))))[:n]
    # duck music under voice
    venv = np.convolve(np.abs(v), np.ones(2205) / 2205, mode="same")
    duck = np.where(venv > 0.01, 0.22, 0.5)
    duck = np.convolve(duck, np.ones(4410) / 4410, mode="same")
    mix = v * 1.0 + m * duck
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.9
    pre = os.path.join(out, "premix.wav")
    with wave.open(pre, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
    # 3) frames
    SHADE = SHADE or make_shade()
    imgs = [prep_image(s["img"], s.get("fx", 0.5), s.get("fy", 0.5)) for s in timeline]
    modes = ["in", "r", "out", "l", "in", "r", "out"]
    nf = int(total * FPS)
    frames_to = sorted(set([int(0.03 * FPS)] + [int(((s["s0"] + s["s1"]) / 2) * FPS) for s in timeline])) if preview else None
    vid = os.path.join(out, "video.mp4")
    if not preview:
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                               "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    caps = [chunks_for(s["words"], s.get("key"), s["say"]) for s in timeline]
    rng = range(nf) if not preview else frames_to
    for fi in rng:
        tt = fi / FPS
        si = max(i for i, s in enumerate(timeline) if s["s0"] <= tt + 1e-6)
        sc = timeline[si]
        p = (tt - sc["s0"]) / max(0.1, sc["s1"] - sc["s0"])
        punch = 0.0 if si == 0 else max(0, 1 - (tt - sc["s0"]) / 0.18)
        img = frame_bg(imgs[si], p, sc.get("move", modes[si % len(modes)]), punch).convert("RGBA")
        img.alpha_composite(SHADE)
        draw_header(img, R, tt, total)
        if sc.get("big"):   # hook / CTA as big text (shown from the very first frame of the scene)
            k = ease((tt - sc["s0"]) / 0.2) if si else 1.0
            big_text(img, sc["big"], sc.get("big_y", 820), sc.get("big_size", 150), sc.get("big_cols", [WHITE, YEL]), k)
        else:
            cur = None
            for ch in caps[si]:
                if ch[0][1] - 0.05 <= tt:
                    cur = ch
            if cur is None and caps[si]:
                cur = caps[si][0]
            if cur:
                k = ease((tt - (cur[0][1] - 0.05)) / 0.12)
                caption(img, cur, sc.get("key"), k)
        if sc.get("tag"):   # small fact tag on a scene (e.g. "CONFIRMED BY ROCKSTAR")
            d = ImageDraw.Draw(img); f = inter(30, "ExtraBold"); tw = text_w(d, sc["tag"], f)
            kk = ease((tt - sc["s0"] - 0.25) / 0.2)
            if kk > 0:
                x = W / 2 - 20 - tw / 2 - 26; y = 1300 + 20 * (1 - kk)
                d.rounded_rectangle([x, y, x + tw + 52, y + 62], 31, fill=TEAL if "CONFIRMED" in sc["tag"] else YEL)
                d.text((x + 26, y + 31), sc["tag"], font=f, fill=INK, anchor="lm")
        # white flash on cuts
        if si and tt - sc["s0"] < 0.1:
            fl = Image.new("RGBA", (W, H), (255, 255, 255, int(110 * (1 - (tt - sc["s0"]) / 0.1))))
            img.alpha_composite(fl)
        rgb = img.convert("RGB")
        if preview:
            rgb.save(os.path.join(out, f"pv_{tt:05.2f}.jpg"), quality=88)
        else:
            ff.stdin.write(rgb.tobytes())
    if preview:
        return
    ff.stdin.close(); ff.wait()
    final = os.path.join(HERE, "out", f"try_this_gta6_{rid}_{R['slug']}_V2.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", final], check=True)
    # cover = frame at 0.4 s (hook fully visible)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.4", "-i", final, "-frames:v", "1", "-q:v", "2",
                    os.path.join(HERE, "out", f"try_this_gta6_{rid}_COVER_V2.jpg")], check=True)
    print(json.dumps(dict(reel=rid, total=total, main_end=round(main_end, 2), cuts=[round(c, 2) for c in cuts], file=final)))


if __name__ == "__main__":
    build(sys.argv[1], preview=len(sys.argv) > 2 and sys.argv[2] == "preview")
