#!/usr/bin/env python3
"""GitHub Analytics as a graph-paper lab sheet with hand-drawn charts. Numbers are parsed from the cached stat files
(assets/stats.svg, assets/ext/streak-*.svg, assets/ext/leetcard-*.svg) so refreshing those refreshes this.
Outputs analytics-sheet.svg + hd-stats.svg. Run from repo root: python3 scripts/gen_analytics_sheet.py"""
import sys, re, math, random, glob
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cover_notes as c
import gen_about_notes as a

D, INK, PAPER = c.D, c.INK, c.PAPER
ROOT = D.parent
YEL, LIME, PINK, BLUE, ORG, LAV = c.YEL, c.LIME, c.PINK, c.BLUE, c.ORG, c.LAV
T = 20.0
P = lambda s: round(s / T * 100, 2)

def texts(path):
    s = Path(path).read_text(encoding="utf-8")
    return [re.sub(r"\s+", " ", t).strip() for t in re.findall(r"<text[^>]*>([^<]+)</text>", s) if t.strip()]

def load():
    st = texts(ROOT / "stats.svg")
    keys = ("Public repos", "Total stars", "Commits (all time)", "Pull requests", "Followers")
    stats = {st[i]: st[i + 1] for i in range(1, len(st) - 1) if st[i] in keys}
    langs = [(st[i], float(st[i + 1].rstrip("%"))) for i in range(len(st) - 1) if st[i + 1].endswith("%") and st[i] not in stats]
    sk = texts(glob.glob(str(ROOT / "ext" / "streak-*.svg"))[0])
    streak = {"total": sk[0], "since": sk[2], "cur_range": sk[4], "cur": sk[5], "longest": sk[6], "long_range": sk[8]}
    lc = texts(glob.glob(str(ROOT / "ext" / "leetcard-*.svg"))[0])
    i = lc.index("Easy")
    leet = {"total": lc[i - 1], "easy": lc[i + 1], "medium": lc[i + 3], "hard": lc[i + 5],
            "rating": lc[lc.index("Contest Rating") + 1], "peak": lc[lc.index("Highest Rating") + 1]}
    return stats, langs, streak, leet

class K:
    def __init__(self):
        self.css, self.n = [], 0
    def fade(self, inner, S, dy=-8, dur=.4):
        self.n += 1; k = self.n
        self.css.append(f"@keyframes f{k}{{0%,{P(S)}%{{opacity:0;transform:translateY({dy}px)}}{P(S+dur)}%,93%{{opacity:1;transform:none}}96.5%,100%{{opacity:0;transform:translateY({dy}px)}}}}.f{k}{{animation:f{k} {T}s ease-out infinite}}")
        return f'<g class="f{k}">{inner}</g>'
    def mark(self, x1, x2, y, col, S, h=22, dur=.5):
        self.n += 1; k = self.n
        self.css.append(c.draw_kf(f"m{k}", S, dur, True, T))
        return f'<line class="m{k}" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" x1="{x1}" y1="{y}" x2="{x2}" y2="{y-2}" stroke="{col}" stroke-width="{h}" stroke-opacity=".95"/>'
    def odo(self, text, x, y, size, S, dur, fill, adv, comma=14):
        Lh = size * 1.22; out = []
        for ch in text:
            aw = comma if ch == "," else adv
            if ch.isdigit():
                self.n += 1; k = self.n; digit = int(ch); tgt = digit if digit else 10
                self.css.append(f"@keyframes o{k}{{0%,{P(S)}%{{transform:translateY(0)}}{P(S+dur)}%,93%{{transform:translateY({-Lh*tgt:.0f}px)}}93.1%,100%{{transform:translateY(0)}}}}.o{k}{{animation:o{k} {T}s cubic-bezier(.3,.7,.3,1) infinite}}")
                digs = "".join(f'<text class="m" x="{x+aw/2:.1f}" y="{y+Lh*j:.0f}" text-anchor="middle" font-size="{size}" font-weight="900" fill="{fill}">{j%10}</text>' for j in range(11))
                out.append(f'<clipPath id="oc{k}"><rect x="{x-1:.1f}" y="{y-size*.85:.0f}" width="{aw+2:.1f}" height="{size*1.05:.0f}"/></clipPath><g clip-path="url(#oc{k})"><g class="o{k}">{digs}</g></g>')
            else:
                out.append(f'<text class="m" x="{x+aw/2:.1f}" y="{y}" text-anchor="middle" font-size="{size}" font-weight="900" fill="{fill}">{ch}</text>')
            x += aw
        return "".join(out)

def width_of(text, adv, comma=14):
    return sum(comma if ch == "," else adv for ch in text)

