#!/usr/bin/env python3
"""ONE DAY - front page for Tuesday 17 November 2026.

Magazine-cover style front page: one big drawn scene (the Kerch Bridge
strike) up top, a single dominant headline, two second stories, and a
four-item news strip at the bottom. Everything is drawn with PIL from
scratch - no photos, no network, no timestamps - so the output is
byte-identical on every run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (247, 243, 234)      # warm cream
INK = (20, 28, 44)           # deep navy ink
RED = (193, 39, 45)          # accent red
TEAL = (46, 110, 126)        # sea teal
GOLD = (201, 141, 32)        # small accent
GREY = (92, 96, 104)
LIGHT_LINE = (180, 175, 160)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, fill, max_w, leading):
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_bridge_scene(d, x0, y0, x1, y1):
    """Flat illustration: a suspension bridge with its middle span
    collapsed into the strait, smoke rising, sea below."""
    pw, ph = x1 - x0, y1 - y0
    # sky: soft vertical gradient, pale blue to warm horizon
    top = (176, 208, 224)
    bot = (240, 228, 205)
    for i in range(ph):
        t = i / max(ph - 1, 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)
    # pale sun, upper right
    sx, sy, sr = x0 + int(pw * 0.82), y0 + int(ph * 0.16), 34
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(244, 214, 130))
    d.ellipse([sx - sr - 10, sy - sr - 10, sx + sr + 10, sy + sr + 10],
              outline=(244, 214, 130), width=3)
    # distant headlands
    d.polygon([(x0, y0 + int(ph * 0.52)), (x0 + int(pw * 0.16), y0 + int(ph * 0.40)),
               (x0 + int(pw * 0.30), y0 + int(ph * 0.52))], fill=(141, 158, 168))
    d.polygon([(x1, y0 + int(ph * 0.52)), (x1 - int(pw * 0.14), y0 + int(ph * 0.42)),
               (x1 - int(pw * 0.28), y0 + int(ph * 0.52))], fill=(141, 158, 168))
    # sea
    sea_y = y0 + int(ph * 0.52)
    d.rectangle([x0, sea_y, x1, y1], fill=TEAL)
    for j, wy in enumerate((0.14, 0.38, 0.62, 0.86)):
        yy = sea_y + int((y1 - sea_y) * wy)
        col = (120, 175, 185) if j % 2 == 0 else (88, 150, 163)
        for k in range(6):
            wx = x0 + 30 + k * 160 + (40 if j % 2 else 0)
            d.arc([wx, yy - 7, wx + 70, yy + 7], 180, 360, fill=col, width=3)
    # bridge geometry
    deck_y = y0 + int(ph * 0.46)
    t1x = x0 + int(pw * 0.24)
    t2x = x0 + int(pw * 0.74)
    tower_top = y0 + int(ph * 0.10)
    tower_bot = deck_y + 26
    # towers
    for tx in (t1x, t2x):
        d.rectangle([tx - 9, tower_top, tx + 9, tower_bot], fill=INK)
        d.rectangle([tx - 34, tower_top + 26, tx + 34, tower_top + 38], fill=INK)
        d.rectangle([tx - 34, tower_top + 84, tx + 34, tower_top + 96], fill=INK)
    # main cables: gentle sag between towers, and out to the edges
    def cable(xa, ya, xb, yb, sag):
        pts = []
        for i in range(41):
            t = i / 40.0
            x = xa + (xb - xa) * t
            y = ya + (yb - ya) * t + sag * 4 * t * (1 - t)
            pts.append((x, y))
        d.line(pts, fill=INK, width=4)

    cable(x0, deck_y - 6, t1x, tower_top + 4, 26)
    cable(t1x, tower_top + 4, t2x, tower_top + 4, 44)
    cable(t2x, tower_top + 4, x1, deck_y - 6, 26)
    # hangers on the intact spans
    for i in range(1, 8):
        t = i / 8.0
        hx = x0 + (t1x - x0) * t
        hy = deck_y - 6 + 26 * 4 * t * (1 - t) * 0.28
        d.line([(hx, hy), (hx, deck_y)], fill=INK, width=2)
    for i in range(1, 8):
        t = i / 8.0
        hx = t2x + (x1 - t2x) * t
        hy = deck_y - 6 + 26 * 4 * t * (1 - t) * 0.28
        d.line([(hx, hy), (hx, deck_y)], fill=INK, width=2)
    # deck: intact left and right, middle span broken away
    gap_l = x0 + int(pw * 0.40)
    gap_r = x0 + int(pw * 0.60)
    d.rectangle([x0, deck_y, gap_l, deck_y + 12], fill=INK)
    d.rectangle([gap_r, deck_y, x1, deck_y + 12], fill=INK)
    # jagged broken ends
    d.polygon([(gap_l - 16, deck_y), (gap_l, deck_y), (gap_l - 4, deck_y + 22),
               (gap_l - 20, deck_y + 12)], fill=INK)
    d.polygon([(gap_r + 16, deck_y), (gap_r, deck_y), (gap_r + 4, deck_y + 22),
               (gap_r + 20, deck_y + 12)], fill=INK)
    # fallen span, tilted into the water
    fx0, fy0 = gap_l + 26, deck_y + 52
    fx1, fy1 = gap_r - 8, deck_y + 118
    d.line([(fx0, fy0), (fx1, fy1)], fill=(60, 66, 76), width=12)
    d.line([(fx0, fy0), (fx1, fy1)], fill=(120, 128, 138), width=4)
    # debris + splash
    for (dx, dy, r) in ((gap_l + 60, deck_y + 96, 10), (gap_l + 110, deck_y + 112, 7),
                        (gap_l + 150, deck_y + 100, 9), (gap_l + 88, deck_y + 128, 6)):
        d.ellipse([dx - r, dy - r, dx + r, dy + r], fill=(90, 98, 108))
    # fire glow at the break + smoke puffs
    d.ellipse([gap_l - 6, deck_y - 26, gap_l + 26, deck_y + 6], fill=(232, 110, 30))
    d.ellipse([gap_l + 2, deck_y - 18, gap_l + 18, deck_y - 2], fill=(245, 178, 60))
    smoke = [(gap_l + 8, deck_y - 52, 24), (gap_l + 34, deck_y - 78, 30),
             (gap_l + 66, deck_y - 98, 32), (gap_l + 100, deck_y - 112, 26)]
    for (cx, cy, r) in smoke:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(226, 224, 220))
        d.ellipse([cx - r + 8, cy - r + 8, cx + r - 6, cy + r - 6], fill=(205, 203, 198))
    # caption chip inside the scene
    chip = "KERCH STRAIT  -  UKRAINE STRIKES FOR A SECOND DAY"
    cf = font(SANS_B, 19)
    tw = d.textlength(chip, font=cf)
    d.rectangle([x0 + 18, y1 - 46, x0 + 34 + int(tw), y1 - 14], fill=INK)
    d.text((x0 + 26, y1 - 41), chip, font=cf, fill=(255, 255, 255))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36                      # side margin
    rx = W - mx

    # ---- masthead ----
    rule(d, mx, 30, rx, 6)
    d.text((mx, 44), "ONE DAY", font=font(SERIF_B, 96), fill=INK)
    d.text((rx - 330, 66), "TUESDAY", font=font(SANS_B, 30), fill=RED)
    d.text((rx - 330, 100), "17 NOV 2026", font=font(SANS_B, 30), fill=INK)
    rule(d, mx, 152, rx, 2)
    tag = "THE WORLD IN ONE PAGE  -  EVERY STORY THAT MATTERED TODAY"
    d.text((mx, 162), tag, font=font(SANS_B, 20), fill=GREY)

    # ---- hero scene ----
    draw_bridge_scene(d, mx, 196, rx, 540)

    # ---- dominant headline ----
    y = 556
    d.text((mx, y), "UKRAINE  -  WAR IN EUROPE", font=font(SANS_B, 22), fill=RED)
    y = 584
    d.text((mx, y), "KERCH BRIDGE DOWN", font=font(SANS_B, 78), fill=INK)
    y = 674
    y = para(d, mx, y,
             "A road span collapses into the strait as Ukrainian drones strike the "
             "bridge to Crimea for a second day. Two killed; Russia shuts all traffic.",
             font(SERIF, 26), INK, rx - mx, 34)

    rule(d, mx, 792, rx, 2)

    # ---- two second stories ----
    col_w = (rx - mx - 30) // 2
    y2 = 808
    d.text((mx, y2), "ASIA  -  DIPLOMACY", font=font(SANS_B, 19), fill=RED)
    d.text((mx, y2 + 26), "TRUMP LANDS", font=font(SANS_B, 34), fill=INK)
    d.text((mx, y2 + 66), "IN MANILA", font=font(SANS_B, 34), fill=INK)
    para(d, mx, y2 + 106,
         "Arrives for the ASEAN summit and signs a trade pact with Thailand.",
         font(SERIF, 21), INK, col_w, 27)

    x2 = mx + col_w + 30
    d.line([(x2 - 15, y2), (x2 - 15, 968)], fill=LIGHT_LINE, width=2)
    d.text((x2, y2), "MIDDLE EAST  -  SHIPPING", font=font(SANS_B, 19), fill=RED)
    d.text((x2, y2 + 26), "HORMUZ: TANKERS", font=font(SANS_B, 34), fill=INK)
    d.text((x2, y2 + 66), "ABLAZE", font=font(SANS_B, 34), fill=INK)
    para(d, x2, y2 + 106,
         "Two tankers struck mines in the strait and caught fire. A third US "
         "carrier arrives.",
         font(SERIF, 21), INK, col_w, 27)

    rule(d, mx, 980, rx, 2)
    d.text((mx, 990), "VULCAN FAILS  -  40 SATELLITES LOST   |   XI, TRUMP & PUTIN TO MEET   |   JAPAN SCRAMBLES JETS   |   EBOLA DOUBLES IN CONGO",
           font=font(SANS_B, 13), fill=GREY)

    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, "entry.png"))


if __name__ == "__main__":
    main()
