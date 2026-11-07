#!/usr/bin/env python3
"""Generates assets/ui/journey-1..6.svg: a vertical checklist timeline, one SVG per milestone.
Ticks draw top->bottom in sequence and loop. Run from repo root: python3 scripts/gen_journey.py"""
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "assets" / "ui"
W, H, NX, NY = 1000, 120, 60, 60
CX0, CX1, CY0, CY1 = 112, 960, 8, 112
T, STEP = 12.0, 1.1          # loop length (s), delay between ticks (s)

# tag, title, detail, big metric, metric label, colour, done?
ITEMS = [
    ("2025",          "B.Tech CSE",       "JMIT Radaur · 2025–2029",              "7.9",     "CGPA",          "#22d3ee", True),
    ("2025 – 26",     "Hackathon streak", "National-level wins across the country", "7×",    "WINS",          "#f5b942", True),
    ("OPEN SOURCE",   "Shipping to open source", "MedTrack · MailGenie · +5 other repos", "118+", "COMMITS", "#34d399", True),
    ("SUMMER 2026",   "ECSoC ’26",        "Tier 1 Developer · Master Contributor", "#4",     "GLOBAL RANK",   "#f472b6", True),
    ("SEP 2026 – NOW", "Backend Intern",  "Enginow · Spring Boot 3",              "Java 17", "STACK",         "#a78bfa", True),
    ("NEXT",          "What’s next",      "Open to Backend &amp; SDE internships",    "→",       "OPEN TO",       "#38bdf8", False),
]

