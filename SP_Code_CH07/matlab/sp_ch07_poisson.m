% SP_CH07 — Poisson process: counts, gaps, superposition, thinning (teaching version)
lam=3; rng(77);
fprintf('P(N(5)=12) = %.3f   P(S_3>1) = P(N(1)<=2) = %.3f\n', poisspdf(12,5*lam), poisscdf(2,lam));
gaps = exprnd(1/lam,1,60); S = cumsum(gaps); N5 = sum(S<=5); fprintf('one simulated N(5) = %d\n', N5);
counts = arrayfun(@(k) sum(cumsum(exprnd(1/lam,1,60))<=5), 1:10000); fprintf('mean %.2f var %.2f\n', mean(counts), var(counts,1));
typ = rand(1,numel(S)) < 0.3; fprintf('complaints among %d arrivals: %d (expected %.1f)\n', numel(S), sum(typ), 0.3*numel(S));
