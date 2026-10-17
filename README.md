# Veriden Karara: Veri Setleri ve Kodlar

Bu depo, *Veriden Karara: SPSS ile Uygulamalı İstatistiksel Analiz* adlı ders kitabında kullanılan veri setlerini, SPSS söz dizimini ve kitaptaki bütün sayısal sonuçları yeniden üreten Python kodlarını içerir. Okur, kitaptaki her tablo, şekil ve örnek sonucunu bu dosyalarla kendi bilgisayarında elde edebilir.

> **Önemli:** Veri setleri öğretim amacıyla **bilgisayar benzetimiyle üretilmiştir**. Gerçek kişilere ait değildir ve hiçbir kişisel veri içermez. Bu verilerden elde edilen sonuçlar gerçek bir evren hakkında bilgi vermez; yalnızca yöntemlerin öğretilmesi içindir.

## İçerik

```
data/
  ogrenci.sav, ogrenci.csv              Ana veri seti (n = 120 öğrenci, 17 değişken)
  kaygi_tekrar.sav, kaygi_tekrar.csv    Tekrarlı ölçümler veri seti (n = 12, 3 ölçüm)
  tutum_olcegi.sav, tutum_olcegi.csv    Faktör analizi veri seti (n = 300, 12 madde)
  kitap_sozdizimi.sps                   Kitaptaki analizlerin SPSS söz dizimi
  SOZLUK.md                             Değişken sözlüğü (adlar, etiketler, kodlar)
kod/
  01_veri_uret.py                       Üç veri setini üretir (tohum değeri sabit)
  fig_b01.py                            Bölüm 1'deki merkezî limit teoremi benzetimi
  b03_betimsel.py ... b14_faktor.py     Bölüm bölüm bütün analizler
  cozumler.py                           Alıştırma çözümlerindeki hesaplamalar
  sonuclar/                             Kodların ekran çıktıları (karşılaştırma için)
figures/data/                           Kitaptaki şekillerin çizildiği sayısal veriler
```

## Veri setleri ve bölümler

| Veri seti | Kullanıldığı bölümler |
|---|---|
| `ogrenci` | 1–4, 6–13 (betimsel istatistik, veri taraması, *t* testleri, ANOVA, MANOVA, ki-kare, korelasyon, regresyon, lojistik regresyon) |
| `kaygi_tekrar` | 6 (eşleştirilmiş *t*), 8 (tekrarlı ölçümler ANOVA, Friedman) |
| `tutum_olcegi` | 14 (açımlayıcı faktör analizi, Cronbach alfa) |

Değişkenlerin ayrıntılı tanımı için [`data/SOZLUK.md`](data/SOZLUK.md) dosyasına bakınız.

## SPSS ile kullanım

1. `data` klasöründeki `.sav` dosyasını SPSS'te açın (**File → Open → Data**). Değişken etiketleri, değer etiketleri ve ölçme düzeyleri tanımlı olarak gelir.
2. Kitaptaki analizleri söz dizimiyle yinelemek için `kitap_sozdizimi.sps` dosyasını açın (**File → Open → Syntax**), dosyanın başındaki `CD` satırını kendi klasörünüze göre düzenleyin ve komutları çalıştırın.

SPSS kullanmayan okurlar `.csv` dosyalarını jamovi, JASP, R ya da Python ile açabilir. Değer kodlarının anlamları `SOZLUK.md` dosyasındadır.

## Sonuçları yeniden üretme (Python)

Kodlar deponun ana klasöründen çalıştırılmalıdır:

```bash
pip install -r requirements.txt
bash calistir.sh
```

`calistir.sh` önce veri setlerini yeniden üretir, ardından bütün analiz kodlarını çalıştırır ve çıktıları `kod/sonuclar/` klasörüne yazar. Veri üretiminde tohum değeri sabit olduğundan aynı kütüphane sürümleriyle birebir aynı veriler elde edilir. Kodlar Python 3.13 ve `requirements.txt` dosyasındaki sürümlerle denenmiştir.

SPSS ile Python arasında yuvarlamadan kaynaklanan son basamak farkları görülebilir. Kitapta SPSS'in varsayılan ayarlarıyla aynı sonucu veren formüller kullanılmıştır (örneğin Tip III kareler toplamı, düzeltilmiş çarpıklık ve basıklık katsayıları, Levene testinin ortalamaya dayalı biçimi).

## Atıf

Bu veri setlerini ya da kodları kullanırsanız lütfen kitaba ve bu depoya atıf yapınız. Atıf bilgileri [`CITATION.cff`](CITATION.cff) dosyasındadır; GitHub sayfasındaki **Cite this repository** düğmesi APA ve BibTeX biçiminde atıf metni üretir.

## Lisans

- Veri setleri ve belgeler (`data/`, `figures/data/`, `kod/sonuclar/`): [Creative Commons Atıf 4.0 Uluslararası (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.tr). Ayrıntı: [`LICENSE-DATA`](LICENSE-DATA).
- Kodlar (`kod/*.py`, `calistir.sh`, `data/kitap_sozdizimi.sps`): [MIT Lisansı](LICENSE).

---

### English summary

Datasets, SPSS syntax and Python code accompanying the Turkish textbook *Veriden Karara: SPSS ile Uygulamalı İstatistiksel Analiz* (From Data to Decision: Applied Statistical Analysis with SPSS). All datasets are **simulated for teaching purposes** and contain no data on real persons. Run `bash calistir.sh` from the repository root to regenerate the data and every numerical result reported in the book. Data are licensed under CC BY 4.0, code under the MIT License.
