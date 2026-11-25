"""Carousel 1, game-HUD style: 'GTA 6 just got fixed' (update 01.002.002, 23 Nov 2026).
Official GTA VI screenshots (rockstargames.com/VI/downloads/screenshots) + in-game style HUD overlays.
4 slides, 1080x1350."""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src_img")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "c1_game")
os.makedirs(OUT, exist_ok=True)
GF = "/usr/share/fonts/truetype/google-fonts/ofl/"
PINK, YEL, CYAN, WHITE, BLK = (255, 46, 136), (255, 214, 60), (60, 230, 255), (255, 255, 255), (10, 6, 14)
GREEN = (90, 230, 120)


def anton(s):
    return ImageFont.truetype(GF + "anton/Anton-Regular.ttf", s)


def mont(s, w="Black", italic=False):
    f = ImageFont.truetype(GF + ("montserrat/Montserrat-Italic[wght].ttf" if italic else "montserrat/Montserrat[wght].ttf"), s)
    f.set_variation_by_name(w + (" Italic" if italic else ""))
    return f


def photo(name, fx=0.5, fy=0.5, zoom=1.0):
    im = Image.open(os.path.join(SRC, name + ".jpg")).convert("RGB")
    s = max(W / im.width, H / im.height) * zoom
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x = int((im.width - W) * fx); y = int((im.height - H) * fy)
    im = im.crop((x, y, x + W, y + H))
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.25)).enhance(1.12)
    a = np.asarray(im).astype(float)
    yy = np.linspace(0, 1, H)[:, None, None]
    k = np.clip((yy - 0.45) / 0.55, 0, 1) ** 1.2 * 0.88 + np.clip(1 - yy / 0.16, 0, 1) * 0.55
    a = a * (1 - k) + np.array(BLK) * k
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


