#!/usr/bin/env python3
"""GitHub Analytics v2: five big full-width pieces (large text, poster-style numbers with hard shadows).
Reads cached stat files via gen_analytics_sheet.load(). Outputs an-nums, an-lang, an-streak, an-leet, an-snake-head (.svg).
Run from repo root: python3 scripts/gen_analytics.py   (also run nightly by the localize workflow)"""
import sys, math, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cover_notes as c
import gen_about_notes as a
import gen_analytics_sheet as s0

D, INK, CREAM, GREY = c.D, c.INK, a.CREAM, a.GREY
YEL, LIME, PINK, BLUE, ORG, LAV = c.YEL, c.LIME, c.PINK, c.BLUE, c.ORG, c.LAV
T = s0.T
P = s0.P

def pop_number(k, text, x, y, size, S, dur, accent, adv, comma):
    """cream number with an offset accent copy behind it = poster-style hard shadow"""
    return k.odo(text, x + 6, y + 6, size, S, dur, accent, adv, comma) + k.odo(text, x, y, size, S, dur, CREAM, adv, comma)

def grow_bar(k, x, y, w, h, fill, S, outline=CREAM, sw=4, rx=12):
    k.n += 1; q = k.n
    k.css.append(f"@keyframes br{q}{{0%,{P(S)}%{{transform:scaleX(0)}}{P(S+.6)}%,93%{{transform:scaleX(1)}}96.5%,100%{{transform:scaleX(0)}}}}"
                 f".br{q}{{transform-box:fill-box;transform-origin:0 50%;animation:br{q} {T}s cubic-bezier(.2,.8,.2,1) infinite}}")
    return f'<rect class="br{q}" x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{rx}" fill="{fill}" stroke="{outline}" stroke-width="{sw}"/>'

def wrap_svg(k, W, H, body, defs=""):
    return c.svg(W, H, "text{text-rendering:optimizeSpeed}" + "".join(k.css), "".join(body), defs)

def piece_nums(stats, streak):
    k = s0.K(); W, H = 1000, 280; b = []
    items = [(stats["Commits (all time)"], "commits", "all time", YEL), (stats["Pull requests"], "pull requests", "opened", PINK),
             (stats["Public repos"], "public repos", "and counting", BLUE), (streak["total"], "contributions", "since " + streak["since"].split(" - ")[0].lower(), LIME)]
    for i, (num, lab, sub, col) in enumerate(items):
        cx = 140 + i * 240
        txt = f"{int(num.replace(',', '')):,}"
        w = s0.width_of(txt, 50, 20)
        S = .5 + i * .35
        rot = (-1.5, 1.0, -1.0, 1.5)[i]
        b.append(f'<g transform="rotate({rot} {cx} 130)">')
        b.append(pop_number(k, txt, cx - w / 2, 126, 84, S, 1.6, col, 50, 20))
        lw = len(lab) * 12.5 + 34
        b.append(k.mark(cx - lw / 2, cx + lw / 2, 184, col, S + .6, 38))
        b.append(k.fade(f'<text x="{cx}" y="192" text-anchor="middle" font-size="22" font-weight="900" fill="{INK}">{lab}</text>', S + .6))
        b.append(k.fade(f'<text class="m" x="{cx}" y="232" text-anchor="middle" font-size="15.5" letter-spacing="1" fill="{CREAM}" fill-opacity=".65">{sub}</text>', S + 1.0))
        b.append('</g>')
    return wrap_svg(k, W, H, b)

