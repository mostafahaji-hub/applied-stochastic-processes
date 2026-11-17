% SP_CH02 — Bayes' rule with natural frequencies and a Monte Carlo check (teaching version)
base=0.03; sens=0.95; fp=0.08; N=100000; rng(22);
post = base*sens/(base*sens+(1-base)*fp);                 % formula (2.5)
defective = rand(1,N) < base;                             % true states
flagged = (defective & rand(1,N) < sens) | (~defective & rand(1,N) < fp);
fprintf('Bayes: %.4f   simulation: %.4f  (flagged %d)\n', post, mean(defective(flagged)), sum(flagged));
