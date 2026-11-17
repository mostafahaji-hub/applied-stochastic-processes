% SP_CH15 — Wright–Fisher fixation probabilities and one GA run on R6 (teaching version)
N=10; gO=46; gM=43; rules={'neutral','roulette','tournament'};
for r=1:3
  M=zeros(N+1);
  for k=0:N
    x=k/N; switch r, case 1, p=x; case 2, p=gO*x/(gO*x+gM*(1-x)+eps*(k==0)); case 3, p=1-(1-x)^2; end
    M(k+1,:)=binopdf(0:N,N,p);
  end
  Q=M(2:N,2:N); R=M(2:N,[1 N+1]); B=(eye(N-1)-Q)\R; fprintf('%-10s fixation from one copy: %.4f\n',rules{r},B(1,2));
end
% one GA run: N=10, tournament, OX, adjacent-swap mutation, elitism
p=[6 3 8 2 5 4]; d=[14 8 20 6 18 12]; tard=@(s) sum(max(0,cumsum(p(s))-d(s)));
rng(158); pop=zeros(10,6); for i=1:10, pop(i,:)=randperm(6); end
for g=1:21
  f=arrayfun(@(i) tard(pop(i,:)),1:10); [~,b]=min(f); new=pop(b,:);
  while size(new,1)<10
    i=randi(10,1,2); [~,w]=min(f(i)); P1=pop(i(w),:); i=randi(10,1,2); [~,w]=min(f(i)); P2=pop(i(w),:);
    child=P1;
    if rand<0.9, ab=sort(randi(6,1,2)); seg=P1(ab(1):ab(2)); rest=P2(~ismember(P2,seg)); child=zeros(1,6); child(ab(1):ab(2))=seg; child(child==0)=rest; end
    if rand<0.2, k=randi(5); child([k k+1])=child([k+1 k]); end
    new=[new; child];
  end
  pop=new;
end
f=arrayfun(@(i) tard(pop(i,:)),1:10); fprintf('best after 21 generations: %d\n',min(f));