def mix(a, b):
    f = lambda h: [int(h[i:i+2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple((x + y) // 2 for x, y in zip(f(a), f(b)))

def pct(s): return round(s / T * 100, 2)

def build(i):
    tag, title, detail, big, lab, c, done = ITEMS[i]
    n = len(ITEMS)
    t0 = 0.5 + i * STEP                    # tick time for this item
    up_start = t0 - STEP + 0.7             # upper connector draws (end = t0 - 0.05)
    low_start = t0 + 0.35                  # lower connector draws (end = t0 + 0.7)
    prev_c = ITEMS[i-1][5] if i else c
    next_c = ITEMS[i+1][5] if i < n-1 else c
    up_mid, low_mid = mix(prev_c, c), mix(c, next_c)

    css = ("text{font-family:'Segoe UI',Inter,Helvetica,Arial,sans-serif}"
           ".m{font-family:'Fira Code','SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace}")
    def kf(name, s, e, a, b):             # a/b = value before/after; resets near loop end
        return (f"@keyframes {name}{{0%,{pct(s)}%{{{a}}}{pct(e)}%,92%{{{b}}}96%,100%{{{a}}}}}")
    kfs = []
    if done:
        kfs += [kf("tk", t0, t0+.45, "stroke-dashoffset:100", "stroke-dashoffset:0"),
                kf("nf", t0, t0+.3, "opacity:0", "opacity:1"),
                kf("gl", t0, t0+.5, "opacity:0", "opacity:1"),
                kf("lw", low_start, low_start+.35, "stroke-dashoffset:100", "stroke-dashoffset:0")]
        css += ".tk{animation:tk %ss linear infinite}.nf,.gl{animation:nf %ss linear infinite}" % (T, T)
        css = css.replace(".nf,.gl{animation:nf", ".nf{animation:nf") + ".gl{animation:gl %ss linear infinite}.lw{animation:lw %ss linear infinite}" % (T, T)
    else:
        kfs.append("@keyframes pn{0%,100%{opacity:.35}50%{opacity:1}}")
        css += ".pn{animation:pn 1.8s ease-in-out infinite}"
    if i:
        kfs.append(kf("uw", up_start, t0-.05, "stroke-dashoffset:100", "stroke-dashoffset:0"))
        css += ".uw{animation:uw %ss linear infinite}" % T
    if done:
        css += "".join([])
    css += "".join(kfs)

    defs = (f'<linearGradient id="gu" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{NY-18}"><stop offset="0" stop-color="{up_mid}"/><stop offset="1" stop-color="{c}"/></linearGradient>'
            f'<linearGradient id="gd" gradientUnits="userSpaceOnUse" x1="0" y1="{NY+18}" x2="0" y2="{H}"><stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="{low_mid}"/></linearGradient>'
            f'<linearGradient id="cf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c}" stop-opacity=".12"/><stop offset=".6" stop-color="#0d1117"/><stop offset="1" stop-color="#0d1117"/></linearGradient>')
    b = []
    # rails (dim base + animated progress)
    if i:
        b.append(f'<line x1="{NX}" y1="0" x2="{NX}" y2="{NY-18}" stroke="#30363d" stroke-width="3"/>')
        b.append(f'<line class="uw" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" x1="{NX}" y1="0" x2="{NX}" y2="{NY-18}" stroke="url(#gu)" stroke-width="3"/>')
    if i < n-1:
        b.append(f'<line x1="{NX}" y1="{NY+18}" x2="{NX}" y2="{H}" stroke="#30363d" stroke-width="3"/>')
        b.append(f'<line class="lw" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" x1="{NX}" y1="{NY+18}" x2="{NX}" y2="{H}" stroke="url(#gd)" stroke-width="3"/>')
    # connector to card
    b.append(f'<line x1="{NX+18}" y1="{NY}" x2="{CX0}" y2="{NY}" stroke="{c}" stroke-opacity=".35" stroke-dasharray="3 4"/>')
    # card
    dash = '' if done else ' stroke-dasharray="6 5"'
    b.append(f'<rect x="{CX0}" y="{CY0}" width="{CX1-CX0}" height="{CY1-CY0}" rx="16" fill="url(#cf)" stroke="{c}" stroke-opacity="{.28 if done else .5}"{dash}/>')
    if done:
        b.append(f'<rect class="gl" x="{CX0}" y="{CY0}" width="{CX1-CX0}" height="{CY1-CY0}" rx="16" fill="none" stroke="{c}" stroke-opacity=".85" stroke-width="1.5"/>')
        b.append(f'<rect class="gl" x="{CX0}" y="{CY0+22}" width="4" height="{CY1-CY0-44}" rx="2" fill="{c}"/>')
    # node
    b.append(f'<circle cx="{NX}" cy="{NY}" r="18" fill="#0d1117" stroke="{c}" stroke-opacity="{.45 if done else .8}" stroke-width="2.5"{"" if done else " stroke-dasharray=\"4 4\""}/>')
    if done:
        b.append(f'<circle class="nf" cx="{NX}" cy="{NY}" r="18" fill="{c}"/>')
        b.append(f'<path class="tk" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="M{NX-8} {NY+1} L{NX-2} {NY+7.5} L{NX+9} {NY-6.5}" fill="none" stroke="#0d1117" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        b.append(f'<circle class="pn" cx="{NX}" cy="{NY}" r="5" fill="{c}"/>')
    # text
    b.append(f'<text class="m" x="{CX0+28}" y="{CY0+32}" font-size="12" letter-spacing="2" fill="{c}">{tag}</text>')
    b.append(f'<text x="{CX0+28}" y="{CY0+62}" font-size="24" font-weight="800" fill="#f1f5f9">{title}</text>')
    b.append(f'<text x="{CX0+28}" y="{CY0+86}" font-size="13.5" fill="#94a3b8">{detail}</text>')
    # metric + done chip
    b.append(f'<text class="m" x="{CX1-28}" y="{CY0+58}" text-anchor="end" font-size="34" font-weight="700" fill="{c}">{big}</text>')
    b.append(f'<text class="m" x="{CX1-28}" y="{CY0+80}" text-anchor="end" font-size="10.5" letter-spacing="2" fill="#94a3b8">{lab}</text>')
    if done:
        b.append(f'<text class="m gl" x="{CX1-28}" y="{CY0+24}" text-anchor="end" font-size="10.5" letter-spacing="2" fill="{c}">✓ DONE</text>' if i < 4 else
                 f'<text class="m gl" x="{CX1-28}" y="{CY0+24}" text-anchor="end" font-size="10.5" letter-spacing="2" fill="{c}">● LIVE</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{defs}</defs><style>{css}</style>{"".join(b)}</svg>\n')

for old in D.glob("journey*.svg"):
    old.unlink()
for i in range(len(ITEMS)):
    p = D / f"journey-{i+1}.svg"
    p.write_text(build(i), encoding="utf-8")
    print("wrote", p.name)
