#!/usr/bin/env python3
"""Build entry.png: a newspaper front page summing up Tuesday 24 November 2026.

Local build tool only (needs Pillow): it draws the image once, and main.ts ships
the finished PNG. Run:
    python3 gen_image.py            # writes entry.png next to this file
All facts were checked against Reuters, Yeni Safak, Times of India and One Turn
reporting on 24 November 2026; see SOURCES in the README.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (16, 16, 16)
NAVY = (15, 35, 64)
GOLD = (217, 164, 65)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_icon(draw, kind, box, color):
    """Small flat icon drawn with primitives. box = (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "tech":  # chip
        draw.rectangle([x0 + 12, y0 + 12, x1 - 12, y1 - 12], fill=color)
        draw.rectangle([x0 + 22, y0 + 22, x1 - 22, y1 - 22], fill=PAPER)
        for i in range(3):
            t = x0 + 20 + i * 12
            draw.line([t, y0 + 4, t, y0 + 12], fill=color, width=3)
            draw.line([t, y1 - 12, t, y1 - 4], fill=color, width=3)
            ty = y0 + 20 + i * 12
            draw.line([x0 + 4, ty, x0 + 12, ty], fill=color, width=3)
            draw.line([x1 - 12, ty, x1 - 4, ty], fill=color, width=3)
    elif kind == "ukraine":  # quadcopter drone
        draw.rectangle([cx - 10, cy - 8, cx + 10, cy + 8], fill=color)
        for sx in (-1, 1):
            for sy in (-1, 1):
                px, py = cx + sx * 20, cy + sy * 16
                draw.line([cx, cy, px, py], fill=color, width=3)
                draw.ellipse([px - 9, py - 4, px + 9, py + 4], outline=color, width=3)
    elif kind == "diplomacy":  # globe
        draw.ellipse([x0 + 4, y0 + 4, x1 - 4, y1 - 4], outline=color, width=4)
        draw.ellipse([cx - 12, y0 + 4, cx + 12, y1 - 4], outline=color, width=3)
        draw.line([x0 + 4, cy, x1 - 4, cy], fill=color, width=3)
        draw.arc([x0 + 4, y0 + 14, x1 - 4, y1 - 14], 200, 340, fill=color, width=3)
    elif kind == "bomb":  # round bomb with fuse
        draw.ellipse([cx - 18, cy - 6, cx + 18, cy + 28], fill=color)
        draw.line([cx + 8, cy - 6, cx + 20, cy - 20], fill=color, width=4)
        for dx, dy in [(24, -26), (16, -28), (28, -18)]:
            draw.line([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], fill=color, width=3)
            draw.line([cx + dx - 3, cy + dy + 3, cx + dx + 3, cy + dy - 3], fill=color, width=3)
    elif kind == "jets":  # fighter jet, nose up-right
        draw.polygon([(x0 + 8, y1 - 8), (x0 + 30, cy - 6), (x1 - 6, y0 + 10),
                      (x1 - 14, cy + 2), (x0 + 34, y1 - 16), (x0 + 22, y1 - 6)],
                     fill=color)
        draw.polygon([(cx - 2, cy + 6), (cx + 16, y1 - 4), (cx + 2, cy + 14)], fill=color)
    elif kind == "blast":  # starburst
        import math
        pts = []
        for i in range(16):
            ang = math.pi * i / 8
            r = 30 if i % 2 == 0 else 13
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        draw.polygon(pts, fill=color)
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=PAPER)


CARDS = [
    ("TECH", (178, 91, 9), "tech",
     "HUANG\u2019S HERO RETURN",
     "A day after the board reinstated him and shares jumped 31%, Trump hails "
     "his own intervention as the chip boss returns to HQ."),
    ("UKRAINE", (166, 58, 46), "ukraine",
     "RUSSIA HITS ZAPORIZHZHIA",
     "Overnight strike kills two and wounds 22, including two children; Moscow "
     "also claims hits on drone sites in Sumy."),
    ("DIPLOMACY", (36, 86, 166), "diplomacy",
     "MERZ: EUROPE READY TO TALK",
     "At a Berlin presser with NATO chief Rutte, Merz says adviser talks could "
     "resume in Abu Dhabi."),
    ("MIDDLE EAST", (16, 110, 92), "bomb",
     "ISRAEL STRIKE KILLS HAMAS CHIEF",
     "An airstrike kills Naeem Abu Nahel, director of Hamas internal security, "
     "in western Gaza City; at least three more die near Khan Younis."),
    ("ASIA", (90, 60, 140), "jets",
     "KOREAS ON EDGE AS JETS SCRAMBLE",
     "Seoul scrambles jets as Russian warplanes enter its defence zone; a "
     "suspected North Korean jet breaches airspace near Ulleung."),
    ("USA", (110, 82, 40), "blast",
     "TRUMP HALTS IOWA DETONATION",
     "The president stops the army blowing up toxic explosives at an Iowa plant "
     "\u2014 but a court clears the blast to go ahead anyway."),
]

