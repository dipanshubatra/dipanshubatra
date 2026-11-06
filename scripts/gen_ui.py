#!/usr/bin/env python3
"""Generates every animated SVG for the profile README into assets/ui/ (pure SVG+CSS, self-hosted)."""
import random, sys
from html import escape as E
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/ui")
OUT.mkdir(parents=True, exist_ok=True)
SANS = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "'Fira Code','SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace"
WHITE, MUTED, CYAN, VIOLET, GOLD = "#f1f5f9", "#94a3b8", "#22d3ee", "#a78bfa", "#f5b942"
random.seed(11)


def wr(name, w, h, defs, css, body):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
         f'<defs>{defs}</defs><style>text{{font-family:{SANS}}}.m{{font-family:{MONO}}}{css}</style>{body}</svg>')
    (OUT / name).write_text(s, encoding="utf-8")


def pw(t, fs=13, pad=28):
    return round(len(t) * fs * 0.56 + pad)


def typing(lines, total, slot, fs, W, y, cls="m", fill=CYAN, prefix="t"):
    """Typewriter cycle: one line at a time, centred. Returns (css, svg)."""
    n, css, body = len(lines), "", ""
    for i, line in enumerate(lines):
        width = len(line) * fs * 0.6
        x = (W - width) / 2
        s = i / n * 100
        te = s + 0.34 * slot / total * 100
        hold = s + 0.93 * slot / total * 100
        css += (f"@keyframes {prefix}{i}{{0%,{s:.2f}%{{width:0}}{te:.2f}%,{hold:.2f}%{{width:{width + 8:.0f}px}}"
                f"{min(hold + .01, 99.99):.2f}%,100%{{width:0}}}}.{prefix}c{i}{{animation:{prefix}{i} {total}s linear infinite}}")
        body += (f'<clipPath id="{prefix}p{i}"><rect class="{prefix}c{i}" x="{x:.1f}" y="{y - fs - 6}" width="0" height="{fs + 18}"/></clipPath>'
                 f'<text class="{cls}" x="{x:.1f}" y="{y}" font-size="{fs}" font-weight="600" fill="{fill}" '
                 f'clip-path="url(#{prefix}p{i})">{E(line)}</text>')
    return css, body


WAVE = "M0 40 Q125 0 250 40 T500 40 T750 40 T1000 40 T1250 40 T1500 40 T1750 40 T2000 40 T2250 40 T2500 40 V200 H0 Z"


def waves(y0):
    out = ""
    for i, (op, dx) in enumerate([(.16, 0), (.24, -120), (.4, -260)]):
        out += (f'<g transform="translate({dx} {y0 + i * 12})"><g class="w w{i}" opacity="{op}">'
                f'<path d="{WAVE}" fill="url(#wg)"/></g></g>')
    return out, "".join(f".w{i}{{animation:wv {d}s linear infinite}}" for i, d in enumerate([8, 11, 15]))


# ───────────────────────────── HERO ─────────────────────────────
def hero():
    W, H = 1000, 400
    glyphs = ["{ }", "</>", "();", "01", "#", "=>", "&&", "[ ]", "λ", "::", "++", "!=", "SELECT", "@Bean"]
    parts = ""
    for _ in range(24):
        x, y = random.randint(24, 976), random.randint(390, 470)
        parts += (f'<text class="m codefloat" x="{x}" y="{y}" font-size="{random.randint(12, 21)}" '
                  f'fill="#8be9fd" opacity="0">{E(random.choice(glyphs))}</text>')
    embers = ""
    for i in range(34):
        x, y = random.randint(18, 982), random.randint(80, 390)
        r = random.choice([1.2, 1.6, 2.0, 2.4])
        delay = random.uniform(0, 9)
        dur = random.uniform(7, 13)
        color = random.choice(["#fb923c", "#f97316", "#fbbf24", "#22d3ee"])
        embers += (f'<circle class="ember e{i%6}" cx="{x}" cy="{y}" r="{r}" fill="{color}" '
                   f'style="animation-delay:{delay:.2f}s;animation-duration:{dur:.2f}s"/>')
    chips = [("ECSoC '26  ·  GLOBAL RANK 4", GOLD), ("7x HACKATHON WINNER", CYAN), ("BACKEND INTERN @ ENGINOW", VIOLET)]
    widths = [pw(t, 13, 34) for t, _ in chips]
    x = (W - sum(widths) - 14 * (len(chips) - 1)) / 2
    chip_svg = ""
    for i, ((t, c), w) in enumerate(zip(chips, widths)):
        chip_svg += (f'<g class="chip" style="animation-delay:{.6 + i*.18:.2f}s"><rect x="{x:.0f}" y="188" width="{w}" height="38" rx="19" '
                     f'fill="{c}" fill-opacity=".10" stroke="{c}" stroke-opacity=".82"/><circle class="dot" cx="{x+17:.0f}" cy="207" r="3.5" fill="{c}"/>'
                     f'<text x="{x+w/2+5:.0f}" y="212" text-anchor="middle" font-size="12.5" font-weight="700" letter-spacing=".4" fill="{WHITE}">{E(t)}</text></g>')
        x += w + 14
    tcss, tsvg = typing(["Building secure & scalable backend systems", "Java 17/21 • Spring Boot 3 • Redis • PostgreSQL",
                         "Distributed systems • concurrency • system design", "ECSoC 2026 • Global Rank 4 • Tier 1 Developer",
                         "Open to SDE & backend opportunities"], 22, 4.4, 21, W, 292)
    wsvg, _ = waves(326)
    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#03050b"/><stop offset=".48" stop-color="#10152c"/><stop offset="1" stop-color="#071b2d"/></linearGradient>
