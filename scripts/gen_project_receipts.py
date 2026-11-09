#!/usr/bin/env python3
"""Projects section v2: receipts that print line by line (light on the renderer: no big moving layer),
rolling metric numbers, drawn ticks, stamp + confetti, doodles; plus link stickers.
Outputs: rcpt-novamart.svg, rcpt-cronvault.svg, lk-*.svg, hd-projects.svg. Run from repo root."""
import sys, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cover_notes as c
import gen_about_notes as a

D, INK, PAPER = c.D, c.INK, c.PAPER
YEL, LIME, PINK, BLUE, ORG, LAV = c.YEL, c.LIME, c.PINK, c.BLUE, c.ORG, c.LAV
T = 18.0
P = lambda s: round(s / T * 100, 2)

def wrap(text, n):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + (1 if cur else 0) <= n: cur = (cur + " " + w).strip()
        else: out.append(cur); cur = w
    return out + [cur] if cur else out

def esc(s): return s.replace("&", "&amp;")

class Doc:
    def __init__(self): self.css, self.n = "", 0
    def block(self, inner, S, dy=-8):
        self.n += 1; k = self.n
        self.css += (f"@keyframes b{k}{{0%,{P(S)}%{{opacity:0;transform:translateY({dy}px)}}{P(S+.35)}%,93%{{opacity:1;transform:none}}96.5%,100%{{opacity:0;transform:translateY({dy}px)}}}}"
                     f".b{k}{{animation:b{k} {T}s ease-out infinite}}")
        return f'<g class="b{k}">{inner}</g>'
    def tick(self, d, S, stroke, w=3):
        self.n += 1; k = self.n
        self.css += c.draw_kf(f"t{k}", S, .35, True, T)
        return f'<path class="t{k}" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    def odo(self, text, xr, y, size, S, fill, adv):
        """right-aligned value; digits roll like an odometer, other chars static"""
        Lh = size * 1.22
        x = xr - len(text) * adv
        out = []
        for ch in text:
            if ch.isdigit():
                self.n += 1; k = self.n; d = int(ch); tgt = d if d else 10
                self.css += (f"@keyframes o{k}{{0%,{P(S)}%{{transform:translateY(0)}}{P(S+1.3)}%,93%{{transform:translateY({-Lh*tgt:.0f}px)}}93.1%,100%{{transform:translateY(0)}}}}"
                             f".o{k}{{animation:o{k} {T}s cubic-bezier(.2,.8,.2,1) infinite}}")
                digs = "".join(f'<text class="m" x="{x+adv/2:.1f}" y="{y+Lh*j:.0f}" text-anchor="middle" font-size="{size}" font-weight="900" fill="{fill}">{j % 10}</text>' for j in range(11))
                out.append(f'<clipPath id="oc{k}"><rect x="{x-1:.1f}" y="{y-size*.85:.0f}" width="{adv+2:.1f}" height="{size*1.05:.0f}"/></clipPath>'
                           f'<g clip-path="url(#oc{k})"><g class="o{k}">{digs}</g></g>')
            else:
                out.append(f'<text class="m" x="{x+adv/2:.1f}" y="{y}" text-anchor="middle" font-size="{size}" font-weight="900" fill="{fill}">{ch}</text>')
            x += adv
        return "".join(out)

