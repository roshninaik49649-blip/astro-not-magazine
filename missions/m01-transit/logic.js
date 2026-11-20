/* M01 exoplanet transit — pure logic, no DOM. Seed fixed for reproducibility. */
function mulberry32(seed){
  return function(){
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const M01 = {
  SEED: 20500116,
  /* Simulated light curve: 400 points, 3 days, depth = (rp/rs)^2 */
  lightCurve: function (rpRs, noise, seed) {
    const rnd = mulberry32(seed ?? this.SEED);
    const n = 400, t = [], f = [];
    for (let i = 0; i < n; i++) {
      const ti = (3.0 * i) / (n - 1);
      const x = (ti - 1.4) / 0.09;
      const dip = Math.max(0, 1 - x * x);
      const depth = rpRs * rpRs;
      f.push(1 - depth * dip + (noise ?? 0.0009) * (rnd() * 2 - 1));
      t.push(ti);
    }
    return { t, f };
  },
  depth: function (rpRs) { return rpRs * rpRs; },
  /* correct radius ratio for the reference depth of 1.56 % */
  ANSWER_RP_RS: Math.sqrt(0.0156),
  /* acceptance: model depth within 15 % relative of the reference */
  checkAnswer: function (rpRs) {
    const ref = this.ANSWER_RP_RS;
    return Math.abs(rpRs - ref) / ref <= 0.15;
  },
};
if (typeof module !== "undefined") module.exports = M01;
