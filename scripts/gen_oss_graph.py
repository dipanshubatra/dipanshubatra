#!/usr/bin/env python3
"""Open Source as a hand-drawn git graph: every repo is a branch off main, every commit a dot (94 + 24),
branch length = real commit count. Numbers roll while commits stream in. Outputs oss-graph.svg, hd-oss.svg, oss-btn-*.svg.
Run from repo root: python3 scripts/gen_oss_graph.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cover_notes as c
import gen_about_notes as a

D, INK = c.D, c.INK
YEL, LIME, PINK, BLUE, LAV = c.YEL, c.LIME, c.PINK, c.BLUE, c.LAV
CREAM, GREY = a.CREAM, a.GREY
T = 18.0
P = lambda s: round(s / T * 100, 2)

LANES = [  # y, colour, name, repo, count, kind
    (160, YEL,  "MedTrack",  "kRamu81/MedTrack_Application", 94, "commits"),
    (268, PINK, "MailGenie", "Nicode2707/MailGenie",         24, "commits"),
    (376, BLUE, "the rest",  "java / spring ecosystem",      16, "repos"),
]
MAIN_Y, DOT_X0, STEP = 58, 276, 6.0

def odo(css, key, text, x, y, size, S, dur, fill, adv):
    Lh = size * 1.22; out = []
    for k, ch in enumerate(text):
        if ch.isdigit():
            d = int(ch); tgt = d if d else 10; nm = f"o{key}{k}"
            css.append(f"@keyframes {nm}{{0%,{P(S)}%{{transform:translateY(0)}}{P(S+dur)}%,93%{{transform:translateY({-Lh*tgt:.0f}px)}}93.1%,100%{{transform:translateY(0)}}}}"
                       f".{nm}{{animation:{nm} {T}s cubic-bezier(.3,.7,.3,1) infinite}}")
            digs = "".join(f'<text class="m" x="{x+adv/2:.1f}" y="{y+Lh*j:.0f}" text-anchor="middle" font-size="{size}" font-weight="900" fill="{fill}">{j%10}</text>' for j in range(11))
            out.append(f'<clipPath id="oc{key}{k}"><rect x="{x-1:.1f}" y="{y-size*.85:.0f}" width="{adv+2:.1f}" height="{size*1.05:.0f}"/></clipPath>'
                       f'<g clip-path="url(#oc{key}{k})"><g class="{nm}">{digs}</g></g>')
        else:
            out.append(f'<text class="m" x="{x+adv/2:.1f}" y="{y}" text-anchor="middle" font-size="{size}" font-weight="900" fill="{fill}">{ch}</text>')
        x += adv
    return "".join(out)

def build():
    W, H = 1000, 440
    css, body, defs = ["text{text-rendering:optimizeSpeed}"], [], []
    # main branch
    css.append(c.draw_kf("mn", .2, 1.3, True, T))
    body.append(f'<line x1="40" y1="{MAIN_Y}" x2="900" y2="{MAIN_Y}" stroke="#8b949e" stroke-opacity=".35" stroke-width="4"/>')
    body.append(f'<line class="mn" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" x1="40" y1="{MAIN_Y}" x2="900" y2="{MAIN_Y}" stroke="{CREAM}" stroke-width="4" stroke-linecap="round"/>')
    for k, mx in enumerate(range(80, 900, 78)):
        body.append(f'<circle class="mn" cx="{mx}" cy="{MAIN_Y}" r="5" fill="#0d1117" stroke="{CREAM}" stroke-width="3"/>')
    body.append(f'<text class="m" x="40" y="{MAIN_Y-18}" font-size="13" font-weight="700" letter-spacing="2" fill="{GREY}">main</text>')
    FORK_X = 244
    for i, (y, col, name, repo, n, kind) in enumerate(LANES):
        S = 1.6 + i * 2.7
        if kind == "commits":
            dots = [DOT_X0 + k * STEP for k in range(n)]
            end = dots[-1] + 6
            dur = 1.2 + n * 0.028
        else:
            dots = [DOT_X0 + k * 17 for k in range(n)]
            end = dots[-1] + 40
            dur = 1.6
        mx = end + 32
        fork = f"M{FORK_X} {MAIN_Y} C{FORK_X} {y} {FORK_X+6} {y} {DOT_X0-10} {y}"
        merge = f"M{end} {y} C{mx} {y} {mx} {MAIN_Y+16} {mx} {MAIN_Y}"
        css.append(c.draw_kf(f"f{i}", S, .5, True, T) + c.draw_kf(f"m{i}", S + .5 + dur, .6, True, T))
        css.append(f"@keyframes rv{i}{{0%,{P(S+.5)}%{{width:0}}{P(S+.5+dur)}%,93%{{width:{end-DOT_X0+20:.0f}px}}93.1%,100%{{width:0}}}}.rv{i}{{animation:rv{i} {T}s linear infinite}}")
        defs.append(f'<clipPath id="rc{i}"><rect class="rv{i}" x="{DOT_X0-10}" y="{y-20}" width="0" height="40"/></clipPath>')
        # lane base
        body.append(f'<path d="{fork}" fill="none" stroke="{col}" stroke-opacity=".25" stroke-width="3"/>')
        body.append(f'<path class="f{i}" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="{fork}" fill="none" stroke="{col}" stroke-width="3.5" stroke-linecap="round"/>')
        body.append(f'<line x1="{DOT_X0-10}" y1="{y}" x2="{end}" y2="{y}" stroke="{col}" stroke-opacity=".2" stroke-width="3"/>')
        g = [f'<line x1="{DOT_X0-10}" y1="{y}" x2="{end}" y2="{y}" stroke="{col}" stroke-width="3.5"/>']
        for k, dx in enumerate(dots):
            if kind == "commits":
                big = (k + 1) % 25 == 0 or k == n - 1
                g.append(f'<circle cx="{dx:.1f}" cy="{y}" r="{6.5 if big else 3.1}" fill="{"#0d1117" if big else col}" stroke="{col}" stroke-width="{3 if big else 0}"/>')
            else:
                g.append(f'<rect x="{dx-6:.1f}" y="{y-6}" width="12" height="12" rx="3" fill="#0d1117" stroke="{col}" stroke-width="2.6"/>')
        if kind == "repos":
            g.append(f'<text x="{end-14}" y="{y+9}" text-anchor="middle" font-size="26" font-weight="900" fill="{col}">+</text>')
        body.append(f'<g clip-path="url(#rc{i})">{"".join(g)}</g>')
        body.append(f'<path d="{merge}" fill="none" stroke="{col}" stroke-opacity=".25" stroke-width="3"/>')
        body.append(f'<path class="m{i}" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="{merge}" fill="none" stroke="{col}" stroke-width="3.5" stroke-linecap="round"/>')
        body.append(f'<circle class="m{i}" cx="{mx}" cy="{MAIN_Y}" r="9" fill="{col}" stroke="{INK}" stroke-width="3"/>')
        # label sticker (left)
        css.append(c.slam_kf(f"lb{i}", S, True, T))
        rot = -2 if i % 2 == 0 else 2
        body.append(f'<g transform="rotate({rot} 120 {y})"><g class="lb{i}">'
                    f'<rect x="44" y="{y-30}" width="184" height="60" rx="12" fill="{INK}" transform="translate(4 4)"/>'
                    f'<rect x="40" y="{y-30}" width="184" height="60" rx="12" fill="{col}" stroke="{INK}" stroke-width="3"/>'
                    f'<text x="132" y="{y-3}" text-anchor="middle" font-size="22" font-weight="900" fill="{INK}">{name}</text>'
                    f'<text class="m" x="132" y="{y+17}" text-anchor="middle" font-size="9.5" font-weight="600" fill="{INK}" fill-opacity=".75">{repo}</text></g></g>')
        # counter after merge
        cx0 = mx + 26
        txt = f"{n}" + ("+" if kind == "repos" else "")
        css.append(f"@keyframes ct{i}{{0%,{P(S+.4)}%{{opacity:0}}{P(S+.8)}%,93%{{opacity:1}}96.5%,100%{{opacity:0}}}}.ct{i}{{animation:ct{i} {T}s linear infinite}}")
        body.append(f'<g class="ct{i}">' + odo(css, i, txt, cx0, y + 14, 44, S + .5, dur, col, 27)
                    + f'<text class="m" x="{cx0}" y="{y+34}" font-size="11.5" font-weight="700" letter-spacing="2" fill="{CREAM}" fill-opacity=".8">{kind.upper()}</text></g>')
    # HEAD sticker
    css.append(c.slam_kf("hd", 11.5, True, T))
    body.append(f'<g transform="rotate(-4 936 {MAIN_Y})"><g class="hd"><rect x="896" y="{MAIN_Y-18}" width="92" height="36" rx="8" fill="{INK}" transform="translate(3 3)"/>'
                f'<rect x="893" y="{MAIN_Y-18}" width="92" height="36" rx="8" fill="{LIME}" stroke="{INK}" stroke-width="3"/>'
                f'<text class="m" x="939" y="{MAIN_Y+5}" text-anchor="middle" font-size="12" font-weight="900" letter-spacing="1" fill="{INK}">HEAD → main</text></g></g>')
    # caption
    css.append(f"@keyframes cp{{0%,{P(12.2)}%{{opacity:0}}{P(13)}%,93%{{opacity:1}}96.5%,100%{{opacity:0}}}}.cp{{animation:cp {T}s linear infinite}}")
    body.append(f'<g class="cp"><text x="40" y="{H-14}" font-size="14" font-style="italic" fill="{GREY}">git log --author=dipanshu  ·  one dot = one commit</text></g>')
    return c.svg(W, H, "".join(css), "".join(body), "".join(defs))

if __name__ == "__main__":
    out = {"oss-graph.svg": build(), "hd-oss.svg": a.heading("07", "open source", LAV, YEL, "// one dot, one commit"),
           "oss-btn-medtrack.svg": c.button("medtrack repo", YEL, 0), "oss-btn-mailgenie.svg": c.button("mailgenie repo", PINK, 1),
           "oss-btn-all.svg": c.button("all my repos", BLUE, 2)}
    for n, s in out.items():
        (D / n).write_text(s, encoding="utf-8"); print("wrote", n, len(s) // 1024 or 1, "KB")
