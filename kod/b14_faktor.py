import pandas as pd, numpy as np, scipy.stats as st
from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
from factor_analyzer.rotator import Rotator
t=pd.read_csv('data/tutum_olcegi.csv'); X=t[[f'm{i}' for i in range(1,13)]]; n,p=X.shape
R=X.corr().values; print(pd.DataFrame(R).round(2))
kmo_all,kmo=calculate_kmo(X); print('KMO',kmo, 'MSA',np.round(kmo_all,3))
chi,pv=calculate_bartlett_sphericity(X); print('Bartlett',chi,'df',p*(p-1)/2,pv)
ev=np.sort(np.linalg.eigvalsh(R))[::-1]; print('eig',ev.round(3),'cum%',(np.cumsum(ev)/p*100).round(2))
rng=np.random.default_rng(11); sims=[]
for _ in range(1000):
    Z=rng.normal(size=(n,p)); sims.append(np.sort(np.linalg.eigvalsh(np.corrcoef(Z,rowvar=False)))[::-1])
sims=np.array(sims); print('PA mean',sims.mean(0)[:5].round(3),'P95',np.percentile(sims,95,axis=0)[:5].round(3))
# PAF SPSS style
def paf(R,k,it=25,tol=.001):
    h=1-1/np.diag(np.linalg.inv(R)); 
    for i in range(it):
        Rr=R.copy(); np.fill_diagonal(Rr,h); w,v=np.linalg.eigh(Rr); idx=np.argsort(w)[::-1][:k]
        L=v[:,idx]*np.sqrt(np.maximum(w[idx],0)); hn=(L**2).sum(1)
        if np.max(np.abs(hn-h))<tol: h=hn; break
        h=hn
    return L,h,i+1,1-1/np.diag(np.linalg.inv(R))
L,h,iters,h0=paf(R,3); print('iters',iters); print('initial comm',h0.round(3)); print('extr comm',h.round(3))
ss=(L**2).sum(0); print('SS loadings extr',ss.round(3),'%',(ss/p*100).round(2),'cum',(np.cumsum(ss)/p*100).round(2))
# varimax with Kaiser normalization
rv=Rotator(method='varimax',normalize=True); Lv=rv.fit_transform(L); print('varimax'); print(pd.DataFrame(Lv,index=X.columns).round(3)); print('ss',(Lv**2).sum(0).round(3))
rp=Rotator(method='promax',normalize=True,power=4); Lp=rp.fit_transform(L); phi=rp.phi_; print('promax pattern'); print(pd.DataFrame(Lp,index=X.columns).round(3)); print('phi',np.round(phi,3)); S=Lp@phi; print('structure'); print(pd.DataFrame(S,index=X.columns).round(3))
print('ss structure-based (SPSS rotation sums for oblique)',(S**2).sum(0).round(3))
def alpha(df):
    k=df.shape[1]; return k/(k-1)*(1-df.var(ddof=1).sum()/df.sum(1).var(ddof=1))
for nm,cols in [('Kaygi',['m1','m2','m3','m4']),('Ilgi',['m5','m6','m7','m8']),('Ozyeterlik',['m9','m10','m11','m12'])]:
    D=X[cols]; a=alpha(D); print(nm,'alpha',round(a,3),'mean',D.sum(1).mean().round(2),'sd',D.sum(1).std().round(2))
    for c in cols:
        rest=D.drop(columns=c).sum(1); print('  ',c,'citc',round(np.corrcoef(D[c],rest)[0,1],3),'alpha if del',round(alpha(D.drop(columns=c)),3),'mean',D[c].mean().round(2))
print('alpha all 12 (with reverse kaygi)', alpha(pd.concat([6-X[['m1','m2','m3','m4']],X[['m5','m6','m7','m8','m9','m10','m11','m12']]],axis=1)))
np.savetxt('figures/data/b14_scree.dat',np.column_stack([np.arange(1,13),ev,np.percentile(sims,95,axis=0)]),header='k eig pa',comments='',fmt='%.4f')
