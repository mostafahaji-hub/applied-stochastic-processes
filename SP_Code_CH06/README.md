# SP_Code_CH06 — Chapter 6: What Is a Stochastic Process? (and Meet the Nava Company)

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch06_figures.py` | Part II opener figure + Figures 6.1–6.13 + number checks |
| python | `sp_ch06_check.py` | Verifies every example and exercise number |
| python | `sp_ch06_simulation.py` | Example 6.21 (cash random walk, 10,000 paths); `--r4` for the R4 first-passage comparison |
| matlab | `sp_ch06_processes.m` | Sample paths of Bernoulli/counting, random walk, AR(1) |
| excel | `SP_CH06_Excel.xlsx` | *RandomWalk* (one live path + m(t), SD(t)), *AR1_Demand* (200-day path, stationary sd, ρ(k)), *R6_Scheduling* (total tardiness of any sequence) |
| figures | `SP_Fig_CH06_00_PartII.png`, `SP_Fig_CH06_01.png` … `SP_Fig_CH06_13.png` | Part opener and chapter figures |

## Nava reference problems (fixed from this chapter on)
- **R1 call center:** arrivals 3/min (4/min peak), service Exp(mean 1.5 min), 5 operators, 10% abandon after 2 min, 3 servers (0.90/day).
- **R2 packing line:** 4 machines in series (0.95/shift); machine 3 shift-to-shift matrix W/S/M = [[.86,.10,.04],[.70,.20,.10],[.50,0,.50]]; up-time Exp(7 shifts), repair Exp(1 shift); downtime 400 €/h.
- **R3 customer club:** monthly matrix Silver/Gold/Platinum/Churned = [[.70,.10,0,.20],[.05,.75,.10,.10],[0,.06,.90,.04],[0,0,0,1]]; monthly value 20/45/110 €; acquisition 60 €.
- **R4 demand & cash:** demand N(500,80²) or AR(1) φ=0.6, σ=40 (sd 50); cash walk ±1,000 with p=0.55, start 20,000, credit limit −10,000.
- **R5 repair shop:** board Exp(8 mo), tire Weibull(2.5,12 mo), bearing Weibull(3,20 mo), parts box 10 with 2 defective, lead times Exp(4)/Exp(6) days, tire costs 80 € planned / 200 €+400 € failure.
- **R6 scheduling:** jobs J1–J6 with p = (6,3,8,2,5,4), due = (14,8,20,6,18,12); objective total tardiness; 720 sequences; J4-J2-J6-J1-J5-J3 gives 11.
