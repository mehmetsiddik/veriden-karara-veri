import pandas as pd, numpy as np, scipy.stats as st
from statsmodels.stats.diagnostic import lilliefors
d=pd.read_csv('data/ogrenci.csv')
n=len(d)
# tek değişkenli z
for v in ['calisma','devamsizlik','kaygi','final']:
    z=(d[v]-d[v].mean())/d[v].std(); print(v,'max|z|',round(z.abs().max(),2), d.loc[z.abs().idxmax(),'id'])
z57=(18-d.final.mean())/d.final.std(); print('z57',z57)
# Mahalanobis
X=d[['calisma','devamsizlik','final']].values; mu=X.mean(0); S=np.cov(X,rowvar=False)
D2=np.einsum('ij,jk,ik->i',X-mu,np.linalg.inv(S),X-mu)
o=np.argsort(-D2)[:5]; print('D2 top', [(int(d.id[i]),round(D2[i],2)) for i in o], 'crit', st.chi2.ppf(.999,3))
print('p57', st.chi2.sf(D2[56],3))
# normallik
for v in ['final','calisma','kaygi','devamsizlik']:
    x=d[v]; D,p=lilliefors(x,dist='norm',pvalmethod='table'); W,pw=st.shapiro(x)
    sk=st.skew(x,bias=False); ku=st.kurtosis(x,bias=False)
    print(v,'KS',round(D,3),round(p,3),'SW',round(W,3),round(pw,3),'zsk',round(sk/0.221,2),'zku',round(ku/0.438,2))
for g,x in d.groupby('yontem').final:
    D,p=lilliefors(x,pvalmethod='table'); W,pw=st.shapiro(x); print('grup',g,round(D,3),round(p,3),round(W,3),round(pw,3))
print('Levene final~yontem', st.levene(*[x for _,x in d.groupby('yontem').final],center='mean'))
print('Levene median', st.levene(*[x for _,x in d.groupby('yontem').final],center='median'))
# QQ verisi
x=np.sort(d.final.values); pp=(np.arange(1,n+1)-0.375)/(n+0.25); q=st.norm.ppf(pp)
pd.DataFrame({'teorik':np.round(d.final.mean()+d.final.std()*q,3),'gozlenen':x}).to_csv('figures/data/b04_qq_final.dat',sep=' ',index=False)
# saçılım calisma-final
d[['calisma','final']].to_csv('figures/data/b04_scatter.dat',sep=' ',index=False)
# dönüşüm gösterimi: simüle tepki süresi
rng=np.random.default_rng(5); rt=np.round(np.exp(rng.normal(6.3,0.5,200)))
print('rt', st.skew(rt,bias=False), st.skew(np.log10(rt),bias=False), st.skew(np.sqrt(rt),bias=False), st.shapiro(rt)[1], st.shapiro(np.log10(rt))[1])
for nm,arr,bins in [('ham',rt,np.arange(0,2400,150)),('log',np.log10(rt),np.arange(2.0,3.5,0.1))]:
    h,e=np.histogram(arr,bins=bins)
    with open(f'figures/data/b04_rt_{nm}.dat','w') as f:
        f.write('x y\n'); [f.write(f'{a:.3f} {b}\n') for a,b in zip(e[:-1],h)]; f.write(f'{e[-1]:.3f} 0\n')
print(rt.min(),rt.max(),np.log10(rt).min(),np.log10(rt).max())
# eksik veri gösterimi: kaygi'de MCAR vs MNAR silme senaryosu
k=d.kaygi.values.copy(); rng=np.random.default_rng(9)
mcar=rng.random(n)<0.15; mnar=(k>np.percentile(k,80)) & (rng.random(n)<0.75)
print('kaygi tam', k.mean(), k.std(ddof=1), 'MCAR', k[~mcar].mean(), (~mcar).sum(), 'MNAR', k[~mnar].mean(), (~mnar).sum())
kk=k.astype(float); kk[mcar]=np.nan; imp=np.where(np.isnan(kk),np.nanmean(kk),kk); print('mean-imp sd', np.nanstd(kk,ddof=1), imp.std(ddof=1))
