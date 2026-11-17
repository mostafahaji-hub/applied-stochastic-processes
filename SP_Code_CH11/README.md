# SP_Code_CH11 — Chapter 11: Markov Processes in Continuous Time, and Long-Run Averages

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch11_ctmc.py` | Importable: Q3 (machine 3 rates), stationary_Q, transition (expm), jump_chain, two_state, age_replacement_rate, simulate_ctmc |
| python | `sp_ch11_figures.py` | Figures 11.1–11.13 + number checks |
| python | `sp_ch11_check.py` | Verifies every example and exercise number |
| python | `sp_ch11_simulation.py` | Example 11.20; `--jumps` (jump-chain law), `--renewal` (Weibull tire lives) |
| matlab | `sp_ch11_ctmc.m` | πQ = 0, expm, two-state formula, age-replacement cost rates |
| excel | `SP_CH11_Excel.xlsx` | *CTMC3* (rates → holding times, jump chain, π, shift cost), *TwoState_Renewal* (p_WW(t); Weibull mean, renewal-reward, age replacement) |
| figures | `SP_Fig_CH11_01.png` … `SP_Fig_CH11_13.png` | Chapter figures |

Fixed numbers: machine 3 continuous rates (per shift) W→S 0.12, W→M 0.05, S→W 3.0, S→M 0.5, M→W 1.0 ⇒ π = (0.908, 0.031, 0.061); two-state (1/7, 1) availability 7/8; two servers (rates 0.1, 1/15, repair 0.5) ⇒ ≥1 down 27.9% of time; Yule 0.2/day from 3 ⇒ E[N(10)] = 22.2; tandem A (μ=4) → B (μ=3.5) at λ=3 ⇒ L = 3 + 6; tire Weibull(2.5,12): mean 10.65 months, 54 replacements/year for 48 tires, run-to-failure 56.4 €/month, age replacement at T ≈ 5 months 27.9 €/month; bearing Weibull(3,20): T ≈ 10 months 24.6 €/month.
