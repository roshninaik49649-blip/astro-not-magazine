/* M06 predictions archive — pure logic: prompt list and storage shape. */
const M06 = {
  /* all data stays in the browser's localStorage; nothing is uploaded */
  STORAGE_KEY: "astronot-m06-predictions",
  PROMPTS: [
    "How many exoplanets will be confirmed by 2050? (Check the current count first.)",
    "Will a biosignature candidate be announced? Which confidence label would you give it?",
    "Will the Hubble tension be resolved - dissolved, confirmed, or still contested?",
    "How many people will have travelled to space by 2050?",
    "Our bet: the Universe will not change drastically by 2050. Agree or disagree - and say what would change your mind.",
  ],
  blank: function () {
    return this.PROMPTS.map((p, i) => ({ index: i, text: "", confidence: 0, falsifier: "" }));
  },
  validate: function (saved) {
    return Array.isArray(saved) && saved.length === this.PROMPTS.length &&
      saved.every(s => typeof s.confidence === "number" && s.confidence >= 0 && s.confidence <= 100);
  },
};
if (typeof module !== "undefined") module.exports = M06;
