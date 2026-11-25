"""Shared game-HUD helpers for gtafinityverse carousels (minimap, wanted stars, slanted titles, panels, progress bar)."""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src_img")
OUT = None

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