def build():
    stats, langs, streak, leet = load()
    k = K(); W, Y0, Y1 = 1000, 26, 572
    H = Y1 + 60
    sheet = a.torn(24, Y0, 976, Y1, amp=6, step=14)
    defs = ['<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0 H0 V24" fill="none" stroke="#cfd9f0" stroke-width="1.1"/></pattern>']
    b = [f'<g transform="rotate(-0.35 500 300)"><path d="{sheet}" transform="translate(8 8)" fill="{LIME}"/>',
         f'<path d="{sheet}" fill="{PAPER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>',
         f'<path d="{sheet}" fill="url(#grid)"/>',
         f'<g transform="rotate(-5 80 28)"><rect x="40" y="14" width="86" height="26" fill="{YEL}" fill-opacity=".85"/></g>',
         f'<g transform="rotate(4 920 28)"><rect x="876" y="14" width="86" height="26" fill="{PINK}" fill-opacity=".8"/></g>']
    big = [(stats["Commits (all time)"], "commits, all time", YEL), (stats["Pull requests"], "pull requests", PINK),
           (stats["Public repos"], "public repos", BLUE), (streak["total"], "contributions", LIME)]
    for i, (num, lab, col) in enumerate(big):
        cx = 150 + i * 232
        txt = f"{int(num.replace(',', '')):,}"
        w = width_of(txt, 35)
        S = .7 + i * .4
        b.append(k.odo(txt, cx - w / 2, 112, 58, S, 1.6, INK, 35))
        lw = len(lab) * 9.6 + 22
        b.append(k.mark(cx - lw / 2, cx + lw / 2, 146, col, S + .5))
        b.append(k.fade(f'<text class="m" x="{cx}" y="151" text-anchor="middle" font-size="14.5" font-weight="800" fill="{INK}">{lab}</text>', S + .5))
    nx = 150 + 232 + 88
    b.append(k.fade(f'<text x="{nx}" y="188" font-size="14" font-style="italic" fill="{INK}" fill-opacity=".6" transform="rotate(-4 {nx} 188)">(not a typo)</text>', 2.4))
    since = streak["since"].split(" - ")[0].lower()
    b.append(k.fade(f'<text class="m" x="{150+3*232}" y="188" text-anchor="middle" font-size="11.5" fill="{INK}" fill-opacity=".55">since {since}</text>', 2.4))
    b.append(f'<path d="M48 208 H952" stroke="{INK}" stroke-opacity=".3" stroke-width="2" stroke-dasharray="6 7"/>')
    # languages donut
    b.append(k.mark(46, 190, 246, ORG, 3.0, 24))
    b.append(k.fade(f'<text x="54" y="252" font-size="18" font-weight="900" fill="{INK}">languages</text>', 3.0))
    cx, cy, r = 112, 372, 60
    C = 2 * math.pi * r
    tot = sum(v for _, v in langs); start = 0; cols = [ORG, BLUE, PINK, YEL, LIME]
    legend = []
    for j, (nm, v) in enumerate(langs):
        ln = C * v / tot; S = 3.4 + j * .5
        k.n += 1; q = k.n
        k.css.append(f"@keyframes sl{q}{{0%,{P(S)}%{{stroke-dasharray:0 {C:.1f}}}{P(S+.5)}%,93%{{stroke-dasharray:{ln-2:.1f} {C:.1f}}}96.5%,100%{{stroke-dasharray:0 {C:.1f}}}}}.sl{q}{{animation:sl{q} {T}s ease-out infinite}}")
        for sw, col in ((42, INK), (34, cols[j % 5])):
            b.append(f'<circle class="sl{q}" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-dashoffset="{-start:.1f}" transform="rotate(-90 {cx} {cy})"/>')
        start += ln
        legend.append(f'<rect x="198" y="{cy-52+j*26}" width="16" height="16" rx="3" fill="{cols[j%5]}" stroke="{INK}" stroke-width="2.4"/>'
                      f'<text class="m" x="222" y="{cy-39+j*26}" font-size="12.5" font-weight="700" fill="{INK}">{nm} {v:.0f}%</text>')
    b.append(k.fade("".join(legend), 5.6))
    # streak grid
    b.append(k.mark(348, 590, 246, LIME, 4.2, 24))
    b.append(k.fade(f'<text x="356" y="252" font-size="18" font-weight="900" fill="{INK}">longest streak: {streak["longest"]} days</text>', 4.2))
    gx, gy, rows_n = 358, 276, 7
    rnd = random.Random(3); cells = []
    shades = ["#2ecc71", "#27ae60", "#58d68d", "#1fa65a"]
    for q in range(int(streak["longest"])):
        col_i, row_i = divmod(q, rows_n)
        cells.append(f'<rect x="{gx+col_i*20}" y="{gy+row_i*20}" width="16" height="16" rx="3" fill="{rnd.choice(shades)}" stroke="{INK}" stroke-width="1.6"/>')
    gw = ((int(streak["longest"]) - 1) // rows_n + 1) * 20
    k.css.append(f"@keyframes gr{{0%,{P(4.7)}%{{width:0}}{P(7.0)}%,93%{{width:{gw+4}px}}96.5%,100%{{width:0}}}}.gr{{animation:gr {T}s linear infinite}}")
    defs.append(f'<clipPath id="gc"><rect class="gr" x="{gx-3}" y="{gy-4}" width="0" height="150"/></clipPath>')
    b.append(f'<g clip-path="url(#gc)">{"".join(cells)}</g>')
    b.append(k.fade(f'<text class="m" x="{gx}" y="{gy+168}" font-size="12" fill="{INK}" fill-opacity=".65">{streak["long_range"].lower()}</text>', 7.0))
    k.css.append("@keyframes fk{0%,100%{transform:scaleY(1) skewX(0)}50%{transform:scaleY(1.12) skewX(-4deg)}}.fk{transform-box:fill-box;transform-origin:50% 100%;animation:fk .5s ease-in-out infinite}")
    flame = (f'<g transform="translate(374 {gy+214})"><g class="fk"><path d="M0 14 C-16 8 -14 -10 -4 -22 C-4 -10 4 -10 6 -26 C18 -14 22 4 12 14 C8 20 -6 20 0 14 Z" fill="{ORG}" stroke="{INK}" stroke-width="2.8" stroke-linejoin="round"/>'
             f'<path d="M0 14 C-6 10 -4 2 2 -4 C4 4 10 6 8 12 C6 18 -2 18 0 14 Z" fill="{YEL}"/></g></g>'
             f'<text x="402" y="{gy+212}" font-size="16" font-weight="900" fill="{INK}">current: {streak["cur"]} days</text>'
             f'<text class="m" x="402" y="{gy+228}" font-size="11.5" fill="{INK}" fill-opacity=".65">{streak["cur_range"].lower()}</text>')
    b.append(k.fade(flame, 7.4))
    # leetcode
    b.append(k.mark(676, 800, 246, PINK, 5.0, 24))
    b.append(k.fade(f'<text x="684" y="252" font-size="18" font-weight="900" fill="{INK}">leetcode</text>', 5.0))
    b.append(k.odo(leet["total"], 690, 328, 54, 5.3, 1.4, INK, 33))
    b.append(k.fade(f'<text class="m" x="{690+width_of(leet["total"],33)+10}" y="326" font-size="14" font-weight="800" fill="{INK}">solved</text>', 5.5))
    solved = {n: int(leet[n].split(" / ")[0]) for n in ("easy", "medium", "hard")}
    mx = max(solved.values())
    for j, (n, col) in enumerate((("easy", LIME), ("medium", ORG), ("hard", PINK))):
        y = 362 + j * 38; S = 6.0 + j * .35
        wbar = max(14, 140 * solved[n] / mx)
        k.n += 1; q = k.n
        k.css.append(f"@keyframes br{q}{{0%,{P(S)}%{{transform:scaleX(0)}}{P(S+.55)}%,93%{{transform:scaleX(1)}}96.5%,100%{{transform:scaleX(0)}}}}.br{q}{{transform-box:fill-box;transform-origin:0 50%;animation:br{q} {T}s cubic-bezier(.2,.8,.2,1) infinite}}")
        b.append(f'<text class="m" x="690" y="{y+5}" font-size="12.5" font-weight="700" fill="{INK}">{n}</text>')
        b.append(f'<rect class="br{q}" x="750" y="{y-12}" width="{wbar:.0f}" height="24" rx="6" fill="{col}" stroke="{INK}" stroke-width="2.6"/>')
        b.append(k.fade(f'<text class="m" x="{750+wbar+10:.0f}" y="{y+5}" font-size="12" fill="{INK}" fill-opacity=".75">{leet[n]}</text>', S + .5, dur=.3))
    k.css.append(c.slam_kf("rt", 7.8, True, T)); k.css.append(c.slam_kf("st1", 8.2, True, T)); k.css.append(c.slam_kf("st2", 8.6, True, T))
    b.append(c.sticker(768, 498, 224, 38, f"contest rating {leet['rating']}", YEL, -2, "rt", 14))
    b.append(k.fade(f'<text class="m" x="768" y="536" text-anchor="middle" font-size="11.5" fill="{INK}" fill-opacity=".65">peak {leet["peak"]}</text>', 8.4))
    b.append(c.sticker(150, 515, 150, 34, f"{stats['Total stars']} stars", LAV, 3, "st1", 14))
    b.append(c.sticker(318, 520, 170, 34, f"{stats['Followers']} followers", ORG, -3, "st2", 14))
    b.append("</g>")
    return c.svg(W, H, "text{text-rendering:optimizeSpeed}" + "".join(k.css), "".join(b), "".join(defs))

if __name__ == "__main__":
    out = {"analytics-sheet.svg": build(), "hd-stats.svg": a.heading("08", "github analytics", LIME, PINK, "// the numbers, unfiltered")}
    for n, s in out.items():
        (D / n).write_text(s, encoding="utf-8"); print("wrote", n, len(s) // 1024 or 1, "KB")
