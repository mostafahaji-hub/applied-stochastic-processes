# SP_Code_CH08 — Chapter 8: Queueing Theory: Why We Wait and How Long

| Folder | File | What it does |
|---|---|---|
| python | `sp_ch08_queue.py` | Importable formulas: mm1, mm1k, mmc (Erlang C), pwait_gt, erlangB, mg1 (P–K), finite_source |
| python | `sp_ch08_figures.py` | Figures 8.1–8.12 + number checks (includes the 1,000,000-call M/M/5 simulation) |
| python | `sp_ch08_check.py` | Verifies every example and exercise number |
| python | `sp_ch08_simulation.py` | Discrete-event M/M/c simulation; `--mm1`, `--deterministic`, `--abandon` modes |
| matlab | `sp_ch08_queues.m` | Staffing table and Erlang B |
| excel | `SP_CH08_Excel.xlsx` | *MMc* (Erlang C staffing table with costs), *MM1_MG1_ErlangB* |
| figures | `SP_Fig_CH08_01.png` … `SP_Fig_CH08_12.png` | Chapter figures |

R1 data used: λ = 3/min (4/min peak), service Exp(mean 1.5 min ⇒ μ = 2/3), 5 operators ⇒ ρ = 0.9, Wq = 137 s, P(wait) = 0.76; 6 ⇒ 25 s; 7 ⇒ 8 s (90/30 met); 10 lines for 1% blocking at a = 4.5; cost 25 €/h per operator, 2 €/customer-minute waiting ⇒ optimum 8 (7 close). R2: 4 machines, failure 1/7 per shift, 1 repairer at 1 per shift.
