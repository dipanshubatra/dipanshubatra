#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W, H = 1000, 126
BG = (13, 17, 23)
WHITE = (235, 241, 248)
MUTED = (132, 146, 164)
LINE = (39, 51, 68)
items = [
    (7, "x", "HACKATHON WINS", "national-level winner", (34, 211, 238)),
    (4, "", "ECSOC '26 GLOBAL RANK", "Tier 1 Developer", (245, 185, 66)),
    (16, "K+", "LINKEDIN FOLLOWERS", "building in public", (167, 139, 250)),
    (16, "+", "OPEN-SOURCE PROJECTS", "Java / Spring ecosystem", (244, 114, 182)),
]
font_dir = Path("/usr/share/fonts/truetype/dejavu")
bold = ImageFont.truetype(str(font_dir / "DejaVuSans-Bold.ttf"), 39)
label_font = ImageFont.truetype(str(font_dir / "DejaVuSans-Bold.ttf"), 10)
sub_font = ImageFont.truetype(str(font_dir / "DejaVuSans.ttf"), 10)
micro_font = ImageFont.truetype(str(font_dir / "DejaVuSans-Bold.ttf"), 8)

def ease(t):
    return 1 - (1-t)**3

def render(progress):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((18, 7), "SELECTED HIGHLIGHTS", font=micro_font, fill=(100, 116, 139))
    tag = "PROOF > PROMISES"
    tw = d.textbbox((0, 0), tag, font=micro_font)[2]
    d.text((W-18-tw, 7), tag, font=micro_font, fill=(100, 116, 139))
    # Thin four-tone spectrum rail.
    stops = [(34,211,238), (245,185,66), (167,139,250), (244,114,182)]
    for x in range(18, 982):
        p = (x-18)/964*3
        idx = min(int(p), 2)
        t = p-idx
        col = tuple(int(stops[idx][k]*(1-t)+stops[idx+1][k]*t) for k in range(3))
        d.line((x, 24, x, 26), fill=col)
    for i, (target, suffix, label, sub, color) in enumerate(items):
        x = 18 + i*250
        if i:
            d.line((x, 43, x, 111), fill=LINE, width=1)
        start = 4 + i*3
        t = max(0.0, min(1.0, (progress-start)/22))
        value = int(round(target*ease(t)))
        value_text = f"{value}{suffix}"
        d.text((x+22, 37), value_text, font=bold, fill=color, stroke_width=0)
        d.ellipse((x+23, 91, x+27, 95), fill=color)
        d.text((x+34, 88), label, font=label_font, fill=WHITE)
        d.text((x+22, 105), sub, font=sub_font, fill=MUTED)
    return im

frames = []
# Brief pause before the figures start, then staggered count-up.
for _ in range(10):
    frames.append(render(-1))
for step in range(34):
    frames.append(render(step))
frames.append(render(80))
out = Path("assets/ui/metrics-countup.gif")
out.parent.mkdir(parents=True, exist_ok=True)
frames[0].save(out, save_all=True, append_images=frames[1:], duration=[90]*10+[65]*34+[5000], optimize=True, disposal=2)
print(f"created {out} with {len(frames)} frames")
