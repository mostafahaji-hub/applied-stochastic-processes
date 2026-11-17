# SP_Code_CH17 — Chapter 17: Monte Carlo Basics (with the Part VI opener)

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch17_mc.py` | Importable: `lcg`, `period`, `hull_dobell`, inverse transforms (exponential, Weibull, discrete), acceptance–rejection for 6x(1−x), `mc_mean` (estimate, SE, 95% interval), `n_needed`, tire constants, renewal-reward cost rate |
| python | `sp_ch17_figures.py` | Part VI opener + Figures 17.1–17.11 |
| python | `sp_ch17_check.py` (+ output) | Checks of examples, Quests and exercises |
| python | `sp_ch17_simulation.py` | `--lcg A C M SEED`, `--plate N`, `--audit` (Table 17.1), `--vr`, `--crn` |
| matlab | `sp_ch17_mc.m` | LCG, inverse transform, P(late), antithetic estimate (teaching version; not executed in the author environment) |
| excel | `SP_CH17_Excel.xlsx` | *LCG* (40 steps, period), *InverseTransform* (1,000 live draws: board, tire, refund, demand with 95% coverage check), *PLate_MC* (1,000 simulated days), *SampleSize* |
| figures | `SP_Fig_CH17_00_PartVI.png`, `SP_Fig_CH17_01.png` … `SP_Fig_CH17_11.png` | Part opener and chapter figures |

Fixed numbers: LCG (5, 3, 16, seed 7) → 7, 6, 1, 8, 11, 10, 5, 12, 15, 14, 9, 0, 3, 2, 13, 4, period 16. Inverse transform: board u = 0.3/0.9 → 2.85/18.42 months; tire u = 0.3/0.5/0.9 → 7.94/10.36/16.75; refund u = 0.10/0.72/0.97 → 0/20/100; Poisson(3) u = 0.55 → 3; demand u = 0.9 → 602.5. Acceptance–rejection 6x(1−x), c = 1.5: rate 2/3. Audit (seed 172): P(late) 0.246 [0.219, 0.273] vs 0.2299; refund 18.69 [17.11, 20.27] vs 18.5; tardiness 35.02 [33.09, 36.95] vs 34.1; runway 0.3805 vs 0.382; tire 10.74 [10.46, 11.02] vs 10.65. Runs: ±0.005 on P(late) 27,214; rare event 4.8e−5 with ±10% relative error ≈ 8.0 million. Variance reduction (seed 178): SD 0.454 plain, 0.061 antithetic, 0.163 control (b = 4.26). CRN (seed 179): SD of the difference 1.68 → 0.71; wrong sign 26% → 10%; exact difference 0.867 €/month.
