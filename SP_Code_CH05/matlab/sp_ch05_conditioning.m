% SP_CH05 — joint table statistics, tower rule, total variance (teaching version)
J=[0.45 0.10 0.02; 0.15 0.12 0.05; 0.03 0.05 0.03]; x=(0:2)';
pX=sum(J,2); pY=sum(J,1)'; EX=x'*pX; EY=x'*pY; EXY=x'*J*x;
cov=EXY-EX*EY; VX=(x.^2)'*pX-EX^2; VY=(x.^2)'*pY-EY^2;
fprintf('E[X]=%.2f E[Y]=%.2f Cov=%.3f rho=%.3f\n',EX,EY,cov,cov/sqrt(VX*VY));
EYgX=(J*x)./pX; fprintf('E[Y|X=x] = %s ; tower: %.3f\n',mat2str(EYgX',3),pX'*EYgX);
% mixture: rain 0.3 (p=0.40) / dry 0.7 (p=0.157), n=12
w=[0.3 0.7]; p=[0.40 0.157]; mu=12*p; v=12*p.*(1-p);
fprintf('E=%.3f  Var=%.3f (within %.3f + between %.3f)\n',w*mu',w*v'+w*(mu-w*mu').^2',w*v',w*(mu-w*mu').^2');