def receipt(name, sub, item, metrics, feats, total, stack, accent, bye, note_l, note_r, tilt, doodle):
    W = 490; RX, RW = 66, 358
    L, R, CX = RX + 22, RX + RW - 22, RX + RW / 2
    d = Doc(); body, y = [], 70
    body.append(d.block(f'<text class="m" x="{CX}" y="{y}" text-anchor="middle" font-size="31" font-weight="900" letter-spacing="2" fill="{INK}">{name}</text>', .3)); y += 24
    s = ""
    for ln in wrap(sub, 44):
        s += f'<text class="m" x="{CX}" y="{y}" text-anchor="middle" font-size="11.5" fill="{INK}" fill-opacity=".75">{esc(ln)}</text>'; y += 17
    body.append(d.block(s, .5)); y += 6
    sep = lambda yy: f'<line x1="{L}" y1="{yy}" x2="{R}" y2="{yy}" stroke="{INK}" stroke-opacity=".5" stroke-width="1.8" stroke-dasharray="5 5"/>'
    body.append(d.block(f'<text class="m" x="{CX}" y="{y}" text-anchor="middle" font-size="10.5" letter-spacing="2.5" fill="{INK}" fill-opacity=".55">{item}</text>' + sep(y + 14), .7)); y += 42
    for i, (lab, val) in enumerate(metrics):
        S = 1.0 + i * .35
        lw, vw = len(lab) * 7.8, len(val) * 11
        row = (f'<text class="m" x="{L}" y="{y}" font-size="13" font-weight="700" fill="{INK}">{lab}</text>'
               f'<line x1="{L+lw+8:.0f}" y1="{y-4}" x2="{R-vw-8:.0f}" y2="{y-4}" stroke="{INK}" stroke-opacity=".45" stroke-width="2" stroke-dasharray="1 5" stroke-linecap="round"/>')
        body.append(d.block(row, S) + d.odo(val, R, y + 1, 18, S + .2, INK, 11)); y += 26
    y -= 6; body.append(d.block(sep(y), 1.9)); y += 24
    for i, f in enumerate(feats):
        S = 2.3 + i * .55
        lines = wrap(f, 36); g = ""
        for k, ln in enumerate(lines):
            g += f'<text class="m" x="{L+22}" y="{y+k*17}" font-size="12" fill="{INK}">{esc(ln)}</text>'
        body.append(d.block(g, S) + d.tick(f"M{L+1} {y-4} L{L+7} {y+2} L{L+17} {y-11}", S + .25, "#16a34a", 3.2))
        y += 17 * len(lines) + 8
    y -= 2; body.append(d.block(sep(y), 4.6)); y += 30
    tl, tv = total
    tot = (f'<text class="m" x="{L}" y="{y}" font-size="12.5" font-weight="900" letter-spacing="1" fill="{INK}">{tl}</text>'
           f'<text class="m" x="{R}" y="{y+2}" text-anchor="end" font-size="26" font-weight="900" fill="{INK}">{tv}</text>')
    body.append(d.block(tot, 4.9) + d.tick(f"M{R-34} {y+10} Q{R-18} {y+6} {R+2} {y+10}", 5.3, accent, 3.5) + d.tick(f"M{R-30} {y+16} Q{R-16} {y+13} {R-2} {y+16}", 5.5, accent, 2.5))
    y += 28; body.append(d.block(sep(y), 5.2)); y += 22
    st = f'<text class="m" x="{L}" y="{y}" font-size="11" font-weight="800" letter-spacing="2" fill="{INK}" fill-opacity=".55">STACK</text>'; y += 18
    for ln in wrap(" · ".join(stack), 42):
        st += f'<text class="m" x="{L}" y="{y}" font-size="12" fill="{INK}">{ln}</text>'; y += 17
    body.append(d.block(st, 5.5)); y += 6; body.append(d.block(sep(y), 5.8)); y += 20
    bx, by, seed, bars, x, i = 108, y, sum(map(ord, name)), [], 108, 0
    while x < 382:
        w = 1 + ((seed * (i + 3) + i * 7) % 4); g = 2 + ((seed + i * 5) % 3)
        if x + w > 382: break
        bars.append(f'<rect x="{x}" y="{by}" width="{w}" height="46" fill="{INK}"/>'); x += w + g; i += 1
    d.css += "@keyframes scn{0%,100%{transform:translateX(0)}50%{transform:translateX(272px)}}.scn{animation:scn 2.6s ease-in-out infinite}"
    body.append(d.block("".join(bars) + f'<rect class="scn" x="{bx}" y="{by-5}" width="2.5" height="56" fill="#ff3b30"/>', 6.0))
    y = by + 66
    body.append(d.block(f'<text class="m" x="{CX}" y="{y}" text-anchor="middle" font-size="10.5" letter-spacing="2.5" fill="{INK}" fill-opacity=".6">{bye}</text>', 6.3))
    ybot = y + 26; H = ybot + 44
    sheet = a.torn(RX, 30, RX + RW, ybot, amp=5, step=11)
    # stamp + confetti
    sx, sy = RX + RW - 84, by + 24
    d.css += c.slam_kf("stm", 6.8, True, T)
    stamp = (f'<g transform="rotate(-13 {sx} {sy})"><g class="stm"><rect x="{sx-58}" y="{sy-24}" width="116" height="48" rx="8" fill="none" stroke="#1fa65a" stroke-width="4.5" stroke-opacity=".92"/>'
             f'<text class="m" x="{sx}" y="{sy+10}" text-anchor="middle" font-size="29" font-weight="900" letter-spacing="5" fill="#1fa65a" fill-opacity=".92">LIVE</text></g></g>')
    rnd = random.Random(sum(map(ord, name)))
    conf = ""
    for q in range(14):
        k = 100 + q; dx, dy, rot = rnd.randint(-120, 120), rnd.randint(-150, -30), rnd.randint(-540, 540)
        col = rnd.choice([accent, YEL, PINK, LIME, LAV])
        S = 7.0 + rnd.random() * .3
        d.css += (f"@keyframes cf{k}{{0%,{P(S)}%{{opacity:0;transform:translate(0,0) rotate(0)}}{P(S+.05)}%{{opacity:1}}{P(S+1.4)}%{{opacity:0;transform:translate({dx}px,{dy+170}px) rotate({rot}deg)}}100%{{opacity:0}}}}"
                  f".cf{k}{{animation:cf{k} {T}s cubic-bezier(.2,.7,.4,1) infinite}}")
        conf += f'<g transform="translate({sx} {sy})"><rect class="cf{k}" x="-3" y="-4" width="6" height="9" fill="{col}" stroke="{INK}" stroke-width="1"/></g>'
    # notes + doodles in the margins
    ymid = (30 + ybot) / 2
    d.css += c.draw_kf("dd", 7.4, .8, True, T)
    d.css += f"@keyframes nt{{0%,{P(7.4)}%{{opacity:0}}{P(8.2)}%,93%{{opacity:1}}96.5%,100%{{opacity:0}}}}.nt{{animation:nt {T}s linear infinite}}"
    d.css += "@keyframes hnd{to{transform:rotate(360deg)}}.hnd{transform-box:fill-box;transform-origin:50% 100%;animation:hnd 5s linear infinite}"
    notes = (f'<g class="nt"><text x="30" y="{ymid:.0f}" text-anchor="middle" font-size="15" font-style="italic" font-weight="600" fill="{accent}" transform="rotate(-90 30 {ymid:.0f})">{note_l}</text>'
             f'<text x="462" y="{ymid:.0f}" text-anchor="middle" font-size="15" font-style="italic" font-weight="600" fill="{accent}" transform="rotate(90 462 {ymid:.0f})">{note_r}</text></g>')
    if doodle == "cart":
        dd = (f'<path class="dd" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="M8 110 h9 l6 26 h28 l5 -20 h-36" fill="none" stroke="{accent}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
              f'<circle class="nt" cx="28" cy="146" r="4" fill="{accent}"/><circle class="nt" cx="46" cy="146" r="4" fill="{accent}"/>')
    else:
        dd = (f'<g class="nt"><circle cx="34" cy="126" r="22" fill="none" stroke="{accent}" stroke-width="3.5"/>'
              f'<path d="M34 108 v4 M34 140 v4 M16 126 h4 M48 126 h4" stroke="{accent}" stroke-width="3" stroke-linecap="round"/>'
              f'<line class="hnd" x1="34" y1="126" x2="34" y2="111" stroke="{accent}" stroke-width="3.5" stroke-linecap="round"/></g>')
    spark = (f'<g class="nt"><path d="M452 112 l4 12 l12 4 l-12 4 l-4 12 l-4 -12 l-12 -4 l12 -4 z" fill="{accent}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/></g>')
    ymid_i = (30 + ybot) / 2
    out = (f'<g transform="rotate({tilt} {W/2} {ymid_i})">'
           f'<path d="{sheet}" transform="translate(8 8)" fill="{accent}"/>'
           f'<path d="{sheet}" fill="{PAPER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
           + "".join(body) + stamp + '</g>'
           f'<rect x="{RX-14}" y="8" width="{RW+28}" height="26" rx="13" fill="{INK}"/><rect x="{RX-4}" y="18" width="{RW+8}" height="8" rx="4" fill="#000"/>'
           + conf + notes + dd + spark)
    return c.svg(W, H, "text{text-rendering:optimizeSpeed}" + d.css, out)

