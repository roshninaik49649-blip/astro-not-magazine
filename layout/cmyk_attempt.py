#!/usr/bin/env python3
"""Try a CMYK/PDF-X Ghostscript conversion of the print PDF; record honestly.
Many WeasyPrint builds embed RGB; Ghostscript's pdfwrite can convert colours but
cannot produce a true X-1a without a valid OutputIntent ICC. We attempt and report."""
import os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(ROOT, "output", "astronot-print.pdf")
dst = os.path.join(ROOT, "output", "astronot-print-cmyk.pdf")
cmd = ["gs", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=pdfwrite",
       "-sColorConversionStrategy=CMYK", "-dProcessColorModel=/DeviceCMYK",
       f"-sOutputFile={dst}", src]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode == 0 and os.path.exists(dst):
    info = subprocess.run(["pdfinfo", dst], capture_output=True, text=True).stdout
    size = [l for l in info.splitlines() if "Page size" in l][0].strip()
    print(f"CMYK attempt: wrote {dst} ({size})")
    print("LIMITATION (record honestly): Ghostscript conversion re-encodes colours but")
    print("does not embed a press-verified OutputIntent/ICC profile. Treat as a")
    print("proofing step only; final CMYK separations must be made by the print shop.")
else:
    print(f"CMYK attempt failed (exit {r.returncode}); print PDF remains RGB.")
    print("LIMITATION: RGB-only output; print shop must handle colour conversion.")
