#!/usr/bin/env python3
"""Generate all QR codes as SVG from the single links.yaml register."""
import os
import yaml
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
links = yaml.safe_load(open(os.path.join(HERE, "links.yaml")))["links"]
for l in links:
    path = os.path.join(OUT, f"{l['qr_id']}.svg")
    segno.make(l["url"], error="m").save(path, scale=8, border=2, kind="svg")
    print("  wrote", os.path.basename(path), "->", l["url"][:60])
print("QR codes complete")
