---
page: 36
headline: "Mission 04: Human vs AI"
section: "33-40 AI, Quantum & Futures"
type: mission
dark: false
confidence: []
references: [R12]
qr: Q-M04
---
## Mission M04 — Human vs AI: spot the artefacts

A simulated sky survey has flagged 12 "interesting" detections. Some are real transients, some are artefacts. The pipeline's AI has an opinion. Do you agree with it?

### QR code → missions/m04-human-vs-ai/index.html

**Your task:**

1. Inspect each flagged source in the SIMULATED sky data (seeded, reproducible): light curve shape, neighbouring pixels, timestamps.
2. **Classify** each: transient ✦ / artefact ✦ / uncertain. (In this game the "truth" is defined by the generator ✦; in real surveys, truth comes from follow-up observation ◆.)
3. **Compare with the AI.** The mission's simulated classifier has a known confusion pattern — it over-trusts sharp shapes and under-flags cosmic-ray-like streaks ◆ (a documented artefact class in real surveys [R12]).
4. Score the round. Then read the debrief: *where* your judgement beat the machine, and where the machine's statistics beat your intuition.

**Going deeper.** This is the real division of labour ::est:: [R12]: machines for coverage and consistency, humans for context and the "wait, that's odd" moments.

**Advanced corner.** The artefact classes in the game (cosmic-ray hits, bad columns, diffraction spikes, saturated bleed) are the same ones real pipelines must reject ::est:: — the game's generator mimics them faithfully, while remaining fully synthetic.

**SIMULATED label:** displayed throughout; no real survey data is used.
