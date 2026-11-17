# SP_Code_CH05 — Chapter 5: Several Random Variables and the Art of Conditioning

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch05_figures.py` | Figures 5.1–5.11 + number checks |
| python | `sp_ch05_check.py` | Verifies every example and exercise number (joint tables, covariance, tower rule, total variance, random sums, LLN/CLT) |
| python | `sp_ch05_simulation.py` | Mixture variance (Ex. 5.12), CLT panels (`--clt`), binomial tail (`--binom`) |
| matlab | `sp_ch05_conditioning.m` | Joint-table statistics, tower rule, total variance |
| excel | `SP_CH05_Excel.xlsx` | *JointTable* (marginals, conditionals, Cov, ρ, Var(X+Y)), *TowerRule_TotalVar*, *RandomSum_CLT* |
| figures | `SP_Fig_CH05_01.png` … `SP_Fig_CH05_11.png` | Chapter figures |

Nava data fixed in this chapter: joint pmf of late city vans X (of 2) and complaints Y per day — rows (0.45,0.10,0.02),(0.15,0.12,0.05),(0.03,0.05,0.03); E[X]=0.54, E[Y]=0.47, Cov=0.186, ρ=0.41. Rain/dry mixture of 12 vans: E=2.76, Var=3.76. Daily revenue: N~Pois(500) orders × value (mean 71.8, SD 48 €) ⇒ 35,900 ± 1,931 €. Monthly repairs: Pois(6) × (300 ± 200 €) ⇒ 1,800 ± 883 €. Two city routes: SD 30 each. Call timing sample: n=100, mean 21 s, SD 5 s.