def piece_lang(langs):
    k = s0.K(); W, H = 1000, 270; b = []; defs = []
    b.append(k.mark(34, 252, 60, ORG, .3, 46))
    b.append(k.fade(f'<text x="48" y="70" font-size="34" font-weight="900" fill="{INK}">languages</text>', .3))
    b.append(k.fade(f'<text x="960" y="66" text-anchor="end" font-size="19" font-style="italic" fill="{CREAM}" fill-opacity=".6">by public repo</text>', 1.0))
    X0, X1, Y0, BH = 40, 960, 108, 74
    tot = sum(v for _, v in langs); x = X0; cols = [ORG, BLUE, PINK, YEL, LIME]; segs = []; lab = []
    for j, (nm, v) in enumerate(langs):
        w = (X1 - X0) * v / tot
        segs.append(f'<rect x="{x:.1f}" y="{Y0}" width="{w:.1f}" height="{BH}" fill="{cols[j % 5]}" stroke="{INK}" stroke-width="4"/>'
                    f'<text class="m" x="{x+w/2:.1f}" y="{Y0+49}" text-anchor="middle" font-size="30" font-weight="900" fill="{INK}">{v:.0f}%</text>')
        lab.append(k.fade(f'<line x1="{x+w/2:.1f}" y1="{Y0+BH+4}" x2="{x+w/2:.1f}" y2="{Y0+BH+22}" stroke="{cols[j%5]}" stroke-width="4" stroke-linecap="round"/>'
                          f'<text x="{x+w/2:.1f}" y="{Y0+BH+50}" text-anchor="middle" font-size="24" font-weight="900" fill="{CREAM}">{nm}</text>', 2.6 + j * .25))
        x += w
    k.css.append(f"@keyframes lr{{0%,{P(1.2)}%{{width:0}}{P(2.8)}%,93%{{width:{X1-X0+12}px}}96.5%,100%{{width:0}}}}.lr{{animation:lr {T}s cubic-bezier(.3,.7,.3,1) infinite}}")
    defs.append(f'<clipPath id="lc"><rect class="lr" x="{X0-4}" y="{Y0-8}" width="0" height="{BH+16}"/></clipPath>')
    b.append(f'<rect x="{X0+7}" y="{Y0+7}" width="{X1-X0}" height="{BH}" rx="0" fill="{ORG}" fill-opacity=".35"/>')
    b.append(f'<g clip-path="url(#lc)">{"".join(segs)}</g>')
    b.append(f'<rect x="{X0-2}" y="{Y0-2}" width="{X1-X0+4}" height="{BH+4}" fill="none" stroke="{CREAM}" stroke-width="3"/>'.replace('stroke-width="3"', 'stroke-width="3" class="lo"'))
    k.css.append(f"@keyframes lo{{0%,{P(1.1)}%{{opacity:0}}{P(1.4)}%,93%{{opacity:1}}96.5%,100%{{opacity:0}}}}.lo{{animation:lo {T}s linear infinite}}")
    b.extend(lab)
    return wrap_svg(k, W, H, b, "".join(defs))

