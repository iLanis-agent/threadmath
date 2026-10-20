# Thread Math

Thread pitch and turns arithmetic. 20 threads per inch is a pitch of 1.27 mm.

## What it computes

- **The inch truth** - threads per inch (1 to 100) as a pitch in mm, with an inch taken as exactly 25.4 mm.
- **The pitch truth** - a pitch (0.05 to 10 mm) as threads per inch.
- **The turns truth** - the turns that move a nut or screw a distance (0.1 to 1000 mm) for a pitch and 1 to 4 starts.

## Boundary

Arithmetic only. The pitch, starts and distance are the owner's own entries. It has not seen any thread and does not know its form, fit, class, material or load, and it gives no verdict that a thread suits a job or that a part is the right one. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers, half-up rounding).
- `oracle.py` - the Python mirror (Fractions, stepping turn by turn) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/threadmath/
Repo: https://github.com/iLanis-agent/threadmath
