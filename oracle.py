#!/usr/bin/env python3
# Thread Math oracle - mirrors engine.js with Fractions: an inch is exactly 25.4 mm, the pitch is its reciprocal, the turns are found by stepping one turn at a time and adding the leftover fraction, rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

TPI = "the threads per inch must be from 1 to 100 with at most one decimal place"
PITCH = "the pitch must be from 0.05 to 10 mm with at most two decimal places"
LEN = "the distance must be from 0.1 to 1000 mm with at most one decimal place"
START = "the number of starts must be a whole number from 1 to 4"
def dec(t, err, intd, places, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,%d}(\.[0-9]{1,%d})?" % (intd, places), t) or not F(lo) <= F(t) <= F(hi): raise ValueError(err)
    return F(t)
def whole(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,3}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def txt(fr, places):
    v = int((Decimal(fr.numerator) / Decimal(fr.denominator) * (10 ** places)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    ip, fp = divmod(v, 10 ** places); fs = str(fp).zfill(places).rstrip("0")
    return f"{ip}.{fs}" if fs else str(ip)
INCH = F(254, 10)

def tpi(t):
    T = dec(t, TPI, 3, 1, "1", "100")
    return f"{txt(T,1)} threads per inch is a pitch of {txt(INCH / T,3)} mm."
def pitch(p):
    P = dec(p, PITCH, 2, 2, "0.05", "10")
    return f"A pitch of {txt(P,2)} mm is {txt(INCH / P,2)} threads per inch."
def turns(p, s, l):
    P = dec(p, PITCH, 2, 2, "0.05", "10"); S = whole(s, START, 1, 4); L = dec(l, LEN, 4, 1, "0.1", "1000")
    lead = P * S; whole_turns = 0; rest = L
    while rest >= lead: rest -= lead; whole_turns += 1
    t = whole_turns + rest / lead
    sh = txt(t, 2)
    shown = "under 0.01 turns" if sh == "0" else sh + (" turn" if sh == "1" else " turns")
    return f"A pitch of {txt(P,2)} mm with {S} start{'' if S == 1 else 's'} advances {txt(lead,2)} mm a turn, so {txt(L,1)} mm takes {shown}."

FNS = {"tpiTruth": tpi, "pitchTruth": pitch, "turnsTruth": turns}
def cases():
    c = []
    for t in ["1", "1.5", "4", "11.5", "13", "16", "20", "24", "32", "40", "56", "100", "99.9", "7.3"]: c.append(("tpiTruth", [t]))
    for p in ["0.05", "0.07", "0.25", "0.5", "0.75", "1", "1.25", "1.5", "1.75", "2", "2.5", "6.35", "9.99", "10"]: c.append(("pitchTruth", [p]))
    for p in ["0.05", "0.5", "1.5", "10"]:
        for s in ["1", "2", "4"]:
            for l in ["0.1", "25", "100.5", "1000"]:
                c.append(("turnsTruth", [p, s, l]))
    for t in [" 20 ", "20.0", "020"]: c.append(("tpiTruth", [t]))
    c += [("pitchTruth", [" 1.5 "]), ("pitchTruth", ["1.50"]), ("turnsTruth", [" 1.5 ", " 2 ", " 25 "])]
    bad = ["", "x", "0", "0.0", "-1", ".5", "5.", "1e2", "0.001", "1.234", "10000", "99999"]
    for v in bad:
        c += [("tpiTruth", [v]), ("pitchTruth", [v]), ("turnsTruth", [v, "1", "25"]), ("turnsTruth", ["1.5", v, "25"]), ("turnsTruth", ["1.5", "1", v])]
    c += [("tpiTruth", ["0.9"]), ("tpiTruth", ["100.1"]), ("pitchTruth", ["0.04"]), ("pitchTruth", ["10.01"]),
          ("turnsTruth", ["1.5", "5", "25"]), ("turnsTruth", ["1.5", "0", "25"]), ("turnsTruth", ["1.5", "1", "1000.1"]), ("turnsTruth", ["1.5", "1", "0.05"])]
    r = random.Random(715)
    for _ in range(10):
        p = f"{r.randint(0, 9)}.{r.randint(0, 99):02d}"; p = "0.05" if float(p) < 0.05 else p
        l = f"{r.randint(0, 999)}.{r.randint(0, 9)}"; l = "0.1" if l == "0.0" else l
        c += [("tpiTruth", [f"{r.randint(1, 99)}.{r.randint(0, 9)}"]), ("pitchTruth", [p]), ("turnsTruth", [p, str(r.randint(1, 4)), l])]
    return c
out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":"), ensure_ascii=False) for o in out) + "\n]\n")
print(len(out), "cases written")
