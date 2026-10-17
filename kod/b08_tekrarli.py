import pandas as pd, numpy as np, scipy.stats as st, pingouin as pg, itertools
r=pd.read_csv('data/kaygi_tekrar.csv'); X=r[['olcum1','olcum2','olcum3']].values; n,k=X.shape
print(r.describe().round(3)); print('means',X.mean(0),'sd',X.std(0,ddof=1))
gm=X.mean(); ss_t=((X-gm)**2).sum(); ss_time=n*((X.mean(0)-gm)**2).sum(); ss_subj=k*((X.mean(1)-gm)**2).sum(); ss_err=ss_t-ss_time-ss_subj
df_time=k-1; df_err=(k-1)*(n-1); F=(ss_time/df_time)/(ss_err/df_err)
print('SS total',ss_t,'time',ss_time,'subj',ss_subj,'err',ss_err,'F',F,'p',st.f.sf(F,df_time,df_err),'peta',ss_time/(ss_time+ss_err),'MSerr',ss_err/df_err)
long=r.melt(id_vars='katilimci',var_name='zaman',value_name='kaygi')
print(pg.rm_anova(long,dv='kaygi',within='zaman',subject='katilimci',correction=True,detailed=True).T)
print(pg.sphericity(long,dv='kaygi',within='zaman',subject='katilimci'))
print('GG',pg.epsilon(long,dv='kaygi',within='zaman',subject='katilimci',correction='gg'),'HF',pg.epsilon(long,dv='kaygi',within='zaman',subject='katilimci',correction='hf'),'LB',1/(k-1))
# SPSS HF (Huynh-Feldt 1976 original): eps_hf = (n*(k-1)*eps_gg - 2)/((k-1)*(n-1-(k-1)*eps_gg))
gg=pg.epsilon(long,dv='kaygi',within='zaman',subject='katilimci',correction='gg')
hf=(n*(k-1)*gg-2)/((k-1)*(n-1-(k-1)*gg)); print('HF original',hf, min(hf,1))
for e,name in [(gg,'GG'),(min(hf,1),'HF')]: print(name,'df',df_time*e,df_err*e,'p',st.f.sf(F,df_time*e,df_err*e))
for a,b in itertools.combinations(range(3),2):
    dd=X[:,a]-X[:,b]; t=st.ttest_rel(X[:,a],X[:,b]); se=dd.std(ddof=1)/np.sqrt(n)
    tc=st.t.ppf(1-.05/6,n-1); print('pair',a+1,b+1,dd.mean().round(3),se.round(3),t.statistic.round(3),t.pvalue.round(4),'bonf',min(1,3*t.pvalue).round(4),'CIbonf',(dd.mean()-tc*se).round(2),(dd.mean()+tc*se).round(2))
fr=st.friedmanchisquare(*X.T); print('Friedman',fr,'Kendall W',fr.statistic/(n*(k-1)))
rk=np.apply_along_axis(st.rankdata,1,X); print('mean ranks',rk.mean(0))
# multivariate test (Hotelling T2 on differences) for RM
D=np.column_stack([X[:,0]-X[:,1],X[:,1]-X[:,2]]); dm=D.mean(0); S=np.cov(D,rowvar=False); T2=n*dm@np.linalg.inv(S)@dm
p_=2; Fm=(n-p_)/(p_*(n-1))*T2; print('Hotelling T2',T2,'F',Fm,'df',p_,n-p_,'p',st.f.sf(Fm,p_,n-p_),'Wilks',1/(1+T2/(n-1)))
# write data for spaghetti plot
r.to_csv('figures/data/b08_kaygi.dat',sep=' ',index=False)
