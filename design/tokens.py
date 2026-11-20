"""Single source of truth for the ASTRO-NOT design system.
All colours, confidence labels and layout metrics are defined once here.
design/tokens.css is generated from this file by scripts in build.py."""
import json
import os

PALETTE = {
    "midnight_navy": "#101B33",
    "deep_blue": "#193F68",
    "icy_cyan": "#83DBF3",
    "paper": "#F4F6F3",
    "solar_accent": "#F3A86C",
}

# Confidence label system: consistent icon + colour for each label.
# Icons are single glyphs so they survive font subsetting in PDFs.
CONFIDENCE = {
    "Established science": {"icon": "●", "colour": "#2E7D4F",
                            "short": "EST"},
    "Active research":     {"icon": "◆", "colour": "#193F68",
                            "short": "ACT"},
    "Plausible projection": {"icon": "▲", "colour": "#B0722A",
                             "short": "PLA"},
    "Fictional scenario":  {"icon": "✦", "colour": "#8A4FA3",
                            "short": "FIC"},
}

LAYOUT = {
    "trim": {"w_mm": 210, "h_mm": 297},
    "bleed_mm": 3,
    "safe_margin_mm": 15,
    "columns": 3,
    "body_pt": 10.5,
    "caption_pt": 8.5,
}

FONTS = {
    "sans": "Noto Sans",          # SIL OFL 1.1, system-installed
    "mono": "DejaVu Sans Mono",   # permissive free licence, system-installed
    "fallback": "DejaVu Sans",    # carries icon glyphs (● ◆ ▲ ✦ →) not in Noto Sans
}

SIMULATED_BANNER = "SIMULATED — synthetic data for illustration only, not real observations"


def css_vars():
    lines = [":root {"]
    for k, v in PALETTE.items():
        lines.append(f"  --{k.replace('_', '-')}: {v};")
    for k, v in CONFIDENCE.items():
        slug = k.lower().replace(" ", "-")
        lines.append(f"  --conf-{slug}: {v['colour']};")
    lines.append(f"  --font-sans: '{FONTS['sans']}', '{FONTS.get('fallback','sans-serif')}', sans-serif;")
    lines.append(f"  --font-mono: '{FONTS['mono']}', monospace;")
    lines.append("}")
    return "\n".join(lines)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "tokens.css"), "w") as fh:
        fh.write(css_vars() + "\n")
    with open(os.path.join(here, "tokens.json"), "w") as fh:
        json.dump({"palette": PALETTE, "confidence": CONFIDENCE,
                   "layout": LAYOUT, "fonts": FONTS}, fh, indent=2)
    print("tokens.css and tokens.json written")
