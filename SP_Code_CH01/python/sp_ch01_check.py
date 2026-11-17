"""SP_CH01 — number checks for every example and exercise of Level 1 (run: python sp_ch01_check.py)."""
from math import comb, perm, factorial
from itertools import product
def show(label, value): print(f"{label:<55} {value}")
# --- counting helpers used in the chapter ---
def P(n, k): return perm(n, k)
def C(n, k): return comb(n, k)
def count_pins(digits=4):
    """Example 1.19: brute-force check of 10^4 and P(10,4)."""
    all_pins = list(product(range(10), repeat=digits))
    no_repeat = [p for p in all_pins if len(set(p)) == digits]
    return len(all_pins), len(no_repeat)
show("Ex 1.6/1.12  F∪E, neither, exactly one", (0.30+0.25-0.10, 1-0.45, 0.45-0.10))
show("Ex 1.13      J∪S∪M", round(0.20+0.15+0.10-0.05-0.04-0.03+0.01, 4))
show("Ex 1.15      locker codes 6^3*10^2", 6**3*10**2)
show("Ex 1.16      4!, P(12,4)", (factorial(4), P(12, 4)))
show("Ex 1.17/1.18 C(8,3), C(5,2)*C(8,2)", (C(8, 3), C(5, 2)*C(8, 2)))
show("Ex 1.19      pins total, no repeat (brute force)", count_pins())
show("Ex 1.20      C(20,4), C(17,4), P(no damaged)", (C(20, 4), C(17, 4), round(C(17, 4)/C(20, 4), 4)))
show("Ex 1.21      5 drivers all different / share", (round(P(7, 5)/7**5, 4), round(1-P(7, 5)/7**5, 4)))
show("Ex 1.22      Sara at 1; Sara&Reza at {1,2}", (round(factorial(7)/factorial(8), 4), round(2*factorial(6)/factorial(8), 4)))
show("Ex 1.23      raffle C(39,4)/C(40,5)", round(C(39, 4)/C(40, 5), 4))
show("Exercise 1.12 k needed (first k with P(none)<=0.10)", next(k for k in range(1, 21) if C(17, k)/C(20, k) <= 0.10))
show("Exercise 1.14 6 drivers share", round(1-P(7, 6)/7**6, 4))
show("Exercise 1.15 adjacent vans", 2*factorial(4)/factorial(5))
show("Exercise 1.16 Arman wins; Arman & Sara", (C(29, 5)/C(30, 6), round(C(28, 4)/C(30, 6), 4)))
show("Exercise 1.18 none / exactly one / at least two", (round(C(21, 5)/C(25, 5), 4), round(4*C(21, 4)/C(25, 5), 4), round(1-C(21, 5)/C(25, 5)-4*C(21, 4)/C(25, 5), 4)))
# --- v2 additions: sum rule, repeated items, conditional probability ---
show("Ex 1.15      sum rule 8+5; pairs 8*5", (8+5, 8*5))
show("Ex 1.18      7!/(3!4!) and C(7,3)", (factorial(7)//(factorial(3)*factorial(4)), C(7, 3)))
show("Ex 1.28      P(late|rain), P(late|dry), total", (24/60, round(22/140, 4), round(0.3*24/60+0.7*22/140, 4)))
show("Ex 1.29      P(F|E), P(E|F)", (0.10/0.25, round(0.10/0.30, 4)))
show("Ex 1.30      3/20*2/19 vs C(3,2)/C(20,2)", (round(3/20*2/19, 4), round(C(3, 2)/C(20, 2), 4)))
show("Ex 1.32      P(rain|late)", round(0.12/0.23, 4))
show("Exercise 1.11(c)(d) 7!/(4!2!1!), 12+3", (factorial(7)//(factorial(4)*factorial(2)), 15))
show("Exercise 1.17 P(late|big), P(late|small), P(late), P(big|late)", (36/120, 28/280, 64/400, 36/64))
show("Exercise 1.18 both good, good-then-bad, exactly one", (round(6/10*5/9, 4), round(6/10*4/9, 4), round(2*6/10*4/9, 4)))
