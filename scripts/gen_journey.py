#!/usr/bin/env python3
"""Generates assets/ui/journey.svg (section 06 timeline). Standalone so it never touches other sections.
Run from repo root:  python3 scripts/gen_journey.py"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "ui" / "journey.svg"
W, H, RY = 1000, 250, 70
CW, CY, CH = 216, 108, 118
M = [  # cx, colour, date, title, detail lines
    (140, "#22d3ee", "2025",           "B.Tech CSE",       ["JMIT Radaur", "2025–2029 · CGPA 7.9"]),
    (380, "#f5b942", "2025 – 26",      "Hackathon streak", ["7× national-level winner"]),
    (620, "#f472b6", "SUMMER 2026",    "ECSoC ’26",        ["Global Rank 4", "Tier 1 Developer"]),
    (860, "#a78bfa", "SEP 2026 – NOW", "Backend Intern",   ["Enginow", "Java 17 · Spring Boot 3"]),
]

defs = ['<linearGradient id="rail" gradientUnits="userSpaceOnUse" x1="60" x2="880">'
        '<stop offset="0" stop-color="#22d3ee"/><stop offset=".34" stop-color="#f5b942"/>'
        '<stop offset=".68" stop-color="#f472b6"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>',
        '<linearGradient id="fut" gradientUnits="userSpaceOnUse" x1="880" x2="950">'
        '<stop offset="0" stop-color="#a78bfa" stop-opacity=".8"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></linearGradient>',
        '<linearGradient id="tail" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".85"/></linearGradient>',
        '<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".13"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
        '<filter id="gl" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="5"/></filter>']
for i, (cx, c, *_r) in enumerate(M):
    defs.append(f'<linearGradient id="f{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}" stop-opacity=".13"/><stop offset="1" stop-color="#0d1117" stop-opacity="1"/></linearGradient>')
    defs.append(f'<clipPath id="k{i}"><rect x="{cx-CW//2}" y="{CY}" width="{CW}" height="{CH}" rx="16"/></clipPath>')

css = ("text{font-family:'Segoe UI',Inter,Helvetica,Arial,sans-serif}"
       ".m{font-family:'Fira Code','SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace}"
       "@keyframes dr{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
       "@keyframes fd{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
       "@keyframes pl{0%{transform:scale(1);opacity:.55}100%{transform:scale(2.1);opacity:0}}"
       "@keyframes run{0%{transform:translateX(0);opacity:0}6%{opacity:1}94%{opacity:1}100%{transform:translateX(820px);opacity:0}}"
       "@keyframes sw{0%{transform:translateX(-120px) skewX(-20deg)}35%,100%{transform:translateX(340px) skewX(-20deg)}}"
       "@keyframes lv{0%,100%{opacity:1}50%{opacity:.25}}"
       "@keyframes nx{0%,100%{transform:translateX(0);opacity:.5}50%{transform:translateX(5px);opacity:1}}"
       ".rl{transform-box:fill-box;transform-origin:left center;animation:dr 1.5s cubic-bezier(.2,.7,.2,1) both}"
       ".orb{animation:run 6.5s ease-in-out 1.8s infinite;opacity:0}"
       ".lv{animation:lv 1.4s ease-in-out infinite}.nx{animation:nx 1.8s ease-in-out infinite}"
       ".pr{transform-box:fill-box;transform-origin:center}")
for i in range(4):
    css += (f".c{i}{{animation:fd .8s ease-out {.3+i*.25:.2f}s both}}"
            f".p{i}{{animation:pl 2.6s ease-out {i*.5:.1f}s infinite}}"
            f".s{i}{{animation:sw 6s ease-in-out {2+i*.6:.1f}s infinite}}")

b = [f'<rect x="60" y="{RY-2}" width="820" height="4" rx="2" fill="#30363d" opacity=".5"/>',
     f'<rect class="rl" x="60" y="{RY-2}" width="820" height="4" rx="2" fill="url(#rail)"/>',
     f'<line x1="884" y1="{RY}" x2="944" y2="{RY}" stroke="url(#fut)" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/>',
     f'<path class="nx" d="M948 {RY-5} L956 {RY} L948 {RY+5}" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
     f'<g transform="translate(60 {RY})"><g class="orb"><rect x="-70" y="-1.5" width="70" height="3" fill="url(#tail)"/>'
     '<circle r="9" fill="#fff" filter="url(#gl)"/><circle r="3.5" fill="#fff"/></g></g>']
for i, (cx, c, date, title, lines) in enumerate(M):
    b.append(f'<g class="c{i}">')
    b.append(f'<circle class="pr p{i}" cx="{cx}" cy="{RY}" r="10" fill="{c}"/>')
    b.append(f'<circle cx="{cx}" cy="{RY}" r="17" fill="none" stroke="{c}" stroke-opacity=".18"/>')
    b.append(f'<circle cx="{cx}" cy="{RY}" r="10" fill="#0d1117" stroke="{c}" stroke-width="3"/><circle cx="{cx}" cy="{RY}" r="4" fill="{c}"/>')
    b.append(f'<line x1="{cx}" y1="{RY+17}" x2="{cx}" y2="{CY}" stroke="{c}" stroke-opacity=".55"/>')
    b.append(f'<rect x="{cx-CW//2}" y="{CY}" width="{CW}" height="{CH}" rx="16" fill="url(#f{i})" stroke="{c}" stroke-opacity=".55"/>')
    b.append(f'<rect x="{cx-18}" y="{CY}" width="36" height="3" rx="1.5" fill="{c}"/>')
    b.append(f'<g clip-path="url(#k{i})"><rect class="s{i}" x="{cx-CW//2}" y="{CY}" width="70" height="{CH}" fill="url(#sh)"/></g>')
    b.append(f'<text class="m" x="{cx}" y="{CY+30}" text-anchor="middle" font-size="11.5" letter-spacing="1.5" fill="{c}">{date}</text>')
    b.append(f'<text x="{cx}" y="{CY+60}" text-anchor="middle" font-size="19" font-weight="800" fill="#f1f5f9">{title}</text>')
    y0 = CY + 84 if len(lines) == 2 else CY + 91
    for j, t in enumerate(lines):
        b.append(f'<text x="{cx}" y="{y0+j*17}" text-anchor="middle" font-size="11.5" fill="#94a3b8">{t}</text>')
    if i == 3:  # live badge
        b.append(f'<rect x="{cx-27}" y="30" width="54" height="18" rx="9" fill="#34d399" fill-opacity=".12" stroke="#34d399" stroke-opacity=".6"/>')
        b.append(f'<circle class="lv" cx="{cx-14}" cy="39" r="3" fill="#34d399"/>')
        b.append(f'<text class="m" x="{cx+4}" y="42.5" text-anchor="middle" font-size="9.5" letter-spacing="1.5" fill="#34d399">NOW</text>')
    b.append('</g>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<defs>{"".join(defs)}</defs><style>{css}</style>{"".join(b)}</svg>\n')
OUT.write_text(svg, encoding="utf-8")
print(f"wrote {OUT} ({len(svg)} bytes)")
