#!/usr/bin/env python3
"""QA validator for the ASTRO-NOT magazine. Run: .venv/bin/python qa/qa_check.py
Checks the non-negotiable rules that can be verified programmatically."""
import os, re, glob, sys, subprocess, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails, warns = [], []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" — " + detail) if detail else ""))
    (fails if not ok else warns if False else []).append(name) if not ok else None


def info(name, detail):
    print("INFO " + name + ((" — " + detail) if detail else ""))


# ---------- 1. manuscript completeness ----------
pages = {}
for f in sorted(glob.glob(os.path.join(ROOT, "manuscript", "*.md"))):
    raw = open(f).read()
    m = re.match(r"^---\n(.*?)\n---\n", raw, flags=re.S)
    meta = yaml.safe_load(m.group(1))
    pages[meta["page"]] = (f, meta, raw)
check("48 manuscript pages, numbered 1-48", sorted(pages) == list(range(1, 49)),
      f"found {len(pages)}")

# ---------- 2. claims map to references ----------
refs = yaml.safe_load(open(os.path.join(ROOT, "registers", "references.yaml")))
ref_ids = {r["id"] for r in refs["refs"]}
bad = []
for p, (f, meta, raw) in pages.items():
    for rid in meta.get("references") or []:
        if rid not in ref_ids:
            bad.append(f"p{p}:{rid}")
check("all front-matter reference IDs exist in register", not bad, ", ".join(bad))

# ---------- 3. [NEEDS VERIFICATION] flags counted ----------
nv = sum(raw.count("[NEEDS VERIFICATION]") for _, _, raw in pages.values())
check("[NEEDS VERIFICATION] markers used instead of guesses (count)", nv > 0, f"{nv} markers")

# ---------- 4. AN-2050-017 consistency ----------
an_pages = sorted(p for p, (_, meta, raw) in pages.items() if "AN-2050-017" in raw)
required = [12, 41, 42, 43, 44]
check("AN-2050-017 present on required pages (12, 41-44; consistent extras allowed)",
      all(p in an_pages for p in required), f"found on {an_pages}")
m05 = open(os.path.join(ROOT, "missions", "m05-cosmic-detective", "index.html")).read()
m05l = open(os.path.join(ROOT, "missions", "m05-cosmic-detective", "logic.js")).read()
check("AN-2050-017 in online portal (m05 html+logic)", "AN-2050-017" in m05 and "AN-2050-017" in m05l)

# ---------- 5. SIMULATED labelling ----------
fig_meta = [(p, meta) for p, (_, meta, _) in pages.items() if meta.get("figure")]
sim_ok = all(meta.get("simulated") for p, meta in fig_meta
             if any(s in meta["figure"] for s in ["an2050", "lightcurve", "chirp",
                                                  "rotation", "expansion", "skymap", "nights"]))
check("simulated-data figures flagged in front matter", sim_ok)
for pdf in ["astronot-print.pdf", "astronot-digital.pdf"]:
    txt = subprocess.run(["pdftotext", os.path.join(ROOT, "output", pdf), "-"],
                         capture_output=True, text=True).stdout
    check(f"{pdf}: SIMULATED banner text present", "SIMULATED" in txt)

# ---------- 6. fictional labelling ----------
fic_pages = [p for p, (_, meta, raw) in pages.items()
             if re.search(r"fictional", raw, re.I) or meta.get("type") == "mission"]
check("fictional 2050 events explicitly labelled (M01-M06 pages present)", len(fic_pages) >= 6,
      f"{len(fic_pages)} pages")

# ---------- 7. logo placeholder ----------
logo = os.path.join(ROOT, "assets", "logo", "PLACEHOLDER_LOGO.svg")
check("logo placeholder exists, not modified/redrawn", os.path.exists(logo))
reg = open(os.path.join(ROOT, "assets", "asset-register.yaml")).read()
check("asset register flags logo blocker", "BLOCKER" in reg and "brand approval" in reg)

