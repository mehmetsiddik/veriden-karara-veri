* Veriden Karara: SPSS ile Uygulamalı İstatistiksel Analiz - kitap söz dizimi.
* Dosyaların bulunduğu klasörü CD komutuyla belirtiniz: CD 'C:\...\data'.
* ---------- Veri hazırlama (Bölüm 2) ----------.
GET FILE='ogrenci.sav'.
COMPUTE donem_notu = 0.4*vize + 0.6*final.
RECODE donem_notu (LOWEST THRU 44.99=1)(45 THRU 64.99=2)(65 THRU HIGHEST=3)
  INTO basari2.
DESCRIPTIVES VARIABLES=final /SAVE.
COMPUTE Tfinal = 50 + 10*Zfinal.
EXECUTE.

* ---------- Betimsel istatistik ve tarama (Bölüm 3-4) ----------.
FREQUENCIES VARIABLES=basari yontem /BARCHART FREQ.
EXAMINE VARIABLES=final BY yontem
  /PLOT BOXPLOT HISTOGRAM NPPLOT SPREADLEVEL(1)
  /STATISTICS DESCRIPTIVES EXTREME.
REGRESSION /DEPENDENT id /METHOD=ENTER calisma devamsizlik kaygi final
  /SAVE MAHAL.
COMPUTE p_mah = SIG.CHISQ(MAH_1, 4).
EXECUTE.

* ---------- t testleri ve parametrik olmayan karşılıkları (Bölüm 6) ----------.
T-TEST /TESTVAL=50 /VARIABLES=final.
T-TEST GROUPS=sube(1 2) /VARIABLES=final.
T-TEST PAIRS=son_test WITH on_test (PAIRED).
NPAR TESTS /M-W=final BY sube(1 2).
NPAR TESTS /WILCOXON=son_test WITH on_test (PAIRED).

* ---------- Varyans analizi (Bölüm 7-8) ----------.
ONEWAY final BY yontem
  /STATISTICS DESCRIPTIVES HOMOGENEITY BROWNFORSYTHE WELCH
  /POSTHOC=TUKEY GH ALPHA(0.05).
NPAR TESTS /K-W=final BY yontem(1 3).
UNIANOVA final BY yontem sube
  /PLOT=PROFILE(yontem*sube)
  /EMMEANS=TABLES(yontem*sube) COMPARE(sube) ADJ(BONFERRONI)
  /PRINT=DESCRIPTIVE ETASQ HOMOGENEITY
  /DESIGN=yontem sube yontem*sube.
UNIANOVA final BY yontem WITH on_test
  /EMMEANS=TABLES(yontem) WITH(on_test=MEAN) COMPARE ADJ(BONFERRONI)
  /PRINT=ETASQ /DESIGN=on_test yontem.

GET FILE='kaygi_tekrar.sav'.
GLM olcum1 olcum2 olcum3 /WSFACTOR=zaman 3 Polynomial
  /EMMEANS=TABLES(zaman) COMPARE ADJ(BONFERRONI)
  /PRINT=DESCRIPTIVE ETASQ /WSDESIGN=zaman.
NPAR TESTS /FRIEDMAN=olcum1 olcum2 olcum3.

* ---------- MANOVA (Bölüm 9) ----------.
GET FILE='ogrenci.sav'.
GLM vize final proje BY yontem
  /PRINT=DESCRIPTIVE ETASQ HOMOGENEITY
  /DESIGN=yontem.

* ---------- Ki-kare (Bölüm 10) ----------.
NPAR TESTS /CHISQUARE=tercih /EXPECTED=EQUAL.
CROSSTABS /TABLES=yontem BY gecti
  /STATISTICS=CHISQ PHI /CELLS=COUNT EXPECTED ROW ASRESID.
CROSSTABS /TABLES=sube BY gecti /STATISTICS=CHISQ PHI RISK.

* ---------- Korelasyon ve regresyon (Bölüm 11-12) ----------.
CORRELATIONS /VARIABLES=calisma devamsizlik kaygi on_test final.
NONPAR CORR /VARIABLES=calisma final /PRINT=BOTH TWOTAIL.
PARTIAL CORR /VARIABLES=kaygi final BY calisma.
REGRESSION /STATISTICS COEFF OUTS CI(95) R ANOVA CHANGE ZPP COLLIN TOL
  /DEPENDENT final
  /METHOD=ENTER on_test
  /METHOD=ENTER calisma devamsizlik kaygi
  /SCATTERPLOT=(*ZRESID, *ZPRED)
  /RESIDUALS DURBIN HISTOGRAM(ZRESID)
  /SAVE ZRESID SDRESID COOK LEVER MAHAL SDBETA COVRATIO.

* ---------- Lojistik regresyon (Bölüm 13) ----------.
LOGISTIC REGRESSION VARIABLES gecti
  /METHOD=ENTER calisma devamsizlik kaygi sube
  /CONTRAST (sube)=Indicator
  /PRINT=GOODFIT CI(95) /CRITERIA=CUT(0.5).
PLUM basari WITH calisma devamsizlik
  /LINK=LOGIT /PRINT=FIT PARAMETER SUMMARY TPARALLEL.
NOMREG tercih (BASE=FIRST ORDER=ASCENDING) BY sube WITH calisma
  /PRINT=PARAMETER SUMMARY LRT CLASSTABLE.

* ---------- Faktör analizi ve güvenirlik (Bölüm 14) ----------.
GET FILE='tutum_olcegi.sav'.
FACTOR /VARIABLES m1 TO m12
  /PRINT INITIAL KMO AIC EXTRACTION ROTATION
  /FORMAT SORT BLANK(.30) /PLOT EIGEN
  /CRITERIA FACTORS(3) ITERATE(25)
  /EXTRACTION PAF /ROTATION PROMAX(4).
RELIABILITY /VARIABLES=m1 m2 m3 m4 /SCALE('Kaygı') ALL
  /MODEL=ALPHA /SUMMARY=TOTAL.
