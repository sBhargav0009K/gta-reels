"""Carousel 1: 'GTA 6 just got fixed' (update 1.002.002, 23 Nov 2026). 4 slides, 1080x1350, Vice Sunset."""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1350
BLK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
PINK, ORNG, GOLD, WHITE, LILAC = (255, 46, 136), (255, 140, 66), (255, 200, 80), (255, 255, 255), (226, 190, 232)
INK = (40, 10, 40)
OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(OUT, exist_ok=True)


def font(s, bold=True):
    try:
        return __import__("PIL.ImageFont", fromlist=["x"]).truetype(BLK if bold else REG, s)
    except OSError:
        return __import__("PIL.ImageFont", fromlist=["x"]).truetype(BLK, s)


def bg():
    y = np.linspace(0, 1, H)[:, None]
    stops = [(0, (18, 10, 40)), (0.55, (70, 14, 78)), (1, (255, 92, 138))]
    col = np.zeros((H, 3))
    yy = y[:, 0]
    for i in range(3):
        col[:, i] = np.interp(yy, [s[0] for s in stops], [s[1][i] for s in stops])
    a = np.repeat(col[:, None, :], W, 1).astype(np.uint8)
    img = Image.fromarray(a)
    glow = Image.new("RGB", (W, H))
    g = ImageDraw.Draw(glow)
    g.ellipse([640, -120, 1240, 480], fill=PINK)
    g.ellipse([-300, 900, 300, 1500], fill=GOLD)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    img = Image.blend(img, Image.fromarray(np.clip(np.array(img, int) + np.array(glow, int) * 0.45, 0, 255).astype(np.uint8)), 1)
    # sunset + skyline at bottom
    d = ImageDraw.Draw(img)
    d.pieslice([340, 1110, 740, 1510], 180, 360, fill=(255, 222, 130))
    for j in range(4):
        yb = 1290 - j * 34
        d.rectangle([340, yb, 740, yb + 5 + j * 2], fill=(255, 130, 80))
    sil = (30, 10, 40)
    x = 0
    rnd = np.random.default_rng(7)
    while x < W:
        bw = int(rnd.integers(50, 110)); bh = int(rnd.integers(40, 150))
        d.rectangle([x, 1310 - bh, x + bw, 1350], fill=sil)
        x += bw + int(rnd.integers(0, 12))
    for px in (120, 930):  # palms
        d.line([(px, 1310), (px + 14, 1150)], fill=sil, width=12)
        for a_ in range(0, 360, 50):
            r = math.radians(a_)
            d.line([(px + 14, 1150), (px + 14 + 80 * math.cos(r), 1150 + 40 * math.sin(r) + 20)], fill=sil, width=9)
    d.rectangle([0, 1308, W, 1312], fill=(255, 120, 150))
    return img


def glass(img, box, outline=None, alpha=36):
    ov = Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle([0, 0, ov.width - 1, ov.height - 1], 34, fill=(255, 255, 255, alpha),
                         outline=(outline + (235,)) if outline else (255, 255, 255, 100), width=4)
    img.paste(ov, box[:2], ov)


def ctext(d, y, txt, size, col=WHITE, stroke=0):
    d.text((W / 2, y), txt, font=font(size), fill=col, anchor="mt", stroke_width=stroke, stroke_fill=(30, 8, 36))


def wrap(d, txt, f, maxw):
    lines, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    return lines


def para(d, x, y, txt, size, col=WHITE, maxw=760, lh=1.32):
    f = font(size, bold=False)
    for i, ln in enumerate(wrap(d, txt, f, maxw)):
        d.text((x, y + i * size * lh), ln, font=f, fill=col)
    return y + len(wrap(d, txt, f, maxw)) * size * lh


def tag(d, x, y, txt, fill=GOLD, col=INK, size=34):
    f = font(size)
    tw = d.textlength(txt, font=f)
    d.rounded_rectangle([x, y, x + tw + 44, y + size + 30], 22, fill=fill)
    d.text((x + 22, y + 12), txt, font=f, fill=col)


