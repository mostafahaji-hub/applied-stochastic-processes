# SP_Code_CH09 — Chapter 9: Markov Chains in Discrete Time: First Steps

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch09_markov.py` | Importable toolkit: nstep, dist, hitting_time, hitting_prob, value, runway, simulate; matrices P2 (R2), P3 (R3), W (weather) |
| python | `sp_ch09_figures.py` | Part III opener + Figures 9.1–9.10 + number checks |
| python | `sp_ch09_check.py` | Verifies every example and exercise number |
| python | `sp_ch09_simulation.py` | Example 9.19 (24-month cohort), `--lifetime`, `--weather` |
| matlab | `sp_ch09_markov.m` | Pⁿ, first-step systems with backslash |
| excel | `SP_CH09_Excel.xlsx` | *Pn_Club* (P² … P⁶ and αPⁿ), *FirstStep* (expected months, lifetime value, hitting probabilities), *Runway_Branching* |
| figures | `SP_Fig_CH09_00_PartIII.png`, `SP_Fig_CH09_01.png` … `SP_Fig_CH09_10.png` | Part opener and chapter figures |

Fixed numbers: R3 expected months before churn (S,G,P) = 7.5/12.5/17.5; P(reach Platinum) S = 0.143, G = 0.429; lifetime value 371/914/1648 €; R2 expected shifts to maintenance from W = 21.4; weather chain [[.6,.4],[.17,.83]] with long-run rain 0.298; cash runway p = 0.55, targets 0/10: h(2) = 0.382, h(5) = 0.732, h(8) = 0.923; referral branching (0.2, 0.5, 0.3): m = 1.1, extinction 2/3.
