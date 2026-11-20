/* M04 human vs AI — pure logic: 12 seeded detections with a fixed answer key. */
function mulberry32(seed){
  return function(){
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const M04 = {
  /* deterministic case list; class: 'transient' or 'artefact'
     artefactKind in: cosmic-ray, bad-column, diffraction-spike, bleed */
  CASES: [
    { id: "D-01", curve: "fast-rise-slow-fade",  cls: "transient", ai: "transient" },
    { id: "D-02", curve: "sharp-single-pixel",   cls: "artefact",  ai: "transient", kind: "cosmic-ray" },
    { id: "D-03", curve: "smooth-symmetric",     cls: "transient", ai: "transient" },
    { id: "D-04", curve: "vertical-streak",      cls: "artefact",  ai: "artefact", kind: "bad-column" },
    { id: "D-05", curve: "slow-rise-slow-fade",  cls: "transient", ai: "transient" },
    { id: "D-06", curve: "spike-through-star",   cls: "artefact",  ai: "transient", kind: "diffraction-spike" },
    { id: "D-07", curve: "flat-bright-square",   cls: "artefact",  ai: "artefact", kind: "bleed" },
    { id: "D-08", curve: "multi-peak",           cls: "transient", ai: "artefact" },
    { id: "D-09", curve: "single-epoch-only",    cls: "artefact",  ai: "transient", kind: "cosmic-ray" },
    { id: "D-10", curve: "dip-then-recover",     cls: "transient", ai: "transient" },
    { id: "D-11", curve: "parallel-streaks",     cls: "artefact",  ai: "artefact", kind: "diffraction-spike" },
    { id: "D-12", curve: "irregular-jagged",     cls: "transient", ai: "transient" },
  ],
  /* the simulated AI's documented confusion pattern:
     over-trusts sharp point-like shapes (calls them transients),
     occasionally rejects genuinely irregular variability (D-08) */
  aiAccuracy: function () {
    const ok = this.CASES.filter(c => c.ai === c.cls).length;
    return ok / this.CASES.length;
  },
  scoreUser: function (answers) {
    let right = 0;
    this.CASES.forEach((c, i) => { if (answers[i] === c.cls) right++; });
    return { right, total: this.CASES.length, accuracy: right / this.CASES.length };
  },
};
if (typeof module !== "undefined") module.exports = M04;
