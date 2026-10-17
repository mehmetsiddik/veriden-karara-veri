import pandas as pd, numpy as np, scipy.stats as st
d=pd.read_csv('data/ogrenci.csv')
def se_sk(n): return np.sqrt(6*n*(n-1)/((n-2)*(n+1)*(n+3)))
def se_ku(n): return 2*se_sk(n)*np.sqrt((n*n-1)/((n-3)*(n+5)))
def tukey_hinges(x):
    x=np.sort(x); n=len(x); # Tukey hinges
    m=(n+1)//2 if n%2 else n//2
    lo=x[:(n+1)//2]; hi=x[n//2:]
    return np.median(lo), np.median(hi)
print("Betimsel tablo")
for v in ['calisma','devamsizlik','kaygi','on_test','vize','final','proje']:
    x=d[v]; n=len(x)
    q=np.percentile(x,[25,50,75],method='weibull')
    print(v, n, round(x.mean(),2), round(x.std(),2), round(x.median(),2), x.min(), x.max(),
          'sk',round(st.skew(x,bias=False),3), round(se_sk(n),3),'ku', round(st.kurtosis(x,bias=False),3), round(se_ku(n),3),
          'Q',q, 'tm5', round(st.trim_mean(x,0.05),2), 'hinges', tukey_hinges(x))
print(d.basari.value_counts().sort_index(), d.yontem.value_counts().sort_index())
print(d.tercih.value_counts().sort_index())
# final gruplanmış frekans
bins=[10,20,30,40,50,60,70,80,90]
print(pd.cut(d.final,bins=[0,20,30,40,50,60,70,80,90],right=False).value_counts().sort_index())
print(d.final.mode().tolist(), d.final.value_counts().head())
# kutu grafiği yontem bazında
for g,x in d.groupby('yontem').final:
    x=x.values; h=tukey_hinges(x); iqr=h[1]-h[0]
    print(g, 'median',np.median(x),'hinges',h,'min',x.min(),'max',x.max(),'out', x[(x<h[0]-1.5*iqr)|(x>h[1]+1.5*iqr)])
    pd.Series(x).to_csv(f'figures/data/b03_final_yontem{g}.dat',index=False,header=['y'])
# histogram verisi
h,e=np.histogram(d.final,bins=np.arange(10,95,5))
with open('figures/data/b03_final_hist.dat','w') as f:
    f.write('x y\n'); [f.write(f'{a} {b}\n') for a,b in zip(e[:-1],h)]; f.write(f'{e[-1]} 0\n')
print(h, e)
# el hesabı örneği
x=np.array([3,5,6,6,7,8,9,10,18])
print('ornek', x.mean(), np.median(x), st.mode(x), x.std(ddof=1), x.var(ddof=1), np.percentile(x,[25,75],method='weibull'), st.gmean(x), st.hmean(x), st.skew(x,bias=False), st.kurtosis(x,bias=False), np.abs(x-x.mean()).mean(), st.trim_mean(x,0.1))
