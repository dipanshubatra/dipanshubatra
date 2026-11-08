#!/usr/bin/env python3
"""Notebook-style header + bottom: hero-note.svg, btn-note-*.svg, cta-note.svg, footer-note.svg (same look as Journey).
Run from repo root: python3 scripts/gen_cover_notes.py"""
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "assets" / "ui"
INK, PAPER = "#15151a", "#f6f1e7"
YEL, LIME, PINK, BLUE, ORG, LAV = "#ffe14d", "#b8f35b", "#ff7eb6", "#6c8cff", "#ff9f45", "#c4a7ff"
FONT = ("text{font-family:'Inter','Segoe UI',Helvetica,Arial,sans-serif}"
        ".m{font-family:'Fira Code','SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace}")

def svg(w, h, css, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}</defs><style>{FONT}{css}</style>{body}</svg>\n')

def slam_kf(name, d, loop=False, T=10.0):
    """sticker drops in with a little overshoot. one-shot (holds) or looping."""
    if not loop:
        return (f"@keyframes {name}{{0%{{opacity:0;transform:translateY(-28px)}}60%{{opacity:1;transform:translateY(5px)}}"
                f"100%{{opacity:1;transform:translateY(0)}}}}.{name}{{animation:{name} .5s ease-out {d}s both}}")
    p = lambda s: round(s / T * 100, 2)
    return (f"@keyframes {name}{{0%,{p(d)}%{{opacity:0;transform:translateY(-28px)}}{p(d+.3)}%{{opacity:1;transform:translateY(5px)}}"
            f"{p(d+.45)}%,90%{{opacity:1;transform:translateY(0)}}95%,100%{{opacity:0;transform:translateY(-28px)}}}}"
            f".{name}{{animation:{name} {T}s ease-out infinite}}")

def draw_kf(name, d, dur, loop=False, T=10.0):
    if not loop:
        return (f"@keyframes {name}{{from{{stroke-dashoffset:100}}to{{stroke-dashoffset:0}}}}"
                f".{name}{{animation:{name} {dur}s ease-out {d}s both}}")
    p = lambda s: round(s / T * 100, 2)
    return (f"@keyframes {name}{{0%,{p(d)}%{{stroke-dashoffset:100}}{p(d+dur)}%,90%{{stroke-dashoffset:0}}95%,100%{{stroke-dashoffset:100}}}}"
            f".{name}{{animation:{name} {T}s ease-out infinite}}")

def sticker(cx, cy, w, h, text, color, rot, cls, size=14, dash=False, label=None):
    d = ' stroke-dasharray="7 5"' if dash else ''
    ty = cy + size * .35 if not label else cy - 2
    out = (f'<g transform="rotate({rot} {cx} {cy})"><g class="{cls}">'
           f'<rect x="{cx-w/2+3}" y="{cy-h/2+3}" width="{w}" height="{h}" rx="9" fill="{INK}"/>'
           f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="9" fill="{color}" stroke="{INK}" stroke-width="3"{d}/>'
           f'<text x="{cx}" y="{ty}" text-anchor="middle" font-size="{size}" font-weight="800" fill="{INK}">{text}</text>')
    if label:
        out += f'<text class="m" x="{cx}" y="{cy+size*.9}" text-anchor="middle" font-size="9.5" font-weight="600" letter-spacing="2" fill="{INK}">{label}</text>'
    return out + '</g></g>'

def page(x, y, w, h, shadow, tilt, cx, cy, lines, margin=None, holes=None, cid="cp"):
    defs = f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/></clipPath>'
    b = [f'<g transform="rotate({tilt} {cx} {cy})">',
         f'<rect x="{x+8}" y="{y+8}" width="{w}" height="{h}" rx="14" fill="{shadow}"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{PAPER}"/>',
         f'<g clip-path="url(#{cid})">' + "".join(f'<line x1="{x}" y1="{ly}" x2="{x+w}" y2="{ly}" stroke="#c9d3ea" stroke-width="1.2"/>' for ly in lines)
         + (f'<line x1="{margin}" y1="{y}" x2="{margin}" y2="{y+h}" stroke="#ff6b6b" stroke-opacity=".75" stroke-width="1.6"/>' if margin else '') + '</g>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="{INK}" stroke-width="3"/>']
    for hy in (holes or []):
        b.append(f'<circle cx="{x+40}" cy="{hy}" r="9" fill="#0d1117" stroke="{INK}" stroke-width="2.5"/>')
    return defs, b

