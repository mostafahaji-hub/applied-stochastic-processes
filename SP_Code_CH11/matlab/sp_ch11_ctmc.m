% SP_CH11 — CTMC machine 3: stationary law, P(t), two-state formula, age replacement (teaching version)
Q=[-0.17 0.12 0.05; 3.0 -3.5 0.5; 1.0 0 -1.0];
A=[Q'; ones(1,3)]; pi=A\[0;0;0;1]; fprintf('pi = %s\n', mat2str(pi',3));
disp('P(5) row W:'); disp(expm(Q*5)(1,:))
lam=1/7; mu=1; t=1:7; pWW = mu/(lam+mu) + lam/(lam+mu)*exp(-(lam+mu)*t); fprintf('pWW(t) = %s\n', mat2str(pWW,3));
k=2.5; eta=12; cp=80; cf=600; F=@(x) 1-exp(-(x/eta).^k);
for T=[4 5 6 8 10 12], EL=integral(@(x) 1-F(x),0,T); fprintf('T=%2d: cost rate %.2f\n',T,(cp*(1-F(T))+cf*F(T))/EL); end
