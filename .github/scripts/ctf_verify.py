#!/usr/bin/env python3
"""CTF submission verifier — runs on every `issues` event.

Reads the issue, extracts any secai{...} tokens, hashes them with SHA-256 and
compares against the known answer hashes. Comments a scorecard; when all three
verify, adds the hunter to HALL-OF-FAME.md and closes the issue.

Security notes:
- The plaintext flags are NOT in this repo — only their SHA-256 digests, here.
- User-supplied issue text is only ever hashed and regex-scanned, never eval'd
  or passed to a shell. The hunter name comes from the trusted event payload
  and is validated against the GitHub username charset before it's written.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request

STAGES = [
    ("stage 1 · base64 · the board that scans me",
     "f23dc01e4f20832aaba9ed91f96a71cf85d418930befc2568d57fddc342bcf01"),
    ("stage 2 · hex · the evidence ladder",
     "0d3df49bf50b735cadab7c0f59c214e0d581893f027ecdf016b66179534ace8b"),
    ("stage 3 · rot13 · the house rules",
     "40e4455a767b4063209c316e4426fceb34097be702b36976d08618033780cee0"),
]
HOF = "HALL-OF-FAME.md"


def api(method: str, path: str, data: dict | None = None):
    url = f"https://api.github.com{path}"
    payload = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=payload, method=method, headers={
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "secai-ctf",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main() -> int:
    event = json.load(open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8"))
    repo = os.environ["GITHUB_REPOSITORY"]
    issue = event.get("issue") or {}
    number = issue.get("number")
    title = issue.get("title") or ""
    body = issue.get("body") or ""
    login = (issue.get("user") or {}).get("login", "")
    labels = [lab.get("name") for lab in issue.get("labels", [])]

    if number is None or not title.strip().upper().startswith("CTF"):
        print("not a CTF submission; skipping")
        return 0
    if "ctf-solved" in labels:
        print("already solved; skipping")
        return 0

    tokens = set(re.findall(r"secai\{[^}\s]{1,64}\}", f"{title}\n{body}"))
    got = {hashlib.sha256(t.encode()).hexdigest() for t in tokens}
    results = [(name, h in got) for name, h in STAGES]
    solved = sum(1 for _, ok in results if ok)
    all_ok = solved == len(STAGES)

    lines = [f"**secai // CTF** — `{solved}/{len(STAGES)}` flags verified.", ""]
    lines += [f"- {'✅' if ok else '⬜'} {name}" for name, ok in results]
    if all_ok:
        lines += ["", "🏴 All three verified. Welcome to the Hall of Fame — "
                  "*proof, not claims.*"]
    else:
        lines += ["", f"Keep going. Each flag is `secai{{...}}`, hidden with a "
                  f"different encoding in the SVGs on the profile. "
                  f"Rules: https://github.com/{repo}/blob/HEAD/CTF.md"]
    api("POST", f"/repos/{repo}/issues/{number}/comments",
        {"body": "\n".join(lines)})

    if not all_ok:
        print(f"scored {solved}/{len(STAGES)}")
        return 0

    name = login if re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", login) else "anonymous"
    content = (open(HOF, encoding="utf-8").read() if os.path.exists(HOF)
               else "# Hall of Fame\n\n| # | hunter | date |\n|---|--------|------|\n")
    if f"/{name})" not in content:
        rows = content.count("](https://github.com/")
        date = datetime.date.today().isoformat()
        content = content.rstrip() + "\n" + \
            f"| {rows + 1} | [@{name}](https://github.com/{name}) | {date} |\n"
        open(HOF, "w", encoding="utf-8").write(content)
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "user.email",
                        "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "add", HOF], check=True)
        subprocess.run(["git", "commit", "-m", f"ctf: {name} captured all flags"], check=True)
        subprocess.run(["git", "push"], check=True)

    api("POST", f"/repos/{repo}/issues/{number}/labels", {"labels": ["ctf-solved"]})
    api("PATCH", f"/repos/{repo}/issues/{number}", {"state": "closed"})
    print(f"solved by @{name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
