# SP_Code_CH14 — Chapter 14: Simulated Annealing as a Markov Chain

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch14_sa.py` | Importable: R6 data, all 720 sequences and tardiness F, swap (15) and adjacent-swap (5) neighborhoods, Metropolis transition matrices, Boltzmann law, stationary law, hitting times, SA runs, the barrier landscape TOY |
| python | `sp_ch14_figures.py` | Part V opener + Figures 14.1–14.13 |
| python | `sp_ch14_check.py` (+ `sp_ch14_check_output.txt`) | Verifies every example and exercise number |
| python | `sp_ch14_simulation.py` | `--trace` (Table 14.2), `--runs` (30 runs), `--toy ALPHA`, `--stationary T` |
| python | `R6_density_of_states.csv` | All 46 tardiness levels and their counts (Table 14.1 in full) |
| matlab | `sp_ch14_sa.m` | Enumeration, one SA run, Boltzmann probabilities |
| excel | `SP_CH14_Excel.xlsx` | *SA_Trace* (live 40-step SA trace with RAND(), any T), *Boltzmann* (density of states, P_T, acceptance table, random search), *Cooling* (T₀, α, schedule) |
| figures | `SP_Fig_CH14_00_PartV.png`, `SP_Fig_CH14_01.png` … `SP_Fig_CH14_13.png` | Part opener and chapter figures |

Fixed numbers: R6 — 720 sequences, minimum 11 (J2-J4-J6-J1-J5-J3, J4-J2-J6-J1-J5-J3), mean 34.1, 46 levels. Adjacent-swap neighborhood: no strict local minima; strict greedy is trapped at J6-J4-J2-J1-J5-J3 (12) with probability 0.167 from a random start (mean 26.2 proposals); greedy with ties always succeeds (mean 28.1; 22.1 from the start sequence). Boltzmann P(optimum) = 0.575 / 0.129 / 0.017 / 0.0028 at T = 1 / 3 / 10 / ∞. Hitting time from the start: 22.1 / 26.9 / 52.1 / 181.7 / 736.8 at T = 0 / 1 / 3 / 10 / ∞ (random search 360). Barrier landscape: best T ≈ 4 (141 steps). SA with T₀ = 10, α = 0.95, 100 iterations: success 99.4% (random starts), mean first hit 46.8; 30/30 runs from the start (mean first hit 48.7). Cooling on the barrier landscape (300 iterations): α = 0.90/0.95/0.97/0.98/0.99 → 4.5/18.5/36.6/53/81.5% success.
