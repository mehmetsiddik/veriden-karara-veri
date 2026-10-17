import pandas as pd, numpy as np, scipy.stats as st, statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel
from scipy.optimize import minimize
d=pd.read_csv('data/ogrenci.csv'); X=d[['calisma','devamsizlik']].values; y=d.basari.values
om=OrderedModel(d.basari,d[['calisma','devamsizlik']],distr='logit').fit(method='bfgs',disp=0,maxiter=1000)
print(om.summary()); th=om.params.values[:2].copy(); th[1]=th[0]+np.exp(om.params.values[3]) if False else th[1]
# statsmodels parametrizes thresholds: first cut, then log increments
cut1=om.params['1/2']; cut2=cut1+np.exp(om.params['2/3']); print('thresholds',cut1,cut2, 'b',om.params[['calisma','devamsizlik']].values)
LL=om.llf; cnt=np.bincount(y)[1:]; LL0=(cnt*np.log(cnt/len(y))).sum(); n=len(y)
print('-2LL0',-2*LL0,'-2LL',-2*LL,'chi',2*(LL-LL0),st.chi2.sf(2*(LL-LL0),2))
cs=1-np.exp((2/n)*(LL0-LL)); print('CS',cs,'NK',cs/(1-np.exp(2*LL0/n)),'McF',1-LL/LL0)
print('OR',np.exp(om.params[['calisma','devamsizlik']]), 'Wald',(om.params/om.bse)**2, om.pvalues)
# general (non-proportional) model: P(Y<=j)=F(th_j - x b_j)
def nll(par):
    t1,t2,b1a,b1b,b2a,b2b=par
    F1=1/(1+np.exp(-(t1-(X@[b1a,b2a])))); F2=1/(1+np.exp(-(t2-(X@[b1b,b2b]))))
    P=np.column_stack([F1,F2-F1,1-F2]); P=np.clip(P,1e-12,1); return -np.log(P[np.arange(n),y-1]).sum()
b=om.params[['calisma','devamsizlik']].values
r=minimize(nll,[cut1,cut2,b[0],b[0],b[1],b[1]],method='Nelder-Mead',options={'maxiter':20000,'xatol':1e-8,'fatol':1e-10})
r=minimize(nll,r.x,method='BFGS'); print('general LL',-r.fun, r.x)
chi=2*(-r.fun-LL); print('parallel lines chi',chi,'df',2,'p',st.chi2.sf(chi,2))
# predicted probs for a student calisma=8, devamsizlik=1
for c,dv in [(8,1),(4,4)]:
    e=c*b[0]+dv*b[1]; F1=1/(1+np.exp(-(cut1-e))); F2=1/(1+np.exp(-(cut2-e))); print('pred',c,dv,F1,F2-F1,1-F2)