def footer(d, n):
    f = font(28)
    d.text((60, 52), "@GTAFINITYVERSE", font=f, fill=LILAC)
    d.text((W - 60, 52), f"{n}/4", font=f, fill=LILAC, anchor="ra")


def buddy(d, cx, cy, mood="happy"):
    body, screen, eye = PINK, (24, 8, 32), GOLD
    d.line([(cx - 40, cy - 128), (cx - 80, cy - 200)], fill=body, width=10)
    d.ellipse([cx - 98, cy - 218, cx - 64, cy - 184], fill=eye)
    d.rounded_rectangle([cx - 165, cy - 128, cx + 165, cy + 128], 56, fill=body)
    d.rounded_rectangle([cx - 125, cy - 92, cx + 125, cy + 92], 36, fill=screen)
    for ex in (-50, 50):
        d.arc([cx + ex - 26, cy - 40, cx + ex + 26, cy + 8], 200, 340, fill=eye, width=11)
    d.arc([cx - 34, cy + 18, cx + 34, cy + 58], 20, 160, fill=eye, width=9)


def star(d, cx, cy, r, fill, outline=None):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill, outline=outline)


def wrench(d, cx, cy, s, col):
    d.line([(cx - s, cy + s), (cx + s * 0.4, cy - s * 0.4)], fill=col, width=int(s * 0.38))
    d.ellipse([cx + s * 0.1, cy - s * 1.1, cx + s * 1.1, cy - s * 0.1], fill=col)
    d.ellipse([cx + s * 0.45, cy - s * 0.95, cx + s * 0.95, cy - s * 0.45], fill=(70, 14, 78))


def barbell(d, cx, cy, s, col):
    d.rounded_rectangle([cx - s * 1.5, cy - 7, cx + s * 1.5, cy + 7], 6, fill=col)
    for sx in (-1, 1):
        d.rounded_rectangle([cx + sx * s * 0.95 - 16, cy - s * 0.75, cx + sx * s * 0.95 + 16, cy + s * 0.75], 10, fill=col)
        d.rounded_rectangle([cx + sx * s * 1.2 - 11, cy - s * 0.55, cx + sx * s * 1.2 + 11, cy + s * 0.55], 8, fill=col)


def cloud(d, cx, cy, s, col):
    d.ellipse([cx + s * 0.1, cy - s * 1.2, cx + s * 1.1, cy - s * 0.2], fill=GOLD)  # sun peeking
    for ex, ey, r in ((-0.55, 0, 0.5), (0, -0.3, 0.62), (0.55, 0, 0.5)):
        d.ellipse([cx + (ex - r) * s, cy + (ey - r) * s, cx + (ex + r) * s, cy + (ey + r) * s], fill=col)
    d.rounded_rectangle([cx - 1.05 * s, cy - 0.1 * s, cx + 1.05 * s, cy + 0.5 * s], int(0.3 * s), fill=col)
    for i in range(3):
        x = cx - 0.5 * s + i * 0.5 * s
        d.line([(x, cy + 0.7 * s), (x - 14, cy + 1.05 * s)], fill=(140, 200, 255), width=9)


def phone(d, cx, cy, s, col):
    d.rounded_rectangle([cx - s * 0.55, cy - s, cx + s * 0.55, cy + s], 22, outline=col, width=10)
    d.rounded_rectangle([cx - s * 0.2, cy - s * 0.85, cx + s * 0.2, cy - s * 0.75], 4, fill=col)
    for k in range(1, 3):  # ringing waves
        r = s * (0.75 + 0.35 * k)
        d.arc([cx + s * 0.2 - r, cy - s * 0.6 - r, cx + s * 0.2 + r, cy - s * 0.6 + r], 300, 350, fill=GOLD, width=8)


def check(d, cx, cy, r=26, col=GOLD):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.4), (cx + r * 0.5, cy - r * 0.4)], fill=INK, width=7)


BG = bg()

