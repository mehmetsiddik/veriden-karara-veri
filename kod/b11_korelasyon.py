import pandas as pd, numpy as np, scipy.stats as st, pingouin as pg
d=pd.read_csv('data/ogrenci.csv')
h=d[['id','calisma','final']].head(8); print(h.T)
x=h.calisma.values.astype(float); y=h.final.values.astype(float); n=len(x)
print('sum x',x.sum(),'sum y',y.sum(),'mean',x.mean(),y.mean())
dx=x-x.mean(); dy=y-y.mean(); print('dx',dx,'dy',dy,'prod',dx*dy,'Sxy',(dx*dy).sum(),'Sxx',(dx**2).sum(),'Syy',(dy**2).sum())
cov=(dx*dy).sum()/(n-1); r=st.pearsonr(x,y); print('cov',cov,'sx',x.std(ddof=1),'sy',y.std(ddof=1),'r',r)
rx=st.rankdata(x); ry=st.rankdata(y); print('ranks',rx,ry,'d2',((rx-ry)**2).sum(),'spearman',st.spearmanr(x,y),'formula',1-6*((rx-ry)**2).sum()/(n*(n**2-1)), 'kendall',st.kendalltau(x,y))
v=['calisma','devamsizlik','kaygi','on_test','final']
R=d[v].corr(); print(R.round(3))
for a in v:
    for b in v:
        if a<b: rr,pp=st.pearsonr(d[a],d[b]); print(a,b,round(rr,3),round(pp,4))
r=st.pearsonr(d.calisma,d.final); print(r, r.confidence_interval(), 't', r.statistic*np.sqrt(118)/np.sqrt(1-r.statistic**2))
z=np.arctanh(r.statistic); se=1/np.sqrt(117); print('fisher z',z,'CI', np.tanh(z-1.96*se), np.tanh(z+1.96*se))
dd=d[d.id!=57]; print('without 57', st.pearsonr(dd.calisma,dd.final))
print('spearman calisma final', st.spearmanr(d.calisma,d.final), 'kendall', st.kendalltau(d.calisma,d.final))
print('spearman kaygi final', st.spearmanr(d.kaygi,d.final), 'pearson', st.pearsonr(d.kaygi,d.final))
s01=(d.sube==1).astype(int); print('rpb final sube1', st.pearsonr(d.final,s01))
rpb=st.pearsonr(d.calisma,d.gecti).statistic; p=d.gecti.mean(); q=1-p; yv=st.norm.pdf(st.norm.ppf(p)); rb=rpb*np.sqrt(p*q)/yv
print('rpb calisma gecti',rpb,st.pearsonr(d.calisma,d.gecti).pvalue,'p',p,'ordinate',yv,'rb',rb)
print(pg.partial_corr(d,x='kaygi',y='final',covar='calisma'))
print(pg.partial_corr(d,x='kaygi',y='final',y_covar='calisma'))   # semipartial: remove calisma from final only? 
print(pg.partial_corr(d,x='kaygi',y='final',x_covar='calisma'))   # remove calisma from kaygi only
rkf=R.loc['kaygi','final']; rkc=R.loc['kaygi','calisma']; rcf=R.loc['calisma','final']
print('partial formula',(rkf-rkc*rcf)/np.sqrt((1-rkc**2)*(1-rcf**2)),'semipartial (kaygi resid)',(rkf-rkc*rcf)/np.sqrt(1-rkc**2))
# simulated panels
rng=np.random.default_rng(5)
for i,rho in enumerate([0.9,0.5,0.0,-0.7]):
    Z=rng.multivariate_normal([0,0],[[1,rho],[rho,1]],80); np.savetxt(f'figures/data/b11_r{i}.dat',Z,header='x y',comments='',fmt='%.3f'); print('sim r',np.corrcoef(Z.T)[0,1])
xx=np.linspace(-2,2,80); yy=xx**2+rng.normal(0,0.3,80); np.savetxt('figures/data/b11_r4.dat',np.column_stack([xx,yy]),header='x y',comments='',fmt='%.3f'); print('nonlin r',np.corrcoef(xx,yy)[0,1])