NOVA = dict(name="NOVAMART", sub="Distributed e-commerce platform · React + Spring Boot", item="ITEM #01 · FEATURED PROJECT",
            metrics=[("ERROR RATE", "0%"), ("AVG LATENCY", "182ms"), ("P95 LATENCY", "326ms")],
            feats=["5,250+ concurrent requests, verified with JMeter", "JWT rotation + Google OAuth2 + Redis OTP store",
                   "Cashfree webhook signature checks, no double-charge", "Reservation-based inventory locking, no overselling"],
            total=("TOTAL DOUBLE-CHARGES", "0"),
            stack=["Java 17", "Spring Boot 3", "Spring Security", "PostgreSQL", "Redis", "Cashfree", "Cloudinary", "Docker", "React"],
            accent=BLUE, bye="THANK YOU · COME AGAIN", note_l="0% errors, no cap", note_r="no double-charge btw", tilt=-1.6, doodle="cart")
CRON = dict(name="CRONVAULT", sub="Multi-tenant distributed job scheduler", item="ITEM #02 · FEATURED PROJECT",
            metrics=[("EXACTLY-ONCE RUNS", "1x"), ("RBAC PERMISSIONS", "9"), ("CRASH RECOVERY", "60s")],
            feats=["Exactly-once execution via DB pessimistic locking", "Custom RBAC across tenants, with full audit log",
                   "Lua sliding-window rate limiter, fails open to DB", "Per-tenant circuit breakers using Resilience4j"],
            total=("TOTAL DUPLICATE RUNS", "0"),
            stack=["Java 21", "Spring Boot 3", "Spring Security", "MySQL", "Redis + Lua", "Resilience4j"],
            accent=ORG, bye="SEE YOU AT THE NEXT RUN", note_l="runs exactly once", note_r="crash? back in 60s", tilt=1.6, doodle="clock")