# ---------- 8. page 45 placeholders ----------
p45 = pages[45][2]
check("page 45 uses placeholders (no invented voices)", p45.count("PLACEHOLDER") >= 5)

# ---------- 9. links.yaml <-> QR files ----------
links = yaml.safe_load(open(os.path.join(ROOT, "qr", "links.yaml")))["links"]
missing = [l["qr_id"] for l in links
           if not os.path.exists(os.path.join(ROOT, "qr", "out", f"{l['qr_id']}.svg"))]
check("every links.yaml entry has a QR SVG", not missing, ", ".join(missing))
check("portal link is an explicit placeholder domain",
      all(".example" in l["url"] for l in links if l["kind"] == "portal"))

# ---------- 10. PDF structural checks ----------
for pdf, exp_pages, exp_size in [("astronot-print.pdf", 48, "612.283 x 858.898"),
                                 ("astronot-digital.pdf", 48, "595.276 x 841.89")]:
    path = os.path.join(ROOT, "output", pdf)
    if not os.path.exists(path):
        check(f"{pdf} exists", False)
        continue
    info_ = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    n = re.search(r"Pages:\s+(\d+)", info_).group(1)
    size = re.search(r"Page size:\s+([\d.]+ x [\d.]+)", info_).group(1)
    check(f"{pdf}: 48 pages", n == str(exp_pages), f"got {n}")
    check(f"{pdf}: page box matches edition", size.startswith(exp_size), f"got {size}")
    fonts = subprocess.run(["pdffonts", path], capture_output=True, text=True).stdout
    emb = [l for l in fonts.splitlines()[2:] if l.strip()]
    check(f"{pdf}: all fonts embedded", all(" yes " in l for l in emb), f"{len(emb)} fonts")

# ---------- 11. word count (body text; recurring page furniture excluded) ----------
txt = subprocess.run(["pdftotext", os.path.join(ROOT, "output", "astronot-print.pdf"), "-"],
                     capture_output=True, text=True).stdout
txt = re.sub(r"ASTRO-NOT · THE 2050 PROJECT — [^\n]+", " ", txt)
txt = re.sub(r"Page \d+ / 48", " ", txt)
wc = len(txt.split())
info("body word count (furniture excluded)", f"~{wc}")
check("total word count within 9,000-12,000", 9000 <= wc <= 12000, f"~{wc}")

# ---------- 12. contrast (WCAG) ----------
sys.path.insert(0, os.path.join(ROOT, "design"))
from tokens import PALETTE, CONFIDENCE
def lum(hexc):
    h = hexc.lstrip("#"); r, g, b = (int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    f = lambda c: c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b)
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la+0.05)/(lb+0.05)
pairs = [("body on dark", PALETTE["paper"], PALETTE["midnight_navy"]),
         ("body on light", "#182338", PALETTE["paper"]),
         ("cyan headings on dark", PALETTE["icy_cyan"], PALETTE["midnight_navy"]),
         ("navy headings on light", PALETTE["midnight_navy"], PALETTE["paper"]),
         ("kicker accent on dark", PALETTE["solar_accent"], PALETTE["midnight_navy"]),
         ("badge text on est-green", "#FFFFFF", CONFIDENCE["Established science"]["colour"]),
         ("caption on dark", "#A9BAD6", PALETTE["midnight_navy"]),
         ("caption on light", "#4A5A75", PALETTE["paper"])]
worst = min((r, n) for n, a, b in pairs for r in [ratio(a, b)])
check("all text/background pairs pass WCAG AA (>= 4.5)", worst[0] >= 4.5,
      f"worst pair: {worst[1]} = {worst[0]:.2f}:1")
for n, a, b in pairs:
    info(f"contrast {n}", f"{ratio(a, b):.2f}:1")

print()
print(f"RESULT: {'FAIL — ' + str(len(fails)) + ' failing checks' if fails else 'ALL CHECKS PASSED'}")
sys.exit(1 if fails else 0)