TICKER = ("ALSO TODAY:  Colombia car bomb  \u00b7  Honda recalls 810,000 cars  "
          "\u00b7  Zanzibar hotel fire")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # frame
    d.rectangle([10, 10, W - 11, H - 11], outline=NAVY, width=3)
    # masthead
    d.rectangle([24, 24, W - 24, 168], fill=NAVY)
    f_title = font(SERIF, 62)
    f_date = font(SANS_B, 34)
    d.text((W // 2, 52), "THE WORLD IN ONE DAY", font=f_title, fill=WHITE, anchor="ma")
    d.text((W // 2, 128), "TUESDAY  \u00b7  24 NOVEMBER 2026", font=f_date, fill=GOLD, anchor="ma")
    # sub-deck
    f_sub = font(SERIF_IT, 23)
    d.text((W // 2, 182), "Six stories that defined the day", font=f_sub, fill=GREY, anchor="ma")
    d.line([W // 2 - 120, 214, W // 2 + 120, 214], fill=GOLD, width=3)

    # grid of cards: 2 cols x 3 rows
    gx, gy, gw, gh, gap = 24, 226, 476, 222, 12
    f_kick = font(SANS_B, 17)
    f_head = font(SANS_B, 28)
    f_deck = font(SANS, 19)
    for i, (kicker, color, icon, head, deck) in enumerate(CARDS):
        cx = gx + (i % 2) * (gw + gap)
        cy = gy + (i // 2) * (gh + gap)
        d.rectangle([cx, cy, cx + gw, cy + gh], fill=WHITE, outline=(200, 192, 172), width=2)
        d.rectangle([cx, cy, cx + gw, cy + 6], fill=color)
        # kicker tag
        kw = d.textlength(kicker, font=f_kick) + 20
        d.rectangle([cx + 14, cy + 18, cx + 14 + kw, cy + 44], fill=color)
        d.text((cx + 24, cy + 31), kicker, font=f_kick, fill=WHITE, anchor="lm")
        # icon top-right
        draw_icon(d, icon, (cx + gw - 78, cy + 16, cx + gw - 14, cy + 80), color)
        # headline (max 2 lines; keep clear of the icon zone at top-right)
        lines = wrap(d, head, f_head, gw - 32 - 88)
        y = cy + 56
        for ln in lines[:2]:
            d.text((cx + 16, y), ln, font=f_head, fill=INK)
            y += 35
        # deck (max 3 lines)
        dlines = wrap(d, deck, f_deck, gw - 32)
        y = cy + 56 + 35 * min(len(lines), 2) + 6
        for ln in dlines[:3]:
            d.text((cx + 16, y), ln, font=f_deck, fill=(60, 60, 60))
            y += 25

    # ticker strip (shrink the font until the line fits the strip)
    ty = gy + 3 * gh + 2 * gap + 12  # 928
    d.rectangle([24, ty, W - 24, ty + 44], fill=NAVY)
    tick_size = 18
    while tick_size > 12:
        f_tick = font(SANS_B, tick_size)
        if d.textlength(TICKER, font=f_tick) <= 940:
            break
        tick_size -= 1
    d.text((W // 2, ty + 22), TICKER, font=f_tick, fill=WHITE, anchor="mm")
    # footer
    f_foot = font(SANS, 14)
    d.text((W // 2, H - 38), "Sources: Reuters \u00b7 Yeni Safak \u00b7 Times of India \u00b7 One Turn \u00b7 24 Nov 2026",
           font=f_foot, fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
