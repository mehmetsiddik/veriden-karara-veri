import pandas as pd, numpy as np, scipy.stats as st, pingouin as pg
import statsmodels.formula.api as smf, statsmodels.api as sm
d=pd.read_csv('data/ogrenci.csv')
m=smf.ols('final~C(yontem,Sum)*C(sube,Sum)',d).fit(); t=sm.stats.anova_lm(m,typ=3); print(t)
mse=m.mse_resid; print('MSE',mse, 'df',m.df_resid)
for k in t.index[1:4]: print(k,'partial eta', t.loc[k,'sum_sq']/(t.loc[k,'sum_sq']+t.loc['Residual','sum_sq']))
cm=d.groupby(['yontem','sube']).final.agg(['mean','std','count']); print(cm.round(3))
print('marg yontem',d.groupby('yontem').final.mean().tolist(),'marg sube',d.groupby('sube').final.mean().tolist())
cells=[g.final.values for _,g in d.groupby(['yontem','sube'])]
print('levene 6 cells', st.levene(*cells,center='mean'))
# simple effects of sube within yontem
for y in (1,2,3):
    a=cm.loc[(y,1),'mean']; b=cm.loc[(y,2),'mean']; se=np.sqrt(mse*(2/20)); tt=(a-b)/se
    print('sube | yontem',y, round(a-b,3), round(se,3), 'F',round(tt**2,3),'p',round(2*st.t.sf(abs(tt),114),4), 'CI', a-b-st.t.ppf(.975,114)*se, a-b+st.t.ppf(.975,114)*se)
for s in (1,2):
    sub=d[d.sube==s]; mm=sub.groupby('yontem').final.mean(); gm=sub.final.mean(); ssb=(20*(mm-gm)**2).sum(); F=ssb/2/mse
    print('yontem | sube',s, mm.round(2).tolist(), 'SS',round(ssb,3),'F',round(F,3),'p',st.f.sf(F,2,114))
# ANCOVA
slopes=smf.ols('final~C(yontem,Sum)*on_test',d).fit(); print(sm.stats.anova_lm(slopes,typ=3))
an=smf.ols('final~C(yontem,Sum)+on_test',d).fit(); ta=sm.stats.anova_lm(an,typ=3); print(ta); print(an.params)
for k in ['C(yontem, Sum)','on_test']: print(k,'peta',ta.loc[k,'sum_sq']/(ta.loc[k,'sum_sq']+ta.loc['Residual','sum_sq']))
mo=d.on_test.mean(); print('mean on_test',mo, d.groupby('yontem').on_test.mean().round(2).tolist())
for y in (1,2,3):
    nd=pd.DataFrame({'yontem':[y],'on_test':[mo]}); pr=an.get_prediction(nd).summary_frame(); print('adj mean',y,pr[['mean','mean_se']].values.round(3))
print('one-way without cov F', 10.45)
