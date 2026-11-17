# SP_Code_CH18 — Chapter 18: Simulating Processes: Discrete-Event Simulation

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch18_des.py` | Importable event-list engine: `r1_stream` (thinning of a rate-4 Poisson stream to the 2/4/2.5/3 profile; Exp(1.5) service; 10% callers leave after 2 min), `run_queue` (arrival, departure, abandonment and shift-change events; queue on a time grid), `day_stats`, `erlang_c`, `line_sim` (R2 line with any repair-time distribution, residual-time bookkeeping), `fleet_bursts` (R5 tire fleet) |
| python | `sp_ch18_simulation.py` | `--trace`, `--audit`, `--day X`, `--crn`, `--r2`, `--r5`, `--warm`, `--all` (re-creates `des_results.json`) |
| python | `sp_ch18_figures.py` | Figures 18.1–18.11 from `des_results.json` |
| python | `sp_ch18_check.py` (+ output) | Checks of examples, Quests and exercises |
| matlab | `sp_ch18_des.m` | A minimal event-list M/M/5 simulation (teaching version; not executed in the author environment) |
| excel | `SP_CH18_Excel.xlsx` | *HandTrace* (Table 18.1 with formulas), *Lindley_MM1* (1,000 callers by the Lindley recursion — note how much a single run varies), *Scenarios_Cost* (five scenarios and daily cost), *Thinning* (live thinning across 10:00) |
| figures | `SP_Fig_CH18_01.png` … `SP_Fig_CH18_11.png` | Chapter figures |

Fixed numbers: hand trace (one operator; arrivals 0.6, 2.0, 2.3, 5.2, 5.7; services 1.8, 1.1, 0.7, 1.2, 0.9; caller 3 leaves after 0.5): waits 0, 0.4, (0.5, abandoned), 0, 0.7; area 1.6; Lq 0.219; utilisation 0.685. Thinning λ_max = 4: keep 0.5/1/0.625/0.75; 1,800 calls a day. Audit (seed 184): M/M/5 Wq 133.2 ± 8.5 s vs 137.2; P(wait) 0.761 vs 0.762. R1 day (100 days, seed 186), answered ≤ 30 s / abandoned / mean wait: A (5 all day, 50 h) 33% / 5.0% / 4.73 min; B (6, 60 h) 61% / 1.8% / 0.91; C (7 at 10–13, 56 h) 61% / 1.3% / 0.73; D (8 at 10–13, 59 h) 69% / 1.0% / 0.57; E (5/7/5/6, 59 h) 70% / 0.7% / 0.47; A by period 88/5/42/43%. CRN C − D service level: SD 0.027 (common) vs 0.076 (independent, seed 188); A vs C mean wait SD 2.17 vs 2.36 (independent seed 187; separate run). Warm-up from empty: 3.8 / 4.8 / 6.6 waiting at 30 / 60 / 120 min vs 6.86. R2 (seed 1812): availability 0.732 / 0.736 / 0.737; P(stop > 2 shifts) 19.2% / 4.2% / 15.1% (exponential / constant / lognormal repair). R5 (seed 1813): bursts per month 4.51 vs 1.04; P(≥ 3) 0.84 vs 0.08; planned 8.84 per month.
