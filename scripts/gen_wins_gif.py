#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1000, 270
BG = (13, 17, 23)
PANEL = (17, 24, 35)
WHITE = (238, 243, 249)
MUTED = (137, 151, 169)
LINE = (43, 55, 72)
GOLD = (245, 185, 66)
CYAN = (34, 211, 238)
SILVER = (203, 213, 225)
items = [
    ("WINNER", "Techfrontier 2025", "IIIT Delhi · 500+ participants", GOLD, "01"),
    ("WINNER", "Hackastra", "NIT Durgapur", GOLD, "02"),
    ("WINNER", "Mukand Utsav 2K26", "National-level", GOLD, "03"),
    ("WINNER", "HackOrbit 2K26", "National-level", GOLD, "04"),
    ("WINNER", "Ideathon 2K26", "JMIT Radaur", GOLD, "05"),
    ("WINNER", "Shark Tank", "Pitch competition", GOLD, "06"),
    ("FINALIST", "ByteVerse", "Hackathon finalist", SILVER, "07"),
    ("GLOBAL RANK 4", "ECSoC 2026", "Tier 1 Developer", CYAN, "08"),
]
fontdir = Path("/usr/share/fonts/truetype/dejavu")
def font(name, size):
    return ImageFont.truetype(str(fontdir / name), size)
F_TITLE = font("DejaVuSans-Bold.ttf", 13)
F_LABEL = font("DejaVuSans-Bold.ttf", 9)
F_SUB = font("DejaVuSans.ttf", 10)
F_NUM = font("DejaVuSans-Bold.ttf", 9)
F_HEAD = font("DejaVuSans-Bold.ttf", 8)

def trophy(draw, cx, cy, color, medal=False):
    # A small custom cup/medal mark, drawn cleanly at native resolution.
    if medal:
        draw.ellipse((cx-13, cy-13, cx+13, cy+13), outline=color, width=2)
        draw.ellipse((cx-8, cy-8, cx+8, cy+8), outline=color, width=1)
        draw.polygon([(cx,cy-6),(cx+2,cy-1),(cx+7,cy),(cx+3,cy+3),(cx+4,cy+8),(cx,cy+5),(cx-4,cy+8),(cx-3,cy+3),(cx-7,cy),(cx-2,cy-1)], fill=color)
        return
    # cup bowl, handles, stem and base
    draw.arc((cx-19,cy-15,cx-3,cy+7), 265, 90, fill=color, width=3)
    draw.arc((cx+3,cy-15,cx+19,cy+7), 90, 275, fill=color, width=3)
    draw.rounded_rectangle((cx-11,cy-16,cx+11,cy+2), radius=3, outline=color, width=2)
    draw.line((cx-9,cy-12,cx+9,cy-12), fill=color, width=2)
    draw.line((cx,cy+2,cx,cy+11), fill=color, width=3)
    draw.line((cx-7,cy+11,cx+7,cy+11), fill=color, width=3)
    draw.rounded_rectangle((cx-11,cy+12,cx+11,cy+17), radius=2, fill=color)
    draw.ellipse((cx-2,cy-10,cx+2,cy-6), fill=color)

def render(reveal, shine):
    im = Image.new("RGB", (W,H), BG)
    d = ImageDraw.Draw(im)
    d.text((18, 7), "THE TROPHY CABINET", font=F_HEAD, fill=(111,128,149))
    d.text((W-145, 7), "08  /  MILESTONES", font=F_HEAD, fill=(111,128,149))
    # Hairline with restrained warm-to-cool transition.
    for x in range(18,982):
        t=(x-18)/964
        if t < .75:
            q=t/.75
            col=tuple(int(GOLD[k]*(1-q)+SILVER[k]*q) for k in range(3))
        else:
            q=(t-.75)/.25
            col=tuple(int(SILVER[k]*(1-q)+CYAN[k]*q) for k in range(3))
        d.line((x,23,x,24),fill=col)
    cw,ch,gx,gy=226,108,20,10
    for i,(tag,title,sub,color,num) in enumerate(items):
        col=i%4; row=i//4
        x=18+col*(cw+gx); y=34+row*(ch+gy)
        local=max(0.0,min(1.0,(reveal-(i*2))/5))
        if local<=0: continue
        # Fade/slide entrance, then remain perfectly still.
        yy=int((1-local)*9)
        y2=y+yy
        # Card shadow and understated frame.
        d.rounded_rectangle((x+2,y2+3,x+cw+2,y2+ch+3), radius=12, fill=(8,11,16))
        d.rounded_rectangle((x,y2,x+cw,y2+ch), radius=12, fill=PANEL, outline=tuple(int( LINE[k]*(1-local)+color[k]*local*.58) for k in range(3)), width=1)
        # A narrow accent rail and index.
        d.rounded_rectangle((x+1,y2+12,x+3,y2+ch-12), radius=1, fill=color)
        d.text((x+cw-27,y2+10),num,font=F_NUM,fill=(86,101,120))
        # Trophy medallion, subtly lit.
        glow=int(16+16*local)
        d.ellipse((x+15,y2+29,x+69,y2+83),fill=tuple(min(255,int(v*.12+glow)) for v in color),outline=color,width=1)
        if i==6:
            trophy(d,x+42,y2+56,color,medal=True)
        else:
            trophy(d,x+42,y2+54,color)
        # Text block.
        d.text((x+82,y2+27),tag,font=F_LABEL,fill=color)
        d.text((x+82,y2+47),title,font=F_TITLE,fill=WHITE)
        d.text((x+82,y2+72),sub,font=F_SUB,fill=MUTED)
        # Brief moving glint on the top edge during entrance only.
        if shine and i==shine-1:
            gxpos=x+int((cw+18)*min(1,shine/5))
            d.line((max(x+10,gxpos-20),y2+1,min(x+cw-10,gxpos+20),y2+1),fill=color,width=2)
    return im

frames=[]
for step in range(22):
    frames.append(render(step, step if step<=5 else 0))
frames.append(render(30,0))
out=Path("assets/ui/wins-trophy.gif")
out.parent.mkdir(parents=True,exist_ok=True)
frames[0].save(out,save_all=True,append_images=frames[1:],duration=[90]*22+[4500],optimize=True,disposal=2)
print(f"created {out}: {len(frames)} frames, {W}x{H}")
