% SP_CH17 — Monte Carlo basics (teaching version)
x=7; seq=x; for k=1:16, x=mod(5*x+3,16); seq(end+1)=x; end; disp(seq)       % LCG, period 16
rng(172); u=rand(10000,1);
tire=12*(-log(1-u)).^0.4; fprintf('mean tire life %.3f (exact 10.647), SE %.3f\n',mean(tire),std(tire)/sqrt(numel(u)));
rain=rand(1000,1)<0.3; lateD=rain.*(rand(1000,1)<0.40)+(~rain).*(rand(1000,1)<0.157);
p=mean(lateD); se=sqrt(p*(1-p)/1000); fprintf('P(late) %.3f, 95%% interval [%.3f, %.3f]\n',p,p-1.96*se,p+1.96*se);
u=rand(50,1); anti=mean(0.5*(12*(-log(1-u)).^0.4+12*(-log(u)).^0.4)); fprintf('antithetic estimate %.3f\n',anti);
fprintf('runs for +-0.005 on P(late): %d\n',ceil(1.96^2*0.23*0.77/0.005^2));
