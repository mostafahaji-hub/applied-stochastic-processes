% SP_CH06 — sample paths of the building blocks (teaching version)
rng(6); n=30;
bern = rand(1,n) < 0.23;                  % Bernoulli process (van 7 late?)
count = cumsum(bern);                      % its counting process
rw = cumsum(1000*(2*(rand(1,60)<0.5)-1));  % cash random walk ±1000
ar = zeros(1,200); e = 40*randn(1,200);    % demand with memory 0.6
for t = 2:200, ar(t) = 0.6*ar(t-1) + e(t); end
fprintf('AR(1): sample sd %.1f (theory 50)  lag-1 corr %.2f (theory 0.6)\n', std(ar), corr(ar(1:end-1)', ar(2:end)'));
subplot(3,1,1); stairs(0:n, [0 count]); title('Counting process of a Bernoulli process');
subplot(3,1,2); plot(0:60, [0 rw]); title('Cash random walk');
subplot(3,1,3); plot(500+ar); yline(500,'--'); title('Stationary demand with memory 0.6');
