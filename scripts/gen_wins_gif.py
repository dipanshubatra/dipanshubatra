#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W,H=1000,365
BG=(13,17,23)
WHITE=(238,243,249)
MUTED=(137,151,169)
GOLD=(255,193,55)
CYAN=(34,211,238)
SILVER=(203,213,225)
fd=Path("/usr/share/fonts/truetype/dejavu")
emoji_path="/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
emoji=ImageFont.truetype(emoji_path,109)
title_font=ImageFont.truetype(str(fd/"DejaVuSans-Bold.ttf"),13)
sub_font=ImageFont.truetype(str(fd/"DejaVuSans.ttf"),10)
tag_font=ImageFont.truetype(str(fd/"DejaVuSans-Bold.ttf"),8)
head_font=ImageFont.truetype(str(fd/"DejaVuSans-Bold.ttf"),9)
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
    d.text((20,10),"ACHIEVEMENTS",font=head_font,fill=(112,129,149))
    d.text((W-143,10),"08  /  MILESTONES",font=head_font,fill=(112,129,149))
    # Thin editorial rule, not a card/container.
    d.line((20,29,980,29),fill=(39,50,65),width=1)
    for i,(symbol,title,sub,tag,color) in enumerate(items):
        col=i%4; row=i//4
        cx=125+col*250
        top=39+row*165
        # Staggered pop-in and a soft settle. No card, border or tile.
        t=max(0,min(1,(frame-i*2.1)/6))
        if t<=0: continue
        ease=1-(1-t)**3
        bob=int((1-ease)*13)
        # Center the native gold trophy emoji.
        box=d.textbbox((0,0),symbol,font=emoji)
        ew,eh=box[2]-box[0],box[3]-box[1]
        d.text((cx-ew//2,top-18-bob),symbol,font=emoji,embedded_color=True)
        # Label sits directly under the floating trophy.
        tag_width=d.textbbox((0,0),tag,font=tag_font)[2]
        d.text((cx-tag_width//2,top+105),tag,font=tag_font,fill=color)
        tw=d.textbbox((0,0),title,font=title_font)[2]
        d.text((cx-tw//2,top+120),title,font=title_font,fill=WHITE)
        sw=d.textbbox((0,0),sub,font=sub_font)[2]
        d.text((cx-sw//2,top+139),sub,font=sub_font,fill=MUTED)
        # One tiny four-point glint during entrance only.
        if i==int(frame//2.1) and frame-i*2.1<6:
            sx=cx+38+int(8*math.sin(frame))
            sy=top+30+int(5*math.cos(frame))
            d.line((sx-4,sy,sx+4,sy),fill=(255,224,151),width=1)
            d.line((sx,sy-4,sx,sy+4),fill=(255,224,151),width=1)
    return im

frames=[render(f) for f in range(30)]
frames.append(render(36))
out=Path("assets/ui/wins-trophy.gif")
out.parent.mkdir(parents=True,exist_ok=True)
frames[0].save(out,save_all=True,append_images=frames[1:],duration=[85]*30+[4200],optimize=True,disposal=2)
print(f"created {out}: {len(frames)} frames, {W}x{H}, no cards")