<linearGradient id="wg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f97316"/><stop offset=".45" stop-color="#22d3ee"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient>
<linearGradient id="ng" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset=".38" stop-color="#67e8f9"/><stop offset=".72" stop-color="#c4b5fd"/><stop offset="1" stop-color="#fb923c"/></linearGradient>
<linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#67e8f9" stop-opacity=".8"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<pattern id="gr" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#a5f3fc" stroke-opacity=".07"/></pattern>
<filter id="bl" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="42"/></filter>
<filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="7"/></filter>
<clipPath id="fr"><rect width="{W}" height="{H}" rx="20"/></clipPath>"""
    css = ("@keyframes wv{from{transform:translateX(0)}to{transform:translateX(-500px)}}"
           "@keyframes rise{0%{transform:translateY(0);opacity:0}12%{opacity:.35}85%{opacity:.16}100%{transform:translateY(-440px);opacity:0}}"
           "@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(55px,24px)}}"
           "@keyframes drift2{0%,100%{transform:translate(0,0)}50%{transform:translate(-45px,-22px)}}"
           "@keyframes ember{0%{transform:translateY(18px) scale(.7);opacity:0}18%{opacity:.8}78%{opacity:.55}100%{transform:translateY(-90px) scale(1.15);opacity:0}}"
           "@keyframes scan{0%{transform:translateX(-260px);opacity:0}15%{opacity:.8}85%{opacity:.65}100%{transform:translateX(1260px);opacity:0}}"
           "@keyframes fade{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}"
           "@keyframes pulse{0%,100%{opacity:.45}50%{opacity:1}}"
           ".grid{opacity:.65}.o1{animation:drift 16s ease-in-out infinite}.o2{animation:drift2 19s ease-in-out infinite}"
           ".ember{animation:ember 9s ease-in-out infinite;will-change:transform,opacity}.codefloat{animation:rise 13s linear infinite;will-change:transform,opacity}"
           ".scanline{animation:scan 9s cubic-bezier(.45,0,.55,1) infinite}.chip{animation:fade .9s ease-out both}.dot{animation:pulse 2.8s ease-in-out infinite}"
           ".nm{animation:fade 1.1s ease-out both}.sb{animation:fade 1.1s ease-out .22s both}" + waves(0)[1] + tcss +
           "@media(prefers-reduced-motion:reduce){*{animation:none!important}}")
    body = f"""<g clip-path="url(#fr)"><rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle class="o1" cx="160" cy="120" r="165" fill="#7c3aed" opacity=".38" filter="url(#bl)"/>
