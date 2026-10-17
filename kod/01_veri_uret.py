# -*- coding: utf-8 -*-
"""
Kitapta kullanılan kurgusal (simülasyonla üretilmiş) veri setlerini üretir.
Veriler gerçek kişilere ait değildir; yalnızca öğretim amaçlıdır.
Çalıştırma: python3 01_veri_uret.py  (çıktılar ../data klasörüne yazılır)
"""
import numpy as np
import pandas as pd
import pyreadstat
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------
# 1) ogrenci: ana veri seti (n = 120)
# ---------------------------------------------------------------
rng = np.random.default_rng(2026)
n = 120
# yöntem x şube dengeli desen: her hücrede 20 öğrenci
yontem = np.repeat([1, 2, 3], 40)
sube = np.tile(np.repeat([1, 2], 20), 3)
perm = rng.permutation(n)
yontem, sube = yontem[perm], sube[perm]
cinsiyet = rng.choice([1, 2], size=n)
yas = np.clip(np.round(rng.normal(21.2, 1.4, n)), 19, 26).astype(int)
calisma = np.clip(np.round(rng.normal(6.5, 2.8, n)), 0, 15).astype(int)
dev_lat = 2.4 - 0.18 * (calisma - 6.5) + rng.normal(0, 1.5, n)
devamsizlik = np.clip(np.round(dev_lat), 0, 8).astype(int)
kaygi = np.clip(np.round(50 - 1.3 * (calisma - 6.5) + rng.normal(0, 9, n)), 20, 80).astype(int)
on_test = np.clip(np.round(rng.normal(45, 10, n)), 10, 90).astype(int)

eff_y = np.select([yontem == 1, yontem == 2, yontem == 3], [0.0, 8.0, 0.0])
eff_s = np.where(sube == 2, -2.0, 0.0)
eff_int = np.where((yontem == 3) & (sube == 2), -8.0, 0.0)
final_lat = (34 + 0.40 * on_test + 2.6 * calisma - 2.4 * devamsizlik
             - 0.18 * kaygi + eff_y + eff_s + eff_int + rng.normal(0, 8, n))
final = np.clip(np.round(final_lat), 0, 100).astype(int)

son_test = np.clip(np.round(on_test + 7 + 0.8 * calisma + rng.normal(0, 6, n)), 0, 100).astype(int)
vize = np.clip(np.round(0.55 * final + 0.30 * on_test + 14 + rng.normal(0, 7, n)), 0, 100).astype(int)
proje = np.clip(np.round(55 + 0.30 * (final - final.mean()) + np.select(
    [yontem == 1, yontem == 2, yontem == 3], [0, 9, 2]) + rng.normal(0, 8, n)), 0, 100).astype(int)

# Planlı aykırı gözlem: sınav günü rahatsızlanan öğrenci (bkz. Bölüm 4 ve 12)
idx_out = 56  # id = 57
calisma[idx_out] = 12
devamsizlik[idx_out] = 0
final[idx_out] = 18

donem_notu = np.round(0.4 * vize + 0.6 * final, 1)
gecti = (donem_notu >= 50).astype(int)
basari = np.select([donem_notu < 45, donem_notu < 65], [1, 2], default=3)

# mezuniyet sonrası tercih (çok kategorili): 1 = iş, 2 = yüksek lisans, 3 = kararsız
eta_yl = -2.2 + 0.30 * calisma + 0.6 * (sube == 1)
eta_ka = 0.3 - 0.10 * calisma
P = np.column_stack([np.ones(n), np.exp(eta_yl), np.exp(eta_ka)])
P = P / P.sum(1, keepdims=True)
tercih = np.array([rng.choice([1, 2, 3], p=p) for p in P])

ogr = pd.DataFrame(dict(
    id=np.arange(1, n + 1), cinsiyet=cinsiyet, yas=yas, yontem=yontem, sube=sube,
    calisma=calisma, devamsizlik=devamsizlik, kaygi=kaygi, on_test=on_test,
    son_test=son_test, vize=vize, final=final, proje=proje,
    donem_notu=donem_notu, gecti=gecti, basari=basari, tercih=tercih))

lab_var = dict(id="Öğrenci numarası", cinsiyet="Cinsiyet", yas="Yaş (yıl)",
               yontem="Öğretim yöntemi", sube="Şube", calisma="Haftalık çalışma süresi (saat)",
               devamsizlik="Devamsızlık (hafta)", kaygi="Sınav kaygısı puanı (20-80)",
               on_test="Dönem başı başarı testi", son_test="Dönem sonu başarı testi",
               vize="Ara sınav notu", final="Final sınavı notu", proje="Proje notu",
               donem_notu="Dönem notu (0,4 vize + 0,6 final)", gecti="Dersi geçme durumu",
               basari="Başarı düzeyi", tercih="Mezuniyet sonrası tercih")
