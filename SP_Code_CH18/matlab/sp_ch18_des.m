% SP_CH18 — a minimal discrete-event simulation of an M/M/c queue with an event list (teaching version)
rng(184); lam=3; mu=2/3; c=5; T=7500; t=0; busy=0; q=[]; waits=[];
nextA=exprnd(1/lam); dep=inf(1,c);                       % departure time of each server (inf = idle)
while t<T
  [td,k]=min(dep);
  if nextA<td                                            % arrival event
    t=nextA; nextA=t+exprnd(1/lam);
    j=find(isinf(dep),1);
    if isempty(j), q(end+1)=t; else dep(j)=t+exprnd(1/mu); if t>500, waits(end+1)=0; end, end
  else                                                    % departure event on server k
    t=td;
    if isempty(q), dep(k)=inf; else a=q(1); q(1)=[]; if a>500, waits(end+1)=t-a; end, dep(k)=t+exprnd(1/mu); end
  end
end
fprintf('mean wait in queue %.1f s (Erlang C 137.2 s)\n',60*mean(waits));
