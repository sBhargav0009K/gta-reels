"""Leonida Bucket List poster: one stacked band per region, official GTA VI screenshots.
Renders a 1080x1350 feed post and a 1080x1920 story version.
SHOTS = folder with the official press-kit screenshots (see code/carousel/carousel.py)."""
import glob, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SHOTS = os.environ.get("SHOTS", "/home/claude/shots_dl/x")
OUT = sys.argv[1] if len(sys.argv) > 1 else "posts/p001"
INK, PAPER = (14, 11, 20), (244, 238, 230)
PINK, ORANGE, TEAL, GOLD = (255, 46, 136), (255, 138, 61), (46, 230, 214), (255, 200, 70)
GREY = (190, 184, 200)
ANTON = "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf"
IF = "/usr/share/fonts/opentype/inter/"

BANDS = [  # region, screenshot, crop focus y, try line, accent
    ("VICE CITY", "Vice_City_15", 0.55, "Take a boat out past the skyline", PINK),
    ("LEONIDA KEYS", "Leonida_Keys_04", 0.45, "Scuba dive the reef with the turtles", TEAL),
    ("GRASSRIVERS", "Grassrivers_03", 0.50, "Run the swamp on an airboat", GOLD),
    ("PORT GELLHORN", "Port_Gellhorn_01", 0.40, "Cruise the neon motel strip at night", ORANGE),
    ("AMBROSIA", "Ambrosia_01", 0.50, "Ride a motorbike through biker town", PINK),
    ("MOUNT KALAGA", "Mount_Kalaga_National_Park_06", 0.55, "Kayak under the old rail bridge", TEAL),
]


def inter(s, w="Bold", display=False):
    return ImageFont.truetype(IF + ("InterDisplay-" if display else "Inter-") + w + ".otf", s)


def shot(name):
    m = glob.glob(os.path.join(SHOTS, "**", name + ".jpg"), recursive=True)
    if not m:
        sys.exit(f"missing screenshot {name}")
    return Image.open(m[0]).convert("RGB")


def cover(im, w, h, fy):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def glow_line(base, y, color, w):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([0, y - 4, w, y + 4], fill=color + (150,))
    layer = layer.filter(ImageFilter.GaussianBlur(6))
    base.alpha_composite(layer)
    ImageDraw.Draw(base).rectangle([0, y - 1, w, y + 1], fill=color + (255,))


def text_shadow(d, xy, txt, font, fill, off=3):
    d.text((xy[0] + off, xy[1] + off), txt, font=font, fill=(0, 0, 0, 200))
    d.text(xy, txt, font=font, fill=fill)


def render(W, H, head_h, foot_h, path):
    img = Image.new("RGBA", (W, H), INK + (255,))
    d = ImageDraw.Draw(img)
    band_h = (H - head_h - foot_h) // len(BANDS)
    big = band_h > 220

    # header
    d.text((48, 34 if not big else 70), "GTAFINITYVERSE  ·  TRY THIS IN GTA 6", font=inter(24 if not big else 28, "Bold"), fill=PINK)
    title_f = ImageFont.truetype(ANTON, 92 if not big else 104)
    d.text((44, 62 if not big else 108), "THE LEONIDA BUCKET LIST", font=title_f, fill=PAPER)
    d.text((48, 172 if not big else 262), "6 regions. 6 things to try. How many can you tick?",
           font=inter(28 if not big else 34, "SemiBold"), fill=GREY)

    name_f = ImageFont.truetype(ANTON, 60 if not big else 84)
    try_f = inter(27 if not big else 34, "Bold")
    num_f = inter(24 if not big else 30, "Black")
    box = 54 if not big else 66
    for i, (region, name, fy, line, acc) in enumerate(BANDS):
        y0 = head_h + i * band_h
        pic = cover(shot(name), W, band_h, fy).convert("RGBA")
        # left-to-right shade so the type reads
        shade = Image.new("RGBA", (W, band_h))
        sd = ImageDraw.Draw(shade)
        for x in range(W):
            a = int(240 * max(0.0, 1 - x / (W * 0.9)) ** 1.1)
            sd.line([(x, 0), (x, band_h)], fill=(10, 8, 16, a))
        pic.alpha_composite(shade)
        img.alpha_composite(pic, (0, y0))
        d = ImageDraw.Draw(img)
        # number tag + region name on one row, try line under it, block centred in the band
        nb = d.textbbox((0, 0), region, font=name_f)
        tb = d.textbbox((0, 0), "TRY:", font=try_f)
        nh, th, gap = nb[3] - nb[1], tb[3] - tb[1], (12 if not big else 18)
        top = y0 + (band_h - (nh + gap + th)) // 2
        tw = 50 if not big else 60
        d.rectangle([48, top, 48 + tw, top + nh], fill=acc + (255,))
        d.text((48 + tw // 2, top + nh // 2), f"{i + 1:02d}", font=num_f, fill=INK, anchor="mm")
        text_shadow(d, (48 + tw + 16, top - nb[1]), region, name_f, PAPER)
        ty = top + nh + gap - tb[1]
        text_shadow(d, (48, ty), "TRY:", try_f, acc + (255,), off=2)
        text_shadow(d, (48 + d.textlength("TRY: ", font=try_f), ty), line, try_f, PAPER + (255,), off=2)
        # checkbox
        bx, by = W - 48 - box, y0 + (band_h - box) // 2
        d.rectangle([bx - 3, by - 3, bx + box + 3, by + box + 3], outline=(0, 0, 0, 255), width=2)
        d.rectangle([bx, by, bx + box, by + box], outline=PAPER + (255,), width=5)
        if i:
            glow_line(img, y0, acc, W)
            d = ImageDraw.Draw(img)
    glow_line(img, head_h, BANDS[0][4], W)
    glow_line(img, head_h + len(BANDS) * band_h, BANDS[-1][4], W)
    d = ImageDraw.Draw(img)

    # footer
    fy0 = head_h + len(BANDS) * band_h
    d.rectangle([0, fy0 + 2, W, H], fill=INK + (255,))
    d.text((48, fy0 + (26 if not big else 50)), "SAVE IT. TICK IT. SEND IT TO YOUR DUO.",
           font=inter(32 if not big else 40, "Black", display=True), fill=PAPER)
    d.text((48, fy0 + (72 if not big else 112)), "@gtafinityverse", font=inter(22 if not big else 28, "Bold"), fill=PINK)
    d.text((W - 48, fy0 + (72 if not big else 112)), "Images: Rockstar Games", font=inter(20 if not big else 24, "Medium"),
           fill=GREY, anchor="ra")
    img.convert("RGB").save(path, quality=93)
    print(path)


os.makedirs(OUT, exist_ok=True)
render(1080, 1350, 222, 118, os.path.join(OUT, "leonida_bucket_list_feed.jpg"))
render(1080, 1920, 330, 190, os.path.join(OUT, "leonida_bucket_list_story.jpg"))
