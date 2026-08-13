#!/usr/bin/env python3
"""
Generate a theme-matched GitHub stats panel (stats.svg) - self-hosted,
no fork, no Vercel, no third-party instance. Authenticates with STATS_PAT
(GraphQL for stars/PRs/issues/contributed-to/languages, REST search for
all-time commit count), renders two side-by-side cards in one SVG.

Theme: matches the projects panel (navy #0A101F, chrome cyan #22D3EE/#0891B2,
portrait/accent indigo #818CF8/#4F46E5, mono font, terminal-style card chrome).
Language dots use GitHub's real per-language colors, not the accent palette.
"""
import json, os, sys, html, urllib.request
from datetime import datetime, timezone

TOKEN = os.environ.get("STATS_PAT", "")
USERNAME = os.environ.get("STATS_USERNAME", "Engrziaullah")

# ---------------- themes (same values as generate_projects.py) ----------------
THEMES = {
    "dark": {
        "BG": "#0A101F", "PANEL": "#0C1426", "PANEL_BAR": "#0B1222",
        "CYAN": "#22D3EE", "VIOLET": "#818CF8", "VIOLET2": "#818CF8",
        "EMERALD": "#10B981", "TEXT": "#F8FAFC", "MUTED": "#94A3B8",
        "DIM": "#475569",
        "STROKE": "rgba(34,211,238,0.28)", "STROKE_HI": "rgba(34,211,238,0.5)",
        "STROKE_LO": "rgba(34,211,238,0.22)", "BARLINE": "rgba(255,255,255,0.08)",
        "RING_BG": "rgba(148,163,184,0.15)",
    },
    "light": {
        "BG": "#F8FAFC", "PANEL": "#FFFFFF", "PANEL_BAR": "#F1F5F9",
        "CYAN": "#0891B2", "VIOLET": "#4F46E5", "VIOLET2": "#4F46E5",
        "EMERALD": "#059669", "TEXT": "#0F172A", "MUTED": "#475569",
        "DIM": "#94A3B8",
        "STROKE": "rgba(8,145,178,0.30)", "STROKE_HI": "rgba(8,145,178,0.55)",
        "STROKE_LO": "rgba(8,145,178,0.20)", "BARLINE": "rgba(0,0,0,0.08)",
        "RING_BG": "rgba(100,116,139,0.20)",
    },
}

BG = PANEL = PANEL_BAR = CYAN = VIOLET = VIOLET2 = EMERALD = TEXT = MUTED = DIM = None
STROKE = STROKE_HI = STROKE_LO = BARLINE = RING_BG = None

def set_theme(name):
    g = globals()
    for k, v in THEMES[name].items():
        g[k] = v

set_theme("dark")

W      = 1180
CARD_W = 578
CARD_H = 192
GAP    = 14
MARGIN = 5
FONT   = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

def esc(s): return html.escape(str(s), quote=True)
def fmt(n): return f"{n:,}"

# ---------------- fetch ----------------
def gh_graphql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "stats-panel",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]

