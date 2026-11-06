#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W,H=1000,420
BG=(13,17,23)
WHITE=(242,246,252)
MUTED=(164,177,194)
GOLD=(255,193,55)
CYAN=(34,211,238)
SILVER=(215,222,232)
fd=Path("/usr/share/fonts/truetype/dejavu")
emoji_path="/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
emoji=ImageFont.truetype(emoji_path,109)
title_font=ImageFont.truetype(str(fd/"DejaVuSans-Bold.ttf"),16)
sub_font=ImageFont.truetype(str(fd/"DejaVuSans.ttf"),12)
tag_font=ImageFont.truetype(str(fd/"DejaVuSans-Bold.ttf"),9)
head_font=ImageFont.truetype(str(fd/"DejaVuSans-Bold.ttf"),10)
items=[
 ("🏆","Techfrontier 2025","IIIT Delhi · Winner","WINNER",GOLD),
 ("🏆","Hackastra","NIT Durgapur · Winner","WINNER",GOLD),
 ("🏆","Mukand Utsav 2K26","National-level · Winner","WINNER",GOLD),
 ("🏆","HackOrbit 2K26","National-level · Winner","WINNER",GOLD),
 ("🏆","Ideathon 2K26","JMIT Radaur · Winner","WINNER",GOLD),
 ("🏆","Shark Tank","Pitch competition · Winner","WINNER",GOLD),
 ("🏆","ByteVerse","Hackathon finalist","FINALIST",SILVER),
 ("🏆","ECSoC 2026","Global Rank #4 · Tier 1","GLOBAL RANK #4",GOLD),
]

def render(frame):
    im=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(im)
    d.text((20,10),"ACHIEVEMENTS",font=head_font,fill=(139,155,176))
    d.text((W-143,10),"08  /  MILESTONES",font=head_font,fill=(139,155,176))
    d.line((20,31,980,31),fill=(43,55,72),width=1)
    for i,(symbol,title,sub,tag,color) in enumerate(items):
        col=i%4; row=i//4
        cx=125+col*250
        top=39+row*190
        # Staggered spring-like entrance, then a small settle.
        elapsed=frame-i*2.5
        if elapsed<0: continue
        t=min(1.0,elapsed/9.0)
        ease=1-(1-t)**3
        bounce=math.sin(min(1,t)*math.pi)*5
        bob=int((1-ease)*17-bounce)
        box=d.textbbox((0,0),symbol,font=emoji)
        ew=box[2]-box[0]
        d.text((cx-ew//2,top-18-bob),symbol,font=emoji,embedded_color=True)
        # Tiny moving gold glints during the entrance only.
        if elapsed<9:
            phase=elapsed/9
            for j in range(2):
                angle=phase*math.pi*2+j*math.pi
                sx=int(cx+53*math.cos(angle))
                sy=int(top+38+22*math.sin(angle)-bob)
                star_size=2 if j else 3
                d.line((sx-star_size,sy,sx+star_size,sy),fill=(255,225,155),width=1)
                d.line((sx,sy-star_size,sx,sy+star_size),fill=(255,225,155),width=1)
        # Strong hierarchy and comfortable line spacing.
        tag_width=d.textbbox((0,0),tag,font=tag_font)[2]
        d.text((cx-tag_width//2,top+112),tag,font=tag_font,fill=color)
        tw=d.textbbox((0,0),title,font=title_font)[2]
        d.text((cx-tw//2,top+132),title,font=title_font,fill=WHITE)
        sw=d.textbbox((0,0),sub,font=sub_font)[2]
        d.text((cx-sw//2,top+155),sub,font=sub_font,fill=MUTED)
    return im

frames=[render(f) for f in range(34)]
frames.append(render(40))
out=Path("assets/ui/wins-emoji.gif")
out.parent.mkdir(parents=True,exist_ok=True)
frames[0].save(out,save_all=True,append_images=frames[1:],duration=[75]*34+[4500],optimize=True,disposal=2)
print(f"created {out}: {len(frames)} frames, {W}x{H}")