def slant_text(img, xy, txt, f, fill, stroke=8, shear=0.18, shadow=True, anchor="la"):
    """Bold italic-ish game title text: stroke + hard drop shadow, sheared."""
    d0 = ImageDraw.Draw(img)
    bb = d0.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    w, h = bb[2] - bb[0] + 60, bb[3] - bb[1] + 40
    lay = Image.new("RGBA", (int(w + h * shear) + 20, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    ox, oy = 10 - bb[0], 10 - bb[1]
    if shadow:
        d.text((ox + 10, oy + 10), txt, font=f, fill=(0, 0, 0, 200), stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
    d.text((ox, oy), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=BLK)
    lay = lay.transform(lay.size, Image.AFFINE, (1, shear, -shear * h, 0, 1, 0), Image.BICUBIC)
    x, y = xy
    if anchor == "ma":
        x -= lay.width / 2
    img.alpha_composite(lay, (int(x), int(y)))
    return lay.width, lay.height


def star(d, cx, cy, r, fill, outline=BLK, w=4):
    pts = [(cx + (r if i % 2 == 0 else r * 0.45) * math.cos(math.radians(-90 + i * 36)),
            cy + (r if i % 2 == 0 else r * 0.45) * math.sin(math.radians(-90 + i * 36))) for i in range(10)]
    d.polygon(pts, fill=fill, outline=outline, width=w)


def minimap(img, cx, cy, r=92, blip=PINK):
    lay = Image.new("RGBA", (2 * r + 20, 2 * r + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = r + 10
    d.ellipse([10, 10, 10 + 2 * r, 10 + 2 * r], fill=(20, 26, 34, 215))
    for (x0, y0, x1, y1, w) in ((c - r, c + 20, c + r, c - 30, 12), (c - 10, c - r, c + 30, c + r, 10), (c - r, c - 50, c + 40, c - 60, 6)):
        d.line([(x0, y0), (x1, y1)], fill=(120, 130, 140, 255), width=w)
    d.ellipse([c + 30, c + 25, c + 70, c + 65], fill=(40, 110, 170, 255))  # water
    d.ellipse([c - 60, c - 40, c - 44, c - 24], fill=YEL)  # objective blip
    d.polygon([(c, c - 20), (c + 14, c + 16), (c, c + 8), (c - 14, c + 16)], fill=blip)  # player arrow
    m = Image.new("L", lay.size, 0)
    ImageDraw.Draw(m).ellipse([10, 10, 10 + 2 * r, 10 + 2 * r], fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel("A")), np.asarray(m))))
    ImageDraw.Draw(lay).ellipse([10, 10, 10 + 2 * r, 10 + 2 * r], outline=(255, 255, 255, 230), width=5)
    ImageDraw.Draw(lay).text((c, 14), "N", font=mont(22), fill=WHITE, anchor="mt")
    img.alpha_composite(lay, (cx - c, cy - c))


def bars(d, x, y, w=184):
    d.rectangle([x, y, x + w, y + 12], fill=(0, 0, 0, 160)); d.rectangle([x + 2, y + 2, x + w * 0.82, y + 10], fill=GREEN)
    d.rectangle([x, y + 18, x + w, y + 30], fill=(0, 0, 0, 160)); d.rectangle([x + 2, y + 20, x + w * 0.55, y + 28], fill=CYAN)


def hud(img, n, stars=0):
    d = ImageDraw.Draw(img)
    minimap(img, 132, 140)
    bars(d, 40, 248)
    for i in range(5):
        star(d, W - 70 - i * 64, 82, 26, YEL if (4 - i) < stars else (255, 255, 255, 60), outline=(0, 0, 0, 255) if (4 - i) < stars else (255, 255, 255, 200), w=3)
    d.text((W - 44, 128), "@GTAFINITYVERSE", font=mont(24, "ExtraBold"), fill=WHITE, anchor="ra", stroke_width=4, stroke_fill=BLK)
    # loading/progress bar across the carousel
    d.rectangle([40, H - 36, W - 40, H - 28], fill=(255, 255, 255, 60))
    d.rectangle([40, H - 36, 40 + (W - 80) * n / 4, H - 28], fill=PINK)
    d.text((W - 40, H - 46), f"{n}/4", font=mont(22, "ExtraBold"), fill=WHITE, anchor="rb")
    d.text((40, H - 46), "Image: Rockstar Games", font=mont(16, "SemiBold"), fill=(200, 200, 210), anchor="lb")


def button(d, x, y, sym, label, r=30):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(20, 20, 24), outline=WHITE, width=4)
    if sym == "x":
        d.line([(x - 12, y - 12), (x + 12, y + 12)], fill=(120, 170, 255), width=6)
        d.line([(x - 12, y + 12), (x + 12, y - 12)], fill=(120, 170, 255), width=6)
    else:
        d.text((x, y), sym, font=mont(28), fill=WHITE, anchor="mm")
    d.text((x + r + 16, y), label, font=mont(30, "ExtraBold"), fill=WHITE, anchor="lm", stroke_width=4, stroke_fill=BLK)


def banner(img, y, txt, sub=None, col=PINK):
    d = ImageDraw.Draw(img)
    d.rectangle([0, y, W, y + 110], fill=(0, 0, 0, 170))
    d.rectangle([0, y, W, y + 5], fill=col); d.rectangle([0, y + 105, W, y + 110], fill=col)
    slant_text(img, (W / 2, y + 12), txt, anton(72), YEL, stroke=5, shear=0.12, shadow=False, anchor="ma")


def panel(img, box, head, lines, col=PINK):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rectangle(box, fill=(8, 6, 14, 200))
    d.rectangle([box[0], box[1], box[2], box[1] + 58], fill=col)
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    d.text((box[0] + 26, box[1] + 29), head, font=mont(28, "Black"), fill=WHITE, anchor="lm")
    return d


def wrap(d, txt, f, maxw):
    out, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > maxw and cur:
            out.append(cur); cur = w
        else:
            cur = t
    return out + [cur]


def checkbox(d, x, y, done=True, s=34):
    d.rectangle([x, y, x + s, y + s], outline=WHITE, width=4)
    if done:
        d.line([(x + 6, y + s / 2), (x + s * 0.42, y + s - 7), (x + s + 6, y - 6)], fill=GREEN, width=7)


# ---------- 1: cover ----------
img = photo("Vice_City_01", fx=0.45, fy=0.5).filter(ImageFilter.GaussianBlur(28))
_full = Image.open(os.path.join(SRC, "Vice_City_01.jpg")).convert("RGB").resize((W, 608), Image.LANCZOS)
_full = ImageEnhance.Contrast(ImageEnhance.Color(_full).enhance(1.25)).enhance(1.12)
_fa = np.asarray(_full).astype(float)
_fy = np.linspace(0, 1, 608)[:, None, None]
_fade = np.clip((_fy - 0.72) / 0.28, 0, 1) ** 1.2
_full = Image.fromarray(np.clip(_fa * (1 - _fade) + np.array(BLK) * _fade, 0, 255).astype(np.uint8))
_m = Image.fromarray((np.clip(_fy[:, :, 0] / 0.08, 0, 1) * np.clip((1 - _fy[:, :, 0]) / 0.12, 0, 1) * 255).repeat(W, 1).astype(np.uint8))
img.paste(_full, (0, 70), _m)
hud(img, 1, stars=0)
d = ImageDraw.Draw(img)
d.rectangle([40, 690, 450, 742], fill=PINK)
d.text((58, 716), "NEW UPDATE  01.002.002", font=mont(26, "Black"), fill=WHITE, anchor="lm")
slant_text(img, (34, 750), "GTA 6 JUST GOT", anton(118), WHITE, stroke=7)
slant_text(img, (30, 895), "FIXED!", anton(230), YEL, stroke=10)
d = ImageDraw.Draw(img)
d.text((44, 1160), "4 THINGS WORTH TRYING AGAIN", font=mont(34, "Black", italic=True), fill=WHITE, stroke_width=5, stroke_fill=BLK)
button(d, 80, 1245, "x", "SWIPE TO CONTINUE")
img.convert("RGB").save(f"{OUT}/slide1.png")

# ---------- 2: wanted level ----------
img = photo("Vice_City_17", fx=0.42, fy=0.35)
hud(img, 2, stars=5)
d = ImageDraw.Draw(img)
d.rectangle([40, 560, 300, 612], fill=PINK)
d.text((58, 586), "FIX 01 / WANTED", font=mont(26, "Black"), fill=WHITE, anchor="lm")
slant_text(img, (34, 620), "LOSE THE COPS", anton(124), WHITE, stroke=7)
slant_text(img, (30, 770), "AGAIN", anton(170), YEL, stroke=9)
d = panel(img, (40, 985, W - 40, 1170), "PATCH NOTE", [])
f = mont(32, "Bold")
y = 1062
for ln in wrap(d, "Wanted levels that never went away are fixed. Plan that getaway again.", f, W - 140):
    d.text((66, y), ln, font=f, fill=WHITE); y += 46
img.convert("RGB").save(f"{OUT}/slide2.png")

# ---------- 3: weather + gym as objectives ----------
img = photo("Ambrosia_04", fx=0.5, fy=0.5)
hud(img, 3)
d = ImageDraw.Draw(img)
d.rectangle([40, 520, 340, 572], fill=PINK)
d.text((58, 546), "FIX 02 + 03 / WORLD", font=mont(26, "Black"), fill=WHITE, anchor="lm")
slant_text(img, (34, 580), "NEW OBJECTIVES", anton(124), WHITE, stroke=7)
slant_text(img, (30, 730), "UNLOCKED", anton(124), YEL, stroke=7)
d = panel(img, (40, 905, W - 40, 1230), "OBJECTIVES", [], col=PINK)
for i, (h, b) in enumerate((("Chase a storm", "Weather could get stuck. Now it changes again."),
                            ("Hit the deadlift bar", "The gym bar works now. Go lift."))):
    y0 = 990 + i * 115
    checkbox(d, 66, y0 + 4)
    d.text((124, y0), h.upper(), font=mont(36, "Black"), fill=YEL)
    d.text((124, y0 + 50), b, font=mont(28, "SemiBold"), fill=WHITE)
img.convert("RGB").save(f"{OUT}/slide3.png")

# ---------- 4: save + CTA ----------
img = photo("Vice_City_22", fx=0.5, fy=0.45)
hud(img, 4)
d = ImageDraw.Draw(img)
# autosave spinner HUD (bottom-right style, placed under stars)
cx, cy = W - 80, 220
for i in range(8):
    a = math.radians(i * 45)
    d.ellipse([cx + 26 * math.cos(a) - 6, cy + 26 * math.sin(a) - 6, cx + 26 * math.cos(a) + 6, cy + 26 * math.sin(a) + 6],
              fill=(255, 255, 255, 60 + i * 24))
d.text((cx - 46, cy), "SAVING...", font=mont(24, "Black"), fill=WHITE, anchor="rm", stroke_width=4, stroke_fill=BLK)
d.rectangle([40, 470, 330, 522], fill=PINK)
d.text((58, 496), "FIX 04 / PROGRESS", font=mont(26, "Black"), fill=WHITE, anchor="lm")
slant_text(img, (34, 530), "NO MORE", anton(124), WHITE, stroke=7)
slant_text(img, (30, 680), "LOST PROGRESS", anton(124), YEL, stroke=7)
d = panel(img, (40, 850, W - 40, 1080), "ALSO FIXED", [])
for i, t in enumerate(("Autosave works properly", "Missed phone calls now come through", "Fence bag hand-offs work again")):
    y0 = 930 + i * 48
    checkbox(d, 66, y0 + 2, s=30)
    d.text((118, y0), t, font=mont(30, "Bold"), fill=WHITE)
d.rectangle([40, 1100, W - 40, 1240], fill=PINK)
d.text((W / 2, 1122), "SEND THIS TO A FRIEND", font=anton(62), fill=WHITE, anchor="mt", stroke_width=4, stroke_fill=BLK)
d.text((W / 2, 1198), "WHO GAVE UP ON GTA 6  ·  FOLLOW FOR DAILY IDEAS", font=mont(26, "Black"), fill=YEL, anchor="mt")
d.text((40, H - 72), "Fixes per update 01.002.002 notes, 23 Nov 2026", font=mont(16, "SemiBold"), fill=(200, 200, 210), anchor="lb")
img.convert("RGB").save(f"{OUT}/slide4.png")
print("ok")
