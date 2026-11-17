% SP_CH12 — hazard rates, k-of-n, line availability, age replacement (teaching version)
t=1:24; h_tire=(2.5/12)*(t/12).^1.5; h_bear=(3/20)*(t/20).^2; fprintf('tire h(6)=%.3f h(12)=%.3f; bearing h(10)=%.3f\n',h_tire(6),h_tire(12),h_bear(10));
R=0.9; R2of3=3*R^2*(1-R)+R^3; fprintf('2-of-3 with R=0.9: %.3f\n',R2of3);
% line: states (n others failed 0..3, m3 failed 0/1), one crew, machine 3 first
lo=0.05; l3=1/7; mu=1; Q=zeros(8); idx=@(n,m) n+4*m+1;
for n=0:3, for m=0:1, i=idx(n,m);
  if n<3, Q(i,idx(n+1,m))=Q(i,idx(n+1,m))+(3-n)*lo; end
  if m==0, Q(i,idx(n,1))=Q(i,idx(n,1))+l3; end
  if m==1, Q(i,idx(n,0))=Q(i,idx(n,0))+mu; elseif n>0, Q(i,idx(n-1,m))=Q(i,idx(n-1,m))+mu; end
  Q(i,i)=-sum(Q(i,:)); end, end
pi=[Q'; ones(1,8)]\[zeros(8,1);1]; fprintf('line availability (1 crew) = %.3f\n',pi(1));
k=2.5; eta=12; F=@(x) 1-exp(-(x/eta).^k);
for T=[4 5 6 8], EL=integral(@(x) 1-F(x),0,T); fprintf('age T=%d: %.2f €/month\n',T,(80*(1-F(T))+600*F(T))/EL); end
