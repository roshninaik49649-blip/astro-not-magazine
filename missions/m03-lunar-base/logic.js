/* M03 lunar base designer — pure logic. Fictional scoring model. */
const M03 = {
  TOTAL: 100,
  HAZARDS: ["night", "radiation", "water", "morale"],
  /* allocation object {power, shielding, water, research} must sum to <= 100;
     unspent units are simply unused (slack) */
  score: function (a) {
    const sum = a.power + a.shielding + a.water + a.research;
    if (sum > this.TOTAL) return { viable: false, reason: "Over budget: " + sum + " > 100" };
    const night = a.power >= 30 ? "OK" : "FAIL";
    const radiation = a.shielding >= 25 ? "OK" : "FAIL";
    const water = a.water >= 20 ? "OK" : "FAIL";
    const morale = a.research >= 15 ? "OK" : "FAIL";
    const viable = [night, radiation, water, morale].every(x => x === "OK");
    return {
      viable, hazards: { night, radiation, water, morale },
      reason: viable ? "Base survives all four hazards." :
        "Failed: " + [night === "FAIL" && "lunar night (power)", radiation === "FAIL" &&
        "radiation (shielding)", water === "FAIL" && "water supply", morale === "FAIL" &&
        "crew morale (research)"].filter(Boolean).join(", "),
    };
  },
  /* reference minimal viable allocation, used in tests */
  ANSWER: { power: 30, shielding: 25, water: 20, research: 15, slack: 10 },
};
if (typeof module !== "undefined") module.exports = M03;
