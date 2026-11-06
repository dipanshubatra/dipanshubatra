#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W,H=1000,350
BG=(13,17,23); PANEL=(17,24,35); WHITE=(238,243,249); MUTED=(137,151,169)
GOLD=(245,185,66); SILVER=(203,213,225); CYAN=(34,211,238)
items=[
 ("WINNER","Techfrontier 2025","IIIT Delhi · 500+ participants",GOLD,"01"),
 ("WINNER","Hackastra","NIT Durgapur",GOLD,"02"),
 ("WINNER","Mukand Utsav 2K26","National-level",GOLD,"03"),
 ("WINNER","HackOrbit 2K26","National-level",GOLD,"04"),
 ("WINNER","Ideathon 2K26","JMIT Radaur",GOLD,"05"),
 ("WINNER","Shark Tank","Pitch competition",GOLD,"06"),
 ("FINALIST","ByteVerse","Hackathon finalist",SILVER,"07"),
 ("GLOBAL RANK 4","ECSoC 2026","Tier 1 Developer",CYAN,"08"),
]
fd=Path("/usr/share/fonts/truetype/dejavu")
def ft(name,size): return ImageFont.truetype(str(fd/name),size)
F_HEAD=ft("DejaVuSans-Bold.ttf",9); F_TAG=ft("DejaVuSans-Bold.ttf",8)
F_TITLE=ft("DejaVuSans-Bold.ttf",12); F_SUB=ft("DejaVuSans.ttf",9)
F_NUM=ft("DejaVuSans-Bold.ttf",8)

def mix(a,b,t): return tuple(int(a[k]*(1-t)+b[k]*t) for k in range(3))
def trophy(d,cx,cy,color,scale=1.0,tilt=0):
    # Custom dimensional cup: bowl, handles, stem, plinth and metallic highlights.
    s=scale
    def pt(x,y): return (int(cx+x*s),int(cy+y*s))
    # handles
    d.arc((cx-22*s,cy-15*s,cx-5*s,cy+11*s),265,100,fill=mix(color,(255,245,200),.35),width=max(2,int(3*s)))
    d.arc((cx+5*s,cy-15*s,cx+22*s,cy+11*s),80,275,fill=mix(color,(255,245,200),.35),width=max(2,int(3*s)))
    # cup body
    d.polygon([pt(-13,-19),pt(13,-19),pt(10,-2),pt(5,7),pt(-5,7),pt(-10,-2)],fill=color)
    d.line([pt(-10,-16),pt(-7,-3),pt(-3,2)],fill=(255,235,170),width=max(1,int(2*s)))
    d.line([pt(-11,-19),pt(11,-19)],fill=(255,239,184),width=max(1,int(2*s)))
    d.line([pt(0,7),pt(0,17)],fill=mix(color,(130,82,20),.25),width=max(2,int(4*s)))
    d.rounded_rectangle((cx-8*s,cy+15*s,cx+8*s,cy+20*s),radius=max(1,int(2*s)),fill=mix(color,(255,240,185),.2))
    d.rounded_rectangle(tuple(map(int,(cx-14*s,cy+20*s,cx+14*s,cy+26*s))),radius=max(1,int(2*s)),fill=mix(color,(130,82,20),.2))
    d.line([pt(-11,23),pt(11,23)],fill=(255,238,175),width=max(1,int(1*s)))

def render(frame):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.text((20,9),"THE TROPHY ROOM",font=F_HEAD,fill=(119,136,157))
    d.text((W-132,9),"08  /  WINS & HONOURS",font=F_HEAD,fill=(119,136,157))
    for x in range(20,980):
        t=(x-20)/960
        col=mix(GOLD,CYAN,t)
        d.line((x,27,x,28),fill=col)
    cw,ch,gapx,gapy=226,144,20,12
    for i,(tag,title,sub,color,num) in enumerate(items):
        x=18+(i%4)*(cw+gapx); y=40+(i//4)*(ch+gapy)
        # One card pops in at a time; all earlier cards remain settled.
        t=max(0,min(1,(frame-i*3)/5))
        if t<=0: continue
        ease=1-(1-t)**3
        lift=int((1-ease)*13)
        yy=y+lift
        d.rounded_rectangle((x+2,yy+4,x+cw+2,yy+ch+4),radius=14,fill=(7,10,15))
        d.rounded_rectangle((x,yy,x+cw,yy+ch),radius=14,fill=PANEL,outline=mix((43,55,72),color,.48),width=1)
        # award ribbon and subtle inner plate
        d.rounded_rectangle((x+12,yy+10,x+cw-12,yy+ch-10),radius=10,outline=(35,45,59),width=1)
        d.rounded_rectangle((x+16,yy+15,x+cw-16,yy+31),radius=5,fill=mix((25,30,39),color,.16))
        d.text((x+24,yy+19),tag,font=F_TAG,fill=color)
        d.text((x+cw-29,yy+19),num,font=F_NUM,fill=(103,119,139))
        # spotlight behind trophy
        glow=int(10+22*ease)
        d.ellipse((x+cw//2-40,yy+35,x+cw//2+40,yy+108),fill=tuple(int(v*.10+glow) for v in color))
        # Trophy rises from a little pedestal.
        ty=yy+63-int(12*ease)
        trophy(d,x+cw//2,ty,color,scale=.92*ease+.08)
        d.line((x+cw//2-25,yy+99,x+cw//2+25,yy+99),fill=mix(color,(43,55,72),.35),width=2)
        # award name and issuer
        bb=d.textbbox((0,0),title,font=F_TITLE); tw=bb[2]-bb[0]
        d.text((x+(cw-tw)//2,yy+108),title,font=F_TITLE,fill=WHITE)
        bb=d.textbbox((0,0),sub,font=F_SUB); sw=bb[2]-bb[0]
        d.text((x+(cw-sw)//2,yy+126),sub,font=F_SUB,fill=MUTED)
        # small sparkle only while the card enters
        if frame>=i*3 and frame<=i*3+4:
            sx=x+cw//2+int(28*math.cos(frame*.8+i))
            sy=yy+53+int(18*math.sin(frame*.8+i))
            d.line((sx-4,sy,sx+4,sy),fill=(255,239,190),width=1)
            d.line((sx,sy-4,sx,sy+4),fill=(255,239,190),width=1)
    return im

frames=[render(f) for f in range(32)]
frames.append(render(40))
out=Path("assets/ui/wins-trophy.gif"); out.parent.mkdir(parents=True,exist_ok=True)
frames[0].save(out,save_all=True,append_images=frames[1:],duration=[85]*32+[4200],optimize=True,disposal=2)
print(f"created {out}: {len(frames)} frames, {W}x{H}")
