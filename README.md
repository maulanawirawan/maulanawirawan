<img src="assets/banner.svg" width="100%" alt="Maulana Wirawan — I build security tools that show their work"/>

<p align="center">
  <a href="https://github.com/maulanawirawan/secai"><img src="https://img.shields.io/badge/building-secai-ff2a4d?style=flat-square&labelColor=1a1d24" alt="building secai"/></a>
  <a href="https://github.com/maulanawirawan/secai"><img src="https://img.shields.io/badge/evidence-272_capabilities-8A2BE2?style=flat-square&labelColor=1a1d24" alt="272 capabilities"/></a>
  <img src="https://img.shields.io/badge/based_in-Jakarta,_ID-00b8c4?style=flat-square&labelColor=1a1d24" alt="Jakarta"/>
  <img src="https://img.shields.io/badge/open_to-work_%26_collabs-2ea44f?style=flat-square&labelColor=1a1d24" alt="open to work"/>
</p>

<img src="assets/terminal.svg?v=47-29-17" width="100%" alt="whoami: security tooling and detection engineering, Jakarta"/>

### Self-scan

<img src="assets/self-scan.svg?v=47-29-17" width="100%" alt="secai self-scan dashboard: PRs merged upstream, severity mix of merged CVE templates, top CVSS, and a live threat feed, auto-refreshed every 30 minutes"/>

**This profile scans itself.** Every night a GitHub Action pulls these numbers
straight from the API — detections merged upstream, their severity mix, the
latest CVE shipped, secai's CI state — and redraws the board above. Same rule
as secai: the figures are real, or the run fails and nothing changes. The
generator is right here in the repo: [`.github/scripts/selfscan.py`](.github/scripts/selfscan.py).

<img src="assets/divider.svg" width="100%" alt=""/>

### About

Detection engineering, mostly — the unglamorous half of security where a
finding only counts if you can prove it. I'd rather ship a short report
that survives triage than a long one that gets bounced with *"impact not
demonstrated."*

Most of my time goes to **secai**, an agentic scanner built on a single
rule: a finding you can't prove is a lead, not a claim. Every result sits
on an explicit evidence ladder, and nothing reaches the report until
independent sources agree on it.

The rest of the week splits between network tooling for small businesses
(café Wi‑Fi is a jungle), scrapers that keep working when the site fights
back, and patches sent upstream to the tools I rely on.

<img src="assets/divider.svg" width="100%" alt=""/>

### Projects

<a href="https://github.com/maulanawirawan/secai"><img src="assets/cards/secai.svg" width="100%" alt="secai: an agentic security scanner that refuses to report what it can't prove"/></a>

<img src="assets/evidence-ladder.svg" width="100%" alt="The evidence ladder — a finding only ships at L3 (deterministically verified) and above"/>

<a href="https://github.com/maulanawirawan/minetwin"><img src="assets/cards/minetwin.svg" width="49%" alt="minetwin"/></a>
<a href="https://github.com/maulanawirawan/ngambis"><img src="assets/cards/ngambis.svg" width="49%" alt="ngambis"/></a>
<a href="https://github.com/maulanawirawan/undangan_nikah_digital"><img src="assets/cards/undangan.svg" width="49%" alt="undangan_nikah_digital"/></a>
<img src="assets/cards/netjaga.svg" width="49%" alt="NetJaga (private)"/>

<details>
<summary><b>Open source contributions</b> · <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Fsearch%2Fissues%3Fq%3Dauthor%253Amaulanawirawan%2520type%253Apr%2520is%253Amerged%2520-user%253Amaulanawirawan&query=%24.total_count&label=merged%20upstream&style=flat-square&color=39ff14" alt="merged upstream"/> · <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Fsearch%2Fissues%3Fq%3Dauthor%253Amaulanawirawan%2520type%253Apr%2520is%253Aopen%2520-user%253Amaulanawirawan&query=%24.total_count&label=open%20upstream&style=flat-square&color=00f0ff" alt="open upstream"/></summary>
<br/>

PRs sent to tools I actually use — vuln templates, scrapers, wordlists,
advisories. The status column is live, so this table can't quietly lie.
Showing the highlights; the full list lives in [CONTRIBUTIONS.md](CONTRIBUTIONS.md).

