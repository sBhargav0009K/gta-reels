"""GTAfinityVerse case-file carousel renderer (locked style: Vice City palette + Swiss grid +
investigative storytelling). 4 slides, 1080x1350 JPEG.

Usage: python3 carousel.py spec.json OUT_DIR
Needs: official GTA VI screenshots under $SHOTS (default /home/claude/shots_dl/x, any subfolder;
download https://media-rockstargames-com.akamaized.net/VI/downloads/screenshots/GTAVI_Screenshots.zip),
fonts Inter (/usr/share/fonts/opentype/inter) and DejaVu Sans Mono.

spec.json:
{
  "case_no": "003",
  "status": "Player-reported. Not confirmed by Rockstar."   (or "Confirmed by Rockstar." / "Reported in Rockstar previews.")
  "sources": "Sources: GameRant, Dexerto, 23 Nov 2026",
  "slides": [   exactly 4, story order: hook, clue/conflict, turn, payoff+CTA
    {"img": "Vice_City_27", "fx": 0.5, "fy": 0.5,
     "label": "STATUS: UNCONFIRMED",          chip on the image (mono, caps)
     "section": "THE RUMOUR",                 numbered 00..03 automatically
     "title": "A door back\\nto 2002.",       \\n for line breaks; size auto-fits
     "body": "One or two short sentences.",
     "highlight": "optional accent-coloured line under the body",
     "evidence": {"head": "TEXT MESSAGE", "text": "U-235 REACTOR2 19-06"},   optional
     "cta": "Send this to the friend who still knows the cheats."           slide 4 only
    }, ...]
}
Exits with an error if any text overflows, so the caller can shorten it."""
import glob, json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W, H, M = 1080, 1350, 72
COL = (W - 2 * M) / 12
INK, PAPER = (14, 11, 20), (244, 238, 230)
PINK, ORANGE, TEAL = (255, 46, 136), (255, 138, 61), (46, 230, 214)
GREY, DIM = (150, 144, 160), (92, 86, 104)
ACCENTS = [PINK, ORANGE, TEAL, PINK]
SHOTS = os.environ.get("SHOTS", "/home/claude/shots_dl/x")
IF = "/usr/share/fonts/opentype/inter/"
IMG_TOP, IMG_H = 150, 560
TXT_W = W - 2 * M
FOOT_Y = H - 92


def inter(s, w="Bold", display=False):
    return ImageFont.truetype(IF + ("InterDisplay-" if display else "Inter-") + w + ".otf", s)


def mono(s):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", s)


def shot(name):
    m = glob.glob(os.path.join(SHOTS, "**", name + ".jpg"), recursive=True)
    if not m:
        sys.exit(f"missing screenshot {name}")
    return m[0]


def photo(name, fx, fy):
    im = Image.open(shot(name)).convert("RGB")
    bw, bh = W - 2 * M, IMG_H
    s = max(bw / im.width, bh / im.height)
    im = im.resize((int(im.width * s + 0.5), int(im.height * s + 0.5)), Image.LANCZOS)
    x = int((im.width - bw) * fx); y = int((im.height - bh) * fy)
    im = im.crop((x, y, x + bw, y + bh))
    return ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.15)).enhance(1.06)


def wrap(d, text, f, maxw):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split(" "):
            t = (line + " " + w).strip()
            if d.textlength(t, font=f) <= maxw or not line:
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


