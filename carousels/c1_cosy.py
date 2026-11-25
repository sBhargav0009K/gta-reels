"""Carousel 1 (cosy/elegant photo version): 'GTA 6 just got fixed', update 01.002.002 (23 Nov 2026).
Backgrounds: official GTA VI screenshots from rockstargames.com/VI/downloads/screenshots (in src_img/).
Output: 4 slides, 1080x1350."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src_img")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "c1_cosy")
os.makedirs(OUT, exist_ok=True)

GF = "/usr/share/fonts/truetype/google-fonts/"
CREAM, PEACH, ROSE, PLUM = (250, 240, 228), (255, 192, 140), (255, 150, 160), (26, 12, 28)
SOFT = (226, 208, 200)


def lora(size, w="SemiBold", italic=False):
    f = ImageFont.truetype(GF + ("Lora-Italic-Variable.ttf" if italic else "Lora-Variable.ttf"), size)
    f.set_variation_by_name(w if not italic else (w + " Italic" if w != "Regular" else "Italic"))
    return f


def mont(size, w="SemiBold"):
    f = ImageFont.truetype(GF + "ofl/montserrat/Montserrat[wght].ttf", size)
    f.set_variation_by_name(w)
    return f


def photo(name, fx=0.5, fy=0.5, warm=0.10, zoom=1.0):
    im = Image.open(os.path.join(SRC, name + ".jpg")).convert("RGB")
    s = max(W / im.width, H / im.height) * zoom
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x = int((im.width - W) * fx); y = int((im.height - H) * fy)
    im = im.crop((x, y, x + W, y + H))
    im = ImageEnhance.Color(im).enhance(0.92)
    a = np.asarray(im).astype(float)
    a = a * (1 - warm) + np.array([255, 170, 120]) * warm * (a / 255) ** 0.8 * 1.0 + a * 0  # warm film tint
    # vignette
    yy, xx = np.mgrid[0:H, 0:W]
    v = ((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2
    a *= np.clip(1 - 0.45 * v, 0.45, 1)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def shade(img, top=0.0, start=0.42, strength=0.92, top_h=260):
    """Soft plum gradient from `start` (fraction of height) to the bottom, plus a light top scrim."""
    a = np.asarray(img).astype(float)
    y = np.linspace(0, 1, H)[:, None, None]
    k = np.clip((y - start) / (1 - start), 0, 1) ** 1.3 * strength
    t = np.clip(1 - np.arange(H) / top_h, 0, 1)[:, None, None] ** 1.5 * top
    k = np.maximum(k, t)
    a = a * (1 - k) + np.array(PLUM) * k
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def spaced(d, xy, txt, f, fill, track=4, anchor="l"):
    w = sum(d.textlength(c, font=f) for c in txt) + track * (len(txt) - 1)
    x, y = xy
    if anchor == "c":
        x -= w / 2
    elif anchor == "r":
        x -= w
    for c in txt:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + track
    return w


def chrome(d, n, credit=True):
    spaced(d, (64, 58), "GTAFINITYVERSE", mont(22, "Bold"), CREAM, track=5)
    spaced(d, (W - 64, 58), f"0{n} / 04", mont(22, "Medium"), CREAM, track=4, anchor="r")
    if credit:
        d.text((W - 64, H - 40), "Image: Rockstar Games", font=mont(17, "Medium"), fill=(200, 180, 180), anchor="rs")


def rule(d, x, y, w=90, col=PEACH):
    d.line([(x, y), (x + w, y)], fill=col, width=3)


def wrap(d, txt, f, maxw):
    out, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > maxw and cur:
            out.append(cur); cur = w
        else:
            cur = t
    return out + [cur]


def para(d, x, y, txt, f, fill, maxw, lh=1.45):
    for i, ln in enumerate(wrap(d, txt, f, maxw)):
        d.text((x, y + i * f.size * lh), ln, font=f, fill=fill)
    return y + len(wrap(d, txt, f, maxw)) * f.size * lh


def pill(d, x, y, txt, f, bg, fg, padx=26, pady=14, track=3):
    w = sum(d.textlength(c, font=f) for c in txt) + track * (len(txt) - 1)
    d.rounded_rectangle([x, y, x + w + 2 * padx, y + f.size + 2 * pady], (f.size + 2 * pady) // 2, fill=bg)
    spaced(d, (x + padx, y + pady - 2), txt, f, fg, track=track)
    return w + 2 * padx


def glass(img, box, alpha=70, radius=30):
    reg = img.crop(box).filter(ImageFilter.GaussianBlur(18))
    ov = Image.new("RGBA", reg.size, (26, 12, 28, alpha))
    reg = Image.alpha_composite(reg.convert("RGBA"), ov)
    m = Image.new("L", reg.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, reg.width - 1, reg.height - 1], radius, fill=255)
    img.paste(reg.convert("RGB"), box[:2], m)
    ImageDraw.Draw(img).rounded_rectangle(box, radius, outline=(255, 220, 200, 90), width=2)


def tick(d, x, y, r=15):
    d.ellipse([x - r, y - r, x + r, y + r], outline=PEACH, width=3)
    d.line([(x - r * 0.45, y), (x - r * 0.1, y + r * 0.38), (x + r * 0.5, y - r * 0.38)], fill=PEACH, width=3)


# ---------- 1: cover ----------
img = shade(photo("Vice_City_11", fx=0.62, fy=0.5, warm=0.12), top=0.55, start=0.40)
d = ImageDraw.Draw(img); chrome(d, 1)
pill(d, 64, 760, "UPDATE 01.002.002", mont(22, "Bold"), PEACH, PLUM)
d.text((60, 830), "GTA 6 just got", font=lora(92, "SemiBold"), fill=CREAM)
d.text((60, 935), "fixed.", font=lora(132, "Medium", italic=True), fill=PEACH)
rule(d, 66, 1110)
d.text((66, 1135), "Four things worth trying again tonight.", font=lora(36, "Regular", italic=True), fill=SOFT)
spaced(d, (66, 1218), "SWIPE  →", mont(24, "Bold"), CREAM, track=6)
img.save(f"{OUT}/slide1.png")

# ---------- 2: wanted level ----------
img = shade(photo("Vice_City_17", fx=0.42, fy=0.35, warm=0.06), top=0.55, start=0.28, strength=0.97)
d = ImageDraw.Draw(img); chrome(d, 2)
pill(d, 64, 736, "NO. 01  ·  WANTED LEVEL", mont(20, "Bold"), PEACH, PLUM)
d.text((60, 795), "Lose the cops", font=lora(96, "SemiBold"), fill=CREAM)
d.text((60, 905), "again.", font=lora(110, "Medium", italic=True), fill=PEACH)
rule(d, 66, 1062)
para(d, 66, 1090, "Some players were stuck with a wanted level that never cleared. This update fixes it, so plan that getaway.",
     lora(36, "Regular"), SOFT, 900)
img.save(f"{OUT}/slide2.png")

# ---------- 3: weather + gym ----------
img = shade(photo("Ambrosia_04", fx=0.5, fy=0.5, warm=0.08), top=0.5, start=0.30)
d = ImageDraw.Draw(img); chrome(d, 3)
pill(d, 64, 546, "NO. 02 & 03  ·  WORLD", mont(20, "Bold"), PEACH, PLUM)
d.text((60, 605), "Chase the weather,", font=lora(80, "SemiBold"), fill=CREAM)
d.text((60, 700), "then hit the gym.", font=lora(84, "Medium", italic=True), fill=PEACH)
glass(img, (60, 850, W - 60, 1205))
d = ImageDraw.Draw(img)
for i, (h, b) in enumerate((("Skies move again", "Weather could get stuck for long stretches. Now it changes, so storms can roll in."),
                            ("The deadlift bar works", "It couldn't be used before. Now it can. Go lift."))):
    y0 = 885 + i * 185
    spaced(d, (104, y0), h.upper(), mont(22, "Bold"), CREAM, track=4)
    para(d, 104, y0 + 42, b, lora(31, "Regular"), SOFT, 860, lh=1.4)
d.line([(104, 1058), (W - 104, 1058)], fill=(255, 220, 200), width=1)
img.save(f"{OUT}/slide3.png")

# ---------- 4: progress + CTA ----------
img = shade(photo("Vice_City_27", fx=0.5, fy=0.2, warm=0.08), top=0.5, start=0.12, strength=0.97)
img = shade(img, start=0.30, strength=0.55)
d = ImageDraw.Draw(img); chrome(d, 4)
pill(d, 64, 466, "NO. 04  ·  PROGRESS", mont(20, "Bold"), PEACH, PLUM)
d.text((60, 522), "No more", font=lora(92, "SemiBold"), fill=CREAM)
d.text((60, 625), "lost progress.", font=lora(104, "Medium", italic=True), fill=PEACH)
y = 800
for t in ("Autosave works properly again", "Missed phone calls, story calls too, now come through", "Partners hand over bags for the fence again"):
    tick(d, 84, y + 22)
    y = para(d, 122, y, t, lora(34, "Regular"), CREAM, 860, lh=1.35) + 18
glass(img, (60, 1030, W - 60, 1235), alpha=110)
d = ImageDraw.Draw(img)
d.text((W / 2, 1060), "Send this to a friend", font=lora(46, "SemiBold"), fill=CREAM, anchor="mt")
d.text((W / 2, 1118), "who gave up on GTA 6.", font=lora(46, "Medium", italic=True), fill=PEACH, anchor="mt")
spaced(d, (W / 2, 1186), "FOLLOW FOR A NEW IDEA EVERY DAY", mont(19, "Bold"), SOFT, track=4, anchor="c")
d.text((64, H - 40), "Fixes per update 01.002.002 notes, 23 Nov 2026", font=mont(17, "Medium"), fill=(200, 180, 180), anchor="ls")
img.save(f"{OUT}/slide4.png")
print("ok")