lab_val = dict(cinsiyet={1: "Kadın", 2: "Erkek"},
               yontem={1: "Geleneksel", 2: "Proje tabanlı", 3: "Çevrim içi"},
               sube={1: "Birinci öğretim", 2: "İkinci öğretim"},
               gecti={0: "Kaldı", 1: "Geçti"},
               basari={1: "Düşük", 2: "Orta", 3: "Yüksek"},
               tercih={1: "İş", 2: "Yüksek lisans", 3: "Kararsız"})
measure = {v: "scale" for v in ogr.columns}
for v in ["cinsiyet", "yontem", "sube", "gecti", "tercih"]:
    measure[v] = "nominal"
measure["basari"] = "ordinal"
measure["id"] = "nominal"
ogr.to_csv(OUT / "ogrenci.csv", index=False)
pyreadstat.write_sav(ogr, OUT / "ogrenci.sav", column_labels=lab_var,
                     variable_value_labels=lab_val, variable_measure=measure)

# ---------------------------------------------------------------
# 2) kaygi_tekrar: tekrarlı ölçümler (n = 12, üç zaman)
# ---------------------------------------------------------------
rng2 = np.random.default_rng(77)
m = 12
kisi = rng2.normal(0, 6, m)
t1 = np.round(58 + kisi + rng2.normal(0, 3, m)).astype(int)
t2 = np.round(52 + kisi + rng2.normal(0, 3.5, m)).astype(int)
t3 = np.round(49 + kisi + rng2.normal(0, 4.5, m)).astype(int)
rm = pd.DataFrame(dict(katilimci=np.arange(1, m + 1), olcum1=t1, olcum2=t2, olcum3=t3))
rm.to_csv(OUT / "kaygi_tekrar.csv", index=False)
pyreadstat.write_sav(rm, OUT / "kaygi_tekrar.sav",
                     column_labels=dict(katilimci="Katılımcı", olcum1="Program öncesi kaygı",
                                        olcum2="1. ay kaygı", olcum3="3. ay kaygı"))

# ---------------------------------------------------------------
# 3) tutum_olcegi: faktör analizi (n = 300, 12 madde, 1-5 Likert)
# ---------------------------------------------------------------
rng3 = np.random.default_rng(31)
N = 300
Phi = np.array([[1.0, -0.35, -0.30], [-0.35, 1.0, 0.40], [-0.30, 0.40, 1.0]])
F = rng3.multivariate_normal(np.zeros(3), Phi, N)
L = np.zeros((12, 3))
L[0:4, 0] = [0.78, 0.74, 0.70, 0.66]      # Kaygı
L[4:8, 1] = [0.80, 0.75, 0.68, 0.62]      # İlgi
L[8:12, 2] = [0.76, 0.72, 0.67, 0.58]     # Öz-yeterlik
L[7, 2] = 0.22                            # hafif çapraz yük
uniq = np.sqrt(1 - (L ** 2).sum(1) - 2 * L[:, 1] * L[:, 2] * 0.40 * (np.arange(12) == 7))
X = F @ L.T + rng3.normal(0, 1, (N, 12)) * uniq
cuts = [-1.3, -0.45, 0.35, 1.15]
items = np.digitize(X, cuts) + 1
cols = [f"m{i}" for i in range(1, 13)]
tut = pd.DataFrame(items, columns=cols)
tut.insert(0, "katilimci", np.arange(1, N + 1))
madde = {
    "m1": "İstatistik sınavlarından önce gerginlik hissederim.",
    "m2": "İstatistik formüllerini görünce zihnim bulanıklaşır.",
    "m3": "İstatistik dersinde soru sormaktan çekinirim.",
    "m4": "Bir analiz sonucunu yorumlamam gerektiğinde endişelenirim.",
    "m5": "İstatistiğin günlük hayattaki kullanımı ilgimi çeker.",
    "m6": "Yeni bir analiz yöntemi öğrenmekten keyif alırım.",
    "m7": "Veriyle ilgili haberleri merakla okurum.",
    "m8": "Ders dışında da istatistikle ilgili içerikleri incelerim.",
    "m9": "Bir veri setini SPSS'te kendi başıma çözümleyebilirim.",
    "m10": "Uygun istatistiksel testi seçebileceğime inanırım.",
    "m11": "Analiz çıktısındaki temel değerleri doğru okuyabilirim.",
    "m12": "Karşılaştığım istatistik problemlerini çözebilirim.",
}
tut.to_csv(OUT / "tutum_olcegi.csv", index=False)
pyreadstat.write_sav(tut, OUT / "tutum_olcegi.sav",
                     column_labels=dict(katilimci="Katılımcı", **madde),
                     variable_value_labels={c: {1: "Kesinlikle katılmıyorum", 2: "Katılmıyorum",
                                                3: "Kararsızım", 4: "Katılıyorum",
                                                5: "Kesinlikle katılıyorum"} for c in cols},
                     variable_measure={**{c: "ordinal" for c in cols}, "katilimci": "nominal"})
print(ogr.describe().T.round(2))
print(rm)
print(tut.describe().T.round(2))