def gh_rest(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "User-Agent": "stats-panel",
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

QUERY = """
query($login: String!) {
  user(login: $login) {
    pullRequests { totalCount }
    issues { totalCount }
    repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
      totalCount
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""

def fetch_stats():
    stats = {"stars": 0, "commits": 0, "prs": 0, "issues": 0, "contributed_to": 0, "languages": {}}
    try:
        u = gh_graphql(QUERY, {"login": USERNAME})["user"]
        stats["prs"] = u["pullRequests"]["totalCount"]
        stats["issues"] = u["issues"]["totalCount"]
        stats["contributed_to"] = u["repositoriesContributedTo"]["totalCount"]
        stats["stars"] = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])
        langs = {}
        # isFork: false in the query already excludes forks (e.g. the
        # github-readme-stats fork itself), which would otherwise flood
        # this with unrelated Dart/TS/JS bytes and corrupt the chart.
        for r in u["repositories"]["nodes"]:
            for e in r["languages"]["edges"]:
                name = e["node"]["name"]
                slot = langs.setdefault(name, {"size": 0, "color": e["node"]["color"] or "#94A3B8"})
                slot["size"] += e["size"]
        stats["languages"] = langs
    except Exception as e:
        print(f"warn: graphql stats fetch failed: {e}", file=sys.stderr)
    try:
        sr = gh_rest(f"https://api.github.com/search/commits?q=author:{USERNAME}")
        stats["commits"] = sr.get("total_count", 0)
    except Exception as e:
        print(f"warn: commit search failed: {e}", file=sys.stderr)
    return stats

# ---------------- render ----------------
STAT_ROWS = [
    ("stars", "Total Stars Earned"),
    ("commits", "Total Commits"),
    ("prs", "Total PRs"),
    ("issues", "Total Issues"),
    ("contributed_to", "Contributed To"),
]

def card_shell(x, y, w, h, title, begin):
    e = []; a = e.append
    a(f'<g transform="translate({x},{y})">')
    a(f'<rect width="{w}" height="{h}" rx="12" fill="{PANEL}" stroke="{STROKE}">'
      f'<animate attributeName="stroke" values="{STROKE_LO};{STROKE_HI};{STROKE_LO}" '
      f'dur="4.5s" begin="{begin:.2f}s" repeatCount="indefinite"/></rect>')
    a(f'<rect width="{w}" height="30" rx="12" fill="{PANEL_BAR}"/>')
    a(f'<rect y="18" width="{w}" height="12" fill="{PANEL_BAR}"/>')
    a(f'<line x1="0" y1="30" x2="{w}" y2="30" stroke="{BARLINE}"/>')
    a(f'<text x="16" y="19" font-size="10" fill="{MUTED}"><tspan fill="{CYAN}">&#8226;</tspan> {esc(title)}</text>')
    return e  # caller appends body, then must a('</g>') and join

def stats_card(stats, x, y):
    e = card_shell(x, y, CARD_W, CARD_H, f"{USERNAME}'s GitHub Stats", 0.3)
    a = e.append
    ry = 58
    for i, (key, label) in enumerate(STAT_ROWS):
        b = 0.4 + i * 0.12
        val = fmt(stats.get(key, 0))
        a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{b:.2f}s" fill="freeze"/>')
        a(f'<circle cx="24" cy="{ry-5}" r="3.5" fill="{VIOLET}"/>')
        a(f'<text x="38" y="{ry}" font-size="13" fill="{MUTED}">{esc(label)}</text>')
        a(f'<text x="{CARD_W-24}" y="{ry}" text-anchor="end" font-size="14" font-weight="700" fill="{TEXT}">{val}</text>')
        a('</g>')
        ry += 28
    a('</g>')
    return "".join(e)

def lang_card(languages, x, y):
    e = card_shell(x, y, CARD_W, CARD_H, "Most Used Languages", 0.5)
    a = e.append
    total = sum(v["size"] for v in languages.values()) or 1
    top = sorted(languages.items(), key=lambda kv: -kv[1]["size"])[:8]

    bar_x, bar_y, bar_w, bar_h = 16, 50, CARD_W - 32, 10
    a(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="5" fill="{RING_BG}"/>')
    cx = bar_x
    for i, (name, info) in enumerate(top):
        frac = info["size"] / total
        seg_w = frac * bar_w
        b = 0.55 + i * 0.08
        a(f'<rect x="{cx:.1f}" y="{bar_y}" width="{seg_w:.1f}" height="{bar_h}" fill="{info["color"]}" opacity="0">'
          f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{b:.2f}s" fill="freeze"/></rect>')
        cx += seg_w

    ly = 82
    col_w = (CARD_W - 32) / 2
    for i, (name, info) in enumerate(top):
        frac = info["size"] / total
        col, row = i % 2, i // 2
        lx = bar_x + col * col_w
        yy = ly + row * 22
        b = 0.6 + i * 0.08
        a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{b:.2f}s" fill="freeze"/>')
        a(f'<circle cx="{lx+4:.1f}" cy="{yy-4}" r="4" fill="{info["color"]}"/>')
        a(f'<text x="{lx+14:.1f}" y="{yy}" font-size="11" fill="{MUTED}">{esc(name)} {frac*100:.1f}%</text>')
        a('</g>')
    if not top:
        a(f'<text x="{bar_x}" y="{ly+10}" font-size="11" fill="{DIM}">no language data</text>')
    a('</g>')
    return "".join(e)

def build(stats, theme="dark"):
    set_theme(theme)
    H = 42 + CARD_H + MARGIN
    gid = f"stats_acc_{theme}"
    s = []; a = s.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="{FONT}" role="img" aria-label="GitHub Stats">')
    a(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    a(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="{VIOLET2}"><animate attributeName="stop-color" values="{VIOLET2};{CYAN};{EMERALD};{VIOLET2}" dur="10s" repeatCount="indefinite"/></stop>'
      f'<stop offset="1" stop-color="{EMERALD}"><animate attributeName="stop-color" values="{EMERALD};{VIOLET2};{CYAN};{EMERALD}" dur="10s" repeatCount="indefinite"/></stop>'
      '</linearGradient></defs>')
    a(f'<text x="{MARGIN+2}" y="18" font-size="11" letter-spacing="2" fill="{CYAN}">GITHUB.STATS</text>')
    a(f'<text x="{MARGIN+140}" y="18" font-size="10" fill="{DIM}">./stats.sh --summary</text>')
    a(f'<line x1="{MARGIN}" y1="28" x2="{W-MARGIN}" y2="28" stroke="url(#{gid})" stroke-width="1.5" opacity="0.7"/>')
    a(stats_card(stats, MARGIN, 42))
    a(lang_card(stats["languages"], MARGIN + CARD_W + GAP + 4, 42))
    a('</svg>')
    return "".join(s)

if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    stats = fetch_stats()
    for theme, fname in (("dark", "stats.svg"), ("light", "stats-light.svg")):
        svg = build(stats, theme)
        path = os.path.join(outdir, fname)
        with open(path, "w") as f:
            f.write(svg)
        print(f"wrote {path}: {theme}, {len(svg)//1024}KB")
    print(f"stars={stats['stars']} commits={stats['commits']} prs={stats['prs']} "
          f"issues={stats['issues']} contributed_to={stats['contributed_to']} "
          f"langs={len(stats['languages'])}")
