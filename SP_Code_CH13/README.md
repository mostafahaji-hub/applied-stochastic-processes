# SP_Code_CH13 — Chapter 13: Brownian Motion and Gaussian Processes (with a Taste of Stochastic Calculus)

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch13_brownian.py` | Importable: bm_paths, p_end_below, p_hit_below, p_ever_below, p_up_before_down, first_passage_cdf_up, gbm_stats, gbm_prob_above, ou_forecast, euler_maruyama, hit_freq |
| python | `sp_ch13_figures.py` | Part IV opener + Figures 13.1–13.12 (includes the monitoring-bias simulation) |
| python | `sp_ch13_check.py` | Verifies every example and exercise number |
| python | `sp_ch13_simulation.py` | Monitoring bias (default, `--start X`), `--qv`, `--gbm`, `--ou` |
| matlab | `sp_ch13_brownian.m` | First passage, two-barrier probability, GBM, simulated hitting probability |
| excel | `SP_CH13_Excel.xlsx` | *BM_Drift_Hitting* (end vs during vs ever; two barriers; time to target), *GBM_OU* (fuel price; OU forecast), *OnePath* (live 90-day path with running minimum) |
| figures | `SP_Fig_CH13_00_PartIV.png`, `SP_Fig_CH13_01.png` … `SP_Fig_CH13_12.png` | Part opener and chapter figures |

Fixed numbers (thousand €, days): fair cash σ = 1; R4 cash μ = 0.1, σ = √0.99 = 0.995. From 20: day 90 mean 29, SD 9.44, P(<10) = 0.022. From 5, limit −10 (a = 15): end 0.0055, during 0.0182, ever 0.048; daily monitoring 0.0154. From 10 (a = 20): end 0.0011, during 0.0032, ever 0.0176. Runway BM 0.383 (discrete 0.382); from 5 of 10: 0.733 (0.732). Time to +10 target: mean 100, SD 99.5 days, P(>200) = 0.114. Cumulative demand deviation σ = 80/√day: buffer 1,000 in 30 days during 0.0225, end 0.0112. Fuel GBM S₀ = 1.60, μ = 4%, σ = 25%: 1-year mean 1.665, median 1.614, P(>2) = 0.196, q95 = 2.44. OU demand θ = −ln 0.6 = 0.511/day, stationary SD 50, half-life 1.36 days. Project bridge (90 days, σ = 1): day-45 SD 4.74.
