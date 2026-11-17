# SP_Code_CH04 — Chapter 4: Continuous Random Variables and Their Distributions

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch04_figures.py` | Figures 4.1–4.12 (300 dpi, book palette) + number checks |
| python | `sp_ch04_check.py` | Verifies every example and exercise number (uniform, exponential, Erlang, normal, lognormal, Weibull, triangular) |
| python | `sp_ch04_simulation.py` | Example 4.24 (normal demand), Exercise 4.19 (`--exp`, `--clt`) |
| matlab | `sp_ch04_normal_exponential.m` | Teaching version with normcdf, norminv, gamcdf, randn |
| excel | `SP_CH04_Excel.xlsx` | *Normal* (z, Φ, percentile, safety stock), *Exponential_Erlang* (tail, Erlang via POISSON, service-level time), *Uniform_Triangular* |
| figures | `SP_Fig_CH04_01.png` … `SP_Fig_CH04_12.png` | Chapter figures |

Nava data fixed in this chapter: daily demand N(500, 80²); call rate 3/min ⇒ waits Exp(3); van-7 arrival window U(8, 20) min after 8:00; board lifetime Exp(mean 8 months); tire life Weibull(k = 2.5, η = 12 months); order value lognormal(median 60 €, s = 0.6); lead-time demand N(1000, 150²); project activity triangular(3, 5, 10).
