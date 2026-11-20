#!/usr/bin/env python3
"""Mission tests: run pure-logic JS via node, validate HTML requirements.
Exits non-zero on any failure. Run from repo root: .venv/bin/python missions/tests/test_missions.py
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
M = os.path.join(ROOT, "missions")
failures = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" — " + detail) if detail else ""))
    if not ok:
        failures.append(name)


def node(code):
    r = subprocess.run(["node", "-e", code], capture_output=True, text=True, cwd=M)
    return r.returncode == 0, r.stdout.strip() + r.stderr.strip()


# --- syntax check every logic.js ---
for m in ["m01-transit", "m02-waveform", "m03-lunar-base", "m04-human-vs-ai",
          "m05-cosmic-detective", "m06-predictions"]:
    ok, out = node(f'require("./{m}/logic.js"); console.log("ok")')
    check(f"node syntax+load {m}", ok, out[:200])

# --- M01: depth physics ---
ok, out = node("""
const M01 = require('./m01-transit/logic.js');
const d = M01.depth(M01.ANSWER_RP_RS);
console.log(Math.abs(d - 0.0156) < 1e-9 ? "pass" : "fail");
const lc = M01.lightCurve(M01.ANSWER_RP_RS, 0.0009, M01.SEED);
const minF = Math.min(...lc.f.filter((_,i)=>lc.t[i]>1.3&&lc.t[i]<1.5));
console.log(Math.abs(minF - (1-0.0156)) < 0.005 ? "pass" : "fail");
""")
check("M01 depth=(rp/rs)^2 == 1.56% and curve dips correctly", out.count("pass") == 2, out[:200])

# --- M02: matched filter detects signal, rejects noise ---
ok, out = node("""
const M02 = require('./m02-waveform/logic.js');
const sig = M02.stream(true, 42), noi = M02.stream(false, 42);
console.log(M02.matchScore(sig) > M02.THRESHOLD ? "pass" : "fail");
console.log(M02.matchScore(noi) < M02.THRESHOLD ? "pass" : "fail");
let fa = 0; for (let s = 0; s < 50; s++) if (M02.isSignal(M02.stream(false, s))) fa++;
console.log(fa <= 5 ? "pass" : "fail");  // false-alarm rate < 10 %
""")
check("M02 detection + false-alarm control", out.count("pass") == 3, out[:300])

# --- M03: scoring ---
ok, out = node("""
const M03 = require('./m03-lunar-base/logic.js');
const a = M03.score(M03.ANSWER);
console.log(a.viable ? "pass" : "fail");
const bad = M03.score({power:10, shielding:25, water:20, research:45});
console.log(!bad.viable && bad.hazards.night === "FAIL" ? "pass" : "fail");
const over = M03.score({power:50, shielding:25, water:20, research:15});
console.log(!over.viable ? "pass" : "fail");
""")
check("M03 viable reference allocation + hazard failures + budget guard", out.count("pass") == 3, out[:300])

# --- M04: answer key sanity ---
ok, out = node("""
const M04 = require('./m04-human-vs-ai/logic.js');
console.log(M04.CASES.length === 12 ? "pass" : "fail");
const r = M04.scoreUser(M04.CASES.map(c => c.cls));
console.log(r.right === 12 ? "pass" : "fail");
console.log(M04.aiAccuracy() < 1 && M04.aiAccuracy() > 0.5 ? "pass" : "fail");
""")
check("M04 12 cases, key self-consistent, AI imperfect", out.count("pass") == 3, out[:300])

# --- M05: answer key ---
ok, out = node("""
const M05 = require('./m05-cosmic-detective/logic.js');
console.log(M05.OBS_ID === "AN-2050-017" ? "pass" : "fail");
console.log(M05.checkAnswer("H3") && !M05.checkAnswer("H1") ? "pass" : "fail");
""")
check("M05 observation ID + answer key", out.count("pass") == 2, out[:200])

# --- HTML requirement checks ---
for m, label in [("m01-transit", "SIMULATED"), ("m02-waveform", "SIMULATED"),
                 ("m03-lunar-base", "FICTIONAL SCENARIO"), ("m04-human-vs-ai", "SIMULATED"),
                 ("m05-cosmic-detective", "FICTIONAL SCENARIO"), ("m06-predictions", "PRIVACY")]:
    html = open(os.path.join(M, m, "index.html")).read()
    check(f"{m}: carries '{label}' label", label in html)
    check(f"{m}: keyboard-friendly controls", 'type="range"' in html or "<select" in html or "button" in html)
    check(f"{m}: aria-live feedback", 'aria-live' in html)

html5 = open(os.path.join(M, "m05-cosmic-detective", "index.html")).read()
check("M05: AN-2050-017 present in mission", "AN-2050-017" in html5)
check("M06: local-storage stated in UI", "local storage" in open(os.path.join(M, "m06-predictions", "index.html")).read())

print()
if failures:
    print(f"{len(failures)} FAILURES:", *failures, sep="\n  ")
    sys.exit(1)
print("All mission tests passed.")
