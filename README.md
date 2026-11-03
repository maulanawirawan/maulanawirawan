<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=22&duration=3200&pause=900&color=58A6FF&center=true&vCenter=true&width=620&lines=Hi%2C+I'm+Maulana+%F0%9F%91%8B;I+write+security+tools+that+show+their+work.;Detection+engineering+%C2%B7+network+tooling+%C2%B7+scraping;Jakarta%2C+Indonesia" alt="Hi, I'm Maulana"/>

<br/>

<a href="https://github.com/maulanawirawan/cyphron"><img src="https://img.shields.io/badge/building-cyphron-8A2BE2?style=flat-square&logo=github" alt="building cyphron"/></a>
<img src="https://img.shields.io/badge/based_in-Jakarta%2C_ID-red?style=flat-square" alt="Jakarta"/>
<img src="https://img.shields.io/badge/open_to-collabs_%26_work-2ea44f?style=flat-square" alt="open to work"/>

</div>

---

### About me

I work on the boring-but-important side of security: detection,
evidence, and tooling that doesn't cry wolf.

Most of my time goes into **[cyphron](https://github.com/maulanawirawan/cyphron)**,
a security assessment engine built around one rule: if a finding can't
be proven, it doesn't go in the report. Outside of that I build network
tools for small businesses (cafe Wi‑Fi is a jungle), write scrapers that
keep working when the site fights back, and send fixes upstream to the
open-source tools I use every day.

Before security, I did a fair bit of computer vision on dental imaging
(U‑Net, FPN, CNN classifiers). That's where I learned to distrust any
metric I can't reproduce.

```yaml
currently:   hardening cyphron's detection skills and Rust core
learning:    writing nuclei templates that survive maintainer review
values:      evidence over vibes, small PRs, honest READMEs
ask me about: detection engineering, false positives, Python, Rust
```

### Featured project

<table>
<tr>
<td width="100%">

**[cyphron](https://github.com/maulanawirawan/cyphron)** · Python + Rust

Evidence-first security assessment. 92 detection skills, one strict
`findings.json` contract shared by Python and Rust, cross-tool quorum
that only promotes a lead when independent sources agree, and threat
intel that keeps itself fresh from CISA KEV, NVD, and OSV.
914 tests in CI. Ships with an MCP server, so you can drive it from
Claude Code or Cursor.

<sub>*No exploit, no report.*</sub>

</td>
</tr>
</table>

### Upstream work

PRs I've opened against projects I depend on. Status badges are live,
so what you see is what's actually there.

| Project | PR | Status |
|---|---|---|
| [projectdiscovery/nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) | [#17651](https://github.com/projectdiscovery/nuclei-templates/pull/17651) · CVE-2026-96654 Plex Media Server detection (KEV) | ![](https://img.shields.io/github/pulls/detail/state/projectdiscovery/nuclei-templates/17651?style=flat-square&label=) |
| [projectdiscovery/nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) | [#17654](https://github.com/projectdiscovery/nuclei-templates/pull/17654) · cut false positives in `smb-default-login` with a canary credential | ![](https://img.shields.io/github/pulls/detail/state/projectdiscovery/nuclei-templates/17654?style=flat-square&label=) |
| [projectdiscovery/nuclei-templates](https://github.com/projectdiscovery/nuclei-templates) | [#17653](https://github.com/projectdiscovery/nuclei-templates/pull/17653) · stop `dell-idrac9-detect` from matching Apple AirPlay receivers | ![](https://img.shields.io/github/pulls/detail/state/projectdiscovery/nuclei-templates/17653?style=flat-square&label=) |
| [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) | [#513](https://github.com/D4Vinci/Scrapling/pull/513) · bound async `all_headers()` waits so they can't hang forever | ![](https://img.shields.io/github/pulls/detail/state/D4Vinci/Scrapling/513?style=flat-square&label=) |
| [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) | [#515](https://github.com/D4Vinci/Scrapling/pull/515) · fix a flaky Cloudflare readiness test on macOS / 3.10 | ![](https://img.shields.io/github/pulls/detail/state/D4Vinci/Scrapling/515?style=flat-square&label=) |

### Other things I've built

- **[minetwin](https://github.com/maulanawirawan/minetwin)**: a mining digital-twin dashboard MVP with a 3D pit view (all data simulated, and it says so on screen)
- **[ngambis](https://github.com/maulanawirawan/ngambis)**: a private accountability and planning space for study circles: daily reports, kanban, focus timer
- **[undangan_nikah_digital](https://github.com/maulanawirawan/undangan_nikah_digital)**: a one-page digital wedding invite with a real-time 3D cover, no build step, edit one config file and ship
- **NetJaga** *(private)*: a LAN guardian for cafe networks: device monitoring, allowlists, DNS patrol
- **Medical imaging research**: [mandible segmentation (U‑Net)](https://github.com/maulanawirawan/Mandible-Segmentation-with-UNET), [FPN + EfficientNet‑B7](https://github.com/maulanawirawan/FPN-with-EFFICIENTNET-B7-backbone-for-Segmentation-Task), [periodontal disease CNN](https://github.com/maulanawirawan/Periodontal-Diseases-with-CNN)

### Toolbox

<p>
  <img src="https://skillicons.dev/icons?i=python,rust,ts,js,react,nextjs,threejs,supabase,docker,linux,githubactions,pytorch,tensorflow&perline=13" alt="tech stack"/>
</p>

### Contribution graph, eaten by a snake

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maulanawirawan/maulanawirawan/output/github-contribution-grid-snake-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/maulanawirawan/maulanawirawan/output/github-contribution-grid-snake.svg"/>
  <img alt="contribution snake" src="https://raw.githubusercontent.com/maulanawirawan/maulanawirawan/output/github-contribution-grid-snake.svg"/>
</picture>

### Let's talk

Happy to collaborate on detection engineering, network security tooling,
or scraping pipelines. The easiest way to reach me is an issue on
[cyphron](https://github.com/maulanawirawan/cyphron/issues), or just
open a PR. I read them all.

<div align="center">
<sub>Built with patience and too much kopi. ☕</sub>
</div>
