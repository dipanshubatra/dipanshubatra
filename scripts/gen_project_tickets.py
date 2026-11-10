#!/usr/bin/env python3
"""Projects v3: wide full-width tickets (big readable text), body + perforated stub, rolling metrics, ticks, barcode scanner,
LIVE stamp + confetti. Outputs tix-novamart.svg, tix-cronvault.svg. Run from repo root: python3 scripts/gen_project_tickets.py"""
import sys, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cover_notes as c
import gen_project_receipts as r

D, INK, PAPER = c.D, c.INK, c.PAPER
YEL, LIME, PINK, BLUE, ORG, LAV = c.YEL, c.LIME, c.PINK, c.BLUE, c.ORG, c.LAV
T, P = r.T, r.P
Doc, wrap, esc = r.Doc, r.wrap, r.esc

def ticket(name, sub, item, metrics, feats, total, stack, accent, bye, tilt, icon):
    W, H = 1000, 450
    X0, X1, Y0, Y1, NX = 20, 980, 14, 418, 722
    d = Doc(); body = []
    L = 56
    body.append(d.block(f'<text class="m" x="{L}" y="52" font-size="14" font-weight="700" letter-spacing="3" fill="{INK}" fill-opacity=".55">{item}</text>', .3))
    tl = len(name) * 36
    d.n += 1
    k = d.n
    d.css += c.draw_kf(f"mk{k}", .5, .7, True, T)
    body.append(f'<line class="mk{k}" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" x1="{L-6}" y1="92" x2="{L+tl+10}" y2="89" stroke="{accent}" stroke-width="58" stroke-opacity=".95"/>')
    body.append(d.block(f'<text x="{L}" y="108" font-size="58" font-weight="900" letter-spacing="-1" fill="{INK}" textLength="{tl}" lengthAdjust="spacingAndGlyphs">{name}</text>', .5))
    body.append(d.block(f'<text x="{L}" y="142" font-size="20" font-weight="600" fill="{INK}" fill-opacity=".8">{esc(sub)}</text>', .9))
    sep = lambda y, x2=NX - 24: f'<line x1="{L}" y1="{y}" x2="{x2}" y2="{y}" stroke="{INK}" stroke-opacity=".45" stroke-width="2" stroke-dasharray="6 6"/>'
    body.append(d.block(sep(162), 1.1))
    for i, (lab, val) in enumerate(metrics):
        x = L + i * 214
        S = 1.3 + i * .35
        vw = len(val) * 29
        body.append(d.odo(val, x + vw, 222, 48, S, INK, 29))
        body.append(d.block(f'<text class="m" x="{x}" y="246" font-size="13" font-weight="700" letter-spacing="1.5" fill="{INK}" fill-opacity=".6">{lab}</text>', S))
    body.append(d.block(sep(266), 2.3))
    y = 300
    for i, f in enumerate(feats):
        S = 2.6 + i * .5
        body.append(d.block(f'<text x="{L+34}" y="{y}" font-size="19" font-weight="500" fill="{INK}">{esc(f)}</text>', S) + d.tick(f"M{L+2} {y-5} L{L+10} {y+3} L{L+23} {y-14}", S + .2, "#16a34a", 4))
        y += 34
    # stub
    SX = NX + 24
    SW = X1 - SX - 22
    smid = SX + SW / 2
    stub = []
    tl_, tv = total
    stub.append(d.block(f'<text class="m" x="{smid}" y="128" text-anchor="middle" font-size="13" font-weight="800" letter-spacing="1" fill="{INK}" fill-opacity=".7">{tl_}</text>', 4.4))
    stub.append(d.odo(tv, smid + len(tv) * 27, 206, 92, 4.6, INK, 54))
    d.css += c.draw_kf(f"ul{d.n}", 5.6, .5, True, T)
    stub.append(f'<path class="ul{d.n}" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" d="M{smid-52} 226 Q{smid} 218 {smid+54} 226" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round"/>')
    stack_txt = f'<text class="m" x="{SX}" y="262" font-size="12.5" font-weight="800" letter-spacing="2" fill="{INK}" fill-opacity=".55">STACK</text>'
    row_y = 282
    for ln in wrap(" · ".join(stack), 28):
        stack_txt += f'<text class="m" x="{SX}" y="{row_y}" font-size="12" fill="{INK}">{esc(ln)}</text>'
        row_y += 17
    stub.append(d.block(stack_txt, 5.0))
    bx, by, seed, bars = SX + 6, 352, sum(map(ord, name)), []
    x, i = SX + 6, 0
    while x < SX + SW - 6:
        w = 1 + ((seed * (i + 3) + i * 7) % 4)
        g = 2 + ((seed + i * 5) % 3)
        if x + w > SX + SW - 6:
            break
        bars.append(f'<rect x="{x}" y="{by}" width="{w}" height="40" fill="{INK}"/>')
        x += w + g
        i += 1
    d.css += f"@keyframes scan{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX({SW-14:.0f}px)}}}}.scan{{animation:scan 2.6s ease-in-out infinite}}"
    stub.append(d.block("".join(bars) + f'<rect class="scan" x="{bx}" y="{by-5}" width="2.5" height="50" fill="#ff3b30"/>', 5.8))
    stub.append(d.block(f'<text class="m" x="{smid}" y="{by+58}" text-anchor="middle" font-size="10.5" letter-spacing="2" fill="{INK}" fill-opacity=".6">{bye}</text>', 6.2))
    if icon == "cart":
        art = (f'<path d="M{SX} 62 h12 l8 34 h38 l7 -26 h-50" fill="none" stroke="{accent}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
               f'<circle cx="{SX+26}" cy="108" r="5.5" fill="{accent}"/><circle cx="{SX+52}" cy="108" r="5.5" fill="{accent}"/>')
    else:
        d.css += "@keyframes hnd{to{transform:rotate(360deg)}}.hnd{transform-box:fill-box;transform-origin:50% 100%;animation:hnd 5s linear infinite}"
        art = (f'<circle cx="{SX+34}" cy="84" r="28" fill="none" stroke="{accent}" stroke-width="5"/>'
               f'<path d="M{SX+34} 60 v6 M{SX+34} 102 v6 M{SX+10} 84 h6 M{SX+52} 84 h6" stroke="{accent}" stroke-width="4" stroke-linecap="round"/>'
               f'<line class="hnd" x1="{SX+34}" y1="84" x2="{SX+34}" y2="64" stroke="{accent}" stroke-width="5" stroke-linecap="round"/>')
    stub.append(d.block(art, 4.0))
    stx, sty = 640, 98
    d.css += c.slam_kf("stm", 6.8, True, T)
    stamp = (f'<g transform="rotate(-12 {stx} {sty})"><g class="stm"><rect x="{stx-58}" y="{sty-26}" width="116" height="52" rx="9" fill="none" stroke="#1fa65a" stroke-width="5" stroke-opacity=".92"/>'
             f'<text class="m" x="{stx}" y="{sty+11}" text-anchor="middle" font-size="31" font-weight="900" letter-spacing="5" fill="#1fa65a" fill-opacity=".92">LIVE</text></g></g>')
    rnd = random.Random(sum(map(ord, name)))
    conf = ""
    for q in range(16):
        kk = 100 + q
        mx_, my_, rt = rnd.randint(-190, 70), rnd.randint(-120, -30), rnd.randint(-540, 540)
        col = rnd.choice([accent, YEL, PINK, LIME, LAV])
        S = 7.0 + rnd.random() * .3
        d.css += (f"@keyframes cf{kk}{{0%,{P(S)}%{{opacity:0;transform:translate(0,0) rotate(0)}}{P(S+.05)}%{{opacity:1}}{P(S+1.4)}%{{opacity:0;transform:translate({mx_}px,{my_+190}px) rotate({rt}deg)}}100%{{opacity:0}}}}"
                  f".cf{kk}{{animation:cf{kk} {T}s cubic-bezier(.2,.7,.4,1) infinite}}")
        conf += f'<g transform="translate({stx} {sty})"><rect class="cf{kk}" x="-4" y="-5" width="8" height="11" fill="{col}" stroke="{INK}" stroke-width="1.2"/></g>'
    shape = (f"M{X0+16} {Y0} H{NX-14} A14 14 0 0 0 {NX+14} {Y0} H{X1-16} Q{X1} {Y0} {X1} {Y0+16} V{Y1-16} Q{X1} {Y1} {X1-16} {Y1} "
             f"H{NX+14} A14 14 0 0 0 {NX-14} {Y1} H{X0+16} Q{X0} {Y1} {X0} {Y1-16} V{Y0+16} Q{X0} {Y0} {X0+16} {Y0} Z")
    out = (f'<g transform="rotate({tilt} {W/2} {H/2})">'
           f'<path d="{shape}" transform="translate(9 9)" fill="{accent}"/>'
           f'<path d="{shape}" fill="{PAPER}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
           f'<line x1="{NX}" y1="{Y0+22}" x2="{NX}" y2="{Y1-22}" stroke="{INK}" stroke-opacity=".5" stroke-width="2.5" stroke-dasharray="3 8" stroke-linecap="round"/>'
           + "".join(body) + "".join(stub) + stamp + conf + '</g>')
    return c.svg(W, H, "text{text-rendering:optimizeSpeed}" + d.css, out)

