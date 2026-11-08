#!/usr/bin/env python3
"""About section in the notebook style, deliberately NOT boxed:
hd-about.svg (marker heading), terminal-note.svg (typed torn-paper printout),
highlights-note.svg (odometer numbers + scribbles), about-note.svg (paragraph with highlighter).
Run from repo root: python3 scripts/gen_about_notes.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cover_notes as c

D, INK, PAPER = c.D, c.INK, c.PAPER
YEL, LIME, PINK, BLUE, ORG, LAV = c.YEL, c.LIME, c.PINK, c.BLUE, c.ORG, c.LAV
CREAM, GREY = "#f1ede2", "#8b949e"

def est(t, size):
    w = 0
    for ch in t:
        if ch == " ": w += .28
        elif ch in "iljI.,;:|!'’": w += .27
        elif ch in "frt()": w += .34
        elif ch in "mw": w += .82
        elif ch in "MW": w += .92
        elif ch.isupper(): w += .66
        elif ch.isdigit(): w += .6
        else: w += .55
    return w * size

def wave(x0, x1, y, amp=6, per=34):
    d, x, up = f"M{x0} {y}", x0, True
    d += f" Q{x0+per/4} {y-amp} {x0+per/2} {y}"; x = x0 + per / 2
    while x < x1:
        d += f" T{x+per/2} {y}"; x += per / 2
    return d

def oval(cx, cy, rx, ry):
    return (f"M{cx-rx*.9:.0f} {cy-ry*.2:.0f} C{cx-rx:.0f} {cy-ry*1.15:.0f} {cx+rx*.8:.0f} {cy-ry*1.25:.0f} {cx+rx:.0f} {cy-ry*.1:.0f} "
            f"C{cx+rx*1.1:.0f} {cy+ry*1.0:.0f} {cx-rx*.8:.0f} {cy+ry*1.25:.0f} {cx-rx:.0f} {cy:.0f} "
            f"C{cx-rx*1.06:.0f} {cy-ry*.5:.0f} {cx-rx*.7:.0f} {cy-ry*.95:.0f} {cx-rx*.25:.0f} {cy-ry*1.02:.0f}")

# ------------------------------------------------------------ heading
def heading(num, title, accent, ring, tag):
    W, H, T = 1000, 110, 12.0
    tl = round(est(title, 52))
    css = (c.draw_kf("rg", .2, .7, True, T) + c.draw_kf("mk", .7, .8, True, T) + c.draw_kf("sq", 1.5, .9, True, T))
    b = [f'<path class="rg" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="{oval(56,56,30,27)}" fill="none" stroke="{ring}" stroke-width="4.5" stroke-linecap="round"/>',
         f'<text class="m" x="56" y="64" text-anchor="middle" font-size="22" font-weight="700" fill="{CREAM}">{num}</text>',
         '<g transform="rotate(-1.2 300 56)">',
         f'<line class="mk" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" x1="100" y1="58" x2="{116+tl+18}" y2="55" stroke="{accent}" stroke-width="64" stroke-opacity=".97"/>',
         f'<text x="116" y="75" font-size="52" font-weight="900" letter-spacing="-1" fill="{INK}" textLength="{tl}" lengthAdjust="spacingAndGlyphs">{title}</text></g>',
         f'<path class="sq" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="{wave(116+tl+60, 960, 70)}" fill="none" stroke="{ring}" stroke-width="4" stroke-linecap="round"/>',
         f'<text class="m" x="960" y="42" text-anchor="end" font-size="13" letter-spacing="1" fill="{GREY}">{tag}</text>']
    return c.svg(W, H, css, "".join(b))

# ------------------------------------------------------------ terminal
def torn(x0, y0, x1, y1, amp=6, step=15, off=0):
    pts, x, i = [], x1, 0
    while x > x0:
        pts.append((x, y1 + (amp if (i + off) % 2 else -amp * .3) * (0.6 + ((i * 7) % 5) / 6)))
        x -= step; i += 1
    d = f"M{x0} {y0} L{x1} {y0} L{x1} {y1}" + "".join(f" L{px:.0f} {py:.1f}" for px, py in pts) + f" L{x0} {y1} Z"
    return d

def terminal():
    W, H, T = 1000, 392, 22.0
    X0, X1, Y0, Y1 = 30, 800, 26, 352
    fs, cw = 13, 7.8
    script = [("$ whoami", "p", .6, 1.0),
              ("dipanshu_batra | backend engineer | java · spring boot · distributed systems", "o", 1.9, 2.0),
              ("$ cat now.txt", "p", 4.4, .9),
              ("Backend Developer Intern @ Enginow · building CronVault, a multi-tenant job scheduler", "o", 5.5, 2.2),
              ("$ ls ./achievements", "p", 8.4, 1.1),
              ("ecsoc-global-rank-4/  7x-hackathon-winner/  16k-linkedin/  16+-open-source-projects/", "o", 9.7, 2.1),
              ("$ echo $STATUS", "p", 12.6, 1.0),
              ("open to SDE & backend internships", "o", 13.8, 1.6)]
    css = ("@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:blink 1s steps(1) infinite}" + c.slam_kf("stk", .8, True, T))
    sheet = torn(X0, Y0, X1, Y1)
    shadow = f'<path d="{sheet}" transform="translate(8 8)" fill="{LAV}"/>'
    b = ['<g transform="rotate(-0.6 415 190)">', shadow,
         f'<path d="{sheet}" fill="{PAPER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>',
         f'<g transform="rotate(-5 60 26)"><rect x="30" y="12" width="76" height="24" fill="{YEL}" fill-opacity=".85"/></g>',
         f'<g transform="rotate(4 770 26)"><rect x="738" y="12" width="76" height="24" fill="{PINK}" fill-opacity=".8"/></g>']
    for k, col in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        b.append(f'<circle cx="{62+k*26}" cy="62" r="7.5" fill="{col}" stroke="{INK}" stroke-width="2.5"/>')
    b.append(f'<text class="m" x="156" y="67" font-size="13" fill="{INK}" fill-opacity=".6">dipanshu@dev: ~/about</text>')
    b.append(f'<line x1="48" y1="84" x2="{X1-18}" y2="84" stroke="{INK}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="6 6"/>')
    y = 118
    for i, (txt, kind, st, dur) in enumerate(script):
        wpx = len(txt) * cw
        s, te, hold = st / T * 100, (st + dur) / T * 100, 94
        css += (f"@keyframes L{i}{{0%,{s:.2f}%{{width:0}}{te:.2f}%,{hold}%{{width:{wpx+10:.0f}px}}{hold+.01}%,100%{{width:0}}}}"
                f".LC{i}{{animation:L{i} {T}s linear infinite}}")
        e = txt.replace("&", "&amp;")
        if kind == "p":
            t = f'<tspan fill="#e0457b" font-weight="700">$</tspan><tspan fill="{INK}" font-weight="600">{e[1:]}</tspan>'
        else:
            t = f'<tspan fill="#3b4f9a">{e}</tspan>'
        b.append(f'<clipPath id="lc{i}"><rect class="LC{i}" x="52" y="{y-18}" width="0" height="26"/></clipPath>'
                 f'<text class="m" x="52" y="{y}" font-size="{fs}" clip-path="url(#lc{i})">{t}</text>')
        y += 26 if kind == "p" else 40
    cur_x = 52 + len(script[-1][0]) * cw + 6
    css += (f"@keyframes show{{0%,{13.8/T*100:.1f}%{{opacity:0}}{14.5/T*100:.1f}%,94%{{opacity:1}}94.1%,100%{{opacity:0}}}}.sh{{animation:show {T}s linear infinite}}")
    b.append(f'<g class="sh"><rect class="cur" x="{cur_x:.0f}" y="{y-40-14}" width="9" height="18" fill="#e0457b"/></g>')
    b.append(c.sticker(716, 62, 124, 30, "online", LIME, 5, "stk", 13).replace('</g></g>', '</g></g>'))
    b.append(f'<circle class="cur" cx="684" cy="62" r="4.5" fill="#1fa65a" stroke="{INK}" stroke-width="1.5" transform="rotate(5 716 62)"/>')
    b.append('</g>')
    b.append(f'<text x="836" y="206" font-size="15" font-style="italic" fill="{GREY}" transform="rotate(6 836 206)">(yes, it types by itself)</text>')
    b.append(f'<path d="M868 216 C862 246 840 262 806 270 M818 258 L805 270 L822 276" fill="none" stroke="{GREY}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
    return c.svg(W, H, css, "".join(b))

# ------------------------------------------------------------ highlights
ADV = {"#": 48, "K": 54, "×": 44, "+": 44}
def highlights():
    W, H, T, SZ = 1000, 270, 12.0, 80
    L = SZ * 1.02
    items = [("7×",   "HACKATHON WINS",        "national-level winner",   YEL,  "oval"),
             ("#4",   "ECSOC ’26 GLOBAL RANK", "tier 1 developer",        PINK, "dbl"),
             ("16K+", "LINKEDIN FOLLOWERS",    "building in public",      BLUE, "wave"),
             ("16+",  "OPEN-SOURCE PROJECTS",  "java / spring ecosystem", LIME, "rays")]
    p = lambda s: round(s / T * 100, 2)
    css, b = "", []
    b.append(f'<g transform="rotate(-2 150 38)"><rect x="40" y="20" width="236" height="32" fill="{LAV}" fill-opacity=".92"/>'
             f'<text class="m" x="158" y="41" text-anchor="middle" font-size="12.5" font-weight="700" letter-spacing="3" fill="{INK}">SELECTED HIGHLIGHTS</text></g>')
    b.append(f'<text class="m" x="960" y="40" text-anchor="end" font-size="13" letter-spacing="1" fill="{GREY}">proof + promises</text>')
    css += c.draw_kf("tp", .2, .5, True, T)
    for i, (num, lab, sub, col, kind) in enumerate(items):
        cx = 130 + i * 247
        by = 150
        S = .6 + i * .45
        advs = [ADV.get(ch, 46) for ch in num]
        x = cx - sum(advs) / 2
        rot = (-1.5, 1.0, -1.0, 1.5)[i]
        css += (f"@keyframes g{i}{{0%,{p(S-.3)}%{{opacity:0}}{p(S)}%,90%{{opacity:1}}94%,100%{{opacity:0}}}}.g{i}{{animation:g{i} {T}s linear infinite}}")
        css += c.draw_kf(f"sc{i}", S + 1.5, .7, True, T)
        css += (f"@keyframes lb{i}{{0%,{p(S+1.4)}%{{opacity:0;transform:translateY(8px)}}{p(S+1.9)}%,90%{{opacity:1;transform:none}}94%,100%{{opacity:0;transform:translateY(8px)}}}}.lb{i}{{animation:lb{i} {T}s ease-out infinite}}")
        b.append(f'<g transform="rotate({rot} {cx} 140)">')
        # scribble behind number
        tw = sum(advs)
        if kind == "oval":
            sc = f'<path d="{oval(cx, by-27, tw/2+22, 44)}" fill="none" stroke="{col}" stroke-width="5.5" stroke-linecap="round"/>'
        elif kind == "dbl":
            sc = (f'<path d="M{cx-tw/2-4} {by+14} Q{cx} {by+6} {cx+tw/2+6} {by+13}" fill="none" stroke="{col}" stroke-width="5.5" stroke-linecap="round"/>'
                  f'<path d="M{cx-tw/2+8} {by+25} Q{cx+6} {by+18} {cx+tw/2-4} {by+24}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round"/>')
        elif kind == "wave":
            sc = (f'<path d="{wave(cx-tw/2-4, cx+tw/2+6, by+16, 6, 28)}" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
                  f'<path d="M{cx+tw/2+16} {by-78} l6 14 l15 2 l-11 10 l3 15 l-13 -8 l-13 8 l3 -15 l-11 -10 l15 -2 z" fill="{col}" stroke="{INK}" stroke-width="2" stroke-linejoin="round" transform="translate(-6 8) scale(.8)"/>')
        else:
            ex = cx + tw / 2 + 12
            sc = "".join(f'<path d="M{ex+dx} {by-70+dy} l{rx} {ry}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
                         for dx, dy, rx, ry in ((6, 0, 10, -14), (18, 12, 17, -6), (0, -6, 2, -18)))
            sc += f'<path d="M{cx-tw/2} {by+16} L{cx+tw/2+4} {by+16}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
        b.append(sc.replace('<path ', f'<path class="sc{i}" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" '))
        # odometer number
        b.append(f'<g class="g{i}">')
        px = x
        for k, ch in enumerate(num):
            a = advs[k]
            if ch.isdigit():
                d = int(ch)
                nm = f"od{i}_{k}"
                css += (f"@keyframes {nm}{{0%,{p(S)}%{{transform:translateY(0)}}{p(S+1.5)}%,94%{{transform:translateY({-L*d:.0f}px)}}94.1%,100%{{transform:translateY(0)}}}}"
                        f".{nm}{{animation:{nm} {T}s cubic-bezier(.2,.8,.2,1) infinite}}")
                digs = "".join(f'<text x="{px+a/2:.1f}" y="{by+L*j:.0f}" text-anchor="middle" font-size="{SZ}" font-weight="900" fill="{CREAM}">{j}</text>' for j in range(10))
                b.append(f'<clipPath id="oc{i}{k}"><rect x="{px-2:.1f}" y="{by-SZ*.8:.0f}" width="{a+4}" height="{SZ*1.0:.0f}"/></clipPath>'
                         f'<g clip-path="url(#oc{i}{k})"><g class="{nm}">{digs}</g></g>')
            else:
                b.append(f'<text x="{px+a/2:.1f}" y="{by}" text-anchor="middle" font-size="{SZ}" font-weight="900" fill="{CREAM}">{ch}</text>')
            px += a
        b.append('</g>')
        b.append(f'<g class="lb{i}"><text class="m" x="{cx}" y="{by+54}" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="2" fill="{col}">{lab}</text>'
                 f'<text x="{cx}" y="{by+76}" text-anchor="middle" font-size="15" font-style="italic" fill="{CREAM}" fill-opacity=".75">{sub}</text></g>')
        b.append('</g>')
    return c.svg(W, H, css, "".join(b))

# ------------------------------------------------------------ paragraph
def paragraph():
    W, T, SZ, LH = 1000, 16.0, 21, 46
    BAR = None
    lines = [
        [("B.Tech CSE", BLUE), ("student", None), ("at", None), ("JMIT Radaur", None), ("(CGPA 7.9)", "oval:" + PINK), ("and", None), ("Backend Developer Intern at Enginow.", ORG)],
        [("I build", None), ("secure, scalable Java / Spring Boot systems", LIME), ("and care about the hard parts:", None)],
        [("exactly-once execution,", YEL), ("concurrency, auth, caching and payments,", None)],
        [("all", None), ("load-tested", "wave:" + PINK), ("before I call them done.", None)],
    ]
    H = 40 + LH * len(lines) + 20
    css, b, k = "", [], 0
    sp = est(" ", SZ)
    for li, line in enumerate(lines):
        y = 58 + li * LH
        x = 44
        for text, hl in line:
            w = round(est(text, SZ))
            kind, col = (hl.split(":") + [None])[:2] if hl and ":" in hl else (("mark", hl) if hl else (None, None))
            if kind == "oval":
                x += 12
            if kind:
                S = 1.0 + k * .85; k += 1
                css += c.draw_kf(f"h{k}", S, .6, True, T)
                if kind == "mark":
                    b.append(f'<line class="h{k}" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" x1="{x-6}" y1="{y-7}" x2="{x+w+6}" y2="{y-9}" stroke="{col}" stroke-width="29" stroke-opacity=".97"/>')
                elif kind == "oval":
                    b.append(f'<path class="h{k}" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="{oval(x+w/2, y-8, w/2+12, 20)}" fill="none" stroke="{col}" stroke-width="3.5" stroke-linecap="round"/>')
                else:
                    b.append(f'<path class="h{k}" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="{wave(x, x+w, y+9, 4, 18)}" fill="none" stroke="{col}" stroke-width="3.5" stroke-linecap="round"/>')
            fill = INK if kind == "mark" else CREAM
            wt = 800 if kind else 500
            b.append(f'<text x="{x}" y="{y}" font-size="{SZ}" font-weight="{wt}" fill="{fill}" textLength="{w}" lengthAdjust="spacingAndGlyphs">{text}</text>')
            x += w + sp + (12 if kind == "oval" else 0)
    return c.svg(W, H, css, "".join(b))

if __name__ == "__main__":
    out = {"hd-about.svg": heading("01", "about me", YEL, LIME, "// the short version"),
           "terminal-note.svg": terminal(), "highlights-note.svg": highlights(), "about-note.svg": paragraph()}
    for n, s in out.items():
        (D / n).write_text(s, encoding="utf-8"); print("wrote", n, len(s), "B")
