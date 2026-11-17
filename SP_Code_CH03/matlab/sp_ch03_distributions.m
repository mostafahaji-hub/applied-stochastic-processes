% SP_CH03 — the six discrete distributions with MATLAB's pdf/cdf functions (teaching version)
fprintf('Binomial B(12,0.23): P(X=3)=%.3f  P(X>3)=%.3f\n', binopdf(3,12,0.23), 1-binocdf(3,12,0.23));
fprintf('Geometric p=0.4 (MATLAB counts failures): P(first answer on 3rd)=%.3f\n', geopdf(2,0.4));
fprintf('Negative binomial r=3,p=0.4: P(3rd success on 5th)=%.3f\n', nbinpdf(2,3,0.4));
fprintf('Hypergeometric N=20,D=3,n=4: P(X=0)=%.3f\n', hygepdf(0,20,3,4));
fprintf('Poisson lambda=3: P(X>=5)=%.3f\n', 1-poisscdf(4,3));
late = binornd(12,0.23,1,10000); fprintf('Simulation mean %.3f var %.3f\n', mean(late), var(late,1));
