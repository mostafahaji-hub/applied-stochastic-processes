% SP_CH14 — simulated annealing on R6 with adjacent swaps (teaching version)
p=[6 3 8 2 5 4]; d=[14 8 20 6 18 12];
tard=@(s) sum(max(0, cumsum(p(s)) - d(s)));
P=perms(1:6); F=zeros(size(P,1),1); for i=1:size(P,1), F(i)=tard(P(i,:)); end
fprintf('720 sequences: min %d (count %d), mean %.2f\n', min(F), sum(F==min(F)), mean(F));
rng(149); T0=10; alpha=0.95; x=1:6; fx=tard(x); best=fx;
for k=0:99
  T=T0*alpha^k; m=randi(5); y=x; y([m m+1])=x([m+1 m]); fy=tard(y); D=fy-fx;
  if D<=0 || rand<exp(-D/T), x=y; fx=fy; end
  best=min(best,fx);
end
fprintf('one SA run: final %d, best %d\n', fx, best);
% Boltzmann probability of the optimum
for T=[1 3 10], w=exp(-(F-min(F))/T); fprintf('T=%2d: P(opt)=%.4f\n',T,sum(w(F==min(F)))/sum(w)); end
