---
page: 16
headline: "Mission 01: The Transit"
section: "09-16 Telescopes, Exoplanets & Life"
type: mission
dark: false
confidence: []
references: [R01]
qr: Q-M01
---
## Mission M01 — Catch a transiting planet

You have a simulated light curve: starlight dimmed by a passing planet. Estimate the transit **depth** and from it the planet's radius.

### QR code → missions/m01-transit/index.html

**The physics ::est:: [R01]:** the fractional dip in light equals the *area ratio*:

> depth ≈ (R_planet / R_star)²

So a planet one-tenth of its star's width blocks about 1 % of the light. Small numbers, big consequences.

**Your task:**

1. Read the SIMULATED light curve; note the dip depth of **1.56 %** — the plot shows relative flux (normalised) against time in days.
2. In the mission, drag the planet-radius slider. Watch the model curve hug the data when the ratio is right.
3. Compute: for a Sun-sized star, what planet radius does a 1.56 % depth imply? The mission gives instant feedback and shows the algebra.
4. Then see how noisy data changes your certainty — jitter the simulation and watch your uncertainty grow.

**SIMULATED label:** the light curve is synthetic (seeded, reproducible), not a real star's data — the method is real ::est::, the dataset is a training ground.

**Why it matters:** this is exactly how thousands of the 5,000+ confirmed exoplanets [R01] were found — by people reading dips like these.
