#!/usr/bin/env python3
"""Generates assets/ui/journey-1..6.svg: a hand-made notebook to-do list, one note per milestone.
Flat colours, hard shadows, wobbly checkboxes, marker highlights. Ticks land top->bottom and loop.
Run from repo root: python3 scripts/gen_journey.py"""
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "assets" / "ui"
W, H = 1000, 120
INK, PAPER = "#15151a", "#f6f1e7"
T, STEP = 12.0, 1.1

# tag, title, caption, sticker big, sticker label, accent, done
ITEMS = [
    ("2025–29 · JMIT RADAUR", "b.tech cse",             "day one. clueless but curious. cgpa 7.9 tho.",               "7.9",     "CGPA",        "#6c8cff", True),
    ("2025–26",               "hackathon arc",          "7 national-level wins. yes, seven.",                         "7×",      "WINS",        "#ffe14d", True),
    ("OPEN SOURCE",           "open source era",        "medtrack, mailgenie + 5 other repos. 118+ commits.",         "118+",    "COMMITS",     "#b8f35b", True),
    ("SUMMER 2026",           "ecsoc ’26",              "global rank 4. tier 1 dev. master contributor.",             "#4",      "GLOBAL RANK", "#ff7eb6", True),
    ("SEP 2026 → NOW",        "backend intern @ enginow", "java 17 + spring boot 3. in the trenches rn.",             "NOW",     "LIVE",        "#ff9f45", True),
    ("NEXT",                  "next up?",               "open to backend &amp; sde internships. hmu :)",              "hire me", "INTERNSHIPS", "#c4a7ff", False),
]

def pct(s): return round(s / T * 100, 2)

