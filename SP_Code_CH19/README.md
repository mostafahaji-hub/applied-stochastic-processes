# SP_Code_CH19 — Chapter 19: Output Analysis, MCMC, and the Book in One Picture

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch19_output.py` | Importable: t-intervals, moving averages (Welch), autocorrelation, batch means, effective sample size, random-walk Metropolis (1-D) and the 2-D Weibull sampler, age-replacement cost curve, exact ruin probability by dynamic programming, plain and importance-sampling ruin estimators |
| python | `sp_ch18_des.py` | Event-list engine from Chapter 18 (scenarios A–E) |
| python | `sp_ch19_simulation.py` | `--all` (re-creates `ch19_results.json`), `--mcmc SD`, `--is PPRIME N` |
| python | `sp_ch19_figures.py` | Figures 19.1–19.11 from `ch19_results.json` |
| python | `sp_ch19_check.py` (+ output) | Checks of all example numbers |
| matlab | `sp_ch19_mcmc.m` | Metropolis for the failure rate (teaching version; not executed in the author environment) |
| figures | `SP_Fig_CH19_01.png` … `SP_Fig_CH19_11.png` | Chapter figures (19.10 = the book in one picture) |

No Excel file in this chapter (the methods need long runs; the Chapter 18 workbook covers the spreadsheet side).

Fixed numbers: scenario E service level 0.704 ± 0.011 (100 days, seed 186; daily SD 0.056; range 0.587–0.855); 121 days for ±0.01, 483 for ±0.005. Welch (200 replications from empty, seed 1902): smoothed queue 5.05 / 6.57 / 6.99 at 60 / 120 / 180 min; delete ≈ 150 min. Long M/M/5 run (seed 1903): 208,487 waits, mean 130.0 s; autocorrelation 0.992 (lag 1), 0.929 (10), 0.578 (100), ≈ 0 (1,000); naive SE 0.39 s, batch-means SE 7.79 s (b = 2,000), plateau 8–9 s; ESS ≈ 477. Bonferroni (m = 4) paired differences E − A/B/C/D: 0.370 ± 0.009, 0.093 ± 0.009, 0.095 ± 0.005, 0.0095 ± 0.0091. MCMC failure rate: prior Gamma(2, 10), 12 failures in 84 shifts ⇒ posterior Gamma(14, 94), mean 0.1489, 95% [0.0814, 0.2365], mean uptime 7.23 shifts; Metropolis SD 0.04 (seed 1905): mean 0.1488, acceptance 0.70, ESS 2,421; tuning SD 0.005/0.04/0.4 ⇒ acceptance 0.96/0.70/0.12, ESS 70/2,423/1,315. Weibull posterior from 20 lives (seed 1919, mean 11.05): k 3.11 [2.11, 4.25], η 12.43 [10.58, 14.45], mean life 11.13 [9.40, 12.96]; T* mean 5.43, 90% [4.5, 6.5], P(4 ≤ T* ≤ 6) = 0.872; regret of T = 5: 0.35 €/month; saving vs run-to-failure 30.8 €/month. Importance sampling: exact ruin (start 20, barrier −10, 90 days, p = 0.55) 5.035e−5; plain 200,000 runs → 3 ruins; IS with p′ = 0.35, 20,000 runs → 5.11e−5 ± 0.046e−5.
