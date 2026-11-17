# Applied Stochastic Processes for Management and Industrial Engineering — Companion Code

Companion code for the book *Applied Stochastic Processes for Management and Industrial Engineering: From Probability to Markov Chains, Metaheuristics, and Simulation—Through One Company’s Story* by Mostafa Hajiaghaei-Keshteli and Fatemeh Gholian-Jouybari (Independently published, 2026; ISBN 9798142697769).

Every number, table, and figure in the book can be reproduced with the code in this repository.

## Structure

One folder per chapter, `SP_Code_CH01` … `SP_Code_CH19`:

| Folder | Contents |
|---|---|
| `python/` | The chapter module; `sp_chxx_check.py`, which reproduces every number of the chapter (recorded output alongside); `sp_chxx_simulation.py` with the modes used in the Code examples and exercises (`--help` lists them); `sp_chxx_figures.py`, which draws every figure |
| `excel/` | Live workbooks for the hand calculations (tables, matrices, policies); no macros |
| `matlab/` | Teaching versions of the main computations, written for reading and adapting; they were not executed for the book—the Python scripts are the reference |
| `figures/` | Every figure of the chapter at 300 dpi, identical to the printed book |
| `README.md` | The files of the chapter and its fixed numbers |

## Requirements

Python 3 with `numpy`, `scipy`, and `matplotlib`. Every simulation runs with a recorded seed, so the numbers in the text are reproduced exactly; a different seed gives a nearby value within the standard error reported in the text (Chapter 17).

Some scripts were written with absolute working paths of the form `/home/claude/chXX/code` and `/home/claude/chXX/fig`; if your setup differs, edit the `OUT`/`sys.path` lines at the top of the figure scripts, or create those folders.

## Reproducing a number from the book

Find the example or exercise in the chapter; the script and seed are named in the text (for example, `sp_ch18_simulation.py --audit`, seed 184). Run the same command; the output matches the printed number.

## Changes

See `CHANGELOG.md`.

© 2026 Mostafa Hajiaghaei-Keshteli and Fatemeh Gholian-Jouybari.
