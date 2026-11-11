#!/usr/bin/env python3
"""Regenerate assets/self-scan.svg from live GitHub data.

The profile "scans itself": every night a GitHub Action runs this, pulls the
real numbers from the public API (merged upstream PRs, the severity mix of the
CVE detection templates that landed, the top CVSS shipped, secai's CI state)
and redraws the board. Same rule as secai — the figures are real, or the run
fails and the previous board stays up. No made-up numbers.

Usage:  python selfscan.py --out assets/self-scan.svg
Auth:   optional, reads GH_TOKEN or GITHUB_TOKEN from the environment.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

USER = "maulanawirawan"
NUCLEI = "projectdiscovery/nuclei-templates"
SECAI = f"{USER}/secai"

SEV_ORDER = ["critical", "high", "medium", "low", "info"]
SEV_COLOR = {
    "critical": "#ff2a4d",
    "high": "#ff7a1a",
    "medium": "#ffb02e",
    "low": "#00f0ff",
    "info": "#6b7079",
}


def _headers() -> dict:
    h = {
        "User-Agent": "secai-selfscan",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok.strip()}"
    return h


def fetch(url: str, raw: bool = False, tries: int = 4):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=_headers())
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read().decode("utf-8")
                return body if raw else json.loads(body)
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (403, 429):
                reset = e.headers.get("x-ratelimit-reset")
                wait = 5 * (attempt + 1)
                if reset:
                    wait = max(1, min(60, int(reset) - int(time.time()) + 1))
                time.sleep(wait)
                continue
            raise
        except urllib.error.URLError as e:
            last = e
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"GET failed after {tries} tries: {url} ({last})")


def search_count(query: str) -> tuple[int, list]:
    url = ("https://api.github.com/search/issues?q="
           + urllib.parse.quote(query) + "&per_page=100")
    data = fetch(url)
    return int(data.get("total_count", 0)), data.get("items", [])


def parse_template(text: str) -> dict:
    out = {}
    for line in text.splitlines():
        s = line.strip()
        for key in ("id", "name", "severity", "cvss-score"):
            if s.lower().startswith(key + ":"):
                out[key] = s[len(key) + 1:].strip().strip('"\'')
                break
    return out


def collect() -> dict:
    merged_total, merged_items = search_count(
        f"author:{USER} type:pr is:merged -user:{USER}")
    open_total, _ = search_count(f"author:{USER} type:pr is:open -user:{USER}")
    if merged_total <= 0:
        raise RuntimeError("merged PR count came back as 0 — refusing to render")

    cves = []  # (closed_at, cve_id, severity, cvss)
    for it in merged_items:
        if not it.get("repository_url", "").endswith("/" + NUCLEI):
            continue
        if "CVE-" not in (it.get("title") or ""):
            continue
        try:
            files = fetch(f"https://api.github.com/repos/{NUCLEI}/pulls/{it['number']}/files")
        except Exception:
            continue
        for f in files:
            fn = f.get("filename", "")
            if "/cves/" not in fn or not fn.endswith(".yaml"):
                continue
            try:
                meta = parse_template(fetch(f["raw_url"], raw=True))
            except Exception:
                continue
            cid = meta.get("id", "").upper()
            sev = (meta.get("severity") or "").lower()
            if not cid.startswith("CVE-") or sev not in SEV_COLOR:
                continue
            try:
                cvss = float(meta.get("cvss-score", "nan"))
            except ValueError:
                cvss = float("nan")
            cves.append((it.get("closed_at") or "", cid, sev, cvss))
            break

    seen, uniq = set(), []
    for row in sorted(cves, key=lambda r: r[0], reverse=True):
        if row[1] not in seen:
            seen.add(row[1])
            uniq.append(row)

    hist = {s: 0 for s in SEV_ORDER}
    for _, _, sev, _ in uniq:
        hist[sev] += 1

    scored = [r for r in uniq if r[3] == r[3]]  # drop NaN
    top = max(scored, key=lambda r: r[3]) if scored else None

    ci = "unknown"
    try:
        runs = fetch(f"https://api.github.com/repos/{SECAI}/actions/runs"
                     "?branch=main&per_page=1&status=completed")
        wr = runs.get("workflow_runs") or []
        if wr:
            ci = wr[0].get("conclusion") or "unknown"
    except Exception:
        pass

    return {
        "merged_prs": merged_total,
        "open_prs": open_total,
        "cve_count": len(uniq),
        "hist": hist,
        "max_cvss": (f"{top[3]:.1f}" if top else "—"),
        "max_cvss_id": (top[1] if top else ""),
        "ci": ci,
        "feed": [(cid, (f"{cvss:.1f}" if cvss == cvss else "—"), sev)
                 for _, cid, sev, cvss in uniq],
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
    }


CSS = """
    text { font-family: 'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace; }
    .hdr  { fill:#f4f4f6; font-size:21px; font-weight:800; letter-spacing:3px; }
    .sub  { fill:#6b7079; font-size:13px; }
    .big  { font-size:42px; font-weight:800; }
    .tl   { fill:#8a8f98; font-size:12px; letter-spacing:1px; }
    .cap  { fill:#8a8f98; font-size:12px; letter-spacing:2px; }
    .leg  { font-size:12.5px; fill:#a9adb7; }
    .chip { font-size:14px; font-weight:700; }
    .cvss { fill:#6b7079; font-size:14px; }
    .live { fill:#39ff14; font-size:12px; font-weight:700; letter-spacing:1px; }
    .foot { fill:#5d626d; font-size:11px; letter-spacing:.5px; }
    .ok   { fill:#39ff14; } .bad { fill:#ffb02e; }
    .dot  { animation: bk 1.4s infinite steps(1); }
    @keyframes bk { 50% { opacity:.2; } }
    .scan { animation: scan 6.5s linear infinite; }
    @keyframes scan { 0% { transform: translateY(2px); } 100% { transform: translateY(306px); } }
    .feedmove { animation: feed FEED_DURs linear infinite; }
    @keyframes feed { to { transform: translateX(-FEED_Wpx); } }
"""


def _chips(feed, base_x):
    gap, out, x = 48, [], base_x
    for cid, cvss, sev in feed:
        c = SEV_COLOR[sev]
        x_cvss = x + 18 + len(cid) * 8.6 + 14
        x_sev = x_cvss + len(cvss) * 8.6 + 16
        out.append(
            f'<circle cx="{x + 5:.0f}" cy="272" r="5" fill="{c}"/>'
            f'<text x="{x + 18:.0f}" y="277" class="chip" fill="{c}">{html.escape(cid)}</text>'
            f'<text x="{x_cvss:.0f}" y="277" class="cvss">{html.escape(cvss)}</text>'
            f'<text x="{x_sev:.0f}" y="277" class="chip" fill="{c}">{sev.upper()}</text>')
        x += 18 + len(f"{cid}   {cvss}   {sev.upper()}") * 8.6 + gap
    return "".join(out), x - base_x


def tile(x, big, label, color):
    return (f'<g transform="translate({x},62)">'
            f'<rect width="273" height="86" rx="12" fill="#0e1016" stroke="#262a33"/>'
            f'<rect width="4" height="86" rx="2" fill="{color}"/>'
            f'<text x="22" y="54" class="big" fill="{color}">{html.escape(str(big))}</text>'
            f'<text x="22" y="74" class="tl">{html.escape(label)}</text></g>')


def render(d: dict) -> str:
    _, feed_w = _chips(d["feed"], 0)
    feed_w = max(1.0, feed_w)
    chips_a, _ = _chips(d["feed"], 190)
    chips_b, _ = _chips(d["feed"], 190 + feed_w)
    css = (CSS.replace("FEED_DUR", str(max(16, len(d["feed"]) * 3)))
              .replace("FEED_W", f"{feed_w:.0f}"))

    ci_ok = d["ci"] == "success"
    ci_cls, ci_txt = ("ok", "passing") if ci_ok else ("bad", d["ci"])

    bar_x, bar_w, bar_y, bar_h = 30, 1140, 180, 26
    total = max(1, sum(d["hist"].values()))
    seg, cx = [], float(bar_x)
    for s in SEV_ORDER:
        if d["hist"][s] == 0:
            continue
        w = bar_w * d["hist"][s] / total
        seg.append(f'<rect x="{cx:.1f}" y="{bar_y}" width="{w:.1f}" height="{bar_h}" fill="{SEV_COLOR[s]}"/>')
        cx += w
    legend, lx = [], bar_x
    for s in SEV_ORDER:
        if d["hist"][s] == 0:
            continue
        legend.append(f'<circle cx="{lx + 5}" cy="226" r="5" fill="{SEV_COLOR[s]}"/>'
                      f'<text x="{lx + 16}" y="231" class="leg">{d["hist"][s]} {s}</text>')
        lx += 20 + (len(s) + len(str(d["hist"][s])) + 1) * 8 + 26

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-label="secai self-scan: live security dashboard of {USER}">
  <defs>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ff2a4d"/><stop offset=".5" stop-color="#8A2BE2"/><stop offset="1" stop-color="#00f0ff"/>
    </linearGradient>
    <clipPath id="frame"><rect width="1200" height="320" rx="14"/></clipPath>
    <clipPath id="barclip"><rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="7"/></clipPath>
    <clipPath id="feedclip"><rect x="30" y="248" width="1140" height="48" rx="10"/></clipPath>
    <style>{css}</style>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="1200" height="320" fill="#0a0b10"/>
    <rect width="1200" height="3" fill="url(#edge)"/>

    <text x="30" y="40" class="hdr">SELF-SCAN</text>
    <text x="200" y="40" class="sub">// {USER} · this profile scans itself</text>
    <circle cx="1116" cy="35" r="5" fill="#39ff14" class="dot"/>
    <text x="1130" y="40" class="live">LIVE</text>

    {tile(30,  d["merged_prs"], "PRS MERGED UPSTREAM", "#39ff14")}
    {tile(319, d["open_prs"],   "IN REVIEW", "#00f0ff")}
    {tile(608, d["cve_count"],  "CVE DETECTIONS SHIPPED", "#8A2BE2")}
    {tile(897, d["max_cvss"],   "TOP CVSS · " + d["max_cvss_id"], "#ff2a4d")}

    <text x="30" y="172" class="cap">MERGED CVE TEMPLATES BY SEVERITY</text>
    <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="7" fill="#12141b" stroke="#262a33"/>
    <g clip-path="url(#barclip)">{''.join(seg)}</g>
    <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="7" fill="none" stroke="#262a33"/>
    {''.join(legend)}

    <g clip-path="url(#feedclip)">
      <rect x="30" y="248" width="1140" height="48" rx="10" fill="#0e1016" stroke="#262a33"/>
      <g class="feedmove">{chips_a}{chips_b}</g>
    </g>
    <rect x="30" y="248" width="176" height="48" rx="10" fill="#10121a" stroke="#262a33"/>
    <text x="48" y="277" class="chip" fill="#00f0ff">THREAT FEED</text>
    <text x="150" y="278" class="cvss">&#9656;</text>

    <text x="30" y="312" class="foot">secai ci: <tspan class="{ci_cls}">{html.escape(ci_txt)}</tspan></text>
    <text x="1170" y="312" text-anchor="end" class="foot">updated {d["updated"]} UTC · regenerated nightly by github actions</text>

    <rect class="scan" x="0" y="0" width="1200" height="2" fill="#00f0ff" opacity=".10"/>
    <rect width="1199" height="319" x=".5" y=".5" rx="14" fill="none" stroke="#262a33"/>
  </g>
  <!-- ctf: c2VjYWl7cHJvb2Zfbm90X2NsYWltc30= -->
</svg>
'''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    data = collect()
    print("self-scan data:", json.dumps(data, ensure_ascii=False))
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render(data))
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