def build(i, items=None):
    items = items or ITEMS
    tag, title, cap, big, lab, c, done = items[i]
    t0 = 0.5 + i * STEP
    tilt = -0.5 if i % 2 == 0 else 0.5
    stk_rot = 3 if i % 2 == 0 else -3
    css = ("text{font-family:'Inter','Segoe UI',Helvetica,Arial,sans-serif}"
           ".m{font-family:'Fira Code','SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace}")
    def kf(name, s, e, a, b):
        return f"@keyframes {name}{{0%,{pct(s)}%{{{a}}}{pct(e)}%,92%{{{b}}}96%,100%{{{a}}}}}"
    kfs = []
    if done:
        kfs += [kf("tk", t0, t0+.35, "stroke-dashoffset:100", "stroke-dashoffset:0"),
                kf("bf", t0+.1, t0+.3, "opacity:0", "opacity:1"),
                kf("mk", t0+.3, t0+.7, "stroke-dashoffset:100", "stroke-dashoffset:0"),
                (f"@keyframes sl{{0%,{pct(t0+.6)}%{{opacity:0;transform:translateY(-22px)}}"
                 f"{pct(t0+.78)}%{{opacity:1;transform:translateY(4px)}}{pct(t0+.88)}%,92%{{opacity:1;transform:translateY(0)}}"
                 f"96%,100%{{opacity:0;transform:translateY(-22px)}}}}")]
        css += (f".tk{{animation:tk {T}s linear infinite}}.bf{{animation:bf {T}s linear infinite}}"
                f".mk{{animation:mk {T}s linear infinite}}.sl{{animation:sl {T}s ease-out infinite}}")
    else:
        kfs.append("@keyframes wg{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}"
                   "@keyframes bk{0%,49%{opacity:1}50%,100%{opacity:0}}")
        css += (".wg{transform-box:fill-box;transform-origin:center;animation:wg 1.6s ease-in-out infinite}"
                ".bk{animation:bk 1s steps(1) infinite}")
    css += "".join(kfs)

    CX0, CX1, CY0, CY1 = 16, 984, 6, 108
    b = []
    defs = f'<clipPath id="cp"><rect x="{CX0}" y="{CY0}" width="{CX1-CX0}" height="{CY1-CY0}" rx="12"/></clipPath>'
    b.append(f'<g transform="rotate({tilt} 500 60)">')
    b.append(f'<rect x="{CX0+6}" y="{CY0+6}" width="{CX1-CX0}" height="{CY1-CY0}" rx="12" fill="{c}"/>')           # hard shadow
    b.append(f'<rect x="{CX0}" y="{CY0}" width="{CX1-CX0}" height="{CY1-CY0}" rx="12" fill="{PAPER}"/>')
    b.append('<g clip-path="url(#cp)">'
             + "".join(f'<line x1="{CX0}" y1="{y}" x2="{CX1}" y2="{y}" stroke="#c9d3ea" stroke-width="1.2"/>' for y in (34, 64, 94))
             + '<line x1="116" y1="0" x2="116" y2="120" stroke="#ff6b6b" stroke-opacity=".75" stroke-width="1.6"/></g>')
    b.append(f'<rect x="{CX0}" y="{CY0}" width="{CX1-CX0}" height="{CY1-CY0}" rx="12" fill="none" stroke="{INK}" stroke-width="3"/>')
    # checkbox
    box = "M-16 -15 C-8 -17 8 -16 16 -15 C17 -5 17 6 16 16 C6 17 -7 16 -16 15 C-17 5 -16 -5 -16 -15 Z"
    b.append('<g transform="translate(72 58)">')
    if done:
        b.append(f'<path class="bf" d="{box}" fill="{c}"/>')
    b.append(f'<path d="{box}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    if done:
        b.append(f'<path class="tk" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="M-9 2 L-2 10 L19 -17" fill="none" stroke="{INK}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        b.append(f'<text x="0" y="9" text-anchor="middle" font-size="24" font-weight="900" fill="{INK}">?</text>')
    b.append('</g>')
    # tag, title with marker, caption
    tl = round(len(title) * 16.2)
    b.append(f'<text class="m" x="140" y="29" font-size="11" letter-spacing="2" fill="{INK}" fill-opacity=".55">{tag}</text>')
    if done:
        b.append(f'<line class="mk" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" x1="136" y1="56" x2="{140+tl+6}" y2="53" stroke="{c}" stroke-width="19" stroke-opacity=".9"/>')
    else:
        b.append(f'<path d="M138 70 Q{140+tl//4} 66 {140+tl//2} 70 T{140+tl+4} 68" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round"/>')
    b.append(f'<text x="140" y="62" font-size="28" font-weight="900" letter-spacing="-.5" fill="{INK}" textLength="{tl}" lengthAdjust="spacingAndGlyphs">{title}</text>')
    b.append(f'<text x="140" y="90" font-size="15" font-weight="500" fill="{INK}" fill-opacity=".72">{cap}</text>')
    # sticker
    sx, sy, sw, sh = 880, 57, 134, 62
    b.append(f'<g transform="rotate({stk_rot} {sx} {sy})"><g class="{"sl" if done else "wg"}">')
    dash = '' if done else ' stroke-dasharray="7 5"'
    b.append(f'<rect x="{sx-sw//2+4}" y="{sy-sh//2+4}" width="{sw}" height="{sh}" rx="10" fill="{INK}"/>')
    b.append(f'<rect x="{sx-sw//2}" y="{sy-sh//2}" width="{sw}" height="{sh}" rx="10" fill="{c}" stroke="{INK}" stroke-width="3"{dash}/>')
    fs = 30 if len(big) <= 4 else 24
    b.append(f'<text x="{sx}" y="{sy+4}" text-anchor="middle" font-size="{fs}" font-weight="900" fill="{INK}">{big}</text>')
    b.append(f'<text class="m" x="{sx}" y="{sy+21}" text-anchor="middle" font-size="9.5" font-weight="600" letter-spacing="2" fill="{INK}">{lab}</text>')
    b.append('</g></g></g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{defs}</defs><style>{css}</style>{"".join(b)}</svg>\n')

if __name__ == "__main__":
    for old in list(D.glob("journey*.svg")) + list(D.glob("note-*.svg")):
        old.unlink()
    for i in range(len(ITEMS)):
        (D / f"note-{i+1}.svg").write_text(build(i), encoding="utf-8")
        print("wrote", f"note-{i+1}.svg")
