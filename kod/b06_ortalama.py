import pandas as pd, numpy as np, scipy.stats as st
d=pd.read_csv('data/ogrenci.csv'); r=pd.read_csv('data/kaygi_tekrar.csv')
def desc(x): return len(x), round(x.mean(),3), round(x.std(),3), round(x.std()/np.sqrt(len(x)),3)
# one-sample
x=d.final; t=st.ttest_1samp(x,50); n=len(x); se=x.std()/np.sqrt(n); tc=st.t.ppf(.975,n-1)
print('1-sample', desc(x), t, x.mean()-50, (x.mean()-50-tc*se, x.mean()-50+tc*se), 'd', (x.mean()-50)/x.std())
# independent: sube
for g in ['sube','cinsiyet']:
    a=d[d[g]==1].final; b=d[d[g]==2].final
    lev=st.levene(a,b,center='mean'); ts=st.ttest_ind(a,b); tw=st.ttest_ind(a,b,equal_var=False)
    sp=np.sqrt(((len(a)-1)*a.var()+(len(b)-1)*b.var())/(len(a)+len(b)-2)); diff=a.mean()-b.mean()
    se_p=sp*np.sqrt(1/len(a)+1/len(b)); se_w=np.sqrt(a.var()/len(a)+b.var()/len(b))
    dfw=(a.var()/len(a)+b.var()/len(b))**2/((a.var()/len(a))**2/(len(a)-1)+(b.var()/len(b))**2/(len(b)-1))
    df=len(a)+len(b)-2
    print(g, desc(a), desc(b), 'lev',lev, 'student',ts, 'welch',tw, 'dfw',dfw, 'diff',diff,'sp',sp,'se',se_p,se_w,
          'CI',(diff-st.t.ppf(.975,df)*se_p, diff+st.t.ppf(.975,df)*se_p), 'CIw', (diff-st.t.ppf(.975,dfw)*se_w, diff+st.t.ppf(.975,dfw)*se_w),'d',diff/sp)
    # Mann-Whitney SPSS style
    allv=pd.concat([a,b]); rk=st.rankdata(allv); ra=rk[:len(a)].sum(); rb=rk[len(a):].sum()
    n1,n2=len(a),len(b); U1=ra-n1*(n1+1)/2; U=min(U1,n1*n2-U1); N=n1+n2
    _,cnt=np.unique(allv,return_counts=True); T=((cnt**3-cnt)).sum()
    sdU=np.sqrt(n1*n2/(N*(N-1))*((N**3-N)/12-T/12)); z=(U-n1*n2/2)/sdU
    print('  MW meanrank',ra/n1, rb/n2,'sumrank',ra,rb,'U',U,'W',min(ra,rb) if U==U1 else rb,'z',z,'p',2*st.norm.sf(abs(z)),'r',abs(z)/np.sqrt(N))
# paired
a=d.son_test; b=d.on_test; dd=a-b; tp=st.ttest_rel(a,b); se=dd.std()/np.sqrt(len(dd)); tc=st.t.ppf(.975,len(dd)-1)
print('paired', desc(a), desc(b), 'dbar',dd.mean(),'sd',dd.std(),'se',se,tp,'CI',(dd.mean()-tc*se,dd.mean()+tc*se),'dz',dd.mean()/dd.std(),'r',np.corrcoef(a,b)[0,1])
# hand paired: kaygi olcum1 vs olcum2
k1=r.olcum1; k2=r.olcum2; dk=k1-k2
print('kaygi', k1.tolist(), k2.tolist(), dk.tolist(), dk.sum(), dk.mean(), dk.std(), (dk**2).sum(), st.ttest_rel(k1,k2), st.t.ppf(.975,11))
# Wilcoxon signed rank SPSS style on k2-k1
def wsr(x,y):
    dif=(y-x).values; dif=dif[dif!=0]; n=len(dif); rk=st.rankdata(np.abs(dif))
    Rp=rk[dif>0].sum(); Rn=rk[dif<0].sum(); npos=(dif>0).sum(); nneg=(dif<0).sum()
    _,c=np.unique(np.abs(dif),return_counts=True); T=(c**3-c).sum()
    var=n*(n+1)*(2*n+1)/24 - T/48; z=(min(Rp,Rn)-n*(n+1)/4)/np.sqrt(var)
    return dict(n=n,npos=npos,nneg=nneg,ties=(len(y)-n),Rp=Rp,Rn=Rn,mrp=Rp/max(npos,1),mrn=Rn/max(nneg,1),z=z,p=2*st.norm.sf(abs(z)))
print('WSR kaygi 2-1', wsr(k1,k2), st.wilcoxon(k1,k2,method='exact'))
print('WSR son-on', wsr(d.on_test,d.son_test))
# one-sample wilcoxon final vs 50
print('1s WSR final-50', wsr(pd.Series(np.full(120,50)), d.final))
print('t crit', st.t.ppf(.975,119), st.t.ppf(.975,118), st.t.ppf(.975,11))
