"""Refresh metrics.json, assets/metrics.svg, the README board and METRICS.md.

Repo and container counts are read from the public git_warden and KNORR
READMEs. cves_reported is edited by hand in metrics.json when a report is sent.
"""

import datetime
import json
import pathlib
import random
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = "https://raw.githubusercontent.com/OpenSource-For-Freedom/{repo}/main/README.md"
SOURCES = {
    "repos_confirmed": ("git_warden", r"of ([\d,]+) repositories confirmed malicious"),
    "containers_confirmed": ("KNORR", r"([\d,]+) confirmed malicious images"),
}


def fetch_count(repo, pattern):
    with urllib.request.urlopen(RAW.format(repo=repo), timeout=30) as resp:
        text = resp.read().decode("utf-8")
    match = re.search(pattern, text)
    return int(match.group(1).replace(",", "")) if match else None


STATS = (
    ("cves_reported", "CVEs REPORTED", "to maintainers", "#ff2d7e"),
    ("repos_confirmed", "MALICIOUS REPOS", "confirmed", "#00eaff"),
    ("containers_confirmed", "MALICIOUS CONTAINERS", "confirmed", "#a66bff"),
)
FONT = "'Consolas','SF Mono','Fira Code',monospace"
W, H = 1280, 320
INSET = 20          # corner brackets sit this far in from every edge
MARGIN = 64         # panels sit this far in from the left and right edges
GAP = 24
PANEL_W = (W - 2 * MARGIN - 2 * GAP) // 3
PANEL_Y, PANEL_H = 100, 144


def _bracket(x, y, dx, dy, size):
    return f'<path d="M{x} {y} h{dx * size} M{x} {y} v{dy * size}"/>'


def _corners(x, y, w, h, size):
    return "".join([
        _bracket(x, y, 1, 1, size), _bracket(x + w, y, -1, 1, size),
        _bracket(x, y + h, 1, -1, size), _bracket(x + w, y + h, -1, -1, size),
    ])


def _matrix_rain():
    """Columns of falling 1s and 0s. Seeded, so the file only changes with the counts."""
    rng = random.Random(1010101)
    step, line = 20, 18
    rows = H // line + 2
    cols = []
    for x in range(10, W, step):
        digits = "".join(rng.choice("01") for _ in range(rows))
        tspans = "".join(f'<tspan x="{x}" dy="{line}">{d}</tspan>' for d in digits)
        dur = rng.uniform(6, 14)
        style = f'animation-duration:{dur:.1f}s;animation-delay:{-rng.uniform(0, dur):.1f}s'
        op = rng.choice((0.10, 0.14, 0.18, 0.24))
        # Two stacked copies make the loop seamless.
        for y in (0, -rows * line):
            cols.append(f'<text class="rain" style="{style}" fill-opacity="{op}" y="{y}">{tspans}</text>')
    return "".join(cols), rows * line


