# -*- coding: utf-8 -*-
# One-off patcher: add README cache-bust to refresh_dashboard.py, extend workflow git-add, fix alt text.
import re

p = r"D:/GODMODE/work/profile/tools/refresh_dashboard.py"
s = open(p, encoding="utf-8").read()

anchor = '    print(f"dashboard refreshed:'
assert s.count(anchor) == 1, "print anchor missing"

cachebust = '''    # Cache-bust the local SVG embeds in README so any proxy/camo layer
    # fetches a fresh URL whenever the counters move.
    stamp = f"{merged}-{opened}-{cve_det}"
    r = open("README.md", encoding="utf-8").read()
    r2 = re.sub(r'(src="assets/(?:terminal|self-scan)\\.svg)(\\?v=[\\w-]+)?"',
                r'\\1?v={stamp}"'.format(stamp=stamp), r)
    if r2 != r:
        open("README.md", "w", encoding="utf-8", newline="").write(r2)

'''
s = s.replace(anchor, cachebust + anchor)
open(p, "w", encoding="utf-8", newline="").write(s)
print("refresh_dashboard.py patched")

p2 = r"D:/GODMODE/work/profile/.github/workflows/refresh-dashboard.yml"
w = open(p2, encoding="utf-8").read()
old2 = "git add assets/self-scan.svg assets/terminal.svg"
assert w.count(old2) == 1
w = w.replace(old2, "git add assets/self-scan.svg assets/terminal.svg README.md")
open(p2, "w", encoding="utf-8", newline="").write(w)
print("workflow patched")

p3 = r"D:/GODMODE/work/profile/README.md"
r = open(p3, encoding="utf-8").read()
if "regenerated nightly" in r:
    r = r.replace("regenerated nightly", "auto-refreshed every 30 minutes")
    open(p3, "w", encoding="utf-8", newline="").write(r)
    print("alt text updated")
else:
    print("alt text: no change needed")
