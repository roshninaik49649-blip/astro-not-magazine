# BUILD LOG — ASTRO-NOT / THE 2050 PROJECT

## Visual rework (post first print)

An ink-coverage audit (60 dpi render → per-page non-background pixel fraction)
found 19 of 48 pages visually sparse (<6 % ink) and one factual inconsistency
(p48 credited a closing illustration that did not exist). Full rework applied:

- **7 original SVG illustrations** (cover key image, 5 chapter openers, back
  cover) — hand-written, palette-based, registered in the asset register as
  original works. Cover now carries the mandated Earth-and-cosmos key image
  without any licence exposure; p48's credit line is now true.
- **Magazine components** added to the layout engine: fenced `:::` blocks
  (callout / pull / cards / chips / ladder / stampbox) processed via
  python-markdown `md_in_html`. The evidence hierarchy (p 24) and verification
  ladder (p 15) render as visual ladders; p 27/p 28/p 40 use card grids;
  p 45's placeholders render as stamped case-file slots.
- **Builder hardening**: fenced-component depth guard (unbalanced `:::` now
  fails the build with the offending filename, instead of silently swallowing
  a page — this bug actually bit during the rework and the guard caught it);
  inline-token renderer now handles compound variants (`::est→▲::`,
  `::est/▲::`) that previously leaked as literal text on pp 35/38/40.
- **Post-rework audit**: 0 sparse pages (min ink 6.1 %, mean 10.1 %, was 5.5 %
  mean), no page content touches the 3 mm bleed edge, 48/48 pages, all QA
  checks pass, word count back within 9,000–12,000 after trimming genuine
  redundancy. AN-2050-017 QA relaxed to "required pages present, consistent
  extras allowed" — contents/opener navigation chips now legitimately mention
  the ID.


## Environment decisions

- **Working dir**: dedicated subdirectory `astro-not-magazine/` inside the user's
  repo (repo root holds unrelated projects).
- **pip install blocked** by PEP 668 → project venv `.venv/` created instead;
  documented in README. Installed: matplotlib, weasyprint, pyyaml, segno, markdown.
- **Fonts**: system-installed Noto Sans (SIL OFL 1.1) + DejaVu Sans (permissive).
  DejaVu Sans added as fallback because it carries the confidence-icon glyphs
  (● ◆ ▲ ✦ →) that Noto Sans lacks. Serif fallbacks visible in `pdffonts` come from
  text inside the matplotlib SVG figures, not body copy.

## Layout route (recorded as required)

- Scribus headless (`scribus -g -py`) not installed; headless Scribus scripting is
  fragile and undocumented for CI use → **fell back to HTML/CSS → WeasyPrint**.
- Page numbers are static (from YAML front matter) instead of `@page` margin-box
  counters — this keeps full-bleed dark/light spreads possible with `margin: 0`.
- WeasyPrint 70 quirk found and worked around: `@page { size: … }` passed via the
  `css=` parameter was ignored; inlining CSS in `<style>` works. One section per
  sheet is guaranteed by per-page named pages (`page: pNN`).
- Print page box 216×303 mm (3 mm bleed), digital 210×297 mm. Verified with pdfinfo.

## CMYK / PDF-X

Ghostscript `pdfwrite` conversion attempted (`layout/cmyk_attempt.py`) and its
output kept as `astronot-print-cmyk.pdf`. Honest limitation: this is a colour
re-encoding, **not** a press-ready X-1a with OutputIntent ICC. Print-shop
separation still required before artwork lock.

## QA results (final run)

- 48/48 pages in both editions; page mapping 1:1 verified via pdftotext.
- All fonts embedded (subset) in both editions.
- Word count: ~10,229 body words (target 9–12k).
- Contrast: all pairs ≥ 5.05:1 (WCAG AA pass).
- Mission tests: M01 depth physics, M02 detection+false-alarm, M03 budget model,
  M04 answer key, M05 case key, M06 storage shape — all pass via node.
- Link checker: local mission targets exist; portal URL is an explicit `.example`
  placeholder; internal anchors resolve.

## Open blockers (before artwork lock)

1. Official ASTRO-NOT logo file + brand approval (placeholder in place).
2. Cover photographic key image: licence review (NASA library terms vary) —
   original vector used meanwhile.
3. 11 `[NEEDS VERIFICATION]` facts to resolve (journal DOIs, NIST record, NASA FY
   budget doc, ISRO Gaganyaan page path).
4. Page 45 voices: awaiting real, permissioned submissions.
5. Portal domain (`.example` placeholder) + hosting decision.
6. Print-shop CMYK separations.
