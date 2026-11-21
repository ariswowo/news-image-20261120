#!/usr/bin/env python3
"""Sum up 20 November 2026's world news in one image.

make.fun bounty: news-image-20261120
  "Sum up 20 November's world news in one image"
  Deadline: 2026-11-22T00:00:00Z. Pot: $250 (top 50 share it).

Writes exactly one image to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png), 1024 x 1024, PNG, <= 1 MiB.

Determinism: no network, no clock, no randomness, no unordered
iteration. The news text is fixed in this file (see NEWS.md for the
sources). The image is drawn with Pillow using the DejaVu fonts
bundled in fonts/ next to this file, so rendering does not depend on
whatever fonts the grader image happens to ship.

Fallback: if Pillow (or a bundled font) is unavailable in the grading
environment, the program copies the pre-rendered entry.png committed
in this repository instead. That file is byte-for-byte the output of
this same program, so both paths write identical bytes.

Run:  python3 main.py
      MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT_PATH = OUT_DIR / "entry.png"
ASSET = BASE / "entry.png"

W, H = 1024, 1024

# --- palette -------------------------------------------------------------
PAPER = (246, 241, 227)
INK = (20, 20, 20)
MUTED = (90, 84, 70)
RED = (180, 35, 24)
NAVY = (27, 58, 92)
TEAL = (14, 107, 107)
CARD = (255, 253, 247)
LINE = (200, 190, 168)
GOLD = (176, 132, 8)


def _fonts():
    from PIL import ImageFont

    def load(name, size):
        return ImageFont.truetype(str(BASE / "fonts" / name), size)

    return {
        "serif_b": lambda s: load("DejaVuSerif-Bold.ttf", s),
        "serif": lambda s: load("DejaVuSerif.ttf", s),
        "sans_b": lambda s: load("DejaVuSans-Bold.ttf", s),
        "sans": lambda s: load("DejaVuSans.ttf", s),
    }


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, max_w, leading, fill=INK):
    """Draw wrapped paragraph; return y just below the last line."""
    for line in wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, font, max_w, leading):
    return para(draw, x, y, text, font, max_w, leading)


def chip(draw, x, y, text, colour):
    f = _F["sans_b"](16)
    w = int(draw.textlength(text, font=f)) + 20
    draw.rounded_rectangle([x, y, x + w, y + 26], radius=4, fill=colour)
    draw.text((x + 10, y + 4), text, font=f, fill=(255, 255, 255))
    return w


def card(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6,
                           fill=CARD, outline=LINE, width=1)
    return x + 22, y + 18, w - 44  # inner x, y, text width


def render():
    from PIL import Image, ImageDraw

    global _F
    _F = _fonts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 34  # margin
    CW = W - 2 * M  # 956

    # --- masthead ------------------------------------------------------
    f_date = _F["sans_b"](20)
    date_line = "F R I D A Y  •  2 0  N O V E M B E R  2 0 2 6"
    d.text(((W - d.textlength(date_line, font=f_date)) / 2, 22),
           date_line, font=f_date, fill=RED)
    f_title = _F["serif_b"](52)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_title)) / 2, 48),
           title, font=f_title, fill=INK)
    d.rectangle([M, 112, W - M, 116], fill=RED)
    d.rectangle([M, 119, W - M, 120], fill=INK)

    # --- ticker --------------------------------------------------------
    d.rectangle([M, 128, W - M, 154], fill=NAVY)
    f_tick = _F["sans_b"](18)
    tick = "KYIV   •   SHENZHEN   •   THE HAGUE   •   NEW YORK   •   ODISHA   •   RIYADH"
    d.text(((W - d.textlength(tick, font=f_tick)) / 2, 132),
           tick, font=f_tick, fill=(255, 255, 255))

    # --- lead story ----------------------------------------------------
    lx, ly, lw, lh = M, 164, CW, 258
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=6,
                        fill=CARD, outline=LINE, width=1)
    d.rectangle([lx, ly + 6, lx + 7, ly + lh - 6], fill=RED)
    tx = lx + 24
    chip(d, tx, ly + 18, "LEAD  —  WAR IN UKRAINE", RED)
    y = headline(d, tx, ly + 52,
                 "Kyiv's bridges hit in Russia's biggest barrage of November",
                 _F["serif_b"](32), 620, 38)
    y = para(d, tx, y + 6,
             "Overnight into Friday, Russia fired 404 drones and 111 missiles "
             "— including 27 ballistic — at Ukraine. Three bridges over the "
             "Dnipro in Kyiv were damaged, power and heating failed, and at "
             "least 8 people were killed, nearly 30 injured.",
             _F["sans"](18), 620, 23)
    para(d, tx, y + 6,
         "Two missiles and a jet drone fell in Poland — no casualties.",
         _F["sans_b"](17), 620, 23)
    # stat tiles, right of the lead text
    sx, sy = lx + 668, ly + 62
    stats = [("404", "drones fired"), ("111", "missiles fired"),
             ("3", "Kyiv bridges hit"), ("8", "people killed")]
    tw, th, gap = 132, 78, 12
    for i, (num, lab) in enumerate(stats):
        x0 = sx + (i % 2) * (tw + gap)
        y0 = sy + (i // 2) * (th + gap)
        d.rounded_rectangle([x0, y0, x0 + tw, y0 + th], radius=6,
                            fill=(238, 231, 214), outline=LINE, width=1)
        d.text((x0 + 12, y0 + 8), num, font=_F["sans_b"](30), fill=RED)
        d.text((x0 + 12, y0 + 46), lab, font=_F["sans"](15), fill=INK)

    # --- row 2: diplomacy / justice ------------------------------------
    ry, rh = 434, 224
    col_w = (CW - 16) // 2  # 470
    # Shenzhen
    ix, iy, iw = card(d, M, ry, col_w, rh)
    chip(d, ix, iy, "DIPLOMACY  —  SHENZHEN", NAVY)
    y = headline(d, ix, iy + 36,
                 "Three leaders, one declaration — and no plan for Ukraine",
                 _F["serif_b"](24), iw, 29)
    para(d, ix, y + 6,
         "Trump, Xi and Putin met for 90 minutes on 19 Nov, their first "
         "three-way summit. Their declaration backs UN reform, more fuel "
         "supply, limits on courts trying officials, and nuclear-risk "
         "talks. It sets no timetable — and never mentions the war in "
         "Ukraine.",
         _F["sans"](16), iw, 21)
    # ICJ
    ix2, iy2, iw2 = card(d, M + col_w + 16, ry, col_w, rh)
    chip(d, ix2, iy2, "JUSTICE  —  THE HAGUE", TEAL)
    y = headline(d, ix2, iy2 + 36,
                 "World court: Myanmar committed genocide",
                 _F["serif_b"](24), iw2, 29)
    para(d, ix2, y + 6,
         "The ICJ ruled 9–6 on 19 Nov that Myanmar committed genocide "
         "against the Rohingya — the first time it has held a state guilty "
         "of genocide. It ordered reparations and the refugees' safe "
         "return. Myanmar called the verdict “unfair”.",
         _F["sans"](16), iw2, 21)

    # --- row 3: markets / cyclone --------------------------------------
    ry3, rh3 = 670, 220
    ix, iy, iw = card(d, M, ry3, col_w, rh3)
    chip(d, ix, iy, "MARKETS  —  NEW YORK", RED)
    y = headline(d, ix, iy + 36,
                 "AI sell-off drags Wall Street into correction",
                 _F["serif_b"](24), iw, 29)
    y = para(d, ix, y + 6,
             "The S&P 500 fell 3.7% on Friday, its seventh straight loss — "
             "more than 10% below its October high. The Nasdaq wiped out all "
             "its 2026 gains.",
             _F["sans"](16), iw, 21)
    # mini bar chart: Friday's falls
    for j, (lab, val, frac) in enumerate(
            [("S&P 500", "-3.7%", 0.74), ("Nikkei", "-5.1%", 1.0)]):
        by = y + 4 + j * 22
        d.text((ix, by), lab, font=_F["sans_b"](15), fill=INK)
        d.rectangle([ix + 82, by + 3, ix + 82 + 150, by + 15],
                    fill=(232, 226, 210))
        d.rectangle([ix + 82, by + 3, ix + 82 + int(150 * frac), by + 15],
                    fill=RED)
        d.text((ix + 240, by), val, font=_F["sans_b"](15), fill=RED)
    # Akvan
    ix2, iy2, iw2 = card(d, M + col_w + 16, ry3, col_w, rh3)
    chip(d, ix2, iy2, "WEATHER  —  INDIA", TEAL)
    y = headline(d, ix2, iy2 + 36,
                 "Cyclone Akvan hits Odisha; 300,000 moved to safety",
                 _F["serif_b"](24), iw2, 29)
    para(d, ix2, y + 6,
         "Akvan hit the coast near Gopalpur on Friday morning, winds "
         "70–80 km/h, gusting to 90. About 300,000 people were evacuated "
         "to 2,500+ relief camps. No major damage was reported.",
         _F["sans"](16), iw2, 21)

    # --- bottom strip: Gulf + also --------------------------------------
    by, bh = 896, 72
    d.rounded_rectangle([M, by, W - M, by + bh], radius=6, fill=NAVY)
    d.text((M + 18, by + 10), "GULF ON EDGE",
           font=_F["sans_b"](17), fill=(255, 205, 100))
    para(d, M + 18, by + 32,
         "Saudi-led forces shot down three Houthi missiles aimed at Riyadh, "
         "the third night of alerts, as the US–Iran war kept Hormuz on edge.",
         _F["sans"](15), 560, 19, fill=(255, 255, 255))
    d.line([M + 606, by + 12, M + 606, by + bh - 12], fill=(120, 140, 170),
           width=1)
    d.text((M + 622, by + 10), "ALSO", font=_F["sans_b"](17),
           fill=(255, 205, 100))
    para(d, M + 622, by + 32,
         "M6.7 quake in Peru • Kenya: 42 days to Ebola-free • Kerch rail "
         "resumes.",
         _F["sans"](15), 318, 19, fill=(255, 255, 255))

    # --- footer ----------------------------------------------------------
    f_foot = _F["sans"](13)
    foot = ("Friday 20 November 2026  •  Facts checked against reporting of 20–21 Nov 2026  •  "
            "One image, six stories")
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 976),
           foot, font=f_foot, fill=MUTED)
    return img


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if os.environ.get("MAKEFUN_FORCE_COPY") == "1":
        shutil.copyfile(ASSET, OUT_PATH)
        print(f"copied {ASSET} -> {OUT_PATH}")
        return 0
    try:
        img = render()
    except Exception as exc:  # Pillow / fonts missing in grader image
        print(f"render unavailable ({exc}); copying pre-rendered asset",
              file=sys.stderr)
        if not ASSET.is_file():
            raise
        shutil.copyfile(ASSET, OUT_PATH)
        print(f"copied {ASSET} -> {OUT_PATH}")
        return 0
    img.save(OUT_PATH, format="PNG", compress_level=9)
    print(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