<circle class="o2" cx="850" cy="170" r="180" fill="#0891b2" opacity=".30" filter="url(#bl)"/>
<circle cx="520" cy="370" r="170" fill="#f97316" opacity=".13" filter="url(#bl)"/>
<rect class="grid" y="-40" width="{W}" height="{H+80}" fill="url(#gr)"/>
<path d="M0 82 H1000 M0 318 H1000" stroke="#67e8f9" stroke-opacity=".12" stroke-dasharray="3 8"/>
{parts}{embers}
<g opacity=".42"><path d="M0 350 Q150 290 300 350 T600 350 T900 350 T1200 350" fill="none" stroke="#f97316" stroke-width="1.2"/><path d="M0 360 Q150 300 300 360 T600 360 T900 360 T1200 360" fill="none" stroke="#22d3ee" stroke-width="1.2"/></g>
{wsvg}
<text class="m" x="28" y="34" font-size="10" letter-spacing="2" fill="#67e8f9" opacity=".85">SYSTEM ONLINE // DIPANSHU.DEV</text>
<text class="m" x="972" y="34" text-anchor="end" font-size="10" letter-spacing="1.5" fill="#fb923c" opacity=".9">JAVA • SPRING • DISTRIBUTED</text>
<text class="nm" x="500" y="108" text-anchor="middle" font-size="68" font-weight="850" letter-spacing="1.5" fill="url(#ng)">Dipanshu Batra</text>
<text class="sb" x="500" y="150" text-anchor="middle" font-size="18" letter-spacing="1.1" fill="#dbeafe">Backend Engineer  /  Java &amp; Spring Boot  /  Distributed Systems</text>
{chip_svg}{tsvg}
<rect class="scanline" x="0" y="0" width="240" height="1.5" fill="url(#scan)" opacity=".7"/>
<text class="m" x="28" y="378" font-size="10" fill="#64748b">BUILD // SCALE // SHIP</text>
<text class="m" x="972" y="378" text-anchor="end" font-size="10" fill="#64748b">LATENCY IS A FEATURE</text></g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="#67e8f9" stroke-opacity=".25"/>"""
    wr("hero.svg", W, H, defs, css, body)

# ───────────────────────────── TERMINAL ─────────────────────────────
def terminal():
    W, H, T = 1000, 318, 22
    script = [("$ whoami", "p", .6, 1.0),
              ("dipanshu_batra  |  backend engineer  |  java · spring boot · distributed systems", "o", 1.9, 2.0),
              ("$ cat now.txt", "p", 4.4, .9),
              ("Backend Developer Intern @ Enginow  ·  building CronVault, a multi-tenant job scheduler", "o", 5.5, 2.2),
              ("$ ls ./achievements", "p", 8.4, 1.1),
              ("ecsoc-global-rank-4/   7x-hackathon-winner/   16k-linkedin/   16+-open-source-projects/", "o", 9.7, 2.1),
              ("$ echo $STATUS", "p", 12.6, 1.0),
              ("open to SDE & backend internships", "o", 13.8, 1.6)]
    css = ("@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}@keyframes pulse{0%,100%{opacity:.5}50%{opacity:1}}"
           ".cur{animation:blink 1s steps(1) infinite}.dotb{animation:pulse 2s infinite}")
    body, y, cw, fs = "", 90, 8.45, 14
    for i, (txt, kind, st, dur) in enumerate(script):
        wpx = len(txt) * cw
        s, te, hold = st / T * 100, (st + dur) / T * 100, 94
        css += (f"@keyframes L{i}{{0%,{s:.2f}%{{width:0}}{te:.2f}%,{hold}%{{width:{wpx + 10:.0f}px}}{hold + .01}%,100%{{width:0}}}}"
                f".LC{i}{{animation:L{i} {T}s linear infinite}}")
        fill = "#e2e8f0" if kind == "p" else "#a5b4fc"
        if kind == "p":
            txt_svg = f'<tspan fill="#4ade80">$</tspan><tspan fill="{fill}">{E(txt[1:])}</tspan>'
        else:
            txt_svg = f'<tspan fill="{fill}">{E(txt)}</tspan>'
        body += (f'<clipPath id="lc{i}"><rect class="LC{i}" x="34" y="{y - 16}" width="0" height="24"/></clipPath>'
                 f'<text class="m" x="34" y="{y}" font-size="{fs}" clip-path="url(#lc{i})">{txt_svg}</text>')
        y += 23 if kind == "p" else 38
    cur_x = 34 + len(script[-1][0]) * cw + 6
    css += f"@keyframes show{{0%,{13.8 / T * 100:.1f}%{{opacity:0}}{14.5 / T * 100:.1f}%,94%{{opacity:1}}94.1%,100%{{opacity:0}}}}.sh{{animation:show {T}s linear infinite}}"
    body += f'<g class="sh"><rect class="cur" x="{cur_x:.0f}" y="{y - 38 - 14}" width="9" height="18" fill="#4ade80"/></g>'
    defs = ('<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset=".5" stop-color="#8b5cf6"/>'
            '<stop offset="1" stop-color="#22d3ee"/></linearGradient><linearGradient id="bgt" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#090c13"/></linearGradient>')
    top = ('<rect x="1" y="1" width="998" height="44" rx="14" fill="#161b26"/><rect x="1" y="30" width="998" height="16" fill="#161b26"/>'
           '<circle cx="28" cy="23" r="6.5" fill="#ff5f56"/><circle cx="50" cy="23" r="6.5" fill="#ffbd2e"/><circle cx="72" cy="23" r="6.5" fill="#27c93f"/>'
           f'<text class="m" x="500" y="28" text-anchor="middle" font-size="13" fill="{MUTED}">dipanshu@dev: ~/about</text>'
           '<circle class="dotb" cx="962" cy="23" r="4" fill="#4ade80"/><text x="948" y="27" text-anchor="end" font-size="11" fill="#64748b">online</text>')
    wr("terminal.svg", W, H, defs, css,
       f'<rect x="1" y="1" width="998" height="{H - 2}" rx="14" fill="url(#bgt)" stroke="url(#bd)" stroke-width="1.5"/>{top}{body}')


# ───────────────────────────── METRICS ─────────────────────────────
def metrics():
    items = [("7x", "Hackathon Wins", "national-level winner", "#22d3ee"), ("#4", "ECSoC '26 Global Rank", "Tier 1 Developer", GOLD),
             ("16K+", "LinkedIn Followers", "building in public", "#a78bfa"), ("16+", "Open-source Projects", "Java / Spring ecosystem", "#f472b6")]
    W, H, cw, gap = 1000, 150, 232, 24
    defs = ('<clipPath id="r"><rect width="232" height="138" rx="18"/></clipPath>'
            '<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".14"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    css = ("@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}@keyframes sw{0%{transform:translateX(-120px) skewX(-18deg)}55%,100%{transform:translateX(340px) skewX(-18deg)}}"
           "@keyframes gl{0%,100%{opacity:.35}50%{opacity:1}}")
    body = ""
    for i, (num, lab, sub, c) in enumerate(items):
        x = i * (cw + gap)
        css += (f".f{i}{{animation:fl {4 + i * .4}s ease-in-out {i * .3}s infinite}}.s{i}{{animation:sw 5s ease-in-out {i * .8}s infinite}}"
                f".g{i}{{animation:gl 3s ease-in-out {i * .5}s infinite}}")
        defs += (f'<linearGradient id="n{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{c}"/></linearGradient>'
                 f'<radialGradient id="a{i}" cx=".5" cy="0" r="1"><stop offset="0" stop-color="{c}" stop-opacity=".35"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>')
        body += (f'<g transform="translate({x} 6)"><g class="f{i}"><rect width="232" height="138" rx="18" fill="#0d1117"/><rect width="232" height="138" rx="18" fill="url(#a{i})"/>'
                 f'<g clip-path="url(#r)"><rect class="s{i}" width="60" height="138" fill="url(#sh)"/></g>'
                 f'<text x="116" y="70" text-anchor="middle" font-size="50" font-weight="800" fill="url(#n{i})">{E(num)}</text>'
                 f'<text x="116" y="98" text-anchor="middle" font-size="14.5" font-weight="600" fill="{WHITE}">{E(lab)}</text>'
                 f'<text x="116" y="119" text-anchor="middle" font-size="11.5" fill="{MUTED}">{E(sub)}</text>'
                 f'<rect class="g{i}" width="232" height="138" rx="18" fill="none" stroke="{c}" stroke-width="1.6"/></g></g>')
    wr("metrics.svg", W, H, defs, css, body)


# ───────────────────────────── MARQUEE ─────────────────────────────
def marquee():
    core, sec, tools, sysc = "#f59e0b", "#22c55e", "#a78bfa", "#f472b6"
    rows = [[("Java 17 / 21", core), ("Spring Boot 3", sec), ("Spring Security", sec), ("Hibernate / JPA", core), ("REST APIs", core),
             ("JWT rotation", sec), ("OAuth2", sec), ("RBAC", sec), ("Rate limiting · Bucket4j", sec), ("Distributed Systems", sysc),
             ("Circuit Breakers", sysc), ("Async Processing", sysc)],
            [("PostgreSQL", "#38bdf8"), ("MySQL", "#38bdf8"), ("Redis · distributed locks", "#38bdf8"), ("Docker", tools), ("GitHub Actions", tools),
             ("Maven", tools), ("JUnit 5", tools), ("JMeter", tools), ("Postman", tools), ("Resilience4j", sysc), ("HikariCP", sysc),
             ("Cashfree", tools), ("Cloudinary", tools), ("React", tools)]]
    W, H, gap = 1000, 124, 14
    defs = ('<linearGradient id="mf" x1="0" x2="1"><stop offset="0" stop-color="#000"/><stop offset=".08" stop-color="#fff"/>'
            '<stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
            '<mask id="mk"><rect width="1000" height="124" fill="url(#mf)"/></mask>')
    css, body = "", ""
    for r, row in enumerate(rows):
        total = sum(pw(t, 14, 44) + gap for t, _ in row)
        css += (f"@keyframes m{r}{{from{{transform:translateX({0 if r == 0 else -total}px)}}to{{transform:translateX({-total if r == 0 else 0}px)}}}}"
                f".mr{r}{{animation:m{r} {total / 38:.0f}s linear infinite}}")
        pills, x = "", 0
        for rep in range(2):
            for t, c in row:
                w = pw(t, 14, 44)
                pills += (f'<g transform="translate({x} 0)"><rect width="{w}" height="44" rx="22" fill="{c}" fill-opacity=".13" stroke="{c}" stroke-opacity=".7"/>'
                          f'<circle cx="20" cy="22" r="4.5" fill="{c}"/><text x="{w / 2 + 8:.0f}" y="27" text-anchor="middle" font-size="14" font-weight="600" fill="{WHITE}">{E(t)}</text></g>')
                x += w + gap
        body += f'<g transform="translate(0 {8 + r * 58})"><g class="mr{r}">{pills}</g></g>'
    wr("marquee.svg", W, H, defs, css, f'<g mask="url(#mk)">{body}</g>')


# ───────────────────────────── PROJECT CARDS ─────────────────────────────
def project(name, tag, title, sub, stats, bullets, tech, c1, c2, live=True):
    W, H = 490, 414
    defs = (f'<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
            f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f1320"/><stop offset="1" stop-color="#0a0c14"/></linearGradient>'
            f'<radialGradient id="gl" cx=".15" cy="0" r="1"><stop offset="0" stop-color="{c1}" stop-opacity=".28"/><stop offset="1" stop-color="{c1}" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="cl"><rect x="3" y="3" width="{W - 6}" height="{H - 6}" rx="22"/></clipPath>')
    css = ("@keyframes sw{0%{transform:translateX(-140px) skewX(-18deg)}50%,100%{transform:translateX(640px) skewX(-18deg)}}@keyframes pl{0%,100%{opacity:.4}50%{opacity:1}}"
           "@keyframes ln{from{stroke-dashoffset:0}to{stroke-dashoffset:-60}}.sw{animation:sw 6s ease-in-out infinite}.pl{animation:pl 1.6s infinite}.bd{animation:pl 3.2s ease-in-out infinite}"
           ".ln{stroke-dasharray:6 6;animation:ln 2s linear infinite}")
    b = (f'<rect x="3" y="3" width="{W - 6}" height="{H - 6}" rx="22" fill="url(#bg)"/><rect x="3" y="3" width="{W - 6}" height="{H - 6}" rx="22" fill="url(#gl)"/>'
         f'<g clip-path="url(#cl)"><rect class="sw" y="0" width="70" height="{H}" fill="url(#sh)"/></g>'
         f'<text class="m" x="28" y="42" font-size="11.5" letter-spacing="2.5" fill="{c1}">{E(tag)}</text>')
    if live:
        b += (f'<rect x="{W - 98}" y="24" width="72" height="26" rx="13" fill="#22c55e" fill-opacity=".14" stroke="#22c55e" stroke-opacity=".7"/>'
              f'<circle class="pl" cx="{W - 82}" cy="37" r="4" fill="#22c55e"/><text x="{W - 54}" y="41.5" text-anchor="middle" font-size="11.5" font-weight="700" fill="#4ade80">LIVE</text>')
    b += (f'<text x="28" y="82" font-size="26" font-weight="800" fill="{WHITE}">{E(title)}</text><text x="28" y="106" font-size="13.5" fill="{MUTED}">{E(sub)}</text>'
          f'<line class="ln" x1="28" y1="122" x2="{W - 28}" y2="122" stroke="{c1}" stroke-opacity=".5"/>')
    for i, (num, lab) in enumerate(stats):
        x = 28 + i * 148
        b += (f'<rect x="{x}" y="138" width="136" height="62" rx="12" fill="#fff" fill-opacity=".04" stroke="#fff" stroke-opacity=".08"/>'
              f'<text x="{x + 68}" y="168" text-anchor="middle" font-size="22" font-weight="800" fill="{c1}">{E(num)}</text>'
              f'<text x="{x + 68}" y="188" text-anchor="middle" font-size="11" fill="{MUTED}">{E(lab)}</text>')
    y = 230
    for t in bullets:
        b += (f'<path d="M34 {y - 9} l5 5 -5 5 -5 -5z" fill="{c2}"/><text x="50" y="{y}" font-size="13.5" fill="#cbd5e1">{E(t)}</text>')
        y += 27
    x, y = 28, y + 4
    for t in tech:
        w = pw(t, 11.5, 24)
        if x + w > W - 24:
            x, y = 28, y + 30
        b += (f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="{c1}" fill-opacity=".12" stroke="{c1}" stroke-opacity=".5"/>'
              f'<text x="{x + w / 2}" y="{y + 16}" text-anchor="middle" font-size="11.5" font-weight="600" fill="{WHITE}">{E(t)}</text>')
        x += w + 8
    b += f'<rect class="bd" x="3" y="3" width="{W - 6}" height="{H - 6}" rx="22" fill="none" stroke="url(#bd)" stroke-width="2"/>'
    wr(name, W, H, defs, css, b)


# ───────────────────────────── JOURNEY ─────────────────────────────
def journey():
    W, H = 1000, 250
    items = [("2025", "B.Tech CSE", "JMIT Radaur · 2025–2029 · CGPA 7.9", "#22d3ee"),
             ("2025 – 26", "Hackathon streak", "7x national-level winner", GOLD),
             ("SUMMER 2026", "ECSoC '26", "Global Rank 4 · Tier 1 Developer", "#f472b6"),
             ("SEP 2026 – NOW", "Backend Intern", "Enginow · Java 17 · Spring Boot 3", "#a78bfa")]
    defs = ('<linearGradient id="lg" x1="0" x2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset=".5" stop-color="#f472b6"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>'
            '<filter id="g"><feGaussianBlur stdDeviation="5"/></filter><path id="pt" d="M60 70 H940"/>')
    css = "@keyframes pl{0%,100%{transform:scale(1);opacity:.5}50%{transform:scale(1.8);opacity:0}}@keyframes fd{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
    body = '<rect x="60" y="68" width="880" height="4" rx="2" fill="url(#lg)" opacity=".5"/>'
    body += '<circle r="9" fill="#fff" filter="url(#g)"><animateMotion dur="7s" repeatCount="indefinite"><mpath href="#pt"/></animateMotion></circle>'
    body += '<circle r="4" fill="#fff"><animateMotion dur="7s" repeatCount="indefinite"><mpath href="#pt"/></animateMotion></circle>'
    for i, (when, title, sub, c) in enumerate(items):
        x = 140 + i * 240
        css += f".n{i}{{transform-box:fill-box;transform-origin:center;animation:pl 2.6s ease-out {i * .5}s infinite}}.c{i}{{animation:fd .8s ease-out {.3 + i * .25}s both}}"
        body += (f'<circle class="n{i}" cx="{x}" cy="70" r="10" fill="{c}"/><circle cx="{x}" cy="70" r="10" fill="#0d1117" stroke="{c}" stroke-width="3"/><circle cx="{x}" cy="70" r="4" fill="{c}"/>'
                 f'<g class="c{i}"><line x1="{x}" y1="86" x2="{x}" y2="108" stroke="{c}" stroke-opacity=".6"/>'
                 f'<rect x="{x - 108}" y="108" width="216" height="104" rx="16" fill="#0d1117" stroke="{c}" stroke-opacity=".55"/>'
                 f'<text class="m" x="{x}" y="134" text-anchor="middle" font-size="11.5" letter-spacing="1.5" fill="{c}">{E(when)}</text>'
                 f'<text x="{x}" y="164" text-anchor="middle" font-size="19" font-weight="800" fill="{WHITE}">{E(title)}</text>'
                 f'<text x="{x}" y="188" text-anchor="middle" font-size="11.5" fill="{MUTED}">{E(sub)}</text></g>')
    wr("journey.svg", W, H, defs, css, body)


# ───────────────────────────── WINS ─────────────────────────────
def wins():
    items = [("WINNER", "Techfrontier 2025", "IIIT Delhi · 500+ participants", GOLD), ("WINNER", "Hackastra", "NIT Durgapur", GOLD),
             ("WINNER", "Mukand Utsav 2K26", "National-level", GOLD), ("WINNER", "HackOrbit 2K26", "National-level", GOLD),
             ("WINNER", "Ideathon 2K26", "JMIT Radaur", GOLD), ("WINNER", "Shark Tank", "Pitch competition", GOLD),
             ("FINALIST", "ByteVerse", "Hackathon", "#cbd5e1"), ("GLOBAL RANK 4", "ECSoC 2026", "Tier 1 Developer", "#22d3ee")]
    W, H = 1000, 212
    star = "M0 -11 L3.2 -3.4 11 -3.4 4.8 1.6 7 9.5 0 5 -7 9.5 -4.8 1.6 -11 -3.4 -3.2 -3.4Z"
    # Keep achievement tiles still; use only a slow, subtle star highlight.
    css = ("@keyframes tw{0%,100%{opacity:.72;filter:drop-shadow(0 0 1px currentColor)}50%{opacity:1;filter:drop-shadow(0 0 6px currentColor)}}"
           "@keyframes sweep{0%,72%{transform:translateX(-270px);opacity:0}78%{opacity:.55}92%{opacity:.25}100%{transform:translateX(270px);opacity:0}}"
           "@keyframes aura{0%,100%{stroke-opacity:.48}50%{stroke-opacity:.9}}")
    body = ""
    for i, (tag, title, sub, c) in enumerate(items):
        x, y = (i % 4) * 256, (i // 4) * 108
        css += (f".w{i}{{transform:translateZ(0)}}.s{i}{{animation:tw 5.8s ease-in-out {i * .22}s infinite}}"
                f".shine{i}{{animation:sweep 7.5s cubic-bezier(.4,0,.2,1) {i * .55}s infinite}}.edge{i}{{animation:aura 5.5s ease-in-out {i * .3}s infinite}}")
        body += (f'<g class="w{i}"><g transform="translate({x} {y + 6})"><defs><clipPath id="winclip{i}"><rect width="232" height="92" rx="16"/></clipPath></defs><rect width="232" height="92" rx="16" fill="#0d1117" stroke="{c}" stroke-opacity=".65"/>'
                 f'<rect width="232" height="92" rx="16" fill="{c}" fill-opacity=".065"/><rect class="edge{i}" x=".7" y=".7" width="230.6" height="90.6" rx="15" fill="none" stroke="{c}" stroke-width="1.3"/><g clip-path="url(#winclip{i})"><path class="shine{i}" d="M-40 0 L12 0 L92 92 L38 92Z" fill="#fff" opacity="0"/></g><circle cx="40" cy="46" r="22" fill="{c}" fill-opacity=".14" stroke="{c}"/>'
                 f'<g transform="translate(40 46) scale(1.15)"><path class="s{i}" d="{star}" fill="{c}"/></g>'
                 f'<text class="m" x="76" y="30" font-size="10" letter-spacing="1.6" fill="{c}">{E(tag)}</text>'
                 f'<text x="76" y="52" font-size="15" font-weight="700" fill="{WHITE}">{E(title)}</text>'
                 f'<text x="76" y="71" font-size="11" fill="{MUTED}">{E(sub)}</text></g></g>')
    css += "@media(prefers-reduced-motion:reduce){*{animation:none!important}}"
    wr("wins.svg", W, H, "", css, body)


# ───────────────────────────── TITLES / BUTTONS / OSS ─────────────────────────────
def title(key, num, text):
    W, H = 1000, 70
    defs = ('<linearGradient id="tg" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#7dd3fc"/></linearGradient>'
            '<linearGradient id="ul" x1="0" x2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset=".6" stop-color="#22d3ee" stop-opacity=".4"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="tr" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    css = ("@keyframes tv{from{transform:translateX(-160px)}to{transform:translateX(1000px)}}@keyframes fd{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:none}}"
           ".tv{animation:tv 3.6s ease-in-out infinite}.tx{animation:fd .9s ease-out both}")
    body = (f'<g class="tx"><text class="m" x="2" y="22" font-size="13" letter-spacing="3" fill="{CYAN}">// {num}</text>'
            f'<text x="0" y="56" font-size="30" font-weight="800" fill="url(#tg)">{E(text)}</text></g>'
            '<rect x="0" y="64" width="1000" height="3" rx="1.5" fill="url(#ul)"/><rect class="tv" y="63" width="160" height="5" rx="2.5" fill="url(#tr)" opacity=".85"/>')
    wr(f"t-{key}.svg", W, H, defs, css, body)


def button(key, label, c):
    w = pw(label, 15, 62)
    defs = (f'<linearGradient id="bd" x1="0" x2="1"><stop offset="0" stop-color="{c}"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="{c}"/></linearGradient>'
            '<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="c"><rect x="2" y="2" width="{w - 4}" height="40" rx="20"/></clipPath>')
    css = (f"@keyframes sw{{0%{{transform:translateX(-50px) skewX(-20deg)}}60%,100%{{transform:translateX({w + 20}px) skewX(-20deg)}}}}@keyframes pl{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}"
           ".sw{animation:sw 3.4s ease-in-out infinite}.bd{animation:pl 2.4s infinite}")
    body = (f'<rect x="2" y="2" width="{w - 4}" height="40" rx="20" fill="#0d1117"/><rect x="2" y="2" width="{w - 4}" height="40" rx="20" fill="{c}" fill-opacity=".1"/>'
            f'<g clip-path="url(#c)"><rect class="sw" width="30" height="44" fill="url(#sh)"/></g><circle cx="26" cy="22" r="5" fill="{c}"/>'
            f'<text x="{w / 2 + 10}" y="28" text-anchor="middle" font-size="15" font-weight="700" fill="{WHITE}">{E(label)}</text>'
            f'<rect class="bd" x="2" y="2" width="{w - 4}" height="40" rx="20" fill="none" stroke="url(#bd)" stroke-width="2"/>')
    wr(f"btn-{key}.svg", w, 44, defs, css, body)


def oss(key, big, label, sub, c):
    W, H = 320, 118
    defs = (f'<radialGradient id="a" cx=".2" cy="0" r="1"><stop offset="0" stop-color="{c}" stop-opacity=".3"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>')
    css = "@keyframes pl{0%,100%{opacity:.4}50%{opacity:1}}@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}.bd{animation:pl 3s infinite}.fl{animation:fl 4s ease-in-out infinite}"
    body = (f'<g class="fl"><rect x="2" y="4" width="316" height="108" rx="18" fill="#0d1117"/><rect x="2" y="4" width="316" height="108" rx="18" fill="url(#a)"/>'
            f'<text x="26" y="64" font-size="42" font-weight="800" fill="{c}">{E(big)}</text>'
            f'<text x="26" y="88" font-size="14" font-weight="700" fill="{WHITE}">{E(label)}</text><text x="26" y="104" font-size="11" fill="{MUTED}">{E(sub)}</text>'
            f'<path d="M286 30 l12 0 0 12 M298 30 l-16 16" stroke="{c}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
            f'<rect class="bd" x="2" y="4" width="316" height="108" rx="18" fill="none" stroke="{c}" stroke-width="1.6"/></g>')
    wr(f"oss-{key}.svg", W, H, defs, css, body)


hero(); terminal(); metrics(); marquee()
project("novamart.svg", "FEATURED PROJECT  /  01", "NovaMart", "Distributed e-commerce platform  ·  React + Spring Boot",
        [("0%", "error rate"), ("182ms", "avg latency"), ("326ms", "P95 latency")],
        ["5,250+ concurrent requests, verified with JMeter", "JWT rotation + Google OAuth2 + Redis OTP store",
         "Cashfree webhook signature checks, no double-charge", "Reservation-based inventory locking, no overselling"],
        ["Java 17", "Spring Boot 3", "Spring Security", "PostgreSQL", "Redis", "Cashfree", "Cloudinary", "Docker", "React"], "#22d3ee", "#a78bfa")
project("cronvault.svg", "FEATURED PROJECT  /  02", "CronVault", "Multi-tenant distributed job scheduler",
        [("1x", "exactly-once runs"), ("9", "RBAC permissions"), ("60s", "crash recovery")],
        ["Exactly-once execution via DB pessimistic locking", "Custom RBAC across tenants, with full audit log",
         "Lua sliding-window rate limiter, fails open to DB", "Per-tenant circuit breakers using Resilience4j"],
        ["Java 21", "Spring Boot 3", "Spring Security", "MySQL", "Redis + Lua", "Resilience4j"], "#f472b6", "#f5b942")
journey(); wins()
for k, n, t in [("about", "01", "About Me"), ("ecsoc", "02", "ECSoC '26"), ("projects", "03", "Featured Projects"), ("stack", "04", "Tech Stack"),
                ("wins", "05", "Achievements"), ("journey", "06", "Journey"), ("oss", "07", "Open Source"), ("stats", "08", "GitHub Analytics")]:
    title(k, n, t)
for k, l, c in [("linkedin", "LinkedIn", "#0a66c2"), ("github", "GitHub", "#a78bfa"), ("leetcode", "LeetCode", "#ffa116"),
                ("x", "X / Twitter", "#e2e8f0"), ("portfolio", "Portfolio", "#22d3ee")]:
    button(k, l, c)
oss("medtrack", "94", "MedTrack_Application", "commits  ·  kRamu81/MedTrack_Application", "#22d3ee")
oss("mailgenie", "24", "MailGenie", "commits  ·  Nicode2707/MailGenie", "#a78bfa")
oss("ecsoc", "16+", "Open-source projects", "Java / Spring ecosystem  ·  ECSoC Global Rank 4", "#f5b942")
print("generated", len(list(OUT.glob("*.svg"))), "svgs ->", OUT)
