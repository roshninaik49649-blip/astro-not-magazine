#!/usr/bin/env python3
"""ASTRO-NOT one-command rebuild. Order: tokens -> figures -> QR -> tests ->
layout (print+digital) -> CMYK attempt -> QA. Exit code reflects QA result."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(ROOT, ".venv", "bin", "python")
STEPS = [
    ("design tokens", [PY, os.path.join(ROOT, "design", "tokens.py")]),
    ("figures", [PY, os.path.join(ROOT, "figures", "make_figures.py")]),
    ("QR codes", [PY, os.path.join(ROOT, "qr", "make_qr.py")]),
    ("mission tests", [PY, os.path.join(ROOT, "missions", "tests", "test_missions.py")]),
    ("layout + PDFs", [PY, os.path.join(ROOT, "layout", "build_layout.py")]),
    ("CMYK attempt", [PY, os.path.join(ROOT, "layout", "cmyk_attempt.py")]),
    ("QA", [PY, os.path.join(ROOT, "qa", "qa_check.py")]),
]
for name, cmd in STEPS:
    print(f"\n=== {name} ===")
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        print(f"STEP FAILED: {name} (exit {r.returncode})")
        sys.exit(r.returncode)
print("\nREBUILD COMPLETE — output/astronot-print.pdf, output/astronot-digital.pdf")
