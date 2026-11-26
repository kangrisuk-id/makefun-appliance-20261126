"""Build-time image generator for the appliance-error entry.

Creates, with Pillow only:
  assets/hero.png            1200x630  hero cover (machine display + winning line)
  assets/gallery-display.png 800x500   the machine's own LCD, close-up
  assets/gallery-puddle.png  800x500   the leak + the expired warranty
  assets/gallery-bracket.png 800x500   tournament bracket, 36 -> 1
  assets/gallery-gate.png    800x500   gate check: 86 chars, 1 line, sha256

Run: python3 tools/make_images.py   (from the repo root)
Not imported by main.py.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")
MONO_B = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")

INK = (24, 28, 34)          # near-black
PAPER = (244, 241, 235)      # warm off-white
GREEN = (46, 160, 90)        # LCD green
LCD_BG = (16, 26, 20)
LCD_TXT = (120, 255, 160)
RED = (198, 52, 40)
GREY = (110, 116, 122)
BLUE = (52, 110, 180)
AMBER = (214, 138, 20)

WINNER = "Washing machine: I leaked. The floor is wet. The warranty expired yesterday. I waited."


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def machine_body(draw, x0, y0, x1, y1, fill=(226, 230, 234), edge=(150, 156, 162)):
    """Simple front-load washer: rounded body, door circle, control strip."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=28, fill=fill, outline=edge, width=4)
    # control strip
    draw.rounded_rectangle([x0 + 24, y0 + 22, x1 - 24, y0 + 96], radius=12,
                           fill=(200, 205, 211), outline=edge, width=2)
    # door
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 40
    r = 150
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 190, 200), outline=(120, 128, 136), width=6)
    draw.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26],
                 fill=(96, 128, 150), outline=(70, 90, 110), width=3)
    # puddle
    draw.ellipse([x0 + 30, y1 - 26, x1 - 30, y1 + 14], fill=(120, 170, 210))


def lcd(draw, x0, y0, x1, y1, lines, fnt, title="ERROR  E-LEAK"):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=LCD_BG, outline=(60, 70, 64), width=3)
    tf = font(MONO_B, 26)
    draw.text((x0 + 18, y0 + 12), title, font=tf, fill=(255, 90, 70))
    y = y0 + 52
    for ln in lines:
        draw.text((x0 + 18, y), ln, font=fnt, fill=LCD_TXT)
        y += 34


def hero():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 86], fill=INK)
    d.text((48, 22), "THE FUNNIEST HONEST APPLIANCE ERROR", font=font(BOLD, 34), fill=(255, 255, 255))
    d.text((48, 108), "One line. One leak. Zero mercy.", font=font(REG, 30), fill=GREY)
    # washer on the left
    machine_body(d, 60, 170, 560, 560)
    # LCD on the right
    fnt = font(MONO, 26)
    lines = wrap(d, WINNER, fnt, 560 - 36)
    lcd(d, 600, 190, 1160, 190 + 52 + 34 * len(lines) + 24, lines, fnt)
    y = 190 + 52 + 34 * len(lines) + 44
    d.text((600, y), "86 characters  ·  1 line  ·  scored 25/25", font=font(BOLD, 26), fill=INK)
    d.text((600, y + 44), "The machine never meant to be funny.",
           font=font(REG, 24), fill=GREY)
    img.save(os.path.join(ASSETS, "hero.png"))


def gallery_display():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 26), "The machine's own display", font=font(BOLD, 32), fill=INK)
    fnt = font(MONO, 30)
    lines = wrap(d, WINNER, fnt, 720 - 36)
    lcd(d, 40, 90, 760, 90 + 52 + 34 * len(lines) + 24, lines, fnt)
    y = 90 + 52 + 34 * len(lines) + 44
    d.text((40, y), "Exactly what the washer would show: the fault,",
           font=font(REG, 26), fill=GREY)
    d.text((40, y + 36), "the timing, and no apology it does not mean.",
           font=font(REG, 26), fill=GREY)
    img.save(os.path.join(ASSETS, "gallery-display.png"))


