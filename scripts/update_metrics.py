"""Refresh metrics.json, assets/metrics.svg, the README board and METRICS.md.

Repo and container counts are read from the public git_warden and KNORR
READMEs. cves_reported is edited by hand in metrics.json when a report is sent.
"""

import datetime
import json
import pathlib
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
    ("containers_confirmed", "MALICIOUS CONTAINERS", "confirmed", "#7b2dff"),
)


def render_svg(metrics):
    """The Board of Truth card, drawn in the same style as assets/banner.svg."""
    w, h = 1280, 300
    font = "'Consolas','SF Mono','Fira Code',monospace"
    panels = []
    for i, (key, label, sub, color) in enumerate(STATS):
        x = 64 + i * 392
        panels.append(f"""
  <g transform="translate({x},96)">
    <rect width="368" height="150" rx="10" fill="#050c1c" fill-opacity="0.85" stroke="{color}" stroke-opacity="0.55"/>
    <rect width="4" height="150" rx="2" fill="{color}"/>
    <text x="28" y="40" font-family="{font}" font-size="15" letter-spacing="3" fill="{color}">{label}</text>
    <text x="28" y="108" font-family="{font}" font-size="64" font-weight="700" fill="#e6f7ff">{metrics[key]}</text>
    <text x="28" y="134" font-family="{font}" font-size="13" letter-spacing="2" fill="#5fd9ff" fill-opacity="0.7">{sub}</text>
  </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Threat Hunting Board of Truth: {metrics['cves_reported']} CVEs reported, {metrics['repos_confirmed']} malicious repos confirmed, {metrics['containers_confirmed']} malicious containers confirmed">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#04070f"/>
      <stop offset="0.7" stop-color="#050c1c"/>
      <stop offset="1" stop-color="#04070f"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.62" r="0.55">
      <stop offset="0" stop-color="#1f6feb" stop-opacity="0.35"/>
      <stop offset="1" stop-color="#1f6feb" stop-opacity="0"/>
    </radialGradient>
    <pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse">
      <rect width="3" height="1" fill="#38bdf8" fill-opacity="0.05"/>
    </pattern>
    <linearGradient id="spine" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#00eaff"/>
      <stop offset="1" stop-color="#1f6feb"/>
    </linearGradient>
    <linearGradient id="rule" gradientUnits="userSpaceOnUse" x1="240" y1="0" x2="1040" y2="0">
      <stop offset="0" stop-color="#00eaff" stop-opacity="0"/>
      <stop offset="0.15" stop-color="#00eaff"/>
      <stop offset="0.5" stop-color="#7b2dff"/>
      <stop offset="0.85" stop-color="#ff2d7e"/>
      <stop offset="1" stop-color="#ff2d7e" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#sky)"/>
  <rect width="{w}" height="{h}" fill="url(#glow)"/>
  <rect width="{w}" height="{h}" fill="url(#scan)"/>
  <rect width="6" height="{h}" fill="url(#spine)"/>
  <g stroke="#38bdf8" stroke-width="2" fill="none" stroke-opacity="0.8">
    <path d="M40 26 h26 M40 26 v26"/>
    <path d="M1240 26 h-26 M1240 26 v26"/>
    <path d="M40 274 h26 M40 274 v-26"/>
    <path d="M1240 274 h-26 M1240 274 v-26"/>
  </g>
  <text x="640" y="56" text-anchor="middle" font-family="{font}" font-size="22" letter-spacing="6" fill="#00eaff">// THREAT HUNTING BOARD OF TRUTH</text>
  <line x1="240" y1="74" x2="1040" y2="74" stroke="url(#rule)" stroke-width="1.5"/>{"".join(panels)}
  <text x="640" y="276" text-anchor="middle" font-family="{font}" font-size="12" letter-spacing="3" fill="#5fd9ff" fill-opacity="0.6">UPDATED {metrics['updated']}</text>
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
