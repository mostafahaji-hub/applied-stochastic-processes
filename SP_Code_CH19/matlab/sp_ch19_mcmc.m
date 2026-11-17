% SP_CH19 — random-walk Metropolis for the failure rate of machine 3 (teaching version)
a0=2; b0=10; x=12; t=84;                                   % prior Gamma(2,10); 12 failures in 84 shifts
logp=@(l) (l>0).*((a0+x-1)*log(max(l,eps))-(b0+t)*l)+(l<=0).*(-1e300);
rng(1905); n=21000; l=0.5; lp=logp(l); chain=zeros(n,1); acc=0;
for i=1:n
  y=l+0.04*randn; ly=logp(y);
  if log(rand)<ly-lp, l=y; lp=ly; acc=acc+1; end
  chain(i)=l;
end
s=chain(1001:end);
fprintf('acceptance %.2f, posterior mean %.4f (exact %.4f), 95%% [%.4f, %.4f]\n',acc/n,mean(s),(a0+x)/(b0+t),quantile(s,0.025),quantile(s,0.975));
