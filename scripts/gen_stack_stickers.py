#!/usr/bin/env python3
"""Tech Stack as a sticker bomb: die-cut stickers slap on one by one (squash), then wiggle in turn.
Outputs stack-note.svg + hd-stack.svg. Run from repo root: python3 scripts/gen_stack_stickers.py"""
import sys, math, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cover_notes as c
import gen_about_notes as a

D, INK = c.D, c.INK
YEL, LIME, PINK, BLUE, ORG, LAV = c.YEL, c.LIME, c.PINK, c.BLUE, c.ORG, c.LAV
T = 16.0
P = lambda s: round(s / T * 100, 2)

CATS = [  # label, colour, shape, items
    ("CORE",     YEL,  "burst", ["Java 17 / 21", "Spring Boot 3", "Spring Security", "Hibernate / JPA", "REST APIs"]),
    ("SECURITY", PINK, "hex",   ["JWT rotation", "OAuth2", "RBAC", "Rate limiting · Bucket4j"]),
    ("SYSTEMS",  BLUE, "oval",  ["Distributed Systems", "Circuit Breakers", "Async Processing", "Resilience4j", "HikariCP"]),
    ("DATA",     LIME, "db",    ["PostgreSQL", "MySQL", "Redis · distributed locks"]),
    ("TOOLS",    LAV,  "pill",  ["Docker", "GitHub Actions", "Maven", "JUnit 5", "JMeter", "Postman", "Cashfree", "Cloudinary", "React"]),
]

def shape(kind, w, h, attrs):
    if kind == "pill":  return f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="{h/2}" {attrs}/>'
    if kind == "oval":  return f'<ellipse rx="{w/2}" ry="{h/2}" {attrs}/>'
    if kind == "hex":
        pts = [(-w/2, 0), (-w/2+14, -h/2), (w/2-14, -h/2), (w/2, 0), (w/2-14, h/2), (-w/2+14, h/2)]
        return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" {attrs}/>'
    if kind == "burst":
        n, pts = 16, []
        for k in range(2 * n):
            r = 1 if k % 2 == 0 else .88; ang = math.pi * k / n
            pts.append((r * math.cos(ang) * w / 2, r * math.sin(ang) * h / 2))
        return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" {attrs}/>'
    if kind == "db":
        ry = 9
        return (f'<path d="M{-w/2} {-h/2+ry} a{w/2} {ry} 0 0 1 {w} 0 v{h-2*ry} a{w/2} {ry} 0 0 1 {-w} 0 z" {attrs}/>')
    return f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="12" {attrs}/>'

def sticker(i, S, Wg, text, color, kind, w, h, x, y, rot, font=15):
    css = (f"@keyframes k{i}{{0%,{P(S)}%{{opacity:0;transform:translate(0,-70px) scale(1.7) rotate(14deg)}}"
           f"{P(S+.15)}%{{opacity:1;transform:translate(0,-18px) scale(1.25) rotate(8deg)}}"
           f"{P(S+.5)}%{{opacity:1;transform:translate(0,3px) scale(.9) rotate(-3deg)}}"
           f"{P(S+.7)}%{{transform:translate(0,0) scale(1.05) rotate(1deg)}}{P(S+.85)}%,{P(Wg)}%{{opacity:1;transform:none}}"
           f"{P(Wg+.12)}%{{transform:scale(1.09) rotate(-4deg)}}{P(Wg+.26)}%{{transform:scale(1.04) rotate(3deg)}}{P(Wg+.4)}%,93%{{opacity:1;transform:none}}"
           f"96.5%,100%{{opacity:0;transform:translate(0,-40px) scale(.8)}}}}.k{i}{{animation:k{i} {T}s ease-out infinite}}")
    extra = ""
    if kind == "db":
        extra = f'<path d="M{-w/2} {-h/2+9} a{w/2} 9 0 0 0 {w} 0" fill="none" stroke="{INK}" stroke-width="2.4"/>'
    s = (f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot})"><g class="k{i}">'
         + shape(kind, w, h, f'fill="{INK}" transform="translate(3.5 4)"')
         + shape(kind, w, h, 'fill="#fff" stroke="#fff" stroke-width="10" stroke-linejoin="round"')
         + shape(kind, w, h, f'fill="{color}" stroke="{INK}" stroke-width="2.8" stroke-linejoin="round"')
         + extra
         + f'<path d="M{-w/2+14} {-h/2+7} q{w*.2} -4 {w*.32} 0" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="3" stroke-linecap="round" transform="translate(0 {2 if kind in ("pill","rrect") else 4})"/>'
         + f'<text x="0" y="{font*.35+(3 if kind=="db" else 0):.1f}" text-anchor="middle" font-size="{font}" font-weight="800" letter-spacing="-.2" fill="{INK}">{text}</text>'
         + '</g></g>')
    return css, s

