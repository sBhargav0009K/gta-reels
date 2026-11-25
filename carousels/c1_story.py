"""Carousel 1, story version: 'The night you almost quit GTA 6' (update 01.002.002, 23 Nov 2026).
Arc: hook -> conflict -> turn -> payoff. Game-HUD look (gamehud.py), official GTA VI screenshots."""
import os, sys, math
from gamehud import *

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "c1_story")
os.makedirs(OUT, exist_ok=True)


def clock(d, txt):
    d.text((W - 44, 168), txt, font=mont(30, "Black"), fill=WHITE, anchor="ra", stroke_width=4, stroke_fill=BLK)


def chapter(d, x, y, txt):
    f = mont(24, "Black")
    w = d.textlength(txt, font=f)
    d.rectangle([x, y, x + w + 36, y + 48], fill=PINK)
    d.text((x + 18, y + 24), txt, font=f, fill=WHITE, anchor="lm")


def subtitle(img, y, lines, speaker=None, size=36):
    """Cutscene-style subtitle: centred white text on a soft dark band."""
    f = mont(size, "Bold")
    d = ImageDraw.Draw(img)
    allw = []
    rows = []
    for ln in lines:
        rows += wrap(d, ln, f, W - 160)
    h = len(rows) * int(size * 1.35) + 44
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([50, y, W - 50, y + h], 18, fill=(0, 0, 0, 175))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    yy = y + 22
    for i, r in enumerate(rows):
        if i == 0 and speaker:
            sw = d.textlength(speaker + " ", font=f)
            tw = d.textlength(r, font=f)
            x0 = W / 2 - (sw + tw) / 2
            d.text((x0, yy), speaker + " ", font=f, fill=YEL)
            d.text((x0 + sw, yy), r, font=f, fill=WHITE)
        else:
            d.text((W / 2, yy), r, font=f, fill=WHITE, anchor="ma")
        yy += int(size * 1.35)
    return y + h


def letterbox(img, top=56, bottom=56):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, top], fill=BLK)


def footnote(d, txt):
    d.text((40, H - 72), txt, font=mont(17, "SemiBold"), fill=(210, 210, 220), anchor="lb")


# ---------- 1: HOOK (title card) ----------
img = photo("Vice_City_01", fx=0.45, fy=0.5).filter(ImageFilter.GaussianBlur(28))
full = Image.open(os.path.join(SRC, "Vice_City_01.jpg")).convert("RGB").resize((W, 608), Image.LANCZOS)
full = ImageEnhance.Contrast(ImageEnhance.Color(full).enhance(1.25)).enhance(1.12)
fa = np.asarray(full).astype(float)
fy = np.linspace(0, 1, 608)[:, None, None]
fade = np.clip((fy - 0.72) / 0.28, 0, 1) ** 1.2
full = Image.fromarray(np.clip(fa * (1 - fade) + np.array(BLK) * fade, 0, 255).astype(np.uint8))
m = Image.fromarray((np.clip(fy[:, :, 0] / 0.08, 0, 1) * np.clip((1 - fy[:, :, 0]) / 0.12, 0, 1) * 255).repeat(W, 1).astype(np.uint8))
img.paste(full, (0, 70), m)
hud(img, 1, stars=0)
d = ImageDraw.Draw(img); clock(d, "11:58 PM")
chapter(d, 40, 690, "A VICE CITY STORY")
slant_text(img, (34, 750), "THE NIGHT YOU", anton(112), WHITE, stroke=7)
slant_text(img, (30, 885), "ALMOST QUIT", anton(170), YEL, stroke=9)
d = ImageDraw.Draw(img)
d.text((44, 1100), "...and the update that pulled you back in.", font=mont(34, "Bold", italic=True), fill=WHITE, stroke_width=5, stroke_fill=BLK)
button(d, 80, 1225, "x", "SWIPE TO PLAY")
img.convert("RGB").save(f"{OUT}/slide1.png")

