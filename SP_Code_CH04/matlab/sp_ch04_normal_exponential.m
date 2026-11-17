% SP_CH04 — normal and exponential calculations (teaching version)
mu=500; sigma=80;
fprintf('P(D>600) = %.3f\n', 1-normcdf(600,mu,sigma));
fprintf('95%% capacity = %.0f\n', norminv(0.95,mu,sigma));
lam=3;  fprintf('Exponential rate 3/min: P(T>1) = %.3f, P(T<0.5) = %.3f\n', exp(-lam*1), 1-exp(-lam*0.5));
fprintf('Erlang k=3: P(T3<=1) = %.3f\n', gamcdf(1,3,1/lam));
D=mu+sigma*randn(1,20000); fprintf('Simulated P(D>600) = %.3f\n', mean(D>600));
