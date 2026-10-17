import pandas as pd, numpy as np, scipy.stats as st, statsmodels.api as sm, statsmodels.formula.api as smf
d=pd.read_csv('data/ogrenci.csv'); d['birinci']=(d.sube==1).astype(int)
n=len(d); p1=d.gecti.mean(); LL0=n*(p1*np.log(p1)+(1-p1)*np.log(1-p1)); print('n pass',d.gecti.sum(),'-2LL0',-2*LL0,'b0 null',np.log(p1/(1-p1)),'exp',p1/(1-p1))
s=smf.logit('gecti~calisma',d).fit(disp=0); print(s.params, s.bse, (s.params/s.bse)**2, s.pvalues, np.exp(s.params), np.exp(s.conf_int()), '-2LL',-2*s.llf)
for h in (4,8): eta=s.params.iloc[0]+s.params.iloc[1]*h; print('calisma',h,'logit',eta,'p',1/(1+np.exp(-eta)))
m=smf.logit('gecti~calisma+devamsizlik+kaygi+birinci',d).fit(disp=0)
print(m.summary2())
print('Wald',(m.params/m.bse)**2); print('OR',np.exp(m.params)); print('ORCI',np.exp(m.conf_int()))
LL=m.llf; chi=-2*LL0+2*LL; print('-2LL',-2*LL,'omnibus',chi,st.chi2.sf(chi,4))
cs=1-np.exp((2/n)*(LL0-LL)); nk=cs/(1-np.exp((2/n)*LL0)); mf=1-LL/LL0; print('CoxSnell',cs,'Nagelkerke',nk,'McFadden',mf)
ph=m.predict(); pred=(ph>=.5).astype(int); ct=pd.crosstab(d.gecti,pred); print(ct, 'acc',(pred==d.gecti).mean())
# HL deciles (SPSS-like: sort, 10 groups by rank, keep ties)
df=pd.DataFrame({'y':d.gecti,'p':ph}).sort_values('p').reset_index(drop=True)
df['g']=pd.qcut(df.p.rank(method='first'),10,labels=False)
H=0
for g,gr in df.groupby('g'):
    o1=gr.y.sum(); e1=gr.p.sum(); o0=len(gr)-o1; e0=len(gr)-e1; H+=(o1-e1)**2/e1+(o0-e0)**2/e0
print('HL',H,st.chi2.sf(H,8))
# example student
x=dict(calisma=8,devamsizlik=1,kaygi=45,birinci=1); eta=m.params['Intercept']+sum(m.params[k]*v for k,v in x.items()); print('example eta',eta,'p',1/(1+np.exp(-eta)))
x2=dict(calisma=4,devamsizlik=4,kaygi=60,birinci=0); eta2=m.params['Intercept']+sum(m.params[k]*v for k,v in x2.items()); print('example2 eta',eta2,'p',1/(1+np.exp(-eta2)))
# diagnostics
inf=m.get_influence(); zr=inf.resid_studentized; pr=(d.gecti-ph)/np.sqrt(ph*(1-ph))
for i in np.argsort(-np.abs(pr.values))[:4]: print('id',d.id[i],'gecti',d.gecti[i],'p',round(ph[i],3),'zres',round(pr[i],2),'dev',round(np.sign(d.gecti[i]-ph[i])*np.sqrt(-2*np.log(ph[i] if d.gecti[i]==1 else 1-ph[i])),2),'cook',round(inf.cooks_distance[0][i],3),'lev',round(inf.hat_matrix_diag[i],3))
print('n |zres|>2',(np.abs(pr)>2).sum(),(np.abs(pr)>3).sum())
# logistic curve data for figure (calisma only model)
xx=np.linspace(0,15,61); np.savetxt('figures/data/b13_curve.dat',np.column_stack([xx,1/(1+np.exp(-(s.params.iloc[0]+s.params.iloc[1]*xx)))]),header='x p',comments='',fmt='%.4f')
jit=d[['calisma','gecti']].values; np.savetxt('figures/data/b13_points.dat',jit,header='x y',comments='',fmt='%d')
print('LR test each var (drop1):')
for v in ['calisma','devamsizlik','kaygi','birinci']:
    f='gecti~'+'+'.join([w for w in ['calisma','devamsizlik','kaygi','birinci'] if w!=v]); r=smf.logit(f,d).fit(disp=0); print(v, 2*(LL-r.llf), st.chi2.sf(2*(LL-r.llf),1))
