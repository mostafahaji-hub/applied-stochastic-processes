# SP_Code_CH10 — Chapter 10: Markov Chains in Discrete Time: The Long Run

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch10_longrun.py` | Importable: stationary, classes, period, longrun_cost, pagerank (uses sp_ch09_markov.py, included) |
| python | `sp_ch10_figures.py` | Figures 10.1–10.10 + number checks |
| python | `sp_ch10_check.py` | Verifies every example and exercise number |
| python | `sp_ch10_simulation.py` | Example 10.21 (10,000-shift path), `--periodic` (Exercise 10.19) |
| matlab | `sp_ch10_longrun.m` | π by backslash, long-run cost, brand shares |
| excel | `SP_CH10_Excel.xlsx` | *Stationary3* (3-state π in closed form + cost), *TwoState_Credit* (two-state formula; credit P² … P⁵ and 5-year default) |
| figures | `SP_Fig_CH10_01.png` … `SP_Fig_CH10_10.png` | Chapter figures |

Fixed numbers: machine 3 π = (0.813, 0.102, 0.085), return to M every 11.7 shifts, cost 184 €/shift (S 800, M 1200); "repair after every stop" 301 €/shift; technical improvement (row W = .90/.07/.03) 140 €/shift. Brand matrix Nava/X/Y rows (.80,.15,.05)/(.10,.75,.15)/(.05,.20,.75) ⇒ π = (0.283, 0.413, 0.304). Credit matrix A/B/C/D ⇒ 5-year default (0.048, 0.129, 0.323), years to default (38.9, 31.8, 22.9). Inventory policies A/B ⇒ 3.25/3.27 €/day. PageRank 4 pages ⇒ (0.380, 0.199, 0.384, 0.038).
