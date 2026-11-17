% SP_CH08 — M/M/1, M/M/c (Erlang C), Erlang B (teaching version)
lam=3; mu=2/3; a=lam/mu;
for c=5:8
    rho=a/c; s=sum(a.^(0:c-1)./factorial(0:c-1)); p0=1/(s+a^c/factorial(c)/(1-rho)); C=a^c/factorial(c)*p0/(1-rho);
    Lq=C*rho/(1-rho); Wq=Lq/lam; SL=1-C*exp(-(c*mu-lam)*0.5);
    fprintf('c=%d: rho=%.2f P(wait)=%.3f Wq=%.1f s  P(Wq<=30s)=%.3f\n',c,rho,C,60*Wq,SL);
end
B=@(a,c) (a^c/factorial(c))/sum(a.^(0:c)./factorial(0:c)); fprintf('Erlang B(10,4.5)=%.4f\n',B(4.5,10));
