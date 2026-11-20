/* M02 signal or noise — pure logic. Seeded chirp detection demo. */
function mulberry32(seed){
  return function(){
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const M02 = {
  /* generate a stream; signal present if hasSignal */
  stream: function (hasSignal, seed) {
    const rnd = mulberry32(seed ?? 20500120);
    const n = 600, data = [];
    for (let i = 0; i < n; i++) data.push((rnd() * 2 - 1) * 0.25);
    if (hasSignal) {
      for (let i = 120; i < 300; i++) {
        const p = (i - 120) / 180;
        const env = Math.sin(Math.PI * p);
        data[i] += env * Math.sin(2 * Math.PI * (3 + 14 * p * p) * p * 4);
      }
    }
    return data;
  },
  /* simplified matched filter: peak normalised correlation with the chirp template */
  matchScore: function (data) {
    const tpl = M02.stream(true, 20500120).slice(120, 300);
    let best = 0;
    for (let off = 0; off + tpl.length <= data.length; off += 4) {
      let c = 0, e1 = 0, e2 = 0;
      for (let i = 0; i < tpl.length; i++) {
        c += data[off + i] * tpl[i]; e1 += data[off + i] ** 2; e2 += tpl[i] ** 2;
      }
      const nc = c / Math.sqrt(e1 * e2 + 1e-12);
      if (nc > best) best = nc;
    }
    return best;
  },
  THRESHOLD: 0.35,
  isSignal: function (data) { return M02.matchScore(data) > M02.THRESHOLD; },
};
if (typeof module !== "undefined") module.exports = M02;
