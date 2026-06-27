<!--
  GitHub PROFILE README  —  repo must be named EXACTLY: OpenSource-For-Freedom (PUBLIC)
  All header art is CODED (generated from a URL) — nothing to commit, nothing to break.
  The ONLY repo-hosted file is the Cyber Legion photo (see the // arsenal section).
-->

<div align="center">

<img src="./assets/banner.svg" width="100%" alt="OpenSource For Freedom — DevSecOps & Threat Hunting"/>

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=900&color=00EAFF&center=true&vCenter=true&width=820&height=45&lines=DevSecOps+%2F%2F+Threat+Hunting+%2F%2F+DFIR;Marine+Vet+%2F%2F+ex-Gang+Investigator+%2F%2F+Security+Engineer;No+cloud.+No+vendor.+No+leash." alt="typing tagline"/>

<br/>

<a href="https://www.linkedin.com/in/tburns-offsec-specialist/">
  <img src="https://img.shields.io/badge/LinkedIn-tburns--offsec--specialist-05060a?style=for-the-badge&logo=linkedin&logoColor=00eaff" alt="LinkedIn"/>
</a>
<img src="https://komarev.com/ghpvc/?username=OpenSource-For-Freedom&color=ff2d7e&style=for-the-badge&label=PROFILE+VIEWS" alt="profile views"/>
<a href="https://github.com/OpenSource-For-Freedom?tab=followers">
  <img src="https://img.shields.io/github/followers/OpenSource-For-Freedom?style=for-the-badge&logo=github&color=7b2dff&labelColor=05060a&label=FOLLOWERS" alt="followers"/>
</a>

</div>

## `// whoami`

US Marine. Former law-enforcement gang investigator. Now a DevOps security professional. Same mission, new battlefield. I've spent my career hunting the enemy: first in uniform, then on the streets, and now in code. The discipline never changes. Find the threat, learn how it operates, shut it down.

Today I build and ship security engineering across the full DevSecOps lifecycle: hardened CI/CD, supply-chain defense, runtime threat detection, and incident response. Shift-left in the pipeline, watch hard at runtime, and run the investigation when something slips through. Detection, forensics, and threat intel built to run on **your** infrastructure with no cloud dependency and no vendor leash.

Everything here is original and end-to-end, from low-level Rust and eBPF runtime internals to local AI analysts that explain a finding in plain language. The throughline is **open source for freedom**: real security capability that isn't locked behind a paywall.

## `// arsenal`

### [Legion](https://github.com/OpenSource-For-Freedom/legion)
**Local threat detection, backed by your own AI SOC.**

> Cover art: [**Cyber Legion // Hunter Unit VII**](https://github.com/OpenSource-For-Freedom/legion/wiki/Legion) — on the Legion wiki.

[![stars](https://img.shields.io/github/stars/OpenSource-For-Freedom/legion?style=flat-square&logo=github&color=ff2d7e&labelColor=05060a)](https://github.com/OpenSource-For-Freedom/legion/stargazers)
[![last commit](https://img.shields.io/github/last-commit/OpenSource-For-Freedom/legion?style=flat-square&color=00eaff&labelColor=05060a)](https://github.com/OpenSource-For-Freedom/legion/commits)
![Rust](https://img.shields.io/badge/-Rust-05060a?style=flat-square&logo=rust&logoColor=00eaff)
![YARA](https://img.shields.io/badge/-YARA-05060a?style=flat-square&logo=virustotal&logoColor=ff2d7e)

Watches installed packages, files, and network connections against live threat feeds (CISA KEV, AbuseIPDB) and detection rules. Then **Ares**, an AI analyst running entirely on-box, explains every finding in plain English. Browser dashboard plus CLI, Windows and Linux, zero cloud. Your telemetry never leaves the machine.

<br clear="right"/>

### [WRAITH](https://github.com/OpenSource-For-Freedom/wraith)
**Windows incident response and threat hunting.**

[![stars](https://img.shields.io/github/stars/OpenSource-For-Freedom/wraith?style=flat-square&logo=github&color=ff2d7e&labelColor=05060a)](https://github.com/OpenSource-For-Freedom/wraith/stargazers)
[![last commit](https://img.shields.io/github/last-commit/OpenSource-For-Freedom/wraith?style=flat-square&color=00eaff&labelColor=05060a)](https://github.com/OpenSource-For-Freedom/wraith/commits)
![Python](https://img.shields.io/badge/-Python-05060a?style=flat-square&logo=python&logoColor=00eaff)
![.NET 8](https://img.shields.io/badge/-.NET_8-05060a?style=flat-square&logo=dotnet&logoColor=7b2dff)

A native Windows triage app running 14 scan modules: YARA signatures, behavioral heuristics, persistence and process analysis, surfaced through a dark WPF dashboard. Runs alongside Defender and feeds Microsoft Sentinel. Enterprise-grade hunting without the enterprise invoice.

### [Git Warden](https://github.com/OpenSource-For-Freedom/git_warden)
**The warden of malicious repositories and code.**

[![stars](https://img.shields.io/github/stars/OpenSource-For-Freedom/git_warden?style=flat-square&logo=github&color=ff2d7e&labelColor=05060a)](https://github.com/OpenSource-For-Freedom/git_warden/stargazers)
[![last commit](https://img.shields.io/github/last-commit/OpenSource-For-Freedom/git_warden?style=flat-square&color=00eaff&labelColor=05060a)](https://github.com/OpenSource-For-Freedom/git_warden/commits)
![Python](https://img.shields.io/badge/-Python-05060a?style=flat-square&logo=python&logoColor=00eaff)

A threat-intel engine that discovers, statically analyzes, and catalogs malicious GitHub repositories. Ingests MITRE ATT&CK, CISA, and OpenSourceMalware feeds, traces repo lineage, and publishes the evidence to a public Wall of Shame. Static analysis only; nothing hostile ever executes.

### [SOURCE](https://github.com/OpenSource-For-Freedom/SOURCE)
**Automated malicious-IP intelligence.**

[![stars](https://img.shields.io/github/stars/OpenSource-For-Freedom/SOURCE?style=flat-square&logo=github&color=ff2d7e&labelColor=05060a)](https://github.com/OpenSource-For-Freedom/SOURCE/stargazers)
[![last commit](https://img.shields.io/github/last-commit/OpenSource-For-Freedom/SOURCE?style=flat-square&color=00eaff&labelColor=05060a)](https://github.com/OpenSource-For-Freedom/SOURCE/commits)
![Python](https://img.shields.io/badge/-Python-05060a?style=flat-square&logo=python&logoColor=00eaff)
![SQLite](https://img.shields.io/badge/-SQLite-05060a?style=flat-square&logo=sqlite&logoColor=00eaff)

An auto-updating database of malicious IPs with geolocation and ASN enrichment. Aggregates trusted feeds, applies severity scoring, maps offenders geographically, and exports queryable CSV/SQLite, refreshed weekly via GitHub Actions. Built for SOCs and threat hunters.

### [Legion Runner](https://github.com/OpenSource-For-Freedom/Legion_runner)
**Ephemeral, eBPF-aware CI.**

[![stars](https://img.shields.io/github/stars/OpenSource-For-Freedom/Legion_runner?style=flat-square&logo=github&color=ff2d7e&labelColor=05060a)](https://github.com/OpenSource-For-Freedom/Legion_runner/stargazers)
[![last commit](https://img.shields.io/github/last-commit/OpenSource-For-Freedom/Legion_runner?style=flat-square&color=00eaff&labelColor=05060a)](https://github.com/OpenSource-For-Freedom/Legion_runner/commits)
![Rust](https://img.shields.io/badge/-Rust-05060a?style=flat-square&logo=rust&logoColor=00eaff)

Disposable GitHub Actions and local CI runners built in Rust with eBPF-level visibility. Secure, single-use build infrastructure for supply-chain-aware pipelines.

## `// stack`

![Rust](https://img.shields.io/badge/RUST-05060a?style=for-the-badge&logo=rust&logoColor=00eaff)
![Python](https://img.shields.io/badge/PYTHON-05060a?style=for-the-badge&logo=python&logoColor=ff2d7e)
![.NET](https://img.shields.io/badge/.NET_8-05060a?style=for-the-badge&logo=dotnet&logoColor=7b2dff)
![eBPF](https://img.shields.io/badge/eBPF-05060a?style=for-the-badge&logo=linux&logoColor=00eaff)
![YARA](https://img.shields.io/badge/YARA-05060a?style=for-the-badge&logo=virustotal&logoColor=ff2d7e)
![SQLite](https://img.shields.io/badge/SQLITE-05060a?style=for-the-badge&logo=sqlite&logoColor=00eaff)
![GitHub Actions](https://img.shields.io/badge/GH_ACTIONS-05060a?style=for-the-badge&logo=githubactions&logoColor=7b2dff)
![Linux](https://img.shields.io/badge/LINUX-05060a?style=for-the-badge&logo=linux&logoColor=00eaff)

<div align="center">

<img src="https://github-profile-trophy.vercel.app/?username=OpenSource-For-Freedom&theme=matrix&no-frame=true&no-bg=true&column=7&margin-w=4&margin-h=4" alt="trophies"/>

<br/>

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=OpenSource-For-Freedom&layout=compact&hide_border=true&bg_color=05060a&title_color=00eaff&text_color=9becff&hide=html" alt="top languages"/>

</div>
