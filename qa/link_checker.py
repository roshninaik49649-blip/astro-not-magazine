#!/usr/bin/env python3
"""Link checker: validates the links register (no invented URLs; placeholder
domains flagged) and internal anchors in the digital HTML."""
import os, re, sys, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
links = yaml.safe_load(open(os.path.join(ROOT, "qr", "links.yaml")))["links"]
fails = []
for l in links:
    url = l["url"]
    if l["kind"] == "local":
        path = os.path.join(ROOT, url)
        if not os.path.exists(path):
            fails.append(f"{l['qr_id']}: missing local target {url}")
        else:
            print(f"PASS {l['qr_id']}: local target exists -> {url}")
    else:
        if ".example/" in url:
            print(f"PASS {l['qr_id']}: portal placeholder domain (no invented URL): {url}")
        else:
            fails.append(f"{l['qr_id']}: non-placeholder portal URL needs licence/brand check")
html = open(os.path.join(ROOT, "output", "astronot-digital.html")).read()
anchors = set(re.findall(r'id="page-(\d+)"', html))
hrefs = set(re.findall(r'href="#page-(\d+)"', html))
missing = hrefs - anchors
fails += missing and [f"dangling anchor page-{m}" for m in missing] or []
print(f"PASS internal anchors: {len(hrefs)} hrefs, all resolve" if not missing else f"FAIL anchors: {missing}")
if fails:
    print("FAILURES:", fails); sys.exit(1)
print("Link checks passed.")
