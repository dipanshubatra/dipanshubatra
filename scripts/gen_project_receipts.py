#!/usr/bin/env python3
"""Projects section: each project is a thermal receipt that prints out of a slot (proj-novamart.svg, proj-cronvault.svg)
+ hd-projects.svg heading. Run from repo root: python3 scripts/gen_project_receipts.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cover_notes as c
import gen_about_notes as a

D, INK = c.D, c.INK
CW = 7.2  # mono advance at 12px

def wrap(text, n):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + (1 if cur else 0) <= n: cur = (cur + " " + w).strip()
        else: out.append(cur); cur = w
    return out + [cur] if cur else out

def esc(s): return s.replace("&", "&amp;")

def receipt(name, sub, item, metrics, feats, stack, accent, stamp_col, bye, note_l, note_r, tilt):
    W, T = 490, 14.0
    RX, RW = 66, 358
    L, R, CX = RX + 22, RX + RW - 22, RX + RW / 2
    p = lambda s: round(s / T * 100, 2)
    b, y = [], 70
    b.append(f'<text class="m" x="{CX}" y="{y}" text-anchor="middle" font-size="31" font-weight="900" letter-spacing="2" fill="{INK}">{name}</text>'); y += 24
    for ln in wrap(sub, 44):
        b.append(f'<text class="m" x="{CX}" y="{y}" text-anchor="middle" font-size="11.5" fill="{INK}" fill-opacity=".75">{esc(ln)}</text>'); y += 17
    y += 6
    b.append(f'<text class="m" x="{CX}" y="{y}" text-anchor="middle" font-size="10.5" letter-spacing="2.5" fill="{INK}" fill-opacity=".55">{item}</text>'); y += 14
    sep = lambda yy: f'<line x1="{L}" y1="{yy}" x2="{R}" y2="{yy}" stroke="{INK}" stroke-opacity=".5" stroke-width="1.8" stroke-dasharray="5 5"/>'
    b.append(sep(y)); y += 28
    for lab, val in metrics:
        lw, vw = len(lab) * 7.8, len(val) * 10.8
        b.append(f'<text class="m" x="{L}" y="{y}" font-size="13" font-weight="700" fill="{INK}">{lab}</text>')
        b.append(f'<line x1="{L+lw+8:.0f}" y1="{y-4}" x2="{R-vw-8:.0f}" y2="{y-4}" stroke="{INK}" stroke-opacity=".45" stroke-width="2" stroke-dasharray="1 5" stroke-linecap="round"/>')
        b.append(f'<text class="m" x="{R}" y="{y+1}" text-anchor="end" font-size="18" font-weight="900" fill="{INK}">{val}</text>'); y += 26
    y -= 6; b.append(sep(y)); y += 24
    for f in feats:
        for k, ln in enumerate(wrap(f, 38)):
            pre = "1x " if k == 0 else "   "
            b.append(f'<text class="m" x="{L}" y="{y}" font-size="12" fill="{INK}"><tspan font-weight="800" fill-opacity=".55">{pre}</tspan>{esc(ln)}</text>'); y += 17
        y += 7
    y -= 2; b.append(sep(y)); y += 22
    b.append(f'<text class="m" x="{L}" y="{y}" font-size="11" font-weight="800" letter-spacing="2" fill="{INK}" fill-opacity=".55">STACK</text>'); y += 18
    for ln in wrap(" · ".join(stack), 42):
        b.append(f'<text class="m" x="{L}" y="{y}" font-size="12" fill="{INK}">{ln}</text>'); y += 17
    y += 6; b.append(sep(y)); y += 20
    # barcode
    bx, by, seed, bars = 108, y, sum(map(ord, name)), []
    x, i = bx, 0
    while x < 382:
        w = 1 + ((seed * (i + 3) + i * 7) % 4); g = 2 + ((seed + i * 5) % 3)
        if x + w > 382: break
        bars.append(f'<rect x="{x}" y="{by}" width="{w}" height="46" fill="{INK}"/>'); x += w + g; i += 1
    b.append("".join(bars))
    b.append(f'<rect class="scn" x="{bx}" y="{by-5}" width="2.5" height="56" fill="#ff3b30"/>')
    y = by + 46 + 20
    b.append(f'<text class="m" x="{CX}" y="{y}" text-anchor="middle" font-size="10.5" letter-spacing="2.5" fill="{INK}" fill-opacity=".6">{bye}</text>')
    ybot = y + 26
    stamp_y = by + 24
    H = ybot + 42
    Hr = ybot - 30 + 12
    sheet = a.torn(RX, 30, RX + RW, ybot, amp=5, step=11)
    css = (f"@keyframes pr{{0%,{p(.4)}%{{transform:translateY({-Hr}px)}}{p(3.6)}%,92%{{transform:translateY(0)}}96%,100%{{transform:translateY({-Hr}px)}}}}"
           f".pr{{animation:pr {T}s steps(44) infinite}}"
           "@keyframes scn{0%,100%{transform:translateX(0)}50%{transform:translateX(272px)}}.scn{animation:scn 2.6s ease-in-out infinite}"
           + c.slam_kf("stm", 3.9, True, T)
           + f"@keyframes nt{{0%,{p(4.4)}%{{opacity:0}}{p(5.0)}%,92%{{opacity:1}}96%,100%{{opacity:0}}}}.nt{{animation:nt {T}s linear infinite}}")
    ymid = (30 + ybot) / 2
    body = [f'<g transform="rotate({tilt} {W/2} {ymid})">',
            f'<clipPath id="pc"><rect x="0" y="34" width="{W}" height="{H}"/></clipPath>',
            '<g clip-path="url(#pc)"><g class="pr">',
            f'<path d="{sheet}" transform="translate(8 8)" fill="{accent}"/>',
            f'<path d="{sheet}" fill="{c.PAPER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>',
            "".join(b), '</g></g>',
            f'<rect x="{RX-14}" y="8" width="{RW+28}" height="26" rx="13" fill="{INK}"/>'
            f'<rect x="{RX-4}" y="18" width="{RW+8}" height="8" rx="4" fill="#000"/>',
            f'<g transform="rotate(-13 {RX+RW-84} {stamp_y})"><g class="stm"><rect x="{RX+RW-142}" y="{stamp_y-24}" width="116" height="48" rx="8" fill="none" stroke="{stamp_col}" stroke-width="4.5" stroke-opacity=".92"/>'
            f'<text class="m" x="{RX+RW-84}" y="{stamp_y+10}" text-anchor="middle" font-size="29" font-weight="900" letter-spacing="5" fill="{stamp_col}" fill-opacity=".92">LIVE</text></g></g>',
            '</g>',
            f'<g class="nt"><text x="30" y="{ymid:.0f}" text-anchor="middle" font-size="15" font-style="italic" font-weight="600" fill="{accent}" transform="rotate(-90 30 {ymid:.0f})">{note_l}</text>'
            f'<text x="462" y="{ymid:.0f}" text-anchor="middle" font-size="15" font-style="italic" font-weight="600" fill="{accent}" transform="rotate(90 462 {ymid:.0f})">{note_r}</text></g>']
    return c.svg(W, H, css, "".join(body))

NOVA = dict(name="NOVAMART", sub="Distributed e-commerce platform · React + Spring Boot", item="ITEM #01 · FEATURED PROJECT",
            metrics=[("ERROR RATE", "0%"), ("AVG LATENCY", "182ms"), ("P95 LATENCY", "326ms")],
            feats=["5,250+ concurrent requests, verified with JMeter", "JWT rotation + Google OAuth2 + Redis OTP store",
                   "Cashfree webhook signature checks, no double-charge", "Reservation-based inventory locking, no overselling"],
            stack=["Java 17", "Spring Boot 3", "Spring Security", "PostgreSQL", "Redis", "Cashfree", "Cloudinary", "Docker", "React"],
            accent=c.BLUE, stamp_col="#1fa65a", bye="THANK YOU · COME AGAIN", note_l="0% errors, no cap", note_r="no double-charge btw", tilt=-1.6)
CRON = dict(name="CRONVAULT", sub="Multi-tenant distributed job scheduler", item="ITEM #02 · FEATURED PROJECT",
            metrics=[("EXACTLY-ONCE RUNS", "1x"), ("RBAC PERMISSIONS", "9"), ("CRASH RECOVERY", "60s")],
            feats=["Exactly-once execution via DB pessimistic locking", "Custom RBAC across tenants, with full audit log",
                   "Lua sliding-window rate limiter, fails open to DB", "Per-tenant circuit breakers using Resilience4j"],
            stack=["Java 21", "Spring Boot 3", "Spring Security", "MySQL", "Redis + Lua", "Resilience4j"],
            accent=c.ORG, stamp_col="#1fa65a", bye="SEE YOU AT THE NEXT RUN", note_l="runs exactly once", note_r="crash? back in 60s", tilt=1.6)

if __name__ == "__main__":
    out = {"proj-novamart.svg": receipt(**NOVA), "proj-cronvault.svg": receipt(**CRON),
           "hd-projects.svg": a.heading("03", "featured projects", c.BLUE, c.LIME, "// built and shipped")}
    for n, s in out.items():
        (D / n).write_text(s, encoding="utf-8"); print("wrote", n, len(s), "B")
