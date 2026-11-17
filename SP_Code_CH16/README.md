# SP_Code_CH16 (v2) — Chapter 16: The Keshtel Algorithm as a Stochastic Process

Version 2 follows the textbook version of the Keshtel algorithm given by its creator (the author of this book): lucky keshtels (attraction of the nearest neighbor, the diagnostic question “slope or pit?”, the bisection swirl capped by S_max), unlucky keshtels (fly away; random newcomers land) and remaining keshtels (move toward the middle of two other keshtels). R6 schedules are represented by random keys decoded by sorting.

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch16_ka.py` | `ka_run` (M, p1, p2 or N1/N2, S_max, budget, optional lake memory; group bookkeeping), `swirl`, `decode`, `hand_trace` (Tables 16.1–16.3), `ka_toy` (barrier landscape with one key) |
| python | `sp_ch16_simulation.py` | `--trace`, `--runs`, `--ablation`, `--groups`, `--toy N2`, `--smax S` |
| python | `sp_ch16_figures.py` | Figures 16.1–16.9 from `ka2_results.json`, `ka2_sweep.json`, `ka2_ttt.json` |
| python | `sp_ch16_check.py` (+ output) | Checks of all example and exercise numbers |
| matlab | `sp_ch16_ka.m` | One textbook-Keshtel run on R6 (teaching version; not executed in the author environment) |
| excel | `SP_CH16_Excel.xlsx` | *Groups_Guarantee* (N1, N2, N3, swirl budget, q and the geometric bound), *Decode_Hustle* (move toward the middle of two keshtels, decoding and total tardiness) |

Fixed numbers (M = 10, N1 = 2, N2 = 3, N3 = 5, S_max = 2, budget 200): hand trace (seed 24) 21 → 19 → 17 by two slopes, then a pit (7 evaluations); landings 36 → 16 and 56 → 46; moves 24 → 26, 25 → 43, 33 → 27; new population best 16, mean 29.2. S_max = 2 / 4 / 8: P(found by 100) 0.64 / 0.52 / 0.43. Ablation (2,000 runs): full 0.63 by 100 (success 87%, mean 75); N1 = 0: 0.35; N2 = 0: 0.54; N3 = 0: 0.66; landings only: 0.24. Groups: improvements 88.3 / 3.8 / 7.9 %, first discovery 86.5 / 2.6 / 10.9 % (lucky / unlucky / remaining). Barrier landscape: with landings 99.85 % (mean 23), without 0 %. Thirty runs: 22 / 30, mean 95, median 83. Time to target (2,000 runs, seed 167), P(by 100) every trial / distinct schedules: greedy 1.00 / 1.00, SA 0.93 / 1.00, GA 0.79 / 0.98, KA 0.62 / 0.94, random 0.24 / 0.26; KA mean 74 trials = 44 distinct schedules. Guarantee q = 0.0083 per iteration.
