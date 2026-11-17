% SP_CH13 — Brownian motion: paths, first passage, GBM, OU (teaching version)
mu=0.1; s=sqrt(0.99);                     % R4 cash, thousand € per day
T=90; a=15; sT=s*sqrt(T);
p_end = normcdf((-a-mu*T)/sT);
p_during = normcdf((-a-mu*T)/sT) + exp(-2*mu*a/s^2)*normcdf((-a+mu*T)/sT);
fprintf('start 5k, limit -10k, 90 days: end %.4f  during %.4f  ever %.4f\n', p_end, p_during, exp(-2*mu*a/s^2));
k=2*mu/s^2; fprintf('runway BM (a=2,b=8): %.4f\n', (1-exp(k*2))/(exp(-k*8)-exp(k*2)));
S0=1.6; m=0.04; v=0.25; t=1; fprintf('fuel: mean %.3f median %.3f P(>2) %.3f\n', S0*exp(m*t), S0*exp((m-v^2/2)*t), 1-normcdf((log(2/S0)-(m-v^2/2)*t)/(v*sqrt(t))));
rng(1311); dt=0.1; n=T/dt; X=5+cumsum(mu*dt+s*sqrt(dt)*randn(20000,n),2); fprintf('simulated (dt=0.1): %.4f\n', mean(min(X,[],2)<=-10));