def render_svg(metrics):
    """The Board of Truth card: matrix rain, symmetric frame, three equal panels."""
    rain, loop = _matrix_rain()
    panels = []
    for i, (key, label, sub, color) in enumerate(STATS):
        x = MARGIN + i * (PANEL_W + GAP)
        cx = PANEL_W // 2
        panels.append(f"""
  <g transform="translate({x},{PANEL_Y})">
    <rect width="{PANEL_W}" height="{PANEL_H}" rx="6" fill="#03060d" fill-opacity="0.88" stroke="{color}" stroke-opacity="0.45"/>
    <g stroke="{color}" stroke-width="2" fill="none">{_corners(0, 0, PANEL_W, PANEL_H, 12)}</g>
    <text x="{cx}" y="36" text-anchor="middle" font-family="{FONT}" font-size="14" letter-spacing="3" fill="{color}">{label}</text>
    <text x="{cx}" y="98" text-anchor="middle" font-family="{FONT}" font-size="58" font-weight="700" fill="#e6f7ff">{metrics[key]}</text>
    <text x="{cx}" y="124" text-anchor="middle" font-family="{FONT}" font-size="12" letter-spacing="3" fill="#7dffb2" fill-opacity="0.65">{sub}</text>
  </g>""")
    title_y = INSET + 42
    rule_y = title_y + 16
    footer_y = H - INSET - 20
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Threat Hunting Board of Truth: {metrics['cves_reported']} CVEs reported, {metrics['repos_confirmed']} malicious repos confirmed, {metrics['containers_confirmed']} malicious containers confirmed">
  <style>
    .rain {{ font-family: {FONT}; font-size: 15px; fill: #00ff9c; animation: fall linear infinite; }}
    @keyframes fall {{ from {{ transform: translateY(0); }} to {{ transform: translateY({loop}px); }} }}
    @media (prefers-reduced-motion: reduce) {{ .rain {{ animation: none; }} }}
  </style>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#010a05"/>
      <stop offset="0.5" stop-color="#031009"/>
      <stop offset="1" stop-color="#010a05"/>
    </linearGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#010a05" stop-opacity="1"/>
      <stop offset="0.18" stop-color="#010a05" stop-opacity="0"/>
      <stop offset="0.82" stop-color="#010a05" stop-opacity="0"/>
      <stop offset="1" stop-color="#010a05" stop-opacity="1"/>
    </linearGradient>
    <pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse">
      <rect width="3" height="1" fill="#00ff9c" fill-opacity="0.04"/>
    </pattern>
    <linearGradient id="rule" gradientUnits="userSpaceOnUse" x1="{W // 2 - 380}" y1="0" x2="{W // 2 + 380}" y2="0">
      <stop offset="0" stop-color="#00ff9c" stop-opacity="0"/>
      <stop offset="0.2" stop-color="#00ff9c"/>
      <stop offset="0.5" stop-color="#00eaff"/>
      <stop offset="0.8" stop-color="#00ff9c"/>
      <stop offset="1" stop-color="#00ff9c" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}"/></clipPath>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <g clip-path="url(#frame)">{rain}</g>
  <rect width="{W}" height="{H}" fill="url(#fade)"/>
  <rect width="{W}" height="{H}" fill="url(#scan)"/>
  <g stroke="#00ff9c" stroke-width="2" fill="none" stroke-opacity="0.85">{_corners(INSET, INSET, W - 2 * INSET, H - 2 * INSET, 28)}</g>
  <text x="{W // 2}" y="{title_y}" text-anchor="middle" font-family="{FONT}" font-size="22" letter-spacing="6" fill="#00ff9c">// THREAT HUNTING BOARD OF TRUTH</text>
  <line x1="{W // 2 - 380}" y1="{rule_y}" x2="{W // 2 + 380}" y2="{rule_y}" stroke="url(#rule)" stroke-width="1.5"/>{"".join(panels)}
  <text x="{W // 2}" y="{footer_y}" text-anchor="middle" font-family="{FONT}" font-size="12" letter-spacing="3" fill="#7dffb2" fill-opacity="0.6">UPDATED {metrics['updated']}</text>
</svg>
"""


def main():
    path = ROOT / "metrics.json"
    metrics = json.loads(path.read_text())
    changed = False
    for key, (repo, pattern) in SOURCES.items():
        value = fetch_count(repo, pattern)
        # Keep the last known value if a README can't be read or parsed.
        if value is not None and value != metrics.get(key):
            metrics[key] = value
            changed = True
    if changed:
        metrics["updated"] = datetime.date.today().isoformat()
        path.write_text(json.dumps(metrics, indent=2) + "\n")

    table = "\n".join([
        "| | |",
        "|---|---|",
        f"| CVEs reported to maintainers | **{metrics['cves_reported']}** |",
        f"| Malicious repositories confirmed | **{metrics['repos_confirmed']}** |",
        f"| Malicious container images confirmed | **{metrics['containers_confirmed']}** |",
        "",
        f"_Updated {metrics['updated']}_",
    ])
    (ROOT / "assets" / "metrics.svg").write_text(render_svg(metrics))
    badges = '<a href="METRICS.md"><img src="assets/metrics.svg" alt="Threat Hunting Board of Truth" width="100%"/></a>'
    readme = ROOT / "README.md"
    readme.write_text(re.sub(
        r"(<!-- metrics-badges:start -->\n).*?(<!-- metrics-badges:end -->)",
        lambda m: m.group(1) + badges + "\n" + m.group(2), readme.read_text(), flags=re.S))

    page = ROOT / "METRICS.md"
    text = page.read_text()
    text = re.sub(r"(<!-- metrics:start -->\n).*?(<!-- metrics:end -->)",
                  lambda m: m.group(1) + table + "\n" + m.group(2), text, flags=re.S)
    page.write_text(text)


if __name__ == "__main__":
    main()