NOVA = dict(name="NOVAMART", sub="Distributed e-commerce platform · React + Spring Boot", item="ITEM #01 · FEATURED PROJECT",
            metrics=[("ERROR RATE", "0%"), ("AVG LATENCY", "182ms"), ("P95 LATENCY", "326ms")],
            feats=["5,250+ concurrent requests, verified with JMeter", "JWT rotation + Google OAuth2 + Redis OTP store",
                   "Cashfree webhook signature checks, no double-charge", "Reservation-based inventory locking, no overselling"],
            total=("TOTAL DOUBLE-CHARGES", "0"),
            stack=["Java 17", "Spring Boot 3", "Spring Security", "PostgreSQL", "Redis", "Cashfree", "Cloudinary", "Docker", "React"],
            accent=BLUE, bye="THANK YOU · COME AGAIN", tilt=-0.7, icon="cart")
CRON = dict(name="CRONVAULT", sub="Multi-tenant distributed job scheduler", item="ITEM #02 · FEATURED PROJECT",
            metrics=[("EXACTLY-ONCE RUNS", "1x"), ("RBAC PERMISSIONS", "9"), ("CRASH RECOVERY", "60s")],
            feats=["Exactly-once execution via DB pessimistic locking", "Custom RBAC across tenants, with full audit log",
                   "Lua sliding-window rate limiter, fails open to DB", "Per-tenant circuit breakers using Resilience4j"],
            total=("TOTAL DUPLICATE RUNS", "0"),
            stack=["Java 21", "Spring Boot 3", "Spring Security", "MySQL", "Redis + Lua", "Resilience4j"],
            accent=ORG, bye="SEE YOU AT THE NEXT RUN", tilt=0.7, icon="clock")

if __name__ == "__main__":
    for fn, spec in (("tix-novamart.svg", NOVA), ("tix-cronvault.svg", CRON)):
        out_svg = ticket(**spec)
        (D / fn).write_text(out_svg, encoding="utf-8")
        print("wrote", fn, len(out_svg) // 1024, "KB")
