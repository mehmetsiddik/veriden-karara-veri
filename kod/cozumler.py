import pandas as pd, numpy as np, scipy.stats as st, statsmodels.formula.api as smf, statsmodels.api as sm, pingouin as pg
from statsmodels.multivariate.manova import MANOVA
from statsmodels.stats.power import TTestIndPower
d=pd.read_csv('data/ogrenci.csv')
x=np.array([12,15,15,18,20,22,25,60.]); print('3.1',x.mean(),np.median(x),x.std(ddof=1),x.max()-x.min()); y=x[:-1]; print(' w/o60',y.mean(),np.median(y),y.std(ddof=1),y.max()-y.min())
g=np.prod([1.25,.9,1.05,1.2])**.25; print('3.2',g)
for s,gg in d.groupby('sube').kaygi: q1,q3=np.percentile(gg,[25,75]); print('3.6 sube',s,gg.mean().round(2),gg.std().round(2),gg.median(),gg.min(),gg.max())
print('4.5',st.shapiro(d.devamsizlik), d.devamsizlik.nunique())
print('5.5 n',TTestIndPower().solve_power(0.35,power=.8,alpha=.05))
a=d[d.cinsiyet==1].kaygi; b=d[d.cinsiyet==2].kaygi; print('6.4',a.mean(),a.std(),b.mean(),b.std(),st.levene(a,b,center='mean'),st.ttest_ind(a,b),st.mannwhitneyu(a,b,method='asymptotic',use_continuity=False))
print('7.2 F p',st.f.sf(60/11,3,36))
print('7.6',pg.anova(d,dv='proje',between='yontem',detailed=True), st.levene(*[g.proje for _,g in d.groupby('yontem')],center='mean')); print(pg.pairwise_tukey(d,dv='proje',between='yontem'))
r=MANOVA.from_formula('vize+final+proje~C(yontem)*C(sube)',d).mv_test(); 
for k in ['C(yontem)','C(sube)','C(yontem):C(sube)']: print('9.5',k,r.results[k]['stat'].loc["Wilks' lambda"].values, r.results[k]['stat'].loc["Pillai's trace"].values)
print('10.1',st.chisquare([15,22,18,25,19,21]))
t=pd.crosstab(d.basari,d.sube); print('10.6',t, st.chi2_contingency(t,correction=False)[:3])
# gamma & tau-b
xb=d.basari.values; ys=(d.sube==1).astype(int).values
print('  tau-b', st.kendalltau(xb,ys))
def gamma(x,y):
    C=D=0
    for i in range(len(x)):
        for j in range(i+1,len(x)):
            s=np.sign(x[i]-x[j])*np.sign(y[i]-y[j]); C+=s>0; D+=s<0
    return (C-D)/(C+D)
print('  gamma',gamma(xb,ys))
xx=np.array([1,2,3,4,5.]); yy=np.array([2,4,5,4,5.]); print('11.1 cov',np.cov(xx,yy)[0,1],'r',np.corrcoef(xx,yy)[0,1])
r=.36; z=np.arctanh(r); se=1/np.sqrt(27); print('11.2 t',r*np.sqrt(28)/np.sqrt(1-r*r),'p',2*st.t.sf(r*np.sqrt(28)/np.sqrt(1-r*r),28),'CI',np.tanh(z-1.96*se),np.tanh(z+1.96*se),'crit',st.t.ppf(.975,28))
print('11.5',st.pearsonr(d.devamsizlik,d.final),st.spearmanr(d.devamsizlik,d.final),st.kendalltau(d.devamsizlik,d.final))
m=smf.ols('proje~C(yontem)+calisma',d).fit(); print('12.6',m.params.round(3),m.pvalues.round(4),m.rsquared)
print('12.3 F p', st.f.sf(13.786,6,193))
lg=smf.logit('gecti~C(yontem)+calisma+devamsizlik',d).fit(disp=0); print('13.6',np.exp(lg.params).round(3),lg.pvalues.round(4), np.exp(lg.conf_int()).round(2))
print('10.5 p',st.chi2.sf(5.6,1),'10.4',st.chi2.sf(22.336,2))
print('13.3', st.chi2.sf(28.3,3), 1-np.exp(-28.3/150), (1-np.exp(-28.3/150))/(1-np.exp(-180.4/150)))
print('7.4 one-sided', st.t.sf(1.539,117))
print('6.1', (496.2-500)/1.6, 2*st.t.sf(2.375,15))
