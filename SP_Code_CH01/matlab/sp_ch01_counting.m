% SP_CH01 — counting tools of Level 1 (MATLAB has nchoosek; permutations need factorial)
Pnk = @(n,k) factorial(n)/factorial(n-k);    % permutations
Cnk = @(n,k) nchoosek(n,k);                  % combinations
fprintf('Example 1.16: P(12,4) = %d\n', Pnk(12,4));
fprintf('Example 1.17: C(8,3)  = %d\n', Cnk(8,3));
fprintf('Example 1.20: P(no damaged) = %.4f\n', Cnk(17,4)/Cnk(20,4));
fprintf('Example 1.21: P(share rest day, 5 drivers) = %.4f\n', 1 - Pnk(7,5)/7^5);