| Project | PR | Status |
|---|---|---|
| [nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) | [#17653](https://github.com/projectdiscovery/nuclei-templates/pull/17653) · stop `dell-idrac9-detect` matching Apple AirPlay receivers | ![](https://img.shields.io/github/pulls/detail/state/projectdiscovery/nuclei-templates/17653?style=flat-square&label=) |
| [Scrapling](https://github.com/D4Vinci/Scrapling) | [#515](https://github.com/D4Vinci/Scrapling/pull/515) · fix a flaky Cloudflare readiness test on macOS / 3.10 | ![](https://img.shields.io/github/pulls/detail/state/D4Vinci/Scrapling/515?style=flat-square&label=) |
| [nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) | [#17669](https://github.com/projectdiscovery/nuclei-templates/pull/17669) · CVE-2026-119495 · Better Search: unauthenticated arbitrary post-type disclosure | ![](https://img.shields.io/github/pulls/detail/state/projectdiscovery/nuclei-templates/17669?style=flat-square&label=) |
| [nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) | [#17672](https://github.com/projectdiscovery/nuclei-templates/pull/17672) · CVE-2026-120597 · Welcart e-Commerce: unauthenticated reflected XSS | ![](https://img.shields.io/github/pulls/detail/state/projectdiscovery/nuclei-templates/17672?style=flat-square&label=) |
| [nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) | [#17675](https://github.com/projectdiscovery/nuclei-templates/pull/17675) · CVE-2026-120446 · madong-admin-saas: platform tenant disclosure | ![](https://img.shields.io/github/pulls/detail/state/projectdiscovery/nuclei-templates/17675?style=flat-square&label=) |
| [nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) | [#17676](https://github.com/projectdiscovery/nuclei-templates/pull/17676) · CVE-2026-120442 · ape-volo-admin: auth bypass via hardcoded JWT secret | ![](https://img.shields.io/github/pulls/detail/state/projectdiscovery/nuclei-templates/17676?style=flat-square&label=) |
| [nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) | [#17685](https://github.com/projectdiscovery/nuclei-templates/pull/17685) · CVE-2026-118523 · EventPrime: unauthenticated pending-post disclosure | ![](https://img.shields.io/github/pulls/detail/state/projectdiscovery/nuclei-templates/17685?style=flat-square&label=) |
| [nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) | [#17691](https://github.com/projectdiscovery/nuclei-templates/pull/17691) · CVE-2026-115574 · Zulip Server: custom profile field disclosure | ![](https://img.shields.io/github/pulls/detail/state/projectdiscovery/nuclei-templates/17691?style=flat-square&label=) |

<p align="center"><a href="CONTRIBUTIONS.md"><b>See every PR, grouped by project →</b></a></p>
</details>

<details>
<summary><b>Earlier research</b> · computer vision on dental imaging</summary>
<br/>

Before security I worked on medical imaging. That's where I learned to
distrust any metric I can't reproduce.

- [Mandible segmentation with U‑Net](https://github.com/maulanawirawan/Mandible-Segmentation-with-UNET) (PyTorch)
- [FPN with an EfficientNet‑B7 backbone](https://github.com/maulanawirawan/FPN-with-EFFICIENTNET-B7-backbone-for-Segmentation-Task) (PyTorch)
- [Periodontal disease classification with a CNN](https://github.com/maulanawirawan/Periodontal-Diseases-with-CNN) (TensorFlow / Keras)

</details>

<details>
<summary><b>Stack</b></summary>
<br/>

<img src="https://skillicons.dev/icons?i=python,rust,ts,js,react,nextjs,threejs,supabase,docker,linux,githubactions,pytorch,tensorflow&perline=13&theme=dark" alt="Python, Rust, TypeScript, JavaScript, React, Next.js, Three.js, Supabase, Docker, Linux, GitHub Actions, PyTorch, TensorFlow"/>

</details>

<details>
<summary><b>Activity</b> · 3D contribution graph</summary>
<br/>

<img src="profile-3d-contrib/profile-night-green.svg" width="100%" alt="3D contribution graph"/>

</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maulanawirawan/maulanawirawan/output/github-contribution-grid-snake-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/maulanawirawan/maulanawirawan/output/github-contribution-grid-snake.svg"/>
  <img alt="contribution snake" src="https://raw.githubusercontent.com/maulanawirawan/maulanawirawan/output/github-contribution-grid-snake.svg"/>
</picture>

<img src="assets/divider.svg" width="100%" alt=""/>

### Capture the flag

Three flags are hidden in the SVGs on this page: the board that scans me, the
evidence ladder, and the terminal's house rules. Each one is wrapped in a
different classic encoding (base64, hex, rot13). Find all three, then prove it
without leaking them: post `sha256("your-username:flag")` for each in a
**CTF submission** issue. A bot checks the proofs and signs you into the
[Hall of Fame](HALL-OF-FAME.md). Rules: [CTF.md](CTF.md).

<sub>Never post a raw flag. Authorized target: this profile. `view-source` is the whole toolkit.</sub>

<img src="assets/divider.svg" width="100%" alt=""/>

### Get in touch

Open to detection engineering, network security tooling, and scraping
work — collab or hire. Fastest way to reach me is an issue or PR on
[secai](https://github.com/maulanawirawan/secai/issues). I read every one.
