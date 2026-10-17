import pandas as pd, numpy as np, scipy.stats as st
from statsmodels.stats.contingency_tables import mcnemar, Table2x2
d=pd.read_csv('data/ogrenci.csv')
o=d.tercih.value_counts().sort_index().values; print('tercih',o, st.chisquare(o), st.chi2.ppf(.95,2))
e=np.array([.40,.35,.25])*120; print('expected prev',e, st.chisquare(o,e))
t=pd.crosstab(d.yontem,d.gecti); print(t)
c=st.chi2_contingency(t,correction=False); print(c)
E=c.expected_freq; O=t.values; res=(O-E)/np.sqrt(E)
rs=O.sum(1,keepdims=True)/O.sum(); cs=O.sum(0,keepdims=True)/O.sum(); adj=(O-E)/np.sqrt(E*(1-rs)*(1-cs))
print('std res',res.round(2),'adj',adj.round(2))
n=O.sum(); V=np.sqrt(c[0]/(n*(min(O.shape)-1))); C=np.sqrt(c[0]/(c[0]+n)); print('V',V,'C',C)
lr=2*(O*np.log(O/E)).sum(); print('LR',lr, st.chi2.sf(lr,2))
print('row pct', (O/O.sum(1,keepdims=True)*100).round(1))
# linear-by-linear not needed
t2=pd.crosstab(d.sube,d.gecti); O2=t2.values; print(t2)
c2=st.chi2_contingency(O2,correction=False); c2y=st.chi2_contingency(O2,correction=True); print('pearson',c2[:3],'yates',c2y[:2], 'E',c2[3])
lr2=2*(O2*np.log(O2/c2[3])).sum(); print('LR',lr2,st.chi2.sf(lr2,1))
print('fisher',st.fisher_exact(O2), st.fisher_exact(O2,alternative='less'), st.fisher_exact(O2,alternative='greater'))
phi=(O2[0,0]*O2[1,1]-O2[0,1]*O2[1,0])/np.sqrt(np.prod(O2.sum(0))*np.prod(O2.sum(1))); print('phi',phi)
tb=Table2x2(O2); print('OR',tb.oddsratio, tb.oddsratio_confint())
# odds of passing: row1 47/13, row2 34/26
print('odds pass sube1', O2[0,1]/O2[0,0], 'sube2', O2[1,1]/O2[1,0], 'OR pass 1 vs 2', (O2[0,1]/O2[0,0])/(O2[1,1]/O2[1,0]))
# McNemar
a=(d.on_test>=50).astype(int); b=(d.son_test>=50).astype(int); mt=pd.crosstab(a,b); print(mt)
print('mcnemar exact',mcnemar(mt.values,exact=True),'chi2 cc',mcnemar(mt.values,exact=False,correction=True),'nocc',mcnemar(mt.values,exact=False,correction=False))
# small fisher example
F=np.array([[1,9],[6,4]]); print('small',st.fisher_exact(F), st.chi2_contingency(F)[3])
