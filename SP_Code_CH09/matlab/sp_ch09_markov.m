% SP_CH09 — Markov chains: n-step, first-step analysis (teaching version)
P3=[.70 .10 0 .20; .05 .75 .10 .10; 0 .06 .90 .04; 0 0 0 1];   % R3 club
disp('P3^2 row Silver'); disp(P3(1,:)*P3)
Q=P3(1:3,1:3); N=inv(eye(3)-Q);
fprintf('expected months before churn (S,G,P): %s\n', mat2str((N*ones(3,1))',3));
fprintf('lifetime value: %s\n', mat2str((N*[20;45;110])',4));
A=[1-.70 -.10; -.05 1-.75]; h=A\[0; .10]; fprintf('P(reach Platinum) from S,G: %.4f %.4f\n', h);
P2=[.86 .10 .04; .70 .20 .10; .50 0 .50]; m=[.14 -.10; -.70 .80]\[1;1]; fprintf('shifts to maintenance from W,S: %.2f %.2f\n', m);
