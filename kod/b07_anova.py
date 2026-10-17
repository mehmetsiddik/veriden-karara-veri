import pandas as pd, numpy as np, scipy.stats as st, pingouin as pg
from statsmodels.stats.multicomp import pairwise_tukeyhsd
d=pd.read_csv('data/ogrenci.csv'); y=d.final; g=d.yontem
gm=y.mean(); stats=d.groupby('yontem').final.agg(['count','mean','std','var'])
print(stats); print('gm',gm)
ssb=(stats['count']*(stats['mean']-gm)**2).sum(); ssw=((stats['count']-1)*stats['var']).sum(); sst=((y-gm)**2).sum()
k=3;N=120; msb=ssb/(k-1); msw=ssw/(N-k); F=msb/msw
print('SSB',ssb,'SSW',ssw,'SST',sst,'MSB',msb,'MSW',msw,'F',F,'p',st.f.sf(F,k-1,N-k),'eta2',ssb/sst,'omega2',(ssb-(k-1)*msw)/(sst+msw),'Fcrit',st.f.ppf(.95,2,117))
print(pg.welch_anova(d,dv='final',between='yontem'))
# Brown-Forsythe F*
n=stats['count'].values; m=stats['mean'].values; v=stats['var'].values
Fs=(n*(m-gm)**2).sum()/((1-n/N)*v).sum(); c=((1-n/N)*v)/((1-n/N)*v).sum(); df2=1/((c**2)/(n-1)).sum()
print('BF F*',Fs,'df2',df2,'p',st.f.sf(Fs,k-1,df2))
print(pairwise_tukeyhsd(y,g).summary())
print(pg.pairwise_gameshowell(d,dv='final',between='yontem').round(4))
# Bonferroni (LSD t with pooled MSW)
import itertools
for a,b in itertools.combinations([1,2,3],2):
    diff=stats.loc[a,'mean']-stats.loc[b,'mean']; se=np.sqrt(msw*(1/40+1/40)); t=diff/se; p=2*st.t.sf(abs(t),N-k)
    print('LSD/Bonf',a,b,round(diff,3),round(se,3),round(t,3),round(p,4),round(min(1,3*p),4),'CI bonf',diff-st.t.ppf(1-.05/6,N-k)*se, diff+st.t.ppf(1-.05/6,N-k)*se)
# Tukey CI
q=st.studentized_range.ppf(.95,3,117); print('q',q,'HSD halfwidth',q*np.sqrt(msw/40))
# contrast proje vs others
cvec=np.array([-1,2,-1]); L=(cvec*m).sum(); seL=np.sqrt(msw*(cvec**2/n).sum()); tL=L/seL
print('contrast L',L,'se',seL,'t',tL,'p',2*st.t.sf(abs(tL),N-k))
# Kruskal Wallis
H=st.kruskal(*[s for _,s in d.groupby('yontem').final]); rk=st.rankdata(y); mr=pd.Series(rk).groupby(g.values).mean()
print('KW',H,'mean ranks',mr.round(2).tolist(), 'H/(n-1)', H.statistic/(N-1))
# Dunn with tie correction
_,cnt=np.unique(y,return_counts=True); T=(cnt**3-cnt).sum()
for a,b in itertools.combinations([1,2,3],2):
    se=np.sqrt((N*(N+1)/12 - T/(12*(N-1)))*(1/40+1/40)); z=(mr[a]-mr[b])/se; p=2*st.norm.sf(abs(z))
    print('Dunn',a,b,round(mr[a]-mr[b],3),round(z,3),round(p,4),'adj',round(min(1,3*p),4))
pd.DataFrame({'g':[1,2,3],'m':m,'lo':m-st.t.ppf(.975,39)*np.sqrt(v/40),'hi':m+st.t.ppf(.975,39)*np.sqrt(v/40)}).round(3).to_csv('figures/data/b07_means.dat',sep=' ',index=False)
print(open('figures/data/b07_means.dat').read())
