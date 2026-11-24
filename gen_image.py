#!/usr/bin/env python3
"""Draw the 24 November 2026 front page: THE WORLD IN ONE DAY.

A single-file Pillow build tool. It renders a 1024x1024 newspaper front page
from the story data below and writes it to entry.png next to this script.
Run:  python3 gen_image.py
"""

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
OUT = "entry.png"

# --- palette ----------------------------------------------------------------
CREAM = (246, 241, 226)
NAVY = (30, 42, 68)
GOLD = (233, 162, 59)
PAPER = (255, 255, 255)
CARD_LINE = (217, 210, 191)
DECK_INK = (76, 70, 58)
MUTED = (110, 103, 90)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

# --- page copy ---------------------------------------------------------------
MASTHEAD = "THE WORLD IN ONE DAY"
DATE_LINE = "TUESDAY \u00b7 24 NOVEMBER 2026"
KICKER = "Six stories that defined the day"
TICKER = "Colombia car bomb \u00b7 Honda recalls 810,000 cars \u00b7 Zanzibar hotel fire"
FOOTER = "Sources: Reuters \u00b7 Yeni Safak \u00b7 Times of India \u00b7 One Turn \u00b7 24 Nov 2026"

# tag, accent colour, icon kind, headline lines, deck
STORIES = [
    (
        "TECH",
        (194, 105, 26),
        "chip",
        ["HUANG\u2019S HERO", "RETURN"],
        "A day after the board reinstated him and shares jumped 31%, "
        "Trump hails his own intervention as the chip boss returns to HQ.",
    ),
    (
        "UKRAINE",
        (168, 58, 48),
        "drone",
        ["RUSSIA HITS", "ZAPORIZHZHIA"],
        "Overnight strike kills two and wounds 22, including two children; "
        "Moscow also claims hits on drone sites in Sumy.",
    ),
    (
        "DIPLOMACY",
        (43, 76, 155),
        "globe",
        ["MERZ: EUROPE READY", "TO TALK"],
        "At a Berlin presser with NATO chief Rutte, Merz says adviser "
        "talks could resume in Abu Dhabi.",
    ),
    (
        "MIDDLE EAST",
        (30, 122, 108),
        "grenade",
        ["ISRAEL STRIKE KILLS", "HAMAS CHIEF"],
        "An airstrike kills Naeem Abu Nahel, director of Hamas internal "
        "security, in western Gaza City; at least three more die near Khan Younis.",
    ),
    (
        "ASIA",
        (106, 63, 160),
        "jet",
        ["KOREAS ON EDGE AS", "JETS SCRAMBLE"],
        "Seoul scrambles jets as Russian warplanes enter its defence zone; "
        "a suspected North Korean jet breaches airspace near Ulleung.",
    ),
    (
        "USA",
        (122, 92, 30),
        "starburst",
        ["TRUMP HALTS IOWA", "DETONATION"],
        "The president stops the army blowing up toxic explosives at an Iowa "
        "plant \u2014 but a court clears the blast to go ahead anyway.",
    ),
]


# --- font helpers ------------------------------------------------------------
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def shrink_to_fit(draw, text, name, size, limit):
    """Largest size at or below `size` whose rendered width fits `limit`."""
    while size > 10 and draw.textlength(text, font=font(name, size)) > limit:
        size -= 1
    return font(name, size)


