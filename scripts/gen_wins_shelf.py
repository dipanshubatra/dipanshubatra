#!/usr/bin/env python3
"""Achievements as a trophy shelf: hand-drawn trophies drop onto planks, luggage tags swing (damped pendulum) from nails,
a tally gets scratched in. Outputs wins-shelf.svg + hd-wins.svg. Run from repo root: python3 scripts/gen_wins_shelf.py"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cover_notes as c
import gen_about_notes as a

D, INK, PAPER = c.D, c.INK, c.PAPER
YEL, LIME, PINK, BLUE, ORG, LAV = c.YEL, c.LIME, c.PINK, c.BLUE, c.ORG, c.LAV
CYAN, SILVER = "#7de0f5", "#d5dbe6"
T = 20.0
P = lambda s: round(s / T * 100, 2)
SW = 3.5

def star(r, cx=0, cy=0, k=5, inner=.45):
    pts = []
    for i in range(k * 2):
        rr = r if i % 2 == 0 else r * inner; ang = -math.pi / 2 + math.pi * i / k
        pts.append(f"{cx+rr*math.cos(ang):.1f},{cy+rr*math.sin(ang):.1f}")
    return " ".join(pts)

# icons: origin = bottom centre, ~120px tall. F main fill, K stroke, W white, D dark, shadow=True -> everything INK, no details
def cup(F, K, W, D, sh, gem=None, label=None):
    s = (f'<rect x="-32" y="-14" width="64" height="14" rx="4" fill="{D}" stroke="{K}" stroke-width="{SW}"/>'
         f'<rect x="-8" y="-38" width="16" height="26" fill="{F}" stroke="{K}" stroke-width="{SW}"/>'
         f'<path d="M-36 -112 L36 -112 Q38 -60 0 -44 Q-38 -60 -36 -112 Z" fill="{F}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>'
         f'<path d="M-36 -100 Q-64 -100 -55 -78 Q-48 -62 -30 -64 M36 -100 Q64 -100 55 -78 Q48 -62 30 -64" fill="none" stroke="{K}" stroke-width="9" stroke-linecap="round"/>'
         + ('' if sh else f'<path d="M-36 -100 Q-64 -100 -55 -78 Q-48 -62 -30 -64 M36 -100 Q64 -100 55 -78 Q48 -62 30 -64" fill="none" stroke="{F}" stroke-width="4" stroke-linecap="round"/>')
         + f'<rect x="-40" y="-122" width="80" height="12" rx="5" fill="{F}" stroke="{K}" stroke-width="{SW}"/>')
    if not sh:
        s += f'<path d="M-24 -104 Q-27 -80 -14 -64" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="4" stroke-linecap="round"/>'
        s += (f'<circle cx="0" cy="-84" r="9" fill="{gem}" stroke="{K}" stroke-width="2.5"/>' if gem else f'<polygon points="{star(15,0,-84)}" fill="#fff" stroke="{K}" stroke-width="2.5" stroke-linejoin="round"/>')
    return s

def medal(F, K, W, D, sh):
    s = (f'<rect x="-30" y="-26" width="60" height="26" rx="5" fill="{D}" stroke="{K}" stroke-width="{SW}"/>'
         f'<path d="M-24 -124 L-4 -124 L10 -80 L-12 -80 Z" fill="{PINK if not sh else K}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>'
         f'<path d="M24 -124 L4 -124 L-10 -80 L12 -80 Z" fill="{BLUE if not sh else K}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>'
         f'<circle cx="0" cy="-60" r="34" fill="{F}" stroke="{K}" stroke-width="{SW}"/>')
    if not sh:
        s += f'<circle cx="0" cy="-60" r="24" fill="none" stroke="{K}" stroke-width="2.4"/><polygon points="{star(14,0,-60)}" fill="#fff" stroke="{K}" stroke-width="2.4" stroke-linejoin="round"/>'
    return s

def planet(F, K, W, D, sh):
    s = (f'<rect x="-30" y="-14" width="60" height="14" rx="4" fill="{D}" stroke="{K}" stroke-width="{SW}"/>'
         f'<rect x="-7" y="-40" width="14" height="28" fill="{F}" stroke="{K}" stroke-width="{SW}"/>'
         f'<circle cx="0" cy="-80" r="36" fill="{F}" stroke="{K}" stroke-width="{SW}"/>'
         f'<ellipse cx="0" cy="-80" rx="58" ry="14" transform="rotate(-18 0 -80)" fill="none" stroke="{K}" stroke-width="6"/>')
    if not sh:
        s += (f'<ellipse cx="0" cy="-80" rx="58" ry="14" transform="rotate(-18 0 -80)" fill="none" stroke="{PINK}" stroke-width="2.6"/>'
              f'<path d="M-22 -96 Q-26 -82 -16 -70" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="4" stroke-linecap="round"/>'
              f'<polygon points="{star(7,52,-118,4,.3)}" fill="#fff" stroke="{K}" stroke-width="1.5"/><polygon points="{star(5,-56,-48,4,.3)}" fill="#fff" stroke="{K}" stroke-width="1.5"/>')
    return s

def bulb(F, K, W, D, sh):
    s = (f'<rect x="-34" y="-10" width="68" height="10" rx="4" fill="{D}" stroke="{K}" stroke-width="{SW}"/>'
         f'<rect x="-15" y="-32" width="30" height="22" rx="4" fill="{SILVER if not sh else K}" stroke="{K}" stroke-width="{SW}"/>'
         f'<path d="M-12 -42 L-14 -32 L14 -32 L12 -42 Z" fill="{SILVER if not sh else K}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>'
         f'<path d="M-13 -42 C-42 -62 -40 -112 0 -114 C40 -112 42 -62 13 -42 Z" fill="{F}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>')
    if not sh:
        s += (f'<path d="M-10 -52 Q-12 -76 -5 -64 Q0 -84 5 -64 Q12 -76 10 -52" fill="none" stroke="{K}" stroke-width="3" stroke-linecap="round"/>'
              f'<path d="M-26 -88 Q-24 -102 -12 -106" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="4" stroke-linecap="round"/>'
              f'<path d="M-52 -96 l-12 -4 M52 -96 l12 -4 M-44 -116 l-9 -9 M44 -116 l9 -9 M0 -128 l0 -10" stroke="{F}" stroke-width="4" stroke-linecap="round"/>')
    return s

def shark(F, K, W, D, sh):
    s = (f'<path d="M-48 0 L-48 -18 Q-36 -30 -24 -18 T0 -18 T24 -18 T48 -18 L48 0 Z" fill="{BLUE if not sh else K}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>'
         f'<path d="M-16 -20 Q-18 -72 6 -112 Q26 -68 36 -20 Z" fill="{F}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>')
    if not sh:
        s += (f'<path d="M-2 -40 Q0 -64 8 -88" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="4" stroke-linecap="round"/>'
              f'<text x="0" y="-4" text-anchor="middle" font-size="17" font-weight="900" fill="#fff">$</text>')
    return s

def startrophy(F, K, W, D, sh):
    s = (f'<rect x="-30" y="-14" width="60" height="14" rx="4" fill="{D}" stroke="{K}" stroke-width="{SW}"/>'
         f'<rect x="-6" y="-46" width="12" height="34" fill="{F}" stroke="{K}" stroke-width="{SW}"/>'
         f'<polygon points="{star(52,0,-86,5,.5)}" fill="{F}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>')
    if not sh:
        s += f'<text x="0" y="-78" text-anchor="middle" font-size="22" font-weight="900" fill="{K}">#4</text>'
    return s

ACH = [  # result, name, venue, icon, F, gem
    ("WINNER", "TechFrontier 2025", "IIIT Delhi · 500+ teams", "cup", YEL, None),
    ("WINNER", "Hackastra", "NIT Durgapur", "cup", ORG, PINK),
    ("WINNER", "Mukand Utsav 2K26", "National-level", "medal", YEL, None),
    ("WINNER", "HackOrbit 2K26", "National-level", "planet", LAV, None),
    ("WINNER", "Ideathon 2K26", "JMIT Radaur", "bulb", LIME, None),
    ("WINNER", "Shark Tank", "Pitch competition", "shark", "#9fb3c8", None),
    ("FINALIST", "ByteVerse", "Hackathon finalist", "cup", SILVER, BLUE),
    ("GLOBAL RANK #4", "ECSOC 2026", "Tier 1", "star", CYAN, None),
]
ICONS = {"cup": cup, "medal": medal, "planet": planet, "bulb": bulb, "shark": shark, "star": startrophy}
CHIP = {"WINNER": LIME, "FINALIST": LAV, "GLOBAL RANK #4": CYAN}

def build():
    W, OY0, PITCH = 1000, 66, 290
    H = OY0 + PITCH + 232 + 62
    css, body = ["text{text-rendering:optimizeSpeed}"], []
    # tally
    body.append(f'<text class="m" x="612" y="36" font-size="13" letter-spacing="1" fill="{a.GREY}">on the shelf:</text>')
    marks = [f"M{760+i*15} 14 L{760+i*15} 42" for i in range(4)] + ["M754 36 L832 18"] + [f"M{846+i*15} 14 L{846+i*15} 42" for i in range(3)]
    for k, d in enumerate(marks):
        css.append(c.draw_kf(f"ty{k}", .3 + k * .22, .2, True, T))
        body.append(f'<path class="ty{k}" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="{d}" stroke="{a.CREAM}" stroke-width="4.5" stroke-linecap="round"/>')
    for r in range(2):
        OY = OY0 + r * PITCH
        py = OY + 232
        # plank + brackets
        body.append(f'<path d="M60 {py+16} L60 {py+44} L100 {py+16} Z M940 {py+16} L940 {py+44} L900 {py+16} Z" fill="#8a6a43" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
        body.append(f'<rect x="30" y="{py}" width="940" height="16" rx="5" fill="#d9a05b" stroke="{INK}" stroke-width="3.5"/>'
                    f'<path d="M60 {py+5} h120 M260 {py+10} h90 M520 {py+5} h140 M760 {py+10} h80" stroke="#a97a3d" stroke-width="2.5" stroke-linecap="round"/>')
    for i, (res, name, venue, icon, F, gem) in enumerate(ACH):
        r, col = divmod(i, 4)
        cx = 140 + col * 240
        OY = OY0 + r * PITCH
        py = OY + 232
        chip = CHIP[res]
        # trophy drop-in
        S = .6 + i * .38
        css.append(f"@keyframes tp{i}{{0%,{P(S)}%{{opacity:0;transform:translateY(-190px) scale(1,1.12)}}{P(S+.32)}%{{opacity:1;transform:translateY(0) scale(1.14,.82)}}"
                   f"{P(S+.5)}%{{transform:translateY(-12px) scale(.96,1.05)}}{P(S+.66)}%,93%{{opacity:1;transform:none}}96.5%,100%{{opacity:0;transform:translateY(-60px)}}}}.tp{i}{{animation:tp{i} {T}s ease-in infinite}}")
        fn = ICONS[icon]
        kw = {"gem": gem} if icon == "cup" else {}
        sh_pass = fn(INK, INK, INK, INK, True, **kw)
        main = fn(F, INK, "#fff", INK, False, **kw)
        body.append(f'<ellipse cx="{cx}" cy="{py-2}" rx="56" ry="7" fill="#000" fill-opacity=".35"/>')
        body.append(f'<g transform="translate({cx} {py}) scale(1)"><g class="tp{i}"><g transform="translate(6 7)">{sh_pass}</g>{main}</g></g>')
        # glint
        G = 11 + i * .55
        css.append(f"@keyframes gl{i}{{0%,{P(G)}%{{opacity:0;transform:scale(.1) rotate(0)}}{P(G+.25)}%{{opacity:1;transform:scale(1.2) rotate(45deg)}}{P(G+.6)}%,100%{{opacity:0;transform:scale(.1) rotate(90deg)}}}}.gl{i}{{animation:gl{i} {T}s ease-out infinite}}")
        body.append(f'<g transform="translate({cx+44} {py-108})"><polygon class="gl{i}" points="{star(13,0,0,4,.22)}" fill="#fff" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/></g>')
        # swinging tag
        TS = 3.4 + i * .42
        ang = [0, 13, -9, 5.5, -3, 1.4, 0]
        times = [0, .25, .7, 1.25, 1.85, 2.5, 3.2]
        stops = "".join(f"{P(TS+t)}%{{transform:rotate({g}deg)}}" for t, g in zip(times, ang))
        css.append(f"@keyframes sw{i}{{0%,{P(TS-.05)}%{{transform:rotate(0)}}{stops}100%{{transform:rotate(0)}}}}"
                   f".sw{i}{{transform-origin:{cx}px {OY}px;animation:sw{i} {T}s ease-in-out infinite}}")
        css.append(f"@keyframes tg{i}{{0%,{P(S+.2)}%{{opacity:0}}{P(S+.7)}%,93%{{opacity:1}}96.5%,100%{{opacity:0}}}}.tg{i}{{animation:tg{i} {T}s linear infinite}}")
        tw, th, ty0 = 184, 74, OY + 22
        tag = (f'<g class="tg{i}"><g class="sw{i}">'
               f'<path d="M{cx} {OY} C{cx-3} {OY+10} {cx+3} {OY+20} {cx} {ty0+13}" fill="none" stroke="{a.CREAM}" stroke-width="2" stroke-linecap="round"/>'
               f'<path d="M{cx-tw/2+8} {ty0+4+th} H{cx+tw/2-8} Q{cx+tw/2} {ty0+4+th} {cx+tw/2} {ty0+th-4} V{ty0+22} L{cx+tw/2-22} {ty0+4} H{cx-tw/2+22} L{cx-tw/2} {ty0+22} V{ty0+th-4} Q{cx-tw/2} {ty0+4+th} {cx-tw/2+8} {ty0+4+th} Z" transform="translate(5 5)" fill="{chip}"/>'
               f'<path d="M{cx-tw/2+8} {ty0+th} H{cx+tw/2-8} Q{cx+tw/2} {ty0+th} {cx+tw/2} {ty0+th-8} V{ty0+18} L{cx+tw/2-18} {ty0} H{cx-tw/2+18} L{cx-tw/2} {ty0+18} V{ty0+th-8} Q{cx-tw/2} {ty0+th} {cx-tw/2+8} {ty0+th} Z" fill="{PAPER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
               f'<circle cx="{cx}" cy="{ty0+13}" r="4.5" fill="#0d1117" stroke="{INK}" stroke-width="2"/>'
               f'<rect x="{cx-len(res)*3.9-10:.0f}" y="{ty0+22}" width="{len(res)*7.8+20:.0f}" height="17" rx="8.5" fill="{chip}" stroke="{INK}" stroke-width="2"/>'
               f'<text class="m" x="{cx}" y="{ty0+34.5}" text-anchor="middle" font-size="10.5" font-weight="900" letter-spacing="1.5" fill="{INK}">{res}</text>'
               f'<text x="{cx}" y="{ty0+55}" text-anchor="middle" font-size="15.5" font-weight="900" fill="{INK}">{name}</text>'
               f'<text class="m" x="{cx}" y="{ty0+68}" text-anchor="middle" font-size="10.5" fill="{INK}" fill-opacity=".7">{venue}</text>'
               f'</g></g>')
        body.append(f'<circle cx="{cx}" cy="{OY}" r="5" fill="{a.GREY}" stroke="{INK}" stroke-width="2"/>')
        body.append(tag)
    return c.svg(W, H, "".join(css), "".join(body))

if __name__ == "__main__":
    out = {"wins-shelf.svg": build(), "hd-wins.svg": a.heading("05", "achievements", YEL, LIME, "// the shelf")}
    for n, s in out.items():
        (D / n).write_text(s, encoding="utf-8"); print("wrote", n, len(s) // 1024, "KB")
