# ASTRO-NOT — THE 2050 PROJECT

A 48-page full-colour A4 science magazine arguing that **the Universe will not change
drastically by 2050** — while our instruments, discoveries and presence in space may
transform our understanding of it. Audience: ages ~14–30.

## One-command rebuild

```bash
.venv/bin/python build.py          # full pipeline, ends with QA gate
# or: make all
```

First-time setup (PEP 668 blocked system pip, so a venv is used):

```bash
python3 -m venv .venv && .venv/bin/pip install matplotlib weasyprint pyyaml segno markdown
```

## Repo structure

```
manuscript/        48 page files (Markdown + YAML front matter: page, headline,
                   section, type, dark, confidence, references, figure, alt, obs_id)
design/            tokens.py — single source of truth: palette, confidence labels
                   (icon+colour), layout metrics, fonts; generates tokens.css/json
registers/         references.yaml — every claim maps to R01-R22, verification status
assets/            logo placeholder (never redraw it), asset register, illustrations
figures/           make_figures.py — seeded matplotlib, SVG out; SIMULATED banners,
                   axis units and uncertainties on every simulated plot
qr/                links.yaml (single link source) -> segno SVGs
missions/          6 interactive browser activities (HTML/CSS/vanilla JS, no external
                   deps, keyboard-friendly); logic.js files are node-testable
layout/            build_layout.py: Markdown -> HTML -> WeasyPrint; style.css +
                   print/digital overrides; cmyk_attempt.py (Ghostscript)
qa/                qa_check.py (rule validator), link_checker.py
output/            astronot-print.pdf (216x303mm bleed box), astronot-digital.pdf
                   (A4, tagged PDF/UA-1 attempt), HTML intermediates, CMYK attempt
build.py           orchestrator (tokens -> figures -> QR -> tests -> layout -> QA)
```

## Editions

- **Print**: A4 trim 210×297 with 3 mm bleed (page box 216×303), 15 mm safe margins,
  three-column flexible grid, embedded open-licensed fonts (Noto Sans SIL OFL,
  DejaVu — see asset register).
- **Digital**: A4, tagged PDF (PDF/UA-1 attempt), alt text on every figure,
  internal links from page references to page anchors, static "Page NN / 48" markers.

## Editorial rules built into the pipeline

1. No fabricated evidence — simulated plots carry visible **SIMULATED** banners.
2. No invented contributors — page 45 is explicitly placeholder until permissioned.
3. Logo untouched placeholder; brand approval flagged as a blocker in the register.
4. No image embedded without a licence entry in `assets/asset-register.yaml`.
5. Every claim maps to `registers/references.yaml`; unverifiable facts are written
   `[NEEDS VERIFICATION]` (11 markers; QA counts them).
6. Fictional events (M01–M06 cases, lunar-base model) labelled ✦ FICTIONAL SCENARIO.
7. Observation ID **AN-2050-017** consistent across pp 12, 41–44 and mission M05
   (QA enforces the exact page list).
8. Indian space science split into verified (ISRO official pages) vs ambitions.

## Confidence labels

● Established science · ◆ Active research · ▲ Plausible projection · ✦ Fictional
scenario — colours and icons defined once in `design/tokens.py`; WCAG AA contrast
verified automatically (worst pair 5.05:1).

## Known limitations (honest list)

- Scribus headless unavailable → **WeasyPrint HTML/CSS route** (decision in BUILD_LOG.md).
- Ghostscript CMYK attempt is a proofing step only; no press OutputIntent embedded.
- Cover key image and photographic openers are original vector placeholders; any
  real NASA/ESA/ESO image needs individual licence review before download.
- Fonts are system-installed Noto Sans/DejaVu; OFL licence text to ship with bundle.
