import pandas as pd, numpy as np, scipy.stats as st
from statsmodels.multivariate.manova import MANOVA
d=pd.read_csv('data/ogrenci.csv'); dv=['vize','final','proje']
print(d.groupby('yontem')[dv].agg(['mean','std']).round(2))
print(d[dv].corr().round(3))
print(MANOVA.from_formula('vize+final+proje~C(yontem)',d).mv_test().results['C(yontem)']['stat'])
# by hand
Y=d[dv].values; g=d.yontem.values; k=3; N=len(d); p=3
gm=Y.mean(0); W=np.zeros((p,p)); B=np.zeros((p,p))
for j in (1,2,3):
    Yj=Y[g==j]; mj=Yj.mean(0); W+=(Yj-mj).T@(Yj-mj); B+=len(Yj)*np.outer(mj-gm,mj-gm)
ev=np.linalg.eigvals(np.linalg.solve(W,B)).real; ev=np.sort(ev)[::-1]; print('eig',ev)
L=np.linalg.det(W)/np.linalg.det(W+B); V=(ev/(1+ev)).sum(); T=ev.sum(); R=ev[0]
s=min(p,k-1); print('Wilks',L,'Pillai',V,'HL',T,'Roy',R,'s',s)
print('partial eta wilks',1-L**(1/s),'pillai',V/s,'HL',(T/s)/(1+T/s),'roy',R/(1+R))
# Box M SPSS
Ss=[];ns=[]
for j in (1,2,3):
    Yj=Y[g==j]; Ss.append(np.cov(Yj,rowvar=False)); ns.append(len(Yj))
ns=np.array(ns); Sp=sum((n-1)*S for n,S in zip(ns,Ss))/(N-k)
M=(N-k)*np.log(np.linalg.det(Sp))-sum((n-1)*np.log(np.linalg.det(S)) for n,S in zip(ns,Ss))
c1=(sum(1/(n-1) for n in ns)-1/(N-k))*(2*p**2+3*p-1)/(6*(p+1)*(k-1))
c2=(sum(1/(n-1)**2 for n in ns)-1/(N-k)**2)*(p-1)*(p+2)/(6*(k-1))
df1=(k-1)*p*(p+1)/2; df2=(df1+2)/abs(c2-c1**2)
if c2>c1**2:
    b=df1/(1-c1-df1/df2); F=M/b
else:
    b=df2/(1-c1+2/df2); F=df2*M/(df1*(b-M))
print('BoxM',M,'F',F,'df1',df1,'df2',df2,'p',st.f.sf(F,df1,df2))
for v in dv:
    grp=[d[d.yontem==j][v] for j in (1,2,3)]; Fv=st.f_oneway(*grp); lev=st.levene(*grp,center='mean')
    ssb=sum(len(x)*(x.mean()-d[v].mean())**2 for x in grp); sst=((d[v]-d[v].mean())**2).sum()
    print(v,'F',Fv,'eta',ssb/sst,'levene',lev)
# two-group Hotelling T2 sube
Y1=Y[d.sube==1]; Y2=Y[d.sube==2]; n1,n2=len(Y1),len(Y2); dm=Y1.mean(0)-Y2.mean(0)
Spp=((n1-1)*np.cov(Y1,rowvar=False)+(n2-1)*np.cov(Y2,rowvar=False))/(n1+n2-2)
T2=n1*n2/(n1+n2)*dm@np.linalg.solve(Spp,dm); Fh=(n1+n2-p-1)/(p*(n1+n2-2))*T2
print('T2 sube',T2,'F',Fh,'df',p,n1+n2-p-1,'p',st.f.sf(Fh,p,n1+n2-p-1))
