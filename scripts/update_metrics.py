"""Refresh metrics.json, the table in METRICS.md and the README badges.

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
    badge = ("[![{label}](https://img.shields.io/badge/{label}-{value}-{color}"
             "?style=for-the-badge&labelColor=04070f)](METRICS.md)")
    badges = "\n".join([
        badge.format(label="CVEs_REPORTED", value=metrics["cves_reported"], color="e11d48"),
        badge.format(label="MALICIOUS_REPOS_CONFIRMED", value=metrics["repos_confirmed"], color="1f6feb"),
        badge.format(label="MALICIOUS_CONTAINERS_CONFIRMED", value=metrics["containers_confirmed"], color="1f6feb"),
    ])
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