# ---------------------------------------------------------------- hero
def hero():
    W, H = 1000, 300
    defs, b = page(16, 10, 968, 272, LIME, -0.4, 500, 150, range(40, 282, 34), margin=104, holes=range(50, 270, 38), cid="hc")
    css = (draw_kf("mk", .4, .8) + draw_kf("sq", 1.3, .7) + draw_kf("ar", .2, .5)
           + slam_kf("s1", 1.0) + slam_kf("s2", 1.25) + slam_kf("s3", 1.5)
           + "@keyframes wg{0%,100%{transform:rotate(-10deg)}50%{transform:rotate(10deg)}}"
           ".st{transform-box:fill-box;transform-origin:center;animation:wg 3.2s ease-in-out infinite}")
    nl = 640
    b.append(f'<text class="m" x="140" y="58" font-size="14" letter-spacing="3" fill="{INK}" fill-opacity=".6">HI, I’M</text>')
    b.append(f'<path class="ar" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="M240 50 C254 64 266 72 284 74 M276 64 L285 74 L273 80" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(f'<line class="mk" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" x1="134" y1="119" x2="{140+nl+10}" y2="115" stroke="{YEL}" stroke-width="50" stroke-opacity=".95"/>')
    b.append(f'<text x="140" y="142" font-size="80" font-weight="900" letter-spacing="-2" fill="{INK}" textLength="{nl}" lengthAdjust="spacingAndGlyphs">dipanshu batra</text>')
    b.append(f'<text x="140" y="178" font-size="19" font-weight="700" fill="{INK}" fill-opacity=".85">backend engineer · java &amp; spring boot · distributed systems</text>')
    b.append(f'<text x="140" y="206" font-size="15" font-weight="500" fill="{INK}" fill-opacity=".7">building secure &amp; scalable backend systems</text>')
    b.append(f'<path class="sq" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="M140 214 Q158 207 176 214 T212 214 T248 214 T284 214 T320 214 T356 214 T392 214" fill="none" stroke="{PINK}" stroke-width="4" stroke-linecap="round"/>')
    b.append(sticker(262, 248, 248, 38, "ecsoc ’26 · global rank 4", PINK, -2, "s1", 14))
    b.append(sticker(500, 248, 200, 38, "7× hackathon winner", YEL, 2, "s2", 14))
    b.append(sticker(758, 248, 252, 38, "backend intern @ enginow", ORG, -1.5, "s3", 14))
    # star doodle + tape
    b.append('<g transform="translate(905 84)"><g class="st"><path d="M0 -34 L10 -11 L35 -10 L15 6 L22 31 L0 17 L-22 31 L-15 6 L-35 -10 L-10 -11 Z" fill="%s" stroke="%s" stroke-width="3.5" stroke-linejoin="round"/></g></g>' % (YEL, INK))
    b.append(f'<g transform="rotate(7 880 14)"><rect x="838" y="0" width="84" height="26" fill="{LAV}" fill-opacity=".85"/></g>')
    b.append('</g>')
    return svg(W, H, css, "".join(b), defs)

# ---------------------------------------------------------------- buttons
def button(label, color, i):
    txt = f"{label} →"
    w = int(len(txt) * 9.2 + 40); H = 52
    rot = -1.5 if i % 2 == 0 else 1.5
    css = slam_kf("bt", .3 + i * .15)
    b = (f'<g transform="rotate({rot} {w/2} 24)"><g class="bt">'
         f'<rect x="7" y="7" width="{w-12}" height="38" rx="10" fill="{INK}"/>'
         f'<rect x="3" y="3" width="{w-12}" height="38" rx="10" fill="{color}" stroke="{INK}" stroke-width="3"/>'
         f'<text x="{(w-12)/2+3}" y="28" text-anchor="middle" font-size="15" font-weight="800" fill="{INK}">{txt}</text></g></g>')
    return svg(w, H, css, b)

# ---------------------------------------------------------------- cta (bottom)
def cta():
    W, H = 1000, 220
    T = 10.0
    defs, b = page(16, 10, 968, 190, YEL, 0.4, 500, 105, range(36, 200, 34), margin=104, cid="cc")
    css = (draw_kf("mk", .3, .8, True, T) + slam_kf("st", .9, True, T)
           + "@keyframes bk{0%,49%{opacity:1}50%,100%{opacity:0}}.bk{animation:bk 1s steps(1) infinite}"
           + "@keyframes wg{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}.wg{transform-box:fill-box;transform-origin:center;animation:wg 1.6s ease-in-out infinite}")
    b.append(f'<circle class="bk" cx="146" cy="52" r="5" fill="#2ecc71" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<text class="m" x="162" y="57" font-size="12" letter-spacing="3" fill="{INK}" fill-opacity=".6">STATUS · OPEN TO WORK</text>')
    tl = 596
    b.append(f'<line class="mk" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" x1="134" y1="108" x2="{140+tl+8}" y2="105" stroke="{LIME}" stroke-width="44" stroke-opacity=".95"/>')
    b.append(f'<text x="140" y="124" font-size="40" font-weight="900" letter-spacing="-1" fill="{INK}" textLength="{tl}" lengthAdjust="spacingAndGlyphs">open to sde &amp; backend internships</text>')
    b.append(f'<text x="140" y="162" font-size="18" font-weight="500" fill="{INK}" fill-opacity=".75">let’s build something reliable together. my inbox is open :)</text>')
    b.append(f'<g class="wg">' + sticker(860, 104, 170, 80, "hire me", LAV, 4, "st", 30, dash=True, label="SAY HI") + '</g>')
    b.append('</g>')
    return svg(W, H, css, "".join(b), defs)

# ---------------------------------------------------------------- footer
def footer():
    W, H = 1000, 130
    T = 10.0
    defs, b = page(16, 10, 968, 100, PINK, -0.3, 500, 60, (38, 72, 106), margin=104, cid="cf")
    css = draw_kf("tk", .6, .5, True, T) + "@keyframes bf{0%,6%{opacity:0}9%,90%{opacity:1}95%,100%{opacity:0}}.bf{animation:bf 10s linear infinite}"
    box = "M-16 -15 C-8 -17 8 -16 16 -15 C17 -5 17 6 16 16 C6 17 -7 16 -16 15 C-17 5 -16 -5 -16 -15 Z"
    b.append(f'<g transform="translate(66 60)"><path class="bf" d="{box}" fill="{LIME}"/><path d="{box}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
             f'<path class="tk" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="M-9 2 L-2 10 L19 -17" fill="none" stroke="{INK}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/></g>')
    tl = 520
    b.append(f'<line x1="134" y1="62" x2="{140+tl+8}" y2="60" stroke="{PINK}" stroke-width="30" stroke-opacity=".9"/>')
    b.append(f'<text x="140" y="68" font-size="26" font-weight="900" letter-spacing="-.5" fill="{INK}" textLength="{tl}" lengthAdjust="spacingAndGlyphs">that’s the whole notebook. thanks for reading.</text>')
    b.append(f'<text x="140" y="98" font-size="15" font-weight="500" fill="{INK}" fill-opacity=".72">now go build something.</text>')
    b.append(f'<text x="880" y="82" text-anchor="end" font-size="30" font-style="italic" font-weight="700" fill="{INK}" transform="rotate(-4 880 82)">— dipanshu</text>')
    b.append(f'<path d="M742 94 Q790 84 836 92 T 884 88" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>')
    b.append('</g>')
    return svg(W, H, css, "".join(b), defs)

if __name__ == "__main__":
    out = {"hero-note.svg": hero(), "cta-note.svg": cta(), "footer-note.svg": footer()}
    for i, (k, lab, c) in enumerate([("linkedin", "linkedin", BLUE), ("github", "github", LIME), ("leetcode", "leetcode", ORG),
                                     ("x", "x / twitter", LAV), ("portfolio", "portfolio", YEL)]):
        out[f"btn-note-{k}.svg"] = button(lab, c, i)
    for name, s in out.items():
        (D / name).write_text(s, encoding="utf-8")
        print("wrote", name, len(s), "B")
