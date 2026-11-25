"""Carousel 2: The Secret Road to Vice City. Swiss / case-file look in the Vice City palette.
Facts: player-reported Easter egg (GameRant, Dexerto, 23 Nov 2026). Not confirmed by Rockstar."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W, H = 1080, 1350
M = 72                      # outer margin
COL = (W - 2 * M) / 12      # 12-column grid
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src_img")
OUT = os.path.join(HERE, "c2")
os.makedirs(OUT, exist_ok=True)

INK = (14, 11, 20)
PAPER = (244, 238, 230)
PINK = (255, 46, 136)
ORANGE = (255, 138, 61)
TEAL = (46, 230, 214)
GREY = (150, 144, 160)
DIM = (92, 86, 104)

IF = "/usr/share/fonts/opentype/inter/"
def inter(s, w="Bold", display=False):
    return ImageFont.truetype(IF + ("InterDisplay-" if display else "Inter-") + w + ".otf", s)
def mono(s):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", s)

IMG_TOP, IMG_H = 150, 560


def photo(name, fx=0.5, fy=0.5, zoom=1.0):
    im = Image.open(os.path.join(SRC, name + ".jpg")).convert("RGB")
    bw, bh = W - 2 * M, IMG_H
    s = max(bw / im.width, bh / im.height) * zoom
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x = int((im.width - bw) * fx); y = int((im.height - bh) * fy)
    im = im.crop((x, y, x + bw, y + bh))
    return ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.15)).enhance(1.06)


def wrap(d, text, f, maxw):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split(" "):
            t = (line + " " + w).strip()
            if d.textlength(t, font=f) <= maxw:
                line = t
            else:
                out.append(line); line = w
        out.append(line)
    return out


def block(d, x, y, text, f, fill, maxw, lead=1.22):
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=fill)
        y += int(f.size * lead)
    return y


def frame(n, img_name, fx=0.5, fy=0.5, zoom=1.0, label="", accent=PINK):
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    # top rule + running head
    d.text((M, 64), "GTAFINITYVERSE", font=inter(22, "ExtraBold"), fill=PAPER)
    d.text((M + COL * 4, 64), "CASE FILE 002", font=inter(22, "Medium"), fill=GREY)
    d.text((W - M, 64), f"{n:02d} / 04", font=inter(22, "Medium"), fill=GREY, anchor="ra")
    d.line([(M, 108), (W - M, 108)], fill=DIM, width=2)
    # progress ticks (4 segments of the top rule)
    seg = (W - 2 * M) / 4
    d.line([(M, 108), (M + seg * n, 108)], fill=accent, width=4)
    # image block on the grid
    p = photo(img_name, fx, fy, zoom)
    im.paste(p, (M, IMG_TOP))
    if label:
        f = mono(20)
        tw = d.textlength(label, font=f)
        d.rectangle([M, IMG_TOP + IMG_H - 44, M + tw + 32, IMG_TOP + IMG_H], fill=accent)
        d.text((M + 16, IMG_TOP + IMG_H - 22), label, font=f, fill=INK, anchor="lm")
    # footer
    d.line([(M, H - 92), (W - M, H - 92)], fill=DIM, width=1)
    return im, d


def footer(d, src, right="SWIPE  →"):
    d.text((M, H - 70), "Player-reported. Not confirmed by Rockstar.", font=inter(18, "Bold"), fill=GREY)
    d.text((M, H - 45), "Sources: GameRant, Dexerto, 23 Nov 2026  ·  Image: Rockstar Games", font=inter(17, "Medium"), fill=DIM)
    if right:
        d.text((W - M, H - 58), right, font=inter(22, "ExtraBold"), fill=PAPER, anchor="rm")


def section(d, y, num, name, accent):
    d.text((M, y), num, font=inter(22, "ExtraBold"), fill=accent)
    d.text((M + COL * 2, y), name, font=inter(22, "Bold"), fill=GREY)
    return y + 52


SRCLINE = "Player-reported. Sources: GameRant, Dexerto, 23 Nov 2026. Not confirmed by Rockstar."
TXT_W = W - 2 * M
Y0 = IMG_TOP + IMG_H + 48

# ---------- 1. HOOK ----------
im, d = frame(1, "Vice_City_27", 0.5, 0.55, 1.0, "STATUS: UNCONFIRMED", PINK)
y = section(d, Y0, "00", "THE RUMOUR", PINK)
y = block(d, M, y, "A door back\nto 2002.", inter(124, "Black", True), PAPER, TXT_W, 1.0) + 26
y = block(d, M, y, "Players say GTA 6 hides a portal to the old Vice City. We followed the clues.", inter(36, "Medium"), GREY, COL * 10)
footer(d, SRCLINE)
im.save(os.path.join(OUT, "slide1.jpg"), quality=93)

# ---------- 2. THE CLUE ----------
im, d = frame(2, "Ambrosia_04", 0.5, 0.45, 1.0, "EXHIBIT A: THE SUBSTATIONS", ORANGE)
y = section(d, Y0, "01", "THE CLUE", ORANGE)
y = block(d, M, y, "12 substations.\nOne old cheat code.", inter(70, "Black", True), PAPER, TXT_W, 1.04) + 22
y = block(d, M, y, "It starts at the Key Lento radio tower: pull the power switch, turn on the TV. Then 12 substations, one letter each. Together they spell a 2002 Vice City cheat.", inter(30, "Medium"), GREY, TXT_W) + 22
# evidence card
d.rectangle([M, y, W - M, y + 92], outline=ORANGE, width=2)
d.text((M + 24, y + 22), "TEXT MESSAGE", font=inter(18, "Bold"), fill=ORANGE)
d.text((M + 24, y + 48), "U-235  REACTOR2  19-06", font=mono(30), fill=PAPER)
footer(d, SRCLINE)
im.save(os.path.join(OUT, "slide2.jpg"), quality=93)

# ---------- 3. THE DOOR ----------
im, d = frame(3, "Vice_City_22", 0.5, 0.5, 1.0, "EXHIBIT B: AFTER DARK", TEAL)
y = section(d, Y0, "02", "THE DOOR", TEAL)
y = block(d, M, y, "Reactor 2.\n7 PM to 6 AM.", inter(70, "Black", True), PAPER, TXT_W, 1.04) + 22
y = block(d, M, y, "19-06 is the time window. At the power station east of Hamlet, pull the switch on the left. A portal opens.", inter(30, "Medium"), GREY, TXT_W) + 18
y = block(d, M, y, "It drops you in a nightclub in a PS2-style 2002 Vice City.", inter(30, "Bold"), TEAL, TXT_W)
footer(d, SRCLINE)
im.save(os.path.join(OUT, "slide3.jpg"), quality=93)

# ---------- 4. PAYOFF ----------
im, d = frame(4, "Vice_City_01", 0.5, 0.4, 1.0, "VERDICT: OPEN CASE", PINK)
y = section(d, Y0, "03", "THE PAYOFF", PINK)
y = block(d, M, y, "Walk out in\nTommy's shirt.", inter(70, "Black", True), PAPER, TXT_W, 1.04) + 22
y = block(d, M, y, "Reported reward: Tommy Vercetti's Hawaiian shirt and a classic motorbike, and you keep both. No fast travel, no dying, or the trail resets.", inter(30, "Medium"), GREY, TXT_W) + 26
d.rectangle([M, y, W - M, y + 74], fill=PINK)
d.text((M + 24, y + 37), "Send this to the friend who still knows the cheats.", font=inter(29, "ExtraBold"), fill=INK, anchor="lm")
footer(d, SRCLINE, "FOLLOW FOR CASE 003")
im.save(os.path.join(OUT, "slide4.jpg"), quality=93)

# contact sheet
ims = [Image.open(os.path.join(OUT, f"slide{i}.jpg")) for i in range(1, 5)]
sh = Image.new("RGB", (W * 4 + 60, H + 40), (40, 40, 40))
for i, s in enumerate(ims):
    sh.paste(s, (20 + i * (W + 7), 20))
sh.resize((sh.width // 2, sh.height // 2)).save(os.path.join(OUT, "sheet.jpg"), quality=88)
print("ok")
