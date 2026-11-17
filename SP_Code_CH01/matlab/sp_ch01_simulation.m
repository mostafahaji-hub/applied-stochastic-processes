% SP_CH01 — Level 1: probability as a long-run frequency (teaching version)
% Simulates n days; each day is "late" with probability p. Plots the running fraction of late days.
p = 0.30; n = 1000; rng(7);                 % parameters and seed (change them and watch the curve)
late = rand(1, n) < p;                       % 1 = late, 0 = on time
runfreq = cumsum(late) ./ (1:n);             % fraction of late days after each day
fprintf('after %4d days: %.4f\n', [10 100 1000; runfreq([10 100 1000])]);
semilogx(1:n, runfreq, 'LineWidth', 1.8); hold on; yline(p, '--', 'LineWidth', 2);
xlabel('number of simulated days (log scale)'); ylabel('fraction of late days so far');
title('Probability as a long-run frequency'); legend('running frequency', 'true probability'); grid on