def build():
    rnd = random.Random(7)
    W = 1000
    rows = []
    for lab, col, kind, items in CATS:
        cur, widths = [], []
        for t in items:
            w = round(a.est(t, 15) + 36 + (12 if kind == "burst" else 0))
            if sum(widths) + (len(cur)) * 12 + w > 805 and cur:
                rows.append((lab, col, kind, cur, widths)); cur, widths, lab = [], [], ""
            cur.append(t); widths.append(w)
        rows.append((lab, col, kind, cur, widths))
    ROWH = 74
    H = 40 + len(rows) * ROWH + 50
    order = list(range(sum(len(r[3]) for r in rows)))
    rnd.shuffle(order)
    wig = list(order); rnd.shuffle(wig)
    css, body, idx = "", [], 0
    for r, (lab, col, kind, items, widths) in enumerate(rows):
        cy = 52 + r * ROWH + 28
        total = sum(widths) + 12 * (len(items) - 1)
        x = 156 + (810 - total) / 2
        if lab:
            tcss, tape = tape_label(r, lab, col, cy, rnd)
            css += tcss; body.append(tape)
        for t, w in zip(items, widths):
            h = {"burst": 62, "db": 56, "hex": 50, "oval": 52}.get(kind, 46)
            S = .3 + order[idx] * .13
            Wg = 6.2 + wig[idx] * .27
            sc, sv = sticker(idx, S, Wg, t.replace("&", "&amp;"), col, kind, w, h, x + w / 2 + rnd.uniform(-4, 4), cy + rnd.uniform(-9, 9), round(rnd.uniform(-7, 7), 1), 15)
            css += sc; body.append(sv); x += w + 12 + rnd.uniform(-2, 2); idx += 1
    # extras: stars + note
    for j, (sx, sy, col) in enumerate(((968, 34, YEL), (36, H - 30, PINK), (940, H - 26, LIME))):
        sc, sv = sticker(200 + j, 4.8 + j * .3, 12.5 + j, "", col, "burst", 34, 34, sx, sy, 10 * (j - 1), 10)
        css += sc; body.append(sv)
    css += c.draw_kf("nt", 10.5, .9, True, T) + f"@keyframes nf{{0%,{P(10.5)}%{{opacity:0}}{P(11.2)}%,93%{{opacity:1}}96.5%,100%{{opacity:0}}}}.nf{{animation:nf {T}s linear infinite}}"
    body.append(f'<g class="nf"><text x="860" y="{H-22}" text-anchor="end" font-size="16" font-style="italic" fill="{a.GREY}">+ chai, obviously</text></g>'
                f'<path class="nt" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="M868 {H-30} C890 {H-40} 902 {H-34} 912 {H-26}" fill="none" stroke="{a.GREY}" stroke-width="2.5" stroke-linecap="round"/>')
    return c.svg(W, H, "text{text-rendering:optimizeSpeed}" + css, "".join(body))

def tape_label(r, lab, col, cy, rnd):
    i = 300 + r
    S = .1 + r * .1
    css = (f"@keyframes k{i}{{0%,{P(S)}%{{opacity:0;transform:translateX(-30px)}}{P(S+.4)}%,93%{{opacity:1;transform:none}}96.5%,100%{{opacity:0;transform:translateX(-30px)}}}}"
           f".k{i}{{animation:k{i} {T}s ease-out infinite}}")
    rot = -4 if r % 2 == 0 else 3
    s = (f'<g transform="translate(92 {cy}) rotate({rot})"><g class="k{i}"><rect x="-56" y="-14" width="112" height="28" fill="{col}" fill-opacity=".92"/>'
         f'<path d="M-56 -14 l-4 4 l4 4 l-4 4 l4 4 l-4 4 l4 4 M56 -14 l4 4 l-4 4 l4 4 l-4 4 l4 4 l-4 4" fill="none" stroke="{col}" stroke-width="3"/>'
         f'<text class="m" x="0" y="4.5" text-anchor="middle" font-size="12.5" font-weight="800" letter-spacing="3" fill="{INK}">{lab}</text></g></g>')
    return css, s

if __name__ == "__main__":
    out = {"stack-note.svg": build(), "hd-stack.svg": a.heading("04", "tech stack", ORG, PINK, "// what's in my bag")}
    for n, s in out.items():
        (D / n).write_text(s, encoding="utf-8"); print("wrote", n, len(s), "B")
