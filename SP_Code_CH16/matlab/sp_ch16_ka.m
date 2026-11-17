% SP_CH16 v2 — textbook Keshtel algorithm on R6 with random keys (teaching version; not executed in the author environment)
p=[6 3 8 2 5 4]; d=[14 8 20 6 18 12]; tard=@(x) local_tard(x,p,d);
rng(162); M=10; N1=2; N2=3; N3=M-N1-N2; Smax=2; budget=200;
X=rand(M,6); f=zeros(M,1); for k=1:M, f(k)=tard(X(k,:)); end; ev=M; best=min(f);
while ev<budget
  [f,ix]=sort(f); X=X(ix,:);
  for i=1:N1                                   % lucky: attraction, slope or pit, bisection swirl
    used=0; L=X(i,:); fL=f(i);
    while used<10*Smax && ev<budget
      others=setdiff(1:M,i); [~,a]=min(sum(abs(X(others,:)-L),2)); r=L-X(others(a),:);
      if ~any(r), break; end
      O=min(max(L+r,0),1); fO=tard(O); ev=ev+1; used=used+1;
      if fO<fL, L=O; fL=fO; continue; end
      moved=false;
      for s=1:Smax
        for c={L+r/2^s, L-r/2^s}
          C=min(max(c{1},0),1); fC=tard(C); ev=ev+1; used=used+1;
          if fC<fL, L=C; fL=fC; moved=true; break; end
        end
        if moved, break; end
      end
      if ~moved, break; end
    end
    X(i,:)=L; f(i)=fL;
  end
  for i=M-N2+1:M, X(i,:)=rand(1,6); f(i)=tard(X(i,:)); ev=ev+1; end          % unlucky: fly away, land
  for i=N1+1:N1+N3                                                            % remaining: toward the middle of two others
    gh=randsample(setdiff(1:M,i),2); lam=rand; X(i,:)=min(max(X(i,:)+lam*((X(gh(1),:)+X(gh(2),:))/2-X(i,:)),0),1); f(i)=tard(X(i,:)); ev=ev+1;
  end
  best=min(best,min(f));
end
fprintf('best total tardiness %d after %d evaluations\n',best,ev);
function T=local_tard(x,p,d), [~,seq]=sort(x); C=cumsum(p(seq)); T=sum(max(0,C-d(seq))); end
