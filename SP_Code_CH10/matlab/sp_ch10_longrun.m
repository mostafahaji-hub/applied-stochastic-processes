% SP_CH10 — stationary distribution and long-run cost (teaching version)
P2=[.86 .10 .04; .70 .20 .10; .50 0 .50];
n=size(P2,1); A=[P2'-eye(n); ones(1,n)]; b=[zeros(n,1);1]; pi=A\b;
fprintf('pi = %s   return times = %s\n', mat2str(pi',3), mat2str((1./pi)',3));
fprintf('long-run cost per shift = %.1f\n', pi'*[0;800;1200]);
Pb=[.80 .15 .05; .10 .75 .15; .05 .20 .75]; A=[Pb'-eye(3); ones(1,3)]; fprintf('brand shares = %s\n', mat2str((A\[0;0;0;1])',3));
disp('P2^10:'); disp(P2^10)