def wrap(draw, text, fnt, limit):
    """Greedy word wrap; returns a list of lines no wider than `limit`."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= limit:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, text, fnt, y, colour, cx=PAGE // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=colour)


# --- icons (simple line-art glyphs, drawn in the card accent colour) ---------
def draw_icon(draw, kind, cx, cy, s, colour):
    h = s // 2
    if kind == "chip":
        draw.rectangle([cx - h * 0.55, cy - h * 0.55, cx + h * 0.55, cy + h * 0.55],
                       outline=colour, width=4)
        draw.rectangle([cx - h * 0.22, cy - h * 0.22, cx + h * 0.22, cy + h * 0.22],
                       fill=colour)
        for k in (-1, 0, 1):
            off = k * h * 0.42
            draw.line([cx + off, cy - h * 0.85, cx + off, cy - h * 0.55], fill=colour, width=3)
            draw.line([cx + off, cy + h * 0.55, cx + off, cy + h * 0.85], fill=colour, width=3)
            draw.line([cx - h * 0.85, cy + off, cx - h * 0.55, cy + off], fill=colour, width=3)
            draw.line([cx + h * 0.55, cy + off, cx + h * 0.85, cy + off], fill=colour, width=3)
    elif kind == "drone":
        draw.rectangle([cx - h * 0.28, cy - h * 0.14, cx + h * 0.28, cy + h * 0.14],
                       fill=colour)
        for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            ex, ey = cx + sx * h * 0.8, cy + sy * h * 0.8
            draw.line([cx, cy, ex, ey], fill=colour, width=3)
            draw.ellipse([ex - h * 0.3, ey - h * 0.3, ex + h * 0.3, ey + h * 0.3],
                         outline=colour, width=3)
    elif kind == "globe":
        draw.ellipse([cx - h * 0.8, cy - h * 0.8, cx + h * 0.8, cy + h * 0.8],
                     outline=colour, width=4)
        draw.arc([cx - h * 0.35, cy - h * 0.8, cx + h * 0.35, cy + h * 0.8],
                 start=270, end=90, fill=colour, width=3)
        draw.arc([cx - h * 0.35, cy - h * 0.8, cx + h * 0.35, cy + h * 0.8],
                 start=90, end=270, fill=colour, width=3)
        draw.line([cx - h * 0.8, cy, cx + h * 0.8, cy], fill=colour, width=3)
    elif kind == "grenade":
        draw.ellipse([cx - h * 0.55, cy - h * 0.15, cx + h * 0.55, cy + h * 0.75],
                     fill=colour)
        draw.rectangle([cx - h * 0.18, cy - h * 0.55, cx + h * 0.18, cy - h * 0.12],
                       fill=colour)
        draw.line([cx + h * 0.18, cy - h * 0.55, cx + h * 0.62, cy - h * 0.85],
                  fill=colour, width=3)
        draw.line([cx + h * 0.62, cy - h * 0.85, cx + h * 0.85, cy - h * 0.6],
                  fill=colour, width=3)
        draw.line([cx + h * 0.85, cy - h * 0.6, cx + h * 0.62, cy - h * 0.4],
                  fill=colour, width=3)
    elif kind == "jet":
        draw.polygon(
            [
                (cx + h * 0.85, cy - h * 0.75),
                (cx - h * 0.75, cy + h * 0.35),
                (cx - h * 0.25, cy + h * 0.15),
                (cx - h * 0.55, cy + h * 0.75),
                (cx + h * 0.05, cy + h * 0.35),
                (cx + h * 0.35, cy + h * 0.55),
            ],
            fill=colour,
        )
    elif kind == "starburst":
        # spiky 8-point star: alternating outer and inner vertices
        import math

        points = []
        for k in range(16):
            angle = -math.pi / 2 + k * math.pi / 8
            radius = h * 0.85 if k % 2 == 0 else h * 0.38
            points.append((cx + radius * math.cos(angle),
                           cy + radius * math.sin(angle)))
        draw.polygon(points, fill=colour)
        draw.ellipse([cx - h * 0.28, cy - h * 0.28, cx + h * 0.28, cy + h * 0.28],
                     fill=CREAM)


# --- card --------------------------------------------------------------------
def draw_card(draw, box, story):
    tag, accent, icon, headline, deck = story
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=PAPER, outline=CARD_LINE, width=1)
    draw.rectangle([x0, y0, x1, y0 + 7], fill=accent)

    tag_font = font("DejaVuSans-Bold.ttf", 19)
    tag_w = draw.textlength(tag, font=tag_font)
    chip_x, chip_y = x0 + 16, y0 + 17
    draw.rectangle([chip_x, chip_y, chip_x + tag_w + 20, chip_y + 27], fill=accent)
    draw.text((chip_x + 10, chip_y + 3), tag, font=tag_font, fill=WHITE)

    draw_icon(draw, icon, x1 - 46, y0 + 40, 52, accent)

    head_font = font("DejaVuSerif-Bold.ttf", 33)
    hy = y0 + 56
    for line in headline:
        draw.text((x0 + 16, hy), line, font=head_font, fill=NAVY)
        hy += 38

    deck_font = font("DejaVuSans.ttf", 19)
    dy = y0 + 142
    for line in wrap(draw, deck, deck_font, (x1 - x0) - 32)[:3]:
        draw.text((x0 + 16, dy), line, font=deck_font, fill=DECK_INK)
        dy += 24


# --- page --------------------------------------------------------------------
def build():
    img = Image.new("RGB", (PAGE, PAGE), CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([10, 10, PAGE - 10, PAGE - 10], outline=NAVY, width=3)

    # masthead
    draw.rectangle([22, 22, PAGE - 22, 166], fill=NAVY)
    title_font = shrink_to_fit(draw, MASTHEAD, "DejaVuSerif-Bold.ttf", 62, 940)
    centred(draw, MASTHEAD, title_font, 44, WHITE)
    date_font = font("DejaVuSans-Bold.ttf", 32)
    centred(draw, DATE_LINE, date_font, 112, GOLD)

    # kicker
    kicker_font = font("DejaVuSerif.ttf", 26)
    centred(draw, KICKER, kicker_font, 180, MUTED)
    draw.rectangle([PAGE // 2 - 60, 216, PAGE // 2 + 60, 219], fill=GOLD)

    # story grid: 2 columns x 3 rows
    left, right = 24, PAGE - 24
    gap = 16
    col_w = (right - left - gap) // 2
    row_h, row_gap, top = 224, 12, 230
    for idx, story in enumerate(STORIES):
        col, row = idx % 2, idx // 2
        x0 = left + col * (col_w + gap)
        y0 = top + row * (row_h + row_gap)
        draw_card(draw, (x0, y0, x0 + col_w, y0 + row_h), story)

    # ticker
    draw.rectangle([left, 936, right, 980], fill=NAVY)
    tick_font = shrink_to_fit(draw, "ALSO TODAY:  " + TICKER,
                              "DejaVuSans.ttf", 21, 930)
    bold_font = font("DejaVuSans-Bold.ttf", tick_font.size)
    label = "ALSO TODAY:  "
    lw = draw.textlength(label, font=bold_font)
    total = lw + draw.textlength(TICKER, font=tick_font)
    tx = (PAGE - total) // 2
    draw.text((tx, 948), label, font=bold_font, fill=WHITE)
    draw.text((tx + lw, 948), TICKER, font=tick_font, fill=WHITE)

    # footer
    foot_font = font("DejaVuSans.ttf", 16)
    centred(draw, FOOTER, foot_font, 990, MUTED)

    img.save(OUT)
    print(f"wrote {OUT} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    build()