# ---------- 2: CONFLICT ----------
img = photo("Vice_City_17", fx=0.42, fy=0.35)
hud(img, 2, stars=5)
d = ImageDraw.Draw(img); clock(d, "12:41 AM")
chapter(d, 40, 560, "CH.1  THE CHASE")
slant_text(img, (34, 620), "5 STARS.", anton(150), YEL, stroke=8)
slant_text(img, (30, 800), "THEY NEVER FADED.", anton(104), WHITE, stroke=7)
subtitle(img, 960, ["You ditched the car. You hid. You waited.", "The stars just... stayed."])
d = ImageDraw.Draw(img)
footnote(d, "Real bug: wanted level that wouldn't clear. Fixed 23 Nov.")
img.convert("RGB").save(f"{OUT}/slide2.png")

# ---------- 3: TURN ----------
img = photo("Ambrosia_04", fx=0.5, fy=0.5)
hud(img, 3, stars=0)
d = ImageDraw.Draw(img); clock(d, "6:12 AM")
chapter(d, 40, 520, "CH.2  THE MORNING AFTER")
slant_text(img, (34, 580), "THEN THE", anton(124), WHITE, stroke=7)
slant_text(img, (30, 730), "SKY MOVED.", anton(150), YEL, stroke=8)
y = subtitle(img, 925, ["Update 01.002.002 had landed.", "The stars fade now. The weather changes again.", "Even the gym's deadlift bar works."], size=33)
d = ImageDraw.Draw(img)
d.rectangle([50, y + 22, 600, y + 74], fill=(0, 0, 0, 0))
lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
ImageDraw.Draw(lay).rectangle([50, y + 22, 720, y + 78], fill=(10, 8, 16, 215))
img.alpha_composite(lay)
d = ImageDraw.Draw(img)
d.rectangle([50, y + 22, 58, y + 78], fill=YEL)
d.text((78, y + 50), "NEW: CHASE A STORM  ·  HIT THE GYM", font=mont(26, "Black"), fill=WHITE, anchor="lm")
footnote(d, "Fixes per update 01.002.002 notes, 23 Nov 2026")
img.convert("RGB").save(f"{OUT}/slide3.png")

# ---------- 4: PAYOFF + CTA ----------
img = photo("Vice_City_22", fx=0.5, fy=0.45)
hud(img, 4, stars=0)
d = ImageDraw.Draw(img); clock(d, "9:00 PM")
cx, cy = W - 300, 186
for i in range(8):
    a = math.radians(i * 45)
    d.ellipse([cx + 20 * math.cos(a) - 5, cy + 20 * math.sin(a) - 5, cx + 20 * math.cos(a) + 5, cy + 20 * math.sin(a) + 5], fill=(255, 255, 255, 60 + i * 24))
d.text((cx - 36, cy), "SAVING", font=mont(22, "Black"), fill=WHITE, anchor="rm", stroke_width=4, stroke_fill=BLK)
chapter(d, 40, 460, "CH.3  ROUND TWO")
slant_text(img, (34, 520), "SO YOU", anton(124), WHITE, stroke=7)
slant_text(img, (30, 670), "GO BACK IN.", anton(150), YEL, stroke=8)
d = panel(img, (40, 860, W - 40, 1075), "THIS TIME", [])
for i, t in enumerate(("Autosave actually saves", "Missed calls come through", "The fence takes your bags")):
    y0 = 935 + i * 46
    checkbox(d, 66, y0 + 2, s=30)
    d.text((118, y0), t, font=mont(30, "Bold"), fill=WHITE)
d.rectangle([40, 1095, W - 40, 1240], fill=PINK)
d.text((W / 2, 1115), "KNOW SOMEONE WHO QUIT?", font=anton(58), fill=WHITE, anchor="mt", stroke_width=4, stroke_fill=BLK)
d.text((W / 2, 1192), "SEND THEM THIS  ·  FOLLOW FOR TOMORROW'S STORY", font=mont(25, "Black"), fill=YEL, anchor="mt")
img.convert("RGB").save(f"{OUT}/slide4.png")
print("ok")
