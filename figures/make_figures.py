#!/usr/bin/env python3
"""ASTRO-NOT figure generator. Seeded RNG => reproducible runs.
Every simulated dataset carries a visible SIMULATED banner, axis labels,
units and (where relevant) uncertainty bands. Output: SVG in figures/out/."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "design"))
from tokens import PALETTE, SIMULATED_BANNER  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({
    "font.family": "Noto Sans",
    "font.size": 9,
    "axes.edgecolor": PALETTE["deep_blue"],
    "axes.labelcolor": PALETTE["midnight_navy"],
    "xtick.color": PALETTE["deep_blue"],
    "ytick.color": PALETTE["deep_blue"],
    "axes.grid": True, "grid.color": "#D8DEE9", "grid.linewidth": 0.5,
    "figure.dpi": 96, "axes.unicode_minus": False,
})
C = PALETTE
SIM_STYLE = dict(fontsize=6.5, color="#8A1F1F", fontweight="bold", alpha=0.95)


def save(fig, name, simulated=True):
    if simulated:
        fig.text(0.01, 0.975, SIMULATED_BANNER, va="top", ha="left", **SIM_STYLE)
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  wrote", name)


rng = np.random.default_rng(20500117)  # fixed seed for reproducibility

# ---- f10: telescope sensitivity over time ---------------------------------
fig, ax = plt.subplots(figsize=(6.2, 2.9))
era = [1960, 1990, 2026, 2050]
sens = [1.0, 30.0, 3000.0, 9000.0]  # arbitrary normalised units, log scale
ax.semilogy([1960, 1990, 2026], sens[:3], "o-", color=C["deep_blue"], lw=2)
ax.scatter([2050], [9000], marker="^", s=70, color=C["solar_accent"], zorder=5)
ax.axvspan(2026, 2050, color=C["icy_cyan"], alpha=0.18)
ax.annotate("extrapolation", (2040, 700), color="#B0722A", fontsize=8, rotation=12)
ax.set_ylabel("aggregate survey capability\n(arbitrary log units)")
ax.set_xlabel("year  [AD]")
ax.set_xticks(era)
ax.text(1961, 1800, "history (measured)", color=C["deep_blue"], fontsize=8)
save(fig, "f10-sensitivity.svg", simulated=False)

# ---- f11: electromagnetic band comparison ---------------------------------
fig, ax = plt.subplots(figsize=(6.2, 2.6))
bands = [("Optical", 500e-9), ("Infrared", 2e-6), ("Radio", 0.21), ("X-ray", 1e-10)]
names = [b[0] for b in bands]
logw = [np.log10(b[1]) for b in bands]
colors = [C["icy_cyan"], C["solar_accent"], C["deep_blue"], "#8A4FA3"]
ax.barh(range(4), [0.6]*4, left=logw, color=colors, height=0.55)
ax.set_yticks(range(4), names)
ax.set_xlabel("typical wavelength  log10( metres )")
ax.set_xlim(-11.5, -0.5)
for i, w in enumerate(bands):
    lbl = f"~{w[1]*1e9:.0f} nm" if w[1] < 1e-6 else (f"~{w[1]*100:.0f} cm" if w[1] >= 1e-4 else f"~{w[1]*1e6:.0f} µm")
    ax.text(logw[i]+0.05, i, lbl, va="center", fontsize=8)
ax.invert_yaxis()
save(fig, "f11-bands.svg", simulated=False)

# ---- f12: AN-2050-017 simulated transmission spectrum ---------------------
fig, ax = plt.subplots(figsize=(6.2, 3.1))
wavelength = np.linspace(0.6, 5.0, 90)  # micrometres (JWST-like NIR range)
base = np.zeros_like(wavelength) + 0.02
features = [(1.4, 0.030, 0.15), (2.7, 0.042, 0.25), (3.3, -0.018, 0.18), (4.3, 0.026, 0.14)]
for mu, amp, wid in features:
    base += amp * np.exp(-(wavelength-mu)**2 / (2*wid**2))
noise = rng.normal(0, 0.006, len(wavelength))
err = np.full(len(wavelength), 0.008) + 0.002*np.abs(wavelength-2.5)
depth = base + noise
ax.errorbar(wavelength, depth, yerr=err, fmt="o", ms=2.6, mfc=C["deep_blue"],
            mec="none", ecolor="#9AA7BD", elinewidth=0.8, capsize=0, label="simulated data")
model = base + rng.normal(0, 0, len(wavelength))
ax.plot(wavelength, model, color=C["solar_accent"], lw=1.8, label="fitted model")
ax.set_xlabel("wavelength  [µm]")
ax.set_ylabel("transit depth offset  [dimensionless]")
ax.legend(frameon=False, fontsize=8, loc="lower right")
save(fig, "f12-an2050-017-spectrum.svg")

# ---- f16: transit light curve (M01 companion) -----------------------------
fig, ax = plt.subplots(figsize=(6.0, 2.8))
t = np.linspace(0, 3.0, 400)          # days
rp_rs = np.sqrt(0.0156)               # depth 1.56 %  => (Rp/Rs)^2
depth = 1 - 0.0156*np.clip(1-((t-1.4)/0.09)**2, 0, 1)
scatter = depth + rng.normal(0, 0.0009, len(t))
ax.plot(t, scatter, ".", ms=1.6, color=C["deep_blue"])
ax.axhline(1-0.0156, color=C["solar_accent"], lw=1.2, ls="--")
ax.text(2.45, 1-0.0148, "transit depth = 1.56 %", fontsize=8, color="#B0722A")
ax.set_xlabel("time  [days]")
ax.set_ylabel("relative flux  [normalised]")
ax.set_ylim(1-0.022, 1+0.008)
save(fig, "f16-lightcurve.svg")

# ---- f19: gravitational-wave strain ---------------------------------------
fig, ax = plt.subplots(figsize=(6.2, 2.7))
t2 = np.linspace(-0.15, 0.02, 500)
f = 60*np.exp(-(t2+0.05)/0.03)
amp = np.exp(-(t2+0.05)**2/0.0009)
phase = 2*np.pi*np.cumsum(f)/ (1/ (t2[1]-t2[0]))
strain = amp*np.sin(2*np.pi*30*np.exp(-(t2+0.05)/0.05)*8)
strain += rng.normal(0, 0.05, len(t2))
ax.plot(t2*1000, strain, lw=0.7, color=C["deep_blue"])
ax.set_xlabel("time relative to merger  [ms]")
ax.set_ylabel("strain h  [dimensionless, ×10⁻²¹ scale]")
ax.text(-148, 0.9, "rising frequency + amplitude = 'chirp'", fontsize=8, color=C["midnight_navy"])
save(fig, "f19-chirp.svg")

# ---- f21: galaxy rotation curve -------------------------------------------
fig, ax = plt.subplots(figsize=(6.0, 2.8))
r = np.linspace(0.4, 10, 100)         # kpc
v_kepler = 220*np.sqrt(r)/np.sqrt(10.0)
v_obs = 220*np.sqrt(1-np.exp(-r/1.8)) * 1.05 + rng.normal(0, 3, len(r))
ax.plot(r, v_kepler, "--", color=C["solar_accent"], label="visible mass prediction")
ax.plot(r, v_obs, ".", ms=2.2, color=C["deep_blue"], label="measured (simulated points)")
ax.set_xlabel("distance from galaxy centre  [kpc]")
ax.set_ylabel("orbital speed  [km/s]")
ax.legend(frameon=False, fontsize=8)
save(fig, "f21-rotation.svg")

# ---- f22: expansion history -----------------------------------------------
fig, ax = plt.subplots(figsize=(6.0, 2.8))
z = np.linspace(0.01, 1.4, 60)
hubble = 67.4*np.sqrt(0.315*(1+z)**3 + 0.685) - rng.normal(0, 2.0, len(z))
ax.errorbar(z, hubble, yerr=3.0, fmt="o", ms=2.4, mfc=C["deep_blue"], mec="none",
            ecolor="#9AA7BD", elinewidth=0.8, label="simulated SN+BAO composite")
zz = np.linspace(0, 1.4, 200)
ax.plot(zz, 67.4*np.sqrt(0.315*(1+zz)**3 + 0.685), color=C["solar_accent"], lw=1.8,
        label="ΛCDM model (Planck 2018)")
ax.set_xlabel("redshift z  [dimensionless]")
ax.set_ylabel("H(z)  [km/s/Mpc]")
ax.legend(frameon=False, fontsize=8)
save(fig, "f22-expansion.svg")

# ---- f23: Hubble tension scatter ------------------------------------------
fig, ax = plt.subplots(figsize=(6.0, 2.8))
meas = [("Planck 2018 (early)", 67.4, 0.5, C["deep_blue"]),
        ("SH0ES (late)", 73.0, 1.0, C["solar_accent"]),
        ("TRGB anchor (late)", 69.8, 0.8, "#2E7D4F")]
for i, (name, h0, e, col) in enumerate(meas):
    ax.errorbar(i, h0, yerr=e, fmt="o", ms=8, color=col, capsize=5)
ax.axhspan(66.9, 72.0, color="#D8DEE9", alpha=0.4)
ax.set_xticks(range(3), [m[0] for m in meas], fontsize=8)
ax.set_ylabel("H₀  [km/s/Mpc]")
ax.text(1.55, 71.6, "5–6σ disagreement", fontsize=8, color="#8A1F1F")
save(fig, "f23-hubble.svg")

# ---- f33: simulated survey sky map ----------------------------------------
fig, ax = plt.subplots(figsize=(6.2, 2.9))
n = 700
ra = rng.uniform(0, 360, n)
dec = np.degrees(np.arcsin(rng.uniform(-0.95, 0.95, n)))
mag = rng.normal(21, 1.1, n)
ax.scatter(ra, dec, s=(22.5-mag)**2*2.2, c=mag, cmap="viridis", alpha=0.75)
ax.set_xlabel("right ascension  [deg]")
ax.set_ylabel("declination  [deg]")
ax.set_xlim(0, 360)
save(fig, "f33-skymap.svg")

# ---- f35: clock precision timeline ----------------------------------------
fig, ax = plt.subplots(figsize=(6.0, 2.6))
years = [1955, 1975, 1995, 2015, 2026]
rel = [1e-9, 1e-13, 1e-15, 1e-17, 1e-18]
ax.semilogy(years, rel, "o-", color=C["deep_blue"])
ax.set_xlabel("year  [AD]")
ax.set_ylabel("relative clock uncertainty (order of)")
ax.set_xticks(years)
save(fig, "f35-clocks.svg", simulated=False)

# ---- f41/f42: cosmic detective evidence (AN-2050-017) ---------------------
fig, ax = plt.subplots(figsize=(6.2, 3.0))
wl = np.linspace(0.6, 5.0, 120)
spec_a = 0.03*np.exp(-(wl-1.4)**2/0.05) - 0.02*np.exp(-(wl-3.3)**2/0.06)
spec_b = 0.03*np.exp(-(wl-1.4)**2/0.05) - 0.02*np.exp(-(wl-3.3)**2/0.06) + 0.045*np.exp(-(wl-4.6)**2/0.02)
ax.errorbar(wl, spec_a + rng.normal(0, 0.004, len(wl)), yerr=0.005, fmt="o", ms=2,
            mfc=C["deep_blue"], mec="none", ecolor="#9AA7BD", elinewidth=0.7, label="night 1")
ax.errorbar(wl, spec_b + rng.normal(0, 0.004, len(wl)), yerr=0.005, fmt="o", ms=2,
            mfc=C["solar_accent"], mec="none", ecolor="#C9B29A", elinewidth=0.7, label="night 7")
ax.set_xlabel("wavelength  [µm]")
ax.set_ylabel("relative absorption depth  [dimensionless]")
ax.legend(frameon=False, fontsize=8)
ax.annotate("night-7 extra feature near 4.6 µm", (4.05, 0.052), fontsize=7.5,
            color="#8A1F1F")
save(fig, "f42-an2050-017-nights.svg")

print("figures complete")
