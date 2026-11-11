#!/usr/bin/env python3
"""CTF submission verifier. Runs on every `issues` event.

Hunters don't post flags, they post proofs: for each flag,
sha256("<github-username>:<flag>") with the username in lowercase. The flag
never shows up in a public issue, and a proof only works for the account that
posted it, so copying someone else's submission gets you nothing.

The three flags sit in the profile's own SVGs, encoded as base64, hex and
rot13 (that's the puzzle). This script decodes them from those files and
checks each one against its published SHA-256 before trusting it. If an SVG
changes and a flag no longer matches, the run fails closed.

Security notes:
- Issue text is only regex-scanned for hex digests. It is never eval'd or
  handed to a shell.
- The hunter name comes from the event payload and must match GitHub's
  username charset before it's written anywhere.
- The repo owner can test the bot without landing in the Hall of Fame.
"""
from __future__ import annotations

import base64
import codecs
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request

HOF = "HALL-OF-FAME.md"
LOGIN_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})")
PROOF_RE = re.compile(r"\b[0-9a-fA-F]{64}\b")

# label, file, pattern for the encoded flag, decoder, sha256 of the decoded flag
STAGES = [
    ("stage 1 · base64 · the board that scans me", "assets/self-scan.svg",
     r"<!--\s*ctf:\s*([A-Za-z0-9+/=]+)\s*-->",
     lambda s: base64.b64decode(s).decode("utf-8"),
     "f23dc01e4f20832aaba9ed91f96a71cf85d418930befc2568d57fddc342bcf01"),
    ("stage 2 · hex · the evidence ladder", "assets/evidence-ladder.svg",
     r"\(hex\):\s*([0-9a-fA-F]+)",
     lambda s: bytes.fromhex(s).decode("utf-8"),
     "0d3df49bf50b735cadab7c0f59c214e0d581893f027ecdf016b66179534ace8b"),
    ("stage 3 · rot13 · the house rules", "assets/terminal.svg",
     r"\(rot13\):\s*([a-z]+\{[^}\s]+\})",
     lambda s: codecs.decode(s, "rot_13"),
     "40e4455a767b4063209c316e4426fceb34097be702b36976d08618033780cee0"),
]


def load_flags() -> list[str]:
    flags = []
    for label, path, pattern, decode, digest in STAGES:
        with open(path, encoding="utf-8") as fh:
            m = re.search(pattern, fh.read())
        if not m:
            raise SystemExit(f"{label}: encoded flag not found in {path}")
        flag = decode(m.group(1))
        if hashlib.sha256(flag.encode("utf-8")).hexdigest() != digest:
            raise SystemExit(f"{label}: decoded flag doesn't match its published hash")
        flags.append(flag)
    return flags


def proof(login: str, flag: str) -> str:
    return hashlib.sha256(f"{login.lower()}:{flag}".encode("utf-8")).hexdigest()


def api(method: str, path: str, data: dict | None = None) -> bytes:
    payload = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(
        f"https://api.github.com{path}", data=payload, method=method, headers={
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "secai-ctf",
            "X-GitHub-Api-Version": "2022-11-28",
        })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], check=check)


def add_to_hall_of_fame(name: str, branch: str) -> None:
    if os.path.exists(HOF):
        with open(HOF, encoding="utf-8") as fh:
            content = fh.read()
    else:
        content = "# Hall of Fame\n\n| # | hunter | date |\n|---|--------|------|\n"
    if f"](https://github.com/{name})" in content:
        return
    rank = content.count("](https://github.com/") + 1
    today = datetime.date.today().isoformat()
    content = (content.rstrip("\n")
               + f"\n| {rank} | [@{name}](https://github.com/{name}) | {today} |\n")
    with open(HOF, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    git("add", HOF)
    git("commit", "-m", f"ctf: {name} captured all three flags")
    for _ in range(3):
        if git("push", "origin", f"HEAD:{branch}", check=False).returncode == 0:
            return
        git("pull", "--rebase", "origin", branch)
    raise SystemExit("could not push the Hall of Fame update")


def main() -> int:
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as fh:
        event = json.load(fh)
    repo = os.environ["GITHUB_REPOSITORY"]
    owner = repo.split("/", 1)[0]
    branch = (event.get("repository") or {}).get("default_branch") or "main"
    issue = event.get("issue") or {}
    number = issue.get("number")
    title = issue.get("title") or ""
    body = issue.get("body") or ""
    login = (issue.get("user") or {}).get("login") or ""
    labels = {lab.get("name") for lab in issue.get("labels") or []}

    if number is None or not title.strip().upper().startswith("CTF"):
        print("not a CTF submission; skipping")
        return 0
    if issue.get("state") == "closed" or "ctf-solved" in labels:
        print("issue already closed or solved; skipping")
        return 0
    if not LOGIN_RE.fullmatch(login):
        print("unexpected login format; skipping")
        return 0

    flags = load_flags()
    text = f"{title}\n{body}"
    submitted = {h.lower() for h in PROOF_RE.findall(text)}
    results = [(stage[0], proof(login, flag) in submitted)
               for stage, flag in zip(STAGES, flags)]
    solved = sum(ok for _, ok in results)
    all_ok = solved == len(STAGES)
    is_owner = login.lower() == owner.lower()
    leaked = any(flag in text for flag in flags)

    lines = [f"**secai // CTF** · `{solved}/{len(STAGES)}` proofs verified for @{login}.", ""]
    lines += [f"- {'✅' if ok else '⬜'} {label}" for label, ok in results]
    if leaked:
        lines += ["", "⚠️ This issue contains a raw `secai{...}` flag, which spoils the "
                      "game for everyone else. Please edit it out and keep only the proofs."]
    if all_ok and is_owner:
        lines += ["", "Owner test passed. The verifier works, and you stay off the Hall of Fame."]
    elif all_ok:
        lines += ["", "🏴 All three proofs check out. You're in the "
                      f"[Hall of Fame](https://github.com/{repo}/blob/HEAD/{HOF}). "
                      "*Proof, not claims.*"]
    else:
        lines += ["", "Keep going. For each flag, post `sha256(\"<your-username>:<flag>\")` "
                      "with your username in lowercase. "
                      f"Rules: https://github.com/{repo}/blob/HEAD/CTF.md"]
    api("POST", f"/repos/{repo}/issues/{number}/comments", {"body": "\n".join(lines)})

    if not all_ok:
        print(f"@{login}: {solved}/{len(STAGES)}")
        return 0
    if not is_owner:
        add_to_hall_of_fame(login, branch)
        api("POST", f"/repos/{repo}/issues/{number}/labels", {"labels": ["ctf-solved"]})
    api("PATCH", f"/repos/{repo}/issues/{number}", {"state": "closed"})
    print(f"@{login}: solved{' (owner test)' if is_owner else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
