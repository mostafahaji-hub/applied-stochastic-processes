# SP_Code_CH15 — Chapter 15: Genetic Algorithms as Stochastic Processes

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch15_ga.py` | Importable: OX crossover, one-point crossover, adjacent-swap mutation, binary tournament, `ga_run` (with elitism option and population recording), position (heat-map) matrix, Wright–Fisher matrices, absorption and stationary laws, `hand_trace` (uses `sp_ch14_sa.py`, included) |
| python | `sp_ch15_figures.py` | Figures 15.1–15.11 (`A` part: diagrams, Wright–Fisher, heat maps, diversity, 30 runs; `B` part: parameter sweep, time-to-target) |
| python | `sp_ch15_check.py` (+ `sp_ch15_check_output.txt`) | Verifies every example and exercise number |
| python | `sp_ch15_simulation.py` | `--trace`, `--runs`, `--ga N G PC PM [--noelite]`, `--wf RULE N MU [--elite]`, `--heat` |
| matlab | `sp_ch15_ga.m` | Wright–Fisher fixation probabilities and one GA run (teaching version; not executed in the author environment) |
| excel | `SP_CH15_Excel.xlsx` | *Selection* (roulette vs tournament, expected copies), *OX_Mutation* (live OX and mutation calculator with tardiness), *WrightFisher* (11-state chain, 60 generations) |
| figures | `SP_Fig_CH15_01.png` … `SP_Fig_CH15_11.png` | Chapter figures |

Fixed numbers: hand trace (seed 2) from P₀ = {36, 33, 25, 21, 56, 24} (mean 32.5) to {21, 35, 20, 25, 24, 21} (mean 24.3, best 20, 5 distinct). Wright–Fisher, N = 10, EDD (11) vs SPT (14): fixation from one copy — neutral 0.10, roulette 0.171, tournament 0.817, elitism 1 (mean 4.43 generations with tournament, 14.6 with roulette); N = 20: 0.136 / 0.807; N = 50: 0.127 / 0.801. Mutation μ = 0.01: roulette P(no EDD) 0.149 (mean share 0.70), tournament 1.3e−9 (0.99). GA on R6 (N = 10, p_c = 0.9, p_m = 0.2, elitism, 21 generations = 199 evaluations): success 89.5%, mean first hit 86.1; without mutation 22.9%; without elitism 88.6% (220 evaluations); p_m = 0.4: 97.7%; N = 20, 10 generations: 94.6%. Heat map generation 10: J3 last 0.88, J5 fifth 0.70, J1 fourth 0.60, J6 third 0.55. Time to target at 100 evaluations: greedy 1.00, SA 0.92, GA (p_m 0.4) 0.78, GA (0.2) 0.63, random 0.24.