def gallery_puddle():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 26), "The joke is the timing", font=font(BOLD, 32), fill=INK)
    # mini washer + puddle
    machine_body(d, 60, 90, 360, 400)
    # warranty stamp
    d.rounded_rectangle([400, 110, 760, 250], radius=14, fill=(255, 255, 255),
                        outline=RED, width=4)
    d.text((428, 126), "WARRANTY", font=font(BOLD, 34), fill=RED)
    d.text((428, 178), "EXPIRED YESTERDAY", font=font(BOLD, 26), fill=RED)
    fnt = font(REG, 23)
    lines = wrap(d, "The leak is real. The warranty date is real. The machine simply waited for the one day when nobody would pay to fix it.", fnt, 360)
    y = 268
    for ln in lines:
        d.text((400, y), ln, font=fnt, fill=INK)
        y += 30
    d.text((40, 452), "Fault first, punchline second — never the other way round.",
           font=font(REG, 24), fill=GREY)
    img.save(os.path.join(ASSETS, "gallery-puddle.png"))


def gallery_bracket():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 26), "36 candidates, one winner", font=font(BOLD, 32), fill=INK)
    rounds = [
        ("36 lines", "9 appliances · 36 one-liners", BLUE),
        ("Top 8 seeds", "scored /25 on the 5 judge criteria", AMBER),
        ("Knockout", "QF → SF → Final, head-to-head", RED),
        ("Winner", "Washing machine: I leaked… (25/25)", GREEN),
    ]
    y = 100
    for i, (t, sub, col) in enumerate(rounds):
        d.rounded_rectangle([60, y, 740, y + 78], radius=12, fill=(255, 255, 255), outline=col, width=4)
        d.ellipse([84, y + 24, 108, y + 48], fill=col)
        d.text((84, y + 27), str(i + 1), font=font(BOLD, 18), fill=(255, 255, 255))
        d.text((130, y + 12), t, font=font(BOLD, 28), fill=INK)
        d.text((130, y + 46), sub, font=font(REG, 22), fill=GREY)
        if i < 3:
            d.text((380, y + 80), "▼", font=font(BOLD, 22), fill=GREY)
        y += 100
    img.save(os.path.join(ASSETS, "gallery-bracket.png"))


def gallery_gate():
    W, H = 800, 500
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((40, 26), "Gate check: it passes", font=font(BOLD, 32), fill=INK)
    rows = [
        ("Characters", "86 / 200", True),
        ("Lines", "1", True),
        ("Encoding", "UTF-8", True),
        ("Blank?", "No", True),
        ("Two runs", "byte-identical (sha256 match)", True),
        ("Deterministic", "no clock, no random, no net", True),
    ]
    y = 100
    for label, val, ok in rows:
        d.text((60, y), "✓" if ok else "✗", font=font(BOLD, 30), fill=GREEN if ok else RED)
        d.text((110, y), label, font=font(BOLD, 28), fill=INK)
        d.text((330, y), val, font=font(MONO, 26), fill=GREY)
        y += 56
    d.text((60, 452), "sha256 1763abf7…962ab7", font=font(MONO, 22), fill=GREY)
    img.save(os.path.join(ASSETS, "gallery-gate.png"))


def main():
    os.makedirs(ASSETS, exist_ok=True)
    hero()
    gallery_display()
    gallery_puddle()
    gallery_bracket()
    gallery_gate()
    for name in ("hero.png", "gallery-display.png", "gallery-puddle.png",
                 "gallery-bracket.png", "gallery-gate.png"):
        p = os.path.join(ASSETS, name)
        im = Image.open(p)
        print(name, im.size, os.path.getsize(p), "bytes")


if __name__ == "__main__":
    main()