def render(spec, out):
    os.makedirs(out, exist_ok=True)
    slides = spec["slides"]
    assert len(slides) == 4, "need exactly 4 slides"
    paths = []
    for n, S in enumerate(slides, 1):
        acc = ACCENTS[n - 1]
        im = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(im)
        d.text((M, 64), "GTAFINITYVERSE", font=inter(22, "ExtraBold"), fill=PAPER)
        d.text((M + COL * 4, 64), f"CASE FILE {spec['case_no']}", font=inter(22, "Medium"), fill=GREY)
        d.text((W - M, 64), f"{n:02d} / 04", font=inter(22, "Medium"), fill=GREY, anchor="ra")
        d.line([(M, 108), (W - M, 108)], fill=DIM, width=2)
        d.line([(M, 108), (M + (W - 2 * M) / 4 * n, 108)], fill=acc, width=4)
        im.paste(photo(S["img"], S.get("fx", 0.5), S.get("fy", 0.5)), (M, IMG_TOP))
        if S.get("label"):
            f = mono(20); lab = S["label"].upper(); tw = d.textlength(lab, font=f)
            d.rectangle([M, IMG_TOP + IMG_H - 44, M + tw + 32, IMG_TOP + IMG_H], fill=acc)
            d.text((M + 16, IMG_TOP + IMG_H - 22), lab, font=f, fill=INK, anchor="lm")
        y = IMG_TOP + IMG_H + 48
        d.text((M, y), f"{n - 1:02d}", font=inter(22, "ExtraBold"), fill=acc)
        d.text((M + COL * 2, y), S["section"].upper(), font=inter(22, "Bold"), fill=GREY)
        y += 52
        # bottom budget: leave room for evidence / cta boxes
        extra = (92 + 22 if S.get("evidence") else 0) + (74 + 26 if S.get("cta") else 0)
        limit = FOOT_Y - 20 - extra
        size = 124 if n == 1 else 76
        while True:
            ft = inter(size, "Black", True)
            lines = wrap(d, S["title"], ft, TXT_W)
            th = len(lines) * int(size * (1.0 if n == 1 else 1.04))
            fb = inter(36 if n == 1 else 30, "Medium")
            bh = len(wrap(d, S.get("body", ""), fb, TXT_W)) * int(fb.size * 1.22) if S.get("body") else 0
            hh = len(wrap(d, S["highlight"], inter(30, "Bold"), TXT_W)) * 37 + 18 if S.get("highlight") else 0
            if y + th + 24 + bh + hh <= limit or size <= 52:
                break
            size -= 4
        y = block(d, M, y, S["title"], ft, PAPER, TXT_W, 1.0 if n == 1 else 1.04) + 24
        if S.get("body"):
            y = block(d, M, y, S["body"], fb, GREY, TXT_W)
        if S.get("highlight"):
            y = block(d, M, y + 18, S["highlight"], inter(30, "Bold"), TEAL if acc != TEAL else PINK, TXT_W)
        if S.get("evidence"):
            y += 22
            ev = S["evidence"]
            d.rectangle([M, y, W - M, y + 92], outline=acc, width=2)
            d.text((M + 24, y + 22), ev["head"].upper(), font=inter(18, "Bold"), fill=acc)
            f = mono(30)
            while d.textlength(ev["text"], font=f) > TXT_W - 48 and f.size > 18:
                f = mono(f.size - 2)
            d.text((M + 24, y + 48), ev["text"], font=f, fill=PAPER)
            y += 92
        if S.get("cta"):
            y += 26
            d.rectangle([M, y, W - M, y + 74], fill=PINK)
            f = inter(29, "ExtraBold")
            while d.textlength(S["cta"], font=f) > TXT_W - 48 and f.size > 18:
                f = inter(f.size - 1, "ExtraBold")
            d.text((M + 24, y + 37), S["cta"], font=f, fill=INK, anchor="lm")
            y += 74
        if y > FOOT_Y - 10:
            sys.exit(f"slide {n}: text overflows by {y - FOOT_Y + 10}px, shorten it")
        d.line([(M, FOOT_Y), (W - M, FOOT_Y)], fill=DIM, width=1)
        d.text((M, H - 70), spec["status"], font=inter(18, "Bold"), fill=GREY)
        f = inter(17, "Medium"); src = spec["sources"] + "  ·  Image: Rockstar Games"
        while d.textlength(src, font=f) > TXT_W - 260 and f.size > 12:
            f = inter(f.size - 1, "Medium")
        d.text((M, H - 45), src, font=f, fill=DIM)
        d.text((W - M, H - 58), "SWIPE  →" if n < 4 else "FOLLOW FOR THE NEXT CASE", font=inter(22 if n < 4 else 19, "ExtraBold"), fill=PAPER, anchor="rm")
        p = os.path.join(out, f"slide{n}.jpg"); im.save(p, quality=92); paths.append(p)
    # contact sheet for visual QC
    sh = Image.new("RGB", (W * 2 + 30, H * 2 + 30), (40, 40, 40))
    for i, p in enumerate(paths):
        sh.paste(Image.open(p), (10 + (i % 2) * (W + 10), 10 + (i // 2) * (H + 10)))
    sh.resize((sh.width // 2, sh.height // 2)).save(os.path.join(out, "sheet.jpg"), quality=85)
    print(json.dumps({"slides": paths, "sheet": os.path.join(out, "sheet.jpg")}))


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
