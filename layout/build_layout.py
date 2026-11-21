#!/usr/bin/env python3
"""Layout engine: manuscript/*.md -> HTML -> WeasyPrint PDF (print + digital).

Architecture (v3, "magazine look"):
- tokens.css (generated from design/tokens.py) is inlined FIRST — all colours
  resolve from the single source of truth. (v2 silently dropped it: undefined
  custom properties rendered dark pages white. Never again.)
- Page architecture by type: full-bleed hero art on covers + openers, display
  chapter type, masthead on the front cover, justified/hyphenated multi-column
  article bodies with standfirst + drop cap, two-column mission briefings,
  dotted-leader contents rows.
- Page numbers are static (from YAML front matter); one section per sheet is
  guaranteed by per-page named pages.
"""
import os, re, glob, yaml, markdown
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "output")
os.makedirs(OUT, exist_ok=True)

TOK = {"est": ("Established science", "●"), "act": ("Active research", "◆"),
       "pla": ("Plausible projection", "▲"), "fic": ("Fictional scenario", "✦")}

MD = markdown.Markdown(extensions=["tables", "attr_list", "md_in_html"], output_format="html5")

# fenced magazine components:  :::name Optional Title  ...  :::
COMPONENTS = {"pull": "pull", "callout": "callout", "cards": "cards", "chip": "chips",
              "ladder": "ladder", "stamp": "stampbox"}


def fenced(text):
    out = []
    depth = 0
    for line in text.split("\n"):
        mc = re.match(r"^:::chip (.+)$", line)
        if mc:
            out.append(f'<span class="chip">{mc.group(1)}</span>')
            continue
        mt = re.match(r"^:::toc (.+?) \| (.+)$", line)
        if mt:
            out.append(f'<div class="tocrow"><span class="tocname">{mt.group(1)}</span>'
                       f'<span class="tocfill"></span><span class="tocpage">{mt.group(2)}</span></div>')
            continue
        m = re.match(r"^::: *(\w+)(?: +(.+))?$", line)
        if m:
            name, title = m.group(1), m.group(2)
            cls = COMPONENTS.get(name, name)
            out.append(f'<div class="{cls}" markdown="1">')
            if title:
                out.append(f'<p class="boxtitle">{title}</p>')
            depth += 1
            continue
        if line.strip() == ":::":
            out.append("</div>")
            depth -= 1
            if depth < 0:
                raise ValueError("fenced component closed more times than opened")
            continue
        out.append(line)
    if depth != 0:
        raise ValueError(f"fenced components left open (depth {depth}) — missing ':::' closer")
    return "\n".join(out)


def inline_toks(text):
    def sub(m):
        key = m.group(1)
        if key in TOK:
            label, icon = TOK[key]
            return f'<span class="tok-{key}" title="{label}">{icon} {label}</span>'
        return m.group(0)
    text = re.sub(r"::(\w+)::", sub, text)

    def compound(m):
        key, sep = m.group(1), m.group(2)
        if key not in TOK:
            return m.group(0)
        lab, icon = TOK[key]
        return (f'<span class="tok-{key}" title="{lab}">{icon} {lab}</span>{sep}'
                f'<span class="tok-pla" title="Plausible projection">▲ Plausible projection</span>')
    text = re.sub(r"::(est|act|pla|fic)(→|/)▲::", compound, text)
    text = text.replace("[NEEDS VERIFICATION]", '<span class="nv">[NEEDS VERIFICATION]</span>')
    return text


def internal_links(html, digital):
    if not digital:
        return html
    def sub(m):
        n = int(m.group(2))
        if 1 <= n <= 48:
            return f'{m.group(1)}<a href="#page-{n}">p {m.group(2)}</a>'
        return m.group(0)
    return re.sub(r"(pp? )(\d{1,2})(?=[^\d/])", sub, html)


def split_title(body_html):
    """Split at the first </h2>: returns (title_html, rest_html)."""
    parts = body_html.split("</h2>", 1)
    if len(parts) == 2:
        return parts[0] + "</h2>", parts[1]
    return "", body_html