def piece_streak(streak):
    k = s0.K(); W, H = 1000, 350; b = []; defs = []
    b.append(k.mark(34, 296, 60, LIME, .3, 46))
    b.append(k.fade(f'<text x="48" y="70" font-size="34" font-weight="900" fill="{INK}">longest streak</text>', .3))
    n = int(streak["longest"]); rows = 7; pitch, cell = 31, 26
    gx, gy = 42, 98
    rnd = random.Random(3); shades = ["#2ecc71", "#27ae60", "#58d68d", "#1fa65a", "#7be495"]; cells = []
    for q in range(n):
        ci, ri = divmod(q, rows)
        cells.append(f'<rect x="{gx+ci*pitch}" y="{gy+ri*pitch}" width="{cell}" height="{cell}" rx="6" fill="{rnd.choice(shades)}" stroke="{INK}" stroke-width="2"/>')
    gw = ((n - 1) // rows + 1) * pitch
    k.css.append(f"@keyframes gr{{0%,{P(1.0)}%{{width:0}}{P(3.6)}%,93%{{width:{gw+6}px}}96.5%,100%{{width:0}}}}.gr{{animation:gr {T}s linear infinite}}")
    defs.append(f'<clipPath id="gc"><rect class="gr" x="{gx-4}" y="{gy-4}" width="0" height="{rows*pitch+8}"/></clipPath>')
    b.append(f'<g clip-path="url(#gc)">{"".join(cells)}</g>')
    b.append(k.fade(f'<text class="m" x="{gx}" y="{gy+rows*pitch+26}" font-size="16" fill="{CREAM}" fill-opacity=".65">{streak["long_range"].lower()}</text>', 3.4))
    num = str(n); w = s0.width_of(num, 92)
    b.append(pop_number(k, num, 700 - w / 2, 200, 150, 1.4, 1.6, LIME, 92, 20))
    b.append(k.mark(560, 840, 248, LIME, 3.0, 40))
    b.append(k.fade(f'<text x="700" y="256" text-anchor="middle" font-size="24" font-weight="900" fill="{INK}">days in a row</text>', 3.0))
    k.css.append("@keyframes fk{0%,100%{transform:scaleY(1) skewX(0)}50%{transform:scaleY(1.12) skewX(-4deg)}}.fk{transform-box:fill-box;transform-origin:50% 100%;animation:fk .5s ease-in-out infinite}")
    flame = (f'<g transform="translate(590 316) scale(1.7)"><g class="fk"><path d="M0 14 C-16 8 -14 -10 -4 -22 C-4 -10 4 -10 6 -26 C18 -14 22 4 12 14 C8 20 -6 20 0 14 Z" fill="{ORG}" stroke="{INK}" stroke-width="2.8" stroke-linejoin="round"/>'
             f'<path d="M0 14 C-6 10 -4 2 2 -4 C4 4 10 6 8 12 C6 18 -2 18 0 14 Z" fill="{YEL}"/></g></g>'
             f'<text x="636" y="312" font-size="28" font-weight="900" fill="{CREAM}">current: {streak["cur"]} days</text>'
             f'<text class="m" x="636" y="334" font-size="16" fill="{CREAM}" fill-opacity=".65">{streak["cur_range"].lower()}</text>')
    b.append(k.fade(flame, 4.0))
    return wrap_svg(k, W, H, b, "".join(defs))

def piece_leet(leet):
    k = s0.K(); W, H = 1000, 350; b = []
    b.append(k.mark(34, 224, 60, PINK, .3, 46))
    b.append(k.fade(f'<text x="48" y="70" font-size="34" font-weight="900" fill="{INK}">leetcode</text>', .3))
    w = s0.width_of(leet["total"], 92)
    b.append(pop_number(k, leet["total"], 50, 210, 150, 1.0, 1.5, YEL, 92, 20))
    b.append(k.mark(46, 46 + 14 * 17 + 34, 256, PINK, 2.6, 40))
    b.append(k.fade(f'<text x="64" y="264" font-size="24" font-weight="900" fill="{INK}">problems solved</text>', 2.6))
    k.css.append(c.slam_kf("rt", 4.0, True, T))
    b.append(c.sticker(210, 316, 340, 54, f"contest rating {leet['rating']}", YEL, -2, "rt", 24, label=f"PEAK {leet['peak']}"))
    solved = {nm: int(leet[nm].split(" / ")[0]) for nm in ("easy", "medium", "hard")}
    mx = max(solved.values())
    for j, (nm, col) in enumerate((("easy", LIME), ("medium", ORG), ("hard", PINK))):
        y = 116 + j * 82; S = 1.8 + j * .4
        wbar = max(30, 260 * solved[nm] / mx)
        b.append(k.fade(f'<text x="500" y="{y+9}" font-size="26" font-weight="900" fill="{CREAM}">{nm}</text>', S, dur=.3))
        b.append(grow_bar(k, 622, y - 24, wbar, 52, col, S + .1, CREAM, 4, 14))
        b.append(k.fade(f'<text class="m" x="{622+wbar+16:.0f}" y="{y+8}" font-size="22" font-weight="700" fill="{CREAM}">{leet[nm]}</text>', S + .6, dur=.3))
    return wrap_svg(k, W, H, b)

def piece_snake_head():
    k = s0.K(); W, H = 1000, 130; b = []
    b.append(f'<g transform="rotate(-4 120 70)"><rect x="22" y="38" width="96" height="30" fill="{LAV}" fill-opacity=".9"/></g>')
    b.append(k.mark(34, 456, 76, LIME, .3, 54))
    b.append(k.fade(f'<text x="48" y="88" font-size="40" font-weight="900" fill="{INK}">contribution graph</text>', .3))
    b.append(k.fade(f'<text x="960" y="84" text-anchor="end" font-size="22" font-style="italic" fill="{CREAM}" fill-opacity=".7">(the snake eats my commits)</text>', 1.2))
    b.append(k.draw_path if False else "")
    k.css.append(c.draw_kf("ar", 1.6, .6, True, T))
    b.append(f'<path class="ar" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="M880 98 C890 112 870 122 846 124 M856 114 L844 124 L858 130" fill="none" stroke="{GREY}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    return wrap_svg(k, W, H, b)

if __name__ == "__main__":
    stats, langs, streak, leet = s0.load()
    out = {"an-nums.svg": piece_nums(stats, streak), "an-lang.svg": piece_lang(langs), "an-streak.svg": piece_streak(streak),
           "an-leet.svg": piece_leet(leet), "an-snake-head.svg": piece_snake_head()}
    for nm, sv in out.items():
        (D / nm).write_text(sv, encoding="utf-8"); print("wrote", nm, len(sv) // 1024 or 1, "KB")
