# SP_Code_CH12 — Chapter 12: Reliability and Maintenance

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch12_reliability.py` | Importable: weibull_hazard, R_series/R_parallel/R_k_of_n, line_availability (8-state CTMC), renewal_function, block_replacement_rate, inspection_rate, spares_needed (uses sp_ch11_ctmc.py, included) |
| python | `sp_ch12_figures.py` | Figures 12.1–12.10 + number checks |
| python | `sp_ch12_check.py` | Verifies every example and exercise number |
| python | `sp_ch12_simulation.py` | Event-driven line simulation with residual times; `--fixed-repair`, `--seed` |
| matlab | `sp_ch12_reliability.m` | Hazards, k-of-n, line availability, age replacement |
| excel | `SP_CH12_Excel.xlsx` | *Hazard_Structure* (Weibull R/h/MTTF, series/parallel/k-of-n, MTTFs), *Maintenance* (age replacement, inspection, warranty, spares) |
| figures | `SP_Fig_CH12_01.png` … `SP_Fig_CH12_10.png` | Chapter figures |

Fixed numbers: line of 4 machines (three at failure rate 0.05/shift, machine 3 at 1/7, repair rate 1, machine 3 first): availability 0.735 with one crew, 0.756 with two (= independent bound); downtime 3,200 €/shift, crew 300 €/shift ⇒ one crew (1,149 vs 1,382). Three servers, one crew (0.1, 0.3) ⇒ availability 0.923. Tire: hazard 0.026/0.074/0.208 at 3/6/12 months; age replacement T ≈ 5 months 27.9 €/month, block ≈ 28.9, run-to-failure 56.4; bearing T ≈ 10 months 24.6 (block 25.6); board age replacement at 4 months 90.4 vs 75 (never). Inspection (λ = 1/50, 50 €, 100 €/shift) ⇒ weekly, 13.8 €/shift. Warranty: tire 6/12 months 13.0/50.6 €, board renewing 6 months 89 €. Standby MTTF 16 vs active 12; spares for 18 expected failures: 25 (95%), 28 (99%).
