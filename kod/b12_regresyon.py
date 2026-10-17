import pandas as pd, numpy as np, scipy.stats as st, statsmodels.formula.api as smf, statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence
from statsmodels.stats.stattools import durbin_watson
d=pd.read_csv('data/ogrenci.csv')
m1=smf.ols('final~calisma',d).fit(); print(m1.summary()); print('anova',sm.stats.anova_lm(m1)); print('SEest',np.sqrt(m1.mse_resid))
pr=m1.get_prediction(pd.DataFrame({'calisma':[10]})).summary_frame(); print(pr)
sxx=((d.calisma-d.calisma.mean())**2).sum(); sxy=((d.calisma-d.calisma.mean())*(d.final-d.final.mean())).sum(); print('sxx',sxx,'sxy',sxy,'b1',sxy/sxx)
X=['on_test','calisma','devamsizlik','kaygi']
m2=smf.ols('final~'+'+'.join(X),d).fit(); print(m2.summary()); print('SEest',np.sqrt(m2.mse_resid),'DW',durbin_watson(m2.resid))
z=d[X+['final']].apply(lambda c:(c-c.mean())/c.std()); mb=smf.ols('final~'+'+'.join(X),z).fit(); print('beta',mb.params.round(3))
Xm=sm.add_constant(d[X]); print('VIF',[round(variance_inflation_factor(Xm.values,i),3) for i in range(1,5)])
# zero-order, partial, part
for v in X:
    others=[o for o in X if o!=v]
    rv=smf.ols(v+'~'+'+'.join(others),d).fit().resid; ry=smf.ols('final~'+'+'.join(others),d).fit().resid
    print(v,'zero',round(np.corrcoef(d[v],d.final)[0,1],3),'partial',round(np.corrcoef(rv,ry)[0,1],3),'part',round(np.corrcoef(rv,d.final)[0,1],3))
print(sm.stats.anova_lm(m2))
m0=smf.ols('final~on_test',d).fit(); print('block1 R2',m0.rsquared, m0.fvalue, m0.f_pvalue)
dR=m2.rsquared-m0.rsquared; Fc=(dR/3)/((1-m2.rsquared)/(120-4-1)); print('dR2',dR,'Fchange',Fc,st.f.sf(Fc,3,115))
m3=smf.ols('final~on_test+calisma+devamsizlik+kaygi+C(yontem)',d).fit(); print(m3.params, m3.bse, m3.pvalues, m3.rsquared, m3.rsquared_adj)
dR3=m3.rsquared-m2.rsquared; Fc3=(dR3/2)/((1-m3.rsquared)/(120-6-1)); print('dR2 b3',dR3,Fc3,st.f.sf(Fc3,2,113))
inf=OLSInfluence(m2); sres=inf.resid_studentized_internal; cook=inf.cooks_distance[0]; lev=inf.hat_matrix_diag; dfb=inf.dfbetas; cov=inf.cov_ratio
mah=(lev-1/120)*119
for i in np.argsort(-cook)[:4]: print('id',d.id[i],'zres',round(m2.resid[i]/np.sqrt(m2.mse_resid),3),'sres',round(sres[i],3),'cook',round(cook[i],3),'lev',round(lev[i],3),'mah',round(mah[i],3),'dfbeta max',np.abs(dfb[i]).max().round(3),'covr',round(cov[i],3))
zres=m2.resid/np.sqrt(m2.mse_resid); print('n |zres|>2',(np.abs(zres)>2).sum(),'>3',(np.abs(zres)>3).sum(), 'max lev',lev.max(),'2p/n', 2*5/120,'max mah',mah.max(), 'cov bounds',1-3*5/120,1+3*5/120)
print('mean lev',lev.mean())
mn=smf.ols('final~'+'+'.join(X),d[d.id!=57]).fit(); print('no57',mn.params.round(3), mn.rsquared, mn.pvalues.round(4))
# residual plot data
np.savetxt('figures/data/b12_res.dat',np.column_stack([(m2.fittedvalues-m2.fittedvalues.mean())/m2.fittedvalues.std(),zres]),header='zpred zres',comments='',fmt='%.4f')
print('shapiro resid',st.shapiro(m2.resid))
# stepwise forward illustration: order of entry by F to enter p<.05

# ---- Ek tanılama çıktıları (kitapta Örnek "Etkili gözlemlerin belirlenmesi" ve tablolarda kullanılır)
print('maxlev id',d.id[int(np.argmax(lev))],lev.max(),list(d.id[np.argsort(-lev)[1:6]]))
print('covratio out',[(d.id[i],round(cov[i],3)) for i in range(120) if abs(cov[i]-1)>3*5/120])
print('|dfbetas|>1',[d.id[i] for i in range(120) if np.abs(dfb[i]).max()>1],'thresh 2/sqrt n',2/np.sqrt(120),
      [(d.id[i],round(np.abs(dfb[i]).max(),2)) for i in range(120) if np.abs(dfb[i]).max()>2/np.sqrt(120)])
print('no57 shapiro',st.shapiro(mn.resid),'skew',st.skew(mn.resid,bias=False),'kurt',st.kurtosis(mn.resid,bias=False),mn.bse.round(3))
print('tol',[round(1/variance_inflation_factor(Xm.values,i),3) for i in range(1,5)])
print('ids |z|>2',list(d.id[np.abs(zres)>2]),list(np.round(zres[np.abs(zres)>2],2)))
ssreg=m2.ess; print('SS reg m2',ssreg,'SSE',m2.ssr,'MSE',m2.mse_resid,'F',m2.fvalue,'R',np.sqrt(m2.rsquared))
print('f2 block2',dR/(1-m2.rsquared))