# ---------- slide 1: cover ----------
img = BG.copy(); d = ImageDraw.Draw(img); footer(d, 1)
tag(d, W / 2 - 205, 150, "NEW UPDATE  ·  01.002.002", fill=PINK, col=WHITE, size=32)
ctext(d, 260, "GTA 6", 150, GOLD, stroke=6)
ctext(d, 430, "JUST GOT", 118, WHITE, stroke=6)
ctext(d, 570, "FIXED", 150, WHITE, stroke=6)
d.rounded_rectangle([W / 2 - 230, 745, W / 2 + 230, 755], 5, fill=PINK)
ctext(d, 795, "4 things worth trying again", 46, LILAC)
buddy(d, W / 2 - 190, 1060)
wrench(d, W / 2 + 170, 1010, 64, GOLD)
tag(d, W / 2 + 60, 1170, "SWIPE  →", fill=WHITE, col=INK, size=40)
img.save(f"{OUT}/slide1.png")

# ---------- slide 2: wanted level ----------
img = BG.copy(); d = ImageDraw.Draw(img); footer(d, 2)
tag(d, 60, 140, "FIX 01", size=34)
d.text((60, 225), "LOSE THE", font=font(104), fill=WHITE)
d.text((60, 345), "COPS AGAIN", font=font(104), fill=GOLD)
glass(img, [60, 520, W - 60, 1050])
d = ImageDraw.Draw(img)
for i in range(6):
    star(d, 170 + i * 148, 630, 56, GOLD if i < 3 else (120, 60, 120))
y = para(d, 110, 730, "Some players got a wanted level that never went away, no matter what they did.", 42, WHITE, maxw=860)
check(d, 132, y + 50)
para(d, 180, y + 25, "Fixed in this update. Go plan that getaway again.", 42, GOLD, maxw=790)
img.save(f"{OUT}/slide2.png")

# ---------- slide 3: gym + weather ----------
img = BG.copy(); d = ImageDraw.Draw(img); footer(d, 3)
for k, (lab, head, body, icon, y0) in enumerate((
        ("FIX 02", "HIT THE GYM", "The deadlift bar couldn't be used. Now it can. Go lift.", barbell, 150),
        ("FIX 03", "CHASE THE WEATHER", "Weather could get stuck for long stretches. Now it changes again, so storms can roll in.", cloud, 640))):
    glass(img, [60, y0, W - 60, y0 + 440], outline=PINK if k == 0 else GOLD)
    d = ImageDraw.Draw(img)
    tag(d, 110, y0 + 45, lab, size=30)
    icon(d, W - 210, y0 + 150, 70, WHITE)
    d.text((110, y0 + 140), head, font=font(70 if k == 0 else 62), fill=WHITE)
    para(d, 110, y0 + 255, body, 42, LILAC, maxw=820)
img.save(f"{OUT}/slide3.png")

# ---------- slide 4: autosave + calls + CTA ----------
img = BG.copy(); d = ImageDraw.Draw(img); footer(d, 4)
tag(d, 60, 140, "FIX 04", size=34)
d.text((60, 225), "NO MORE", font=font(96), fill=WHITE)
d.text((60, 335), "LOST PROGRESS", font=font(96), fill=GOLD)
glass(img, [60, 500, W - 60, 840])
d = ImageDraw.Draw(img)
phone(d, W - 150, 620, 60, WHITE)
items = ["Autosave works properly again", "Missed phone calls (story calls too) now come through", "Partners hand over bags for the fence again"]
y = 545
for t in items:
    check(d, 112, y + 28, r=22)
    y = para(d, 150, y, t, 38, WHITE, maxw=660) + 14
d.rounded_rectangle([90, 885, W - 90, 1075], 40, fill=PINK)
ctext(d, 908, "SEND THIS TO A FRIEND", 56, WHITE)
ctext(d, 985, "WHO GAVE UP ON GTA 6", 56, GOLD)
ctext(d, 1095, "Follow for a new GTA 6 idea every day", 36, WHITE)
d.rounded_rectangle([70, 1142, W - 70, 1186], 20, fill=(30, 10, 40))
d.text((W / 2, 1150), "Source: update 01.002.002 patch notes, 23 Nov 2026 (PS5 / Xbox Series X|S)", font=font(23, bold=False), fill=LILAC, anchor="mt")
img.save(f"{OUT}/slide4.png")
print("ok")
