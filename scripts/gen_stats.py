#!/usr/bin/env python3
"""Generate assets/stats.svg (GitHub stats + top languages) from the GitHub API. Run by the Action."""
import collections, json, os, pathlib, urllib.request
from html import escape

USER = "dipanshubatra"
TOK = os.environ.get("GITHUB_TOKEN", "")
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "stats.svg"


def api(path, default=None):
    try:
        req = urllib.request.Request("https://api.github.com" + path, headers={
            "Authorization": f"Bearer {TOK}", "Accept": "application/vnd.github+json", "User-Agent": "stats-card"})
        return json.load(urllib.request.urlopen(req, timeout=30))
    except Exception as e:
        print("api fail", path, e)
        return default


user = api(f"/users/{USER}", {})
repos = api(f"/users/{USER}/repos?per_page=100&type=owner", []) or []
commits = (api(f"/search/commits?q=author:{USER}&per_page=1", {}) or {}).get("total_count", 0)
prs = (api(f"/search/issues?q=author:{USER}+type:pr&per_page=1", {}) or {}).get("total_count", 0)
stars = sum(r.get("stargazers_count", 0) for r in repos)
langs = collections.Counter(r["language"] for r in repos if r.get("language") and not r.get("fork"))
top = langs.most_common(5)
total = sum(c for _, c in top) or 1

rows = [("Public repos", user.get("public_repos", len(repos))), ("Total stars", stars),
        ("Commits (all time)", commits), ("Pull requests", prs), ("Followers", user.get("followers", 0))]
COLORS = ["#70a5fd", "#bb9af7", "#38bdae", "#f7768e", "#e0af68"]

left = "".join(
    f'<text x="30" y="{88 + i * 28}" class="k">{escape(k)}</text>'
    f'<text x="300" y="{88 + i * 28}" class="v" text-anchor="end">{v}</text>' for i, (k, v) in enumerate(rows))
right = ""
for i, (name, cnt) in enumerate(top):
    pct = cnt / total * 100
    y = 76 + i * 32
    right += (f'<text x="470" y="{y}" class="k">{escape(name)}</text>'
              f'<text x="800" y="{y}" class="v" text-anchor="end">{pct:.0f}%</text>'
              f'<rect x="470" y="{y + 8}" width="330" height="8" rx="4" fill="#2a2e45"/>'
              f'<rect class="bar" style="animation-delay:{i * .15}s" x="470" y="{y + 8}" width="{330 * pct / 100:.0f}" height="8" rx="4" fill="{COLORS[i]}"/>')
if not top:
    right = '<text x="470" y="90" class="k">No language data yet</text>'

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="830" height="250" viewBox="0 0 830 250">
  <style>
    text{{font-family:'Segoe UI',Helvetica,Arial,sans-serif}}
    .t{{font-size:19px;font-weight:700;fill:#70a5fd}}
    .k{{font-size:14px;fill:#a9b1d6}} .v{{font-size:14px;font-weight:700;fill:#38bdae}}
    .bar{{transform-box:fill-box;transform-origin:left;animation:g 1.2s ease-out both}}
    @keyframes g{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
  </style>
  <rect x=".5" y=".5" width="829" height="249" rx="16" fill="#1a1b27" stroke="#2a2e45"/>
  <text x="30" y="46" class="t">GitHub Stats</text>
  <text x="470" y="46" class="t">Top Languages <tspan class="k" font-size="12">(by repository)</tspan></text>
  <line x1="415" y1="30" x2="415" y2="220" stroke="#2a2e45"/>
  {left}
  {right}
</svg>
"""
OUT.write_text(svg, encoding="utf-8")
print("wrote", OUT, rows, top)