# ------------------------------------------------------------ link stickers
def link(proj, text, color, kind, tilt, delay):
    W, H = 300, 68
    css = c.slam_kf("s", delay) + "@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}.bl{animation:bl 1s steps(1) infinite}"
    dash = ' stroke-dasharray="7 5"' if kind == "private" else ""
    if kind == "live":
        icon = f'<circle class="bl" cx="40" cy="34" r="7" fill="#1fa65a" stroke="{INK}" stroke-width="2.5"/>'
    elif kind == "src":
        icon = f'<text class="m" x="40" y="40" text-anchor="middle" font-size="17" font-weight="900" fill="{INK}">&lt;/&gt;</text>'
    else:
        icon = (f'<rect x="31" y="32" width="18" height="14" rx="3" fill="{INK}"/><path d="M35 32 v-5 a5 5 0 0 1 10 0 v5" fill="none" stroke="{INK}" stroke-width="3"/>')
    b = (f'<g transform="rotate({tilt} 150 34)"><g class="s">'
         f'<rect x="12" y="12" width="270" height="48" rx="12" fill="{INK}"/>'
         f'<rect x="8" y="8" width="270" height="48" rx="12" fill="{color}" stroke="{INK}" stroke-width="3"{dash}/>'
         + icon +
         f'<text class="m" x="64" y="26" font-size="10" font-weight="700" letter-spacing="2.5" fill="{INK}" fill-opacity=".7">{proj}</text>'
         f'<text x="64" y="46" font-size="18" font-weight="900" fill="{INK}">{text}</text></g></g>')
    return c.svg(W, H, css, b)

if __name__ == "__main__":
    for old in list(D.glob("proj-*.svg")): old.unlink()
    out = {"rcpt-novamart.svg": receipt(**NOVA), "rcpt-cronvault.svg": receipt(**CRON),
           "lk-nova-live.svg": link("NOVAMART", "live project →", BLUE, "live", -1.5, .2),
           "lk-nova-src.svg": link("NOVAMART", "source code →", LIME, "src", 1.2, .4),
           "lk-cron-live.svg": link("CRONVAULT", "live project →", ORG, "live", 1.4, .6),
           "lk-cron-private.svg": link("CRONVAULT", "source: private", LAV, "private", -1.2, .8),
           "hd-projects.svg": a.heading("03", "featured projects", BLUE, LIME, "// built and shipped")}
    for n, s in out.items():
        (D / n).write_text(s, encoding="utf-8"); print("wrote", n, len(s), "B")
