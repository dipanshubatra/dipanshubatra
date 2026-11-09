#!/usr/bin/env python3
"""ECSoC '26 level-up map: a rocket flies a hand-drawn trail; each badge pops as the rocket reaches it.
Badge art is extracted from assets/ecsoc/card-*.svg and re-encoded small (webp) so the SVG stays light.
Outputs ecsoc-map.svg + hd-ecsoc.svg. Run from repo root: python3 scripts/gen_ecsoc_map.py"""
import sys, re, base64, io, math, random
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cover_notes as c
import gen_about_notes as a

D, INK = c.D, c.INK
ROOT = D.parent
YEL, LIME, PINK, BLUE, ORG, LAV = c.YEL, c.LIME, c.PINK, c.BLUE, c.ORG, c.LAV
T = 18.0
P = lambda s: round(s / T * 100, 2)

BADGES = [("card-contributor", "CONTRIBUTOR", "#6c8cff"), ("card-2", "LEVEL 2", ORG), ("card-3", "LEVEL 3", YEL),
          ("card-4", "LEVEL 4", "#7de0f5"), ("card-5", "LEVEL 5", LAV), ("card-6", "MASTER", "#ff6b6b")]
NODES = [(120, 430, 60), (275, 300, 60), (435, 440, 60), (595, 295, 60), (750, 435, 60), (885, 255, 84)]
W, H = 1000, 590

def badge_uri(name, px):
    s = (ROOT / "ecsoc" / f"{name}.svg").read_text(encoding="utf-8")
    b64 = re.search(r'href="data:image/png;base64,([^"]+)"', s).group(1)
    im = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGBA").resize((px, px), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=80, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()

def trail():
    segs, d = [], f"M{NODES[0][0]} {NODES[0][1]}"
    for (x0, y0, _), (x1, y1, _) in zip(NODES, NODES[1:]):
        mx = (x0 + x1) / 2
        d += f" C{mx} {y0} {mx} {y1} {x1} {y1}"; segs.append(((x0, y0), (mx, y0), (mx, y1), (x1, y1)))
    # arc-length fractions at each node
    lens = []
    for p0, p1, p2, p3 in segs:
        L, prev = 0, p0
        for k in range(1, 201):
            t = k / 200
            x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
            y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
            L += math.hypot(x - prev[0], y - prev[1]); prev = (x, y)
        lens.append(L)
    tot = sum(lens); fr, acc = [0.0], 0
    for L in lens: acc += L; fr.append(acc / tot)
    return d, fr

