"""Regenerate CONTRIBUTIONS.md from the GitHub search API.

Lists every pull request the user opened in repositories they do not own,
grouped by repository, newest first. The header above "Jump to:" is kept as is.
Run by .github/workflows/refresh-dashboard.yml (GH_TOKEN = GITHUB_TOKEN).
"""
import json
import os
import re
import urllib.request
from collections import OrderedDict

USER = "maulanawirawan"
FILE = "CONTRIBUTIONS.md"
ORDER = [
    "projectdiscovery/nuclei-templates",
    "D4Vinci/Scrapling",
    "github/advisory-database",
    "swisskyrepo/PayloadsAllTheThings",
    "OWASP/CheatSheetSeries",
    "danielmiessler/SecLists",
]
NAMES = {
    "projectdiscovery/nuclei-templates": "nuclei-templates",
    "D4Vinci/Scrapling": "Scrapling",
    "github/advisory-database": "advisory-database",
    "swisskyrepo/PayloadsAllTheThings": "PayloadsAllTheThings",
    "OWASP/CheatSheetSeries": "OWASP CheatSheetSeries",
    "danielmiessler/SecLists": "SecLists",
}


def api(path):
    req = urllib.request.Request(
        "https://api.github.com/" + path,
        headers={
            "Authorization": "Bearer " + os.environ["GH_TOKEN"],
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_prs():
    items, page = [], 1
    while True:
        data = api(
            f"search/issues?q=is:pr+author:{USER}+-user:{USER}"
            f"&per_page=100&page={page}&sort=created&order=desc"
        )
        items += data["items"]
        if len(items) >= data["total_count"] or not data["items"] or page >= 10:
            return items
        page += 1


def name_of(repo):
    return NAMES.get(repo, repo.split("/")[1])


def anchor(text):
    return re.sub(r"[^a-z0-9 -]", "", text.lower()).replace(" ", "-")


def clean(title):
    title = re.sub(r"^(Add(ed)?|feat:?)\s+", "", title.strip(), flags=re.I)
    return title.replace(".yaml", "").replace("|", "\\|")


def render(header, items):
    groups = OrderedDict()
    for it in items:
        groups.setdefault(it["repository_url"].split("repos/")[1], []).append(it)
    repos = [r for r in ORDER if r in groups] + sorted(r for r in groups if r not in ORDER)

    out = [header.rstrip() + "\n"]
    out.append("Jump to: " + " · ".join(
        f"[{name_of(r)}](#{anchor(name_of(r))}) ({len(groups[r])})" for r in repos) + "\n")
    out.append("[← back to profile](README.md)\n")
    for repo in repos:
        prs = sorted(groups[repo], key=lambda i: -i["number"])
        merged = sum(1 for i in prs if (i.get("pull_request") or {}).get("merged_at"))
        opened = sum(1 for i in prs if i["state"] == "open")
        out.append(
            f"## {name_of(repo)}\n\n<sub>[{repo}](https://github.com/{repo}) · "
            f"{len(prs)} PRs · {merged} merged · {opened} open</sub>\n\n| PR | Status |\n|---|---|"
        )
        for i in prs:
            out.append(
                f"| [#{i['number']}]({i['html_url']}) · {clean(i['title'])} | "
                f"![](https://img.shields.io/github/pulls/detail/state/{repo}/{i['number']}"
                f"?style=flat-square&label=) |"
            )
        out.append("")
    out.append("<sub>Table regenerated automatically from the GitHub API. "
               "Badges above are live counts.</sub>\n\n[← back to profile](README.md)\n")
    return "\n".join(out)


def main():
    with open(FILE, encoding="utf-8") as fh:
        old = fh.read()
    header = old.split("Jump to:")[0]
    new = render(header, fetch_prs())
    if new != old:
        with open(FILE, "w", encoding="utf-8") as fh:
            fh.write(new)
        print("CONTRIBUTIONS.md updated")
    else:
        print("CONTRIBUTIONS.md unchanged")


if __name__ == "__main__":
    main()
