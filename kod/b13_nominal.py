import pandas as pd, numpy as np, scipy.stats as st, statsmodels.api as sm
d=pd.read_csv('data/ogrenci.csv'); d['birinci']=(d.sube==1).astype(int)
X=sm.add_constant(d[['calisma','birinci']]); y=d.tercih-1   # 0=İş (reference),1=YL,2=Kararsız
m=sm.MNLogit(y,X).fit(disp=0); print(m.summary()); print('OR',np.exp(m.params)); print('Wald',(m.params/m.bse)**2)
LL=m.llf; LL0=m.llnull; n=len(y); chi=2*(LL-LL0); print('-2LL0',-2*LL0,'-2LL',-2*LL,'chi',chi,'df',4,st.chi2.sf(chi,4))
cs=1-np.exp((2/n)*(LL0-LL)); print('CS',cs,'NK',cs/(1-np.exp(2*LL0/n)),'McF',1-LL/LL0)
for v in ['calisma','birinci']:
    r=sm.MNLogit(y,X.drop(columns=v)).fit(disp=0); c=2*(LL-r.llf); print('LRT',v,c,st.chi2.sf(c,2))
pr=m.predict().argmax(1); ct=pd.crosstab(y,pr); print(ct,'acc',(pr==y).mean())
pp=d.tercih.value_counts(normalize=True).sort_index(); print('props',pp.values,'sum sq',(pp**2).sum(),'1.25x',1.25*(pp**2).sum())
print('CI OR',np.exp(m.conf_int()))