def build():
    d, fr = trail()
    R0, R1 = .6, 9.2   # rocket start / end (s)
    css = ["text{text-rendering:optimizeSpeed}"]
    body = []
    # faint full trail + drawn trail
    body.append(f'<path d="{d}" fill="none" stroke="#8b949e" stroke-opacity=".45" stroke-width="4" stroke-dasharray="2 12" stroke-linecap="round"/>')
    css.append(f"@keyframes tr{{0%,{P(R0)}%{{stroke-dashoffset:100}}{P(R1)}%,93%{{stroke-dashoffset:0}}96.5%,100%{{stroke-dashoffset:100}}}}.tr{{animation:tr {T}s linear infinite}}")
    body.append(f'<path class="tr" id="trk" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="{d}" fill="none" stroke="{PINK}" stroke-width="5" stroke-linecap="round" stroke-opacity=".9"/>')
    # title block (top-left)
    css.append(c.slam_kf("ttl", .3, True, T))
    body.append(f'<g class="ttl"><g transform="rotate(-2 200 60)"><line x1="36" y1="64" x2="386" y2="60" stroke="{LIME}" stroke-width="54" stroke-opacity=".97"/>'
                f'<text x="48" y="80" font-size="46" font-weight="900" letter-spacing="-1" fill="{INK}" textLength="330" lengthAdjust="spacingAndGlyphs">global rank #4</text></g>'
                f'<g transform="rotate(2 130 118)"><rect x="40" y="104" width="190" height="30" rx="15" fill="{PINK}" stroke="{INK}" stroke-width="2.8"/>'
                f'<text class="m" x="135" y="124" text-anchor="middle" font-size="12.5" font-weight="800" letter-spacing="2" fill="{INK}">TIER 1 DEVELOPER</text></g>'
                f'<text class="m" x="244" y="124" font-size="11.5" letter-spacing="1" fill="{a.GREY}">elite coders summer of code 2026</text></g>')
    # nodes
    defs = []
    for i, ((x, y, r), (name, tag, col)) in enumerate(zip(NODES, BADGES)):
        t = R0 + fr[i] * (R1 - R0) + .05
        uri = badge_uri(name, 230 if r > 70 else 170)
        css.append(f"@keyframes pn{i}{{0%,{P(t)}%{{opacity:0;transform:scale(.15) rotate(-30deg)}}{P(t+.3)}%{{opacity:1;transform:scale(1.2) rotate(6deg)}}"
                   f"{P(t+.5)}%{{transform:scale(.94) rotate(-2deg)}}{P(t+.65)}%,93%{{opacity:1;transform:none}}96.5%,100%{{opacity:0;transform:scale(.4)}}}}.pn{i}{{animation:pn{i} {T}s ease-out infinite}}")
        defs.append(f'<clipPath id="bc{i}"><circle r="{r}"/></clipPath>')
        rot = -3 if i % 2 == 0 else 3
        tag_w = 150 if i == 5 else 128
        g = (f'<g transform="translate({x} {y})"><g class="pn{i}">'
             f'<circle r="{r+6}" fill="{INK}" transform="translate(4 5)"/><circle r="{r+7}" fill="#fff"/>'
             f'<image href="{uri}" x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" clip-path="url(#bc{i})"/>'
             f'<circle r="{r}" fill="none" stroke="{INK}" stroke-width="3"/>'
             f'<g transform="translate({r*.74:.0f} {-r*.78:.0f})"><circle r="16" fill="{col}" stroke="{INK}" stroke-width="2.8"/>'
             f'<text x="0" y="6" text-anchor="middle" font-size="17" font-weight="900" fill="{INK}">{i+1}</text></g>'
             f'<g transform="translate(0 {r+30}) rotate({rot})"><rect x="{-tag_w/2}" y="-13" width="{tag_w}" height="26" fill="{col}" fill-opacity=".95"/>'
             f'<path d="M{-tag_w/2} -13 l-4 4 l4 4 l-4 4 l4 4 l-4 4 M{tag_w/2} -13 l4 4 l-4 4 l4 4 l-4 4 l4 4" fill="none" stroke="{col}" stroke-width="3"/>'
             f'<text class="m" x="0" y="4.5" text-anchor="middle" font-size="12.5" font-weight="800" letter-spacing="2.5" fill="{INK}">{tag}</text></g>'
             f'</g></g>')
        body.append(g)
        if i == 5:   # master extras: crown scribble + confetti
            css.append(c.draw_kf("cr", t + .5, .6, True, T))
            body.append(f'<path class="cr" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="M{x-40} {y-r-26} L{x-30} {y-r-52} L{x-14} {y-r-34} L{x} {y-r-58} L{x+14} {y-r-34} L{x+30} {y-r-52} L{x+40} {y-r-26} Z" fill="none" stroke="{YEL}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
            rnd = random.Random(5)
            for q in range(16):
                k = 100 + q; dx, dy, rt = rnd.randint(-150, 150), rnd.randint(-190, -60), rnd.randint(-540, 540)
                col2 = rnd.choice([PINK, YEL, LIME, LAV, BLUE, ORG]); S = t + .3 + rnd.random() * .3
                css.append(f"@keyframes cf{k}{{0%,{P(S)}%{{opacity:0;transform:translate(0,0) rotate(0)}}{P(S+.05)}%{{opacity:1}}{P(S+1.5)}%{{opacity:0;transform:translate({dx}px,{dy+200}px) rotate({rt}deg)}}100%{{opacity:0}}}}"
                           f".cf{k}{{animation:cf{k} {T}s cubic-bezier(.2,.7,.4,1) infinite}}")
                body.append(f'<g transform="translate({x} {y-30})"><rect class="cf{k}" x="-3.5" y="-4.5" width="7" height="10" fill="{col2}" stroke="{INK}" stroke-width="1"/></g>')
    # closing caption
    css.append(f"@keyframes cl{{0%,{P(10.8)}%{{opacity:0;transform:translateY(10px)}}{P(11.4)}%,93%{{opacity:1;transform:none}}96.5%,100%{{opacity:0}}}}.cl{{animation:cl {T}s ease-out infinite}}")
    css.append(c.draw_kf("ck", 11.3, .4, True, T))
    body.append(f'<g class="cl"><text class="m" x="72" y="{H-26}" font-size="14" font-weight="700" letter-spacing="1.5" fill="{a.CREAM}">6/6 BADGES UNLOCKED</text>'
                f'<text x="72" y="{H-6}" font-size="13" font-style="italic" fill="{a.GREY}">contributor to master. every level, no skips.</text></g>'
                f'<path class="ck" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="M34 {H-30} L44 {H-20} L62 {H-42}" fill="none" stroke="{LIME}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    # rocket (SMIL motion, synced to the trail)
    kt0, kt1 = R0 / T, R1 / T
    css.append("@keyframes fl{0%,100%{transform:scaleX(1)}50%{transform:scaleX(1.5)}}.fl{transform-box:fill-box;transform-origin:100% 50%;animation:fl .18s linear infinite}")
    rocket = (f'<g><animateMotion dur="{T}s" repeatCount="indefinite" rotate="auto" calcMode="linear" keyPoints="0;0;1;1" keyTimes="0;{kt0:.4f};{kt1:.4f};1"><mpath href="#trk"/></animateMotion>'
              f'<path class="fl" d="M-17 0 L-32 -6 L-30 0 L-32 6 Z" fill="{ORG}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
              f'<path d="M-16 -8 L-25 -17 L-6 -8 Z M-16 8 L-25 17 L-6 8 Z" fill="{PINK}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
              f'<path d="M-16 -8 L10 -8 Q26 0 10 8 L-16 8 Z" fill="#fff" stroke="{INK}" stroke-width="2.8" stroke-linejoin="round"/>'
              f'<path d="M12 -7.2 Q24 0 12 7.2 Z" fill="{PINK}" stroke="{INK}" stroke-width="2"/><circle cx="-2" cy="0" r="4" fill="{BLUE}" stroke="{INK}" stroke-width="2"/></g>')
    body.append(rocket)
    return c.svg(W, H, "".join(css), "".join(body), "".join(defs))

if __name__ == "__main__":
    out = {"ecsoc-map.svg": build(), "hd-ecsoc.svg": a.heading("02", "ecsoc ’26", PINK, LIME, "// summer of code 2026")}
    for n, s in out.items():
        (D / n).write_text(s, encoding="utf-8"); print("wrote", n, len(s) // 1024, "KB")
