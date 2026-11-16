"""Regenerate the profile dashboard numbers from live GitHub search API.

Updates assets/self-scan.svg (big stat cards) and assets/terminal.svg
(upstream line). Idempotent: running twice changes nothing unless the
counts actually moved. Designed for the nightly "Refresh dashboard"
workflow; GH_TOKEN (GITHUB_TOKEN) raises the rate limit.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HDR = {"User-Agent": "profile-dashboard", "Accept": "application/vnd.github+json"}
if os.environ.get("GH_TOKEN"):
    HDR["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]

SEARCH = "https://api.github.com/search/issues?q="
AUTHOR = "maulanawirawan"


def api(url):
    req = urllib.request.Request(url, headers=HDR)
    for _ in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                print("  rate-limited, sleeping 20s")
                time.sleep(20)
                continue
            raise
        except Exception as e:
            print("  retry:", e)
            time.sleep(5)
    raise RuntimeError("API failed: " + url)


def count(query):
    return api(SEARCH + urllib.parse.quote(query))["total_count"]


def main():
    merged = count(f"author:{AUTHOR} type:pr is:merged -user:{AUTHOR}")
    opened = count(f"author:{AUTHOR} type:pr is:open -user:{AUTHOR}")
    nuc = api(SEARCH + urllib.parse.quote(
        f"author:{AUTHOR} type:pr is:merged repo:projectdiscovery/nuclei-templates"))
    cve_det = sum(1 for it in nuc.get("items", []) if it["title"].startswith("Add CVE-"))

    s = open("assets/self-scan.svg", encoding="utf-8").read()
    s = re.sub(r'(fill="#39ff14">)\d+(</text>)', rf"\g<1>{merged}\g<2>", s, count=1)
    s = re.sub(r'(fill="#00f0ff">)\d+(</text>)', rf"\g<1>{opened}\g<2>", s, count=1)
    s = re.sub(r'(fill="#8A2BE2">)\d+(</text>)', rf"\g<1>{cve_det}\g<2>", s, count=1)
    open("assets/self-scan.svg", "w", encoding="utf-8", newline="").write(s)

    t = open("assets/terminal.svg", encoding="utf-8").read()
    t = re.sub(r"\d+ merged, \d+ open \u00b7 nuclei-templates",
               f"{merged} merged, {opened} open \u00b7 nuclei-templates", t)
    open("assets/terminal.svg", "w", encoding="utf-8", newline="").write(t)

    # Cache-bust the local SVG embeds in README so any proxy/camo layer
    # fetches a fresh URL whenever the counters move.
    stamp = f"{merged}-{opened}-{cve_det}"
    r = open("README.md", encoding="utf-8").read()
    r2 = re.sub(r'(src="assets/(?:terminal|self-scan)\.svg)(\?v=[\w-]+)?"',
                r'\1?v={stamp}"'.format(stamp=stamp), r)
    if r2 != r:
        open("README.md", "w", encoding="utf-8", newline="").write(r2)

    print(f"dashboard refreshed: {merged} merged, {opened} open, {cve_det} cve detections")


if __name__ == "__main__":
    main()
