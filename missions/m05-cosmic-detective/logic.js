/* M05 cosmic detective — pure logic: case AN-2050-017 (fictional, simulated). */
const M05 = {
  OBS_ID: "AN-2050-017",
  /* fictional case data; spectra are SIMULATED (see figures/out) */
  HYPOTHESES: [
    { id: "H1", name: "Biological", fits: "both nights with a seasonal assumption" },
    { id: "H2", name: "Photochemical", fits: "both nights with known abiotic chemistry" },
    { id: "H3", name: "Instrumental", fits: "night-7 feature via thermal correlation" },
  ],
  /* resolved answer of the fictional case */
  ANSWER: "H3",
  RATIONALE: [
    "The 4.6 um feature correlates with instrument B's logged thermal noise, not with the planet.",
    "A corrected-thermal re-analysis removed the feature; an independent team's reduction never showed it.",
    "Base rates: artefact explanations outrank biological ones a priori.",
    "H2 (photochemical) remains the runner-up for the original dips; H1 was never required.",
  ],
  checkAnswer: function (id) { return id === this.ANSWER; },
};
if (typeof module !== "undefined") module.exports = M05;
