#!/usr/bin/env python3
"""Self-contained runner for humanizer-pl evals.

Reads evals.json, evaluates every binary assertion against each case's frozen
(input, output) pair, and checks the result against the case's `expect` map.
No LLM call needed - the humanized outputs are stored in the file. Exit code 0
iff every assertion passes for every case.

    python3 evals/run_evals.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(HERE, "evals.json"), encoding="utf-8"))

EMDASH = cfg["forbidden_chars"]                       # actual U+2014 / U+2013 chars
ARTIFACTS = next(a["list"] for a in cfg["assertions"] if a["id"] == "no_chatbot_artifacts")


def check(lang, inp, out):
    o, ol = out, out.lower()
    first = next((l for l in out.splitlines() if l.strip()), "").strip().lower()
    banned = cfg["banned_words"][lang]
    fillers = cfg["filler_openers"][lang]
    r = {
        "no_emdash_endash": not any(c in o for c in EMDASH),
        "no_banned_words": not any(w in ol for w in banned),
        "not_longer_than_input": len(o) <= len(inp),
        "first_line_not_filler": not any(first.startswith(f) for f in fillers),
        "no_chatbot_artifacts": not any(a in ol for a in ARTIFACTS),
    }
    if lang == "pl":
        r["pl_diacritics_present"] = bool(re.search(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", o))
    return r


ok = True
for c in cfg["cases"]:
    res = check(c["lang"], c["input"], c["output"])
    print(f"\n=== {c['name']} (lang={c['lang']}) "
          f"len(in)={len(c['input'])} len(out)={len(c['output'])} ===")
    for k, v in res.items():
        exp = c.get("expect", {}).get(k)
        status = "PASS" if v else "FAIL"
        mism = "" if (exp is None or exp == v) else f"  (expected {exp})"
        print(f"  [{status}] {k}{mism}")
        if not v or (exp is not None and exp != v):
            ok = False

print("\n" + ("ALL ASSERTIONS PASS" if ok else "SOME ASSERTIONS FAILED"))
sys.exit(0 if ok else 1)
