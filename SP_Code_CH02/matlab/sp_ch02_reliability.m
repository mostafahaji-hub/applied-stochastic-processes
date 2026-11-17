% SP_CH02 — series / parallel / mixed reliability (Examples 2.23–2.26)
series   = @(r) prod(r);  parallel = @(r) 1 - prod(1 - r);
fprintf('Series of four 0.95: %.4f\n', series([0.95 0.95 0.95 0.95]));
fprintf('Three parallel 0.90: %.4f\n', parallel([0.9 0.9 0.9]));
fprintf('Mixed system: %.4f\n', series([parallel([series([0.9 0.9]) 0.85]) 0.98]));
n = find(0.2.^(1:10) <= 0.01, 1); fprintf('Generators needed for 99%%: %d\n', n);