def page_html(meta, body_html, edition):
    page_no = int(meta["page"])
    dark = "dark" if meta.get("dark") else "light"
    ptype = meta.get("type", "article")
    kicker = meta.get("section", "")

    # --- confidence badges ---
    badges = ""
    class_by_label = {v[0]: k for k, v in TOK.items()}
    for b in meta.get("confidence", []):
        key = class_by_label.get(b)
        if key:
            label, icon = TOK[key]
            badges += f'<span class="conf conf-{key}">{icon} {label}</span>'
    badges = f'<div class="badges">{badges}</div>' if badges else ""

    # --- QR (mission pages: placed inside the briefing layout) ---
    qr_html = ""
    if meta.get("qr"):
        qr_path = os.path.join(ROOT, "qr", "out", f"{meta['qr']}.svg")
        if os.path.exists(qr_path):
            qr_html = (f'<div class="qrbox static"><img src="{qr_path}" alt="QR code linking to '
                       f'{meta["qr"]} destination; see qr/links.yaml"/><p>{meta["qr"]} · scan or open '
                       f'the missions folder</p></div>')

    # --- figure ---
    fig_html = ""
    if meta.get("figure"):
        fig_path = os.path.join(ROOT, meta["figure"])
        sim = ""
        if meta.get("simulated"):
            sim = ('<div class="sim-banner">SIMULATED — synthetic data for illustration only, '
                   'not real observations. Axes carry units; bars show 1σ uncertainty.</div>')
        alt = meta.get("figure_alt", "Figure")
        fig_html = (f'<figure class="wide"><img src="{fig_path}" alt="{alt}"/>{sim}'
                    f'<figcaption>{alt} — generated figure; register: assets/asset-register.yaml</figcaption></figure>')

    # --- hero artwork (full-bleed) ---
    hero = ""
    if meta.get("art"):
        art_path = os.path.join(ROOT, meta["art"])
        if os.path.exists(art_path):
            alt = meta.get("art_alt", "Original illustration")
            hero = (f'<figure class="hero"><img src="{art_path}" alt="{alt}"/>'
                    f'<figcaption>{alt} — original artwork; assets/asset-register.yaml</figcaption></figure>')

    kicker_line = f'<p class="kicker">{kicker}</p>' if ptype not in ("cover", "opener") else ""
    mission_tag = '<span class="mission-tag">INTERACTIVE MISSION</span>' if ptype == "mission" else ""

    # --- assemble body per page type ---
    if ptype == "cover" and page_no == 1:
        # masthead + hero + cover text (masthead h1/h2 from markdown are stripped)
        body_html = re.sub(r"^\s*<h1>.*?</h1>\s*<h2>.*?</h2>", "", body_html, count=1, flags=re.S)
        body_html = re.sub(r"<p>ASTRO-NOT logo placeholder.*?</p>", "", body_html, flags=re.S)
        logo = os.path.join(ROOT, "assets", "logo", "PLACEHOLDER_LOGO.svg")
        masthead = (f'<div class="masthead"><img src="{logo}" alt="ASTRO-NOT logo PLACEHOLDER — '
                    f'official artwork and brand approval required before artwork lock"/>'
                    f'<div class="mast-words"><span class="mast-name">ASTRO-NOT</span>'
                    f'<span class="mast-sub">THE 2050 PROJECT · ISSUE 01 · NOVEMBER 2026</span>'
                    f'</div></div>')
        inner = masthead + hero + f'<div class="coverflow">{body_html}</div>'
    elif ptype == "cover":
        inner = hero + f'<div class="coverflow">{body_html}</div>'
    elif ptype == "opener":
        title, rest = split_title(body_html)
        inner = hero + badges + title + f'<div class="cols2">{rest}</div>'
    elif ptype in ("article", "reference"):
        title, rest = split_title(body_html)
        cols = 2 if ("<table" in rest or ptype == "reference") else 3
        inner = kicker_line + badges + f'<div class="pagebody">{title}{fig_html}<div class="cols{cols}">{rest}</div></div>'
    elif ptype == "mission":
        title, rest = split_title(body_html)
        inner = (kicker_line + mission_tag + badges +
                f'<div class="pagebody">{title}'
                f'<div class="mission-layout"><div class="mission-text">{rest}</div>{qr_html}</div></div>')
    else:  # infographic
        inner = kicker_line + badges + f'<div class="pagebody">{fig_html}{body_html}</div>'

    inner = internal_links(inner, edition == "digital")
    footer = (f'<footer class="pageline"><span class="wordmark">ASTRO-NOT · THE 2050 PROJECT</span>'
              f'<span class="sect">{kicker}</span>'
              f'<span class="pageno">Page {page_no:02d} / 48</span></footer>')
    return (f'<section class="page {dark} type-{ptype}" id="page-{page_no}" '
            f'data-confidence="{",".join(meta.get("confidence", []))}">'
            f'<div class="body">{inner}</div>{footer}</section>')


def build(edition):
    sections = []
    for md_file in sorted(glob.glob(os.path.join(ROOT, "manuscript", "*.md"))):
        raw = open(md_file).read()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, flags=re.S)
        meta = yaml.safe_load(m.group(1))
        try:
            body = fenced(m.group(2))
        except ValueError as e:
            raise ValueError(f"{md_file}: {e}")
        MD.reset()
        html = MD.convert(body)
        html = inline_toks(html)
        if meta.get("simulated") and not meta.get("figure"):
            html = ('<div class="sim-banner">SIMULATED — synthetic data for illustration only, '
                    'not real observations.</div>') + html
        sections.append(page_html(meta, html, edition))
    title = "ASTRO-NOT — THE 2050 PROJECT"
    css_files = [os.path.join(ROOT, "design", "tokens.css"),
                 os.path.join(HERE, "style.css"),
                 os.path.join(HERE, "style-digital.css" if edition == "digital" else "style-print.css")]
    named = "".join(f"section#page-{n} {{ page: p{n:02d}; }}" for n in range(1, 49))
    css_all = "".join(open(f).read() for f in css_files) + named
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<title>{title}</title><style>{css_all}</style></head><body>{"".join(sections)}</body></html>"""
    variant = {"pdf_variant": "pdf/ua-1"} if edition == "digital" else {}
    out_pdf = os.path.join(OUT, f"astronot-{edition}.pdf")
    HTML(string=doc, base_url=ROOT).write_pdf(out_pdf, **variant)
    open(os.path.join(OUT, f"astronot-{edition}.html"), "w").write(doc)
    print(f"  built {out_pdf}")


if __name__ == "__main__":
    print("layout: print edition")
    build("print")
    print("layout: digital edition")
    build("digital")
